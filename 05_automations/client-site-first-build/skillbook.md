# Site First Build: Skillbook

> **Persona**: Dr. Merry Backus: first-time-build specialist

> **Generic edition.** This skillbook is for people building their own sites on their own accounts: their own GitHub repository, Cloudflare or Vercel account, `main` as production, and `preview` or another branch for preview deployments. Examples use invented businesses: a kitchen-equipment maker, a bicycle-parts company, a garden-supply shop, a ceramic studio, and a regional bakery chain. Skill IDs and statuses support cross-references. Look up strategies by skill ID or descriptive phrase in this skillbook. Package tools are documented in `06_web_tools/README.md`. Deployment guidance is in `09_guides/GITHUB_SETUP.md`, `09_guides/DEPLOY_CLOUDFLARE.md`, and `09_guides/DEPLOY_VERCEL.md`. Verify current platform limits and prices before relying on them.

This skillbook is a self-improving strategy collection. Every build run appends a curator log entry describing what was learned. Strategies are tagged with `[PROTECTED]` (H ≥ 5, Harm = 0) or with H-counts. Here, H records helpful applications and Harm records harmful applications. ACE review loops contribute evidence for strategy updates.

---

## How to Use This Skillbook

1. **At startup**: read this file after loading the build persona and retrieving relevant strategies.
2. **During the ACE loop**: consult strategies when the Generator faces a decision, such as which pattern or library to use.
3. **At each Curator cycle**: add, update, protect, or retire strategies based on what the Reflector flagged.
4. **At post-run review**: add a curator log entry summarizing what was learned this session.

---

## Inherited Skills (from resource-hub maintenance)

These resource-hub strategies apply to any RESOURCE_HUB_ONLY or COMBINED build. WEBSITE_ONLY mode skips most of them.

### Setup Skills (inherited)

#### setup-001: One Free Sanity Org Per Independent Site [PROTECTED]
Create a separate Sanity organization for each independently managed site. This separates billing, media libraries, and API quotas where those limits apply at the organization or project level. For example, a ceramic studio's resource hub should remain independently manageable if ownership changes. Verify free-plan eligibility and current document, bandwidth, and request allowances before provisioning.
- **Lookup**: setup-001 **Tags**: setup, sanity, ownership, isolation
- **Status**: active [PROTECTED]

#### setup-002: Polymorphic Schema: Four Types Only [PROTECTED]
For this resource-hub model, use only four document types: resource, taxonomy, collection, and series. Distinguish resource types through taxonomy categories rather than separate schema types. Keep the model under a working budget of 50 attribute paths and verify the platform's current attribute limit. Adding a document type for each content category consumes attribute budget without improving the tagging model.
- **Lookup**: setup-002 **Tags**: setup, schema, attributes, polymorphic
- **Status**: active [PROTECTED]

### Content Skills (inherited)

#### content-002: Blog Asset Compilation [PROTECTED]
When importing a blog series, such as a bakery's how-to articles: (1) Upload each article's hero and inline images to Sanity CDN. (2) Upload each article's MP3 audio file, where supplied. (3) Replace `[AUDIO_URL_PLACEHOLDER]` with its CDN URL. (4) Replace `draft-image-slot` divs with `<img>` tags pointing to the uploaded images. (5) Verify that no placeholder text remains visible before deployment.
- **Lookup**: content-002 **Tags**: content, blogs, images, audio, compilation
- **Status**: active [PROTECTED]

#### content-003: Hybrid Page Strategy
In a hybrid library, only resources with `htmlContent` receive their own Astro page. PDFs link directly to the file, and external resources link directly to their destination. For example, a bicycle-parts library can render its own guides while linking to an external maintenance article. This avoids empty wrapper pages. Use this strategy only when a dedicated indexable detail page is unnecessary; direct links do not provide the same on-site SEO opportunities as substantive detail pages.
- **Lookup**: content-003 **Tags**: content, pages, seo, hybrid
- **Status**: active

#### content-004: WordPress CSV Import Format
WordPress WP All Export CSVs can contain BOM-prefixed UTF-8, pipe-separated taxonomy values, hierarchical product categories, and quoted fields with embedded commas. Your import script must handle all of these. For a garden-supply shop, preserve parent-child category relationships rather than flattening them accidentally. Always run the import in dry-run mode first.
- **Lookup**: content-004 **Tags**: content, import, csv, wordpress

#### content-005: Rate Limiting for Sanity Operations
Use conservative starting limits: a 100ms delay between document creates, a 200ms delay after asset uploads, at most 10 parallel uploads, and at most 100 concurrent mutations. Retry HTTP 429 responses with exponential backoff, such as 2/4/8 seconds, and honor `Retry-After` when supplied. Adjust concurrency to observed responses and current service limits.
- **Lookup**: content-005 **Tags**: content, rate-limiting, sanity

### Collection Skills (inherited)

#### collection-002: Collection Image System
Each collection has two image variants: `featuredImageUrl` (4:3, for topic tile cards on the hub) and `heroImageUrl` (16:9, for a collection page hero with text on the left and an image on the right). Upload via `client.assets.upload('image')`.
- **Lookup**: collection-002 **Tags**: collections, images, featured, hero

### Build Skills (inherited)

#### build-001: Astro Template Customization Points
Review eight customization points per site: (1) Global CSS tokens. (2) Header component. (3) Footer component. (4) Astro configuration. (5) Sanity connection configuration. (6) Base-layout typography. (7) Hub hero text and collection mapping. (8) Taxonomy seed data.
- **Lookup**: build-001 **Tags**: build, template, customization

#### build-003: ACE Loop for Frontend at 9.8/10 [PROTECTED]
Major frontend builds go through an ACE loop: Generator → Reflector → Curator. Repeat until the acceptance criteria pass; do not assume a fixed number of iterations. The Reflector must provide exact file-and-line references with actionable “change X to Y” instructions. Fix flagged issues and document any necessary companion changes. **The production acceptance threshold is 9.8/10, supported by explicit checks and observed results.**
- **Lookup**: build-003 **Tags**: build, ace-loop, frontend
- **Status**: active [PROTECTED]

### Quality Skills (inherited)

#### quality-001: Playwright Self-Review After Every Deploy
Navigate to the live URL. Capture screenshots at 1440px, 768px, and 375px. Check that cards render, filters work, series navigation appears, images load, audio has sources, and no placeholder text remains. Fix issues within the authorized scope before reporting completion.
- **Lookup**: quality-001 **Tags**: quality, playwright, self-review, responsive

#### quality-002: CDN Cache Awareness
After updating Sanity content, CDN responses may still contain stale data. Use `useCdn: false` during development when freshness matters. For production builds immediately after content changes, wait until the update is visible or fetch through a client configured to bypass the CDN. Creating a new client instance alone does not invalidate cached responses.
- **Lookup**: quality-002 **Tags**: quality, cdn, caching, sanity

#### quality-003: Attribute Count Monitoring
After any schema-adjacent change, estimate the attribute count. The polymorphic model should stay under the working budget of 50 paths. Verify usage through available schema statistics. Never solve a tagging problem by adding document types.
- **Lookup**: quality-003 **Tags**: quality, attributes, monitoring, limits

### Accessibility Quality Skills

#### qa-008: AA-Derivative Brand Tokens for Accessibility-Required Surfaces
Preserve the original brand colors. When WCAG AA contrast requires a darker or lighter variant for text or interactive surfaces, add a `*-press`, `*-tint`, or `*-dark` companion token rather than changing the original token. Normal text needs 4.5:1 contrast. Document each companion token's intended use in a CSS comment. The values below are invented for illustration; measure the ratios for your own palette with a contrast checker.

**Pattern:**
```css
:root {
  /* Invented example palette for display contexts (not from any real brand) */
  --accent: #E0A030;       /* about 2.3:1 against white: too low for text */
  --link: #5FA0C8;         /* about 2.9:1 against white: too low for text */

  /* Contrast companions for text and interactive surfaces */
  --accent-press: #8A5A12; /* about 5.9:1 with white text */
  --link-press: #245E80;   /* about 7.0:1 as text on white */
}
.nav-cta {
  color: #FFFFFF;
  background: var(--accent-press);
}
.section-eyebrow {
  color: var(--link-press);
  background: #FFFFFF;
}
```

**Verification rule:** Run a static WCAG luminance check, for example with Python, before building. It catches shades just below AA, such as 4.48:1, before the rendered audit. Then verify actual backgrounds, states, and overlays in the browser.

- **Lookup**: qa-008
- **Tags**: quality, accessibility, wcag, brand-tokens, derivative-tokens
- **Status**: active

#### qa-009: Heading-Order Audit is Whole-Document: Fix Companion Siblings
When axe heading-order flags a skip, such as `h2 → h4`, the fix can require changes beyond the named element. Footer column headings can create the same skip pattern after the main content.

**Rule:** After any heading-order fix, inspect the entire DOM heading sequence in document order. Heading levels should increase by no more than one at a time; returning to a higher-level section can skip back. Check downstream landmarks, including footers, asides, and complementary regions, for residual skips. Match heading levels to the actual section hierarchy. Do this before re-running axe.

**Example:** In a kitchen-equipment resource library, correcting a sidebar heading from `h4` to `h3` can expose a later jump to footer `h5` headings. Review the footer's section hierarchy and assign appropriate levels. Record this companion fix in the generation report so the reviewer can assess the scope expansion.

- **Lookup**: qa-009
- **Tags**: quality, accessibility, heading-order, whole-document, companion-fix
- **Status**: active

---

## Inherited Skills (from website-maintenance: Agent-Readiness Level 5 baseline)

These AEO and agent-readiness strategies apply to every first build: WEBSITE_ONLY, RESOURCE_HUB_ONLY, and COMBINED, regardless of deployment platform. Build agent-readiness support into implementation and verify it during the Reflector pass. “Level 5” is this workbench's internal target, not an external certification.

### aeo-001: 4-schema minimum on every indexable page [PROTECTED]
Review four structured-data types for every indexable page: Organization for the site identity, WebSite, BreadcrumbList, and FAQPage. Include each only where it accurately describes the page and visible content. Do not invent breadcrumbs or FAQs to meet a count. Under this build convention, noindex pages omit these discovery-oriented schemas.
- **Lookup**: aeo-001 **Tags**: aeo, schemas, baselayout
- **Status**: active [PROTECTED]

### aeo-002: SpeakableSchema on ALL content pages
Evaluate speakable structured data on every content page. Where supported and appropriate, identify concise passages that make sense when read aloud. Verify eligibility and markup rather than assuming that adding it guarantees voice-assistant use.
- **Lookup**: aeo-002 **Tags**: aeo, schemas, speakable

### aeo-003: Agent-Readiness Level 5 target on day one [PROTECTED]
Every new site targets the complete agent-readiness baseline from its first release: supported well-known discovery endpoints, an A2A Agent Card where an agent service exists, crawler content signals, discovery Link headers, an LLM-oriented site summary, WebMCP initialization where supported, and real SHA-256 digests for published skill content. Verify that every advertised capability works. Do not publish discovery metadata for services the site does not provide.
- **Lookup**: aeo-003 **Tags**: aeo, agent-readiness, level-5, hard-requirement
- **Status**: active [PROTECTED]

### aeo-005: Real sha256 digests in the agent-skills manifest
Compute SHA-256 digests from the actual published skill content as a pre-build step and insert them into the skill manifest. Never ship placeholder digests. Recompute whenever the corresponding content changes so consumers can verify its integrity.
- **Lookup**: aeo-005 **Tags**: aeo, agent-skills, digests

### aeo-006: Markdown negotiation: BOTH header + URL fallback
Generate a Markdown representation of each supported page at build time and expose it through a discoverable fallback URL. At runtime, handle `Accept: text/markdown` requests through the deployment platform's supported request handler. Configure caches to distinguish negotiated representations. On Cloudflare, use the appropriate Worker or framework adapter; on Vercel, use supported middleware or routing. Providing both negotiated responses and direct URLs lets consumers retrieve Markdown even when they cannot control request headers.
- **Lookup**: aeo-006 **Tags**: aeo, markdown, content-negotiation, platform-aware
### aeo-007: OAuth authorization_servers MUST be live, resolvable URLs [PROTECTED]
Scanner probes each URL. Use the site's real Clerk frontend API URL, such as `https://<your-instance>.clerk.accounts.dev`. Find the configured hostname by searching the app HTML for `clerk.accounts.dev`. Never substitute a hostname that is not DNS-configured.
- **Tags**: aeo, oauth, authorization-server, hard-requirement
- **Status**: active [PROTECTED]

### aeo-008: Deployment header pattern specificity
Specific rules for individual resource types must NOT overlap with catchall rules that set the same headers, or both may apply and duplicate headers. Inspect the hosting platform's header configuration and verify with `curl -I` after deployment.
- **Tags**: aeo, headers, specificity

### aeo-009: OAuth Protected Resource: resource field MUST match serving origin [PROTECTED]
Scanner validates this and rejects "origin mismatch". To describe origin X, publish at X: do not publish at origin Y pointing to X.
- **Tags**: aeo, oauth, origin-match, hard-requirement
- **Status**: active [PROTECTED]

### aeo-010: OAuth decision tree by site type [RETIRED]
The retired decision tree distinguished between (a) a marketing site with no authentication, (b) a Clerk-backed application, (c) an Auth0-backed application, (d) a WooCommerce site using cookie authentication, and (e) a Shopify storefront. Its failure was treating metadata omission and an empty authorization-server list as interchangeable discovery choices.
- **Tags**: aeo, oauth, decision-tree
- **Status**: Invalid (RETIRED; retained to explain the failure mode). Do not implement this as a current decision tree. Determine the site's actual authentication model, then validate the complete discovery chain and metadata against that model. Cookie authentication alone does not establish OAuth support. For configured authorization-server URLs, follow aeo-007 [PROTECTED].

### aeo-011: A2A Agent Card at /.well-known/agent-card.json
Distinct from an MCP Server Card. Required fields: name, version, description, supportedInterfaces[], capabilities{streaming, stateTransferHistory, pushNotifications}, skills[]. Publish BOTH the MCP card AND the A2A card when providing both interfaces: they serve complementary discovery purposes.
- **Tags**: aeo, a2a, agent-card

### aeo-012: Force fresh scans via POST /api/scan [RETIRED]
A scanner may cache results per URL. After production promotion, request a fresh scan through the scanner's supported interface and parse the JSON response for per-check status and evidence. This is not applicable while the first-build environment is access-controlled and the external scanner cannot reach it.

Example command using an illustrative scanner endpoint:
```bash
curl -X POST https://scanner.example/api/scan \
  -H "Content-Type: application/json" \
  -d '{"url":"https://bakery.example"}'
```
- **Tags**: aeo, scanner, force-fresh
- **Status**: Invalid within the first-build workflow (RETIRED; retained to explain scope). Public post-launch scans belong in website maintenance. Use `05_automations/website-maintenance/skillbook.md` for maintenance guidance.

### cf-006: Cloudflare Web Analytics RUM beacon (Cloudflare-only)
For builds using the Cloudflare analytics integration: install the RUM beacon in the shared page layout immediately before `</head>`. It provides cookieless traffic and Core Web Vitals measurement. Keep installation platform-aware: do not copy a deployment-specific integration into a Vercel build without verifying its setup and endpoint behavior.
- **Tags**: cloudflare, analytics, beacon, platform-specific

### cf-007: Public-by-design tokens: gitleaks allowlist
Cloudflare Analytics tokens, GA4 measurement IDs (`G-XXXXXXXXXX`), and Turnstile site keys are PUBLIC by design and appear in browser-delivered HTML. A secret scanner's generic API-key heuristic can flag these high-entropy values. Add verified public values to the gitleaks configuration's allowlist `regexes` array.

**UPDATE: match vendor public and test values by exact value, using the vendor's complete published list.**

- **Allowlist by value, never by path.** A path allowlist prevents gitleaks from detecting a real secret accidentally written into that location. This is especially dangerous for public-key files. Do not assume default rules detect a JWK private component `d`. Add a rule keyed to the JWK structure and prove it fails on a deliberately planted, disposable private-key fixture.
- **A production guard refuses every vendor test value, on the trimmed value.** Build the rejection set from the vendor's complete current list of test credentials, not just the example used during development. A guard based on one familiar value can admit other test keys. Surrounding whitespace can also bypass an anchored pattern. Trim the value, or reject padding, before checking it. The general rule is qa-030.
- **Falsifier**: a public-key file gains a private component and gitleaks stays silent, or a build with any published test key, padded or unpadded, passes the production guard.
- **Validation**: exercise the secret scanner and production guard independently with disposable fixtures. Confirm that public values pass, private-key material fails, and every vendor test credential fails in production configuration.
- **Generality**: any site using a vendor with separate test and production credentials needs this boundary. Guards written from whichever credential is at hand are likely to miss other valid test values.
- **Evidence**: retain reproducible fixture results with the configuration so future changes can be checked against the same failure cases.
- **Tags**: gitleaks, allowlist, public-tokens, turnstile, test-keys, production-guard

---

## NEW First-Build-Specific Skills

### Design Input Skills

#### design-input-001: User-Supplied Design Archive as Canonical Handoff [PROTECTED]
The handoff convention is a user-supplied Claude Design or custom ZIP archive in a designated, gitignored input directory. Discover archives in that directory. If multiple matches exist, ask which to use. If there are no matches, stop and request the archive. Prefer the manual archive handoff over API fetching because a file deliberately supplied by the person is an explicit, reviewable input. Preserve the supplied archive and verify its hash so changes cannot silently alter the build input.
- **Tags**: input, handoff, zip, design-content
- **Status**: active [PROTECTED]

#### design-input-002: Handoff Instructions First → Verifiable Summary Artifact
Before touching any markup or component, read the extracted bundle's introductory documentation and capture its key sections in a written workspace artifact. A spoken recap is not verifiable during the Reflector pass. A written summary lets the Reflector confirm that the Generator parsed handoff inconsistencies, asset references, color tokens, and font references. This catches inconsistencies BEFORE they cost an ACE iteration and leaves an audit trail.
- **Tags**: input, readme, summary-artifact, validation
- **Rationale**: a written summary provides reviewable evidence that the handoff was read and understood.

#### design-input-003: Asset Hash Manifest Before Component Mapping
Run `sha256sum` on every file in the extracted bundle and write a JSON manifest containing relative paths and hashes. Use it to identify identical content, flag repeated filenames in different directories, and record related asset variants. Hashes prove byte identity; identifying resized variants also requires inspecting dimensions or content. The manifest provides an audit trail if anything changes during the build.
- **Tags**: input, manifest, audit

#### design-input-004: Design Token Extraction Before Markup
Enumerate ALL design tokens, including color, font, spacing, radius, and shadow, from the source HTML/CSS into a JSON artifact before writing any Astro component. Translation is where first builds often drift silently. Explicit tokens give implementation and review a shared reference for detecting that drift.
- **Tags**: input, design-tokens, extraction

### Decomposition Skills

#### decomposition-001: Flat HTML → BaseLayout + Hero + Section Pattern
Map the flat HTML document to an Astro component tree: `<BaseLayout>` (head + nav + footer + slots) wrapping `<Hero />` + N `<Section />` children. Each Section accepts a `variant` prop (`default | dark | accent | hub`) so the design system stays in one place.
- **Tags**: decomposition, layout, components

#### decomposition-002: Tailwind v4 Vite Plugin Setup
Use `@tailwindcss/vite` for Tailwind v4 rather than the older `@astrojs/tailwind` integration. Register the plugin in Astro's configuration:

```js
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  vite: {
    plugins: [tailwindcss()],
  },
});
```

- **Tags**: decomposition, tailwind, astro, vite

#### decomposition-003: AEO 4-Schema Mandate Wired in BaseLayout
Evaluate four schema types for every indexable page: Organization, WebSite, BreadcrumbList, and FAQPage. Wire page-specific structured data through `<slot name="head" />` in BaseLayout. Emit each type where it accurately describes the page and its visible content; do not invent breadcrumbs or FAQs to meet a count. Even noindex pages MAY include schemas, but typically skip them when they serve no useful purpose, as with a simple thank-you page.
- **Tags**: decomposition, aeo, schemas, baselayout

#### convention-005: Astro `class:list` Over Ternary `class=` for Falsy-Aware Emission
When a class is conditionally applied based on a falsy value, such as `link.active`, prefer Astro's `class:list` directive over `class={cond ? 'x' : ''}`. The ternary produces an empty class value when false. `class:list` filters falsy entries and expresses conditional class composition directly, making the markup easier to review.

**Pattern:**
```astro
<!-- Avoid an empty-string branch for conditional classes -->
<a href={link.href} class={link.active ? 'active' : ''}>{link.label}</a>

<!-- Prefer falsy-aware class composition -->
<a href={link.href} class:list={[link.active && 'active']}>{link.label}</a>
```

- **Tags**: decomposition, astro, idiom, class-list, html-cleanliness
- **Status**: active

### ACE Loop Skills (build critical path)

#### ace-001: Astro Build Phase MUST Run As ACE Loop @ 9.8/10 HARD [PROTECTED]
The Astro build phase ALWAYS runs through Generator → Reflector → Curator. The SATISFACTORY threshold is 9.8/10 HARD. No rounding. 9.79 = CONTINUE. Plan for 3 iterations as the norm. MAX 5 iterations; STALLED if there is no improvement of at least 0.1 across 2 consecutive iterations.
- **Tags**: ace, threshold, build-phase, mandatory
- **Status**: active [PROTECTED]

#### ace-002: Empirical Lighthouse + axe Scans Required to Clear 9.8+ [PROTECTED]
The Reflector pass MUST run real-browser Lighthouse + axe-core scans before promoting to SATISFACTORY. Subjective code-inspection scoring caps at 9.6-9.7 because source review cannot establish rendered performance or accessibility. Targets: Performance ≥ 90, Accessibility ≥ 95, Best Practices ≥ 95, SEO ≥ 90, and zero Critical/Serious axe violations.
- **Tags**: ace, empirical, lighthouse, axe, quality-gate
- **Status**: active [PROTECTED]
#### ace-003: 9.79 Is Not 9.8: No Rounding
Reflector heuristic: 9.8 HARD means 9.79 = CONTINUE, with no "close enough" interpretation. If a build is marked SATISFACTORY below the threshold, reopen the review. Read the stopping condition as written.
- **Tags**: ace, threshold, discipline

#### ace-004: ACE Workspace at Project Root, Never in Distro
Keep the ACE workspace at the repository root, excluded from version control, NEVER inside the site's deployable source tree. This keeps the website distribution clean and lets you delete temporary review workspaces without touching the build artifact.
- **Tags**: ace, workspace, structure

#### ace-005: Curator Memories Tagged ace-curator
After every Curator cycle, store ALL skillbook skills, both pre-seeded and newly added, as individual entries in your project's persistent knowledge store, tagged `ace-curator`. Use one entry per skill. Store generic patterns only, never private business data. This makes each lesson independently retrievable for later builds.
- **Tags**: ace, curator, memory, propagation

#### tooling-001: Playwright Bundled Chromium for Lighthouse + axe Without System Chrome
Use the Playwright-bundled Chromium binary as `CHROME_PATH` for Lighthouse, and as the launcher for Playwright-injected axe-core scans. This avoids needing a system-wide Chrome installation.

**Discovery + Lighthouse:**
```bash
CHROME_PATH="$(node -e "process.stdout.write(require('playwright').chromium.executablePath())")" \
  npx lighthouse https://example.com --chrome-flags='--headless --no-sandbox --disable-gpu' \
  --output=json
```

**axe via Playwright:**
```bash
node - https://example.com <<'JS'
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(process.argv[2]);
  await page.addScriptTag({ url: 'https://cdn.jsdelivr.net/npm/axe-core@4/axe.min.js' });
  const results = await page.evaluate(async () => await axe.run());
  console.log(JSON.stringify(results, null, 2));
  await browser.close();
})();
JS
```

This pattern addresses the "Lighthouse couldn't connect to Chrome" tooling gap that can prevent a Generator from scanning its own work. Both the Generator's pre-submission self-scan and the Reflector's authoritative review can use the same pattern.
- **Tags**: ace, tooling, lighthouse, axe, playwright
- **Status**: active

#### ace-006: Anti-pattern: Color-Shifting on Reflector Hex Without WCAG Re-Verification (CAUTIONARY)
When the Reflector cites a specific color hex for accessibility, ALWAYS re-verify the WCAG ratio yourself before applying it. Treat specific review findings as actionable, but independently verify numerical values such as color hexes, contrast ratios, and font sizes. The Reflector's first-pass hex may be computed against the wrong rendering background or land just below the threshold.

**Invented example:** A ceramic studio's navigation button uses white text. A suggested background of `rgb(119, 119, 119)` produces approximately 4.48:1 contrast, just below the 4.5:1 AA threshold for normal text. Refining the background to `rgb(102, 102, 102)` produces approximately 5.74:1. Document the refinement in the generation report rather than applying it silently.

**Process:**
1. When the Reflector cites a hex, compute the WCAG ratio against the ACTUAL rendering background. White and tinted backgrounds differ.
2. If the proposed hex produces contrast below 4.5:1 for normal text or 3:1 for large text, darken or lighten it until the ratio is at least 0.4 above the applicable threshold.
3. Document the refinement in the generation report with both hexes and computed ratios.
4. Pair with `qa-008` to create AA-compliant derivative tokens while keeping PROTECTED brand tokens intact.

- **Tags**: ace, anti-pattern, wcag, color-contrast, generator-verification
- **Status**: active (cautionary)

### Cross-Automation Handoff Skills

#### handoff-002: Maintenance Registry Entry on Every Build
After SATISFACTORY ACE close and the first deploy, regardless of mode, append a row to `05_automations/website-maintenance/runbook_appendix/client_registry.md` so the maintenance workflow can discover the site. Include the platform tag (`cloudflare-workers` or `vercel`), preview status, noindex status, and sign-off-required flag. Without this entry, ongoing maintenance lacks a reliable record of the site.
- **Tags**: handoff, maintenance, registry, lifecycle

#### handoff-003: Handoff Notes Per Site
Write a human-readable handoff summary in the repository root documenting what was built, where it lives, what requires approval or restricted access, who was invited, and what must happen before production release. Keep this summary consistent with the resource-hub and website-maintenance registry entries. Without it, the person running the site has no readable record of the completed work.
- **Tags**: handoff, documentation, site-record

### agent-ready-002: Platform-Aware Markdown Negotiation Middleware
For Cloudflare deploys, retain the Markdown negotiation logic in a request handler supported by the chosen Cloudflare deployment mode. For Vercel deploys, port that logic to Vercel middleware. Preserve the same behavior: detect requests accepting `text/markdown` and serve the corresponding route's Markdown representation instead of HTML. See `aeo-006`.
- **Tags**: agent-readiness, markdown, middleware, platform-aware

## Skill Registry

