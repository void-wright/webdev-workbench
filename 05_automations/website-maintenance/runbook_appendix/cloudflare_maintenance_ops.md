# Website Maintenance: Cloudflare Maintenance Ops (generic edition)

> **PRIMARY path: Cloudflare Workers + Workers Builds from your GitHub repo.** See `05_automations/website-maintenance/comprehensive_guide.md` for deployment guidance. This appendix covers recurring post-launch operations. Cloudflare Pages commands appear in a short note at the end. Account setup: `09_guides/DEPLOY_CLOUDFLARE.md`.
>
> **Credentials**: use your own Cloudflare API token in a protected key file with mode 600. The tools in `06_web_tools/`, including `cf-api` and `wrangler-safe`, parse credentials without sourcing the file or printing its contents. Run the examples from the package root with `WT="$PWD/06_web_tools"`. Never print a token, cookie or secret; pin `account_id` in the site's Wrangler configuration.
>
> Before starting, review the site's recorded launch decisions, production configuration and preview configuration.

## W1. The change path after launch (every change, no exceptions)

The preview branch is the change path for everything once a Workers site is live:

1. Edit on `preview` or a feature branch. Build the preview in a clean environment and run the site's available validators, such as AEO, links, source lint and figure checks.
2. Commit. Wait until the absence check below before pushing.
3. **Preview watch by URL marker**: first prove the marker is absent from the preview currently serving. Run the watcher briefly before pushing; it must time out. Then push and watch for the marker:
   ```bash
   PV="https://<your-preview-host>"     # The preview branch alias shown on the Worker's dashboard.
   python3 "$WT/preview_url_watch.py" --url "$PV" --probe /<probe-path> --marker '<marker>' --max-seconds 30
   before_rc=$?
   echo "before push rc=$before_rc (must be 2: marker absent)"
   test "$before_rc" -eq 2 || exit 1

   git push origin preview
   python3 "$WT/preview_url_watch.py" --url "$PV" --probe /<probe-path> --marker '<marker>' --max-seconds 720
   after_rc=$?
   echo "after push rc=$after_rc (must be 0: the new build is serving)"
   test "$after_rc" -eq 0 || exit 1
   ```
   Require absent, then present. A marker already present before the push cannot prove that the new deployment arrived. If previews sit behind Cloudflare Access, configure the watcher to send the service token from the protected key file so both runs see the real page. The Workers Builds `/builds` listing cannot establish that a Worker Preview is serving.
4. Confirm the deployment tagged with the pushed commit lists every required binding by name. Use the branch-alias link shown on the Worker's dashboard for review, rather than a per-push version link.
5. Record sign-off, including your own review when working alone. Refresh remote refs with `git fetch origin`, confirm `git merge-base --is-ancestor origin/main HEAD`, then run `git push origin preview:main`. Use fast-forward updates only.
6. **Main watch by build UUID**: use `bash "$WT/cf-api" GET '/accounts/{account}/builds/builds/<build_uuid>'` and inspect `result.status` and `build_outcome`. Fetch logs from the same build's `/logs` endpoint. Watch the build UUID rather than the commit: a commit-based watcher can select an older failed build and miss a retry.
7. Verify the live custom domain. Assert production headers exactly; accept preview-only `noindex` headers only on the designated preview hosts. Complete the printed-URL loop in W3.

**Side change while the preview checkout is busy**: run `git worktree add <dir> -b <branch> origin/main`, build in a clean environment, push the branch, verify its own Worker Preview, record sign-off and fast-forward to main. A branch cut from main inherits main's Wrangler configuration. If its preview build fails because the `previews` block is missing, copy only that block from `preview`. Leave out preview-only cron configuration and document the omission.

## W2. Pages generated from data kept outside the repo

For pages built from data that lives elsewhere, such as a bakery's menu kept in a spreadsheet:

1. Edit the source data, never the generated pages in the repository.
2. Run your generator with the site repository as its destination, on the `preview` branch.
3. Build in a clean environment and run the validators, then follow W1 steps 2 through 7.
4. Generated text still goes through every page check.

