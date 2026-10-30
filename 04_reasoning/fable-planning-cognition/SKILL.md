---
name: fable-planning-cognition
description: A cross-cutting reasoning layer that raises the reasoning quality of planning, design, and critique work. Not a persona and not a workflow — a thin set of thinking moves to run while you author a plan, design doc, or critique. Engage when the task is to DESIGN a plan, DECOMPOSE an approach, WEIGH alternatives, PRE-MORTEM a proposal, MAP an analogy, INVESTIGATE a cause, or CRITIQUE someone else's plan. It opens with a framing pre-step — reframe the real target and state the governing design principle before designing — then runs three disciplines: alternatives-rigor (name more + finer rejected options, each with a task-specific reason), second-order anticipation (correlated + downstream effects, not an independent checklist), epistemic calibration (tag assumptions precisely, flag fabrication risk). Three task-shaped sub-techniques fold in: an adversarial gaming table (mechanism/incentive design), dependency-sequencing with named gates, and pre-registered falsifiers + a summing attribution ledger (investigations). For tasks with other reacting agents (negotiation, mediation, nudge/incentive, escalation) it adds counterparty-modeling — plan the interaction and how each agent responds, not just your own move — plus anchor-defeating sequencing, substitutes-before-friction, counter-metric pairing, and asymmetric-error-cost sizing. For reconciling two conflicting plans it adds synthesis moves (decouple-the-axes, goals-vs-mechanisms, find-the-unused-structural-lever, keep-cut-bind — never split-the-difference); for repairing a plan that failed in execution it adds root-cause moves (failure-signature, shadow-systems-as-signal, Grudin/adoption-by-subtraction, conserved-quantity, forcing-function audit, capex-vs-opex). Plus one deliberate anti-pattern to NOT copy: scope-fit over-build. Triggers on: "design a plan", "plan this", "decompose", "weigh the alternatives", "pre-mortem", "critique this plan", "what could go wrong", "map this onto", "why did X drop", "investigate this".
ships-with-voidloom: false
disable-model-invocation: false
---

# Fable Planning Cognition — A Reasoning Layer for Plans, Designs, and Critiques

This skill is **not** a persona and **not** a workflow. It is a thin set of thinking moves that raise the *reasoning quality* of a plan without adding apparatus to the artifact.

**Where this comes from.** These moves were distilled from blind comparisons of planning outputs written for the same tasks. The differences were real but modest and varied by task, and calibration decided most close calls: a strong planner who invents specifics under pressure loses to one who stays calibrated. The skill encodes **one framing move, three disciplines, a set of task-triggered moves and one anti-pattern to avoid**. Apply them as polish on an already-good plan, not as a reason to overhaul a sound one.

---

## When to engage

Engage this skill when the task is a **plan / design / critique / pre-mortem / analogy-mapping / investigation** — anything where the deliverable is *reasoning about a course of action* rather than executing one. Skip it for pure execution, lookups, or single-fact answers.

## Core Operating Principle — Frame First, Then the Three Questions

**Move 0 — the Framing Gate (do this BEFORE the three questions).** Strong plans open by reframing, and this move does more work than any single downstream one. Three steps: **(a) demote the proposed solution or the stated question to *one hypothesis among others*** — *"'freelancers' is the owner's hypothesis, not a validated target"*; **(b) name the real problem class and the real target** — *"this is not a feature-launch risk analysis; it is an economy-conversion risk analysis"*; *"'Fridays off' is not one policy — it is four different policies wearing one name"*; **(c) state ONE design principle that governs the downstream choices**, so later decisions read as *derivations, not fresh debates* — *"make enforcement mechanical"*; *"the health system must not itself add load to the overworked maintainer."* Output of the gate: a **reframed target + a one-line governing principle**. Done well, that reframing does most of the design work.

Then, before you finalize, answer these three. Each maps to one discipline below. If you can answer all three well *and* the artifact is right-sized to the ask, you have captured most of what this skill offers.

