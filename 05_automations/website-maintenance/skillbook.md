# Website Maintenance: Skillbook (generic edition)

> **Generic edition**: for anyone maintaining their own sites on their own accounts. Examples use invented businesses. Cloudflare Workers is the primary deployment platform; Cloudflare Pages and Vercel are alternatives.

**Persona**: Dr. Cassian Holt, Web Architect & Caretaker (maintenance specialist, platform aware)
**Version**: Generic maintenance edition.
**Last curated**: Update this field when strategies are reviewed.
**Scope change note**: First-time build skills, including template cloning, brand application and new-site scaffolding, belong in `05_automations/client-site-first-build/skillbook.md`. This skillbook covers maintenance of existing sites across supported platforms.

This skillbook is a self-improving strategy collection. Every maintenance, agent-readiness or audit run appends a curator log entry describing what was learned. Strategies are tagged with H-count (Helpful) and Harm-count. Protected strategies have H ≥ 5 and Harm = 0.

---

## How to use this skillbook

1. **At startup**: read this file after loading the maintenance persona and recalling relevant prior lessons.
2. **During generation**: consult strategies when facing a decision, such as which pattern or library to use.
3. **At curator cycle**: after each ACE reflector cycle, add, update, protect or retire strategies based on what the Reflector flagged.

---

## Seed Strategies (bootstrap from reusable maintenance lessons)

### ARCHITECTURE

| ID | H | Strategy |
|----|---|----------|
| arch-001 | seed | **Static-first Astro**. Default to `output: 'static'`. Use server rendering only when a specific feature demands it, such as personalized content. Use the rendering options supported by the installed Astro version. Zero-JS default means React islands only where interactive behavior is needed. |
| arch-002 | seed | **React Islands pattern**. Interactive components use `<ReactComponent client:load />` or `client:visible`. Keep islands small and independently testable. |
| arch-003 | seed | **BaseLayout head-slot pattern**. `<slot name="head" />` in BaseLayout allows per-page schema injection and agent-ready link tags using relations such as `api-catalog`, `describedby` and `service-doc`. Every page's `<Layout>` wrapper can inject its own schemas. |
| arch-004 | seed | **Config as tokens**. Keep site-level constants, including name, URL, description, theme color and navigation links, in shared configuration. Keep colors, spacing and typography in shared visual tokens. Reference these values rather than repeating them throughout components. |
| arch-005 | seed | **Feature flags in shared configuration**. Gate the blog, resource hub, contact form and quote form behind explicit flags. This lets one template support sites with different scopes without leaving unused features visible. |
| arch-006 | seed | **Hybrid page strategy for resource hubs**. Resources with `htmlContent` get their own route; resources with only `externalUrl` link directly to the destination. Avoid empty detail pages. Keep Sanity document attributes within the applicable limit, including the 50-attribute constraint where enforced. |

### DESIGN SYSTEM

| ID | H | Strategy |
|----|---|----------|
| design-001 | seed | **CSS custom properties for all visual tokens**. Define colors, spacing and typography scales in `:root` or `body` as `--color-*`, `--space-*` and similar properties. React islands using inline styles MUST reference these through `var(--token-name)`, never hardcoded hex values. |
| design-002 | seed | **60/30/10 color rule**. Use 60% neutral, 30% secondary and 10% primary CTA color as a starting balance. Use at most one primary CTA color per viewport to preserve emphasis. |
| design-003 | seed | **Tablet grid collapse**. Three-column desktop grids become `repeat(2, 1fr)` at tablet widths of 640-1023px. Do not jump directly to a mobile single-column layout at that width. |
| design-004 | seed | **8px grid + 1.25 type ratio**. Use spacing values in multiples of 8px, with 4px for fine adjustments. Use a geometric type scale with a 1.25 ratio. |
| design-005 | seed | **When porting design systems, grep for ALL tokens**. Check functional colors, spacing scales and typography tokens as well as brand colors. A mismatch in any layer breaks the visual system. |

### AEO + AGENT-READINESS

| ID | H | Strategy |
|----|---|----------|
| aeo-001 | seed (PROTECTED-candidate) | **Review four schema types on every indexable page**. Check Organization, WebSite, BreadcrumbList and FAQPage. Include each only where it accurately describes the site or visible page content. Exclude noIndex pages from this search-discovery requirement. |
| aeo-002 | seed | **Review speakable markup on content pages**. Where supported and appropriate, identify concise passages suitable for spoken summaries. Keep the markup aligned with visible content and do not assume it guarantees voice-assistant use. |
| aeo-003 | seed (PROTECTED-candidate) | **Agent-readiness from launch**. Make public content and supported services discoverable through applicable metadata, agent cards, Link headers, content-use signals and machine-readable documentation. Publish real SHA-256 digests where integrity metadata is provided. Enable WebMCP or other interfaces only when they expose working capabilities. Record unsupported features as not applicable instead of inventing services to improve a score. |
| aeo-004 | seed | **Link headers through hosting configuration**. Define discovery endpoints for the site's actual capabilities. Example endpoint paths are `/.well-known/api-catalog` for an API catalog, `/.well-known/oauth-protected-resource` for OAuth resource metadata, `/llms.txt` for service documentation and `/sitemap-index.xml` for the sitemap. An example header is `Link: </.well-known/api-catalog>; rel="api-catalog", </.well-known/oauth-protected-resource>; rel="describedby", </llms.txt>; rel="service-doc", </sitemap-index.xml>; rel="sitemap"`. Omit endpoints and relations that do not apply, including OAuth metadata on sites without OAuth. Set appropriate Content-Type headers for JSON and Markdown responses. |
| aeo-005 | seed | **Real SHA-256 digests in the agent-skills index**. Generate digests from the exact skill files being published as a pre-build step. Regenerate them whenever those files change. Never ship placeholder digests. |
| aeo-006 | seed | **Markdown negotiation: BOTH header + URL fallback**. Generate Markdown versions of public content at build time and give them explicit URLs. Use request middleware to handle `Accept: text/markdown` when the platform supports it. Providing both routes supports consumers that cannot negotiate response formats. |
| aeo-007 | seed (PROTECTED-candidate) | **OAuth authorization_servers MUST be live, resolvable URLs**. Discovery checks probe each URL. Use the site's actual authorization-server URL. For Clerk, use the configured instance URL, such as `https://<instance>.clerk.accounts.dev`, and verify it against the application's configuration. Never substitute a branded hostname that has not been configured in DNS. |
| aeo-008 | seed | **Header-rule specificity**. Specific rules for published skill Markdown must not accidentally overlap with broad Markdown rules. Cloudflare can apply both and duplicate headers. Verify the deployed responses with `curl -I`. |
| aeo-009 | seed (PROTECTED-candidate) | **OAuth Protected Resource: `resource` field MUST match the resource being described**. For an origin-level resource, publish its metadata at that origin and use that origin as the resource identifier. Do not serve metadata from an unrelated origin while claiming it describes the current site. |
| aeo-010 | **RETIRED** (soft delete, lesson kept) | ~~**OAuth decision tree by business type**.~~ RETIRED: business categories do not establish authentication requirements, and an empty `authorization_servers` list does not provide usable OAuth discovery. Decide from the site's actual authentication architecture. A public garden-supply how-to hub should not advertise an OAuth service it does not offer. A protected service should publish valid metadata for its configured authorization server. Cookie authentication alone is not evidence that OAuth is supported. |
| aeo-011 | seed | **A2A Agent Card for a real A2A service**. Define `/.well-known/agent-card.json` as the discovery endpoint when the site operates an A2A agent. The card is distinct from an MCP Server Card. Describe the name, version, description, supported interfaces, capabilities and skills using the schema supported by the deployed protocol version. Publish both cards only when both services exist; they describe complementary capabilities. |
| aeo-012 | seed | **Force fresh scans, then classify failures**. Scanners may cache results per URL. After deployment, request a fresh scan through the evaluator's documented interface and inspect per-check status and evidence. Compare failures with the site's recorded exceptions. Distinguish a justified non-applicable check, such as an MCP card on a site without MCP, from an omitted implementation step. Fix new failures and omissions; do not fabricate capabilities to turn every indicator green. |

### FORMS + CONTACT

| ID | H | Strategy |
|----|---|----------|
| forms-001 | seed | **Contact form: Turnstile + Resend + Pages Function**. The form handler validates input with field checks and length limits, verifies the Turnstile token and sends the message through Resend. Return 200 on success, 400 on validation failure and 403 on Turnstile failure. |
| forms-002 | seed | **First-person CTAs**. Prefer a clear action such as "Send My Message" over "Submit". A ceramic studio's inquiry form should tell visitors what the button does. Treat any conversion benefit as a hypothesis to test on the site's own traffic. |
| forms-003 | seed | **Thank-you page noIndex**. After a successful submission, redirect to a dedicated confirmation page with `<meta name="robots" content="noindex, nofollow" />`. Configure the GA4 conversion using a `page_location` match for that page when analytics consent permits it. |
| forms-004 | seed | **Payload size limit 10KB**. Reject contact-form payloads larger than 10KB. Enforce the limit server-side to reduce abuse. |
| forms-005 | seed | **Interest dropdown is enum-validated server-side**. Define an explicit allowlist. For an invented regional bakery chain, values might be `order_question`, `store_feedback`, `event_catering` and `something_else`. Reject anything outside the allowlist. |
| forms-006 | seed | **HTML entity escaping in email templates**. Never interpolate user input directly into the Resend HTML body. Use an escape function so submitted text cannot become email markup. |

### SECURITY

| ID | H | Strategy |
|----|---|----------|
| sec-001 | seed (PROTECTED-candidate) | **CSP with tight allowlists, zero unsafe-eval**. For a site using Google Tag Manager and Turnstile, a starting script policy is `script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://challenges.cloudflare.com`. Include only origins the site actually needs, and replace broad inline-script permission with nonces or hashes where practical. Never use `unsafe-eval` or a wildcard source. |
| sec-002 | seed | **CSP must include ALL external font/stylesheet domains**. If fonts load from Google Fonts, add `fonts.gstatic.com` to `font-src` and `fonts.googleapis.com` to `style-src`. Missing a required origin can silently break typography or styling. |
| sec-003 | seed | **HSTS preload**. The header `max-age=31536000; includeSubDomains; preload` commits the domain and its subdomains to HTTPS. Verify HTTPS support across all affected hosts before enabling it. Observe the live configuration before submitting at https://hstspreload.org, and check the submission requirements at that time. |
| sec-004 | seed | **Pages secrets via Wrangler**. Use `npx wrangler pages secret put SECRET_NAME --project-name example-site` and supply the value through the secret prompt. Never commit secrets to Git or put their values in command-line arguments. |
| sec-005 | seed | **gitleaks + pre-commit hooks on every repo**. Configure secret scanning and commit hooks in the repository. New contributors run `pip install pre-commit && pre-commit install`. This catches accidental credential commits before they leave the machine. |
| sec-006 | seed | **Protect `main`**. Disable force pushes and land changes through a preview or feature branch. Configure branch protection or rulesets in GitHub where available. If the account cannot enforce a rule, document and follow the same verification, preview and review discipline manually. |
| sec-007 | seed | **Security hardening checklist for every repo**: secret scanning with gitleaks and pre-commit, protected main, least-privilege tokens, CSP, HSTS and other security headers, form hardening and dependency auditing. |

### DEPLOYMENT

| ID | H | Strategy |
|----|---|----------|
| deploy-001 | seed | **Git → Cloudflare Pages auto-deploy (alternative platform)**. Connect the repository through the Cloudflare Pages dashboard so a push to `main` triggers a build and deployment. Wait for the build result before treating the change as live. Select Git integration during setup; switching from Direct Upload requires recreating the project. |
| deploy-002 | seed | **Cloudflare API through `cf-api` for infrastructure**. From the package root, use `bash 06_web_tools/cf-api GET '/zones/{zone}/dns_records'` to read DNS records. Here, `/zones/{zone}/dns_records` is the Cloudflare API endpoint, with `{zone}` replaced by the zone identifier. POST, PATCH and DELETE change infrastructure. Read the current state before destructive calls and print only the fields needed, using a small `python3 -c` filter on the response if useful. Load the token from the configured key file and never print it. |
| deploy-003 | seed | **Use managed credentials for Git operations**. Authenticate through the operating system's credential manager or the Git provider's supported sign-in flow. Never paste a passphrase or token into a command line. |
| deploy-004 | seed | **Cannot change Pages deploy source**. Treat Direct Upload and Git integration as separate project setup choices. If the wrong source was selected, recreate the project after recording its configuration, domains and required secrets. |
| deploy-005 | seed | **Remove custom domains BEFORE deleting a Pages project**. Attached domains can block deletion. Detach them first and verify the deletion result rather than assuming the request succeeded. |
| deploy-006 | seed | **Runtime secrets don't survive project deletion**. After recreating a project, restore each required secret with `wrangler pages secret put` and verify the dependent features before returning the site to service. |
### QA + VERIFICATION

