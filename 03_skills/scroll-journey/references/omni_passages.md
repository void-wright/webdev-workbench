# Passage prompts: making a clip fly instead of slide

A passage is one Frames to Video render in Google Flow: **start frame = stop A, end frame = stop B**. You (Claude) write the prompts; the human pastes them into Flow and downloads the results. This file is the craft.

## Vendor facts that shape a passage

All of these are **(as of October 2026; re-check before relying on it)**. Flow and its video model change often; when a fact here disagrees with what the human sees in Flow, believe Flow and update the package's `STATUS.md`.

| Fact | Value | Consequence |
|---|---|---|
| Mode | Flow's **Frames to Video**: a start image and an end image, and the model bridges them | the passage mechanism |
| Model name | the video model was offered in Flow as "Omni" | name it in `HANDOFF.md` as the human sees it |
| Clip length | 10 s maximum per generation | a passage is at most 10 s raw; 8 s is the default (see below) |
| Resolution | 720p native; 1080p is an upscale | the 1080p tier adds bytes more than detail |
| Aspect ratios | 16:9, 9:16, 1:1, 4:3, 3:4 | desktop passages at 16:9, phone passages at 9:16 |
| Ingredients | at most 3 images per prompt | a passage uses 2 (stop A and stop B); add a third only if a recurring identity truly needs it |
| Audio | generated natively, even when the prompt says "Silent" | always strip it at encode (`-an`); never block on it |
| Watermark | an invisible watermark on every output | check each export for any *visible* mark anyway |
| Editing a take | quality drifts after a few conversational edit turns | start a fresh generation instead of editing again |

**Measure, never assume:** the size, frame rate, real length, audio track and end-frame adherence of a render are facts about the clip you got, not about the model in general. Read them from the file with `ffprobe` and the render gate (`pipeline.md`), and compare the first and last frames against stop A and stop B before you trust a passage. Your own probe (below) is the measurement that counts.

**Why 8 seconds when the reader may scroll past in one?** The reader's scroll sets the pace, not the clip's length. Eight seconds simply gives enough frames that a slow scroll stays smooth. A longer journey comes from more scroll distance per passage (`--sj-pass`), not from a longer clip.

## The passage contract

1. **Start frame = stop A's painted still; end frame = stop B's.** Hand Flow the exact files from `ingredients/`, never a re-export.
2. **Silent and wordless.** No voice, no music, no lettering. The copy is HTML.
3. **Camera travel is the point.** Both ends are pinned, so the camera may fly forward, rise, descend, orbit or pull back between them. (A *loop* is the opposite: a locked camera. Do not carry the loop habit into a passage.)
4. **Upright and level. No roll, ever.** A rolled camera never settles back onto a level still, and roll is unforgiving under scrubbing. The *paint* may turn; the *view* never tilts.
5. **Motion from the first frame, eased at both ends, no written holds.** The page's stills already do the holding.
6. **The travel medium is the scene's own material, flown through:** cloud, mist, shafts of light, falling motes, watercolour pigment. It carries the join. Never a separate veil that covers the view and recedes: that reads as a cross-dissolve.
7. **Nothing new appears** that is in neither stop.

## The five-part prompt

State the ingredients before the prompt, then fill five parts in order. Every prompt is **self-contained and copy-paste complete**: palette and composition restated inline, because the model carries nothing between renders. End with `Silent.`

```text
INGREDIENTS (upload these first)
  start frame: <package>/ingredients/S0_16x9.png   (name it s0_16x9 if Flow allows names)
  end frame:   <package>/ingredients/S1_16x9.png   (name it s1_16x9)

GOAL: An eight-second silent, unbroken flight through <the world, in its own terms>. The camera
travels from the scene in @s0_16x9 into the scene in @s1_16x9 in one weightless glide. It must feel
like moving through real depth, never like sliding across a flat picture, and never like one
picture dissolving into another.

INPUT ROLES: The start image (@s0_16x9) is the exact first frame and the end image (@s1_16x9) is
the exact last frame. They set the palette, the ground and the brushwork of every moment between
them; everything in between is the same world seen as the camera travels through it.

SCENE: <The world: the ground, the medium at many depths, near and far.> <How the medium is alive
in THIS passage.> At the start, <what is actually painted in stop A, where>. At the end, <what is
actually painted in stop B, where, and which side is calm and open>.

MOTION: From the very first moment, the camera <one move, with a direction measured from the
stills>, gathering into a smooth, steady glide and never stopping until it eases to rest in the
last moment. <A depth cue: near material sweeps past quickly while far material drifts slowly.>
<What the medium does as we pass through it.> <The one change that belongs to this journey: a form
gathers, a light wakes.> As the last of it thins, the camera slows softly and comes to rest exactly
on @s1_16x9.

CONSTRAINTS: One continuous flight with smooth, constant movement and no pauses, cuts,
cross-dissolves or jumps; graceful and unhurried, never fast or jerky. The camera stays upright and
level, with no roll. <Only one bright light; no extra lights, badges, discs or rings appear.>
Palette: <each colour by name and hex, with where it may appear>. These are the only colours in the
clip. <Medium and finish>, matching the two images. Silent.
```

