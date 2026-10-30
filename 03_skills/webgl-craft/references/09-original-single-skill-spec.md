<!-- This specification describes how to organise and validate a reusable WebGL skill.
     Status markers: VERIFIED (checked against a primary source or recomputed), CONTRADICTED (do not build on it),
     UNSETTLED (a lead), ESTIMATE (no measurement). Performance targets below are acceptance criteria, not measured results.
     The worked example is an invented garden-supply shop's guide library. Supporting implementation assets must be created and validated before use. -->

## 9. SPEC FOR THE SKILL `webgl-craft`

### 9.1 Placement, build method, gates

- **Where**: keep one canonical skill entry and use the same instructions across builder tools.
- **How**: validate the skill's structure and refine it through an ACE loop with a 9.8 quality threshold. Record each reusable lesson separately.
- **Tags**: `webgl-craft`.
- **Acceptance**: the skill parses cleanly; a micro-demo built from it hits ≥50 fps on a named desktop GPU and under a 4× CPU-throttled mobile profile; reduced-motion and no-JS states are verified.
- **Completion checkpoint**: review missing evidence across design, implementation and testing. Record the skill's structure and rationale, plus the micro-demo's frame rates and the renderer that produced them. When several tools can update shared notes, assign distinct records or use a single writer to prevent collisions.
- **Inputs not yet gathered**: identify any reference-site analysis still needed. State the exact element to examine and the unanswered question. Keep pending analysis visibly separate from verified guidance.

### 9.2 Folder layout

The shipped cluster separates the entry point, implementation guidance and validation guidance:

```text
03_skills/
  webgl-craft/
    SKILL.md
    references/
      00-how-to-read.md
      09-original-single-skill-spec.md
      10-licence-ledger.md
      11-mistakes.md
      12-open-conflicts.md
  webgl-renderer-and-budget/
    SKILL.md
    references/
      01-renderer-decision.md
      02-performance-budget.md
  webgl-hardening-and-testing/
    SKILL.md
    references/
      03-hardened-recipe.md
      08-testing-and-measurement.md
  webgl-interaction/
    SKILL.md
    references/
      04-interaction-recipes.md
  webgl-light-and-color/
    SKILL.md
    references/
      05-glow-and-light.md
  webgl-constellations/
    SKILL.md
    references/
      06-constellations.md
  webgl-cosmic-art-direction/
    SKILL.md
    references/
      07-motifs.md
  webgl-handoff-and-porting/
    SKILL.md
```

A project implementing this specification also needs the following assets. These are implementation requirements, not claims that additional files ship with this package:

- Your own small WebGL helper, written in TypeScript, for context creation, fallback selection, program linking, VAO/instancing setup, a 4×4 format probe, blitting, context-loss handling and a frame clock.
- Shaders for halo sprites, SDF capsules, dithering, loop-exact curl displacement and morphing.
- One seeded PRNG implementation shared by Node prebuild and browser code.
- One halo definition that produces both SVG gradient stops and sprite stops.
- A runtime token-to-uniform adapter using `getComputedStyle` and sRGB floats.
- A licensed blue-noise texture with attribution where required.
- A micro-demo, reusable Playwright checks and deterministic fixtures.
- Instrumentation for renderer identification, steady-state fps, p95 frame interval, long tasks and INP.
- A licence ledger covering helper code, shader mathematics and textures, including required notices.

### 9.3 What each section contains

**Skill entry** (keep it short; route to references):
- Use `webgl-craft` as the skill's identifier. Describe triggers such as "WebGL", "canvas layer", "layered art", "constellation", "starfield", "glow", "particles", "WebGL mode for a layered art component" and "WebGL handoff".
- **Doctrine in five lines**: the fallback is the design; GPU rendering starts on first interaction, never on load; the canvas never carries essential text or meaning; the DOM owns state and the canvas follows; budget fill-rate, not just object count.
- **Hard rules**: DPR ≤1.5; `antialias:false`; sprites instead of default square points; instanced quads for hittable stars; reduced motion never fetches the GPU chunk; a pause control for auto-motion lasting more than 5 seconds; IntersectionObserver pause at a 0.1 threshold with clock reset; `visibilitychange` pause; first-frame validation before applying `.demo-live`; context-loss recovery; `touch-action: pan-y` with no `preventDefault` on touch; colours from runtime tokens; no CDN scripts; no web storage for this decorative layer; no GPL or unlicensed code in this implementation. Distinguish project constraints from general platform requirements.
- **Routing table**: map each task to a shipped reference.
- **Decision tree**: essential meaning or no-JS access → HTML/SVG/CSS; a few hundred sprites without custom shaders → Canvas2D; thousands of particles, SDF lines or instancing → raw WebGL2 plus your own small WebGL helper; extra API convenience → OGL; scene graphs or loaders → three.js with an explicitly reviewed budget; compute workloads → consider WebGPU, without adding it solely for a decorative content-site layer.

