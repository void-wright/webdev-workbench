# Appendix: Redirect Authoring (site ports only)

> Generic edition: written for a site on **Cloudflare Workers with static assets**. On Vercel, use the platform's redirect configuration or middleware when the map exceeds its limits. The mapping logic is unchanged; only the implementation differs.

## Purpose

Turn the discovered old-URL inventory into an approved redirect map, so every URL that people or search engines know resolves to a real destination on the new site at cutover, or returns an intentional gone response. Build the old-URL inventory before mapping slugs, then compare the inventoried URLs with the completed map to catch omissions.

## Layer decision

- **Domain-level moves** (apex ↔ www, old domain → new domain, subdomain consolidation) belong at the edge layer, with DNS routing traffic there. On Workers, the apex is a custom-domain route on the site's Worker, and `www` is a small separate Worker that returns a 301 to the apex while preserving the path and query. Cloudflare Bulk Redirects is an alternative for a whole-domain move.
- **Path-level redirects** live with the site: use the static-assets redirect configuration for 301/302/307/308 rules, and a small Worker route for anything it cannot express, such as 410 Gone responses, conditional logic or very large maps. Read the platform's current static and dynamic rule limits before implementation, and switch to a Worker lookup table when necessary.
- **Apex-canonical is the default**: the apex serves; `www` redirects. The configured site URL, sitemap, crawler directives, canonical tags and agent-facing metadata must all agree on it.

## Inputs

- The discovered old-URL and backlink inventory, plus any redirect chains from the old site.
- The new site's generated sitemap index and its child sitemaps.

## Output

- A JSON redirect map with one entry per source URL and audit metadata.
- A CSV review sheet, approved before applying redirects and placing migrated assets.
- A mapping decision log explaining non-obvious mappings, consolidations, 410 responses and edge cases.

## Default heuristics (the site owner reviews and overrides any row)

| Old URL pattern | Default new URL | Why |
|---|---|---|
| `/about` | `/about` | 1:1 parity when the page exists |
| `/team` | `/about#team` if no `/team` | consolidation; the site owner confirms |
| `/guides/<slug>` | same slug if it exists, else the closest match for review | preserve slugs |
| `/wp-content/uploads/YYYY/MM/<file>` | `/assets/<file>` or a CDN URL | place the asset before enabling its redirect |
| `/?p=NNN` | the canonical URL resolved from Wayback → its new equivalent | permalink queries |
| `/category/<term>`, `/tag/<term>` | a filtered listing, or 410 | the site owner decides |
| `/feed*` | the new feed, or 410 | 410 if there is no feed |
| `/wp-admin/*`, `/wp-login.php` | 410 | retired administration paths have no public replacement |
| `/page/N` | the first page | pagination collapse |
| HIGH-priority, no equivalent | halt and ask | never blind-redirect |
| LOW-priority, no equivalent | 410 | appropriate when review confirms no useful replacement or known inbound links |

Classify WordPress uploads, categories, tags, feeds and administration paths separately before assigning destinations.

## 301 vs 302

301 by default. Use 302 only for an explicitly temporary arrangement, such as an old site retained as a parallel archive, confirmed by the site owner in writing.

## Chains

Never chain through a deprecated middle URL: `/legacy → /new-current` directly, and `/current → /new-current` directly. Walk the old site's recorded redirect chains and flatten them before writing the new rules.

## Redirect map shape

```json
[
  {"source": "/our-story", "destination": "/about", "status": 301, "type": "page", "priority": "high",
   "referrers": ["https://example.org/bakery-guide"], "rationale": "company history moved to the about page"},
  {"source": "/wp-content/uploads/bread-storage-guide.pdf", "destination": "/assets/bread-storage-guide.pdf", "status": 301,
   "type": "asset_pdf", "priority": "high", "hosting_layer": "site_public", "rationale": "linked from an outside article"},
  {"source": "/wp-admin/*", "status": 410, "type": "admin", "priority": "low", "rationale": "admin paths have no public surface"}
]
```

When applying the map, render the 3xx rows as static redirect rules (`/old /new 301`) where supported, and the 410 rows into the Worker's gone-list. Preserve query-dependent mappings in Worker logic if the static configuration cannot express them. Keep the audit metadata in the archived JSON.

A source that already serves its intended destination needs no redirect rule. Retain it in the inventory as a verified unchanged URL, so the audit remains complete without creating a redirect loop.

## Site-owner review

Present totals for all rows, HIGH-priority rows, LOW-priority rows, 410 responses and external outreach, alongside the CSV. The site owner flags changes: change destination, switch 301↔302, return 410 or move to outreach. Repeat the review until the site owner replies "approved".

## Halts

Do not proceed to redirect application and migrated-asset placement until the site owner has explicitly approved the map, every HIGH-priority row has a destination, every asset row has a `hosting_layer`, and every external-outreach row is recorded in the site handoff notes. External outreach is documented for follow-up; it is never treated as an automatic redirect.