| ID | H | Strategy |
|----|---|----------|
| qa-001 | seed (PROTECTED-candidate) | **Playwright self-critique at 3 viewports**. 1440 (desktop), 768 (tablet), 375 (mobile). Save screenshots with the task's review evidence. Check: cards render, filters work, navigation is consistent, and images load. |
| qa-002 | seed | **Lighthouse ≥95 all 4 axes**. Performance, Accessibility, Best Practices, SEO. Run both mobile + desktop profiles. Re-run after any material change. |
| qa-003 | seed | **isitagentready.com scan after every agent-readiness change**. Target: all current standards pass. Results may be cached server-side. Allow propagation after deployment and request a fresh scan through the service's supported interface before treating a cached result as current evidence. |
| qa-004 | seed | **curl -I verification of every endpoint post-deploy**. Never trust "it deployed"; trust "I verified the response". Check status, Content-Type, Link, CSP, and HSTS. Fetch the body separately to verify the actual content. |
| qa-005 | seed | **Axe accessibility before Lighthouse**. Axe catches specific violations Lighthouse aggregates. Fix Axe first, then re-run Lighthouse. |

### COMMERCE STANDARDS

| ID | H | Strategy |
|----|---|----------|
| commerce-001 | seed | **Commerce standards decision tree by business model**. (a) Marketing site with no commerce → skip ALL payment and commerce integrations (x402, UCP, ACP, AP2). (b) Kitchen-equipment maker selling through verified trade accounts → skip x402; evaluate UCP and ACP for supported catalog and order operations, without advertising checkout that the site cannot complete. (c) Regional bakery chain with a direct-to-consumer Shopify storefront → check Shopify's native ACP support; evaluate UCP only if needed; skip x402. (d) Explicitly monetized API access or micropayments → evaluate x402 middleware. |
| commerce-002 | seed | **x402 default: SKIP for high-value B2B sales**. x402 targets micropayments through an HTTP 402 Payment Required flow. It does not fit a bicycle-parts wholesaler's account approval and negotiated purchasing process merely because the site sells products. Implement only when API access is explicitly monetized, and verify middleware support for the chosen runtime. |
| commerce-003 | seed | **UCP discovery profile served as application/json**. Use the discovery location and schema required by the supported UCP specification. Declare the protocol version, services, capabilities, payment handlers, and signing keys. Use reverse-domain service identifiers owned by the business, and advertise only implemented capabilities. Verify the schema against ucp.dev before publishing. |
| commerce-004 | seed | **ACP discovery served as application/json**. Use the discovery location and schema required by the supported ACP specification. Declare protocol identity and supported versions, documentation location, API base URL, transports, and supported services. Include extensions, intervention types, currencies, and locales only where supported. Validate enum values and identifier formats against agenticcommerce.dev before publishing. |
| commerce-005 | seed | **DEFAULT commerce stack for new storefronts: Astro static + Pages Functions**. Use WordPress/WooCommerce when maintaining an inherited site that already relies on it. For Astro sites that need commerce later, evaluate Shopify headless integration or Stripe Checkout via Pages Functions. |

### EDGE-CASE PATTERNS (inherited sites)

| ID | H | Strategy |
|----|---|----------|
| edge-002 | seed | **WordPress security plugins may block standards-discovery endpoints**. Wordfence, iThemes Security, and similar plugins can block requests before they reach the application. Explicitly allow the required discovery endpoints before testing. |
| edge-003 | seed | **WordPress page cache plugins can bypass custom Link headers**. WP Rocket and W3 Total Cache may serve cached HTML without running the `send_headers` action. Purge the cache after installing agent-readiness snippets, then verify headers on cached responses too. |

### CLOUDFLARE PAGES SPECIFICS

| ID | H | Strategy |
|----|---|----------|
| cf-001 | seed | **Use the Pages Functions integration for Pages deployments**. A separately deployed Worker is not automatically part of a Pages site. Use the supported Pages Functions routing pattern when request handling belongs to that deployment. |
| cf-002 | seed | **Configure response headers per path with globbing**. Check which rules match both a path and its children. Account for overlapping global and specific rules rather than assuming one replaces the other. Verify the resulting response. See aeo-008. |
| cf-003 | seed | **Use static redirect rules for simple path redirects**. Use 301/302 redirects where appropriate. Use Functions for routing that depends on request data or other dynamic conditions. |
| cf-004 | seed | **Serve R2 media through a dedicated custom domain**. Choose a bucket name associated with the site and configure its custom domain through R2. Verify DNS, public access, and HTTPS before using asset URLs in content. |
| cf-005 | seed | **`--commit-dirty=true` acknowledges uncommitted deployment changes**. Use it only for deliberate testing. For production, commit first so the deployed artifact has a reviewable source revision. |
| cf-006 | seed | **Cloudflare Web Analytics (RUM) beacon installed sitewide when enabled for the site**. Add to the shared layout immediately before `</head>`: `<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token": "<SITE_TOKEN>"}'></script>`. Obtain the token from Cloudflare Dashboard → Web Analytics → Add a site. Document the site's analytics and consent decision rather than treating cookieless collection as a blanket exemption. Use the dashboard's supported page-view, referrer, device, location, and Core Web Vitals reports to assess real visits. Do not equate referrer hosts with full source/medium attribution. Add `https://static.cloudflareinsights.com` to CSP `script-src` and `https://cloudflareinsights.com` to `connect-src`. If secret scanning flags the public beacon token, add a narrowly scoped exception for that value. CDN request totals alone do not replace browser measurements. Configure a separate Web Analytics entry and token for a separately deployed resource hub, and verify that its visits appear in the intended property. |

_For Cloudflare **Workers** sites deployed through Workers Builds from GitHub, see cf-008 and cf-009 for preview and main deployment guidance._

### ACE LOOP (UPDATED: ALWAYS for maintenance)

| ID | H | Strategy |
|----|---|----------|
| ace-001 | **PROTECTED** | **Generator → Reflector → Curator every iteration, MANDATORY for EVERY website change.** Apply the loop to copy edits, design tweaks, bug fixes, security updates, and small CSS adjustments. Small changes can accumulate into website drift; generation, independent review, and durable lessons each address a different part of that risk. Skipping a role weakens the loop. |
| ace-002 | **PROTECTED** | **9.8/10 HARD SATISFACTORY threshold, no rounding.** 9.79 = CONTINUE. A score below the threshold must not be marked SATISFACTORY. Below 9.5 on any dimension = CONTINUE. 2 consecutive flat iterations = STALLED. Maximum 5 iterations. |
| ace-003 | seed | **Pre-seed the skillbook from prior site-maintenance loops**. Reuse verified, generic lessons to give the first iteration reliable guidance. |
| ace-004 | seed | **After every Curator cycle, preserve ALL skillbook skills in the durable lesson store**. Keep one entry per skill and use consistent tags such as `ace-curator`, `website-maintenance`, and `webdev`. Batch updates when supported. Store generic patterns only; exclude private site data and credentials. |
| ace-005 | seed (PROTECTED) | **Empirical Lighthouse + axe scans REQUIRED to clear 9.8+ in any iteration.** Subjective code-inspection scoring caps at 9.6-9.7. The Reflector pass MUST run real-browser scans before promoting to SATISFACTORY. Minimum ACE scan targets: Performance ≥90, Accessibility ≥95, Best Practices ≥95, SEO ≥90, and axe zero Critical/Serious violations. These minimums do not replace the stricter qa-002 target. |
| ace-006 | seed | **Budget for architecture, polish, and final verification as separate passes.** Early passes settle structure; later passes address prioritized findings and validate the result. Do not promise SATISFACTORY after a fixed number of passes. Let the evidence and the hard threshold determine completion. |

### TEMPLATE-FIRST PROTOCOL

| ID | H | Strategy |
|----|---|----------|
| tpl-001 | seed (PROTECTED-candidate) | **Never generate a page from scratch when a canonical template and reference example exist**. READ the template, READ the reference, VERIFY understanding, THEN generate. Follow this sequence when creating Astro pages. |
| tpl-002 | seed | **Template = the existing page family.** On a live site, the canonical template for a new page is its nearest sibling page plus the shared layout and components; read them before generating. |
| tpl-003 | seed | **Template de-branding pattern for cloning**. Replace hardcoded navigation and footer brand references with the shared site-name setting. Replace CSS tokens with the destination site's tokens. Replace the logo SVG. |

### MEMORY + SELF-HEAL

| ID | H | Strategy |
|----|---|----------|
| mem-001 | seed (PROTECTED-candidate) | **Batch recall as DEFAULT startup**. Use the queries in `05_automations/website-maintenance/startup_queries.json` to retrieve relevant stored lessons together when the available retrieval tool supports batching. Start with up to 8 matches per query, then drill down with targeted searches. |
| mem-002 | seed (PROTECTED-candidate) | **Mandatory lesson-index self-heal at session end**. Store each new lesson with a concise retrieval summary and enough detail to apply it. Add index phrases only after verifying that they return the intended lesson in the top 5 results; do not rely on opaque IDs as search phrases. Update the curation record and record that the maintenance pass is complete. |
| mem-003 | seed | **One durable surface per kind**: reusable lessons belong in the lesson store; procedures belong in the automation's documentation. Avoid competing copies that can drift apart. |

### PLATFORM AWARENESS (multiple deployment platforms)

| ID | H | Strategy |
|----|---|----------|
| platform-001 | seed | **Read `05_automations/website-maintenance/runbook_appendix/client_registry.md` on EVERY startup and confirm the platform from the repo.** Workers, Pages, and Vercel use different deployment, secret, and domain commands. Never assume. |
| platform-002 | seed | **Use Workers commands for Workers sites**. Follow the configured Workers Builds commands for main and preview branches; use the appropriate Wrangler operations for secrets, D1 migrations, and rollback. Pages (`wrangler pages …`) and Vercel (`vercel …`) are separate deployment paths. See `05_automations/website-maintenance/runbook_appendix/platform_detection.md`. |
| platform-003 | seed | **DNS lives where the site's registry entry says**: Cloudflare, Vercel, or the registrar. For Cloudflare, use `06_web_tools/cf-api` with your own scoped token. Read the existing records first, decide the exact change, then apply it. |
| platform-004 | seed | **Protected previews need credentials for self-review.** If Worker previews sit behind Cloudflare Access, supply the service-token headers to Playwright and curl. `06_web_tools/preview_url_watch.py` supports this using `CF_ACCESS_CLIENT_ID` and `CF_ACCESS_CLIENT_SECRET`. Load secrets from a mode-600 credential file rather than placing their values on the command line. For Vercel, use saved authentication state or a protection-bypass token. |

### CROSS-AUTOMATION HANDOFF

| ID | H | Strategy |
|----|---|----------|
| handoff-001 | seed | **Route first-time setup to the first-build automation.** For a request such as "build a website for a ceramic studio", use `05_automations/client-site-first-build/comprehensive_guide.md`. It covers design handoff, repository and hosting setup, and reaching a stable preview. Website maintenance takes over after that handoff. |
| handoff-002 | seed | **Route Sanity content operations to resource-hub maintenance.** For requests such as "add this guide to the garden shop's hub" or "update its categories", use `05_automations/resource-hub-maintenance/comprehensive_guide.md`. Keep website-level maintenance distinct from content and taxonomy operations. |
| handoff-003 | seed | **Preview → production belongs to website maintenance.** For the configured Workers Builds flow, use a fast-forward merge to main after recorded sign-off, watch the build by UUID, and verify the live result. Roll back through Workers deployments when necessary. See `05_automations/website-maintenance/runbook_appendix/promote_to_production.md`. |

### CROSS-PROPAGATED FROM FIRST-BUILD REVIEW

These three skills also apply to maintenance of sites created through the first-build automation. They preserve the design handoff's JavaScript, require comparison with the approved visual reference, and ensure placeholder content is removed before production promotion. See `05_automations/client-site-first-build/skillbook.md`.

| ID | H | Strategy |
|----|---|----------|
| scaffold-004 | seed (PROTECTED, shared with first-build) | **JS port mandate from a Claude Design handoff is NON-NEGOTIABLE.** When maintaining a site built from a Claude Design handoff, preserve its main application script, animation and initialization scripts, and other shipped JavaScript assets during refactoring. These assets are part of the canonical design contract and may include Three.js, GSAP, or Lottie behavior that defines the visual deliverable. Replacing them with static SVG fallbacks silently changes that deliverable. Preserve the behavior or obtain agreement for an intentional design change. |
| qa-010 | seed (PROTECTED, shared with first-build) | **Canonical visual diff is a P0 Reflector gate when a canonical exists.** For any maintenance change, including copy edits, design tweaks, and bug fixes, compare against the approved design reference when available. The Reflector pass MUST include a CSS-token comparison for brand-critical selectors PLUS a 1440px screenshot diff. Identify the selectors during first build: typically the primary button, navigation call to action, hero, page header, and tab or filter bar. A maintenance refresh must not silently drift from the approved visual surface. |
| scaffold-003-consume | seed (Production prerequisite) | **Delete placeholder content before production promotion.** Mark temporary Sanity documents with `isPlaceholder: true` and the tag `PLACEHOLDER_REMOVE_BEFORE_LAUNCH` during first build. Before recording production sign-off, verify through the resource-hub maintenance process that every marked placeholder has been removed from the site's dataset. Confirm the result with a fresh query. If placeholders remain, stop promotion and complete their removal before proceeding. See `05_automations/website-maintenance/runbook_appendix/promote_to_production.md` and scaffold-003 in the client-site-first-build skillbook. |
### CROSS-PROPAGATED FROM A FIRST BUILD

These two skills apply to ongoing maintenance of resource hubs that intentionally show an empty state during preview, and to preserving a Tailwind compatibility pin when rebuilding an Astro site with prerendered routes.

