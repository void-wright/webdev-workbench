/**
 * The scroll journey's controller (src/components/ScrollJourney.astro). No WebGL, no dependencies. The component's
 * small waker imports it when the journey comes within a screen and a half, so a reader who never scrolls that far
 * never downloads it. It ports the method of the upstream sn-motion-html motion runtime (MIT; see VENDOR_NOTE.md):
 * one stage, a tall track, stops held on their stills, passages scrubbed. On top of that method it carries these
 * player fixes:
 *   - the route is bands: hold S0, P1, hold S1, ... , the last stop's hold; any number of stops (two or more); the band
 *     lengths come from the CSS constants --sj-hold / --sj-pass / --sj-end (in screens) times each stop's own
 *     data-hold, and ?hold= and ?pass= override them live for tuning;
 *   - a passage's local progress drives its clip's currentTime through a TIME-BASED lerp, so 60 Hz and 120 Hz screens
 *     and throttled tabs feel the same;
 *   - only the current and the next passage are fetched; every other clip is released (src removed, element dropped),
 *     because memory otherwise grows until a phone browser kills the tab;
 *   - a clip is shown only once a frame is truly painted (requestVideoFrameCallback where there is one); a clip that
 *     fails, or is not painted yet, leaves the two stills to crossfade, so the journey is never blank;
 *   - every clip is primed (play, then pause) once a gesture has happened, including clips made after it (iOS needs a
 *     gesture before a muted video will seek and paint reliably);
 *   - the reader's place is kept through resize, rotation and the wide/portrait flip (a narrowed desktop tab flips live);
 *   - rail jumps and the skip link are instant, so no download burst runs through the passages in between; focus on a
 *     hidden stop's link brings that stop into view; Esc clears a door preview;
 *   - the motion pause (<html data-motion="paused">), reduced motion and Save-Data: every clip is paused and released,
 *     the stills crossfade, nothing is fetched (whatever ?journey= says).
 * Which clips (the tier): portrait screens take the 9:16 passages; landscape takes 720p, or 1080p from 1600 CSS px wide
 * at devicePixelRatio >= 1.5. ?journey=720 and ?journey=1080 force a landscape tier; ?journey=stills gives the stills
 * crossfade everywhere. Re-decided live.
 * A journey whose words cannot sit whole in the pinned screen (the component's fit test, data-sj-stack, tested again
 * here on wake, on resize and once the web fonts have loaded) is laid out stacked, as without script: the controller
 * then shows nothing and fetches nothing.
 * State for tests, on the root: data-sj-ready, data-sj-mode (the tier or 'stills'), data-sj-band ('hold-2', 'pass-1'),
 * data-sj-stop, data-sj-clips (passages with an element), data-sj-shown (the passage whose clip is shown, or '').
 * No words, colours or storage here.
 */
type Band = { kind: 'hold' | 'pass'; i: number; units: number; start: number; end: number };
type Clip = { v: HTMLVideoElement; tier: string; ready: boolean; painted: boolean; failed: boolean; cur: number; target: number };