1. **Did I name enough alternatives — finely enough — each rejected for a task-specific reason?** (→ Discipline 1: Alternatives Rigor)
2. **Did I trace the correlated and downstream effects, not just an independent risk checklist?** (→ Discipline 2: Second-Order Anticipation)
3. **Did I tag my assumptions precisely and flag anything I might be fabricating?** (→ Discipline 3: Epistemic Calibration)

Then the guard question: **Is the artifact right-sized to the ask, or did I add apparatus?** (→ Scope-Fit Guard). Depth of reasoning is the goal; formatting apparatus is the trap.

---

## Discipline 1 — Alternatives Rigor (Decision-Quality)

**Triggering condition:** engage when the task is a plan/design/critique that makes a *choice* — a mechanism, a mapping, an allocation, an architecture. Any decision with more than one defensible option.

**The move:** name **more** and **finer** rejected alternatives than feels necessary, and give **each** a specific reason tied to *this* task — not a generic "less scalable." Include your own second-choice by name and say why it lost. (The Framing Gate feeds this: once the proposed solution is demoted to a hypothesis, it becomes just one candidate in the field to weigh.)

| Do | Instead of |
|---|---|
| Name 5 candidate designs, reject 4 with task-specific reasons | Name 2-3, reject with generic reasons |
| Name your OWN runner-up explicitly and why it lost | Present the winner as if unopposed |
| Reject the *tempting-but-wrong* mapping with a functional reason | Silently skip the mapping a reader would propose |
| Tie each rejection to a named property of this task | "Option B is worse" without saying at what |

**Threshold — do this until:** every option a sharp reader would raise has been named *and* dismissed with a reason that could only apply to this task; and your runner-up is on the page with its losing reason. Stop when naming another alternative would be padding, not discrimination.

**Contrastive worked example (weaker → stronger):**
- *Wider field (an investigation plan):* a weaker plan names the two or three obvious alternatives and rejects them; a stronger one adds the remaining discriminating options, the ones a sharp reader would otherwise ask about.
- *Finer (mapping a restaurant kitchen brigade onto a software team):* reject the seductive "expediter = scrum master" mapping with a functional reason, for example *"it under-delivers on 3 of the expediter's 5 functions."* A weaker plan leaves the tempting mapping unaddressed.
- *Own runner-up (allocating a shared resource among volunteers):* name **"weighted lottery"** as your *own* runner-up and give the reason it lost: *harder to explain and audit for a volunteer body.* Naming your second choice and killing it is stronger than presenting the winner alone.

---

## Discipline 2 — Second-Order Anticipation

**Triggering condition:** engage when the task is a plan/design/critique whose success depends on *how the system behaves after the first move* — anything with users, feedback loops, targets, incentives, or a mapping that must survive edge cases.

**The move:** surface **correlated and second-order effects** — consequences of consequences, and effects that are *desirable* despite looking like failures. This is not an independent risk checklist; it is a causal trace. Run the cheap arithmetic on the target itself *before* planning how to hit it.

| Do | Instead of |
|---|---|
| Ask whether an apparent failure is actually *wanted* | List "drop-off" as a risk to minimize |
| Stress-test the design against degenerate cases → derive the exception | Assume the normal case holds everywhere |
| Run "zeroth-failure" feasibility arithmetic on the target | Accept the target and plan execution around it |
| Trace loops (content, pricing, incentive) as loops | List their symptoms as separate line items |

**Threshold — do this until:** you have (a) checked whether any "failure" in the plan is actually a desirable filter, (b) named the degenerate case that breaks the design and the exception it forces, and (c) sanity-checked the target's arithmetic. Stop before enumerating effects that don't change the plan.

**Contrastive worked example (weaker → stronger):**
- *Healthy-failure reframe (a vague onboarding spec):* some onboarding drop-off is **healthy disqualification** of poor-fit users: *"are the droppers people you wanted?"* A weaker plan treats all drop-off as loss.
- *Degenerate-case stress-test (the brigade analogy):* test the analogy against a **zero-timezone-overlap team** and a **solo maintainer**, and *derive* the incident-command exception from those degenerate cases. A weaker plan maps the normal case only.
- *Feasibility arithmetic (a paid-newsletter pre-mortem):* run a **"zeroth failure"** check, *churn × target ÷ conversion → required audience size*, which can show that the **target itself** is the root cause. Then name the **free/paid-content-erosion loop** and **pricing-as-a-burnout-vector** as *loops*, not line items.

