# Setup Instructions: Website Maintenance (generic edition)

> What you need on your machine (macOS, Linux, or Windows through WSL2) to maintain a site you already own and run. For a new site's first build, use `05_automations/client-site-first-build/setup_instructions.md`.
>
> Placeholders used below: `<workbench-root>` (your local Voidwright package directory), `<your-site-repo>` (your local site checkout), `<your-github-user>/<your-repo>`, `<your-domain>`, and `<your-private-key-file>` (a private file outside the repository). Replace them with your own values.

## 1. Node.js (match the repo)
```bash
node --version
cd <your-site-repo>
# Read the repository's Node version declaration, if present:
cat .nvmrc 2>/dev/null
```
Use nvm, fnm or Volta to match the repository's declared Node version. Check that it meets the requirements of the Astro version used by the project. Install dependencies with `npm ci` from the committed lockfile.

## 2. Your repo on GitHub
If the site is not on GitHub yet, follow `09_guides/GITHUB_SETUP.md`.
```bash
git clone https://github.com/<your-github-user>/<your-repo>.git <your-site-repo>
cd <your-site-repo>
git switch preview || git switch -c preview
```
Use `main` for production and `preview` (or another working branch) for preview deployments. Merge to `main` only after the build and verification checks pass and you have inspected the preview. Enable branch protection where your GitHub plan supports it; otherwise, apply the same review discipline yourself.

