# Building the journey into an Astro site

The template is three files plus examples. It needs no packages beyond Astro itself (it uses `astro:assets` for the stills), no WebGL and no framework. It was built and checked with Astro 7 (`astro check`: 0 errors, 0 warnings, 0 hints; `astro build`: 2 pages), and exercised in headless Chromium at the five phone sizes plus one desktop size of the battery in `references/mobile.md`.

| Template file | Copy to | What it is |
|---|---|---|
| `template/src/components/ScrollJourney.astro` | `src/components/` | the markup, the parse-time fit test, the pause control, the lazy waker, and all styles |
| `template/src/scripts/journey.ts` | `src/scripts/` | the controller, imported only when a journey comes near |
| `template/src/data/journeys/types.ts` | `src/data/journeys/` | the data types |
| `template/src/data/journeys/seed-library.ts`, `night-sky.ts` | `src/data/journeys/` | two invented examples (light and dark); replace them |
| `template/src/pages/seed-library.astro`, `night-sky.astro` | `src/pages/` | two example pages; delete them once your page uses the component |

## Steps

Run these from the site's root folder.

1. Copy the template in:

   ```bash
   cp -Rn "$HOME/.claude/skills/scroll-journey/template/src/." src/
   ```

   (That is the installed skill. From the unzipped package, copy from `03_skills/scroll-journey/template/src/.` instead.)

   (`-n` never overwrites a file that already exists, so if your site already had a file at one of these paths, compare the two by hand. Check `git status` afterwards.)

2. Put the stills in `src/assets/journeys/<slug>/` as `s0-w.jpg`, `s0-p.jpg`, `s1-w.jpg`, ... (`.png` and `.webp` also work). The component finds them by name and fails the build with a clear message if one is missing. To lay out the page before the paintings exist, paint placeholders (`stills.md` § Placeholders).

3. Put the encodes in `public/video/<slug>/` with the names the pipeline wrote (`p1-16x9-v1.mp4`, `p1-16x9-1080-v1.mp4`, `p1-9x16-v1.mp4`, ...):

   ```bash
   mkdir -p public/video/seed-library
   cp ~/journeys/seed-library/web/*.mp4 public/video/seed-library/
   ```

   Clips stay in `public/`, never imported through the bundler: bundled assets get hashed names that bypass a host's range handling on some platforms, and the controller sets `video.src` to the `clips` pattern directly.

4. Write the data file (copy an example and edit it). Every word the reader sees lives here as a plain string: titles, subheads, body paragraphs, lines, link labels, the skip and rail labels and the pause labels. `art: 'seed-library/s0'` names the still. `side` is where the words sit on wide screens. `hold` lengthens a stop (give the peak more). `fit: true` turns on the fit test. `door` lays a link over a painted form, with its box as fractions of each still (`w` wide, `p` phone).

5. Use the component on a page:

   ```astro
   ---
   import ScrollJourney from '../components/ScrollJourney.astro';
   import { seedLibrary } from '../data/journeys/seed-library';
   ---
   <ScrollJourney journey={seedLibrary} />
   ```