### Takes A and B

- **Take A** is the default, written in full: the majestic version.
- **Take B** is a **replacement MOTION paragraph only**: the same choreography, bigger and more sweeping. Never a different move, so the two takes differ in one variable.
- Render take A first. Render B only where A misses or when the human wants a comparison.

### Phone passages (9:16)

Write each phone prompt **in full** so every block pastes as it stands. Phones favour the vertical (climb, descend, rise, tip) where the choreography allows, and keep the subject in the upper part with the lower part calm for the words. Measure the phone stills' focal points too. Cropping to 9:16 often moves the focal light sideways between the two stills, so a passage you would describe as "straight ahead" may need a sideways drift, or the prompt will fight its own end frame.

## The flight doctrine (why the template reads this way)

Each row pairs a common request with the defect it tends to produce, and what to ask for instead.

| Asked for | What came back | Ask instead |
|---|---|---|
| "a passage across one landscape", "camera eases right, the scene slides left" | a flat sideways pan across a picture | a flight **through depth**: forward, rise, descend, orbit or pull back, with material at many depths |
| "a wash blooms over the view, veiling it, then recedes" | a cross-dissolve: one picture morphing into the next | the camera flies **through the scene's own material**; no separate veil; and ban "cross-dissolves" by name in CONSTRAINTS |
| "scale changes by no more than a sixth" | almost no depth | no cap: let forms grow and pass the edges of the view |
| "every form keeps its own shape; only the mist moves" | frozen shapes | the medium is **alive**: it blooms, spreads, curls, pools, condenses, unspools |
| half a second of hold at the start, a second at the end | dead air, then a lurch in the middle | motion from the first frame, eased in and out, **no written holds** |
| "slow", "gently" six times | a timid clip | "graceful, unhurried, never stopping" |
| a camera direction with no depth cue | it decays into a pan | pair every camera cue with a depth cue: near material fast, far material slow |
| a direction chosen from the board's sentence | the clip fought its own end frame | choose the direction from **where the focal light actually sits** in each still (measure its x position) |

## Words that invite the wrong thing

Naming a thing you do not want invites it. Describe empty areas as what they are ("open, calm, bright white space"; "a calm dark sky").

- **Text and interface:** title, words, letters, lettering, sign, logo, label, caption, UI, "text-free", "no text".
- **Gallery furniture:** website, page, painting, frame, canvas edge. Say "the scene in @s1_16x9", not "the painting @s1_16x9".
- **Water, over any horizon or band of light:** waves, pours, drops, falls, pools into a pond, river, sea. Phrases such as "in two soft waves" or "pours into a pool" tend to paint waterfalls and ponds. Prefer "beads of pigment" or "motes of light" to "drops" or "flakes".
- **Objects by another name:** renaming a banned noun while keeping its verbs smuggles it back. If you ban "curtain" but still write "parts, folds, draws aside", expect a curtain.
- **Roll:** roll, spin, barrel, corkscrew, tilt the horizon. Where the material turns, write "the cloud turns; the view never tilts".
- **Extra lights:** an unbounded "stars" invites badges and discs. State the count: "only one bright light".

## Describe what is painted, not what was planned

Read every still before writing its sentence. A prompt that describes the planned frame instead of the painted one makes the model fight the end frame, and the probe then measures your contradiction instead of the model. If a still has an accidental feature (a loop that reads as an eye, a faint band of haze), describe it neutrally ("a loose loop around an open gap") and never with a word that strengthens the misreading.

## The choreography menu

**Every passage gets its own choreography**: one camera move plus one way the medium behaves. Two passages that share a move feel like a repeat even when the stills differ. Pick from this menu (or invent), and record each pick in the uniqueness ledger.