Keep the source location and the generation command written down together, so the next edit follows the same path.

## W3. Printed and QR-coded URLs

A QR code on a poster or card should point at a short path you control, which forwards to the real page with a temporary redirect (302 or 307) so you can re-point it later. Never use a permanent 301 for a printed target: browsers cache it and the print can no longer be moved. Test the printed image itself: decode it with a QR decoder, follow the decoded URL and require the expected final page. For example, a garden-supply shop's planting card should land on the intended how-to article. Re-test after any change that touches those routes.

## W4. Dated deploy-tool upgrade (wrangler)

Prefer to hold a deploy-tool release until it is at least 7 days old, allowing time for early regression and supply-chain reports to surface. Record the earliest upgrade date in a durable maintenance note; a session timer disappears with the session.

```bash
npm view wrangler time --json
# Find the intended version's publication time.
# Earliest upgrade date = publication date + 7 days.
```

Check both preview and production configurations. Push nothing until the local checks pass:

1. Bump the repository's Wrangler dependency pin, run `npm install`, then run `npm audit`. Record which advisories close and which remain.
2. Build both **preview** and **production** in clean environments. Use `WORKERS_CI_BRANCH=main` and the production public keys for the production build.
3. Run the site's validators.
4. Start a local production Worker with `npx wrangler dev --local-upstream localhost --port <port>`. Run the site's agent-readiness and link checks against it in production mode, then stop it by its PID.
5. Push preview and watch it as described in W1 step 3. Complete review, fast-forward main and watch the main build by UUID as described in W1 step 6.
6. Run live probes, including every printed and QR-coded URL from W3.
7. Confirm Workers Builds uses the repository's pinned Wrangler version when running `npx wrangler deploy`, so the validated version is also the production deploy tool.

## W5. DNS-AID (agent discovery over DNS)

Prerequisite: DNSSEC must be active on the zone. Read the existing records before deciding what to add:

```bash
bash "$WT/cf-api" GET '/zones/{zone}/dns_records'
```

If the site implements the advertised discovery endpoints, the following illustrates two SVCB records. `CLOUDFLARE_ZONE_ID` in the protected key file supplies `{zone}`:

```bash
bash "$WT/cf-api" POST '/zones/{zone}/dns_records' '{"type":"SVCB","name":"_index._agents.<your-domain>","ttl":3600,"comment":"DNS-AID index","data":{"priority":1,"target":"<your-domain>.","value":"alpn=\"h2,http/1.1\" port=443"}}'
bash "$WT/cf-api" POST '/zones/{zone}/dns_records' '{"type":"SVCB","name":"_a2a._agents.<your-domain>","ttl":3600,"comment":"DNS-AID a2a","data":{"priority":1,"target":"<your-domain>.","value":"alpn=\"a2a\" port=443"}}'
```

Verify both records through DNS-over-HTTPS JSON with DNSSEC requested, using queries such as `https://cloudflare-dns.com/dns-query?name=_index._agents.<your-domain>&type=SVCB&do=true` and the header `accept: application/dns-json`. Require the expected answers, DNSSEC signatures and `AD: true`. Then re-scan as described in W6.

Write only the records you deliberately selected. DNS-AID is an emerging convention; verify its current specification and support before relying on it.

## W5b. DMARC reporting and CAA (Cloudflare-specific)

- **DMARC reports**: verify the current Cloudflare endpoint and read the existing record before using `bash "$WT/cf-api" PATCH '/zones/{zone}/email/auth/dmarc-reports' '{"enabled":true,"skip_wizard":true}'`. Confirm the change adds the reporting destination while preserving the intended policy. Prefer moving to quarantine and then reject only after about two weeks of clean reports covering all legitimate senders. Tightening too early can cause legitimate mail to be rejected.
- **CAA**: keep the apex records aligned with Cloudflare's current certificate-authority requirements, including backup issuers and the applicable `issuewild` entries. After certificate renewal, confirm the expiry moved. Re-read the current CA requirements before changing CAA because providers can change issuers.