| ID | H | Strategy |
|----|---|----------|
| cassian-maint-001 | Seed | **Empty-resource-hub maintenance pattern: do NOT replace an intentional empty state with placeholder cards.** When a collection page intentionally contains no real resources during preview because content entry has not started, its empty-state UI is part of the design. Do not replace it with `<PlaceholderCard />` components or "Coming soon" cards during a polish pass. For example, a kitchen-equipment maker's resource library can show a clear empty state until its first guides are ready. This makes the missing content visible and gives the site operator a clear next task. Placeholder cards hide that task and introduce visual debt that must be removed later. Read the available build and handoff notes to confirm that the empty state is intentional, then preserve it. Pairs with `wren-handoff-004` (resource-hub-maintenance skillbook) for bulk removal of marked placeholder content. |
| cassian-build-001 | Seed | **Preserve the Tailwind 4.1.18 pin when it is a documented workaround for an Astro 6 prerender failure.** When rebuilding or reinstalling dependencies for an affected Astro 6 site with a page declaring `export const prerender = true`, retain the exact dependency entry `"tailwindcss": "4.1.18"`, not `^4.1.18`. The failure to guard against is `Missing field 'tsconfigPaths' on BindingViteResolvePluginConfig.resolveOptions` during prerendering after an upgrade to Tailwind 4.2.x. Treat this as a dependency compatibility issue involving the Vite/rolldown resolver configuration; do not assume that the same failure affects every Astro 6 installation. Preserve a known working pin until a candidate upgrade passes a clean install and the full prerender build. Avoid reflexively running `npm update` or `npm-check-updates` during an unrelated maintenance refactor. Document the pin's reason beside the project's dependency instructions, keeping package JSON valid without comments. |

### STRICT-FIDELITY MODE A

These three skills define MODE A for faithful HTML-to-Astro recreation of captured HTML within an already deployed Astro site. Use this mode when the supplied HTML is the authoritative design.

| ID | H | Strategy |
|----|---|----------|
| strict-fidelity-html-recreation-mode | Seed | **Use MODE A when the user provides pristine HTML for faithful Astro recreation.** Trigger: a strict-fidelity handoff phrase, as defined in `trigger-phrase-mode-routing`. Process: assign a per-page Generator a strict-fidelity contract, then a per-page Reflector with 10–15 explicit fidelity checks. The Generator must not invent, reorder, paraphrase, omit or add sections; keep all internal `<a>` links relative; preserve supplied asset placeholders and `data-original-url` attributes; replace jQuery, theme or page-builder widgets with native CSS and browser behavior where equivalent; and treat the HTML as authoritative when accompanying notes conflict. Require a final high-level Reflector when the batch contains two or more pages, covering eight integration dimensions: navigation, routes, shared layout, typography, assets, responsive behavior, interactions and accessibility. For medium batches, process five to seven pages in parallel per round. SATISFACTORY requires a composite score ≥ 9.80/10 under `ace-002`. Use this mode for a faithful page addition or replacement, such as a bicycle-parts company's supplied HTML guide design or a page migrated from its existing WordPress site. |
| trigger-phrase-mode-routing | Seed | **Detect MODE A versus MODE B from the user's phrasing before choosing the process.** MODE A trigger phrases include "reverse-engineered HTML", "lift this page verbatim", "absolute recreation", "byte-perfect", "I'm passing you a pristine HTML page", "rebuild this page from this captured HTML", "high-fidelity Astro recreation" and "faithful port". MODE B means creative design through the existing ACE process. Its trigger phrases include "design a new page", "from the content brief", "make this on-brand from scratch" and "I want a fresh take on X". If ambiguous, ask: "Is the HTML you sent me the authoritative design, or a reference for a redesign?" Authoritative design → MODE A. Reference → MODE B. Do not silently send a strict-fidelity request through the creative process: the Generator may redesign it, and creative review may approve output that fails fidelity checks. Resolve this distinction before choosing the workflow. |
| inherited-from-first-build-multi-agent-rebuild | PROTECTED | **The MODE A rebuild discipline applies to both first builds and maintenance.** Consult `05_automations/client-site-first-build/skillbook.md` for shared strict-fidelity guidance rather than maintaining conflicting copies of the full process. First builds may recreate an entire existing site from captured HTML; maintenance usually adds or replaces a single page or small batch within a deployed site. The mechanics remain the same: a per-page Generator contract, a per-page Reflector contract, a final cross-page review, authoritative HTML taking precedence over conflicting notes, and bounded parallel rounds. Only the deployment target and scope differ. Preserve these requirements when adapting the process to maintenance. |

---

## Curator Log

_Keep a local record of rule changes. Record the lesson and supporting evidence without retaining identifying project details._

| Date | Session | Operation | Details |
|------|---------|-----------|---------|
| Date of change | Local review | ADD / UPDATE / TAG / RETIRE | Record the skill ID, what changed, why it changed and how the rule was checked. |

---

## Brand-swap Strategies

### DESIGN SYSTEM (additions, design-006 through design-014)

| ID | H | Strategy |
|----|---|----------|
| design-006 | Established | **Keep retired token names alive as aliases during a design-system port.** When a new version renames tokens, add one `:root` block that points each retired name at its replacement. For an invented ceramic studio: `--color-surface: var(--color-porcelain); --color-accent: var(--color-cobalt);`. Components that still use the old names keep rendering correctly, so the port can land in one pass and component cleanup can follow later. Check screenshots of every page, not just the CSS. |
| design-007 | Established | **Wordmarks that mix typefaces: align on the baseline and hide the separator from screen readers.** Wrap each part of the wordmark in its own `<span>` inside a parent with `display: inline-flex; align-items: baseline; gap: 0.12em`. Set `font-family`, `color` and `letter-spacing` explicitly on the second span because it otherwise inherits them. Put the decorative separator inside an element with `aria-hidden="true"` and give the link an accessible name, so a screen reader announces the bakery's name rather than "slash slash". Check the header at desktop and phone widths on every page that uses it. |
| design-008 | Established | **Load fonts from one place only.** Use `<link rel="stylesheet">` in the base layout, paired with `<link rel="preconnect">` for an external font origin, and remove any `@import url(...)` for the same fonts from the CSS. A stylesheet link is discoverable early without waiting for the browser to parse an importing stylesheet. Duplicate declarations create redundant loading paths, even when caching prevents duplicate transfers. |
| design-009 | Established | **When a token keeps its name but changes its meaning, sort its uses by intent.** If a name such as `--color-stone` meant "muted body text" in the old version and "dark footer background" in the new one, an alias cannot fix it. Find every use, label it by purpose, such as muted text, border or dark background, and point each group at the right new token. Document the change of meaning beside the token definitions. |
| design-010 | Established | **After moving to a darker accent, re-check every link style.** A darker accent does not automatically provide enough contrast for link text on a light background. For an invented garden-supply shop, test its new leaf-green accent against every surface where links appear. Normal body text needs at least 4.5:1 contrast. A useful pattern is body-colour link text with an accent underline: the readable text meets the text-contrast requirement, while the underline identifies the link without relying on hue alone. Verify hover and focus states too. |
| design-011 | PROTECTED-candidate | **Find the opacity floor for muted text by calculation, never by eye.** Text drawn with opacity blends toward its background, and the resulting colour must maintain at least 4.5:1 contrast for normal body text. Calculate dark-on-light and light-on-dark combinations separately; their minimum passing opacities need not match. Use the WCAG contrast formula for the actual blended colours, add a margin above the passing threshold, and run axe after changes. **This is the canonical path for muted text on dark surfaces**; `design-014` covers muted tokens on light surfaces. |
| design-012 | Established | **Text on a saturated accent button: try true white before an off-white.** An off-white chosen for page surfaces can fail against an accent even when `#FFFFFF` passes. For an invented kitchen-equipment maker, compare both text colours against the actual button background. Keep the surface colour for page and card backgrounds, and use white for button text only if the measured contrast passes. If neither passes, adjust the button background or text colour. Re-check the primary button, the navigation call to action and the cookie banner's accept button. |
| design-013 | Established | **After restyling selectors, run axe for heading order as well as colour.** Class-based styling separates a heading's appearance from its semantic level, so a restyle can leave an `h4` directly under an `h2`, or style a card heading as `h3` when the page outline needs `h2`. Automated checks can reveal issues that visual code review misses. Inspect the page outline, fix the element level, then restyle the class. |
| design-014 | Established | **When a rebrand remaps an alias, give "muted" its own token.** If an old alias such as `--color-secondary-copy` meant muted grey and the rebrand points it at the new dark background token, every use that relied on a quieter text tier silently turns full strength. Contrast checks can still pass because darker text on a light background remains readable, while the visual hierarchy breaks. **Add a dedicated `--color-muted` token during the rebrand and point legacy aliases that mean muted text at it.** For an invented bicycle-parts company, select that colour against its actual light surfaces and verify both contrast and visual hierarchy. One shared token change can then correct all matching uses at once. |
### QA + VERIFICATION (additions, qa-006..007)

| ID | H | Strategy |
|----|---|----------|
| qa-006 | **PROTECTED** | **Empirical Lighthouse + axe gate before SATISFACTORY promotion**. After the ACE iteration completes build, lint, source, and visual-diff checks, run Lighthouse for performance, accessibility, best practices, and SEO, plus axe accessibility scans BEFORE marking SATISFACTORY. Code inspection cannot establish runtime performance or accessibility: check LCP and CLS under simulated mobile throttling, test interaction responsiveness separately, and inspect dynamic-state contrast, touch targets at relevant breakpoints, and heading order. Retain reports and screenshots with the iteration evidence. Without these checks, apparently complete builds can ship accessibility failures and lack regression evidence. |
| qa-007 | Seed | **Playwright with a locally cached Chromium binary as fallback when `@axe-core/cli` has a ChromeDriver mismatch**. Launch with `playwright.chromium.launch({ executablePath: process.env.CHROME_PATH })`, inject axe with `await page.evaluate(axeCore.source)`, then run `await page.evaluate(async () => await axe.run(document))`. A compatible Playwright browser avoids dependence on a mismatched ChromeDriver. Use this as the primary axe execution path for ACE QA. |

---

## CROSS-PROPAGATED FROM COOKIE-CONSENT MAINTENANCE

Cookie-consent maintenance connects directly to production verification. If the site shares consent with a parent site on the same domain (for example a CMS site at the root and this site on a subdomain), check after any DNS change that the consent cookie is still scoped to the shared domain so the banner is not shown twice, that the parent's consent configuration still matches what this site expects, and that privacy-policy links still point at the current policy. On a standalone site, check that the banner (if one ships at all, see port-027) still reads and writes its own cookie correctly. In both cases keep the ACE review and browser-based checks for these changes.

| ID | H | Strategy |
|----|---|----------|
| ace-loop-agent-discipline-001 | Seed [PROTECTED] | **Every maintenance ACE iteration MUST use formal subagents** (`design-generator`, `design-reflector`, `design-curator`). Generator builds → Reflector scores → loop until SATISFACTORY ≥ 9.8/10 → Curator closes. NEVER replace these roles with an inline self-review. Combining generation and evaluation can hide assumptions and make the result difficult to reproduce. The Generator's report must record changes, evidence, and unresolved issues so the Reflector can repeat the checks. Pairs with `ace-001` + `ace-002`. |
| browser-automation-tool-decision-001 | Seed [PROTECTED] | **Browser automation tool decision tree for maintenance QA and production verification.** (1) Headless Playwright via a Node script is the DEFAULT for cookies, network checks, assertions, axe injection, and computed-style measurements. Use `chromium.launch({ executablePath: process.env.CHROME_PATH })`. When testing the human-visible behavior of libraries configured with `hideFromBots: true`, such as vanilla-cookieconsent v3, use `await page.addInitScript(() => Object.defineProperty(navigator, 'webdriver', { get: () => false }))` before navigation and record the override in the evidence. (2) A browser CLI that supports JavaScript evaluation against a deployed URL can handle one-shot checks. (3) Playwright MCP is the LAST CHOICE for this workflow and is reserved for visual inspection, not assertion-driven testing. Include the bot-detection override when needed in cross-subdomain consent tests. |

---

### editorial-canonical-css-global-stylesheet-architecture [PROTECTED]

**Body**: When per-page `htmlStyles` is set to an empty string because a global stylesheet should cover the canonical classes, VERIFY that the global stylesheet covers EVERY canonical class, not just the most recently added subset. A partial migration can leave a kitchen-equipment maker's resource pages with styled cards but unstyled titles, metadata, introductions, summaries, file previews, media embeds, transcripts, source credits, print layouts, responsive rules, and theme variables. Clearing the per-page CSS before migrating those rules removes the styling that the pages still need.

**Architectural fix**: Replace repeated per-page CSS with one complete global ruleset scoped to the templated-page wrapper. Inventory all template classes, migrate their rules, and verify each supported page pattern before clearing its local styles. Follow the scope separation in the next section.

**Generator contract**: `htmlStyles: ""` is correct in a Sanity content patch once the global stylesheet covers the template. Do NOT duplicate canonical class styling in each page. If a NEW canonical class needs styling, ADD it to the shared ruleset under a clearly labeled canonical-template section.

**Reflector contract**: Verify that `htmlStyles` is an empty string for fully migrated templates. If it is non-empty, verify that the rules are page-specific rather than generic canonical styling that belongs in the global stylesheet.

