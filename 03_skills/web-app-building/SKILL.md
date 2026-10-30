---
name: web-app-building
description: Patterns for building and deploying web applications: routes, auth, database, state, UI, deployment and troubleshooting. Use when building or porting a web app.
---

# Web Application Patterns

Use this reference when designing or reviewing application boundaries, tenant access, data updates, browser state, and production operations.

## Request boundaries and access control

Treat every incoming request as untrusted, including requests from your own interface and scheduler.

For protected routes:

1. Authenticate the caller.
2. Verify the caller's organization context and membership.
3. Resolve external identity-provider identifiers to internal database identifiers.
4. Reject missing or failed mappings before accessing tenant data.
5. Authorize the requested operation on the server.
6. Validate incoming request bodies against an explicit schema, using a tool such as Zod.

Authentication establishes identity. Organization verification and authorization establish which data and actions that identity may access. Never accept a browser-supplied organization identifier as sufficient proof of access.

Keep privileged authorization configuration on the server. Hiding controls in the interface or checking browser-visible configuration does not protect a route.

Authenticate scheduled requests before executing their handlers by validating the configured request secret. A scheduler's endpoint can also receive requests from other callers.

Enforce rate limits on write endpoints. Review both ordinary application writes and privileged operations for excessive-request controls.

Related references:

- `03_skills/web-app-building/knowledge/api-routes-and-server.md`
- `03_skills/web-app-building/knowledge/auth-and-security.md`

## Database identity and tenant isolation

External identity-provider identifiers and internal database keys represent different identity systems. Resolve between them explicitly before assigning foreign keys or querying tenant-owned records.

Enforce tenant isolation at both layers:

- Application queries must filter by the verified internal tenant identifier.
- Database row-level security policies must enforce the same tenant boundary.

For a kitchen-equipment maker, a request for one organization's equipment records must remain scoped to that organization even if the caller supplies another record identifier. Check reads and writes for this behavior.

Match every upsert conflict target to an actual database uniqueness constraint. For a composite constraint, include every required key column. If a product reference is unique within an organization, its row identity includes both the organization key and the product reference.

Review schema definitions alongside query code. A conflict target that merely looks plausible does not establish correct row identity.

See `03_skills/web-app-building/knowledge/database-and-schema.md`.

## Secrets, errors, and audit records

Keep credentials and refresh tokens on the server. Inspect public configuration, serialized page data, and browser responses for accidental exposure.

Encrypt stored sensitive tokens using authenticated encryption:

- Generate a fresh initialization vector for every encryption.
- Encrypt sensitive values independently for each record.
- Verify the authentication tag during decryption and reject failed verification.

Use timing-safe comparison for secret authentication codes:

```js
crypto.timingSafeEqual(expected, received)
```

Both arguments must be buffers of equal length. Check lengths before calling the comparison and reject mismatches without exposing secret values.

Return generic errors to clients while retaining useful, redacted diagnostic context on the server. Review thrown errors as well as explicit logs. Raw upstream response bodies can contain credentials or personal data.

Audit security-relevant operations, including data changes, authentication events, and background operations. Record the actor, operation, affected resource, and outcome where appropriate. Do not record tokens, credentials, authentication codes, or unredacted request bodies.

See `03_skills/web-app-building/knowledge/security-hardening.md`.

## Server and browser responsibilities

Keep authentication, authorization, secrets, and metadata in server components or server handlers. Place browser hooks and interactive state behind a thin client boundary.

Use the client directive for modules that need browser interaction:

```js
'use client';
```

A client boundary is an execution boundary, not an authorization boundary. Server handlers must still enforce access control.

When adapting a desktop application to the web, reassess each responsibility. Privileged local operations need an appropriate server boundary rather than a direct move into browser code.

See `03_skills/web-app-building/knowledge/electron-to-web.md`.

### Personalized responses and caching

Prevent shared caches from reusing user-specific content across users. Review authenticated rendering, response headers, and any shared cache configuration together.

Where the framework requires dynamic rendering for authenticated content, use:

```js
export const dynamic = 'force-dynamic';
```

This setting does not replace a review of other cache layers.

## Interface state and component loading

Organize related state cohesively. When an API response provides several related values, update them together so the interface does not display an inconsistent combination.

Subscribe to specific store fields rather than destructuring the entire store. Narrow selectors keep each component tied to the state it actually needs.

Persist only deliberately chosen user preferences, such as display density or preferred units. Review persistence middleware and stored fields. Avoid persisting credentials, tenant data, or transient request state by default.

Create lazy component definitions outside render so their identity remains stable. Render them within `Suspense` and provide a useful loading fallback.

Related references:

- `03_skills/web-app-building/knowledge/state-management.md`
- `03_skills/web-app-building/knowledge/ui-components.md`

### Independent asynchronous operations

Use settled-result aggregation when operations are independent and partial success is useful:

```js
const outcomes = await Promise.allSettled(tasks);
```

Inspect every fulfilled and rejected result. Preserve successful outcomes and handle failures explicitly rather than silently dropping them.

Use a different coordination strategy when operations depend on each other or must succeed atomically. A rejection from `Promise.all` does not cancel outstanding work.

## Production review

Before deployment, verify the application boundaries in the deployed configuration:

- Protected routes authenticate callers, verify organization access, and enforce server-side authorization.
- Scheduled handlers reject requests with invalid secrets before doing work.
- Write endpoints validate request bodies and enforce rate limits.
- Tenant query filters and row-level security policies agree.
- Public configuration and browser responses contain no credentials or refresh tokens.
- Personalized responses cannot enter shared caches.
- Client errors and server diagnostics do not expose sensitive upstream content.
- Audit records cover security-relevant operations without storing secrets.

Limit content security policy permissions to domains required by actual application features. Review each allowed domain and remove permissions that have no current purpose.

See `03_skills/web-app-building/knowledge/build-and-deploy.md` for release guidance and `03_skills/web-app-building/knowledge/security-hardening.md` for security review.

## Maintaining reusable guidance

Reconcile verified lessons with existing documentation before adding new entries. Update or merge overlapping guidance so readers do not encounter competing instructions.

For each lesson, document:

- The failure condition.
- The corrective pattern.
- The verification that demonstrated the fix.

Keep identifying evidence in private records. Public guidance should contain reusable technical lessons without private paths, project identifiers, or run history.

See `03_skills/web-app-building/knowledge/ace-loop-patterns.md`.
