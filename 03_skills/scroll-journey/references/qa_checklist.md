# QA checklist

Two audits at two moments. **Part A** runs on `HANDOFF.md` before the human spends a single render, because a prompt defect is the cheapest defect to fix. **Part B** runs on the built page, because the "assembly" of a scroll journey is the browser joining clips to stills under the reader's scroll.

Give each audit fresh eyes: a separate subagent that receives the files (the handoff, the board, the stills; or the preview URL) and this checklist, not your reasoning. An auditor handed your conclusion tends to confirm it. Treat the writer's own self-flags as leads to verify, not facts: on a real build one of the writer's flags was false.

Every finding uses one line with a literal fix:

```text
Part A: <PromptID>/<take>, <defect>, <replacement text>
Part B: at <stop or passage ID> / <size or scroll position>, <defect>, <fix>, routed to <prompt | pipeline | build | board>
```

The verdict is always one of two words: **CLEAR TO RENDER** or **REVISE** (part A), **PASS** or **REVISE** (part B). No render until part A is clear. After every fix, re-audit: fixing one ruling can recreate the original defect elsewhere (for example, removing a pull-back to fix one finding can bring back a flat sideways slide).

## Part A: the prompt audit (before any render)

For every prompt section, every take B paragraph and every phone prompt:

- [ ] **Ingredients:** the paths exist; stop A is the **start** frame and stop B the **end** frame; the aspect of both stills matches the prompt's aspect; the names match the `@` names in INPUT ROLES.
- [ ] **At most 3 ingredients;** a passage normally uses exactly 2.
- [ ] **No inviting words:** no title, words, letters, lettering, sign, logo, label, caption, UI, "text-free", "no text"; no website, page, painting, frame; no water words over a horizon or band (waves, pours, drops, falls, pool, river, sea); no banned object smuggled back by its verbs. (`omni_passages.md` § Words that invite the wrong thing.)
- [ ] **A flight:** MOTION names one camera move through depth **and** a depth cue (near fast, far slow). A camera cue with no depth cue decays into a pan.
- [ ] **No roll:** no roll, spin, barrel, corkscrew, tilt. Where material turns, "the view never tilts" is written.
- [ ] **Direction matches the stills:** the stated drift agrees with where the focal light sits in stop A and in stop B (measured, for phone stills as well as wide).
- [ ] **Motion from the first moment, eased at both ends, no written holds;** "comes to rest exactly on @<stop B>" closes MOTION.
- [ ] **Cross-dissolves banned by name** in CONSTRAINTS.
- [ ] **Nothing new:** no object, light or shape that exists in neither still; the count of bright lights is stated.
- [ ] **Describes what is painted,** not what was planned (read the stills).
- [ ] **Self-contained:** palette restated inline with hex values and where each may appear, closed with "These are the only colours in the clip."; ends with `Silent.`
- [ ] **White page:** the ground is called light or space, not paper; the end-state clause asks for clean white at both ends; the white rule binds only the first and last frames.
- [ ] **Takes:** take B is a replacement MOTION paragraph only, same choreography, bigger.
- [ ] **Uniqueness:** no two passages share a camera move or a medium behaviour (the ledger is filled in).
- [ ] **Aspect, length (at most 10 s, normally 8) and filename** (`<PromptID>_<aspect>_<take>_take<N>.mp4`) are stated for every render.
- [ ] **The probe is marked** (the hardest passage, 16:9, take A) and the handoff tells the human to stop after it.

## Part B: the page pass (after the build)

Use a production build served locally (`npx astro preview`) or a deployed preview, never the dev server alone (it can behave differently with ranges and caching).

**Seams under scrub, both directions**
- [ ] Scroll **forward** through every stop, passage, stop join: no jump, flash, colour step or stutter at either end of any passage.
- [ ] Scroll **backward** through the same joins: reverse scrubbing is where weak encodes stutter and hidden seams reappear.
- [ ] Fast flick and slow crawl both; a rail jump lands on a still, not a half-decoded frame.
- [ ] At most two clip elements alive at once (`data-sj-clips`); passages shown with a painted clip (`data-sj-shown`).

To see a scrubbed page, drive the scroll with Playwright, capture screenshots at every hold, at every seam and at mid-passage in both directions, and read them. `scripts/journey_battery.mjs` already records the clip counts and the per-stop boxes.

**Words over picture**
- [ ] Each stop's words sit in the painting's calm side and read clearly over it; they fade early in the outgoing passage and settle only as the destination settles.
- [ ] **Contrast:** take a screenshot at each hold and at the start of each passage (where words and moving frames briefly overlap), and measure the text colour against the pixels under the words. WCAG AA asks for 4.5:1 for body text and 3:1 for large text. On a light journey raise the data's `veil` until the worst stop passes; on a dark journey raise the veil or the text shadow. `stop_check.py` gives the raw contrast of each still before any veil.
- [ ] Doors: each link box sits on its painted form at every size; its name and description read; hover and focus show the description; Esc clears it; on touch the description is always shown.

**Pacing**
- [ ] Holds are long enough to read every stop whole; passages feel like travel and do not drag; the peak stop gets the most deliberate arrival. Tune with `?hold=` and `?pass=` on the real device, then write the values into the CSS.

**Phones** (`mobile.md`)
- [ ] The five-size battery passes (`journey_battery.mjs`, rc 0).
- [ ] The human has looked on a real phone, forward and back, and reported no stop that needed scrolling inside its hold, no label under the words, no grey or white bar, no stutter.

**Fallbacks and access**
- [ ] **Reduced motion** (`prefers-reduced-motion: reduce`): mode `stills`, zero requests to `/video/`.
- [ ] **Pause:** pressing it switches to stills and releases every clip; pressing again resumes; `aria-pressed` and the label follow.
- [ ] **No script:** every stop's heading and words present in order, no `<video>`, the stops stacked.
- [ ] **Save-Data** or `?journey=stills`: the stills crossfade, nothing fetched.
- [ ] **A missing clip** (rename one in a test build): the stills crossfade over that passage; no blank stage, no console error beyond the failed request.
- [ ] Keyboard: tab order reaches the skip link, the pause button, the rail and each door; focus is visible; the skip link lands on the last stop's words.
- [ ] Headings in document order; the rail has an accessible name; the stills are decorative (`alt=""`) because the words are real text.

**Performance**
- [ ] The page's largest contentful element is not a journey still; layout shift stays at zero; the controller and clips load only on approach. Run Lighthouse (mobile) and an accessibility scanner (for example axe) on the built page and record the numbers in `STATUS.md`.

**Media**
- [ ] `verify_web_media.py` on the folder that ships: every file PASS (codec, no audio, faststart, GOP, size).
- [ ] A deployed clip answers a range request with `206` (`build_astro.md` § Hosting).

Routing: a seam or encode defect goes to the pipeline (repair or re-encode); a passage that misses its board row goes to the prompt (rewrite, re-audit, the human renders a fresh take, the gate); a copy, layout or interaction defect goes to the build; the pacing of holds against passages goes to the board, where the human decides.
