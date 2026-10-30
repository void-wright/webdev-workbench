# EDITION NOTES: client-site-first-build (generic edition)

## What this edition is

A first-build automation for anyone building their own business site or resource library with Voidwright. Work runs on your machine, using your GitHub account and your Cloudflare or Vercel account. Examples use invented businesses and placeholders for account details.

The worked path is **Cloudflare Workers + Workers Builds + GitHub**: `main` deploys production, and other branches provide Worker Previews when preview builds are configured. Protecting previews with Cloudflare Access is optional; prefer it for unreleased work. Vercel is a documented alternative.

This edition focuses on reusable web craft: preparing inputs, building pages, reviewing the result, deploying safely and maintaining a useful handoff.

## What changed from the previous edition

- **Examples and placeholders.** Examples use an invented kitchen-equipment maker's resource library, a bicycle-parts company's guides, a garden-supply shop's how-to hub, a ceramic studio and a regional bakery chain. Account details use placeholders such as `<your-site-repo>`, `<your-github-user>`, `<your-worker>` and `<your-workers-subdomain>`.
- **Rules include reasons.** Review each iteration to catch regressions early. Use deliberate merge checks when branch protection is unavailable. Approve final copy before publishing so draft wording does not become a public claim.
- **Preview protection is optional.** Checks that depend on Cloudflare Access apply only when previews are protected.
- **Credentials.** Keep credentials in a file you control with mode `600`. Tools should parse that file, never source it or print its contents. Alternatively, use `npx wrangler login`. See `09_guides/keys.env.example` for the supplied configuration example.
- **Tools.** The package supplies `06_web_tools/wrangler-safe`, `06_web_tools/cf-api`, `06_web_tools/bearer-curl`, `06_web_tools/builds_watch.py` and `06_web_tools/preview_url_watch.py`.
- **Account setup is linked, not repeated.** Use `09_guides/GITHUB_SETUP.md`, `09_guides/DEPLOY_CLOUDFLARE.md` and `09_guides/DEPLOY_VERCEL.md`.
- **Folders.** Choose local working directories for inputs and port archives. Keep temporary build and review work out of version control. Keep the automation instructions separate from generated site files.
- **Memory references.** Recall phrases use generic web-craft vocabulary. Search the supplied memory pack with those phrases and verify the results. The automation's phrase map is `05_automations/client-site-first-build/recall_phrases.json`, with entries containing `phrase` and `row` fields.
- **Doctrine.** Build guidance states reusable rules and explains their purpose. Post-launch follow-up covers typical unfinished tasks, such as checking redirects, confirming form delivery and resolving content gaps.
- **Code fixes.** Command examples need intact call syntax and separators. A method reference such as `.strip` does not perform the work of `.strip()`. Check repaired examples for valid syntax and working behavior, including axe checks. Deployment verification must inspect the target platform's actual headers and indexing controls.
- **Skillbook**: examples are generic and entry IDs remain stable. See `05_automations/client-site-first-build/skillbook.md`.
- **Persona** (`05_automations/client-site-first-build/personality.json`): the role supports clear explanations, careful review and explicit boundaries. Repository details and preview-protection settings belong in project configuration.

## Not available here (and what to use instead)

- For a second perspective on a build, use the supplied design reflector and the review guidance in `04_reasoning/commands/inner-council.md`. Stop when the required checks pass and no material issue remains.
- For writing and review, use the active agent and inspect the resulting changes. A separate writer service is not required.
- For specialist guidance, use the shipped design, graphic-design, AEO, agent-readiness, WebGL, scroll-journey and resource-hub skills.
- Keep project knowledge in the supplied memory pack, project documentation and your repository. Connect additional content systems only when your site needs them.
- Use GitHub repositories and deployment accounts that you control.

## Tools this edition expects

- Access to the supplied memory pack in `02_memory/webdev_pack.json`. Use `02_memory/run_battery.py` with `02_memory/recall_battery.json` to check recall behavior.
- Node 22, npm, Python 3.10+, git, `gh`, gitleaks, pre-commit, Playwright with Chromium, Lighthouse and axe-core.
- `npx wrangler`, authenticated through login or the supplied `06_web_tools/wrangler-safe` wrapper.
- The tools documented in `06_web_tools/README.md` and the agent definitions in `05_automations/agents/design-generator.md`, `05_automations/agents/design-reflector.md` and `05_automations/agents/design-curator.md`.
- For ports: `cdx-toolkit`, `scrapy` and access to the site's Google Search Console property when search data is needed.

## About the recall phrases

The phrases in the memory map, `05_automations/client-site-first-build/startup_queries.json` and `05_automations/client-site-first-build/recall_phrases.json` use the vocabulary of the web-craft memory pack. Treat them as search terms, not guaranteed matches. With keyword-only search, a phrase can return nothing when a required word is absent from the stored text. Remove unnecessary words or search using the terms in the map's "What you get" column. Before adding a phrase to the map, verify that it retrieves the intended guidance.

## Files

- **Core instructions**: `05_automations/client-site-first-build/comprehensive_guide.md`, `05_automations/client-site-first-build/setup_instructions.md` and `05_automations/client-site-first-build/EDITION_NOTES.md`.
- **Build and handoff guidance**: `05_automations/client-site-first-build/runbook_appendix/ace_loop_astro_build.md`, `05_automations/client-site-first-build/runbook_appendix/asset_placement.md`, `05_automations/client-site-first-build/runbook_appendix/cross_automation_handoff.md`, `05_automations/client-site-first-build/runbook_appendix/dns_cutover_pause.md`, `05_automations/client-site-first-build/runbook_appendix/redirect_application.md`, `05_automations/client-site-first-build/runbook_appendix/sanity_org_setup.md` and `05_automations/client-site-first-build/runbook_appendix/zip_handoff.md`.
- **Configuration and review**: `05_automations/client-site-first-build/personality.json`, `05_automations/client-site-first-build/startup_queries.json` and `05_automations/client-site-first-build/_gate/GATE.md`. The gate document is a draft, not an executable check.
- **Deployment and port guidance**: `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md`, `05_automations/client-site-first-build/runbook_appendix/backlink_discovery.md`, `05_automations/client-site-first-build/runbook_appendix/build_mode_decision.md`, `05_automations/client-site-first-build/runbook_appendix/gsc_export_pause.md`, `05_automations/client-site-first-build/runbook_appendix/in_browser_compute_module.md`, `05_automations/client-site-first-build/runbook_appendix/old_website_archive.md` and `05_automations/client-site-first-build/runbook_appendix/redirect_authoring.md`.
- **Recall phrases**: `05_automations/client-site-first-build/recall_phrases.json`.
- **Skillbook**: `05_automations/client-site-first-build/skillbook.md`.
