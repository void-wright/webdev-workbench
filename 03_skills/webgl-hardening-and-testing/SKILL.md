---
name: webgl-hardening-and-testing
description: Makes a WebGL or canvas layer production-safe on a real website and proves it. Covers the layer stack where the static page is the design, booting without hurting load (on interaction, or on visibility after load and idle), feature detection, first-frame truth, context loss, reduced motion, the WCAG 2.2.2 pause control, loop hygiene, touch and scroll, the resize/bfcache defence, Lighthouse/INP/CLS with a canvas, and a Playwright test battery. Use when adding any WebGL/canvas/animated layer to a page, reviewing one, or writing its tests. Part of the webgl-craft cluster.
---

# WebGL hardening and testing

**The doctrine in one line:** *the fallback IS the design*. Decide what the page does when the runtime never arrives **before** writing the happy path, and make that state useful and complete. The canvas only deepens what is already true without it.

## When to use this skill (and when another one)

| You are… | Use |
|---|---|
| adding, reviewing or testing any live canvas/WebGL layer on a page | **this skill** |
| choosing the renderer or setting fps/byte/particle budgets | `webgl-renderer-and-budget` |
| building pointer behaviour, hit-testing, preview/pin | `webgl-interaction` |
| making glow, halos, dither, colour match the page | `webgl-light-and-color` |
| not sure | `webgl-craft` (the router) |

## The stack (every layer, every page)

- **z0, the static design:** a `<picture>` plate (or CSS), SVG/HTML figures, every word.
- **z1, the canvas:** `aria-hidden`, `pointer-events:none`, **opacity 0 until its first frame is proven**, then a `.live` class fades it in over about 200 ms.
- **z2, content:** DOM buttons, readouts, legend, an accessible DOM equivalent of the visual, and the **pause control**.

The DOM equivalent lives in the page, never in `<noscript>`. `visibility:hidden` does **not** stop rAF, so halt the loop explicitly.

## Hard rules (each sourced in `references/03-hardened-recipe.md`)

1. **The canvas never carries text or meaning.** Every label and relation exists in the DOM. `aria-live` fires only on pin or focus.
2. **Never start during load.** Two allowed boots:
   - **Interactive layers:** first intent. `pointerenter`/`focusin` on desktop; on touch, the first `pointerdown` toggles a class and the heavy work waits a paint.
   - **Ambient decorative layers** (when the site calls for ambient motion): `import()` when the section first enters the viewport, **after** the load event and an idle period. The loader is at most 2 KB gzipped.
   - Never use Astro `client:visible`/`client:idle` alone to enforce these conditions.
3. **Reduced motion or Save-Data:** never fetch the GPU chunk. Freeze twice: CSS on the slot and a JS early return.
4. **Context:**
   - Request `getContext('webgl2', {alpha:true, premultipliedAlpha:true, antialias:false, depth:false, stencil:false, preserveDrawingBuffer:false, failIfMajorPerformanceCaveat:true, powerPreference:'low-power'})`.
   - A null context or a throw keeps the plate.
   - A software renderer string (SwiftShader) keeps the plate or a minimal tier. Read it once and never log it.
   - Never tier on GPU names: browsers may mask them.
5. **First-frame truth:**
   - Frame 0 equals the poster (same seed, t = 0, same halo). Design motion as displacement from rest with d(0) = 0.
   - Wait a double rAF, then fade in.
6. **Context loss:**
   - On `webglcontextlost`: `preventDefault()`, stop the loop, show the plate.
   - On restore: recompile, re-upload from CPU copies, and re-prove the first frame.
   - Test with `WEBGL_lose_context`.
7. **WCAG 2.2.2:** any motion that starts by itself, lasts over 5 s and sits beside other content needs a **visible pause control**. That applies regardless of reduced motion. One page-level control may pause every loop on the page.
8. **Loop hygiene:**
   - rAF only, on a pausable clock.
   - Pause on IntersectionObserver (threshold 0.1) and `visibilitychange`. Reset `lastT` before the first frame back.
   - Clamp dt to ≤ 0.1 s. Give springs fixed 1/120 s sub-steps.
   - Every ease is `1 − exp(−dt/τ)`.
   - Stop requesting frames when motion energy is below ε.
9. **Touch:** `touch-action: pan-y`, and never `preventDefault` on touch.
10. **Refresh/bfcache:**
    - Defer the first measure through rAF.
    - Put the `ResizeObserver` on the container.
    - Re-measure on `pageshow` at 0/100/400 ms.
    - Check size drift every 30 frames.
11. **Same-origin bundles only** (CSP). No colour literals: read tokens at runtime. No web storage beyond what the site's own privacy rule allows.

## Testing: instruments first

- **Headless Chromium may render WebGL on SwiftShader (CPU).** Check the renderer before interpreting results. Software-rendered fps is a relative cost only. Real-GPU frame rate needs a headed browser on a real GPU, with hardware rendering verified. Otherwise report it as **not run**.
- **4× CPU throttle** tests boot, INP and long tasks, **not** mobile fill-rate.
- **Lighthouse navigation mode never interacts:**
  - It scores the poster page, which is exactly the design.
  - Measure INP with timespan mode or `web-vitals` `onINP`.
  - For a large visual hero, use a poster `<img>` that can be an LCP candidate. A canvas or inline SVG is not itself an LCP candidate.
- **The test battery** is in `references/08-testing-and-measurement.md`:
  - scripts off, script error, no WebGL, software GL, context loss;
  - reduced motion: no GPU request;
  - 2.2.2 keyboard pause freezes the frame counter;
  - off-screen/hidden: no time jump;
  - touch scrolls;
  - 60 vs 120 Hz frame-rate independence;
  - INP, CLS = 0, poster parity;
  - boot trigger: no GPU before intent/visibility;
  - long tasks, cross-origin, bundle size, refresh/bfcache.
- **Expose state as data attributes** (`data-gpu="poster|booting|live|lost|paused"`, a frame counter, scheduler counts), never a debug global in production.
- **Prove every new check can fail** by deliberately introducing the fault it should detect.

## Field lessons from production

`references/13-field-lessons.md`:

- Tie verification logs to the build hash so results identify the build actually tested.
- Check the first screen at the *visible* viewport size.
- Consider `lvh` for sticky art windows that should remain stable as browser controls move.
- Make pin links land on the subject they name.
- Check temporary-directory access when Lighthouse fails before producing a report.
- Preserve the test command's exit status when piping output through `tail`; otherwise a successful output filter can hide a failed test.

## Go deeper

- `references/03-hardened-recipe.md`: the full recipe, plus a checklist of common fixes for a decorative three.js scene.
- `references/08-testing-and-measurement.md`: the instruments, the Playwright traps, the 4× profile, Lighthouse with a canvas, CLS while hovering, the battery.
- Record hardening lessons with the failure, the fix and a reproducible check. Tag them `webgl-craft` and `webgl-hardening` so they are easy to find before the next build.
