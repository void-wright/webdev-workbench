# Web Application Security Review

Review each feature from request entry through authorization, data access, storage, rendering, and operational handling. Record what the implementation enforces, what you verified, and any remaining gaps.

## Authentication and authorization

Require a verified caller on every protected API route. Return `401 Unauthorized` when authentication is missing or invalid.

Check permissions separately from authentication. Enforce administrative permissions on the server and return `403 Forbidden` when an authenticated caller lacks the required permission. Hiding controls in the interface does not enforce access restrictions.

For tenant-specific operations:

- Resolve tenant context from verified identity and membership.
- Treat tenant identifiers supplied by the caller as untrusted input.
- Scope application queries to the authorized tenant.
- Enforce tenant isolation through database row-level security policies as well.

Verify query scoping and database policies independently, including attempts to read or modify another tenant's records. For a kitchen-equipment maker, an administrator for one dealer account must not gain access to another dealer's orders by changing an identifier.

## Request validation

Validate request bodies against explicit schemas before application logic processes them. Define required fields, types, identifier formats, allowed values, and applicable size limits. Decide explicitly whether unknown fields should be rejected or discarded.

For a UUID field, a schema check can use:

```js
z.string().uuid()
```

A valid identifier format does not establish ownership or permission. Perform authorization checks after validation.

Return field-level errors that identify the invalid field and expected constraint without echoing credentials, personal information, or other sensitive submitted values. Inspect every body-handling endpoint, including administrative and integration routes.

## Secrets and stored credentials

Keep secrets in server-side configuration. Browser-exposed variables, generated client bundles, and client responses cannot hold confidential values.

Search public configuration declarations for potential credentials and investigate every match. Confirm that server-only configuration cannot enter browser code through imports or serialization.

When credentials must be recoverable for server-side use:

- Encrypt them with authenticated encryption.
- Generate a fresh random initialization vector for every encryption, including updates to existing records.
- Keep encryption keys separate from encrypted records.
- Decrypt only on the server.
- Verify that ciphertext, initialization vectors, and authentication tags survive encoding and decoding through the database client.

Confirm that modified ciphertext fails authentication rather than yielding usable plaintext.

Refresh credentials on the server. Encrypt replacement credentials before storing them, and expose only the minimum status information the interface needs. Review refresh success and failure responses to ensure neither refresh tokens nor replacement credentials reach the browser.

## Rendering and cache boundaries

Prevent authenticated content from crossing user or tenant boundaries through rendering or caching. Review these layers separately:

- **Rendering:** Can a page containing private data be generated or reused across callers?
- **Data caching:** Can a cached query result be reused without the correct identity and tenant scope?
- **Response caching:** Can a browser, proxy, or CDN store and share a private response?

Where supported by the framework, a route may explicitly require dynamic rendering:

```js
export const dynamic = 'force-dynamic';
```

This declaration alone does not prove that data caches or response caches are safe. Inspect their configuration and verify behavior with separate authenticated users and tenants.

## Browser content security policy

Allow only the origins required by enabled browser functionality. Review policy directives individually and connect each allowed origin to a necessary browser request or resource.

Server-side integrations do not need browser policy entries merely because the server contacts them. Remove unused allowances and check that required browser features still work under the resulting policy.

## Scheduled tasks and write limits

Authenticate scheduled-task endpoints with a configured, nonempty secret. Check that the configuration value exists before comparing request authorization. Missing configuration must fail closed; absent or mismatched request authorization must receive `401 Unauthorized`.

Keep the secret out of URLs, logs, and error responses. Verify both missing-configuration and mismatched-secret cases.

Apply rate limits to write operations at relevant user and tenant boundaries. Authentication does not prevent excessive requests from authorized callers. Check that one caller cannot bypass a tenant-wide limit by using multiple identities, and that enforcement works across the application's deployed instances.

Document any deferred rate limiting with its scope, rationale, and mitigating controls.

## Logging and audit records

Review every application logging call, including error handling and advisory paths. A useful starting search is:

```sh
rg -n 'console\.' --glob '!node_modules/**'
```

Also inspect logging frameworks and wrappers that this search does not find. Raw errors, request headers, and external response bodies can contain credentials or personal information. Prefer allowlisted diagnostic fields and sanitized error summaries.

Maintain audit records for privileged changes and sensitive operational lifecycles. Capture enough context to establish who acted, which tenant or resource was affected, what operation occurred, and whether it succeeded. Do not include secret values.

Verify audit coverage for relevant success and failure paths. Document omissions with their rationale and mitigating controls.

## Evidence and review completion

Read all files involved in a feature, including shared authorization helpers, data access code, background tasks, rendering configuration, and migrations. Route handlers alone are insufficient evidence.

Locate schema definitions as a starting point:

```sh
rg -n -i 'CREATE TABLE'
```

Compare those definitions and migrations with the deployed database, including active row-level security policies. A repository declaration does not prove that a deployment applies it.

For each finding, record:

- The expected security behavior.
- File and line references supporting the finding.
- Relevant deployed configuration or database evidence.
- The verification performed and its result.
- Any unresolved gap, rationale, and mitigating controls.

Distinguish verified behavior from assumptions and untested claims. Keep credentials and personal information out of the review evidence itself.
