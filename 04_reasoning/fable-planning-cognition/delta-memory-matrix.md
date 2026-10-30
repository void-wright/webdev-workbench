# Fable Cognition: Delta-Memory Matrix (optional)

**Status:** OPTIONAL. These are atomic delta-memories you may store in your own Voidloom brain if you want recall to surface the disciplines. Review them first; nothing stores them automatically.

**Provenance:** distilled from blind, order-swapped comparisons of plans written for the same tasks. The comparison write-ups are not included in this package.

**Storing conventions (if you store them):**
- One concept per memory (atomicity). Plain-language summaries so the ratio-guard preserves their causal edges.
- Every memory carries tags `fable-cognition` + `delta:<slug>` (add `ace-curator` if you keep ACE curator memories).
- `importance` by rank: **0.90** (load-bearing discipline), **0.82** (sub-technique), **0.75** (finer / meta).
- `derived_from` = the kind of comparison task each delta came from, to be swapped for your own evidence memories when you have them.
- `--related` → the `fable-cognition` nexus hub; add inter-delta edges as noted.

---

## Rank 1 — Load-bearing disciplines (importance 0.90)

### 1. `delta:alternatives-rigor`
- **content:** In a plan/design/critique that makes a choice, name MORE and FINER rejected alternatives than feels necessary, and give EACH a reason tied to THIS task (not a generic "less scalable"). Discrimination, not enumeration.
- **category:** skill_lesson
- **tags:** `fable-cognition`, `delta:alternatives-rigor`
- **importance:** 0.90
- **derived_from:** a greenwashing-investigation task (the stronger plan named and rejected more alternatives)
- **why:** Decision-quality was the single largest judged contributor to the stronger plans' margin; finer rejected-alternatives is the most transferable move in it.
- **edges:** → `delta:own-runner-up`, `delta:reject-the-tempting-mapping` (specializations)

### 2. `delta:second-order-effects`
- **content:** Surface correlated and second-order effects as a causal TRACE (consequences of consequences, loops as loops), not an independent risk checklist. Ask what happens after the first move, not just what the first move is.
- **category:** insight
- **tags:** `fable-cognition`, `delta:second-order-effects`
- **importance:** 0.90
- **derived_from:** a newsletter pre-mortem task and a kitchen-brigade-to-software analogy task
- **why:** Anticipation was the second pillar of the delta; the checklist→trace reframe is what separated the stronger pre-mortems from the weaker ones.
- **edges:** → `delta:healthy-failure-reframe`, `delta:degenerate-case-stress-test`, `delta:feasibility-arithmetic`

### 3. `delta:feasibility-arithmetic`
- **content:** Before planning HOW to hit a target, run a "zeroth failure" back-of-envelope on the target ITSELF (e.g., churn × target ÷ conversion → required audience size). If the arithmetic says the target is infeasible, that is the root cause — surface it loudly above all execution risk.
- **category:** workflow_pattern
- **tags:** `fable-cognition`, `delta:feasibility-arithmetic`
- **importance:** 0.90
- **derived_from:** a newsletter pre-mortem task
- **why:** Highest-leverage single move observed — it can invalidate an entire plan in two lines and weaker plans missed it entirely.

### 4. `delta:two-tier-assumption-tagging`
- **content:** Tag invented assumptions `[A#]` separately from re-used industry heuristics `[H#]`; give each a NAMED checkpoint at which to re-validate. A single undifferentiated `[ASSUMPTION]` flattens "I made this up" and "the field generally holds this" into one bucket.
- **category:** skill_lesson
- **tags:** `fable-cognition`, `delta:two-tier-assumption-tagging`
- **importance:** 0.90
- **derived_from:** a vague-spec task and a greenwashing-investigation task
- **why:** Epistemic calibration was the third pillar; two-tier tagging is its most concrete, copyable artifact.
- **edges:** → `delta:citation-fabrication-guard`, `delta:verification-battery`

