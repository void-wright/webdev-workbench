# Appendix: Asset Placement (site ports only)

> Runs ONLY when `IS_SITE_PORT == true`. Requires a completed redirect plan with a `hosting_layer` decision for every file destination.

## Purpose

For every inbound link whose target is a file (PDF, image, or other binary), make sure the file exists on the new site at a stable URL **before** the redirect goes live. A redirect to a missing file turns one 404 into another and loses the value of the inbound link. Files served by the old CMS may become unavailable at DNS cutover unless they have been migrated.

## Two hosting layers

| Layer | When | How |
|---|---|---|
| `site_public` (default) | Website-only builds; brand assets; anything that should be same-origin | Copy into the repository's public asset directory and serve through the Worker's static assets at a stable URL on the site's domain. Verify the current per-file size limit before placement; larger files need another hosting layer. |
| `sanity_cdn` (hub modes) | PDFs and images that belong to hub content, or need on-demand image transforms | Upload through the Sanity client or Studio using your own project token (`SANITY_API_TOKEN`), loaded securely from your key file; use the returned `cdn.sanity.io` URL as the destination. |

A third option, an R2 bucket on the same Cloudflare account behind a custom domain, suits very large files or large collections. Make this an explicit hosting decision with the person responsible for the site, never a default.

## Where the file comes from (in order)

1. **Wayback's archived copy** of the exact URL (`https://web.archive.org/web/<timestamp>id_/<url>`; the `id_` suffix returns the raw file).
2. **The live old site**, while it still answers.
3. **The person responsible for the site's content**, given an itemized request identifying each file neither source has.

Download each file into a staging directory in the workspace, record its SHA-256 hash, then place it.

## Verification (HARD)

- Send a HEAD request to the new destination: expect 200 and the correct content type. On a protected preview, send the Access service-token headers from a file with permissions set to `600`. Load that file through the HTTP tool's header-file option; never put token values directly on the command line.
- Write an asset-placement manifest containing the original URL, source, SHA-256 hash, hosting layer, new URL, and timestamp. Archive it with the rest of the migration records.

## Halts

- Any asset destination answers anything but 200: halt; fix the destination or ask the person responsible for the site to resolve it.
- A file that cannot be sourced must either be supplied by the person responsible for the content or have its original URL return **410 Gone**, with that decision explicitly agreed. **Never blind-redirect to a file that does not exist.**
