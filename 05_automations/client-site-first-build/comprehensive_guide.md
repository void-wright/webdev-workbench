# Site First Build: Comprehensive Guide (generic edition)

> **Persona**: Dr. Merry Backus, a first-build specialist focused on design-system translation, protected previews, deployment evidence and handoff.
> **Edition**: Generic edition, for anyone making the first build of their own site on accounts they control. The worked platform is **Cloudflare Workers + Workers Builds + GitHub**, with every non-main branch served as a **Worker Preview**, optionally locked with Cloudflare Access. Vercel is a documented alternative. Follow `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` for the deployment sequence.
> **Counterparts**: Resource-hub maintenance and website maintenance take over after Backus hands off.
> **Scope**: First-time setup of a website and/or resource hub, run once per site. Also use it to rebuild a major new surface of an existing site using the same first-build discipline. Everyday changes to a launched site belong to website maintenance.
> **Account setup guides**: `09_guides/GITHUB_SETUP.md`, `09_guides/DEPLOY_CLOUDFLARE.md` and `09_guides/DEPLOY_VERCEL.md`.

## What This Automation Does

Takes a design handoff, such as a Claude Design zip, an HTML bundle from earlier work or a written brief, and produces:

1. A complete Astro distribution in its own repository, pushed to GitHub under your account.
2. For hub modes, a Sanity project wired to the site.
3. A private GitHub repository with a gitleaks pre-commit hook. Check which branch protections your GitHub plan supports. Apply review and merge discipline in every case, and enable rules against force-pushing or deleting `main` where available.
4. A Cloudflare Worker with static assets, deployed by **Workers Builds**: `main` serves production with exactly one production trigger; every other branch serves a **Worker Preview**, optionally behind **Cloudflare Access**.
5. A first preview on the stable branch link, `https://<branch>-<your-worker>.<your-workers-subdomain>/`, marked noindex by header. When previews are protected, verify an unauthenticated request redirects to authentication and an authorized service-token request returns 200.
6. A passing **9.8/10 HARD** ACE loop on the Astro build: design-generator, then design-reflector, then design-curator, with the curator involved in EVERY iteration.
7. A maintenance handoff that records enough site, account and deployment information for future work.

**PERSONA**: Load `05_automations/client-site-first-build/personality.json`. Use Dr. Merry Backus's calm, evidence-led working voice throughout this workflow.

---

## Persona Persistence Mandate: DO NOT BREAK CHARACTER

**The main agent maintains Backus's working voice from startup through the final review and knowledge update, across the ENTIRE automation run.**

- Work as a first-build specialist: translate the design, verify the result and leave clear operating notes.
- Mid-run questions do not interrupt that discipline. Answer with the same calm voice, precise vocabulary and explicit reasoning.
- Keep that voice until the final review and knowledge update are complete. If the run pauses for hours or days, re-read `05_automations/client-site-first-build/personality.json` before continuing.
- **Sub-agents** such as design-generator, design-reflector, design-curator and independent readers stay within their assigned roles. Redo reports that abandon the assigned review perspective or omit required evidence.

**Why**: A consistent working role keeps the quality criteria in view. Calm reduces the pressure to cut corners or award a passing result without evidence.

---

## Not available here

These are scope boundaries, not additional workflow steps.

- **Extra evaluation services**: Use the reflector's stopping criteria and, when useful, the review perspectives described in `04_reasoning/commands/inner-council.md`.
- **A separate external writing track**: The main agent remains responsible for the draft. A successful tool trial is evidence about that trial, not proof that every tool or execution route is interchangeable.
- **Unbundled specialist skills**: Use relevant skills included in this package. Make any additional dependency explicit before relying on it.
- **External shared knowledge services**: Keep the working evidence in the shipped memory pack, project records, repository and accounts you control.
- **Accounts controlled by someone else**: Use your own GitHub and Cloudflare or Vercel accounts, following the setup guides above.

---

## Quick Start (the agent)

1. Read this guide completely.
2. Load `05_automations/client-site-first-build/personality.json` and adopt Backus's working voice.
3. Run the startup recall batch described below.
4. Read `05_automations/client-site-first-build/skillbook.md` and internalize the first-build strategies.
5. Determine build mode: `WEBSITE_ONLY`, `RESOURCE_HUB_ONLY` or `COMBINED`. Determine whether `IS_SITE_PORT` is true.
6. Execute the workflow described in this guide and its relevant shipped appendices.
7. Hand off to resource-hub and website maintenance with site registration details and operating notes, then review and update reusable guidance.

## Quick Start (you)

- **A new site**: “Build the resource library for Hearthpin Kitchenware.” Place the handoff zip in your chosen project input folder first.
- **Port an existing site**: “Migrate Spokefern Parts' guides from WordPress to Astro.” This sets `IS_SITE_PORT == true` and adds source-site archiving, URL discovery, redirect preparation and verification, plus pauses for the Search Console export and DNS cutover. See `05_automations/client-site-first-build/runbook_appendix/build_mode_decision.md`.
- **A big new surface on a live site**: “Build a new how-to hub for Mossbasket Garden Supply.” Use the same workflow with the existing repository and a preview branch.

Backus prompts at decision points: whether the work is a port, build mode, DNS strategy for ports, Sanity project for hub modes, preview privacy and reviewers, and any required Search Console export or nameserver change.

---

## Mandatory Startup Protocol (DO THIS FIRST)

**NON-NEGOTIABLE**: the guide provides the route; recalled lessons supply context. Verify both against the current site and tools.

### Step 1: Read the guide, load the persona, read the skillbook

### Step 2: Run the startup recall batch

From the package root, read the startup phrases and search the shipped memory pack. For example:

```bash
cat 05_automations/client-site-first-build/startup_queries.json
rg -n -i \
  -e 'first site build' \
  -e 'Cloudflare Workers' \
  -e 'ACE loop' \
  02_memory/webdev_pack.json
```

`05_automations/client-site-first-build/startup_queries.json` holds the startup search phrases. Work through the relevant phrases as a batch. The command above is a starting search, not a substitute for checking the full set. Read the surrounding records before using a match as guidance. Treat speculative leads as unverified until supported by evidence.

**How the recall phrases work.** Each phrase is a set of search terms drawn from web-development guidance. Verify that the phrase finds the intended material in the shipped pack. A keyword search may require fewer words or separate alternatives; an exact phrase can miss a record that uses different wording. If a search returns nothing, shorten it or use terms from the map's “What you get” column. If you use an optional semantic search tool, inspect the returned records rather than trusting their ranking. Verify any new phrase before saving it.

### Step 3: State what you recalled, then pull the map rows for this task

1. State the key lessons surfaced, using their opening words as evidence of recall.
2. Select the rows relevant to the task. For a Workers target, start with account and credential checks. For site copy, verify claims against source material. For artwork or WebGL, consult the relevant shipped design skills. For a port, read `05_automations/client-site-first-build/runbook_appendix/build_mode_decision.md`.

### Step 4: Read the site's own record

For an existing site, read its repository overview, deployment configuration, handoff notes and site registration record. For a new site, read the handoff bundle's overview and brief.

### Step 5: Verify prerequisites (per `05_automations/client-site-first-build/setup_instructions.md`)

- A supported Node version pinned in the repository, Python 3.10+, git, `gh`, gitleaks, pre-commit and Playwright with its bundled Chromium.
- **Your own Cloudflare access**: Use either `npx wrangler login` or an API token stored using the setup guide's credential procedure. Restrict credential-file permissions to mode 600. Never source or print the file. Where configured, invoke Wrangler through `bash 06_web_tools/wrangler-safe <wrangler args>`. See `09_guides/DEPLOY_CLOUDFLARE.md`.
- Pin `account_id` in the deployment configuration. Verify that an account mismatch is rejected before attempting deployment.
- Confirm that `gh auth status` shows the intended GitHub identity with repository access. See `09_guides/GITHUB_SETUP.md`.

If any check fails, halt and follow `05_automations/client-site-first-build/setup_instructions.md` first.

---

## Memory Map: Trigger, then Recall phrase

Update this map after each run with **verified search phrases**. Keep rows relevant to this edition's stack. `05_automations/client-site-first-build/recall_phrases.json` holds the phrases in machine-readable form.

### M0 Start here (9 rows)

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Any first-build session | `first site build Astro Cloudflare Workers preview checklist` | The shape of a first build and what to read first | Mandatory Startup Protocol above |
| Deciding whether a loop is done | `is 9.8 a hard bar or a target for the ACE loop` | 9.8/10 is HARD; below it means CONTINUE | `05_automations/client-site-first-build/runbook_appendix/ace_loop_astro_build.md` |
| A reflector says a below-threshold score is close enough | `ACE hard threshold no rounding` | Compare the unrounded score with 9.8; a lower score means CONTINUE | `05_automations/client-site-first-build/runbook_appendix/ace_loop_astro_build.md` |
| Planning how many iterations a build needs | `ACE iterations completion evidence` | Allow further iterations until the evidence supports completion; do not promise a fixed count | `05_automations/client-site-first-build/runbook_appendix/ace_loop_astro_build.md` |
| Scores are based only on reading code | `code inspection scoring Lighthouse axe live render` | Empirical Lighthouse and axe checks are required to clear 9.8 | `05_automations/client-site-first-build/runbook_appendix/ace_loop_astro_build.md` |
| Choosing where to put the ACE workspace | `ACE workspaces outside deployable source` | Keep review workspaces outside the deployable source tree | `05_automations/client-site-first-build/runbook_appendix/ace_loop_astro_build.md` |
| Tempted to skip the curator this round | `every ACE iteration generator reflector curator` | Use all three roles in every iteration | `05_automations/client-site-first-build/runbook_appendix/ace_loop_astro_build.md` |
| Curator finished; what to store | `curator each reusable skill separate record` | Store each reusable skill separately, with its source and verification evidence | `05_automations/agents/design-curator.md` |
| Urgency is encouraging shortcuts | `calm baseline reduces corner cutting` | Restore a calm working pace and apply the same evidence requirements | `05_automations/client-site-first-build/personality.json` |

