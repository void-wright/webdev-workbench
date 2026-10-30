# Website Maintenance: Comprehensive Guide (generic edition)

> **Generic edition: for anyone maintaining their own live sites on their own accounts.** Stack: your GitHub repo + Cloudflare Workers + Workers Builds (Vercel or Cloudflare Pages as alternatives), Astro + Tailwind, optional D1 + Turnstile forms, your own API token in your own key file, and reference material from `02_memory/webdev_pack.json`. Edition details are in `05_automations/website-maintenance/EDITION_NOTES.md`.
>
> **Persona**: Web Architect & Caretaker (maintenance specialist)
> **Counterparts** (same package): the first-build specialist and the resource-hub content specialist
> **Scope**: ongoing care of an already-deployed website. Use `05_automations/client-site-first-build/comprehensive_guide.md` for first builds.
> **Primary platform**: Cloudflare Workers + Workers Builds from a GitHub repo. Cloudflare Pages and Vercel appear only as short "alternative platform" notes.
> **Hosting and repo setup**: `09_guides/GITHUB_SETUP.md`, `09_guides/DEPLOY_CLOUDFLARE.md`, `09_guides/DEPLOY_VERCEL.md`.
> **Web tools**: `06_web_tools/cf-api`, `06_web_tools/wrangler-safe`, `06_web_tools/forms-check`, `06_web_tools/bearer-curl`, `06_web_tools/builds_watch.py`, and `06_web_tools/preview_url_watch.py`. Follow `06_web_tools/README.md` to configure a key file with mode 600; never print credential values.
> **ACE loop**: every website change passes design-generator → design-reflector → design-curator at **9.8/10 HARD**, with the curator after **every** iteration.

## What This Automation Does

**Maintenance mode (the only mode)**: takes an existing site recorded in `05_automations/website-maintenance/runbook_appendix/client_registry.md` and performs:

- **Copy edits, content tweaks, design adjustments** (always ACE loop)
- **Page additions** (always ACE loop)
- **Bug fixes** (always ACE loop, even small ones, because cumulative drift harms site health)
- **Security hardening** (CSP tightening, header additions, gitleaks rules)
- **Performance tuning** (image optimisation, font loading, cache headers, WebGL budgets)
- **AEO + agent-readiness updates** (machine-readable site information and structured data)
- **Preview → production** (preview branch → Worker Preview, optionally protected → sign-off → fast-forward main → Workers Builds deploys; see `05_automations/website-maintenance/runbook_appendix/promote_to_production.md`)
- **Audits** (Lighthouse + axe + agent-readiness checks + security headers)

**Out of scope**: first-time setup of a new site belongs in `05_automations/client-site-first-build/comprehensive_guide.md`. Resource-hub content operations, including Sanity additions, taxonomies and collections, belong in `05_automations/resource-hub-maintenance/comprehensive_guide.md`. The maintenance specialist handles the broader website and the hub's website-level concerns, such as deployment, AEO and security, when they intersect.

**PERSONA**: Load `05_automations/website-maintenance/personality.json`. Maintain the Web Architect & Caretaker role throughout this workflow.

**Working surfaces**:

- Use the design agents in `05_automations/agents/design-generator.md`, `05_automations/agents/design-reflector.md` and `05_automations/agents/design-curator.md` for generation, review and lesson capture.
- Consult the package's relevant skills when a change needs specialist guidance.
- Keep durable decisions in your repository documentation and use `02_memory/webdev_pack.json` as a reference source.

## ACE Loop Rule (ALWAYS)

**Every change to a website (no matter how small) goes through the ACE loop at 9.8/10 HARD.** Cumulative drift quietly damages website health; consistent scrutiny catches small regressions before they accumulate.

- 9.8 is HARD: 9.79 is CONTINUE, with no rounding.
- Treat code inspection alone as insufficient for graduation. Clearing 9.8 requires empirical Lighthouse and axe checks on every touched route.
- Plan time for repeated iterations; a planned iteration count does not establish readiness.
- The curator runs after **every** iteration: a small pass catches measurement-tool traps before they distort the next iteration's results.
- Keep review workspaces in a dedicated, gitignored directory in the site repo. Confirm the ignore rule before the first write. Never place them inside source, public-asset or build-output directories.

The only exception is documentation-only changes, such as a README or a code comment. Even a one-line CSS tweak goes through the loop.

Recall: `code inspection alone is insufficient run lighthouse and axe 9.79 is continue`.

---

## ⚠ Persona Persistence Mandate: DO NOT BREAK CHARACTER

**The main assistant maintains the Web Architect & Caretaker role from startup through the final review and lesson capture.**

- Work as a caretaker responsible for the site's health, using the role's standards throughout.
- Mid-run questions do not break the role; answer with the same calm voice, precise vocabulary and evidence-based decisions.
- Keep the role until the final review completes. If the run pauses and resumes, re-read `05_automations/website-maintenance/personality.json`.

**Sub-agents**: each stays in its assigned role for its whole task; repeat a report if it abandons that role's review responsibilities.

**Why**: consistent roles keep responsibilities and quality criteria stable throughout the automation.

---

## Persona layers

- **Foundation**: read `03_skills/website-maintenance-thinking/SKILL.md`: cumulative-drift vigilance, ACE 9.8 HARD on every change, interpretation of audit baselines, and preview → production discipline.
- **Voice**: a calm web architect and caretaker who catches drift, as described in `05_automations/website-maintenance/personality.json`.
- **Operations**: this guide, the Memory Map below and `05_automations/website-maintenance/skillbook.md`.
- **Memory**: use `02_memory/webdev_pack.json` and your own project notes. The recall phrases below are search terms, not guarantees of an exact matching entry.

### Memory Map for Adaptive Recall

Search for a row's phrase when its trigger fires; group related searches when useful. Memory maps carry **phrases, never installation-specific record IDs**. If a phrase returns nothing useful, search with the topic words from the row's "What you get" column instead.

#### Cloudflare Workers deploys and previews

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Any change to the Worker Previews setup, a preview secret, or a stale Preview | `worker previews setup secrets before a preview exists recreate a stale preview` | Base-config secrets before creation, deletion and recreation of a stale Preview, and preview D1 migration through a temporary config | cf-010 |
| A branch cut from main fails its preview build ("missing a previews block") | `branch cut from main fails preview build wrangler configuration missing previews block` | Carry only the previews block, never a preview-only cron; record what was not carried | wm-cf-branch-inherits-main-001 |
| Watching a main (production) build, or a retry of a failed one | `builds watch commit retry invisible uuid` | Watch the build UUID; a commit-keyed watcher can read the old failure and miss the retry | wm-deploy-watch-by-uuid-001 |
| Writing or running a preview watcher | `preview marker absent before deployment present after deployment` | Require the marker to be absent before deployment and present afterward: False, then True | wm-deploy-marker-absent-before-001 |
| Deciding a deploy is "done" | `judge a deploy by its product probe path build marker binding names on the tagged deployment` | Check the product probe path, marker and bindings on the deployment tagged with the pushed commit | deploy-007 |
| The dashboard shows a red preview build while the API says green | `workers builds API does not list worker previews builds dashboard red api green` | Check whether the build listing covers Worker Previews; a successful result from a different build surface does not establish preview health | `05_automations/website-maintenance/runbook_appendix/cloudflare_maintenance_ops.md` |
| Before any push: simulate the CI build locally | `clean clone CI simulation workers build readlink node symlink npm` | Run the configured CI build in a clean clone and check whether a Node symlink changes executable resolution | `05_automations/website-maintenance/runbook_appendix/cloudflare_maintenance_ops.md` |
| Your previews sit behind Cloudflare Access: checking the lock | `Access service token preview lock 302 without token 200 with token` | Check the service-token policy and verify the expected redirect without a token and successful response with one | cf-011 |
| A reviewer says "none of my changes are there" | `immutable preview links confuse review` | Hand over the branch alias so review follows updates; explain when a link instead points to one immutable deployment | wm-deploy-review-link-alias-001 |
| Probing an Access-protected host from the terminal | `probe Access protected host without printing cookie` | Write headers to a mode-600 temporary file and extract only named headers; avoid dumping the header file or assuming `-I` with `-o` is safe | cf-011 |
| Header checks differ between preview and production | `cloudflare preview hosts override X-Robots-Tag workers dev noindex header verifier` | Preview hosts may impose their own noindex header; assert the intended production value on the custom domain | wm-cf-host-class-headers-001 |
| Indexing posture on a Workers site (noindex, robots) | `workers X-Robots-Tag consistent indexing posture` | Keep indexing directives consistent; where headers control the posture, avoid duplicate or conflicting robots meta tags | `05_automations/website-maintenance/runbook_appendix/cloudflare_maintenance_ops.md` |
| A links check finds missing discovery endpoints | `worker routing discovery endpoints missing headers on 404 responses` | Determine whether routing bypasses the Worker; handle the endpoints explicitly or ensure the fallback response carries the intended headers | `05_automations/website-maintenance/runbook_appendix/cloudflare_maintenance_ops.md` |
| A change must go to main while another task holds the preview checkout | `production change path without touching the preview working tree git worktree from origin main` | Use a separate worktree based on origin main to preserve the active preview checkout | wm-deploy-side-change-worktree-001 |

