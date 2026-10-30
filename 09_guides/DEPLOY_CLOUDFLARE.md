# Deploy an Astro site on Cloudflare

## What you will have at the end

- A live website for the invented Crumb & Crust Bakery.
- Automatic publishing when you update your approved code.
- A preview address for reviewing each proposed change.
- Optional sign-in protection and your own domain.
- A way to restore an earlier version.

## Before you start

Allow two to three hours, plus any time needed for domain changes.

You need an email address and accounts for Cloudflare and GitHub.
You can create the hosting account in Step 1.
A domain, the address you buy for a website, is optional.

Have Git, Node.js, npm, Python 3 and curl installed.
Git records changes. Node.js runs JavaScript tools. npm installs project packages.
curl checks web responses from your terminal.
The optional `gh` tool is GitHub's command-line interface (as of October 2026; re-check before relying on it). See [GitHub CLI](https://cli.github.com/manual/).

Complete Section A of [SERVICES.md](SERVICES.md) before any authenticated command.
It installs the helper at `~/.config/webtools/with_keys.py`.
Your only local key file is `~/.config/webtools/keys.env`, with mode `600`, meaning only your user can read or write it.
Never print, copy or `source` that file. Never send its contents to an AI or commit it to Git.

Ask your agent to edit site files and explain errors.
Enter credentials yourself, in your own terminal, private editor or the hosting platform's secret store.

**In your own terminal:** check your tools:

```bash
git --version
node --version
npm --version
python3 --version
curl --version
```

Stop and finish tool installation if any command is missing.
In examples, replace text inside angle brackets, including the brackets, with your own value.
Keep the surrounding quotes in commands.

