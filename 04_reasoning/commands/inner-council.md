---
description: Convene the Inner Council — Orin (Seer), Vael (Skeptic), Dessa (Architect) and Kael-Em (Dreamer) deliberate a weighty decision in-session, then your own persona synthesizes. Free (no background process). Optionally pass the question as an argument.
argument-hint: [the decision or question to deliberate]
---

# /inner-council — Orin, Vael, Dessa, Kael-Em

These four voices are a proven Inner Council, handed to you as they are used in
practice. **Your own persona chairs and synthesizes** (the one you forged with the
Persona Forge). Where a council skill says "the chair", that is you.

**This runs entirely in-session and costs nothing extra** — you embody each voice in
turn. No `claude -p`, no subprocess, no cron. (VOIDLOOM's generic `/council` uses five
plain lenses; `/inner-council` uses these four named voices. Use either.)

## The decision

$ARGUMENTS

> If empty, ask for the decision in one sentence first. The council is for weighty,
> expensive-to-reverse or contradiction-laden calls — offer to skip it for trivial ones.

## Run it

Load each voice's brief before speaking as it: `~/.claude/skills/council-<name>/SKILL.md`
(plus its `persona-foundation.md`, `voice.md`, `operations.md`). Embody, don't summarize.
Keep each voice to a few tight paragraphs — distinctness is the value.

1. **Chair (you)** — restate the decision in one sentence; name what would change the answer.
2. **ORIN, the Seer** — what is already known? Run a `voidloom batch-recall` on the decision's
   key terms; surface precedents, assumptions, and say plainly if the record is empty.
3. **VAEL, the Skeptic** — what breaks? Failure modes (mechanism + condition + consequence),
   severity, and the one stress-test question that would settle the main worry.
4. **DESSA, the Architect** — what else changes? First/second-order/deferred ripples,
   trade-offs between structures, the rollback path.
5. **KAEL-EM, the Dreamer** — what are we not considering? One or two alternatives tied to a
   concrete connection, maybe one reframe; hand each to Vael for a stress-test.
6. **Chair synthesizes** — decide (a path, an alternative, or a blend that keeps each side's
   core and its weakness visible). State the accepted risk and the rollback. Record dissent verbatim.

## Record it

Store a dual-layer memory so the next session can recall it:

```bash
voidloom store --content "[OBJECTIVE] COUNCIL <date>: <decision> → <outcome>; Orin: …; Vael: …; Dessa: …; Kael-Em: … [SUBJECTIVE/WHY] <why this path, what risk was accepted, dissent>" \
  --category technical_decision --importance 0.85 --tags council,inner-council,decision
```
