# Adding a NEW resource type to a hub (runbook module, generic edition)

**When to read this:** the site owner wants a resource that is not one of the existing types ("a Case Study", "a
How-to", "a Customer Story") and wants it **classified separately** in the library. For example, a ceramic studio
might add customer stories alongside its guides.

**Recall:** when adding a resource type or diagnosing a missing card image, check both the taxonomy and the
thumbnail defaults.

---

## The core insight: LAYOUT and CLASSIFICATION are orthogonal

| field | controls | example |
|---|---|---|
| `pagePattern` | which **template** renders the page | `blog` → the article template |
| resource-type **taxonomy ref** | how the resource is **classified, badged, filtered** | `resource-kind-customer-story` |

They are independent. **A new TYPE almost never needs a new TEMPLATE.** A customer story can use the existing
article template, including its CSS and scroll-spy, while carrying its own taxonomy. It then appears in badges
and filters as a customer story. Reuse the layout and give the resource its own classification.

Cost of a new type: **one Sanity doc + a few small code edits** when the existing template already fits.
Check the hardcoded maps before estimating the work.

---

## Checklist

### 1. Taxonomy document (Sanity)
```json
{ "_id": "resource-kind-<slug>", "_type": "taxonomy",
  "category": "type", "title": "<Title Case>",
  "slug": { "_type": "slug", "current": "<slug>" } }
```
The `category` value is what makes it a type rather than a topic/product facet; use whatever category name the
hub's schema already uses for types (read it, don't guess). Use `createOrReplace` with a **fixed `_id`** so a re-run
is idempotent.

### 2. Type-default thumbnail (Sanity): even if a real image is coming
```
hubConfig.defaultThumbnails["<slug>"] = "<cdn url>"
```
⚠️ **A hyphenated key cannot be used directly in a dot-notation Sanity patch path.**
For example, `set: {"defaultThumbnails.customer-story": url}` can fail with
`Syntax error. (Illegal token "-")`. **Mutations within a transaction are atomic**, so the other changes in that
transaction will not be applied either. Check the error response. **Read the whole object, add the key in code,
and `set` the entire object back.** Coordinate concurrent edits so this replacement does not overwrite another change.

Wire the placeholder at the **type** level, never on the resource. When the real image arrives, set the
resource's `featuredImage` and let it override the default. Ensure the rendering code treats an empty image value
as missing and falls back to the type default. This leaves no resource-level placeholder to hunt down later.

### 3. Code touchpoints: grep for every hardcoded map
Run this from the site's source directory:
```bash
rg -n 'getBadgeLabel|getCTALabel|TYPE_LABELS|TYPE_CTAS|TOPIC_ORDER' .
```

| place | symptom if missed |
|---|---|
| the card component's badge-label map | card badge silently reads "Resource" |
| the card component's CTA-label map | CTA falls back to "Read more" |
| **the detail template's OWN separate badge map** | **eyebrow on the resource page reads "Resource"** |
| any sync/ingest script's type-title map | new docs get the slug as their display title |

A detail template may carry a **second, independent** label map rather than importing the card component's map.
These maps can drift. The mismatch is invisible on the library page and shows only on the resource page itself,
which is the page people share. Update both maps, or consolidate them into a shared source.

**No change needed** where facets are derived from taxonomy docs: the new type appears in the filter by itself.
A curated "browse by topic" list is optional; skip it until the type has enough resources to look populated.

### 4. Resource document
Mirror a relevant sibling's other taxonomies so related resources and filters behave, swapping only the type ref
where the other classifications still apply. If the hub stores CSS per document, ship the template CSS on the doc
plus any page-scoped additions.

### 5. Verify on the deployed preview
Set these variables to the preview URLs and the new type's display title. For a protected preview, use the site's
supported authentication method when fetching it.
```bash
# Check that the type title appears on the library page.
curl --fail --silent --show-error "$LIBRARY_PREVIEW_URL" | grep -Fc "$TYPE_TITLE"
# Check the resource page too: this catches a missed detail-template map.
curl --fail --silent --show-error "$RESOURCE_PREVIEW_URL" | grep -Fc "$TYPE_TITLE"
```
These text checks are only a first pass. Open the deployed preview and verify the card badge, CTA, filter facet,
and thumbnail on the library page. Then open the resource page and inspect its badge and layout. Confirm that
filtering by the new type returns the intended resource.

---

## Placeholder images (per-type)

Sample the palette from a **live** thumbnail on the site, not from memory. A remembered palette can produce
placeholders that look too light or otherwise inconsistent beside existing images. Use one centred motif per type,
thin uniform strokes, generous margins, and **zero text/letters/numbers/logos**. Do not include proposed overlay
wording in an image prompt.

Generate with an available image tool. For unattended CLI generation, use a securely configured credential,
close stdin, and set a timeout. Convert to WebP (`cwebp -q 86`), and **look at every image before shipping**
to check the motif and catch accidental text.

## Reference
[Sanity content operations](05_automations/resource-hub-maintenance/runbook_appendix/sanity_content_ops.md) ·
[Cloudflare Workers redeployment](05_automations/resource-hub-maintenance/runbook_appendix/redeploy_cloudflare_workers.md) ·
[Resource slug design](03_skills/resource-slug-design-canonical/SKILL.md).
Treat the slug as permanent and apply the slug-design guidance before publishing.
