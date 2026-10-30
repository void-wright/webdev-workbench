# Website Maintenance: Preview to Production (generic edition)

> **PRIMARY path: a Cloudflare Workers site built by Workers Builds from your GitHub repo.** Preview branch → Worker Preview (optionally behind Cloudflare Access) → your own sign-off → fast-forward merge to `main` → Workers Builds deploys → watch by build UUID → live verify. **Rollback** via Workers deployments, then correct `main` through preview.
>
> "Promote" here means shipping a maintenance change to a site that is already live, rather than a first launch. The production settings (no site-wide noindex header, production crawler rules) should be applied **by the build on main**, so there is no manual cutover edit to forget.
>
> Below, `WT` points to the package's `06_web_tools` directory. Set it from the package root before changing directories. Hosting setup: `09_guides/DEPLOY_CLOUDFLARE.md` and `09_guides/DEPLOY_VERCEL.md`.

## Pre-conditions (refuse if any fails)

1. The change is on `preview` (or a feature branch), committed and pushed, ACE-SATISFACTORY at 9.8 HARD, with the curator review complete.
2. Preview validation passes, with log hashes matching the commit you will merge.
3. Sign-off is recorded (who, when, which commit). If you work with others, they have a one-line heads-up of what is going out. If the change alters page **copy**, the person responsible for the words has signed it explicitly ("ship it", "go live"); "looks good" is feedback, not sign-off.
4. No in-progress ACE loop, no failing build on the branch, and nobody else mid-merge (check `git fetch && git status`; find out why if `main` moved unexpectedly).

If any pre-condition fails, halt and say which.

## The flow

### Step 1: Production CI simulation
Run a clean-clone CI simulation on the branch with `WORKERS_CI_BRANCH=main` and the production public keys, so any production guards in your build (an account pin, an environment check refusing a missing or dummy public key) and the production settings run locally first. Then run the site's validators. Read every exit code directly (`cmd > log 2>&1; echo rc=$?`), never through a pipe.

### Step 2: Fast-forward main
```bash
git fetch origin
git merge-base --is-ancestor origin/main HEAD && echo "fast-forward OK"   # refuse if not an ancestor
git push origin preview:main     # fast-forward only; never --force
```
Use the actual branch name if it differs from `preview`, and confirm its tip is the validated commit. If `origin/main` is not an ancestor, a side change has shipped: merge or rebase it into `preview`, re-run preview validation, and record sign-off again for the new commit.

### Step 3: Watch the main build by uuid
Workers Builds runs the configured main trigger: `npm run build`, then `npx wrangler deploy`. Find the new build's UUID in the Cloudflare dashboard under your Worker's builds and poll it. `cf-api` reads your token from your configured key file without printing it:
```bash
# Run from the Voidwright package root.
WT="$(pwd)/06_web_tools"
build_response="$(mktemp)"
bash "$WT/cf-api" GET '/accounts/{account}/builds/builds/<build_uuid>' > "$build_response"
build_rc=$?
echo "rc=$build_rc"
if [ "$build_rc" -eq 0 ]; then
  python3 -c 'import json,sys; r=json.load(open(sys.argv[1]))["result"]; print(r.get("status"),r.get("build_outcome"))' "$build_response"
fi
rm -f "$build_response"
```
Never watch by commit: an older failed build of the same commit can appear as the answer while a retry is missed. "Done" names its deployment ID. If a build fails, read its logs (`bash "$WT/cf-api" GET '/accounts/{account}/builds/builds/<build_uuid>/logs'`), fix on `preview`, and repeat from Step 1. Verify the API paths against current Cloudflare documentation before relying on them.

### Step 4: Live verify on the custom domain
- `curl -sI https://<your-domain>/<route>` → check the EXACT production values for the named headers: CSP, HSTS, X-Robots-Tag absent or its intended production value, and Referrer-Policy.
- Run the site's links check and agent-readiness check in production mode. Compare any failures with documented, intentional exceptions.
- Test every printed or QR-coded URL as W3 in `05_automations/website-maintenance/runbook_appendix/cloudflare_maintenance_ops.md` describes.
- Run Lighthouse + axe on the changed routes. Save Lighthouse JSON, or record the run as "not run".

### Step 5: Record
Update `05_automations/website-maintenance/runbook_appendix/client_registry.md` with the last production commit and deployment date if you track them. Record reusable failure-and-fix lessons, and write one short note of what shipped, the deployment ID, and anything not run.

## Rollback

Use when production is wrong after Step 3 or 4.

1. **Roll the Worker back** to the last good deployment (the static assets travel with the Worker version):
   ```bash
   cd <your-site-repo>
   bash "$WT/wrangler-safe" deployments list            # find the previous good version ID
   bash "$WT/wrangler-safe" rollback <version-id> --message "rollback: <why>"
   ```
   Or select the previous version in the Worker's deployment history in the Cloudflare dashboard and choose Rollback. Verify the live site as in Step 4. Check the Wrangler help text at execution time: flags move between releases.
2. **Put main right.** A rollback changes what serves, not what `main` holds; the next main push would redeploy the bad commit. On `preview`, `git revert <bad-commit>` (never rewrite history), push, watch the preview, then fast-forward main (Steps 1 to 4).
3. **What a rollback does not undo**: D1 migrations already applied with `--remote`, secrets changed since, DNS or zone changes, and Access policies. Keep migrations additive and confirm that an older Worker still runs against the newer schema. Undo other changes explicitly and deliberately.
4. Record the deployment IDs before and after, and tell anyone who shares responsibility for the site.

## Alternative platforms (short note)

- **Vercel**: preview branch → preview URL (optionally protected) → sign-off → merge to main (Git-connected production deploy) or `vercel deploy --prod`; rollback with `vercel rollback` or promote a previous deployment. For a first launch, keep a written checklist of site URL, indexing, crawler rules, and access-protection changes. Apply and verify any changes your deployment configuration does not automate. Setup: `09_guides/DEPLOY_VERCEL.md`.
- **Cloudflare Pages**: a push to the configured production branch triggers deployment; rollback is available from the dashboard's deployment list. Keep a written checklist for production settings that the build does not apply automatically.

## Anti-Patterns

- ❌ Merging without a successful build, passing validation, and a checked preview, or shipping a **copy** change its responsible editor has not signed off. If branch protection is unavailable or disabled, enforce these checks yourself.
- ❌ Force-pushing `main`, or pushing a commit that did not pass preview validation.
- ❌ Hand-editing indexing headers or crawler rules for production when the build owns those settings.
- ❌ Watching the main build by commit; calling it done without a deployment ID and a live check.
- ❌ A rollback without the follow-up revert on main.