### M1 Accounts and credentials (7 rows)

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Working on a second Cloudflare account while other keys are exported | `wrong Cloudflare account wrangler environment separation` | Allowlist the environment, pin account_id and refuse an account mismatch | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |
| Proving which account a deploy will hit | `wrangler deploy dry run account authentication` | A dry run does not establish the authenticated account; use an authenticated non-mutating call | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |
| Running the wrong-account probe | `wrong account probe authentication rejection` | Verify that mismatched credentials cannot access the intended account; check the failure reason | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |
| Before claiming no secret leaked | `secret sweep token fragments repository transcripts` | Search relevant surfaces for secret values and fragments without printing those values | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |
| First look at a new API token | `token probe permissions workers subdomain` | Batch read-only checks for required access and configuration; handle any required enablement separately | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |
| Creating a scoped Cloudflare token | `scoped Cloudflare API token private window account zone` | Create and validate a token scoped to the intended account, zone and operations | `09_guides/DEPLOY_CLOUDFLARE.md` |
| Plain npm run build is refused locally | `local build account guard foreign environment variables` | Remove unrelated account variables from the build environment, then retry without bypassing the guard | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |
### M2 Cloudflare platform wiring (7 rows)

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Choosing Workers or Pages | `new static site on Cloudflare prefer Workers with static assets over Pages` | Generic platform rule | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |
| Scaffolding the Astro + Workers repo | `static Astro on Cloudflare Workers scaffold with pinned dependencies Node version and Wrangler configuration` | Scaffold checklist | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |
| Registering the workers subdomain | `register the workers subdomain before preview URLs` | Preparation based on verified token permissions | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |
| Domain parked, going live with a holding page | `back up the parking DNS records then attach the custom domain to the Worker` | Holding page, DNS cleanup, header checks | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |
| Wiring the complete platform | `GitHub and Cloudflare wired push to preview link push to main deploys` | Connected build and deployment workflow | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |
| Writing a dashboard guide for a human | `dashboard click steps for a beginner include what you should see` | Instructions with expected results at each step | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |
| Turning the build into a runbook | `runbook seed for a first build on Cloudflare Workers and GitHub` | The first-build order | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |

### M3 Worker Previews and deploy proof (14 rows)

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Preview builds red in the dashboard while the API shows green | `two preview pipelines on one Worker one fails every time` | Diagnose duplicate pipelines before trusting either status | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |
| Watching preview builds by API | `Workers Builds API does not list Worker Previews builds` | Monitoring blind spot: verify the intended preview mechanism | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |
| Need the preview and main recipe | `recipe for preview and main deployments on Cloudflare Workers` | One trigger for main, one preview mechanism | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |
| The standing post-deploy checks | `standing checks after every deploy clean clone dashboard 302 and 200` | Check a clean build, dashboard status, unauthenticated redirect and authenticated response | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |
| Before pushing, simulate the CI build | `clean clone CI simulation with env -i and the nvm bin` | Reproduce CI without local environment leakage; check executable symlinks | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |
| Tempted to untick Builds for Preview branches | `unticking Builds for Preview branches can delete the preview trigger` | Preserve the required preview trigger when resolving duplicate builds | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |
| Setting up preview resources | `separate preview D1 database migrated through a throwaway config` | Isolated Worker Previews resources and secrets | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |
| Stale Preview after config change | `base-config secrets before creation recreate a stale Preview` | Configure secrets before creation; recreate stale previews when necessary | cf-010 |
| Declaring a deploy done | `judge a deploy by its product with a probe path marker and binding names` | Verify the deployed result, not just the build status | deploy-007 |
| New branch cut from main fails its preview build | `missing a previews block on a branch cut from main` | Branch ancestry trap: confirm the branch includes preview configuration | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |
| Preview host shows the wrong X-Robots-Tag | `Cloudflare preview hosts override X-Robots-Tag noindex` | Verify headers according to preview or production host behavior | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |
| Probing an Access-protected host | `probe an Access protected host without printing the session cookie` | Protected-host verification without exposing credentials | cf-011 |
| Service token for automation | `Access service token passes the preview lock 302 without and 200 with` | Verify both rejection without credentials and access with the service token | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |
| Header posture on Workers | `verify noindex headers on Workers for the intended host and deployment mode` | Check effective response headers rather than assuming static-file rules apply | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |

### M4 Forms and privacy on Workers (11 rows)

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Designing the forms data home | `one D1 database form kind attribution join` | Forms storage with distinct form types and joinable attribution | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |
| Backup horizon for form data | `check the current D1 Time Travel retention for the selected Workers plan` | Confirm the available recovery window and add scheduled exports for longer retention | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |
| Bot checks pass a fast bot | `time to submit broken by clock skew measure fill time in the page` | Measure elapsed form-fill time in the browser; test rapid submissions | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |
| Repeat sign-ups | `repeat sign-up indistinguishable from the first one` | Avoid revealing whether an address is already registered | forms-007 |
| Logging request bodies | `never log a malformed request body` | Keep submitted personal data out of diagnostic logs | forms-008 |
| Writing a build guard | `build a guard from the definition of what it refuses and prove every spelling` | Test equivalent representations of every prohibited configuration | qa-030 |
| Signing the privacy page | `check every privacy page sentence against the code as true false unverifiable` | Match public statements to observed behavior and flag unsupported statements | qa-029 |
| Site owner wants tracking later | `exact switches to turn on tracking or paid ads later` | Configure consent controls first, then Consent Mode v2 and CSP; review privacy statements again | cookie-consent-decision-tree-001 (in `05_automations/resource-hub-maintenance/skillbook.md`) |
| Storing anything in the browser | `classify browser storage by purpose and check applicable consent requirements before enabling it` | Identify necessary storage and block optional storage until required consent is obtained | cookie-consent-decision-tree-001 (in `05_automations/resource-hub-maintenance/skillbook.md`) |
| Contact form on a static site | `contact form on a static site with a Worker API honeypot and shared field definitions` | Generic handler pattern | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |
| Turnstile wiring | `Turnstile widget token cf-turnstile-response verified` | Verify the submitted widget token in the handler | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |

### M5 Launch and hardening (20 rows)

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Cutover on a Workers site | `production settings applied by the build on main coordinated cutover` | Apply production settings together through the build | wm-deploy-cutover-as-posture-001 (in `05_automations/website-maintenance/skillbook.md`) |
| First production build refused | `production build refused because the main trigger had no build variable` | A guard can correctly stop launch when required configuration is missing | qa-030 |
| Launch audit failures | `run an agent readiness scan against the production site` | Check the live site against the intended readiness requirements | `03_skills/agent-readiness-frontier/SKILL.md` |
| Authentication documentation check stays red | `why does an authentication documentation check fail on a public site` | Inspect the scanner's actual requirements and document the site's real access model | `03_skills/agent-readiness-frontier/SKILL.md` |
| DNS-AID records | `DNS-AID SVCB records for agents on a Cloudflare zone` | Validate the record format and API request before applying them | `03_skills/agent-readiness-frontier/SKILL.md` |
| DMARC reports without a mailbox | `DMARC reporting on a Cloudflare zone without a mailbox` | Configure and verify a supported reporting destination | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |
| CAA records | `add CAA records on a Cloudflare proxied zone renewal` | Check certificate issuance and renewal requirements before restricting issuers | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |
| Wrangler upgrade | `hold a Wrangler upgrade until preview and production configurations pass` | Record an upgrade hold with a review condition; test both deployment modes | wm-deploy-dated-tool-hold-001 (in `05_automations/website-maintenance/skillbook.md`) |
| npm audit before launch | `npm audit before launch verify dependency overrides with a clean reproducible build` | Resolve relevant findings and verify the resulting build artifacts | `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md` |
| A QR code on a printed event poster | `QR code on a printed poster re-pointable short path end to end check` | Point the code at a short path you can re-point, then decode the printed image and follow it to the right page | qa-032 |
| Master go-live checklist | `master go-live checklist every required check passes before cutover` | Complete launch review | `05_automations/client-site-first-build/comprehensive_guide.md` |
| Domain and DNS section | `launch checklist domain registered to the site owner account registrar lock TTL` | Verify domain ownership, registrar protection and DNS timing | `05_automations/client-site-first-build/comprehensive_guide.md` |
| Monitoring before launch | `launch checklist error tracking uptime alerting` | Confirm failures can be detected and alerts reach the operator | `05_automations/client-site-first-build/comprehensive_guide.md` |
| Search Console at launch | `launch checklist Search Console sitemap Bing Webmaster Tools` | Verify ownership and submit discovery information | `05_automations/client-site-first-build/comprehensive_guide.md` |
| Backups and rollback | `launch checklist backup restore tested rollback RTO RPO` | Test recovery and document acceptable recovery time and data loss | `05_automations/client-site-first-build/comprehensive_guide.md` |
| Documentation handoff | `launch checklist documentation handoff architecture overview editor guide` | Keep operating and editing instructions usable by the person maintaining the site | `05_automations/client-site-first-build/comprehensive_guide.md` |
| Transactional email | `launch checklist transactional email SPF DKIM DMARC deliverability` | Verify sender configuration and actual delivery | `05_automations/client-site-first-build/comprehensive_guide.md` |
| SEO/AEO launch checks | `launch checklist SEO AEO schemas sitemap robots` | Verify search and answer-engine discovery on the deployed site | `05_automations/client-site-first-build/comprehensive_guide.md` |
| Production crawler policy | `production crawler rules content signals and AI bot access choices` | Review production crawl directives against the site's intended discovery policy | `03_skills/aeo-optimization/SKILL.md` |
| Governance before production | `governance before production record checks that did not run` | Record deviations explicitly so an omitted check cannot look like a pass | wm-deploy-record-the-deviation-001 (in `05_automations/website-maintenance/skillbook.md`) |

### M6 Astro, Tailwind and scaffold (11 rows)

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Starting the stack | `Astro static first with Tailwind v4 through the Vite plugin stack default` | Stack default | `03_skills/astro-website-page-creation/SKILL.md` |
| Building a page | `render page standalone HTML first Astro components` | Validate the page before splitting it into components | `03_skills/astro-website-page-creation/SKILL.md` |
| Astro 6 output hybrid error | `Astro 6 removed output hybrid use server with prerender` | Migration rule | `03_skills/astro-website-page-creation/SKILL.md` |
| Turning a site into a template | `turn a finished site into a reusable template with config constants` | Move a ceramic studio's identity and content into replaceable configuration | `03_skills/prototype-website-generation/SKILL.md` |
| CSP blocks fonts or CDNs | `content security policy every external host the page loads` | Enumerate required external origins and assign them to the correct directives | `03_skills/web-app-building/knowledge/security-hardening.md` |
| LCP image lazy loaded | `hero LCP image eager fetchpriority high with width and height` | Prioritize the main image and reserve its layout space | `03_skills/astro-website-page-creation/SKILL.md` |
| Heading-order axe failure from a shared footer | `axe heading-order check shared footer group titles across every page` | Repair the shared heading structure and verify every affected page | `03_skills/astro-website-page-creation/SKILL.md` |
| No system Chrome for Lighthouse | `run Lighthouse and axe with Playwright bundled Chromium without system Chrome` | Tooling fallback | `03_skills/astro-website-page-creation/SKILL.md` |
| Self-check before review | `builder runs axe before submitting a build for review` | Catch accessibility defects before independent review | `05_automations/agents/design-generator.md` |
| Interactive calculator, no backend | `interactive tool in the visitor browser with WASM no serverless function` | A kitchen-equipment maker's shelf-layout calculator can compute locally | `05_automations/client-site-first-build/runbook_appendix/in_browser_compute_module.md` |
| Fragment link should open a disclosure | `open the targeted details FAQ item when following a fragment link` | Make linked answers visible when visitors arrive | perf-003 |

