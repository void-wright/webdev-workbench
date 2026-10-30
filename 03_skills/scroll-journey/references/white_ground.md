# White-ground journeys: the paper is the page

Use this when the site's page is white and the journey sits directly on it, with no dark box around it. The governing rule: **every still's border, and every clip's first and last frame, must be the page's own #FFFFFF.** If a clip's white is even slightly grey or tinted, the clip shows on the page as a grey card.

## The stills

- Paint on bare white, with the forms never touching the top or bottom edge. Good stills have paper that reads at or very near 255, and `stop_check.py ... --paper` requires the 4 % bands at the top and bottom edges to have a 5th-percentile luminance of at least 248 (the `--paper-min` default).
- The left and right edges may carry colour on wide stills (they are the viewport's own edges). On phones they read as a card edge, which the component feathers (below).
- A white page still wants grandeur. Without an explicit clause, image models paint a tidy still life (a bowl, a cup, a sprig). If the journey should feel like a landscape, say so: "a vast landscape of watercolour clouds seen from within, layered near, middle and far, forms the size of continents".

## The prompts: call the ground light, not paper

This is the most expensive mistake to make on a white page. Prompts that call the ground "bright white paper", cap the scale change, keep every form's shape, and ask for a wash to bloom over the view and recede tend to come back static and choppy: a flat pan across a sheet plus a cross-dissolve. Ask for this instead:

- Call the ground **"an endless, bright white space"** or **"a sea of light"**, never "paper". With "paper", the model pans across a flat sheet.
- Fly the camera **through depth** (forward, rise, descend, orbit, pull back, skim), with pigment clouds at many depths.
- The travel medium is **the scene's own pigment**, flown through. No separate wash that veils and recedes.
- **The watercolour is alive:** it blooms, spreads, curls, pools, wicks, granulates and paints itself while we watch. Name one behaviour per passage and never repeat it (the uniqueness ledger in `omni_passages.md`).
- **Movement from the first frame**, eased in and out, never held.
- Ban **cross-dissolves** by name in CONSTRAINTS, and ban extra lights, badges and discs.
- **The white rule binds only the first and last frames.** Mid-flight, pigment may sweep across the edges; the component's stage mask fades the top and bottom into the page anyway. End CONSTRAINTS with: "The ground is bright, clean white light at both ends, and the pigment clears from the top and bottom edges by the last moment; no grey or tinted veil settles over the white."

The defences against a tint had become the cause of a dead clip. Measure only what the page needs (the end frames) and free everything between.

## The soft probe

Render the first passage at 16:9 before anything else, gate it within minutes with `seam_check.py --paper`, and read its contact sheet. If the white greys, tints or keeps a residue on the end frame, change the end-state clause in **every** prompt, re-audit and probe again.

## The mechanical order for a white passage

```text
seam_check --paper (raw)  ->  color_match --paper-lift  ->  seam_repair (both ends)  ->  web_normalize
                          ->  seam_check --paper (encoded)  ->  verify_web_media
```

The commands are in `pipeline.md`. Two facts from the toolkit's code:

- `seam_check.py --paper` judges the whole clip: the worst frame's 95th percentile luminance must be at least 248 (an encoded pure white reads about 253 after the yuv420 round trip) and the brightest tenth's tint at most 4. A grey veil or a cast is REPAIRABLE; paper darker than 235 is FAIL. A passage that flies through intentionally dark billows mid-flight can FAIL on `paper_dark` while its end frames are clean: read the contact sheet and the first and last frames before re-rendering it.
- `color_match.py --paper-lift` maps the clip's measured white to 255 per channel and leaves every value below the knee (default 236) untouched, so the pigment keeps its colour. Its self-test lifts a 239 paper to 253 while the coloured area moves by 2 levels (re-encode loss only).

## Not a fix: CSS multiply

`mix-blend-mode: multiply` over a #FFFFFF page is the identity: a frame whose paper is #FBFBFD stays #FBFBFD. It also darkens the stills' crossfade, because two multiplied stills overlapping darken to their product. Multiply is right only for an isolated watercolour element over a non-white or textured backdrop. Lift the clip's paper instead.

## What the component does on a light journey

- **Fades** every still and clip into the page at its top and bottom (a 12 % / 88 % mask).
- **Phones:** shows each phone still from its **top** (`object-position: 50% 0%` on both the still and the clip, so they stay registered), because the forms live in the upper part and the cover crop should lose the bare foot.
- **Phones:** feathers the **sides** as well (the top and bottom band intersected with a 16 % / 84 % side band), because phone washes that end in straight edges just inside the frame read as a card. A narrow side band (under about a tenth of the width) is usually not enough.
- **Words:** ink on a feathered paper veil. Wide: a radial veil. Phones: a full-width band of paper rising from the foot with a 3.5rem feathered top, because a radial veil thins at the block's top, exactly where a long stop's title sits. The veil's strength comes from the data (`veil: { wide, phone }`), set from measured contrast (`qa_checklist.md`).
