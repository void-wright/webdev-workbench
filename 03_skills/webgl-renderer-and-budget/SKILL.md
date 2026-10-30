---
name: webgl-renderer-and-budget
description: Chooses the rendering technology for a browser graphics layer (HTML/SVG/CSS, Canvas2D, raw WebGL2 plus a small helper, OGL/twgl/regl/PicoGL, three.js WebGLRenderer, three.js WebGPURenderer+TSL, raw WebGPU) and sets its performance budget (frame time, DPR cap, fill-rate and overdraw, particle/link caps, bundle bytes, shader compile, render-target formats, off-screen pause, dt clamps, LCP/CLS/INP). Includes guidance for checking library sizes, licences and browser capabilities. Use before writing any WebGL/canvas code, when a scene is slow, or when picking a library. Part of the webgl-craft cluster.
---

# WebGL renderer choice and performance budget

## When to use this skill (and when another one)

| You are… | Use |
|---|---|
| deciding what to render with, or how much it may cost | **this skill** |
| making the layer safe (fallback, boot, pause, context loss) and testing it | `webgl-hardening-and-testing` |
| making it look right (glow, colour) or behave right (pointer) | `webgl-light-and-color`, `webgl-interaction` |

## The decision tree (ask in order; the first "yes" picks the tier)

| # | Question | Tier |
|---|---|---|
| 1 | Does it carry meaning, or must it work without JS or with reduced motion? | **HTML/SVG/CSS**: always, for words, readouts, legends and a static equivalent |
| 2 | A few hundred sprites and hairlines, additive, no custom shader? | **Canvas2D**. Test the intended sprite sizes, blending and device range before committing. |
| 3 | Thousands of particles, SDF links, instancing, `MAX` blending or float targets? | **Raw WebGL2 plus a small helper** (the default) |
| 4 | Helpers wanted, but no engine? | **OGL** or **twgl**. Check the selected version's licence and compressed bundle size. |
| 5 | A scene graph, glTF/DRACO/KTX2 loaders, `UnrealBloomPass` or `Line2`? | **three.js WebGLRenderer.** Measure the production bundle and explicitly justify any budget increase. |
| 6 | Compute or WebGPU features with automatic fallback? | **three.js WebGPURenderer + TSL.** Measure bundle weight and shader compilation time, and test the fallback path. |
| 7 | WebGPU with no framework? | **Raw WebGPU**, plus a **separate** WebGL2 path |

**Default recommendation:** raw WebGL2 plus your own small WebGL helper. Keep program setup, material state, full-screen draws and render-target probing explicit. If adapting third-party code, verify its licence and retain the required attribution.

- Live decorative layers can use instanced quads, capsules and closed-form particles.
- **Fill-rate and overdraw can dominate cost.** Compare pixel counts and post-processing passes before assuming that fewer API calls will fix a slow scene.

## Budget rules of thumb (sourced and status-marked in `references/02-performance-budget.md`)

- **Frame:** 16.7 ms at 60 Hz (8.3 ms at 120 Hz); a 50 fps floor means ≤ 20 ms. 33 ms is a degrade trigger, never a target. Use a **one-shot tier-down** (the first 5 frames averaging over 33 ms → back to the poster), never a resolution-pumping controller.
- **DPR:** `Math.min(devicePixelRatio, 1.5)` for the canvas; HTML/SVG keep native DPR. From 3 to 1.5 removes 75% of the pixels.
- **Budget overdraw, not object count.** One 1200×560 panel at DPR 1.5 is 1.51 Mpx, or 90.7 Mpx/s at 60 fps per full-panel layer.
- **Scale ceiling (per panel):** ≤ 300 stars, ≤ 500 links, ≤ 20k particles. These are starting limits, not guarantees. Per-width caps remain proposals until tested on representative devices:

  | Viewport width | Stars / links / particles |
  |---|---|
  | <560 px | 120 / 150 / 3k |
  | 560–1023 px | 200 / 300 / 8k |
  | 1024–1679 px | 300 / 500 / 15k |
  | 1680 px and up | 300 / 500 / 20k |

- **Bytes:** ≤ 30 KB gzipped per layer (target); 200 KB is a hard ceiling for this budget. Keep the background artwork as AVIF/WebP in HTML unless the effect requires texture sampling. Bake star sprites at boot with Canvas2D or ship a small 32 px PNG. Avoid KTX2 unless large textures justify its loader cost.
- **Render targets:**
  - Prefer **RGBA16F** for floating-point filtering or blending, after checking the required capabilities.
  - Keep RGBA32F for unfiltered state when its precision is necessary.
  - Probe candidate formats on a 4×4 FBO: R16F → RG16F → RGBA16F → RGBA8 + dither. Verify the operations you need, not just framebuffer completeness.
- **Never store drifting positions in half-float.** Representable values are 1.0 apart across 1024–2048, so small updates can round away and slow drift sticks. Prefer closed-form (analytic) motion.
- **Compile:** use a handful of small programs. Feature-detect `KHR_parallel_shader_compile`; do not assume availability across browsers.
- **Boot slicing:** yield with `setTimeout`/`MessageChannel`. Feature-detect `scheduler.yield` and `requestIdleCallback` before using them.
- **INP** counts tap, click and keydown interactions, not pointermove, hover or wheel. Keep individual main-thread tasks below 50 ms after boot.
- **LCP:** make the poster `<img>` eligible to be the LCP element. Canvas drawing and inline SVG shapes do not provide an equivalent LCP candidate. **CLS:** reserve space and fade with opacity.
- **Glow:** use sprites without a post-processing chain when they achieve the intended effect (see `webgl-light-and-color`).

## Re-verify before trusting (changing facts)

Browser coverage, package sizes and maintenance status change. Before a decision depends on them:

- Check WebGPU support across the browsers and devices your site serves, including mobile Safari.
- Check WebGL2 availability and test context creation on the supported device range.
- Confirm the three.js version, renderer APIs and loader compatibility.
- Read the licence included with the chosen OGL release; do not assume all small graphics libraries use MIT.
- Check PicoGL's release and maintenance activity before adopting it.
- Measure twgl and other helpers in the actual production bundle, with the same compression settings used for your budget.

Use capability surveys to identify likely gaps, then test the required features. A support percentage does not prove that your rendering path works.

## Go deeper

- `references/01-renderer-decision.md`: the options table, library size and licence checks, capability considerations and reasons to reject an option.
- `references/02-performance-budget.md`: the full budget table with evidence and status.
- **Sources:** verify consequential claims against official documentation, package licences and reproducible measurements. Record the version and test conditions beside each result.
- **Learning notes:** tag your renderer and budget lessons `webgl-craft` and `webgl-renderer` for later retrieval. Treat research summaries as leads until their claims have been checked.
