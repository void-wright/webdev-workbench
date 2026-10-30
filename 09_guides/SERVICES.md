# Outside services: keys, spending caps, and the no-key route

## What you will have at the end

- A choice of optional services, each with a manual route that needs no key.
- One private file for any keys you choose to use.
- A spending limit chosen before you use a paid service.
- Safe checks that never display your keys.
- A way to replace or remove each key.

## Before you start

The workbench's skills and automations can use outside services.
**None is required. Use only the ones you choose.**
Each service runs on your account, with your permission and spending choices.
A manual route needs no API key, but it may still cost money.

An API is a way for software to ask another service to do something.
An API key or token is a secret that authorizes those requests.
A spending cap stops further spending. An alert only sends a warning.
Where a paid service has no suitable hard cap, choose the free route or leave it disabled.

Have the package folder, your own terminal, and a browser ready.
A terminal is the application where you type commands.
Allow about 15 minutes for the private file and 10 to 20 minutes per chosen service.
Account verification can take longer.

You need Python 3 for the helper.
For the deployment checks, you also need Node.js and npm, its package installer.
Ask your Claude Code agent to help check these tools without handling your keys.

**In your own terminal:**

```bash
python3 --version
```

For deployment checks only:

**In your own terminal:**

```bash
node --version
npm --version
```

Look for a version number from each command.
If a command is missing, finish your workbench tool setup first.
You need accounts only for the services you choose.

## Section A: The one private key file

### Step 1: Find the package folder

Find the folder containing `09_guides/keys.env.example` and `09_guides/with_keys.py`.
The helper reads selected values privately and passes them to one command.
It is package code, so use the copy supplied with your workbench.

A repository, often shortened to repo, is the folder whose project history you save.
Your key file belongs outside every repository.

Check: You can locate both supplied files without opening any existing secret file.

### Step 2: Read the storage rules

- Never paste a key into a chat with any AI.
- Never commit the private file, meaning save it in repository history.
- Never print, copy, or `source` the private key file.
- Never put a key directly on a command line. History and process lists can expose it.
- Give a local command a key only through `with_keys.py`.
- Enter secrets yourself, in your own terminal or private editor.
- Use the hosting platform's secret store when a hosted application needs secrets.
- Keep no extra key files in the project.

The file format is one `KEY=value` per line.
Do not add quotes or `export`.
Comment lines begin with `#`.

This is the layout reference, not a command to run:

```text
CLOUDFLARE_API_TOKEN=
CLOUDFLARE_ACCOUNT_ID=
CLOUDFLARE_ZONE_ID=
CF_ACCESS_CLIENT_ID=
CF_ACCESS_CLIENT_SECRET=
VERCEL_TOKEN=
VERCEL_AUTOMATION_BYPASS_SECRET=
GEMINI_API_KEY=
SANITY_API_TOKEN=
DEPLOY_HOOK_URL=
```

Leave unused entries EMPTY (nothing after `=`). The workbench web tools (`cf-api`, `wrangler-safe`, `bearer-curl`,
`forms-check`, `builds_watch.py`, `preview_url_watch.py`) and `with_keys.py` all read this one file, and they treat an
empty entry as missing.
An account ID identifies an account. Store it here alongside its token.

Check: You know which entries you need and which will remain unused.

### Step 3: Create the private folder and file

Replace `<the package folder>` with the full path to your downloaded package.
Keep the surrounding quotation marks.
The guarded copy below preserves an existing key file.

**In your own terminal:**

```bash
mkdir -p ~/.config/webtools && chmod 700 ~/.config/webtools
[ -f ~/.config/webtools/keys.env ] || cp "<the package folder>/09_guides/keys.env.example" ~/.config/webtools/keys.env
chmod 600 ~/.config/webtools/keys.env
ls -l ~/.config/webtools/keys.env
```

`~` means your home folder.
Permission mode `700` restricts the directory to your user.
Mode `600` lets only your user read and write the file.

Check: The file's permission field begins with `-rw-------`.

### Step 4: Install the helper

Replace `<the package folder>` with the same full path.

**In your own terminal:**

```bash
cp "<the package folder>/09_guides/with_keys.py" ~/.config/webtools/with_keys.py
python3 ~/.config/webtools/with_keys.py --check CLOUDFLARE_API_TOKEN,CLOUDFLARE_ACCOUNT_ID
```

The check reports `present`, `missing` (absent or empty), or `placeholder` (an old `REPLACE_WITH...` value) for each name.
It never prints a value.
A `present` result means a value exists, not that the vendor accepts it.

