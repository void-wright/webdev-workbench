# Build, Deployment, and Runtime Configuration

## Dependencies and workspace boundaries

Inspect the relevant `package.json` before adding a package. Reuse an existing dependency when it already meets the need, and install new packages in the workspace that owns them.

Declare development-only tools as development dependencies:

```sh
npm install --save-dev <package>
npm run type-check
```

Replace `<package>` with the required package name. Run the commands in the intended workspace, or use your package manager's workspace targeting option.

For monorepo deployments, verify that the hosting configuration includes:

- The correct application root directory.
- A build command targeting the intended workspace.
- The correct framework detection or explicit framework setting.
- Access to shared packages and files outside the application directory.

## Secrets and environment isolation

Keep secrets out of version control. Ignore local secret files in Git and run secret detection before committing. If a secret is committed, revoke or rotate it. Removing the file alone does not make the exposed credential safe.

Separate development, preview, and production credentials and service access. Review the hosting provider's variable settings for each environment, including database connections and external service credentials. A preview deployment should not inherit production access by default.

Generate encryption keys only after confirming the implementation's required byte length and encoding. For example:

```sh
openssl rand -hex 32
```

This generates 32 random bytes represented as 64 hexadecimal characters. Use it only when that size and representation match the implementation's requirements. Check whether the application expects decoded bytes or the encoded string.

After changing deployment environment variables, trigger a new deployment directly or through the configured Git integration. Existing deployments may retain their previous configuration.

## Build caching and release validation

Include every build-affecting environment variable in the build cache configuration. Otherwise, a cache hit can return output generated with an old configuration.

For Turbo, review `globalEnv` whenever a feature introduces a build-affecting variable. Ensure changes to those variables invalidate the relevant cached output.

Configure the hosting provider's Git integration to deploy automatically from the intended branch. Protect that branch and disable force pushes so the source history used for releases cannot be casually rewritten.

Run type checking in continuous integration even when the hosting provider also builds the application:

```sh
npm run type-check
```

Confirm that the command is defined for the project and that a failing check blocks the release workflow.

## Database changes and access policies

Review migrations before execution. Check the schema changes, potential data loss, and compatibility with the application version that will use them.

Before applying a migration, verify the target environment and database connection. After applying it, inspect the expected schema in the database editor.

Run seed data separately, after schema migrations succeed. Keeping these operations distinct makes structural changes and data population easier to review and control.

Verify database access policies through representative user access. An enabled row-level security indicator proves only that the feature is enabled, not that its policies enforce the intended permissions.

For a regional bakery chain, test that a branch employee can access permitted branch records and cannot access restricted records belonging to another branch. Include unauthenticated access and any privileged roles in the checks.

## Private routes and data caching

Render private, user-specific pages at request time where the framework supports it. Audit private routes for consistent rendering configuration.

In Next.js routes that support this setting:

```js
export const dynamic = 'force-dynamic';
```

Treat rendering mode, authorization, and data caching as separate concerns:

- Check authentication and authorization on the server before returning private data or performing protected actions.
- Review shared caches for private data. Disable shared caching where appropriate, or scope cache entries to the authorized user or tenant.
- Confirm that one user's request cannot receive another user's cached response.

Request-time rendering alone does not establish any of these access boundaries.

## Scheduled endpoints

Authenticate scheduled endpoint requests before executing the task or performing side effects. Validate the bearer authorization header against the configured secret, and reject missing or invalid credentials. Reject requests if the expected secret is not configured.

Match the handler and schedule to the hosting platform's supported request method and plan constraints. For Vercel:

- Support GET requests for the scheduled endpoint.
- Verify that the job appears in Cron Jobs settings.
- Confirm that the hosting plan supports the intended schedule.

Use environment-specific credentials for scheduled work, just as for other service access.

## Loading and error states

Scope route loading placeholders to the content being loaded. Persistent navigation and layout elements should remain in their shared layout rather than appearing again inside the placeholder. Inspect loading states for duplicate headers, sidebars, or navigation.

Give route error states both a retry action and a way to leave the failed route.

In Next.js, make the route error boundary a client component by placing this directive at the start of the file:

```js
'use client';
```

Wire the retry action to the boundary's supplied reset function:

```js
reset();
```

Include a link to a safe destination that remains useful when the failed route cannot recover.
