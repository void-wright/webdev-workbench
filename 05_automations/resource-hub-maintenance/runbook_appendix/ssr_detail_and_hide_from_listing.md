# Runbook: detail-page freshness, hide-from-listing and closure checks (generic edition)

**Purpose**: prevent newly published resources from appearing as cards that return 404 until the next build.
**Applies to**: any Sanity-backed Astro hub.

---

## 1. The failure mode: listing and detail in different render modes

The listing fetches Sanity on every request, but the detail route is prerendered with `getStaticPaths()`. The detail route only knows the slugs that existed at the last build. Content published after that build appears as cards whose pages do not exist.

**Rule: the listing and the detail route render the same way.** Two correct shapes:

### 1a. Static both + rebuild on publish (recommended start on Cloudflare Workers)
Prerender both routes and configure Sanity's webhook to fire the platform's deploy hook on every publish or unpublish. See [the Cloudflare Workers redeployment runbook](05_automations/resource-hub-maintenance/runbook_appendix/redeploy_cloudflare_workers.md). Freshness depends on build completion. Nothing at runtime depends on Sanity. Run the closure check in §3.

### 1b. On-request detail (only after measuring caching on Workers)
Keep both the listing and detail routes request-rendered.

```astro
---
export const prerender = false;          // requires the @astrojs/cloudflare adapter
const { slug } = Astro.params;
const resource = await getResourceBySlug(slug!);
if (!resource) return Astro.redirect('/resources/');
Astro.response.headers.set('Cache-Control', 'public, s-maxage=60, stale-while-revalidate=86400');
---
```

Verify caching on the deployment platform. On Vercel, inspect `x-vercel-cache` for a `HIT`. On Cloudflare Workers, do not assume that setting `Cache-Control` caches a Worker's own response. Without an explicit caching mechanism, each request may hit Sanity. Implement caching using a supported mechanism such as the Cache API, then verify repeated requests using cache instrumentation, relevant response headers such as `cf-cache-status` where available, and Sanity request counts. Keep a fallback redirect for missing slugs.

---

## 2. Hide from listing (live by URL, absent from cards)

Use when a page should stay reachable and indexable by its URL but not appear in the library. For example, a kitchen-equipment maker might keep an older oven care guide available through existing links without promoting it in the resource library.

### Schema field (Studio, if you run it)
```ts
defineField({
  name: 'hideFromListing', type: 'boolean', title: 'Hide from resource hub listing',
  description: 'Reachable by direct URL and indexable, but not shown as a card in the listing, related or collection queries.',
  initialValue: false,
}),
```

Studio is optional: the field can be written through the API without a deployed schema.

### Queries
Add `&& hideFromListing != true` to the main listing query, the related-resources query and its top-up fallback, and collection queries. **Leave untouched:** the single-resource lookup, which must stay reachable, and series navigation.

### Patch
Run from the package root, replacing the project and document placeholders:

```bash
bash 06_web_tools/bearer-curl SANITY_API_TOKEN -sS -f -X POST \
  "https://<your-sanity-project-id>.api.sanity.io/v2024-01-01/data/mutate/production" \
  -H "Content-Type: application/json" \
  -d '{"mutations":[{"patch":{"id":"<resource-document-id>","set":{"hideFromListing":true}}}]}'
echo "rc=$?"
```

Check that the mutation succeeded, then rebuild through the deploy hook.

### Verify
```bash
curl -sS -o /dev/null -w 'direct URL: %{http_code}\n' \
  "https://<your-domain>/resources/<slug>/"   # 200

curl -fsS "https://<your-domain>/resources/" |
  rg -oF '/resources/<slug>/' |
  wc -l                                    # 0
```

Also check related-resource and collection listings. For request-rendered listings, inspect the rendered cards if their links are populated in the browser.

The page stays in the sitemap and remains eligible for indexing. For content that must become unavailable, unpublish it instead. If the page may remain accessible but should leave search results, use `noindex` and the relevant search-removal process. For reversible removal from listings and direct access, use `isHidden` in every listing AND detail query.

---

## 3. Per-slug 200 loop (closure after every content deploy)

Source the slug list from the content batch's saved mutation payloads or from GROQ, never from memory. The following example creates temporary files for the query response, slug list, and HTTP results:

```bash
slug_query_file=$(mktemp)
slug_list_file=$(mktemp)
slug_results_file=$(mktemp)

curl -fsSG "https://<your-sanity-project-id>.api.sanity.io/v2024-01-01/data/query/production" \
  --data-urlencode 'query=*[_type=="resource" && defined(htmlBody) && isHidden != true].slug.current' \
  > "$slug_query_file" || exit 1

python3 -c '
import json, sys
slugs = json.load(sys.stdin)["result"]
if not slugs or any(not isinstance(s, str) or not s.strip() for s in slugs):
    raise SystemExit("Expected a nonempty list of valid slugs")
print("\n".join(slugs))
' < "$slug_query_file" > "$slug_list_file" || exit 1

while IFS= read -r slug; do
  printf '%s %s\n' \
    "$(curl -sS -o /dev/null -w '%{http_code}' "https://<your-domain>/resources/$slug/")" \
    "$slug"
done < "$slug_list_file" > "$slug_results_file"

cat "$slug_results_file"
awk '$1 != "200" { failures++ } END { print failures+0; exit(failures > 0) }' \
  "$slug_results_file"                      # must print 0
```

Zero non-200 responses are tolerated. On a failure, check in order:

1. Is the document published in Sanity?
2. Did a build run after publication? Check the platform's build history.
3. Is the route prerendered, and did the build see the slug?
4. Fix the root cause and rerun the loop.

---

## 4. Local build gate (before every push)
```bash
npx astro build
echo "rc=$?"    # must be 0
```

A literal `</script>` inside a string or comment within a script element can terminate the element and break the build at a confusing location. A local build catches this before the remote build runs. Never put a literal `</script>` in a script element body, even in a comment.