## 3. Your hosting account
- **Cloudflare Workers** (this edition's primary path): follow `09_guides/DEPLOY_CLOUDFLARE.md`.
- **Vercel** (alternative): follow `09_guides/DEPLOY_VERCEL.md` and sign in with `vercel login` (the CLI keeps its own login).

### Your Cloudflare key file
Keep the credentials needed by the web tools in one private file you own, with mode 600. Use `09_guides/keys.env.example` and `06_web_tools/README.md` to configure the file location expected by the tools. The tools parse the file rather than sourcing it. Never put a key in the repo, in a chat, or on a command line.
```bash
# Choose a private directory outside the repository.
mkdir -p <your-private-config-directory>
chmod 700 <your-private-config-directory>
touch <your-private-key-file>
chmod 600 <your-private-key-file>
"${EDITOR:-nano}" <your-private-key-file>
```
Lines it can hold (one `NAME=value` per line):

| Name | Needed for |
|---|---|
| `CLOUDFLARE_API_TOKEN` | Cloudflare API authentication using a scoped token you create under your own Cloudflare user |
| `CLOUDFLARE_ACCOUNT_ID` | Account-scoped Cloudflare calls |
| `CLOUDFLARE_ZONE_ID` | Optional: DNS and other zone-scoped calls |
| `CF_ACCESS_CLIENT_ID`, `CF_ACCESS_CLIENT_SECRET` | Optional: terminal access to previews protected by Cloudflare Access |

Give the token only what maintenance needs: Workers scripts (edit), Workers Builds (read), D1 (edit, only if the site uses D1), account settings (read), and the zone's DNS (read; edit only when you intend to change records). Verify the current permission names and scope each permission to the accounts and zones you manage.

Check the token through the package's wrapper, which reads the configured file without sourcing it:
```bash
cd <your-site-repo>
bash <workbench-root>/06_web_tools/wrangler-safe whoami
```
`npx wrangler login` (browser sign-in) is an alternative when you work alone on one account. If your repository's Wrangler configuration pins `account_id`, a token without access to that account will fail authentication. Check the intended account before changing either setting.

## 4. Preview access (optional)
Previews may be accessible to anyone with the link unless you protect them. To protect them, use Cloudflare Access (see `09_guides/DEPLOY_CLOUDFLARE.md`) or Vercel Deployment Protection (see `09_guides/DEPLOY_VERCEL.md`). If you use Access and want terminal checks, create a service token in your Zero Trust dashboard, authorize it in the preview Access policy, and put its two values in your key file as `CF_ACCESS_CLIENT_ID` and `CF_ACCESS_CLIENT_SECRET`. `06_web_tools/preview_url_watch.py` uses these credentials as request headers without printing their values.

## 5. Verification tooling
```bash
npm install -g lighthouse            # or run it with npx
npx playwright install chromium
# Ask Playwright for its Chromium executable:
export CHROME_PATH="$(node -e 'process.stdout.write(require("playwright").chromium.executablePath())')"
```
Run the executable lookup from a repository where Playwright is installed. This avoids hard-coding a browser cache path that differs between operating systems. Lighthouse can use that Chromium binary; axe runs through `@axe-core/playwright` in your project's verification code.

If Lighthouse inherits a temporary-directory setting that is missing or not writable, set `TMPDIR`, `TEMP` and `TMP` to an existing, writable temporary directory before running it.

## 6. Secrets hygiene
```bash
gitleaks version        # install via your package manager
pre-commit --version    # pipx install pre-commit; then in the repo: pre-commit install
```
Configure the repository's hooks to run the intended secret checks. Installing the hook manager alone does not enable a secret scanner.

## 7. Package memory
The package includes reference material and recall queries. Check that you can locate the guidance needed for maintenance:
```bash
cd <workbench-root>
rg -n -i 'preview|deploy|workers' \
  02_memory/webdev_pack.json \
  05_automations/website-maintenance/startup_queries.json \
  05_automations/website-maintenance/recall_phrases.json
```
`05_automations/website-maintenance/recall_phrases.json` lists recall phrases and the topics they serve. Treat the phrases as search terms. If a phrase returns nothing useful, search with the topic words instead. See `02_memory/PACK_MANIFEST.md` for the memory pack's contents.

## 8. Agents and skills
- Agent definitions are included in `05_automations/agents/design-generator.md`, `05_automations/agents/design-reflector.md`, and `05_automations/agents/design-curator.md`. Configure them for your chosen agent environment using `SETUP_GUIDE.md`.
- Relevant skills include `03_skills/website-maintenance-thinking/SKILL.md`, `03_skills/webgl-craft/SKILL.md`, `03_skills/corporate-graphic-design/SKILL.md`, `03_skills/design-architect-thinking/SKILL.md`, `03_skills/astro-website-page-creation/SKILL.md`, `03_skills/aeo-optimization/SKILL.md`, `03_skills/agent-readiness-frontier/SKILL.md`, and `03_skills/web-app-building/SKILL.md`.
- Planning and review guidance is available in `04_reasoning/fable-planning-cognition/SKILL.md` and `04_reasoning/commands/inner-council.md`.

## 9. Hardware requirements
Nothing in this automation requires a GPU. A machine that can run the site's Node dependencies, build tools and browser checks is sufficient.

## First-time check
```bash
node --version
cd <your-site-repo>
npx --no-install wrangler --version
gitleaks version
pre-commit --version
```
Confirm that the package references are readable:
```bash
cd <workbench-root>
test -r 02_memory/webdev_pack.json
test -r 05_automations/website-maintenance/startup_queries.json
```
Then run a clean build:
```bash
cd <your-site-repo>
npm ci &&
  env -u CLOUDFLARE_ACCOUNT_ID -u CLOUDFLARE_API_TOKEN npm run build
```
Check the exit status and build output before proceeding to preview verification.

## Troubleshooting
- **An account check refuses a local build**: your shell may export an account ID that differs from the repository configuration. Check both, then try `env -u CLOUDFLARE_ACCOUNT_ID -u CLOUDFLARE_API_TOKEN npm run build` to exclude inherited credentials from the build.
- **Preview build fails with “missing a `previews` block”**: the working branch may lack the required preview configuration. Compare it with a branch whose preview deployment works, then copy only the needed configuration. See `09_guides/DEPLOY_CLOUDFLARE.md`.
- **Form posts fail only locally**: if the project uses a separate local upstream server, check its address and try `npx wrangler dev --local-upstream localhost`.
- **A CLI hangs with no output in a background shell**: it may be waiting for an interactive credential prompt. Check for that prompt, or use the configured key-file route through `06_web_tools/wrangler-safe`.