## W6. isitagentready re-scan

After changes to discovery documents, agent guidance, Link headers, crawler rules, DNS-AID or production configuration, request a fresh scan with `POST https://isitagentready.com/api/scan`, after verifying the service's current API.

Compare results with the site's recorded intentional exceptions. Classify each failed check as either an intentional mismatch or an overlooked requirement. For example, adding authentication metadata to a public site that has no token protection would misrepresent its behavior. Advertising an MCP server that does not exist would do the same.

Investigate new failures and fix overlooked requirements. Keep deliberate exceptions documented instead of adding misleading features to improve a score. Also run the site's own agent-readiness checks against a local production Worker.

## W7. Known residuals and traps on Workers

- Paths excluded by `run_worker_first`, such as discovery-document routes, skip Worker-level response logic. A header added by the Worker, such as X-Robots-Tag on 404 responses, may therefore be absent. Record the exact exception so link checks can distinguish it from a new failure. To remove the exception, route that prefix through the Worker or use an appropriate assets `not_found` rule.
- Local request handling can depend on the upstream hostname. Use `wrangler dev --local-upstream localhost` for the expected local setup and verify that POST requests follow the local path. A fail-closed Turnstile configuration can otherwise refuse every success case.
- Check the current D1 Time Travel retention for your plan and choose an export schedule that meets your recovery needs. For periodic exports, use `bash "$WT/wrangler-safe" d1 export <your-d1-db> --remote --output <file>`. Exports may contain personal information from forms, so use mode 600 and keep them outside the repository. `bash "$WT/forms-check" --db <your-d1-db> export <dir>` provides per-table CSV exports; protect those outputs the same way.
- Probe Access-protected hosts without printing cookies. Write headers to a mode-600 temporary file and extract only the named headers needed for the check.
- For production secrets, use `bash "$WT/wrangler-safe" secret put <NAME>`. Configure preview secrets in the Preview base configuration before creating the Preview.
- Apply D1 schema migrations locally with `npx wrangler d1 migrations apply <your-d1-db> --local`, then apply remote migrations through `wrangler-safe` before deployment. For preview D1, use a temporary configuration naming only the intended preview database.

## Security audit (any Cloudflare site)

1. Inspect response headers from `curl -sI https://<your-domain>/`, selecting CSP, HSTS, X-Content-Type-Options, Referrer-Policy, Permissions-Policy and X-Robots-Tag without printing cookies.
2. Confirm CSP has no `unsafe-eval` and permits only the origins the page needs.
3. Include HSTS `preload` only after confirming the domain and its subdomains meet the preload requirements and the site operator accepts the lasting HTTPS commitment.
4. Run `gitleaks detect` on the repository. Allowlist public-by-design values, such as a Turnstile site key or public analytics beacon token, by exact value rather than by path.

## Alternative: Cloudflare Pages sites (short note)

Cloudflare Pages is an alternative deployment path. Pages deploys on `git push` to the configured production branch, or manually with `npx wrangler pages deploy dist --project-name <project> --branch main`. Set runtime secrets with `npx wrangler pages secret put <NAME> --project-name <project>` and inspect logs with `npx wrangler pages deployment tail --project-name <project>`.

Use the Pages Functions directory for server handlers. Pages header configuration applies every matching rule; a specific rule does not replace a catch-all. Never use Pages commands on a Workers site.

## Anti-Patterns

- ❌ Pages commands (`wrangler pages deploy`, `pages secret put`) on a Workers site.
- ❌ Treating the `/builds` listing as proof that a preview deployed.
- ❌ Pushing to main before sign-off or force-pushing main.
- ❌ Skipping live verification. A successful deployment report does not prove that the expected response is serving.
- ❌ Changing DNS, CAA, DMARC or Access policies without first reading the existing configuration and deliberately choosing the change.
