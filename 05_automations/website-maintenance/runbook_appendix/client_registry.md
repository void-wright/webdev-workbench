# Website Maintenance: Site Registry (generic edition)

> Sites maintained by you or your small team. Add a row after a first build; update rows as sites change and never delete them (mark `retired`).
>
> **Read this file on EVERY startup.** The repo is the final word on platform. Follow `05_automations/website-maintenance/runbook_appendix/platform_detection.md`.

This registry ships with no real sites. The single row below is an INVENTED EXAMPLE that shows the shape; replace it with your own site, or delete it once your first real row exists.

| Slug | Display name | Repo | Platform | Worker(s) | Branches | Preview link + lock | Forms data | Deploy status | Indexing | Mode |
|------|--------------|------|----------|-----------|----------|---------------------|------------|---------------|----------|------|
| hearthlane-bakery | EXAMPLE ONLY: Hearthlane regional bakery chain | github.com/<your-github-user>/<your-repo> (private) | cloudflare-workers | `<your-worker>` (site + `/api/*`) | `main` = production (Workers Builds: `npm run build` then `npx wrangler deploy`); `preview` + any other branch = a Worker Preview (`npx wrangler preview`) | `https://<your-preview-host>` (the branch alias from the dashboard); optional Cloudflare Access, scope Previews only | D1 `<your-d1-db>` (production) / `<your-d1-db>-preview` (previews); Turnstile fail-closed | live (https://<your-domain>) | indexed (production posture applied by the build on main; workers-dot-dev previews forced noindex) | website |

Keep each site's local checkout clearly associated with its registry row. Store credentials in your own key file with mode 600, parsed by the web tools, never sourced. See `09_guides/keys.env.example` for the configuration format. Account, zone and service-token identifiers are not written here; read them from your dashboard or your key file when a command needs them, and never paste them into this folder.

## Schema

| Column | Meaning |
|--------|---------|
| Slug | Lowercase, hyphenated identifier |
| Display name | Human-readable name |
| Repo | Git remote |
| Platform | `cloudflare-workers` (primary) / `cloudflare-pages` / `vercel` |
| Worker(s) | Worker script names (Workers sites) or project name (Pages/Vercel) |
| Branches | Which branch is production and how previews are made |
| Preview link + lock | Stable preview URL and what protects it (nothing, Cloudflare Access, or Vercel Deployment Protection) |
| Forms data | Databases and services that hold or send form data |
| Deploy status | `preview` / `live` / `retired` |
| Indexing | `noindex` / `indexed` (and how the posture is applied) |
| Mode | `website` / `resource-hub` / `combined` |

## Operational Notes

- **Reading a row (every startup)**: platform tells you which commands to use; branches tell you where to push; preview lock tells you how to probe; forms data tells you which database a test may touch (previews only).
- **Updating a row**: keep it internally consistent; optionally note the last production commit and date.
- **Changes across your sites**: use this file to identify the affected sites and their deployment settings; read it first and update it last. Confirm platform details against each repo before acting.

## Anti-Patterns

- ❌ Maintaining a site not in this registry: complete its first build and register it before ongoing maintenance.
- ❌ Writing account IDs, tokens, emails or service-token values into this file.
- ❌ Deleting a real site's row: mark `retired` instead.
