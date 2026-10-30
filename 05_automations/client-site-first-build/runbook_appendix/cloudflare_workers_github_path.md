# Runbook Appendix: The Cloudflare Workers + GitHub First-Build Path

> **Owner**: the person running the first build. Hand-off target: whoever maintains the site after launch.
> **Status**: an end-to-end first-build procedure for Cloudflare Workers + GitHub. **This is the worked path in this edition.** Account setup: `09_guides/DEPLOY_CLOUDFLARE.md` and `09_guides/GITHUB_SETUP.md`.
> **Recall first**: account separation, platform wiring, preview verification, forms and launch requirements.
> **On your machine**: either `npx wrangler login` with your own Cloudflare account, or an API token in a local key file configured for the web tools. Keep that file mode 600; parse it, never source or print it. Run Wrangler through `bash 06_web_tools/wrangler-safe <verb>`. Raw API calls below use `bash 06_web_tools/cf-api <METHOD> <path>`, which fills `{account}` and `{zone}` from the configured credentials. For a shared account, confirm who can authorize changes before writing.
> **Ground truth beats memory text.** Vendor UI names, plan limits and CLI verbs drift. Re-check current behavior before relying on a number, permission name or click path. An assumption about an account is not verified account state.

This is the platform path a first build takes when the site deploys to **Cloudflare Workers with Workers Builds connected to a GitHub repo**. Vercel is the documented alternative in `09_guides/DEPLOY_VERCEL.md`. This file gives the end-to-end order, from setup to launch.

**Why Workers and not Pages**: this procedure uses Workers for custom-domain routes managed through `wrangler.jsonc`, static-asset headers and redirects, and a single Worker entry point for markdown negotiation and `/api/*` through `run_worker_first`. Workers Builds provides the GitHub connection without placing a separate Wrangler deployment token in GitHub Actions secrets. Verify current platform support before choosing the deployment model.

---

## The order (one screen)

| # | Step | Who | Gate before the next step |
|---|---|---|---|
| 1 | Account separation: clean environment, pin, wrong-account probe, reverse census, secret sweep | Build operator | probe answers an auth error; census 0 with coverage reported; sweep 0 |
| 2 | Token probe: permissions AND feature enablement | Build operator + account holder | every blocker listed in one batch |
| 3 | Repo + scaffold + `wrangler.jsonc` + zone hygiene | Build operator | private-repo pair check; parking records backed up and gone |
| 4 | Workers subdomain, first deploy, custom domains, holding page | Build operator | apex 200, www 301, noindex posture |
| 5 | Workers Builds: main trigger + Worker Previews (`previews` block) | Account holder connects GitHub; build operator configures builds | one main trigger; preview proof of concept passes |
| 6 | (optional) Access on previews + service token | Account holder onboards Zero Trust; build operator adds policy | 302 without token, 200 with |
| 7 | Forms: D1 + Turnstile + a transactional email provider | Build operator + account holder | form checks pass on preview; dummy token refused on production |
| 8 | DNSSEC + DNS-AID | Account holder enters DS; build operator writes records | AD flag true; SVCB answers |
| 9 | Markdown negotiation Worker, agent files, indexing posture | Build operator | header posture verified on preview and production hosts |
| 10 | Launch: production posture by build, launch checks, supply-chain holds | Build operator + site owner's go-ahead | agent-readiness checks and probes pass; preview and production postures verified |
| 11 | Hand-off: post-launch change path, standing checks, residuals | Build operator | maintenance notes complete |

---

## 1. Account separation (before any write)

**The hazard**: when the shell exports ambient vendor keys, such as `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` and Sanity variables, tool calls can use those credentials regardless of the current folder. Environment variables can override Wrangler's own login. A naive `wrangler deploy` in a new repo can land in the wrong account.

**The design**:

- Credentials in one key file, mode 600, read by parsing. Never `source` it, which would execute its contents and export its values.
- Thin wrappers that run each tool with a clean environment: either `env -i` plus an **allowlist** of required variables such as HOME, USER, LOGNAME, TERM, LANG and PATH with the Node binary, or removal of every ambient `CLOUDFLARE_*`/`CF_*` variable before the selected key file's values are exported. Prefer the allowlist when writing your own wrapper because a denylist can miss newly introduced variables. The package provides `06_web_tools/wrangler-safe`.
- Pin `account_id` in `wrangler.jsonc`, and make the wrapper **refuse** when the repo's pin differs from the loaded account. Test both ways: a dummy pin refuses, and the real repo runs.
- Wrappers print a banner naming the account's last four characters, so a wrong account is visible before anything runs.
- For GitHub, use a per-command `GH_TOKEN=$(gh auth token --user <account>)`; never change the global account with `gh auth switch` while other sessions run.
- Do not assume vendor connectors use the wrapper's account. Their OAuth sessions are separate; verify their identity independently before use.
- `npm install` runs under the clean environment too.

**Prove it, measured**: count unintended ambient credential variables in the normal shell and inside the wrapper. The wrapper count must be 0. Report counts, never values. This turns an isolation claim into a measured check.

**The wrong-account probe**: `wrangler deploy --dry-run` does not establish that authentication targets the correct account. Use a **logged-in, non-mutating** call, such as `npx wrangler deployments list`, with credentials for another account you control against the pinned account. Pass = an authentication or account-mismatch rejection. A response such as `Authentication error [code: 10000]` may provide that evidence; verify the current CLI behavior rather than depending on exact wording. The error is the pass.

**Reverse census**: perform a read-only listing of the other account's Workers, D1 databases, Turnstile widgets, Web Analytics sites and Access apps, filtered for the new site's name. The result must be 0, and the census must **print the endpoint types it could not read**. Report coverage as checked types out of attempted types. A silent skip creates a false impression of a complete zero result. A hash comparison marked "CHANGED" is not useful evidence of misplaced resources when other writers can change the account.

**Secret sweep**: search for each stored secret's full value plus head, tail and middle fragments. Use a raw-byte scan over planning files, repositories including `git log -p --all --binary`, the workspace, and any local logs or conversation exports used during the build. Never print a value, fragment or length. Use exit codes 0/1/2 for no matches, matches found and incomplete scan or error. Exclude fragment matches contained in declared-public values, since a secret and a public identifier can share a prefix. Continue checking full secret values. Re-run after every rotation and before each deployment milestone.

Re-run the probe, census and sweep before attaching domains and before launch.

---

## 2. Token probe: permissions AND feature enablement

Before any write, run read-only probes through `06_web_tools/cf-api`, for example `bash 06_web_tools/cf-api GET /accounts/{account}/workers/subdomain`:

- Token verification: status and **expiry**. A token without an expiry needs an explicit rotation plan.
- Account type, zone and plan, Workers scripts, D1, Turnstile, Web Analytics, DNS records, DNSSEC state, zone settings, Workers routes, user details and memberships.
- **Feature enablement**, which no permission list reveals: the account's Workers subdomain and Zero Trust onboarding. Responses such as `10007` for an unregistered subdomain or `9999 access.api.error.not_enabled` for unavailable Access configuration can indicate setup work rather than missing token scope. Check the response context and current API behavior. No token edit completes feature onboarding.

Batch every required human dashboard step into one request. GET requests prove read scope only; prove each EDIT permission at its first authorized write.

**Human guides**: write each dashboard step for someone new to the service. Include expected time and prerequisites, the reason for the step, a You/Me responsibility box, and steps with "what you should see." Include a wrong-account tell, such as the visible account name or email. Give a permission table with reasons and make the **LEVEL (Read vs Edit) as prominent as the name**. Present optional steps as boxed decisions, put dangers BEFORE the click, and include an exact report-back phrase and troubleshooting guidance. Use a private browser window for token setup to avoid reusing another account's session. A fresh read-through catches sequence bugs but not UI drift: describe screens by visible labels, qualify screens you have not inspected, and **after every human click read the resulting state back by API** where available before proceeding. Update the guide from the person's observations.

---