### M7 AEO and agent readiness (10 rows)

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Schemas per page | `review structured data on every indexable page` | Apply appropriate schema types that match visible content | `03_skills/aeo-optimization/SKILL.md` |
| Agent readiness overview | `Cloudflare agent readiness framework categories` | Technical reference for applicable readiness checks | `03_skills/agent-readiness-frontier/SKILL.md` |
| Agent-ready baseline files | `agent ready baseline documents for a public static Astro site` | Generic baseline | `03_skills/agent-readiness-frontier/SKILL.md` |
| OAuth resource check fails | `OAuth protected resource metadata resource field must match the serving origin` | Origin-mismatch lesson | `03_skills/agent-readiness-frontier/SKILL.md` |
| Authentication documentation on a public site | `public site authentication documentation states that no resources require authentication` | Describe the actual access model without inventing protected services | `03_skills/agent-readiness-frontier/SKILL.md` |
| A2A card | `A2A agent discovery card is distinct from the MCP card` | Keep discovery documents aligned with the service they describe | `03_skills/agent-readiness-frontier/SKILL.md` |
| API catalog format | `API catalog must use the RFC 9264 linkset format` | Linkset rule | `03_skills/agent-readiness-frontier/SKILL.md` |
| Markdown negotiation | `markdown negotiation Accept actually return markdown not just Link header` | Middleware must serve the negotiated representation | `03_skills/agent-readiness-frontier/SKILL.md` |
| Live scan before calling it done | `run a live agent readiness scan and require the applicable checks to pass` | Verify the deployed site, with explicit treatment of inapplicable checks | `03_skills/agent-readiness-frontier/SKILL.md` |
| Generated AI catalog | `generate the AI catalog in the build never hand author it` | Compile a regional bakery chain's guide catalog from its content source to prevent drift | `03_skills/agent-readiness-frontier/SKILL.md` |

### M8 Site-port migration (when replacing an existing site) (8 rows)

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Porting an existing site | `rebuilding a site build the old URL inventory before mapping slugs` | Never assume a bicycle-parts company's old guide URLs match its new slugs | `05_automations/client-site-first-build/runbook_appendix/backlink_discovery.md` |
| Crawled pages as a contract | `set equality audit of crawled URLs` | Account for every discovered URL in the migration plan | `05_automations/client-site-first-build/runbook_appendix/redirect_authoring.md` |
| Old-URL discovery tiers | `backlink discovery tiers sitemap Wayback search Common Crawl` | Start with direct inventories, then expand to archives and external discovery | `05_automations/client-site-first-build/runbook_appendix/backlink_discovery.md` |
| WordPress URL patterns | `classify WordPress media category tag and feed URLs for redirects` | Categorize legacy URLs before assigning redirect behavior | `05_automations/client-site-first-build/runbook_appendix/redirect_authoring.md` |
| Old Apache redirects | `flatten old Apache redirect chains` | Send legacy URLs directly to their final destinations | `05_automations/client-site-first-build/runbook_appendix/redirect_authoring.md` |
| Old CMS asset URLs | `old CMS asset URLs on the domain become 404 at DNS cutover` | Preserve or redirect assets as well as pages | `05_automations/client-site-first-build/runbook_appendix/asset_placement.md` |
| Strict-fidelity rebuild | `transcribe reverse-engineered captured pages` | Use captured pages as the visual and structural contract | `05_automations/client-site-first-build/runbook_appendix/build_mode_decision.md` |
| Many pages to transcribe | `multi-agent parallel rebuild in bounded batches of pages` | Divide page work with shared conventions and review each integrated batch | `05_automations/client-site-first-build/runbook_appendix/build_mode_decision.md` |

### M9 ACE loop operations (6 rows)

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Roles in the loop | `generator reflector curator as separate agents in sequence` | Separate generation, independent review and lesson curation | ace-loop-agent-discipline-001 |
| Keeping the loop honest | `the examinee may not modify the exam generator reports check defects` | Report suspected evaluation defects without changing the checks being used to judge the build | ace-loop-agent-discipline-001 |
| Orchestrator doing generator work | `independent reviewer scores and never fixes orchestrator never builds inline` | Preserve role separation so review remains independent | ace-loop-agent-discipline-001 |
| Canonical reference exists | `visual diff against the canonical handoff when one exists` | Compare the implementation with the agreed reference | template-to-astro-build-fidelity-verification-recipe-001 (in `05_automations/resource-hub-maintenance/skillbook.md`) |
| House defaults don't fit | `write down where workbench defaults do not apply before the build loop` | Record justified deviations before evaluation begins | `05_automations/client-site-first-build/runbook_appendix/ace_loop_astro_build.md` |
| Planning the build | `recall in batches and run read-only sweeps before writing the plan` | Gather relevant guidance and inspect the existing project before committing to a build plan | `05_automations/client-site-first-build/runbook_appendix/ace_loop_astro_build.md` |
### M10 Content gate and writing wave (12 rows)

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Designing a content gate | `content gate separates hidden harms from house style` | Separate checks for consequential defects from editorial lint | Check factual accuracy and unintended disclosure before style |
| Floor classes for leaks | `prove each disclosure check with a deliberately defective example` | Generic disclosure checks | Verify that each check rejects a known defect |
| Positive control lies | `positive control certified the defect` | Controls are claims that need verification | Inspect the control before trusting its result |
| Cold-reader test | `cold reader belief test on the foundation` | Test what an unfamiliar reader would believe | Compare the reader's interpretation with supported facts |
| Writer defects trace to briefs | `orchestrator wording most writer defects` | Brief wording can become published copy | Correct misleading instructions before regenerating copy |
| Facts digest format | `fact digest one line per fact with status source and verified` | A compact, traceable facts digest | Record each fact's status, source and verification |
| Status placement | `status lives in tense one status statement page` | Clear availability and release status | Match each claim's tense to its verified availability and keep the status beside the claim it describes |
| FAQ JSON-LD status | `FAQ answers that name products carry their own status word` | FAQ answers remain accurate outside the page | Include relevant availability status in each standalone answer |
| Product claims vs code | `check a capability against the path that serves it with a tense per capability` | Claims tied to working functionality | Verify each claimed feature through the route that provides it |
| Deep research claims | `fetch and check source claims for contradictions` | Claims limited by the available evidence | Open the underlying sources and resolve contradictions |
| Amending a fact | `amending a fact requires a sweep of affected copy` | Consistent corrections across writing passes | Recheck every page that depends on the amended fact |
| Signed strings registry | `register signed page strings with a dry run and refuse unknown keys` | Registry protection | Dry-run registration and reject unknown keys |

### M11 Design wave: imagery, figures, motion (10 rows)

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Words over a painting | `check text readability over painted imagery` | Text-over-image review | qa-031 |
| Adding a scrim | `check the scrim against the image and text` | Scrim guidance | media-007 |
| Art-directed image container | `art directed image container` | Image-container guidance | media-005 |
| Image model paints layout words | `image prompt calibration pilot what the model did` | Prompt calibration | Test a representative prompt before generating the full asset set |
| Painting that moves | `make a painting move cutting elements against the fill` | Painted-art lesson | Separate moving elements and reconstruct the background beneath them |
| Data figure | `build-time figure layout solver from a spec of keys` | Figure system | Define stable keys and solve the layout during the build |
| Sticky layer judged wrongly | `inspect sticky layers in their actual scroll state` | Sticky-layer review | tooling-004 |
| Headline in first screen on phones | `first screen check at the visible viewport minus browser UI` | Visible-viewport rule | Check the headline with mobile browser controls visible |
| Auto motion | `pause stop hide WCAG 2.2.2 ambient motion` | Design obligations | Provide applicable pause, stop or hide controls |
| Above-the-fold media | `govern above-the-fold media competing for LCP as one class` | Media governance | Budget competing images, video and canvas together |

### M12 WebGL (7 rows)

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Choosing a renderer | `renderer decision tree WebGL` | Decision tree | `03_skills/webgl-craft/SKILL.md` |
| When may the GPU layer start | `when may a WebGL layer boot never during page load` | Boot rules | `03_skills/webgl-hardening-and-testing/SKILL.md` |
| Static design under the canvas | `layer stack static design aria-hidden canvas first frame truth` | Layer stack | `03_skills/webgl-hardening-and-testing/SKILL.md` |
| Boot jank on scroll | `slice WebGL boot so no task exceeds 50 ms perf-002` | Boot-task budgeting | perf-002 |
| Animations broken in production only | `production CSP stopped painted scenes because data URLs were blocked` | CSP parity error | Test required media sources under the production policy |
| Gates under production CSP | `run motion checks with production CSP headers` | Test parity rule | Apply production headers to the served build before testing |
| Device tier in headless | `headless SwiftShader force and confirm the device tier` | Headless-device verification | tooling-006 |

### M13 Gates, provenance and agent operations (9 rows)

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Verification taking hours | `verification churn can dominate a build cycle` | Verification budget | Run relevant checks and repeat them when changes or failures justify it |
| Which build did a gate grade | `gate log names the build it graded with the served tree hash` | Build provenance | tooling-005 |
| Lighthouse wrote nothing | `Lighthouse produced zero reports and the script printed all pass` | Zero-input PASS trap | Treat missing reports as failure |
| Mutant proof | `prove a new gate rule by running the old gate code on the mutant` | Old-code-vs-mutant rule | Demonstrate that the old check misses the defect and the new check catches it |
| Pipes hide failures | `cmd piped to tail returns the pipe exit status` | Silent instrument faults | Preserve and inspect the tested command's exit status |
| Process checks | `pgrep -f matches its own command line` | pgrep self-match trap | Confirm the intended process rather than a matching search command |
| Too many agents | `background agents can exhaust session memory` | Agent fan-out limit | Bound concurrency and context size |
| Shared scratchpad | `shared scratchpads can compromise independent review` | Blinding hazard | Keep independent review evidence separate until comparison |
| Fast first preview | `ship a credible first preview for design review` | Loop shape | Get the page into a reviewable browser state early |