**03_skills/webgl-renderer-and-budget/references/01-renderer-decision.md**: compare renderer options by verified bundle sizes, licences, maintenance and capabilities. Explain the recommendation and rejected options. Record when version-sensitive facts were checked and re-verify them before relying on them.

**03_skills/webgl-renderer-and-budget/references/02-performance-budget.md**: define per-width caps, overdraw arithmetic and degradation triggers. Label each budget row either `ESTIMATE` or `measured on <device> <date>`. Replace estimates only after running the demo.

**03_skills/webgl-hardening-and-testing/references/03-hardened-recipe.md**: define the z-stack contract for the wrapper component that holds the canvas and its fallback (for example `LayeredArt`), context attributes, fallback ladder, boot sequence with Safari-safe yielding, first-frame validation, visual handover, context loss, reduced-motion freezing, pause controls, no-JS behaviour, loop hygiene and resize defence. Include a keep/change review of any source implementation so its omissions are not copied into the port.

**03_skills/webgl-interaction/references/04-interaction-recipes.md**: cover DOM-owned state, force fields, springs, curl flow, hit-testing, preview/pin behaviour, parallax and moving highlights. Write fresh GLSL and TypeScript examples rather than copying code from sources available only for study.

**03_skills/webgl-light-and-color/references/05-glow-and-light.md**: explain the shared halo profile, blend choices, `alpha=max(r,g,b)`, dithering, colour space and the token-to-uniform path.

**03_skills/webgl-constellations/references/06-constellations.md**: explain contrast measurement, compounded opacity, seeded randomness, relative neighbourhood graph links, ranked brightness and reserved readout space. For example, applying opacity 0.35 twice produces an effective opacity of 0.1225, which can make an otherwise legible line disappear.

**03_skills/webgl-cosmic-art-direction/references/07-motifs.md**: present motifs as an open menu drawn from each site's own subject (for example, rising steam for a kitchen-equipment maker or turning spokes for a bicycle-parts company), never as a fixed set. Show the loop-period arithmetic for each animated motif.

**03_skills/webgl-hardening-and-testing/references/08-testing-and-measurement.md**: put instrumentation rules first: identify the actual renderer, distinguish hardware rendering from software fallback and state that CPU throttling does not emulate a mobile GPU. Implement the acceptance checks as reusable Playwright tests.

**03_skills/webgl-handoff-and-porting/SKILL.md**: define a per-page handoff package containing:
- A brief with one intended impression, exact tokens, z-stack contract, pointer and keyboard behaviour, named controls, reduced-motion and off-screen states, a ≤200 KB bundle ceiling, DPR and per-width particle caps, no essential text in canvas, and target viewports of 1440/1024/390.
- Assets with explicit roles, such as a painted background or a decorative marker.
- Reference captures.
- Hardening instructions.
- Port notes naming the wrapper component the port integrates into (for example `LayeredArt`).
- Acceptance checks.

Preserve the handoff's animation mathematics when porting. Remove the design-tool runtime and unused heavy assets. Provide a static reduced-motion state, IntersectionObserver pause, ResizeObserver-driven resizing and a DPR cap. Prove fidelity by comparing constants and keyframes. Size the focal element with `min(W·kx, H·ky)`. Reset the clock after an off-screen pause. Keep unfinished product controls inert behind one feature flag. Give each page one memorable visual moment.

**03_skills/webgl-craft/references/10-licence-ledger.md** and **03_skills/webgl-craft/references/11-mistakes.md**: record licence obligations and recurring failure modes with their fixes.

**Source notes**: retain supporting URLs with verification verdicts. Flag suspicious or unresolved sources instead of presenting them as evidence.

**Reference-site analysis**: record read-only browser observations, network requests, renderer/API identification, input mapping, measured frame budget, reduced-motion, visibility, off-screen and no-JS behaviour, and licence findings. Use observations to learn techniques, not to copy proprietary implementation assets. Leave unanswered questions explicitly pending.

### 9.4 The micro-demo

**Purpose**: prove the skill at an explicit scale ceiling: ≤300 stars, ≤500 connecting segments and ≤20k particles in a 1200×560 panel at DPR 1.5. Testing at the ceiling exposes limits that a small decorative example could hide.