## 3. Repo, scaffold and zone hygiene

**Repo**: create the private repo with your own GitHub login using `09_guides/GITHUB_SETUP.md`. Set per-repo `user.email`, add a pre-commit gitleaks hook, and check privacy as a pair: anonymous REST 404 AND authenticated `private=true`. Read the upstream file layout before regrouping any supplied brand assets. Copy rather than move, and retain SHA-256 manifests so completeness can be checked.

**`wrangler.jsonc` essentials**:

- Pin `account_id`; set `workers_dev: false` so the production site answers on its configured domain; set `preview_urls: true` explicitly for preview URLs on the account's Workers subdomain. Verify the current schema and defaults.
- Set `assets` to the build output with an `ASSETS` binding, a not-found handling rule and trailing-slash handling.
- Use `run_worker_first: ['/*', '!/_astro/*', '!/fonts/*', '!/images/*', '!/*.svg', '!/*.md', '!/*.txt', '!/*.xml', '!/.well-known/*']` where these routes match the site's output. Negative rules go straight to asset handling, so Worker code cannot enforce headers or access checks on those requests. Test the excluded routes separately.
- Set `routes: [{ pattern: '<apex>', custom_domain: true }]`; put `www` on a separate small Worker that sends a 301 to the apex while preserving path and query.
- Define static-asset header rules in `public/_headers`. Check that responses fetched through `env.ASSETS.fetch` receive them. Responses constructed by Worker code, such as markdown twins or API replies, need their headers set in code.

**Zone hygiene**:

- Back up every registrar parking record, including any wildcard that answers unknown subdomains, to the workspace. Immediately before attaching the custom domain, delete only the intended records, asserting that each still has its expected content.
- Decide inherited defaults deliberately: enable always-HTTPS and set minimum TLS to 1.2.
- Web Analytics may already have automatic installation enabled. Verify whether the beacon appears in Worker-served HTML; add it to the base layout if needed, avoiding duplicate installation.
- Check availability and plan requirements for zone-level markdown conversion. Keep build-time `.md` twins when the site needs markdown independently of that feature.

**Holding page until launch**: production shows a holding page with meta noindex AND `X-Robots-Tag` AND a crawlable `robots.txt`, so crawlers can discover the noindex instruction. Keep unfinished site builds on preview URLs. The public holding page is the exception and contains no unfinished site content.

---

## 4. Workers subdomain, first deploy, custom domains

1. Register the account's Workers subdomain by API before the first deploy: `bash 06_web_tools/cf-api PUT /accounts/{account}/workers/subdomain '{"subdomain":"<name>"}'`. Preview URLs use the account's Workers subdomain. Verify the generated URL format and any current custom-hostname support before relying on them. This first write proves the permission required for subdomain registration; verify Workers Scripts Edit through the deployment itself.
2. Run the first deploy through `bash 06_web_tools/wrangler-safe deploy`, or use `npx wrangler deploy` in the verified clean environment. This creates the Worker. A message such as "No targets deployed" can be expected with `workers_dev: false` and no routes yet; distinguish a missing public route from a failed upload.
3. Attach the custom-domain route and deploy; deploy the `www` redirect Worker.
4. **Provisioning is not failure**: new preview certificates and custom-domain routes can briefly produce TLS errors or server errors while provisioning. Check deployment and certificate state, then re-probe. Do not change healthy configuration solely because the first request failed.
5. Verify: apex 200; HSTS, frame and CSP headers; the noindex header; `Accept: text/markdown` returns `text/markdown`; a random path returns 404; `www` returns 301 while preserving path and query; HTTP redirects to HTTPS.

---
## 5. Workers Builds: main and previews (the proven recipe)

**Connect GitHub to Workers Builds through the dashboard**, then read the triggers back by API. Confirm that the connection created exactly one production trigger on `main`.

**Main (production): exactly one trigger.** Branch `main`, build `npm run build`, deploy `npx wrangler deploy`. The build carries the production guards: an account check that matches the build account to the pinned account, an environment check that rejects missing required keys or vendor test keys after trimming values, and checks that production routes, bindings and headers match the intended configuration. Check against the vendor's complete published test-key list. Nothing else deploys to production.