Check: The helper reports a status for both names without showing their values.

### Step 5: Learn how to save one value

Run this block each time a service section tells you to save a key.
Replace `CLOUDFLARE_API_TOKEN` on the first line with the exact key name from that section.
At the hidden prompt, enter the value yourself.
Nothing should appear while you enter it.

**In your own terminal:**

```bash
python3 - CLOUDFLARE_API_TOKEN <<'PYEOF'
import getpass, os, re, sys
p = os.path.expanduser('~/.config/webtools/keys.env')
name = sys.argv[1]
k = getpass.getpass(name + ' (input hidden): ').strip()
t = open(p).read()
t = re.sub(r'(?m)^' + re.escape(name) + r'=.*$', lambda m: name + '=' + k, t) if re.search(r'(?m)^' + re.escape(name) + '=', t) else t + '\n' + name + '=' + k + '\n'
open(p, 'w').write(t); os.chmod(p, 0o600); print('saved', name, '(value not shown)')
PYEOF
```

If Python warns that hidden input is unavailable, cancel with Ctrl+C.
Run it in your own interactive terminal instead.

Check: You see the saved name and “value not shown”, never the value.

## Section B: Image generation

The design and art-direction skills can request draft images through Google's Gemini API (as of October 2026; re-check before relying on it). [Image documentation](https://ai.google.dev/gemini-api/docs/image-generation)

### Step 1: Use your own account

