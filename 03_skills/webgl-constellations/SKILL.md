---
name: webgl-constellations
description: Builds legible, interactive constellation and knowledge-graph figures (stars as items, clusters as groups, lines as relations) in SVG with an optional WebGL layer. Covers build-time seeded layout (shared SplitMix32), line rendering (gl.LINES is 1 px; instanced SDF capsules), linking rules (relative neighbourhood graph; no edge bundling), contrast and dimming math including the compounding-alpha trap, ranked light, focus+context and keyboard paths, Gestalt perception checks (no crossings, no enclosures, no congruent junctions, one end per star), matching painted art at display scale, and living-constellation motion (floating stars, transient signals, streaks). Use when designing or reviewing any star/node-link figure. Part of the webgl-craft cluster.
---

# Constellations that stay legible (and can come alive)

## When to use this skill (and when another one)

| You are… | Use |
|---|---|
| laying out, drawing, linking, dimming or animating a star/node-link figure | **this skill** |
| the hover/pin/readout wiring itself | `03_skills/webgl-interaction/SKILL.md` |
| the glow of each star | `03_skills/webgl-light-and-color/SKILL.md` |
| matching a painted plate's look | `03_skills/webgl-cosmic-art-direction/SKILL.md` |

## Rules (full detail and sources in `references/06-constellations.md` and `references/14-perception-and-living-constellations.md`)

1. **Solve the layout at build time** with a fixed seed. Emit SVG with class hooks, so every lighting state is a class toggle.
   - Share one **SplitMix32** between Node and the browser; Python's default Mersenne Twister does not produce the same sequence.
   - Better still, have the runtime **read the coordinates the build emitted**, and use the PRNG only for decoration.
2. **Lines:**
   - Treat `gl.LINES` as a 1 px option for portable rendering.
   - The default is **instanced SDF capsules:** per-instance endpoints, `exp(−d²/σ²)` edges, round caps, hover by id, a travelling light, and draw-in by discarding where `u > progress`.
   - Joints double-draw, so use premultiplied "over".
   - SVG draw-in uses `pathLength="1"`, once per screen, and only for dozens of paths.
3. **Links:**
   - Build-time links use a **relative neighbourhood graph.** Delaunay can make hairballs, an MST can be too sparse, and k-NN can fragment.
   - Runtime links use a squared-radius test, alpha ∝ 1 − d²/r², ends trimmed, and hysteresis (form at 100 px, break at 120 px).
   - **No edge bundling:** it hurts path tracing.
4. **Contrast** (WCAG 1.4.11 requires 3:1 for graphical elements needed to understand the content):
   - Dimmed **lines that fall below the contrast requirement** carry context only, never essential meaning.
   - Compute a safe minimum alpha for white stars against the actual background using the WCAG luminance formula.
   - **The compounding trap:** a 0.9-alpha star token × `opacity:.35` = 0.315 effective alpha. Testing 0.35 alone can miss a failure. Divide the required effective alpha by the token alpha to find the minimum multiplicative opacity, then verify the rendered result.
   - Measure against the real plate under each star. Colour is never the only carrier.
5. **Ranked light:**
   - As a rough design model, perceived brightness goes as I^0.5 for points, so "twice as bright" needs 4× the luminance. Tiers of about 1000:10:1 can provide a starting point; verify them at display scale.
   - Twinkle at 0.1–0.5 Hz, never more than 3 flashes a second.
6. **Focus+context and access:**
   - Siblings dim to a safe level and lit edges rise to about 0.9.
   - Reserve a readout band; Escape returns to the default story state.
   - Use roving tabindex over cluster → star, with relations in an equivalent accessible table.
   - Use 48 px targets. On mobile, redraw rather than shrink: tap to focus, tap again to clear.
7. **Perception (each one a build-time check):**
   - no crossings except at a shared end;
   - no star enclosed by lines that don't join it;
   - a doubled relation is one connection drawn as two close lines;
   - lanes ordered by span;
   - no two congruent junction patterns of the same size;
   - no line through a star it doesn't end on;
   - one end per star while its cluster has a free member;
   - layout constants emitted from the solver, never typed twice.
8. **Draw no relation the data doesn't hold.** Decorative or random connections stay inside the true relations, with "any" as an explicit flag for unrestricted decorative linking.
9. **Match the art at display scale:**
   - Mark sizes in displayed-plate units.
   - Measure star half-maximum width using the interpolated crossing.
   - The minimum contrast holds in every visible state.
   - DPR-1 line cells below the antialias footprint are reported as unmeetable.

## Living constellations (motion vocabulary; see `references/14-perception-and-living-constellations.md`)

- Floating stars (≤ 2.5 px, fixed DOM targets).
- Stable constellation lines inside each cluster.
- Transient signals between clusters: staggered, attach, wobble, fade; paused while a star is pinned.
- Faint background streaks.
- Testable through data attributes.
- **The static SVG figure stays the design underneath.**

## Go deeper

- `references/06-constellations.md`: layout, lines, links, the contrast table, ranked light, keyboard and mobile.
- `references/14-perception-and-living-constellations.md`: perception checks and the motion vocabulary.
- **Evidence:** verify graph-legibility claims against representative tasks before treating them as universal. Check accessibility requirements against the applicable WCAG criterion.
- **Reusable lessons:** tag your own constellation notes `webgl-craft` and `webgl-constellations` so they remain easy to find. See `03_skills/webgl-craft/SKILL.md` for the related skills.