**Previews: Cloudflare Worker Previews.** Verify the current Workers Builds behavior before configuring previews, including whether non-main branch builds run `npx wrangler preview` regardless of the custom Preview command. Then:

1. Dashboard: Worker > Settings > Builds > **Previews Base** tab > "Builds for Preview branches" **ticked**, Preview command `npx wrangler preview`. Check the current labels before proceeding. Do NOT untick this casually: disabling preview builds can delete preview build configurations, including API-created custom triggers.
2. Add a **`previews` block** to the project's Wrangler configuration. A Preview inherits **no** production bindings, so declare every one: vars, its **own D1 database** so test submissions never touch production tables, its own ratelimit `namespace_id`, and observability settings that keep any logging promise the privacy page makes. Crons do not run on Previews. Use a production dry run to verify that `wrangler deploy` ignores the block and leaves production bindings unchanged.
3. **Migrate the preview database through a throwaway config** that names only that database, with `migrations_dir` set to the repository's absolute migrations path, so a slip cannot reach production.
4. **Set preview secrets in the Preview base config BEFORE any Preview exists** (`wrangler preview base-config secret put <NAME>`, value piped on stdin, never printed). Base-config secrets are copied into a Preview when it is **created**, then persist across its deployments; per-Preview `secret put/bulk` values last **one** deployment. A Preview created before its required base configuration existed is stale: **delete and recreate it** behind an exact-name guard, because `wrangler preview delete` auto-confirms.
5. **Test on a throwaway named Preview** before pushing (`wrangler preview --name setup-check`), and test the path you will actually take: two consecutive deployments, plus the existing Preview if there is one.
6. Push the preview branch. Verify that its stable alias serves at `https://<branch>-<your-worker>.<your-workers-subdomain>/`. With a `preview` branch, that is the link reviewers keep. Each push also gets an immutable version link.

**Branch ancestry trap**: a branch cut from `main` inherits main's Wrangler configuration, not the preview branch's. If main lacks the `previews` block, a branch based on main can fail its preview build with "missing a `previews` block". Carry only the block the preview mechanism needs, byte for byte, and NOT preview-only extras. For example, a cron trigger whose handler exists only on the preview branch can break production deploys. Name in a code comment what was deliberately not carried. When the preview branch merges into main at launch, main gains the block.

**Watching builds: the monitoring consequence**:

- The Workers Builds API (`/builds/workers/<script_tag>/builds`) may expose main-trigger builds without exposing Worker Previews builds. Verify the current API and CLI capabilities. Where preview listing is unavailable, watch a preview by **polling its URL for a page marker**: `python3 06_web_tools/preview_url_watch.py --url <preview-url> --probe /<path> --marker '<text>'`. Require both a 200 response on the probe path and a marker unique to the new build. The watcher sends the Access service token when configured in the key file and logs the anonymous response, which should redirect to authentication on a protected preview.
- Watch main by **build UUID**, never by commit alone: `bash 06_web_tools/cf-api GET /accounts/{account}/builds/builds/<build_uuid>` for status and outcome, and the same endpoint with `/logs` appended for logs. `python3 06_web_tools/builds_watch.py --worker <your-worker> --commit <sha7> --branch main` finds the build and watches it. Confirm that the selected UUID is the intended attempt. A commit alone can match a preview build or an old failed attempt after a retry.
- **Judge a deploy by its product**: done means a probe path returns 200 with a marker absent from the previous build, AND the latest deployment carries the pushed commit tag and lists every required binding by name. Refuse to judge until the tag matches. Every completion report names the deployment ID.
- The dashboard's per-branch page is another view of the build, and it can disagree with the API. Confirm a first preview in the dashboard as well, then resolve discrepancies against the served page and deployment metadata.

**Preview review hand-off**: give reviewers the stable branch alias, never a per-push version link. A frozen link can make a correct fix appear unchanged.

