# Keeping each account separate: Sanity and Cloudflare on your own credentials

> Runbook appendix for `resource-hub-maintenance`, Voidwright edition.
> Read it before the first Sanity or Cloudflare call on a new hub, and whenever one machine holds more than one
> account, such as separate accounts for a shop website and its resource library.
> Review the account and credential records for the target site before proceeding.

---

## Part A. Every account is reached by its own credentials and tools

**When this applies:** always. It matters most when the same machine holds credentials for more than one
account, such as a ceramic studio's storefront and its independently managed guide library.

### A1. Why not a shared tool with a flag

- A CLI may default to an existing login. Using it for another account can silently target the wrong organisation.
- **Separation that depends on remembering a flag is not separation.** Use a dedicated tool configuration with an
  isolated credential source and an explicit account check.
- Keep the patterns: a polymorphic content schema, atomic `/data/mutate` seeding,
  `projectId` + `dataset` pinned in the site's Sanity client, and a staging filter if one is needed.

### A2. The ambient-credential hazard (check it before any work)

A login shell that loads a shared environment file exports vendor keys for hosting, content, mail and analytics into
**every** shell. A plain `wrangler` or `sanity` call may then reach whichever account those keys belong to.
Count matching environment variable names without printing their values:

```bash
printenv | rg -c '^(CLOUDFLARE|CF_|SANITY|RESEND|TURNSTILE|GA4|VERCEL)' || true
```

No matches is a good starting point. Keep the habit anyway: a future tool install can add an environment file.
If matching variables exist, use `06_web_tools/wrangler-safe` for every Wrangler call. It removes other
`CLOUDFLARE_*` and `CF_*` variables before loading the intended credentials. Never run a bare `npx wrangler`
while conflicting credentials are present.

### A3. The separation recipe

1. **One private key file per account:** use the credential-file setup documented in `06_web_tools/README.md`.
   Set the containing directory to mode 700 and the file to mode 600. Use plain `NAME=value` lines.
   The package's tools **parse** the file rather than sourcing it, so its contents are not executed as shell code.
   Ensure each invocation selects the intended account's file.
2. **Keys go in by hand and are never echoed:** open the file in an editor and paste the value. Never type a key on
   a command line, where it can enter shell history. Never print it or read it back through an agent to check it.
   Verify it with a read-only request.
3. **Run tools with only your account's values:** run these package commands from the package root.
   - Wrangler: `bash 06_web_tools/wrangler-safe <args>`. If using `npx wrangler login`, first isolate the environment
     and confirm which account the stored OAuth login reaches.
   - Cloudflare API: `bash 06_web_tools/cf-api GET '/accounts/{account}/workers/scripts'`.
   - Sanity API writes: `bash 06_web_tools/bearer-curl SANITY_API_TOKEN <curl args>`.
     The token travels to curl through standard input, so it never appears in the process list.
   - Sanity CLI: `npx sanity login`. The CLI keeps its own login; verify its target independently of the API token.
4. **Pin the account twice:** set `account_id` in the site's Wrangler configuration AND use a token scoped to that
   account only. `06_web_tools/wrangler-safe` refuses to run when the repository's pin and the key file disagree.
   Enforce the account boundary before making requests instead of relying on memory.
5. **Keep alternate authentication paths out of this workflow:** browser OAuth connectors authenticate outside the
   credential wrappers. Do not use one for a second account unless it provides equivalent account isolation and
   target verification.
6. **Verify read-only, live, before any write:** replace the project placeholder with the intended Sanity project ID.
   ```bash
   # Token check: expect 200.
   bash 06_web_tools/bearer-curl SANITY_API_TOKEN -s -o /dev/null -w '%{http_code}\n' \
     "https://<your-sanity-project-id>.api.sanity.io/v2024-01-01/users/me"

   # A public-read dataset answers a query without a token.
   curl -sG \
     "https://<your-sanity-project-id>.api.sanity.io/v2024-01-01/data/query/production" \
     --data-urlencode 'query=count(*)'
   ```
   Confirm the authenticated identity and intended project and dataset, not just a successful status code.
   With a public-read dataset, **no read token needs to live in the site build**. Keep the write token in the private
   credential store.
7. **Record each decision when it is made:** update the site's account record and implementation notes with the
   chosen account, project, dataset and credential source, but no secret values. A decision that lives only in a
   temporary plan can be lost before the next maintenance task.

### A4. Credential hygiene

- Anything that needs a secret in CI, such as a Sanity webhook secret or a deploy hook URL, is treated as a secret:
  scoped, stored only where it is used, never committed and never pasted into chat. Record its existence,
  not its value, and its rotation date using
  `05_automations/resource-hub-maintenance/runbook_appendix/client_registry.md`.
- A Cloudflare token's permission list is not proof a feature works. Probe the feature itself with a read call on
  the exact resource and record any error codes.

---

## Part B. The external-writer track

**Not available here.** Use the package's design agents and the Inner Council instead:
`05_automations/agents/design-generator.md`, `05_automations/agents/design-reflector.md`,
`05_automations/agents/design-curator.md` and `04_reasoning/commands/inner-council.md`.

For any delegated writing, put source inputs in a read-only folder, compare file manifests before and after the
run, and preserve every required review and validation check. These checks make delegated work reviewable;
the writer's identity does not establish its quality.
