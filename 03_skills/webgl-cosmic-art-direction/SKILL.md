---
name: webgl-cosmic-art-direction
description: Use when matching interactive graphics to source artwork, preparing visual assets, or validating animation continuity.
---

# Match interactive graphics to source artwork

Treat the source artwork as the visual reference for the interactive layer. Measure its shapes, light, texture, and composition before choosing effects. Interaction should extend that visual language while preserving a complete, usable page.

## Choose rendering from the required behavior

List the behaviors the graphic needs to support, then choose the simplest rendering approach that supports them.

| Requirement | Suitable approach | Main validation |
| --- | --- | --- |
| Finished still composition | Image or SVG | Composition, cropping, and legibility |
| Predetermined ambient movement | Prerecorded animation | Visual fidelity, playback start, and loop closure |
| Pointer, focus, or interface responses | Live SVG, Canvas, or WebGL | State behavior and visual continuity |
| Rich static detail with limited movement | Static artwork plus a live layer | Alignment and transitions between layers |

Prerecorded animation can move artwork convincingly, but it cannot by itself respond to individual interface targets. Identify which behaviors actually require live rendering before building the effect.

Bake detail that does not change. Animate only the regions or layers that need movement.

## Make the page complete before motion

Keep text and meaningful controls in the DOM. Every graphical destination should have a corresponding DOM link or button with a clear accessible name. A canvas may enhance the presentation, but it should not be the only place that text or navigation exists.

Provide a finished static presentation before animation initializes. Compare the first animated frame with that presentation for changes in crop, brightness, position, or composition. Loading the animated layer should not make the artwork jump.

For reduced motion, show a meaningful completed composition. If animation reveals relationships or destinations, those relationships and destinations must remain available when motion is disabled.

If you need one, a wrapper component holds the canvas and its fallback; give it a descriptive name (for example `LayeredArt`). Let DOM controls own interaction state and pass that state to the visual layer.

## Define the visual vocabulary

Choose motifs according to the site's subject. Possible directions include material textures, botanical forms, geometric arrangements, landscape contours, drawn marks, or abstract light. These are options to investigate, not a required set.

For a ceramic studio, glaze texture or the curved profile of a vessel might provide a useful starting point. Use a motif only when it helps explain the content or establish the intended atmosphere.

Use `03_skills/webgl-cosmic-art-direction/references/07-motifs.md` as a place to consider motif options. Record the selected vocabulary and its measurable properties in `03_skills/webgl-cosmic-art-direction/references/PLATE_STYLE_SPEC.md`.

Choose colors from the source artwork and the page's readability needs. Name tokens by purpose, such as surface, text, accent, filament, and halo. Distinguish an element's core color from its surrounding glow rather than treating them as one color.

Preserve this vocabulary during interaction. Hover and focus can change brightness, opacity, scale, or emphasis, but should not unexpectedly introduce a different shape language or unrelated effect.

## Measure before matching

Measure representative regions of the source artwork and compare them with rendered output at its intended display size.

Useful measurements include:

- Shape, curvature, and orientation.
- Core width and surrounding glow falloff.
- Filament width and edge softness.
- Texture density and grain.
- Color and local contrast against the background.

Measure distinct parts separately. A narrow bright core and a broad faint halo have different visual roles. A single width measurement can hide a mismatch between them.

For a brightness cross-section, estimate the local background before locating half-maximum crossings. Interpolate between adjacent samples that straddle the threshold rather than rounding to whole pixels. Measure the halo separately from the core, and record the method so later comparisons use the same definition.

Group elements by role before comparing distributions. Small background points, prominent focal points, and interactive destinations should not share one average size or brightness target. A mismatch in the mix of roles can make an otherwise accurate rendering appear incorrect.

Use these paths for the related measurement work, inspecting their interfaces before running them:

- `03_skills/webgl-cosmic-art-direction/scripts/plate_style_probe.py`
- `03_skills/webgl-cosmic-art-direction/scripts/figure_star_probe.py`

For light profiles and color handling, consult `03_skills/webgl-light-and-color/SKILL.md`. For graphics organized as points and relationships, consult `03_skills/webgl-constellations/SKILL.md`.