**History** (one line): when replacing a custom API-created trigger using `wrangler versions upload --preview-alias` with Worker Previews, check for overlapping triggers and destructive toggle behavior, then verify by API that production still has exactly one trigger on `main`.

---

## 6. Access on previews (optional)

Prefer protecting previews when they show unreleased work, such as a ceramic studio's upcoming collection, because a preview link travels. A public site's previews may stay public; they should still send a noindex header.

1. Complete Zero Trust onboarding in the dashboard with a team name and plan. Check the current payment-method requirements directly rather than relying on third-party summaries.
2. Locate Worker > Domains & Routes > the Worker URL box > Enable Access > "Manage Worker access", checking current dashboard labels. Set the scope to **Previews only**; "All traffic" would lock production. Add a policy for **Cloudflare Account** members. An "Email domain = gmail.com" rule admits every Gmail user.
3. Use an Access app whose destination type is `preview_worker` to protect preview URLs by Worker rather than hostname. Prove coverage with an unauthenticated request that redirects to authentication.
4. Add a **service-token policy** with decision `non_identity` so automation can pass. Write the two values straight into your key file as `CF_ACCESS_CLIENT_ID` and `CF_ACCESS_CLIENT_SECRET`, with mode 600, never displayed. The Worker re-checks the Access JWT (`Cf-Access-Jwt-Assertion`: signature, `aud`, `iss`, `exp`) on preview hosts and fails closed when its configuration is unset.
5. **Probe without leaking the session**: use `curl -s -o /dev/null -D <600-mode-temp-file>`, then extract only named headers. Never combine `-I` with `-o` for this procedure, because response headers, including `Set-Cookie`, can end up in the output file. Keep service-token headers off the command line; `06_web_tools/preview_url_watch.py` sends them in-process. Delete temporary files in a `finally` block and never put a credential temporary file inside a Git tree.
6. For a collaborator, grant repository Write access only as needed and check which branch-protection features the current GitHub plan supports. Where enforcement is unavailable, require a successful build, verification, a checked preview and a note to the site owner before merging to `main`. Add an Access include rule for the collaborator's email with One-time PIN login. Decide deliberately whether they need a dashboard role, since the account may hold visitors' personal data in the forms database. Never share credentials.

---

## 7. Forms: D1, Turnstile, transactional email

**Data home**: use one D1 database for all form kinds, such as contact, stock notifications and attribution, so attribution analytics can use a join. Check the current D1 Time Travel retention for the selected plan and add a monthly `wrangler d1 export` for longer-term backups. Before launch, verify the plan's database count, per-database storage, account storage and per-invocation query limits.

**Handler order**: method, host, origin and Access check, then configuration check, then rate limit, then a size cap, then honeypot plus a page-measured fill time, then field validation from ONE shared JSON definition read by both pages and Worker, then **Turnstile fail-closed**, then a **parameterised D1 INSERT first**, then email via `ctx.waitUntil` with an Idempotency-Key and `email_status` recorded. D1 is the record; email is a notification. Gate an optional follow-up answer with a one-time HMAC token, return a 303 redirect to the thank-you page, and enforce uniqueness per submission to refuse replay.

**Preview vs production**: rows carry `source_host`, and analytics views exclude preview rows. With Worker Previews, those rows also land in the separate preview database. Use the Turnstile dummy key only on preview hosts; **prove by request that the dummy token gets 403 on production**. A production build guard refuses every published vendor test key.

**Endpoint hardening**: make repeat sign-ups indistinguishable from first ones with the same status, body and redirect. Link duplicate records after the response so deletion still reaches them. Never log malformed bodies: catch every parse failure, return 4xx and log `e.name` only. Worker code logs errors only, enforced by a lint check over its full import closure that covers every console spelling.

**Testing traps**:

