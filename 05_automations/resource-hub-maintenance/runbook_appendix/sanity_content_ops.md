# Sanity content ops cookbook (generic edition)

> Day-to-day Sanity operations for your resource library, using the **Sanity HTTP API and your own
> token**. Writes go through the package's `06_web_tools/bearer-curl`, which loads `SANITY_API_TOKEN`
> from your configured credentials and hands it to curl on standard input, so the token is never printed
> or placed on a command line. See
> `05_automations/resource-hub-maintenance/runbook_appendix/second_account_sanity_and_external_writer.md`.

Conventions used below, with commands run from the package root:
```bash
PID="<your-sanity-project-id>"   # from your site's Sanity configuration
DS=production
API="https://$PID.api.sanity.io/v2024-01-01"
BC=./06_web_tools/bearer-curl
# reads need no token on a public-read dataset; writes go through bearer-curl
q() { curl -sG "$API/data/query/$DS" --data-urlencode "query=$1"; }
# private dataset? read with the token instead:
# q() { bash "$BC" SANITY_API_TOKEN -sG "$API/data/query/$DS" --data-urlencode "query=$1"; }
```

## Op 0: Before any write
- Check Sanity's current request limits and plan batch sizes before a bulk job.
- **Dry-run:** print the mutation body you are about to send and the list of slugs; check slug collisions:
  `q 'count(*[_type=="resource" && slug.current in ["choosing-baking-trays","caring-for-cookware"]])'`
  must be 0 for new docs.
- Representative first: send ONE document, read it back, then the batch.

## Op 1: Add resources (atomic, idempotent)
This example adds a guide to a fictional kitchen-equipment maker's library. Replace the example publication
date with the resource's actual date.
```bash
cat > /tmp/resource-mutation.json <<'JSON'
{"mutations":[
  {"createOrReplace":{"_id":"taxonomy-format-buying-guide","_type":"taxonomy","category":"type",
    "title":"Buying Guide","slug":{"_type":"slug","current":"buying-guide"}}},
  {"createOrReplace":{"_id":"resource-baking-tray-guide","_type":"resource","title":"Choosing Baking Trays",
    "slug":{"_type":"slug","current":"choosing-baking-trays"},"abstract":"Compare tray shapes, finishes, and storage needs.",
    "publishedDate":"2025-04-17",
    "taxonomies":[{"_type":"reference","_key":"formatRef","_ref":"taxonomy-format-buying-guide"}]}}
]}
JSON
bash "$BC" SANITY_API_TOKEN -s -X POST "$API/data/mutate/$DS?returnIds=true" \
  -H "Content-Type: application/json" --data @/tmp/resource-mutation.json > /tmp/resource-mutation.out
echo "rc=$?"
cat /tmp/resource-mutation.out
```
All-or-nothing: one bad operation rolls back the whole transaction, including an improperly expressed patch
path containing a hyphen. See
`05_automations/resource-hub-maintenance/runbook_appendix/new_resource_type.md`.
Deterministic `_id`s make a re-run update in place. Because `createOrReplace` replaces the document, use it
only when the payload represents the complete intended document. Then read back:
`q '*[_id=="resource-baking-tray-guide"][0]{title,"slug":slug.current,"tags":taxonomies[]->title}'`.

Rate limits: keep approximately 100 ms between single creates and 200 ms after uploads if you loop; prefer one
transaction within the API's limits. Retry 429 responses with backoff (2 / 4 / 8 s), respecting any server
retry guidance.

## Op 2: Upload an asset
Set `PDF_SOURCE` to the local PDF you intend to upload. The uploaded filename below is an invented example.
```bash
PDF_SOURCE="<path-to-your-pdf>"
bash "$BC" SANITY_API_TOKEN -s -X POST "$API/assets/files/$DS?filename=baking-tray-buying-guide.pdf" \
  -H "Content-Type: application/pdf" --data-binary @"$PDF_SOURCE" > /tmp/resource-asset.out
echo "rc=$?"
# images: $API/assets/images/$DS
```
Asset IDs are based on content hashes, so identical bytes reuse the existing asset within the dataset.
Before uploading a PDF, set its `/Title` metadata to the resource title. Design-tool exports may carry
generic titles such as "Untitled", which browsers display as the tab name. Then patch the resource:
`fileAsset: {_type:"file", asset:{_type:"reference", _ref:"<asset _id>"}}`; for cards that render `src`
directly, store the image's **CDN URL string**, not an image object.

## Op 3: Retag a resource
After creating the relevant taxonomy terms, replace the resource's tag references:
```json
{"mutations":[{"patch":{"id":"resource-baking-tray-guide",
  "set":{"taxonomies":[{"_type":"reference","_key":"formatRef","_ref":"taxonomy-format-buying-guide"},
                       {"_type":"reference","_key":"topicRef","_ref":"taxonomy-topic-bakeware"}]}}}]}
```
Ground every tag in the resource's own content; tag an additional use only when the body covers it.

## Op 4: New taxonomy term
`createOrReplace` a taxonomy document with a deterministic ID and a **Title Case** `title`, never the slug
as its title. For example, the referenced `taxonomy-topic-bakeware` document would use category `topic`,
title `Bakeware`, and slug `bakeware`.

The library's facets are derived from taxonomy documents, so the term appears once a resource references it.

## Op 5: Collections
For a fictional bicycle-parts company's guides:
```json
{"createOrReplace":{"_id":"collection-wheel-care","_type":"collection","title":"Wheel Care",
  "slug":{"_type":"slug","current":"wheel-care"},"filterCategory":"topic","filterValue":"wheel-care*"}}
```
A wildcard value aggregates a family when the collection query supports wildcard matching.
Use a 4:3 featured image and a 16:9 hero image.

## Op 6: Article series with images/audio
For a fictional ceramic studio's how-to series, upload every image and audio file (Op 2), replace every
placeholder in the bodies with the CDN URLs, create the `series` document, and set `series` + `seriesOrder`
on each part. Prove zero placeholders twice: use GROQ
(`*[_type=="resource" && htmlBody match "*PLACEHOLDER*"]`; note that `match` tokenizes, so it is not a
substring test), then search the generated output after the build:
```bash
BUILD_OUTPUT="<your-build-output-directory>"
rg -n 'PLACEHOLDER' "$BUILD_OUTPUT"
```
Both checks must return no placeholder matches. Inspect command errors separately; a failed check is not
proof of absence.

## Op 7: Placeholders and graduation
Placeholders carry `isPlaceholder: true` and the tag `PLACEHOLDER_REMOVE_BEFORE_LAUNCH`. When real content replaces the
temporary entries, review and bulk-delete the placeholders:
```bash
q '*[isPlaceholder == true || "PLACEHOLDER_REMOVE_BEFORE_LAUNCH" in tags]._id'   # review the list first
# then one transaction of {"delete":{"id":...}} ops
```

## Op 8: Freshness
Build-time reads use `useCdn: false`. If a build right after a patch shows old content, check whether the
query used the CDN. Correct the read configuration and trigger a rebuild through the deploy hook rather
than adding sleeps. Diagnose a write that fails with "permission" by sending the same body as a raw
`/data/mutate` POST through the token wrapper and reading the error text.

## Anti-patterns
- Skipping the dry run on a bulk change.
- Creating a new document type to solve a tagging problem. Use the existing resource and taxonomy model.
- Leaving placeholders in published bodies.
- Echoing a token, or writing one into the repository or the build.
