# Appendix: GSC Export Pause (Pause Point #1)

> Use during backlink discovery. Runs ONLY when `IS_SITE_PORT == true` AND `--skip-gsc` was not passed. This is the first pause for user input in a site-port build.

## Purpose

Google Search Console (GSC) provides Google's report of external links to a verified site. It is useful evidence for preserving linked URLs during a migration, but it is not a complete inventory of backlinks or ranking signals. A domain property requires DNS TXT verification unless ownership is already verified, followed by a manual CSV export. While the user completes those tasks, run Wayback and Common Crawl discovery in parallel.

This pause is **encoded as a soft halt**: Wayback and Common Crawl discovery can complete during the wait, but the merged discovery results are NOT finalized until either the GSC CSV arrives OR `--skip-gsc` is set explicitly.

## Assistant's Voice (printed verbatim at start of backlink discovery)

> *"Backlink discovery is starting. Wayback CDX and Common Crawl discovery will run automatically in the background and need no setup from you. You'll need to export Google Search Console data manually. A domain property requires DNS verification on the old domain. I won't finalize the merged discovery results until you deliver the CSV or explicitly skip GSC.*
>
> *Step 1: Open https://search.google.com/search-console using your own Google account. Check whether you already have access to the old domain's property.*
>
> *Step 2: If you need to add it, click 'Add property' → 'Domain' → enter `<OLD_DOMAIN>` (e.g. example.com).*
>
> *Step 3: Google will show a TXT record. Copy the entire `google-site-verification=...` string.*
>
> *Step 4: Log into the domain's DNS provider, which may be the registrar or Cloudflare. Open DNS for `<OLD_DOMAIN>` and add a TXT record at the domain apex. Use `@` if your provider uses that notation. Set the value to Google's string and the TTL to 1 hour. Save.*
>
> *Step 5: Allow time for DNS propagation, then click 'Verify' in GSC. Verification may work within minutes, but some providers take longer.*
>
> *Step 6 (data wait): An existing property may already have link data. A newly added property may need several days to populate reports. Verification alone does not guarantee that link data will appear immediately.*
>
> *Step 7: In GSC, navigate to 'Links' → 'External links' → 'Top linked pages'. Open the full report and export it as CSV.*
>
> *Step 8: Place the CSV in the build workspace and provide its location.*
>
> *Step 9: Tell me 'GSC export ready' and I'll read it, deduplicate the discovered URLs across Wayback, Common Crawl and GSC, and complete backlink discovery."*
>
> *Skip option: if you don't want to use GSC for this run, tell me '--skip-gsc'. We'll proceed without that source. The discovery metadata will record the skip reason so future audits can identify the coverage limitation.*

## Continuation Phrases

Phrases the assistant accepts from the user:

- **"GSC export ready"** OR **"GSC ready"** OR **"GSC done"**: The assistant reads the supplied CSV, validates that it parses, merges its URLs into the discovery results, and proceeds to URL verification.
- **"--skip-gsc"** OR **"skip GSC"**: The assistant marks `metadata.skip_gsc = true` in the discovery results, documents the reason ("user opt-out for this run"), and proceeds without GSC data.

If the user supplies a file outside the build workspace, the assistant accepts that location and copies the file into the workspace before processing it.

## CSV Format Validation

GSC offers several external-link report views:

- `Top linking sites`: referring domains.
- `Top linked pages`: destination pages on the verified site. **This is the report needed here.**
- `Top linking text`: anchor text.

The assistant expects **"Top linked pages"** and can also accept the other reports as supplementary evidence. Validate the actual headers rather than assuming every export has identical labels. The fields of interest are:

- The target page: an old URL on example.com that has external links.
- The external-link count: the reported number of links to that page. Do not treat it as a count of unique referring sites.

After processing, the assistant surfaces a summary:

```text
GSC processed: <N> linked pages, total <M> reported external links
Top 10 linked pages by reported external-link count: [...]
Cross-reference with Wayback and Common Crawl: <X> URLs matched the old-site URL inventory
```

If GSC reports a URL missing from the old-site inventory, flag it for investigation. Missing archive or sitemap evidence does not establish that the URL never existed. Check for a typo in a referring link, an unarchived page, or a legacy redirect missed during discovery before deciding whether to add a redirect or request an external-link correction.

## Failure Modes

### "Verify" fails in GSC

Common reasons:

- The DNS TXT record has not propagated yet. Wait 15–60 minutes and retry; some providers may take longer.
- The TXT record was added to the wrong host. A domain property's record belongs at the apex, not `www`.
- The DNS interface altered the record value. Check that the stored value matches Google's string, allowing for quotation marks used only by the interface to display TXT data.

The assistant offers troubleshooting:

> *"If verification fails, run `dig TXT example.com` from your terminal and check for the Google verification string. Confirm that you edited the authoritative DNS provider for the domain. A saved record may take time to reach other resolvers; wait 30 minutes and retry."*

### CSV is empty or has zero rows

An empty export means the selected report contains no rows. It does not prove that the old site has no backlinks. Check whether:

- The property is newly added and reports are still populating.
- The correct property and external-link report were selected.
- The site has crawl restrictions that merit separate investigation. Do not change those restrictions without understanding why they exist.

Allow time for reporting to populate, then try the export again. If no usable data is available, the assistant accepts `--skip-gsc` and proceeds with Wayback and Common Crawl only, recording the limitation.

### User wants to skip but already did the TXT verification

No additional action is needed. The verification record can stay in place if continued GSC access is wanted. Google may recheck ownership, so preserve the record when moving DNS if ongoing verification depends on it.

## Post-Cutover Note

After the DNS cutover, use the old domain's GSC property alongside redirect tests and request logs to monitor migration health. Review reported not-found URLs against the redirect inventory. A missing redirect for a valuable old URL should be corrected; not every reported 404 requires a redirect.

Document the GSC property, its access requirements, any skipped exports, and the monitoring responsibility in the site handoff notes so the person maintaining the site can continue those checks.