**Forward-applicable to every site**: Define theme variables for the site. One complete, correctly scoped global stylesheet lets all templated editorial pages render consistently with empty per-page `htmlStyles`.

---

### global-css-scope-templated-only-local-handauthored [PROTECTED]

**The architectural rule** (CRITICAL, write once, applies forever):

Two content categories can live inside a resource detail route's shared `.resource-detail` outer wrapper:

| Category | Examples | Styling source |
|---|---|---|
| **TEMPLATED editorial patterns** (generated from a file or external-link source) | bicycle-parts guides, spec sheets, externally hosted customer stories, video embeds, podcast embeds | GLOBAL stylesheet, scoped to `[class*="resource-page-pattern-"]` |
| **HAND-AUTHORED content** (built from scratch without a file or external-link source) | workshop journals, essays, custom pages, topic pages, hand-authored case studies | LOCAL per-page `htmlStyles`, untouched by global template rules |

**The enforcement mechanism**: Scope all global editorial template CSS to `[class*="resource-page-pattern-"]`, a wrapper class present ONLY on templated pages and ABSENT on hand-authored content. This keeps template rules out of hand-authored pages. Keep local page styles scoped to their own page wrapper as well.

**ANTI-PATTERN that this prevents**: Scoping global editorial CSS to `.resource-detail`, the shared outer wrapper. Hand-authored content also lives inside that wrapper, so global template rules can override its design. Fix the regression by rescoping every affected selector to the template-only wrapper, then checking both content categories.

**Generator/reflector contract**:

- When emitting per-page `htmlStyles` for hand-authored content, scope rules to that page's wrapper and omit the `resource-page-pattern-` class family.
- When generating templated editorial pages, emit `htmlStyles: ""` and rely on the global template rules. A wrapper such as `<div class="care-guide-page resource-page-pattern-guide">` MUST be present as the outer element in `htmlBody`.
- The Reflector must verify that global template edits use a wrapper absent from hand-authored pages. Flag REFINE if a template rule could leak into hand-authored content.

**Forward-applicable to every site and automation that writes global CSS**:

- Resource-hub maintenance, including template updates, content changes, and UI operations
- First-site builds, including scaffolding and initial content
- Website maintenance, including production promotion and ongoing content operations

**Reference**: Keep the shared rules in the site's global stylesheet under a clearly commented TEMPLATED EDITORIAL PAGE CANONICAL STYLES block.

---

## Page-Pattern Corrections (Shared Maintenance Rules)

Apply these seven page-pattern corrections to resource detail pages across the site's hub: guides, datasheets, externally hosted customer stories, videos, podcasts, and future patterns. For example, a garden-supply shop's how-to hub should help visitors learn without adding sales panels or unnecessary navigation chrome.

### `no-bottom-cta-box-on-pages-001` [PROTECTED, UNIVERSAL]

Remove the bottom-page CTA section, panel, or banner from every resource detail page. Reason: the page's primary purpose is education. The last visible element in the resource content becomes a "Back to all resources" link.

### `no-breadcrumbs-on-resource-pages-001` [PROTECTED, UNIVERSAL]

Remove the visible breadcrumb trail at the top of every resource detail page. The header starts with H1. Accurate `BreadcrumbList` JSON-LD may remain in the structured data.

### `no-all-caps-metadata-strip-001` [PROTECTED, UNIVERSAL]

Remove the all-caps metadata strip below the page title, including resource type, topic, products, file size, and page count. The hero contains H1 only. Metadata stays in Sanity.

### `no-related-resources-tagline-001` [PROTECTED, UNIVERSAL]

Remove the explanatory subhead beneath the Related resources header. The section contains the header and a grid of 2–4 cards only.

### `related-resources-header-rename-001` [UNIVERSAL]

Change the section header from "Similar resources" to "Related resources" verbatim across every page pattern.

### `no-whats-inside-header-merge-into-descriptor-001` [PROTECTED, UNIVERSAL, guide/datasheet/file-bearing patterns]

Remove the "What's inside" section header on guide and datasheet pages. Merge its content into the top descriptor as bullets. Apply the same rule to future file-bearing patterns.

### `file-preview-before-download-001` [PROTECTED, UNIVERSAL, file-bearing patterns]

On every file-bearing page pattern, the file PREVIEW comes FIRST in the visual flow, with the DOWNLOAD button BELOW it. This applies to guides, datasheets, and future file-bearing patterns. It does not apply to external-source pages that link to a customer story rather than hosting its file.

---

## Universal META-PRINCIPLES (cross-automation skills)

| Skill | Status | Purpose |
|-------|--------|---------|
| `memory-source-file-self-containment-001` | PROTECTED UNIVERSAL | When a memory references a file as its source of truth, include the relevant source content verbatim in the memory body. A path alone is insufficient because the file may move or disappear. Exclude secrets and material that must not be retained. |
| `automation-aggressive-memory-storage-discipline-001` | PROTECTED UNIVERSAL | Store detailed, useful records throughout each run, including current state, decisions, evidence, and candidate workflow improvements. Do not wait until the end, when context may already be lost. |

Both skills apply across first-site builds, resource-hub maintenance, and website maintenance.

---

### gtm-astro-integration-canonical-procedure [PROTECTED]

**The rule**: When the site operator provides Google Tag Manager (GTM) container snippets:

1. **Snippet 1 (script)** → Place it immediately after the opening `<head>` tag in the shared Astro layout, before other scripts and page metadata. Use Astro's `is:inline` directive so Astro does not bundle it.
2. **Snippet 2 (noscript iframe)** → Place it immediately after the opening `<body>` tag as the first body element.

**CSP allowlist**:

- Review `script-src`, `img-src`, `connect-src`, and **`frame-src`** for the supplied GTM integration. Allow `https://www.googletagmanager.com` where required. `frame-src` is easy to miss and is required for the noscript iframe fallback.
- Add any further destinations required by the tags actually enabled in the container.

**Coexistence**: GTM and direct `gtag.js` loaders can share the `window.dataLayer` array. Preserve that array rather than resetting it. For example, a ceramic studio may use GTM for event tracking and a direct GA4 loader for analytics configuration, but must check that both paths do not send duplicate page views or events.

**Anti-patterns**:

- Placing the GTM script late in the head, after other scripts, contrary to its early-loading placement requirement
- Forgetting `is:inline`, which allows Astro processing to alter the supplied snippet
- Forgetting `frame-src` in CSP, which can silently block the noscript iframe
- Placing the noscript snippet later in the body instead of immediately after the opening tag
- Configuring the same analytics event in both GTM and a direct loader without checking for duplicates

**Forward-applicable to every site** using Astro and Vercel CSP headers. The same placement and verification procedure applies to a regional bakery chain's site or any other business site.

---
## Above-the-Fold Media Governance + Collaborative Editing

### media-001: Above-the-Fold Media Governance [PROTECTED, INHERITED from Design Review]
**Rule**: Any element competing for the LCP slot follows one discipline regardless of asset class: image, video, WebGL, WebGPU, or a future format. Apply asset-specific weight budgets, codec and format conventions, and pre-deployment checks.

**Weight Budgets**:
- Images: ≤500KB AVIF/WebP, ≤300KB poster; AVIF first → WebP → JPEG; quality 75-82 content, 85 hero; avoid lossless photographic exports
- Video: ≤20MB for a 1080p hero up to 30s, preferably ≤10MB; h.264 high profile level 4.0 yuv420p, CRF 23 preset slow, faststart movflag REQUIRED, audio stripped
- WebGL canvas + bundled JS: ≤200KB bundle for Three.js scenes, ≤50KB for canvas controllers; opacity 0.5-0.6 for ambient backgrounds; `pointer-events: none` unless interactive
- Future asset classes: review loading behavior and browser support before setting budgets; apply the same rubric

**LCP Discipline**:
- For images that ARE the LCP candidate: `loading="eager" fetchpriority="high" decoding="async"` + explicit width and height. See qa-016 in the client-site-first-build skillbook.
- For video, make the poster the intended initial LCP candidate. Video frames can also qualify, so verify the measured candidate. Use `preload="metadata"` or `preload="none"` to prioritize the poster. For desktop-only video, use a matching source condition such as `<source media="(min-width:768px)">` and verify that mobile displays the poster without downloading the video.

**Master vs Web Export Topology**:
- Master files, including design handoffs and raw codecs such as APV, ProRes, or DNxHD, live in a dedicated folder outside the website repository.
- Web exports live in the site's public asset directory and are committed.
- Re-encoding happens at handoff time using ffmpeg or a PyAV build with the required decoder.
- The PyAV decoding and h.264 export approach is described in media-002 below.

**Pre-Deploy Gate**:
Set `BUILD_OUTPUT` to the generated site's output directory before running these checks.

- `find "$BUILD_OUTPUT" -type f -name '*.mp4' -size +20M` → FAIL unless a reviewed exception is documented
- `find "$BUILD_OUTPUT" -type f \( -name '*.jpg' -o -name '*.jpeg' -o -name '*.png' \) -size +500k` → WARN
- Check WebGL-related JavaScript bundles against the 200KB budget → WARN when exceeded
- Total build output size: warn at 15MB / fail at 25MB per site

**Why**: A large master video and oversized poster can dominate a homepage's transfer cost. Create browser-ready exports and measure the result against a baseline. Smaller files alone do not prove an LCP improvement.

**Tags**: above-fold-media-governance, weight-budget, lcp-discipline, asset-class-future-proof
**Status**: active [PROTECTED]

### collab-001: Collaborative Website Build + Edit + Maintenance Discipline [PROTECTED, INHERITED from Design Review]
**Rule**: Every website may have multiple contributors, including one person working across several assistant sessions. The pre-edit ritual, pre-commit asset check, and branch hygiene prevent overwrites, divergence, and silent regressions.

**Pre-Edit Ritual** (every session, every contributor):
1. `cd` into the site repository.
2. `git fetch origin` to update the configured remote-tracking refs.
3. `git status` to check for existing changes. Preserve them before rebasing or switching branches.
4. `git rev-list --left-right --count origin/preview...preview` to compare the remote and local preview branches.
5. If `origin/preview` is ahead, run `git pull --rebase origin preview` while on the preview branch with a clean working tree.
6. When another contributor is editing, also run `git log origin/preview --since=24hr --oneline` and READ those commits before pushing.

**Branch Hygiene** (enforced through deployment configuration and contributor practice):
- `main` = production-only; update it through the reviewed release process.
- `preview` = shared active development branch for substantive work.
- Never push directly to `main` outside the release process.

**Pre-Commit Asset-Size Gate**:
- Any file >5MB outside designated video, WebGL, or 3D asset directories → HALT for manual review.
- Designated heavy-asset directories remain subject to media-001 budgets.

**Storage Topology**:
- Masters → a dedicated folder outside the repository, retained as the source of truth.
- Web exports → the website repository's public asset directory, committed.
- Document the mapping between each master and its web exports in the site's asset inventory.

**Tags**: collaborative-website-build, pre-edit-ritual, pre-commit-asset-gate, branch-hygiene, master-vs-export-topology
**Status**: active [PROTECTED]

### media-002: pyav APV/ProRes/Future-Codec Decoder Recipe
**Rule**: When ffmpeg returns "unknown codec" or "Decoder not found" for a master video, check whether that build includes the required decoder. A newer PyAV build may provide a compatible libav decoder, but version alone does not guarantee support for a particular codec or variant.

**Recipe**: Verify decoder availability → `av.open(src)` → demux, decode, and reformat to `yuv420p` → `add_stream("libx264")` with `{"crf":"23","preset":"slow","profile":"high"}` → encode and flush the stream. Set `{"movflags":"+faststart"}` on the MP4 output container. Check the resulting duration, playback, pixel format, and file size.

**Tags**: pyav, apv-codec, video-decoder, escape-valve, future-codec-readiness, **Status**: active

### media-003: Lighthouse Control vs Treatment Discipline
**Rule**: Before making a performance-impacting change, such as an asset swap, library upgrade, or layout adjustment, capture a baseline Lighthouse run. Compare control and treatment after the change under matching conditions.

**Pattern**: `npx lighthouse <url> --only-categories=performance --form-factor=mobile --output=json --output-path=./control --chrome-flags="--headless=new"` → make change → re-run with `--output-path=./treatment` → compare the JSON for Performance score, LCP, and total bytes. Repeat measurements when run-to-run variation could explain the difference.

**Why**: A baseline is necessary for an improvement claim. Without one, report only the measured end state. A single before-and-after pair is a preliminary observation, not proof of a consistent gain.

**Tags**: lighthouse-control-treatment, empirical-validation, before-after-discipline, **Status**: active

---

## Curator Log: Above-the-Fold Media Governance Review

Record the trigger, action, and affected skills when a review changes this guidance. Keep project-specific measurements in the relevant site's records.

---

## Cross-References (other automations' skills maintenance work must respect)

### production-hotfix-small-commits-iteration-pattern-001
**Rule**: Post-launch hotfixes follow one fix per commit, with a human reviewer checking each. Don't bundle fixes. Use `Hotfix: <specific change>` commit subjects. Before committing, run `astro check`. After deployment, use `curl -sI` as a response check and verify that the expected release is live. Headers alone do not prove deployment identity or visual correctness. Describe unobserved fixes through their CSS mechanism, such as "X centers Y because Z", and let the reviewer verify the appearance.

