# Appendix: Redirect Application + Curl Test on the Preview (site ports only)

> Generic edition: Cloudflare Workers. Runs ONLY when `IS_SITE_PORT == true`, after every asset has been placed.

## Steps

1. **Render** the approved redirect map. Create `public/_redirects` as the build's redirect rules file: 3xx rows use `<source> <destination> <status>`, with specific rules before splats. Send 410 rows to a small gone-list module that the Worker checks before serving assets; make sure those paths are not excluded by `run_worker_first`. If the map exceeds the `_redirects` limits, move the whole map into a Worker lookup table.
2. **Build and simulate**: run `npm run build`, the project's validators, then reproduce the CI build from a clean clone. Commit the redirect rules file, gone-list and approved redirect map with a message naming the number of entries.
3. **Push the preview branch** and wait for the deployed site, not just a successful pipeline: the preview URL must answer 200 on a probe path with a marker from this build.
4. **Curl test every non-pattern redirect** against the stable preview link. If previews are behind Cloudflare Access, read the service-token headers from a temporary file with mode 600, created from your configured key file and deleted afterwards. Never put secret values on the command line:
   ```bash
   # Set KEY_FILE to your key file and PREVIEW_URL to the stable preview URL.
   # Set SOURCE_PATH to the redirect source path being tested.
   # Only when previews are protected: build headers without printing values.
   (
     umask 077
     redirect_headers="$(mktemp)" || exit 1
     trap 'rm -f "$redirect_headers"' EXIT
     awk -F= '
       $1=="CF_ACCESS_CLIENT_ID" {
         print "CF-Access-Client-Id: " substr($0, index($0, "=") + 1)
       }
       $1=="CF_ACCESS_CLIENT_SECRET" {
         print "CF-Access-Client-Secret: " substr($0, index($0, "=") + 1)
       }
     ' "$KEY_FILE" > "$redirect_headers" || exit 1

     result=$(curl -sS -o /dev/null -w '%{http_code} %{redirect_url}' \
       -H @"$redirect_headers" "${PREVIEW_URL%/}${SOURCE_PATH}")
     curl_exit=$?
     printf '%s\n' "$result"  # Expect the specified status and destination.
     exit "$curl_exit"
   )
   ```
   On public previews, omit the header-file setup and `-H @"$redirect_headers"`. A gone row should return 410 with no redirect destination. Record every row in a redirect verification report with source, expected result, actual result and PASS/FAIL. Capture the HTTP status and curl exit status directly, never through a pipe.
5. **Pattern rules**: test one or two sample paths per splat rule and record them in a "Pattern verification" section.
6. **Re-archive** the redirect verification report and regenerated summary with the migration archive, following `05_automations/client-site-first-build/runbook_appendix/old_website_archive.md`.

## Halts

- Any non-pattern row fails: fix the approved redirect map, re-render, push and re-test.
- Any high-priority destination answers 404 on the preview: halt and ask the site owner.
- The redirect verification report is missing or empty: halt.

Present the DNS cutover pause described in `05_automations/client-site-first-build/runbook_appendix/dns_cutover_pause.md` only when every condition above passes.