## Prepare textures and edited assets

Reuse source artwork as a texture when it helps the live layer match the static composition. Confirm that the initial rendered frame preserves the source's appearance. Reusing an existing asset may avoid a separate download, but exported crops and sprites still add bytes and should be counted.

Keep deformation local. Use a mask to restrict image displacement to regions intended to move, with suitable transitions at the mask boundaries. Inspect stationary details throughout the motion to detect smearing or unintended drift.

For asset preparation, review the relevant workflow at:

- `03_skills/webgl-cosmic-art-direction/scripts/calm_plate.py` (needs Python 3 with `numpy`, `Pillow` and `scipy`: `python3 -m pip install numpy pillow scipy`)
- `03_skills/webgl-cosmic-art-direction/scripts/cloud-sprites-from-plate.mjs`

Save edited assets with resolution, color handling, and encoding quality appropriate to the source. Avoid repeated lossy saves during editing.

Validate repaired regions locally. Compare channel values and local brightness maxima with nearby clean regions of similar texture. Derive tolerances from those regions rather than choosing an arbitrary universal threshold. Look for bright residuals, color smudges, softened patches, and repeated texture. Restore matching grain where cleanup has made the repair conspicuous.

## Align geometry with the displayed artwork

Source-image coordinates are not display coordinates. Map image-derived geometry through the actual scale, crop, alignment, and container position.

For a source image of size \(W_i \times H_i\) displayed in a container of size \(W_c \times H_c\):

- With `object-fit: cover`, the scale is `max(Wc / Wi, Hc / Hi)`.
- With `object-fit: contain`, the scale is `min(Wc / Wi, Hc / Hi)`.

Apply the offsets produced by the live `object-position`, then include the container's position in the coordinate system used by the overlay. Recalculate when layout changes.

Check alignment at visible boundaries as well as interior landmarks. Where a rendered line continues a painted line, measure both positional offset and angular mismatch. Correct positions alone will not hide a sudden change in direction.

For adjoining images, measure perceptual color differences across corresponding edge regions. Then inspect the seam at its displayed size. Similar average colors can still conceal discontinuities in texture, gradients, or line direction.

## Keep motion coherent

Let scroll events update animation parameters or target values. Read those values in the existing render loop. Do not create a second rendering mechanism inside the scroll handler.

For looping motion, verify closure across all animated elements. If the intended loop duration is \(T\), each periodic element with period \(P_i\) should satisfy:

`T / Pi = an integer`

Also check nonperiodic state such as particle resets, noise evolution, fades, and camera movement. A seamless loop needs compatible positions and appearance at the boundary, with continuous motion where appropriate.

Symmetry can shorten a loop only when repeated elements are visually interchangeable. Different textures, labels, brightness levels, or interaction states can invalidate that assumption.

Compare the start and end frames, then watch the boundary in motion. Matching still frames does not prove that velocity or fading remains continuous.

## Evaluate the full page

Keep ambient effects switchable during evaluation. Compare the complete page with the effect enabled and disabled, including text, controls, imagery, and spacing. An attractive isolated animation can still distract from the page or alter its intended character.

Validate these states:

- Static presentation before initialization.
- First animated frame.
- Resting, pointer, and keyboard-focus states.
- Reduced-motion presentation.
- Responsive crops and resized containers.
- Loop boundaries and adjoining image seams.

Use both measurements and visual inspection. Measurements locate mismatches; inspection determines whether they matter in context.

## Record reusable evidence

Adapt principles from references while deriving implementation details independently. Recalculate motion behavior for the current artwork and review applicable licenses before reusing code, textures, or other assets.

Record source measurements, display transforms, token roles, motion periods, asset settings, and accepted tolerances. Include failure modes and the checks that revealed them. Describe lessons in terms another project can apply without copying a site's identity.

When preparing a transfer to another developer or tool, use `03_skills/webgl-handoff-and-porting/SKILL.md`. Include the static reference, assets, measurement notes, interaction states, and validation criteria so the intended appearance can be reproduced and checked.