**Two named sub-techniques of the second-order trace:**
- **Adversarial gaming table** *(mechanism / incentive / allocation designs).* Build an explicit **attack → why-it-fails** table: for each way a rational actor games the design, show the move is made **worthless**, **expensive in an unfakeable currency**, or **self-defeating**. Design for *low-yield-and-visible*, not un-gameable. The table fits allocation schemes (who gets the shared dinner slots, who books the shared cargo bike) and any control on people. Add the guard *"cars don't lie, employees do"*: pair every control with governance rather than trusting the control alone.
- **Dependency-sequencing with a named gate.** Express sequencing as **dependencies, not a dated timeline**: each step is a *trust-* or *data-prerequisite* of the next (baseline before intervention; check-in ledger before penalties; detection before control), and name the **gate** that must pass before the next unlocks. The most common real-world error is running a step before its upstream dependency exists — *"announcing before mod co-design and a public ledger fires the volunteer-revolt and sellout-schism cascades simultaneously."*

---

## Discipline 3 — Epistemic Calibration

**Triggering condition:** engage on any plan/design/critique that rests on assumed facts, named standards/regulations/statistics, unverified premises, or hypotheses under investigation — i.e., almost all of them.

**The move:** distinguish *what you invented* from *what you're re-using as a heuristic*, tag each precisely, and flag anything a downstream reader might mistake for a verified fact. Close with a named verification battery so the plan can be checked, not just believed.

| Assumption type | Tag it | And commit to |
|---|---|---|
| Something you invented to proceed | `[A#]` (invented assumption) | re-validate at a **named checkpoint** before it hardens |
| An industry heuristic you're leaning on | `[H#]` (heuristic) | re-check against reality at the same checkpoint |
| A named regulation / standard / statistic | flag as **verify-at-execution** | re-verify **and cite** at run time; never assert as background fact |

**Threshold — do this until:** every load-bearing assumption is tagged by *kind* (not a single undifferentiated `[ASSUMPTION]`), every named external fact is marked for re-verification, and the plan ends with a battery a stranger could run (e.g., falsifiability / traceability / stranger-test / fork-closure). Stop when further tagging is labeling the obvious.

**Contrastive worked example (weaker → stronger):**
- *Two-tier tagging:* use **`[A#]` for invented assumptions and `[H#]` for industry heuristics**, each with a named checkpoint. A single undifferentiated `[ASSUMPTION]` flattens "I made this up" and "the field generally holds this" into one bucket.
- *Citation-fabrication awareness (an environmental-claims investigation):* flag that **any named regulation or standard must be re-verified and cited at execution time.** Stating the regulation as flat background fact is the exact posture that produces confidently wrong citations.
- *Verification battery:* **close** plans with a named battery: *falsifiability / traceability / stranger-test / fork-closure.*

**Named sub-technique — pre-registered falsifiers + a summing attribution ledger** *(investigation / diagnosis / root-cause tasks).* Write each hypothesis's **disconfirmer BEFORE looking at the data**; accept a cause only when its confirmer is present, its falsifier absent, *and* it accounts for a **named share** of the whole. Close with an **attribution ledger whose rows must sum to the total** — a real-but-tiny cause cannot close the investigation: *"if the ledger doesn't sum, the investigation isn't done."* Rank hypotheses by *prior × cheapness-to-test*, not by interestingness. It suits metric-drop investigations (falling monthly active users, falling donations); its point: *"confirmation bias operates at query-design time, not just interpretation time."*

---

## Responsive-World & Sequencing Moves

These moves matter most on tasks that reason about *other agents reacting* and about *process order*. Five moves: apply only the one(s) the task triggers; the Scope-Fit Guard still governs (these are depth, not apparatus).

