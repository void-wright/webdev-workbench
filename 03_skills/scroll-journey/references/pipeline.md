# The pipeline: the render gate and the mechanical pass

Everything here runs on CPU with `ffmpeg`, `ffprobe`, `numpy` and `Pillow`. Run every tool as `python3 -B <tool>.py`; each has `--help` and `--selftest`. Exit codes: **0 pass, 1 fail (or "needs attention"), 2 usage**. Read return codes from a file or from `$?` right after the command, never through a pipe (a pipe reports the last command's status, not the tool's).

The commands below assume this package layout and these two variables. Set them once per shell:

```bash
SJ="$HOME/.claude/skills/scroll-journey/scripts"   # the installed skill; from the unzipped package use 03_skills/scroll-journey/scripts
PKG=~/journeys/seed-library
mkdir -p "$PKG/work/gate" "$PKG/work/mid" "$PKG/web"
```

- stills: `$PKG/ingredients/S0_16x9.png`, `S0_9x16.png`, `S1_16x9.png`, ...
- raw renders: `$PKG/renders/P1_16x9_A_take1.mp4`, `P1_9x16_A_take1.mp4`, ...
- passage `Pk` joins stop `S(k-1)` to stop `Sk`.

## Why the order matters

The repairs write high-quality intermediates (CRF 16). The web encode runs **last**, because re-encoding after it would destroy the short keyframe interval (GOP 8) that makes backward scrubbing cheap. Boundary frames and seam checks for the site are taken from the **encoded** clip, never from the raw export.

## Part 1: the render gate (every raw take, before anything is encoded)

You see stills, not motion, so the gate is stills plus measurements, and you are the judge. For one take:

```bash
cd "$PKG"
ID=P1_16x9; RAW=renders/P1_16x9_A_take1.mp4; S=ingredients/S0_16x9.png; E=ingredients/S1_16x9.png
mkdir -p work/gate/$ID
python3 -B "$SJ/boundary_frames.py" "$RAW" work/gate/$ID
python3 -B "$SJ/contact_sheet.py" "$RAW" work/gate/$ID sheet 0.5 4 4
python3 -B "$SJ/seam_check.py" "$RAW" --start "$S" --end "$E" --json-out work/gate/$ID/seam_raw.json > work/gate/$ID/seam_raw.log 2>&1; echo $? > work/gate/$ID/seam_raw.rc
python3 -B "$SJ/blend_detect.py" "$RAW" > work/gate/$ID/blend.log 2>&1; echo $? > work/gate/$ID/blend.rc
python3 -B "$SJ/freeze_detect.py" "$RAW" > work/gate/$ID/freeze.log 2>&1; echo $? > work/gate/$ID/freeze.rc
```

On a **white page**, add `--paper` to the `seam_check.py` line.

Then **read** `work/gate/$ID/<take>-first.png` beside stop A, `<take>-last.png` beside stop B, and `sheet_sheet01.jpg` (16 frames, two per second). Decide each check:

| # | Check | How | If it fails |
|---|---|---|---|
| 1 | start seam: the first frame meets stop A | `seam_raw.json` `start.ssim` | REPAIRABLE if a nearby frame matches; else RE-RENDER |
| 2 | end seam: the last frame meets stop B | `end.ssim` | REPAIRABLE (trim and crossfade) or RE-RENDER |
| 3 | colour drift at both ends | `color_delta_max` (default bound 8 levels) | REPAIRABLE if uniform; RE-RENDER if local or the palette changes |
| 4 | one continuous camera move: no roll, no reverse travel, no hidden cut | the sheet; `scene_cuts` in the JSON | RE-RENDER |
| 5 | a flight, not a slide or a dissolve | the sheet; `blend.log` (`SOFT BLEND` lines) | RE-RENDER (rewrite MOTION, `omni_passages.md`) |
| 6 | nothing new appears: no extra lights, discs, shapes, lettering | the sheet, frame by frame | RE-RENDER |
| 7 | the passage reads as its board row and lands on stop B's focal point | the sheet | RE-RENDER |
| 8 | the calm side stays calm at the end | the last frame | RE-RENDER |
| 9 | audio | `has_audio` in the JSON | note only: the encode strips it |
| 10 | length and size | `duration`, `width`, `height` in the JSON | record; RE-RENDER only if no usable trim window exists |
| 11 | no frozen span mid-travel | `freeze.log` | RE-RENDER if the freeze sits mid-flight |
| 12 | no visible watermark | the sheet | ask the human (an assumption failed) |
| 13 | white page only: the paper is #FFFFFF at both ends, no grey veil or tint | `paper` in the JSON | grey or tint: REPAIRABLE (paper lift); darker than 235 or residue on the end frame: RE-RENDER and re-word the end-state clause in every prompt |

