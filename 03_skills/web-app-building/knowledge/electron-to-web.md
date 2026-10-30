# Moving Desktop Responsibilities to the Web

A desktop application can combine interface code, privileged operations, and local persistence within one installation. A browser application needs explicit boundaries between presentation, authenticated server services, and shared storage.

Start by assigning each responsibility to its new owner.

| Responsibility | Owner |
|---|---|
| Rendering, interaction, and non-sensitive interface preferences | Browser |
| Authorization, service credentials, token refresh, and privileged operations | Server |
| Shared records, access policies, and background-operation state | Database |
| Recurring work that must run without an open browser | Authenticated server scheduler |

Replace desktop process messaging with browser requests to server handlers. Treat each request as crossing a trust boundary.

## Protect Server Operations and Shared Data

Every server endpoint must authenticate the caller and authorize the requested operation. A signed-in user does not automatically have permission to read or change every record.

For each route:

- Establish the caller’s identity through a validated session or service credential.
- Check permission for the specific action and resource.
- Derive or validate the tenant or resource scope on the server.
- Apply that scope to database reads and writes.

Enforce scope in database access policies as well as server handlers. Scoped tables should carry the appropriate foreign key, and policies should restrict access through that relationship. A scope identifier supplied by the browser is input to validate, not proof of permission.

For a neighbourhood climbing gym, permission to view one member’s booking should not imply permission to view every member’s bookings. Check the requested booking against the caller’s access rights.

## Keep Credentials on the Server

Service credentials, provider tokens, and token refresh operations belong on the server. Service clients should obtain credentials through a server-side token manager rather than accepting provider tokens from browser storage.

Encrypt stored tokens and keep the encryption keys separate from the token database. This separation limits exposure if the database contents are compromised.

Use a server-handled OAuth authorization-code flow:

1. Bind the authorization request to the initiating session using state.
2. Use PKCE where the provider supports it.
3. Validate callback state before accepting the authorization response.
4. Exchange the code on the server.
5. Store tokens securely and perform subsequent refreshes on the server.

When an SDK requires a token adapter, implement its required interface. Check method signatures, return values, and refresh behavior against the SDK contract. A type assertion only suppresses a compiler complaint; it does not supply missing behavior.

Use `localStorage` only for non-sensitive preferences, such as a selected view or collapsed navigation section. Do not use it for credentials or confidential configuration.

## Preserve Data Meaning During Migration

Review database types together with the application code that reads and serializes them. A value that fits in the destination database may still lose precision when converted to a JavaScript number.

| SQL construct | Use and migration check |
|---|---|
| `BIGINT` | Large integers. Check source ranges and preserve values beyond JavaScript’s safe integer range through an explicit serialization strategy, such as decimal strings. |
| `DATE` | Calendar dates without a time of day. Avoid converting them into instants that can shift dates across time zones. |
| `TIMESTAMPTZ` | Instants in time. Define how the application accepts, serializes, and displays time zones. |
| `DEFAULT NOW()` | A database-generated timestamp default. Confirm that its timing semantics match the intended event. It does not automatically update a modification timestamp on later writes. |

Avoid storing all dates as undifferentiated text. Distinguish calendar dates from timestamps and make that distinction explicit at API boundaries.

### Make Record Identity Scope-Aware

If an identifier is unique only within a tenant or resource scope, include that scope in record identity.

For example, a composite uniqueness constraint on `(scope_id, external_id)` allows different scopes to contain the same external identifier without treating those records as one entity. Use the same identity consistently in lookups, write conditions, and conflict handling.

### Review Upserts and Replacement Behavior

Back every upsert conflict target with a matching uniqueness constraint. If identity includes scope, the conflict target must include it too.

Compare source and destination write semantics explicitly. A source replacement operation may delete and recreate a row, while a destination upsert may update selected columns. Review the effects on:

- Fields omitted from the new payload.
- Defaults and generated values.
- Foreign-key relationships.
- Triggers and audit fields.

Await remote database writes and handle failures explicitly. Do not report a save as complete before persistence succeeds. If the interface uses optimistic updates, provide a defined recovery path when the write fails.

## Move Recurring Work Out of the Browser

Work that must continue independently of an open browser belongs in an authenticated server scheduler. Configure the schedule and verify that the invoked handler validates the scheduler’s identity and permissions.

Persist background-operation lifecycle state in durable storage. Record enough information to distinguish queued, running, completed, and failed operations, along with relevant timestamps, progress, and safe error details.

This lets the interface recover status after a reload or reconnect. An in-memory flag in a browser tab cannot serve as the authoritative record of server work.

## Organize Browser State Around Lifecycle

Choose state-store boundaries according to what initializes, changes, and resets together. State that shares a lifecycle may belong in one store; independently managed state may need separate boundaries.

Make resets explicit when the user signs out or changes access scope. Previously loaded data must not remain visible under a different session or scope.

In frameworks that use the directive, `'use client'` marks a client component boundary. It does not provide authorization or make privileged operations safe to run in the browser.

### Load Details When They Become Relevant

Fetch optional detail data when the interface needs it, such as when a detail panel opens or a record becomes selected. Consult the cache before requesting data, and define when cached entries need revalidation.

Include both access scope and record identity in cache keys. A key containing only a record identifier can collide across scopes. If results depend on the user’s permissions within a scope, partition or invalidate the cache accordingly.

### Cancel Requests and Polling

Create an abort controller for requests tied to a selection or component lifecycle:

```js
const controller = new AbortController();

const response = await fetch(url, {
  signal: controller.signal,
});
```

Call `controller.abort()` during cleanup when the selection changes, the content closes, or the component unmounts. Treat expected cancellation separately from a request failure. Also prevent obsolete responses from updating current state if cancellation arrives too late.

Clear polling intervals when the consuming component unmounts or no longer needs the results. Stop any in-flight request associated with that polling lifecycle as well.

## Preserve HTTP Behavior When Changing Libraries

Replace an HTTP library with `fetch` only after checking that the replacement covers the application’s requirements.

Compare authentication handling, request and response processing, timeouts, cancellation, retries, error handling, and any required upload or download progress behavior. Account for behavior previously supplied by interceptors or shared defaults.

With `fetch`, check HTTP status explicitly, such as through `response.ok`: an HTTP error response does not by itself reject the promise. Keep required behavior visible and tested rather than assuming a smaller dependency provides equivalent semantics.

## Verify the Boundaries

Before considering the migration complete, verify that:

- Every endpoint checks identity and permission, including scheduled handlers.
- Server queries and database policies enforce resource scope.
- Credentials and refresh operations remain server-side, with encrypted token storage and separate keys.
- OAuth callbacks validate state and use PKCE where supported.
- Database types, serialization, scoped identities, and upsert constraints preserve the intended data.
- Failed remote writes produce an explicit recovery path.
- Background operations expose durable progress and outcomes.
- Browser caches respect access scope, and requests and polling stop when their consumers disappear.
- SDK adapters and HTTP replacements satisfy the behavior their callers require.