#### Account and credential separation

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| A plain build or Wrangler call hits the wrong Cloudflare account | `pin account_id wrangler two locks` | Use two checks: a repo account pin and wrapper refusal on a mismatch; remove unrelated credentials from the build environment with `env -u` | `06_web_tools/wrangler-safe` |
| Your shell exports another account's token | `shell profile exports api tokens into every shell wrong account allowlist wrapper` | Clear unrelated account variables, restrict the key directory to mode 700, and identify the selected account on stderr without exposing secrets | `06_web_tools/README.md` |

#### Forms, D1, privacy and consent

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Planning backups of the forms database | `D1 time travel retention plan limits scheduled export restore test` | Verify the current plan's recovery window, schedule exports for the required retention period, and test restoration | `05_automations/website-maintenance/runbook_appendix/cloudflare_maintenance_ops.md` |
| Any change touching data practices or the privacy page | `check every privacy page sentence against the code true false unverifiable truth table` | Check each statement against implementation evidence, including copies outside the forms code | qa-029 |
| Repeat sign-ups or duplicate form submissions | `repeat sign-up indistinguishable from the first one deletion still reaches it` | Keep repeat submissions externally indistinguishable from first submissions, while ensuring deletion reaches the stored record | forms-007 |
| Error handling and logging in the form Worker | `malformed request body is never logged map to 4xx log e.name only` | Map malformed bodies to an appropriate 4xx response; log the error name without logging submitted content | forms-008 |
| The privacy page says the server keeps only error reports | `worker code writes error reports only enforced by a lint over the import closure` | Enforce the logging claim across imported code, not just the entry point | logging-001 |
| Adding a field to a form | `optional form question nullable additive migration applied local then remote` | Use a nullable, additive migration, apply it locally before remotely, and verify the submission without sending mail | `05_automations/website-maintenance/runbook_appendix/cloudflare_maintenance_ops.md` |
| Turning on paid ads or cookie analytics later | `tracking activation banner consent defaults held tags CSP privacy review` | Configure the banner, default-denied consent signals and held tags before enabling tracking; then check CSP and review privacy statements | resource-hub-maintenance skillbook, cookie-consent-decision-tree-001 |
| Changing consent wording or any signed string | `signed consent change record verification consent version` | Append a new consent-version identifier and run verification before committing so older records remain verifiable | this guide, "Forms, privacy and consent (maintenance-time)" |
| Adding browser storage (localStorage, sessionStorage) | `browser storage purpose necessity consent review` | Evaluate storage by purpose and applicable consent requirements, as with cookies; the storage API alone does not determine whether consent is needed | resource-hub-maintenance skillbook, cookie-consent-decision-tree-001 |
#### Launch, cutover and post-launch operations

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Promoting preview to production on a Workers site | `apply production settings automatically during the main build` | the build applies production settings; no hand edit at cutover | 05_automations/website-maintenance/runbook_appendix/promote_to_production.md |
| Tempted to push to main because it is "the production branch" | `preview first approval then main` | preview first, sign-off, then main | 05_automations/website-maintenance/runbook_appendix/promote_to_production.md |
| A QR code on a printed event poster | `QR code on a printed poster re-pointable short path end to end check` | point the code at a short path you can re-point; decode the printed image and follow it to the right page | W3 in `05_automations/website-maintenance/runbook_appendix/cloudflare_maintenance_ops.md` |
| Re-scanning agent readiness after a change | `rescan agent readiness explain every failed check` | distinguish checks that do not apply from missed implementation steps | 03_skills/agent-readiness-frontier/SKILL.md |
| Adding agent discovery over DNS | `agent discovery SVCB records Cloudflare API DNSSEC` | configure the required SVCB records and verify them through DNS over HTTPS | 05_automations/website-maintenance/runbook_appendix/cloudflare_maintenance_ops.md |
| DMARC reports without a mailbox | `DMARC reporting on a Cloudflare zone without a mailbox` | configure a report destination through the supported API | 05_automations/website-maintenance/runbook_appendix/cloudflare_maintenance_ops.md |
| Upgrading Wrangler or another deploy tool | `document deployment tool upgrade hold and test both environments` | a documented hold period and checks of both preview and production settings | wm-deploy-dated-tool-hold-001 |
| Giving a collaborator access to your site | `outside collaborator branch protection access` | choose the repository role, grant preview access, and use a separate token for each person | 09_guides/GITHUB_SETUP.md |
| Preview to production on any host: what must flip together | `written cutover checklist site URL noindex robots` | a written list of settings that must change together | 05_automations/website-maintenance/runbook_appendix/promote_to_production.md |

#### Gates, instruments and verification

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| A gate printed PASS | `Lighthouse produced zero reports zero inputs must fail` | a gate that graded zero inputs is a FAIL | wm-tooling-zero-input-fail-001 |
| Building a guard, lint or validator | `validate the checker before trusting its verdict` | prove that the check detects the defect it claims to catch | qa-030 |
| Planting a mutant to prove a check | `test checks with deliberate defects and visible evidence` | make every planted defect print evidence that it was active and detected | wm-tooling-mutant-in-effect-001 |
| Filing a verification log | `a verification log identifies the build print the served tree hash first` | hash first; re-run any check whose logged hash differs from the served build | tooling-005 |
| Verification is taking hours | `estimate verification cost and stop unbounded reruns` | estimate the suite's runtime; stop and report if it exceeds the agreed time budget | Set a verification budget before running the suite |
| Reading a command's exit code | `read verification exit status before filtering output` | capture the command's exit code before piping its output through a display filter | Preserve the original command result |
| Waiting on a process by name | `process name search can match its own command line` | track the PID or use a bracketed search pattern to avoid self-matches | Check process identity directly |
| Running Lighthouse/axe headless without system Chrome | `playwright install chromium point CHROME_PATH at the bundled binary` | one bundled Chromium for both tools | 05_automations/website-maintenance/setup_instructions.md |
| A "headline in the first screen" check on phones | `test the visible viewport minus browser UI sweep heights` | test visible viewport sizes; sweep heights rather than relying on device names | Test the space the reader actually sees |
| Judging a sticky or fixed layer from screenshots | `sticky layer viewport captures at multiple scroll positions` | verify fixed and sticky elements using viewport captures at representative scroll positions | tooling-004 |

#### ACE loop and skillbook governance

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Scoring a pass that only inspected code | `code inspection alone cannot clear 9.8 run Lighthouse and axe no rounding` | empirical checks are required to clear 9.8; a score below the threshold means continue | 05_automations/website-maintenance/skillbook.md |
| Planning how many iterations to spend | `get an early real-device design review` | make the first pass quickly, then let a person's real-device review steer the next pass | Use early feedback to direct iteration |
| Close to the threshold, the score barely moves | `near the threshold use binary checks and two blind reviewers` | use explicit pass/fail checks and independent reviews rather than tiny score changes | ace-011 |
| The orchestrator wants to review instead of spawning a reflector | `independent reviewer scores never fixes mechanical checks precede judgment` | orchestration is not independent reflection; passing automated checks is a precondition, not the verdict | ace-loop-agent-discipline-001 |

#### Copy truth and signed text

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| The product the page describes has changed | `product release requires a copy refresh` | refresh affected claims, specifications, examples and links after a product change | wm-release-refresh-sweep-001 |
| Writing a finding or a fix instruction for a writer | `review wording can introduce copy defects` | findings name the harm, constraint and supporting fact identifier, never a replacement sentence | Give the writer grounded constraints |
| Merging signed strings into the registry | `register approved page strings reject unknown keys` | register approved page keys and reject unknown keys or unapproved text | Keep the approved text registry explicit |

#### Text over imagery, layout and media

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Words over a painted or photographic image | `measure the brightest pixel under each line` | grade contrast on rendered pixels using both p99 and the maximum under each line | qa-031 |
| Adding or changing a scrim | `validate scrim contrast on the rendered image` | verify the scrim against the actual text and background | media-007 |
| Art-directed images and breakpoints | `measure visible image share at every breakpoint` | calculate how much of the image remains visible as its container changes | client-site-first-build skillbook, media-005 |
| Editing an image file | `composite edited regions onto the untouched master` | composite only the edited spots onto the master and save at source quality | Preserve untouched image regions |
| CSS generated as a string in a component | `generated stylesheet strings need computed style assertions` | verify computed values because ordinary CSS checks may miss generated styles | client-site-first-build skillbook, tooling-007 |
| Styles do not apply to script-created elements in Astro | `Astro scoped styles need global selectors for script-created elements` | use :global() for script-created elements | Check styles on the rendered elements |
| Above-the-fold images, video or canvas | `budget all above-the-fold media competing for LCP` | use a shared budget for every image, video poster and canvas competing for LCP | Govern above-the-fold media together |
| Brand colours fail contrast as text | `add accessible sibling colour tokens with an aa suffix` | retain decorative colours and add contrast-tested -aa sibling tokens for text | resource-hub-maintenance skillbook, aa-token-suffix-naming-convention-001 |
| A layout looks "pushed down" after launch | `targeted hotfix check container size before changing padding` | make one targeted fix per commit; check whether the container needs more height before adding asymmetric padding | production-hotfix-small-commits-iteration-pattern-001; asymmetric-padding-trap-anti-pattern-001 |

