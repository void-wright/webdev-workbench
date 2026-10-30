# Phones

Most mobile misses come from checking one emulated size. The method below is cheap, and each miss it prevents costs the human a session on their own phone.

## What a phone gets

- **Portrait screens take the 9:16 passages by default** (tier `9x16`, encoded at 720 x 1280). They looked good enough on real phones to lead with; `?journey=stills` on the URL swaps in the stills crossfade for comparison. Portrait means `(max-aspect-ratio: 1/1)`; a desktop window narrowed past square flips live, keeping the reader's place.
- **The phone stills** are their own compositions (forms in the top third, calm lower part for words), not a crop of the wide still.
- **Holds and passages** use the same screen-height units as desktop. A phone screen is short, so a hold of 1 screen is a short scroll; tune with `?hold=` and `?pass=` on the real device before changing the CSS.
- **Reduced motion, Save-Data and the pause** give the stills crossfade and fetch nothing, on phones as everywhere.

## The browser's own bars

A phone browser's toolbars (for example a floating bottom bar) cover the foot of a pinned `100svh` stage, and **an emulator never shows them**. Words anchored to the stage's foot can sit under that bar on a real phone while every emulated size passes, and the reader then has to scroll inside a hold to read one stop. A pale strip a tester reports at the foot of the screen is usually the browser's own toolbar, not the page.

The component lifts the words clear of that strip on portrait screens:

```css
--sj-bar: clamp(2.5rem, 10svh - 1rem, 5.5rem);   /* scaled with the screen's height */
.sj-copy { bottom: calc(max(0.75rem, 2.5cqh) + var(--sj-bar)); }
```

It also sets the type a little tighter on portrait screens and hides the tap hint below 46rem of height (the door's name and glow already say it). A fixed-height bar can overlap the labels on short phones, which is why the bar scales with `svh`.

Use `svh` for pinned stages: the small viewport height is the always-visible height. `dvh` changes as the bars show and hide, and jolts anything sized by it mid-scroll. The controller also ignores height-only resizes under 80 px, which is what a URL bar showing and hiding looks like.

If your site has its own pinned header, set `--sj-head` to its height on the `.sj` element (per breakpoint if it changes). The words, the skip link and the pause button keep clear of it, and the fit test counts it.

## The five-size battery

Measure at **360 x 640, 375 x 667, 390 x 664 (a phone with its bars showing), 390 x 844 and 430 x 932**, plus one desktop size. Per stop, check:

1. the words box sits inside the stage, below `--sj-head` and above the `--sj-bar` strip;
2. the whole stop is readable without scrolling inside its hold;
3. no words box overlaps a door's name label;
4. the journey did not stack itself (or, if it did, that stacking was intended);
5. scrubbing top to bottom shows each passage's clip, and never keeps more than two clip elements alive.

The skill's `scripts/journey_battery.mjs` (shipped at `03_skills/scroll-journey/scripts/journey_battery.mjs` in the package) does all five, in numbers. From the site folder (Playwright installed there once):

```bash
npm i -D playwright
npx playwright install chromium
npm run build
npx astro preview --port 4321
```

Astro's preview may detach and keep running in the background (`npx astro preview stop` ends it, as of October 2026; re-check). In a second terminal, from the same folder, with `SJ` set to the skill's `scripts` folder as in `SKILL.md`:

```bash
SJ="$HOME/.claude/skills/scroll-journey/scripts"   # the installed skill; from the unzipped package use 03_skills/scroll-journey/scripts
node "$SJ/journey_battery.mjs" http://localhost:4321/seed-library/ --json battery.json > battery.log 2>&1; echo "rc=$?"
cat battery.log
```

A passing run ends `PASS: every stop fits at every size` with `rc=0`. Each row reads like `390x664 mode=9x16 S0:ok(448-597/664) ...`: the words' top and bottom in px against the stage height, then `shown=[1,2,3] max_clips=2` from the scrub pass. `OUT` marks a stop that leaves its bounds; `LABEL` marks a words box over a door label.

Two artifacts to know: Chromium's emulation reports a fine pointer unless the context is a touch context (the battery uses touch contexts for portrait sizes, so the touch hint is the one measured); and the first stop's hold can begin before the stage pins, so measure stops after jumping through the rail (the battery does) rather than at the page's natural scroll position.

## Tuning by injected CSS, before touching the source

To fix a phone layout, try candidate CSS on the built page at every size first, and edit the component only once every size passes. Put the candidate rules in a file:

```bash
cat > candidate.css <<'CSS'
@media (max-aspect-ratio: 1/1) {
  .sj { --sj-bar: clamp(3rem, 11svh - 1rem, 6rem); }
  .sj-body { font-size: 0.9rem; }
}
CSS
node "$SJ/journey_battery.mjs" http://localhost:4321/seed-library/ --css candidate.css > battery_candidate.log 2>&1; echo "rc=$?"
cat battery_candidate.log
```

The battery adds the file as a `<style>` in the page's head before measuring. It works on a deployed preview URL too, so a live page can be tuned without a redeploy loop. Numbers per stop per size beat a screenshot judged by eye.

## Real-phone sign-off

The battery is necessary, never sufficient: it cannot see browser bars, the dynamic toolbar, notches or iOS overlays. Before calling mobile done, ask the human to open the preview on their own phone and scroll the whole journey forward and back, and to report (or screen-record) any stop they had to scroll inside, any label under the words, any white or grey bar, and any stutter. Record the device and browser in `STATUS.md`.

When the human describes a fix in space ("the labels must go down"), restate it relative to the visible object ("the name sits just below its form's foot") before building. An instruction relative to something invisible ("halfway between the header and the old spot") can easily move labels the wrong way.
