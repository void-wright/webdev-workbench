# Deploy an Astro site on Vercel

## What you will have at the end

- A deployed copy of your site.
- A preview address for reviewing changes.
- Spending controls and tested access protection.
- An optional custom domain for launch.
- A way to restore an earlier deployment.

## Before you start

Allow 60 to 90 minutes, plus any waiting time for domain changes.

This guide uses the invented **Crumb & Crust Bakery** and its `bakery-site` repository.
A repository, or repo, is a folder whose changes are tracked with Git.
A deployment is a built copy of your site running on a hosting service.

Have these ready:

- Your GitHub account and a repo containing your working site.
- Your local project folder, with Git, Node.js, npm, Python 3 and curl installed.
- A browser and your own terminal running bash.
- SERVICES.md Section A completed: the private key file and the helper.
- Access to your domain's settings if you want a custom address.

Your Claude Code agent can edit project files and explain errors.
You handle account access, secret values and billing choices yourself.
Never give the agent your key file or ask it to read that file.

Keep keys only in `~/.config/webtools/keys.env` or the hosting platform's secret store.
Never print, copy, paste into chat, or `source` the key file.
Mode `600` means only your operating-system user can read or write it.

**In your own terminal:** Open the project folder, then check your tools.

```bash
pwd
git status
node --version
npm --version
python3 --version
curl --version
```

Look for your project folder and a version from each tool.
Stop and fix missing tools before continuing.
Commands below run from the folder containing your site's `package.json`, which lists its dependencies and scripts.

## 1. Create your account

