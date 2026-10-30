# Resource hub registry (generic edition)

> Track the resource hubs you maintain. Add one row per site that has a hub. Record secrets
> by **name and location** (for example "`SANITY_API_TOKEN` in the deployment platform's secret store"), never by value.

| Site | Hub status | Platform | Repo | Branches | Sanity | Forms | Previews | Deploy trigger |
|---|---|---|---|---|---|---|---|---|
| *EXAMPLE, delete this row:* `willowspade.example` | stub: Sanity project exists, no how-to hub routes yet | `cloudflare-workers` (static assets + Workers Builds) | `<your-github-user>/garden-howto-site` | `main` = production, `preview` + feature branches = preview deployments | dataset `production`, public-read; project ID in the site's Sanity configuration | the shop's own contact form | public-by-URL preview links | code: push; CMS: deploy hook (`DEPLOY_HOOK_URL` in the CMS integration's secret store) |

Platform values: `cloudflare-workers`, `cloudflare-pages`, `vercel`. Previews values: `public-by-URL`,
`Cloudflare Access`, `Vercel Deployment Protection`.

## Stack notes (one block per site)

Write the site's framework and versions, the Node pin, where its keys live (by name), and anything a redeploy
must know (for example "on-request detail routes need the Cloudflare adapter").

## Decisions log (append as they are made)

| Date | Site | Decision | Why | Memory stored? |
|---|---|---|---|---|

## Audit log (one line per maintenance run)

| Date | Site | Run | What changed | Commit | Build/Deploy | Checks (Lighthouse / axe / slug loop) |
|---|---|---|---|---|---|---|