**In your browser:** Open [AI Studio](https://aistudio.google.com/) and sign in with your own Google account (as of October 2026; re-check before relying on it). [Account and key setup](https://ai.google.dev/gemini-api/docs/api-key)

Keep workbench experiments separate from other projects.
Use invented material, such as a window illustration for Crumb & Crust Bakery.

Check: You are signed into the account you intend to use.

### Step 2: Create the narrowest key

**In your browser:** Choose **Get API key** and create a new Google Cloud project used only for this workbench (as of October 2026; re-check before relying on it). [Key setup](https://ai.google.dev/gemini-api/docs/api-key)

A project groups service settings, usage, and billing.
Create the key in that project.

**In your browser:** For a standard API key, open Google Cloud console > **APIs & Services > Credentials**, select the key, and restrict its API access to **Generative Language API** (as of October 2026; re-check before relying on it). [API key documentation](https://cloud.google.com/api-keys/docs)

Key types and available restrictions can change. Follow the current key documentation if your screen differs (as of October 2026; re-check before relying on it). [Gemini key documentation](https://ai.google.dev/gemini-api/docs/api-key)

Check: The key belongs to the dedicated project and has the narrowest supported access.

### Step 3: Set the spending limit first

The free tier needs no linked billing account and has rate limits, meaning limits on request frequency or volume (as of October 2026; re-check before relying on it). [Billing](https://ai.google.dev/gemini-api/docs/billing)

When free quota is exhausted, requests fail, commonly with HTTP 429, instead of becoming paid requests automatically (as of October 2026; re-check before relying on it). [Rate limits](https://ai.google.dev/gemini-api/docs/rate-limits)

A free API account does not guarantee free image generation. Check the selected model's availability and pricing first (as of October 2026; re-check before relying on it). [Pricing](https://ai.google.dev/gemini-api/docs/pricing)

Paid usage requires billing setup (as of October 2026; re-check before relying on it). [Billing](https://ai.google.dev/gemini-api/docs/billing)
For a zero-spend limit, leave billing unlinked.

**In your browser:** If you enable billing, open **Billing > Budgets & alerts** and create a project budget with alerts at 50%, 90%, and 100% (as of October 2026; re-check before relying on it). [Budget instructions](https://cloud.google.com/billing/docs/how-to/budgets)

**An alerts-only budget does not stop charges** (as of October 2026; re-check before relying on it). [Budget limitations](https://cloud.google.com/billing/docs/how-to/budgets)
To stop future paid use, unlink project billing. Deleting a key stops requests using that key, not other credentials or existing charges (as of October 2026; re-check before relying on it). [Billing](https://ai.google.dev/gemini-api/docs/billing), [Keys](https://ai.google.dev/gemini-api/docs/api-key)

Google may use free-service prompts and outputs to improve its products (as of October 2026; re-check before relying on it). [Terms](https://ai.google.dev/gemini-api/terms)
Do not submit private material on the free tier.

Check: Billing is unlinked, or you have deliberately accepted paid use and verified its spending controls.

### Step 4: Save the key

Use Section A, Step 5.
Enter the exact name `GEMINI_API_KEY`, then enter the key at the hidden prompt.

**In your own terminal:**

```bash
python3 ~/.config/webtools/with_keys.py --check GEMINI_API_KEY
```

Check: The helper reports `present` without displaying the key.

### Step 5: Run a free test

Listing models makes no image-generation request and has no generation charge (as of October 2026; re-check before relying on it). [Models API](https://ai.google.dev/api/models), [Pricing](https://ai.google.dev/gemini-api/docs/pricing)

**In your own terminal:**

```bash
python3 ~/.config/webtools/with_keys.py GEMINI_API_KEY -- python3 -c "import json,os,urllib.request; r=urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/models', headers={'x-goog-api-key': os.environ['GEMINI_API_KEY']}); d=json.load(urllib.request.urlopen(r, timeout=30)); print('OK:', len(d.get('models', [])), 'models visible to this key')"
```

The count covers the returned list. It does not prove you can generate images.
An HTTP status is a numbered response from a web service.

**In your browser:** Read the current image model name and supported settings in the [image-generation guide](https://ai.google.dev/gemini-api/docs/image-generation) (as of October 2026; re-check before relying on it).
Give your agent the model name, never the key.

Check: The command prints an `OK:` verdict and a model count.

### Step 6: Rotate or remove

Rotating a key means replacing it with a new secret.

**In your browser:** In **Credentials**, use the key's regeneration option if available, or delete it and create a replacement with the same restrictions (as of October 2026; re-check before relying on it). [Key management](https://cloud.google.com/api-keys/docs)

Update `GEMINI_API_KEY` through Section A, Step 5, then repeat the test.
To stop using it, revoke the key and empty the local value: run Section A, Step 5 with the same name and press Enter at the hidden prompt.

Check: The old key is revoked, and the replacement passes or the local entry is empty.

### The manual route (no key)

Ask the skill to write the exact prompt, image size, settings, destination folder, and filename into a handoff file.
A handoff file is a set of instructions for work you perform yourself.
**Before spending credits, read the prompt and compare it with the page plan.**

**In your browser:** Open [AI Studio](https://aistudio.google.com/) or the Gemini app, and check the image tools and charges available to your account (as of October 2026; re-check before relying on it). [Image guidance](https://ai.google.dev/gemini-api/docs/image-generation)
Paste the prompt, choose supported settings, generate, and download the image.
Save it using the exact folder and filename in the handoff.
Tell Claude where you saved it.

Check: The image exists at the requested path and matches the page plan.

## Section C: Short video passages

The scroll-journey skill uses short video passages between still images.
This package uses Google Flow manually and has no Flow API key integration.

### Step 1: Use your own account

**In your browser:** Open [Flow](https://labs.google/flow) with your own Google account and inspect available access and subscription options (as of October 2026; re-check before relying on it).
Choose any subscription yourself. Some accounts may also have access without a subscription (as of October 2026; re-check before relying on it). [Flow options](https://labs.google/fx/tools/flow)

Check: You know which account and access option you will use.

### Step 2: Choose the narrowest access

No key is needed for this package's Flow route.
Keep the work in your own browser session.
Do not add a Flow key or account password to `keys.env`.

Check: You have not created or shared a credential for Flow automation.

### Step 3: Set the spending limit first

Monthly credits, generation costs, available models, and subscription terms can change (as of October 2026; re-check before relying on it). [Flow credit help](https://support.google.com/flow/answer/16526234)
Credits are units consumed by generation. Unused monthly credits do not roll over under the documented rules (as of October 2026; re-check before relying on it). [Credit rules](https://support.google.com/flow/answer/16526234)

**In your browser:** Check the credit cost before each clip and any recurring subscription charge (as of October 2026; re-check before relying on it). [Flow](https://labs.google/flow)
Use the subscription charge as your chosen monthly ceiling.
Do not buy extra credit packs unless you deliberately raise that ceiling.
If your account offers automatic top-ups, leave them disabled.

Check: You know your recurring cost and have made no extra-credit purchase.

### Step 4: Keep keys out of this route

There is nothing to save in the private key file.
Ask the skill for each passage's prompt, first frame, last frame, planned duration, and output path.
Duration means the clip's running time.

Check: Your handoff contains every passage and both frame images.

### Step 5: Perform a no-generation check

**In your browser:** Open Flow and inspect your account's credit balance without generating anything (as of October 2026; re-check before relying on it). [Credit help](https://support.google.com/flow/answer/16526234)
Read every prompt and inspect every frame image.
Report “Ready” to Claude only when the inputs and spending choice are correct.
This is a readiness check, not a free sample generation.

Check: You can report “Ready” without having spent generation credits.

### Step 6: Remove access or stop renewing

There is no package key to rotate.

**In your browser:** Use your subscription's management page to cancel renewal if you no longer want paid access (as of October 2026; re-check before relying on it). [Google subscription help](https://support.google.com/googleone/)
Check the stated end date and save any clips you need.

Check: You have confirmed the subscription status and retained your chosen clips.

### The manual route (no key)

**In your browser:** Create a Flow project, choose the available frames-to-video mode, and add the first and last frame images (as of October 2026; re-check before relying on it). [Flow help](https://support.google.com/flow/)
Paste the passage prompt and choose the nearest supported length at or above the planned duration.
Trim a longer clip later. Never pad a shorter clip to hide missing footage.
**Review the prompt and both frames before generating.**
Regeneration can consume more credits (as of October 2026; re-check before relying on it). [Credit help](https://support.google.com/flow/answer/16526234)

Generate and download the clip as MP4 where that download format is offered (as of October 2026; re-check before relying on it). [Flow help](https://support.google.com/flow/)
Save it under the handoff's exact filename and folder.
Tell Claude to check and normalize the clip, meaning convert it to the project's required media settings.

Check: Claude confirms the saved clip meets the passage requirements.

## Section D: Cloudflare API

This route supports local deployments and the workbench's Cloudflare helpers.
Deploying means publishing a project to its hosting service.

### Step 1: Use your own account

**In your browser:** Sign into your own Cloudflare account and select the intended account (as of October 2026; re-check before relying on it). [Workers setup](https://developers.cloudflare.com/workers/get-started/)
Find its account ID and keep it ready for the hidden-input prompt (as of October 2026; re-check before relying on it). [Account ID help](https://developers.cloudflare.com/fundamentals/account/find-account-and-zone-ids/)

Check: You recognize the account selected for deployment.

### Step 2: Create the narrowest key

**In your browser:** Open **My Profile > API Tokens**, create a custom token, select one account, and set an expiry (as of October 2026; re-check before relying on it). [Token creation](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/)

Use these permission rows where offered (as of October 2026; re-check before relying on it). [Workers authorization](https://developers.cloudflare.com/workers/authorization/)

- Account > Workers Scripts > Edit.
- Account > Account Settings > Read.
- User > User Details > Read.
- User > Memberships > Read.

For custom domains managed through Wrangler, add **Zone > Workers Routes > Edit** and **Zone > DNS > Edit**, scoped to one zone (as of October 2026; re-check before relying on it). [Permissions](https://developers.cloudflare.com/fundamentals/api/reference/permissions/)
A zone is the domain managed in that account.
Add **Account > Workers Builds Configuration > Edit** only if you use the workbench's `builds_watch.py`, which reads your Worker's builds through the Builds API; without this row it stops with exit code 4. The Builds API accepts only tokens created under My Profile, as in this step, not account-owned tokens (as of October 2026; re-check before relying on it). [Builds API](https://developers.cloudflare.com/workers/ci-cd/builds/api-reference/)
Add database, key-value storage, or access-control permissions only for features you use.
Cloudflare names those services D1, KV, and Access (as of October 2026; re-check before relying on it). [Documentation](https://developers.cloudflare.com/)

Check: The token has an expiry and no unrelated account, zone, or feature access.

### Step 3: Set the spending limit first

Workers Free enforces usage limits instead of automatically billing Workers overages (as of October 2026; re-check before relying on it). [Limits](https://developers.cloudflare.com/workers/platform/limits/)
Other enabled products have their own billing rules (as of October 2026; re-check before relying on it). [Pricing](https://developers.cloudflare.com/workers/platform/pricing/)

**In your browser:** Verify the selected plan. If using Workers Paid, set available billing notifications before deploying (as of October 2026; re-check before relying on it). [Billing documentation](https://developers.cloudflare.com/billing/)
Notifications are not a hard spending cap.
For a strict zero-spend setup, stay on free services within their limits.

Check: You have verified the plan and have not mistaken notifications for a spending stop.

### Step 4: Save both values

Use Section A, Step 5 twice.
Save `CLOUDFLARE_API_TOKEN`, then `CLOUDFLARE_ACCOUNT_ID`.

**In your own terminal:**

```bash
python3 ~/.config/webtools/with_keys.py --check CLOUDFLARE_API_TOKEN,CLOUDFLARE_ACCOUNT_ID
```

Check: Both names report `present`.

### Step 5: Run a free test

Wrangler is Cloudflare's command-line tool. Its `whoami` command reports identity and permissions without deploying anything (as of October 2026; re-check before relying on it). [Wrangler commands](https://developers.cloudflare.com/workers/wrangler/commands/)
This identity check does not create billable hosting work (as of October 2026; re-check before relying on it). [Commands](https://developers.cloudflare.com/workers/wrangler/commands/)

**In your own terminal:**

```bash
python3 ~/.config/webtools/with_keys.py CLOUDFLARE_API_TOKEN,CLOUDFLARE_ACCOUNT_ID -- npx wrangler@4 whoami
```

`npx` runs the selected package command. It may first ask to download the package.
Read the installation prompt before accepting.

Check: The reported account and permissions match your intended token.

After the workbench is installed, the web tools read the same file. A second free check, through Cloudflare's own
token-verify endpoint (it prints JSON with `"status": "active"`, never the token):

**In your own terminal:**

```bash
bash ~/.local/share/webdev-workbench/web_tools/cf-api GET /user/tokens/verify
```

If you also want the optional `CLOUDFLARE_ZONE_ID` (for `cf-api` paths that name a zone), copy it from your domain's
overview page and save it with Section A, Step 5.

### Step 6: Rotate or remove

**In your browser:** Open **My Profile > API Tokens**, select the token, and use **Roll** to replace it, or revoke it to stop using it (as of October 2026; re-check before relying on it). [Token management](https://developers.cloudflare.com/fundamentals/api/get-started/)
Save a replacement through Section A, Step 5, and repeat `whoami`.
For removal, empty the local entry (Section A, Step 5, then press Enter at the hidden prompt).

Check: The old token is invalid and the local entry reflects your choice.

### The manual route (no key)

**In your browser:** Follow `DEPLOY_CLOUDFLARE.md`, Step 5, to connect the repository through Workers Builds (as of October 2026; re-check before relying on it). [Git integration](https://developers.cloudflare.com/workers/ci-cd/builds/)
Configured branch pushes can then build and deploy on Cloudflare's side without a local API token (as of October 2026; re-check before relying on it). [Build configuration](https://developers.cloudflare.com/workers/ci-cd/builds/configuration/)
Manage Access, DNS, and rollbacks in the dashboard (as of October 2026; re-check before relying on it). [Documentation](https://developers.cloudflare.com/)

Check: The connected repository deploys through the dashboard workflow.

## Section E: Vercel API

This route supports commands run from your own machine.

### Step 1: Use your own account

**In your browser:** Sign into Vercel and select the account or team that will own the project (as of October 2026; re-check before relying on it). [Getting started](https://vercel.com/docs/getting-started-with-vercel)

Check: You recognize the selected owner.

### Step 2: Create the narrowest key

**In your browser:** Open [account tokens](https://vercel.com/account/tokens), create a token, select one team instead of Full Account where offered, and set an expiration (as of October 2026; re-check before relying on it). [Token documentation](https://vercel.com/docs/rest-api/reference/welcome#creating-an-access-token)

Check: The token has the narrowest offered scope and an expiry.

### Step 3: Set the spending limit first

Hobby is the no-bill option for eligible personal, non-commercial use (as of October 2026; re-check before relying on it). [Hobby plan](https://vercel.com/docs/plans/hobby)
An invented bakery exercise can be personal practice. An actual business site needs an appropriate plan.

**In your browser:** Before paid use on Pro, configure Spend Management, including its available pause action rather than alerts alone (as of October 2026; re-check before relying on it). [Spend Management](https://vercel.com/docs/spend-management)
Review what the control covers. A usage limit does not erase subscription charges or guarantee instantaneous enforcement (as of October 2026; re-check before relying on it). [Spend Management](https://vercel.com/docs/spend-management)

Check: Your plan fits your use, and you understand the selected spending controls.

### Step 4: Save the key

Use Section A, Step 5, with `VERCEL_TOKEN`.

**In your own terminal:**

```bash
python3 ~/.config/webtools/with_keys.py --check VERCEL_TOKEN
```

Check: The helper reports `present`.

### Step 5: Run a free test

Install the Vercel CLI once with npm (as of October 2026; re-check before relying on it). [CLI installation](https://vercel.com/docs/cli)

**In your own terminal:**

```bash
npm install -g vercel
python3 ~/.config/webtools/with_keys.py VERCEL_TOKEN -- vercel whoami
```

The CLI supports `VERCEL_TOKEN` from its environment (as of October 2026; re-check before relying on it). [CLI global options](https://vercel.com/docs/cli/global-options)
`whoami` prints the authenticated username without deploying or running a paid workload (as of October 2026; re-check before relying on it). [Command documentation](https://vercel.com/docs/cli/whoami)
If global installation fails, ask your agent to repair npm setup without giving it the key.

Check: The username is yours. Do not accept a different cached account as success.

### Step 6: Rotate or remove

**In your browser:** Delete the old token on the [tokens page](https://vercel.com/account/tokens), then create a replacement if needed (as of October 2026; re-check before relying on it). [Authentication documentation](https://vercel.com/docs/rest-api)
Update `VERCEL_TOKEN` through Section A, Step 5.
For removal, press Enter at the hidden prompt, which empties the entry.

Check: The replacement passes `whoami`, or the entry reports `missing`.

### The manual route (no key)

**In your browser:** Follow `DEPLOY_VERCEL.md`, Step 3, to connect the repository using the Git integration (as of October 2026; re-check before relying on it). [Git deployments](https://vercel.com/docs/git)
Configured pushes deploy on Vercel's side without a local token (as of October 2026; re-check before relying on it). [Git deployments](https://vercel.com/docs/git)
Manage environment variables, domains, protection, and rollbacks in the dashboard (as of October 2026; re-check before relying on it). [Documentation](https://vercel.com/docs)

Check: The project is connected and its deployment appears in the dashboard.

## Section F: Optional Cloudflare Access service token

Use this only for command-line checks of protected previews.
A protected preview is a test site that requires permission to open.
This token is separate from your deployment token.

### Step 1: Use your own account

**In your browser:** Open the account containing your protected preview and its Zero Trust application (as of October 2026; re-check before relying on it). [Access documentation](https://developers.cloudflare.com/cloudflare-one/access-controls/)

Check: You have identified the preview application you intend to test.

### Step 2: Create the narrowest token

**In your browser:** Open **Zero Trust > Access > Service credentials > Service tokens**, create a token, and set a duration (as of October 2026; re-check before relying on it). [Service tokens](https://developers.cloudflare.com/cloudflare-one/access-controls/service-credentials/service-tokens/)
Add that token to the preview application's **Service Auth** policy (as of October 2026; re-check before relying on it). [Service token policies](https://developers.cloudflare.com/cloudflare-one/access-controls/service-credentials/service-tokens/)
A policy is a rule deciding who or what may enter.
Grant access only to the required preview.

Check: The policy selects your token and the intended application.

### Step 3: Set the spending limit first

**In your browser:** Review the account's Zero Trust plan and the preview's hosting plan before making requests (as of October 2026; re-check before relying on it). [Cloudflare billing](https://developers.cloudflare.com/billing/)
Use the free hosting setup from Section D if you need zero spend.
Authentication does not make the application behind it free to run.

Check: Both access and hosting costs fit your chosen limit.

### Step 4: Save both values

Use Section A, Step 5 twice.
Save `CF_ACCESS_CLIENT_ID` and `CF_ACCESS_CLIENT_SECRET`.
Enter both values privately.

Check: Both values are stored under their exact names.

### Step 5: Run a free local test

This check makes no network request and incurs no service charge.
It checks storage only, not whether the preview accepts the token.

**In your own terminal:**

```bash
python3 ~/.config/webtools/with_keys.py --check CF_ACCESS_CLIENT_ID,CF_ACCESS_CLIENT_SECRET
```

For a later live check, have the package tool receive both names through the helper.
Never put secret request headers directly on a command line.

Check: Both names report `present`; live authentication remains untested.

### Step 6: Rotate or remove

**In your browser:** Replace or revoke the service token, and update the application's policy if you replace it (as of October 2026; re-check before relying on it). [Service token management](https://developers.cloudflare.com/cloudflare-one/access-controls/service-credentials/service-tokens/)
Update both local entries through Section A, Step 5.
For removal, empty both entries the same way.

Check: The old token is revoked and no stale policy entry remains.

### The manual route (no key)

**In your browser:** Open the preview and complete its configured login (as of October 2026; re-check before relying on it). [Access documentation](https://developers.cloudflare.com/cloudflare-one/access-controls/)
Keep browser login permission when removing machine-only access.

Check: You can view the preview after signing in.

## Section G: Optional Sanity token (resource hubs)

The resource-hub automation can keep a library of resources in Sanity, a hosted content store, and the web tool
`bearer-curl` can query it. Skip this section unless you build a resource hub.

### Step 1: Use your own account

**In your browser:** Sign in at [sanity.io/manage](https://www.sanity.io/manage) with your own account and open the
project you created for the site (as of October 2026; re-check before relying on it). [Sanity documentation](https://www.sanity.io/docs)

Check: You can see the project and its project ID.

### Step 2: Create the narrowest key

**In your browser:** In the project, open **API > Tokens > Add API token**, name it after this computer, and choose the
narrowest role the work needs: **Viewer** (read only) for checks, an editing role only when an automation must write
(as of October 2026; re-check before relying on it). [API tokens](https://www.sanity.io/docs/http-auth)
The token is shown once.

Check: The token has the role you intended, and no broader one.

### Step 3: Set the spending limit first

Sanity has a free plan with usage quotas (as of October 2026; re-check before relying on it). [Pricing](https://www.sanity.io/pricing)
Stay on it while learning, and do not add a payment method you do not need. On a paid plan, read how overages are
billed before you import a large library.

Check: The project's plan is the one you chose.

### Step 4: Save the key

Use Section A, Step 5, with the name `SANITY_API_TOKEN`.

Check: `python3 ~/.config/webtools/with_keys.py --check SANITY_API_TOKEN` reports `present`.

### Step 5: Run a free test

After the workbench is installed (SETUP_GUIDE.md, P4), this read-only query counts documents and prints the answer,
never the token. Replace `<your-sanity-project-id>` with the project ID and keep the quotes:

**In your own terminal:**

```bash
bash ~/.local/share/webdev-workbench/web_tools/bearer-curl SANITY_API_TOKEN "https://<your-sanity-project-id>.api.sanity.io/v2025-02-19/data/query/production?query=count(*)"
```

Check: The answer is JSON with a `result` number (0 for a new, empty dataset).

### Step 6: Rotate or remove

**In your browser:** Delete the token under **API > Tokens**, and create a new one if needed. Save it with Section A,
Step 5, or empty the entry.

Check: The old token no longer answers the test.

### The manual route (no key)

**In your browser:** Edit the content in your Sanity Studio, the editing website for your project, and publish it there.
The automation writes what to add (titles, fields, files) into a handoff file; you enter it in the Studio and tell
Claude when it is published.

Check: The new entries appear in the Studio and on the site after its next build.

## Section H: Optional deploy hook

A deploy hook is a private URL that starts a new build of your site when something calls it. The resource-hub
automation can call one after content changes. Cloudflare Workers Builds and Vercel both offer them
(as of October 2026; re-check before relying on it). [Workers Builds deploy hooks](https://developers.cloudflare.com/workers/ci-cd/builds/deploy-hooks/),
[Vercel deploy hooks](https://vercel.com/docs/deploy-hooks)

### Step 1: Use your own account

Use the host account that already builds the site (DEPLOY_CLOUDFLARE.md or DEPLOY_VERCEL.md).

Check: The site already builds from its repository.

### Step 2: Create the narrowest key

**In your browser:** Cloudflare: the Worker > **Settings > Builds > Deploy Hooks**; Vercel: the project >
**Settings > Git > Deploy Hooks** (as of October 2026; re-check before relying on it). Create ONE hook for ONE branch,
named after its use. **The URL itself is the secret**: anyone who holds it can start a build.

Check: The hook names the branch you meant.

### Step 3: Set the spending limit first

Every call is a build, and builds count against the host's build limits. The host settings from Section D or E apply.

Check: You know the host's build limit for your plan.

### Step 4: Save the key

Use Section A, Step 5, with the name `DEPLOY_HOOK_URL`.

Check: `python3 ~/.config/webtools/with_keys.py --check DEPLOY_HOOK_URL` reports `present`.

### Step 5: Run a free test

There is no call that tests a hook without starting a build. The presence check in Step 4 is the free test; the first
real use happens when the automation asks, and you watch the build appear in the host's dashboard.

Check: The presence check passes.

### Step 6: Rotate or remove

**In your browser:** Delete the hook in the same settings page and create a new one if needed. Save it with Section A,
Step 5, or empty the entry.

Check: The old hook is gone from the settings page.

### The manual route (no key)

**In your browser:** Start the build yourself: Cloudflare's **Deployments** page or Vercel's **Redeploy** button, or
push a commit to the branch.

Check: A new build of the branch appears and succeeds.

## Service reference

The tests and manual routes below refer to the detailed steps above.

| Service | Used by | Key name | Free test | Manual route |
|---|---|---|---|---|
| Image generation | Design and art-direction skills | `GEMINI_API_KEY` | Model-list count | Generate and download from the handoff |
| Flow | Scroll-journey skill | None | Review inputs without generating | Create and download clips |
| Cloudflare API | Deployments and helper tools | `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` | Wrapped `whoami` | Connected builds and dashboard |
| Vercel API | Local deployment commands | `VERCEL_TOKEN` | Wrapped `whoami` | Git integration and dashboard |
| Access service token | Protected preview checks | `CF_ACCESS_CLIENT_ID`, `CF_ACCESS_CLIENT_SECRET` | Local presence check only | Browser login |
| Sanity | Resource-hub automation, `bearer-curl` | `SANITY_API_TOKEN` | Read-only count query | Sanity Studio |
| Deploy hook | Resource-hub rebuild step | `DEPLOY_HOOK_URL` | Presence check only | Dashboard redeploy or a push |

## Troubleshooting

**Symptom:** The helper reports `missing` or `placeholder`, or a web tool says a key "is missing or empty".
**Cause:** The exact name has no usable value.
**Fix:** Repeat Section A, Step 5, using the service's exact name. Check again without opening the file.

**Symptom:** The key file permissions are broader than `-rw-------`.
**Cause:** Another tool changed the file permissions.
**Fix:** Run the following yourself.

**In your own terminal:**

```bash
chmod 700 ~/.config/webtools
chmod 600 ~/.config/webtools/keys.env
ls -l ~/.config/webtools/keys.env
```

**Symptom:** The image test returns HTTP 400 or 403.
**Cause:** The key, API restriction, project access, or request may be invalid (as of October 2026; re-check before relying on it). [API troubleshooting](https://ai.google.dev/gemini-api/docs/troubleshooting)
**Fix:** **In your browser:** Check the selected project and key restrictions. Replace the key privately if needed.

**Symptom:** Generation returns HTTP 429.
**Cause:** A rate or quota limit may have been reached (as of October 2026; re-check before relying on it). [Rate limits](https://ai.google.dev/gemini-api/docs/rate-limits)
**Fix:** Wait for the documented reset or use the manual route. Do not enable billing automatically.

**Symptom:** A deployment identity check fails.
**Cause:** The token may be expired, revoked, or missing permissions (as of October 2026; re-check before relying on it). [Cloudflare tokens](https://developers.cloudflare.com/fundamentals/api/get-started/), [Vercel authentication](https://vercel.com/docs/rest-api)
**Fix:** **In your browser:** Check its scope and expiry, then replace it through the hidden-input prompt.

**Symptom:** A protected preview rejects a service token.
**Cause:** The token or its application policy may not match (as of October 2026; re-check before relying on it). [Service tokens](https://developers.cloudflare.com/cloudflare-one/access-controls/service-credentials/service-tokens/)
**Fix:** **In your browser:** Check the preview application's Service Auth rule and selected token.

**Symptom:** Spending continues after an alert.
**Cause:** An alert is a notification, not necessarily a stop.
**Fix:** Stop new work and use the service's spending controls described above. Check recurring subscriptions separately.

**Symptom:** A key appeared in chat, history, or a repository.
**Cause:** The secret left its intended storage.
**Fix:** Revoke it immediately, then create a replacement. Deleting visible text does not make the old key safe.

## Undo / remove

### Removing everything

First stop local commands and automations that use these credentials.
**In your browser:** Revoke each API key and service token using its service's Step 6.
Cancel unwanted subscriptions and review paid resources separately.
Deleting a local key does not cancel hosted resources, subscription renewals, or existing charges.

Only after revoking the credentials, delete the private file.

**In your own terminal:**

```bash
rm ~/.config/webtools/keys.env
```

Optionally remove the helper too.

**In your own terminal:**

```bash
rm -f ~/.config/webtools/with_keys.py
```

Verify removal without reading any secret.

**In your own terminal:**

```bash
if [ -e ~/.config/webtools/keys.env ]; then
  printf '%s\n' 'Key file still exists.'
else
  printf '%s\n' 'Key file removed.'
fi
```

Check: The file is removed, vendor credentials are revoked, and unwanted paid services are canceled.