### M14 Memory capture and self-heal (4 rows)

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Capture during the build | `capture decisions evidence and refresh points during a site build` | Capture contract | Record reusable lessons alongside their supporting evidence |
| Flag bias | `audit reusable lessons across build and maintenance workflows` | Flag audit | Apply the same correction criteria wherever a lesson is used |
| Batch store from agent JSON | `empty body memory store bug assert minimum content length` | Recovery lesson | Validate extracted bodies before storing and retry failed entries |
| Packaging for another developer | `package reusable lessons with search phrases` | Packaging rule | Include readable search phrases rather than relying on private record identifiers |

### M15 Brand assets and documents (3 rows)

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Brand bundle moved | `copy and verify the brand bundle before retiring its old location` | Brand-asset migration | Verify copied assets and update references before removing the original |
| Project tooling separation | `keep project tooling separate from shared configuration` | Separation rule | Scope project-specific tools and settings to that project |
| A foreign document as a page | `imported document pages need a fidelity check` | Imported-document recipe | Compare the rendered page with its source for content and layout fidelity |

---

## Site registry

Add a row for each site you operate. Keep the corresponding website-maintenance and, where applicable, resource-hub-maintenance records consistent when handing over the build. The example row is invented; replace it with your first real site.

| Site | Platform | Repo | Branches | Worker / previews | Data | Gate | Status |
|---|---|---|---|---|---|---|---|
| copperbasket-kitchens.example (invented kitchen-equipment maker) | cloudflare-workers (static assets + Workers Builds) | GitHub `<your-github-user>/copperbasket-site` | `main` = production; `preview` and any feature branch = Worker Preview | Worker Previews, optionally behind Cloudflare Access; record the actual stable preview URL supplied by Cloudflare | D1 `copperbasket-inquiries` (production) / `copperbasket-inquiries-preview` (previews); Turnstile; a transactional email provider | production settings applied by the build on `main` | example only |

---

## File Manifest

| File | Purpose |
|------|---------|
| comprehensive_guide.md | This file |
| personality.json | Dr. Merry Backus, the first-build automation persona |
| skillbook.md | Reusable strategies with stable entry IDs |
| setup_instructions.md | Prerequisites on your machine |
| startup_queries.json | The startup recall batch of search phrases |
| recall_phrases.json | Recall-map phrases and triggers |
| EDITION_NOTES.md | What this edition includes and how to use it |
| _gate/GATE.md | Build and maintenance quality checks |
| runbook_appendix/cloudflare_workers_github_path.md | **The worked path**: the Workers + GitHub first-build order, start to launch |
| runbook_appendix/ace_loop_astro_build.md | ACE loop specification, hard 9.8/10 threshold and empirical checks |
| runbook_appendix/build_mode_decision.md | WEBSITE_ONLY / RESOURCE_HUB_ONLY / COMBINED + IS_SITE_PORT |
| runbook_appendix/zip_handoff.md | Design-handoff archive preparation and intake |
| runbook_appendix/in_browser_compute_module.md | Running a real runtime in the visitor's browser while retaining static hosting |
| runbook_appendix/sanity_org_setup.md | Sanity project setup for hub modes, with your own credentials |
| runbook_appendix/cross_automation_handoff.md | Registry handoff to website and resource-hub maintenance |
| runbook_appendix/backlink_discovery.md | Discovering inbound links before a site migration |
| runbook_appendix/redirect_authoring.md | Authoring Workers redirects for a site migration |
| runbook_appendix/asset_placement.md | Placing migrated assets and preserving references |
| runbook_appendix/redirect_application.md | Applying redirects and testing them with curl on the preview |
| runbook_appendix/gsc_export_pause.md | Requesting the site's Google Search Console export |
| runbook_appendix/dns_cutover_pause.md | Coordinating the domain owner's DNS cutover |
| runbook_appendix/old_website_archive.md | Maintaining a persistent archive of the old site |

---

## Step 2.5: Input-source discipline: Strict-Fidelity vs Creative-Liberty

Before the Generator runs, identify the mode from the input and pass it into the Generator's task specification. The Reflector's rubric switches with it.

**MODE A: STRICT-FIDELITY** (the input is a reverse-engineered capture of a live site: per-page HTML + screenshot + notes + media list). The Generator TRANSCRIBES. It does not invent sections, change section order, paraphrase copy, omit or add elements, rearrange layout or swap components beyond approved deviations. It MAY clean builder/jQuery DOM bloat into semantic HTML + Tailwind, use native `position: sticky` and `<details>/<summary>`, apply the approved shared header and footer, and retain explicit asset placeholders until the corresponding files are resolved. The Reflector verifies per page: layout pattern, section order, verbatim copy on 3 sampled sections, imagery placement against the screenshot, and components. Any unverified deviation is a defect. (Recall: `transcribe reverse-engineered captured pages`.)

**MODE B: CREATIVE-LIBERTY** (a Claude Design zip, a brief, or a from-scratch build). The Generator brings full design and graphic-design judgment: layout, section order, added sections that improve the visitor's path, responsive behaviour, motion, accessibility, and performance. It still honours the brand tokens, shared site components, structured-data requirements and empirical checks. Most first builds are MODE B.

## Step 2.6: MODE A multi-agent parallel rebuild (8 or more captured pages, or a multi-page fix wave)

Parallel design-generator agents transcribe pages in batches of 5 to 7. One design-reflector per generator checks each page for exact content and structural fidelity: section parity, verbatim copy, asset placeholder count, relative internal links, no builder residue, slug fidelity, unchanged shared header and footer, form-source values, heading hierarchy, landmarks, Tailwind class shape, modifier isolation, and visual differences. A **MANDATORY final cross-page reflector** then audits build health, shared-component consistency, navigation, CSS regression, consent persistence, asset coverage, slug fidelity and form integration. **Cross-file check**: when several forms post to one endpoint, union every client-side form-source value and assert it is a subset of the server's allowlist. A value missing from the allowlist causes a silent 400 that per-page checks can miss. Close with targeted fixes and a re-run of the cross-page reflector. (Recall: `multi-agent parallel rebuild in bounded batches of pages`.)

---

## Execution Model

The main agent reads this guide and executes directly using the first-build persona. The ACE build loop uses the three agent definitions in `05_automations/agents/design-generator.md`, `05_automations/agents/design-reflector.md`, and `05_automations/agents/design-curator.md`; everything else is direct orchestration. First builds are sequential: resolve input, configure Sanity when required, build with Astro, connect GitHub, configure Workers, and hand over. These stages benefit from full context. Use sub-agents where parallel specialization helps.

---

## Workflow

### PHASE 1: BOOTSTRAP

**Step 1: Startup protocol**. Run the startup recall batch in `startup_queries.json` and state what you recalled before continuing.

**Step 0.5a: IS_SITE_PORT** (always establish; default false). If the request makes it obvious, proceed. Otherwise ask: *"Has anything been published at this domain in the last few years that people link to? If yes, this is a port; if no, it is a new site."* If true, capture `OLD_DOMAIN` and include DNS planning, backlink discovery, redirects, asset migration, preview verification, the Search Console export, and the domain owner's cutover.

**Step 0.5b: DNS strategy** (ports only). Recommend moving the old domain's nameservers to Cloudflare when its DNS controls and apex CNAME flattening fit the site's requirements. Verify current plan availability and pricing before relying on them. The domain owner changes nameservers at the registrar during the coordinated cutover; the automation does not modify the registrar.

**Step 0.5: Build mode** (`runbook_appendix/build_mode_decision.md`): WEBSITE_ONLY (static Astro, no Sanity), RESOURCE_HUB_ONLY (Sanity-backed hub), COMBINED (marketing site + hub routes in one Astro project, with a hybrid page strategy).

**Step 2: Resolve input** (`runbook_appendix/zip_handoff.md`): locate the supplied handoff archive; unzip it into a dedicated extraction directory in the build workspace, never into the repository; hash every asset into an asset manifest; read the handoff's introductory documentation and recite its key sections; enumerate the design tokens in a structured record. Before proceeding, confirm that the instructions are parsed and cited, every referenced asset is present, and tokens are enumerated. Halt and ask about any missing asset; never fabricate one.

**Step 3: Identity and naming**: establish the slug, display name, GitHub repository, Worker name, preview branch name (`preview` is a good default), and separate production and preview D1 database names. Use a consistent project prefix, such as `pedalbrook-guides` for an invented bicycle-parts company's guide library. Confirm each default.

**Step 3.5: Forms, gated content, tracking posture.** Ask, never default:

1. **Where do submissions go?** On a Workers site, the standard pattern is a Worker API writing to D1 first and emailing second, so an email failure does not lose the submission. If the site already uses a CRM or marketing-automation form, record it and allowlist its submission origin in the CSP `form-action`.
2. **Gated content?** If yes, list the slugs. During the build, scaffold a registry plus a per-slug landing page and a thank-you page that provides the asset. The form provider's post-submission redirect points to the site's thank-you page, so moving an asset requires changing only one registry entry.
3. **Tracking posture.** The proposed default is **no cookies, no banner, cookieless analytics, and no browser storage for attribution**, subject to confirmation. If tracking or paid ads are requested, establish consent controls first: banner, Consent Mode v2 default-denied, tags typed `text/plain` by category, CSP allowlist, and a fresh review of the privacy page. A site under a parent domain that already runs a consent plugin bridges to it instead. See `cookie-consent-decision-tree-001` (in `05_automations/resource-hub-maintenance/skillbook.md`) and `cookie-consent-existing-wp-bridge-001`.

Record the answers in the workspace's intake record. Confirm that the form destination, gated-content list, and tracking posture are recorded before generation begins.
### PHASE 2: SANITY (skipped when WEBSITE_ONLY)

Per `05_automations/client-site-first-build/runbook_appendix/sanity_org_setup.md`: one Sanity project per site under the site owner's own organization; the four polymorphic document types only (resource, taxonomy, collection, series); a write token stored in an external key file as `SANITY_API_TOKEN`, mode 600, never in the repo. Read through `@sanity/client` or `bash 06_web_tools/bearer-curl SANITY_API_TOKEN <url>` from the workbench root. Seed taxonomy only if the site owner supplied it; otherwise leave seeding until the resource categories have been agreed. **R2**: Studio loads; four types present; a GROQ test query returns documents; no auth errors.

### PHASE 3: ASTRO BUILD VIA ACE LOOP @ 9.8/10 HARD

> **MANDATORY**: Steps 6-8 run inside an ACE Design Loop: Generator, then Reflector, then **Curator every iteration**, until SATISFACTORY at 9.8/10 HARD with every dimension at 9.5 or above and every empirical gate green. Plan for 3 iterations; max 5; STALLED if no improvement of 0.1 or more across two iterations. Code-inspection scoring caps around 9.6-9.7; Lighthouse + axe on the built site are required to clear 9.8.
>
> **ACE workspace**: create a separate, ignored workspace for the site's build records, outside the deployable source tree. Full spec: `05_automations/client-site-first-build/runbook_appendix/ace_loop_astro_build.md`.

