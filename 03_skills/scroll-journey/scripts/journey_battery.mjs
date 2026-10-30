#!/usr/bin/env node
/**
 * JOURNEY BATTERY: measure a built scroll journey at the five phone sizes and one desktop size, per stop, in numbers.
 *
 * For every viewport it loads the page, jumps to each stop's hold through the rail (the same instant jump a reader
 * gets), waits for the stage to settle and records, per stop:
 *   - the words box against the pinned stage: clear of the top strip (--sj-head) and of the foot strip a phone
 *     browser's own bars may cover (--sj-bar, portrait only); "fits" means the whole block is readable without scrolling;
 *   - any overlap between the words box and a door's name label;
 *   - whether the journey stacked itself (the fit test), and which clip tier it chose (data-sj-mode).
 * Then a scrub pass from top to bottom records which passages were shown with a painted clip (data-sj-shown) and the
 * largest number of clip elements alive at once (data-sj-clips; the controller keeps at most two).
 *
 * --css FILE injects candidate CSS into the live page first (a <style> in <head>), so a phone layout can be tuned on the
 * real page, at every size, before any source file changes. An emulator has no browser bars: a pass here is necessary,
 * never sufficient. Finish on a real phone.
 *
 * usage (from your site's folder, where Playwright is installed: npm i -D playwright && npx playwright install chromium):
 *   node "$SJ/journey_battery.mjs" URL [--css FILE] [--root SELECTOR] [--json OUT]
 *   (SJ = this skill's scripts folder: 03_skills/scroll-journey/scripts in the package, or the installed skill's scripts)
 * Exit 0: every stop fits, no overlap, at every size / 1: something does not / 2: usage or the page has no journey.
 */
import { createRequire } from 'node:module';
import { readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const opt = (name) => {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : undefined;
};
const url = args.find((a, i) => !a.startsWith('--') && !['--css', '--root', '--json'].includes(args[i - 1]));
if (!url) {
  console.error('usage: node journey_battery.mjs URL [--css FILE] [--root SELECTOR] [--json OUT]');
  process.exit(2);
}
// resolve Playwright from the folder you run this in (your site), not from the skill's folder
const require = createRequire(path.join(process.cwd(), 'noop.js'));
let chromium;
try {
  ({ chromium } = require('playwright'));
} catch {
  console.error('Playwright is not installed here. In your site folder run: npm i -D playwright && npx playwright install chromium');
  process.exit(2);
}
const css = opt('--css') ? readFileSync(opt('--css'), 'utf8') : '';
const ROOT = opt('--root') || '[data-scroll-journey]';
const SIZES = [
  [360, 640],
  [375, 667],
  [390, 664], // a phone with the browser's bars showing
  [390, 844],
  [430, 932],
  [1440, 900],
];

const browser = await chromium.launch();
const report = [];
let bad = 0;
for (const [w, h] of SIZES) {
  const touch = w < h;
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 2, hasTouch: touch, isMobile: touch });
  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: 'load' });
  if (css) await page.addStyleTag({ content: css });
  if (!(await page.$(ROOT))) {
    console.error(`no element matches ${ROOT} at ${url}`);
    await browser.close();
    process.exit(2);
  }
  // bring the journey near so the controller wakes, then let fonts and the fit test settle
  await page.$eval(ROOT, (r) => r.scrollIntoView({ block: 'start', behavior: 'instant' }));
  await page.waitForFunction((sel) => document.querySelector(sel)?.dataset.sjReady !== undefined || document.querySelector(sel)?.hasAttribute('data-sj-stack'), ROOT, { timeout: 15000 }).catch(() => {});
  await page.evaluate(() => document.fonts?.ready);
  await page.waitForTimeout(300);
  const stacked = await page.$eval(ROOT, (r) => r.hasAttribute('data-sj-stack'));
  const mode = await page.$eval(ROOT, (r) => r.dataset.sjMode || '');
  const row = { size: `${w}x${h}`, stacked, mode, stops: [], scrub: null };
  if (!stacked) {
    const n = await page.$$eval(`${ROOT} [data-rail]`, (m) => m.length);
    for (let i = 0; i < n; i++) {
      await page.$eval(`${ROOT} [data-rail="${i}"]`, (m) => m.click());
      await page.waitForTimeout(450);
      const m = await page.$eval(
        ROOT,
        (r, i) => {
          const sticky = r.querySelector('.sj-sticky').getBoundingClientRect();
          const cs = getComputedStyle(r);
          const px = (v) => {
            const d = document.createElement('div');
            d.style.height = v || '0px';
            r.appendChild(d);
            const out = d.getBoundingClientRect().height;
            d.remove();
            return out;
          };
          const head = px(cs.getPropertyValue('--sj-head').trim());
          const bar = innerWidth <= innerHeight ? px(cs.getPropertyValue('--sj-bar').trim()) : 0;
          const stop = r.querySelector(`.sj-stop[data-stop="${i}"]`);
          const c = stop.querySelector('.sj-copy').getBoundingClientRect();
          const names = [...stop.querySelectorAll('.sj-door__name')].map((e) => e.getBoundingClientRect());
          const overlap = names.some((b) => b.left < c.right && b.right > c.left && b.top < c.bottom && b.bottom > c.top);
          const top = c.top - sticky.top;
          const bottom = c.bottom - sticky.top;
          return {
            stop: i,
            words_top: Math.round(top),
            words_bottom: Math.round(bottom),
            stage: Math.round(sticky.height),
            head: Math.round(head),
            bar: Math.round(bar),
            fits: top >= head && bottom <= sticky.height - bar,
            label_overlap: overlap,
          };
        },
        i,
      );
      if (!m.fits || m.label_overlap) bad++;
      row.stops.push(m);
    }
    // the scrub pass: top to bottom in small steps
    const span = await page.$eval(ROOT, (r) => ({ top: r.getBoundingClientRect().top + scrollY, h: r.offsetHeight }));
    const shown = new Set();
    let maxClips = 0;
    for (let y = span.top; y <= span.top + span.h; y += Math.max(40, Math.round(h / 6))) {
      await page.evaluate((y) => scrollTo({ top: y, behavior: 'instant' }), y);
      await page.waitForTimeout(120);
      const s = await page.$eval(ROOT, (r) => ({ shown: r.dataset.sjShown || '', clips: (r.dataset.sjClips || '').split(',').filter(Boolean).length }));
      if (s.shown) shown.add(s.shown);
      maxClips = Math.max(maxClips, s.clips);
    }
    row.scrub = { passages_shown: [...shown].sort(), max_clips_alive: maxClips };
  }
  report.push(row);
  const stopsTxt = row.stops.map((s) => `S${s.stop}:${s.fits && !s.label_overlap ? 'ok' : s.fits ? 'LABEL' : 'OUT'}(${s.words_top}-${s.words_bottom}/${s.stage})`).join(' ');
  console.log(`${row.size} mode=${mode || '-'} ${stacked ? 'STACKED (fit test)' : stopsTxt}${row.scrub ? ` | shown=[${row.scrub.passages_shown}] max_clips=${row.scrub.max_clips_alive}` : ''}`);
  await ctx.close();
}
await browser.close();
if (opt('--json')) writeFileSync(opt('--json'), JSON.stringify(report, null, 1));
console.log(bad ? `FAIL: ${bad} stop measurement(s) out of bounds or overlapping a label` : 'PASS: every stop fits at every size');
process.exit(bad ? 1 : 0);
