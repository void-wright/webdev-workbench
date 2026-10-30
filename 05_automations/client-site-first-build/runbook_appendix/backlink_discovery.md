# Appendix: Backlink Discovery (Step 1.5)

> Used at Step 1.5 of the workflow defined here. Runs ONLY when `IS_SITE_PORT == true`. Skip entirely for greenfield builds.

## Purpose

When porting an existing site to a new tech stack, every known external inbound link to the OLD site should resolve to a real destination on the NEW site at cutover. Broken links interrupt visitors and can undermine search visibility. Uploaded files need the same attention as pages.

This step produces `backlinks_discovered.json`: a map joining (A) own-URL inventory and (B) third-party referrer discovery. It records what was found and which sources were unavailable; it does not prove that every backlink has been discovered.

## Two-Axis Discovery Split

The work is split into two complementary sub-problems with different sources:

| Sub-problem | What it answers | Sources |
|---|---|---|
| **(A) Own-URL inventory**: the redirect-FROM set | "What URLs existed on the OLD site? What needs a redirect rule?" | sitemap.xml, Wayback CDX, Common Crawl own-domain captures, WordPress exports |
| **(B) Third-party referrer discovery**: the why-they-matter set | "Which old URLs receive links from external sites?" | Google Search Console, Bing Webmaster, GitHub code search, supplier directories, manual search and owner-provided lists |

Sitemap.xml and Wayback answer (A). They do not identify third-party sites that link to us. Search Console and other backlink sources answer (B). The Common Crawl URL index used below contributes to (A), not a reverse-link lookup for (B).

The redirect-priority decision later joins both:

- **HIGH-priority** = URL appears in (A) AND has at least one third-party referrer in (B).
- **LOW-priority** = URL appears only in (A), with no discovered external referrers. Consider a 410 response only after confirming there is no useful replacement or reason to retain it.
- **EXTERNAL-OUTREACH** = a referrer in (B) points to a URL confirmed never to have existed on the old site. Document it for possible contact with the referring site; do not automatically redirect it. Absence from the inventory alone is not proof that a URL never existed.

## Tier Structure

### Tier 1 (default for every site-port build)

Always runs. Comprises four sources:

- **Step A0: Sitemap.xml fetch (A)**: fetch published sitemap entries.
- **Step A1: Wayback CDX (A)**: recover archived own-site URLs.
- **Step A2: Google Search Console export (B)**: ⏸️ **PAUSE POINT #1**: the user verifies access if needed and exports available link data. See `05_automations/client-site-first-build/runbook_appendix/gsc_export_pause.md`.
- **Step A3: Common Crawl cdx-toolkit (A)**: extend the own-URL inventory from crawl captures.

### Tier 2 (opt-in `--with-tier2`, additional discovery sources)

- **Step A4: Bing Webmaster**: export available backlink data; domain verification may be required.
- **Step A5: GitHub code search**: search for old-domain references with `gh search code "OLD_DOMAIN"`.
- **Step A6: Supplier and stockist directories**: inspect relevant public listings, such as a kitchen-equipment maker's dealer pages.

### Tier 3 (opt-in `--with-tier3`, targeted manual discovery)

- **Step A7: Partner resource pages**: inspect known links from partners, such as a bicycle-parts company's fitting guides referenced by repair shops.
- **Step A8: DuckDuckGo searches**: search for the old domain, narrowing to likely referring sites with `site:` operators.
- **Step A9: Manual outreach list**: review URLs provided by the site owner.

**Combined Tier 1+2+3 coverage**: unknown. Private, blocked, unindexed and dynamically rendered pages can remain undiscovered. A paid backlink index may add evidence, but no source guarantees complete coverage.

The option names in this appendix describe run choices to record. They do not imply that a packaged command implements them.

## Phase A: Discovery (parallelized where flagged)

Create a working directory named `backlink_discovery` inside the build workspace. The filenames below are generated artifacts, not files supplied with Voidwright. Write results in batches and report counts and errors rather than pasting entire datasets into the conversation.