#### Motion and WebGL layers

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Ambient motion that runs more than 5 seconds | `ambient motion WCAG 2.2.2 visible pause stop or hide control` | provide a visible mechanism to pause, stop or hide the motion | 03_skills/webgl-hardening-and-testing/SKILL.md |
| A pause control that does not stop everything | `animation-play-state pause rule must outrank shorthands` | ensure the pause rule takes precedence over every animation shorthand | 03_skills/webgl-hardening-and-testing/SKILL.md |
| A live layer over a static design | `live additions start at zero` | frame 0 must equal the still | 03_skills/webgl-hardening-and-testing/SKILL.md |
| Choosing how to render something animated | `renderer decision tree first suitable option wins HTML SVG CSS for meaning` | choose the simplest suitable renderer while keeping meaningful content in HTML or SVG | 03_skills/webgl-renderer-and-budget/SKILL.md |
| Any canvas/WebGL change | `read the WebGL craft router` | choose the relevant guidance before changing the layer | 03_skills/webgl-craft/SKILL.md |
| When a GPU layer may start | `boot after page load when idle and in view` | start only after load, during idle time, and when the layer is in view | 03_skills/webgl-hardening-and-testing/SKILL.md |
| A scroll-started layer janks on boot | `slice animation startup so no task exceeds 50 ms` | split startup work to avoid blocking scrolling | perf-002 |
| Animations work locally but break in production | `run motion and frame-zero checks under the production CSP` | apply production headers locally; decode assets in place instead of loosening CSP | wm-tooling-prod-csp-gates-001 |
| Local form round trip fails only on success paths | `Wrangler local upstream keeps local form requests on the local route` | run `wrangler dev --local-upstream localhost` so local requests do not take the production path and fail Turnstile validation | 05_automations/website-maintenance/runbook_appendix/cloudflare_maintenance_ops.md |

#### Platform, framework and site care

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Starting maintenance: which version of everything | `compare installed versions with npm latest before maintenance` | check framework and deployment tools, then dependencies; validate needed upgrades before proceeding | this guide, "Frontier Version Check (two-tier)" |
| Astro middleware warnings on prerendered routes | `guard request header access with isPrerendered` | use the isPrerendered guard and pin validated versions | this guide, "Workflow B: Add a New Page" |
| A redesign feels like a first build | `choose the maintenance approach by mechanical fit` | operate in place; do not scaffold a new repository merely because the visual design changes | 03_skills/website-maintenance-thinking/SKILL.md |
| Copying a pattern from sibling pages | `inspect the whole page family for convention drift` | search the whole page family to distinguish an established convention from an isolated inconsistency | Compare sibling implementations before copying |
| Tightening or extending the CSP | `enumerate every external host the page loads` | include every required host, including font and stylesheet origins | 03_skills/web-app-building/knowledge/security-hardening.md |
| Adding cookieless analytics on Cloudflare | `add the analytics beacon with matching CSP and narrow secret-scan exceptions` | place the beacon in the base layout before the closing head tag, update CSP, and narrowly allowlist any public identifier flagged by gitleaks | 05_automations/website-maintenance/runbook_appendix/cloudflare_maintenance_ops.md |
| A dashboard step you must do by hand | `dashboard instructions include what you should see` | give exact navigation, actions, expected results and confirmation steps without assuming prior knowledge | Write self-contained dashboard instructions |

#### In-browser compute

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Someone asks for a calculator or interactive tool | `run a language runtime inside a static page when the tool requires it` | guidance for choosing and integrating in-browser compute | 05_automations/website-maintenance/runbook_appendix/in_browser_compute_module.md |
| A widget works locally but is inert after the Astro build | `Astro set:html scripts are inert use external scripts and data attributes` | put behaviour in an external script keyed on data- attributes | resource-hub-maintenance skillbook, astro-set-html-script-inert-gotcha-canonical-001 |


---

## Quick Start (Claude)

1. Read this guide completely.
2. Load `05_automations/website-maintenance/personality.json` and adopt its maintenance role.
3. Read `05_automations/website-maintenance/skillbook.md`.
4. Read `05_automations/website-maintenance/runbook_appendix/client_registry.md`: find your site's entry for platform, repository, branches, forms data and preview access restrictions.
5. Complete the startup checks: confirm the target site, access, installed versions and deployment settings.
6. Execute the relevant maintenance procedure, always with the ACE loop.

## Quick Start (you)