- Fill time is a duration measured in the page with `performance.now`, never a client timestamp. Clock skew can make a rapid automated submission appear old enough to pass.
- The Workers rate-limit binding is eventually consistent and per location: it is a flood brake, not a strict admission gate. Do not assert an exact request count before rejection; accept any 429 as evidence that a burst test reached the limiter.
- `wrangler dev` can rewrite the host to production unless started with `--local-upstream localhost`. Local posts can then be treated as production, causing Turnstile to fail closed with 503 `not_configured` only on otherwise successful paths. When a local Worker fails only on success paths, check which host it thinks it serves.
- Additive form fields use nullable D1 migrations applied `--local` and then `--remote` before deployment. Test with a probe that sends no mail.
- An account-pin guard can refuse a local build when the shell exports another account. Build with `env -u CLOUDFLARE_ACCOUNT_ID -u CLOUDFLARE_API_TOKEN npm run build` when the build should use its pinned configuration.
- "Sent" is not "delivered". Send one smoke-test email to a real address you control, never a fabricated address, and close the test only after a human confirms arrival.

**Transactional email (Resend example)**: create a sending subdomain by API. Write DNS records **through `06_web_tools/cf-api` from the provider's API response**, rather than a "Sign in to Cloudflare" Domain Connect button that may act on whichever account the browser holds. Use the returned record types, names and values rather than a remembered record count. Begin DMARC monitoring with `p=none` and no external `rua`, then strengthen the policy after reviewing mail authentication. Turn open and click tracking OFF. Replace a temporary full-access key with a domain-restricted sending key and verify its restrictions by behavior, including rejection on unauthorized endpoints. Re-poll a lagging verifier before changing correct DNS records.

**Privacy page**: before approval, check every data-practice sentence against the code using a TRUE/FALSE/UNVERIFIABLE table, and repeat the check after relevant changes. Count copies outside the forms code, including the site operator's inbox, CSV exports, D1 restore history and Worker invocation logs, and name every processor. Promise a deletion route only after executing it end to end. A minimal starting configuration uses no cookies, no banner, cookieless analytics and no browser storage for attribution; verify that the actual integrations and applicable requirements support that configuration.

---

## 8. DNSSEC and DNS-AID

**DNSSEC**: enable it on the zone by API. Generate the registrar instructions' DS values **from the API**, never by retyping them; a human completes the registrar entry. When `dig` is absent, verify through a validating DNS-over-HTTPS resolver's JSON response with the `AD` flag true. Registry publication can lag: confirm your side, then wait and recheck. Some registrars restrict DS records for certain TLDs on third-party nameservers, so check registrar support first.

**DNS-AID**: where the site supports the advertised agent endpoints, configure the intended SVCB records, such as `_index._agents.<domain>` with `alpn="h2,http/1.1" port=443` and `_a2a._agents.<domain>` with `alpn="a2a" port=443`. Confirm the current discovery specification and endpoint support before publishing. Write records by API through `06_web_tools/cf-api` using `POST /zones/{zone}/dns_records` and a body shaped as `{type:'SVCB', name, data:{priority:1, target:'<domain>.', value:'alpn="..." port=443'}, ttl, comment}`. Once DNSSEC validates, adding the records is straightforward; the registrar DS handoff often needs more coordination. Include intended discovery records in the DNS checklist and verify them at launch, since a planned record is not a published record.

---
## 8b. DMARC reporting and CAA (Cloudflare-specific; not the Vercel path)

**Cloudflare only.** These routes use the Cloudflare zone API. On a Vercel build, DNS may live elsewhere, such as at the registrar or in Vercel DNS. Use that provider's tools for equivalent changes. For a Cloudflare zone, review DNSSEC, DNS-AID, DMARC reporting and CAA in that order, then assess agent readiness.

**DMARC reporting without a mailbox**. A missing mailbox product does not require `p=none`. A domain can send through a transactional provider with aligned SPF or DKIM and receive through Cloudflare Email Routing. Reporting provides visibility into which senders authenticate successfully. Steps:

