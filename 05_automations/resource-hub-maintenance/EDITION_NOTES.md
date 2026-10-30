# Edition notes: resource-hub-maintenance (generic edition)

## What this edition is

This is the **generic edition** of the Voidwright resource-hub automation. It is for anyone who wants to stand up a
CMS-backed resource hub (a library of articles, guides, videos, case studies and files) on a site **they own**, and then
look after it, using **their own** GitHub repository, **their own** Cloudflare or Vercel account and **their own**
Sanity project.

The automation acts as a content infrastructure architect and hub curator. Its guidance focuses on clear
decisions, careful source reading and maintainable content. Examples are invented and unrelated to any private
site, account or person.

## What changed from the previous edition

| Area | Previous edition | This edition |
|---|---|---|
| Target | assumptions about a particular deployment | any site you own |
| Accounts | fixed account assumptions | your own GitHub, Cloudflare or Vercel, and Sanity accounts |
| Credentials | environment-specific credential loading | a private key file with mode 600 permissions, **parsed, never sourced**, using the package's web tools |
| Previews | protection assumed for every preview | public-by-URL by default; protection is optional through Cloudflare Access or Vercel Deployment Protection |
| Registry | pre-filled site configuration | an empty template with a clearly marked invented example |
| Examples | deployment-specific examples | invented kitchen-equipment makers, bicycle-parts companies, garden-supply shops, ceramic studios and regional bakery chains |
| Rulings | decisions without portable explanations | rules with their reasons: “Prefer X, because Y” |
| Memory references | opaque lookup references | descriptive search phrases |
| Recall checks | references tied to a particular memory store | `{phrase, row}` pairs that can be checked against your loaded content |
| Deploy steps | deployment-specific commands | package deploy guides and generic commands |
| Skillbook | rules mixed with project details | reusable rules with their reasons preserved |

## Tools this edition expects

Use [the skill installer](../../bin/install_skills.sh) to install the packaged skills:

```bash
bash bin/install_skills.sh
```

The package provides these supporting files and tools. Check their setup instructions before use:

- **Memory content and checks**: [web-craft memory pack](../../02_memory/webdev_pack.json), [recall battery](../../02_memory/recall_battery.json) and [battery runner](../../02_memory/run_battery.py).
- **Agent definitions**: [design-generator](../agents/design-generator.md), [design-reflector](../agents/design-reflector.md) and [design-curator](../agents/design-curator.md).
- **Web tools**, documented in [the web-tools README](../../06_web_tools/README.md):
  - [cf-api](../../06_web_tools/cf-api) for Cloudflare API calls;
  - [wrangler-safe](../../06_web_tools/wrangler-safe) for Wrangler with the intended account's variables;
  - [bearer-curl](../../06_web_tools/bearer-curl) for authenticated HTTP requests, including Sanity API writes;
  - [builds_watch.py](../../06_web_tools/builds_watch.py) and [preview_url_watch.py](../../06_web_tools/preview_url_watch.py) to watch builds and previews.
- **Guides**: [GitHub setup](../../09_guides/GITHUB_SETUP.md), [Cloudflare deployment](../../09_guides/DEPLOY_CLOUDFLARE.md) and [Vercel deployment](../../09_guides/DEPLOY_VERCEL.md).
- **Your own accounts**: GitHub, Cloudflare or Vercel, and Sanity, authenticated with `npx sanity login` or an API token as appropriate.

Configure credentials using [the setup guide](../../SETUP_GUIDE.md) and [the key-file example](../../09_guides/keys.env.example).
Keep the actual key file outside the repository with mode 600 permissions. Parse it as data rather than sourcing
it as shell code. Never paste a key into chat, the repository, stored notes or logs.

## Not available here (and what to use instead)

| Not available | Use instead |
|---|---|
| A hosted knowledge service | the packaged memory content and your own searchable project notes |
| A custom Sanity management service | the Sanity HTTP API through the packaged bearer-curl tool, or `npx sanity` with its own login |
| A ready-made product catalogue | the resource's own source document, fetched and read before writing |
| Built-in messaging, task-tracking or marketing integrations | your repository's content registry, Sanity content records and your site's form stack |
| An external review service | the packaged [Inner Council instructions](../../04_reasoning/commands/inner-council.md) and reasoning skills |
| Extra domain-specific skills | the packaged resource-hub, page-building, slug-design, design, maintenance, AEO, agent-readiness, graphic-design, WebGL and planning skills |
| Managed repository or hosting accounts | your own GitHub repository and Cloudflare or Vercel account |

## About the recall phrases

The memory map in [the comprehensive guide](comprehensive_guide.md), [startup queries](startup_queries.json) and
[recall phrases](recall_phrases.json) contains **search phrases**. These use the vocabulary of the web-craft memory
pack, but this edition does **not** claim they were verified against the content you loaded. If a phrase returns
nothing useful, search with the topic words in the map's “What you get” column, then replace the phrase with one
that works in your search system.

## Judgement calls

- **The curator stands up the hub as well as caring for it.** A hub added to an existing site extends a structure
  that already exists, so use the resource-hub setup guidance alongside the
  [first-build guidance](../client-site-first-build/comprehensive_guide.md). Use the first-build automation for a
  whole new site.
- **Static pages plus a deploy hook are the recommended starting point** on Cloudflare Workers. For pages rendered
  on request, verify the hosting platform's caching behavior. A Worker's own responses are not edge-cached by
  default; configure and test caching explicitly.
- **Cloudflare and Vercel UI locations and variable names require verification at execution.** Re-check the
  platform's current documentation before relying on setup instructions.
- **The skillbook keeps its structure and entry names.** Project-specific details are removed or generalised,
  while reusable rules and their reasons remain. Tool references should resolve to packaged tools or public
  platforms.
