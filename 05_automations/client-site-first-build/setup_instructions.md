# Site First Build: Setup Instructions (generic edition)

> For your own machine (macOS, Linux, or Windows through WSL2). Most of this is already done if you ran `SETUP_GUIDE.md`; this file lists what this automation needs and how to verify it. Never print or paste a secret.

## System requirements

- Node 22.x through nvm, plus npm. Pin the Node version in each repository and run `nvm use` there.
- Python 3.10+ for monitoring, verification, and site migration tasks.
- git and the GitHub CLI `gh`, signed in as **you**. See `09_guides/GITHUB_SETUP.md`.
- Voidwright installed according to `SETUP_GUIDE.md`, with the package's memory pack loaded.
- The package's design, WebGL, scroll journey, AEO, agent readiness, Astro, prototype, web app, resource hub, maintenance, and planning skills installed. Include the packaged Council voices and the design generator, reflector, and curator agents.
- The tools provided in `06_web_tools/`. Follow `06_web_tools/README.md` and run `bash bin/install_skills.sh` as directed by the setup guide.

## 1. Cloudflare access (all modes)

Account and token setup, step by step: `09_guides/DEPLOY_CLOUDFLARE.md`. Choose the authentication method your work requires:

- **Wrangler login** (simplest): `npx wrangler login`, then `npx wrangler whoami`. Wrangler keeps its own login.
- **An API token in your key file** (needed by `06_web_tools/cf-api`, `06_web_tools/builds_watch.py`, and scripted work): create a token scoped to one account and, for DNS work, one zone. Use a private browser window and confirm the intended account before creating it. Store `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`, and, for DNS work, `CLOUDFLARE_ZONE_ID` in the private key file configured during setup. Set its permissions to mode 600. The web tools parse this file; never `source` it, print it, or commit it.
- If previews will sit behind Cloudflare Access, store the service token's two values in the same key file as `CF_ACCESS_CLIENT_ID` and `CF_ACCESS_CLIENT_SECRET`.
- `bash 06_web_tools/wrangler-safe <wrangler args>` runs Wrangler with the key file's token, removes other exported `CLOUDFLARE_*` variables, and refuses to proceed when the repository's pinned `account_id` differs from the key's account. Resolve the tool's path from the package root when working in a site repository.

## 2. GitHub

- `gh auth status` shows your account. Confirm that account has write access to the site repository.
- For a new site repository, run `gh repo create <your-github-user>/<site-slug> --private`, then set the commit email within the local repository using `git config user.email <your-address>`.

## 3. Security baseline

- Install `gitleaks` and `pre-commit`. Each site repository must contain secret-scanning and pre-commit configuration. Run `pre-commit install` after every clone. Verify detection by staging a synthetic test credential that matches a configured rule and confirming the commit is blocked. Remove the test credential afterward.
- Public-by-design values, such as a Turnstile sitekey or public analytics beacon token, may receive narrow gitleaks allowlist entries. Secrets never do.

## 4. Playwright (empirical gates)

```bash
npx playwright install chromium
node -e 'console.log(require("playwright").chromium.executablePath())'
# Use the reported executable path as CHROME_PATH for Lighthouse.
```

Use a short temporary directory for Chrome's profile. A long path can break its socket and leave Lighthouse without output.

## 5. Sanity (hub modes only)

Use a Sanity organization you control, a project per site, and a token stored as `SANITY_API_TOKEN` in your private key file with mode 600 permissions. See `05_automations/client-site-first-build/runbook_appendix/sanity_org_setup.md`.

## 6. Site-port prerequisites (only if `IS_SITE_PORT == true`)

- `python3 -m pip install --user cdx-toolkit` installs the Common Crawl client and its `cdxt` command.
- `python3 -m pip install --user scrapy` installs tooling for referrer verification.
- Obtain Google Search Console access for the old domain. The domain owner verifies ownership with a DNS TXT record. See `05_automations/client-site-first-build/runbook_appendix/gsc_export_pause.md`.

## 7. Folders

- Keep site repositories in your usual development location. Commands below use `<your-site-repo>` as a placeholder.
- Keep source inputs and old-site archives in a separate working folder outside the repository.
- Keep ACE workspaces outside the deployable source tree and exclude them from version control. This prevents temporary review material from entering a release.

## 8. Local model execution (optional)

If a step uses a local model, confirm its runtime requirements and available resources before starting. Set any required device configuration before launching the process, then verify which device the process actually uses. Late configuration changes may have no effect.

## Quick verification

Run package commands from the package root:

```bash
python3 verify_manifest.py
npx wrangler whoami
# Confirm your identity and account after running npx wrangler login.

bash 06_web_tools/cf-api GET /user/tokens/verify
# Only needed for key-file authentication. Expect an active token.

gh auth status
```

Run the build check in your site repository:

```bash
cd <your-site-repo> && nvm use && npm ci && npm run build
rc=$?
echo "build rc=$rc"
```

Capture each command's exit status directly (`rc=$?`), never through a pipe. For example, `cmd | tail` ordinarily reports the status of `tail`.

## Inputs collected at invocation

Site name and slug; build mode; `IS_SITE_PORT` and, if applicable, `OLD_DOMAIN`; design handoff location; form destination and tracking posture; whether previews must be private and who reviews them; and, for hub modes, the Sanity project.

## Troubleshooting

- `Authentication error [code: 10000]` from Wrangler: the credentials in use may not match the pinned account, or another token may have entered through the shell environment. Correct the credentials rather than changing the account pin to fit them.
- `npm: command not found` during a clean-clone check: resolve the active Node executable with `node -p 'process.execPath'` and make its containing directory available on the check's `PATH`.
- A preview build fails with “missing a `previews` block”: the branch may have been created from a `main` branch without the required preview configuration. Add the configuration and ensure the preview branch contains it.
- Lighthouse reports “ALL PASS” but produces no report files: Chrome may never have started. Shorten the temporary profile path and rerun. A check that read no results is not a pass.
- A web tool reports that the key file is not mode 600: apply `chmod 600` to the private key file configured during setup.

## Once setup is verified

Return to `05_automations/client-site-first-build/comprehensive_guide.md` and follow its startup instructions.