| ID | Section | Status | Added | Source |
|------|---------|--------|-------|--------|
| setup-001 | Setup | active [PROTECTED] | Baseline | Setup guidance |
| setup-002 | Setup | active [PROTECTED] | Baseline | Setup guidance |
| content-002 | Content | active [PROTECTED] | Baseline | Content guidance |
| content-003 | Content | active | Baseline | Content guidance |
| content-004 | Content | active | Baseline | Content guidance |
| content-005 | Content | active | Baseline | Content guidance |
| collection-002 | Collection | active | Baseline | Collection guidance |
| build-001 | Build | active | Baseline | Build guidance |
| build-003 | Build | active [PROTECTED] | Baseline | Build guidance |
| quality-001 | Quality | active | Baseline | Quality guidance |
| quality-002 | Quality | active | Baseline | Quality guidance |
| quality-003 | Quality | active | Baseline | Quality guidance |
| design-input-001 | Design Input | active [PROTECTED] | Baseline | Design input guidance |
| design-input-002 | Design Input | active | Baseline | Design input guidance |
| design-input-003 | Design Input | active | Baseline | Design input guidance |
| design-input-004 | Design Input | active | Baseline | Design input guidance |
| decomposition-001 | Decomposition | active | Baseline | Task decomposition guidance |
| decomposition-002 | Decomposition | active | Baseline | Task decomposition guidance |
| decomposition-003 | Decomposition | active | Baseline | Task decomposition guidance |
| ace-001 | ACE Loop | active [PROTECTED] | Baseline | ACE review discipline |
| ace-002 | ACE Loop | active [PROTECTED] | Baseline | ACE review discipline |
| ace-003 | ACE Loop | active | Baseline | Threshold enforcement |
| ace-004 | ACE Loop | active | Baseline | Workspace isolation |
| ace-005 | ACE Loop | active | Baseline | Curator knowledge retention |
| handoff-002 | Cross-Automation Handoff | active | Baseline | Maintenance registry guidance |
| handoff-003 | Cross-Automation Handoff | active | Baseline | Site handoff documentation |
| aeo-001 | Agent-Readiness | active [PROTECTED] | Baseline | Agent-readiness guidance |
| aeo-002 | Agent-Readiness | active | Baseline | Agent-readiness guidance |
| aeo-003 | Agent-Readiness | active [PROTECTED] | Baseline | Agent-readiness guidance |
| aeo-005 | Agent-Readiness | active | Baseline | Agent-readiness guidance |
| aeo-006 | Agent-Readiness | active | Baseline | Markdown negotiation guidance |
| aeo-007 | Agent-Readiness | active [PROTECTED] | Baseline | Agent-readiness guidance |
| aeo-008 | Agent-Readiness | active | Baseline | Agent-readiness guidance |
| aeo-009 | Agent-Readiness | active [PROTECTED] | Baseline | Agent-readiness guidance |
| aeo-010 | Agent-Readiness | Invalid (RETIRED; do not apply) | Baseline | Agent-readiness review |
| aeo-011 | Agent-Readiness | active | Baseline | Agent-readiness guidance |
| aeo-012 | Agent-Readiness | Invalid (RETIRED from first-build use; belongs in ongoing maintenance) | Baseline | Scope review |
| cf-006 | Platform-Specific Analytics | active (Cloudflare-only) | Baseline | Cloudflare analytics guidance |
| cf-007 | Platform-Specific Analytics | active; trim values and compare against the vendor's complete test-key set | Baseline | Test-key validation guidance |
| agent-ready-002 | Agent-Readiness | active | Baseline | Platform-aware Markdown negotiation |
| qa-010 | Quality (Visual Fidelity) | active [PROTECTED]; a design specification's acceptance probe is a canonical visual reference | Baseline | Visual acceptance guidance |
| qa-012 | Quality / WebGL | active | Baseline | Visual review guidance |
| cookie-consent-existing-wp-bridge-001 | Cookie Consent / Privacy | active [PROTECTED] | Baseline | Existing WordPress consent integration |
| cookie-consent-greenfield-001 | Cookie Consent / Privacy | active | Baseline | New-site consent setup |
| vanilla-cookieconsent-cookie-domain-config-001 | Cookie Consent / Privacy | active | Baseline | Consent cookie domain configuration |
| wp-cookie-notice-bridge-pattern-001 | Cookie Consent / Privacy | active | Baseline | WordPress consent handoff |
| privacy-policy-unified-on-parent-domain-001 | Cookie Consent / Privacy | active [RULE] | Baseline | Shared privacy policy guidance |
| cookieconsent-port-template-001 | Cookie Consent / Privacy | active | Baseline | Consent implementation porting |
| cookie-consent-pre-allowlist-csp-001 | Cookie Consent / Privacy | active | Baseline | Consent and CSP preparation |
| cookie-settings-revisit-link-pattern-001 | Cookie Consent / Privacy | active | Baseline | Reopening consent settings |
| ace-loop-agent-discipline-001 | ACE Loop | active [PROTECTED: recurring failure mode] | Baseline | ACE role discipline |
| browser-automation-tool-decision-001 | ACE Loop / Tooling | active [PROTECTED] | Baseline | Browser automation tool selection |
| cf-008 | Cloudflare Workers Deploy | active [PROTECTED, RULE] | Baseline | Workers Builds guidance |
| cf-009 | Cloudflare Workers Deploy | active [PROTECTED, RULE] | Baseline | Clean-clone CI verification |

---
## Curator Log

| Context | Source | Action | Skill |
|---------|--------|--------|-------|
| Initial setup | Resource-library workflow | ABSORB | Reuse applicable setup, content, collection, build and quality procedures when building a site's resource library. |
| Quality baseline | Build review | PROMOTE TO PROTECTED | ace-001 (9.8/10 HARD), ace-002 (empirical scans), design-input-001 (zip handoff) and build-003. Verify preview indexing restrictions and authentication separately. |
| Analytics setup | Platform review | NOTE | Gate platform-specific analytics configuration by the selected hosting platform. Apply cf-006 where appropriate rather than assuming every host uses the same integration. |
| Design intake | Handoff review | UPDATE | design-input-002: replace a verbal recital with a written, verifiable summary of the design handoff. |
| Build acceptance | Repeated verification | REAFFIRM | Empirical checks, preview indexing restrictions, deployment configuration and build verification remain essential. The HARD acceptance threshold is 9.8/10, without rounding up. |
| Visual review | Fidelity correction | UPDATE | ace-002: empirical review MUST include a canonical-design visual diff when a reference exists, such as rendered HTML, a canonical screenshot or rendered design-tool output. Static checks such as axe, Lighthouse and AEO file presence cannot detect all visual fidelity differences. |
| Visual review | Failure-mode analysis | LESSON LOGGED | A satisfactory score can hide large visual drift from the design handoff. While fixing accessibility findings, a generator may recolour or flatten important surfaces, including buttons, hero backgrounds and tabs, or replace scripted animation with a static fallback. Static checks can still pass. Restore the handoff stylesheet as the visual baseline, then resolve any renewed contrast findings explicitly with the site owner rather than silently repainting the design. |
| Post-fix review | Build evidence | VERIFY | Record a clean build with zero warnings; resource and filter counts read from rendered HTML and compared with the CMS; JSON-LD, noindex metadata and agent-readiness link relations; every required script and its canvas element; an intact `<main>` landmark; required `.well-known` endpoints; and a preview deployment that refuses unauthenticated requests. An unexpectedly empty resource list indicates that the data layer needs investigation. |
| Build acceptance | Visual and interaction review | REAFFIRM PROTECTED | scaffold-004 (JavaScript port mandate), qa-010 (canonical visual diff) and ace-002 (empirical visual verification). |
| Placeholder cleanup | Production-readiness review | NOTE | scaffold-003 remains active. Promote it to protected only after repeated builds demonstrate both useful preview content and reliable removal before public release. |

---

## NEW SKILLS: Preview Content

### scaffold-003: Placeholder Sanity cards on every first build

**Status**: active  
**Tags**: first-build, placeholder-cards, sanity, production-cleanup, scaffold-003

Seed a small, representative set of realistic but fictional resource documents into Sanity on every first build. Match the site's subject matter. For example, a fictional kitchen-equipment maker's preview library might include mixer care guides, storage advice and product spec sheets. Mark each placeholder with `isPlaceholder: true` AND `tags: ["PLACEHOLDER_REMOVE_BEFORE_LAUNCH"]` so either field can identify it during cleanup.

Before disabling noindex, removing preview authentication or attaching the public domain, query `*[_type in ["resource","taxonomy","collection"] && (isPlaceholder == true || "PLACEHOLDER_REMOVE_BEFORE_LAUNCH" in tags)]` and bulk-delete the returned documents.

Workflow: create the taxonomies needed to exercise the filters first, using `createOrReplace` with stable `_id` values, then create the placeholder resources with stable `_id` values. Mark any demonstration-only taxonomies as placeholders too. Submit the mutations together through Sanity's transactional HTTP mutation API. Realistic fictional content matters: NEVER use lorem ipsum. The build should read as a polished demo and expose layout problems that meaningless filler would hide.

Anti-pattern: never let placeholder cards ship to public production.

## NEW SKILLS: Visual Verification

### qa-012: Hero-Canvas Screenshot Diff Has Three.js Animation Timing Variance

**Status**: active  
**Section**: Quality / WebGL  
**Tags**: qa, screenshot-diff, webgl, tolerance

When comparing canonical and build screenshots that include WebGL canvases, the canvas region may capture different animation frames. This is **expected timing variance**, not automatically a code defect. Use **pixel-tolerant comparison**, such as a 5% pixel-diff threshold, for canvas regions. Reserve **strict pixel-equality** for static design surfaces such as CTAs, headings, gradients and layout chrome when the capture environment is controlled.

**Compare on canvas regions:**

- Structural framing: canvas size and position within its parent container
- Background colour tone: the hero's background gradient should remain present mid-animation
- Aspect ratio and DPI scaling

**Do NOT compare on canvas regions:**

- Frame-exact pixel equality
- Specific particle or glyph positions

**Future deterministic-diff option:** add a `window.PAUSE_HERO_FOR_CAPTURE` flag that the animation script honours on its first frame. Set it only during screenshot capture. This is an implementation option, not an existing feature. Use it if animation-related false positives repeatedly obstruct visual review.

## NEW First-Build Skills


### ACE Meta Skills (NEW)

No additional ACE meta skills are defined in this section.

### Convention Skills (NEW)

### convention-006: as-const Readonly Array With Optional Prop Needs Explicit Type [PROTECTED]

**Rule**: Astro/TypeScript can infer `[{a:1},{a:2,b:true}] as const` as a union whose bare-shape entries do not expose the optional property. When a readonly literal array has optional fields, ALWAYS use an explicit type annotation:

```typescript
type NavLink = { label: string; href: string; cta?: boolean };
export const NAV_LINKS: readonly NavLink[] = [
  { label: "Guides", href: "/guides" },
  { label: "Contact", href: "/contact", cta: true },
] as const;
```

Verify `npx astro check` exits 0 before handing off.

### convention-007: Component-Scoped Class Specificity Must Beat Parent Type Selector [PROTECTED]

**Rule**: When a component-scoped class must override a competing ancestor-qualified type selector, such as `.nav-links a`, account for the specificity of the rendered selectors. Patterns:

1. Chain the selector: `.nav-links a.nav-cta` has specificity 0,2,1 versus 0,1,1.
2. Add an attribute selector to the existing class selector, such as `.nav-cta[class~="nav-cta"]`, when an explicit specificity increase is needed.
3. Use `:where()` to reduce the competing selector's specificity, such as `:where(.nav-links) a`.
4. Use `!important` only as a last resort, with a comment explaining why.

**Verification**: ALWAYS use Playwright to inspect `getComputedStyle` on important design surfaces. Never trust source-code declarations alone; see tooling-003.

**Failure mode**: a navigation CTA can declare a larger, heavier font yet retain the ordinary link styling because `.nav-links a` defeats `.nav-cta`. Editing the losing declaration again will not fix the rendered result.

- **Severity**: HIGH

### Quality Skills (NEW)

### qa-010 [UPDATED: fix-priority order made explicit]

**Rule**: When a canonical visual reference exists, compare CSS tokens on important design selectors. Preserve the canonical design while resolving contrast findings. Any unresolved accessibility conflict must be made explicit to the site owner.

**FIX-PRIORITY ORDER (strict)**:

1. Increase font size or weight where appropriate to qualify for the AA large-text contrast requirement of 3:1: at least 14pt bold, approximately 18.67px, or 18pt regular, equivalent to 24px.
2. Increase opacity if transparency causes the contrast problem and the underlying colour must be preserved. Alpha-only adjustments retain the base hue, though they change the composited appearance.
3. RECOLOUR ONLY IF the canonical colour cannot be retained in a suitable accessible treatment AND the user has signed off on the deviation. NEVER recolour silently.

Recording a recolour in a known-gaps list does NOT constitute approval.

### qa-010-fix-pattern: Canonical Remediation Pattern [PROTECTED]

**Rule**: When a design colour fails AA on an important surface, first consider a font-size and font-weight increase that reaches the AA large-text threshold and at least 3:1 contrast. Recolouring is acceptable only with approval and an explicitly documented derived design token, such as `--action-strong` or `--text-on-muted`, with a rationale. An opacity increase is an acceptable middle path when a font increase is unsuitable and the resulting contrast passes. Record the alpha adjustment in the design handoff.

**EXPLICIT PT/PX CONVERSION TABLE**:

- 14pt ≈ 18.67px: AA large-text threshold for bold text
- 18pt = 24px: AA large-text threshold for regular text
- **16px bold, equivalent to 12pt bold, is BELOW the threshold** and needs at least 4.5:1 normal-text contrast
- **18px regular, equivalent to 13.5pt regular, is BELOW the threshold** and needs at least 4.5:1 normal-text contrast
- 19px bold, equivalent to 14.25pt bold, qualifies for the large-text 3:1 requirement
- 24px regular, equivalent to 18pt regular, qualifies for the large-text 3:1 requirement

**POST-BUMP VERIFICATION**: rerun axe-core after the change. Use Playwright `getComputedStyle`, as described in tooling-003, to confirm rendered values rather than source declarations. Reaching the size threshold alone does not prove that the text passes contrast requirements.

### qa-013: Footer-Source-Fidelity-vs-Axe Conflict Resolution

**Rule**: Source HTML may contain low-opacity footer text that matches the visual reference but fails axe-core contrast checks. Preserve the source colour as the starting point, then resolve the conflict along one of two axes: increase alpha until contrast passes, or increase text size to meet the large-text threshold where the layout permits and the resulting contrast is at least 3:1.

Apply the chosen treatment consistently across footer text tiers. Record the adjustment and its measured result in the build report. Keeping the original failing values without remediation does not resolve the conflict.

### AEO Skills (NEW)

### aeo-014 (formerly duplicate id aeo-008 [REMAPPED]): AEO Validation MUST Not Rely on Static Build HTML When output:'server' [PROTECTED]

**Rule**: Server-mode Astro builds using `output: 'server'` do not necessarily emit static HTML for the routes being checked. Scanning only static build output can produce a false green: zero schemas reported because zero HTML files were found. Make the validator either:

1. Parse Astro page source with an AST to check for AEO component imports and invocations.
2. Fetch rendered routes after starting the server and inspect the returned HTML.

Source inspection establishes component wiring; rendered-route checks establish the emitted result. A validator must report missing coverage rather than treating zero checked pages as success.

A false green is worse than an absent check because it conveys safety.

### Tooling Skills (NEW)

### tooling-002: Lighthouse Against Astro Dev Is Not Production

**Rule**: Measurements against `astro dev` include development overhead and local environment effects. With `output: 'server'` and a Vercel adapter, the available local preview behaviour may also differ from the deployed runtime. Do not treat development-server Lighthouse scores as production performance evidence.

**Action**: Classify dev-mode Performance below 90 as provisional, with a tooling-002 caveat. Investigate actionable findings, then measure production performance after deployment through the intended CDN and runtime. Use that deployed result for final performance acceptance.
### tooling-003: Reflector Empirical-Pass Via Playwright getComputedStyle [PROTECTED]

**Rule**: Reflector axe + visual-diff passes MUST use Playwright `getComputedStyle` to read RENDERED CSS values, not parse source `.astro` or `.css` declarations. Source declarations can be defeated by cascade specificity, parent inheritance, or `!important` overrides. Playwright sees the actual rendered output.

**Implementation**: Every assertion about a critical visual property should read the computed value:
```js
expect(await page.locator(sel).evaluate(el => getComputedStyle(el).fontSize)).toBe('20px')
```
Do not substitute a regex check over source.

**Why**: A navigation button can declare the intended font size while a more specific selector overrides it. Contrast checks can also use the wrong foreground or background if they rely on declarations alone. Reading computed styles exposes these failures; source-only inspection can miss them. Use axe and visual inspection alongside these assertions.

- **Severity**: HIGH

---

## Site-Port Migration Skills


### port-001: Backlink Discovery is MANDATORY Before DNS Cutover [PROTECTED]

**Rule**: When migrating an existing site, backlink discovery is MANDATORY. Halt before DNS cutover if the discovery inventory is missing or empty. Do not proceed without a complete redirect manifest covering the discovered URLs and their intended destinations or removal decisions.

- **Tags**: site-port, backlinks, discovery, mandatory, halt-discipline
- **Reference**: `05_automations/client-site-first-build/runbook_appendix/backlink_discovery.md`
- **Status**: active [PROTECTED]

### port-002: Wayback CDX is Cheap First-Cut for Own-URL Inventory

**Rule**: Use the public Wayback CDX API as an early discovery source after checking sitemaps. Endpoint: `https://web.archive.org/cdx/search/cdx?url=DOMAIN&matchType=domain&output=json`. It can reveal orphaned pages, unlisted pages, and historical URLs that sitemaps miss. Respect service limits and record gaps when requests fail or archived coverage is incomplete.

- **Tags**: site-port, wayback, discovery, own-url, public-source
- **Reference**: `05_automations/client-site-first-build/runbook_appendix/backlink_discovery.md`
- **Status**: active

### port-004: Owner-Provided Internal-Link List is Most Reliable

**Rule**: When the site owner can provide a sitemap export, content database export, or server redirect configuration, use it as the primary inventory and cross-check Wayback + GSC against it. A current first-party export is usually the strongest single source for the site's own URLs, but historical and external records can reveal omissions.

- **Tags**: site-port, owner-data, sitemap, source-verification
- **Status**: active

### port-005: Redirect Permanence Defaults to 301

**Rule**: Use 301 permanent redirects by default for permanent migrations. Use 302 only when the redirection itself is temporary. Keeping the old domain available as an archive does not by itself make a redirect temporary. Never chain through deprecated middle URLs (port-013). Direct redirects avoid extra requests and reduce opportunities for broken destinations.

- **Tags**: site-port, redirects, 301, 302, continuity
- **Reference**: `05_automations/client-site-first-build/runbook_appendix/redirect_authoring.md`
- **Status**: active

### port-007: Tier 1 is Default; Tier 2/3 are Opt-In

**Rule**: Tier 1 (sitemaps + Wayback + GSC + Common Crawl) is the default for every site migration. Tier 2 (Bing Webmaster Tools + public GitHub references) and Tier 3 (search-engine queries + manually supplied lists) are optional extensions. Record why an additional tier is needed in the discovery metadata. No combination guarantees complete backlink coverage. Record source limitations and consider paid tools when unresolved gaps justify them.

- **Tags**: site-port, tiers, coverage, opt-in
- **Reference**: `05_automations/client-site-first-build/runbook_appendix/backlink_discovery.md`
- **Status**: active

### port-008: Nameserver Cutover Pause is Non-Negotiable [PROTECTED]

**Rule**: The pause between preview redirect application + curl tests and DNS cutover is a HARD HALT. Present the site owner with the required nameserver instructions. Do not proceed until the owner explicitly confirms that the nameservers are ready AND the Cloudflare API reports the zone as active:

```bash
bash 06_web_tools/cf-api GET '/zones?name=<OLD_DOMAIN>'
```

Check the matching zone in the response for `"status": "active"` and verify the current API response format before relying on an automated check.

- **Tags**: site-port, nameserver, hard-halt, cloudflare
- **Reference**: `05_automations/client-site-first-build/runbook_appendix/dns_cutover_pause.md`
- **Status**: active [PROTECTED]

### port-009: GSC Export Pause is Non-Negotiable [PROTECTED]

**Rule**: At the start of backlink discovery, present GSC TXT verification instructions immediately. Run Wayback + Common Crawl discovery while the owner completes verification, then halt until the owner supplies the GSC backlink export. Allow skipping GSC only through an explicit owner decision with the reason logged in discovery metadata. Record the resulting coverage gap without inventing a percentage.

- **Tags**: site-port, gsc, export-pause, parallel-during-wait
- **Reference**: `05_automations/client-site-first-build/runbook_appendix/gsc_export_pause.md`
- **Status**: active [PROTECTED]

### port-010: Sitemap.xml is the First Check (Cheapest First-Cut for Own-URL Inventory)

**Rule**: Try the site's standard sitemap locations in this order: the main sitemap, sitemap index, WordPress sitemap, and numbered sitemap fallback. Recurse into nested sitemap entries. Do this BEFORE Wayback. A sitemap lists URLs its publisher chose to include; orphaned, hidden, or historical pages may require archived records. Sitemaps answer "what URLs might need redirects FROM"; they do NOT answer "who links to us". Use GSC + Common Crawl referrer data for that.

- **Tags**: site-port, sitemap-xml, own-url, cheapest-first
- **Reference**: `05_automations/client-site-first-build/runbook_appendix/backlink_discovery.md`
- **Status**: active

### port-011: Two-Axis Backlink Discovery [PROTECTED]

**Rule**: Discovery splits into two independent sub-problems:

- **(A) Own-URL inventory** (sitemaps + Wayback + Common Crawl captures of the site): what URLs need redirects FROM
- **(B) Third-party referrer discovery** (GSC + Common Crawl referrer data + optional additional sources): what external sites link to us

Categorization joins both:

- HIGH-priority redirects = URL appears in (A) AND has at least one third-party referrer in (B)
- LOW-priority = URL in (A) only
- EXTERNAL-OUTREACH = referrer in (B) for a URL we never owned. Document it and consider requesting a link correction; do not auto-redirect it.

Different problems need different sources. Join their results during categorization with priority flags.

- **Tags**: site-port, two-axis, discovery, categorization, priority
- **Reference**: `05_automations/client-site-first-build/runbook_appendix/backlink_discovery.md`
- **Status**: active [PROTECTED]

### port-012: WordPress URL-Pattern Auto-Categorization

**Rule**: When the old site is WordPress, auto-classify URLs into known WordPress patterns:

- Dated media-upload URLs → PDF/image assets. Preserve the referenced files on the new site.
- Numeric query-string permalinks → resolve to canonical slugs using the WordPress export or an archived page.
- Category and tag archives → decide whether to redirect to the closest content hub or return 410.
- Feed endpoints → decide whether to keep them, redirect to a replacement feed, or return 410.
- Retired WordPress administration and login endpoints → return 410 on the replacement site.

Apply these rules during URL categorization.

- **Tags**: site-port, wordpress, url-patterns, auto-categorize
- **Reference**: `05_automations/client-site-first-build/runbook_appendix/backlink_discovery.md`
- **Status**: active

### port-013: Chain Old-Site Existing Redirects

**Rule**: WordPress sites can accumulate years of server redirects, such as `old-page → current-page`. Fetching only the current sitemap misses those earlier URLs. During inventory collection, obtain the existing redirect configuration from the site owner or inspect archived redirect responses. Reconstruct the chains, then map each historical URL directly to its new equivalent. For example, an invented bicycle-parts company should send an older wheel-care guide URL straight to the replacement guide, without routing through a retired intermediate page. See port-005.

- **Tags**: site-port, legacy-redirects, server-config, chain-flatten
- **Reference**: `05_automations/client-site-first-build/runbook_appendix/backlink_discovery.md`
- **Status**: active

### port-026: Analytics Default Is Cookieless and Host-Side

**Rule**: A first build defaults to cookieless analytics from the host, such as Cloudflare Web Analytics or Vercel Web Analytics. Verify the actual integration: no additional tracking tags, no cookies, and nothing written to the visitor's browser storage for attribution. Host-provided analytics may still use a browser script, so describe the implementation accurately. Enable additional tag-based or cookie-based tracking only when the site owner requests it, then follow port-027 and update the privacy page under port-028 in the same change. Prefer this default because collecting less data reduces consent complexity, script overhead, and the amount of processing the privacy page must explain.

- **Tags**: site-port, analytics, privacy, cookieless, tracking-posture
- **Reference**: `05_automations/client-site-first-build/comprehensive_guide.md`
- **Status**: active

### port-027: Cookie Banner Only When Something Needs Consent

**Rule**: Ship a consent banner when the site's actual tracking or storage behavior requires consent. Use `cookie-consent-decision-tree-001` in `05_automations/resource-hub-maintenance/skillbook.md`. Check the behavior of embedded services as well as cookies and browser storage; a cookieless label alone does not settle the decision. When a banner ships, nothing requiring consent may load before acceptance, and "reject" must be as easy as "accept". Prefer a configuration that needs no banner (port-026), because a banner guarding nothing adds noise and trains visitors to click through.

- **Tags**: site-port, cookie-consent, privacy, banner
- **Reference**: `cookie-consent-decision-tree-001`
- **Status**: active

### port-028: Every Build With a Form Ships a True Privacy Page

**Rule**: Any site that collects information through forms, newsletter sign-ups, or retained server logs ships a privacy page linked from the footer. Cover: who runs the site and how to reach them; what is collected and through which mechanism; why; where it is stored and for how long; who processes it, including the host and email service; cookies and analytics, or their absence; how to request access or deletion; and the date of the last change. Before publishing, check every statement against the implementation as TRUE, FALSE or UNVERIFIABLE (qa-029). Fix false statements and investigate unverifiable ones. The page must describe what the site actually does.

- **Tags**: site-port, privacy, forms, privacy-page
- **Reference**: `05_automations/client-site-first-build/comprehensive_guide.md`
- **Status**: active

## NEW SKILLS: First-Build Toolchain Lessons

### scaffold-008: Astro 6 output:'server' + Per-Route Prerender Replaces Removed Hybrid Mode

**Status**: active
**Tags**: first-build, build-toolchain, astro-6, hybrid-removed, output-server, prerender, scaffold-008

**Rule**: In Astro 6, use `output: 'server'` for a site that combines request-time rendering and build-time prerendering. Add `export const prerender = true;` to the frontmatter of every page that should be statically generated. Other pages render at request time. The older `output: 'hybrid'` mode is no longer supported. Preserve inline structured data, sitemap coverage, and robots directives when migrating; the output setting alone does not guarantee those outcomes.

**When to apply**: Every first build on Astro 6+ that mixes dynamic and static routes. For an invented kitchen-equipment maker, request-dependent pages can use SSR while product guides and resource collections use prerendering. Choose based on freshness and request-time needs; both modes can serve crawlable HTML.

**How to apply**:

1. Set the Astro configuration to `output: 'server'`. Do not use the removed `'hybrid'` value.
2. For each page that should be statically generated, add to frontmatter:
   ```ts
   export const prerender = true;
   ```
3. Verify the build log lists the intended prerendered URLs.
4. Verify the generated client output contains HTML for each prerendered route, using the output layout produced by the configured adapter.
5. SSR-only routes do not have prerendered HTML files. Verify that the adapter renders them at runtime, for example through Vercel functions or Cloudflare Workers.

**Anti-pattern**: Carrying `output: 'hybrid'` forward from an older configuration into an Astro version that no longer supports it. The build rejects the invalid output mode. Inspect the configuration and page directives after migration rather than assuming an upgrade tool handled them.

**Generic example**: An older configuration using `output: 'hybrid'` + `export const prerender = false;` on dynamic pages becomes `output: 'server'` + `export const prerender = true;` on static pages. The default reverses: static rendering becomes opt-in.

- **Severity**: HIGH (build-blocker if the removed mode remains; correctness-blocker if intended static pages lack prerender directives)
### qa-016: LCP Image MUST Be loading='eager' fetchpriority='high' decoding='async' + Explicit width/height

**Status**: active
**Tags**: first-build, performance, lcp, image-loading, lighthouse, qa-016

**Rule**: The Largest Contentful Paint candidate `<img>` (typically the above-fold hero image) MUST have all four attribute requirements:
- `loading="eager"` (lazy-loading the LCP image delays its load)
- `fetchpriority="high"` (signals high resource priority to the browser)
- `decoding="async"` (allows non-blocking image decode)
- explicit `width="..."` and `height="..."` attributes (reserve space and reduce layout shift as the image loads)

**When to apply**: Every above-fold hero `<img>` on every page. Especially: collection page hero, resource detail hero, homepage hero, product-use page hero. Any large image in the first viewport could be the LCP candidate.

**How to apply**:
```astro
<img
  src={data.heroImageUrl}
  alt={data.title}
  loading="eager"
  fetchpriority="high"
  decoding="async"
  width="800"
  height="500"
/>
```
Pick width/height from the source asset's intrinsic dimensions, or use dimensions that preserve its aspect ratio. Ensure responsive CSS preserves the reserved space.

**Anti-pattern**: Reflexively setting `loading="lazy"` on EVERY `<img>` for "performance hygiene". Lazy-loading the LCP image can cause a Lighthouse LCP regression on both local and deployed builds. Use lazy loading for offscreen images and eager loading for the LCP candidate.

**Verification**: Re-run Lighthouse after the fix and check for LCP < 2.5s (Good). Local measurements can vary with the development environment, so verify against a Vercel preview deployment too.

**Generic example**: A kitchen-equipment maker's resource library uses a large product photograph on collection and detail pages. If the existing static page uses `loading="eager"` correctly, apply the same attributes to the dynamic detail route.

- **Severity**: MEDIUM (performance regression, not a build blocker; can prevent meeting a Lighthouse Performance ≥ 90 target)

## NEW SKILLS: Rendered Contrast Validation

### qa-019: WCAG Ratio Validation MUST Be Empirical, NOT Analytic

**Status**: active
**Tags**: first-build, wcag, accessibility, axe-core, empirical-validation, qa-019, calibration