**Reading the two detectors:** both are evidence for your eye, not verdicts. `blend_detect.py` finds a dissolve by its signature (motion up while edge sharpness drops), so it needs texture: a dissolve between two soft, smooth shapes can pass it unseen, and the contact sheet is what catches that. `freeze_detect.py` calls any span whose mean grey change per frame is under 1.0 (out of 255) frozen, so a very slow, smooth drift can read as one long freeze. A freeze only matters when the sheet shows the camera stopping mid-flight.

**Reading `seam_check.py`:** its verdict is in the JSON. `PASS` = both seams at or above 0.90 SSIM, colour within 8 levels, no cut, no audio. `REPAIRABLE` = seams at or above 0.75 and no cut, but something else is off (it exits 1, so read the JSON, not only the code). `FAIL` = a seam below 0.75 (the clip lands somewhere else) or a hidden cut. A raw Flow export is usually `REPAIRABLE` for one reason only: `audio_stream`.

**Calibration (starting points from the toolkit's own self-tests):** two unrelated images score SSIM about 0.62, so 0.75 is the floor below which a crossfade cannot honestly repair a seam. Ordinary adjacent frames of moving content score 0.90 to 0.94. A passage that truly lands on its stills should score well above that floor at both ends, and a repaired, web-encoded seam usually stays in the high 0.8s or 0.9s. These bands are starting points: read the two frames side by side before trusting a number, and when a number passes but the picture is wrong, believe the picture. Every measured check can pass while the eye still finds an invented glow or faint tiling lines mid-flight.

**Verdicts:** `PASS`, `REPAIRABLE` (a mechanical fix restores the seam without changing what the passage is), or `RE-RENDER` (write notes, change **one** thing in the prompt, re-audit it, the human renders a fresh take). Three failures for the same reason on one passage: stop and bring the human the takes, the numbers and the diagnosis. Log every repair and re-render with its root cause in `STATUS.md`.

## Part 2: the mechanical pass (every gated take)

Nothing creative happens here. Anything that needs taste goes back to the board or to a re-render.

### Step 1, white pages only: lift the paper

```bash
cd "$PKG"
python3 -B "$SJ/color_match.py" renders/P1_16x9_A_take1.mp4 work/mid/P1_16x9_c.mp4 --paper-lift > work/gate/P1_16x9/color.log 2>&1; echo $? > work/gate/P1_16x9/color.rc
```

Pass line: `paper_after=` shows `paper_p95_min` of 252 or more. On a dark ground skip this step (use the raw file as the input to step 2). Use `--ref STILL` (a whole-clip grade toward one still) only when the drift is uniform across the clip; a grade toward stop A can break a tail that already matches stop B, and the both-ends repair below usually makes it unnecessary.

### Step 2: repair both seams

Run it on **every** passage, at both ends, not only the failing ones. It searches the first and last 24 frames for the best match to each still, trims there, and bakes an 8-frame crossfade so the clip's first frame **is** stop A and its last frame **is** stop B. It costs about two frames and turns every poster-to-clip handoff into a non-event.

```bash
python3 -B "$SJ/seam_repair.py" work/mid/P1_16x9_c.mp4 work/mid/P1_16x9_r.mp4 --start ingredients/S0_16x9.png --end ingredients/S1_16x9.png > work/gate/P1_16x9/repair.log 2>&1; echo $? > work/gate/P1_16x9/repair.rc
grep -E 'out_(start|end)_ssim' work/gate/P1_16x9/repair.log
```

Pass line: both `out_start_ssim` and `out_end_ssim` at 0.98 or above. The tool exits 1 whenever either is below its `--min-ssim` (default 0.99) even when the repair succeeded, so read the printed values. For a head or tail that drifted further, widen the fade with `--fade-frames 12`. (On a dark ground, the input is the raw render instead of `_c.mp4`.)

### Step 3: the web encodes, one per tier

The controller asks for three tiers, named to match the data file's `clips` pattern (`/video/<slug>/p{n}-{tier}-v1.mp4`).
The third tier is the 9x16 passage, so it needs its own repaired intermediate first. Run Part 1 on the 9x16 take
(`ID=P1_9x16`, the `_9x16` stills and render), then steps 1 and 2 above for it, which write `work/mid/P1_9x16_r.mp4`
(white page shown; on a dark ground skip the first command and give `seam_repair.py` the raw render instead):

```bash
mkdir -p work/gate/P1_9x16
python3 -B "$SJ/color_match.py" renders/P1_9x16_A_take1.mp4 work/mid/P1_9x16_c.mp4 --paper-lift > work/gate/P1_9x16/color.log 2>&1; echo $? > work/gate/P1_9x16/color.rc
python3 -B "$SJ/seam_repair.py" work/mid/P1_9x16_c.mp4 work/mid/P1_9x16_r.mp4 --start ingredients/S0_9x16.png --end ingredients/S1_9x16.png > work/gate/P1_9x16/repair.log 2>&1; echo $? > work/gate/P1_9x16/repair.rc
```

Then encode the three tiers:

```bash
python3 -B "$SJ/web_normalize.py" work/mid/P1_16x9_r.mp4 web/p1-16x9-v1.mp4 --width 1280 --height 720 > work/gate/P1_16x9/norm.log 2>&1; echo $? > work/gate/P1_16x9/norm.rc
python3 -B "$SJ/web_normalize.py" work/mid/P1_16x9_r.mp4 web/p1-16x9-1080-v1.mp4 --width 1920 --height 1080 > work/gate/P1_16x9/norm1080.log 2>&1; echo $? > work/gate/P1_16x9/norm1080.rc
python3 -B "$SJ/web_normalize.py" work/mid/P1_9x16_r.mp4 web/p1-9x16-v1.mp4 --aspect 9:16 > work/gate/P1_9x16/norm.log 2>&1; echo $? > work/gate/P1_9x16/norm.rc
```

Defaults (from the code): 24 fps constant, H.264 `yuv420p` limited range, a fixed keyframe every 8 frames with no scene-cut keyframes, CRF 22, no audio, `+faststart`, metadata stripped, and a 6 MB per-file budget (`--max-mb`, decimal MB) that makes the tool exit 1 if exceeded. Pass line: one line per file with no `OVER_BUDGET`, rc 0. Measured sizes per 8 s passage: about 1.4 MB at 1280 x 720, 3.3 to 4.3 MB at 1920 x 1080, about 1.4 MB at 720 x 1280.

Why H.264 with GOP 8: on a side-by-side scrub test the human could barely tell it from an all-intra encode (`--all-intra`, about 2.9 MB per 8 s) or a strip of WebP frames (about 2 MB, visibly softer), and it is the smallest and most compatible. If reverse scrubbing stutters on a target browser, try `--all-intra` for that tier. `--webm` and `--av1` write optional VP9 and AV1 twins; the template does not use them.

### Step 4: check the seams again, on the encodes

```bash
python3 -B "$SJ/seam_check.py" web/p1-16x9-v1.mp4 --start ingredients/S0_16x9.png --end ingredients/S1_16x9.png --json-out work/gate/P1_16x9/seam_web.json > /dev/null 2>&1; echo $? > work/gate/P1_16x9/seam_web.rc
```

Add `--paper` on a white page. Pass line: verdict `PASS` in the JSON. A seam at 0.88 to 0.90 after a CRF 22 encode is encode noise, not a landing error: read the two frames, and accept or re-encode with a lower `--crf`.

### Step 5: verify every web file

```bash
python3 -B "$SJ/verify_web_media.py" web --expect-fps 24 --expect-gop 8 > work/verify.log 2>&1; echo $? > work/verify.rc
tail -1 work/verify.log
```

Every check is measured from the file: codec, pixel format, no audio stream, `moov` before `mdat` (faststart), the largest keyframe interval, frame rate, bytes. Pass line: `files=N pass=N fail=0` and rc 0.

### Step 6: the route sheet

```bash
python3 -B "$SJ/route_sheet.py" --stops ingredients/S0_16x9.png ingredients/S1_16x9.png ingredients/S2_16x9.png ingredients/S3_16x9.png --passages web/p1-16x9-v1.mp4 web/p2-16x9-v1.mp4 web/p3-16x9-v1.mp4 work/route_16x9.jpg > work/route.log 2>&1; echo $? > work/route.rc
tail -1 work/route.log
```

One row per passage: stop, first frame, middle, last frame, next stop, with each seam's divider green or red and its SSIM printed. It needs exactly one more stop than passages. Pass line: `below_0.9=0`. Then **read** `work/route_16x9.jpg`. Repeat with the 9x16 stills and encodes.

## The whole journey in one loop

Once each take has passed the gate, this runs steps 1 to 5 for every passage and both aspects. Set `N` to the number of passages and `PAPER` to `--paper` on a white page or to nothing on a dark ground:

```bash
cd "$PKG"; N=3; PAPER=--paper
for k in $(seq 1 $N); do a=$((k-1)); for asp in 16x9 9x16; do id=P${k}_${asp}; S=ingredients/S${a}_${asp}.png; E=ingredients/S${k}_${asp}.png; mkdir -p work/gate/$id
  IN=renders/${id}_A_take1.mp4
  if [ -n "$PAPER" ]; then python3 -B "$SJ/color_match.py" "$IN" work/mid/${id}_c.mp4 --paper-lift > work/gate/$id/color.log 2>&1; echo $? > work/gate/$id/color.rc; IN=work/mid/${id}_c.mp4; fi
  python3 -B "$SJ/seam_repair.py" "$IN" work/mid/${id}_r.mp4 --start "$S" --end "$E" > work/gate/$id/repair.log 2>&1; echo $? > work/gate/$id/repair.rc
done
python3 -B "$SJ/web_normalize.py" work/mid/P${k}_16x9_r.mp4 web/p${k}-16x9-v1.mp4 --width 1280 --height 720 > work/gate/P${k}_16x9/norm.log 2>&1; echo $? > work/gate/P${k}_16x9/norm.rc
python3 -B "$SJ/web_normalize.py" work/mid/P${k}_16x9_r.mp4 web/p${k}-16x9-1080-v1.mp4 --width 1920 --height 1080 > work/gate/P${k}_16x9/norm1080.log 2>&1; echo $? > work/gate/P${k}_16x9/norm1080.rc
python3 -B "$SJ/web_normalize.py" work/mid/P${k}_9x16_r.mp4 web/p${k}-9x16-v1.mp4 --aspect 9:16 > work/gate/P${k}_9x16/norm.log 2>&1; echo $? > work/gate/P${k}_9x16/norm.rc
for asp in 16x9 9x16; do python3 -B "$SJ/seam_check.py" web/p${k}-${asp}-v1.mp4 --start ingredients/S${a}_${asp}.png --end ingredients/S${k}_${asp}.png $PAPER --json-out work/gate/P${k}_${asp}/seam_web.json > /dev/null 2>&1; echo $? > work/gate/P${k}_${asp}/seam_web.rc; done
done
python3 -B "$SJ/verify_web_media.py" web --expect-fps 24 --expect-gop 8 > work/verify.log 2>&1; echo $? > work/verify.rc
for f in work/gate/*/*.rc; do echo "$f $(cat "$f")"; done; tail -1 work/verify.log
grep -h 'out_' work/gate/*/repair.log
```

Change `_A_take1` to the take the gate chose for any passage that needed a re-render. The `.rc` files list every step's code: `color`, `norm*` and `verify` must be 0; `repair` and `seam_web` may be 1, in which case read `repair.log` (`out_*_ssim` at 0.98 or above) and the `seam_web.json` verdicts. This loop was run end to end on synthetic renders while the skill was built: every web file verified, every seam measured 0.996 on the route sheet.

## After the pass

Copy `web/*.mp4` into the site's `public/video/<slug>/` (see `build_astro.md`) and record in `STATUS.md`, per passage: the chosen take, the trim, every seam number before and after repair, the file sizes, and the gate verdict. When a clip changes later, encode it under a new version (`-v2`), update the data file's `clips` pattern, and never overwrite a published name: immutable caches would keep serving the old one.

## A looping banner instead (no journey)

For a short silent clip that loops in place, `loop_seal.py` crossfades the tail into the head, encodes it exactly as `web_normalize.py` does, and writes a frame-0 WebP poster no larger than 300 KB:

```bash
python3 -B "$SJ/loop_seal.py" renders/banner_take1.mp4 web/banner-v1.mp4 --fade 1.0 > work/loop.log 2>&1; echo $? > work/loop.rc
```

It passes when the sealed loop point is no worse than the clip's own worst ordinary frame step (minus 0.01). Loops want a **locked** camera with only light moving, the opposite of a passage.
