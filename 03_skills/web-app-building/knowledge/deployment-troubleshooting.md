# Troubleshooting Deployed Web Applications

Diagnose failures at the boundary where they occur: configuration, authorization, API transport, credential storage, or scheduling. A successful step at one boundary does not prove that the next one works.

## Check deployment configuration first

When several applications share an environment, use unambiguous configuration names so each application selects its intended provider registration and encryption key.

Separate configuration by when and where it is used:

- Keep runtime secrets on the server, outside client-visible code and bundles.
- Declare build-affecting configuration in the build cache’s environment inputs so changes invalidate affected outputs.
- Review the relevant Turbo environment configuration when a deployment appears to retain old build-time values.

Confirm that the deployed application receives the intended values without printing secrets.

## Separate sign-in from resource access

Successful sign-in establishes identity. It does not prove that the identity has the role, scope, or access grant required for a resource.

Before reporting that an integration works:

1. Confirm which account and resource context are selected.
2. Verify the required roles, grants, and permissions.
3. Perform a minimal authorized request against the intended resource.

For a seed library, signing in successfully does not necessarily grant access to its shared seed inventory.

Request only the OAuth scopes needed by the integration. Treat optional identity enrichment, such as fetching a display name or profile image, as best-effort. Its failure should not invalidate an otherwise successful connection.

## Configure OAuth for the deployed application

### Match the client type and callback

Choose an OAuth client type that matches the deployment model. Installed applications and hosted web applications have different redirect configuration requirements.

For a hosted Google OAuth integration, confirm that the registration is a **web application** client and that its authorized callback URI matches the intended deployed callback.

Return users to the interface that initiated authorization. Show the outcome beside the initiating controls so users can tell whether the connection succeeded, failed, or needs further action. If the return destination is carried through the flow, validate it before redirecting.

### Distinguish login from consent

Providers may reuse an existing session or grant. Requesting a new login is different from requesting renewed consent.

Use only parameters supported by the provider, and check whether they require additional identity configuration:

```js
authUrl.searchParams.set('prompt', 'login'); // Only where documented by the provider.
```

Do not assume this parameter forces renewed consent. Verify the provider’s documented behavior for the outcome you need.

## Diagnose API failures without exposing credentials

### Check the request contract

Use only documented request headers and API versions. For authorization failures, compare the request with the endpoint’s requirements and check:

- The selected resource and account context.
- Granted scopes and resource permissions.
- The token’s intended audience.
- The required headers and supported API version.

Do not attribute a failure to headers before checking grants, permissions, and token audience.

### Keep errors safe

Provider response bodies can contain tokens or other sensitive values. Do not copy them into thrown errors or logs.

Use a bounded error message:

```js
if (!response.ok) {
  throw new Error(`Request failed (${response.status})`);
}
```

Keep diagnostic logging on the server and redact sensitive details. Prefer safe fields such as status, operation name, and a provider request identifier when available. Exclude authorization headers, credentials, and unfiltered response bodies.

### Isolate client-library transport problems

Authentication plugins and transport dependencies can behave differently in serverless runtimes. Identify whether the failure occurs while obtaining credentials, constructing the request, sending it, or interpreting the response.

Consider a documented REST alternative only after isolating the client-library failure. Before adopting it, validate against the provider’s REST documentation:

- Request fields and response mappings.
- Authentication requirements.
- Pagination behavior.
- Error handling.
- Successful responses from a minimal request.

A successful HTTP connection alone does not establish that the replacement handles the integration correctly.

## Manage token expiry and rotation

Check token expiry before authenticated API calls. Refresh with a safety margin so a token does not expire during a request.

Follow the provider’s documented refresh endpoint, client authentication requirements, and request encoding. Where specified, the refresh request includes:

```text
grant_type=refresh_token
```

After a successful refresh, encrypt and persist the current credentials, including any replacement refresh token. If the provider omits a replacement refresh token, preserve the existing one unless its documented behavior requires otherwise.

Verify persistence by loading the updated credentials through the normal storage path and using them for a minimal authorized request. An in-memory refresh can appear successful while leaving subsequent requests with stale stored credentials.

## Make encrypted storage representations explicit

### Define the encoding contract

Document what crosses each application and database boundary: plaintext, ciphertext bytes, or encoded text.

For base64 text storage, use one consistent sequence:

```text
plaintext
  → encrypt
ciphertext bytes
  → base64 encode
base64 text
  → store and retrieve unchanged
base64 text
  → base64 decode
ciphertext bytes
  → decrypt
plaintext
```

Include any required nonce, authentication tag, and format metadata in the documented storage format. Base64 is an encoding step, not encryption.

Verify the full round trip with a known, non-sensitive test record. Check that database adapters do not silently transform the value and that encoding or decoding happens exactly once.

### Migrate according to the stored representation

Inspect the actual representation of existing values before converting them. A conversion intended for raw ciphertext can corrupt values that are already encoded.

Make migration behavior conditional on a verified format or explicit format metadata. Do not rely solely on whether a value looks like base64.

Test decryption before and after migration, and retain a recoverable copy until verification succeeds. A database write succeeding is not proof that the migrated ciphertext is usable.

If stored credentials cannot be recovered, obtain fresh credentials through authorization.

## Diagnose scheduled execution

### Match the hosting platform’s request contract

A scheduled endpoint must accept the request method used by the platform and reject unauthorized invocations.

For Vercel cron endpoints, handle `GET` requests and validate bearer authorization against the configured server-side secret before performing work.

### Verify registration before debugging the handler

When an execution appears to be missing:

1. Confirm that scheduler configuration is under the deployed application’s root.
2. Check that the deployment containing the configuration is active.
3. Inspect the hosting dashboard to confirm schedule registration.
4. Review the schedule expression, its timezone semantics, and the expected invocation time.
5. Inspect deployment and invocation logs.

Once registration and timing are confirmed, investigate endpoint authentication, handler failures, and downstream API calls. Keep scheduled-task diagnostics subject to the same redaction rules as interactive requests.
