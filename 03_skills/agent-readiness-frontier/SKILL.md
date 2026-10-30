---
name: agent-readiness-frontier
description: Standing radar for the agentic-web frontier plus a fleet-propagation method. Monitors agent-readiness and AEO standards (ARDS, Cloudflare agent-readiness, Web Bot Auth, MCP server-card, DNS-AID, NLWeb, llms.txt) through a Standing Monitoring List with version-check-before-build; keeps a deployment matrix of every site you run; gates adopt/replace/augment decisions behind a Frontier Decision Gate (a full Inner Council deliberation); propagates an adopted change across all your sites through one ACE loop that ends in a verified redeploy per site. Capability-agnostic (ARDS is the first case study). Trigger on "frontier radar", "agent-readiness frontier", "propagate ARDS to the fleet", "deployment matrix", "version-check the agent-readiness standards", "evaluate <technique> for the fleet".
---

# Agent-Readiness Frontier

A method for keeping every website you run current with the fast-moving "agent-ready web" standards, without chasing every announcement.

**What is not included in this package:** the full standalone automation this skill was cut from (its persona, operating manual and post-run self-heal protocol). This file carries the method itself, which is enough to run it by hand. The pieces it leans on that DO ship are named below.

## What this method does
1. **MONITORS** the agent-readiness / AEO frontier through a Standing Monitoring List (version-check-before-build; act on a delta only).
2. **OWNS** a deployment matrix: one file you keep in your own project, for example `docs/deployment_registry.md`, with one row per site (domain, host, live or preview, last verified date, which agent-readiness features it serves). Read it first, write it last. Keep it out of any public repo if it names private hosts.
3. **GATES** any adopt/replace/augment decision behind the Frontier Decision Gate (a full Inner Council deliberation; fires only on a genuine frontier delta).
4. **PROPAGATES** an adopted change across every site through one ACE loop over the matrix (one design-generator / reflector / curator pass, then per site: verify cutover state, redeploy, write the result back to the matrix).

## Non-negotiables
- **Version-check FIRST.** Before building anything, check the current published version of every standard on the list against the version recorded in your matrix. No delta: log it and stop. Prefer this because most "new standard" news is a re-announcement, and building against an unchanged spec wastes a full loop.
- **Frontier Decision Gate before any frontier decision.** Run `/inner-council` (shipped in this package under `04_reasoning/commands/inner-council.md`) on the question "adopt, replace, augment, or hold?" and name the scope fence every time: which sites, which feature, what is explicitly out.
- **Use the official design agents for every ACE-loop generation** (`design-generator`, `design-reflector`, `design-curator`, shipped in `05_automations/agents/`). Never self-pilot the generator, because a generator that grades its own work drifts toward approving it. The same applies to reflector and curator.
- **Verify live-vs-preview / cutover state before any production redeploy.** Some sites sit ambiguously between a preview deployment and the live domain; never promote a preview by accident.
- **Draft standards are advisory; one score is a hard gate.** Treat conformance to draft standards as advisory. The one hard gate is a public agent-readiness scanner score: `isitagentready` at 70 or above (as of October 2026; re-check before relying on it, both the tool and the threshold).
- **9.80/10 HARD reflector floor** on the fleet-propagation loop, with the reflector re-verifying independently rather than trusting the generator's notes.
- **Close every run with a short self-review**: what changed in the standards, what changed on each site, what the matrix now says, and what you would check sooner next time. Store it in your memory brain.

## Startup recall
If you run the Voidloom memory brain, start with one `voidloom batch-recall` over: the standards on your monitoring list, your deployment matrix, and any prior frontier decision. State what came back before deciding anything.

## Boundary
- Agent-readiness / AEO frontier plus the deployment-matrix fleet: THIS method.
- General stack, tooling and infrastructure choices: decide them separately, with the same Frontier Decision Gate.
- First-time site builds: the `client-site-first-build` automation (`05_automations/client-site-first-build/`). Run this method as the last step of a first build, so the new site enters the matrix.