**In your browser:** Open [vercel.com/signup](https://vercel.com/signup).
Choose the GitHub sign-up connection to link your login accounts (as of October 2026; re-check before relying on it). [Account documentation](https://vercel.com/docs/accounts)

Choose a plan:

- **Hobby:** Free for personal, non-commercial use only (as of October 2026; re-check before relying on it). [Hobby documentation](https://vercel.com/docs/plans/hobby)
- **Pro:** Charges per paid seat per month, with usage charges possible; choose Pro for commercial use rather than Hobby (as of October 2026; re-check before relying on it). [Pricing](https://vercel.com/pricing)

A practice bakery site is different from a site promoting an operating bakery.
Use the commercial plan when the site serves a business.

**In your browser:** Open your account's **Settings > Authentication** and enable two-factor authentication, which requires a second proof of identity at login (as of October 2026; re-check before relying on it). [Authentication documentation](https://vercel.com/docs/two-factor-authentication)
Complete the setup and store recovery codes privately.

**Check:** You can sign in, your intended plan is selected, and two-factor authentication shows as enabled.

## 2. Set spending controls before deploying

Hobby hosting has no usage bill; exceeding included limits can pause or block service rather than charge overages (as of October 2026; re-check before relying on it). [Plan documentation](https://vercel.com/docs/plans)
Domain purchases and separately purchased services are separate costs.

**In your browser:** For Pro, open the team's **Settings > Billing > Spend Management** before your first deployment (as of October 2026; re-check before relying on it). [Spend Management documentation](https://vercel.com/docs/spend-management)

Set an amount you can afford for additional monthly usage.
Enable notifications and the action to pause production deployments when the amount is reached.
Save any confirmation the page requires.

This budget concerns on-demand usage, not your entire invoice.
Pausing production stops existing sites from serving visitors; it does more than stop new builds (as of October 2026; re-check before relying on it). [Spend Management documentation](https://vercel.com/docs/spend-management)
Allow room for subscription charges and delays in usage reporting.

**Check:** Reopen the settings and confirm the amount, notifications and pause action remain saved.

## 3. Import the site

Start with harmless placeholder content.
The first import can create a production deployment before you finish configuring protection (as of October 2026; re-check before relying on it). [Deployment documentation](https://vercel.com/docs/deployments)
If the site must remain private from its first moment, configure team protection defaults from Step 7 first.

**In your own terminal:** Confirm that the existing site builds.

```bash
npm run build
```

A build converts source files into deployable files.
Ask your agent to fix any build errors before importing.

**In your browser:** Choose **Add New > Project > Import Git Repository**, then select `bakery-site` (as of October 2026; re-check before relying on it). [GitHub integration documentation](https://vercel.com/docs/git/vercel-for-github)
When asked to install the GitHub app, grant access to **Only select repositories** and choose this repo (as of October 2026; re-check before relying on it). [GitHub app documentation](https://docs.github.com/en/apps/using-github-apps/installing-a-github-app-from-a-third-party)

Review these build settings before deploying (as of October 2026; re-check before relying on it). [Build documentation](https://vercel.com/docs/builds/configure-a-build)

| Setting | Value for this guide |
| --- | --- |
| Framework preset | Astro, normally detected automatically |
| Build command | `npm run build`, if that script runs `astro build` |
| Output directory | `dist` for a static site |
| Root directory | The folder containing the site's `package.json` |

A monorepo is one repo containing several projects.
For a monorepo, select the site's subfolder, not automatically the repo's top folder.

**In your browser:** Check the Node.js version under **Settings > Build and Deployment** (as of October 2026; re-check before relying on it). [Build documentation](https://vercel.com/docs/builds/configure-a-build)
Use a version supported by your installed framework and dependencies.
For a project compatible with Node 22, your agent can merge `"engines": {"node": "22.x"}` into `package.json`.

A fully static Astro site needs no adapter; server-rendered routes need `@astrojs/vercel` (as of October 2026; re-check before relying on it). [Astro deployment guide](https://docs.astro.build/en/guides/deploy/vercel/)
An adapter connects framework server features to a hosting service.
For server output, follow the adapter's settings instead of forcing a static output directory.

A checker scanning only `dist/*.html` can inspect zero pages and still report success.
Server-rendered pages may have no matching HTML files there.
Check the deployed routes and require your checker to report how many pages it tested.

**In your browser:** Start the deployment and inspect its build log.
Complete Step 7 immediately afterward.

**Check:** The deployment succeeds and provides an address shaped like `https://bakery-site-<something>.vercel.app` (as of October 2026; re-check before relying on it). [Generated URLs](https://vercel.com/docs/deployments/generated-urls)
Use the actual address supplied, not this example.

## 4. Separate preview work from production

A branch is a named line of work.
Production is the version intended for visitors.
Preview is a version used to review changes.

Normally, enabled pushes to non-production branches create Preview deployments.
Pushes to the production branch create Production deployments, with `main` preferred by default (as of October 2026; re-check before relying on it). [Git deployment documentation](https://vercel.com/docs/git)

**In your browser:** Confirm branch tracking under **Settings > Environments > Production**; older interfaces may place the setting under **Settings > Git** (as of October 2026; re-check before relying on it). [Production branch documentation](https://vercel.com/docs/git)

Ask your agent to merge this configuration into `vercel.json` on `main`, then commit and push it.
This is JSON file content, not a terminal command.

```json
{ "git": { "deploymentEnabled": { "main": false } } }
```

This disables Git-triggered deployments from `main`; it does not remove an existing deployment or prevent manual production deployment (as of October 2026; re-check before relying on it). [Git configuration](https://vercel.com/docs/project-configuration/git-configuration)
If your production branch has another name, use that name instead.
Preserve any existing settings in the file.

**In your own terminal:** Once that change is on your local `main`, create your working branch.

```bash
git switch -c preview
git push -u origin preview
```

If `preview` already exists, use `git switch preview` instead of the first command.
Do unfinished work on this branch.

Each deployment gets its own address, while the branch address follows the branch's latest deployed changes (as of October 2026; re-check before relying on it). [Generated URLs](https://vercel.com/docs/deployments/generated-urls)
A branch address resembles `bakery-site-git-<branch>-<team>.vercel.app`.
Copy the real branch address rather than constructing one yourself.
Give reviewers this address when they should see ongoing updates.

A pull request, or PR, proposes merging one branch into another.
The integration adds deployment information and preview links to PRs (as of October 2026; re-check before relying on it). [GitHub integration](https://vercel.com/docs/git/vercel-for-github)

**Check:** A change pushed to `preview` produces a Preview deployment, and the branch address shows the change.

## 5. Set environment variables

An environment variable is a named setting supplied to a program.
Some contain public configuration; others contain secrets.

**In your browser:** Open **Settings > Environment Variables** and choose the required environment for each variable: Production, Preview or Development (as of October 2026; re-check before relying on it). [Environment variable documentation](https://vercel.com/docs/environment-variables)
Enter secret values yourself in the platform's secret store.
Do not add your deployment-management token to the website's variables.

Astro exposes browser variables through the `PUBLIC_` prefix, and build-time values require rebuilding after changes (as of October 2026; re-check before relying on it). [Astro environment variables](https://docs.astro.build/en/guides/environment-variables/)
For example, `PUBLIC_SITE_URL` may hold your public site address.
Never give a secret a `PUBLIC_` name.
Anyone receiving the page may be able to read browser-visible values.

After completing Step 6, this CLI command prompts for a Preview variable value (as of October 2026; re-check before relying on it). [Environment CLI documentation](https://vercel.com/docs/cli/env)

**In your own terminal:**

```bash
python3 ~/.config/webtools/with_keys.py VERCEL_TOKEN -- vercel env add PUBLIC_SITE_URL preview
```

The general form is `vercel env add NAME preview`.
Replace `NAME` with the actual variable name, never its value.

The command `vercel env pull .env.local` downloads Development variables into a local file (as of October 2026; re-check before relying on it). [Environment CLI documentation](https://vercel.com/docs/cli/env)
Do not use it to download secrets under this workbench's single-file rule.
Keep local secret values in `keys.env` and supply only needed names through the helper.
If you use `.env.local` for public settings, exclude it from Git anyway.

Ask your agent to add `.env.local`, `.env.*.local` and `.vercel/` to `.gitignore`.
That file tells Git which untracked files to ignore.

**In your own terminal:**

```bash
git check-ignore .env.local .vercel/project.json
git ls-files .env.local
```

**Check:** The ignore check lists both paths, the tracked-file check lists nothing, and each hosted variable has the intended environment selected.

## 6. Install and connect the CLI

A CLI is a command-line interface.
The following installs the Vercel CLI once (as of October 2026; re-check before relying on it). [CLI documentation](https://vercel.com/docs/cli)

**In your own terminal:**

```bash
npm install -g vercel
vercel login
vercel whoami
```

**In your browser:** Complete the login flow opened by the command.
If installation reports a permissions error, fix your user-owned Node installation rather than adding `sudo`.

If login appears successful but `whoami` repeatedly says you are not logged in, use a token.
A token is a secret credential for command access.

**In your browser:** Open [vercel.com/account/tokens](https://vercel.com/account/tokens).
Create a token scoped to the intended team and set an expiration (as of October 2026; re-check before relying on it). [Token documentation](https://vercel.com/docs/rest-api/reference/welcome#creating-an-access-token)

**In your own terminal:** save it with the hidden-input command in SERVICES.md, Section A, Step 5, using the name `VERCEL_TOKEN`.
The value never appears on screen, and the other entries in the file are kept.

The CLI accepts `VERCEL_TOKEN` from its environment (as of October 2026; re-check before relying on it). [CLI global options](https://vercel.com/docs/cli/global-options)

**In your own terminal:** Check and link the existing project.

```bash
python3 ~/.config/webtools/with_keys.py --check VERCEL_TOKEN
python3 ~/.config/webtools/with_keys.py VERCEL_TOKEN -- vercel whoami
python3 ~/.config/webtools/with_keys.py VERCEL_TOKEN -- vercel link
```

Choose the intended team and existing `bakery-site` project.
Linking records the project connection locally (as of October 2026; re-check before relying on it). [CLI deployment guide](https://vercel.com/docs/projects/deploy-from-cli)
If browser login works, you may run commands without the helper; every token-authenticated command must use it.

The following creates a manual Preview deployment (as of October 2026; re-check before relying on it). [CLI deployment guide](https://vercel.com/docs/projects/deploy-from-cli)

**In your own terminal:**

```bash
python3 ~/.config/webtools/with_keys.py VERCEL_TOKEN -- vercel
```

The production equivalent adds `--prod`.
Do not run that until Step 10.

**Check:** The helper reports the token as present, identity matches your account, and the folder links to the intended project.

## 7. Protect and test previews

**In your browser:** Open project **Settings > Deployment Protection** and select **Vercel Authentication** (as of October 2026; re-check before relying on it). [Protection documentation](https://vercel.com/docs/deployment-protection)

**Standard Protection** protects preview and generated deployment URLs, including production deployment URLs, but excludes production domains (as of October 2026; re-check before relying on it). [Protection documentation](https://vercel.com/docs/deployment-protection)
Do not assume every address ending in `vercel.app` has the same protection.
A stable production domain and a particular deployment URL have different roles.

**All Deployments** with Vercel Authentication is available on all plans without a paid add-on according to the current documentation (as of October 2026; re-check before relying on it). [Protection documentation](https://vercel.com/docs/deployment-protection)
Choose it while the entire unfinished site must remain private.

Legacy preview-only protection leaves production deployments exposed (as of October 2026; re-check before relying on it). [Protection documentation](https://vercel.com/docs/deployment-protection)
Check each deployment's actual classification, even when its branch name suggests Preview.

**In your own terminal:** Enter the actual preview URL when prompted.
Use an ordinary deployment URL without a sharing token.

```bash
read -r -p "Preview URL, including https://: " preview_url
curl -s -o /dev/null -w '%{http_code}\n' "$preview_url"
curl -sI "$preview_url"
```

Look for `401`, meaning authentication is required, or a `30x` redirect leading to login.
A redirect alone does not prove protection.
**In your browser:** Open the same address in a private window and confirm the page is blocked until login.
Repeat for the branch address and production addresses.

**In your browser:** For outside reviewers, use the deployment's **Share** controls or invite them through the available access flow (as of October 2026; re-check before relying on it). [Access methods](https://vercel.com/docs/deployment-protection/methods-to-bypass-deployment-protection)
Treat a link that grants access as private.

For automation, use **Protection Bypass for Automation** and its `x-vercel-protection-bypass` header (as of October 2026; re-check before relying on it). [Automation bypass documentation](https://vercel.com/docs/deployment-protection/methods-to-bypass-deployment-protection/protection-bypass-automation)
**In your browser:** Create a bypass secret in the protection settings.
**In your own terminal:** save it with SERVICES.md, Section A, Step 5, using the name `VERCEL_AUTOMATION_BYPASS_SECRET`.
Never put the secret in a URL or command argument.

This optional check creates a temporary mode-600 header file outside the repo, then deletes it.
The private key file remains the only lasting local secret store.

**In your own terminal:** replace `<exact deployment URL>` with the full `https://` address, keeping the quotes:

```bash
python3 ~/.config/webtools/with_keys.py VERCEL_AUTOMATION_BYPASS_SECRET -- python3 - '<exact deployment URL>' <<'PY'
import os
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit

url = sys.argv[1].strip()
parts = urlsplit(url)
if parts.scheme != "https" or parts.username or parts.password or parts.query:
    raise SystemExit("Use an HTTPS deployment URL without credentials or a query.")
secret = os.environ["VERCEL_AUTOMATION_BYPASS_SECRET"]
if not secret or "\r" in secret or "\n" in secret:
    raise SystemExit("Invalid bypass secret.")
fd, path = tempfile.mkstemp(prefix="workbench-vercel-", suffix=".headers")
try:
    os.fchmod(fd, 0o600)
    with os.fdopen(fd, "w") as header:
        header.write("x-vercel-protection-bypass: " + secret + "\n")
    subprocess.run(
        ["curl", "-sS", "-o", "/dev/null", "-w", "%{http_code}\n",
         "--header", "@" + path, url],
        check=True,
    )
finally:
    os.unlink(path)
PY
```

Do not add verbose output or automatic redirect following to this secret-bearing request.

**Check:** Anonymous access is blocked, approved reviewers can enter, and the optional bypass check reaches the expected page response.

## 8. Prepare your custom domain

A domain is a readable site address.
DNS is the system that directs that address to a server.
Use `bakery.example.com` only as an illustration; substitute a domain you own.

Attaching a production domain can make the site public under Standard Protection.
Keep All Deployments protection until launch if necessary.

**In your browser:** Open **Settings > Domains**, add your domain, and read the requested DNS records (as of October 2026; re-check before relying on it). [Domain documentation](https://vercel.com/docs/domains/working-with-domains/add-a-domain)
An apex is the bare domain, such as `example.com`.
A subdomain adds a label, such as `bakery.example.com`.

An apex commonly uses an A record, and a subdomain commonly uses a CNAME; use the exact records shown for your project (as of October 2026; re-check before relying on it). [Domain documentation](https://vercel.com/docs/domains/working-with-domains/add-a-domain)
Do not copy an IP address from an unrelated tutorial.

**In your browser:** At your DNS provider, create or update only the requested records.
If using Cloudflare, choose **DNS only**, shown by a grey cloud, for these records (as of October 2026; re-check before relying on it). [Proxy status documentation](https://developers.cloudflare.com/dns/proxy-status/)
This sends traffic directly to the host and avoids proxy interference during setup.

**Check:** Domain verification succeeds and HTTPS opens without a certificate warning. Recheck access in a private window.

## 9. Add headers and redirects

A response header gives the browser instructions about a page.
A redirect sends a visitor from one address to another.
Vercel reads `headers` and `redirects` from `vercel.json` (as of October 2026; re-check before relying on it). [Project configuration](https://vercel.com/docs/project-configuration)

Ask your agent to merge the following into your existing file.
Replace the two example domains with your actual domain choices.
The `www` address must also be attached and configured in DNS.
This is JSON file content, not a terminal command.

```json
{
  "git": { "deploymentEnabled": { "main": false } },
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
        { "key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()" },
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "Content-Security-Policy", "value": "default-src 'self'; script-src 'self'; connect-src 'self'; img-src 'self' data:; style-src 'self'; font-src 'self'; frame-src 'none'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'self'" },
        { "key": "Strict-Transport-Security", "value": "max-age=300" },
        { "key": "X-Robots-Tag", "value": "noindex" }
      ]
    }
  ],
  "redirects": [
    {
      "source": "/:path*",
      "has": [{ "type": "host", "value": "www.bakery.example.com" }],
      "destination": "https://bakery.example.com/:path*",
      "permanent": true
    }
  ]
}
```

This starter disables type guessing, limits referral information and blocks unused device permissions.
It also prevents other sites from framing your pages.
CSP, or Content Security Policy, limits where page resources can come from.
HSTS tells browsers to keep using HTTPS; start with five minutes while testing.
Do not add `includeSubDomains` until every affected subdomain supports HTTPS.

The strict CSP may block inline scripts, styles or external services.
Ask your agent to test every page and allow only resources the site needs.
Do not solve failures by allowing every source.

For preview comments, allow `https://vercel.live` in `script-src`, `connect-src`, `img-src`, `style-src`, `font-src` and `frame-src`; the toolbar also documents additional resource and connection requirements (as of October 2026; re-check before relying on it). [Toolbar CSP requirements](https://vercel.com/docs/vercel-toolbar/managing-toolbar)
Have your agent apply the complete documented requirements for previews and test the toolbar.
Keep production's policy narrower when it does not need those tools.

**In your own terminal:** After deployment, enter an accessible site URL.

```bash
read -r -p "Site URL, including https://: " site_url
curl -sI "$site_url"
```

A protected response may show authentication headers instead of your page headers.
Inspect the authenticated page through browser developer tools, or use the bypass technique from Step 7.

**Check:** The page response has the intended headers, pages still work, and the `www` address redirects once to your chosen address.

## 10. Launch with one coordinated change

Keep access protection enabled while preparing these changes.
Ask your agent to assemble and review them together:

1. Remove `noindex` from page metadata and the `X-Robots-Tag` header.
2. Change `public/robots.txt` to allow crawling, with the content below.
3. Confirm the sitemap exists and uses your real public domain.
4. Remove `deploymentEnabled.main: false`, preserving unrelated configuration.
5. Commit the reviewed changes and merge them into the production branch.
6. Confirm the new production deployment succeeds before opening public access.

A sitemap lists pages for search engines.
Use your actual sitemap URL in this file content, not the example.

```text
User-agent: *
Allow: /
Sitemap: https://bakery.example.com/sitemap-index.xml
```

A sitemap declaration does not create a sitemap.
Have your agent configure and verify the actual file.

**In your browser:** Attach the custom domain if you postponed Step 8.
Switch to Standard Protection when the production domain should become public (as of October 2026; re-check before relying on it). [Protection documentation](https://vercel.com/docs/deployment-protection)
Retest previews separately.

For an intentional manual production deployment, the CLI uses `--prod` (as of October 2026; re-check before relying on it). [CLI deployment guide](https://vercel.com/docs/projects/deploy-from-cli)

**In your own terminal:** Run this only if you are launching manually from the reviewed production files.

```bash
python3 ~/.config/webtools/with_keys.py VERCEL_TOKEN -- vercel --prod
```

**In your own terminal:** Enter your real public domain.

```bash
read -r -p "Public site URL, including https://: " live_url
curl -sI "$live_url"
curl -fsS "${live_url%/}/robots.txt"
curl -sI "${live_url%/}/sitemap-index.xml"
```

If your sitemap has another name, change the last command to match it.
Look for a successful page response, no blocking robots directive, and a reachable sitemap.

**In your browser:** Visit the site while signed out.
Test navigation, forms, mobile layout and missing-page behavior.
Use your intended social platform's card validator to check the public title, description and image.
Submit only the public URL, never a bypass or private sharing link.

**Check:** The public domain works without login, previews remain protected, and search and social previews use the final address.

## 11. Restore a previous deployment

A rollback restores an earlier deployed version.
It does not undo database changes or external actions.

**In your browser:** Open **Deployments**, select the previous working production deployment, and use **Instant Rollback** when available (as of October 2026; re-check before relying on it). [Rollback documentation](https://vercel.com/docs/instant-rollback)
A **Promote** action serves a different purpose: moving a chosen deployment into production.
Check the target and confirmation carefully.

The CLI also offers `vercel rollback` (as of October 2026; re-check before relying on it). [Rollback CLI](https://vercel.com/docs/cli/rollback)

**In your own terminal:**

```bash
python3 ~/.config/webtools/with_keys.py VERCEL_TOKEN -- vercel rollback
```

Read the proposed target before confirming.
Hobby rollback is limited to the immediately previous deployment; paid plans have broader eligible targets (as of October 2026; re-check before relying on it). [Rollback documentation](https://vercel.com/docs/instant-rollback)
Ask your agent to fix or revert the broken source change before the next production release.

**Check:** The live domain shows the earlier working version, and your important routes still function.

## Troubleshooting

**Symptom:** “No Output Directory named dist” or “public.”
**Cause:** The framework preset, project root or output override is wrong.
**Fix:** Revisit Step 3. Select the folder containing the correct `package.json`; use adapter defaults for server rendering.

**Symptom:** The build fails because a variable is missing.
**Cause:** It was omitted or assigned to another environment.
**Fix:** Set it for the deployment's environment and deploy again. Share only a redacted error with your agent.

**Symptom:** A preview opens without login.
**Cause:** Its URL is outside the chosen protection scope, or your browser already has access.
**Fix:** Test anonymously, inspect the deployment's classification, and use the protection settings in Step 7.

**Symptom:** The domain shows “Invalid Configuration.”
**Cause:** DNS records conflict, point elsewhere, or still use a proxy.
**Fix:** Compare against the exact requested records, use DNS only where instructed, and allow time for DNS updates.

**Symptom:** The comments toolbar is missing.
**Cause:** It may be disabled or blocked by CSP.
**Fix:** Check its visibility settings and the browser console, then apply the documented preview CSP requirements.

**Symptom:** Login succeeds in the browser but fails in the terminal.
**Cause:** The CLI did not retain or find usable authentication.
**Fix:** Use Step 6's token route through the helper. Never put the token after a command-line flag.

**Symptom:** A checker passes but pages fail.
**Cause:** It may have tested zero HTML files or tested the login page.
**Fix:** Require a nonzero route count and verify expected page content on deployed routes.

## Undo / remove

**In your browser:** Remove the custom domain from the project and remove its obsolete DNS records.
Delete only records created for this site.

**In your browser:** Open project settings and find **Delete Project**, commonly under **Advanced** or **General** (as of October 2026; re-check before relying on it). [Project management documentation](https://vercel.com/docs/projects/managing-projects)
Read the deletion confirmation. Save any non-secret settings you still need before confirming.

**In your browser:** Revoke this project's tokens and automation bypass secrets.
Review any paid subscription or add-on separately; deleting a project is not a substitute for checking billing.

**In your browser:** In GitHub's installed-app settings, remove this repo from the Vercel app's access; uninstall the app only if no other repo needs it (as of October 2026; re-check before relying on it). [Installed-app management](https://docs.github.com/en/apps/using-github-apps/reviewing-and-modifying-installed-github-apps)

**In your own terminal:** Edit `keys.env` yourself and remove the revoked entries.
Keep the file at mode `600`.
Ask your agent to remove obsolete project configuration and the local `.vercel` link folder without touching secrets.

**Check:** The domain no longer serves the removed project, its app access is gone, and unwanted billing has been cancelled.