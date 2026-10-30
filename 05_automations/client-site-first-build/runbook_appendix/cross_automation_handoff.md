# Appendix: Cross-Automation Hand-off

> Voidwright edition. Before closing the build, register the site with the maintenance automations so they can find and operate on it.

## Where the registries live

Use your own copies of the registries shipped with this workbench:

- `05_automations/website-maintenance/runbook_appendix/client_registry.md` (every build)
- `05_automations/resource-hub-maintenance/runbook_appendix/client_registry.md` (hub modes)

If a registry file does not exist yet, create it with the corresponding columns below. A registry holds names and operational pointers only: never a token, an account ID, or anyone's email address. A Sanity project ID identifies a project, not an account or credential.

## Website-maintenance row (every build)

```
| Site | Platform | Repo | Branches | Worker | Previews | Data | Noindex posture | Mode | Built | Sign-off required |
|---|---|---|---|---|---|---|---|---|---|---|
| <domain> | cloudflare-workers | <your-github-user>/<repo> | main = production; preview + feature branches = Worker Preview | <worker> | public, or Access (Previews only) | <production D1 database> / <preview D1 database> | header (X-Robots-Tag on previews; production posture by build) | <mode> | <launch date> | true |
```

An invented kitchen-equipment maker's example row, for shape only:

```
| hearthspoke-kitchen.example | cloudflare-workers | <your-github-user>/hearthspoke-site | main = production; preview + feature branches = Worker Preview | hearthspoke-web | Access (Previews only) | D1 hearthspoke-inquiries / hearthspoke-inquiries-preview | header; production posture by build | website only | <launch date> | true |
```

Read the Worker name from the repository's Wrangler configuration rather than trusting a registry line.

## Resource-hub-maintenance row (hub modes)

```
| Site slug | Display name | Sanity project ID | Repo | Platform | Preview branch | Mode | Built | Sign-off required |
|---|---|---|---|---|---|---|---|---|
| <site slug> | <display name> | <Sanity project ID> | <your-github-user>/<repo> | cloudflare-workers | preview | <mode> | <launch date> | true |
```

## Site handoff notes (in the repo root)

1. What was built: mode, scope, and pages.
2. Where it lives: repository, Worker, D1 databases, Sanity project, and Access app if previews are protected.
3. What is gated: Access on previews only, if used; noindex by header on previews; production indexing posture applied by the build on `main`.
4. **The change path**: build the preview in a clean environment, run validators, push the preview, watch for its URL, obtain site-owner sign-off, run `git push origin preview:main`, watch the main build by its UUID, and verify the live site.
5. **Standing maintenance checks**: document each check, how to run it, its expected result, and what to do if it fails. Include enough detail to run the checks without relying on an external guide.
6. Accepted residual issues and open items, recorded as statuses to verify rather than assumed facts.
7. Reviewers and, if previews are protected, how they get through Access. Keep credentials out of the notes.
8. For ports, include a **redirect manifest** pointer, redirect counts, and the preview verification pass rate. Record **external outreach needs** for referring sites that link to URLs you never owned and for assets that could not be sourced.

## Handoff checkpoint

The website-maintenance row is written, the resource-hub-maintenance row is written for hub builds, and the repository's handoff notes are complete. A maintenance run starting without prior context must be able to find and operate on the site using the applicable registry and handoff notes alone.
