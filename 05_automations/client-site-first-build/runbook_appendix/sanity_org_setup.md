# Appendix: Sanity Project Setup (hub modes only)

> Generic edition. Uses your own Sanity organization and a token stored in a local key file outside the repository.

## Steps

1. **Organization** (site owner, dashboard): create or confirm your Sanity organization at sanity.io/manage. Check current plan limits before relying on document, bandwidth or API allowances. Use a separate project for each site to keep content, permissions and usage isolated.
2. **Project + dataset**: run `npx sanity@latest init` (or use the dashboard) inside your organization; create the dataset `production` with private visibility. Record the project ID in the repository's public configuration; it is not a secret.
3. **Token**: create a token with the least privileges needed for the task, such as Editor for seeding or Viewer for reads. Set `KEY_FILE` to your local key file's location, store the token there as `SANITY_API_TOKEN=...`, then run `chmod 600 "$KEY_FILE"`. Never print the token, commit it or paste it into a chat.
4. **Wiring**: the site reads through `@sanity/client` with the project ID and dataset. Keep the token on the server. For manual API requests, use `06_web_tools/bearer-curl` as described in `06_web_tools/README.md`; it sends the token as a header without putting its value on the command line. Keep each site's credentials separate.
5. **Schema**: use only the four polymorphic document types (resource, taxonomy, collection, series); deploy the Studio schema. Respect API rate limits when seeding. Batch mutations in transactions with stable `_id`s and idempotent mutation operations so reruns do not create duplicates.
6. **Seed** only content supplied or approved by the site owner; otherwise defer seeding until that content is available.

## Checkpoint R2

Studio loads; the four types exist; a GROQ test query returns the seeded documents, or an empty result if seeding was deferred; no authentication errors occur; the key file has mode 600 and remains outside every repository; `gitleaks` reports no exposed secrets.
