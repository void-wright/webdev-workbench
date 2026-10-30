# Website Maintenance: Platform Detection (generic edition)

> Determine the platform BEFORE picking deploy verbs, secret commands or domain steps.

## Decision Tree

```
1. Read 05_automations/website-maintenance/runbook_appendix/client_registry.md and find the site's row.
2. Read its Platform column:
   ├── cloudflare-workers → Section A (PRIMARY)
   ├── cloudflare-pages   → Section B (alternative)
   ├── vercel             → Section C (alternative)
   └── absent             → STOP: identify and register the platform before maintenance
3. Confirm from the repo (below) before running any verb.
```

**Confirm from the repo, not only the registry** (Pages and Workers both use `wrangler`): a Workers site has a Wrangler configuration with `main` (a Worker entry) and/or an `assets` block, deploys with `npx wrangler deploy`, and has no `pages_build_output_dir`. A Pages site uses Pages deployment settings, often including `pages_build_output_dir` or Pages Functions, and deploys with `wrangler pages deploy`. A Vercel site has Vercel project configuration or a local project link. Confirm these clues against the connected hosting project and its build settings.

## Section A: Cloudflare Workers (PRIMARY)

Workers Builds connected to your GitHub repo; static assets plus a Worker entry. Account setup: `09_guides/DEPLOY_CLOUDFLARE.md`.

Verbs (your own token through `06_web_tools/wrangler-safe`, or `npx wrangler login`; `account_id` pinned in the repo). Run the following from the package root with `WT=./06_web_tools`:

- **Preview**: push `preview` (or another configured branch); Workers Builds runs `npx wrangler preview` when Worker Previews and the Wrangler `previews` block are configured. Watch it by polling the preview URL for a marker absent from the previous build (`python3 "$WT/preview_url_watch.py"`).
- **Production**: after the checks, fast-forward `main` (`git push origin preview:main`); the single main trigger runs `npm run build` then `npx wrangler deploy`. Configure the build to apply production indexing, site-URL and access settings. Watch the build by UUID (`bash "$WT/cf-api" GET '/accounts/{account}/builds/builds/<build_uuid>'`).
- **Rollback**: `bash "$WT/wrangler-safe" deployments list`, then `bash "$WT/wrangler-safe" rollback <version-id> --message "<why>"`, then revert on main through preview. See `05_automations/website-maintenance/runbook_appendix/promote_to_production.md`.
- **Secrets**: production `bash "$WT/wrangler-safe" secret put <NAME>`; preview secrets belong in the preview base configuration and must exist BEFORE a preview is created.
- **D1**: `npx wrangler d1 migrations apply <your-d1-db> --local`, then apply with `--remote` through `wrangler-safe`, before any deploy that requires the migration. Migrate the preview D1 through a temporary configuration naming only that database.
- **DNS / zone**: use the Cloudflare API through `bash "$WT/cf-api"` for DNS records and zone settings. Verify with DNS-over-HTTPS JSON when `dig` is absent; inspect the AD flag when checking DNSSEC validation. Read before you write, and change a zone only as part of an intended DNS change.
- **Local dev**: `npx wrangler dev --local-upstream localhost` when local behavior depends on the request host; otherwise the Worker may interpret requests as serving production.

Detail: `05_automations/website-maintenance/runbook_appendix/cloudflare_maintenance_ops.md` and `09_guides/DEPLOY_CLOUDFLARE.md`.

## Section B: Cloudflare Pages (alternative, short)

With Git integration configured, pushing to the production branch auto-deploys. Manual deployment: `npx wrangler pages deploy dist --project-name <project> --branch main`; secrets: `npx wrangler pages secret put <NAME> --project-name <project>`; logs: `npx wrangler pages deployment tail --project-name <project>`; local development: `npx wrangler pages dev dist`.

## Section C: Vercel (alternative, short)

Preview deployments per branch (optionally behind Vercel Deployment Protection); production by merging to the configured production branch or running `vercel deploy --prod`; environment variables: `vercel env add <NAME> <environment>`; rollback: `vercel rollback`. On a first go-live, explicitly check and update noindex, robots, site-URL and protection settings unless the project automates them. Account setup: `09_guides/DEPLOY_VERCEL.md`.

## Mixed operations

- DNS may live at Cloudflare, Vercel or your registrar; the registry row and the dashboard say which.
- Git is platform-agnostic: use your own GitHub credentials, push to `preview` (or a feature branch), and never force-push `main`.
- Lighthouse, axe and Playwright are platform-agnostic.

## Anti-Patterns

- ❌ Pages verbs on a Workers site, or treating the Workers Builds `/builds` listing as proof a preview deployed. Verify the preview URL itself; the production build listing is not preview evidence.
- ❌ Vercel verbs on a Cloudflare site, or the reverse.
- ❌ Skipping the registry and repo checks at startup.
- ❌ Running any command for the site in a shell whose exported token belongs to a different account. Use `06_web_tools/wrangler-safe` to scrub conflicting token variables.
