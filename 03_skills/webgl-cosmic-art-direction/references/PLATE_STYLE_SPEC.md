# Translating approved artwork into web graphics

Use approved artwork as the visual reference for related static assets and interactive graphics. Preserve its visible proportions, texture, edge softness and light behaviour across implementations. Compare the reference and rendered result side by side at their intended display sizes.

## Define the visual language

Choose motifs to suit the site's subject. Possible directions include photographic details, abstract shapes, diagrams, textured surfaces or illustrative marks. Treat these as options, not a required set. An amateur astronomy club might use an observation sketch as its reference when that supports the page's purpose.

Identify visually distinct classes before measuring them. Fine lines, soft patches and compact bright marks may each need different rendering parameters. Measure each class independently and compare equivalent classes across references. An average across unlike elements can describe none of them accurately.

Choose colour tokens by their roles and relationship to the artwork. Names such as `surface`, `text-primary`, `line-muted` and `accent` communicate intent. Sample candidate colours from the reference, then validate them in the finished composition. Raw token values alone do not establish a match.

## Measure what appears on screen

Measure visible geometry and light profiles before selecting rendering parameters:

- Subtract the local background when sampling luminance profiles.
- Measure the core width, edge falloff and surrounding glow separately.
- Record opacity and apparent size alongside nominal dimensions.
- Exclude surrounding margins when measuring the artwork area.
- Express dimensions relative to that artwork area so they remain comparable at different display sizes.

A soft mark can appear much larger than its bright core. Matching only its nominal diameter can therefore produce the wrong result.

Compare final composited pixels with reference samples. Opacity and blend mode change the displayed colour, especially where elements overlap. Repeat comparisons over the actual backgrounds used by the page.

For measurement support, consult `03_skills/webgl-cosmic-art-direction/scripts/plate_style_probe.py`. Keep measurements attached to their visual class, sampled region and display scale so they remain interpretable.

## Finish the static design first

Build a complete static composition before adding animation. It should provide the intended appearance and readable content while the enhanced renderer is unavailable or still loading.

Apply the same measurements to the static fallback and enhanced output. Both should share the reference's proportions, light profiles and composited colours.

Match the enhanced renderer's initial frame to the static placeholder. Compare screenshots at the same viewport, crop and scale using both visual inspection and an image-similarity metric. Use the metric to locate discrepancies, then inspect whether those differences matter visually. Pay particular attention to alignment, edge softness and brightness at the moment the renderer appears.

## Choose rendering from interaction requirements

Decide what the user needs to interact with before choosing a medium.

| Requirement | Approach to evaluate |
| --- | --- |
| A fixed composition | A static image, SVG or CSS |
| Predetermined motion without independently interactive elements | Prerecorded media |
| Individual elements that respond to input | SVG, canvas or WebGL, according to complexity |
| Animated texture that must retain the artwork's character | Source-derived textures with selective rendering |

Prerecorded motion cannot make individual depicted elements independently interactive. Additional rendering systems introduce dependencies and asset costs, so inspect actual bundle and asset sizes before choosing them. If WebGL needs a thin utility layer, use a small WebGL helper of your own; none ships with this package.

Reuse an existing image resource when it also serves as a rendering texture. This can avoid a separate download of the base image, but it does not eliminate decoding or GPU upload work. Account separately for encoded asset sizes, supporting textures and GPU uploads.

## Preserve texture and control movement

When animation must retain the illustration's texture, derive reusable assets from that illustration. Keep the extraction process reproducible so those assets can be regenerated when the approved artwork changes.

Use masks to distinguish regions that may move from regions that must remain stable. Protect fixed details and areas behind readable content. Inspect animation throughout its range for smearing, exposed boundaries and movement across protected regions.

Keep interaction feedback within the established visual language. Compare resting and active states with the reference, checking that recognisable forms and proportions survive changes in position, brightness or scale.

## Check readability in motion

Test text against the final composited background, including moving layers. A resting state that passes a contrast check does not establish that animated states will pass.

Find the most obstructive animation state behind each text region. Calculate WCAG relative-luminance contrast from the composited foreground and background colours. Normal-sized text should meet at least **4.5:1**.

If motion reduces contrast, adjust the mask, text placement or supporting surface, then check the composition again.

## Make the handoff explicit

Use `03_skills/webgl-handoff-and-porting/SKILL.md` when preparing the rendering handoff.

Include:

- The approved artwork and a visual specification identifying which assets define the appearance.
- Each asset's role, such as reference, static placeholder, base texture, moving texture or mask.
- Measurements by visual class, including the artwork bounds used for normalisation.
- Colour-token roles, backgrounds and compositing assumptions.
- Allowed movement, protected regions and interaction limits.
- Static, initial-frame and active-state comparisons, plus contrast results.
- Bundle and asset sizes, resource reuse decisions and GPU upload considerations.

The handoff should make clear what each asset contributes and which visible properties the implementation must preserve.
