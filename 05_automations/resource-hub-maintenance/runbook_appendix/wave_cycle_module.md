# Wave Cycle Module: the two steps that get skipped, and why

> **REQUIRED. SITE-INDEPENDENT.** Governs every batch of resource pages for your site.
> Both steps below are easy to miss, even after a reviewer has pointed out their absence.
>
> **Review trigger:** any batch of resource pages · *"seed the batch"* · *"the generators all came back green"* ·
> *"are we still doing reflectors?"* · a batch about to enter Sanity → **read this module first.**
>
> Use this module when building many resource pages at once or deciding whether passing mechanical checks means the work is done.

---

## THE CYCLE

```
generate → REFLECT → gate → seed Sanity → WRITE THE RECORD → next wave
```

**Two of those steps are the ones that vanish.** Both vanish for the same reason: **each feels covered by
something adjacent to it.**

| step | what it felt covered by | why that's false |
|---|---|---|
| **REFLECT** | the generators' own detailed self-reports | a generator reviewing only its own page can miss false relationships and content borrowed from a sibling page |
| **THE RECORD** | "we'll reconcile at the end" | the site's editorial database or repository content registry is the **source of truth**; the debt compounds every wave |

---

## 🔴 THE REFLECTOR: and the trap that is *good* self-verification

**A retrospective review can find substantive defects on pages that are already live with every mechanical check green.**
One recurring defect is right-numbers-wrong-relation. These invented examples illustrate it:

- A kitchen-equipment guide says *"three rack positions **in each oven**"* when the source describes **three oven models**, each with a different fixed rack position.
- A bicycle-parts comparison says *"weights range from **260 g** across the collection"* when the lightest listed part weighs **180 g**. The full range is 180–720 g, so the heaviest is four times the lightest.

A generator can report that every automated check passed while leaving either error intact.

### The trap, named precisely

Generators can produce unusually careful self-verification. They **refute their own findings**,
**retract their own numbers**, **catch their own fabrications**, independently reproduce calculations,
and consult the content index before claiming that a page adds something new.

**Reading reports like that, seeding FEELS verified.**

> ⚠️ **A sloppy self-report makes you suspicious. An immaculate one makes you trust.**
> **The seduction scales with the quality of the self-report.**

**A generator scoring its own work is not a reflector.** Mechanical checks can detect
placeholders, duplicated content, image aspect ratios that disagree with a PDF's MediaBox, and invalid dates.
**They cannot reliably judge a thin bullet, reference bleed, promotional language presented as neutral evidence,
an overstated quantifier, or a summary drawn from the wrong spec sheet.** That judgment is the reflector's job.

### Rules

- **ONE `design-reflector` review per page** (REQUIRED). 9.80/10 HARD, every dimension ≥ 9.8. Use the review instructions in `05_automations/agents/design-reflector.md`.
- **PAIR THE TWINS.** Give near-identical siblings to **one** reflector so it can read both bullet sets side
  by side. **A reflector given only one page cannot perform the cross-contamination check** because it has
  nothing to compare against. Each sibling still needs its own verdict.
- **Overlap independent work:** **wave N's reflectors can run alongside wave N+1's generators.**
  Reflectors READ wave N while generators WRITE wave N+1. Keep their inputs and outputs separate and
  choose concurrency that fits the available resources. This can reduce added waiting time without
  removing the review requirement. Generation of the next wave may start early; seeding must wait.

---

## 🔴 THE PRECONDITION (this is the actual fix)

> **NEVER seed a wave whose predecessor is unreflected.**

This is **a precondition on seeding**, not a good intention. Require recorded review verdicts before
allowing the operation. The current wave must also complete its own reflection and pass its checks,
as the cycle above specifies. If a review requires changes, resolve them and obtain a passing verdict
before seeding the affected page.

Make the check executable, just as a content-integrity check can reject a mismatch between reviewed
HTML and the `htmlBody` being submitted. The purpose is to prevent the invalid transition rather than
merely document it.

---

## WHY THE FIRST CORRECTION DIDN'T STICK: read this part twice

A reviewer flags missing reflection. The affected pages receive reviews, and the lesson gets written down.
That repairs **the instance**. Unless reflection becomes a required step of the seed cycle,
it does not repair **the structure**.

Later waves can still enter Sanity without quality verdicts, leaving the reviewer to catch the same
omission again.

> **The lesson of `05_automations/resource-hub-maintenance/runbook_appendix/gate_doctrine_module.md` applies here:**
> Understanding a failure mode does not prevent it. Use that understanding to build a check that blocks
> the failure, because remembering the lesson at the right moment is unreliable.

Even the person who documents a rule can repair an instance without changing the process.

### The general rule for every self-heal

> **When a correction lands, ask: "what in the loop will ASK for this next time?"**
> **If the answer is "I will remember", it is not fixed.**

A stored lesson is only as useful as the trigger that brings it into the next decision.
**Require evidence at the point of seeding so that forgetting cannot silently bypass the review.**