### 5. `delta:scope-fit-guard`
- **content:** Add DEPTH IN REASONING, never apparatus. Right-size the artifact to the ask. WP-numbered work-packages, methodology asides, and tripwire calendars beyond the ask are the trap — they cost the rubric's scope-fit point. Self-check: "If I deleted the formatting scaffolding, would the reasoning still be there and the artifact match the ask better?" If yes, delete it.
- **category:** skill_lesson
- **tags:** `fable-cognition`, `delta:scope-fit-guard`
- **importance:** 0.90
- **derived_from:** a subway-to-communications analogy task (a tighter, right-sized artifact beat a more elaborate one)
- **why:** This is the over-build trap to avoid; without it the moves would import an elaborate plan's failure mode alongside its strengths.
- **edges:** → `delta:modest-margin-calibration`

---

## Rank 2 — Sub-techniques (importance 0.82)

### 6. `delta:own-runner-up`
- **content:** Name your OWN second choice explicitly and state why it lost. Presenting the winner as if unopposed hides the decision; naming and killing your runner-up shows it.
- **category:** skill_lesson
- **tags:** `fable-cognition`, `delta:own-runner-up`
- **importance:** 0.82
- **derived_from:** a commons-allocation task (the stronger plan named a weighted lottery as its runner-up and rejected it as harder to explain and audit for a volunteer body)
- **why:** A specific, high-frequency form of alternatives-rigor that reliably lifted decision-quality scores.

### 7. `delta:reject-the-tempting-mapping`
- **content:** In an analogy or mapping task, explicitly reject the seductive-but-wrong mapping a reader would propose, with a FUNCTIONAL reason (e.g., "it under-delivers on 3 of the expediter's 5 functions"). Don't silently skip it.
- **category:** skill_lesson
- **tags:** `fable-cognition`, `delta:reject-the-tempting-mapping`
- **importance:** 0.82
- **derived_from:** a kitchen-brigade-to-software analogy task (expediter ≠ scrum master)
- **why:** Analogical tasks reward addressing the obvious-but-wrong mapping head-on; weaker plans left it unaddressed.

### 8. `delta:healthy-failure-reframe`
- **content:** Ask whether an apparent "failure" is actually desirable. Some drop-off is healthy disqualification of poor-fit users — "are the droppers people you wanted?" Not every loss should be minimized.
- **category:** insight
- **tags:** `fable-cognition`, `delta:healthy-failure-reframe`
- **importance:** 0.82
- **derived_from:** a vague onboarding-spec task (the stronger plan flagged healthy drop-off; the weaker one missed it)
- **why:** A distinctive second-order move that weaker plans consistently missed; cheap to apply, high signal.

### 9. `delta:degenerate-case-stress-test`
- **content:** Stress-test a design or mapping against its degenerate cases (zero-timezone-overlap team, solo maintainer) and DERIVE the needed exception from the break (e.g., the incident-command exception). Don't assume the normal case holds everywhere.
- **category:** workflow_pattern
- **tags:** `fable-cognition`, `delta:degenerate-case-stress-test`
- **importance:** 0.82
- **derived_from:** a kitchen-brigade-to-software analogy task
- **why:** Turns edge-case awareness into concrete design output (the exception), rather than a caveat.

### 10. `delta:citation-fabrication-guard`
- **content:** Flag any named regulation, standard, or statistic as VERIFY-AT-EXECUTION — re-verify and cite at run time; never assert it as flat background fact. Stating an unverified regulation as fact is the exact posture that produces confidently-wrong citations.
- **category:** skill_lesson
- **tags:** `fable-cognition`, `delta:citation-fabrication-guard`
- **importance:** 0.82
- **derived_from:** a greenwashing-investigation task
- **why:** Directly addresses fabrication risk (aligns with any citation and traceability rule you keep); the weaker plan stated the regulation as fact.

---

## Rank 3 — Finer / meta (importance 0.75)

### 11. `delta:verification-battery`
- **content:** Close a plan with a NAMED verification battery a stranger could run — falsifiability / traceability / stranger-test / fork-closure — turning "trust me" into "here's how to check me."
- **category:** workflow_pattern
- **tags:** `fable-cognition`, `delta:verification-battery`
- **importance:** 0.75
- **derived_from:** a vague-spec task and a greenwashing-investigation task
- **why:** A repeatable closing move that raised traceability scores; lower rank because it's a finishing polish, not a core discriminator.