**Step 1.5: Backlink discovery** (ports only; runs beside Phase 3): `05_automations/client-site-first-build/runbook_appendix/backlink_discovery.md`. Print the Search Console verification instructions immediately so the domain owner can start the DNS TXT step while discovery runs. Check the sitemap, then Wayback, then Common Crawl for both the site's own captured URLs and referring pages. Wait for the Search Console export or an explicit decision to skip it, then verify referrers and categorize: HIGH = found as both a site URL and a referrer target, LOW = site URL only, EXTERNAL_OUTREACH = referrer target only. Then archive the old site using `05_automations/client-site-first-build/runbook_appendix/old_website_archive.md`.

**Step 6: Generator pass (design-generator)**
- **Initial scaffold.** Start from a clean scaffold, not a copy of another site's repo. If copying is necessary, exclude `.git`, `node_modules`, `dist`, `.astro` and the lockfile; otherwise the other site's remote travels with it and a later push can land in the wrong repo. Stack: Astro static-first + Tailwind v4 through the Vite plugin; exact-pinned dependencies checked against npm latest; `.nvmrc` + `.node-version`; `wrangler.jsonc` with `account_id` pinned, `workers_dev: false`, `preview_urls: true`, `assets` with an `ASSETS` binding, `run_worker_first` for the Worker routes, and the apex as a custom-domain route. These are files and settings to create in the site repo.
- **6c Decomposition.** Translate the site's written intent into BaseLayout + Hero + Section components; design tokens into CSS custom properties; AEO schemas into BaseLayout (Organization, WebSite, BreadcrumbList; FAQPage where the page has an FAQ; noindex pages carry none); page scripts into the layout slot. **Indexing posture on Workers is a header posture**: preview builds send `X-Robots-Tag: noindex, nofollow` on every response, robots.txt stays crawlable, and no robots meta tag ships. The alternative combination of robots meta + `Disallow: /` + platform authentication applies only to the Vercel preview setup.
- **6.5 Agent-readiness Level 5 scaffold (HARD; 70 or more on isitagentready is the gate, Level 5 the target).** Create the site's discovery artifacts: robots.txt (production: a content-signal line + AI-crawler allowlist + Sitemap + Agentmap), sitemap, Link response headers (`public/_headers`, and in code for Worker-built responses), markdown negotiation (the Worker answers `Accept: text/markdown` from build-time `.md` twins with `Vary: Accept`), `llms.txt`, `humans.txt`, `/.well-known/api-catalog` (RFC 9264 linkset), `agent-skills/index.json` (agentskills.io format with real sha256 digests), `agent-card.json` (A2A, distinct from an MCP card), and `ai-catalog.json` generated in the build from those files, never hand-authored, with an advisory conformance check. Add WebMCP read-only tools and honest authentication metadata: `auth.md`, `oauth-authorization-server` with `agent_auth`, and `oauth-protected-resource` with a NON-EMPTY `authorization_servers` naming the site's own metadata, empty scopes, and a `resource` field equal to the serving origin. **Never declare a third-party OAuth server the site does not gate behind.** On a public site with no token-protected API, the strict authMd sub-check stays red by principle; do not fabricate scopes to make it green. Record that expected result separately from required passing checks. Web Bot Auth uses an ed25519 key directory signed and served under `.well-known`; check its routing against the `run_worker_first` exclusion. Before building these files, check the current versions and requirements of the agent-readiness standards, including ARDS, isitagentready, agent-skills, MCP server card, DNS-AID and Web Bot Auth. Review any changed requirements before adopting them.
- **Analytics on Workers**: verify whether the current delivery setup injects the Cloudflare Web Analytics beacon into Worker-served HTML. If it does not, add the beacon to the base layout explicitly. Its token is public by design and may go on the gitleaks allowlist. Public-by-design keys, such as the Turnstile sitekey and analytics token, may be allowlisted; secrets never are.
- **6.6 Build-time gates in the repo**: implement a `validate-aeo` command that walks built HTML, validates JSON-LD per type, and exits 1 on failure; a build verification script that checks preview and production postures; a content check against the agreed requirements; a links check; an axe battery over every route; and a CSP hash step. Gated content, if any, needs a registry, landing page and thank-you page, smoke-tested on the preview.
- **6.7 Privacy page** (every build): assess every sentence against the code using a TRUE/FALSE/UNVERIFIABLE truth table, resolve unsupported statements, and link the resulting page from the footer. Ship a consent banner only when the site's tracking setup requires one.
- **6d**: the Generator records the strategies it applied and a manifest of files written, and runs its own axe pass before handing over.

**Step 7: Reflector pass (design-reflector)**
- 7a: score the five dimensions (completeness, correctness, quality, convention adherence, skillbook utilization).
- 7b: **EMPIRICAL gates** on the built site (`rm -rf dist && npm run build`, zero warnings): Lighthouse (Performance 90+, Accessibility 95+, Best Practices 95+, SEO 90+; CPU-timed metrics as a distribution of 5 or more runs), axe (zero Critical/Serious) on every route at 1440, 768 and 375, `validate-aeo`, header posture, structurally valid agent-readiness files (linkset array, server-card shape, real digests, honest auth files), markdown negotiation answering `text/markdown` locally (`npx wrangler dev`), CSP parity (motion and initial-frame checks run with the built `dist/_headers` rules injected), and first-screen checks at the visible viewport. Every gate log's first line is the served tree's hash plus the commit.
- **No system Chrome?** Run `npx playwright install chromium`, resolve the bundled browser's executable path through Playwright, and set `CHROME_PATH` to it. Run Lighthouse with `--chrome-flags='--headless --no-sandbox --disable-gpu'`, and run axe by injecting the installed axe-core browser bundle into a Playwright page. Use a SHORT temporary path for Chrome's profile: an overly long socket path can prevent Lighthouse from writing results while a careless summary still prints PASS. A gate that read zero inputs is not a PASS.
- 7c: classify prior strategies helpful/harmful/neutral; 7d: create the P-list (file:line, "change X to Y" for code; for copy, the harm and the constraint, never a replacement sentence).
- 7e: stopping decision. SATISFACTORY = 9.8 HARD (9.79 is CONTINUE) AND all dimensions at 9.5 or above AND all empirical gates green. STALLED = no gain of 0.1 or more over two iterations. MAX = 5, then escalate to the site owner.

**Step 8: Curator pass (design-curator), EVERY iteration**: apply ADD/UPDATE/TAG/REMOVE deltas to `05_automations/client-site-first-build/skillbook.md` from the iteration's reflection, keeping changes small. Tag strategies helpful or harmful, and retain each new or updated skill as a separate, searchable lesson. If SATISFACTORY, exit to Phase 4; otherwise return to Step 6 with the P-list.

**R-ACE**: final overall score 9.8 or above, every dimension at 9.5 or above, every empirical gate green on the hand-off build's hash, skillbook updated, new lessons retained, and workspace complete. MAX without SATISFACTORY: escalate; do NOT proceed.

### PHASE 4: GIT + DEPLOY (Cloudflare Workers + GitHub, the worked path)

Account setup for this phase: `09_guides/GITHUB_SETUP.md` and `09_guides/DEPLOY_CLOUDFLARE.md`. For Vercel instead, use `09_guides/DEPLOY_VERCEL.md`.

**Merge discipline (the rule that replaces branch protection).** Merge to `main` only after `npm run build` and the verification scripts are green, the preview link has been checked, and the site owner has received a one-line note of what is going out: commit + what changed. Check the repository's current plan and protection settings; where branch protection is unavailable, this discipline is the release control because merging to `main` deploys production. Get the content owner's sign-off before changes to page **copy**, because published words are a promise to readers. The first build ships to the **preview branch**; `main` receives the site at launch by fast-forward (`git push origin preview:main`) after sign-off and successful pre-launch checks.

**Step 9: GitHub repo.** Run `gh repo create <your-github-user>/<slug>-website --private`; set per-repo identity with `git config user.email <your-address>`. Create `.gitleaks.toml` with default rules and an allowlist for public-by-design keys, plus `.pre-commit-config.yaml`, then run `pre-commit install`. Verify privacy as a pair: anonymous REST 404 AND authenticated `private: true`. Make the first commit within 30 minutes of scaffolding so work has a recoverable baseline. Enable branch protection on `main`, including no force pushes, where the GitHub plan allows it; otherwise apply the merge discipline above.

**Steps 9.5 / 9.6: Redirects and assets** (ports only): use `05_automations/client-site-first-build/runbook_appendix/redirect_authoring.md` for 1:1 mapping decisions, 301 by default, flattened chains, 410 for retired admin paths, and site-owner approval of the CSV. Use `05_automations/client-site-first-build/runbook_appendix/asset_placement.md` to HEAD-check every asset redirect at its new home. Never redirect to a file that does not exist.

**Steps 10-11: Cloudflare Workers deployments: preview and main** (below), then the first preview hand-off: give reviewers the stable branch link and, if previews are protected, add them to the Access policy. Provide a short review brief stating what is ready and what feedback is needed.

**Step 11.5a: Redirect application + curl test on the preview** (ports only): `05_automations/client-site-first-build/runbook_appendix/redirect_application.md`. Require 100% of non-regex redirect checks to pass before requesting launch approval.

#### Cloudflare Workers deployments: preview and main

**Who**: the site builder + the account holder for dashboard-only actions: GitHub connection, the Previews Base checkbox, and Zero Trust onboarding if previews will be protected. Confirm the intended account and deployment posture first. Full order: `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md`.

**The rule: one path per environment, judged by its product.** Main gets exactly one trigger. Previews get exactly one mechanism: Worker Previews. Two preview pipelines on one Worker is the failure itself, whichever one is green.

**Credentials on your machine.** Either log Wrangler in with your own account (`npx wrangler login`) and run `npx wrangler <verb>` from the site root, or keep an API token in the external key file configured for the workbench and invoke `06_web_tools/wrangler-safe` from the site repo using its resolved package location. The wrapper reads the key file without sourcing it, removes any other `CLOUDFLARE_*` variables your shell exports, and refuses when the repo's pinned `account_id` differs from the key's account. Either way, `account_id` is pinned in `wrangler.jsonc`. For raw API calls, run `bash 06_web_tools/cf-api <METHOD> <path>` from the workbench root; `{account}` and `{zone}` in the path are filled from the key file.