**Pattern**: The reviewer sees an issue → describes it, often with a screenshot → the assistant diagnoses and applies a targeted edit → commits with a descriptive message, including "Reviewer flagged:" when appropriate → pushes preview and completes release checks → fast-forwards main through the release process → waits for deployment → the reviewer refreshes live and accepts the fix or flags the next issue.

**When to escape iteration**: If the reviewer says "looks the same" after a non-trivial fix, verify deployment identity, then revisit the diagnosis. After 3+ attempts on the same surface without convergence, pause for a broader design review and obtain a precise description of the remaining problem.

**Why**: Focused commits make each change easier to inspect, attribute, and revert. Human review after each deployment catches mistakes before unrelated fixes obscure their cause.

**Tags**: production-hotfix, iteration-discipline, small-commits, human-vet-loop, post-launch. **Status**: active

### defensive-css-no-rendered-access-pattern-001
**Rule**: When debugging visual issues without rendered access, consider defensive CSS in three layers: (1) a targeted fix based on the inferred CSS issue, (2) defensive containment using relative positioning, cautious overflow handling, or additional padding, and (3) section sizing using min-height or flex centering. Apply and verify each layer separately using `astro check`, response checks, and reviewer feedback. ANTI-PATTERN: stacking defensive guesses in one commit makes it impossible to tell what fixed the issue.

**The trust calibration**: The reviewer's direct observation carries more weight than the assistant's mental model. When they conflict, investigate the observed result. If the reviewer says "looks the same", request a precise description or screenshot. Describe the CSS mechanism without claiming an unobserved visual result.

**Why**: A technically plausible fix can address the wrong layout mechanism. Without rendered access, the person looking at the page supplies evidence that code inspection cannot provide.

**Tags**: defensive-css, visual-debugging, no-render-access, human-trust-calibration, post-launch. **Status**: active

### just-increase-the-height-lesson-001
**Rule**: When content reads as "pushed down", "unbalanced", or "compressed", first test additional container space through padding, min-height, or gap. Try overlap, negative margins, or absolute positioning only when a simple sizing adjustment fails.

**Validation**: On an invented ceramic studio's class overview, a cramped information strip can appear misaligned even when its children are correctly centered. Increasing its available height while retaining symmetric padding addresses the underlying space constraint. Verify the result at each supported viewport.

**The human reviewer's description is useful evidence** about visual balance. When the user says "feels compressed", test an increase in space. When the user says "too much space", test a decrease. Don't reach for negative margins until size adjustment fails.

**Tags**: simpler-is-better, design-lesson, human-intuition, container-sizing, post-launch. **Status**: active

### asymmetric-padding-trap-anti-pattern-001
**Rule**: ANTI-PATTERN: removing padding-bottom to eliminate a visible gap can make content appear pushed upward or otherwise unbalanced. The apparent gap may be symmetric padding providing necessary breathing room.

**Decision rule**: Ask "does the content still look centered without this padding?" If yes, proceed with removal. If no, choose: (a) accept the gap, (b) extend the next section's background to cover it, or (c) use a negative margin on the next section with caution, since overlap may hide space that should remain visible.

**Why**: On an invented regional bakery's location overview, removing lower padding from a store-information strip can disrupt its balance with the next section. Additional offsets may compound the problem. Restoring symmetric padding and adjusting min-height addresses the spacing directly.

**Tags**: css-anti-pattern, padding-symmetry, gap-fix-trap, section-transition, post-launch. **Status**: active

### full-bleed-banner-container-escape-markup-pattern-001
**Rule**: For full-bleed banners inside sections with a max-width `.container`, restructure the markup to pull the banner OUT of `.container`. Add a separate inner wrapper class to constrain text width. Don't reuse `.container` when the layout intent differs.

**Markup pattern**:
```astro
<section class="parent">
 <div class="banner-class"> <!-- OUTSIDE .container, full-bleed -->
 <div class="banner-inner"> <!-- inner wrapper for text max-width -->
 <h2>...</h2>
 </div>
 </div>
 <div class="container"> <!-- other content in normal .container -->
 ...
 </div>
</section>
```

**Why**: An invented kitchen-equipment maker's resource library may need a full-width banner above a constrained guide grid. Separating the banner from the grid container expresses both layout requirements directly and avoids nested-container workarounds.

**Tags**: astro, markup-pattern, full-bleed-banner, container-escape, maintenance-edits. **Status**: active

### text-on-banner-radial-backdrop-pattern-001 [CROSS-REF with first-build guidance]
**Rule**: For text-overlay sections that lack sufficient contrast, add a radial-gradient backdrop to the text element. Fade its edges to improve legibility without a visible rectangular boundary.

**CSS**:
```css
.text-overlay {
 background: radial-gradient(ellipse 110% 100% at center,
 rgba(0, 0, 0, 0.78) 0%,
 rgba(0, 0, 0, 0.52) 55%,
 rgba(0, 0, 0, 0) 95%);
 padding: clamp(24px, 3vw, 40px) clamp(40px, 4vw, 56px);
 border-radius: clamp(20px, 2vw, 24px);
}
```

Use a dark backdrop behind light text or a light backdrop behind dark text. For a light version, use `255, 255, 255` as the RGB channels while preserving the alpha stops. Check contrast against the actual image at supported sizes. The same technique applies during initial builds and maintenance.

**Why**: A solid box can make an editorial banner read as a card. A radial backdrop that reaches zero alpha at its edges supports the text while preserving the image-led composition.

**Tags**: radial-backdrop, css-pattern, text-overlay, banner-readability, first-build-cross-reference, maintenance-edits. **Status**: active

---

## Cross-Reference: resource-page canonicals

Resource-page conventions also apply during **ongoing website maintenance**, especially when editing existing resource layouts or adding interactive behavior to a deployed site. For an invented bicycle-parts company's guides or a garden-supply shop's how-to hub, consult `03_skills/resource-hub-resource-page-builder/SKILL.md` and preserve the established content structure, source grounding, and interaction behavior.
### 1. Pattern S Three-Layer Fidelity Contract (when editing existing self-styled HTML resource pages)

Maintenance edits to a Pattern S page, whose stored HTML owns its layout (a bicycle-parts guide with a TOC, a kitchen-equipment case study with custom chrome, etc.) MUST preserve all three layers:

- **Layer 1, Sanity GROQ projections** include `htmlContent, htmlStyles, htmlSchemas` together. If you add a new GROQ query that touches resource documents, such as a related-content widget, include all three fields in the projection. Silently dropping `htmlStyles` ships a page without its custom styling.
- **Layer 2, Astro resource-detail injection** preserves the `<style data-resource-styles>` AND `<script type="application/ld+json">` injection blocks. Use frontmatter-const hoisting; never nest template literals inside JSX `set:html`, which can trigger esbuild parsing errors.
- **Layer 3, Top-level Astro `<script>`** handles interactive behavior such as scroll-spy, accordions, and modals. Gate initialization on a wrapper-class detector.

**Common maintenance failure mode**: editing the resource-detail template to add a feature, accidentally collapsing the Pattern S injection branch, and shipping a Sanity-controlled page that renders without its styles. The three-layer contract is a checklist for every PR that touches the resource-detail template or its Sanity queries.

**Tags**: pattern4, fidelity-contract, maintenance-edits, layer-1-2-3.

### 2. LIVE Production-Test Gate (Playwright 7-assertion list: must hit live URL post-deploy)

After ANY Vercel deploy from a maintenance edit, the LIVE production-test gate MUST run against the deployed URL, not the self-contained local preview or standalone HTML preview file.

**Use `meta.branchAlias` for the URL** when available: the stable per-branch alias, such as `<project>-git-preview-<team>.vercel.app`, rather than the per-commit URL. Confirm that the alias serves the intended READY deployment before testing.

**7-point Playwright assertion list**:

1. Wrapper class present in DOM, matching the expected Pattern S wrapper.
2. `style[data-resource-styles]` exists with `.textContent.length > 1000`.
3. `script[type="application/ld+json"]` count matches expected.
4. Sample computed style on a signature element matches the design token, such as the expected background gradient on a featured card.
5. Sanity CDN URLs resolved: image `naturalWidth > 0`.
6. Interactive script behavior fires: scroll to a known H2 and verify that the matching TOC link gains `.is-active`.
7. Mobile breakpoint at 375px stacks correctly: hero-figure `order: -1`, sidebar `position: static`.

**Verdict**: any assertion failing means BLOCK ship and diagnose using the live DOM, browser console, network requests, and deployment build logs. For Vercel, use `vercel inspect <deployment-url> --logs`; for Workers, inspect the build logs through `06_web_tools/cf-api`. All seven passing means this verification is complete.

**Why**: a self-contained preview can look polished while the live render has `styleTagCount: 0`. Without live testing, a satisfactory preview can conceal a broken deployment. Maintenance edits are not exempt.

**Tags**: production-test-gate, playwright, live-render, maintenance.

### 3. Astro-Level `<script>` for Any Interactive Behavior (`set:html` doesn't execute embedded scripts)

When adding interactive behavior during maintenance, such as an accordion, scroll-spy, modal, autoplay video, or IntersectionObserver, place the script in a top-level Astro `<script>` block in the resource-detail template, not inside Sanity `htmlContent`.

**Why**: scripts inserted through `innerHTML` do not execute. HTML injected through `set:html` must not depend on embedded scripts running. Behavior may work in a standalone preview, where the browser parses the original document normally, yet remain silently inactive after injection.

**Pattern**: gate the top-level script on a wrapper-class detector so one resource-detail template safely serves all resource types:

```html
<script>
 if (document.querySelector('.resource-page-with-toc')) {
   // Initialize interactive behavior here.
 }
</script>
```

**Tags**: astro-script, set-html-inert, layer-3, interactive-behavior.

---

## Shared Maintenance Lessons: SSR Detail + Production Rebuild + Hide-From-Listing

### S-CH-SSR-A content-batch-prod-rebuild-and-curl-loop-verification [PROTECTED, UNIVERSAL]

**Rule**: Every content batch approved on preview for release MUST reach main, complete a Vercel production rebuild, and pass per-slug curl verification as a mandatory closure step. Without this check, content can appear on preview while returning 404 on production.

1. After preview sign-off, merge the release branch into main and push:
   ```bash
   git checkout main
   git merge --no-ff preview
   git push
   ```
2. Wait for the Vercel production deployment and confirm `state: READY`. Verify that it corresponds to the intended commit.
3. Run a curl loop over every shipped slug, expecting HTTP 200. Investigate every non-200 response.
4. If any page returns 404, halt and triage in order: Sanity publication state, Vercel deployment state, SSR versus SSG routing, then CSP and build diagnostics. Fix, redeploy, and verify again.

**Tags**: deploy, curl-loop, content-batch, maintenance. Status: active.

### S-CH-SSR-B detail-page-404-on-prod-symptom-is-ssr-ssg-mismatch [PROTECTED]

**Rule**: When resource detail pages return 404 on production after a content batch ships, check for an SSR listing paired with SSG detail pages. The listing can discover new content before a static detail route exists.

1. Inspect the resource-detail route for `prerender = true`. Confirm whether the missing slug was absent when the static routes were built.
2. If the hub requires new resources to become reachable without rebuilding every detail route, convert the detail route to SSR. See `05_automations/resource-hub-maintenance/runbook_appendix/ssr_detail_and_hide_from_listing.md`.
3. After deploying the SSR conversion to main, verify that new and existing slugs resolve through live Sanity reads rather than relying on build-time-only routes.

**Tags**: astro, ssr, ssg, diagnosis, maintenance. Status: active.

### S-CH-SSR-C aeo-hide-from-listing-maintenance-toggle [UNIVERSAL]

**Rule**: When an existing resource should be hidden from listings while remaining live and crawler-findable, patch its Sanity document with `hideFromListing: true` through the Sanity mutation API. Keep the detail page reachable at its direct URL, and filter the document out of listing, related-resource, and collection queries. Reverse with `hideFromListing: false`. This flag controls discovery within the site; it does not guarantee search-engine indexing or provide access control.

Typical case: a regional bakery chain retires a seasonal customer story from its current collection while preserving links from earlier newsletters.

**Tags**: sanity, hide-from-listing, maintenance, aeo. Status: active.

### S-CH-SSR-D deploy-local-astro-build-before-push-default [PROTECTED, UNIVERSAL]

**Rule**: Before any `git push` on an Astro site during maintenance, run `npx astro build` locally and require exit code 0. A local build catches syntax and structural failures before the remote deployment cycle, including an accidental literal `</script>` inside a script comment or string. Skipping this check delays feedback and can leave the intended release unavailable.

**Tags**: astro, deploy, local-build, discipline, maintenance. Status: active.

### S-CH-SSR-E publishedonsite-maintenance-time-discipline [PROTECTED, UNIVERSAL]

**Rule**: When maintaining a resource hub that uses `publishedOnSite`, apply four operating disciplines:

1. **Never write a Sanity resource document without explicitly setting `publishedOnSite`**. Missing fields are undefined; the production listing filter `publishedOnSite == true` strictly requires `true`. Content intended for preview defaults to `false`; content explicitly approved for immediate publication uses `true`. Make the choice explicit on every write.

2. **Recognize the alternative pattern (`isPreview` + `PUBLIC_INCLUDE_PREVIEW_RESOURCES`)**. If the hub already uses this pattern, do not add `publishedOnSite` alongside it. Both can implement publication staging; choose one system per hub to avoid conflicting filters.