1. Run `bash 06_web_tools/cf-api GET /zones/{zone}/email/auth/dmarc-reports` to inspect `enabled`, the zone's `rua_prefix`, and the current DMARC and SPF records.
2. `PATCH` the same endpoint with `{"enabled":true,"skip_wizard":true}`.
3. Verify that Cloudflare updated the reporting destination while preserving the intended policy, for example: `v=DMARC1; p=none; rua=mailto:<rua_prefix>@dmarc-reports.cloudflare.net;`. Check a public resolver, then review incoming reports in Cloudflare's DMARC dashboard.
4. With the domain owner's approval, move to `p=quarantine`, then `p=reject` after reports cover the normal sending cycle and confirm that legitimate senders authenticate correctly. Anyone sending as the domain from a personal mailbox needs an authorized, aligned sending service first. Configure and verify authentication before adding a new mail service.

**CAA**. CAA is checked when a certificate is issued. An incorrect configuration can leave the current certificate working while blocking its renewal. Steps:

1. Record the existing CAA records and the live certificate's issuer and expiry: `openssl s_client -connect <host>:443 -servername <host> | openssl x509 -noout -issuer -enddate`.
2. Read Cloudflare's current certificate-authority documentation at execution time: https://developers.cloudflare.com/ssl/reference/certificate-authorities/. Identify the authorities required by the certificate products enabled on the zone, including backup certificates.
3. Create the required apex records using the documented authority values and parameters. Configure `issue` and, where wildcard issuance is needed, `issuewild`, with flags `0`. Do not copy a historical CA list without checking it.
4. Verify the effective records through DNS-over-HTTPS on two resolvers. Cloudflare may supply additional CAA authorizations for Universal SSL that are visible in DNS but absent from the dashboard or API. Subdomains inherit apex restrictions unless a more specific applicable record overrides them.
5. Check the behavior of Advanced certificates separately and explicitly authorize their authorities where required. Account for CAA processing through CNAME targets.
6. Record checks establish the configuration; successful renewal establishes that issuance worked. Schedule a check after renewal and confirm that the certificate's expiry advanced.

## 9. Markdown negotiation, agent files, indexing posture

- **Markdown negotiation**: define a build-time Markdown twin for each eligible page. The Worker serves that twin when a request accepts `text/markdown`, fetching it through `env.ASSETS.fetch(...)` and returning `Vary: Accept`. Define the direct twin URL as the page's URL followed by `index.md`, and test both access methods. Publish agent discovery files only for capabilities the site actually supports. If Web Bot Auth is implemented, check directory signing and whether the `run_worker_first` configuration excludes its discovery route.
- **Indexing posture on Workers is a header posture**: previews carry `X-Robots-Tag: noindex, nofollow` on every response, including Markdown twins and API replies. Set the header in code for Worker-generated responses. Keep robots.txt crawlable so crawlers can see the header. In this recipe, omit robots meta tags because a twin generator that treats them as exclusion signals can skip required preview pages. Do not use `Disallow: /` to enforce preview noindex.
- **Preview hosts override the header**: Cloudflare preview hosts may replace the build's `X-Robots-Tag` value with their own `noindex` value while retaining other configured headers. A verifier accepts a valid `noindex` directive on those hosts and separately checks the exact intended production value. Never weaken the production assertion to make a preview pass. Inspect the generated header configuration and verify production behavior on the production host.

---

## 10. Launch

Classify every failed agent-readiness check as either a missed implementation step or a justified non-applicable requirement. Fix missed steps. For a public site without credentials or token scopes, do not invent authentication claims to satisfy a scanner. Document the limitation and any resulting failed check.

**Production posture is applied by the build, not by hand**: use a build hook to select production posture when `WORKERS_CI_BRANCH=main`. It removes site-wide noindex from the generated header configuration and emits production robots.txt with the intended crawler policy and sitemap reference. Preview builds retain noindex. Validate both outputs. Hand-editing generated files is fragile: the next build can overwrite the edit or apply it to the wrong environment. The Worker also adds noindex to HTML 404 responses.

**Launch sequence**:

1. Obtain the site owner's go-ahead, confirm that the update is a fast-forward, and promote the preview branch into main with `git push origin preview:main`.
2. Expect build guards to reject missing configuration, even when setup instructions describe it. For example, a missing public Turnstile site key must fail the production build. Set public trigger variables through `bash 06_web_tools/cf-api PATCH /accounts/{account}/builds/triggers/<uuid>/environment_variables` using the current API request schema. Start a manual build with `bash 06_web_tools/cf-api POST /accounts/{account}/builds/triggers/<uuid>/builds '{"branch":"main"}'` and follow that build's UUID.
3. Confirm the required production Worker secrets by name, without printing their values: the Access audience where used, form token secret, email service key and Turnstile secret.
4. Run live checks: product-page probes, rejection of a dummy Turnstile token with HTTP 403, link checks, axe, local production Worker checks using `--local-upstream`, and agent-readiness validation. If a scanner provides a score, apply the acceptance threshold agreed before launch. Separate justified non-applicable checks, such as an MCP server card for a site without MCP, from missed setup such as intended DNS discovery records. Fix the latter and record the former.
5. If printed material carries a QR code, check it as qa-032 in `05_automations/client-site-first-build/skillbook.md` describes.

**Supply chain**: give an image-affecting dependency fix its own commit. Verify it with a fresh `npm ci` from the lockfile and a cold build with the image cache moved aside, because hosted builds may lack the local cache. If the fix should preserve image output, compare the generated bytes and investigate differences. Use `overrides` where exact transitive dependency pins are needed. Apply a documented minimum release age, such as 7 days, before adopting a new Wrangler release, and store the review date in project notes rather than relying on a session timer. For an upgrade: update the pin, run `npm install`, build preview and production in clean environments, run every validator, test the local production Worker, push preview, follow the build UUID, obtain sign-off, fast-forward main and run live probes.

**Recorded deviations**: read the project's release rules before the first production push. Validate preview, obtain the site owner's sign-off, then promote main. If sign-off precedes the formal ACE loop or Lighthouse checks, record exactly what ran and what remains incomplete, then offer to close the gap. A Lighthouse command that produced no usable report does not count as completed validation.

---

## 11. Hand-off to maintenance

Record the following in the site's maintenance notes:

- **Platform**: Cloudflare Workers, Workers Builds and GitHub; the credential method, such as Wrangler login or a protected key file used through `06_web_tools/wrangler-safe`; and the account's descriptive name. Keep account identifiers out of broadly shared notes.
- **Change path after launch**: use the preview branch for changes. Run a clean-environment preview build and validators, push preview, confirm the preview URL, obtain site-owner sign-off, run `git push origin preview:main`, follow the main build by UUID and verify the live site. Before launch, an isolated side change can use a `git worktree` based on `origin/main`; confirm ancestry with `git merge-base --is-ancestor` before a fast-forward.
- **The four standing checks**: (1) simulate CI from a clean clone before every push (cf-009); (2) confirm success through deployed behavior, using a URL marker for preview and the build UUID plus commit-associated deployment bindings for main, with a dashboard check when first configuring the setup; (3) if previews use Access protection, verify the intended unauthenticated response, such as a 302 login redirect, and a 200 response with the service token; (4) use exactly one preview mechanism for this recipe: Worker Previews with the `previews` block, one trigger on `main` and no separate custom preview trigger.
- **Accepted residuals**: if `run_worker_first` excludes `/.well-known/*`, missing discovery routes may bypass the Worker's 404-noindex logic and lack `X-Robots-Tag` in production. Record any observed exception. Fix it by routing the prefix through the Worker or configuring an appropriate assets not-found response.
- **Open post-launch items**: record the current status and next check for DMARC enforcement, CAA renewal verification, any planned accessibility statement, token lifetime and rotation, the Wrangler upgrade review date, and agent-readiness validation after agent-file or DNS changes.

---

## Sources

Use the shipped deployment guidance in `09_guides/DEPLOY_CLOUDFLARE.md` and maintenance procedures in `05_automations/website-maintenance/runbook_appendix/cloudflare_maintenance_ops.md`. Consult current Cloudflare documentation when confirming certificate authorities, API request schemas and preview-host behavior.