**Rule**: A contrast calculation for a proposed pair of color tokens does not prove that the page renders that pair. Inheritance, opacity, overlays, and cascade overrides can change the effective foreground or background. Therefore, when picking a NEW color value to clear a contrast threshold, ALWAYS validate the rendered page via Playwright `getComputedStyle` plus WCAG contrast computation, or axe-core with `runOnly: ['color-contrast']`, BEFORE committing the value to source. For flat backgrounds, resolve transparency and layered colors before computing contrast. If the rendered contrast fails the threshold, darken or lighten the relevant color and re-test until it clears the threshold by at least a 0.4 safety margin.

**When to apply**: Every time the Generator, or a Reflector recommending a hex value, selects a new color to clear AA/AAA contrast. Mandatory for:
- New CTA backgrounds with text overlays
- New text-on-light tokens, including eyebrows, section labels, and small body text
- Any darkening or lightening of an existing brand token to derive a separate `*-cta` variant

**How to apply (binary-search-darken pattern)**:
1. Start with the analytic recommendation, such as a proposed darker teal for a bicycle-parts company's guide library.
2. Build and serve the page; launch Playwright headless Chromium with axe-core.
3. Run the axe `color-contrast` rule against the page where the new token renders. Inspect `failureSummary` for the reported contrast and review nodes that require manual checking.
4. If the measured ratio is below the threshold plus a 0.4 safety margin, adjust the relevant channel by approximately 10% in the direction that improves contrast and re-test.
5. Repeat until the measured ratio clears the threshold plus 0.4. This provides headroom for small presentation changes, but does not replace testing after those changes.

**Anti-pattern 1 (the specific failure mode)**: Trusting the Reflector's proposed token pair as proof that the rendered page passes. A recommended color can pass in isolation while an inherited opacity or background override makes the actual CTA fail. Inspect the effective styles, fix the source of the mismatch, adjust the shade if needed, and independently re-measure the rendered result.

**Anti-pattern 2**: Skipping the safety margin and committing a value exactly at the threshold. Small changes to effective colors can push it below the requirement. The 0.4 margin is a working buffer, not a guarantee against future CSS changes.

**Generic example**: A garden-supply shop needs a darker green CTA variant for white button text. Validate it on the actual how-to page, including hover and focus states, rather than relying only on a calculation for the proposed token.

**Pairs with**:
- Generator accessibility checks: run axe before review and use this procedure to fix contrast failures
- Separate CTA color tokens: preserve the decorative brand color while selecting a tested shade for text-bearing controls
- ace-006: independently verify Reflector color recommendations
- tooling-003: extend rendered-style verification from Reflector review to Generator authoring
- qa-031: for text over painted or photographic art, computed styles alone cannot describe the raster background. Measure a text-transparent render and check both p99 over the text box and the brightest pixel under each line, never p95 alone. The flat-background methods here do not replace image-background checks.

- **Severity**: HIGH (silent AA failure if violated; Reflector recommendation alone is insufficient)

## Skill Registry: Accessibility and Consent Additions

| ID | Section | Status | Added | Source |
|------|---------|--------|-------|--------|
| qa-016 | Performance | active | LCP image handling | Image-loading guidance above |
| qa-019 | Accessibility | active | Rendered contrast validation | Contrast procedure above |

---

## NEW SKILLS: Shared Cookie-Consent Lessons


### cookie-consent-existing-wp-bridge-001 [PROTECTED, Scenario A core]

**Status**: active [PROTECTED: shared consent consistency]
**Section**: Cookie Consent / Privacy
**Tags**: cookie-consent, wp-bridge, cross-subdomain, vanilla-cookieconsent

**Rule**: When an Astro subdomain, such as `resources.example.com`, integrates into an existing WordPress site with its own cookie management plugin, the subdomain MUST run a bridge that BOTH reads the WP plugin's consent cookie BEFORE rendering its own banner AND writes back to the WP cookie format AFTER user action. This prevents duplicate banners and inconsistent choices during cross-subdomain navigation. Map consent categories explicitly; do not infer permission for categories the existing cookie does not represent.

**Pattern**: Use a function pair, `bridgeFromWordPress` called before `CookieConsent.run`, and `bridgeToWordPress` called inside the `onFirstConsent`, `onConsent`, and `onChange` callbacks. Both functions return early unless the hostname is the configured parent domain or one of its subdomains. This keeps unrelated preview environments and localhost separate.

- **Tags**: cookie-consent, wp-bridge, cross-subdomain, protected

### cookie-consent-greenfield-001 [Scenario B core]

**Status**: active
**Section**: Cookie Consent / Privacy
**Tags**: cookie-consent, greenfield, vanilla-cookieconsent

**Rule**: When a banner is needed (port-027: only when something on the site needs consent), you control every property end-to-end and no parent-domain CMS plugin manages consent, use vanilla-cookieconsent v3 without bridge functions. Greenfield means: (a) all properties are your own builds; (b) no parent WordPress, Drupal, or Joomla site manages a separate consent cookie; and (c) a shared cookie domain can support cross-subdomain reuse. If even ONE property in the domain family uses an existing CMS consent plugin, use Scenario A and explicitly reconcile its consent model.

- **Tags**: cookie-consent, greenfield

### vanilla-cookieconsent-cookie-domain-config-001

**Status**: active
**Section**: Cookie Consent / Privacy
**Tags**: cookie-consent, cookie-domain, cross-subdomain, vanilla-cookieconsent

**Rule**: For cross-subdomain consent reuse, explicitly set `cookie.domain` to the parent domain, for example `'.example.com'`. Modern browsers ignore the leading dot; what matters is that the cookie has a parent-domain `Domain` attribute. A cookie written without that attribute is host-only and cannot provide shared consent across sibling hosts. Use an `isCrossSubdomainCapable` guard that returns `true` only for the configured parent hostname or its subdomains. Omit the shared-domain setting on localhost and unrelated preview hosts.

- **Tags**: cookie-consent, cookie-domain

### wp-cookie-notice-bridge-pattern-001 [WordPress consent handoff]

**Status**: active
**Section**: Cookie Consent / Privacy (WordPress integration)
**Tags**: cookie-consent, wordpress, cookie-notice-plugin, cross-subdomain, production-handoff

**Rule**: A WordPress Cookie Notice installation may use `cookie_notice_accepted` with values `'true'` for accepted, `'false'` for declined, or no cookie when no choice has been made. Verify the installed plugin's actual values, category model, expiration, and domain behavior before implementing a bridge. A host-only parent cookie is not readable from a resource subdomain.

For shared consent, configure the WordPress cookie writer through a supported plugin setting or integration hook to use the parent domain, path `/`, an appropriate `SameSite` setting, and `Secure` on HTTPS. Keep expiration aligned with the site's chosen consent policy. Remove conflicting host-only cookies when migrating so that duplicate cookie names do not produce ambiguous reads. If the installed plugin cannot support this, select a consent implementation that supports the required domain scope and category mapping.

**First-build implication**: When a ceramic studio adds an Astro resource library to an existing WordPress parent under Scenario A, document the WordPress configuration work for the production handoff. Build the Astro bridge during implementation, apply the matching WordPress configuration during cutover, and test acceptance, rejection, and changed preferences in both navigation directions.

- **Tags**: cookie-consent, wordpress, production-handoff

### privacy-policy-unified-on-parent-domain-001 [RULE]

**Status**: active [RULE: use the parent privacy notice in Scenario A]
**Section**: Cookie Consent / Privacy
**Tags**: cookie-consent, privacy-policy, unified-on-parent, rule

**Rule**: When integrating an Astro subdomain into an existing WordPress or CMS site under Scenario A, use one privacy notice on the parent domain that covers both properties. Link every privacy reference on the Astro subdomain to that parent URL. Do not create a competing privacy page on the resource hub. Reasons: (1) one source for policy updates; (2) less content drift; (3) consistent descriptions of data handling across properties; and (4) less confusion when users compare the hub and parent site. Centralize the URL in a `PARENT_PRIVACY_URL` constant so all references use the same value.

**First-build implication**: During cookie-consent setup for a regional bakery chain's resource hub, if Scenario A is chosen, omit a separate hub privacy page. Set `PARENT_PRIVACY_URL` to the parent's existing notice and confirm that the notice describes the hub's actual data handling.

- **Tags**: cookie-consent, privacy-policy, rule
### cookieconsent-port-template-001 [PORT-SOURCE]

**Status**: active
**Section**: Cookie Consent / Privacy (port-source template)
**Tags**: cookie-consent, template, port-source, vanilla-cookieconsent, brand-tokens

**Rule**: Keep ONE canonical port-source template for vanilla-cookieconsent v3 deployments, taken from a site where the consent implementation passed review. It provides 3 categories (necessary readOnly + analytics + advertising), autoClear regexes for GA4 + GA legacy + Google Ads + LinkedIn cookies, Google Consent Mode v2 wiring (gated on `typeof window.gtag === 'function'`), brand styling via CSS custom properties, equalWeightButtons 3-button bar layout, `data-cc='show-preferencesModal'` wiring, and language strings via `language.translations.en`. To port it to a new site: copy the reviewed template, replace brand tokens, adapt the interface strings and category descriptions to the site's actual services, and verify the result.

**First-build implication**: Use the reviewed consent component as the port source. Do not rebuild it from scratch once you have a version that passed review.

- **Tags**: cookie-consent, template, port-source

### cookie-consent-pre-allowlist-csp-001 [FORWARD-READINESS]

**Status**: active
**Section**: Cookie Consent / Privacy (CSP forward-readiness)
**Tags**: cookie-consent, csp, forward-readiness, analytics, pre-allowlist

**Rule**: When adding a cookie banner to a site with planned analytics integrations, prepare the corresponding CSP allowlists (`script-src` + `connect-src` + `img-src`) at the same time. This avoids a second CSP edit when those integrations are enabled. For planned GA4 / Google Ads / LinkedIn Insight Tag integrations, the starting allowlist is: `script-src` += `googletagmanager.com` + `snap.licdn.com`; `connect-src` += `google-analytics.com` + `*.analytics.google.com` + `*.g.doubleclick.net` + `googleadservices.com` + `px.ads.linkedin.com`; `img-src` += `google-analytics.com` + `googleadservices.com` + `px.ads.linkedin.com`. Verify the actual endpoints used by the chosen integrations. CSP permission does not grant consent or authorize scripts to run before consent.

- **Tags**: cookie-consent, csp, forward-readiness

### cookie-settings-revisit-link-pattern-001 [GDPR Article 7(3)]

**Status**: active
**Section**: Cookie Consent / Privacy (consent withdrawal mechanism)
**Tags**: cookie-consent, footer-link, gdpr-article-7-3, vanilla-cookieconsent

**Rule**: A footer link with `data-cc='show-preferencesModal'` lets the user revisit consent preferences at any time without leaving the page. GDPR Article 7(3) requires withdrawal of consent to be as easy as giving it. This link provides access to the withdrawal controls; verify that withdrawing consent also stops the relevant tracking. Pattern: `<a href="#" data-cc="show-preferencesModal">Cookie Settings</a>` in the footer component. The vanilla-cookieconsent v3 library handles the click through event delegation; no custom click handler is needed.

- **Tags**: cookie-consent, footer-link, gdpr

### ace-loop-agent-discipline-001 [PROTECTED: recurring failure mode]

**Status**: active [PROTECTED: recurring failure mode]
**Section**: ACE Loop
**Tags**: ace-loop, agent-discipline, generator, reflector, curator, protected-recurring-failure

**Rule**: Every ACE iteration MUST use formal subagents following `05_automations/agents/design-generator.md`, `05_automations/agents/design-reflector.md`, and `05_automations/agents/design-curator.md`. Generator builds → Reflector scores → loop until SATISFACTORY ≥ 9.8/10 → Curator closes. NEVER perform these roles inline. NEVER skip the Generator agent. Building an artifact outside the assigned Generator role breaks the review trail even when the artifact appears sound. The Generator's written report is the audit trail; without it, the Reflector cannot reproduce the review against a documented build. Pairs with `ace-001` + `ace-002` + `build-003` (9.8 HARD): the threshold is meaningless without the agent discipline that produces it.

- **Tags**: ace-loop, agent-discipline, protected

### browser-automation-tool-decision-001 [PROTECTED]

**Status**: active [PROTECTED]
**Section**: ACE Loop / Tooling
**Tags**: browser-automation, playwright, headless, navigator-webdriver-override, mcp-decision-tree, protected

**Rule**: Browser automation tool decision tree:
1. **Headless Playwright via Node script**: DEFAULT for programmatic verification (cookies, network, assertions, axe-core injection, computed-style measurement). Use `chromium.launch()` with a Playwright-installed browser. When testing your own site's consent UI, use `addInitScript(() => Object.defineProperty(navigator, 'webdriver', { get: () => false }))` if needed to exercise behavior hidden by `hideFromBots:true` in libraries such as vanilla-cookieconsent v3. Record this test condition so the result is reproducible.
2. **One-shot browser evaluation**: An alternative for a small JavaScript check against a deployed URL. Record the evaluated code and result.
3. **Playwright MCP**: LAST CHOICE in this workflow; use for visual inspection, with scripted assertions providing the repeatable verification.

**Failure mode**: A visual report that the banner renders can disagree with a standard headless test because `hideFromBots:true` silently suppresses the banner under automation. Record the browser configuration and initialization override alongside the assertions. See `05_automations/resource-hub-maintenance/runbook_appendix/playwright_cookie_test_harness.md` for reusable test guidance.

- **Tags**: browser-automation, playwright, protected


---

## Shared Resource Hub UI Defaults (Resource Hub canonical defaults)

Apply these defaults when scaffolding a resource hub or a site that combines business pages with a resource library. Establishing them during the first build keeps card actions and discovery controls consistent.

### cta-articles-less-canonical-001 [PROTECTED: RULE, shared default]
All resource-hub card CTAs MUST be article-LESS (no 'the' / 'a' / 'an'). Pattern: `<verb> <noun>`. Prefer this because short verb-noun CTAs scan easily in a grid and keep phrasing consistent. For a kitchen-equipment maker's resource library, an illustrative `TYPE_CTAS` map is: `guide: 'Read guide'`, `spec-sheet: 'View spec sheet'`, `video: 'Watch video'`, `customer-story: 'Read customer story'`, `datasheet: 'Download datasheet'`. Match the verb to the actual destination or action. The `toCard` fallback string is "View resource", not "View the resource"; a hardcoded featured-card fallback uses "Read guide", not "Read the guide".
- **Tags**: cta-canonical, article-less, rule, reusable
- **Status**: active [PROTECTED: RULE]

### resource-hub-ui-minimalism-bundle-001 [RULE, shared default]
8 atomic minimalism patterns to scaffold from the start. Prefer them because removing redundant labels, counts, and hints lets the cards and search carry discovery, making the page read as a library:
(1) page-header-title-only (short noun H1, no subtitle, no rule, approximately 50% less padding than the expanded header);
(2) featured-section-h2-only (drop eyebrow and curation credit; H2 is the section label);
(3) library-section-no-eyebrow-no-desc ("All Resources" title only);
(4) hero-card-image-only (`.hero-card--image-only` modifier for a spotlight without body text);
(5) hero-meta-removed (no page-count and format summary line);
(6) library-search-no-kbd-hint (no `<kbd>` badge; keyboard binding remains active);
(7) library-no-results-count-no-sort (no resource count or sort control; sidebar and search carry discovery; default sort is `publishedDate` descending);
(8) res-card-meta-no-redundant-type (corner badge handles type; product/topic and year remain).
- **Tags**: ui-minimalism, rule, canonical-pattern, reusable
- **Status**: active [RULE]

## Shared Curator Log Entry

Record reusable UI decisions with their rationale and verification evidence.


---

## GA4 Analytics Configuration Default

Document the intended analytics destinations explicitly so later integration work does not introduce duplicate event delivery.

## Shared Curator Log Entry (GA4)

Record analytics configuration changes with the checks used to verify consent behavior and event delivery.


---

## NEW SKILLS: SATISFACTORY close

Retain reusable lessons from completed reviews without preserving project-specific scores or history.

## Skill Registry: close additions

Record each retained skill's ID, section, status, and supporting evidence.

---

## NEW SKILLS: Self-Heal Pass (Multi-Agent Rebuild Pattern Codification)


### mandatory-final-high-level-reflector: Cross-Page Integration Audit On 8 Dimensions [PROTECTED]

**Status**: active **[PROTECTED]** (per-page reflectors cannot reliably catch cross-file defects)
**Section**: Multi-Agent Build Discipline / Final Verification
**Tags**: high-level-reflector, cross-file-validation, mandatory, PROTECTED

**Rule**: After all per-page reflectors pass, a final high-level design-reflector MUST run an 8-dimension cross-page integration audit. **NEVER SKIP.** The 8 dimensions:

1. **Build health**: `npm run build` completes; no Astro errors; no broken `<Image>` references.
2. **Structural consistency**: shared headers, footers, and other site chrome are consistent across pages.
3. **Navigation coherence**: every navigation link resolves to a real route; no orphan slugs.
4. **CSS regression**: global utility defaults are unchanged; per-page modifiers stay scoped.
5. **Cookie persistence**: consent configuration is structurally valid across pages, and saved preferences survive navigation.
6. **Asset coverage**: every `{{ASSET:filename}}` placeholder is resolved.
7. **Slug fidelity**: generated routes match the approved slug inventory.
8. **Form API integration**: every `formSource` value sent by a form is present in the contact endpoint's `ALLOWED_SOURCES` set.

**Why PROTECTED**:
- A late-added bicycle-parts warranty enquiry form can send a `formSource` value absent from the server allowlist. Its page may pass visual review while submissions fail with HTTP 400.
- Cross-file inconsistency can break any form at runtime while leaving its page visually intact.
- The fix is mechanical: extract the values sent by forms, extract the server allowlist, and assert that the former is a subset of the latter.
- **Skipping this Reflector risks shipping silent runtime failures.** That makes the audit a release requirement.

**Pairs with**:
- Cross-file validation of submitted form-source values against the server allowlist.
- Per-page fidelity checks, which are necessary before the integration audit but do not replace it.
- An explicit comparison of approved slugs against generated routes.

## Skill Registry: Self-Heal Pass additions

Register reusable fixes with the defect they prevent and the evidence needed to verify them.

## Curator Log: Self-Heal Pass entry

Record the failure mode, its fix, and the check that would catch a recurrence.


## Curator Log: Shared workflow entry

Carry reusable changes into other applicable workflows only after checking their assumptions.


## Curator Log: Universal Similar Resources defaults

Keep related-resource presentation consistent across resource types.


## Curator Log: Polish-pass defaults

Retain polish changes that improve clarity without hiding essential content or controls.


---

## Page-Pattern Corrections (Shared Resource Hub Defaults)


### `no-bottom-cta-box-on-pages-001` [PROTECTED: UNIVERSAL]
Remove the bottom-page CTA section, panel, or banner on every resource detail page. Prefer this because the page's primary purpose is to help the reader use the resource, and a closing sales box distracts from that purpose. The last visible element of the resource content becomes a "Back to all resources" link.

### `no-breadcrumbs-on-resource-pages-001` [PROTECTED: UNIVERSAL]
Remove the visible breadcrumb trail at the top of every resource detail page. The content header starts with H1. Accurate BreadcrumbList JSON-LD may remain in the page's structured data.

### `no-all-caps-metadata-strip-001` [PROTECTED: UNIVERSAL]
Remove the all-caps metadata strip below the page title, including resource type, topic, products, file size and page count. The hero contains the H1 only. Keep metadata in Sanity.

### `no-related-resources-tagline-001` [PROTECTED: UNIVERSAL]
Remove the explanatory tagline under the Related resources header. The section contains the header and a grid of 2-4 cards only.

### `related-resources-header-rename-001` [UNIVERSAL]
Change the section header from "Similar resources" to "Related resources" verbatim across every page pattern.

### `no-whats-inside-header-merge-into-descriptor-001` [PROTECTED: UNIVERSAL, guide/spec-sheet/file-bearing patterns]
Remove the "What's inside" section header on guide and spec-sheet pages. Merge its content into the top descriptor as bullets. Apply this to existing and future file-bearing patterns.

### `file-preview-before-download-001` [PROTECTED: UNIVERSAL, file-bearing patterns]
On every file-bearing page pattern, place the file PREVIEW FIRST in the visual flow and the DOWNLOAD button BELOW it. Apply this to guides, spec sheets and future file-bearing patterns. This rule does not govern full-layout HTML resources.

---

## Resource Page Generation Rule

### workflow-l-one-agent-per-page-canonical-NO-BATCHING [PROTECTED: RULE]

**Sister rules**: Assign generators ONE PER PAGE, never batched. Assign reflectors ONE PER PAGE and run each immediately after its generator, never batched. A separate cross-page final reflector always runs after the per-page reflectors.

**THE RULE (PROTECTED)**: Resource-page generation MUST dispatch ONE design-generator agent PER RESOURCE PAGE and ONE design-reflector agent PER RESOURCE PAGE. Never batch multiple pages into one generator or reflector agent.

**Why batching fails**:
1. **Attention dilution causes quality drift**: Processing several pages spreads context across them. A per-page assignment keeps attention on one page.
2. **Stream-idle timeouts**: Large batches can time out before completion. Smaller assignments reduce the amount of work exposed to each interruption.
3. **Recovery cost**: When a batched agent times out, it may be unclear which pages are complete. Recovery then requires an inventory and individual reassignment.
4. **Atomic clarity**: Per-page logs, validation and handoffs keep findings attached to the correct page.

**Canonical cadence**: N pages → N generators in bounded parallel groups → N reflectors, each starting immediately after its generator → one cross-page final reflector for slug uniqueness, links and hub validation.

**ONE EXCEPTION (requires an explicit decision recorded in the run log)**: One reflector per page pattern is valid only when every affected page has already received an individual review. This can support a shared template retrofit. Per-page reflection remains the default.

**Pre-dispatch orchestrator check**: The dispatch list must contain N individual-page invocations. Flag any orchestration draft that batches pages.

**Forward-applicable**: Apply this rule to resource-hub maintenance, multi-page first builds and template-aware website maintenance.

## Universal META-PRINCIPLES (cross-automation skills)

Per-page review and source grounding apply across all three automations in this package.

---

### source-grounding-mandatory-for-all-resource-page-generators-001 [PROTECTED UNIVERSAL: RULE]

Apply the same source-grounding discipline during first builds and resource-hub maintenance.

**The rule**: When a first build includes resource-page generation, every Generator agent prompt MUST instruct the agent to FETCH SOURCE MATERIAL FIRST. Read the original source page or document before writing any user-facing summary, bullets or framing. For a kitchen-equipment maker's resource library, this means opening the actual product guide or spec sheet before describing it.

**Why**: Existing `htmlContent` is second-hand and can accumulate fidelity drift with each rewrite. Brief summaries, key points and explanations of usefulness must remain grounded in the original material.

**Supporting practices**: Verify quotations against their source, use document extracts for quick orientation, and check the full source before finalizing claims. An extract is a navigation aid, not a substitute for verification.

**Forward-applicable to every site** with a resource hub. The first-build handoff must include source-grounded page content as its baseline.

**EXTENSION**: Source grounding applies to UPDATES too. Even a partial update must revisit the relevant source material, because rewriting from the old page alone can carry forward its errors.

---

## Curator Log: Resource Hub Finalization

Record reusable lessons from finalization without carrying project-specific history into this skillbook.

## NEW SKILLS: Resource Hub Production Cutover + Agent-Readiness Repair

Capture reusable cutover and agent-readiness fixes in the relevant skill entries.

## Curator Log: Resource Hub Production Cutover + Agent-Readiness Repair

Record the observed failure, corrective action and verification evidence.

## Above-the-Fold Media Governance + Collaborative Editing

### media-002: pyav APV/ProRes/Future-Codec Decoder Recipe
**Rule**: When `ffmpeg` returns "unknown codec" or "Decoder not found" for a master video file, check whether its build includes a decoder for that codec. A newer PyAV build may provide a suitable bundled libav version, but verify support for the exact codec and profile before relying on it.

**Recipe**: With a compatible PyAV build, use `av.open(src)` → demux and decode → reformat to `yuv420p` → encode with `add_stream("libx264")`. Use encoder options `{"crf":"23","preset":"slow","profile":"high"}` and the output-container option `{"movflags":"+faststart"}`. Flush the encoder and close the container, then verify playback and output properties.

**Tags**: pyav, codec-support, video-decoder, fallback, future-codec-readiness. **Status**: active.

## Curator Log: Above-the-Fold Media Governance

Record decoder compatibility and playback checks when adopting a new media conversion approach.

---

## Curator Log: Site Banner System + Production Release

Record reusable banner integration and release lessons alongside the affected skills.

## Cross-Reference: Article Batch Canonicals

### Pattern S Three-Layer Fidelity Contract (must be wired correctly from day 1)

Pattern S (self-styled HTML page) means rendered resources whose documents own their full HTML layout, such as a bicycle-parts company's guides with a sticky table of contents or custom comparison sections. A first-build Astro app supporting these resources MUST wire ALL THREE layers:

- **Layer 1: Sanity GROQ projections** include `htmlContent, htmlStyles, htmlSchemas` together in EVERY query that retrieves resource documents, including listing, detail, series and related-resource queries.
- **Layer 2: Resource-detail rendering** injects `htmlStyles` as scoped `<style data-resource-styles>` and `htmlSchemas` as `<script type="application/ld+json">`. Hoist constructed values into frontmatter constants to avoid the JSX nested-template-literal esbuild trap.
- **Layer 3: A top-level Astro `<script>` block** provides interactive behavior such as scroll-spy or accordions. Gate initialization on a wrapper-class detector so it can coexist safely with other resource types.

**If the first build only wires Layers 1+2**, document the deferred Layer 3 hook so maintenance work can connect it when the first interactive resource arrives.

**Related skills**: `pattern4-three-layer-fidelity-contract-canonical-001`, `sanity-query-htmlstyles-htmlschemas-projection-canonical-001`, `astro-set-html-script-inert-gotcha-canonical-001`, `jsx-nested-template-literal-esbuild-trap-canonical-001` and `scroll-spy-astro-script-canonical-001`. **Tags**: pattern4, fidelity-contract, first-build, layer-1-2-3.

### Why These Are First-Build Concerns (not maintenance)

The per-wave Curator discipline (`ace-curator-per-wave-mandatory-canonical-001`) and live production-render checks (`ace-reflector-production-test-gate-live-render-mandatory-001`) catch these failure modes. Catching them later costs revision cycles, cloud builds and human review time. Wiring the layers correctly during the first build avoids that rework.

---

## Cross-Propagated from Resource-Hub Maintenance: SSR Detail Defaults

### S-BX-SSR-A astro-ssr-detail-with-edge-cache-default-at-first-build [PROTECTED, UNIVERSAL]
**Rule**: At first-build time, use SSR with edge caching for CMS-backed Astro detail pages when the host supports that caching behavior. Keep listing and detail freshness aligned. Pattern:
```astro
export const prerender = false;
const { slug } = Astro.params;
const resource = await getResourceBySlug(slug!);
if (!resource) return Astro.redirect('/resources/');
Astro.response.headers.set('Cache-Control', 'public, s-maxage=60, stale-while-revalidate=86400');
```
This prevents a fresh SSR listing from linking to stale or missing SSG detail pages. Verify edge-cache behavior on the deployment platform. A Cloudflare Worker's own responses are not automatically edge-cached merely because these headers are present. Where an explicit caching implementation is unavailable, use static listing and detail pages with a CMS deploy hook. See `05_automations/resource-hub-maintenance/runbook_appendix/redeploy_cloudflare_workers.md`. **Tags**: astro, ssr, edge-cache, first-build, default. **Status**: active.

### S-BX-SSR-D deploy-local-astro-build-before-push-default [PROTECTED, UNIVERSAL]
**Rule**: Make `npx astro build` a mandatory check before pushing a deployment change. If the build passes, proceed. If it fails, stop and fix it locally. This catches build failures, including a literal `</script>` inside embedded script text, before spending time on a failed cloud build. A successful build does not replace runtime or visual checks. **Tags**: astro, deploy, local-build, discipline, first-build. **Status**: active.

## Pre-Launch Readiness Checklist (MANDATORY)

Confirm source grounding, per-page review, resource rendering, content freshness and a successful local build before launch.

## persona-conference-injection-001 [PROTECTED, UNIVERSAL]

