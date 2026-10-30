# Authentication and Secure Request Handling

Treat browser input, identity-provider responses, and stored credentials as data that must cross explicit trust boundaries. Authenticate on the server, authorize access to each resource, and validate data before using it.

## Validate inputs at the boundary

Apply explicit schemas to request bodies, route parameters, and query parameters before application logic uses them. Define allowed types, lengths, ranges, formats, and values. Decide whether to reject or discard unknown fields.

For an identifier whose database format is a UUID, a schema field can use:

```ts
z.string().uuid()
```

Do not apply this constraint to external identity-provider identifiers unless their documented format is also a UUID.

Return HTTP 400 for invalid input, with field-level details that explain how to correct the request. Report field names and safe validation messages without echoing passwords, tokens, or other sensitive values.

Static types do not validate external data. After verifying a cookie signature and decoding its payload, apply a runtime schema before reading its fields.

## Authorize every server entry point

Authentication establishes who is making a request. Authorization establishes what that identity may do.

Enforce both independently in API routes, Server Actions, and other server entry points. Layout checks, hidden buttons, and client redirects cannot protect direct requests.

For each scoped operation:

1. Authenticate the request.
2. Resolve the external identity-provider identifier to the corresponding internal database identifier.
3. Verify authorized membership in the requested scope.
4. Check access to the specific resource and operation.
5. Query or mutate data within that authorized scope.

Reject requests when identity mapping or authorized scope is missing. Never treat a client-supplied organization or resource identifier as proof of access.

For a ceramic studio, being signed in might allow a member to view their own workshop bookings. Changing another member's booking requires a separate permission check.

Keep authorization rules and privileged credentials on the server. Browser code may display available actions, but server code must make the authoritative decision.

### Add database protection

Combine application authorization with database row-level security where supported.

Review policies for unrestricted reads or writes to sensitive tables. Test policies using the restricted database roles that application requests actually use.

Privileged database credentials may bypass row-level security. Every route using those credentials must explicitly enforce membership, resource access, and query scope in application code.

## Separate server authentication from client interaction

In Next.js, use Server Components to authenticate requests and redirect when necessary. Place interactive behavior in client components, with the directive at the beginning of the client module:

```tsx
'use client';
```

Keep provider wrappers small and place them only where their context is needed. Do not move privileged configuration into client code to make it available through a wrapper.

When the installed Next.js rendering configuration requires and supports explicit dynamic rendering for request-dependent authentication, use:

```ts
export const dynamic = 'force-dynamic';
```

Check the project's rendering configuration before adding this setting. Rendering choices do not replace authorization inside routes or Server Actions.

## Build OAuth around a protected transaction

### Request minimal permissions

Request only the OAuth scopes needed by the integration. Document the feature that requires each scope. Include identity scopes only when the application needs identity information.

Prefer an authorization-code flow with PKCE when the provider supports it. Generate a standards-compliant verifier and derive its challenge using SHA-256 through the S256 method.

### Bind the callback to its initiating request

Generate unpredictable random state for each authorization attempt. Store short-lived correlation data in a signed cookie configured with:

- `HttpOnly`.
- A short expiry.
- `Secure` in production.
- A `SameSite` setting appropriate to the provider's callback method.

A signature protects integrity, not confidentiality. Keep cookie contents minimal and use protected server-side transaction storage for sensitive transaction data where appropriate.

On callback, verify the cookie signature, decode the payload, and validate its structure at runtime. Require an unexpired transaction and matching state before accepting the result.

Exchange the authorization code on the server, supplying the original PKCE verifier when applicable. Keep client secrets and token responses within the server boundary.

Clear temporary cookies after processing success or failure. Reject missing, expired, malformed, or mismatched correlation data.

For browser-initiated failures, redirect to a known application destination with a generic failure indicator. Do not expose provider response bodies or accept an arbitrary redirect destination from callback input.

## Protect stored credentials

### Use authenticated encryption

Encrypt stored access tokens, refresh tokens, and other credentials with authenticated encryption. Keep the encryption key exclusively on the server and separate from the encrypted records.

For AES-256-GCM:

- Validate that the decoded key is exactly 32 bytes.
- Generate a fresh, cryptographically random 12-byte IV for each encryption.
- Never reuse an IV with the same key.
- Retain the authentication tag.
- Reject malformed payloads and failed authentication without returning plaintext.

Generate the IV with:

```ts
crypto.randomBytes(12)
```

### Define the storage format

Use a documented text representation when storing encrypted payloads through JSON-based database clients. One format is base64 encoding of the IV, authentication tag, and ciphertext:

```ts
Buffer.concat([iv, authTag, ciphertext]).toString('base64')
```

Define the boundaries explicitly, such as a 12-byte IV followed by a 16-byte authentication tag and then ciphertext. Validate the encoded input and decoded length before splitting it. Configure encryption and decryption to use the same tag length.

If supporting multiple formats or encryption keys, store explicit version and key identifiers alongside the payload. Keep the actual keys out of the record.

### Compare authentication digests safely

For authentication digest comparisons, use Buffer values and constant-time comparison after checking lengths:

```ts
expected.length === actual.length && crypto.timingSafeEqual(expected, actual)
```

Validate encodings and expected digest sizes before this comparison. Do not substitute ordinary string equality for secret digest verification.

## Refresh credentials before provider calls

Check token expiry before making a provider request. Use a small expiry buffer so a token is unlikely to expire during the request.

When refreshing credentials:

1. Decrypt the stored refresh token only on the server.
2. Request replacement credentials.
3. Validate the response.
4. Encrypt and persist the new access token and expiry.
5. Persist a replacement refresh token when one is supplied.

If the provider omits a replacement refresh token, preserve the existing one when that matches the provider's contract. Coordinate concurrent refresh attempts so an older result cannot overwrite newly rotated credentials.

Do not report refresh success until required replacement credentials have been saved securely.

## Share security logic and sanitize errors

Centralize repeated authentication, identity mapping, authorization, cookie verification, and credential-handling logic. Each server entry point must still invoke the required checks. Shared helpers should reject invalid or missing security context by default.

Keep diagnostics useful without exposing secrets. Log safe fields such as a request identifier, operation name, sanitized error category, and provider status code.

Exclude tokens, cookies, authorization headers, encryption keys, raw provider bodies, and sensitive submitted values from logs. Keep stack traces and internal paths out of client responses.

Return generic client-facing errors for internal failures. Preserve safe field-level detail for input validation failures.

## Derive CSP from browser requirements

Build Content Security Policy from the destinations and capabilities actually used by browser code. Server-to-server token exchanges and provider requests do not require browser CSP allowances.

Check the installed integrations and enabled features to identify required script, connection, frame, image, and style sources. Allow only the necessary destinations.

Prefer supported nonce-based policies, with a fresh nonce for each response and matching nonces on authorized scripts. Keep exceptions narrow and documented. Avoid `unsafe-eval` unless a verified integration requirement makes it necessary.

Test sign-in, callback completion, session refresh, and protected pages under the deployed policy. Confirm that required browser behavior works without broadening the policy beyond demonstrated needs.
