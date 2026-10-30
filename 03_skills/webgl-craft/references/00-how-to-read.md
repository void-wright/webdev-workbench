<!-- Reading guide for the WebGL craft references.
     Status markers: VERIFIED (checked against a primary source or recomputed), CONTRADICTED (do not build on it),
     UNSETTLED (a lead), ESTIMATE (no measurement).
     Worked examples are illustrative. They do not establish measured GPU performance. -->

## 0. How to read this file

### 0.1 Citation key

| Tag | Means |
|---|---|
| Primary source | Public documentation or a specification supporting the adjacent claim |
| Verification note | An explanation of how a claim was checked and what the check established |
| Browser inspection | Observed behaviour in a browser, with the rendering backend and test conditions stated |
| Research summary | Leads that need verification before they become implementation rules |
| Design requirement | A rule stated in full where it is used |
| Dependency note | A prerequisite explained alongside the affected implementation |
| Example code | Illustrative code included with the explanation, not evidence of production behaviour |
| Porting guidance | Guidance in `03_skills/webgl-handoff-and-porting/SKILL.md` |
| Calculation | Reproducible arithmetic with its inputs and assumptions stated |
| Measurement | An observed result with the hardware, workload and test method stated |

Claims should be understandable from the shipped material. If supporting evidence is unavailable, state the uncertainty rather than relying on an inaccessible citation.

### 0.2 Status markers (from verification and reproducible checks)

- **VERIFIED**: confirmed against a primary source, or recomputed from stated inputs. A verified calculation is not a hardware measurement.
- **CONTRADICTED**: verification or arithmetic found the claim wrong. Do not build on it.
- **UNSETTLED**: checked but not resolved; treat as a lead.
- **ESTIMATE**: an arithmetic or judgement-based figure with no measurement behind it. Do not present it as observed GPU performance.

### 0.3 Three facts that frame everything

1. **Software-rendered results are not GPU measurements.** When ANGLE uses SwiftShader, rendering runs on the CPU. Frame-rate figures from that setup describe costs under those test conditions, not performance on a physical GPU. Treat per-device caps as ESTIMATE until tested on representative hardware.
2. **Research output can contain incorrect claims.** Check consequential claims against primary sources and recompute numerical examples. Research summaries provide leads, not established facts.
3. **An admired website is not proof of sound implementation.** Inspect reduced-motion handling, off-screen and hidden-tab pausing, and frame-rate independence separately from visual quality. The static fallback must work as a complete design; visual references do not establish that discipline for you.

### 0.4 What a real-GPU bench does and does not gate

- Ship **SVG/HTML figures over still images** first. They do not wait for a GPU benchmark.
- A visual component can carry a `mode="webgl"` **stub** at first: it renders the still and reserves a canvas layer. For example, a ceramic studio's `LayeredArt` component could show a still arrangement of glaze swatches.
- The benchmark gates only the real WebGL mode, performance comparisons between implementations of the same visual, and handoff packages that include the WebGL implementation. Use representative hardware and the same workload for comparisons.
- Before a benchmark exists, design every figure so that a WebGL layer can later be added **without a redesign**.

---