6. Check and build:

   ```bash
   npm i -D @astrojs/check typescript
   npx astro check > astro_check.log 2>&1; echo "check rc=$?"
   npm run build > build.log 2>&1; echo "build rc=$?"
   ```

   Both must print `rc=0`. (`astro check` needs the two packages installed first; without them it stops to ask, and an agent's shell has no keyboard to answer.)

## How it behaves (all from the code)

- **Layout.** With script, a sticky full-screen stage inside a tall track. The track's height is `(--sj-hold x the holds + --sj-pass x the passages + --sj-end x the last hold) x 100svh`, computed from the data. Without script, or when the fit test fails, the stops stack: on a dark journey each stop is a screen of its painting with its words on it; on a light journey each painting comes first and its words follow on the paper. Headings are real `h2`/`h3` in document order either way.
- **The bands.** Hold S0, passage 1, hold S1, ... The outgoing words fade in the first tenth of a passage; the incoming words settle in its last sixth. The clip's time follows the scroll through an eased curve with a time-based lerp, so 60 Hz and 120 Hz screens feel the same.
- **Fetching.** Nothing is fetched until the page has loaded and the journey's top has passed the middle of the screen. Then only the current and the next passage exist as `<video>` elements; every other one is released (its `src` removed and the element dropped), because phones kill tabs that hold many decoders.
- **The reveal.** A clip becomes visible only once a frame is truly painted (`requestVideoFrameCallback` where the browser has it, `seeked` otherwise). Until then, and if a clip fails to load, the two stills crossfade, so the stage is never blank.
- **iOS priming.** After the first tap, key press or pointer press, every clip is played and paused once, including clips created later, so muted videos seek and paint reliably on iOS.
- **Tiers.** Portrait screens (`max-aspect-ratio: 1/1`) get `9x16`; landscape gets `16x9`, or `16x9-1080` from 1600 CSS px wide at a device pixel ratio of 1.5 or more. Re-decided live on resize; the reader keeps their place across a resize, a rotation or the wide/portrait flip.
- **Stills only** (nothing fetched, the stills crossfade): `prefers-reduced-motion: reduce`, Save-Data, the pause (`<html data-motion="paused">`), or `?journey=stills`.
- **The pause.** The component renders a "Pause motion" button (WCAG 2.2.2) that sets `data-motion="paused"` on `<html>` and remembers the choice in `localStorage` when storage is allowed. If your site already has a site-wide motion control, have it set the same attribute and pass `pause: false` in the data.
- **The fit test.** At parse, before first paint, an inline script checks every stop's words against the pinned screen (clear of `--sj-head` at the top). If any stop overflows, the journey stacks. The controller runs it again on wake, on resize and **after `document.fonts.ready`**: a parse-time test measures the fallback font, which usually sets shorter, so a long stop can pass at parse and overflow once the web font arrives.
- **Navigation.** A stop rail (dots) jumps instantly to a stop's hold; "Skip the journey" jumps to the last stop's hold and moves focus to its words; tabbing to a link inside a hidden stop brings that stop into view; Esc clears a door's preview.
- **Live tuning.** `?hold=1.4&pass=1.6` overrides the hold and passage lengths (screens) for a test on a real device. `?journey=720` or `?journey=1080` forces a landscape tier.
- **Test hooks** on the root element: `data-sj-ready`, `data-sj-mode`, `data-sj-band`, `data-sj-stop`, `data-sj-clips`, `data-sj-shown`. The battery script reads them.

## Theming: the custom properties

Override any of these on `.sj` (dark) or `.sj--light` from your own stylesheet; nothing else in the component hard-codes a colour, font or size you would want to change.

| Property | Default (dark / light) | Meaning |
|---|---|---|
| `--sj-hold`, `--sj-pass`, `--sj-end` | 1, 1.2, 1 | screens per stop hold, per passage, for the last hold |
| `--sj-ar` | 1.7917 (portrait 0.5581) | the stills' width / height |
| `--sj-head` | 0px | your pinned header's height |
| `--sj-bar` | `clamp(2.5rem, 10svh - 1rem, 5.5rem)` on portrait | the strip the phone browser's bars may cover (`mobile.md`) |
| `--sj-gutter`, `--sj-target` | `clamp(1rem, 4vw, 2rem)`, 44px | side margin; the minimum tap target |
| `--sj-font-display`, `--sj-font-body` | Georgia stack, inherit | titles and lines; body text |
| `--sj-title-size` | 1.6rem (wide `clamp(1.7rem, 2.4vw, 2.3rem)`, portrait 1.35rem) | stop titles and door names |
| `--sj-ground` | #1b1712 / #ffffff | the page ground behind the journey, and the veil colour |
| `--sj-text`, `--sj-heading` | #f2ede4 / #1c1f24, #1e3a5f | body text; titles and subheads |
| `--sj-accent` | #8fd3c1 / #2f6f4e | links, rail, skip, pause, focus rings |
| `--sj-swell-c` | the accent / #c9a227 | a door's glow (per door: `door.color`) |
| `--sj-label-veil` | 0.7 / 0.8 (door names 0.4) | the scrim behind small labels |
| `--sj-veil-w`, `--sj-veil-p` | 0.8, 0.86 (light only) | the words' paper veil, wide and phone (data: `veil`) |

For a light journey, set `--sj-ground` to your page's exact white.

## Hosting the clips

- **Byte ranges.** The host must answer `Range` requests for the MP4s with `206 Partial Content`. Check a deployed clip:

  ```bash
  curl -s -r 0-99 -o /dev/null -w '%{http_code}\n' https://your-site.example/video/seed-library/p1-16x9-v1.mp4
  ```

  It must print `206`. Static hosting on the common platforms answered ranges for files in `public/` when this was written (as of October 2026; re-check before relying on it). If yours prints `200`, seeking may wait for the whole file; serve the folder through the platform's static assets or a small range handler.
- **Caching.** Give `/video/*` a long immutable cache (`Cache-Control: public, max-age=31536000, immutable`), and change the version in the file name whenever a clip changes. Check that only one `Cache-Control` header ships: a site-wide rule plus a path rule can produce two.
- **Content Security Policy.** The controller uses same-origin `video.src`, so no `blob:` or `media-src` exception is needed beyond what `default-src 'self'` allows.
- **Weight.** About 1.4 MB per 8 s passage at 720p and about 3 to 4 MB at 1080p. A four-passage journey adds roughly 6 MB (720p), 15 MB (1080p) and 6 MB (9:16) to the repository; consider Git LFS or keeping the encodes out of the repository if that matters to the person.

## Blending the journey into the page around it

- A **light** journey melts into a white page by itself (its top and bottom are masked into the page).
- A **dark** journey under a hero: when two paintings meet, overlap them and cross-dissolve the paintings themselves, rather than meeting at a flat colour. A flat seam colour tends to leave a visible dark line; sliding the journey up under the hero by a few rem and fading the hero out over that band removes it.
- Do not set the first stop's still as the page's largest contentful element; let the hero keep that role. The stills load lazily with low fetch priority.

## Other frameworks

The controller is plain TypeScript with no Astro dependency. To port: render the same markup (classes `sj`, `sj-sticky`, `sj-stop` with `data-stop`, `data-side`, `data-hold`, `sj-still`, `sj-copy`, `sj-media` with `data-sj-media`, `sj-rail` marks with `data-rail`, `sj-track`), copy the `<style>` block, keep the `html.sj-js` class script before the markup, and call `wake(root)` from your own lazy loader. Responsive images then come from your framework's image tool instead of `astro:assets`.
