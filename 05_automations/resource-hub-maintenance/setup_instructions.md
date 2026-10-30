# Resource Hub Maintenance: setup instructions (generic edition)

> What Voidwright needs on your machine (macOS, Linux, or Windows through WSL2) before maintaining a hub. The site itself
> (repository, hosting project, first deploy) is covered by the package's guides:
> `09_guides/GITHUB_SETUP.md`, `09_guides/DEPLOY_CLOUDFLARE.md` and `09_guides/DEPLOY_VERCEL.md`.
> This file lists only the additional maintenance requirements.

## System requirements

| Requirement | Version | Check |
|---|---|---|
| Node.js | the version pinned by your repository | `node --version` |
| npm | 10+, compatible with your repository | `npm --version` |
| Git, with access to your site repo | 2.x | `git -C <your-site-repo> ls-remote origin > /dev/null; echo rc=$?` checks read access; confirm push permission separately |
| Python | 3.10+ | `python3 --version` |
| Playwright + Chromium | the version installed for your repository | `npx playwright --version`; also confirm Chromium can launch |
| Voidwright reference material | included package files | Confirm `02_memory/webdev_pack.json` and `02_memory/recall_battery.json` are readable |

## 1. Your key file

Keep the keys used by the package's tools in ONE file that only you can read. The tools parse it; they do not source it as shell code.

```bash
mkdir -p ~/.config/webtools && chmod 700 ~/.config/webtools
touch ~/.config/webtools/keys.env && chmod 600 ~/.config/webtools/keys.env
ls -l ~/.config/webtools/keys.env      # must show -rw------- (mode 600)
```

Open the file in your editor and add, one per line, `NAME=value` with no quotes and no spaces around `=`:

| Key | When you need it |
|---|---|
| `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` | the hub runs on Cloudflare and you use `06_web_tools/wrangler-safe` or `06_web_tools/cf-api`; interactive Wrangler use can instead authenticate with `npx wrangler login` |
| `CF_ACCESS_CLIENT_ID`, `CF_ACCESS_CLIENT_SECRET` | only if your previews sit behind Cloudflare Access |
| `SANITY_API_TOKEN` | when writing to Sanity, using a token with the required project permissions from sanity.io/manage; reads of a public dataset need no token |
| `DEPLOY_HOOK_URL` | when you configure a hosting platform's deploy hook; treat the URL as a secret |

Never paste a value into chat, the repo, stored notes or a log. For the rationale and verification steps, see:
`05_automations/resource-hub-maintenance/runbook_appendix/second_account_sanity_and_external_writer.md`.

## 2. A clean environment for wrangler

If your hub runs on Cloudflare, call Wrangler through the package's wrapper. It removes other Cloudflare
variables from the command environment, loads your key file's values, and refuses when the repo pins a different account.

Set `VOIDWRIGHT_ROOT` to the absolute path of your extracted package before running:

```bash
cd <your-site-repo>
bash "${VOIDWRIGHT_ROOT:?Set VOIDWRIGHT_ROOT to the package directory}/06_web_tools/wrangler-safe" whoami
wrangler_status=$?
echo "whoami rc=$wrangler_status"
```

The account it names must be the intended account for the site. On Vercel, run `npx vercel login` once and `npx vercel whoami` instead.

## 3. Sanity reachability (read-only)

```bash
curl -sS --fail --get \
  "https://<your-sanity-project-id>.api.sanity.io/v2024-01-01/data/query/production" \
  --data-urlencode 'query=count(*)'
sanity_status=$?
echo
echo "Sanity read rc=$sanity_status"
```

A JSON `result` (0 on a new project) proves the public read path. The project ID is in your site's Sanity client
configuration. Replace `production` if your dataset has another name. If your dataset is private, reads need a token too:
see `05_automations/resource-hub-maintenance/runbook_appendix/sanity_content_ops.md`.

## 4. Agents and skills

- Make the included agent definitions available to your agent runner:
  `05_automations/agents/design-generator.md`,
  `05_automations/agents/design-reflector.md` and
  `05_automations/agents/design-curator.md`.
- Make the relevant package skills available:
  `03_skills/resource-hub-thinking/SKILL.md`,
  `03_skills/resource-hub-resource-page-builder/SKILL.md`,
  `03_skills/resource-slug-design-canonical/SKILL.md`,
  `03_skills/design-architect-thinking/SKILL.md`,
  `03_skills/website-maintenance-thinking/SKILL.md`,
  `03_skills/aeo-optimization/SKILL.md`,
  `03_skills/agent-readiness-frontier/SKILL.md` and
  `03_skills/webgl-craft/SKILL.md`.
- For planning and structured review, use
  `04_reasoning/fable-planning-cognition/SKILL.md` and
  `04_reasoning/commands/inner-council.md`.

## 5. Gate tooling

Install the HTML and CSS parsing dependencies in your Python environment, then install the browser audit dependencies in the site repository:

```bash
python3 -m pip install beautifulsoup4 tinycss2
npm i -D @axe-core/playwright lighthouse
```

These dependencies support HTML, CSS, accessibility and page audits; installing them does not run or pass those checks.

Export a short, writable `TMPDIR`, `TEMP` and `TMP` in any Lighthouse runner. If these point somewhere unsuitable, Lighthouse can leave temporary browser-profile folders in the working directory.

## Quick verification

Run these checks with `VOIDWRIGHT_ROOT` set to your package directory:

```bash
node --version
node_status=$?
echo "node rc=$node_status"

ls -l ~/.config/webtools/keys.env
keys_status=$?
echo "keys file rc=$keys_status"

python3 -c 'import json, pathlib, sys; root = pathlib.Path(sys.argv[1]); json.loads((root / "02_memory/webdev_pack.json").read_text()); json.loads((root / "02_memory/recall_battery.json").read_text()); print("Reference JSON is readable and valid")' "${VOIDWRIGHT_ROOT:?Set VOIDWRIGHT_ROOT to the package directory}"
reference_status=$?
echo "reference files rc=$reference_status"
```

Each check prints its own `rc`; never infer a command's status from the final command in a pipe. Inspect the key file's permissions separately: successful listing alone does not prove mode 600. Valid reference JSON confirms file availability, not successful recall.

## Not in this maintenance setup

- Domain, DNS, security headers and production go-live: see `05_automations/website-maintenance/setup_instructions.md`.
- A whole new site, including its repository, hosting project and first deploy: see `05_automations/client-site-first-build/setup_instructions.md`.
- Additional shared knowledge services, private command-line tools and messaging integrations are not required. Use the included reference material, the Sanity HTTP API with your own token, and the structured review guidance in `04_reasoning/commands/inner-council.md`.
