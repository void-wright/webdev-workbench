# Secure API Handlers, Integrations, and Background Work

## Establish identity and authorization

Before accessing tenant data:

1. Require an authenticated identity.
2. Resolve the trusted internal tenant identifier through server-controlled membership records.
3. Reject missing tenant context, failed resolution, or inactive membership.
4. Check permission for the requested action.
5. Scope every data query to the resolved internal tenant identifier.

A tenant identifier supplied in a body, URL, or header is a selection request, not proof of access. Authentication establishes who the caller is; authorization determines which actions they may perform.

For a garden-supply shop, permission to view stock does not automatically grant permission to change stock or run an inventory synchronization.

Apply these checks to reads, writes, and background operations. Privileged database clients may bypass row-level security, so their queries need explicit tenant restrictions and action permission checks.

Keep server database clients independent of persistent browser sessions. Configure their authentication options as:

```ts
{
  auth: {
    persistSession: false,
    autoRefreshToken: false
  }
}
```

Keep privileged credentials on the server.

## Validate inputs before performing operations

Define an explicit schema for each request body, including allowed operation types, required fields, value ranges, and collection limits. Handle malformed JSON through the same controlled validation path as invalid values:

```ts
const input = await req.json().catch(() => undefined);
const result = schema.safeParse(input);
```

If schema parsing fails, return a controlled client error, such as HTTP 400. Do not perform writes, invoke external services, or enqueue work. After successful validation, use the parsed data rather than the original input.

Return useful validation messages without echoing sensitive payloads.

## Bound resource consumption

Apply limits at the scope appropriate to the operation. Check both user and tenant budgets so that several users cannot collectively exhaust a tenant’s allowance.

Bound more than request frequency:

- Batch size and concurrent operations.
- External request duration and retry count.
- Total execution time and work performed per request.
- Response size and records processed.

Reject excess work predictably. For request rate limits, use HTTP 429 and provide retry guidance where available.

If rate limiting is deferred, document the affected endpoint and its concrete mitigation, such as restricted administrative access. Restricted access still needs resource budgets for expensive operations.

## Share scheduled and manual execution

Put the underlying operation in a shared server function. Let each entry point enforce its own authentication and validation before calling it.

For a scheduled endpoint:

- Require the scheduler secret to be configured. Fail closed when it is missing.
- Validate the request’s authorization header against the configured secret.
- Use the HTTP method expected by the scheduler.
- Give scheduled work an explicit authorized scope.

For Vercel cron, use a GET handler and validate the bearer authorization header using the configured cron secret. Never treat a missing secret as permission to run.

For an authorized manual trigger, use a POST handler that validates its body, resolves tenant context, checks administrative permissions, and calls the same underlying function.

Check any `maxDuration` export against the hosting platform and plan’s supported execution limits. A route setting cannot grant more runtime than the host allows. Move work that cannot reliably finish within those limits to a suitable background worker.

## Preserve independent batch outcomes

Validate operation types, then deduplicate them before creating tasks:

```ts
const unique = [...new Set(requestedTypes)];
```

Run independent work with bounded concurrency. Collect every outcome so that one rejection does not discard successful results:

```ts
const results = await Promise.allSettled(tasks);
```

Keep tasks in the same order as `unique`, and associate each settled result with its operation type. Return a safe success or failure result for every requested distinct operation.

`Promise.allSettled` collects outcomes; it does not limit concurrency. Apply concurrency limits when starting tasks. Deduplication within a request also does not prevent duplicate execution across retries or overlapping invocations. Use an idempotency mechanism where repeated side effects would be harmful.

## Track background status explicitly

Record a waiting state before execution, a running state when work starts, and a terminal outcome when it finishes. Terminal outcomes should distinguish success, failure, cancellation, or skipped work where those distinctions matter.

Track individual operation status as well as overall job status. An orchestration function can finish successfully while some operations fail.

Run dependent computations after upstream work settles, then inspect the inputs they actually received. Decide explicitly whether a computation:

- Requires all upstream inputs and must fail or be skipped if any are missing.
- Can produce a partial result with missing inputs clearly identified.
- Can use a documented fallback.

Do not silently turn a failed input into an empty or zero value. Preserve enough status information to diagnose failures and safely retry appropriate work.

## Isolate external-service calls

Keep each external integration in its own module. Each module should report its own failure through a defined result or error contract, allowing orchestration to preserve other outcomes.

Use a bounded timeout for every external request:

```ts
const controller = new AbortController();
```

Pass the controller’s signal to the request, schedule an abort at the timeout, and clear the timer in a `finally` block. Check HTTP response status explicitly because an unsuccessful HTTP response does not necessarily reject the request promise.

Bound retries and keep them within the overall work budget. Retry only when the operation is safe to repeat or protected by idempotency.

## Manage external credentials securely

Obtain a valid access token before calling an external API:

1. Load credentials for the authorized tenant and integration.
2. Decrypt them only on the server.
3. Inspect token expiry.
4. Refresh proactively when expiration is near.
5. Persist refreshed credentials encrypted, including a rotated refresh token if supplied.
6. Use the valid access token for the request.

Coordinate concurrent refresh attempts so they do not overwrite newer credentials or reuse an invalidated refresh token. Treat failure to persist refreshed credentials as an integration failure that needs handling.

For browser-initiated OAuth callbacks, validate the callback and complete the token exchange before redirecting the browser to an appropriate application page. Return a redirect for failure flows too, using a safe status indicator. Keep tokens and diagnostic details out of redirect URLs, and restrict redirect destinations to trusted locations.

## Handle errors without exposing internals

Caught values are not guaranteed to be `Error` objects. Narrow them before inspecting their properties:

```ts
catch (err: unknown) {
  const message = err instanceof Error ? err.message : 'Unknown error';
}
```

Treat the extracted message as potentially sensitive. Redact it before logging if it may contain credentials, external response bodies, or request data.

Keep diagnostic details in server logs with safe context, such as an operation type and correlation identifier. Exclude tokens, secrets, decrypted credentials, and sensitive payloads.

Return controlled client errors for validation and authorization failures. For unexpected failures, return a generic message and a correlation identifier rather than stack traces, database errors, or raw provider responses.

## Review before release

Verify that malformed JSON produces a controlled client error, unauthorized tenant access is rejected, and privileged queries remain tenant-scoped. Check that scheduled requests fail when their secret is missing or incorrect.

Exercise partial batch failure, external timeouts, expired credentials, and incomplete upstream inputs. Confirm that results remain associated with their operations, statuses reach accurate terminal outcomes, OAuth callbacks redirect, and route runtime settings fit the hosting limits.