### Step A0: Sitemap.xml fetch (A)

```bash
mkdir -p backlink_discovery
cd backlink_discovery

OLD_DOMAIN="example.com"  # Replace with the old site's domain.

for sm in /sitemap.xml /sitemap_index.xml /wp-sitemap.xml /sitemap-1.xml; do
  curl --fail --silent --show-error --location --max-time 30 \
    "https://${OLD_DOMAIN}${sm}" -o "sitemap_$(basename "$sm")"
done

python3 - <<'PY'
import glob
import json
import urllib.request
import xml.etree.ElementTree as ET

urls = set()
pending = []
seen_sitemaps = set()

def collect(root):
    kind = root.tag.split("}")[-1]
    for el in root.iter():
        if el.tag.split("}")[-1] != "loc" or not el.text:
            continue
        value = el.text.strip()
        if kind == "sitemapindex":
            pending.append(value)
        elif kind == "urlset":
            urls.add(value)

for filename in glob.glob("sitemap_*.xml"):
    try:
        collect(ET.parse(filename).getroot())
    except (ET.ParseError, OSError) as exc:
        print(f"Could not parse {filename}: {exc}")

while pending:
    url = pending.pop()
    if url in seen_sitemaps:
        continue
    seen_sitemaps.add(url)
    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            collect(ET.fromstring(response.read()))
    except Exception as exc:
        print(f"Could not fetch nested sitemap {url}: {exc}")

with open("sitemap_urls.json", "w") as output:
    json.dump(
        [{"url": url, "source": "sitemap"} for url in sorted(urls)],
        output,
        indent=2,
    )
print(f"{len(urls)} URLs from sitemaps")
PY
```

**Caveat (port-010)**: a sitemap lists only the URLs its publisher includes. Orphaned pages, hidden resources and manually unlinked URLs may be absent. Wayback (A1) can recover some previously public URLs, but cannot reliably recover unpublished drafts.

### Step A1: Wayback CDX (A)

**Direct fetch (preferred when TLS to web.archive.org works from your machine)**:

```bash
python3 - <<'PY'
import json
import requests

OLD_DOMAIN = "example.com"
response = requests.get("https://web.archive.org/cdx/search/cdx", params={
    "url": OLD_DOMAIN,
    "matchType": "domain",
    "output": "json",
    "collapse": "urlkey",
    "fl": "original,timestamp,statuscode",
    "filter": "!statuscode:[45].."
}, timeout=120)
response.raise_for_status()
data = response.json()
urls = sorted({row[0] for row in data[1:] if row[2] == "200"})

with open("wayback_urls.json", "w") as output:
    json.dump(
        [{"url": url, "source": "wayback"} for url in urls],
        output,
        indent=2,
    )
print(f"{len(urls)} unique own-site URLs from Wayback")
PY
```

**Cloudflare Browser Rendering fallback (use when a local TLS handshake to web.archive.org fails or repeatedly times out). Check current availability and billing before use.**

Set `VOIDWRIGHT_ROOT` to the absolute path of your Voidwright checkout before running the fallback commands.