1. **CF-a: Main (production), exactly one trigger.** The dashboard's GitHub connection creates it; read it back by API right after the click. Branch `main`, build `npm run build`, deploy `npx wrangler deploy`. Implement production guards in the build: check that the build's account equals the pin; reject missing required keys and published vendor test keys after trimming values; and apply the production posture described in CF-h. Public build variables, such as the Turnstile sitekey, are trigger environment variables set by API. Nothing else deploys to production.
2. **CF-b: Previews = Cloudflare Worker Previews.** In Worker > Settings > Builds > **Previews Base**, keep "Builds for Preview branches" **ticked**, with Preview command `npx wrangler preview`. Verify the current platform behavior for non-main branches and the installed Wrangler version before setup. **Never untick the option as a casual way to stop a pipeline**: it can remove the preview build configuration. Use a Wrangler version that supports this workflow. Each non-main branch should receive a stable Preview URL such as `https://<branch>-<your-worker>.<your-workers-subdomain>/`, plus an immutable version URL per push; confirm the actual URLs returned by the platform.
3. **CF-c: The `previews` block.** A Preview inherits **no** production bindings, so `wrangler.jsonc` declares every binding under `previews`: vars, its **own D1 database**, its own ratelimit `namespace_id`, and observability settings that keep the privacy page's promise. Crons do not run on Previews. Production `wrangler deploy` ignores the block; prove it with a dry run. Without it, preview pushes fail with a missing-configuration error. **Branch ancestry trap**: a branch cut from `main` inherits main's config; until main has the block, every main-based branch fails. Carry only the block, byte for byte, never preview-only extras such as a cron whose handler exists only on the preview branch. Name in a comment what was deliberately not carried.
4. **CF-d: Preview resources and secrets.** Create the preview D1 and apply migrations **through a throwaway config** that names only that database, with `migrations_dir` pointing to the repo's migration directory by absolute path. Set preview secrets in the **Preview base config BEFORE any Preview exists** using `npx wrangler preview base-config secret put <NAME>`, with the value piped on stdin and never printed. Base-config secrets are copied into a Preview when it is created, then persist; a per-Preview `secret put` lasts one deployment. A Preview created before its configuration is stale: **delete that Preview and let the next push recreate it**. Since `wrangler preview delete` auto-confirms, guard any scripted delete by exact name:
   ```bash
   [ "$PREVIEW_NAME" = "$EXPECTED_PREVIEW_NAME" ] || exit 9
   ```
   Require `EXPECTED_PREVIEW_NAME` to contain the explicitly selected disposable Preview name. **Spike first** on a throwaway named Preview (`npx wrangler preview --name setup-check`), with two consecutive deployments. Set production secrets using `npx wrangler secret put` while main is the latest deployed version.
5. **CF-e: Optionally lock the preview with Access.** Prefer locking previews when they show unreleased work, such as a ceramic studio's upcoming collection, because a preview link travels. Zero Trust onboarding is the account holder's dashboard step; check the current plan and payment requirements. Enable Access for **Previews only** through the Worker's domain and access settings; choosing "All traffic" would lock production. Allow the intended account members. One Access app with destination type `preview_worker` covers the Worker's Previews. Add a service-token policy with decision `non_identity` for automation; store its two values in the external key file as `CF_ACCESS_CLIENT_ID` and `CF_ACCESS_CLIENT_SECRET`, never displayed. Probe without leaking the session: dump headers to a mode-600 temporary file and inspect only the required header names and safe values. Never print the complete header dump. Setup guidance: `09_guides/DEPLOY_CLOUDFLARE.md`.
6. **CF-f: Pre-push gate, the clean-clone CI simulation.** Build a clean clone of exactly what you are about to push, the way Workers Builds will:
   ```bash
   # Commit first: a clone sees only committed files, which is all the builder sees.
   # Set SITE_REPO, BUILD_BRANCH and BUILD_ACCOUNT_ID before running.
   # SITE_REPO is the local repository path.
   # Use main before a production push so production guards and posture run.
   # BUILD_ACCOUNT_ID is the non-secret account ID from the configured key file.
   # Parse that file as data; never source it.
   : "${SITE_REPO:?Set the local repository path}"
   : "${BUILD_BRANCH:?Set the branch to build}"
   : "${BUILD_ACCOUNT_ID:?Set the expected account ID}"

   SIM="$(mktemp -d)"
   mkdir -p "$SIM/home"
   git clone --quiet --branch "$BUILD_BRANCH" "$SITE_REPO" "$SIM/site" || exit 1

   # A node symlink directory may have no npm beside it; ask Node itself.
   NODE_BIN="$(dirname "$(node -p 'process.execPath')")"

   (
     cd "$SIM/site" &&
     env -i PATH="$NODE_BIN:/usr/bin:/bin" HOME="$SIM/home" \
       CLOUDFLARE_ACCOUNT_ID="$BUILD_ACCOUNT_ID" \
       CI=true WORKERS_CI=1 WORKERS_CI_BRANCH="$BUILD_BRANCH" \
       WORKERS_CI_COMMIT_SHA="$(git -C "$SIM/site" rev-parse HEAD)" \
       bash -c 'npm clean-install --progress=false && npm run build'
   )
   rc=$?
   echo "clean-clone build exit=$rc"
   # Capture the status directly, never through a pipe.
   # Exit 0 passes this build check; the remaining release checks still apply.
   ```
   Workers Builds supplies build metadata and account context; verify the current environment-variable names when configuring the workflow. The account guard compares the supplied account with the pin. A plain local build in a shell that exports another account must be refused; build locally with `env -u CLOUDFLARE_ACCOUNT_ID -u CLOUDFLARE_API_TOKEN npm run build`.
7. **CF-g: Watch the product, not the pipeline.** For previews, do not assume the main-trigger Builds API reports Worker Preview builds. Poll the preview URL until a probe path answers 200 AND carries a marker absent from the previous build. Log the anonymous response, expected to be 302 when Access protects it, and check the binding names on the deployment tagged with the pushed commit. Refuse to judge until the tag matches. For main, watch by **build uuid** using `GET /accounts/{account}/builds/builds/<uuid>` and its `/logs` endpoint, never by commit alone. Every "done" names the deployment id. At first wiring, the account holder also confirms the first preview in the dashboard. Hand reviewers the stable branch link, never a per-push link. Run the shipped watchers from the workbench root:
   ```bash
   python3 06_web_tools/preview_url_watch.py --url 'https://<branch>-<your-worker>.<your-workers-subdomain>' --probe '/<path>' --marker '<text only the new build has>'
   python3 06_web_tools/builds_watch.py --worker '<your-worker>' --commit '<sha7>' --branch main
   ```
   The preview watcher sends the Access service token when the configured key file has one. The main-build watcher exits 0 for success, 1 for failure, and 2 for timeout. Confirm the build it reports belongs to the `main` trigger, then keep watching that build's uuid.
8. **CF-h: Production posture is applied by the build.** Implement a production-posture step that runs in the build on `main` (`WORKERS_CI_BRANCH=main`): it removes the site-wide noindex header from the generated `dist/_headers` and swaps in the production robots.txt. Preview builds keep noindex; build verification checks both. This replaces hand-edited cutover. Where Cloudflare forces its own noindex on preview hosts, verifiers accept any noindex on those hosts and assert the exact configured value on production.
9. **CF-i: The four standing post-deploy checks.** Run all four at the first deploy and retain them for every later deploy: (1) the clean-clone simulation passed before the push; (2) success confirmed by the product, using URL marker + commit-tagged bindings for preview, or build uuid + live probe for main, with dashboard confirmation at first wiring; (3) the preview link's lock, if previews are protected: **302** without credentials and **200** with the service token. Run the following from the workbench root:
   ```bash
   PREVIEW="https://<branch>-<your-worker>.<your-workers-subdomain>/"
   curl -s -o /dev/null -w 'no token: %{http_code}\n' "$PREVIEW"
   # Expect 302 when Access protects previews.
   python3 06_web_tools/preview_url_watch.py --url "$PREVIEW" --probe / --marker '<text on the page>' --max-seconds 60
   # Expect 200 with the token.
   ```
   A 200 without the token on a preview that should be private means it is public: stop and fix Access before sharing the link. (4) Exactly one preview mechanism: the triggers list shows only the `main` trigger, "Builds for Preview branches" is ticked, and `wrangler.jsonc` has a `previews` block.

**Post-launch change path**: the preview branch is the change path for everything: clean-environment preview build + validators, push preview, URL watcher, a note to the site owner with sign-off for copy changes, `git push origin preview:main`, watch main by build uuid, and verify live. Hold deploy-tool upgrades for at least 7 days and test them through both postures.

**R5-CF**: one main trigger; Worker Previews with a `previews` block and base-config secrets; clean-clone simulation green; all four standing checks green, including the dashboard check performed by a human rather than inferred from the API; both postures verified by the build.
### PAUSE POINT #2: NAMESERVER FLIP (ports only)

HARD halt (`05_automations/client-site-first-build/runbook_appendix/dns_cutover_pause.md`). Print the redirect totals and the curl pass rate, then the domain owner's steps: at the registrar, set the two Cloudflare nameservers shown for the zone; propagation can take up to 48 h; reply "nameservers ready". Verify the zone status by API (`active`) and only then proceed with the cutover.

### PHASE 5: HAND-OFF + SELF-HEAL

**Step 12: Cross-automation hand-off** (`05_automations/client-site-first-build/runbook_appendix/cross_automation_handoff.md`): record the site in `05_automations/website-maintenance/runbook_appendix/client_registry.md` and, for hub modes, `05_automations/resource-hub-maintenance/runbook_appendix/client_registry.md`. Add hand-off notes to the site's repo covering what was built, where it lives (repo, Worker, D1, Sanity), access and indexing controls (Access on Previews if used, header noindex, production settings by build), the change path, recurring verification checks, accepted limitations, and open items. For ports, include the redirect inventory and any external links that need updating.

**Step 13: Post-run self-heal**: review failures and manual workarounds, correct reusable instructions, and record unresolved issues with their next action.

## Reflector Checkpoints

| # | After | Key checks |
|---|---|---|
| R1 | Input review | Bundle located; supplied instructions reviewed; assets complete; tokens enumerated |
| R2 | Hub setup | Studio loads; required resource types exist; GROQ test returns documents |
| R3.5 | Forms and tracking review | Form destination, gated resource list, and tracking posture recorded |
| **R-ACE** | Build review | 9.8 HARD across all dimensions; empirical checks pass on the hand-off hash; curator ran every iteration |
| R5-CF | Deployment setup | One main trigger; Worker Previews + `previews` block; recurring verification checks pass |
| R-HANDOFF | Step 12 | Registry entries written; repo hand-off notes complete |

---

## Build Doctrine (V1 to V8): general lessons for sites on Cloudflare Workers

Generic rules for building business sites and resource libraries on Cloudflare Workers + GitHub with Astro. They cover content checks, independent writing and review, external contributions, and WebGL layers. Each rule explains why it matters. The skillbook carries the atomic versions.