| # | Camera move | A medium behaviour that pairs with it |
|---|---|---|
| 1 | a slow push in toward the centre of the scene | fog thins ahead of the lens and closes softly behind it |
| 2 | a slow pull back that reveals the whole scene | near leaves or dust drift out of frame as the far scene comes into view |
| 3 | a crane up from near the ground to a high, level view | falling snow or petals slow and hang in the air as the camera rises past them |
| 4 | a crane down from above, settling at eye level | shafts of light shorten and soften as the camera descends into them |
| 5 | a sideways track through depth past near foreground shapes (never a flat slide across a picture) | near shapes pass the lens quickly while the far scene barely moves |
| 6 | a rack focus from a near element to the far scene, with a gentle forward drift | the near element melts into soft discs of light as the far scene sharpens |
| 7 | a dissolve through light: a forward drift into a bright haze that clears on the end frame | brightness blooms, holds for a moment, then falls away to reveal the new scene |
| 8 | a dissolve through texture: a forward drift into a close surface (paper grain, frost, cloth) | the texture fills the frame, then thins to reveal the new scene behind it |
| 9 | a match on shape: the camera holds on a form whose outline the next scene shares | the medium settles into the shared outline before the new scene resolves around it |
| 10 | a slow descent through falling motes | motes soften into beads of pigment that fall and bloom where they land |
| 11 | a low glide forward close to the ground | grass, sand or dust stirs in the camera's wake and settles behind it |
| 12 | a level rise over a near edge (a hill, a wall, a cloud top), then a sink beyond it | dark pigment spreads like ink dropped into water and granulates |
| 13 | a long forward drift while a dense layer crosses the view | the dense layer thins and opens from the middle outward; light spreads through the gap |
| 14 | a slow pull back through layers of mist, each layer passing the lens | mist sheets separate and drift apart, revealing the far form behind them |

On a dark ground the medium is usually cloud, mist, veils of light, dust and motes; on a white page it is the scene's own watercolour pigment (see `white_ground.md`).

## The uniqueness ledger

Put this table at the end of `HANDOFF.md` and check every new passage against it. No two rows may share a camera move, and no two may share a medium behaviour.

| Passage | Camera move | Medium behaviour |
|---|---|---|
| P1 | | |
| P2 ★ (peak) | | |
| P3 | | |

## Probe first

End-frame adherence, real clip length, audio and the feel of the motion are unknown until one render is measured. **Before the human renders the batch:**

1. Write all the prompts, audit them (`qa_checklist.md` part A), and mark the **hardest** passage as the probe (the biggest change of scale or composition between its two stills).
2. The human renders the probe at 16:9, take A, and stops.
3. Gate it (`pipeline.md` § The render gate) and read its 2 fps contact sheet.
4. Decide on the result:
   - **lands and flies** (or is repairable): render the rest on this doctrine;
   - **flat, a slide, or a dissolve:** the doctrine is wrong. Rewrite the MOTION approach across the whole handoff, re-audit, probe again. A probe that comes back static or choppy usually means the prompt asked for a pan instead of a flight through depth. Fix the doctrine before the batch, so the other renders are written on the fixed version instead of the broken one;
   - **ignores the end frame:** fall back to start-frame-only passages for the stubborn seams and let `seam_repair.py` bake a short crossfade onto the next still.

## The HANDOFF.md shape (written for the human)