**Rule**: Every ACE Generator and Reflector subagent spawned to build or score a website page, individual resource page, resource-page template or resource card MUST receive its role-specific conference instruction block at spawn time. See `05_automations/client-site-first-build/comprehensive_guide.md`. Keeping the discipline in a skill file is insufficient: include the applicable instructions in each agent's task prompt.

**Per-content-type skill map (this package)**:
- Website page: `03_skills/design-architect-thinking/SKILL.md`, `03_skills/astro-website-page-creation/SKILL.md` and `03_skills/aeo-optimization/SKILL.md`.
- Resource page or template: `03_skills/resource-hub-resource-page-builder/SKILL.md`, `03_skills/resource-hub-thinking/SKILL.md` and `03_skills/resource-slug-design-canonical/SKILL.md`.
- Visual or brand surface: `03_skills/corporate-graphic-design/SKILL.md`. For a live graphics layer, also consult `03_skills/webgl-craft/SKILL.md`.
- Weighty trade-off: `04_reasoning/commands/inner-council.md`.

Use these shipped skills and human copy review to assess wording, brand consistency and factual support.

**Status**: active. MANDATORY for every content-bearing ACE loop.

---

### Curator log: Agent-Discovery Catalog Adoption + Version-Check Discipline

Apply these reusable practices when adding agent-discovery support:

- **`ards-scaffold-001` [ACTIVE]**: Generate an honest agent-discovery catalog from the site's actual agent description, capabilities and API definitions. Treat it as a compiled view rather than hand-maintained content to reduce drift. Omit empty capabilities and unsupported trust or identity claims. Use real domain-based identifiers and represent contact capabilities only as the adopted schema permits. Advertise the catalog through the file, robots discovery directive, HTML discovery link and HTTP Link header where supported by the current specification.
- **`ards-version-check-first-001` [ACTIVE]**: Before building agent-readiness features, check the authoritative specification, evaluator documentation and hosting-platform documentation and changelogs. Record the versions checked, compare them with the previous check and act on relevant changes.
- **`frontier-decision-gate-001` [PROTECTED]**: Before adopting a new technique that could replace or materially change established build practice, deliberate on its evidence, alternatives and consequences using `04_reasoning/commands/inner-council.md`. Complete that review before changing shared guidance or recording the decision as settled. Apply this to consequential architectural decisions, not routine work or ordinary notes. See `03_skills/agent-readiness-frontier/SKILL.md`.
- **`ards-advisory-gate-001` [ACTIVE]**: Treat conformance to an experimental discovery specification as advisory: report findings without making them release blockers. Keep established agent-readiness checks separate. Consider mandatory conformance only after the specification stabilizes and ordinary sites can demonstrate practical discovery support. Review that policy change through the deliberation process above.
- **`ards-fleet-propagation-001` [ACTIVE]**: At the end of a run, record newly adopted agent-readiness techniques and their evidence with `03_skills/agent-readiness-frontier/SKILL.md`. This lets a person or small team assess whether the same technique would help another site they operate.

Generation in ACE loops MUST use the design-generator role defined in `05_automations/agents/design-generator.md`.
## NEW SKILLS: Cloudflare Workers deployments, preview and main

These skills cover preview configuration and reproducible build checks for a site's Cloudflare Workers deployment. Use them alongside [the first-build guide](05_automations/client-site-first-build/comprehensive_guide.md).

### cf-008: One Preview Mechanism Per Worker, Confirmed in the Dashboard as Well as the API [PROTECTED, RULE]
> **UPDATED**: Use Cloudflare Worker Previews as the default mechanism. The version-alias approach below is an alternative, not an additional pipeline.

**Rule**: A Cloudflare Worker gets exactly ONE preview mechanism: (A) a version preview alias trigger (`wrangler versions upload --preview-alias <branch>`) with Settings > Build > Branch control > "Enable Preview Builds" OFF, or (B) Worker Previews with that checkbox ON and a `previews` block of preview-safe resources, including a separate preview D1 database, its own rate-limit namespace, preview variables and secrets, and optionally Cloudflare Access in front. At first-build setup, choose one, defaulting to B. Verify the checkbox state in the dashboard rather than inferring it from API results, and record the choice and state in the site's handoff notes. Confirm every deploy in BOTH the Workers Builds API and the dashboard's per-branch / Preview view, because either view can omit a competing pipeline.

- **Evidence**: A version-alias trigger can succeed while Worker Previews fails on the same push with "Your Wrangler configuration is missing a `previews` block". The dashboard's branch view and the builds and triggers APIs can then present apparently contradictory results. Check the current dashboard setting explicitly; do not assume a default or treat an absent API field as proof that preview builds are disabled.
- **Tags**: cloudflare, workers, workers-builds, preview, deploy, verification-blind-spot, first-build
- **Status**: active [PROTECTED, RULE]

### cf-009: Clean-Clone Pre-Push Build in the Workers Builds Environment [PROTECTED, RULE]
**Rule**: Before every push to a Workers Builds branch, clone the committed branch into a temporary directory and run `npm clean-install && npm run build` under `env -i`. Supply a minimal PATH containing the intended Node installation and required build utilities, plus `CI=true WORKERS_CI=1 WORKERS_CI_BRANCH=<branch>` and `CLOUDFLARE_ACCOUNT_ID` from your configured credentials file, parsed rather than sourced. Push only on exit 0. A clean clone sees only committed files and explicitly supplied variables, so uncommitted files, local caches and shell state cannot hide a failure. `WORKERS_CI_BRANCH=main` exercises the production guards before the first main push. This strengthens a plain local `astro build` check by approximating the hosted builder's environment.

- **Evidence**: A clean-clone check can verify that a preview build includes its preview-only component showcase while the main build applies production guards. Record the build result and any unresolved checks separately; a successful build does not resolve a pending content or configuration question.
- **Tags**: cloudflare, workers, ci-simulation, pre-push, clean-clone, deploy, first-build
- **Status**: active [PROTECTED, RULE]

## NEW SKILLS: Cloudflare Workers forms, privacy and deploy verification

These skills address failures that build, accessibility and page-render checks alone can miss. Each entry includes evidence, a falsifier, a generality claim and a ledger state. Validation rests on executable checks and independent re-verification, not score magnitudes.

### qa-029: Check Every Privacy-Page Sentence Against the Code as a TRUE / FALSE / UNVERIFIABLE Truth Table Before Signature [VALIDATED]
**Rule**: Before a privacy page goes to the site operator for sign-off, list every sentence of its rendered body, its meta description, and every consent line or machine-readable description that restates a data practice. Give each sentence its own row and a verdict supported by code or live configuration. TRUE cites a file and line or measured behaviour. FALSE cites contradicting code or measurement and opens a finding. UNVERIFIABLE explains why, such as pending configuration, vendor behaviour or production-only state. A FALSE row blocks sign-off until the code or words change. An UNVERIFIABLE row is named in the handoff, never passed silently. Re-run the whole table after every fix because changing one data practice can make another sentence false.

- **Evidence**: Sentence-level review exposes discrepancies that build, lint, axe, Lighthouse and form round-trip checks do not assess: an unnamed inbox provider; a claimed "referring page" that is actually the form's own URL with its query string; repeat-sign-up answers or consent versions that are dropped or left unlinked; and an "error reports only" promise contradicted by scheduled success logs or platform invocation logs. Re-check each correction independently and keep production-dependent contradictions open until the live configuration resolves them.
- **Falsifier**: A page that passed this table is later shown to contain a sentence already contradicted by the code when the table was run, or repeated use finds only wording preferences with no data-practice consequence.
- **Generality**: Every first build with a form ships a privacy page (port-028). Its text describes intended behaviour while the code changes underneath it, so the gap can recur.
- **Ledger**: VALIDATED through independent re-application after fixes; production-dependent findings remain open until verified.
- **Dedup**: port-028 KEEP: it defines what the page must cover; this skill checks whether those statements are true.
- **Tags**: privacy, review, truth-table, forms, pre-signature, first-build
- **Status**: active

### forms-007: Make a Repeat Sign-Up Indistinguishable From a First One, and Link It So Deletion Still Reaches It [VALIDATED]
**Rule**: A sign-up endpoint answers a repeat address exactly as it answers a new one: the same status, body shape (for example `{ok:true, token:<string>}`), redirect and follow-up card, with no extra work before the response that could make a repeat measurably slower or faster. To keep the token meaningful without revealing the existing row, sign it over a fresh ID for this request. After the response, for example in `ctx.waitUntil`, write a server-side link row from that fresh ID to the existing sign-up. Anything keyed to the token, such as an optional answer or note, must be reachable by deletion by email and by the retention job. An answer insert requires its parent row (`INSERT... SELECT... WHERE EXISTS`), so no answer is keyed to a vanished row.

- **Evidence**: For an invented regional bakery chain's newsletter, returning `{"ok":true,"token":"..."}` for a new address but `{"ok":true,"token":null}` for a repeat would expose membership. Hiding the follow-up card only for repeat addresses would expose it again. Issuing a fresh token fixes that visible difference but can orphan the repeat's answer if deletion follows only the original sign-up ID. A link table, created through a migration and written after the response, connects the records. Verify with a repeat sign-up followed by an answer and deletion: no associated answer, link or sign-up rows should remain.
- **Falsifier**: A comparison of first and repeat sign-ups distinguishes them by status, body length, token shape or latency beyond noise, or deletion by email leaves a row keyed to the repeat's token.
- **Generality**: Every notification, newsletter or waitlist form faces this choice. An "already signed up" reply allows address enumeration, and fixing that leak can break deletion unless the link is designed in.
- **Ledger**: VALIDATED through response-equivalence and deletion checks, independently repeated after the link fix.
- **Dedup**: forms-001 KEEP: it covers contact-form validation and delivery, not response equivalence.
- **Tags**: forms, privacy, enumeration, erasure, retention, cloudflare-workers, d1
- **Status**: active

### forms-008: A Malformed Request Body Is Never Logged [VALIDATED]
**Rule**: In a form or API handler, every parse of request input, including `JSON.parse`, base64 or `atob` decoding and token decoding, sits inside its own try/catch. Map failures to a 4xx, such as 400 `bad_body` or 403 `invalid_token`, without rethrowing or logging the parser error. The top-level catch logs only the error's name (`e instanceof Error ? e.name : typeof e`), never `String(e)`, `e.message` or the stack, because V8 parse errors can quote the first bytes of their input.

- **Evidence**: A malformed JSON body beginning with an email address can cause an unguarded handler to return 500 and copy part of that address into a parser-error log. A forged token with invalid base64 can follow the same failure path. Reproduce both locally with `wrangler dev`. Then verify that the body parser returns a controlled `bad_body` response, the token reader returns null on decoding failure, and the top-level catch logs only the error name.
- **Falsifier**: A malformed body or token sent to a handler following this rule produces a 5xx, or a log line contains bytes from the request.
- **Generality**: Any Worker or V8 server that parses request input and logs raw errors can leak input into the platform's retained logs.
- **Ledger**: VALIDATED through malformed-input probes and inspection of logs after the fix.
- **Dedup**: logging-001 KEEP: that skill forbids success logs; this one governs what an error log may contain.
- **Tags**: forms, logging, privacy, security, workers-logs, v8
- **Status**: active

### logging-001: Worker Code Writes Error Reports Only, Enforced by a Lint Over the Worker's Import Closure [VALIDATED]
**Rule**: When a site promises that it keeps only error reports, enforce that promise with a lint. Scope the lint to every file reachable through relative imports from each Worker entry point; a fixed path list misses shared libraries. Reject every reference to the `console` token other than `console.error`, including dot, bracket and optional-chaining calls. Refuse bare references used for destructuring or aliasing. Include scheduled handlers, since a counts-only success line is still a success log. Plant one mutant per spelling (qa-030).

- **Evidence**: A scheduled retention success message contradicts an "error reports only" promise when platform logging captures it. A lint limited to entry-point files misses logging inside imported helpers. Even after expanding its scope, a naive pattern can catch `console.log` and `console["log"]` while missing `console?.log(x)`, `const { log } = console; log(x)` and `const c = console; c.log(x)`. Independent mutation checks expose these gaps.
- **Falsifier**: A success-path log reaches the platform's log store from a Worker whose lint passes under this rule.
- **Generality**: A Worker that logs errors can later acquire a well-intended success log. A privacy statement about logs is literal, and manual review can miss a single logging line.
- **Ledger**: VALIDATED through captured logging behaviour and independent mutation checks of lint coverage.
- **Related**: The platform half of the same promise is `observability.logs.invocation_logs: false` on the production Worker and in any `previews` block. Keep this as an unresolved launch check until the deployed configuration is verified.
- **Tags**: logging, privacy, lint, workers-logs, import-graph, cloudflare-workers
- **Status**: active
### copy-001: Merge Writer Copy Into the Strings Registry Through a Guard: Signed Text Changes Only by Name, and the Original Is Kept [VALIDATED]
**Rule**: When a writer's copy lands in a site's strings registry by script, the merge classifies every key before writing anything. A pending slot is written. An identical value is a no-op. Any other current value (signed, locked, a name, an editorial decision) is a CONFLICT that is reported and not written, unless the key is named explicitly on the command line (for example `--allow-revise key=N`, naming the open item the revision resolves). A permitted revision keeps the ORIGINAL signed text beside the new value (for example as `superseded_signed`) through every later revision, and an entry that carries it is never refreshed automatically, even when its source prefix matches the writer's. Validate every value first (punctuation rules, known includes, no pending markers), so one refusal writes nothing, and exit non-zero when conflicts were reported.
- **Evidence**: A copy review exposed a draft that changed signed values without a guarded merge path. An initial guard still refreshed a previously revised signed string without permission because its source shared the writer's prefix. Excluding entries that carry `superseded_signed` closed that bypass: an unapproved change exits non-zero with a CONFLICT, while an explicitly permitted revision preserves the original signed text.
- **Falsifier**: a signed or locked value changes in the registry without its key being named in the revise flag, or a revision loses the original signed text.
- **Generality**: Any site that combines writer drafts with approved copy has multiple writers affecting one file. The order of refresh rules and protection checks determines whether silent overwrites can happen.
- **Ledger**: VALIDATED (the protection bypass was reproduced, and the corrected guard was independently reviewed).
- **Dedup**: content-002, content-003, content-004 and content-005 KEEP (content import and CMS operations, not a strings registry). Choosing an authoritative design source is separate from deciding who may change signed words.
- **Tags**: copy, strings, merge, signed-copy, guard, content-ops
- **Status**: active

### cf-010: Worker Previews Setup: Base-Config Secrets Before Creation, Recreate a Stale Preview, Spike on a Throwaway Named Preview, Migrate Through a Throwaway Config [VALIDATED]
**Rule**: After choosing Cloudflare Worker Previews, set them up in this order, for one outcome: a Preview that the pipeline builds with every binding it needs.
1. **Secrets live in the Preview base config** (`wrangler preview base-config secret put <NAME>`) and are set BEFORE any Preview exists. Cloudflare copies base-config secrets into a Preview only when the Preview is CREATED; they then persist across its deployments. A Preview created earlier (for example by failed builds) never receives them, and `wrangler preview secret put` or `bulk --name <p>` attaches secrets to a single deployment only, so the next push creates a deployment without them. Cure a stale Preview by deleting it and letting the next CI push recreate it from the base config; never patch it deployment by deployment.
2. **Spike on a throwaway named Preview** (`wrangler preview --name <spike>`) before the first real push, and spike the path you will actually take: two consecutive deployments (to prove persistence) and, if a Preview already exists, that existing Preview rather than only a fresh one. In a non-interactive shell `wrangler preview delete` answers its own confirmation, so guard every scripted delete with an exact-name check (`[ "$N" = spike ] || exit 9`).
3. **Apply D1 migrations to the preview database through a throwaway config** that names only the preview database, with an absolute `migrations_dir`. Wrangler resolves the database from the config's D1 list, so a config in which production does not exist cannot migrate production. Apply the same migration to production separately, after a restore bookmark.

Cron triggers do not run on Previews, so a scheduled job never runs there; clean preview data with its own tool.
- **Evidence**: An existing Preview lacked required base-config secrets, causing forms to fail closed. A per-Preview secret update repaired one deployment, but the next CI push lost those secrets. A throwaway Preview created from the configured base retained its secrets across consecutive deployments. Recreating the stale Preview through CI resolved the same failure. Testing only a fresh Preview had missed the existing Preview's configuration problem.
- **Falsifier**: a Preview created before a base-config secret receives it on a later deployment; a secret set with `preview secret put` survives into the next CI deployment; or a Preview created after the base config lacks a base secret on its second deployment.
- **Generality**: Any Preview created before its required base configuration is complete can retain stale configuration. Test both creation and subsequent deployment through the pipeline you use.
- **Ledger**: VALIDATED for the tested Preview workflow through consecutive pipeline deployments. Re-check these platform-dependent behaviours after a Wrangler or platform change. The `wrangler preview --secrets-file` alternative remains untested here. The production migration path was checked by dry run only.
- **Dedup**: cf-008 KEEP (it chooses the mechanism; this sets it up). cf-009 KEEP (a clean-clone build, not Preview configuration). deploy-006 KEEP (Pages secrets and project deletion, a different object).
- **Tags**: cloudflare, workers, worker-previews, secrets, d1, migrations, spike, first-build
- **Status**: active

### cf-011: Probe an Access-Protected Host Without Ever Printing or Saving the Session Cookie [VALIDATED]
**Rule**: A credentialed request to a Cloudflare Access-protected preview can return `Set-Cookie: CF_Authorization=<session JWT>`. Never print raw response headers and never write them into a body file. Use `curl -s -o /dev/null -D <file>` with the file created mode 0600 in the system temp directory (never inside a git working tree), select only the named headers you need, show no `set-cookie` line, and delete the file in a `finally`. `curl -I` combined with `-o` writes the headers into the `-o` file, so a "body preview" of that file prints the cookie. Pass service-token headers from a 0600 file, never on the command line, and redact the query of the anonymous Access login redirect when printing it.
- **Evidence**: Header inspection exposed two leak paths: a raw header dump printed a session cookie, and a probe using `-I -o` placed response headers in a file treated as a body preview. Reading service-token headers from a restricted temporary file outside the repository and printing only selected response headers avoided those exposures.
- **Falsifier**: a probe that follows this rule prints or retains a CF_Authorization value after cleanup, or the service-token values appear in process listings or shell history.
- **Generality**: Any reviewer or deployment watcher probing an Access-protected preview with credentials can leak session data through ordinary curl habits.
- **Ledger**: VALIDATED (both header-output failure modes were observed during review).
- **Dedup**: cf-007 KEEP (public values in the repo, not session credentials at probe time). Sharing a preview link is separate from handling credentials during a probe.
- **Tags**: cloudflare, access, security, credentials, curl, reviewer-hygiene
- **Status**: active

### deploy-007: Judge a Deploy by Its Product: a Probe Path Plus a Build Marker, and Binding Names on the Deployment Tagged With the Pushed Commit [VALIDATED]
**Rule**: After every push, a deploy counts as done only when both checks pass. (1) A probe path on the deployed URL answers 200 AND its body contains a marker that exists only in the new build (a class name, a new sentence), fetched with the access the reviewer will have; on an Access-protected preview that means the service token, with an anonymous request recorded as the expected 302. (2) The platform's record of the LATEST deployment is tagged with the pushed commit and lists every required binding by name and type (names only, never values). The check refuses to judge, with its own exit code, while the tag does not match yet or when the response has an unfamiliar shape. A pipeline API that reports success is not evidence: it may not list every pipeline on the Worker, and a stale deployment still answers 200. Any "done" claim about live state carries the deployment id and commit it was measured on, and is re-derived after the last push.
- **Evidence**: A deployment watcher reported success because its API did not list the failing Preview builds. A probe that checked both the path and a new-build marker distinguished the stale 200 response from the deployed change. A binding check initially misread the API response shape and reported missing secrets; refusing unfamiliar shapes corrected that diagnosis. Review also caught a completion claim that described an earlier deployment rather than the build under review.
- **Falsifier**: a deploy that passed both checks under this rule serves a build other than the pushed commit, or lacks a required binding.
- **Generality**: Any platform with multiple pipelines, preview aliasing or delayed rollout can show success for a build other than the one you pushed. Verify the served output and deployment record against your commit.
- **Ledger**: VALIDATED (both checks were exercised, and review exposed stale evidence in both pipeline status and a completion report).
- **Dedup**: cf-008 KEEP (it finds hidden pipelines; this judges the build). quality-001 KEEP (it checks quality; this establishes which build is live). Checks before handoff do not replace verification after deployment.
- **Tags**: deploy, verification, observability, cloudflare-workers, worker-previews, post-push
- **Status**: active

### deploy-008: Test a Deploy Guard Where Its Failure Cannot Ship [VALIDATED]
**Rule**: Prove that a guard against a dangerous action (a production deploy of a preview build, a remote database write, an auto-confirming delete) refuses correctly WITHOUT performing that action for real. Test it where failure is harmless: evaluate the guard's condition on its own, feeding it each argument shape; run the tool in a temp directory with a fake trigger (a fake preview-only artifact, a dummy config that names no real resource); put a PATH shim first that refuses the dangerous flag (for example `--remote`), and prove the shim's refusal first; or import the tool as a module and swap only its transport for a local executor that asserts the dangerous flag never appears. Never test a deploy guard by running the real deploy in the real repository.
- **Evidence**: Testing a preview-build guard through a real deploy created a near-miss: a failed guard would have shipped the preview build to production. Evaluating the condition separately across argument shapes then revealed bypasses without running Wrangler. Other safe checks used a PATH shim that redirected permitted operations to local execution and refused everything else, or a module-level local executor that asserted `--remote` never appeared. The shim's refusal was tested before it was trusted.
- **Falsifier**: a guard tested only by these harmless methods passes them and then fails to stop the real action in the same argument shape (the harmless test did not model the real invocation).
- **Generality**: Whenever a build adds guards around deploys and remote writes, testing must assume the guard can fail. A test that reaches the real destination makes the guard's defect capable of causing the action it should prevent.
- **Ledger**: VALIDATED (a near-miss demonstrated the hazard, and harmless tests exposed real defects).
- **Dedup**: qa-030 KEEP (which shapes a guard must refuse; this is where to test it). Running a local build before pushing is separate from testing a deploy guard.
- **Tags**: deploy, guards, testing, safety, near-miss, operator-cli
- **Status**: active
### ace-011: In the NEAR Regime, Accept on Binary Checks and Two Blind Reviewers, Not on the Scalar [VALIDATED]
**Rule**: When the lowest dimension score is close to its acceptance floor, call this the NEAR regime and stop using the scalar score to decide acceptance. The last reflection restates every remaining criterion as a binary, execution-verifiable check (C1 to Cn: a command, a live request or a planted mutant, each with its expected result). Two independent reviewers then run every check themselves, blind to each other's output. Acceptance requires both to recommend ACCEPT with every check PASS; any scalar they report does not decide. In this regime the Generator stops reading the skillbook mid-run and works only from the prioritised issue list and the checks. Arrange independence explicitly: brief the reviewers without the iteration budget, and give them disjoint resources, including port ranges and scratch directories, so neither can test the other's server. Non-blocking findings go to a residual list with exact fixes, not into another scored round.
- **Evidence**: independent reviewers caught missing deployment secrets by executing live checks, despite a review brief describing the issue as fixed. Both accepted after the underlying deployment configuration was corrected. The review also exposed shared test ports and an iteration budget in the brief, both of which weakened independence.
- **Falsifier**: the two reviewers disagree on a check's verdict against the same deployment with neither misreading the artifact, showing that the check was not binary; or a defect that a written check should have caught is found after a two-reviewer ACCEPT.
- **Generality**: near an acceptance floor, reviewer-to-reviewer score variation can exceed the remaining gap. A scalar then cannot reliably resolve acceptance. Any iterative build-and-review process approaching its threshold can encounter this problem.
- **Ledger**: VALIDATED through concordant independent verdicts before and after a fix. Executed checks caught a live regression that the score-based review had not established as resolved.
- **Dedup**: ace-001 (9.8 HARD) and ace-003 (no rounding) KEEP: they still define score handling outside the NEAR regime. Keep score-calibration guidance out of the Generator's repair brief in every regime. A final cross-page integration audit remains useful, but does not replace the binary acceptance checks.
- **Tags**: ace, acceptance, near-regime, binary-checks, blind-review, evidence
- **Status**: active

### qa-030: Build a Guard From the Definition of What It Refuses, Then Prove It Against Every Spelling [VALIDATED]
**Rule**: Specify a guard, lint or validator by the whole class it must refuse, not by the instance in hand. First write the definition ("any console use except console.error", "any vendor test key", "any invocation that deploys"). Then enumerate the spellings of that class from the vendor's list, the language's syntax or the tool's argument grammar: the vendor's full published set of test values; dot, bracket, optional-chaining, destructured and aliased references; the subcommand anywhere in argv, after global flags, and its alternates (for Wrangler, `versions upload` and `versions deploy`); values with surrounding whitespace (trim, or refuse padding, before any anchored pattern); and the guard's own pre-processing (a regex comment-stripper treats `//` inside a string as a comment and hides the rest of that line). Plant one mutant per spelling and require each to fire.
- **Evidence**: guards built around a single observed spelling missed other members of their stated class. A Turnstile pattern missed published test keys. An error-reports-only lint missed destructured and aliased console references. Whitespace let a test key pass production checks. A deploy guard that read only the first argument (`${1:-}`) missed invocations with global flags before the subcommand.
- **Falsifier**: a guard whose definition and spelling census were written, and whose mutants all fire, is later bypassed by a spelling of its own defined class.
- **Generality**: every build writes guards, including environment checks, lints, deploy wrappers and secret scanners. An ad hoc search covers what its author suspects; a systematic enumeration starts from the complete refusal rule.
- **Ledger**: VALIDATED across different guard types, including failures found independently by blind reviewers.
- **Clause: a mutant counts only when the plant is shown in effect.** Before treating a mutant as a detected failure, prove the plant applied. The mutating step must fail loudly when its pattern matches nothing, and the log must print what was planted and where. Also prove that the plant survives the defences the page already has: a planted animation must outrank the site's reduced-motion reset, and a planted fault must not be absorbed by a fallback. Read failure from the check's own FAIL line naming the planted defect, never from the process's exit code alone. A plant that throws can exit non-zero without exercising the check; a plant that silently does nothing leaves the check green. Use a guarded replacement such as `const once = (s, re, to) => { const n = s.replace(re, to); if (n === s) throw new Error('mutant did not apply'); return n; };` and log `planted into <file>: <line>`. Evidence: mutation checks exposed both replacements that failed to match regenerated output and animations neutralised by an existing `* { animation-duration: 0s !important }` reset. Falsifier: a logged, effective plant produces the check's own FAIL line naming the defect, but later inspection shows that an unrelated side effect caused the failure. Ledger (clause): VALIDATED across failed insertion and neutralised insertion. Generality: text rewrites against minified or regenerated output can stop applying whenever the build changes.
- **Dedup**: cf-007 KEEP (the vendor-value instance). logging-001 KEEP (the console-lint instance). deploy-008 KEEP (where to test a guard, not what it must refuse). Checking that browser-submitted form values are a subset of the server allowlist remains a separate property. The broader principle also applies to reference searches: enumerate the population before claiming coverage.
- **Clause: a mutant must deliver the STRENGTH it claims.** Measure the mutant's actual effect with the check's own probe on the build variant that ships before treating it as proof. A plant on an unused branch, a plant of the value already shipped, or a plant that saturates below its nominal strength can leave a correct check green. For a brightness mutant, clone the layer and composite with `plus-lighter` when testing additive light output, rather than assuming a filter delivers the requested multiplier. For example, `filter: brightness(3)` can clip near-white pixels before it produces a threefold measured increase. Even additive clones need measurement because the rendering pipeline may still clip the output. Ledger (clause): VALIDATED through ineffective plants caused by unused branches, unchanged values and saturation.
- **Feedback**: useful corrections included changing a haze control away from its shipped value so the plant actually altered the image; replacing an absolute pixel floor with a ratio when testing colour balance; applying a colour-wash mutant to every shipped shader variant and naming each in the log; and replacing a saturating brightness filter with measured additive layers. Each correction made the mutant exercise the defect it claimed to test.
- **Tags**: guards, lint, mutation-testing, class-over-instance, security, qa
- **Status**: active

## Skill Registry: site-chrome loop additions