```bash
# The configured token needs Browser Rendering permission.
# cf-api sends it without printing it.
: "${VOIDWRIGHT_ROOT:?Set VOIDWRIGHT_ROOT to your Voidwright checkout}"
: "${OLD_DOMAIN:?Set OLD_DOMAIN to the old site's domain}"

WB_URL="https://web.archive.org/cdx/search/cdx?url=${OLD_DOMAIN}&matchType=domain&output=json&collapse=urlkey&fl=original,timestamp,statuscode,mimetype&filter=!statuscode:%5B45%5D..&limit=10000"

bash "$VOIDWRIGHT_ROOT/06_web_tools/cf-api" POST '/accounts/{account}/browser-rendering/content' \
  "{\"url\":\"${WB_URL}\",\"gotoOptions\":{\"waitUntil\":\"domcontentloaded\",\"timeout\":55000}}" \
  > cf_response.json

# The rendered response may contain CDX JSON inside a <pre> tag.
python3 - <<'PY'
import html
import json
import re

with open("cf_response.json") as source:
    outer = json.load(source)
if not outer.get("success"):
    raise SystemExit("Browser Rendering failed; inspect the saved response.")

match = re.search(r"<pre[^>]*>(.*?)</pre>", outer["result"], re.DOTALL)
if not match:
    raise SystemExit("No CDX data block found in the rendered response.")

data = json.loads(html.unescape(match.group(1)))
if not data:
    raise SystemExit("No CDX rows returned; record this source as empty.")

headers = data[0]
items = []
seen = set()
for values in data[1:]:
    row = dict(zip(headers, values))
    original = row.get("original")
    if row.get("statuscode") != "200" or not original or original in seen:
        continue
    seen.add(original)
    items.append({
        "url": original,
        "timestamp": row.get("timestamp"),
        "mimetype": row.get("mimetype"),
        "source": "wayback",
    })

with open("wayback_urls.json", "w") as output:
    json.dump(items, output, indent=2)
print(f"{len(items)} unique URLs from Wayback via Browser Rendering")
if len(data) - 1 >= 10000:
    print("Query reached its limit; retrieve remaining results before merging.")
PY
```

When direct access fails, this fallback routes the request through Cloudflare's network. Record failed requests and result limits so a partial response is not mistaken for a complete inventory.

### Step A2: Google Search Console export (B): ⏸️ PAUSE POINT #1

See `05_automations/client-site-first-build/runbook_appendix/gsc_export_pause.md` for the user-facing export instructions. Continue A1 and A3 independently during the user-side wait, then halt before merging Tier 1 sources until either:

- The user delivers the export, saved as `gsc_backlinks.csv`, and signals "GSC export ready".
- The user explicitly opts out with `--skip-gsc`. Record that choice in metadata and describe the resulting gap in referrer discovery.

Distinguish source-page URLs from reports that provide only referring domains or target-page totals. Do not invent source-page URLs from aggregated data.

### Step A3: Common Crawl cdx-toolkit (A+B)

This step contributes to the overall A+B discovery process through own-domain captures (A). The open index query below does not discover third-party referrers (B).

**Direct (preferred when TLS to index.commoncrawl.org works from your machine)**:

```bash
# Own-domain captures (A): extends the own-URL inventory.
cdxt --cc --crawl 3 --filter '=status:200' --limit 5000 \
  iter "*.${OLD_DOMAIN}/*" --jsonl > cc_own_captures.jsonl

# The open Common Crawl index API does not support a linksto: filter.
# Use GSC and the other referrer sources for (B).
# Record the crawl range and result limit; extend the query if it hits the cap.
```

**Cloudflare Browser Rendering fallback (when TLS to index.commoncrawl.org fails).**

