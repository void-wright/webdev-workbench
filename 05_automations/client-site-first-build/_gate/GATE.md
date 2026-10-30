# THE GATE: site cohort (client-site-first-build · website-maintenance · resource-hub-maintenance)

> Generic edition. **Status: DRAFT definition, NOT YET CONNECTED TO AN EXECUTOR.** It defines how the three site automations should decide "done"; until an executor uses it, the reflector's stop rule (9.8/10 HARD, every dimension ≥ 9.5, every empirical check green) remains in effect. Change the gate here and nowhere else.

## Why it exists

The three site automations share one engine (generator → reflector → curator) and state "9.8/10 HARD" in several places. A score is not the same thing as a gate: adding an image after review can make the shipped bytes differ from the bytes covered by a SATISFACTORY verdict. A composite score and a written rule cannot prevent that mismatch. The verdict must be bound to the bytes it describes.

## 1. The stop predicate (the only conditional)

A round terminates SATISFACTORY iff **zero OPEN findings of class DESTROYS · LIES · DOESN'T DELIVER · UNBOUND** remain on the artifact **at the verdict's subject hash**, and the deterministic tier passed on the re-rendered bytes. The dimension scores and their composite are published and ranked; they appear in no conditional.

## 2. The four classes, site-shaped: each settled by an observation the reviewer PERFORMED

| class | on a site, the product… | the observation that settles it |
|---|---|---|
| **DESTROYS** | a route, redirect, form endpoint, schema block or asset that existed at the start is absent or altered outside the pre-listed change set; or the shipped bytes are not the verdict's bytes | route inventory at HEAD vs the change list (`find "$BUILD_OUTPUT" -name '*.html'`, with `BUILD_OUTPUT` set to the build output directory, plus the sitemap and redirect configuration); the served tree's hash vs the hash in the last SATISFACTORY reflection; slug fidelity |
| **LIES** | a claim that affects a reader's decision, such as a kitchen-equipment maker's claim that a product fits a particular cabinet opening, is contradicted by the product's own record, such as a spec sheet or configuration data | the claim ledger: relation, locator, source, passage; CONTRADICTED = Critical |
| **DOESN'T DELIVER** | a deterministic check fails under a frozen severity map: build, axe Critical/Serious, Lighthouse below the derived tolerance, schema validity, CSP, header posture, links, form allowlists | the check's own output on the re-rendered bytes |
| **UNBOUND** | a rule the guide states has no executing check | a census of rule-shaped prose vs executing checks; a rule with no executor is identified as unimplemented, never treated as enforced |

Anything the reviewer cannot settle by an observation it performed is Medium/Low and goes in the ledger.

## 3. The finding schema

A finding is admitted only if its citation string-matches the artifact AND its `file:lines` locator resolves to a span that contains the citation. Listing checks without executing them can let fabricated citations pass. Fields: class · observation (the command) · evidence (the output) · citation · locator · blast radius · reproduced · state (`OPEN` / `WITHDRAWN` on the reviewer's side only). The reviewer's starting state is the evaluation criteria and the artifact, never the generator's self-estimate or the previous round's number.

## 4. The claim ledger

Every claim that affects a reader's decision in the shipped bytes has a row: relation · locator · source (code path, fact digest, the run's own inputs, a fetched outside source) · query · passage · verdict (SOURCED / SUPPORTED / CONTRADICTED / UNTRACEABLE / OWNER-ATTESTED / STRIPPED). Such a claim traceable to nothing is Critical; the sanctioned repairs are SOURCE or OMIT, never soften. A deletion between passes is a named STRIPPED row, never an unrecorded repair.

## 5. The epoch stamp (on every verdict)

Source tree hash and build output hash · this file's hash · task-spec hash · reflector-agent hash · severity-map hash · claim-ledger hash. A verdict is a statement about this tuple; any change invalidates it by default.

## 6. Open forks (the person who runs the automations decides; the reviewer does not)

1. Whether a fifth class, VISUAL-DEPARTS (a measured pixel diff against an approved reference), enters the gate.
2. Whether 9.8 stays a threshold or becomes a rank once the gate executes.
3. Who may waive what (only DESTROYS is never waivable).

## 7. What this gate does not catch

Tone, proportion, persuasion, whether the site operator will like it, whether an owner-attested claim is true, cross-site phrase reuse. Those live in the ledger and the dimension scores: published, ranked, never the gate.

## Standing rule

A gate that has not been watched firing on a defect already on the tree is not a gate: before trusting the first verdict, plant positive controls (a contradicted relation, an out-of-list route change, a severity-map failure), watch each fail as designed, and independently verify that each control introduced the intended defect.