### Move 4 — Counterparty / Responsive-Agent Modeling  *(the highest-value move in this group)*
**Trigger:** the task involves other optimizing agents — negotiation, mediation, an incentive/commission scheme, a nudge, an escalation path, a pricing tier, a norm.
**The move:** don't plan your action; plan the **interaction**. For each move you make, trace how the reacting agent(s) respond given *their* payoff, and design against that response — not against a passive world.
- *Negotiation:* build the counterpart's move-by-move game-tree **and their BATNA**, and interrogate whether their leverage (the "national-chain tenant") nets out *weaker* than it looks once concessions are priced.
- *Mediation:* work **interests beneath positions**, name the shared enemy, unbundle the decision so trades exist.
- *Nudge / incentive:* predict the response **persona-by-persona**, and price in the **new perverse behavior your fix itself creates** (the referral-annuity that gets churned, the booth-timer that gets gamed).
- *Weaker:* optimizes its own move against a static board. *Stronger:* models the other side's optimization and the second-order behavior it triggers. This matters most on mediation, devil's-advocate and escalation tasks.

### Move 5 — Anchor-Defeating Sequencing  *(group decisions, selections, evaluations)*
Fix the **criteria and weights, and elicit views privately, BEFORE** options are seen or discussed. Whoever frames or scores first anchors everyone; pre-committed criteria + silent independent elicitation is the cheapest strong debias. Score capability *before* seeing price. (Fits deliberation, comparative evaluation and values-conflict tasks.)

### Move 6 — Substitutes-Before-Friction  *(removing something / adding friction / behavior change)*
Ship the **substitute or the subtraction first**. Removing the chair before the focus-room exists turns users into opponents of the change; "take before you add" (a felt subtraction win) funds the trust the rest of the change spends. (Fits nudge, norm-design and via-negativa tasks.)

### Move 7 — Counter-Metric Pairing  *(measurement / KPI / incentive design)*
Every target gets a **counter-metric holding the opposing failure mode** (a quality target paired with a speed *guardrail*, never a second maximization target). Swapping one solo metric for another only relocates the gaming; aim for an equilibrium where the laziest high score is genuine good work. Prefer measures **behavioral > perceptual > self-reported** (they resist gaming in that order). (Fits metric-reframing and incentive-realignment tasks.)

### Move 8 — Asymmetric-Error-Cost Sizing  *(commitments under uncertainty)*
When guessing wrong costs differently in each direction, **size the commitment to the real cost asymmetry, not symmetric gut** — planned stockouts where over-supply is cheap, buffers where under-supply is ruinous — and match each commitment's reversibility to the information certainty available at the moment it's made. (Fits capacity-under-uncertainty, escalation and staffing tasks.)

---

## Diagnostic & Reconciliation Moves

These moves are for GENERATIVE work: reconciling two conflicting plans, or diagnosing a failed plan and then fixing it. On pure evaluative flaw-hunting they help less and calibration matters more (see the calibration sharpening below). Two move-families follow; apply only the one the task triggers, and the Scope-Fit Guard still governs (these are depth, not apparatus).