### 12. `delta:modest-margin-calibration`
- **content:** The whole edge these disciplines capture is a modest REFINEMENT MARGIN, not a categorical leap. Apply these disciplines as a light overlay/polish on an already-good plan, never as a reason to overhaul a sound plan. The "add rigor everywhere" urgency is itself the scope-fit failure mode.
- **category:** insight
- **tags:** `fable-cognition`, `delta:modest-margin-calibration`
- **importance:** 0.75
- **derived_from:** the comparisons' overall result (a consistent but modest margin)
- **why:** Prevents over-application; keeps the disposition calm and the artifact right-sized. Pairs with `delta:scope-fit-guard`.

---

## Framing and sub-technique atoms (importance 0.82 unless noted)

These five atoms back the recall tags in the SKILL.md memory map that are not covered above.

### 13. `delta:framing-gate`
- **content:** Before designing, demote the proposed solution or stated question to one hypothesis among others, name the real problem class and target, and state ONE governing design principle so later choices read as derivations rather than fresh debates.
- **category:** workflow_pattern
- **tags:** `fable-cognition`, `delta:framing-gate`
- **importance:** 0.90
- **derived_from:** the opening moves of the strongest plans across several task types
- **why:** Reframing the target did more design work than any single downstream move.
- **edges:** → `delta:alternatives-rigor` (the demoted proposal becomes one candidate among the alternatives)

### 14. `delta:gaming-table`
- **content:** For a mechanism, incentive or allocation design, write an attack → why-it-fails table: for each way a rational actor could game the design, show the move is worthless, expensive in a currency that cannot be faked, or self-defeating. Aim for low-yield and visible, not un-gameable, and pair each control with governance.
- **category:** workflow_pattern
- **tags:** `fable-cognition`, `delta:gaming-table`
- **importance:** 0.82
- **derived_from:** mechanism and allocation design tasks
- **why:** Turns second-order anticipation into a concrete check on designs that other people will try to exploit.
- **edges:** → `delta:second-order-effects`

### 15. `delta:dependency-sequencing`
- **content:** Express a plan's order as dependencies, not a dated timeline: each step is a trust or data prerequisite of the next, and each has a named gate that must pass before the next step unlocks.
- **category:** workflow_pattern
- **tags:** `fable-cognition`, `delta:dependency-sequencing`
- **importance:** 0.82
- **derived_from:** rollout and policy-change tasks
- **why:** The most common real-world sequencing error is running a step before its upstream dependency exists.
- **edges:** → `delta:second-order-effects`

### 16. `delta:pre-registered-falsifiers`
- **content:** In an investigation or diagnosis, write each hypothesis's disconfirming evidence BEFORE looking at the data, and rank hypotheses by prior likelihood times cheapness to test.
- **category:** skill_lesson
- **tags:** `fable-cognition`, `delta:pre-registered-falsifiers`
- **importance:** 0.82
- **derived_from:** metric-drop investigation tasks
- **why:** Confirmation bias operates when the query is designed, not only when results are interpreted.
- **edges:** → `delta:attribution-ledger`, `delta:two-tier-assumption-tagging`

### 17. `delta:attribution-ledger`
- **content:** Close an investigation with an attribution ledger whose rows must sum to the total change. Accept a cause only when its confirmer is present, its falsifier is absent and it accounts for a named share; a real but tiny cause cannot close the investigation.
- **category:** skill_lesson
- **tags:** `fable-cognition`, `delta:attribution-ledger`
- **importance:** 0.82
- **derived_from:** metric-drop investigation tasks
- **why:** If the ledger does not sum, the investigation is not done.
- **edges:** → `delta:pre-registered-falsifiers`

---

## Nexus (optional, to store alongside)

A `fable-cognition` nexus hub should tie all 17 atoms together (tags `nexus, fable-cognition, protected`, importance 0.95; summary carrying `index/master` so the ratio-guard demotes hub edges to `references`). Segmented index: **Framing** (#13) · **Decision-quality** (#1, #6, #7) · **Anticipation** (#2, #3, #8, #9, #14, #15) · **Calibration** (#4, #10, #11) · **Investigation** (#16, #17) · **Scope-fit / calibration** (#5, #12). Recall the hub by its `fable-cognition` tag when you want the whole map.