const clamp = (x: number, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const smooth = (x: number) => {
  const t = clamp(x);
  return t * t * (3 - 2 * t);
};

export function wake(root: HTMLElement): void {
  if (root.dataset.sjWoken !== undefined) return;
  root.dataset.sjWoken = '';
  const sticky = root.querySelector<HTMLElement>('.sj-sticky');
  const track = root.querySelector<HTMLElement>('.sj-track');
  const media = root.querySelector<HTMLElement>('[data-sj-media]');
  const stops = [...root.querySelectorAll<HTMLElement>('.sj-stop')];
  if (!sticky || !track || !media || stops.length < 2) return;
  const PASSAGES = stops.length - 1;
  const holdOf = stops.map((s) => {
    const h = Number(s.dataset.hold);
    return Number.isFinite(h) && h > 0 ? h : 1;
  });
  const stills = stops.map((s) => s.querySelector<HTMLElement>('.sj-still'));
  const copies = stops.map((s) => s.querySelector<HTMLElement>('.sj-copy'));
  const doors = stops.map((s) => s.querySelector<HTMLElement>('.sj-doorbox'));
  const links = stops.map((s) => s.querySelector<HTMLElement>('.sj-door'));
  const marks = [...root.querySelectorAll<HTMLAnchorElement>('[data-rail]')];
  const clipUrl = root.dataset.sjClips || '';
  const html = document.documentElement;
  const PORTRAIT = matchMedia(root.dataset.sjPortrait || '(max-aspect-ratio: 1/1)');
  const REDUCE = matchMedia('(prefers-reduced-motion: reduce)');
  const FINE = matchMedia('(hover: hover) and (pointer: fine)');
  const saveData = (navigator as Navigator & { connection?: { saveData?: boolean } }).connection?.saveData === true;
  const q = new URLSearchParams(location.search);
  const want = (q.get('journey') || '').toLowerCase();
  // live tuning: ?hold=1.4&pass=1.6 (screens), bounded
  for (const [k, name] of [['hold', '--sj-hold'], ['pass', '--sj-pass']] as const) {
    const v = Number(q.get(k));
    if (q.has(k) && Number.isFinite(v) && v >= 0.3 && v <= 5) root.style.setProperty(name, String(v));
  }

  /** the clips to scrub now, or null for the stills */
  const tierNow = (): string | null => {
    if (REDUCE.matches || saveData || html.dataset.motion === 'paused' || want === 'stills') return null;
    if (PORTRAIT.matches) return '9x16';
    if (want === '720') return '16x9';
    if (want === '1080') return '16x9-1080';
    return innerWidth >= 1600 && devicePixelRatio >= 1.5 ? '16x9-1080' : '16x9';
  };
  let tier = tierNow();

  // ---- the route -----------------------------------------------------------------------------------------------------
  let bands: Band[] = [];
  let total = 1;
  let unit = 1; // px per screen-unit of the track
  let span = 1; // the track's pinned scroll, px
  const num = (name: string, d: number) => {
    const v = parseFloat(getComputedStyle(root).getPropertyValue(name));
    return Number.isFinite(v) && v > 0 ? v : d;
  };
  function layout(): void {
    const hold = num('--sj-hold', 1);
    const pass = num('--sj-pass', 1.2);
    const end = num('--sj-end', 1);
    const units: [Band['kind'], number, number][] = [];
    for (let i = 0; i <= PASSAGES; i++) {
      units.push(['hold', i, (i === PASSAGES ? end : hold) * holdOf[i]]);
      if (i < PASSAGES) units.push(['pass', i, pass]);
    }
    total = units.reduce((n, u) => n + u[2], 0);
    span = track!.offsetHeight;
    unit = span / total;
    let at = 0;
    bands = units.map(([kind, i, u]) => {
      const b = { kind, i, units: u, start: at * unit, end: (at + u) * unit };
      at += u;
      return b;
    });
  }
  /** the stage's container top in page px (the sticky stage pins from here for `span` px) */
  const coreTop = () => sticky!.parentElement!.getBoundingClientRect().top + scrollY;
  const yNow = () => clamp(-root.getBoundingClientRect().top, 0, span);
  /** the scroll position (page px) that shows stop i's hold, at a share of it */
  const holdY = (i: number, at = 0.35) => {
    const b = bands.find((x) => x.kind === 'hold' && x.i === i);
    return b ? coreTop() + b.start + (b.end - b.start) * at : coreTop();
  };

  // ---- the clips -------------------------------------------------------------------------------------------------------
  const clips: (Clip | null)[] = Array.from({ length: PASSAGES }, () => null);
  let gestured = false;
  const prime = (v: HTMLVideoElement) => {
    const p = v.play();
    if (p && p.then) p.then(() => v.pause()).catch(() => {});
  };
  function release(k: number): void {
    const c = clips[k];
    if (!c) return;
    c.v.pause();
    c.v.removeAttribute('src');
    c.v.load();
    c.v.remove();
    clips[k] = null;
  }
  function ensure(k: number): void {
    if (!tier || k < 0 || k >= PASSAGES) return;
    const have = clips[k];
    if (have && have.tier === tier) return;
    release(k);
    const v = document.createElement('video');
    v.muted = true;
    v.defaultMuted = true;
    v.playsInline = true;
    v.setAttribute('muted', '');
    v.setAttribute('playsinline', '');
    v.setAttribute('disableremoteplayback', '');
    v.setAttribute('aria-hidden', 'true');
    v.preload = 'auto';
    v.dataset.passage = String(k + 1);
    const c: Clip = { v, tier, ready: false, painted: false, failed: false, cur: 0, target: 0 };
    v.addEventListener('loadedmetadata', () => {
      c.ready = true;
      kick();
    });
    v.addEventListener('error', () => {
      c.failed = true;
      v.removeAttribute('data-on');
    });
    v.addEventListener('seeked', () => {
      const r = v as HTMLVideoElement & { requestVideoFrameCallback?: (cb: () => void) => number };
      if (r.requestVideoFrameCallback) r.requestVideoFrameCallback(() => (c.painted = true));
      else c.painted = true;
      kick();
    });
    v.src = clipUrl.replace('{n}', String(k + 1)).replace('{tier}', tier);
    media!.appendChild(v);
    clips[k] = c;
    if (gestured) prime(v);
  }
  function fetchFor(b: Band): void {
    // the current passage and the next: a hold looks ahead to its own passage and the one after it
    const keep = new Set([b.i, b.i + 1]);
    for (let k = 0; k < PASSAGES; k++) {
      if (tier && armed && !stacked && keep.has(k)) ensure(k);
      else release(k);
    }
    root.dataset.sjClips = clips
      .map((c, k) => (c ? k + 1 : 0))
      .filter(Boolean)
      .join(',');
  }
  const onGesture = () => {
    if (gestured) return;
    gestured = true;
    for (const c of clips) if (c) prime(c.v);
  };
  for (const ev of ['pointerdown', 'touchstart', 'keydown'] as const) addEventListener(ev, onGesture, { once: true, passive: true });

  // ---- the fit: stacked when any stop's words leave the pinned screen ------------------------------------------------
  let stacked = root.hasAttribute('data-sj-stack');
  const FIT = root.hasAttribute('data-sj-fit');
  function refit(): void {
    if (!FIT) return;
    root.removeAttribute('data-sj-stack');
    let out = false;
    if (getComputedStyle(sticky!).position === 'sticky') {
      const top = sticky!.getBoundingClientRect().top;
      const head = parseFloat(getComputedStyle(root).getPropertyValue('--sj-head')) || 0;
      for (const c of copies) {
        if (!c) continue;
        const r = c.getBoundingClientRect();
        if (r.top - top < head + 8 || r.bottom - top > sticky!.offsetHeight - 8) out = true;
      }
    }
    root.toggleAttribute('data-sj-stack', out);
    if (out === stacked) return;
    stacked = out;
    if (stacked) {
      // the stacked layout is CSS's: hand every inline style back and fetch nothing
      for (let k = 0; k < PASSAGES; k++) release(k);
      for (const el of [...stills, ...copies, ...doors, ...links]) {
        el?.style.removeProperty('opacity');
        el?.style.removeProperty('pointer-events');
      }
    }
  }

  // ---- the frame -------------------------------------------------------------------------------------------------------
  let active = -1;
  let armed = false;
  let share = -1; // the reader's place as a share of the pinned journey (-1: outside it)
  let bandKey = '';
  let near = false;
  let raf = 0;
  let last = 0;
  const op = (el: HTMLElement | null, v: number) => {
    if (!el) return;
    const s = v > 0.999 ? '1' : v < 0.001 ? '0' : v.toFixed(3);
    if (el.style.opacity !== s) el.style.opacity = s;
  };
  const live = (el: HTMLElement | null, on: boolean) => {
    if (!el) return;
    const s = on ? '' : 'none';
    if (el.style.pointerEvents !== s) el.style.pointerEvents = s;
  };
  function frame(now: number): void {
    raf = 0;
    if (stacked) return;
    const dt = last ? Math.min(0.1, (now - last) / 1000) : 0.016;
    last = now;
    const y = yNow();
    share = y > 0 && y < span ? y / span : -1;
    const b = bands.find((x) => y < x.end) || bands[bands.length - 1];
    const u = clamp((y - b.start) / Math.max(1, b.end - b.start));
    // no clip is fetched until the page has loaded and the journey's top has passed the middle of the screen, so the
    // page's own first paint stays first and a reader who never scrolls this far never pays for a passage
    const on = document.readyState === 'complete' && root.getBoundingClientRect().top < innerHeight * 0.5;
    const key = `${b.kind}-${b.i}${on ? '' : '-idle'}`;
    armed = on;
    if (key !== bandKey) {
      bandKey = key;
      root.dataset.sjBand = `${b.kind}-${b.i}`;
      fetchFor(b);
    }
    // what each stop shows: its still, its words (and its door)
    const still: number[] = new Array(PASSAGES + 1).fill(0);
    const words: number[] = new Array(PASSAGES + 1).fill(0);
    let shown = -1;
    if (b.kind === 'hold') {
      still[b.i] = 1;
      words[b.i] = 1;
    } else {
      const k = b.i;
      // the outgoing words leave in the first tenth of the passage; the incoming ones settle in its last sixth
      words[k] = 1 - smooth(u / 0.1);
      words[k + 1] = smooth((u - 0.85) / 0.15);
      const c = clips[k];
      if (c && c.ready && !c.failed) {
        // eased scrub: gentle at both ends of the passage, over the clip's own duration
        const e = 0.5 * u + 0.5 * smooth(u);
        c.target = e * Math.max(0, (c.v.duration || 0) - 0.04);
      }
      if (c && c.painted && !c.failed) {
        shown = k;
        still[u < 0.5 ? k : k + 1] = 1;
      } else {
        // the stills crossfade (no clip, a clip not painted yet, or a failed one)
        still[k] = 1;
        still[k + 1] = smooth((u - 0.2) / 0.6);
      }
    }
    const top = b.kind === 'hold' ? b.i : words[b.i + 1] > words[b.i] ? b.i + 1 : b.i;
    for (let i = 0; i <= PASSAGES; i++) {
      op(stills[i], still[i]);
      op(copies[i], words[i]);
      op(doors[i], words[i]);
      live(copies[i], words[i] > 0.5);
      live(links[i], words[i] > 0.5);
    }
    if (top !== active) {
      active = top;
      root.dataset.sjStop = String(top);
      marks.forEach((m, i) => (i === top ? m.setAttribute('aria-current', 'step') : m.removeAttribute('aria-current')));
      // touch: a door's glow swells once as its stop arrives (there is no hover to reveal it)
      if (!FINE.matches && !REDUCE.matches) {
        const d = stops[top].querySelector<HTMLElement>('.sj-door');
        if (d) {
          d.removeAttribute('data-wake');
          void d.offsetWidth;
          d.setAttribute('data-wake', '');
        }
      }
    }
    // the clips: only the shown one is visible; it chases its target in time, not in frames
    let moving = false;
    const ke = 1 - Math.exp(-dt / 0.09);
    clips.forEach((c, k) => {
      if (!c) return;
      const vis = k === shown;
      if (vis !== c.v.hasAttribute('data-on')) c.v.toggleAttribute('data-on', vis);
      if (k !== b.i || !c.ready || c.failed) return;
      // coalesced seeks: one at a time; the next waits for 'seeked'
      c.cur += (c.target - c.cur) * ke;
      if (Math.abs(c.target - c.cur) < 0.004) c.cur = c.target;
      else moving = true;
      if (!c.v.seeking && Math.abs(c.v.currentTime - c.cur) > 0.02) c.v.currentTime = c.cur;
      else if (!c.painted && !c.v.seeking && c.v.readyState >= 2 && c.v.currentTime === 0) c.v.currentTime = 0.001;
    });
    root.dataset.sjShown = shown >= 0 ? String(shown + 1) : '';
    // the stops' inline opacities are set: the CSS default (the first stop only) steps aside
    if (root.dataset.sjReady === undefined) root.dataset.sjReady = '';
    if (moving) kick();
  }
  function kick(): void {
    if (!raf && near) raf = requestAnimationFrame(frame);
  }

  // ---- re-deciding: the tier, the layout, the place -------------------------------------------------------------------
  function retier(): void {
    const t = tierNow();
    root.dataset.sjMode = t || 'stills';
    if (t === tier) return;
    tier = t;
    for (let k = 0; k < PASSAGES; k++) release(k);
    bandKey = '';
    kick();
  }
  let relayRaf = 0;
  let lastW = innerWidth;
  let lastH = innerHeight;
  function relay(): void {
    cancelAnimationFrame(relayRaf);
    relayRaf = requestAnimationFrame(() => {
      // a phone's URL bar showing and hiding changes only the height a little: the svh track does not move
      if (innerWidth === lastW && Math.abs(innerHeight - lastH) < 80) return;
      lastW = innerWidth;
      lastH = innerHeight;
      // keep the reader's place: the same share of the journey (as last drawn) after the re-layout
      const place = share;
      refit();
      layout();
      if (place > 0) scrollTo({ top: coreTop() + place * span, behavior: 'instant' as ScrollBehavior });
      retier();
      bandKey = '';
      kick();
    });
  }

  // ---- wiring ----------------------------------------------------------------------------------------------------------
  // the fit again now, and once the web fonts are in: the parse-time test may have measured the fallback face, which
  // usually sets the words shorter, so a long stop can pass at parse and overflow once the real font arrives
  refit();
  document.fonts?.ready.then(() => {
    refit();
    layout();
    bandKey = '';
    kick();
  });
  layout();
  retier();
  addEventListener('scroll', kick, { passive: true });
  addEventListener('resize', relay, { passive: true });
  PORTRAIT.addEventListener('change', relay);
  REDUCE.addEventListener('change', retier);
  new MutationObserver(retier).observe(html, { attributes: true, attributeFilter: ['data-motion'] });
  new IntersectionObserver(
    (es) => {
      near = es.some((e) => e.isIntersecting);
      if (near) kick();
      else for (const c of clips) c?.v.pause();
    },
    { rootMargin: '100% 0px' },
  ).observe(root);
  // the rail: an instant jump to the stop's hold (no smooth travel through the passages between, so nothing between is
  // fetched)
  for (const m of marks) {
    m.addEventListener('click', (e) => {
      e.preventDefault();
      scrollTo({ top: holdY(Number(m.dataset.rail)), behavior: 'instant' as ScrollBehavior });
    });
  }
  // "Skip the journey": an instant jump to the START of the last stop's hold (its words whole and settled, nothing
  // between fetched), then focus on those words (tabindex -1), so keyboard and screen-reader users land there too
  const skip = root.querySelector<HTMLAnchorElement>('.sj-skip');
  const lastWords = stops[PASSAGES].querySelector<HTMLElement>('.sj-copy');
  skip?.addEventListener('click', (e) => {
    e.preventDefault();
    scrollTo({ top: holdY(PASSAGES, 0.02), behavior: 'instant' as ScrollBehavior });
    lastWords?.focus({ preventScroll: true });
  });
  // focus inside a stop that is not shown (a keyboard reaching its door) brings that stop's hold into view
  root.addEventListener('focusin', (e) => {
    const s = (e.target as HTMLElement).closest<HTMLElement>('.sj-stop');
    if (!s) return;
    s.removeAttribute('data-esc');
    // the skip link's own landing (the words block itself) has already placed the reader
    if ((e.target as HTMLElement).classList.contains('sj-copy')) return;
    const i = Number(s.dataset.stop);
    if (i !== active || bandKey.startsWith('pass')) scrollTo({ top: holdY(i, 0.5), behavior: 'instant' as ScrollBehavior });
  });
  root.addEventListener('pointerover', (e) => {
    (e.target as HTMLElement).closest<HTMLElement>('.sj-stop')?.removeAttribute('data-esc');
  });
  // Esc clears a door preview (the pointer hint names it)
  addEventListener('keydown', (e) => {
    if (e.key !== 'Escape' || active < 0) return;
    stops[active].setAttribute('data-esc', '');
  });
  near = root.getBoundingClientRect().top < innerHeight * 2;
  if (document.readyState !== 'complete') addEventListener('load', kick, { once: true });
  kick();
}