This guide uses Workers with static assets, meaning files served without generating each page on demand, and Workers Builds, the Git integration that publishes changes (as of October 2026; re-check before relying on it). See [static assets](https://developers.cloudflare.com/workers/static-assets/) and [Builds](https://developers.cloudflare.com/workers/ci-cd/builds/).
Cloudflare Pages still works, but Cloudflare steers new projects to Workers and adds new features there (as of October 2026; re-check before relying on it). See [Pages migration](https://developers.cloudflare.com/workers/static-assets/migration-guides/migrate-from-pages/).

## 1. Create and secure your account

**In your browser:** open [dash.cloudflare.com](https://dash.cloudflare.com/), sign up, verify your email and enable two-factor authentication, which adds a second check at login (as of October 2026; re-check before relying on it). See [account documentation](https://developers.cloudflare.com/fundamentals/).

Save recovery codes somewhere private.
Do not give them to your agent.

**In your browser:** find your Account ID in the Workers & Pages overview, often in the right-hand column, or in Account home (as of October 2026; re-check before relying on it). See [finding account IDs](https://developers.cloudflare.com/fundamentals/account/find-account-and-zone-ids/).

An Account ID identifies your account. It is not a secret.
Enter it yourself under `CLOUDFLARE_ACCOUNT_ID` in the private key file described in SERVICES.md.
Do not put it in chat.

**Check:** your email is verified, two-factor authentication is enabled and you know which account you will use.

## 2. Set spending boundaries before deploying

Stay on the Workers Free plan while learning. It is enough for this starter site (as of October 2026; re-check before relying on it). See [pricing](https://developers.cloudflare.com/workers/platform/pricing/).
Do not add a payment method you do not need.

On Free, exceeding the daily Worker request limit makes affected requests fail instead of creating usage charges. Static asset requests are free (as of October 2026; re-check before relying on it). See [pricing](https://developers.cloudflare.com/workers/platform/pricing/) and [limits](https://developers.cloudflare.com/workers/platform/limits/).
Builds also have their own usage limits (as of October 2026; re-check before relying on it). See [Builds limits](https://developers.cloudflare.com/workers/ci-cd/builds/limits-and-pricing/).

**In your browser:** if you later choose Workers Paid, first open Manage Account > Notifications and configure “Usage-based billing” notifications (as of October 2026; re-check before relying on it). See [billing notifications](https://developers.cloudflare.com/billing/).
A notification warns you. Do not treat it as a spending cap.

**Check:** the Workers subscription says Free. If upgrading later, confirm notification delivery before deploying on Paid.

## 3. Prepare the bakery site

A repository, often shortened to repo, is a project folder with recorded changes.
Run the creation command from the folder where you keep projects.
If you already have the bakery project, enter its folder and skip creation.

**In your own terminal:**

```bash
npm create astro@latest bakery-site
cd bakery-site
```

Choose a simple starter template. Agree to install dependencies, the packages the project needs, and initialize Git.
The setup prompts and supported Node versions can change (as of October 2026; re-check before relying on it). See [Astro installation](https://docs.astro.build/en/install-and-setup/).
If the installer rejects your Node version, install a supported version before continuing.

**In your own terminal:** install Wrangler, the deployment tool, record your actual Node version and build:

```bash
npm install --save-dev --save-exact wrangler@4
node -p 'process.versions.node' > .nvmrc
npm run build
```

Astro's static build writes the publishable site to `dist/` (as of October 2026; re-check before relying on it). See [Astro deployment](https://docs.astro.build/en/guides/deploy/cloudflare/).
Workers Builds reads `.nvmrc` to select Node (as of October 2026; re-check before relying on it). See [build environment](https://developers.cloudflare.com/workers/ci-cd/builds/build-image/).
Commit `.nvmrc`, `package.json` and `package-lock.json` so local and hosted builds use recorded versions.

Ask your agent to create `wrangler.jsonc` in the repository root, the folder containing `package.json`.
JSONC is a settings format that permits comments.
Enter the Account ID yourself. Replace the date placeholder with today's date in `YYYY-MM-DD` form.
This non-secret identifier is also pinned in configuration to make the intended account explicit.

```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "bakery-site",
  "compatibility_date": "<today's date, YYYY-MM-DD>",
  "account_id": "<your Account ID>",
  "workers_dev": true,
  "preview_urls": true,
  "assets": {
    "directory": "./dist",
    "not_found_handling": "404-page"
  }
}
```

These settings have the following meanings (as of October 2026; re-check before relying on it). See [Wrangler configuration](https://developers.cloudflare.com/workers/wrangler/configuration/).

- `$schema` lets your editor check the file.
- `name` identifies the Worker. Keep the dashboard name identical.
- `compatibility_date` selects the platform behavior your site expects.
- `account_id` pins the intended account. A token for another account should fail rather than silently choose a destination.
- `workers_dev` enables the platform's public address.
- `preview_urls` explicitly enables version-review URLs. Step 6 configures isolated branch previews separately.
- `assets.directory` points to the generated files.
- `not_found_handling` selects 404-page handling for missing paths.

Ask your agent to add `src/pages/404.astro`, containing a useful “Page not found” message and a home link.
Astro generates the corresponding static error page (as of October 2026; re-check before relying on it). See [Astro routing](https://docs.astro.build/en/guides/routing/).

Keep this first site static.
A site with server code uses the `@astrojs/cloudflare` adapter, which connects server execution to the host (as of October 2026; re-check before relying on it). See [Deploy your Astro Site to Cloudflare](https://docs.astro.build/en/guides/deploy/cloudflare/).

**Check:** `npm run build` succeeds, `dist/` contains the site and the configuration has no remaining placeholders.

## 4. Make an optional first deployment by hand

A deployment publishes a version of your site.
Before proceeding, complete Step 10 to create the token, then return here.
An API token is a credential that grants a tool specific account permissions.

Use the private file from SERVICES.md. Enter the token yourself in your private editor.
Keep one `KEY=value` per line, with no quotes or `export`. Comments start with `#`.
Leave unrelated service entries alone.

**In your own terminal:** confirm permissions and check names without revealing values:

```bash
chmod 600 ~/.config/webtools/keys.env
python3 ~/.config/webtools/with_keys.py --check CLOUDFLARE_API_TOKEN,CLOUDFLARE_ACCOUNT_ID
```

Continue only when both names are present and neither is a placeholder.
Before the first public deployment, complete Step 9 if you want search engines told not to index the site.
That instruction does not make a site private.

**In your own terminal:**

```bash
env -u CLOUDFLARE_API_TOKEN -u CLOUDFLARE_ACCOUNT_ID npm run build
python3 ~/.config/webtools/with_keys.py CLOUDFLARE_API_TOKEN,CLOUDFLARE_ACCOUNT_ID -- npx wrangler@4 deploy
```

Wrangler uses those environment variables for authentication and account selection (as of October 2026; re-check before relying on it). See [Wrangler environment variables](https://developers.cloudflare.com/workers/wrangler/system-environment-variables/).

Look for a published address of the form `https://bakery-site.<your-subdomain>.<workers-dev domain>`: this is the free workers-dev address Cloudflare gives every Worker, on a subdomain named after your account (as of October 2026; re-check before relying on it). The dashboard shows the exact address. See [the workers-dev docs](https://developers.cloudflare.com/workers/configuration/routing/workers-dev/).
Use the actual address from your deployment.

**In your browser:** open that address and test the home page.
A brand-new account subdomain can briefly show a TLS error while its certificate is issued (as of October 2026; re-check before relying on it). See [the workers-dev docs](https://developers.cloudflare.com/workers/configuration/routing/workers-dev/).
TLS is the encrypted connection used by HTTPS. Wait a few minutes and retry before changing settings.

**Check:** the bakery site loads at the published address.

## 5. Publish the repository and connect automatic builds

Before recording files, ask your agent to check `.gitignore`, the list of files Git should leave out.
Exclude `node_modules/`, `dist/`, `.wrangler/`, `dry-run-out/` and local secret files.
Review `git status` before committing. Never commit credentials.

**In your own terminal:** for this new project:

```bash
git status
git add .
git commit -m "Prepare bakery site for deployment"
git branch -M main
gh auth login
gh repo create bakery-site --private --source=. --remote=origin --push
```

Follow the browser login offered by `gh`; do not paste a token into chat.
These commands create and push a private repository (as of October 2026; re-check before relying on it). See [repository creation](https://cli.github.com/manual/gh_repo_create).
If Git asks for an author identity, configure your own identity locally before retrying the commit.

**In your browser:** the alternative is GitHub > New repository. Name it `bakery-site`, choose Private and leave initialization options empty (as of October 2026; re-check before relying on it). See [creating a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository).
Follow its instructions for pushing an existing repository. Use this route instead of `gh repo create`.

**In your browser:** open Workers & Pages > Create > Import a repository, or open the existing Worker > Settings > Builds > Connect. Authorize the GitHub app for only `bakery-site` (as of October 2026; re-check before relying on it). See [Git integration](https://developers.cloudflare.com/workers/ci-cd/builds/git-integration/).
The initial connection is a dashboard authorization step, not a Wrangler command (as of October 2026; re-check before relying on it). See [Builds](https://developers.cloudflare.com/workers/ci-cd/builds/).

Enter these settings. The dashboard fields and deployment behavior are documented in [Builds configuration](https://developers.cloudflare.com/workers/ci-cd/builds/configuration/) (as of October 2026; re-check before relying on it).

| Setting | Value |
| --- | --- |
| Worker name | `bakery-site` |
| Production branch | `main` |
| Build command | `npm run build` |
| Deploy command | `npx wrangler@4 deploy` |
| Root directory | `/` |

The dashboard may suggest `npx wrangler deploy`; explicitly use major version 4 here.
A name mismatch can fail the build or target an unintended Worker (as of October 2026; re-check before relying on it). See [build troubleshooting](https://developers.cloudflare.com/workers/ci-cd/builds/troubleshoot/).
Use the platform's deployment credential settings. Never upload your local key file.

Build variables are separate from runtime variables, which exist while server code handles requests (as of October 2026; re-check before relying on it). See [Builds configuration](https://developers.cloudflare.com/workers/ci-cd/builds/configuration/).
**In your browser:** put values needed during compilation in the build's Variables or Environment variables section (as of October 2026; re-check before relying on it). See the same documentation.
This static bakery needs none initially.

If you later require a public value such as `PUBLIC_SITE_KEY`, ask your agent to add a prebuild check that rejects an empty value or `REPLACE_WITH_` placeholder.
Public values may appear in downloaded site files. Never use them for secrets.

**Check:** the first hosted build succeeds and its production address shows the same site.

## 6. Enable branch previews

A branch is a separate line of changes. `main` holds approved production code.
Use one preview mechanism per Worker.

New Workers Builds projects use Worker Previews. Older projects may use version preview aliases instead (as of October 2026; re-check before relying on it). See [build branches](https://developers.cloudflare.com/workers/ci-cd/builds/build-branches/).
Worker Previews requires Wrangler 4.135.0 or later (as of October 2026; re-check before relying on it). See [Previews](https://developers.cloudflare.com/workers/previews/).

Ask your agent to add `"previews": {}` as another top-level entry in `wrangler.jsonc`, with the required comma.
Keep it on `main` before creating branches.
The current configuration documentation requires this block even when empty. A plain static site needs no preview bindings inside it (as of October 2026; re-check before relying on it). See [preview configuration](https://developers.cloudflare.com/workers/previews/configuration/).
A binding connects server code to a resource, such as a database.

**In your browser:** enable “Builds for non-production branches” or “Enable Preview Builds” under the Worker's build branch settings. Set the preview command to `npx wrangler@4 preview` (as of October 2026; re-check before relying on it). See [build branches](https://developers.cloudflare.com/workers/ci-cd/builds/build-branches/).
Commit and push the configuration change before starting Step 12.

Preview links have two purposes (as of October 2026; re-check before relying on it). See [preview URLs](https://developers.cloudflare.com/workers/previews/) and [version URLs](https://developers.cloudflare.com/workers/versions-and-deployments/version-urls/).

| Link | What it shows |
| --- | --- |
| Branch alias, of the form `https://<branch>-bakery-site.<your-subdomain>.<workers-dev domain>` | The latest successful deployment of that branch |
| Per-deployment or per-version link | One fixed deployment; older version links use an eight-character version prefix |

Always give reviewers the branch alias for ongoing review. Copy the actual link from the dashboard.

Keep these changing preview behaviors in mind:

- The older command is `npx wrangler@4 versions upload --preview-alias "<branch>"`. The newer command is `npx wrangler@4 preview`. Configuring both pipelines can duplicate builds and leave one failing (as of October 2026; re-check before relying on it). See [workflow comparison](https://developers.cloudflare.com/workers/previews/).
- Define preview-only bindings in `previews` when adding databases, KV storage, rate limits or other resources. Configure preview secrets separately (as of October 2026; re-check before relying on it). See [configuration](https://developers.cloudflare.com/workers/previews/configuration/).
- New branches inherit the configuration of the branch they start from. Keeping preview settings only on one long-lived branch leaves branches from `main` without them.
- Worker Previews do not inherit production secrets or database bindings, and cron triggers, meaning scheduled jobs, target production. Older version URLs can use production resources (as of October 2026; re-check before relying on it). See [resource isolation](https://developers.cloudflare.com/workers/previews/resources/) and [version URLs](https://developers.cloudflare.com/workers/versions-and-deployments/version-urls/).
- Do not rely only on an API build list. Check the Worker's preview, deployment and build screens before declaring a push successful (as of October 2026; re-check before relying on it). See [Builds](https://developers.cloudflare.com/workers/ci-cd/builds/).
- Recheck commands after changing preview controls. Switching preview models replaces the preview command and can be irreversible (as of October 2026; re-check before relying on it). See [build branches](https://developers.cloudflare.com/workers/ci-cd/builds/build-branches/).
- Preview addresses on the workers-dev domain supply `X-Robots-Tag: noindex`; expect the platform's indexing instruction to take precedence over yours (as of October 2026; re-check before relying on it). See [Previews](https://developers.cloudflare.com/workers/previews/).

**Check:** Step 12 produces one intended preview build, and its branch alias shows the change.

## 7. Optionally require sign-in for previews

Cloudflare Access adds a login gate (as of October 2026; re-check before relying on it). See [Access for Workers](https://developers.cloudflare.com/workers/configuration/cloudflare-access/).
Use it when unfinished work should be private.

**In your browser:** activate Zero Trust, also called Cloudflare One, and choose a team name. Its Free plan covers up to 50 users (as of October 2026; re-check before relying on it). See [Zero Trust documentation](https://developers.cloudflare.com/cloudflare-one/).
Then open the Worker > Settings > Domains & Routes and enable Access for the relevant workers-dev, preview and version URLs. The dashboard can create an Access application for you (as of October 2026; re-check before relying on it). See [Workers Access setup](https://developers.cloudflare.com/workers/configuration/cloudflare-access/).

**In your browser:** configure the policy, the rule deciding who may enter. Account members can use their Cloudflare login. For outside reviewers, enable One-time PIN and allow their exact email addresses (as of October 2026; re-check before relying on it). See [Access documentation](https://developers.cloudflare.com/cloudflare-one/).
A “not enabled” API error can mean Zero Trust has not been activated. Adding token permissions does not activate it (as of October 2026; re-check before relying on it). See the same documentation.

For automated checks, create an Access service token under Access > Service credentials and allow it in a Service Auth policy (as of October 2026; re-check before relying on it). See [service tokens](https://developers.cloudflare.com/cloudflare-one/access-controls/service-credentials/service-tokens/).
Enter its values yourself in the existing private key file as `CF_ACCESS_CLIENT_ID` and `CF_ACCESS_CLIENT_SECRET`.

Requests use `CF-Access-Client-Id` and `CF-Access-Client-Secret` headers (as of October 2026; re-check before relying on it). See [service tokens](https://developers.cloudflare.com/cloudflare-one/access-controls/service-credentials/service-tokens/).
Never put their values on a curl command line.
The following creates a temporary mode-600 header file from the helper's environment, uses it, then deletes it.

**In your own terminal:** replace `<your-preview-url>` with the full HTTPS preview address:

```bash
python3 ~/.config/webtools/with_keys.py CF_ACCESS_CLIENT_ID,CF_ACCESS_CLIENT_SECRET -- python3 - '<your-preview-url>' <<'PY'
import os
import subprocess
import sys
import tempfile

fd, path = tempfile.mkstemp(prefix="workbench-access-")
try:
    with os.fdopen(fd, "w") as headers:
        for name, header in (
            ("CF_ACCESS_CLIENT_ID", "CF-Access-Client-Id"),
            ("CF_ACCESS_CLIENT_SECRET", "CF-Access-Client-Secret"),
        ):
            value = os.environ[name]
            if "\r" in value or "\n" in value:
                raise SystemExit("Invalid credential format")
            headers.write(f"{header}: {value}\n")
    subprocess.run(
        ["curl", "-sS", "-o", os.devnull, "-w", "%{http_code}\n",
         "-H", "@" + path, sys.argv[1]], check=True
    )
finally:
    os.unlink(path)
PY
```

**Check:** in a private browser window, the preview requires login and then shows the site. Test both the branch alias and a fixed-version link.

## 8. Attach a custom domain only at launch

DNS is the system that directs a domain to its hosting service.
A registrar is the service where you registered the domain.
Keep your real domain disconnected until the production site is ready.

**In your browser:** if the domain is registered elsewhere, choose Add a domain, select the Free zone plan and review imported DNS records. Change the nameservers at your registrar to the two assigned by Cloudflare, then wait until the domain's status in the dashboard reads active (as of October 2026; re-check before relying on it). See [domain setup](https://developers.cloudflare.com/dns/zone-setups/full-setup/setup/).
Preserve existing email records. Nameservers identify the service managing your DNS.

**In your browser:** open Worker > Settings > Domains & Routes > Add > Custom domain. Enter the domain you own. Cloudflare creates its DNS record and certificate (as of October 2026; re-check before relying on it). See [Custom Domains](https://developers.cloudflare.com/workers/configuration/routing/custom-domains/).
`bakery.example.com` is only an illustration. You cannot launch there.

Alternatively, add `"routes": [{ "pattern": "bakery.example.com", "custom_domain": true }]` to the configuration, replacing the example address before deploying (as of October 2026; re-check before relying on it). See [Custom Domains](https://developers.cloudflare.com/workers/configuration/routing/custom-domains/).
This CLI route needs the extra token permissions in Step 10.

For `www`, attach a second custom domain or create a redirect to the apex, the address without `www` (as of October 2026; re-check before relying on it). See [redirect rules](https://developers.cloudflare.com/rules/url-forwarding/).

**In your browser:** under SSL/TLS > Edge Certificates, enable Always Use HTTPS and minimum TLS 1.2. Optionally enable DNSSEC under DNS > Settings and add the supplied DS record at your registrar (as of October 2026; re-check before relying on it). See [edge certificates](https://developers.cloudflare.com/ssl/edge-certificates/) and [DNSSEC](https://developers.cloudflare.com/dns/dnssec/).
DNSSEC helps verify DNS answers. The DS record connects that verification to your registrar.

After launch, you may set `workers_dev` to `false` to remove the extra production address. Review URLs remain a separate setting (as of October 2026; re-check before relying on it). See [the workers-dev docs](https://developers.cloudflare.com/workers/configuration/routing/workers-dev/).

**Check:** your domain loads over HTTPS, the chosen `www` behavior works and existing email still works.

## 9. Add response headers

Headers are instructions sent alongside a web response.
Ask your agent to create `public/_headers` with the following text.
Astro copies `public/` into `dist/`, and static asset hosting reads `_headers` (as of October 2026; re-check before relying on it). See [Astro project structure](https://docs.astro.build/en/basics/project-structure/) and [asset headers](https://developers.cloudflare.com/workers/static-assets/headers/).

```text
/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  X-Frame-Options: DENY
  Content-Security-Policy: default-src 'self'
  Strict-Transport-Security: max-age=31536000
  X-Robots-Tag: noindex
```

This disables content-type guessing, limits referring-address information, denies device permissions and prevents framing.
The Content Security Policy, or CSP, restricts where the page loads resources.
Start with your own origin, meaning the site's protocol and address.
Ask your agent to add specific directives for each outside font, image or analytics host you actually use.
Inline scripts or styles may need hashes, which identify approved content. Test the page rather than broadly disabling the policy.

Strict Transport Security remembers HTTPS for one year.
Add `includeSubDomains` only when every subdomain supports HTTPS. Leave `preload` off until you understand its lasting effect.
Remove the site-wide `X-Robots-Tag: noindex` at launch and rebuild.

Every matching header rule applies. Overlapping rules can combine or duplicate header values (as of October 2026; re-check before relying on it). See [asset headers](https://developers.cloudflare.com/workers/static-assets/headers/).
Keep rules non-overlapping where they set the same header.
Do not combine `robots.txt` containing `Disallow: /` with reliance on `noindex`: a crawler blocked from fetching a page cannot see its header.

A `public/_redirects` file handles simple redirects (as of October 2026; re-check before relying on it). See [asset redirects](https://developers.cloudflare.com/workers/static-assets/redirects/).
Rebuild and deploy after changing either file.

**In your own terminal:** replace `<your-site>` with the hostname:

```bash
curl -sI 'https://<your-site>/' | grep -i content-security
```

**Check:** the response contains the intended CSP, and the site still displays and works correctly.

## 10. Create a narrowly scoped deployment token

**In your browser:** use My Profile > API Tokens > Create Token > Create Custom Token. Use a private window if you have multiple logins (as of October 2026; re-check before relying on it). See [creating tokens](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/).

Use these permission rows for the static deployment. Permission names and requirements can change (as of October 2026; re-check before relying on it). See [API permissions](https://developers.cloudflare.com/fundamentals/api/reference/permissions/).

| Scope | Permission | Level |
| --- | --- | --- |
| Account | Workers Scripts | Edit |
| Account | Account Settings | Read |
| User | User Details | Read |
| User | Memberships | Read |
| Account | Workers Builds Configuration | Edit (only if you use `builds_watch.py`) |

The two User rows support identity lookup and avoid Wrangler warnings (as of October 2026; re-check before relying on it). See [Wrangler authentication](https://developers.cloudflare.com/workers/wrangler/).
The Workers Builds Configuration row is for the workbench's `builds_watch.py` only: it lists your Workers to find the Worker's tag (covered by Workers Scripts) and then reads that Worker's builds, and Cloudflare's Builds API reference names Workers Builds Configuration > Edit for that API. The token must be one you create under My Profile > API Tokens, because the Builds API does not accept account-owned tokens (as of October 2026; re-check before relying on it). See [Builds API](https://developers.cloudflare.com/workers/ci-cd/builds/api-reference/). Leave the row out if you only watch builds in the dashboard.
Add Zone > Workers Routes > Edit and Zone > DNS > Edit only for CLI-managed routes or custom domains. Add database, KV or Access permissions only when a feature needs them (as of October 2026; re-check before relying on it). See [API permissions](https://developers.cloudflare.com/fundamentals/api/reference/permissions/).

**In your browser:** select Account Resources > Include > Specific account. If using zone permissions, select Zone Resources > Include > Specific zone. Set an expiry, also called TTL, and optionally an IP filter if your internet address is fixed (as of October 2026; re-check before relying on it). See [token creation](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/).
Record a reminder to replace the token before expiry.

The token value is shown once (as of October 2026; re-check before relying on it). See [token creation](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/).
Transfer that newly displayed value directly into `CLOUDFLARE_API_TOKEN` in your own private editor, following [SERVICES.md](SERVICES.md).
Never copy the key file or paste the value into a command, repository or chat.

**In your own terminal:** verify identity without printing the token:

```bash
python3 ~/.config/webtools/with_keys.py CLOUDFLARE_API_TOKEN,CLOUDFLARE_ACCOUNT_ID -- npx wrangler@4 whoami
```

Existing shell variables can select another credential or account (as of October 2026; re-check before relying on it). See [environment variables](https://developers.cloudflare.com/workers/wrangler/system-environment-variables/).
**In your own terminal:** count them without showing values, then build without the two account variables:

```bash
env | grep -c '^CLOUDFLARE_'
env -u CLOUDFLARE_API_TOKEN -u CLOUDFLARE_ACCOUNT_ID npm run build
```

A zero count is fine. Continue using the helper for authenticated commands.
After the workbench is installed (SETUP_GUIDE.md, P4), its `wrangler-safe` tool does the same job with more guards:
it reads the same key file, drops stray `CLOUDFLARE_*` and `CF_*` variables, and refuses when `wrangler.jsonc` pins a
different account. For example: `bash ~/.local/share/webdev-workbench/web_tools/wrangler-safe whoami`
(see `~/.local/share/webdev-workbench/web_tools/README.md`).
An explicit account ID documents your target; it does not replace checking credentials.

**Check:** `whoami` identifies the intended account. Return to Step 4 if you came here for your first token.

## 11. Learn the essential deployment commands

Run these from the repository root.
These Wrangler commands inspect identity, versions and deployment history (as of October 2026; re-check before relying on it). See [command reference](https://developers.cloudflare.com/workers/wrangler/commands/).

**In your own terminal:**

```bash
python3 ~/.config/webtools/with_keys.py CLOUDFLARE_API_TOKEN,CLOUDFLARE_ACCOUNT_ID -- npx wrangler@4 whoami
python3 ~/.config/webtools/with_keys.py CLOUDFLARE_API_TOKEN,CLOUDFLARE_ACCOUNT_ID -- npx wrangler@4 versions list
python3 ~/.config/webtools/with_keys.py CLOUDFLARE_API_TOKEN,CLOUDFLARE_ACCOUNT_ID -- npx wrangler@4 deployments list
```

A dry run prepares deployment files without uploading. Local development serves the built assets on your machine (as of October 2026; re-check before relying on it). See [commands](https://developers.cloudflare.com/workers/wrangler/commands/).
**In your own terminal:** run these separately. Stop the local server with Ctrl+C.

```bash
npx wrangler@4 deploy --dry-run --outdir dry-run-out
npx wrangler@4 dev
```

After inspecting it, delete only the generated `dry-run-out` folder.
Rebuild before another real deployment, then use the helper-wrapped `deploy` command from Step 4.

Rollback restores a selected earlier Worker version. It does not reverse external database changes (as of October 2026; re-check before relying on it). See [rollbacks](https://developers.cloudflare.com/workers/configuration/versions-and-deployments/rollbacks/).
**In your own terminal:** only when needed, replace `<version-id>` with an ID from the history:

```bash
python3 ~/.config/webtools/with_keys.py CLOUDFLARE_API_TOKEN,CLOUDFLARE_ACCOUNT_ID -- npx wrangler@4 rollback '<version-id>' --message "Restore the last reviewed bakery version"
```

**In your browser:** the alternative is the Worker's Deployments > Rollback control (as of October 2026; re-check before relying on it). See [rollbacks](https://developers.cloudflare.com/workers/configuration/versions-and-deployments/rollbacks/).

`tail` shows live Worker logs; a static-only site may produce no Worker execution logs. `secret put` accepts a value interactively or through standard input (as of October 2026; re-check before relying on it). See [commands](https://developers.cloudflare.com/workers/wrangler/commands/).
**In your own terminal:** use either command only when needed. Replace `<secret-name>` with the variable name, never its value.

```bash
python3 ~/.config/webtools/with_keys.py CLOUDFLARE_API_TOKEN,CLOUDFLARE_ACCOUNT_ID -- npx wrangler@4 tail
python3 ~/.config/webtools/with_keys.py CLOUDFLARE_API_TOKEN,CLOUDFLARE_ACCOUNT_ID -- npx wrangler@4 secret put '<secret-name>'
```

Stop `tail` with Ctrl+C before running another command.
Enter a secret only at the private prompt. For automation, have the helper pass the named value from the mode-600 key file to a small program that feeds standard input without printing it.
Do not create another plaintext key file.

As a project practice, wait about a week before adopting a brand-new Wrangler release, unless an urgent fix requires it.
Keep the exact dependency and lockfile committed.
Before deployment, run `npm audit` and review findings with your agent. Do not blindly apply forced fixes.

**Check:** you can identify the current deployment and an earlier version without changing production.

## 12. Complete one review and publishing loop

Start with a clean working tree, meaning no uncommitted changes.
**In your own terminal:**

```bash
git status
git switch main
git pull --ff-only
git switch -c add-opening-hours
```

Ask your agent to add invented bakery opening hours to `src/pages/index.astro`.
Review the wording yourself.

**In your own terminal:**

```bash
env -u CLOUDFLARE_API_TOKEN -u CLOUDFLARE_ACCOUNT_ID npm run build
npm audit
git diff
git add src/pages/index.astro
git commit -m "Add bakery opening hours"
git push -u origin add-opening-hours
gh pr create --base main --head add-opening-hours --title "Add opening hours" --body "Add opening hours to the bakery home page."
```

A pull request is a proposed change for review. `gh pr create` opens one (as of October 2026; re-check before relying on it). See [pull requests](https://cli.github.com/manual/gh_pr_create).
**In your browser:** alternatively, open the repository's Pull requests tab and create one from `add-opening-hours` into `main` (as of October 2026; re-check before relying on it). See [GitHub pull requests](https://docs.github.com/en/pull-requests).

**In your browser:** watch the preview build, open its branch alias and check the hours, layout, links and narrow-screen display.
From the terminal, the workbench's watchers can wait for you: `builds_watch.py` follows a Workers Build for one commit
(its token needs the Workers Builds Configuration row from Step 10; without it the tool stops with exit code 4, "API call failed"),
and `preview_url_watch.py` waits until the preview answers with text only the new build has, for example
`python3 ~/.local/share/webdev-workbench/web_tools/preview_url_watch.py --url https://<preview-host> --probe / --marker 'Open on Sundays'`.
After review, merge the pull request using its merge control (as of October 2026; re-check before relying on it). See [merging pull requests](https://docs.github.com/en/pull-requests).
Then watch the production build and open the live address.

**Check:** the reviewed hours appear in production, and the successful build corresponds to the merged change.

> **If you prefer Pages**
>
> Create a separate Pages project instead of following the Worker configuration path. Pages uses a `functions/` folder for server code, and `_headers` and `_redirects` work for static responses in the same way (as of October 2026; re-check before relying on it). See [Pages documentation](https://developers.cloudflare.com/pages/).
>
> Give its token the appropriate Pages permission instead of assuming Workers permissions cover it (as of October 2026; re-check before relying on it). See [API permissions](https://developers.cloudflare.com/fundamentals/api/reference/permissions/).
>
> **In your own terminal:** after building, replace `<name>` with the Pages project name:
>
> ```bash
> python3 ~/.config/webtools/with_keys.py CLOUDFLARE_API_TOKEN,CLOUDFLARE_ACCOUNT_ID -- npx wrangler@4 pages deploy dist --project-name '<name>'
> ```
>
> Check the published Pages address before sharing it.

## Troubleshooting

**Symptom: the build says a `previews` block is missing.**
Cause: Worker Previews needs that configuration, including for a static site (as of October 2026; re-check before relying on it). See [configuration](https://developers.cloudflare.com/workers/previews/configuration/).
Fix: add `"previews": {}` on `main`. Add explicit test bindings if needed, then bring that change into your branch.

**Symptom: the preview shows an old version.**
Cause: a fixed deployment link stays on its original deployment, or the latest build failed (as of October 2026; re-check before relying on it). See [Previews](https://developers.cloudflare.com/workers/previews/).
Fix: open the branch alias and confirm the latest commit succeeded.

**Symptom: authentication fails with 9109 or 10000.**
Cause: these errors can reflect a wrong token, wrong account or insufficient permissions (as of October 2026; re-check before relying on it). See [API troubleshooting](https://developers.cloudflare.com/fundamentals/api/).
Fix: check the helper's presence report, account selection and permission rows. Editing token permissions need not change its value (as of October 2026; re-check before relying on it). See [token management](https://developers.cloudflare.com/fundamentals/api/).

**Symptom: deployment targeted the wrong account.**
Cause: inherited shell credentials or incorrect configuration selected another destination (as of October 2026; re-check before relying on it). See [Wrangler environment variables](https://developers.cloudflare.com/workers/wrangler/system-environment-variables/).
Fix: stop deploying, verify `account_id` and helper-managed credentials, and inspect both accounts before removing anything.

**Symptom: `/about` behaves differently from `/about/`.**
Cause: generated directory pages and host redirects determine the canonical path (as of October 2026; re-check before relying on it). See [asset routing](https://developers.cloudflare.com/workers/static-assets/routing/).
Fix: check that the page exists in `dist/`, inspect both paths and use the final canonical address consistently.

**Symptom: video cannot seek in Safari.**
Cause: some asset setups may return the entire file with HTTP 200 instead of answering a byte-range request with 206 (as of October 2026; re-check before relying on it). Recheck [static asset behavior](https://developers.cloudflare.com/workers/static-assets/).
**In your own terminal:** replace `<site>` and `<file>` with your hostname and video filename:

```bash
curl -sI -H 'Range: bytes=0-99' 'https://<site>/<file>.mp4'
```

Fix: look for `206` and a valid `Content-Range`. Confirm with an actual playback test because a header-only request is not conclusive.
If range requests return the whole file, use a Worker route that implements ranges or a suitable media host.

**Symptom: a new workers-dev address has a TLS error.**
Cause: initial certificate issuance may still be pending (as of October 2026; re-check before relying on it). See [the workers-dev docs](https://developers.cloudflare.com/workers/configuration/routing/workers-dev/).
Fix: wait a few minutes and retry. Do not disable certificate checking.

**Symptom: Access repeatedly returns to login.**
Cause: the email, login method or protected hostname may not match the policy (as of October 2026; re-check before relying on it). See [Access documentation](https://developers.cloudflare.com/cloudflare-one/).
Fix: verify the exact email and hostname, enable One-time PIN for invited reviewers and retry in a private window.

## Undo / remove

First decide whether you need a rollback or permanent removal.
Use Step 11 for a rollback. Disable automatic publishing before permanent removal.

**In your browser:** disconnect the repository's build integration, remove custom domains, then delete the Worker through Settings > Delete (as of October 2026; re-check before relying on it). See [Workers documentation](https://developers.cloudflare.com/workers/).
Confirm the Worker name before deleting it.

**In your browser:** under GitHub > Settings > Applications, remove this repository from the Cloudflare app's access. Uninstall the app only if no other project needs it (as of October 2026; re-check before relying on it). See [installed apps](https://docs.github.com/en/apps/using-github-apps/reviewing-and-modifying-installed-github-apps).

**In your browser:** delete the site's Access application and revoke its service token if unused elsewhere (as of October 2026; re-check before relying on it). See [Access documentation](https://developers.cloudflare.com/cloudflare-one/).

**In your browser:** open My Profile > API Tokens and choose Roll to replace the credential, or Delete to revoke it (as of October 2026; re-check before relying on it). See [token management](https://developers.cloudflare.com/fundamentals/api/).
Update or remove only the relevant entries in your private key file yourself. Keep unrelated service credentials.

Remove the custom domain before deleting its DNS zone, the collection of records for that domain.
If moving DNS elsewhere, preserve all required records and coordinate DNSSEC changes with the registrar before removing the zone (as of October 2026; re-check before relying on it). See [DNS documentation](https://developers.cloudflare.com/dns/).

**Check:** publishing is disconnected, the removed site is unavailable, unused credentials are revoked and unrelated sites and email still work.