### Move 9 — Reconciliation / Synthesis  *(reconcile two conflicting plans/approaches into one)*
**Trigger:** you must merge or choose between two conflicting plans, proposals, designs, or factions. **Never split-the-difference — a 50/50 blend or "bolt both on" is the tell of a fake reconciliation.** Five sub-moves:
- **Decouple-the-axes:** most A-vs-B conflicts weld two *independent* choices together (school lunch: *where* food is made vs *what* is made; a "structured vs natural" park is really *ratio* + *layout* + *what-to-commit-now*). Separate the axes and the conflict often dissolves — resolve each on its own merits.
- **Goals-vs-mechanisms:** name each plan's underlying **goal** separately from its proposed **mechanism**; merge the *goals*, then pick the cheapest mechanism serving both. (Plan A's goal was "nobody unqualified in the hazard," not "months of training.") Genuine synthesis merges goals; compromise merges mechanisms.
- **Unused-structural-lever:** hunt for an asset **neither** plan used that dissolves the trade-off (a co-op's *patronage dividend* turns "margin = extraction from members" into "margin = surplus returned"; *centralized procurement* is what makes small-farm local sourcing viable). Sometimes one plan's cherished goal is best served by the other plan's machinery.
- **Keep-cut-bind:** keep each plan's valid **core**, cut each plan's **overreach**, bind them with a coordinating mechanism. Quality gate: *"does the merged plan still carry each side's WEAKNESS, or only their strengths?"*
- **Salvage-the-cheap-parts** of the losing plan — its low-cost value carriers (gardens, education, community layer) survive even when its expensive mechanism is cut.

### Move 10 — Repair / Root-Cause Diagnosis  *(a plan was implemented and FAILED — diagnose the root, then fix)*
**Trigger:** something shipped and failed; you must find the real cause and repair it. Attribute to the **system/design, never to individuals** (blameless).
- **Failure-signature first:** uniform failure across heterogeneous cases = a **system property**, not a people problem. Read the *shape* of the failure (quiet, bilateral, same ~clock → structural, not motivational).
- **Shadow-systems-as-signal:** side spreadsheets / back-channels / workarounds are a **spec for what the official system must become** — never a discipline failure to enforce away. They prove demand exists and the official tool's cost/benefit is inverted.
- **Grudin's-law / adoption-by-subtraction:** adoption fails when the people doing the data-entry are not the ones getting the benefit. Fix by **killing the replaced workflow** (make the consumer pull status *only* from the new system) — not by adding a mandate on top.
- **Conserved-quantity / waterbed:** banning a behavior in one zone **displaces and concentrates** it elsewhere (quiet-floor → the noise moves, it doesn't vanish). Build the **sink before the ban**.
- **Forcing-function audit:** before removing anything, ask what invisible scaffold it was silently providing (a parent's commute was an unrecognized attendance-enforcement mechanism; an accrual deadline was the use-it forcing function).
- **Capex-vs-opex:** programs die when funded as one-time **artifacts** with no maintenance loop. If the real product is an ongoing service (rebalancing, curation, stewardship), budget the **loop**, not just the launch.

### Calibration sharpening (the fatal-flaw lesson)
On a pure **flaw-hunt / critique**, calibrated restraint wins. The tell of an over-reaching critique is **fabricating magnitudes to condemn a plan** (ranges such as "0-90/hr, 5-40M" asserted as near-fact). So, extending Discipline 3 to the evaluative direction: **when hunting a flaw, never invent numbers to condemn the plan — keep any figures strictly in the confirm/disconfirm section as hypotheses to test, never as near-facts inside the mechanism.** (Corollary from the Repair lens: grounding a *diagnosis* in a real, flagged-as-recalled evidence base is an asset — the same instinct, pointed the right way.)

## Scope-Fit Guard: the over-build trap to avoid

The most consistent weakness of an otherwise strong planner is **scope-fit over-build**: over-formalizing with WP-numbered work-package apparatus, methodology asides and tripwire calendars beyond the ask. On an analogy task (mapping a subway system onto team communications), a tighter artifact beats a padded one precisely because the padding spends the reader's attention on apparatus instead of reasoning.

**The rule:** every move above — framing, the three disciplines, the sub-techniques — adds **depth in reasoning, never apparatus.** Right-size the artifact to the ask.

| Add (depth) | Do NOT add (apparatus) |
|---|---|
| A one-line governing principle that steers real choices | A framing essay that restates the prompt |
| A finer rejected alternative with a real reason | A WP-numbered work-package scaffold the ask didn't request |
| A second-order effect (or gaming row) that changes the plan | A methodology aside on how you plan |
| A dependency + named gate that reorders the work | A dated Gantt calendar beyond scope |
| A precise assumption tag / a summing ledger | A tripwire calendar / governance ritual beyond scope |

**Self-check before you ship:** *"If I deleted the formatting scaffolding, would the reasoning still be there — and would the artifact be shorter and match the ask better?"* If yes, delete the scaffolding. Depth survives compression; apparatus does not.

This skill practices its own rule: it is deliberately short.

---

## Disposition & Escalation

- **Disposition:** calm, additive, non-anxious. This is a **modest refinement**, not a rescue. Apply the moves as a light overlay on an already-good plan; do not tear a sound plan down to retrofit them. The desperate "I must add rigor everywhere" impulse is itself the scope-fit failure mode.
- **When the moves conflict with scope-fit, scope-fit wins.** A tighter artifact that reasons deeply beats a padded one that formats deeply. If adding an alternative, a gaming row, or a tag would bloat the artifact past the ask, hold it in your reasoning and cut it from the page.
- **Escalate to the human** when: the Framing Gate surfaces that the proposed solution is the wrong target entirely; a load-bearing assumption can't be resolved even at a checkpoint; the feasibility arithmetic (or a non-summing ledger) says the *target itself* is infeasible (surface that loudly — it is often the highest-value output); or the "right size" of the artifact is genuinely ambiguous. Name the trade-off; don't silently pick.

---

## Anti-Patterns to Catch

| Symptom | Anti-pattern | Right move |
|---|---|---|
| Designing straight from the ask's words | Skipped the Framing Gate | Reframe: demote the proposed solution to a hypothesis, name the real target, state the one governing design principle |
| One clear winner, no rivals named | Alternatives under-rigor | Name the runner-up and at least one tempting-but-wrong option; kill each with a task-specific reason |
| "Risks:" as a flat independent list | Checklist instead of causal trace | Convert to a second-order trace: which risks are correlated, which "failures" are wanted, what loops exist |
| Mechanism/incentive design with no abuse analysis | Missing gaming table | Add an attack → why-it-fails table: each game made worthless / expensive-in-unfakeable-currency / self-defeating |
| Plan is a dated timeline | Sequencing not expressed as dependencies | Re-express steps as trust/data dependencies, each with a named gate before the next unlocks |
| Target accepted at face value | Skipped feasibility arithmetic | Run the zeroth-failure back-of-envelope on the target before planning execution |
| Investigation stops at the first confirming cause | No falsifiers / no summing ledger | Pre-register disconfirmers; close with an attribution ledger whose rows sum to the whole |
| Single `[ASSUMPTION]` bucket | Flat epistemic tagging | Split into `[A#]` invented vs `[H#]` heuristic, each with a re-validation checkpoint |
| Named regulation/stat stated as fact | Citation-fabrication risk | Flag as verify-at-execution; re-verify + cite at run time |
| WP numbers, methodology asides, tripwire calendars | Scope-fit over-build | Delete the apparatus; keep the reasoning; match the ask |
| "Let me add rigor everywhere" urgency | Desperate over-formalizing | Calm down; this is a light overlay, not an overhaul |

---

## Memory-Map Hints

The distilled deltas behind this skill can live as atomic memories in your Voidloom brain (the optional matrix: `delta-memory-matrix.md`). If you store them, recall them by tag:

| When you're... | Recall tag |
|---|---|
| Opening a plan / reframing the target | `delta:framing-gate` |
| Weighing options in a plan/design | `delta:alternatives-rigor`, `delta:own-runner-up`, `delta:reject-the-tempting-mapping` |
| Anticipating consequences / running a pre-mortem | `delta:second-order-effects`, `delta:healthy-failure-reframe`, `delta:degenerate-case-stress-test`, `delta:feasibility-arithmetic` |
| Designing a mechanism/incentive/allocation | `delta:gaming-table`, `delta:dependency-sequencing` |
| Running an investigation/diagnosis | `delta:pre-registered-falsifiers`, `delta:attribution-ledger` |
| Stating assumptions or citing external facts | `delta:two-tier-assumption-tagging`, `delta:citation-fabrication-guard`, `delta:verification-battery` |
| Tempted to formalize / add structure | `delta:scope-fit-guard`, `delta:modest-margin-calibration` |
| Loading the whole map | `fable-cognition` (nexus hub) |

**Companion file:** `delta-memory-matrix.md` holds one atomic memory per move, ready to store in your own memory if you want them recallable.