3. **Backfill before adding the publication filter**. Before deploying a `publishedOnSite` filter to a hub that lacks it, set `publishedOnSite: true` on every existing resource intended to remain public. Classify staged resources explicitly. Deploying the filter before the backfill can temporarily empty the production listing.

4. **Verify branch-aware filter integrity whenever editing Sanity queries**. Search for every use of the publication filter and confirm that every listing query applies it. In this direct-link staging model, detail and series queries omit it. Verify that this remains the intended visibility policy: a listing filter does not make content private.

**Tags**: sanity, publishedonsite, maintenance, integrity-check. Status: active.

## Pre-Launch Checklist Reference

### S-CH-SSR-F launch-checklist-cassian-relevant-sections [PROTECTED]

- **Build and repository hygiene**: every maintenance commit preserves repository hygiene and passes the build.
- **Security headers, CSP, and secret detection**: rerun the security audit after every CSP edit; run secret detection on every commit.
- **Links, navigation, and performance**: run a non-regression sweep and compare Lighthouse results after every change.
- **Core Web Vitals**: check for regressions after layout or asset changes.
- **Observability**: verify error rates and uptime through deployments.
- **Reusable lessons**: record newly discovered failure modes, fixes, and verification steps for future maintenance.

**Tags**: launch-checklist, maintenance, protected, canonical. Status: active.

---
---

## persona-conference-injection-001 [PROTECTED, UNIVERSAL]: package skill consultation

For content-bearing work, include a clause in every generator and reflector prompt requiring consultation of the relevant shipped skills. Choose according to the task: design architecture, graphic design, answer-engine optimization, agent readiness, WebGL, web-app building, or planning. Use the shipped Council instructions when structured review would help resolve a tradeoff. This consultation is optional for changes limited to infrastructure or CSS.

---

### Curator log: in-browser compute, a language runtime inside a static page

Reusable lessons for adding browser-side computation to a static site. Supporting guidance: `05_automations/website-maintenance/runbook_appendix/in_browser_compute_module.md`.

- **`in-browser-compute-001` [ACTIVE]**: a language runtime such as Pyodide, CPython on WebAssembly, can load from a CDN and execute **inside the visitor's browser tab**. A garden-supply shop could offer a planter-volume calculator without a computation backend. The site can retain static hosting on Cloudflare Pages, Vercel, or another CDN. Test the actual hosting environment; local-file behavior can differ. **Architectural ceiling: browser code cannot safely hold secrets or bypass access controls on a private database or API**. Any authenticated service requires a separate access design. Browser execution avoids a server computation charge per run, but hosting and asset-transfer limits still apply.

- **`external-script-data-attr-widget-001` [PROTECTED]**: for interactive widgets whose markup may arrive through Sanity, MDX, or `set:html`, put behavior in a separately loaded script keyed on `data-` attributes. Never rely on inline scripts inside injected markup. As described in the Astro script guidance above, injected scripts do not execute. A host-loaded initializer can discover a `data-compute-widget` element and activate it regardless of where its markup originated. This portability rule applies beyond browser-side computation.

- **`fallback-first-runtime-001` [ACTIVE]**: decide what the page does when the runtime never arrives BEFORE writing the happy path, and make that state useful. For example, a ceramic studio's material estimator can retain a worked example and manual calculation instructions. Use two timeouts: an advisory timeout that reports continued loading, and a hard timeout that ends the wait. Verify four separate states: CDN blocked, JavaScript disabled, WebAssembly unavailable, and connection throttled. The runtime is an enhancement; useful content must survive its absence.

- **`invariant-not-occurrence-001` [ACTIVE]**: the invariant is *“a usable instruction is on screen in every failure state,”* not *“the string appears once.”* Trace each branch before removing duplicate fallback text. With JavaScript enabled but the widget script unavailable, `<noscript>` content remains hidden and no injected fallback can appear. Removing the visible baseline instructions can leave a permanently disabled button. **Count invariants, not occurrences.**

- **`measured-bounds-001` [ACTIVE]**: set widget bounds from the measured artifact, not a convenient round number, and assert that JavaScript and CSS limits agree. A CSS `max-height` can clamp a height set by JavaScript and silently truncate content. Measure initial content, expanded results, narrow layouts, and enlarged text before choosing a limit. Recheck after content changes.

- **`privacy-as-feature-001` [ACTIVE]**: local computation can be a useful product property. A kitchen-equipment maker's planning tool may let visitors calculate from their own inputs without uploading those inputs. Verify the claim through network inspection, including analytics, error reporting, and third-party requests. Describe the observed boundary precisely: *“Calculation inputs are processed in this browser and are not sent by this tool.”* Runtime downloads are still network traffic. For tools handling private business information, keeping inputs local can be a central benefit.

These lessons apply across maintenance work. `external-script-data-attr-widget-001` is protected because it describes a general Astro portability requirement, not a Pyodide-specific detail.
### S-REVIEW-001 three-iteration-graduation-exhaustive-iter1 [PROTECTED, UNIVERSAL] 🔴
**Rule**: Target every ACE loop at THREE iterations (generate → ONE EXHAUSTIVE reflection → one fix round → one verification). The iter-1 reflection must be **exhaustive, not prioritised**: enumerate EVERYTHING between the artifact and the threshold on every dimension, including one-character items; give the literal fix per item; state explicitly whether each is an **ADD** or a **REPLACE** (quote both sides for a replace); separate BLOCKERS from ACCEPTED RESIDUALS with reasons so residuals are closed rather than re-litigated; sanity-check each prescription against its surrounding text; declare out-of-scope dependencies (restricted operations, shared-file changes, decisions only the site owner can make) in round one with evidence. **Why**: a kitchen-equipment maker's product video page can take unnecessary rounds when findings arrive incrementally, one visible defect per review. Each may be correct but should have surfaced in the first reflection. **The mechanism**: a reflection's default audience model optimises for a READER'S ATTENTION (top N findings); an ACE loop's scarce resource is ITERATIONS, so selective reporting works against convergence. **Stop signal for the orchestrator**: a decelerating score curve with shrinking findings means the loop has moved from finding defects to polishing. Demand the complete remaining list in one message or ship with declared residuals once required checks pass. Apply complete reporting to both reflection and final lesson capture, because reflection is where iteration cost accrues. **Status**: active.

### S-REVIEW-002 recover-the-reason-before-applying-a-checklist-edit [UNIVERSAL]
**Rule**: Before applying any prescribed edit to positioning-bearing or claim-bearing copy, recover WHY the item exists. Test: *"what would make this edit wrong?"* If you cannot answer, you have not recovered the reason and must not make the edit yet. A checklist compresses a reason into an action; acting on the action alone closes the item and can break the rule it was protecting. **Why**: a reflector instruction to "name the component once in the section's closing sentence" can be read as MODIFY when it means ADD. In a bicycle-parts guide, swapping a noun phrase might collapse the distinction between a maintenance task and the component used for it, leaving one of them unnamed. **Corollary**: long loops manufacture this posture. In later rounds, the orchestrator can start clearing a queue rather than reasoning about the artifact. That is a CORRECTNESS argument for short loops independent of token cost. **Status**: active.

### S-REVIEW-003: Scoping doctrine has two halves: property AND geometric
**PROTECTED.** Guarding against CSS *property* collisions catches values that lose an override fight, leaving residue a detector can find. **Geometric collisions leave no residue.**
A ported `scroll-margin-top:24px` may be applied exactly as authored yet measured against an
origin that moved when the page gained a 72px fixed header it was never authored for. Whenever
`htmlStyles` is preserved, enumerate every length encoding a distance from a viewport edge and
re-measure against the hub's real header. Verify by measuring the delivered offset of EVERY in-page
jump target: a single centre-point hit-test is scroll-state dependent and can return a confident,
meaningless green. Set the offset from the measured header height plus the intended visible gap.

### S-REVIEW-004: Write the PRINCIPLE, not the mechanism
**PROTECTED.** The preceding scoping rule is needed because property overrides are only one mechanism.
The principle is a context change: this markup now renders in a viewport it was not authored for.
Every check built from a rule that names only one mechanism can inherit its narrowness, even when
written by the same author. When writing doctrine, state the principle and let the mechanism stand
as one example, because the next detector will be built from whichever half got written down.

### S-REVIEW-005: A positive control proves failure on ONE input, not coverage
**PROTECTED.** A check for unintended public content can miss most pages when `str.replace('',' ')`
shreds documents containing an empty `<style>`. Its positive control can still PASS if the probes
happen to land on unaffected pages. Probe EVERY member of the population, assert
`set(injected) − set(found)` is empty, and report the fraction.
Re-derive the control whenever the check changes, and prove the new control catches the old bug.
Add a structural invariant so the silent mode is impossible, not merely detected.

**A second way a green control proves nothing.** Coverage is one failure mode;
**provenance of the planted input is the other**. A control can be invalid in a way its own green result
hides: it plants a term the rule never prohibited, so it could not have triggered that rule.
For example, a garden-supply shop might prohibit the unsupported phrase `"maintenance-free forever"`
in its copy rules. Planting `"easy to maintain"` would not test that prohibition.
The re-derived control must plant the actual prohibited phrase and make the check go RED.
**So: derive every control from the PRIMARY TEXT, never from the brief, checklist or
inherited list that restates it, and prove the control fires before you trust the check it certifies.**
The generalised root is that **a restatement of a rule is not the rule.**
Failing to verify the primary text can produce an over-blocking phrase list, a paragraph defending
wording against a rule that does not exist, or a citation pointing at a file that was never there.
Finding that a green control was vacuous is worth more than adding a new check. Inspect the actual
shipped artifact when assessing appearance, and the primary rule when assessing requirements.

### S-REVIEW-006: Enumerate the population; never guess it with an allowlist
**PROTECTED.** An extension allowlist can omit shipped text files and leave live breaches outside the
checked population. Derive the population from built output, using a null-byte test as an initial
binary filter and explicitly handling any excluded format that can carry public text.
Count leaks AFTER any derivation step: per-route markdown alternates generated from built HTML can
multiply one HTML comment across many files. Apply the same rule to internal references in content:
enumerate every comment and judge each, rather than grepping only for markers you thought of.
Pattern guessing can miss an unfamiliar reference or a path wrapped across a line break.

### S-REVIEW-007: Orchestrator review is not reflection
**PROTECTED.** Running generator rounds and supplying corrections yourself before requesting independent
reflection inverts the three-iteration doctrine and costs more than it saves. The orchestrator wrote
the spec and shares its blind spots. Breaking that correlation is the reflector's entire function.
Repeated self-review can leave blockers intact that the first independent reflection would expose.
Reflect before starting another corrective generation round.

### S-REVIEW-008: `htmlStyles` comments are wire content
**PROTECTED.** `htmlStyles` injects into `<head>`; every `/* comment */` is public. Internal policy labels,
`PROTECTED` markers, private record identifiers, process labels and local filesystem paths can all
reach a live page this way. For comment-only replacements, require comment-stripped CSS to remain
byte-identical and comment counts to remain unchanged. For intentional comment removals, verify
the expected count reduction separately. When Sanity is read at BUILD time, a live-page fix needs
a redeploy to reach the wire.

---

## Cross-Propagated from Resource-Hub Maintenance: shared validation lessons

_Resource-hub maintenance and website maintenance share the same need for trustworthy checks.
The following lessons apply to both. Related guidance is available in
[the resource-hub-maintenance skillbook](../resource-hub-maintenance/skillbook.md).
Asset-ingest mechanics remain with resource-hub maintenance; the lessons here concern validation
that applies across site workflows._

### S-CH-GATE-A gate-assignment-not-just-membership [PROTECTED, UNIVERSAL] 🔴 **PROVISIONAL**
A gate testing set **MEMBERSHIP** ("every number on the page appears in the source") is structurally blind
to wrong **ASSIGNMENT**: two values swapped between two nouns are both still members. Add a **separate**
proximity gate binding each value to *its own* noun; keep the two gates apart so failures stay diagnostic.
Generalises to any attribute-to-entity binding: figure→noun, date→event, product code→product,
spec→model. **Validation example**: a ceramic studio's source lists a mug at 320 ml and a pitcher at
1.4 litres. Swapping those capacities leaves both values present but makes both assignments false.
Require the binding check to reject the swap wherever those products appear.
**Falsifier**: a swap the proximity window cannot separate means the binding needs a parse,
not a window.
**Status**: PROVISIONAL. Promote this entry to validated only after executing the checks.

### S-CH-GATE-B poison-pill-read-level-sweep-and-two-probe-agreement [PROTECTED, UNIVERSAL] **PROVISIONAL**
A **verdict-level** sweep for "does any gate grade its own inputs?" misses a gate that reads a constant
*inconsequentially*. Use a **read-level** probe: replace each content constant with a poison-pill object
whose every operation (`len`, `in`, iteration, indexing, `str`, `eq`, `bool`, attribute access) raises
an exception. It detects the READ, not a flipped verdict.
**Two probes of different strength agreeing is the standard of proof**; one probe's clean result is a
claim about the probe. Each carries its own positive control.
**Validation procedure**: run the verdict sweep across every gate and content constant, then repeat
with the poison-pill probe. Confirm that deliberately introduced reads trigger each probe's control.
Changing specification constants alone does not establish coverage of content-constant reads.
**Falsifier**: a gate reading a constant inside `try/except` may swallow the pill and return a false
clean. Account for swallowed exceptions before accepting the result.
**Status**: PROVISIONAL. Promote this entry to validated only after executing the checks.

