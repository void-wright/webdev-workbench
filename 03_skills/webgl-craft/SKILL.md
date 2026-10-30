---
name: webgl-craft
description: Router and home base for the WebGL craft cluster. Explains which of the seven WebGL skills to use for renderer selection and budgets, hardening and testing, interaction, light and colour, constellations, cosmic art direction, and handoff and porting. States shared design rules, common mistakes, evidence markers, and licence guidance. Use for browser 3D, canvas, WebGL, WebGPU, shader, particle, glow, starfield, constellation or animated-background work, or when unsure which WebGL skill applies.
---

# WebGL craft (the cluster router)

## Which skill (use them together freely)
| Task | Skill |
|---|---|
| choose HTML/SVG vs Canvas2D vs WebGL2 vs a library vs WebGPU; set frame/byte/DPR/particle budgets | `webgl-renderer-and-budget` |
| make a layer production-safe (static design first, boot, pause, reduced motion, context loss, a11y) and **test** it | `webgl-hardening-and-testing` |
| pointer and touch, springs, curl flow, hit-testing, hover-preview and click-pin, parallax | `webgl-interaction` |
| glow without bloom, halos, blending, dither, colour from tokens, art on a white page | `webgl-light-and-color` |
| star/node-link figures: layout, lines, links, dimming math, perception rules, living constellations | `webgl-constellations` |
| how it should look and move: match painted plates, clouds from the plate, motion metaphors, plate tools | `webgl-cosmic-art-direction` |
| brief someone else to build it, port a design-tool output, or send a painted banner to a video model | `webgl-handoff-and-porting` |

**A typical new layer uses them in this order:** art direction → renderer and budget → constellations and interaction (if it has a figure) → light and colour → hardening and testing. Bring in handoff and porting whenever another builder is involved.

## The shared doctrine (every skill assumes it)
1. **The fallback IS the design.** The static HTML/SVG/plate page is complete. The canvas only deepens it, and can vanish at any moment without loss.
2. **The canvas never carries text or meaning.** Words, labels and relations live in the DOM, and the canvas stays `aria-hidden`.
3. **The DOM owns state; the canvas follows** (one highlight uniform per role).
4. **Nothing runs during page load.** Interactive layers start on first intent. Ambient decorative layers start on first visibility, after load and idle. Reduced motion means no GPU rendering for these layers.
5. **Budget overdraw, not object count.** Cap DPR at 1.5, and use sprites instead of bloom chains.
6. **Treat research as leads.** Plausible technical claims can be wrong. Check primary sources and calculations before using a claim as a design constraint. Use VERIFIED marks only when that check is recorded.

## The ten biggest mistakes (`03_skills/webgl-craft/references/11-mistakes.md`)
1. treating fps measured in headless Chrome with SwiftShader as hardware GPU performance, or measuring on a device other than the intended target;
2. booting on load or directly in a scroll handler;
3. revealing the canvas before a proven first frame;
4. uncapped DPR and MSAA;
5. default square points and live per-node blur;
6. frame-rate-dependent motion and `setInterval` loops;
7. no reduced-motion path and no pause control (WCAG 2.2.2);
8. trapping page scroll with `preventDefault` on touch;
9. meaning where it can't be read: text in the canvas, dimmed lines carrying meaning, or compounded alpha making important connections disappear;
10. loading an engine from a runtime CDN dependency, or trusting performance figures without checking how they were obtained.

## Status markers used across the cluster
- **VERIFIED:** checked against a primary source, or recomputed. Record which kind of check supports the claim.
- **CONTRADICTED:** do not build on it.
- **UNSETTLED:** a lead that still needs checking.
- **ESTIMATE:** no supporting measurement. Per-device caps stay estimates until a real-device benchmark runs.

Record source URLs, the claim being checked, and the outcome together. A source check establishes what the source supports; it does not establish performance on your target hardware. See `03_skills/webgl-craft/references/00-how-to-read.md` for guidance on reading the reference material.

## The reference record (included guidance)
| File | What it is |
|---|---|
| `03_skills/webgl-renderer-and-budget/references/01-renderer-decision.md` | renderer choices and their tradeoffs |
| `03_skills/webgl-renderer-and-budget/references/02-performance-budget.md` | frame, byte, DPR and rendering budgets |
| `03_skills/webgl-hardening-and-testing/references/03-hardened-recipe.md` | production lifecycle, fallbacks and accessibility |
| `03_skills/webgl-interaction/references/04-interaction-recipes.md` | pointer behaviour, springs, flow and hit-testing |
| `03_skills/webgl-light-and-color/references/05-glow-and-light.md` | glow, blending, colour and line treatment |
| `03_skills/webgl-constellations/references/06-constellations.md` | legible node-link figures and layout |
| `03_skills/webgl-cosmic-art-direction/references/07-motifs.md` | visual motifs and motion choices |
| `03_skills/webgl-hardening-and-testing/references/08-testing-and-measurement.md` | checks, measurement methods and evidence limits |
| `03_skills/webgl-craft/references/12-open-conflicts.md` | disagreements that need an explicit decision or further verification |

## Also here
- `03_skills/webgl-craft/references/10-licence-ledger.md`:
  - **may adapt:** material whose licence permits the intended use, with required attribution, notices and other obligations preserved;
  - **learn only:** material without permission to reuse, or whose licence obligations the project cannot meet. Do not treat an admired example as a reusable asset.
- `03_skills/webgl-craft/references/12-open-conflicts.md`: where sources disagree, the available evidence, and the reasoning behind a choice.
- `03_skills/webgl-craft/references/09-original-single-skill-spec.md`: background on the cluster's scope and demo-testing approach. Use the task-specific skills for implementation guidance.

## Keeping the cluster alive
- **Add measured results to the skill they belong to,** stamped "measured on <device> <date>". Record the browser, rendering backend, workload and settings so someone else can interpret the result. Replace an ESTIMATE only with a measurement.
- **Worked builds:** a garden-supply shop might use a node-link figure to connect growing guides, with all guide titles and relationships also available in HTML. Fold proven helpers, shaders and tests from your own builds into the relevant skills once review and testing are complete.
- **Local index (optional):** keep a plain index of relevant skills, source notes and measurements. The included cluster configuration ships at `07_nexus_tools/configs/webgl.json` (after setup: `~/.local/share/webdev-workbench/nexus_tools/configs/webgl.json`); `07_nexus_tools/README.md` shows how to run it. Keep the index useful without a private memory service: use shipped paths for package references and clearly distinguish your own local notes.

  **Recall tags** (use these consistently if your notes support tags):

  | Tag | Covers |
  |---|---|
  | `webgl-craft` | everything |
  | `webgl-research` | source notes and verification |
  | `webgl-renderer` | renderer choice and budgets |
  | `webgl-hardening` | production safety and testing |
  | `webgl-interaction` | pointer, springs, flow, hit-testing |
  | `webgl-light` | glow, blends, dither, colour |
  | `webgl-constellations` | star and graph figures |
  | `webgl-art-direction` | the plate look and motion metaphors |
  | `webgl-handoff` | handoffs and porting |
  | `webgl-builds` | worked examples |
  | `webgl-skills` | the cluster's skills |

  Use descriptive titles and portable paths so the notes remain understandable outside the tool that created them.