### V1. Accounts, credentials and secrets
- Any work on a second Cloudflare account from a shell that exports other credentials runs only through a clean environment built from an **allowlist**, plus an `account_id` pin and refusal on a pin mismatch. A denylist goes stale when ambient credentials change. `06_web_tools/wrangler-safe` provides a wrapper for this purpose.
- Prove separation with an **authenticated**, non-mutating call using credentials that lack access to the target account (pass = authentication or authorization error); `--dry-run` skips auth and proves nothing. Pair this with an inventory that reports resources it could not read.
- The secret sweep scans every relevant surface, including repo history, workspace files, local databases and their WAL files, and session transcripts, for full values and fragments. Never print a match's secret value. Re-run the sweep at verification checkpoints and after credential rotation.
- The first token probe checks product **enablement** (the workers subdomain, Zero Trust) as well as permissions, so required dashboard actions surface in one batch. Create tokens in a private window so another account's session is not used.

### V2. Content gate and the writing wave
**Gate structure.**
- Two tiers: a FLOOR for harms that readers may not notice directly (unsupported claims, tense drift on planned features, leaks, incorrect attribution, approved strings retyped instead of included, cross-page repeats) and a LINT tier for visible house style, auto-fixed before reviewers. A floor check that false-fires more than about 1 in 10 times on real copy becomes a reviewer advisory. Calibrate on real copy from a different model, not on the check author's fixtures.
- The floor runs inside the deploy build against a committed, hashed list of prohibited wording. Derive that list from documented product limitations and editorial decisions, then measure coverage with the floor's own matcher. A copied list can silently omit terms or encode them in a form the matcher cannot recognize.
- A false-positive correction may only narrow the check: prove the false positive goes silent AND the true positive still fires, then re-scan every approved, shipped text. Numeric rules run on prose only.
- Exact n-gram checks miss synonym swaps: pair them with a one-substitution window check and scan joins between content slots. An exact-string restriction must be tested as an exact string.

**Facts and truth.**
- Facts live in a digest of `ID: fact (status · source · verified)`. Match each claim's tense and wording to its verified availability: present tense only for what a visitor can use today, and plainly future wording for anything that is not. Put the status beside the thing it describes, and keep at most one general status note per page for context. For example, a bicycle-repair co-op that has not yet opened online booking writes "online booking is planned" next to the booking section, not "book online" with a footnote further down. Surfaces that travel separately, such as metadata, OG descriptions, crawler summaries, and JSON-LD, keep their own status word.
- Put the limit before the modal ("if offered, either could ..."); a reader resolves "could" using the nearest preceding context.
- FAQ answers travel byte-equal as FAQPage JSON-LD without the rest of the page, so an answer that names something not yet available states that status inside the answer.
- The site never outruns the product: verify each product fact against its current authoritative specification or implementation, and prove **arrival** where a claim concerns delivered output. For example, a kitchen-equipment maker's spec-sheet download must produce the correct file where the visitor expects it. Execution alone is not delivery. Claims must stay within both the supporting evidence and the product's actual capability; fetch and check research summaries before using them.
- Amending a fact means sweeping it: search every writer input for the retired phrasing and re-derive every ledger row citing the fact ID.

**Rounds and reviewers.**
- Use two blind reviewers with identical manifests: one grounded in implementation and records, one reading composition as rendered. A closure check by a fresh reviewer re-observes every previously identified harm across the whole page. Allow at most 3 perceptible fixes per round, with floor fixes uncapped; after round 3, SHOW the content owner a generated approval page.
- Findings name the harm, the constraint, and the fact ID, never a replacement sentence, and introduce no unsupported quantifiers. Every orchestration artifact, including briefs, findings, check messages, mockups, and controls, is copy the writer may follow.
- The ledger's proposition restates the phrase's WHOLE claim as a stranger would understand it, cited per sentence. Watch for two true facts stitched into an untrue third and for changes in quantifier scope. A bicycle-parts guide must not imply universal compatibility merely because two components share one listed dimension.
- A cold-reader belief test is the final judge of what a stranger believes. Give a fresh reviewer rendered visitor text, including navigation and surrounding interface copy, structured belief questions, and one open question. Run it every round and on the final bytes.
- Read the page as rendered: expand includes, include surrounding interface copy, and read the heading column alone after any heading change.

**Registry, locks and content-owner decisions.**
- Approved copy enters the strings registry through a guarded update: dry-run first, unknown keys refused, approved text revised only by name with its authorizing decision, originals kept. Verify the registry after build and before any commit touching strings or facts; a consent wording change creates a new append-only consent version.
- Shared rules and facts have one canonical source. Hash-check before overwrite and keep backups outside any folder a writer reads in full.
- Content-owner decisions become fact-digest entries or rules, recorded verbatim. The content owner resolves rule interactions, and a deliberate inconsistency is not silently "tidied" away. Approval pages focus attention on what approval changes; when an amendment cannot be supported, default to cutting it.
- About pages emphasize useful value and verifiable business facts. For a ceramic studio, describe its work, services, and visitor experience using approved records. Choose structured data that fits the page and check that its fields introduce no unsupported claims.
- A product release triggers a content refresh: re-read every bullet against its heading and every closed list and "only/never" claim when an option list grows.

### V3. Design wave: imagery, figures, motion and WebGL
- **Words over art**: axe does not grade text over a raster, so render with text transparent and check p99 luminance in each line box AND the brightest pixel under each line, never p95 alone. Derive allowable background luminance from the actual text color and required contrast ratio. For dark text over light art, the lightest text color is the limiting case.
- **Scrims** are a mix toward a color: compare on/off captures, ensuring a dark scrim never makes the background lighter under light text and that areas beyond it retain at least 0.95 of their original luminance. Bound the fill to the text elements and re-audit compensating layers when the art is fixed at source. Measure the veil for each image; never carry its settings from another.
- **Art direction**: a container switches composition at the breakpoint of the CONTENT it holds. Prove coverage as `(boxW/boxH)/(imgW/imgH)` across widths AND content states. Marks over cover-fit art are sized in the art's displayed units. A layer derived from one crop draws only while that crop shows, with a live listener that handles transitions in both directions.
- **Imagery pipeline**: describe the picture, never the page, because image models paint layout nouns. Pilot 3 to 5 images, with at most 3 rerolls using changed wording. Check stacked plates for seams using CIE76 ΔE across their shared 5% edges. Phones get their own composition; any pixel edit composites onto the untouched master and saves at source quality.
- **Painted art in motion**: the painting is the spec. Cut it into pieces that recompose it at rest, removing matte contamination against the fill so frame 0 equals the still. Animate by displacement and keep displacement zero wherever its reach would disturb thin painted detail.
- **Figures**: static-first, with a specification of keys, solved JSON at build time using a shared seeded PRNG, and a static component. Collisions and Gestalt violations fail the build. Keep words in the registry and provide an HTML equivalent outside an aria-hidden SVG. Derive coupled coordinates rather than typing them separately. Decide which labels remain visible at rest before choosing orbit angles.
- **Captures and viewports**: judge sticky or fixed layers from viewport captures at named scroll positions, never a full-page capture. Run first-screen checks at the VISIBLE viewport, about 375x553 on a small phone, and sweep heights. Report what headless cannot emulate as "not run".
- **Motion**: auto-motion longer than 5 s ships a visible pause control (WCAG 2.2.2) whose rule outranks every animation shorthand on the same element. Reduced motion means no decorative motion; every hover-revealed layer has a touch path.
- **WebGL**: route every canvas/WebGL layer through `03_skills/webgl-craft/SKILL.md`: renderer choice, DPR at most 1.5, at most 30 KB gz per layer, static design under an aria-hidden canvas, ambient layers booting after load and idle while in view, context-loss handling, and loop cleanup. No boot task exceeds 50 ms at 4x CPU slowdown; slice uploads into macrotasks. Run motion and frame-0 checks under the production CSP. Vite can inline small assets as `data:` URLs that `connect-src 'self'` blocks when fetched. Confirm the actual renderer: headless runs may use SwiftShader, whose fps indicates relative software-rendering cost rather than visitor-device performance. Treat research summaries as leads and verify their claims against primary sources.

### V4. Forms and privacy on Workers
- D1 insert first, email second; Turnstile fails closed. Test keys work only on preview hosts and must be proven rejected on production. The rate-limit binding is a brake, never the sole validation gate; fill time is a page-measured duration.
- **Verify D1 Time Travel retention for the current Workers plan** before relying on it; add a monthly export so recovery does not depend entirely on the platform's retention window.
- Repeat sign-ups are indistinguishable from first ones; request bodies are never logged. The Worker logs errors only, with automated checks for accidental payload logging.
- Privacy page = a TRUE/FALSE/UNVERIFIABLE truth table against the code before approval. Default posture: no nonessential cookies or browser storage, no consent-dependent tracking, and cookieless analytics only after checking their actual behavior. For a garden-supply shop adding attribution tracking, determine the applicable consent requirements before enabling it. Where consent is required, deploy the banner first, set Consent Mode v2 to default-denied, keep tags inert as `text/plain` by category, review the CSP allowlist, and re-verify the privacy page.

