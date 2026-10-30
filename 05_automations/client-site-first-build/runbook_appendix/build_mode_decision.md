# Appendix: Build Mode Decision Tree

> Choose the build mode and determine whether an existing site is being replaced before beginning other work.

## Two Independent Dimensions

Every build is parameterized by TWO independent decisions:

1. **Build mode** (Section: Three Modes below): what gets built (website / hub / combined)
2. **Site-port flag** (Section: IS_SITE_PORT Dimension below): is this a greenfield first build, or a port of an existing site?

Ask about the site-port flag first, then the build mode. These decisions are independent: any build mode can be either greenfield or a site-port.

## Three Modes

### WEBSITE_ONLY

**Build**: Standard marketing or product website.
**Sanity**: NO. Skip Sanity setup entirely.
**Astro structure**: Pure-static pages. No Sanity client wired. One Worker.
**Deploy artifact**: The site repository.
**Repo**: An owner-controlled repository named for the site.
**Worker name**: A matching, site-specific deployment name.

**Triggers**:
- User says: "Build a website for my ceramic studio" / "Build our bakery's landing page" / "Stand up a marketing site for our bicycle-parts business"
- The Claude Design handoff is a single-page or few-page marketing site with no resource-library or blog structure
- The business does not currently publish ongoing content such as guides, customer stories, or downloadable resources

### RESOURCE_HUB_ONLY

**Build**: Sanity-backed resource hub with no surrounding marketing site.
**Sanity**: YES. Complete Sanity setup.
**Astro structure**: Sanity client wired. Resource routes are Sanity-driven; supporting pages may be static. One Worker.
**Deploy artifact**: The hub repository.
**Repo**: An owner-controlled repository named for the resource hub.
**Worker name**: A matching, hub-specific deployment name.

**Triggers**:
- User says: "Build a resource hub for our kitchen-equipment business" / "Stand up our bicycle-parts guide library" / "Build our garden shop's how-to hub"
- The Claude Design handoff has a hub-page structure with collections, taxonomies, and filterable cards
- The business already has a marketing site elsewhere and is adding only the hub component
- This is the **default for hub-only handoffs**

### COMBINED

**Build**: Marketing website plus integrated resource hub. Two route classes within one Astro application.
**Sanity**: YES. Complete Sanity setup.
**Astro structure**: Hybrid pages strategy. Static marketing routes for the home, about, and contact pages, plus Sanity-driven hub listing, resource detail, and topic pages. One Worker, one Astro application.
**Deploy artifact**: One repository containing the combined site; the hub occupies a section of the site.
**Repo**: An owner-controlled repository named for the site.
**Worker name**: A matching, site-specific deployment name.

**Triggers**:
- User says: "Build our bakery's full site with customer stories" / "Build our garden shop's site with how-to articles" / "Build a combined website and guide library for our kitchen-equipment business"
- The Claude Design handoff has BOTH a marketing-style hero AND a resources or library section
- The business needs both components and does not currently have a separate marketing site

## Decision Logic (when ambiguous)

If the user's request makes the mode obvious, proceed without asking again. If ambiguous, ask:

> Quick check, is this a website only, a resource hub only, or a combined website + hub?
> 1. website-only: marketing or product site, no Sanity backend
> 2. resource-hub-only: Sanity-backed hub, no surrounding site
> 3. combined: marketing site + integrated resource hub

If the user is unsure, ask one more diagnostic:

> Does the Claude Design handoff include: (a) collections, taxonomies, and filterable cards (resource hub indicators), (b) only landing-page-style content (website indicators), or (c) both?

## Mode-Specific Workflow Differences

| Activity | WEBSITE_ONLY | RESOURCE_HUB_ONLY | COMBINED |
|------|--------------|-------------------|----------|
| Sanity setup | SKIP | RUN | RUN |
| Component decomposition | static pages only | resource pages, with static supporting pages if needed | hybrid: marketing and resource pages |
| Sanity client | SKIP | wire it | wire it |
| Taxonomy seed | SKIP | run if YAML provided | run if YAML provided |
| GitHub repository naming | site-specific name | hub-specific name | site-specific name |
| Worker naming | match site repository | match hub repository | match site repository |
| Sanity environment variables | SKIP | configure required variables | configure required variables |
| Resource-hub maintenance handoff | SKIP | RUN | RUN |
| Website maintenance handoff | RUN | RUN | RUN |
| Site handoff notes | always | always | always |

## IS_SITE_PORT Dimension

Independent of build mode. Determine this before choosing the build mode.

### `IS_SITE_PORT == false` (greenfield, default)

The business has no existing site at the target domain. Build from scratch using the standard build process, with no site-port-specific work.

### `IS_SITE_PORT == true` (porting an existing site)

