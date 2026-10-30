<!-- Generic guidance for matching SVG posters and WebGL glow.
     Performance choices are starting points, not measurements for a particular device.
     Verify compositing, colour parity and interaction costs in the target browsers. -->

## 5. Glow and light without bloom chains

### 5.1 The default: halo sprites

- Bake a radial Gaussian once (Canvas2D at init, or a 32 px PNG) and draw it on **additive instanced quads**. This is a useful starting point for sparse scenes. At thousands of stars, compare sprites against 1 px points plus a 1/8-resolution blurred copy: overlapping sprites increase fill cost, while a blur pass adds overhead even with only a few stars.
- **Instanced quads, not `gl_PointSize`**, for hover-hittable stars: points clip by centre and pop at panel edges, and `ALIASED_POINT_SIZE_RANGE` limits size.
- **Hover**: raise brightness and σ for the focused ID; no extra pass is needed. Selective bloom adds rendering work and should justify its cost.
- **A reusable billboard technique**: use a camera-facing plane with a pre-generated glow texture when a soft halo does not require a live bloom effect.
- **An example sprite**: a bicycle-parts guide could use a 64 px radial core with a faint circular rim for route markers. Bake the core and rim into one texture, then check that the result remains legible at its displayed size.

### 5.2 One halo profile, two renderers

Use radial gradients for static halos and baked sprites for their WebGL equivalents. Per-node live SVG blur can add repaint work during hover, which a page-load audit may miss. If design notes prescribe blur while the implementation uses gradients, resolve the conflict into one shared rendering rule.

Define the halo **once** as data (gradient stops, core radius, σ) and emit both the SVG `<radialGradient>` used by the poster and the Canvas2D stops used to bake the sprite from that data. This keeps the source profile consistent; still check rendered parity because interpolation and compositing can differ. The σ conversion is only needed where a blur is truly Gaussian: shader σ in device pixels = SVG `stdDeviation` in CSS pixels × DPR, assuming SVG user units map directly to CSS pixels. At DPR 1.5, multiply by 1.5.

### 5.3 Where lines and halos overlap

| Blend | What it does | Use for |
|---|---|---|
| Additive `(ONE, ONE)` | Sums colour contributions; can clip to white where many overlap | Halos and small highlights |
| Premultiplied "over" `(ONE, ONE_MINUS_SRC_ALPHA)` | Uses the same source-over compositing model as SVG; bounds accumulation when colours are correctly premultiplied | **Connecting lines** and crossings that should match the poster |
| `gl.MAX` | Keeps the largest channel value; does not accumulate brightness at crossings | Effects that deliberately need maximum intensity rather than layered lines |
| HDR target + Reinhard `c/(1+c)` | Preserves bright intermediate values, then compresses them in an extra pass | Dense glow that demonstrably needs more range |

Choose blending by the element's role. For example, a garden-supply how-to hub could use additive highlights for selected planting locations and source-over lines for paths between them. Colour alone should not determine the blend mode.

### 5.4 Glow over the plate, banding, colour space

- **Output `alpha = max(r,g,b)`** with `ONE, ONE_MINUS_SRC_ALPHA` for a glow whose opacity follows its strongest colour channel. With RGB bounded to 0–1, this produces valid premultiplied output that can composite over a painted background. It is a source-over approximation to additive glow, so check it against both light and dark areas of the artwork.
- **Avoid `mix-blend-mode` on the canvas by default**. It can add compositing work and change how the whole canvas interacts with the page background.
- **Use `premultipliedAlpha:true`** and ensure shader output follows that convention. Test transparent canvas edges and glow over the actual page background in the target browsers.
- **Static ±1/255 blue-noise dither** can reduce visible banding in dark gradients. Keep it static: temporal noise can shimmer on still panels. Generate a small noise texture or use one with a verified redistribution licence, preserving any required attribution. Wider-gamut or higher-precision intermediate buffers do not guarantee a banding-free final display; test the output viewers actually receive.
- **Colour space**: for parity with an SVG poster, explicitly match its colour interpolation and output encoding. When the poster interpolates in sRGB, start by matching that appearance. Do not write linear-light values directly to an sRGB canvas without the required encoding. Compare both renderers over the same background.
- **Colours come from tokens at runtime**: keep colour literals in one shared token definition and check for stray hex, rgb and hsl values elsewhere, including script strings. Read `--demo-star`, `--demo-line`, `--demo-highlight` and `--demo-background` with `getComputedStyle` at boot. Parse them into the colour representation expected by the shader; for a deliberately sRGB-matched pipeline, use normalized sRGB values without an extra linear conversion.
- **Other inexpensive approximations to test**: nested shells at falling opacity can suggest glow without a blur pass. A particle buffer at 0.5–0.7× the output dimensions can reduce fill work, at the cost of softer detail. Compare visual quality and rendering cost before adopting either technique.

---