```bash
# The configured token needs Browser Rendering permission.
: "${VOIDWRIGHT_ROOT:?Set VOIDWRIGHT_ROOT to your Voidwright checkout}"
: "${OLD_DOMAIN:?Set OLD_DOMAIN to the old site's domain}"

# Discover available Common Crawl indexes.
bash "$VOIDWRIGHT_ROOT/06_web_tools/cf-api" POST '/accounts/{account}/browser-rendering/content' \
  '{"url":"https://index.commoncrawl.org/collinfo.json","gotoOptions":{"waitUntil":"domcontentloaded","timeout":55000}}' \
  > cc_collinfo.json

# Extract three recent index identifiers from the returned listing.
python3 - <<'PY'
import html
import json
import re

with open("cc_collinfo.json") as source:
    outer = json.load(source)
if not outer.get("success"):
    raise SystemExit("Index discovery failed; inspect the saved response.")
match = re.search(r"<pre[^>]*>(.*?)</pre>", outer["result"], re.DOTALL)
if not match:
    raise SystemExit("No index listing found in the rendered response.")
indexes = json.loads(html.unescape(match.group(1)))
with open("cc_index_ids.txt", "w") as output:
    for entry in indexes[:3]:
        output.write(entry["id"] + "\n")
PY

# Query the listed indexes for own-domain URLs.
while IFS= read -r CC_ID; do
  bash "$VOIDWRIGHT_ROOT/06_web_tools/cf-api" POST '/accounts/{account}/browser-rendering/content' \
    "{\"url\":\"https://index.commoncrawl.org/${CC_ID}-index?url=*.${OLD_DOMAIN}&output=json\",\"gotoOptions\":{\"waitUntil\":\"domcontentloaded\",\"timeout\":55000}}" \
    > "cc_${CC_ID}.json"
done < cc_index_ids.txt

# Parse NDJSON inside each <pre> tag and deduplicate across indexes.
python3 - <<'PY'
import glob
import html
import json
import re

records = {}
for filename in glob.glob("cc_CC-MAIN-*.json"):
    with open(filename) as source:
        outer = json.load(source)
    if not outer.get("success"):
        print(f"Failed query: {filename}")
        continue
    match = re.search(r"<pre[^>]*>(.*?)</pre>", outer["result"], re.DOTALL)
    if not match:
        print(f"No data block: {filename}")
        continue
    content = html.unescape(match.group(1)).strip()
    if not content.startswith("{"):
        print(f"No usable records: {filename}")
        continue
    for line in content.splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            print(f"Malformed record: {filename}")
            continue
        url = row.get("url")
        if url and str(row.get("status")) == "200" and url not in records:
            records[url] = {
                "url": url,
                "timestamp": row.get("timestamp"),
                "mime": row.get("mime"),
                "status": row.get("status"),
                "source": "common_crawl",
            }

with open("cc_own_captures.json", "w") as output:
    json.dump(list(records.values()), output, indent=2)
print(f"{len(records)} unique Common Crawl URLs")
PY
```

Use the returned index listing rather than guessing identifiers. Record query failures, pagination and truncation limits before treating results as ready to merge.

### Tier 2 (only if `--with-tier2`)

```bash
# A4: Export available Bing Webmaster backlink data manually.
# A5: Search GitHub code for old-domain references.
gh search code "${OLD_DOMAIN}" --limit 100 --json url,name,repository > github_refs.json
# A6: Inspect relevant supplier and stockist directories manually.
# Save candidate referring page URLs and the old-site targets they mention.
```

A GitHub search hit is a candidate reference, not automatically a verified backlink. Inspect the result and record its actual link context.

### Tier 3 (only if `--with-tier3`)

```bash
# A7: Inspect known partner resource pages for old-site links.
# A8: Search DuckDuckGo manually for the old domain.
# Narrow searches to likely referring sites with site: operators.
# A9: Review the site owner's CSV of possible referring pages.
```

## Phase A.4: Chain Old-Site Existing Redirects (port-013)

WordPress sites can accumulate years of `.htaccess` redirects. Fetching only the current sitemap misses their source URLs. Use two paths:

1. Ask the site owner for an `.htaccess` export or equivalent redirect configuration.
2. Query Wayback CDX for historical redirects using a `statuscode:301` filter. Confirm destinations from available captures or live responses.

Output: `legacy_redirect_chains.json`. During redirect authoring, map each legacy chain `oldX → currentY` directly to `oldX → newY_equivalent`. Avoid routing through a deprecated intermediate URL. Extra hops add latency and create more opportunities for failure; see port-005.

## Phase B: Verification (Scrapy)

For each unique candidate referrer URL from the available backlink sources, fetch the page and confirm that an `<a href>` still points to the old domain. A minimal Scrapy spider with a start-URL list and a callback that extracts matching links is enough. Resolve relative links before comparing domains.

