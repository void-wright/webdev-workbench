# EDITION NOTES: website-maintenance, generic edition

## What this edition is

A website-maintenance automation for **anyone looking after their own live sites**, on **their own** GitHub, Cloudflare or Vercel accounts. The automation preserves a careful, evidence-led approach: ACE loops at 9.8/10 HARD with a curator every iteration, empirical Lighthouse and axe checks, preview-first changes, verification of deployed output, agent-readiness re-scans, and checks that confirm testing tools actually detect failures.

Examples are invented and unrelated to any existing business. The site registry contains no configured sites, only an illustrative row for a fictional regional bakery chain.

## What changed from the previous edition (by category)

| Category | Previous edition | This edition |
|---|---|---|
| Audience | a site-specific maintenance workflow | anyone maintaining their own sites |
| Site specifics | fixed repository and hosting configuration | placeholders (`<your-site-repo>`, `<your-github-user>/<your-repo>`, `<your-domain>`, `<your-worker>`, `<your-d1-db>`, `<your-preview-host>`) and invented examples |
| Decisions | context-dependent instructions | stated as rules with their reasons ("Prefer X, because Y"); record your own sign-off |
| Previews | protection assumed | optional protection (Cloudflare Access or Vercel Deployment Protection); checks that need a token say "only if previews are protected" |
| Credentials | environment-specific credential handling | a key file you control (mode 600), parsed by the package's web tools, never sourced and never printed |
| Deploy steps | account-specific setup | package guides: `09_guides/GITHUB_SETUP.md`, `09_guides/DEPLOY_CLOUDFLARE.md`, and `09_guides/DEPLOY_VERCEL.md` |
| Memory map | environment-dependent lookup references | search phrases in `05_automations/website-maintenance/recall_phrases.json`, using `{phrase, row}` entries |
| Skillbook | context-dependent evidence | same rules and skill IDs; evidence and reasons stated in general terms |
| Guide | site-specific maintenance records | an "Open items (yours to keep)" section and an empty self-heal log |

## Files

Paths below are relative to the package root.

| File | Status |
|---|---|
| `05_automations/website-maintenance/comprehensive_guide.md` | rewritten for the generic edition, preserving the operating principles |
| `05_automations/website-maintenance/skillbook.md` | same structure and skill IDs; examples generalised and references updated |
| `05_automations/website-maintenance/personality.json` | careful maintenance voice preserved; stack, boundaries, modes and edition note made generic |
| `05_automations/website-maintenance/setup_instructions.md` | setup for your own repository, key file, optional preview protection and package tools |
| `05_automations/website-maintenance/startup_queries.json` | startup search phrases for web-maintenance topics |
| `05_automations/website-maintenance/recall_phrases.json` | search phrases paired with the rows they serve |
| `05_automations/website-maintenance/runbook_appendix/client_registry.md` | no configured sites; one invented example row |
| `05_automations/website-maintenance/runbook_appendix/platform_detection.md` | Workers primary, Pages and Vercel alternatives, generic operations |
| `05_automations/website-maintenance/runbook_appendix/cloudflare_maintenance_ops.md` | Workers post-launch operations through the package's web tools |
| `05_automations/website-maintenance/runbook_appendix/promote_to_production.md` | preview-to-main promotion and rollback |
| `05_automations/website-maintenance/runbook_appendix/in_browser_compute_module.md` | reusable rules for browser-based calculations |

## Tools this edition expects

Use `bin/install_skills.sh` for package installation. The web tools ship under `06_web_tools/`:

- `bash 06_web_tools/cf-api <METHOD> <path> [json-body]`: Cloudflare API calls (`{account}` and `{zone}` filled from your key file).
- `bash 06_web_tools/wrangler-safe <wrangler args>`: Wrangler with your token; clears conflicting account variables and refuses an `account_id` pin mismatch.
- `bash 06_web_tools/forms-check --db <your-d1-db> <command>`: read, export and privacy-delete form rows in a D1 database.
- `bash 06_web_tools/bearer-curl <KEY_NAME> <curl args>`: Bearer-token API calls without putting the token on the command line.
- `python3 06_web_tools/builds_watch.py` and `python3 06_web_tools/preview_url_watch.py`: build and preview watchers.

Also provide Node 22.12+, Git with your GitHub login, Playwright with its bundled Chromium, Lighthouse, gitleaks and pre-commit. Use the package's memory files and ordinary text search for recall.

## Not available here, and what to use instead

| Not available | Use instead |
|---|---|
| A hosted knowledge service | the package's documentation, memory files and your own maintenance notes |
| A preconfigured content account | the Sanity HTTP API with your own token (`bash 06_web_tools/bearer-curl SANITY_API_TOKEN ...`) and your own content sources |
| An external approval service | record sign-off in your own notes or commit messages |
| An external review service | the design agent definitions under `05_automations/agents/` and the review guidance in `04_reasoning/commands/inner-council.md` |
| An additional specialist library | the shipped skills and Council guidance |
| A managed hosting or Git account | your own GitHub, Cloudflare or Vercel account |

## About the recall phrases

The phrases in `05_automations/website-maintenance/recall_phrases.json` and `05_automations/website-maintenance/startup_queries.json` are **search terms** written in web-craft vocabulary. This edition does **not** claim each phrase was verified against this package's memory pack. If a phrase returns nothing useful, search with the topic words in the row's "What you get" column. When you find the relevant entry, replace the phrase with wording that retrieves it.