1. **What this is:** one table, one row per render: `Prompt ID | what happens | start → end still | move | aspect | length`.
2. **Render order:** the probe first and stop; then everything else, take A first everywhere.
3. **How to run each one in Flow** (re-check these steps against Flow's current screens, as of October 2026):
   1. Open **Frames to Video**. Put the section's **start** still in the start-frame slot and its **end** still in the end-frame slot, from the paths given.
   2. If Flow lets you name the two frames, name them as the section does (without the `@`). If it does not, paste the prompt unchanged: it also describes both stills in words.
   3. Paste the take A prompt (the whole code block). For take B, paste the same prompt with its MOTION paragraph swapped for the take B paragraph.
   4. Set the aspect and **8 seconds**. If 8 s is not offered, pick the next length up; the pipeline trims. Turn audio off if there is a switch; if there is none, that is fine.
   5. Download the MP4 into `renders/` as `<PromptID>_<16x9|9x16>_<A|B>_take<N>.mp4`, N being the attempt number.
   6. If a take wanders, start a **fresh generation** rather than editing it again.
4. **What happens after:** the gate, the mechanical pass, the page build (one short paragraph each).
5. **One section per render:** the two ingredient paths with their names, the take A prompt in a code block, the take B MOTION paragraph in a code block, the length, the aspect, the filename.
6. **Notes:** why the prompts read this way, and the uniqueness ledger.

## Worked example 1: a white page (an invented seed library)

Stop S0 (words left): a loose cluster of pale green seed pods, painted in watercolour, floating on the right in bright white space. Stop S1 (words right): one young seedling of soft green washes unfurling on the left, a faint ochre glow at its base.

```text
INGREDIENTS (upload these first)
  start frame: ~/journeys/seed-library/ingredients/S0_16x9.png   (name: s0_16x9)
  end frame:   ~/journeys/seed-library/ingredients/S1_16x9.png   (name: s1_16x9)

GOAL: An eight-second silent, unbroken flight through a bright world of living watercolour. The
camera travels from the scene in @s0_16x9 into the scene in @s1_16x9 in one weightless glide. It
must feel like drifting through deep, luminous space, never like sliding across a flat picture, and
never like one picture dissolving into another.

INPUT ROLES: The start image (@s0_16x9) is the exact first frame and the end image (@s1_16x9) is
the exact last frame. They set the palette, the white ground and the loose watercolour brushwork of
every moment between them; everything in between is the same world seen as the camera travels
through it.

SCENE: An endless, bright white space with soft clouds of green and ochre watercolour pigment
floating in it at many depths, near and far. The pigment is alive: it softens, splits like a pod
opening, and curls outward in slow feathered tendrils, as if being painted while we watch. At the
start, a loose cluster of pale green pods floats on the right, the left side open white space. At
the end, a single young seedling of soft green washes unfurls on the left, a faint ochre glow at
its base, the right side open white space.

MOTION: From the very first moment, the camera floats forward into the cluster of pods and curves
gently to the left as it goes, gathering into a smooth, steady glide and never stopping until it
eases to rest in the last moment. The nearest pods swell and slip past the edges of the view while
the far ones drift slowly, so the space feels deep. One pod opens as we pass it and its pigment
curls ahead of us into a single green tendril, which grows, leans and unfurls into the seedling as
its ochre glow warms at the base. As the last tendrils thin, the camera slows softly and comes to
rest exactly on @s1_16x9.

CONSTRAINTS: One continuous flight with smooth, constant movement and no pauses, cuts,
cross-dissolves or jumps; graceful and unhurried, never fast or jerky. The camera stays upright and
level, with no roll. The ground is bright, clean white light at both ends, and the pigment clears
from the top and bottom edges by the last moment; no grey or tinted veil settles over the white.
Only one seedling; no extra plants, discs or rings appear. Palette: white #FFFFFF; pale green
#CFE3C8; leaf green #5C8C60; deep green #2F5A3A only in the deepest pigment; ochre #C89B45 only as
the small glow at the seedling's base. These are the only colours in the clip. Loose, luminous
watercolour throughout, matching the two images. Silent.
```

Take B (replace the MOTION paragraph):

```text
MOTION: From the very first moment, the camera floats forward into the cluster of pods and sweeps
left in one wide, graceful arc, never stopping until it eases to rest in the last moment. The pods
rush past on every side, the near ones quickly, the far ones turning slowly. Every pod opens as we
pass and their pigment streams ahead in long green tendrils that braid together, rise and unfurl
into the seedling as its ochre glow warms at the base. As the last tendrils stream aside, the camera
slows softly and comes to rest exactly on @s1_16x9.
```

## Worked example 2: a dark ground (an invented astronomy club)

Stop S1 (words right): a soft violet-blue nebula on the left with one bright star at its heart. Stop S2 (words left): a slow arc of faint stars on the right, one of them gold.

```text
MOTION: From the very first moment, the camera rises up and over the top edge of the nebula,
drifting a little right, gathering into a smooth, steady glide and never stopping until it eases
to rest in the last moment. Near wisps of the nebula sweep beneath the lens quickly while its far
body sinks away slowly. Beyond the edge the sky opens and the camera sinks gently toward a slow arc
of faint stars, which brighten one after another as we approach, the last one warming to gold. As
the final wisps thin, the camera slows softly and comes to rest exactly on @s2_16x9.
```

The other four parts follow the template, with the dark palette restated by role and hex, each colour with where it may appear: the ground (the open sky), the one or two nebula colours, the star colour, and the single accent reserved for the one gold star. Take the hex values from your own stills and tokens, never from an example.