### S-CH-GATE-C recalibrate-the-instrument-never-reshape-the-artifact [PROTECTED, UNIVERSAL] 🔴 **PROVISIONAL**
When a **prescribed** check fails on an artifact independently confirmed CORRECT, the finding is about the
**instrument**. Recalibrate it, **declare the deviation in the report**, and keep every control red where
it belongs. Editing correct work to satisfy a mis-specified gate inverts which one is the measurement
and hides the error because the gate then goes green.
**Validation example**: a regional bakery chain's page description condenses several body sentences
about collection options into one sentence. A literal sentence-to-sentence parity check may reject
that faithful summary because no one-to-one alignment exists. Have an independent reviewer reproduce
the failure and assess the summary against the underlying requirement before changing the check.
**Falsifier**: a recalibration that also greens an invalid mutation the gate previously caught is a
weakening, not a calibration.
**Status**: PROVISIONAL. Promote this entry to validated only after executing the checks.

### S-CH-GATE-D encode-the-rule-do-not-resolve-to-follow-it [PROTECTED, UNIVERSAL] 🔴 **PROVISIONAL**
A rule written correctly in **prose** and left unencoded is not a guard. Turn every "I will always…" into
an assertion that **stops the run**: a refusal with non-zero exit, an `assert`, or a gate.
Positive-control it before trusting it. A soft dependency that reports UNRESOLVED and stops nothing
lets the artifact be emitted, gated green and handed on.
**Validation examples**: (1) A rule to omit unsupported fields cannot prevent `Article.image` from
shipping the literal token `PENDING_IMAGE_URL` unless unresolved placeholders trigger a refusal,
such as `exit 2`. Verify that refusal independently. (2) Assert `os.path.exists` for every cited
local path. Run the assertion on the final report too, because a report about dead citations can
introduce new ones.
**Falsifier**: an encoded guard that refuses a correct artifact is enforcing the requirement at the
wrong level. Apply S-CH-GATE-C rather than removing it.
**Status**: PROVISIONAL. Promote this entry to validated only after executing the checks.
### S-CH-GATE-E articleBody-is-an-assertion-not-a-quotation-channel [UNIVERSAL] **PROVISIONAL**
`schema.org` defines `articleBody` as *the body of this article*. Treat anything placed there as published content attributable to the page. Moving an unsupported product claim from visible copy into structured data does not qualify it or remove it from publication.

Apply the same evidence and wording checks to structured data as to visible copy. For example, a kitchen-equipment maker should not remove an unsupported durability claim from a guide while retaining it in the page's structured data. Remove or qualify the claim in both places, check the generated output, and update any derived word count.

**PROVISIONAL because** preferential retrieval from `articleBody` has not been established here. The publication-consistency rule stands on its own; the retrieval hypothesis is a hint to investigate, not a measured result.
**Falsifier**: a controlled retrieval test finding no preference for `articleBody` would refute the retrieval hypothesis, without changing the need for accurate structured data.

---

## Logo bars and hero video swaps

Write the review rubric before changing a logo bar or swapping a page's media, with an ACE acceptance threshold of 9.8 where applicable and no rounding across that threshold. Verify the build independently, preserve the build command's exit status when piping output through a logger, run `astro check`, and inspect the live page in Playwright at 320/360/375/414/768/1024/1440px. Include a desktop screenshot.

Before recording a reusable lesson, reproduce its supporting observations from the artifact. Inspect the logo-bar CSS, the explanation for any media-crop change, and the SVG's painted elements and clipping definitions. A rectangle inside `<defs>` may define a clip without painting a background.

First-occurrence skills enter **PROVISIONAL**. Promotion to VALIDATED requires an independent second occurrence or an executed counterfactual check.

### design-015 monochrome-trust-logo-bar-one-css-rule [DESIGN SYSTEM] **PROVISIONAL**
**Rule**: Render a customer or stockist logo bar in monochrome using a single shared selector for the row's images. For an invented bicycle-parts company's stockist bar, a starting treatment might be `filter:grayscale(1); opacity:.7` at rest and `filter:grayscale(0); opacity:1` on `:hover`, using authentic, transparent, full-colour logo assets. Check permission for this treatment.

Give logos a uniform base height, such as `36px`, with a `.tall` modifier of about `50px` for stacked lockups so their optical weight matches wide wordmarks. Use `grayscale(1)`, **never a black silhouette** produced by `brightness(0)` or a solid fill: silhouettes can destroy internal detail. Guard the hover transition with `@media (prefers-reduced-motion:reduce)` and `transition:none`. Centralizing the treatment makes restoring full colour a small, reversible change.

**Verify** the row by measuring each logo's **vertical centre**, not its `top`. Under `align-items:center`, tall and standard logos have different top coordinates even when they share a row. Compare centres with a small tolerance for subpixel rounding.

**Evidence to collect**: computed filters and opacity, base and tall-logo heights, hover behaviour, the reduced-motion override, screenshots showing retained internal detail, and centre coordinates at desktop widths.
**Falsifier**: solid-fill glyphs may look identical under grayscale and silhouette treatments. Brand guidelines may prohibit desaturation. An opaque raster with a baked background requires a suitable transparent asset; use design-016 or, for an editable vector, design-017.
**Generality**: customer and stockist bars recur across business sites; a shared, reversible treatment avoids per-logo styling drift.
**Validation status**: provisional until independently reproduced or tested against a counterexample.

### design-016 partner-logo-sourcing-order-and-verify-the-bytes [DESIGN SYSTEM] **PROVISIONAL**
**Rule**: To acquire a clean, transparent, full-colour logo for a trust bar, use a fixed source order when no official asset kit is available:

1. **Wikimedia Commons first** where the organization is represented. Resolve a suitably sized PNG through the API's `imageinfo`, using `iiurlwidth` and the returned `thumburl`. Throttle requests with 3–5s pauses and send a descriptive User-Agent.
2. **`unavatar.io/twitter/<handle>?fallback=false`** for a company with a known brand social handle, if the service resolves it.
3. **User-provided direct URLs** for remaining assets.

**Always verify the fetched bytes visually** by opening or rendering the actual file. A plausible URL can return a wrong crop, a placeholder, a boxed variant, or an opaque raster. For a garden-supply shop's partner bar, confirm that every fetched image represents the intended partner and has suitable permission for reuse.

**Evidence to collect**: each image loads with `naturalWidth>0` and `complete:true`, renders correctly in Playwright, and retains the intended mark and transparency. Record its source and reuse terms.
**Falsifier**: an official brand-asset kit removes the need for this search sequence. A source that prohibits redistribution cannot supply a bundled asset without permission.
**Generality**: every logo bar needs verified assets; checking the actual bytes prevents errors that URL inspection misses.
**Validation status**: provisional until independently reproduced.

### design-017 boxed-logo-to-transparent-monochrome-svg-derivation [DESIGN SYSTEM] **PROVISIONAL**
**Rule**: When a logo's clean vector includes a background box, derive a transparent variant only if its usage guidelines permit the adaptation. Inspect the SVG fills: set the painted background `<rect>` fill, and any permitted decorative accent fills, to `none`. Give the wordmark an approved colour suitable for a transparent background. A knocked-out white wordmark may otherwise disappear. Keep the original as a fallback.

**Before deciding a logo has a box, verify which rectangles are painted.** A full-viewBox `<rect>` inside `<defs>` that is referenced only as a `<clipPath>` source through `<use>` defines clipping geometry; it does not paint a background. Do not remove it as though it were a visible box. A rectangle in the render tree with a visible fill is a different case.

**Evidence to collect**: for an invented ceramic studio's partner logo, inspect the original and derived SVGs. Confirm that the painted background is removed, the wordmark remains legible, and clipping definitions still work. Render the result both normally and under `grayscale(1)` to check for unwanted blocks.
**Falsifier**: a background drawn as a `<path>` or supplied through CSS will survive an edit to the wrong rectangle. A raster has no SVG fills to edit. Re-source the logo using design-016, or use a permitted masking treatment.
**Generality**: boxed vectors occur in many asset kits; distinguishing painted shapes from clipping geometry prevents destructive edits.
**Validation status**: provisional until the SVG structure and rendered result have been independently checked.

### media-004 media-swap-reuse-markup-verbatim-but-css-from-the-explicit-list [Above-the-Fold Media cluster: sits with media-001..003] **PROVISIONAL**
**Rule**: When replacing a media element with one already used elsewhere on the site, reuse the shipping element's markup **verbatim** where it is suitable for the new context. For example, a regional bakery chain might replace a contact-page still with its homepage video. Copy the complete `<video autoplay muted loop playsinline preload=… poster=…>` element, its `<source>` elements, and its fallback markup so attributes do not drift.

Take the replacement element's CSS from the specification's **explicit property list**, rather than automatically inheriting the source pattern's crop. If the specification gives `width:100%; height:auto`, those properties govern even when the old still and source hero use a fixed `aspect-ratio` with `object-fit:cover`. A portrait cover crop can hide important parts of a wide video. Preserve its native ratio and use the wrapper's `overflow:hidden` for rounded corners.

**Document the divergence in the source** with a comment explaining why the copied crop was dropped.

**Evidence to collect**: compare the reused markup, verify autoplay/muted/loop/playsInline properties, check poster and source loading, and inspect fallback behaviour. Compare decoded dimensions with the rendered ratio. Confirm that the replacement styles use the intended selector:

```css
.aside-figure video,
.aside-figure img {
  width: 100%;
  height: auto;
  display: block;
}
```

Check that the wrapper preserves the specified rounding without clipping meaningful content.
**Falsifier**: if the specification only says “match the old treatment,” clarify whether its crop is intended. A uniform card grid may explicitly require a fixed crop; native ratio would then violate the layout requirement.
**Generality**: image and video swaps are routine maintenance. Reusing markup while reading CSS requirements separately prevents attribute drift and unintended cropping.
**Validation status**: provisional until independently reproduced.

### design-018 autoplay-looping-hero-video-wcag-2.2.2 [ADVISORY: RULER-CANDIDATE, NOT A DEFECT]
**Rule (advisory)**: An automatically moving `<video>` that continues for more than five seconds alongside other content needs a pause, stop, or hide mechanism under WCAG 2.2.2 unless the movement is essential. A reduced-motion rule that only disables an unrelated hover transition does not address video playback. A short clip that loops continuously can still exceed five seconds of movement.

Treat a gap in reused hero markup as a **shared-pattern issue**. Add an accessible pause or stop control to the shared implementation, respect reduced-motion preferences, and verify every page that uses it. Reduced-motion handling alone does not provide a control for all users.

**Why ADVISORY**: this is a check to add to review rubrics, not a defect recorded on a shipped page. Add automatic-motion checks to review rubrics for any page that reuses autoplay video. A rubric that leaves automatic motion out does not establish accessibility conformance or make an observed accessibility gap disappear.

**Evidence to collect**: inspect the shared video for autoplay and looping, look for usable pause controls, test actual reduced-motion playback behaviour, and identify every page that reuses the implementation.
**Falsifier**: the shared implementation already provides the required control, movement stops within five seconds, or a documented essential-motion exception applies. Muting the video or excluding the criterion from a local rubric does not itself create a WCAG exception.
**Generality (as a ruler candidate)**: autoplay hero video commonly appears in shared components. Include automatic-motion checks in future rubrics and fix shared behaviour at its source.
**Validation status**: advisory for rubric design; assess the rendered behaviour before claiming conformance.

**Curator delta log**: record incremental changes, keep each lesson focused on one concept, and check for semantic duplication against the full skillbook.

- **ADD** design-015: shared monochrome logo treatment and row verification by vertical centre. Keep it distinct from design-007's wordmark typography and tpl-003's logo replacement.
- **ADD** design-016: logo sourcing order and visual verification of fetched bytes.
- **ADD** design-017: permitted transparent SVG derivation and verification of painted fills versus clipping geometry.
- **ADD** media-004: reuse media markup while taking CSS from explicit requirements. Keep it distinct from media-001, media-002, and media-003, which address media weight, codecs, and loading.
- **ATOMICITY SPLIT**: separate logo rendering from asset acquisition. They have different procedures and failure modes.
- **ADD (advisory)** design-018: automatic-motion accessibility in shared hero components. Propose an explicit automatic-motion criterion for review rubrics.
- **REINFORCE** positive-control discipline: before trusting a zero-match search, demonstrate that the search finds a known matching input. Before trusting an overflow detector, introduce a temporary oversized element, confirm detection, remove it, and confirm the baseline returns. A positive control proves detection for that input, not complete coverage.
- **CONSIDERED, HELD (no ADD)**: an earlier fix that is still intact, such as a `minmax(0,1fr)` grid column, is verification evidence, not automatically a new lesson. Record a new lesson only when independent evidence adds something reusable.
- **DEDUP decisions**: retain separate lessons for wordmark typography and monochrome logo treatment, media loading and swap-CSS interpretation, and single-element replacement and whole-page recreation.
- **Bloat check**: review overlapping entries and family size before adding more skills. Preserve well-supported lessons and avoid turning repeated verification into duplicate rules.

---
## Cloudflare Workers deployments: preview and main

