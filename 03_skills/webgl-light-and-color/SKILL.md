---
name: webgl-light-and-color
description: Light and colour for WebGL/canvas layers that sit over painted or photographic art and beside SVG/HTML. Covers glow without bloom chains (baked halo sprites on instanced quads), defining one halo profile that drives both the SVG poster and the GPU sprite, blend modes for halos vs lines (additive vs premultiplied over vs MAX vs HDR), alpha=max(r,g,b) compositing over a background, static blue-noise dither against banding on dark grounds, sRGB vs linear, and reading colours from CSS tokens at runtime. Use when anything must glow, when banding shows, or when canvas and SVG must match. Part of the webgl-craft cluster.
---

# WebGL light and colour

## When to use this skill (and when another one)
| You are… | Use |
|---|---|
| making stars, sparks or lines glow; fixing banding; matching canvas to SVG | **this skill** |

## Rules (full detail and sources in `03_skills/webgl-light-and-color/references/05-glow-and-light.md`)
1. **Glow without bloom.** Bake a radial Gaussian sprite once (Canvas2D at boot, or a 32 px PNG) and draw it on **additive instanced quads**.
   - At high star counts, compare sprites with a blur pass; the crossover depends on sprite area and overdraw.
   - Selective bloom adds rendering work. A billboard carrying a pre-baked glow texture can provide a simpler alternative.
2. **Use instanced quads, not `gl_PointSize`, for anything hittable or near an edge.** Points clip by their centre, pop at the edges, and are size-limited.
3. **Hover:** raise brightness and σ for the focused id, without an extra pass.
4. **One halo profile, two renderers.**
   - Define the halo once as data (stops, core radius, σ).
   - Emit both the SVG `<radialGradient>` (poster) and the sprite's Canvas2D stops from it, so parity holds by construction.
   - Never use live SVG blur per node: it repaints on hover. Shader σ in device px = CSS stdDeviation × DPR.
5. **Blends:**

   | Blend | What it does | Use for |
   |---|---|---|
   | Additive `(ONE, ONE)` | sums; can saturate in a bounded colour buffer | halos and sparks |
   | Premultiplied "over" `(ONE, ONE_MINUS_SRC_ALPHA)` | the same maths as SVG source-over; attenuates the destination as it adds the source | lines and crossings |
   | `MAX` | selects the larger value per channel; does not accumulate overlapping light | generally unsuitable for layered glow |
   | HDR + Reinhard | preserves accumulated light before tone mapping; adds a pass | only at high density |

6. **Over a painted background:** for bounded glow RGB values, output `alpha = max(r,g,b)` with premultiplied over. Never put `mix-blend-mode` on the canvas. Keep `premultipliedAlpha:true`.
7. **Banding on dark grounds:** add a **static** ±1/255 blue-noise dither before output. Temporal dither shimmers on still panels. Use a verified CC0 blue-noise texture and retain its provenance. Wide-gamut or float16 canvases don't remove the need to check for banding.
8. **Colour space:** blend in sRGB and tune by eye for parity with the SVG poster. Do not write linear values to an sRGB canvas without encoding them.
9. **Colours come from tokens:** read CSS custom properties with `getComputedStyle` at boot and convert them to sRGB floats for uniforms. There are no colour literals in shader or script source.
10. **Cheap tricks that work:**
    - nested shells at falling opacity (a simple fake glow);
    - a 0.5–0.7× off-screen particle buffer.

## Art on a light (white) ground
Drawing tide lines, dots and soft washes behind a ceramic studio's guide library inverts the usual problem: **dark text** sits on art that darkens the ground.
- **Grade each text line against the darkest background pixel under it,** and keep it at or above max(4.5:1, 0.75 × its contrast on plain white).
- **Pale decorative colours may fail contrast requirements on white.** Measure each colour in context before using it to convey meaning.
- **Keep the experiment** behind one switch until its readability and visual fit have been reviewed.

## Go deeper
- `03_skills/webgl-light-and-color/references/05-glow-and-light.md`: halo sprites, the one-profile pattern, the blend table, compositing, dither, colour space, tokens.
- **Licences:** check `03_skills/webgl-craft/references/10-licence-ledger.md` and verify the terms for each asset you actually use.
- **Record lessons:** tag your own light-and-colour notes `webgl-craft` and `webgl-light` so they remain easy to retrieve.
