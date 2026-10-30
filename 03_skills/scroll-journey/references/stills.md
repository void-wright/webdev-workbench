# Painting the stops

Every stop is a finished picture that stands alone: the hold the reader rests on, the poster, the reduced-motion image, the no-script image and the phone fallback. It is also the exact first or last frame of a passage, so it decides what every clip must land on. Paint the stops before any passage prompt is written, and never change a still after its passages are rendered.

Any image tool works if it can paint at 16:9 and 9:16 and, ideally, edit from a reference image. Which tools exist, what they cost and how they are reached changes often (as of October 2026; re-check before relying on it).

## Sizes and names

| Still | Size the template expects | File in the site | File in the package |
|---|---|---|---|
| wide (16:9) | 1376 x 768 or larger, same aspect | `src/assets/journeys/<slug>/s0-w.jpg` | `ingredients/S0_16x9.png` |
| phone (9:16) | 768 x 1376 or larger, same aspect | `src/assets/journeys/<slug>/s0-p.jpg` | `ingredients/S0_9x16.png` |

If your stills have a different aspect, change `--sj-ar` (wide) and its portrait value in the component to width / height. Keep lossless masters (PNG); the site build makes the AVIF, WebP and JPEG sizes. The files in `ingredients/` are **byte-copies** of the masters the human uploads to Flow: copy them, never re-export, because a re-save (for example JPEG quality 75) adds 8 x 8 block noise that the seam check will then measure.

## One style block for every stop

Write one style block and paste it, unchanged, into every still prompt:

```text
MEDIUM: [watercolour on white / painterly digital landscape / ...]
PALETTE: [named colours with hex, and where each may appear]
LIGHT: [direction, softness]
CAMERA: [lens feel, distance; a vast landscape seen from within, or a close study]
COMPOSITION: [16:9 or 9:16]; the forms on the [side]; the [other side] calm and open for words
CONTINUITY: one world; the ground's brightness the same in every stop
```

Describe what should be in the picture. Do not add a line like "no text, no logo": naming the unwanted thing invites it. If a model keeps adding lettering, reword the empty area as what it is ("open, calm sky").

## The calm side for words

The words sit on the painting, so each stop reserves a calm area for them:

- **Wide stills:** a calm left or right 40 % column (the component's `side: 'left' | 'right'`), or the open upper middle for a centred stop (`side: 'center'`, words at 38 % of the height).
- **Phone stills:** the calm lower part; the forms live in the **top third**. For a long stop (several sentences), the words can need the lower 55 to 60 % of a 390 x 664 screen, so the form must sit above about a third of the height. Measure your longest stop with the phone battery (`mobile.md`) before painting its phone still.
- **Alternate sides** from stop to stop (left, right, left, ...). It keeps the page lively, and it gives every wide passage a natural sideways drift. Write that drift into the board from day one.

Measure each still's words area before accepting it:

```bash
SJ="$HOME/.claude/skills/scroll-journey/scripts"   # the installed skill; from the unzipped package use 03_skills/scroll-journey/scripts
python3 -B "$SJ/stop_check.py" ~/journeys/seed-library/ingredients/S0_16x9.png --side left --theme light --paper
python3 -B "$SJ/stop_check.py" ~/journeys/seed-library/ingredients/S0_9x16.png --side bottom --theme light --paper
```

It prints the words area's luminance (mean, 5th and 95th percentiles), its busyness (standard deviation), the raw contrast of your text colour against the worst 5 % of that area, and, with `--paper`, the white of the top and bottom edges. Exit 0 means PASS. The bands are starting guesses: tiny specks or brush flecks can flag an area that reads fine, so read the numbers next to the picture.

## The focal point

Each stop has one focal point where the eye lands on arrival, and the passage into it should carry the camera toward it. Record it on the board as an x, y fraction. Keep it inside a safe central crop, away from the words' side. Treat a strong accent colour the same way: whatever single accent you choose, allow at most one or two small points of it per still and say so in the prompt ("at most one small spot of the accent colour"), or every passage has to manage the accent appearing and vanishing.

## Doors (a link over a painted form)

When a stop carries a link to another page, paint a form the reader can recognise and click, and record its box on the board as fractions of the painting: centre x, centre y, width, height, for the wide and the phone still separately (the data's `door.w` and `door.p`). On phones the door's name label sits just below the form's foot, so leave room under it, above the words.

## Matching the stops to each other

- **Ground brightness:** measure the open sky or paper of every stop and bring them close before any passage is written; otherwise every passage has to swim through a brightness change. One line in every prompt that names a single ground tone ("the open ground everywhere is the same pale warm grey, never near-black, never pure white") pulls the outliers back into line.
- **One world per journey:** treat the stops as places in one continuous landscape, at one scale. Small objects centred on blank ground make passages that only drift between props; a vast landscape seen from within makes a journey.
- **Abstract over literal:** abstract words such as "grid" or "network" pull a model toward hard lines and even spacing. Describe the material you want instead ("soft, uneven brushstrokes, never straight, never evenly spaced") and ban evenness.

## Re-roll tactics

1. Paint 2 or 3 style samples (the first, a middle and the last stop). The human approves the look before the rest are painted.
2. When a still misses, change one thing in its prompt and re-roll.
3. After two misses on composition (the model keeps a form on the wrong side), stop re-rolling: give the model its own best take in edit mode with one instruction ("move the cluster to the centre; keep everything else"). One targeted edit often succeeds where several re-worded prompts do not.
4. If the margin is bare ground, a deterministic fix is fine: shift the pixels and pad with the ground's own colour. Then re-measure.
5. Record which take was chosen and why in `STATUS.md`.

## Placeholders while you wait

To build and lay out the page before the paintings exist:

```bash
SJ="$HOME/.claude/skills/scroll-journey/scripts"   # the installed skill; from the unzipped package use 03_skills/scroll-journey/scripts
python3 -B "$SJ/placeholder_stills.py" src/assets/journeys/seed-library --stops 4 --theme light --sides l,r,l,c
```

Run it from the site folder. It writes labelled stand-ins (`s0-w.jpg` ... `s3-p.jpg`) with the form away from the words. Replace every one before shipping.