**Scope**: preview and production deployments for a site's Cloudflare Worker. Procedure context: `05_automations/website-maintenance/comprehensive_guide.md` and `05_automations/website-maintenance/runbook_appendix/cloudflare_maintenance_ops.md`. The IDs continue the cf- series.

### cf-008 one-preview-mechanism-per-worker-dashboard-and-api [PROTECTED]
**Preferred mechanism**: Use Worker Previews with Previews Base enabled, `npx wrangler preview`, and a `previews` block containing preview-only variables, D1 bindings, rate limits and observability settings. Set base-config secrets before creating a Preview. Do not add a custom preview trigger alongside this mechanism. Disabling Preview Builds can delete existing preview builds, so inspect the consequences before changing that setting.

**Rule**: Configure exactly ONE preview mechanism per Worker: (A) a version preview alias trigger using `wrangler versions upload --preview-alias <branch>` with "Enable Preview Builds" OFF, or (B) Worker Previews with that setting ON and a preview-safe `previews` block. Verify each pipeline using a view that actually covers it. For Worker Previews, poll the preview URL for a marker absent from the previous build; the builds listing may not expose those builds. For main, watch the build by UUID. Inspect the dashboard's branch and Preview views when reconciling status. When views disagree, identify which pipeline each failed build belongs to before fixing anything. Never add a `previews` block merely to silence an error on a version-alias setup.

**Failure mode**: A bicycle-parts company's guide site can have a successful version-alias trigger and a failing Worker Previews pipeline on the same push. If the API watcher sees only the successful pipeline, it reports green while the dashboard reports red. A missing `previews` block is a configuration problem in the second pipeline, not evidence that the first failed.

**Falsifier**: If Cloudflare exposes the relevant setting and all Worker Previews builds through the API, an API check can replace the dashboard inspection. The one-mechanism rule still stands.

**Generality**: Any platform can acquire a parallel deployment pipeline. A watcher measures only the pipeline it was built to observe.

**Why**: A successful API response cannot establish deployment success for a pipeline that the API does not expose.

### cf-009 clean-clone-pre-push-build-workers [PROTECTED]
**Rule**: Before every push to a Workers Builds branch, clone the committed branch into a temporary directory and run `npm clean-install && npm run build` under `env -i`. Supply only the required executable paths, the selected Node version, `CI=true`, `WORKERS_CI=1`, `WORKERS_CI_BRANCH=<branch>` and `CLOUDFLARE_ACCOUNT_ID`. Read that account value alone from the configured credentials source; do not source an entire credentials file. Push only on exit 0. Use `WORKERS_CI_BRANCH=main` before merging to main so production guards run locally first.

**Verification**: Confirm the build uses committed files, includes expected preview-only components in preview mode, and excludes them in production mode. Record unresolved checks explicitly.

**Falsifier**: A commit that passes the simulation but fails in Workers Builds indicates a mismatch such as a build image, Node version or environment variable. Reconstruct the simulation from the failing build's log.

**Generality**: A local build asks whether the project builds in the working environment. A clean-clone simulation asks whether committed code builds under the builder's conditions. Both checks remain useful.

**Why**: Uncommitted files, cached dependencies and inherited environment variables can conceal deployment failures.

**Maintenance notes**:
- Keep cf-008 and cf-009 as separate rules: one checks pipeline visibility, the other checks build reproducibility.
- Keep platform selection distinct from preview-pipeline configuration.
- Ensure platform detection explicitly recognizes Workers-hosted sites instead of routing them through Pages or Vercel instructions.
- Keep the deployment guide and platform-specific procedures consistent when mechanisms change.

---

## Workers build cross-propagation: PRIMARY for Workers sites

**Scope**: reusable maintenance rules for sites using Cloudflare Workers and GitHub. IDs remain stable for cross-references; the `wm-` prefix distinguishes maintenance rules. PROVISIONAL entries require validation in the target environment. CHECK REQUIRED entries also need local evidence before being treated as validated. Procedure context: `05_automations/website-maintenance/comprehensive_guide.md` and `05_automations/website-maintenance/runbook_appendix/cloudflare_maintenance_ops.md`.

### CLOUDFLARE WORKERS (continues cf-001 to cf-009)

| ID | H | Strategy |
|----|---|----------|
| cf-010 | CHECK REQUIRED | **Worker Previews: secrets at creation, recreate stale Previews.** Set secrets in the Preview base configuration BEFORE any Preview exists; they are copied at creation and then persist. A per-Preview `secret put/bulk` can last only one deployment. Recreate a stale Preview from the corrected base configuration instead of repeatedly patching it. Check the exact Preview name before the self-confirming `wrangler preview delete`; migrate preview D1 through a temporary configuration. |
| cf-011 | PROVISIONAL | **Probe an Access-protected host without printing its session cookie.** Use `curl -s -o /dev/null -D <0600 temp file>`, select only named headers, never print `set-cookie`, never combine `-I` with `-o`, and delete the temporary file in a cleanup block that runs even on failure. |
| wm-cf-branch-inherits-main-001 | PROVISIONAL | **A branch cut from main inherits main's Wrangler configuration.** If its preview build fails because a `previews` block is missing, copy only the reviewed preview block, byte for byte. Do not carry unrelated preview-only settings; a cron whose handler exists only on preview can break production. Document intentionally omitted settings. |
| wm-cf-host-class-headers-001 | PROVISIONAL | **Header verifiers must know the host class.** Where Cloudflare's shared-domain Worker previews force the platform's `X-Robots-Tag: noindex`, accept a valid noindex directive there and assert the intended exact value on production. Never weaken production checks to pass a preview. For a Workers setup using header-only indexing controls, keep robots.txt crawlable so crawlers can see the header. Do not import a Vercel-specific combination of indexing checks without checking how the Workers host behaves. |

### DEPLOYMENT (continues deploy-001 to deploy-006)

| ID | H | Strategy |
|----|---|----------|
| deploy-007 | PROVISIONAL | **Judge a deploy by its product.** Done means a probe path returns 200 with a marker unique to the new build AND the deployment associated with the pushed commit lists every required binding by name. Every completion report names its deployment ID. |
| deploy-008 | PROVISIONAL | **Test a deploy guard where failure cannot ship.** Evaluate its condition, use a temporary directory with a fake trigger, or use a shim that refuses deployment. Never test guard failure by attempting a real deployment from the real repository. |
| wm-deploy-marker-absent-before-001 | PROVISIONAL | **A deployment watcher's marker must be absent from the previous build.** Require a negative check before deployment and a positive check afterward. A marker already present cannot prove that the new deployment arrived. |
| wm-deploy-watch-by-uuid-001 | PROVISIONAL | **Watch a build by its UUID, never solely by commit.** A commit-keyed watcher can select an older failed build of the same commit and miss the retry. |
| wm-deploy-cutover-as-posture-001 | PROVISIONAL | **Apply production settings through the main-branch build and verify both preview and production configurations.** Build-environment guards, such as refusing placeholder keys, catch cutover steps that were documented but never executed. |
| wm-deploy-dated-tool-hold-001 | PROVISIONAL | **Hold deployment-tool releases for at least 7 days.** Record the earliest upgrade date in durable project notes and test both preview and production configurations when upgrading. For dependency changes expected to preserve generated images, use a fresh `npm ci` and a cold build to prove byte-identical image output; investigate differences before accepting them. |
| wm-deploy-review-link-alias-001 | PROVISIONAL | **Give reviewers the stable branch-alias preview URL.** Explain that it follows the branch's latest deployment, while a per-push version URL remains tied to one build. |
| wm-deploy-record-the-deviation-001 | PROVISIONAL | **When sign-off precedes the formal ACE loop or Lighthouse, record what did not run and offer to complete it.** A Lighthouse run without its JSON evidence does not satisfy the recorded check. Do not infer permission to push to main merely because it is called the production branch. |
| wm-deploy-side-change-worktree-001 | PROVISIONAL | **Make a side change in a `git worktree` based on origin/main when another session owns the preview checkout.** Fast-forward only after checking the merge base. |

### FORMS + PRIVACY (continues forms-001 to forms-006)

| ID | H | Strategy |
|----|---|----------|
| forms-007 | PROVISIONAL | **Repeat sign-ups must be indistinguishable from first sign-ups.** Return the same status, body and redirect. Link repeat submissions after the response while ensuring deletion reaches all linked records. Answer records require their parent submission row. |
| forms-008 | PROVISIONAL | **Never log malformed request bodies.** Catch parsing failures, return a 4xx response and log only `e.name`. |
| logging-001 | PROVISIONAL | **Worker code writes error reports only.** Enforce this logging policy with a lint check over the Worker's imports, covering every console spelling. |
| qa-029 | CHECK REQUIRED | **Audit the privacy page as a TRUE / FALSE / UNVERIFIABLE table against the code.** Use one row per data-practice statement and repeat the audit after each relevant change. FALSE blocks release. |
| qa-030 | PROVISIONAL | **Build a guard from the definition of what it refuses.** Plant a failing test case for each spelling, including vendor-specific values, alternate syntax and values requiring whitespace trimming. |

### QA, MEDIA + TOOLING

| ID | H | Strategy |
|----|---|----------|
| qa-031 | CHECK REQUIRED | **For words over imagery, grade p99 AND the brightest pixel under each line.** Render with the text transparent to inspect its background at every supported size and state. A 0.3 relative-luminance ceiling can serve as an additional background check for large white text; still enforce the applicable contrast ratio for the actual text size. Never substitute p95 or mean brightness for local checks. Treat axe's incomplete results as requiring review, not as passes. |
| wm-qa-qr-end-to-end-001 | PROVISIONAL | **Printed and QR-coded URLs:** follow W3 in `05_automations/website-maintenance/runbook_appendix/cloudflare_maintenance_ops.md`. |
| media-007 | CHECK REQUIRED | **Grade scrims using captures with the scrim on and off.** The background under the words must never become lighter, and areas beyond the words should remain untouched. Bound the fill to the text elements. Re-audit compensating layers when the underlying asset is fixed. |
| media-009 | PROVISIONAL | **Size overlay marks on cover-fit artwork in the artwork's displayed units.** Use cover scale = max(W/w, H/h), or hold the box height fixed. Measure in artwork pixels at every supported size and state, excluding differences below raster resolution. Revisit fixed-size overlay rules when changes in cover scaling invalidate them. |
| tooling-004 | CHECK REQUIRED | **Judge sticky and fixed layers from viewport captures at named scroll positions.** Full-page captures cannot overrule those observations. Checks that the environment cannot emulate are reported as "not run". |
| tooling-005 | CHECK REQUIRED | **Start every verification log with the served tree's hash and commit.** Commit, build, run checks, then report. Repeat any check whose logged hash differs from the served tree. |
| wm-tooling-zero-input-fail-001 | PROVISIONAL | **A check that grades fewer inputs than expected FAILS.** A PASS prints the input count. |
| wm-tooling-mutant-in-effect-001 | PROVISIONAL | **A deliberately broken test case counts only when the change is shown to be applied and its intended check explicitly FAILS.** URL fragments are not part of network requests, so `page.route` cannot match requests by fragment. An initialization script must account for whether `documentElement` exists before attaching an observer; otherwise the intended mutation may never happen. |
| wm-tooling-prod-csp-gates-001 | PROVISIONAL | **Run motion and first-frame checks under the production CSP.** Inject the headers generated by the build into the test server. Avoid `fetch(data:)`. Assert that the live layer actually started so a silent static fallback cannot pass. |
| ace-010 | CHECK REQUIRED | **CPU-timed checks are distributions.** Run at least 5 consecutive measurements, apply the threshold to a named statistic and print the spread. Across sessions, compare the ratio to an unchanged control. |
| ace-011 | PROVISIONAL | **Near the measurement floor, decide acceptance using binary checks run by two independent reviewers who cannot see each other's results.** Do not rely on a scalar score that cannot reliably distinguish the remaining differences. |
| perf-002 | PROVISIONAL | **Booting a scroll-started live layer must not create a main-thread task over 50 ms at 4x CPU slowdown.** Split the work into smaller tasks, cap candidate pools first and upload textures in bands. |
| perf-003 | CHECK REQUIRED | **Open a fragment-targeted `<details>` element during parsing.** Use a small inline script authorized by a CSP hash, and test a direct fragment load with a layout-shift observer. |
| wm-release-refresh-sweep-001 | PROVISIONAL | **On a product release, read every clause against each plan tier or delivery option the site describes, and every bullet against its heading.** Review words such as "only", "never" and "fallback", plus closed lists, wherever instructions are reused across contexts. |

**Maintenance review notes**:
- Keep the deployment, privacy, rendering and tooling rules distinct where they address different failure modes.
- For cf-007 (client-site-first-build skillbook), check exact allowed values and reject every applicable vendor test value after trimming whitespace.
- For cf-008, document the selected preview mechanism and its evidence source: a preview URL marker for Worker Previews, and a build UUID for main.
- For aeo-012, distinguish unexpected failures from deliberately failing checks whose reasons are recorded.
- Retire score-prediction guidance that turns a reviewer's score into a target. Preserve observable acceptance criteria instead.
- When a rule's falsifier is met, document the replacement and retain enough explanation to show why the earlier rule no longer applies.
- Scan for duplicate IDs after additions. Do not claim to update entries that are absent from the book.
- Before consolidation, collect evidence of which rules help or cause confusion. Merge on evidence rather than on entry count alone.
