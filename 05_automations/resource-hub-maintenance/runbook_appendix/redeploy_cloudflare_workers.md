# Redeploying a hub (Cloudflare Workers Builds, with a Vercel note)

> Platform setup is covered in `09_guides/GITHUB_SETUP.md`, `09_guides/DEPLOY_CLOUDFLARE.md`, and
> `09_guides/DEPLOY_VERCEL.md`.
> The setup assumed here: your GitHub repo is connected to **Workers Builds**;
> `main` = production; `preview` and any configured feature branch = a preview deployment with its own URL.
> Verify current Cloudflare settings and UI locations before relying on them.

## A. After a code change (components, CSS, copy)

Set `VOIDWRIGHT_ROOT` to your package directory. Replace the example repository and branch values before running:

```bash
cd "<your-site-repo>"
npx astro build > /tmp/build.log 2>&1
build_rc=$?
echo "rc=$build_rc"                                   # local check first: exit 0 or stop
if [ "$build_rc" -ne 0 ]; then exit "$build_rc"; fi
git switch -c hub/<topic>                              # or work on preview
git add -A && git commit -m "hub: <what changed>"
git push -u origin hub/<topic>
```

Workers Builds builds the configured branch and publishes a preview URL. Review it there. When it is right, merge to `main`
and Workers Builds deploys production.

Watch the build instead of guessing:

```bash
python3 "$VOIDWRIGHT_ROOT/06_web_tools/builds_watch.py" --worker "<your-worker>" --commit "$(git rev-parse --short HEAD)" --branch "hub/<topic>"
echo "rc=$?"     # 0 = all builds succeeded, 1 = a build failed, 2 = timeout
```

**Monitoring trap:** a watcher can report success without covering the preview build you need to verify. Check whether
the Workers Builds API exposes the relevant preview builds, and judge the preview by what it serves too:

```bash
python3 "$VOIDWRIGHT_ROOT/06_web_tools/preview_url_watch.py" --url "<preview-url>" --probe /resources/ --marker '<a string only the new build has>'
echo "rc=$?"     # 0 = the expected build is serving, 2 = timeout
```

## B. After a Sanity-only change

For content fetched at build time, a Sanity edit makes no git diff, so it needs a separate rebuild trigger.
Configure a deploy hook to rebuild the production branch. Its URL is a secret, so read it from your key file without
printing it or putting it on a command line. Set `WEBTOOLS_KEYS_FILE` to that file's location:

```bash
awk -F= '$1=="DEPLOY_HOOK_URL"{print "url = \"" substr($0, index($0, "=") + 1) "\""}' "$WEBTOOLS_KEYS_FILE" \
  | curl -sS -X POST -K - -o /dev/null -w '%{http_code}\n'
```

Once the Sanity webhook is connected to the rebuild trigger, publishing does this automatically. An empty commit is not
a reliable rebuild trigger; use the hook or a real file change.

To see a CMS change on a **preview** before production, push a real change to the preview branch. If publishing already
triggers production rebuilds, use an isolated preview content source or pause that trigger before publishing.

## C. Secrets and variables

Build-time variables live in the Workers Builds settings; set runtime secrets with
`bash "$VOIDWRIGHT_ROOT/06_web_tools/wrangler-safe" secret put NAME` (Wrangler prompts for the value).
Reading published content from a public Sanity dataset needs **no** token in either place. Ensure changed runtime secrets
or variables are included in the deployment you verify.

## D. Verify

Set `SITE_URL` to the production origin and `CHANGED_SLUG` to the changed resource's slug.
Create `shipped_slugs.txt` as a local verification input containing one published resource slug per line.
The commands below generate temporary page output and a status log:

```bash
# production: a string only the new build has
curl -sS "$SITE_URL/resources/$CHANGED_SLUG/" > /tmp/page.html
echo "rc=$?"
grep -c '<a-string-only-the-new-build-has>' /tmp/page.html
# every shipped slug returns 200
while read -r s; do
  printf '%s %s\n' "$(curl -sS -o /dev/null -w '%{http_code}' "$SITE_URL/resources/$s/")" "$s"
done < shipped_slugs.txt > slug_check.log
grep -vc '^200 ' slug_check.log      # must print 0
```

If your previews are protected by Cloudflare Access or Vercel Deployment Protection, `curl` without credentials can get
a login page, often after a redirect, and that is not the site.
`06_web_tools/preview_url_watch.py` sends your Access service token when `CF_ACCESS_CLIENT_ID` and
`CF_ACCESS_CLIENT_SECRET` are in its configured key file; otherwise use a logged-in Playwright context
with saved storage state kept outside the repo.

## E. Rollback

Run `bash "$VOIDWRIGHT_ROOT/06_web_tools/wrangler-safe" rollback` to restore the previous production version, or
revert the commit on `main` and let Workers Builds redeploy. Record which method you used and the restored version
in your site's maintenance log.

## Vercel note

On Vercel the same setup applies: a push to a configured non-production branch makes a preview deployment, a merge to `main`
deploys production, and a Vercel deploy hook, stored as `DEPLOY_HOOK_URL` and called as shown in B, rebuilds after a
CMS-only change. Setup: `09_guides/DEPLOY_VERCEL.md`. Rollback: promote the previous deployment in the dashboard, or revert on
`main`. If you manually pin a review alias to a preview deployment, re-point it after every deploy; that pinned alias
does not follow later deployments automatically.

## Anti-patterns

- Pushing without a local `npx astro build` (a remote build failure costs minutes and a commit).
- Reading a build's exit code through a pipe (`npm run build | tail` reports `tail`'s status).
- Trusting a watcher that only reads the builds API.
- Using `curl -L` through a login page and calling the login page a pass.