| ID | Section | Status | Added | Source |
|------|---------|--------|-------|--------|
| qa-029 | Quality / Privacy verification | active, VALIDATED | During review | Site-chrome verification |
| forms-007 | Forms / Privacy | active, VALIDATED | During review | Site-chrome verification |
| forms-008 | Forms / Logging | active, VALIDATED | During review | Site-chrome verification |
| logging-001 | Logging / Privacy | active, VALIDATED | During review | Site-chrome verification |
| copy-001 | Copy / Strings registry | active, VALIDATED | During review | Site-chrome verification |
| cf-010 | Cloudflare Workers Deploy | active, VALIDATED | During review | Site-chrome verification |
| cf-011 | Cloudflare Access / Security | active, VALIDATED | During review | Site-chrome verification |
| deploy-007 | Deploy verification | active, VALIDATED | During review | Site-chrome verification |
| deploy-008 | Deploy guards | active, VALIDATED | During review | Site-chrome verification |
| ace-011 | ACE Loop / Acceptance | active, VALIDATED | During review | Site-chrome verification |
| qa-030 | Quality / Guards | active, VALIDATED | During review | Site-chrome verification |

## NEW SKILLS: art-directed apertures, text over painted art, review captures

These lessons come from product-page review. Each entry is checked against the artifact and written criteria using logs, captures, source lines or arithmetic, without relying on the reviewer's reasoning alone. Each carries evidence, a falsifier, a generality claim and a ledger state. Score magnitudes are not evidence. Examples below are illustrative business scenarios, not project records.

