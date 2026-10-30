# Web tools

Small command-line helpers for building and running your own sites on Cloudflare (and, for the preview watcher, any
host). They all use YOUR accounts and YOUR keys. Nothing in this folder knows about any other person's site.

After `bash bin/install_skills.sh` they live in `~/.local/share/webdev-workbench/web_tools/`. Call them with `bash` or
`python3` exactly as shown below (unzipping drops the "executable" mark, so never run them as `./name`).

## Your key file

Every tool that needs a credential reads it from one file:

```
~/.config/webtools/keys.env
```

Create it once, readable by you only:

```bash
mkdir -p ~/.config/webtools && touch ~/.config/webtools/keys.env && chmod 600 ~/.config/webtools/keys.env
```

Then open it in a text editor and add one `NAME=value` line per key you have. Lines starting with `#` are comments.
Never paste a key into a chat, a commit or a command line.

| Key name | Needed by | Where it comes from |
|---|---|---|
| `CLOUDFLARE_API_TOKEN` | cf-api, wrangler-safe, forms-check, builds_watch.py | a Cloudflare API token you create (see the Cloudflare deploy guide) |
| `CLOUDFLARE_ACCOUNT_ID` | wrangler-safe, forms-check, builds_watch.py, cf-api paths with `{account}` | your Cloudflare dashboard, account home page |
| `CLOUDFLARE_ZONE_ID` | cf-api paths with `{zone}` (optional) | your domain's overview page in Cloudflare |
| `CF_ACCESS_CLIENT_ID`, `CF_ACCESS_CLIENT_SECRET` | preview_url_watch.py (optional) | only if your previews sit behind Cloudflare Access: a service token |
| `SANITY_API_TOKEN` | bearer-curl, for the Sanity HTTP API (optional) | your Sanity project, API settings |
| `DEPLOY_HOOK_URL` | the resource-hub automation's rebuild step (optional) | a Workers Builds or Vercel deploy hook you create; the URL itself is the secret |

How the tools treat the file (this is enforced in `webtools-lib.sh` and `webtools_keys.py`):

- It is **parsed** line by line, never sourced or executed, so nothing written in it can run.
- It must be a regular file you own with mode 600 (or 400); otherwise the tools stop and tell you the `chmod` to run.
- **No value is ever printed.** Banners show only the last four characters of an account id. Tokens reach `curl` on
  its standard input (`curl -K -`) or are sent from inside Python, so they never appear in a command line or the
  process list.
- `WEBTOOLS_KEYS=/other/path` points the tools at a different file with the same rules.

The Cloudflare guide (`~/.local/share/webdev-workbench/guides/DEPLOY_CLOUDFLARE.md`, in the package
`09_guides/DEPLOY_CLOUDFLARE.md`) shows how to create the token with the right permissions. If you prefer, plain
`npx wrangler login` also works for wrangler; these tools exist for the cases where a stored token is better
(scripts, watchers, a shell that already holds another account's variables).

## The tools

| Tool | What it does | Keys it reads | Example |
|---|---|---|---|
| `cf-api` | One Cloudflare API call; prints the JSON answer. `{account}` and `{zone}` in the path are filled in from your keys. | `CLOUDFLARE_API_TOKEN`, plus `CLOUDFLARE_ACCOUNT_ID` / `CLOUDFLARE_ZONE_ID` when the path uses them | `bash ~/.local/share/webdev-workbench/web_tools/cf-api GET /user/tokens/verify` |
| `wrangler-safe` | Runs wrangler for your account only: drops stray `CLOUDFLARE_*`/`CF_*` variables, refuses when `wrangler.jsonc` pins a different account, refuses `deploy` of a build that contains `dist/.preview-build` | `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` | `bash ~/.local/share/webdev-workbench/web_tools/wrangler-safe deploy --dry-run` |
| `bearer-curl` | curl with `Authorization: Bearer <one of your keys>`, for any API that uses bearer tokens (Sanity, for example) | the key you name | `bash ~/.local/share/webdev-workbench/web_tools/bearer-curl SANITY_API_TOKEN "https://<your-sanity-project-id>.api.sanity.io/v2025-02-19/data/query/production?query=count(*)"` |
| `forms-check` | Looks after form submissions stored in a Cloudflare D1 database: tables, counts, newest rows, CSV export, and deleting one person's rows on request. Starts `forms_check.py`. Run it from your site's repository folder. | through wrangler-safe | `bash ~/.local/share/webdev-workbench/web_tools/forms-check --db <your-d1-db> summary` |
| `builds_watch.py` | Watches Cloudflare Workers Builds for one commit until it finishes. Exit 0 success, 1 failed, 2 timeout, 3 Worker not found, 4 API error (most often a token without the Account > Workers Builds Configuration > Edit row; see the Cloudflare deploy guide, Step 10). | `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` | `python3 ~/.local/share/webdev-workbench/web_tools/builds_watch.py --worker <your-worker> --commit <sha7> --branch preview` |
| `preview_url_watch.py` | Polls a preview URL until a page that changed answers 200 and contains a marker only the new build has. Does not follow redirects, so a login wall shows as 302. Exit 0 live, 2 timeout. | `CF_ACCESS_CLIENT_ID`, `CF_ACCESS_CLIENT_SECRET` (only if present) | `python3 ~/.local/share/webdev-workbench/web_tools/preview_url_watch.py --url https://<preview-host> --probe /about --marker 'Open on Sundays'` |

Support files: `webtools-lib.sh` (shared bash helpers, loaded by the bash tools), `webtools_keys.py` (the same key
rules for the Python tools), `forms_check.py` (the program behind `forms-check`).

Every tool prints its usage when run with no arguments or `--help`.

## Notes and limits

- Cloudflare API paths, field names and token permission names are as of October 2026; re-check before relying on them.
- `forms-check delete-email` only reaches tables that have an `email` column. It lists the other tables so you can
  check them for linked rows yourself. It counts first and deletes only with `--yes`.
- `wrangler-safe` uses the project's own wrangler (`node_modules/.bin/wrangler`) when installed, otherwise
  `npx --yes wrangler@4`.
- All tools need `bash` (3.2 or later is fine), `python3` 3.8 or later, and `curl`.

## Dropped from the previous edition, and why

- **The `cf` CLI pass-through** (the old Cloudflare wrapper could also run a third-party `cf` CLI): dropped, because
  that CLI is not something a new reader has or needs; `cf-api` and `wrangler-safe` cover the same ground with
  public tools.
- **The cwd guard** (refusing to run outside one fixed site folder): dropped, because it depended on one person's
  folder layout. The account-pin check in `wrangler-safe` is the guard that matters.
- **The site-specific forms report** (fixed table names, a "how did you hear about us" report): replaced by the
  generic `forms-check`, which discovers your tables instead of assuming them.