**Contents** (one `LayeredArt` page for an invented garden-supply shop's guide library, built from validated project assets):
1. z0: a calibrated still image or CSS placeholder, with the image supplied through `<picture>`.
2. z2: an SVG constellation laid out during the TypeScript prebuild, using a fixed seed and relative neighbourhood graph links. Represent 48 guides in 6 topic groups with 48 px DOM buttons, a legend that controls selection, a reserved readout band, an equivalent HTML guide list and a visible pause control.
3. z1, after first interaction only: raw WebGL2 plus your own small WebGL helper, drawing:
   - 300 instanced halo sprites in three brightness tiers: 48 guide markers and 252 background stars;
   - 500 SDF capsule segments moving through loop-exact curl displacement, with a 60-second period;
   - 20,000 analytic dust particles using closed-form drift with a 120-second period;
   - one moving signal highlight, coloured through a `--demo-...` token;
   - hover, focus and pin states supplied by DOM events, with a travelling light along active edges;
   - static blue-noise dither and `alpha = max(r,g,b)` output.
4. Instrumentation: `window.__demoFrames`, `data-gpu` states, a frame-interval ring buffer and `window.__demoSetTime(t)` for deterministic screenshots.

**Pass criteria** (all must hold; record raw numbers, not just PASS):

| # | Criterion | How it is measured |
|---|---|---|
| 1 | The skill parses cleanly | Validate frontmatter and routing; confirm every referenced file exists |
| 2 | **≥50 fps on the named desktop GPU** | Use a browser with hardware rendering, not SwiftShader; viewport 1440×900, emulated DPR 2 with canvas DPR capped at 1.5; measure 10 seconds of steady state after boot with a scripted pointer sweep; mean fps ≥50 and p95 frame interval ≤20 ms; record the actual renderer and browser configuration |
| 3 | **≥50 fps under a 4× CPU-throttled mobile profile** | Verify hardware rendering; use CDP CPU throttle 4×, viewport 390×844, emulated DPR 3 with canvas DPR capped at 1.5, and touch input; mean fps ≥50, p95 frame interval ≤20 ms, boot interaction latency <200 ms and no long task >50 ms after boot |
| 4 | **Reduced-motion freeze verified** | With `emulateMedia({reducedMotion:'reduce'})`, verify zero GPU-chunk requests, no WebGL context and `window.__demoFrames` remaining 0; background and SVG stay visible; hover highlighting works through SVG classes; switching the media query live stops a running layer within one frame |
| 5 | **No-JS state complete** | With `javaScriptEnabled:false`, verify the background, SVG constellation, legend, readout text and equivalent guide list; every label in the build data appears in the DOM; keyboard navigation activates the `:target` highlight path; axe reports zero critical or serious violations |
| 6 | Hardening holds | Context loss shows the poster; restoration validates the first frame before fading in; off-screen and hidden-tab pauses freeze the counter without a time jump; touch swipes scroll the page; keyboard activation of pause stops frames |
| 7 | Budget | GPU chunk ≤30 KB gzip as a target and ≤200 KB as a hard ceiling; poster `<img>` is the LCP element; CLS is 0 during boot and hover |
| 8 | Record | Store renderer and version, browser and version, test configuration, frame-rate tables and bundle size together so every result can be traced to the renderer that produced it |

What the micro-demo does **not** prove: mobile GPU fill-rate or Safari behaviour. CPU throttling changes CPU execution speed, not GPU capability. State these limits in the record and keep real-device and Safari validation open until tested.

### 9.5 The test battery

Implement reusable Playwright checks against the micro-demo first, then apply them to pages marked with `data-webgl-layer`. Cover parsing, hardware-renderer verification, frame timing, reduced motion, no-JS access, context recovery, pause behaviour, touch scrolling, keyboard operation, accessibility and loading budgets. This specification describes required checks; it does not imply that a runnable test suite ships alongside it.

Add two static checks:

- **Implementation-gap lints**: search built JavaScript for `setInterval(` in render paths, unseeded `Math.random` in layout, per-frame increments without elapsed-time scaling, `preventDefault` in touch handlers, CDN script URLs, colour literals outside tokens and use of `localStorage`, `sessionStorage` or IndexedDB. Review matches in context and correct violations of the layer's constraints.
- **Port proof**: when porting a design-tool handoff, compare constants and keyframes against the source. Matching the visible assets alone does not preserve motion, timing or interaction behaviour.

---