The business has a live site at the target domain, such as WordPress or another hosted CMS, and is rebuilding on Astro on Cloudflare Workers, with Sanity in hub modes. Content may be rewritten. The apex domain is preserved; each existing URL and asset path requires an explicit mapping decision to preserve inbound links and search visibility.

**Triggers**:
- User says: "Migrate our ceramic studio's site" / "Port our bakery's WordPress site to Astro" / "We're rebuilding our bicycle-parts company's existing site"
- The business has a live, indexed website at the target domain
- The business has existing third-party backlinks, such as guide references, partner mentions, or coverage on news and trade sites

**Site-port-only steps** (gated behind `IS_SITE_PORT == true`):

| Activity | Purpose | Reference appendix |
|------|---------|--------------------|
| DNS strategy | Ask how DNS and nameservers should be managed during migration | Establish the preference before preparing cutover |
| Backlink discovery | Identify existing URLs and externally linked assets | `05_automations/client-site-first-build/runbook_appendix/backlink_discovery.md` |
| Search and archive collection | Provide Google Search Console export instructions immediately; query Wayback Machine and Common Crawl in parallel | `05_automations/client-site-first-build/runbook_appendix/gsc_export_pause.md` |
| Export wait | Pause dependent work until the requested Google Search Console export is available | `05_automations/client-site-first-build/runbook_appendix/gsc_export_pause.md` |
| Discovery consolidation | Merge sources, verify URLs, and categorize destinations | `05_automations/client-site-first-build/runbook_appendix/backlink_discovery.md` |
| Existing-site archive | Save the old site's content and assets in a project-local archive | `05_automations/client-site-first-build/runbook_appendix/old_website_archive.md` |
| Redirect authoring | Prepare explicit URL mappings for user review | `05_automations/client-site-first-build/runbook_appendix/redirect_authoring.md` |
| Asset placement | Place retained assets on Sanity CDN or in the site's static asset directory | `05_automations/client-site-first-build/runbook_appendix/asset_placement.md` |
| Redirect application | Configure redirects and Worker routes for HTTP 410 responses; test the preview with curl | `05_automations/client-site-first-build/runbook_appendix/redirect_application.md` |
| Nameserver change | Pause before any required user-side nameserver change | `05_automations/client-site-first-build/runbook_appendix/dns_cutover_pause.md` |
| Production cutover | Execute the reviewed production transition | `05_automations/website-maintenance/runbook_appendix/promote_to_production.md` |
| Handoff documentation | Add redirect mappings and any needed external-link update requests to the handoff notes | `05_automations/client-site-first-build/runbook_appendix/cross_automation_handoff.md` |
| Maintenance record | Record whether the redirect mappings are live and verified | `05_automations/client-site-first-build/runbook_appendix/cross_automation_handoff.md` |

If `IS_SITE_PORT == false`, skip these activities entirely. Adding site-port support should not change the output of an otherwise identical greenfield build.

### Site-port-by-build-mode interaction

Site-port behavior layers on top of build mode:

| Build mode × IS_SITE_PORT | Notes |
|----|----|
| WEBSITE_ONLY × false | Greenfield marketing site |
| WEBSITE_ONLY × true | Port of an existing marketing site from WordPress to Astro on Workers |
| RESOURCE_HUB_ONLY × false | Greenfield Sanity hub |
| RESOURCE_HUB_ONLY × true | Port of an existing resource hub |
| COMBINED × false | Greenfield marketing site + hub |
| COMBINED × true | Port of an existing site with an integrated hub |

Site-port adds discovery, verification, and redirect mappings. Build mode determines the default asset destination: Sanity CDN for hub modes, or the site's static asset directory for website-only builds.

## Decision Logic (IS_SITE_PORT)

If the user's request makes the answer obvious, such as "Migrate the old example.com site," proceed without asking again. If ambiguous, ask:

> Is this a port of an existing site or a greenfield first build?
> 1. Port: an existing site at the target domain; we need to preserve inbound links
> 2. Greenfield: no existing site; we're building from scratch

If the user is unsure:

> Has the business previously published anything publicly at this domain, such as a website, a marketing page, or a landing page that appeared in search results? If yes, treat it as a port and investigate the existing URLs. If no, treat it as greenfield.

## Edge Case: Mode Switch Mid-Build

If the user reveals during initial planning that the build needs a different mode, pause dependent work and confirm the revised scope. Repeating planning is inexpensive before infrastructure exists. Changing modes after creating the Sanity project, GitHub repository, and Worker can require substantial rework.

Before continuing, verify indexing restrictions and identify every preview and production deployment surface. Confirming the revised scope early prevents avoidable infrastructure changes and accidental public exposure.