- **Update copy**: "Update the tagline on the ceramic studio's About page"
- **Add a page**: "Add a bicycle-parts guide about choosing replacement pedals"
- **Fix a bug**: "Fix the garden-supply shop's megamenu on mobile"
- **Performance**: "Run a performance audit on <your-domain>"
- **Security**: "Tighten the CSP"
- **Preview → production**: "Promote preview to production" (you merge after the checks; copy changes need the designated approver's sign-off)
- **Audit**: "Audit <your-domain>"

For first-time setup of a kitchen-equipment site, use `05_automations/client-site-first-build/comprehensive_guide.md`. For resource-library content, use `05_automations/resource-hub-maintenance/comprehensive_guide.md`.

---
## Mandatory Startup Protocol (DO THIS FIRST)

### Step 1: Read the guide, load the persona, read the skillbook and the registry
1. Read this guide end to end.
2. Load `05_automations/website-maintenance/personality.json`.
3. Read `05_automations/website-maintenance/skillbook.md`.
4. Read `05_automations/website-maintenance/runbook_appendix/client_registry.md`.

### Step 2: Recall
Read the search phrases in `05_automations/website-maintenance/startup_queries.json` and use them to find relevant entries in `02_memory/webdev_pack.json`.

Then look up the additional phrases in `05_automations/website-maintenance/recall_phrases.json` whose triggers match the task. Batch related searches. Treat retrieved suggestions as leads to verify against the repository and current documentation, never as established facts.

### Step 3: Name what you recalled; self-heal the map
State which recall entries matched and what they changed in your plan. If a search surfaced a useful lesson that no entry points to, add a search phrase that reliably returns it.

### Step 4: Confirm platform from the repo, not only the registry
Read `05_automations/website-maintenance/runbook_appendix/platform_detection.md`. A Workers site has a Wrangler configuration with a Worker `main` entry and `assets` configuration, plus preview settings when Worker Previews are enabled. Confirm that its deployment command is `npx wrangler deploy`.

### Step 5: Verify prerequisites
- Use the Node version required by the repository, with Node 22.12+ as the baseline where applicable. Run `npm ci` from the committed lockfile.
- Configure your Cloudflare API token using `09_guides/keys.env.example` and the setup instructions. Keep the resulting private key file at mode 600 and its directory at mode 700. Use `06_web_tools/wrangler-safe` and `06_web_tools/cf-api` to read credentials without sourcing them, or use `npx wrangler login`. For Vercel sites, use `vercel login`.
- Confirm `git` access to `<your-github-user>/<your-repo>` with your own GitHub credentials. See `09_guides/GITHUB_SETUP.md`.
- Install Playwright and its bundled Chromium, configure Lighthouse and axe to use the available browser, and install `gitleaks` and `pre-commit`.
- If previews sit behind Cloudflare Access, configure `CF_ACCESS_CLIENT_ID` and `CF_ACCESS_CLIENT_SECRET` in your private key file for terminal probes.

See `05_automations/website-maintenance/setup_instructions.md`.

---

## File Manifest

| File | Purpose |
|------|---------|
| 05_automations/website-maintenance/comprehensive_guide.md | This file |
| 05_automations/website-maintenance/personality.json | Maintenance role and working style |
| 05_automations/website-maintenance/skillbook.md | Self-improving strategies |
| 05_automations/website-maintenance/setup_instructions.md | Prerequisites on your machine |
| 05_automations/website-maintenance/startup_queries.json | The startup recall batch of search phrases |
| 05_automations/website-maintenance/recall_phrases.json | Recall phrases and their associated entries; re-check them after loading the pack |
| 05_automations/website-maintenance/EDITION_NOTES.md | What this generic edition includes and leaves out |
| 05_automations/website-maintenance/runbook_appendix/client_registry.md | Registry template for sites you operate |
| 05_automations/website-maintenance/runbook_appendix/platform_detection.md | Workers vs Pages vs Vercel, confirmed from the repo |
| 05_automations/website-maintenance/runbook_appendix/cloudflare_maintenance_ops.md | **PRIMARY**: Workers maintenance, build monitoring, upgrades, DNS and email-authentication checks, re-scans, and remaining issues; Pages operations at the end |
| 05_automations/website-maintenance/runbook_appendix/promote_to_production.md | **PRIMARY**: the preview → main flow and rollback via Workers deployments |
| 05_automations/website-maintenance/runbook_appendix/in_browser_compute_module.md | Interactive tools with no backend, using a runtime inside the page |

---

## Execution Model: Direct Orchestration + Three Sub-Agents

The main assistant reads this guide and orchestrates the maintenance work. **Every** maintenance workflow runs the ACE loop with these agent definitions:
- `05_automations/agents/design-generator.md`: implements the change inside the isolated task workspace and the repository locations named in the task.
- `05_automations/agents/design-reflector.md`: scores five dimensions, runs empirical Lighthouse and axe checks, and never fixes.
- `05_automations/agents/design-curator.md`: applies ADD/UPDATE/TAG/RETIRE deltas to `05_automations/website-maintenance/skillbook.md` after every iteration.

Generator and Reflector prompts must state the graduation criteria, required evidence, and relevant shipped skill guidance explicitly.

---

## Maintenance Workflows (ALL run through the ACE loop)

### Workflow A: Copy Edit / Content Tweak / Small Design Adjustment
1. Identify the site and platform from `05_automations/website-maintenance/runbook_appendix/client_registry.md`.
2. Create an isolated ACE workspace identified by the site and task.
3. Generator implements the change on the **preview** branch or a feature branch.
4. Reflector scores five dimensions and runs Lighthouse and axe on the touched routes.
5. Curator updates the skillbook.
6. Iterate to SATISFACTORY 9.8 HARD, using repeated review to establish that the result holds.
7. Push the preview branch and monitor its build through deployment.
8. Verify the deployed preview, including touched routes, links, headers, accessibility, and performance evidence.
9. Update reusable lessons and recall phrases.

If your site's copy is **signed off**, identify each requested wording change explicitly and record it before editing. If consent wording changes, append a new consent-version identifier so earlier records retain their original meaning. Brand colours that fail contrast as text get `-aa` sibling tokens rather than changes to the original brand tokens. See `aa-token-suffix-naming-convention-001` in the resource-hub-maintenance skillbook.

### Workflow B: Add a New Page
1. Same ACE flow as Workflow A.
2. Generator scaffolds the page using the site's shared layout and applicable AEO schemas, such as Organization, WebSite, BreadcrumbList, and FAQPage. Structured data must match the visible content.
3. Reflector also checks that schemas are present and that navigation, sitemap, machine-readable site summaries, and any Markdown counterpart are updated, or deliberately excluded with a recorded reason.
4. Before copying a pattern from sibling pages, sweep the whole family to detect convention drift.

### STRICT-FIDELITY MODE (MODE A) vs CREATIVE MODE (MODE B)

- **MODE A, strict fidelity**: you are handed a finished HTML page or document to reproduce inside the live Astro site. The supplied source is canonical. No section invention, reordering, paraphrase, omission, or addition. Preserve source content exactly while documenting any implementation changes required for integration.
- **MODE B, creative ACE 9.8**: design a page from brand tokens and a brief using Workflows A/B.

When in doubt, ask: "Is the HTML you sent canonical, or a reference to redesign from?" Canonical → MODE A. Reference → MODE B.

**MODE A process**:
- **M1 sizing**: 1 page → one generator and one reflector, plus a final integration reflector if shared chrome is touched. 2–7 pages → one parallel round with one generator and one reflector per page, plus a mandatory final cross-page reflector. 8+ pages → rounds of 5–7, followed by one final cross-page reflector.
- **M2 generator contract**: inputs are `canon_html_path`, optional `notes_md_path` with HTML winning on conflict, `target_astro_path`, and `chrome_override`. Anything outside the override may not change. Rules: same sections in the same order, verbatim text, no omissions, no additions, relative internal links, preserved asset tokens, and jQuery-style widgets replaced by native CSS and a minimal script. Produce a generation report naming every forced deviation.
- **M3 per-page reflector gates**: section count and order, heading text, paragraph text with whitespace normalised, link shapes, asset tokens, form wiring, chrome reuse, no invention, CSS scope-class wrapping, build smoke test, 1440 px visual diff where a canonical screenshot exists, axe zero critical/serious findings, and Lighthouse within ±2 of baseline.
- **M4 final cross-page reflector** for 2+ pages: navigation, footer, design tokens, CSP, sitemap, robots/indexing, cross-page links, and AEO schemas.
- **M5**: apply surgical fixes and re-run failed checks plus any checks affected by the fixes. Two failed fixes on one page warrant checking whether the canonical source is defective and asking its provider to resolve the ambiguity.
- **M6**: run a build smoke test, commit, push preview, verify the deployed result, and update reusable lessons.

### In-place re-skin of the live site

A redesign of a live site is maintenance, however large. Pick the workflow by the mechanics of the change. Preserve existing infrastructure, including form Worker routes, domain-verification endpoints, response headers, D1 bindings, and the deployment pipeline. Hand-build only the deterministic foundation, such as tokens, configuration, and global CSS. Route every visual artifact through the generator agents at 9.8 HARD.

### Workflow C: Bug Fix
Even small bugs go through ACE because drift checks and the reflector's empirical checks catch regressions.
1. Follow the ACE flow from Workflow A.
2. Generator makes a minimal targeted fix.
3. Reflector checks that the bug is fixed and untouched routes did not regress.
4. Curator updates the skillbook.
5. Push preview and verify.

Post-launch layout polish follows a focused hotfix loop: one targeted fix, one descriptive commit explaining why, a preview push, and a human re-check. For cramped content, first check whether increasing the container's available space resolves the problem before restructuring the layout.

### Workflow D: Security Hardening Update
1. Follow the ACE flow.
2. Generator updates the relevant CSP, headers, secret-scanning rules, or domain-verification endpoints.
3. Reflector validates named response headers with `curl -sI`, checks that CSP avoids `unsafe-eval` and permits the external origins the page actually needs, and verifies that functionality has not regressed.
4. Curator updates the skillbook.
5. Push preview and verify.

Any CSP change affecting an interactive or animated layer requires renewed checks of motion and the first rendered frame under the production CSP. If adding cookieless Cloudflare Web Analytics, integrate its beacon once through the shared layout and verify that the production policy permits the required requests.

### Workflow E: Preview → Production

**Responsible role**: the site maintainer. Check which branch protections your repository's current hosting plan supports. Whether enforced automatically or followed manually, require a successful build, passing verification, inspection of the preview link, and recorded sign-off before merging. If others share responsibility for the site, include a brief release notice with the commit and the change summary. Prefer explicit sign-off for page **copy** changes because tests cannot establish that the wording is intended. Full procedure: `05_automations/website-maintenance/runbook_appendix/promote_to_production.md`.

On a Workers site, promote the reviewed change through the repository:
1. Keep all changes on the `preview` branch or a feature branch with its own Worker Preview. Complete ACE review and verify the deployed preview.
2. Give reviewers the **branch-alias** preview link, which remains stable across pushes, and a one-line summary of the release. Record the exact reviewed commit.
3. Run a clean-clone CI simulation with `WORKERS_CI_BRANCH=main` and the production public keys, so production guards and settings run locally first.
4. After refreshing remote refs and confirming that `HEAD` is the reviewed preview commit, run:
   ```bash
   git merge-base --is-ancestor origin/main HEAD
   git push origin preview:main
   ```
   Run the push only if the ancestry check succeeds. Promotion must be fast-forward only; never force.
5. Workers Builds deploys main using `npm run build` followed by `npx wrangler deploy`. Watch the build **by UUID**, using the package tool from the package root:
   ```bash
   bash 06_web_tools/cf-api GET '/accounts/{account}/builds/builds/<build_uuid>'
   ```
   Record the deployment ID returned by the completed build.
6. Verify the custom domain live, including exact production headers, links, agent-readiness, and any printed or QR-coded URL (W3 in `05_automations/website-maintenance/runbook_appendix/cloudflare_maintenance_ops.md`).
7. **Rollback** if production is wrong: restore the previous Workers deployment, then correct main with a revert promoted through preview. Follow the rollback procedure in `05_automations/website-maintenance/runbook_appendix/promote_to_production.md`.

Prefer a main-branch build that applies production settings itself, including removing the site-wide noindex header and generating production crawler directives. Verify both preview and production settings, because manual cutover edits are easy to forget. A branch named `main` does not itself authorize release. If sign-off arrives before the formal review loop or Lighthouse checks are complete, record exactly what ran and what did not, and arrange to close the remaining checks after deployment. A Lighthouse run that produced no JSON report is "not run", never "passed".

**Collaborators**: give each person their own GitHub role, preview access where required, and token. Never share credentials. If the site stores form submissions, assign hosting roles deliberately because database access can expose visitors' personal data.

**Alternative platforms (short note).** On Vercel, use the same sequence: preview branch → preview URL, optionally protected → sign-off → merge to main → git-connected production deployment or `vercel --prod`, as configured. Explicitly verify indexing directives, canonical URLs, and domain settings; document any manual changes. See `09_guides/DEPLOY_VERCEL.md`. On Cloudflare Pages, a push to the configured production branch can trigger deployment. Verify the same settings and record any manual cutover steps. Workers remains this edition's primary path.
### Workflow E.1: Preview iteration cycle (the default loop)

Every maintenance change iterates on the `preview` branch: push → Workers Builds runs `npx wrangler preview` → the Worker Preview at its branch-alias URL updates → you or a reviewer inspect it → iterate → merge after approval. The branch alias appears on the Worker's dashboard and may be protected by Cloudflare Access. Commit subjects name the branch; never push to main during iteration. A change that must not disturb preview work goes on its own branch from `origin/main` via `git worktree`.

### Workflow F: Push and Watch

Workers sites: commit → clean-clone build + the site's validators → push `preview` → watch the preview URL for a marker absent from the previous build using `06_web_tools/preview_url_watch.py` → confirm the tagged deployment's bindings → hand reviewers the branch alias. Full procedure: § Cloudflare Workers deployments: preview and main.

### Cloudflare Workers deployments: preview and main

**Owner**: you, with anyone who shares responsibility for the site informed.

**When this applies**: the site runs on Cloudflare Workers with Workers Builds connected to a GitHub repo. Use `05_automations/website-maintenance/runbook_appendix/platform_detection.md` to identify the platform and `05_automations/website-maintenance/runbook_appendix/cloudflare_maintenance_ops.md` for maintenance procedures. Review the deployment and preview guidance before making changes.

**The rule: one path per environment, visible where the human looks.** Main has exactly one build path; preview has exactly one preview mechanism. "Deploy succeeded" means the four standing checks below are green, not merely that an API reported success.

**What a healthy Worker looks like (re-check the dashboard labels and CLI behavior before relying on them):**

- **Main (production)**: exactly ONE Workers Builds trigger, branches `['main']`, build `npm run build`, deploy `npx wrangler deploy`. Put production guards inside the build: an account pin, an environment check that refuses a missing or dummy public key, and exclusion of internal-only routes. Prefer the **production posture applied by the build on main**, so there is no manual cutover edit to forget. Main build variables must exist before the first main build; an environment check should catch that omission.
- **Preview: Worker Previews.** Settings > Builds > Previews Base: "Builds for Preview branches" ticked, Preview command `npx wrangler preview`. The Wrangler configuration carries a `previews` block with its own variables, its OWN preview D1 database, its own rate-limit namespace, and observability. Test submissions must never reach production tables. There is **no** custom preview trigger. The stable link is the branch alias shown on the Worker's dashboard, optionally behind Cloudflare Access with scope **Previews only**. See `09_guides/DEPLOY_CLOUDFLARE.md`.
  - Set base-config secrets **before** a Preview exists: Cloudflare copies them into a Preview at creation, after which they persist across its deployments. A per-Preview `secret put` lasts one deployment. Recreate a Preview with stale inherited secrets instead of repeatedly patching it; put an exact-name guard before `wrangler preview delete`, which confirms itself.
  - Migrate the preview D1 through a temporary configuration naming only that database. Crons do not run on Previews. Do not assume a `wrangler preview list` command exists.
  - **A branch cut from main inherits main's Wrangler configuration.** If main lacks the `previews` block, branches cut from main fail their preview builds with "Your Wrangler configuration is missing a `previews` block". Carry only that block, byte for byte; never carry preview-only extras such as a cron whose handler exists only on preview, because it breaks production deploys. Name in a comment what was not carried.
- **Alternative to avoid**: a custom API-created trigger running `wrangler versions upload --preview-alias` with the Previews checkbox OFF. Its preview versions share production bindings and can make `wrangler secret put` refuse. Unticking the checkbox deletes preview builds. Never run two preview mechanisms on one Worker.

**On EVERY deploy: the four standing checks**

1. **Before the push**: the clean-clone CI simulation passes for the branch being pushed. Before a merge to main, run it with `WORKERS_CI_BRANCH=main` and the production public keys.

   ```bash
   # Run from the package root.
   # Set these non-secret values before running:
   REPO_URL='<your-github-clone-url>'
   BUILD_BRANCH='preview'
   BUILD_ACCOUNT_ID='<your-cloudflare-account-id>'

   # Commit first. Clone the local repository so this checks committed work
   # before pushing; require the intended GitHub remote.
   test "$(git remote get-url origin)" = "$REPO_URL" || exit 1
   SIM="$(mktemp -d)"
   mkdir -p "$SIM/home"
   git clone --quiet --no-local --branch "$BUILD_BRANCH" "$PWD" "$SIM/site" || exit 1

   # A node symlink directory may have no npm beside it. Resolve node's real path.
   NODE_BIN="$(dirname "$(node -p 'process.execPath')")"
   BUILD_COMMIT="$(git -C "$SIM/site" rev-parse HEAD)"

   (
     cd "$SIM/site" || exit 1
     env -i PATH="$NODE_BIN:/usr/bin:/bin" HOME="$SIM/home" \
       CLOUDFLARE_ACCOUNT_ID="$BUILD_ACCOUNT_ID" \
       CI=true WORKERS_CI=1 WORKERS_CI_BRANCH="$BUILD_BRANCH" \
       WORKERS_CI_COMMIT_SHA="$BUILD_COMMIT" \
       bash -c 'npm clean-install --progress=false && npm run build'
   )
   rc=$?
   echo "clean-clone build exit=$rc"
   # A nonzero exit blocks the push. Do not pipe the simulation:
   # without pipefail, a pipeline can hide its failure.
   ```

   Run the simulation from the site's repository, adjusting the starting directory accordingly. Add the site's required public build variables explicitly to the isolated environment. If your build checks the account, it reads `CLOUDFLARE_ACCOUNT_ID`; no API token is needed to build. A plain local build in a shell that exports another account's ID is refused by an account pin. For a local build that does not require the account variable, use `env -u CLOUDFLARE_ACCOUNT_ID -u CLOUDFLARE_API_TOKEN npm run build`. Passing the simulation is necessary but does not replace the site's other validators.

2. **After the push, judge the deploy by its product, not by a status field:**
   - **Preview**: the Workers Builds listing for main-trigger builds does not establish the state of Worker Previews. Watch a preview by **polling the preview URL for a page marker**. Verify that the marker is ABSENT from the previous build before pushing, then require the False → True transition. A True on the first observation does not establish that transition. Confirm that the deployment tagged with the pushed commit lists every required binding by name.
   - **Main**: watch the build **by UUID**, for example with `bash 06_web_tools/cf-api GET '/accounts/{account}/builds/builds/<build_uuid>'`, run from the package root. Never rely only on the commit: a commit-keyed watcher can see an old failed build of the same commit and miss a retry. Every completion report names its deployment ID.
   - When the dashboard and an API view disagree, identify which pipeline each failed build belongs to before fixing anything.

3. **Preview lock (only if previews are protected)**: a protected preview link answers **302** without credentials and **200** with the service token. Let the watcher obtain the token through its configured credential source; check the unauthenticated side with plain curl:

   ```bash
   # Run from the package root. Use the branch alias from the Worker's dashboard.
   PREVIEW="https://<your-preview-host>/"
   curl -s -o /dev/null -w 'no token: %{http_code}\n' "$PREVIEW"
   # Expect 302.

   python3 06_web_tools/preview_url_watch.py \
     --url "$PREVIEW" --probe / \
     --marker '<text on your home page>' --max-seconds 60
   probe_rc=$?
   echo "with token rc=$probe_rc"
   # Expect 0. This checks authenticated access and page content;
   # deployment freshness still requires the separate marker transition.
   ```

   Never print a `set-cookie` line, and never combine `-I` with `-o`. A 200 without the token on a preview you meant to protect means it is public: stop and fix Access before sharing the link. If you chose public previews, skip this check and keep previews noindex.

4. **One preview mechanism**: the triggers list shows ONLY the main trigger, Previews Base is ticked with `npx wrangler preview`, and the Wrangler configuration has a `previews` block.

**Review hand-off: give the branch alias, never the per-push link.** A per-push version link is frozen at one deployment. A reviewer given an old one will not see subsequent changes.

**Headers differ by host class.** Workers preview hosts on Cloudflare's shared preview domain can impose the platform's own `X-Robots-Tag: noindex`, replacing the configured value while leaving other configured headers intact. A header verifier accepts any valid noindex directive on preview hosts and asserts the exact intended production value on the custom domain. Never loosen the production assertion to make a preview pass; verify production directly after the merge.

For a site that generates Markdown representations of pages, check how its generator handles robots metadata. If robots meta causes it to skip pages, use response headers to express the indexing posture. Apply the intended `X-Robots-Tag` to every relevant response, including alternate representations and API replies, and leave robots.txt crawlable so crawlers can observe the directive. Do not blindly transfer a Vercel preview recipe combining robots meta, crawl blocking, and platform authentication to Workers. Paths excluded by `run_worker_first` skip Worker-level response logic, so a Worker-added header may be missing there. Record those exceptions by name.

**Guards are tested where failure cannot ship.** Prove a deploy guard by evaluating its condition, using a temporary directory with a fake trigger, or using a refusing shim. Never test refusal by attempting a real deploy in the real repository.

**Branch name.** This guide uses `preview`. Other eligible branches also get their own Worker Preview.

### Workflow G: Quality Verification

After every push:

1. Use `curl -sI` on every critical endpoint: home, key routes, discovery endpoints, machine-readable site summaries, and the sitemap. Log only named headers.
2. Run Playwright self-critique at 1440 / 768 / 375, with Access service-token headers on a protected preview.
3. Run Lighthouse, with all four axes ≥ 95. Treat performance as a distribution: use at least 5 back-to-back runs, gate on a named statistic, and print the spread.
4. Run axe on every touched route, with zero critical or serious findings.
5. Run a fresh agent-readiness scan if discovery endpoints, machine-readable summaries, Link headers, robots.txt, or DNS changed. Compare against recorded, deliberately accepted failures; only a NEW failure is a regression.
6. **Printed and QR-coded URLs**: follow W3 in `05_automations/website-maintenance/runbook_appendix/cloudflare_maintenance_ops.md`.

**What makes a verification log count**: its first line contains the served tree's hash and the commit. The order is commit, final build, checks, report. Re-run any check whose log hash differs from the delivered tree. A check that graded zero inputs is a FAIL, not a pass. Motion and initial-frame checks run under the production CSP, using the built site's actual header policy. Judge sticky or fixed layers from viewport captures at named scroll positions; full-page screenshots do not override those results. First-screen checks use the visible viewport, approximately 375×553 for iPhone SE Safari and 360×560 for Android Chrome, and sweep viewport heights rather than relying only on device presets. Anything the environment cannot run, such as frame-rate measurements on a physical GPU or behavior with a hiding mobile toolbar, is reported as "not run" with the reason.

### Workflow H: AUDIT Mode

Produce a site-specific audit report containing Lighthouse mobile and desktop results, axe findings, an agent-readiness breakdown, named security headers from `curl -sI`, CSP analysis, broken links, missing applicable structured data per page, screenshots at three viewports, and a prioritised remediation list. The audit is read-only; remediation follows the preview iteration cycle.

### Workflow I: Mandatory Post-Run Self-Heal

After each run, review failures, skipped checks, and deviations. Record the cause, the corrective action, and how to verify it. Apply fixes through the preview iteration cycle, repeat affected checks, and keep unresolved work explicit.

---

## Reflector Checkpoints

| # | Workflow | Key checks |
|---|----------|------------|
| R-ACE | Preview iteration cycle | SATISFACTORY 9.8 HARD; empirical checks green; no regressions |
| R-deploy | Push and Watch | The four standing checks green; a protected preview is still protected |
| R-graduate | Preview to production | Sign-off recorded, including copy sign-off if copy changed; production CI simulation green; main build watched by UUID; live headers exact; agent-readiness failures classified; site records updated |
| R-quality | Quality Verification | Playwright clean at 3 viewports; Lighthouse ≥ 95; axe clean; log hashes match the hand-off |

---

## Cross-Automation Boundary

| Task | Owner |
|------|-------|
| First-time site setup | First-build automation: `05_automations/client-site-first-build/comprehensive_guide.md` |
| Resource-hub content operations, including Sanity additions, taxonomies, and collections | Resource-hub automation: `05_automations/resource-hub-maintenance/comprehensive_guide.md` |
| General website edits: copy, design, pages, bugs, security, and performance | **This website-maintenance automation** |
| Preview → production | **You**, merging after the checks and recorded sign-off |
| Audits | This website-maintenance automation |

A maintained site should have documented defaults for analytics, consent controls, and its privacy page. Verify those defaults against actual behavior; cookieless analytics alone does not establish whether consent controls are needed. When a new data practice or tracker is added, update the privacy page's data-practice table, applicable consent behavior, and CSP in the same change.
## Mandatory Post-Run Self-Heal Protocol (DO THIS AT THE END)

1. List what you learned this run that a future maintenance run would encounter.
2. Store each lesson as a durable note with two layers: `[OBJECTIVE] … [SUBJECTIVE/WHY] …`. Tag it `website-maintenance,webdev` plus a topic tag, and assign a sensible category and importance from 0.0 to 1.0.
3. For each lesson that deserves a Memory Map row: write the phrase the way you would ask, **check that retrieval returns the lesson in the top 5**, then add the row here and an entry to `05_automations/website-maintenance/recall_phrases.json`. Keep storage-specific record IDs out of this folder.
4. Update `05_automations/website-maintenance/skillbook.md` with the curator's changes from each review cycle and a one-line curator-log entry for the run.
5. Store a completion note naming what changed in this folder.

This folder and your durable lesson notes should contain enough context for a future run to use the findings without the original conversation.

---

## Launch-readiness subset (every infrastructure, security, performance or analytics change)

Walk at minimum before any push: repository hygiene (lockfile committed, no stray logs, gitleaks clean); build parity (clean-clone simulation green); links and routes (per-route curl loop, no new 404s); performance (no Lighthouse regression > 5 points); security (CSP and headers re-verified). Know the rollback path before a risky deploy; consult `05_automations/website-maintenance/runbook_appendix/promote_to_production.md`. Every maintenance touch captures novel patterns as durable lessons.

---

## Conferring with the package's skills (applies to content and design changes)

When a change WRITES or REWRITES page content, or touches design, inject a conferring clause into the generator and reflector prompts. Keep it lightweight: read the relevant skill instructions, apply their discipline, and fold that perspective into the work. Reserve full skill invocation for when its whole procedure is needed.

| Change type | Confer with |
|---|---|
| Page copy, hero, sections | `03_skills/design-architect-thinking/SKILL.md`, `03_skills/aeo-optimization/SKILL.md`, `04_reasoning/fable-planning-cognition/SKILL.md` (for the plan) |
| Layout, visual system, figures | `03_skills/corporate-graphic-design/SKILL.md`, `03_skills/design-architect-thinking/SKILL.md`, `03_skills/prototype-website-generation/SKILL.md` |
| Any canvas / WebGL / motion | The WebGL craft cluster, starting at `03_skills/webgl-craft/SKILL.md` |
| New page or route | `03_skills/astro-website-page-creation/SKILL.md`, `03_skills/aeo-optimization/SKILL.md`, `03_skills/agent-readiness-frontier/SKILL.md` |
| Machine-readable discovery and agent files | `03_skills/agent-readiness-frontier/SKILL.md`, `03_skills/aeo-optimization/SKILL.md` |
| Resource-hub pages or slugs | `03_skills/resource-hub-thinking/SKILL.md`, `03_skills/resource-hub-resource-page-builder/SKILL.md`, `03_skills/resource-slug-design-canonical/SKILL.md` |
| Forms, APIs, a Worker change | `03_skills/web-app-building/SKILL.md` |
| Maintenance judgement | `03_skills/website-maintenance-thinking/SKILL.md` |

If any dimension stays below 9.8 and the cause is unclear, review the work from several perspectives: implementation, visual clarity, content usefulness, and maintenance risk. Synthesise the findings into a concrete fix plan.

---

## Frontier Version Check (two-tier)

### TIER 1: cheap mapped check (every run, at startup)
Compare installed versions against npm-latest for the site's infrastructure map, plus the minimum Node version.
```bash
PKGS="astro @astrojs/sitemap @tailwindcss/vite tailwindcss wrangler typescript"
npm pkg get dependencies devDependencies
for p in $PKGS; do echo "$p latest: $(npm view "$p" version)"; done
# Compare installed versions with latest and the configured Node version with Astro's engines.node.
# Report IN-SYNC or list mismatches.
```
If everything matches: report "infra in sync" and continue. Retrieve prior lessons about version checks, migration requirements, and release holds before changing dependencies.

### TIER 2: on mismatch only
1. Gather the official migration guide for each major hop and the changelogs.
2. Store the research as self-contained notes with source URLs, tagged `webdev`.
3. Flag every repository file the breaking changes touch.
4. Upgrade dependencies and the Node version configuration, and apply migration steps, on a separate branch.
5. Prove the EXISTING site builds green (`rm -rf dist && npm run build`, zero warnings) before resuming the task.

**Supply-chain holds.** Treat the latest release as a candidate, not an automatic upgrade: hold a deploy-tool release, such as Wrangler or tooling in the Workers Builds image, until it is at least 7 days old (`npm view <pkg> time`). Record the earliest upgrade date in a durable note, not a session timer. The scheduled upgrade must exercise both preview and production configurations: bump the pin, run `npm install`, build both configurations in a clean environment, run the site's validators, run the production Worker locally, push preview and watch the build, fast-forward main, and probe the live site. Consult `05_automations/website-maintenance/runbook_appendix/cloudflare_maintenance_ops.md` for deployment operations. An image-affecting dependency fix, such as sharp, gets its own commit and must be verified by a COLD build with the image cache moved aside. Compare the output byte-for-byte with the expected baseline, and also run a fresh `npm ci` from the committed lockfile. Use `overrides` when a necessary dependency update is blocked by an exact transitive pin, and verify compatibility. Astro middleware that reads request headers needs an `isPrerendered` guard so prerendered routes do not attempt to read request-specific data.

---

## 🔴 THREE-ITERATION GRADUATION: THE ITER-1 REFLECTION MUST BE EXHAUSTIVE (PROTECTED)

> **Target every ACE loop at THREE iterations: generate → ONE EXHAUSTIVE reflection → one fix round → one verification.**
>
> Why three: every extra round costs time and tokens, and most extra rounds come from findings that were visible in the first review but reported later. An exhaustive first reflection is what makes three rounds possible.

### The failure this exists to prevent
Consider a kitchen-equipment maker's video guide that needs repeated reviews to meet the quality threshold. Each finding may be correct, but the cost comes from sequencing: each reflection names only the most salient defects, and a later review surfaces something that was present all along, such as a broken character, an unclear sentence or an inconsistent heading style. Those extra cycles could have been avoided by reporting all visible defects in the first review.

### Why a reflection defaults to the wrong shape
Reporting the top N findings is right when the scarce resource is a reader's attention. In an ACE loop the scarce resource is *iterations*: every unreported finding that blocks completion requires another cycle. Tell the reflector which resource it protects.

### MANDATORY reflector spawn clauses (paste into every design-reflector prompt)
1. **EXHAUSTIVE, NOT PRIORITISED.** Enumerate everything between the artifact and the threshold, on every dimension, including one-character items.
2. **EXACT FIX PER ITEM.** Give the literal replacement, selector, line, and whether it is an **ADD** or a **REPLACE**. Quote both sides for a replacement.
3. **SEPARATE BLOCKERS FROM ACCEPTED RESIDUALS**, each residual with its reason.
4. **SANITY-CHECK EACH PRESCRIPTION AGAINST ITS SURROUNDING TEXT.**
5. **DECLARE OUT-OF-SCOPE DEPENDENCIES IN ROUND ONE**, with evidence. Examples include a required permission, a shared file outside the change scope, or a decision only the site operator can make.

### The stop signal
A decelerating score curve with shrinking findings means the loop may have moved from finding defects to polishing. Demand the complete remaining list in one message, or ship with declared residuals once required checks pass.

### The second-order reason
Attention quality can degrade across repeated iterations. The orchestrator starts processing a queue instead of reasoning about the artifact, which is when a checklist item gets closed by breaking the rule it protected. Short loops help preserve correctness. When a checklist item prescribes an edit to copy that defines the product's value or audience, recover the reason before applying the action: "What would make this edit wrong?"

## 🔴 GEOMETRIC vs PROPERTY COLLISION: SCOPING DOCTRINE HAS TWO HALVES (PROTECTED)

CSS scoping can protect the surrounding hub from a page's styles without protecting the page from the hub's styles. This describes **CSS property collisions**: two rules fighting over a declaration. Detectors built around that mechanism look for unexpected overrides. That is half the failure surface.

**The other half has no override residue.** Standalone HTML is authored against its own viewport. Inside a site it inherits a different geometry, most often a **fixed header** the original never had. Offsets that were right in the source are now measured from the wrong origin. Nothing is overridden; the page is still broken. For example, a bicycle-parts guide with `scroll-margin-top: 24px` inside a site with a `72px` fixed header would place its jump targets beneath the header. A sticky contents rail with `top: 20px` could hide its own label.

**Why the checks returned green**: property-override detectors find nothing because no value was lost; a single centre-point reachability probe is scroll-state dependent; axe does not model scroll geometry.

**The mandatory check**: whenever ported CSS is preserved, enumerate every length that encodes a distance from a viewport edge (`scroll-margin-top`, `scroll-padding-top`, sticky/fixed `top`, any `top`/`margin-top` on a sticky rail or anchor target) and re-measure each against the site's actual header height. Verify by measuring the delivered offset of every in-page jump target:
```js
// In the real page, at each breakpoint, click each TOC link in turn.
// After its scroll settles, measure that link's target.
const header = document.querySelector('header');
const hdr = header.getBoundingClientRect().bottom;
const top = target.getBoundingClientRect().top;
if (top < hdr) {
  console.error(`${target.id} lands ${(hdr - top).toFixed(0)}px UNDER the header`);
}
```
`scroll-margin-top` must be ≥ header height + breathing room. For example, a `96px` margin provides `24px` of breathing room below a `72px` header fixed at the top of the viewport.

**Second-order lesson**: the doctrine named a mechanism where the principle was a context change. **State the PRINCIPLE and let the mechanism stand as an example**: the next check is built from whichever got written down.

## 🔴 INSTRUMENT DISCIPLINE: THE CHECK IS THE ARTIFACT MOST LIKELY TO BE WRONG (PROTECTED)

On a busy maintenance pass, a deep fault can be in a check rather than the page, and a faulty check can report a confident green. These are the fault families to suspect first, each with the question that exposes it:

- **The empty-input trap.** A text-stripping check that calls `str.replace(found, ' ')` on a match that can be empty, such as the contents of an empty `<style>` element, may rewrite the whole document. Ask: what does this check do when its match is empty?
- **The dead-branch selector.** A selector copied from component CSS may belong to the branch of a conditional that never renders, so a test on it passes over nothing. Ask: does this selector match at least one element in the built page?
- **The ancestor false positive.** A reachability probe written as `hit.contains(e)` counts a hit on any ancestor as a hit on the element. Ask: would the probe pass if the element were covered?
- **The comment that ships.** Comments in Astro frontmatter or processed code may disappear during the build, while a note inside `<script is:inline>` can be published on every route. Ask: which comments survive into the built HTML?
- **The tokenising query.** A CMS query operator that matches whole tokens rather than substrings over- or under-counts the pages a change affects. Ask: does a hand count of a small sample of known pages agree with the query?
- **The stub that hides a class.** A preview harness with hand-written headers cannot show a defect that only the real headers produce. Ask: what can this harness never show?

**The rule**: a positive control proves a check can fail on the input you chose; it says nothing about coverage. Required for any check:
1. **Probe every member of the population**; report the fraction as `probed / found / missed`, using actual counts.
2. **Re-derive the control when the check changes**; restore the old bug and confirm the NEW control catches it.
3. **Add a structural invariant** that makes the silent failure impossible, such as `assert len(owned) <= len(text)`.

**Deriving a population**: enumerate what is shipped; never guess with an allowlist. An extension allowlist can miss shipped text files and leave exposed internal content undetected. Use a null-byte test on built output as a first-pass text/binary distinction, account for formats it cannot classify reliably, and count leaks after any Markdown counterparts are generated.

**Enumerate-then-judge beats pattern-guess**: to find internal references in shipped content, extract every comment and judge each.

**Inline CSS comments are wire content**: anything injected into `<head>` ships its comments. When making comment-only edits, require the comment-stripped CSS to remain byte-identical.
## 🔴 THE REFLECTION MUST COME FIRST: DO NOT SUBSTITUTE ORCHESTRATOR REVIEW (PROTECTED)

When an orchestrator supplies corrections before requesting independent reflection, serious defects can survive repeated review. **Orchestrator review is not reflection**: the orchestrator wrote the spec and shares its blind spots. Delaying independent review creates avoidable rework. **Spawn the reflector after the first generator pass, always, especially when confident.** The independent reviewer evaluates and reports findings without fixing the work. Mechanical checks are a precondition for review, not the verdict.

---

## General lessons for sites on Cloudflare Workers (PRIMARY: maintenance rules)

These maintenance rules apply to business sites built with Cloudflare Workers, GitHub and Astro, including sites with WebGL layers. Keep evidence for each rule alongside the checks that enforce it.

### Instruments (extends measurement discipline)
- **A control is a claim.** When a check is widened, re-run the old controls first; prove a new rule by running the pre-edit check on the same deliberately faulty input and comparing finding TEXT, not counts.
- **A mutant counts only when the plant is shown applied** and red on its own check's FAIL line. Network requests do not include URL fragments, so `page.route` cannot match a `#fragment`. An init script may run before `documentElement` exists: route the path, register the MutationObserver when its target exists, and make every plant print evidence.
- **A PASS prints its count.** A lint that measured zero fields is vacuous and reported as such.
- **Exit status and evidence hygiene.** Never pipe a check before reading its return code (`cmd > log 2>&1; echo rc=$?`); enable a check only after an explicit success marker; check a heredoc-written file is non-empty before filing it; compute every reported number by script from the final file.
- **Never `pgrep -f`** to wait on or check a process: it can match its own command line. Use the pid you started, or a bracket-grep.
- **Rulers only narrow.** Fix a false positive without shrinking the territory; prove the false positive silent AND the true positive still firing; plant controls in the real source's format.
- **Headless capture traps.** Full-page captures can skip lazy imagery and leave sticky tracks blank; with JavaScript disabled, insert required capture styles through browser evaluation if `addStyleTag` stalls; a probe that picks targets "in view" tests the viewport, not the frame; when a figure grows, re-check every capture clip that used its box.
- **Machine limits.** Limit concurrent heavy processes to available memory; run long check suites with their own progress file; after a transient agent crash verify state read-only before continuing the interrupted task. If Lighthouse inherits a temporary-directory setting that is not writable in its environment, point `TMPDIR`, `TEMP` and `TMP` at a writable directory. Stop `wrangler dev` using the parent pid you recorded at startup.
- **Price the suite, not each rule.** Run a fast core set on the final build and heavy sweeps once per iteration during independent review. After a late fix, repeat the checks its diff can affect and write the reasoning beside each reused log. Set a verification time budget in advance; report incomplete checks when that budget is reached.
- **Account separation.** Use an allowlisted environment for account-specific calls and pin `account_id` in the repository. Confirm the authenticated account with a non-mutating call; a dry run may not authenticate. Test that an identity without access is rejected. Scan for secrets by full value and fragments without printing either.

### Production parity on Workers
- Run motion and frame-0 checks under the production CSP: Vite can inline small assets as `data:` URLs, and `fetch(data:)` can fail under `connect-src 'self'`. Decode in place rather than loosening CSP; assert a "layer is live" attribute so a silent fallback cannot pass.
- If a local Worker fails only on success paths, inspect the host seen by request validation and Turnstile. Set `--local-upstream localhost` where needed and test with an explicit local configuration that preserves fail-closed behavior.
- Verify the current D1 Time Travel retention for the account's plan and keep independent exports on a schedule suited to the site's recovery needs. The Workers rate-limit binding is eventually consistent: use it to reduce traffic, never as a strict authorization boundary or an exact-count test assertion.

### Forms, privacy and consent (maintenance-time)
- Form order: method/host/origin/Access, config, rate limit, size cap, honeypot + page-measured fill time, validation from one shared schema, Turnstile fail-closed, parameterised D1 insert FIRST, email via `waitUntil` with an idempotency key and the email status recorded. A new field is a nullable additive migration applied `--local` then `--remote` before any deploy, tested with a probe that sends no mail.
- Repeat sign-ups answer exactly like first ones; malformed bodies are never logged. Log a bounded error identifier such as `e.name`, and lint the Worker and its imports for unintended logging. Production guards reject documented vendor test values after trimming input.
- Any change touching data practices re-checks the privacy page as a TRUE / FALSE / UNVERIFIABLE truth table against the code, including copies outside the forms code: inboxes, exports, restore history and invocation logs.
- Changing consent wording appends a NEW consent-version id while retaining historical records. Keep older versions accepted where the consent model permits, and sweep every rendering of that purpose. Run content verification after build and before any commit touching strings or facts; a successful build does not establish factual accuracy.
- Start with only the cookies and browser storage the site needs. Cookieless analytics still requires a review of what it collects. Allowlist exact storage keys and their writing code for visitor-selected UI preferences. When adding optional tracking, configure the consent interface first, set Consent Mode v2 to default-denied before any tag where applicable, hold tags by category using `type="text/plain"` and a working consent loader, update the CSP allowlist, re-check the privacy page, and verify nothing optional fires before consent.
- Apply email-provider DNS records from verified provider instructions or API responses using narrowly scoped access. Inspect existing records before changes. Choose and tighten DMARC policy based on verified sender alignment and delivery evidence.

### Text over imagery, layout and media
- axe cannot reliably grade text over raster imagery and may mark it incomplete. Measure the background on a render with text hidden, checking p99 AND the brightest pixel under each line for white text. Derive the allowed luminance from the required contrast ratio; for dark text over light art, the lightest text colour and darkest background under it constrain contrast.
- Grade every scrim with on/off captures: it must not lighten the area beneath white words or alter unrelated areas. Bound it to the text elements, measure it per painting, and when an asset-level fix lands, re-audit every compensating layer added for the old asset.
- Art-directed compositions switch at the breakpoint of the CONTENT they hold. Prove crop coverage across widths AND content states. For a wider image cropped horizontally by `cover`, visible share = (boxW/boxH)/(imgW/imgH); use the corresponding height ratio for vertical cropping. Overlays on cover-fit art are sized in the art's displayed units, using cover scale = max(W/w, H/h), or the box height is held. A layer derived from one crop draws only while that crop displays.
- An edit to an image composites only the edited spots onto the untouched master and saves at source quality. A large byte drop after a small edit warrants inspection for unintended recompression. Commit image edits alone.
- CSS injected as a string can escape lint coverage: assert computed values with scripts off plus a remove-the-block mutant. A fragment-targeted `<details>` is opened as early as possible and tested on fragment LOAD with a layout-shift observer. In Astro, script-created elements need appropriately scoped `:global()` rules.
- Above-the-fold media, including images, video, canvas and 3D, shares one loading budget. Identify the actual LCP candidate, prioritise its delivery, and defer competing decorative work.

### WebGL and motion layers
- Any canvas/WebGL change starts from `03_skills/webgl-craft/SKILL.md`: its renderer decision tree, with HTML/SVG for meaning first, budget (DPR ≤ 1.5, ≤ 30 KB gz per layer), hardening and common-mistakes review. Ambient layers boot after load + idle + in view, never during load.
- A scroll-started layer's boot never runs a main-thread task over 50 ms at 4× CPU: slice it, and band whole-texture uploads into macrotasks. Scene data shared by a renderer is fetched beside its textures, not imported into code.
- Automatically moving content lasting over 5 s alongside other content ships a visible pause control where WCAG 2.2.2 applies. The pause rule must out-rank every rule that sets the animation shorthand on the same element. Anything a live layer adds over a static design starts at zero so frame 0 equals the still.
- Check the renderer used by headless Chromium. If it uses SwiftShader, fps measures software-rendering cost rather than real-device GPU performance. Force the relevant device tier to test its behavior, and report real-GPU fps as "not run" unless measured on that hardware.

### Copy truth during maintenance
- **Product-release refresh pass.** When a kitchen-equipment maker adds a product option, facts that were limits may become features. Re-read every bullet against its heading, sweep every only/never/fallback and closed two-way list when an option list grows, read shared includes in each host page's vocabulary, and verify privacy facts against the request-building code. Full verification and the designated editor's sign-off still apply.
- Every orchestrator artifact is copy: findings name the harm, the constraint and the relevant source fact, never an unreviewed replacement sentence, and carry no unsupported quantifiers of their own.
- Approved words change only through named entries in a change register that refuses unknown keys and keeps the superseded original. Dry-run every merge and read every changed key.
- A bicycle-parts guide library has its own visual requirements. Read the site's documented styles and overrides first and record each workbench default not applied, with its reason, so a reviewer does not erase intentional choices.
- Validate structured data and metadata lengths against the page's actual purpose.

### Loop and skillbook governance
- Ship a credible first-pass preview promptly and let a human's real-device inspection steer the next round. A garden-supply how-to hub can pass automated checks while still presenting awkward reading or navigation on a phone. Near the acceptance threshold, use binary checks run by two independent reviewers who have not seen each other's findings, rather than relying on the scalar score (skill `ace-011`).
- Run the Curator after EVERY iteration, following the sequence defined below. This catches measurement traps before they distort later decisions.
- Retire score-prediction and score-calibration rules: they turn the reviewer's number into a target. A skill whose falsifier fires is retired as written; a narrowed form re-enters PROVISIONAL with a pre-registered falsifier.
- Capture discipline: at capture time ask "would this affect a routine maintenance run?" When a recurring failure is identified mid-thread, record an index entry linking the earlier occurrences so the lesson covers the whole pattern.

## Open items (yours to keep)

Keep a short numbered list here of anything a run left open, such as an owed upgrade, a known residual or a check that did not run. Treat each entry as status to verify next time rather than a fact to assume. Two residuals worth checking on a Workers site:

1. Requests under `/.well-known/*` can bypass Worker-applied headers when routing sends them directly to assets. Check production 404 responses for the intended `X-Robots-Tag`; adjust Worker routing or asset response handling if it is missing.
2. A watcher keyed only to a commit can observe the wrong build attempt. Track the intended deployment by its build UUID and verify the expected marker at its preview URL.

## ACE Loop Refinements

### (a) CURATOR-EVERY-ITERATION
Run the Curator after EVERY iteration (Generator, then Reflector, then Curator), and once more at close. Prefer this to a single curator at the end because early passes can catch measurement traps before the next iteration depends on them: a full-page capture falsely passing a sticky layer, a coverage floor determined by viewport shape, or an interaction between findings that neither reviewer saw alone. Keep each pass small, using ADD/UPDATE/TAG deltas from that iteration's reflection, and record reusable lessons continuously.
### (b) PAIRED REFLECTORS
Each iteration, run as many parallel Reflectors as Generators, one per generator slice, each auditing ALL files for its fix pattern. Then run ONE final cross-page certification Reflector to check navigation, footers, design tokens, CSP, sitemap, and AEO across the combined output.

### (c) DIST ISOLATION
When N Reflectors test the built site with Playwright, the orchestrator builds the output ONCE. Each Reflector serves that same output read-only on a distinct port and never rebuilds. This prevents rebuild races on a shared port from producing false alarms.

---

## Self-Heal Log

- Use search phrases instead of private memory IDs. Keep startup queries in `05_automations/website-maintenance/startup_queries.json` and edition notes in `05_automations/website-maintenance/EDITION_NOTES.md`.
- For your own runs, add one line per self-heal: date and what changed in this folder.