### media-005: An Art-Directed Image Container Switches Composition at the Breakpoint of the Content It Holds, Not at a Device Breakpoint of Its Own [VALIDATED]
**Rule**: When a container serves art-directed compositions of one image (a `<picture>` whose portrait `<source media>` swaps a wide plate for a tall one) and holds content that changes its own layout at a breakpoint, drive the composition switch from the content's layout breakpoint. The content, or a shared token, passes its breakpoint to the container, so whenever the tall layout shows, the tall composition is served. A device breakpoint chosen inside the container is only a default. Prove it with arithmetic on measured boxes, not by eye: under `object-fit: cover`, the share of the served image's width that shows is (box width / box height) / (image width / image height), capped at 100%. Use the box the art actually fills, whether that is the whole container or a viewport-height layer when the art is sticky. Sweep every width from the narrowest served width to the content's wide breakpoint, including the band between the two breakpoints, in every content state that changes the box's height. An opened disclosure, expanded accordion or revealed panel can re-crop the art when a reader clicks. Assert a floor, for example 50%.
- **Evidence**: mismatched image and content breakpoints can pass component-level checks while producing severe cropping between those breakpoints. As an illustrative example, a kitchen-equipment maker's resource page switches to portrait art below 48rem, while its comparison figure uses a tall layout below 64rem. At a 16px root font size, the mismatch spans 768 to 1023px. A 1600 × 900 wide image covering an 800 × 2000 box shows only 22.5% of its width. Each breakpoint may look reasonable in isolation; the defect appears where their behaviours overlap.
- **Evidence, follow-up**: coupling the switch to the content breakpoint addresses the composition mismatch, but does not guarantee the coverage floor. In an illustrative bicycle-parts guide, a 900 × 1200 portrait image covering that same 800 × 2000 box shows about 53.3% of its width. If an expanded disclosure grows the box to 2400px tall, coverage falls to about 44.4%. Bounding the art to an 800 × 1000 sticky window brings horizontal coverage to 100%. At wider layouts, opening a disclosure can also make the wide composition fail the floor. Measure both closed and expanded states from the art's actual box; a width-only sweep misses this failure mode.
- **Falsifier**: isolate the composition switch by disabling the sticky window in a test variant. Compare measured coverage against the formula across the breakpoint gap. For the illustrative dimensions above, expect 22.5% for the wide image and about 53.3% for the portrait image in the 800 × 2000 box. Reject the measurement claim if observed shares depart from the formula by more than 2 percentage points. Reject the claimed improvement if any width in the tested tall-layout range shows a smaller horizontal share with the coupled switch than without it.
- **Generality**: image components often choose device-class breakpoints before their contents are designed. The content then chooses its layout breakpoint elsewhere. Any container reused for figures, forms or card grids can encounter a layout it was not designed for, while isolated checks on both components still pass.
- **Ledger**: VALIDATED through measured-box arithmetic and a test variant that isolates the composition switch. A recurrence after disclosure expansion established that the sweep must cover content states as well as widths. The dimensions above illustrate the method and are not a retained project measurement.
- **Dedup**: media-001 KEEP (weight budgets and LCP discipline; a desktop-only video switch is a different concern from composition-versus-content coupling). Guidance on image style and composition choice remains separate from deciding when to switch compositions. tooling-004 KEEP (which captures can judge a sticky art layer; this skill decides which composition a box receives).
- **Tags**: art-direction, picture, breakpoints, responsive-images, object-fit, cover-crop, apertures, cross-component
- **Status**: active (VALIDATED)
### qa-031: Grade Text Over Painted or Photographic Art at the Worst Pixels Under the Words (p99 and the Maximum Under Each Line), Never p95 [VALIDATED]
**Rule**: axe's colour-contrast rule does not grade text over a background image as a normal flat-colour pair; it can return such nodes for review rather than as violations. Text over art therefore needs a separate check: render the page with the text made transparent, leaving layout and scrims unchanged, take each text element's boxes from its text nodes' client rects, and read the background luminance inside those boxes. Grade on the worst background beneath the words using two checks: (1) the 99th percentile of luminance for light text, or the 1st percentile for dark text, meets the applicable contrast threshold; (2) the brightest pixel under each line box, or the darkest for dark text, stays within a stated cap. A glyph mask can make the second check more precise. For white text, an example extreme-pixel cap is 0.3 relative luminance, about 3:1 at that single pixel; this does not replace the applicable contrast requirement. A percentile excludes every feature smaller than its tail: p95 can miss a highlight covering under 5% of the box, and p99 can miss one covering under 1%. A small highlight can still interrupt a letter. Report p95 if useful, but never gate on p95, a mean or a median. When a brief describes an image's text zone by its p95, treat that as a placement hint, not as the grading statistic.
- **Evidence**: a kitchen-equipment maker's resource library illustrates the failure mode. A checker can print both p95 and p99 while using only p95 to decide whether a caption passes. Small reflections on cookware may then sit beneath the words even though the reported result passes and axe reports no contrast violations. Test expanded disclosures as well as the initial page state, because they can place additional text over the image.
- **Evidence, controlled comparison**: compare the same text boxes before and after removing bright details from the image. If the text also moves or gains a scrim, the comparison cannot isolate the cause. A more direct test plants a small white dot under a word. Keep it small enough to fall below the p99 tail, then verify that the line-maximum check catches it. Apply that check to every text element over art at every tested width; checking only the hero title on phones leaves desktop captions unprotected.
- **Evidence, ordinary content**: inspect unmodified artwork for small reflections or painted highlights beneath headings, captions and introductory text. A box can pass p99 while its line maximum fails. Locate and view each failing feature before changing the image. Recheck the edited image using the same boxes and capture conditions.
- **Falsifier**: (1) After removing the suspected bright features, a persistent p95-p99 gap of more than about one contrast-ratio point challenges the proposed explanation and requires inspection of the remaining pixels. (2) If a p99 failure comes only from pixels between lines or glyphs, with no letter stroke over them, the box-level check is too broad; use a glyph mask rather than returning to p95. (3) If the line maximum fails because of isolated compression or anti-aliasing artefacts with no visible feature beneath the words, use a glyph mask and a stated minimum feature size, such as 2 x 2 px at DPR 1, rather than relying on a percentile alone.
- **Generality**: hero images, banners and art windows often carry text. Painted, generated and photographic images can all contain small bright details. Image-backed text needs explicit review, and a convenient statistic copied from the brief can accidentally become the acceptance rule.
- **Ledger**: VALIDATED for the percentile-tail mechanism: a planted feature below the percentile tail demonstrates why p99 alone is insufficient. Acceptance requires both the percentile check and the extreme-pixel check, with the glyph-mask and feature-size falsifiers considered.
- **Dedup**: qa-019 KEEP (measuring flat-colour contrast through axe or computed styles; this skill addresses raster backgrounds). qa-010-fix-pattern KEEP (remediation for flat-colour failures). tooling-004 KEEP (which capture the checker reads when art is sticky; this skill defines the statistic). media-007 KEEP (the scrim's effect on the artwork beneath and beyond the words, which must be considered alongside contrast).
- **Tags**: wcag, contrast, text-over-image, percentile, measurement, axe-limits, apertures, accessibility
- **Status**: active (VALIDATED)

### tooling-004: Judge From Captures That Show What a Visitor Sees: Viewport Shots at Named Scroll Positions Whenever a Layer Is Sticky or Fixed [VALIDATED]
**Rule**: A full-page screenshot, or an element screenshot taller than the viewport, can capture a sticky or fixed layer at only one scroll position. The rest of its container may show whatever lies behind it. Before a capture drives a decision to remove, shrink or rework a design, confirm that it shows what a visitor at that width sees. For any sticky or fixed layer, such as an art window behind scrolling content, a heading rail or a pinned band, add viewport captures at named scroll positions: the container's top, middle and foot. Judge from those captures and state any full-page capture limitation in the report. Every pixel checker, including text-over-art contrast checks, style probes and layout audits, must read the same viewport captures or risk grading a page no visitor sees.
- **Evidence**: a bicycle-parts company's guide illustrates the risk. The design calls for a photograph held behind scrolling instructions on phones. A full-page screenshot shows a flat background below the photograph's first screen, so a reviewer removes the sticky treatment and replaces it with a severe cover crop. If every checker also captures only the full page from the top, or one tall element, none establishes what the visitor sees while scrolling through the guide.
- **Evidence, capture comparison**: implement the viewport-height sticky window, then capture the container's top, middle and foot separately. Compare the same narrow strip of the art window in those captures and the full-page image. A nearly uniform strip in the full-page image, alongside visible photographic variation in the viewport captures, demonstrates that the full-page image misrepresents the scrolled experience. Move all pixel checks to the viewport captures before judging the design.
- **Scope**: desktop Chromium has no collapsing mobile browser toolbar, so its captures cannot establish whether a dynamic-viewport seam appears beneath a sticky layer on a phone. Report that check as not run unless it was tested in a suitable environment, such as a real device.
- **Falsifier**: a full-page capture shows the viewport-height sticky artwork behind its content at every depth, or the viewport captures at the container's top, middle and foot reveal no difference relevant to the decision. In that case, the claimed capture limitation has not been demonstrated for that setup.
- **Generality**: sticky headers, heading rails, pinned bands and art windows are common page patterns. Full-page captures are convenient review artefacts, but their limitations can quietly become design constraints if reviewers never compare them with the visitor's viewport.
- **Ledger**: VALIDATED for the capture mechanism: compare a full-page image with viewport captures of the same built page and show where the former replaces visible artwork with the underlying background.
- **Dedup**: tooling-003 KEEP (reading computed CSS rather than source). qa-012 KEEP (animation-frame variance in canvas comparisons). quality-001 KEEP (when and at which widths to capture after deployment; this skill selects the capture type for sticky layers). Scroll-handler implementation remains a separate concern. qa-031 KEEP (the contrast statistic; this skill defines the capture it reads).
- **Tags**: screenshots, playwright, full-page, viewport, sticky, review-measurement, capture-limitations, qa
- **Status**: active (VALIDATED)

## Skill Registry: product-page review additions

| ID | Section | Status | Added | Source |
|------|---------|--------|-------|--------|
| media-005 | Media / Art direction | active, VALIDATED | Art review | Product-page review |
| qa-031 | Quality / Accessibility (text over art) | active, VALIDATED | Contrast review | Product-page review |
| tooling-004 | Tooling / Review captures | active, VALIDATED | Capture review | Product-page review |

## NEW SKILLS: gate-log provenance

Source: build-verification review. Derive provenance from build identities, served responses, Lighthouse `fetchTime` fields and git rather than relying on a reviewer's narrative. Treat timestamps as supporting evidence, not proof of build identity. The core rule is validated; the narrower log-reuse clause remains provisional and has a promotion check below. Score magnitudes are not evidence of provenance.

### tooling-005: A Gate Log Names the Build It Graded: Print the Served Tree's Hash First, and Re-run Every Log Whose Hash Is Not the Hand-Off's [VALIDATED]
**Rule**: Every verification log, including build, test battery, axe, Lighthouse, contrast, coverage and probe logs, prints the identity of the exact build it checked as its first line: the whole-tree hash of the served directory, computed by one fixed command, and the commit. For example, for a build output directory named `dist`, use `find dist -type f | sort | xargs md5sum | md5sum`. The hand-off states the final build's hash. Re-run any log whose hash differs or is missing, subject to the documented scope clause below. Order the hand-off so nothing changes the build after verification: commit, including hooks; create the final build; run the full verification suite; write the report. Modification times are not a substitute. A commit hook's stash and restore can rewrite source timestamps and trigger a rebuild, while a late fix can leave an older log beside a newer build. The hash, not the clock, identifies what a log supports.
- **Scope clause (PROVISIONAL; where the page specification sets a verification budget, that specification governs)**: re-run logs whose subjects the intervening diff can affect. A log stamped with an earlier commit may support the hand-off when `git diff --stat <its commit> <hand-off commit>`, followed by inspection of the actual diff and dependencies, establishes that nothing changed that its subject loads. Consider modules, components, styles, data and build scripts. For whole-page measures such as Lighthouse, byte size or layout shift, include every relevant served asset and string. Record the diff and dependency argument beside each reused log. Re-run every affected check on the final build. A reviewer need not repeat a check already stamped with the final hash beyond a small independent sample. Repeating an unaffected suite consumes the verification budget without broadening what the suite can detect.
- **Evidence**: a garden-supply shop's how-to hub illustrates two routes to stale evidence. A contrast log may precede a late source edit, or test and Lighthouse logs may precede a commit hook that triggers a rebuild. A hand-off claiming that all checks ran against the final build cannot be established by a hash absent from those logs. Re-running permitted checks can recover evidence; a verification budget may prevent repeating every expensive check.
- **Evidence, direct identity test**: commit and build first, then run each check through a wrapper that writes `dist <hash> commit <sha>` as its first line and preserves the command's exit status. Compare every log with the currently served tree. Plant a one-byte source change and rebuild after verification: the provenance check must reject the old logs. Restore the source and rebuild: the original identity should return for a reproducible build. Fetch the served files and compare their bytes with the hashed output to establish that the server uses that tree. Lighthouse `fetchTime` can remain unchanged when a later build leaves the old report untouched, so timestamp ordering alone will not catch the mismatch. Independently re-run selected checks against the served build.
- **Evidence, scope-clause exercise**: on a ceramic studio's site, a late change confined to a gallery-positioning calculation may require rerunning the affected visual probe without repeating unrelated checks. Record why each reused check cannot depend on that calculation, rerun the affected probe, and independently sample the test battery, axe and console output. Also test concerns outside the existing suite; repetition does not expand coverage. Changes to shared layouts, strings or other pages require a fresh dependency review because they can alter shared chunks, page bytes or layout shift even when the gallery code stays unchanged. Similar measurements on another build support the argument but do not prove it for every check.
- **Falsifier**: every log carries the final hash, yet a rerun against actual server responses catches a defect the corresponding check previously missed because it read a cache, another root or a different build. The hash then identifies the wrong object. Bind identity to served responses, using a build marker in the HTML as deploy-007 does for deployments.
- **Falsifier (3), for the scope clause**: a reused check gives a different verdict when rerun on the hand-off build, after accounting for declared sampling variability. The dependency argument missed a path such as a shared stylesheet, data file, build script or chunk boundary.
- **Generality**: late fixes, commit hooks and final rebuilds can all separate verification logs from the build being handed over. A log's age cannot establish that it describes the final output. Record build identity as part of the normal verification process rather than adding it only after a mismatch.
- **Ledger**: VALIDATED for the core identity rule through the planted-change test, restoration, served-byte comparison and independent reruns. The scope clause remains PROVISIONAL. Promote it only after a later independent review reruns at least one reused check on the hand-off build and obtains the same verdict, without triggering its falsifier. Keep that evidence attached to the dependency argument.
- **Dedup**: running checks before hand-off is necessary; this rule additionally binds each log to its build. deploy-007 KEEP (the corresponding principle for live deployments, using a probe path, build marker and commit). qa-030 KEEP (proving a check can fail; this proves which build it judged). tooling-004 KEEP (which capture a checker reads; this identifies which build).
- **Feedback**: on a regional bakery chain's site, consistent build hashes and commit stamps would let a reviewer distinguish earlier measurements from final evidence across a restart or interrupted review. If the working tree is dirty, record that explicitly alongside the served-tree hash; the commit alone cannot identify uncommitted changes. Stamp auxiliary logs as well as the main report.
- **Tags**: gates, provenance, evidence, hash, hand-off, measurement, stale-claims, verification-budget, reuse, diff-reach
- **Status**: active (VALIDATED)
## Skill Registry: product-page review changes

| ID | Section | Status | Added | Source |
|------|---------|--------|-------|--------|
| tooling-005 | Tooling / Review evidence | active, VALIDATED | Review consolidation | Product-page review |
| media-005 | Media / Art direction | active, VALIDATED; includes content states | Review consolidation | Product-page review |
| qa-031 | Quality / Accessibility (text over art) | active, VALIDATED; includes p99 and the line maximum | Review consolidation | Product-page review |
| tooling-004 | Tooling / Review captures | active, VALIDATED | Review consolidation | Product-page review |
| aeo-010 | Agent-Readiness | Invalid (RETIRED) | Earlier guidance | Product-page review |

## NEW SKILLS: marks and scrims over cover-fit art

These entries describe lessons from reviewing product pages. When a review reaches its iteration cap with unresolved issues, present the current build and those issues to the site maintainer for a decision. Derive each finding independently from artifacts and written criteria, using logs, captures, source code or arithmetic rather than accepting another reviewer's reasoning. Each entry includes evidence, a falsifier, a generality claim and a ledger state. Score magnitudes are not evidence. Project-specific records are omitted.

### media-006: Size Marks Drawn Over Cover-Fit Art in the Art's Displayed Units, Never in the Overlay's Own [RETIRED: the narrowed form re-entered as media-009 (PROVISIONAL)]
**Rule**: When an overlay draws marks that must match, or sit inside, an image shown with `object-fit: cover` or `background-size: cover`, size the marks from the scale at which the image is displayed. Examples include hotspots on a kitchen-equipment photograph, annotation lines on a bicycle-parts diagram or location markers on a garden layout. For a box W × H and an image w × h, the cover scale is `max(W / w, H / h)`. An SVG viewBox follows its own viewport and scaling rules, while CSS px stay fixed in CSS coordinates. In either case, the ratio of mark to art can drift whenever the box's aspect changes or a state changes its height, such as an opened disclosure, a script-off fallback, a sticky window or a resize.

Hold the ratio one of two ways: express each mark's size as a constant times the cover scale, or hold the box's size across states so the cover scale cannot change. For SVG strokes, `vector-effect: non-scaling-stroke` lets you set the displayed stroke width explicitly from the computed cover scale. If using viewport units, use the same viewport units that size the image's box. Then measure the marks in the art's own pixels, against the size at which the art paints comparable marks, at every named size, in every state, at DPR 1 and 2.

- **Evidence**: Review measurements exposed three distinct triggers for drift: sizing against a narrower overlay stage instead of the image's actual aperture, drawing strokes in viewBox units over a cover-fit image at a different aspect ratio, and opening a disclosure that enlarged the image's box while the overlay marks kept their CSS size. Calculating the actual cover scale explained the direction of each change. Scaling strokes with the displayed art corrected the first two cases; holding the image box's height corrected the state-dependent case. Deliberately restoring the old sizing or removing the height constraint reproduced the failures.
- **Evidence, later check (the falsifier)**: A live WebGL overlay used widths proportional to the cover scale but still failed its stroke-width band on compact screens. Its reduced rendering tier allocated one backing-store pixel per CSS pixel, even on a DPR-2 screen. The same geometry rendered through SVG at device resolution passed. Increasing the canvas backing-store resolution improved the result, but the smallest viewport still failed. Pass and fail followed how much of the source image one raster pixel represented. The sizing rule worked where the raster was fine enough; the original falsifier had excluded subpixel device rendering but had not accounted for a canvas rendered below device resolution.
- **Falsifier**: (1) A box change with a known cover-scale ratio produces a change in art-relative mark size that differs from the predicted ratio by more than 2%; or (2) marks sized as a constant times the cover scale leave a predeclared, artwork-specific width band at a named size at DPR 2. For fixed-size marks, increasing the cover scale by a factor of r predicts an art-relative size change by `1 / r`. Originally, DPR-1 cases with marks narrower than one device pixel were excluded because antialiasing dominates their measured footprint. The narrowed claim treats resolution as the resolution of the surface into which the marks are rasterised: the device surface for SVG and CSS, or the backing store for canvas. Establish the minimum usable raster resolution before rerunning the check; do not infer a universal cutoff from one artwork.
- **Generality**: Overlays on cover-fit imagery are common in product-photo hotspots, annotated diagrams, layout markers and figure layers on hero or section art. Their units are often chosen at one viewport. Drift appears at another aspect ratio or in another state, so a check at the design width can pass while the implementation remains wrong. Measure the relationship rather than relying on visual inspection alone.
- **Ledger**: RETIRED. The original falsifier fired on a canvas whose reduced tier rendered below device resolution. Comparing SVG and canvas on the same build isolated raster resolution as the limiting factor, but narrowing a falsifier after failure cannot validate the revised claim. The narrowed claim requires an independent check against criteria recorded before the rerun. Earlier evidence supported the sizing mechanism through predicted scale changes and deliberately broken variants; it did not establish the claim for every rendering surface.
- **Dedup**: media-005 KEEP (determines which composition a box gets and how much of the image shows; this skill concerns what is drawn over it). qa-010 KEEP (the measurement method; this is the cause and sizing rule). tooling-004 KEEP (captures of sticky art layers). tooling-003 KEEP (computed style alone cannot establish a mark's size relative to the displayed art).
- **Tags**: object-fit, cover-scale, svg, viewbox, vector-effect, overlays, responsive, art-direction, states, figures, canvas, raster-floor
- **Status**: Invalid (RETIRED; retained for audit). A claim whose falsifier fires must be retired and may re-enter in narrowed form as PROVISIONAL. The narrowed claim, concerning display units on surfaces above an established raster floor, re-enters as media-009 with its falsifier recorded before any rerun. Until that claim is validated, size marks by display scale and verify the actual raster output.

### media-007: Grade a Scrim Over Art by What It Does to the Art, Beneath and Beyond the Words, Not Only by the Words' Contrast [VALIDATED]
**Rule**: A scrim, such as a translucent fill or feathered shadow behind text over art, blends toward its own colour. It does not necessarily darken the image. Where the art is darker than the scrim colour, the scrim can lighten it. Where the scrim extends past the words, it can paint a visible panel onto the picture. Text-contrast checks, including qa-031 and axe where applicable, do not assess that visual cost.

Grade every scrim with a pair of text-transparent captures, scrim on and scrim off, at each named size and state. Check two statistics: (1) under each line box, the scrim does not make the ground lighter, with an on/off luminance ratio at most 1.0; (2) beyond the words' line boxes plus a declared feather margin, for example 48 px, the art remains substantially unchanged, with an on/off ratio at least 0.95 in every column. These are proposed visual acceptance thresholds, not accessibility standards. Declare whether each is blocking before testing.

A scrim that fails (1) needs a colour darker than the ground it covers if darkening is required. A scrim that fails (2) should be bounded to the elements holding the words: put the fill on a text element that shrinks to its own measure rather than on a full-width container. A deliberately broken variant carrying the failing scrim must fail the statistic it is intended to test.

- **Evidence**: Paired captures exposed two failure modes. A translucent coloured scrim lightened dark areas beneath headings, even though it darkened brighter areas elsewhere. Removing it preserved the required text contrast. A separate full-width scrim darkened decorative artwork well beyond the words and lightened some darker areas within its box. Measuring only its average darkening had missed both costs. For an invented ceramic studio, the equivalent check would compare the artwork around a collection title with and without its backdrop, including areas where no text appears.
- **Evidence, promotion check**: Moving the fill and a tighter feather onto the text elements preserved the declared text-contrast targets while passing the outside-art ratio across desktop sizes, sticky states and disclosure states. Restoring the full-width scrim made the outside statistic fail. The bounded scrim still lightened some ground beneath the words. That result was reported as unresolved because the under-text statistic had not been adopted as a blocking requirement; the validation therefore supports the bounded-extent remedy, not a claim that both statistics passed. Removing the broad shadow also exposed a discontinuity in a nearby image fade. The full-page check caught it, showing why a local scrim change needs a surrounding-art review.
- **Falsifier**: (1) A scrim bounded to the words' line boxes cannot preserve the full-width version's required text protection across the declared viewport sizes and states, showing that the broader extent was necessary; or (2) the 0.95 outside ratio rejects an edge that viewers comparing the on/off captures at normal display size cannot perceive, showing that the threshold is too strict. Record the required contrast, p99 sampling method and maximum background-luminance limit before the comparison.
- **Generality**: Text over imagery often leads designers to add a scrim, and text-only checks can reward stronger protection without revealing damage to the surrounding art. A shared scrim colour may be lighter than the darkest parts of an image. A regional bakery chain's customer-story banner, for example, needs both readable words and a photograph that does not acquire a visible rectangular panel. Measure both outcomes.
- **Ledger**: VALIDATED for the bounded-extent remedy: the declared outside statistic passed, the text retained its required contrast and a full-width variant failed the outside check. Falsifier (1) was tested and did not fire. Falsifier (2), concerning an imperceptible edge rejected by the threshold, remains untested. Lightening beneath the words was observed and remains a separate acceptance decision. Validation must state that limit rather than imply that every proposed criterion passed.
- **Dedup**: qa-031 KEEP (grades the words over art; this grades the scrim's cost to the art). radial-backdrop-pattern-for-text-on-banner-001 KEEP (a text-bound radial backdrop is one implementation of bounded extent). design-input-004 KEEP (plans tokens before markup; this determines how a scrim colour is judged against the actual art). media-001 KEEP (LCP media governance).
- **Clause: the veil's SHAPE, not only its extent.** Over structured art, such as curved garden paths, foliage or decorative pottery patterns, a rectangular veil can reveal its outline even when feathered and bounded to the words. Shape it to the text with a radial or elliptical mask whose transparent rim lies at least about 4rem beyond the text box, checked at the text box's corners, or use a layered glyph halo in the ground colour. For a circular boundary, the reach along each axis at a diagonal point is about 0.71 of the radius; an ellipse likewise needs a corner check rather than a side-only measurement. Recheck text contrast after changing the shape. Verify the intended form from computed styles: no rectangular background or box-shadow, a radial pseudo-element when that technique is chosen, and adequate reach around the text. A pixel step across the edge also measures the underlying art and cannot reliably identify the veil's shape by itself. A rectangular variant and a deliberately undersized halo should fail the form check. **Ledger (clause)**: VALIDATED for distinguishing the intended form from those broken variants; visual inspection remains necessary to judge its fit with the artwork.
- **Tags**: scrim, overlay, text-over-image, art-direction, contrast-cost, panels, measurement, counterweight
- **Status**: active (VALIDATED for bounded extent and form checks, with the stated limits)
## Skill Registry: product-page review changes

| ID | Section | Status | Added | Source |
|------|---------|--------|-------|--------|
| media-006 | Media / Art direction | Invalid; retired and re-entered with narrower scope as media-009 | Initial review | Product-page review |
| media-007 | Media / Art direction | active, VALIDATED | Initial review | Product-page review |
| qa-010 | Quality (Visual Fidelity) | active [PROTECTED]; scope note VALIDATED | Existing entry | Product-page review |
| tooling-005 | Tooling / Gate evidence | active, VALIDATED; scope clause PROVISIONAL | Initial review | Product-page review |
| qa-031 | Quality / Accessibility (text over art) | active, VALIDATED; evidence and a pointer to media-007 added | Initial review | Product-page review |

## NEW SKILLS: live layers over art-directed images, and the device tier in headless tests

These entries cover reviewing a page that layers live graphics over artwork. Each entry is grounded in artifacts and written criteria, using logs, captures, source inspection or arithmetic rather than relying on another reviewer's reasoning. Each entry carries evidence, a falsifier, a generality claim and a ledger state. Provisional entries name the check needed for promotion. Score magnitudes are not evidence.

### media-008: A Script Layer Derived From One Composition of an Art-Directed Image Draws Only While That Composition Is Showing, Checked Live [VALIDATED]
**Rule**: When a script layer's geometry comes from one composition of an art-directed image, such as continuation lines taken from a wide illustration's edge, hotspots placed on a landscape photograph or a mask cut from one crop, the layer is valid only while that composition is on screen. Keep two checks live for the layer's whole life: (1) the media condition that boots the layer stays subscribed in both directions, tearing the layer down when it stops matching and rebuilding it when it matches again; never use a test read once at boot with a one-shot listener for the upward change; (2) before drawing, confirm that the image actually displayed is the one the data came from, using its `currentSrc`, or `naturalWidth` x `naturalHeight` when those dimensions uniquely identify the source. Draw nothing otherwise, because the `<picture>` breakpoint and the layer's query can live in different files, and the displayed source changes after a resize. Test by booting the layer on either side of the art-direction breakpoint and resizing across it in both directions. Print the displayed source beside the layer's state, and introduce a boot-only mutant that the test must reject.
- **Evidence**: A resize probe exposed a layer that continued drawing geometry derived from the landscape image after `<picture>` switched to the phone composition. The layer checked its media query only at boot and used a one-shot listener for the upward transition. It mapped the geometry through the displayed image's box without verifying the source. An equivalent example is a kitchen-equipment maker's resource library: an animated outline continues a counter edge from a wide kitchen photograph, but remains visible after the page switches to a close-up product crop with no matching edge. A persistent media listener and a displayed-source guard address the mismatch.
- **Falsifier**: (1) After adding a live, two-way listener and a displayed-source guard, crossing the breakpoint still leaves the layer drawing against a composition it was not derived from. This can happen if the guard runs inside the media listener before `<picture>` has swapped its source. The check must cover wide-to-narrow and narrow-to-wide transitions and compare the restored layer with a fresh load at the same viewport. (2) A resize within one composition tears down and rebuilds the layer with a visible flash, so the listener introduces a new visual defect.
- **Generality**: Art-directed images often use a portrait crop for phones and a landscape composition for wider screens. Script layers built from one crop, including continuation lines, hotspots, masks and scroll-linked paths, are often tested at a fixed viewport where a boot-time check passes. Device rotation, split screens and narrowed desktop windows can cross the breakpoint after boot, leaving the layer attached to the wrong composition.
- **Ledger**: VALIDATED. The resize check confirmed that the corrected layer stopped drawing on the incompatible composition and resumed on the matching composition. The restored geometry matched a fresh load, and the boot-only mutant failed the check. Falsifier (1) was tested and did not occur. Falsifier (2), flashing during a resize within one composition, remains untested. Validation covers this mechanism; it does not establish that every resize path is free of visual defects.
- **Dedup**: media-005 KEEP: it governs which composition a box serves and which breakpoint drives the switch; this skill governs a separate layer whose data belongs to one composition. media-009 KEEP: it governs mark sizing on the rendering surface; this skill decides whether a layer may draw at all. tooling-004 KEEP: it governs captures. Container-resize handling alone does not establish that the layer still matches the displayed image.
- **Tags**: art-direction, picture, matchMedia, resize, live-layers, webgl, canvas, overlays, breakpoints, cross-component
- **Status**: active (VALIDATED)

### tooling-006: In Headless Tests, Force the Tier a Real Device Runs Before Measuring a Tiered WebGL Layer's Fidelity [PROVISIONAL]
**Rule**: When headless Chromium uses a software rasteriser such as SwiftShader, a layer that tiers on `failIfMajorPerformanceCaveat` or the renderer string may run only its fallback tier. The intended device tier then goes unmeasured. Before reporting that tier as "not run", force its code path in the test harness: in an init script, request the context without `failIfMajorPerformanceCaveat` and hide the renderer string by returning null for `WEBGL_debug_renderer_info` and a neutral value for `RENDERER`. Confirm the forced tier from the layer itself before trusting any capture, using the canvas's backing-store pixels per CSS px, frames drawn per second and any stand-down flag. Then run the same fidelity probes, including stroke widths, mark sizes, positions and coverage, in both tiers and report both. Timing under a forced tier still measures the software rasteriser, so real-GPU frame rate remains "not run".
- **Evidence**: A tiered layer's headless measurements covered only the fallback path, while its intended device path was reported as untested. Tier selection depended on the context caveat request and a software-renderer check, and the paths used different backing-store resolutions. Forcing the device path exposed different compact-layout fidelity results, while the narrowest layout still failed. For an equivalent bicycle-parts guide, animated route marks could appear too thin in the fallback tier yet meet the visual target at the device tier's higher resolution. Forcing the path makes that difference measurable without establishing real-device timing.
- **Falsifier**: (1) A headed browser on a real GPU, with its renderer verified, measures the same layer's stroke widths or mark sizes at the same viewport and DPR outside a tolerance declared before testing. That would show that software rasterisation is not an adequate fidelity substitute at equal resolution. (2) The layer also tiers on a condition the init script does not control, such as slow startup frame intervals, and falls back while the report labels it the device tier. Inspecting backing-store resolution and stand-down state throughout the run catches this second failure; a forced-tier report without that verification is invalid.
- **Generality**: WebGL and canvas layers are commonly tested in headless Chromium. Where the test environment uses software rendering, hardening logic may reject the context or select a minimal tier, leaving another rendering path untested. Forcing that path can support fidelity checks while real-device verification remains outstanding. Without this distinction, a team may change the product merely to accommodate the test environment.
- **Ledger**: PROVISIONAL. Forcing and independently checking the tier demonstrated that the alternate rendering path could be measured. Promote when a real-GPU run agrees with the forced fidelity readings within a predeclared tolerance, or when forcing finds a device-tier defect in another build that fallback-only tests passed.
- **Dedup**: tooling-004 KEEP: it governs captures that show what a visitor sees when a layer is sticky; this skill selects the rendering path being measured. qa-010 KEEP: it governs the style probe itself; this skill determines which tier it measures. qa-012 KEEP: it governs animation-frame variance in canvas diffs. ace-010 KEEP: it governs timing statistics; a forced tier yields no real-device timing evidence.
- **Tags**: webgl, headless, swiftshader, tiers, testing, playwright, measurement, device-path, fidelity
- **Status**: active (PROVISIONAL)

## Skill Registry: live-layer review changes

| ID | Section | Status | Added | Source |
|------|---------|--------|-------|--------|
| media-008 | Media / Art direction | active, VALIDATED | Live-layer review | Product-page review |
| tooling-006 | Tooling / Measurement | active, PROVISIONAL | Live-layer review | Product-page review |
| media-007 | Media / Art direction | active, VALIDATED | Initial review | Product-page review |
| media-006 | Media / Art direction | Invalid; retired and re-entered with narrower scope as media-009 after a reduced canvas tier exposed the need to distinguish the raster surface from displayed scale | Initial review | Product-page review |

## NEW SKILLS: boot cost of live layers, fragment-opened disclosures, mark units re-entered

These entries cover a final review before a component is reused elsewhere, including keeping reruns bounded (tooling-005). Each entry is grounded in artifacts and written criteria, using logs, captures, source inspection or arithmetic rather than relying on another reviewer's reasoning. Each entry carries evidence, a falsifier, a generality claim and a ledger state. Provisional entries name the check needed for promotion. Score magnitudes are not evidence.
### perf-002: A Live Layer That Boots on Scroll Is Bounded by Its Longest Boot Task, Not by Its Frame Cost: Slice the Boot So No Task Exceeds 50 ms [PROVISIONAL]
**Rule**: A decorative live layer (WebGL or canvas) that starts when its section scrolls into view does its setup (context, shaders, buffers, and any geometry derived from the layout: route pools, collision tests, packing) while the visitor is scrolling. Its cost is the longest main-thread task during that boot, which neither Lighthouse in navigation mode (when the layer is below the fold at load) nor a per-frame trace (steady frames only) sees. Split the boot into macrotasks of at most 50 ms each at 4x CPU, yielding with `setTimeout(0)` or a `MessageChannel` post. Use `scheduler.yield` only when feature-detected; do not rely on `requestIdleCallback` alone because browser support varies. Defer what the first frame does not need, and reject pairwise geometry candidates by bounding box before any fine sampling. Measure it: install a `longtask` PerformanceObserver by init script, load the page, set 4x CPU, scroll to the layer and record every task for about 12 s. Report the longest task and the blocking time over three runs, beside the previous build served the same way as a control.
- **Evidence**: A page review found that a live decorative layer caused long tasks when scrolled into view, despite passing navigation-time Lighthouse checks. The same component exposed its setup cost when it appeared inside Lighthouse's measurement window on a component preview page. The performance requirement covered boot tasks, but the page checks had not carried that requirement forward when startup moved from interaction to visibility. A suspected contributor, not isolated as the cause, was layout-derived route generation that sampled every candidate against every existing line.
- **Falsifier**: (1) After the boot is sliced so that every task during it reads at most 50 ms at 4x CPU (three runs), a tap issued during the boot window still waits more than 200 ms for its next paint (Event Timing or `web-vitals` `onINP` at 4x CPU): long tasks do not explain the remaining wait, and the rule's measure is insufficient. Investigate other contributors, including rendering or GPU synchronization. (2) Slicing to 50 ms cannot be reached without delaying the layer's first frame by more than 1 s beyond the unsliced boot at 4x CPU, so the bound must be restated as a ceiling with that tradeoff named.
- **Generality**: A kitchen-equipment maker's resource library might reuse a decorative component across product guides. Moving its boot off the load path protects initial loading but also places the work outside navigation-only checks. Layout-derived geometry can make setup more expensive as features accumulate, and finer collision sampling can multiply that cost. A shared component carries the regression to every page that uses it.
- **Ledger**: PROVISIONAL. Slicing reduced the measured setup work, but the visible run still exceeded the bound. A proposed explanation attributed the remaining task to the software compositor's first display of the canvas; that explanation remains unverified on hardware. A control must hide every live layer that the probe's scroll positions can reveal, or unrelated setup work can contaminate it. Promotion requires three runs at 1440x900 and 390x844 meeting the 50 ms bound, a deliberately unsliced version that fails, and a tap-during-boot check that does not trigger falsifier (1). Use a hardware-GPU run or a control that separates compositor cost, and report any excluded cost explicitly. Until then, the remedy remains provisional.
- **Dedup**: ace-010 KEEP (how to read a CPU-timed check over runs; this entry names the boot task that steady-frame traces miss). tooling-006 KEEP (which rendering tier a probe measures). Navigation-time rendering costs and font LCP remain separate concerns.
- **Tags**: webgl, canvas, boot, long-tasks, INP, main-thread, scheduling, scroll, live-layers, measurement
- **Status**: active (PROVISIONAL)

### perf-003: Open a Fragment-Targeted Disclosure While the Parser Is Still at It, and Test the Fragment Load, Not the Click [VALIDATED]
**Rule**: When a URL fragment names a disclosure that should arrive open (a `<details>` FAQ item, an accordion panel, a tab), apply the open state during parse, immediately after the disclosure group's markup and before anything below it is parsed. Use a small inline script (`<script is:inline>` in Astro) that reads `location.hash`, finds the element and sets `open` for `<details>`, or applies the appropriate selected state for another widget. Keep the deferred listener for `hashchange` only, since those changes happen after initial navigation. A module or deferred script can run after the document is laid out and the browser has scrolled to the fragment, so opening then pushes on-screen content down as a layout shift with no recent input. Under a hashed script CSP, add the new inline script's hash and confirm the build's hash count rose by one. Test with a buffered `layout-shift` PerformanceObserver added by init script: load the page with each fragment at a desktop and a phone size and sum the entries whose `hadRecentInput` is false (must be 0). A click test cannot see this defect, because shifts within 500 ms of input are excluded from CLS. A mutant that restores the deferred opener must go red.
- **Evidence**: A page's FAQ opened its fragment target from a deferred module on load and on `hashchange`. The implementation assumed that opening moved only content below the question, but that content was already visible. Fragment-load checks detected shifts in the following questions, imagery and a sign-up form at desktop and phone sizes. Click-only checks reported zero CLS and missed the defect. Moving the initial opener directly after the disclosure markup removed the measured shifts; restoring the deferred opener reproduced them.
- **Falsifier**: (1) With the inline opener placed directly after the disclosure group, a fragment load of a lower item at 390x844 still records layout shift without recent input above 0.01 attributable to the disclosure. For example, the browser might paint and scroll before the parser reaches the inline script on a long or streamed document. In that case, “during parse” is not early enough: arrange for the initial state to be available before paint where possible, or apply fragment scrolling after opening. A server cannot read a URL fragment directly. (2) The buffered observer reads 0 on fragment loads while a frame sequence of the same load shows content below the opened item moving on screen, meaning the measurement misses the shift.
- **Generality**: A bicycle-parts company's guides might link directly to compatibility questions inside an FAQ. Shared answer links make fragment navigation a normal entry path. Widget behaviour commonly lives in deferred scripts, so initial URL-driven state can accidentally land there too. Click-driven tests pass because they exercise a different timing path.
- **Ledger**: VALIDATED for the tested disclosure pattern. Fragment loads opened the intended question with zero measured CLS at desktop and phone sizes, while a deliberately deferred opener failed the same check. The pattern also held on another page. Falsifier (1) did not fire at the tested sizes; falsifier (2), comparing the observer with a frame sequence, remains untested. For reuse, check multiple deep-linked questions at 1440x900 and 390x844, confirm the intended open state and zero CLS, and verify that restoring deferred initialization makes the check fail.
- **Dedup**: Progressive enhancement remains the default, but initial state supplied by the URL must be ready before deferred behaviour when it affects layout. `astro-set-html-script-inert-gotcha-canonical-001` in `05_automations/resource-hub-maintenance/skillbook.md` KEEP (scripts inside `set:html` CMS bodies do not run; initialise those widgets from a page-level script). qa-030 KEEP (red mutants; this entry names the missing test case: the fragment load). media-005 KEEP.
- **Tags**: details, accordion, disclosure, fragment, deep-link, CLS, layout-shift, hadRecentInput, csp, measurement
- **Status**: active (VALIDATED within the tested conditions)

### media-009: Mark Weight Over Cover-Fit Art Is Set in the Art's Displayed Units, and Holds Wherever the Raster Is Fine Enough to Show It [PROVISIONAL]
**Rule**: When an overlay draws marks that must keep their weight relative to an image shown with `object-fit: cover` (a figure's strokes and stars over a background image, hotspots on a photograph, annotation lines), express each mark's size as a constant times the image's displayed scale. The cover scale is `max(W / w, H / h)`, where uppercase dimensions describe the display box and lowercase dimensions describe the source image. Use, for example, `calc(c * var(--plate-px))`, where the variable carries that scale as a CSS length, or the layer's measured scale. Never use the overlay's own CSS px or viewBox units as the independent sizing basis, because the ratio of mark to art can drift with the box's aspect or state. The claim covers raster surfaces fine enough to show the width: the device for SVG and CSS, the backing store for a canvas. Test cases in which one raster pixel spans more than about 1.4 source-image px are below the raster floor and are reported as unmeetable, not graded. The claim is about the unit. Whether a mark passes an absolute band also depends on the nominal width's headroom over the band's floor: a thin antialiased line's measured half-max can read below its nominal width. Choosing that value is a separate decision.
- **Evidence**: Earlier checks found that marks sized in overlay units changed weight relative to the image as the display box or disclosure state changed. Image-scaled marks held their relative weight more consistently, while a deliberately viewBox-sized version failed. A reduced-resolution canvas exposed a separate raster limit. Further checks showed that image-scaled marks could remain consistent across sizes yet narrowly miss an absolute minimum width because the chosen nominal width left too little headroom. That is a value-selection issue, not evidence that the scaling unit failed.
- **Falsifier** (register before any re-run): (1) On a surface where one raster pixel spans at most 1.0 source-image px, the same set of marks sized by this rule, read as each test case's median half-max width in source-image px, differs by more than 0.3 source-image px between any two declared sizes or states with the nominal width unchanged; or (2) a mutant that sizes the same marks independently in CSS px or viewBox units varies across those cases by no more than the rule's own marks do, so the chosen unit does not explain the stability.
- **Generality**: A garden-supply shop's how-to hub might overlay annotations on cover-fit photographs. An overlay tuned at one viewport can drift when the image is cropped into another aspect ratio or an expandable panel changes its box. Reusing the component with new photographs makes consistent sizing units especially useful.
- **Ledger**: PROVISIONAL. This narrows the earlier claim to unit choice and the raster floor. Promotion requires an independent review of a build whose nominal width has enough headroom above the acceptance floor. Measure per-case median widths at DPR 2 across a declared set of compact viewport sizes and relevant states. The medians must stay within 0.3 source-image px of each other, and the unit-changing mutant described in falsifier (2) must fail. Declare the measurement method and test matrix before running the check.
- **Dedup**: media-006 RETIRED (this replaces it; one concept, narrowed to the unit and the raster floor). media-005 KEEP (which composition a box serves). media-008 KEEP (whether a layer may draw at all). qa-010 KEEP (the probe). tooling-006 KEEP (which tier is measured).
- **Tags**: object-fit, cover-scale, svg, canvas, strokes, raster-floor, overlays, figures, units
- **Status**: active (PROVISIONAL)
## Skill Registry: product-page review changes

| ID | Section | Status | Added | Source |
|------|---------|--------|-------|--------|
| perf-002 | Performance / Live layers | active, PROVISIONAL | Initial review | Product-page review |
| perf-003 | Performance / Layout stability | active, PROVISIONAL | Initial review | Product-page review |
| media-009 | Media / Art direction | active, PROVISIONAL (narrowed replacement for media-006) | Initial review | Product-page review |
| tooling-005 | Tooling / Gate evidence | active, VALIDATED; scope clause PROVISIONAL (rerun checks according to the diff's reach and the agreed verification budget) | Initial review | Product-page review |
| media-008 | Media / Art direction | active, VALIDATED (promoted after its registered check passed) | Initial review | Product-page review |
| media-006 | Media / Art direction | Invalid (retired; replaced by the narrower media-009) | Initial review | Product-page review |
| aeo-012 | Agent-Readiness (inherited guidance) | Invalid (retired here; other copies require separate review) | Initial review | Product-page review |

## NEW SKILLS: generated stylesheets, coupled geometry (closing review)


### tooling-007: A Stylesheet Generated as a String Can Escape CSS Checks: Assert the Computed Value of What It Styles, With No Script Layer Painting Over It [VALIDATED]
**Rule**: CSS that a component assembles in a template string and injects raw (Astro `<style is:inline set:html={...}>`, a `style` element filled by script, a CSS-in-JS string) can escape build, bundler, CSS-linter and type-checker validation unless the pipeline explicitly inspects that output. A lost declaration block turns the selector list into a dangling prelude that the browser drops silently, or joins it to the next rule's selector. Styled elements can then fall back to the property's initial value, such as black for an SVG `fill`. The result can look plausible rather than visibly broken. After any edit to such a string, assert the computed value (`getComputedStyle(el).fill`, `.color`, ...) on every element class the rule targets, on each page that uses the component. Hold off any progressive-enhancement layer that could paint over the static design, and test a deliberately broken variant with the declaration block removed. For server-rendered styles, also inspect a context with page JavaScript disabled; for script-generated styles, allow the style injection while disabling the enhancement layer.
- **Evidence**: A selector-list edit in a generated stylesheet also removed its gradient declaration block. Build, source, accessibility and browser checks passed, but the preview briefly showed black SVG shapes before the live graphics layer covered them. With that layer held off, computed-style checks passed on the repaired version and detected the fallback fill on the deliberately broken version. An illustrative use is the fictional Hearthspoke kitchen-equipment maker's resource library: a static product diagram must remain correct before its animated overlay starts.
- **Falsifier**: (1) A build tool already in the pipeline, such as a linter over the built HTML's inline styles, reports the missing declaration block inside the injected string. In that case, the gap is configuration or coverage rather than an uninspected class of CSS. (2) An existing computed-style check with page JavaScript enabled and the live layer held off already detects the fallback value. In that case, disabling page JavaScript is not what makes the defect visible.
- **Generality**: Component frameworks can generate per-instance CSS strings for gradients and positioned markers. A live layer over a static design can hide defects in that design from browser checks that run only after enhancement starts. Selector-list edits are routine late fixes, and a one-line diff can affect every page that uses the component.
- **Ledger**: VALIDATED for the tested mechanism: the probe passes on the repaired output and fails when the declaration block is removed, while the existing checks miss the defective output. Evidence remains limited to this failure pattern. Narrow the rule if either falsifier applies.
- **Dedup**: tooling-003 [PROTECTED] KEEP (assert rendered values rather than relying only on source parsing; this rule identifies string-injected CSS and the static rendering context). qa-030 KEEP (the deliberate-defect testing discipline used here). media-008 KEEP (when an enhancement layer may draw, rather than whether the design beneath it is correct).
- **Tags**: css, template-strings, set:html, inline-style, computed-style, progressive-enhancement, no-script, svg, verification
- **Status**: active (VALIDATED)

### figure-001: Derive a Coordinate That Must Meet Another From the Value It Must Meet, Never Type It Beside It [PROVISIONAL]
**Rule**: When one element of a solved or designed figure must line up with another (a flow's last node with a target's centre line, a leader's end with its marker, a label's reserved box with the text the browser lays out), compute the dependent value from its source in the solver at build time. Assert the coupling in the figure check (`|end - centre| <= tolerance`, per layout). A typed constant is correct only for the parameters it was typed against. The source moves when the solver's other parameters change, including amplitude, phase, scale and wrapping width, while the typed value stays where it was without any error.
- **Evidence**: A compact diagram used a manually entered target centre while its final node was positioned by a layout solver. After layout tuning, the connector missed the target on phones. Deriving the target centre from the final node (`xc: nodes[n - 1].x` for the compact layout) restored alignment. A related label failure came from reserving the estimated width of the longest text line while the browser laid out a wider wrapping box. A sweep of the other layouts found another manually entered centre with no assertion checking its alignment. For an illustrative business use, the fictional Rimvale bicycle-parts company could encounter this in a guide showing how wheel components fit together.
- **Falsifier**: (1) A designed layout needs a deliberate offset between the two values, such as an art-directed asymmetry. The rule must then allow a named offset from a derived anchor. (2) A coupling assertion would pass on the misaligned build because its tolerance is too loose or it measures the wrong elements. In that case, the assertion also needs correction.
- **Generality**: Figures generated at build time often use per-layout parameters that are tuned visually. A manually duplicated coordinate can become stale when either side changes, and the defect may appear only in a layout that was not inspected.
- **Ledger**: PROVISIONAL. Deriving the coordinate restored alignment, but the regression check still needs proof. Promote when the coupling assertion fails on a deliberately stale coordinate and passes on the derived build, or when the same failure pattern is independently confirmed in another figure.
- **Dedup**: media-009 KEEP (mark weight over artwork, rather than positions). media-005 KEEP (which composition a box serves). qa-030 KEEP (verification of deliberate defects). Cross-file value validation is related but distinct: this rule requires geometric derivation inside a solver, rather than checking that a string belongs to an allowed set.
- **Tags**: figures, layout, solver, build-time, geometry, coupling, single-source, specs
- **Status**: active (PROVISIONAL)

## Skill Registry: product-page closing review changes

| ID | Section | Status | Added | Source |
|------|---------|--------|-------|--------|
| tooling-007 | Tooling / Gate coverage | active, VALIDATED | Closing review | Product-page review |
| figure-001 | Figures / Layout | active, PROVISIONAL | Closing review | Product-page review |
| qa-030 | QA / Guards | active, VALIDATED; clause VALIDATED (a deliberate defect counts only when it is shown to be in effect) | Closing review | Product-page review |
| perf-003 | Performance / Layout stability | active, VALIDATED (promoted after its registered check passed) | Closing review | Product-page review |
| perf-002 | Performance / Live layers | active, PROVISIONAL (reviewed; not promoted) | Closing review | Product-page review |

## NEW SKILLS and UPDATES: business-site build comprehensive review

Source: a post-build review of a business site deployed through Cloudflare Workers and GitHub. Deployment guidance is available in `05_automations/client-site-first-build/runbook_appendix/cloudflare_workers_github_path.md`. Apply these lessons to sites you operate, such as the fictional Mossbasket garden-supply shop's how-to hub. Status is VALIDATED where repeated executed checks support the rule, otherwise PROVISIONAL. Recheck platform behaviour before relying on it in a new deployment.

### UPDATE cf-008: the one preview mechanism is Cloudflare Worker Previews
The rule stands: use one preview mechanism per Worker and confirm its result where the site operator reviews it. Use **Worker Previews** as the default: enable "Builds for Preview branches", set the Preview command to `npx wrangler preview`, declare each required binding in a `previews` block, and set base-config secrets before creating the Preview (cf-010).

Do not combine this with a custom version-alias trigger that depends on preview builds being disabled. In the reviewed behaviour, clearing that setting deleted the preview build configurations, including the custom trigger, and preview branches ran `npx wrangler preview` regardless of the configured Preview command. Verify those behaviours against the platform before depending on them.

Confirm the setup across consecutive CI deployments and at launch. Inspect production triggers separately from preview readiness. For a Worker Preview, use the URL and rendered marker checks described in deploy-007, because the builds API did not expose Worker Preview builds in the reviewed setup.

### UPDATE cf-009: run the simulation as main before the launch merge
Run the clean-clone simulation with `WORKERS_CI_BRANCH=main` before fast-forwarding into main, so production guards and the production-posture step (deploy-009) run locally first. For example, the fictional Clayhaven ceramic studio should test the launch configuration of its class and product pages before merging.

An account-pin guard should reject a local build when the shell exports a different account. To remove those inherited overrides for the build, use `env -u CLOUDFLARE_ACCOUNT_ID -u CLOUDFLARE_API_TOKEN npm run build`. Keep the account check intact.

### UPDATE deploy-007: watch main by build uuid; a commit is not a build identity
A commit-keyed watcher can match a preview build of the same commit or an earlier failed attempt after a retry. Watch the production build by its build UUID, using the build-detail and logs API endpoints for that UUID. Watch a Worker Preview by its URL plus a rendered marker absent from the previous build. This distinguishes both deployment targets and repeated builds of the same source.

### qa-023: A header verifier knows the host class
On Cloudflare-managed preview hostnames, the platform can force its own `X-Robots-Tag: noindex`, replacing the build's value while other configured headers still apply. Recheck this platform behaviour before relying on it.

Accept a valid `noindex` directive on preview hosts; assert the exact intended value on production. Never weaken the production assertion to make a preview pass. For the fictional Brookgrain regional bakery chain, the preview and public location pages therefore require different indexing expectations. Verify the production response directly after the merge.

### port-022: Sort launch-audit reds before acting
Sort every red in an agent-readiness scan into **principled N/A** (greening it would be a false claim, for example `authMd` scopes on a public site or an MCP server card with no MCP server) and **forgotten step** (for example DNS-AID where applicable, once DNSSEC validates). Fix the forgotten ones; record the principled ones with their reasons.

### UPDATE tooling-004: first-screen checks at the visible viewport
A "headline in the first screen" check runs at the VISIBLE viewport: screen space minus browser UI at load, about 375x553 on a small iPhone or 360x560 on Android Chrome. Sweep heights from 540 to 720 when a frame is tied to svh/lvh; include checks at small-phone sizes of 320x568, 360x640 and 375x667.

### account-001: Second-Account Vendor CLIs Run Only Through Allowlist Wrappers and a Repo Pin [VALIDATED]
**Rule**: When the shell exports ambient vendor keys, every second-account call (Wrangler, Sanity, gh or any vendor CLI) runs through a wrapper that builds its environment with `env -i` plus an ALLOWLIST, loads that account's 0600 credentials under prefixed names, and refuses when the repo's pinned `account_id` differs from the loaded credentials' account. Never use a denylist, because the ambient credential file can change. Avoid connectors whose account selection cannot be pinned; use per-command `GH_TOKEN`, never a global account switch. This package's `06_web_tools/wrangler-safe` applies account isolation to Wrangler: it scrubs other `CLOUDFLARE_*`/`CF_*` variables, reads your key file without sourcing it, and refuses an `account_id` pin mismatch.
- **Evidence**: Ambient environment variables can override a vendor CLI's own authentication profile. Verify that the wrapper removes all ambient vendor credentials and rejects account-pin mismatches in both directions.
- **Falsifier**: A wrapped call reaches the ambient account, or a denylist wrapper remains complete despite repeated changes to the ambient credential file.
- **Tags**: credentials, account-separation, cloudflare, wrangler, first-build
- **Status**: active (VALIDATED)

### account-002: Prove Account Separation With a Logged-In Wrong-Account Call, Plus a Census That Prints Its Blind Spots [VALIDATED]
**Rule**: `wrangler deploy --dry-run` never authenticates, so it cannot prove separation. Run a logged-in, non-mutating call (`wrangler deployments list`) with the WRONG credentials against the pinned account: the expected result is an authentication error, such as code 10000. Pair it with a reverse inventory of the other account that prints which endpoint types it could and could not read. Re-run both at each release checkpoint.
- **Falsifier**: A wrong-account probe passes while a real deploy with the same credentials would have landed in the wrong account.
- **Tags**: credentials, negative-test, census, gates, first-build
- **Status**: active (VALIDATED)

### cf-012: The First Token Probe Tests Product Enablement, Not Only Permissions [VALIDATED]
**Rule**: Before any write, probe with read-only GETs that test feature enablement as well as permissions: an unregistered Workers subdomain (10007) and Zero Trust never onboarded (9999 `not_enabled`) are blockers no token edit fixes. Batch every human dashboard step the probe surfaces into one request; prove each EDIT permission at its first write; record the token's expiry.
- **Falsifier**: A first build's probe lists every permission green and a later step is still blocked by a product that was never switched on.
- **Tags**: cloudflare, token, probe, zero-trust, workers-dev, first-build
- **Status**: active (VALIDATED)

### cf-013: A Branch Cut From Main Inherits Main's Wrangler Config [PROVISIONAL]
**Rule**: When Workers Builds runs `npx wrangler preview` for non-main branches, a branch cut from a main that lacks the required `previews` block fails its preview build. Carry only the `previews` block, byte for byte, and never preview-only extras. A cron whose handler exists only on the preview branch can break production deploys. Name in a code comment what was deliberately not carried.
- **Falsifier**: A main-based branch builds a working preview without the block.
- **Tags**: cloudflare, workers, worker-previews, branching, hotfix
- **Status**: active (PROVISIONAL)

### deploy-009: On Workers, Cutover Is a Build Posture on Main, Not a Hand Edit [VALIDATED]
**Rule**: A production-posture step in the build, gated on the main branch, removes the site-wide noindex header and generates production crawler rules; preview builds keep the noindex posture. Build verification checks both postures. Build-environment guards refuse documented-but-unexecuted cutover steps, such as a missing production key; set trigger variables by API. On Workers sites, encode cutover in the build. On Vercel, explicitly verify the equivalent production and preview settings before launch.
- **Evidence**: A hand edit can break later preview builds when verification requires noindex on non-main builds. A guard for a missing production site key turns a silent test key on a live form into a clear build refusal.
- **Falsifier**: A production build ships with the preview posture, or a preview build ships the production posture.
- **Tags**: cutover, launch, cloudflare, workers, noindex, robots, guards
- **Status**: active (VALIDATED)

### deploy-010: Prove an Image-Affecting Dependency Bump by a Cold Byte-Identical Build; Hold Deploy-Tool Releases a Week [PROVISIONAL]
**Rule**: A dependency fix that can change images gets its own commit, proved by a COLD build with the image cache moved aside and byte-identical output, plus a fresh `npm ci` from the lockfile. Use `overrides` for exact pins. Hold deploy-tool releases such as Wrangler until at least 7 days old, with a durable dated reminder because session timers do not persist, and run the upgrade through both production and preview postures.
- **Falsifier**: A cold byte-identical build later shows a visual change on the live site, or a week-old deploy-tool release breaks a deploy the hold was meant to protect.
- **Tags**: supply-chain, npm, wrangler, sharp, cold-build, launch
- **Status**: active (PROVISIONAL)

### forms-009: A Workers Form Records First, Emails Second, and Fails Closed on Bot Checks [VALIDATED]
**Rule**: Handler order: method, host, origin and Access, then config, rate limit, size cap, honeypot and fill time, validation from ONE shared JSON definition, Turnstile FAIL-CLOSED, a parameterised D1 INSERT first, then email via `waitUntil` with an Idempotency-Key and `email_status` recorded. The Turnstile test key is accepted only on preview hosts: a guard refuses it anywhere else, and a request proves it gets 403 on production. Verify the current D1 Time Travel retention for your plan before relying on it; add a monthly export.
- **Falsifier**: An email-provider outage loses a submission, or the dummy token is accepted on production.
- **Tags**: forms, d1, turnstile, resend, workers, fail-closed
- **Status**: active (VALIDATED)

### forms-010: Bot Timing Is a Page-Measured Duration; the Rate-Limit Binding Is a Brake [VALIDATED]
**Rule**: Measure fill time in the page (`performance.now`) and send the duration; a client timestamp breaks under clock skew. The Workers rate-limit binding is eventually consistent and per location: treat it as a flood brake, never an exact admission boundary or deterministic test assertion. A burst test can confirm throttling when it receives a 429 without requiring refusal at an exact request count.
- **Falsifier**: A timestamp-based check survives a measured 2 s skew, or the binding refuses exactly at its limit across locations.
- **Tags**: forms, bot-check, rate-limit, workers, testing
- **Status**: active (VALIDATED)

### forms-011: Email-Provider DNS Is Written From the Provider's API Response Through the Account Wrapper [VALIDATED]
**Rule**: Create the sending domain by API and write the DNS records it returns through the account wrapper. Use the returned record set rather than a remembered count. Avoid a Domain Connect "Sign in to Cloudflare" button, which acts on whichever account the browser holds. Keep tracking off; begin DMARC monitoring with `p=none` and review the policy at launch. Replace a temporary full-access key with a domain-restricted sending key. Re-poll a lagging verifier; do not change correct DNS records merely because verification is delayed.
- **Falsifier**: A record set typed from memory verifies first time across vendors, or the Domain Connect button provably targets the wrapper's account.
- **Tags**: email, resend, dns, account-separation, first-build
- **Status**: active (VALIDATED)

### forms-012: Run a Local Worker With the Local Upstream; Success-Path-Only Failures Mean a Host Question [VALIDATED]
**Rule**: Start `wrangler dev` with `--local-upstream localhost` for host-keyed code. Without it the Worker can see the production host, treat posts as production, and return 503 `not_configured` from a fail-closed bot check on otherwise successful paths. When a local Worker fails only on success paths, ask first which host it thinks it serves.
- **Falsifier**: A host-keyed handler behaves identically with and without the flag.
- **Tags**: wrangler, local-dev, forms, workers, debugging
- **Status**: active (VALIDATED)

### gate-002: Imperceptible Harms on the Floor, Perceptible Style on an Auto-Fixed Lint Tier, With an Admission Rule [VALIDATED]
**Rule**: A content gate's FLOOR holds harms that may escape a visual review: unsupported or incorrect source references, tense drift on planned facts, private information leaks, incorrect trademark notation, approved fixed wording retyped instead of included, and cross-page repetition. Perceptible house style, such as punctuation, contractions and length budgets, belongs in a LINT tier auto-fixed before review. A floor check that false-fires more than about 1 in 10 times on real copy is demoted to a reviewer advisory. Calibrate on real copy from a different model, never only on the check author's fixtures.
- **Falsifier**: A floor tuned on fixtures holds its false-fire rate on the first real copy.
- **Tags**: content-gate, floor, lint, calibration, copy
- **Status**: active (VALIDATED)

### gate-003: A Positive Control Is a Claim; Widening a Check Reruns the Old Controls First [VALIDATED]
**Rule**: When a check is widened, rerun the old positive controls before trusting it: a control that now fails was certifying the defect. Prove a new rule by also running the pre-edit gate on the new mutant and compare the finding TEXT, not the count. Plant controls in the real source's format, not the fixture's, and re-run after the last voice pass.
- **Falsifier**: Repeated widening of a check never changes an old control's result.
- **Tags**: gates, positive-control, mutants, validation
- **Status**: active (VALIDATED)

### gate-004: A Gate That Read Zero Inputs Is Not a PASS [VALIDATED]
**Rule**: Every PASS prints what it measured; a check that found no input reports that, never PASS; every conditional check prints the branch it took. Count inputs before grading. A Lighthouse "ALL PASS" over zero reports or a budget lint that checked 0 fields proves nothing.
- **Falsifier**: A gate printing only PASS/FAIL catches a zero-input run as often as one that prints its count.
- **Tags**: gates, vacuous-pass, validation
- **Status**: active (VALIDATED)

### gate-005: Pair an Exact n-Word Run Gate With a One-Substitution Window Check [PROVISIONAL]
**Rule**: A writer told to avoid a six-word collision may swap one word and keep the frame. Beside the exact-run rule, run a window check (7-word window, 6 of 7 positions matching, at least 3 content words) as at least an advisory. Scan text slots and headings together as they appear on the page, including their joins; screen drafts against the brief and findings themselves.
- **Falsifier**: Across independently reviewed pages, the window check flags nothing a reviewer did not already flag.
- **Tags**: content-gate, repetition, n-gram, copy
- **Status**: active (PROVISIONAL)
### copy-002: Findings Name the Harm, the Constraint and the Fact Id, Never Replacement Words [VALIDATED]
**Rule**: Every orchestration artifact a writer reads (brief slot purposes, findings, amendments, review messages, mocks, controls) is copy the writer may follow. Findings identify the harm, the supporting fact ID and the fact boundary. Label any suggested wording "one acceptable fix, not an instruction." Constraints introduce no quantifiers of their own (only/never/every) and no verbs that imply unsupported claims. Fact-check every example wording placed in a task.
- **Memory**: recall by this skill's title. **Falsifier**: dictated replacement wording ships without introducing duplication or drift across three rounds.
- **Tags**: copy, briefs, findings, writer, review
- **Status**: active (VALIDATED)

### copy-003: Status Lives in Tense, the Limit Precedes the Modal, and Travelling Answers Carry Their Own Status [VALIDATED]
**Rule**: Match each claim's tense and wording to its verified availability: present tense only for what a visitor can use today, and plainly future wording for anything that is not. Put the status beside the thing it describes rather than in a distant banner; headlines carry no status tags. Put the condition before the modal ("if offered, the class could..."), because a reader resolves "could" from the nearest preceding context. FAQ answers travel as JSON-LD without the rest of the page, so an answer that names something not yet available states that status itself, with no date or price. For example, a ceramic studio whose evening wheel classes are not yet scheduled writes "evening wheel classes are planned" in that FAQ answer, not "join our evening wheel classes".
- **Memory**: recall by this skill's title. **Falsifier**: cold readers resolve a distant status note correctly for a later modal across two pages.
- **Tags**: copy, status, tense, faq, json-ld, aeo
- **Status**: active (VALIDATED)

### copy-004: A Product Fact Is Checked Against the Code That Serves It, and "Live" Means Arrival [VALIDATED]
**Rule**: Before a fact about a site's product capability reaches a writer, verify it against the code path that serves it. Call a capability live only if it works for a visitor: its output arrives where the visitor looks for it. A successful job exit is not enough. A fact's ceiling is the lower of what the supporting documentation establishes and what the product delivers. Soften an unproven claim and record the test that would justify stronger wording.
- **Memory**: recall by this skill's title. **Falsifier**: a site fact verified only against a summary survives a code read unchanged across three facts.
- **Tags**: copy, product-truth, arrival, claims, verification
- **Status**: active (VALIDATED)

### copy-005: Amending a Fact Means Sweeping Every Input and Re-Deriving Every Ledger Row That Cites It [VALIDATED]
**Rule**: On amending a fact, search every writer input (digest, brief rows, source copies, claim maps) for the retired phrasing, and re-derive every claims-ledger row that cites the fact ID, locked or not. If the amended fact no longer supports an approved line, unlock that line for revision and renewed approval. Follow the cause, not just the sentence.
- **Memory**: recall by this skill's title. **Falsifier**: a targeted fix without the sweep leaves no stale phrasing across two amendments.
- **Tags**: copy, facts, amendments, ledger, signatures
- **Status**: active (VALIDATED)

### review-001: A Cold-Reader Belief Test Runs Every Round and on the Final Bytes [VALIDATED]
**Rule**: A fresh reviewer reads only the rendered visitor text, including navigation and other interface text, with a fixed audience perspective. Record structured answers (what the page offers right now, first-screen impression, most and least convincing points, next click) and one open, unscripted question. Each belief unsupported by a verified fact is a perceptible defect. Test the brief's own wording first. Send persuasion findings to the site owner as strategy questions rather than copy instructions.
- **Memory**: recall by this skill's title. **Falsifier**: a page passing every other review leaves cold readers with no unsupported belief across three pages.
- **Tags**: review, cold-reader, belief-test, copy
- **Status**: active (VALIDATED)

### review-002: A Ledger Proposition Restates the Phrase's Whole Claim, as a Stranger Would [VALIDATED]
**Rule**: The claims ledger's proposition restates the phrase's entire claim in the phrase's own structure, rather than copying the source summary or narrowing the meaning. Cite support per sentence. Flag two true facts stitched into an untrue third, quantifier scope, presuppositions and connecting words that change the meaning of lists. A row that needs a disclaimer marks the phrase as false or weak.
- **Memory**: recall by this skill's title. **Falsifier**: a ledger restating source summaries catches as many blocking findings as one restating the published phrases.
- **Tags**: review, claims-ledger, entailment, copy
- **Status**: active (VALIDATED)

### tooling-008: Price the Verification Suite, Not Each Rule [PROVISIONAL]
**Rule**: For each new check, ask who already performs it and how often it must run. The generator runs a fast core set on the final build; heavy sweeps run once per iteration during review. A late fix reruns only the checks its changes can affect. Record the diff summary and the reasoning for excluding other checks beside each reused log. If verification for an iteration exceeds about 90 minutes, stop and report.
- **Memory**: recall by this skill's title. **Falsifier**: a reused log hides a defect its check would have caught despite the recorded reasoning.
- **Tags**: gates, verification-budget, ace-loop, tooling
- **Status**: active (PROVISIONAL)

### tooling-009: Never Pipe Between a Gate and Its Exit Status; "Running" Is a Claim About a Handle [VALIDATED]
**Rule**: Redirect a check's output to a log and read the command's own return code (`> log; echo rc=$?`). A pipeline's status can mask a failing command. Require an explicit success marker before treating an installation as complete. Treat a background agent as making progress only when its output file grows and writes are newer than its start marker. After machine sleep, stop it, health-check its inputs, refresh the marker and relaunch.
- **Memory**: recall by this skill's title. **Falsifier**: a piped check reliably reports the failing command's return code.
- **Tags**: shell, diagnostics, agents, liveness
- **Status**: active (VALIDATED)

### webgl-001: Every Canvas/WebGL Layer Starts From the webgl-craft Cluster's Decision Tree, Budget and Hardening [VALIDATED]
**Rule**: Load `03_skills/webgl-craft/SKILL.md` first. Renderer: HTML/SVG for meaning, then Canvas2D, then raw WebGL2 with a small helper (default), then OGL/twgl, with three.js requiring a budget waiver. Budget: DPR at most 1.5, at most 30 KB gzipped per layer, and a one-shot downgrade to a lighter rendering tier. Hardening: a static design under an aria-hidden canvas, nothing booted during load, and ambient layers started only after load, during idle time and while in view. Verify first-frame fidelity, handle context loss, make reduced motion skip GPU asset fetching, provide a page pause control and clean up animation loops. No boot task may exceed 50 ms at 4x CPU throttling (perf-002).
- **Memory**: recall by this skill's title. **Falsifier**: a layer built outside the decision tree meets the same budget and hardening checks with less work across two pages.
- **Tags**: webgl, canvas, performance, accessibility, design
- **Status**: active (VALIDATED)

### webgl-002: Motion and Frame-0 Gates Run Under the Production CSP [VALIDATED]
**Rule**: Apply the build's production response headers to the local server for motion, frame-0 and live-layer checks. Deliberately reintroduce the defect and confirm the check fails. Never fetch `data:` URLs: Vite can inline small assets as `data:`, which `connect-src 'self'` blocks. A layer can therefore silently fall back to its still in production while local checks pass. Assert that the layer reports itself live, since a fallback may otherwise look successful.
- **Memory**: recall by this skill's title. **Falsifier**: a layer passing local checks without production headers is never found falling back in production.
- **Tags**: webgl, csp, production-parity, gates
- **Status**: active (VALIDATED)

### media-010: Describe the Picture, Never the Page [VALIDATED]
**Rule**: Image prompts never name layout nouns (frame, border, region, overlay, band, box): models paint them. Use full-bleed composition and affirmative descriptions. Control order and prominence by count, shape and placement, rather than interface geometry words or adjectives asking for less emphasis. Keep a shared opening style description verbatim and change only subject and composition. Pilot 3 to 5 images, allow at most 3 retries with changed wording, and check each render.
- **Memory**: recall by this skill's title. **Falsifier**: prompts naming layout regions render without painted frames across two image sets.
- **Tags**: imagery, prompts, image-generation, art-direction
- **Status**: active (VALIDATED)

### media-011: To Animate a Painting, Cut It So the Pieces Recompose the Still at Rest [VALIDATED]
**Rule**: The rendered painting is the specification. Cut each moving element and remove the background contribution against the fill behind it (`sprite = P - (1-a)F`). Compose the static still from the shipped textures so frame 0 equals the painting by construction. Animate by displacement, and keep displacement zero wherever movement could disturb thin painted detail. On a light ground, derive a moving element's alpha from its darkness against the paper.
- **Memory**: recall by this skill's title. **Falsifier**: plain alpha cuts over an inpainted background reconstruct the still without a visible pop at the handover.
- **Tags**: painted-art, animation, webgl, design
- **Status**: active (VALIDATED)

### qa-032: A QR Code on a Printed Poster Points at a Re-pointable Page and Is Checked From the Image [VALIDATED]
**Rule**: For an event poster with a QR code, point the code at a short path you control (for example `/poster`) that forwards with a temporary redirect (302 or 307) to the current event page, so the printed code can be re-pointed later. Never use a permanent 301 there, because browsers cache it. Test the printed image itself: decode it, follow the URL, and check that the final page loads and is the page you meant. Re-test after any change to that route.
- **Memory**: recall by this skill's title. **Falsifier**: a code that passes every other check is never found leading nowhere useful.
- **Tags**: qr, links, launch, verification
- **Status**: active (VALIDATED)

### capture-001: A Batch-Store File Built From Agent JSON Asserts Content Length and Normalises Mixed Elements [VALIDATED]
**Rule**: Before storing reusable lessons built from an agent's JSON, assert a minimum content length on every item and explicitly normalise heterogeneous list elements (`str | {text}`). A tag-count check can report empty-bodied records as correctly classified.
- **Evidence**: Header-only records can retain all expected tags while losing the lesson text. Recover missing bodies from the source reports, then validate content before storing again.
- **Memory**: recall by this skill's title. **Falsifier**: a batch with mixed element types stores full bodies without the assertion.
- **Tags**: memory, capture, batch-store, diagnostics
- **Status**: active (VALIDATED)

## Skill Registry: site build and recovery

| ID | Section | Status | Added | Source |
|------|---------|--------|-------|--------|
| account-001 | Accounts / Credentials | active, VALIDATED | Included | Build and recovery guidance |
| account-002 | Accounts / Negative tests | active, VALIDATED | Included | Build and recovery guidance |
| cf-012 | Cloudflare Workers Deploy | active, VALIDATED | Included | Build and recovery guidance |
| cf-013 | Cloudflare Workers Deploy | active, PROVISIONAL | Included | Build and recovery guidance |
| deploy-009 | Deploy / Cutover | active, VALIDATED | Included | Build and recovery guidance |
| deploy-010 | Deploy / Supply chain | active, PROVISIONAL | Included | Build and recovery guidance |
| forms-009 | Forms / Workers | active, VALIDATED | Included | Build and recovery guidance |
| forms-010 | Forms / Bot checks | active, VALIDATED | Included | Build and recovery guidance |
| forms-011 | Forms / Email DNS | active, VALIDATED | Included | Build and recovery guidance |
| forms-012 | Forms / Local dev | active, VALIDATED | Included | Build and recovery guidance |
| gate-002 | Content gate | active, VALIDATED | Included | Build and recovery guidance |
| gate-003 | Gates / Controls | active, VALIDATED | Included | Build and recovery guidance |
| gate-004 | Gates / Vacuous pass | active, VALIDATED | Included | Build and recovery guidance |
| gate-005 | Content gate / Repetition | active, PROVISIONAL | Included | Build and recovery guidance |
| copy-002 | Copy / Findings | active, VALIDATED | Included | Build and recovery guidance |
| copy-003 | Copy / Status | active, VALIDATED | Included | Build and recovery guidance |
| copy-004 | Copy / Product truth | active, VALIDATED | Included | Build and recovery guidance |
| copy-005 | Copy / Amendments | active, VALIDATED | Included | Build and recovery guidance |
| review-001 | Review / Cold reader | active, VALIDATED | Included | Build and recovery guidance |
| review-002 | Review / Claims ledger | active, VALIDATED | Included | Build and recovery guidance |
| tooling-008 | Tooling / Verification budget | active, PROVISIONAL | Included | Build and recovery guidance |
| tooling-009 | Tooling / Shell and agents | active, VALIDATED | Included | Build and recovery guidance |
| webgl-001 | WebGL / Doctrine | active, VALIDATED | Included | Build and recovery guidance |
| webgl-002 | WebGL / Production parity | active, VALIDATED | Included | Build and recovery guidance |
| media-010 | Media / Image prompts | active, VALIDATED | Included | Build and recovery guidance |
| media-011 | Media / Painted art | active, VALIDATED | Included | Build and recovery guidance |
| qa-032 | Quality / Links | active, VALIDATED | Included | Build and recovery guidance |
| capture-001 | Memory / Capture | active, VALIDATED | Included | Build and recovery guidance |
| aeo-014 | AEO (distinct from aeo-008) | active [PROTECTED] | Included | Skill ID disambiguation |
## NEW SKILLS and UPDATES: propagating an approved image change to every derivative, with visual-gate and tooling lessons

Generic skills for calibrating visual gates, carrying an approved image fix into every image derived from it, and processing artwork in business-site heroes and figures. The examples below use invented businesses to illustrate the checks and failure modes. IDs follow this file's scheme. Recall phrases below are drawn from each rule's own words.

### gate-006: Calibrate Every Numeric Gate Threshold Between Work Already Accepted and Work Already Rejected Before It Gates [VALIDATED]
**Rule**: Before a numeric floor or cap gates anything (a reviewer's acceptance clause, a new battery check, a skill's own falsifier), measure it on at least one artifact already accepted by eye and at least one already rejected, set it between them, and show the gate red on a known failing build. A threshold that fails accepted work is miscalibrated: version the ruler, never move the artifact to satisfy it. The converse binds too: recalibrate only when ACCEPTED work fails; when a changed layout makes a real defect fail at near zero, the gate is right and the threshold stays. For a QUALITY gate the accepted reference must predate the candidate (the candidate itself may serve as the reference only for a PRESENCE gate). A requirement with an upper qualifier ("a little", "subtle", "a hint, not a flood") needs a ceiling, calibrated against an over-strength mutant, as well as a floor.
- **Evidence**: In a kitchen-equipment maker's resource library, a texture floor could reject an approved soft background while accepting a gritty variant. Calibrate against both before deciding whether the requirement needs a floor, a cap, or both. Likewise, measure approved highlights, absent highlights and deliberately excessive highlights before setting brightness bounds. Derive any secondary check from the same calibrated requirement. Keep a colour threshold when a layout change actually removes the required colour. If grading median rows protects accepted artwork, check what that aggregation hides.
- **Memory**: recall: `every numeric gate threshold accepted rejected ceiling` **Falsifier**: a threshold set between measured accepted and rejected artifacts later fails an artifact the reviewer accepts, or passes one the reviewer rejects, on the same kind of region.
- **Dedup**: gate-002 KEEP (the content-gate instance: calibrate on real copy); gate-003 KEEP (rerun old controls when a check widens); qa-030 KEEP (a check must be shown able to fail); gate-008 KEEP (whether the measured quantity is the property at all).
- **Tags**: gates, calibration, thresholds, rulers, ceilings
- **Status**: active (VALIDATED)

### gate-007: A Live-Minus-Reference Shape Probe Takes Its Reference From the Same Paused Frame With Only the Subject Hidden [VALIDATED]
**Rule**: When a gate measures a shape (roundness, edge, spread, a hover's response) as live minus reference, build the reference from the SAME paused live frame with only the measured subject hidden (a test hook that zeroes that one draw), never from a still with every live layer off: the other live layers near the subject (glows, shimmers, running lights) enter the difference as a one-sided gradient and a correct shape fails. Pair the percentile spread (p90/p10) with max/median at the same threshold, because a percentile ignores thin features under 10% of the samples, and keep a thin-feature mutant (a four-pointed spike) that must read red. Show every new gate red on a known defective build before it is used.
- **Evidence**: In a ceramic studio's hero, a round glaze highlight drawn above an animated kiln glow can appear asymmetric when compared with a reference that disables both layers. Hiding only the highlight in the same frozen frame isolates its shape. A deliberately pointed mutant tests whether the probe detects narrow spikes that percentile spread can miss. The same isolation principle applies to comparing an initial live frame with its still and measuring hover response while the background animation remains frozen.
- **Memory**: recall: `same paused frame subject hidden reference probe max median` **Falsifier**: a same-frame, subject-hidden probe with max/median fails a correct shape across 3 runs, or passes the thin-feature mutant.
- **Dedup**: tooling-006 KEEP (which device tier to measure); webgl-002 KEEP (frame-0 gates under the production CSP); qa-030 KEEP (mutants must fire).
- **Tags**: gates, visual-probes, reference-frames, mutants, webgl
- **Status**: active (VALIDATED)

### gate-008: A Gate's PASS Is Evidence Only Where It Can See the Defect: Measure the Property the Requirement Means, and Name What a Calibration Choice Hides [VALIDATED]
**Rule**: A metric gate passes a wrong picture when it measures a proxy (any bright fragment counted as a flower; a largest step where the defect is a non-monotonic dip) or covers a region too small to fail. Define the measured shape as the requirement means it, apply the same test to reference and candidate, name every region or failure shape the gate cannot see, and look at the crop before trusting a pass there. When a calibration choice protects accepted work (grading a row family on its median, starting profiles after the painting), add the complementary check it removed: a high percentile after masking point sources, and a graded span moved to wherever a fix moved the defect's start.
- **Evidence**: A garden-supply shop's painted seed-packet banner might pass a flower-count check because the detector also counts reflected fragments and short decorative lines. Restricting the count to round blooms tests the intended shape; inspecting the sampled area reveals whether it is large enough to detect a shortage. Similarly, a largest-step check can miss a broad luminance dip that reads as a border. Median-row grading can hide that dip when most sampled rows are unaffected, so it needs a complementary check over the affected span.
- **Memory**: recall: `gate pass evidence only where it can see the defect proxy coverage` **Falsifier**: a gate whose measured shape is defined by the requirement, with its blind spots named and looked at, passes a picture the reviewer rejects in a region it claimed to cover.
- **Dedup**: gate-004 KEEP (zero inputs is the degenerate case; this is wrong inputs and blind regions); tooling-004 KEEP (which capture to judge from).
- **Tags**: gates, proxies, coverage, fluency-trap, measurement
- **Status**: active (VALIDATED)

### media-012: A Share or Thumbnail Image Passes the Same Structure Gates and Rulings as the Hero It Stands For [VALIDATED]
**Rule**: An image that stands for a page (og:image, social card, thumbnail, poster frame) inherits every visual ruling already applied to that page's hero. Build it from the shipped, processed plate, since the raw render still carries the defects the pipeline removed. Run the hero's structure gate and its by-eye ruling on it before choosing it, and check it at full size, in the centre 630x630 square and at about 120 px. A fresh render needs the same processing or the same gate.
- **Evidence**: A ceramic studio retouches a bright glare spot off a glazed bowl in its product photo, and the hero ships clean. If the social card is then cropped from the original camera file, the glare spot comes back on every shared link. Running the hero's glare check on the card catches the regression; building the card from the retouched file and looking at it full size, in the centre square and at thumbnail size confirms the fix survives at every size people will see.
- **Memory**: recall: `share thumbnail image same structure gates as the hero` **Falsifier**: a card that passes the hero's gate is read as contradicting the hero, or a card that fails it is judged consistent with it.
- **Dedup**: media-010 KEEP (how to prompt a render); media-013 KEEP (how the structure is removed).
- **Tags**: og-images, derived-assets, gates, art-direction
- **Status**: active (VALIDATED)

### media-013: Remove Concentric Bands by Blurring Isotropically, Then Along the Radius Only in the Region's Polar Frame; Re-gate After Any Texture Restore [VALIDATED]
**Rule**: To remove concentric rings from a roughly elliptical region of a painted image, first soften the bands with an isotropic blur inside its mask, then blur along the radius only in the region's own elliptical polar frame (about its centre, aligned to its axes): the bands vary along rho, so a rho-only blur removes them while the angular texture survives. Fade the polar blur in just outside the centre so a hollow keeps its profile. Re-run the structure gate after ANY texture restore: recombining a full-strength high-pass at stroke scale can return the rings, and synthetic grain can read as grit on a smooth area; the gate decides, not the method.
- **Evidence**: A seed library's watercolour banner shows faint concentric rings around a painted seed head where the scan picked up ripples in the paper. A radial blur alone may leave strong rings. An isotropic pass first, then a radius-only blur, can remove them while keeping the brush texture that runs around the seed head. Restoring fine detail at full strength can bring the rings back, and adding grain can turn smooth paper into visible grit. Check both the ring measure and the surface by eye after each restoration attempt.
- **Memory**: recall: `radius only blur polar frame after isotropic blur concentric bands` **Falsifier**: on a further banded region the isotropic blur plus rho-only blur does not bring the band measure under its cap, or the reviewer still reads rings, or reads an airbrushed smear where the reference reads as paint.
- **Dedup**: media-011 KEEP (cutting a painting so pieces recompose the still); media-012 KEEP (applies this to derived images).
- **Tags**: image-processing, painted-art, polar-transform, banding
- **Status**: active (VALIDATED)

### media-014: Fade Dark Art Onto a Light Ground With One Tinted Product Mask and a Monotonic Ramp; Butt Dark Against Dark [VALIDATED]
**Rule**: A plain alpha fade from a dark painting onto a white or pale ground can pass through a desaturated grey band, and feathered corners can make the art read as a blurred photo or drop shadow. Where the art meets a dark element (a header or nav band), run it flush, dark against dark. Where it must meet the light ground: (1) tint the fading pixels toward the ground's palette white before the alpha falls; (2) keep the luminance ramp monotonic toward the ground: the tint fades in from zero and is never darker than the art beneath, so it leads the art's fade (starting at about 1.3x the fade width, full by about 0.45x); (3) use ONE combined mask for all edges, one tint layer whose alpha is 1 - (rampX x rampY) (in CSS `mask-image: solid, rampX, rampY` with `mask-composite: exclude, intersect`), with a rounded corner falloff of about 10rem, because two separately tinted edges overlap at the corner and complete a frame; (4) fade over a long distance with an eased curve.
- **Evidence**: In a kitchen-equipment maker's resource-library banner, a plain alpha fade can produce a grey strip between dark painted artwork and a pale page. Tinting the transition can preserve its colour, but separate edge tints can create a visible corner frame or a luminance dip at their onset. A single combined mask with a leading tint addresses both defects. Compare the broken and corrected versions with the same monotonic-fade check, then inspect the full transition for a visible rectangle.
- **Memory**: recall: `fade dark art onto light ground product mask monotonic ramp tint` **Falsifier**: the combined tinted mask with a leading tint still shows a dip below the running maximum or a grey band (fade mid-tone chroma under half the art's own), or the reviewer still reads a framed rectangle.
- **Dedup**: media-007 KEEP (a scrim behind words; this is art dissolving into the page ground); qa-031 KEEP.
- **Tags**: css-masks, gradients, compositing, art-direction
- **Status**: active (VALIDATED)
### webgl-003: In a Chain of Additive Soft Lights, Space by True Arc Length and Hold Spacing-to-Radius Constant [VALIDATED]
**Rule**: When a river, streak, trail or thread is drawn as a chain of additive radial lights along an arc whose length changes, a fixed light count with a fixed alpha breaks: the summed alpha on the axis is about alpha x 2R / spacing, so a short segment saturates into a blob, a long one reads as a uniform tube, and too-wide spacing reads as beads. Space the lights evenly by TRUE arc length (build a fine polyline, accumulate segment lengths, place the N lights at equal cumulative length), not by the curve's parameter, which bunches lights where an easing is flat, then scale each light's alpha by min(1, spacing / (0.35 x R)). Gate it as a ratio: maximum added luminance along the chain at most about 1.5x its median, at every viewport.
- **Evidence**: A fixed-count, fixed-alpha chain can bunch into bright patches on small screens and flatten into a tube on larger screens. Compare it with arc-length spacing and spacing-normalised alpha at each viewport, then restore the faulty version deliberately to confirm that the check detects the defect.
- **Memory**: Search phrase: `additive soft lights chain true arc length spacing normalised alpha`. **Falsifier**: after arc-length spacing and spacing-normalised alpha the max/median ratio still exceeds 1.5 on short segments.
- **Dedup**: webgl-001 KEEP (the doctrine and budget); media-011 KEEP.
- **Tags**: webgl, additive-blending, particles, density
- **Status**: active (VALIDATED)

### webgl-004: A Halo's Fall Table Carries Light Inside Its Radius; No Dark Trough Between Core and Rim [VALIDATED]
**Rule**: A soft glow drawn as an annulus whose fall table is zero inside the ring reads as a bullseye whatever is drawn under it. Give the ring's own table a floor inside its radius that rises continuously into the peak, and draw a halo under the ring that reaches inside it (the floor alone is not enough). Use a centred halo table, never a hollow ring table, for pulses and swells. Check it: along 8 rays from the centre, the least light between the core's edge and the rim's peak is at least 0.7 x that peak.
- **Evidence**: Compare a hollow rim, a rim with an inside floor, and a rim with both the floor and an underlying halo. The floor can soften the trough without removing it; the underlying halo supplies the missing light. Repeat the comparison at different sizes and after rim changes. Check animated pulses separately using a centred halo table.
- **Memory**: Search phrase: `halo fall table light inside radius no dark trough bullseye`. **Falsifier**: a rim table with a continuous inside floor plus an under-ring halo still fails the 8-ray trough check (below 0.7) across repeated runs at some size, or the reviewer reads a bullseye while the check passes.
- **Dedup**: webgl-001 KEEP; media-007 KEEP (scrims are a different layer).
- **Tags**: webgl, radial-gradients, halos, fall-tables
- **Status**: active (VALIDATED)

### convention-009: Code in a Shared Chunk Spends Every Importing Page's Budget; Put Page-Specific Code in a Page-Specific Chunk [VALIDATED]
**Rule**: A change to a module several pages import (a shared layer chunk) lands in every one of those pages' bundles, including pages marked untouchable or near their cap. Before editing a shared chunk, list its importers; put behaviour that serves one page in that page's own chunk (for example, draw the effect for a part id the shared renderer never handles), and check each importer's budget against its pre-change figure, not only against the cap.
- **Evidence**: An effect added to a shared renderer can increase an unrelated page's bundle while leaving it below its cap, so a cap-only check misses the regression. Moving the effect into the requesting page's chunk should restore the other pages' bundle sizes. Verify both the byte totals and whether the shared module changed.
- **Memory**: Search phrase: `shared chunk spends every importing page budget page specific chunk`. **Falsifier**: moving the behaviour into a page-specific chunk does not restore the other importers' figures, or a shared-chunk change is found that cannot be page-scoped without costing more than it saves.
- **Dedup**: webgl-001 KEEP (per-layer budget); perf-002 KEEP (boot cost, not bytes).
- **Tags**: build, budgets, bundling, code-splitting
- **Status**: active (VALIDATED)

### tooling-010: A Lock Held by a Script Is Held by Every Long-Lived Process It Spawns; Run Heavy Jobs Under `flock -o` [VALIDATED]
**Rule**: A process started while a script holds a flock (`exec 9>LOCK; flock 9`, or `flock LOCK cmd`) inherits the lock's file descriptor; if it outlives the script (a file server, a watcher, a backgrounded build), it holds the lock until it dies and every job queued on that lock stalls. Run finite heavy jobs as `flock -o LOCK cmd` (the fd is closed in the command, so only the flock process holds it), and start long-lived servers outside the lock or with the fd closed (`9>&-`).
- **Evidence**: A file server started inside a script holding a flock can outlive the script and block queued work. Reproduce this with a temporary lock: a non-blocking `flock -n` attempt fails while the child retains the descriptor. Repeat with `flock -o` and verify that the orphaned child no longer retains the lock after the lock-owning process exits.
- **Memory**: Search phrase: `flock lock fd inherited long-lived server deadlock flock -o`. **Falsifier**: a long-lived child started under `flock -o` or with the fd closed is found holding the lock.
- **Dedup**: tooling-009 KEEP (liveness and exit status); tooling-011 KEEP (why the stray process survives cleanup).
- **Tags**: tooling, bash, flock, locks, processes
- **Status**: active (VALIDATED)

### tooling-011: In `( cd D && server & echo $! )`, `$!` Is the Subshell, Not the Server [VALIDATED]
**Rule**: `&` binds to the whole `&&` list, so `cd D && server &` backgrounds a subshell; `$!` can identify that subshell rather than the server, so a later `kill $(cat pid)` can miss the server, which keeps its port and any inherited lock. Change directory first with failure handling, then start the server and record its pid: `cd D || exit; server & echo $! > pid`. Alternatively, use `(cd D && exec server) &` and record `$!` in the parent shell. Check the recorded pid's command name before relying on it.
- **Evidence**: A background server can survive cleanup when the recorded pid belongs to an intermediate shell. Inspect the process tree for the `&&` form, then compare it with a server started after the directory change. Shell exec optimisations can affect the result, so verify the actual process rather than assuming either form's pid ownership.
- **Memory**: Search phrase: `dollar bang subshell cd and server background kill misses`. **Falsifier**: on the shell in use, the `cd && cmd &` form records the command's own pid through an exec optimisation, so the kill reaches it.
- **Dedup**: tooling-009 KEEP ("running" is a claim about a handle; this makes the recorded handle the right one); tooling-010 KEEP.
- **Tags**: tooling, bash, processes, pids
- **Status**: active (VALIDATED)

## Skill Registry: visual effects and tooling lessons

| ID | Section | Status | Added | Source |
|------|---------|--------|-------|--------|
| gate-006 | Gates | active, VALIDATED | Included | Search: `every numeric gate threshold accepted rejected ceiling` |
| gate-007 | Gates | active, VALIDATED | Included | Search: `same paused frame subject hidden reference probe max median` |
| gate-008 | Gates | active, VALIDATED | Included | Search: `gate pass evidence only where it can see the defect proxy coverage` |
| media-012 | Media / Painted art | active, VALIDATED | Included | Search: `share thumbnail image same structure gates as the hero` |
| media-013 | Media / Painted art | active, VALIDATED | Included | Search: `radius only blur polar frame after isotropic blur concentric bands` |
| media-014 | Media / Painted art | active, VALIDATED | Included | Search: `fade dark art onto light ground product mask monotonic ramp tint` |
| webgl-003 | WebGL | active, VALIDATED | Included | Search: `additive soft lights chain true arc length spacing normalised alpha` |
| webgl-004 | WebGL | active, VALIDATED | Included | Search: `halo fall table light inside radius no dark trough bullseye` |
| convention-009 | Conventions / Build | active, VALIDATED | Included | Search: `shared chunk spends every importing page budget page specific chunk` |
| tooling-010 | Tooling / Shell | active, VALIDATED | Included | Search: `flock lock fd inherited long-lived server deadlock flock -o` |
| tooling-011 | Tooling / Shell | active, VALIDATED | Included | Search: `dollar bang subshell cd and server background kill misses` |
| qa-030 | Quality / Guards (strength clause) | active, VALIDATED | Included | Search: `mutant must deliver the strength it claims` |
| media-007 | Media / Scrims (veil shape clause) | active, VALIDATED | Included | Search: `text veil over structured art not a box` |
| tooling-005 | Tooling / Gate provenance | active, VALIDATED | Included | Check provenance of test commands and their results |

## Generic lessons for business sites

These concise lessons apply to a person or small team running their own sites. Use the quoted search phrases or distinctive wording to find related guidance in the shipped workbench. Search phrases are descriptive lookup aids, not private memory identifiers.

- When turning a finished site into a reusable template, replace every hardcoded brand name in navigation and footer components with a single configuration constant. Search: `turn a finished site into a reusable template with config constants`.
- Give each independently deployed site its own repository and build configuration. For an existing Cloudflare Pages site, confirm the build command, generated output directory and supported Node version.
- For GitHub connection failures, diagnose the authentication or host-verification error before retrying. Verify host fingerprints through a trusted source before accepting a changed host key. See `09_guides/GITHUB_SETUP.md`.
- Set a repository baseline: require two-factor authentication where supported, choose visibility deliberately and protect the main branch against force-pushes.
- A Content-Security-Policy must enumerate every external host the page actually loads: stylesheet hosts in `style-src`, font-file hosts in `font-src`, script hosts in `script-src`, and analytics or API destinations in `connect-src`. Permit `data:` only where needed. Search: `content security policy every external host the page loads`.
- A reusable consent pattern is vanilla-cookieconsent v3 as a layout component. Check its licence, dependencies and compressed asset sizes for the version installed.
- When deploying one app from a Turborepo monorepo on Vercel, select the app's directory as the project root and configure the build so workspace packages resolve. Verify the current platform settings and build working directory.
- Cloudflare's application-creation flow can lead to different deployment products. Select the service that matches the intended architecture; Workers with static assets and Pages have different configuration paths.
- For a static Astro site, generate crawler directives, a sitemap and relevant machine-readable discovery documents into the public output. Add appropriate response links and content types. Advertise only capabilities the site actually provides. Search: `agent ready baseline documents for a public static Astro site`.
- For OAuth Protected Resource Metadata under RFC 9728, the `resource` field must identify the origin serving the metadata or an applicable subpath, rather than an unrelated application host.
- In a generate/review loop for production web work, code inspection alone cannot establish readiness. Verify real LCP, CLS and INP under representative conditions, contrast in hover and focus states, touch-target sizes at each breakpoint, and heading order in rendered pages.
- A useful default stack is Astro with static output and islands where needed, plus Tailwind v4 through its official Vite plugin. Confirm compatibility with the installed versions. Search: `Astro static first with Tailwind v4 through the Vite plugin stack default`.
- When axe flags contrast in a canonical design, preserve protected brand tokens while finding an accessible foreground, background or placement combination. If the reference cannot meet the requirement, document the conflict and obtain an approved design change.
- On Linux without system Chrome, run `npx playwright install chromium` and obtain the executable path through Playwright. Point `CHROME_PATH` at that binary for Lighthouse, and run axe-core in a Playwright page after the page has settled. Search: `run Lighthouse and axe with Playwright bundled Chromium without system Chrome`.
- In generate/review loops, compare the generator's self-estimate with the reviewer's empirical score on each pass. Use recurring differences to improve the generator's checks.
- When scaffolding from an existing site, use `rsync --exclude=.git` with additional exclusions for dependencies, generated output, framework caches and any lockfile that will deliberately be regenerated. Alternatively, copy only the required source and assets into a fresh repository created with `git init -b main`.
- For review builds on Vercel, keep the production branch configured as `main` and send active work to a preview branch until release.
- Old CMS asset URLs on the site's own domain can become 404s at DNS cutover. Inventory and migrate those assets before switching the origin. Search: `old CMS asset URLs on the domain become 404 at DNS cutover`.
- When choosing visual assets for a kitchen-equipment resource library, download candidates with descriptive names, inspect each image, and compare it with the alt text and surrounding copy. Keep the semantic match under the chosen final filename and remove unused candidates.
- Choose the lead-capture backend per site, based on delivery, validation, consent, storage and maintenance needs.
- Separate domain routing from page routing. Configure host resolution through DNS, and implement apex-to-www changes, old-domain redirects and subdomain consolidation through an HTTP-capable registrar service or edge layer.
- Shipping discovery metadata is not sufficient: scan the live preview or released site and verify that advertised resources resolve with correct content and headers. Search: `run a live agent readiness scan and require the applicable checks to pass`.
- A CMS-to-static rebuild is rarely byte-identical. Inventory old URLs and explicitly map page slugs and asset paths rather than assuming parity. Search: `rebuilding a site build the old URL inventory before mapping slugs`.
- When upgrading to an Astro version that rejects `output: 'hybrid'`, use the supported server output mode with explicit prerendering where appropriate. Search: `Astro 6 removed output hybrid use server with prerender`.
- For a CMS-backed Astro site on Vercel, allow only required script sources in the CSP. If the preview comment toolbar is enabled, include its required origin in the preview policy.
- Before declaring a build ready for review, the builder runs a clean production build, resolves warnings, serves the generated site through the appropriate runtime and runs axe-core against it with Playwright. Search: `builder runs axe before submitting a build for review`.
- If a shared footer or filter sidebar uses `h3` group titles but its host page has no preceding `h2`, axe can flag heading-order problems on every page that mounts it. Use a heading structure appropriate to the surrounding document. Search: `axe heading-order check shared footer group titles across every page`.
- Give an above-fold hero image that is the LCP candidate `loading="eager"`, `fetchpriority="high"`, `decoding="async"` and explicit width and height. Search: `hero LCP image eager fetchpriority high with width and height`.
- Iterative build loops use three separate roles in sequence: the generator writes artifacts and records applied strategies; the reflector scores and runs build, axe, Lighthouse and schema checks without editing; the curator updates the playbook without changing the implementation. Search: `generator reflector curator as separate agents in sequence`.
- For cookie, network, header and multi-step assertions, write a headless Playwright Node script. Use `chromium.launch({headless:true, channel:'chrome'})` only when system Chrome is available; otherwise use the installed Playwright browser. Filter results before printing, while retaining failures and exit status.
- When a static resource hub sits beneath a parent CMS site with an existing consent plugin, configure the consent cookie for the shared parent domain only when both sites intentionally share consent semantics. Domain sharing alone does not translate cookie formats.
- Every site with a consent banner needs a working footer “Cookie Settings” control beside its privacy links. With vanilla-cookieconsent v3, `<a href="#" data-cc="show-preferencesModal">Cookie Settings</a>` reopens preferences; verify keyboard use and that changes take effect.
- If Vercel Analytics is selected for an Astro site, install its package, import the Astro Analytics component in the base layout and render it before the closing body tag. Apply the site's consent policy.
- Record a default conversion event after confirmed form submission, usually on the success page. Avoid counting page reloads or failed submissions as new conversions.
- For a cohesive bicycle-parts guide library, use one image-prompt template with fixed blocks for STYLE, palette and COMPOSITION. For example, use clear editorial product illustrations, a consistent approved palette, 16:9 body figures and 1:1 icons.
- When rebuilding an existing site, treat the crawled page index as a URL contract. Compare the old and new URL sets, accounting explicitly for retained pages, redirects and intentional removals. Search: `set equality audit of crawled URLs`.
- If the source of truth is a captured page with HTML, screenshots and notes, transcribe it faithfully: preserve sections, order, copy, elements and proportions unless a change is explicitly approved. Search: `transcribe reverse-engineered captured pages`.
- Publish agent-discovery documents consistently, with suitable content types and discoverable links. Keep mirrored descriptions in sync, describe tools individually and publish authentication metadata only when it truthfully represents supported access.
- Use progressive enhancement: the widget's essential function remains available with JavaScript disabled.
- When pages embed CDN-hosted PDFs with `<object type="application/pdf">` or `<iframe>`, allow the host in the corresponding `object-src` or `frame-src` directive. Add it to `connect-src` for fetches and `img-src` for thumbnails; allow `data:` only if those thumbnails require it.
- A CLI that checks an encrypted OS keyring before environment variables may wait indefinitely for an interactive password prompt in a background shell. Use its supported non-interactive credential mechanism and fail clearly when credentials are unavailable.
- Keep generator, reviewer and curator roles separate. Iterate toward the defined threshold; if the score stays the same or worsens twice, escalate the specific blocker rather than repeating the same repair.
- Adding an analytics package to a Sanity site can expose incompatible React peer dependencies. Inspect the actual dependency conflict and choose compatible versions instead of forcing installation without understanding the result.
- To bridge consent between a static subdomain and a WordPress parent, identify the installed plugin and inspect its shipped JavaScript for the cookie name, value format and update behaviour.
- Before loading marketing tags, initialise `dataLayer` and `gtag`, then call `gtag('consent','default',{ad_storage:'denied', analytics_storage:'denied', ad_user_data:'denied', ad_personalization:'denied', wait_for_update:500})`. Wire subsequent consent changes to the relevant storage settings and verify network behaviour.
- For a public garden-supply how-to hub with no protected API, distinguish a scanner's missing-authentication warning from a real access defect. Explain public access accurately rather than inventing an OAuth service to satisfy a scanner.
- When implementing DNS-AID discovery, validate the expected SVCB record name, ServiceMode priority of at least 1 and required service parameters against the applicable specification.
- Keep active work on a `preview` branch and leave `main` at the approved baseline until release.
- Govern all above-the-fold media together because images, animation, video, canvas and 3D can compete for the LCP slot. Search: `govern above-the-fold media competing for LCP as one class`.
- Before prompting for a banner background, inspect the target section's CSS, resolve colour variables to their actual values and include the exact background treatment in the prompt: either a solid colour throughout or the precise gradient direction, stops and percentages.
- An esbuild JSX trap can occur with inline nested template literals such as `<Fragment set:html={`<style data-x=${slug}>${block}</style>`} />`. Misleading brace errors are easier to diagnose when the generated string is computed separately and passed into the expression.
- Add GA4 behind an existing consent banner in three changes: establish denied defaults before tag loading, map consent changes to analytics permission, and verify that events and storage match the selected preferences.
- Choose between a hosted form iframe and an HTML form posting to a handler by comparing styling control, accessibility, validation, consent, error handling and operational ownership.
- A Google Tag Manager container ID and a GA4 measurement ID identify different resources. Use each in the integration that expects it.
- Use one go-live checklist for every site or resource hub. Assign each item to design/content review, engineering or both, and resolve every required item before cutover. Search: `master go-live checklist every required check passes before cutover`.
- Register the domain in the business's own account where possible, with registrar lock, auto-renew and domain-registration privacy enabled where available.
- When coordinating parallel agents for web content, write one precise shared contract for generation, review and page structure, then give each agent the same relevant requirements.
- `pgrep -f PATTERN` matches full command lines, including the shell running the check when its command contains the pattern. A terminated process can therefore appear alive. Verify the pid and command identity rather than trusting a broad match. Search: `pgrep -f matches its own command line`.
- Generate aggregate discovery catalogs during the build, after their inputs are available and before Astro builds the site. Do not maintain duplicate catalogs by hand. Search: `generate the AI catalog in the build never hand author it`.
- For a public site with no protected resources, keep the access description, discovery metadata, response headers and live behaviour consistent. Do not publish placeholder authentication endpoints that imply unsupported features.
- For Web Bot Auth key generation, use `crypto.generateKeyPairSync('ed25519')` and export the public key with `publicKey.export({format:'jwk'})`. Keep the private key out of published metadata.
- Estimate a legacy CMS port by counting unique layouts and repeated instances separately. A regional bakery chain's location pages may reuse one layout, while its ordering and catering pages require distinct work.
- Keep previews out of search indexes with a robots meta directive and an `X-Robots-Tag` response header where appropriate. Configure crawler directives deliberately and use platform authentication for access control; a crawl block alone does not guarantee deindexing.
- Verify Vercel deployment protection across both production and preview targets. A setting that excludes custom domains can still protect platform-hosted deployment URLs, but confirm the current setting and test access anonymously.
- In a generator/reviewer/curator loop, the generator builds, an independent reviewer scores without fixing, and the curator closes the review. Keep the orchestration role separate from implementation. Search: `independent reviewer scores and never fixes orchestrator never builds inline`.
- Keep a review loop honest: the generator may report a faulty check with a reproducible falsifier but must not change the check used to judge its own work. Search: `the examinee may not modify the exam generator reports check defects`.
- A command piped to `tail` or `head` normally reports the last pipeline command's exit status. Preserve the original status with appropriate pipeline handling before declaring success. Search: `cmd piped to tail returns the pipe exit status`.
- For an interactive tool that needs no private data, such as a ceramic studio's tile-layout estimator, consider running the computation in the visitor's browser. Use WebAssembly only when justified by the implementation. Search: `interactive tool in the visitor browser with WASM no serverless function`.
- A static site's Worker contact API should accept POST only, cap request size, validate fields from a definition shared with the page, and reject failed Turnstile verification. Honeypot or implausibly fast submissions may receive quiet success without storage. A missing verification secret must fail closed. Search: `contact form on a static site with a Worker API honeypot and shared field definitions`.
- On a machine used with multiple service accounts, check whether shell startup configuration exports tokens or account identifiers that could silently select the wrong account.
- For a new static site on Cloudflare, consider Workers with static assets and Workers Builds for Git integration. Assess Pages separately if maintaining an existing deployment. Search: `new static site on Cloudflare prefer Workers with static assets over Pages`.
- For copy that must exclude internal information, define explicit failure classes and prove each check with a deliberately faulty example. Trace factual claims to sources and recompute derived numbers. Search: `floor classes each proven by a mutant for a site that must not leak`.
- Keep separate projects' configuration and brand guidance isolated. A garden-supply shop's palette or terminology should not become a shared default for an unrelated ceramic studio. Search: `keep project tooling separate from shared configuration`.
- Before planning a site build, review prior lessons in batches and perform read-only exploration. Then critique the draft for coverage of every requested outcome and for concrete causal failure chains. Search: `recall in batches and run read-only sweeps before writing the plan`.
- Create a Cloudflare API token in an isolated browser session when account confusion is possible. Scope it to the intended account and zone, grant only permissions needed by the planned operations, and validate both permitted and prohibited actions. Search: `scoped Cloudflare API token private window account zone`.
- Guard Cloudflare work in both directions: pin the intended account in deployment configuration so a foreign token fails, and scope the token so it cannot act on unrelated accounts or zones. Verify each boundary independently.
- For dashboard-only tasks the site operator must perform, state time and prerequisites first, then give ordered actions, expected screen states and a clear completion check. Search: `dashboard click steps for a beginner include what you should see`.
- Treat shell arguments as executable syntax: backticks and dollar expressions inside double quotes can trigger expansion or command substitution. Pass search text through structured arguments, safe quoting or parameterised queries.
- For a static Astro site on Cloudflare Workers, select compatible dependency versions, pin them deliberately and record the Node version and deployment configuration. Check package metadata before adopting versions. Search: `static Astro on Cloudflare Workers scaffold with pinned dependencies Node version and Wrangler configuration`.
- Test a Worker forms API with cases for wrong method, unknown route, invalid fields, missing verification token, foreign origin, oversized body and unsupported content type. Also test successful storage, replay handling, forged tokens, no-JavaScript redirects, and quiet rejection of honeypot or too-fast submissions.
- Before a build loop starts, record where the default stack does not apply and why. Search: `write down where workbench defaults do not apply before the build loop`.
- A leak-detection denylist derived from repository names, notices, configuration keys and package metadata is only as complete as its source inventory. Audit the inventory and test omissions deliberately.
- When copy work awaits business decisions, proceed with reversible defaults and list them explicitly so later answers require edits rather than structural rewrites.
- For a ceramic studio's About page, build a sourced fact set from approved business records and published material. Classify facts as publishable, needing confirmation or excluded before writing the page.
- Before a product page states a capability, verify the implementation that actually provides it and use wording that distinguishes available features from planned ones. Search: `check a capability against the path that serves it with a tense per capability`.
- When a canonical reference exists, compare the rendered build with it. A CSS-token comparison can catch brand-critical differences cheaply, but also inspect screenshots for layout and rendering discrepancies. Search: `visual diff against the canonical handoff when one exists`.
- When packaging a site project for another developer, make guidance portable: use shipped references and descriptive search phrases rather than private memory or database row identifiers. Search: `packaging a site project for another developer search phrases not IDs`.
## Curator Log: generic edition

| Date | Source | Action | Skills |
|------|--------|--------|--------|
| Not retained | Generic edition | REWRITE | Preserve skill IDs, tags and status markers so cross-references remain usable. Replace private context with generic web-development guidance. Keep each lesson, rule and reason without project-specific history. Use `RULE` for standing requirements. Retain `cookieconsent-port-template-001` and limit references in `persona-conference-injection-001` to shipped skills. |
| Not retained | Generic edition | REMOVE (records only) | Remove project-specific review histories and provenance notes that point only to unavailable review files. Preserve the reusable lessons in their skill entries. Removing historical records must not remove skill entries. |