### V5. Gates, provenance and the ACE page loop
- A positive control is a claim: after widening a check, rerun the old controls first, because a newly failing control may have been certifying a defect. Prove a new rule by running the pre-edit check on the new deliberately defective input. That input counts only when its defect is shown applied and the relevant check reports its own FAIL.
- A check that read zero inputs is not a PASS; every PASS prints what it measured, and every conditional check prints the branch it took.
- Every verification log's first line is the served tree's hash plus the commit. Hand-off order is commit, final build, checks, report. Re-run any check whose logged hash differs from the delivered tree.
- Budget the suite, not each rule: run a fast core set on the final build and heavy sweeps once per iteration during review. Late fixes re-run the checks their diff can affect. Stop and report when verification exceeds about 90 minutes.
- CPU-timed checks are distributions: use at least 5 back-to-back runs, apply the threshold to a named statistic, and print the spread.
- **Never read an exit status through a pipe** (`cmd | tail` returns tail's status; capture `rc=$?` directly or `set -o pipefail`). **Avoid `pgrep -f` for job-liveness checks** because it can match the checking command itself; verify the expected process using its PID and start identity, alongside output growth. A background agent's "running" status is a claim about a handle, so check output growth and a start marker. Limit concurrent context-heavy agents according to available resources and avoid competing work during Playwright measurements. Shared scratchpads can compromise blind review, so reviewers get separate input folders.
- Loop shape: build the non-design plumbing, including image assets, art direction, data specification, test suite, and word registry, before the first design iteration. Ship a credible first preview quickly and let the site owner's real-device inspection steer. A regional bakery chain's ordering page can pass automated checks while still placing a key choice awkwardly on a phone. Showing the result at the iteration cap with a decision brief is healthy; scores from different scoring criteria are not a trend.
- Skillbook governance: retire guidance that predicts scores without evidence. A skill whose stated falsification condition occurs is retired as written, and its narrowed form returns as PROVISIONAL. The curator runs every iteration.
- **Resource-intensive jobs**: keep image generation and similar background work separate from browser measurements. Record the execution environment and rerun measurements if competing work could have affected the result.
### V6. Sandboxed helper tools
If you add a sandboxed tool or agent to a build, test the exact command the real run uses and confirm both what it can read and what it can write, because a setting that limits writes may not limit reads.

### V7. Launch, platform choices and foreign-document pages
- On Workers, cutover is a build posture on `main`, not a hand edit. Build guards catch documented-but-unexecuted steps. Set build-trigger variables through the API and watch builds by UUID.
- Sort launch-audit failures into "principled N/A" where passing would require a false claim, and "forgotten step" where required work remains. Document the former and fix the latter.
- Give image-affecting dependency fixes their own commit and prove reproducibility with cold builds that produce byte-identical output. Hold deploy-tool releases for at least 7 days and record the release date and reason for the hold.
- Run the full startup recall for every site. Record each default deliberately not applied and explain why, so reviewers do not restore it unintentionally. Keep each Sanity project's credentials scoped to that project.
- Apply every page check to every page, limiting any marked exemption to the smallest necessary container.
- Read the deployment rules before the first production push. Record checks that did not run instead of implying that they passed.

### V8. Memory capture during a build
- Close each phase with a checkpoint that starts by checking for missing lessons. Tag lessons with `selfheal:client-site-first-build` and `webdev` when storing them, so one query can retrieve the work needed to update the guide. If a tag is introduced mid-thread, add an index note identifying earlier untagged entries.
- At capture, ask whether website maintenance or resource-hub maintenance would encounter the same issue. Tag the lesson for those uses too; build-focused capture can otherwise miss maintenance needs.
- When building a batch-store file from an agent's JSON, assert a minimum content length on every item and normalise mixed list elements (`str | {text}`). This prevents apparently successful imports that store headings with empty lesson bodies.

### Typical open items after a first launch (status to verify at the next run; not facts)
1. Review DMARC reports before moving beyond `p=none`; verify that the accessibility statement reflects the site.
2. Review token rotation needs, including tokens with no expiry.
3. Revisit any held Wrangler upgrade and validate both preview and production build configurations before adopting it.
4. Check whether production 404 responses under `/.well-known/*` lack the intended `X-Robots-Tag`. If needed, fix response handling through Worker routes or an assets not-found rule.
5. Benchmark any live WebGL layer on representative physical devices. Per-device limits remain estimates until measured.
6. Consolidate the skillbook when it exceeds its agreed size limit, using helpful/harmful counters before pruning entries.

---

## FINAL PRE-LIVE DEPLOYMENT GATE (MANDATORY)

Runs AFTER the final ACE Reflector declares SATISFACTORY and BEFORE any push to `main`, the post-run memory update and the hand-off. **NON-NEGOTIABLE.**

**Step 1: Recall the go-live checklist rows** using search phrases covering domain and DNS, search console, backup and recovery, documentation hand-off, transactional email, error tracking, and SEO/AEO. If no stored checklist exists, assemble it from the current site's requirements. Some lessons may describe a different hosting or CMS setup; preserve the requirement and translate its implementation to the current platform.

**Step 2: Walk the checklist** in four quadrants: Infrastructure & Code (repo hygiene, DNS, security headers, backups); Content & Brand (preview review, claims, imagery, privacy disclosures checked against actual behaviour); Site-owner sign-off (explicit); Cutover & post-deploy (Search Console, monitoring, 24 h and 1-week checks). Every box must pass or have an explicit waiver with its reason stored as a memory.

**Step 3: Hard gate.** If any box remains red, HALT, fix it on the preview, re-walk the section, and proceed only on the site owner's explicit go-ahead.

**On Workers**: fast-forward the preview branch into `main`; let the build apply the production configuration. Expect build guards to refuse documented-but-unexecuted steps. Watch the main build by UUID, then run the launch checks described in `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md`. Probe product pages and key journeys, verify that production refuses the Turnstile dummy token, and audit the live site's agent readiness. Separate principled N/A findings from forgotten steps. Check DNS security and discovery configuration, email authentication and reporting, and certificate-authority restrictions in dependency order. Check any printed QR links as qa-032 describes.

**Step 4: Post-cutover.** Store a tracking memory with the cutover time and the 1 h, 24 h and 1-week checks. The next run verifies that they happened.

---

## Above-the-fold media governance

Treat everything competing for the LCP slot (images, animated images, video, WebGL/WebGPU canvas, 3D) as ONE class. Give the LCP image candidate `loading="eager"`, `fetchpriority="high"`, and explicit width and height. For video or canvas, prioritise its static poster or fallback and reserve its layout dimensions. Nothing above the fold lazy-loads, and a live layer never blocks the static design beneath it. Recall the rule to govern above-the-fold media competing for LCP as one class. On a shared preview branch, pull before editing and keep each change to one commit with a clear message.

---

## Conferring with skills and the Council

Every time this automation spawns a design-generator or design-reflector for a **page, a resource page, a resource-page template or a resource card**, inject a conference block into its prompt. Agents do not reliably recall a discipline they were never told to use.

> **CONFER**: Before and during your work, read the entry file for each applicable skill below, apply its discipline, and incorporate its perspective. Ground every product claim in the code or record that serves it, and every outside claim in a fetched source.

| Content type | Confer with (package skills) |
|---|---|
| Website page (hero, product, landing copy) | `design-architect-thinking`, `corporate-graphic-design`, `aeo-optimization`, `agent-readiness-frontier` |
| Page with a live or interactive layer | the `webgl-craft` cluster (renderer and budget, hardening and testing, interaction, light and color, constellations, cosmic art direction) |
| A long scroll story or guided journey page | `scroll-journey` |
| Resource hub, resource page, resource card | `resource-hub-thinking`, `resource-hub-resource-page-builder`, `resource-slug-design-canonical`, `aeo-optimization` |
| Prototype or a new page type | `prototype-website-generation`, `astro-website-page-creation`, `web-app-building` |
| Planning, design decisions, critiques | `fable-planning-cognition` |

**The Council**: use the review process in `04_reasoning/commands/inner-council.md` when a dimension stays below 9.8 and the root cause is unclear, for a pivotal architectural decision, and before adopting a new agent-readiness or platform standard. Read the participating skills, consider each perspective in turn, synthesize the findings, and record the decision as a memory.

---

## Frontier Version Check (two-tier)

**Tier 1: cheap, every run.** Compare installed versions with npm-latest for the shared dependency list (`astro`, `@astrojs/sitemap`, `@tailwindcss/vite`, `tailwindcss`, `wrangler`, `typescript`, plus `@sanity/client` in hub modes). Compare Astro's `engines.node` requirement with the project's pinned Node version and the version selected by the build host. Report IN-SYNC or list mismatches.

```bash
for p in astro @astrojs/sitemap @tailwindcss/vite tailwindcss wrangler typescript; do
  printf '%s latest %s\n' "$p" "$(npm view "$p" version)"
done
npm pkg get dependencies devDependencies
```

**Tier 2: on mismatch only.** Research the upgrade using official migration notes. Store what you learned as self-contained memories with source URLs, search the scaffold for affected patterns, upgrade BEFORE design work, and prove a clean production build passes. Hold deploy-tool releases younger than 7 days.

---

## ACE Loop Refinements

**(a) CURATOR EVERY ITERATION.** Prefer Generator, then Reflector, then Curator, every iteration, and once more at close. The curator catches measurement traps before the next iteration relies on misleading results. Examples include a full-page capture that hides a sticky-layer failure, a coverage threshold distorted by viewport shape, and interactions between findings that individual reviewers miss. Keep each pass small: capture only changes arising from that iteration's reflection.

**(b) PAIRED REFLECTORS**: run as many reflectors as generators, with one tightly scoped reflector per generator slice. Each reflector audits ALL files for its assigned fix pattern. Then run ONE final whole-site cross-page review.

**(c) DIST ISOLATION**: the orchestrator builds the distribution ONCE. Each reflector serves that same output READ-ONLY on its own port and never rebuilds it. This prevents shared-port rebuild races from producing false alarms.

---

## Alternative platform: Vercel (short note)

A site can live on Vercel instead. Account and project setup are covered in `09_guides/DEPLOY_VERCEL.md`. Configure preview deployments for non-production branches and use Vercel Deployment Protection when previews show unreleased work. Protect previews through robots meta directives, crawler rules, and platform authentication; verify their combined behaviour because authentication can prevent crawlers from seeing page directives. Configure redirects through Vercel's supported project configuration, or middleware when appropriate for the rule count. Verify the current protection setting that keeps the custom production domain public while restricting previews. Record platform-specific lessons in the recall map and skillbook. Everything else in this guide, including the ACE loop, agent readiness, deployment checks, and operating rules, applies across platforms.

---

## Mandatory Post-Run Self-Heal Protocol (DO THIS AT THE END)

At startup, stored lessons inform the guide. At the end, the run updates both the lesson store and the guide, so the next run starts with better instructions. **NON-NEGOTIABLE.**

1. **Store dual-layer memories** for every lesson as the run progresses: `[OBJECTIVE] what happened, the command, the measurement ... [SUBJECTIVE/WHY] why it matters, what was confusing, what to do next time`. Use the tags `selfheal:client-site-first-build`, `webdev`, and the topic. Use your chosen store's batch import when available, validate every item, and follow its supported importance scale and categories.
2. **List this run's memories** using phrases drawn from the run's own words, or retrieve them by tag. Check that the stored entries contain the actual lessons.
3. **Update this automation's maps with search phrases, never IDs**: for each new memory that belongs on the map, write a row (Trigger | Recall phrase | What you get | Skill/appendix). Pick 3-8 words that appear in the memory and that a stranger would type. Verify that the phrase returns the memory in the top 5 results, then add it to `05_automations/client-site-first-build/recall_phrases.json`. Fix or remove any phrase that no longer retrieves its intended memory.
4. **Update the curator log** in `05_automations/client-site-first-build/skillbook.md` with one entry for the run.
5. **Store a "post-run self-heal complete" memory** containing the run identifier, memories stored, rows added, and anything deliberately skipped with its reason.

Keep two maintained surfaces: the lesson store and this automation's shipped documentation. Avoid creating additional copies that can drift.

**Escape hatch**: a memory can stay off the map if it is site-specific trivia with no future use, a one-off debug note, or a duplicate. Record that decision in the post-run completion memory.
