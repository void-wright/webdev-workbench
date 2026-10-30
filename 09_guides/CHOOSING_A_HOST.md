# Cloudflare or Vercel? A short guide

Both are good. For a mostly static Astro site, either can work free within its limits, provided the site qualifies for the plan (as of October 2026; re-check before relying on it). A static site serves pages prepared before visitors arrive. Pick Cloudflare if you want free commercial hosting or already manage your domain there. Pick Vercel if reviewer comments matter and you accept paying for a business site (as of October 2026; re-check before relying on it). Check [Cloudflare’s plans](https://www.cloudflare.com/plans/) and [Vercel’s commercial-use rules](https://vercel.com/docs/limits/fair-use-guidelines).

## What you will have at the end

- A hosting choice that fits your site.
- A clear reason for that choice.
- A checklist of what changes if you move later.
- The next deployment guide to follow.

## Before you start

You need a browser and a description of your planned site.
No hosting account, terminal tools or payment details are needed to make this choice.
Allow a short reading session, plus time to check any unclear requirements with your agent.
A host is the service that makes your website available online.

## 1. Compare the hosts

The table covers hosting a static site, with optional server code.
Server code runs on the host instead of in a visitor’s browser.
A preview is a test copy of your site.
A branch is a separate line of work in your project.

Comparison: all vendor facts in this table are **(as of October 2026; re-check)**.

| Question | Cloudflare | Vercel |
| --- | --- | --- |
| Free plan and commercial use | Workers Free allows commercial sites within its limits. See [plans](https://www.cloudflare.com/plans/). | Hobby is for personal, non-commercial use only. A business site needs Pro or higher. See [commercial-use rules](https://vercel.com/docs/limits/fair-use-guidelines). |
| What happens beyond free limits? | Worker requests over the daily free limit fail. Direct static asset requests are free and unlimited; requests that run server code count separately. See [billing and limits](https://developers.cloudflare.com/workers/static-assets/billing-and-limitations/). | Hobby usage can be limited or projects paused. Pro offers Spend Management to monitor and control spending. See [Hobby limits](https://vercel.com/docs/plans/hobby) and [usage management](https://vercel.com/docs/pricing/manage-and-optimize-usage). |
| Preview links per branch | Yes, with branch previews configured. See [branch builds](https://developers.cloudflare.com/workers/ci-cd/builds/build-branches/). | Yes. See [sharing deployments](https://vercel.com/docs/deployments/sharing-deployments). |
| Protecting previews | Cloudflare Access, part of Zero Trust, controls who can enter. Its free plan covers up to 50 users. Outsiders can use an emailed one-time PIN. See [plans](https://www.cloudflare.com/plans/) and [PIN login](https://developers.cloudflare.com/cloudflare-one/integrations/identity-providers/one-time-pin/). | Vercel Authentication with Standard Protection is available on all plans. Reviewers need an account with access or a shareable link that bypasses protection. See [protection](https://vercel.com/docs/deployment-protection) and [shareable links](https://vercel.com/docs/deployment-protection/methods-to-bypass-deployment-protection/sharable-links). |
| Reviewer comments on previews | No equivalent built-in reviewer comments toolbar. Plan a separate feedback channel. | A built-in toolbar supports comments. Commenting requires a Vercel account, even when viewing through a shareable link. See [preview sharing](https://vercel.com/docs/deployments/sharing-deployments). |
| Server code | Workers uses an edge runtime, an execution environment distributed across the network. It supports many Node.js features but is not full Node.js. See [compatibility](https://developers.cloudflare.com/workers/runtime-apis/nodejs/). | Functions supports a Node.js runtime, an environment for running JavaScript outside a browser. See [Node.js Functions](https://vercel.com/docs/functions/runtimes/node-js). |
| DNS and domains | Also provides DNS, the records that direct a domain to its services. Its registrar sells and renews supported domain names at cost. See [DNS](https://developers.cloudflare.com/dns/) and [Registrar](https://developers.cloudflare.com/registrar/). | Your domain needs DNS records pointing to the host. Any DNS provider can manage them, including Cloudflare with its proxy off. See [Cloudflare integration](https://vercel.com/docs/integrations/external-platforms/cloudflare). |
| Configuration files | This workbench uses `wrangler.jsonc`, plus `public/_headers` and `public/_redirects` for static responses. See [Workers docs](https://developers.cloudflare.com/workers/), [headers](https://developers.cloudflare.com/workers/static-assets/headers/) and [redirects](https://developers.cloudflare.com/workers/static-assets/redirects/). | Uses `vercel.json` for hosting configuration, including headers and redirects. See [project configuration](https://vercel.com/docs/project-configuration). |
| Lock-in | Low for static sites: the generated files can move. Provider-specific server code takes more work. | Low for static sites: the generated files can move. Provider-specific server code takes more work. |

Lock-in means the effort required to leave a service.
Headers are instructions sent with a web response.
Redirects send visitors from one address to another.
A proxy is an extra service between visitors and the host.

**In your browser:** Open the linked plan and protection documentation for your likely choice.
Check whether its current terms fit your site.

**Check:** You can explain its commercial-use rule, usage limits and reviewer access method.

## 2. Answer the questions that decide it

Write your answers in a project note.
Ask your agent to explain anything you cannot answer yet.

### Is it a business site?

Crumb & Crust Bakery’s `bakery-site` promotes a business, even without online ordering.
For that site, Vercel means Pro or higher (as of October 2026; re-check before relying on it). See [commercial-use rules](https://vercel.com/docs/limits/fair-use-guidelines).
Do not assume a site qualifies as personal merely because it is small.

### Do you want reviewers to comment on previews?

If comments beside the page are important, favour Vercel’s built-in toolbar (as of October 2026; re-check before relying on it). See [preview sharing](https://vercel.com/docs/deployments/sharing-deployments).
If written feedback elsewhere is enough, this feature need not decide your host.

### Is your domain’s DNS already on Cloudflare?

Staying with a familiar dashboard may reduce the setup you need to learn.
You can also keep that DNS provider while hosting on Vercel, with the relevant records set to DNS only, meaning the proxy is off (as of October 2026; re-check before relying on it). See [integration guidance](https://vercel.com/docs/integrations/external-platforms/cloudflare).

### Do you need long-running server code?

Describe the job first: for example, processing a large upload.
Ask your agent to distinguish computing time from time spent waiting for another service.
Both platforms impose execution limits; neither ordinary request handler should be treated as an always-running server (as of October 2026; re-check before relying on it). See [Workers limits](https://developers.cloudflare.com/workers/platform/limits/) and [Vercel limits](https://vercel.com/docs/limits).
Check whether the job needs a separate background service before choosing.

### Do you want one bill?

List hosting, domain renewal, email and any other paid services.
Using one supplier can simplify administration, but does not guarantee one invoice.
Check the actual services and charges before consolidating.

**Check:** Write “I choose this host because…” and complete it using your answers.

## 3. Understand that you can move later

For a static site, moving usually means configuration and testing rather than rewriting pages.
Budget for these tasks:

- **DNS:** Point the website records to the new host. Keep a record of the old values. Leave email records alone.
- **Environment variables:** Recreate named settings supplied outside your source code. Check preview and live settings separately.
- **Headers and redirects:** Translate the rules, then test their effects.
- **Preview protection:** Recreate reviewer permissions and test them while signed out.
- **Server features:** Check any provider-specific code or stored data separately.

Cloudflare’s static `_headers` and `_redirects` rules need translation into Vercel’s `vercel.json`, or the reverse (as of October 2026; re-check before relying on it). See [Cloudflare headers](https://developers.cloudflare.com/workers/static-assets/headers/), [redirects](https://developers.cloudflare.com/workers/static-assets/redirects/) and [Vercel configuration](https://vercel.com/docs/project-configuration).
For this workbench, the Cloudflare source files sit under `public/`.
Do not simply rename the files.

Keep keys only in `~/.config/webtools/keys.env` with mode `600`, which restricts access to its owner, or in the host’s secret store.
Never print, copy, paste or `source` the key file.
Never put keys in the repository, an AI chat or a command line.
Enter any needed key yourself in your own terminal or editor, or directly into the host’s secret store.

Moving costs your setup time and may involve overlapping paid service.
Test the replacement before changing DNS, and keep the old deployment available until the move works.
A deployment is a published copy of your site.

**Check:** Your move checklist covers DNS, settings, response rules and reviewer access.

## 4. Follow the deployment guide

Choose the guide for your decision:

- [DEPLOY_CLOUDFLARE.md](DEPLOY_CLOUDFLARE.md)
- [DEPLOY_VERCEL.md](DEPLOY_VERCEL.md)

Follow its prerequisites before creating accounts or publishing anything.
Tell your agent your chosen host, whether the site is commercial and how reviewers should give feedback.

**Check:** You have opened the matching guide and can explain your choice to your agent.

## Troubleshooting

- **Symptom:** You cannot decide. **Cause:** You are comparing features without requirements. **Fix:** Answer the questions in Step 2 for your actual site.
- **Symptom:** A reviewer cannot open a preview. **Cause:** Access may be restricted. **Fix:** Check permissions and test the intended reviewer route.
- **Symptom:** A preview opens but comments do not work. **Cause:** Viewing and commenting can require different access. **Fix:** Check the comments row and linked sharing documentation.
- **Symptom:** Hosting stops working after traffic increases. **Cause:** A usage limit may have been reached. **Fix:** Check the host’s usage information before changing plans.
- **Symptom:** Pages work after moving, but redirects fail. **Cause:** Hosting rules may not have been translated. **Fix:** Test each rule against the new configuration.

## Undo / remove

Reading this guide changes nothing, so there is nothing to remove.
If you only wrote a decision note, edit it when your requirements change.
If you already deployed, use that deployment guide’s removal instructions.
Before removing an old host, confirm the replacement works and check any remaining subscriptions separately.