Output: `backlinks_verified.json` with rows of `(referrer_url, target_old_url, anchor_text, status_code)`. Keep blocked, failed and unverifiable candidates in a separate review record rather than silently treating them as absent links.

**Token-budget discipline**: restrict Scrapy fetches to the deduplicated candidate referrer set, not the own-site Wayback inventory. Report summary counts and exceptions. The verification workload depends on the number of candidate referring pages.

## Phase C: Categorize

For each verified backlink, classify the target. Apply WordPress URL-pattern categorization (port-012) when the OLD site is WordPress:

| Pattern | Category | Default decision |
|---|---|---|
| `/wp-content/uploads/YYYY/MM/*` | `asset_pdf` / `asset_image` / `asset_other` | Preserve the file on the new site or map to a suitable replacement |
| `/?p=NNN` | `permalink_query` | Resolve to a canonical slug using the WordPress export or archive, then 301 |
| `/category/*` | `taxonomy_archive` | User decides: redirect to the closest relevant content hub or return 410 |
| `/tag/*` | `taxonomy_archive` | Same as category |
| `/feed/*` | `rss_endpoint` | User decides: keep, redirect or return 410 |
| `/wp-admin/*` | `admin` | Return 410 when WordPress administration is retired |
| `/wp-login.php` | `admin` | Return 410 when WordPress login is retired |
| `/page/N` | `pagination` | Map to an equivalent listing page; use the first page only when it remains a useful destination |
| any other | `page` | Review and map individually during redirect authoring |

Output: `backlinks_discovered.json` with categorized, deduplicated items and priority flags joining (A) and (B).

The following is an invented, abbreviated garden-supply example. Its date is a format placeholder, and its counts describe the example rather than a past project. Actual totals must match the full generated inventory.

```json
{
  "metadata": {
    "old_domain": "old-willowcart.example",
    "discovery_date": "YYYY-MM-DD",
    "tier": 1,
    "skip_gsc": false,
    "is_wordpress_origin": true,
    "totals": {
      "own_urls_inventory": 3,
      "third_party_referrers": 2,
      "high_priority": 2,
      "low_priority": 1,
      "external_outreach": 0,
      "legacy_redirect_chains": 0
    }
  },
  "items": [
    {
      "old_url": "/wp-content/uploads/2024/08/planter-sizing-guide.pdf",
      "category": "asset_pdf",
      "priority": "high",
      "referrers": ["https://courtyard-club.example/resources"],
      "hosting_layer": null,
      "decision": null
    },
    {
      "old_url": "/?p=746",
      "category": "permalink_query",
      "priority": "low",
      "referrers": [],
      "decision": null
    },
    {
      "old_url": "/guides/balcony-watering",
      "category": "page",
      "priority": "high",
      "referrers": ["https://weekend-growers.example/container-gardens"],
      "decision": null
    }
  ]
}
```

Fill `decision` and, where applicable, `hosting_layer` during user review of the redirect plan. See `05_automations/client-site-first-build/runbook_appendix/redirect_authoring.md`.

## Step 1.5j: Archive

After Phase C completes, copy all raw, intermediate and final artifacts into a persistent migration archive outside the temporary build directory. Include a mapping summary describing source coverage, failures, exclusions and unresolved decisions. See `05_automations/client-site-first-build/runbook_appendix/old_website_archive.md`.

This archive is the canonical record that survives build-folder cleanup.

## Mandatory Pause-Point Discipline

Halt Step 1.5 if any of these conditions apply:

- `gsc_backlinks.csv` is missing and `--skip-gsc` was not selected: halt at Pause Point #1 (port-009).
- Phase B verification has not run on the deduplicated candidate referrer set: halt. If that set is empty, record why and review discovery gaps.
- `backlinks_discovered.json` lacks metadata or contains zero items: halt and ask the user to resolve the missing evidence.

Do not advance to redirect authoring without a reviewed `backlinks_discovered.json` that records source limitations and unresolved cases, as required by port-001.
