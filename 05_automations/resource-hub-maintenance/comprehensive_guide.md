# Resource Hub Maintenance: comprehensive guide (generic edition)

> **Generic edition: for anyone standing up and caring for a resource hub on a site they own, with their own
> GitHub, Cloudflare or Vercel, and Sanity accounts.** The operating principles and practical lessons are kept;
> what changed and why is in `05_automations/resource-hub-maintenance/EDITION_NOTES.md`.
>
> **Persona**: the resource-hub curator (`05_automations/resource-hub-maintenance/personality.json`).
> **Counterparts** (also in this package): the first-build automation for new sites and the website-maintenance automation for the wider site and production launch.
> **Scope**: standing up, and then caring for, a CMS-backed resource hub on an Astro + Sanity site hosted on Cloudflare Workers or Vercel.

---

## What this automation does here

The assumed stack: Astro + Tailwind on the Node version your repo pins; your own GitHub repo; **Cloudflare Workers
with static assets + Workers Builds** (git integration) or **Vercel**, with `main` = production and `preview` (or any
feature branch) = a preview deployment; a Sanity project (dataset `production`, public-read unless you chose
otherwise); the site's own form stack. Setup guides: `09_guides/GITHUB_SETUP.md`, `09_guides/DEPLOY_CLOUDFLARE.md`,
and `09_guides/DEPLOY_VERCEL.md`.

The curator's work on that stack falls into two modes:

1. **Stand up the hub** (once): decide the resource types, wire the Sanity read path, build the listing and detail
   routes, connect publish-to-deploy, seed placeholders, run the UI through an ACE loop, and validate it on a preview
   before anything is public. A hub added to a live site is a section of an existing site, so the curator runs it with
   the first-build guidance in `05_automations/client-site-first-build/comprehensive_guide.md` available.
   If the request is a whole new site, use that automation.
2. **Care for it** (ongoing): add resources, adjust taxonomies and collections, import articles, swap files,
   regenerate card images, trigger rebuilds, and occasionally change the hub UI (ACE loop, 9.8 HARD).

**Working resources:**

- Keep decisions and reusable lessons in your repo alongside the packaged guidance.
- Access Sanity through its HTTP API with your own token; see `05_automations/resource-hub-maintenance/runbook_appendix/second_account_sanity_and_external_writer.md`. Ground facts in each resource's own source document.
- Use your repo and Sanity as the source of truth, and connect forms through your site's own stack.
- For structured review, use `04_reasoning/commands/inner-council.md`.
- Consult the relevant packaged guidance, including `03_skills/design-architect-thinking/SKILL.md`, `03_skills/resource-hub-thinking/SKILL.md`, `03_skills/website-maintenance-thinking/SKILL.md`, `03_skills/resource-hub-resource-page-builder/SKILL.md`, and `03_skills/resource-slug-design-canonical/SKILL.md`.

**PERSONA**: load `05_automations/resource-hub-maintenance/personality.json`. Maintain the curator's role for the whole run (§ Persona persistence).

---

## 🔴🔴🔴 CARDINAL RULE: handed-to-us, already-written content ships VERBATIM

**The first decision on ANY page is a classification, and it decides everything downstream:**

| The content is… | Mode | The prose is… | Workflow |
|---|---|---|---|
| **Already written & published by its owner, handed over ready to go** (an existing article, a finished page, a document) | **MODE A, VERBATIM** | **UNTOUCHABLE.** The owner's final editorial decision. | Strict-fidelity recreation or faithful integration of a finished self-contained page |
| **We author it** (resource pages we create: case study / video / guide editorial pages, new articles we are asked to write) | MODE B, authored | ours to write correctly | Source-grounded authoring and review |

**This cuts both ways; both directions are errors.**

- **Over-applying MODE A** to content we are supposed to author produces thin, under-written pages.
- **Under-applying MODE A** rewrites finished work without authorization. For example, sending a kitchen-equipment maker's published guides through an authoring process could paraphrase passages, merge paragraphs, turn headings into questions, and add introductions or takeaways. A later restyle can carry those changes forward unless fidelity is checked.

**The test is ONE question: did the owner already write and publish this and hand it over finished?** YES →
MODE A (adapt the template, never touch the prose). NO → MODE B (write it well). Unsure → ask the person you are
working with; guessing fails in one of the two directions.

**MODE A rules:** template chrome (hero, sticky TOC, accents, closing CTA) is fine; the content text is not
touched. No paraphrase or "smoothing" (`build upon` → `build on` is a violation), no merging paragraphs, no
heading rewrites, no added lede / "Key takeaways" / pull-quote unless the original has one.

**Mechanism (no LLM touches the prose):** fetch the original → extract its ordered content model
programmatically (bs4: headings, paragraph chunks as verbatim inner HTML, list items, byline, links) →
assemble into the template → **HARD content-fidelity check**: a normalized text diff of every content node
against the original, FAIL on any mismatch. Normalize only agreed formatting differences, preserve node order
and paragraph boundaries, and check links separately. Keep added chrome **outside `<main>`** so the comparison
covers the full source content without including template additions.

---

## ACE Loop Rule

Pure backend Sanity operations (adding documents, taxonomy terms, asset uploads, GROQ design) do NOT need an
ACE loop; they are deterministic content ops.

**ACE loop @ 9.8/10 HARD is REQUIRED when:** changing the hub's Astro components; changing its design system
(tokens, fonts, layouts); adding hub pages or page templates; significant copy/UX edits; authored resource
pages. Empirical Lighthouse + axe runs are required to clear 9.8; code-only review caps below it.
9.79 is CONTINUE; there is no rounding.

The loop is **design-generator → design-reflector → design-curator**, using
`05_automations/agents/design-generator.md`, `05_automations/agents/design-reflector.md`, and
`05_automations/agents/design-curator.md`. Run the **curator after EVERY iteration** to catch measurement
failures before they distort the next iteration, and once more at close. Keep temporary review workspaces
outside source and generated-output directories, and exclude them from version control.

---

## ⚠ Persona persistence

The lead assistant maintains the resource-hub curator's role from startup through the final review and
record updates. Answer mid-run questions in that voice. Sub-agents stay in their assigned role for their
whole task; repeat a review if role drift compromises its purpose. After a pause, re-read
`05_automations/resource-hub-maintenance/personality.json` and restore the working context.

---

## Mandatory Startup Protocol (do this first)

1. Read this guide end to end, load `05_automations/resource-hub-maintenance/personality.json`, read `05_automations/resource-hub-maintenance/skillbook.md` and `05_automations/resource-hub-maintenance/runbook_appendix/client_registry.md` (the record of your own sites; empty on first use).
2. **Batch lookup**: search the packaged memory and skillbook together. For example, run this from the package root:
   ```bash
   python - <<'PY'
   import json
   from pathlib import Path

   memory = Path("02_memory/webdev_pack.json")
   skillbook = Path("05_automations/resource-hub-maintenance/skillbook.md")
   sources = {
       str(memory): json.dumps(json.loads(memory.read_text()), ensure_ascii=False, indent=2),
       str(skillbook): skillbook.read_text(),
   }
   topics = ("ACE", "Sanity", "fidelity", "taxonomy", "credentials")
   for topic in topics:
       print(f"\nTopic: {topic}")
       found = False
       for source, content in sources.items():
           matches = [line.strip() for line in content.splitlines()
                      if topic.casefold() in line.casefold()]
           if matches:
               found = True
               print(source)
               print("\n".join(matches[:8]))
       if not found:
           print("No exact match; try related topic words.")
   PY
   echo "rc=$?"          # Capture the command's own status without an intervening pipe.
   ```
   This is a keyword lookup, not a semantic search. The phrases in `05_automations/resource-hub-maintenance/startup_queries.json` provide additional search terms. If one returns nothing useful, search with related topic words.
3. **State what came back** using titles and readable summaries. Before acting on a topic in the memory map below, find and read the relevant guidance.
4. **Credentials: read-only first**: follow `05_automations/resource-hub-maintenance/runbook_appendix/second_account_sanity_and_external_writer.md`. Keep keys in your own restricted configuration file with mode 600; parse them with the packaged tools and never source them as shell code. Before any write, verify that the Sanity `users/me` check returns 200, a token-free query succeeds if the dataset is public, and `bash 06_web_tools/wrangler-safe whoami` or `npx vercel whoami` names your own account.
5. **Frontier check**: compare the installed versions and configured integrations with the project's pinned requirements and relevant platform guidance. Report IN-SYNC or list the mismatches.
6. If the run will **generate images**, confirm your image tool works non-interactively before the build phase, with its key read from your own key file, stdin closed, and a timeout.

Any failed check → stop and fix setup using `05_automations/resource-hub-maintenance/setup_instructions.md` before touching content.

---

## Memory Map (recall phrases)

How to use it: when the trigger matches, search the packaged memory and skillbook with the phrase, or batch
several searches. The phrases in `05_automations/resource-hub-maintenance/recall_phrases.json` are search aids,
not guaranteed matches. If a phrase returns nothing useful, search with the "What you get" words and record
a useful replacement for future lookups.

### ACE loop and agents

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Any UI change to the hub (components, tokens, layout, copy) | `ACE loop quality bar 9.8 hard threshold` | why UI work loops to 9.8 HARD, no exceptions | § ACE Loop Rule |
| Reflector about to score without running the page | `empirical Lighthouse and axe scans required to clear 9.8` | code-only review caps below 9.8; measure | § ACE Loop Rule |
| Planning how many iterations a loop will take | `budget for repeated design and review passes` | allow time for correction and verification; do not promise a fixed pass count | Plan until the quality bar is met |
| Curator just closed a cycle | `store reusable skillbook lessons individually` | one reusable lesson per entry, with private details removed | Record lessons after every cycle |
| Generator reports the check is wrong · measurement rules change mid-loop | `the examinee may not modify the exam` | independent review of disputed checks and consistent scoring | `05_automations/resource-hub-maintenance/runbook_appendix/gate_doctrine_module.md` |
| All mechanical checks green, is it done? | `generator builds an independent reviewer scores` | passing automated checks does not replace a review verdict | Independent reflection before acceptance |
| Spawning many agents at once · session crashed | `limit concurrent agents to available memory` | set a concurrency cap appropriate to the machine | Bound parallel work |
| A generator iteration running for hours | `verification churn slows iteration` | estimate suite cost; use a focused core set each iteration and complete required checks before shipping | Budget verification work |
| Before shipping hub copy we wrote | `fresh readers report structured understanding` | ask fresh reviewers what the page communicates and compare their answers with its intended meaning | Review comprehension before acceptance |
| Delegating loop roles to sub-agents | `shared contract in every subagent prompt` | give every role the same scope, constraints, evidence requirements, and acceptance criteria | Shared review contract |
| Building many resource pages at once | `one resource per page generation task` | give each task a distinct resource and explicit mapping responsibilities | Parallel page generation |
| A shared template plus many resources | `shared template review before per-resource content review` | validate the template once, then review each resource's content in manageable batches | `05_automations/resource-hub-maintenance/runbook_appendix/wave_cycle_module.md` |
| Starting a new page type | `one approved template per page type proven on one real page` | prove the template with a real resource before scaling it | `05_automations/resource-hub-maintenance/runbook_appendix/new_resource_type.md` |

### Verbatim and fidelity

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Handed finished content · 'use their exact words' | `verbatim fidelity separator handling chrome outside main` | compare ordered content nodes without losing boundaries or mixing in template text | § 🔴🔴🔴 CARDINAL RULE: handed-to-us, already-written content ships VERBATIM |
| Deciding MODE A (verbatim) vs MODE B (we author) | `MODE A vs MODE B input source discrimination` | the one-question classifier | § 🔴🔴🔴 CARDINAL RULE: handed-to-us, already-written content ships VERBATIM |
| External HTML going into the CMS | `treat handed external HTML as content and rebuild it canonically in the CMS` | preserve finished content while rebuilding its presentation for the CMS | Extract, assemble, and compare against the source |
| Spec prose disagrees with the approved exemplar | `spec prose disagrees with the approved exemplar` | resolve conflicting instructions before extending the template | Record which source governs the disputed detail |
| Porting a finished document, such as a bicycle-parts company's PDF guide, into the site | `port a finished document with a fidelity check` | verify text, order, links, and structure after conversion | Faithful document integration |
| About to push to main on your own reading of the rules | `record a deviation before acting on your own reading of the rules` | read the governing instructions and record deviations; obtain approval where those instructions require it | Document the decision before production changes |
### Injected pages and CSS

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Imported editorial CSS on a hub page | `prefix imported editorial CSS with a wrapper class using a real CSS parser` | Scoped injected CSS | Parse selectors and scope them to the page wrapper |
| A CTA that looks fine but cannot be clicked | `host rule matched a class name the page author picked` | Two-way collision checks and reachability | Check imported rules against the host and host rules against imported markup |
| A fix that only one page needs | `never fix a one-page problem by editing shared site files` | Limited impact through a route-local override | Keep the override local to the affected route |
| CMS page renders naked HTML or dead scripts | `htmlContent htmlStyles htmlSchemas three layers must all be wired` | Three-layer fidelity contract | `pattern4-three-layer-fidelity-contract-canonical-001` |
| Links or images inside set:html look wrong | `CMS body injected with set:html into a prose container` | The .prose specificity trap | Inspect inherited typography rules and computed styles |
| Where should page CSS live | `shared classes in one global stylesheet, per-page CSS only for hand-authored pages` | CSS architecture | Keep shared rules central and page-specific rules scoped |
| Script-created elements come out unstyled | `Astro scoped styles do not reach elements created by client script` | Use :global() for runtime nodes | Scope global selectors beneath the component wrapper |

### Sanity and content operations

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Collections that fill themselves | `resource hub data model with four document types` | Collection binding | Use resource, taxonomy, collection and series documents |
| Sanity limits before a bulk job | `Sanity critical architectural constraints attribute limit` | Platform constraints | `05_automations/resource-hub-maintenance/runbook_appendix/sanity_content_ops.md` |
| Seeding many documents | `single atomic Sanity mutate POST when seeding documents` | Atomic seeding | `05_automations/resource-hub-maintenance/runbook_appendix/sanity_content_ops.md` |
| Filtering resources by several taxonomies | `GROQ patterns for a polymorphic hub` | GROQ filter patterns | `05_automations/resource-hub-maintenance/runbook_appendix/sanity_content_ops.md` |
| Stale build reads · a write fails with 'permission' | `Sanity patch followed by git push builds with stale content` | Sanity gotchas | `05_automations/resource-hub-maintenance/runbook_appendix/sanity_content_ops.md` |
| Storing JSON-LD in a Sanity field | `Sanity rejects @-prefixed keys in JSON-LD` | String-array schemas | `sanity-attribute-name-no-at-prefix-001` |
| Adding a new resource type | `adding a new resource type to a Sanity Astro resource hub` | New-type touchpoints | `05_automations/resource-hub-maintenance/runbook_appendix/new_resource_type.md` |
| Reviewing a hub before real content exists | `seed realistic marked placeholder documents for review` | Placeholder seeding and bulk deletion | R0–R2 below |
| Which resources get their own page | `emit a page only for resources whose HTML body is non-empty` | Hybrid page strategy | R0–R2 below |
| An article or blog as a hub resource | `store lean body styles and JSON-LD on the resource doc with one slug template` | Blog-as-resource | `pattern4-three-layer-fidelity-contract-canonical-001` |
| Imported HTML carries data-URI images | `strip base64 data URI images from CMS HTML at ingest and upload by hash` | Base64 extraction and a 200 KB payload check | Extract images, upload them once by hash and replace embedded data with asset URLs |
| A PDF opens with a tab named 'Untitled' | `design tool PDF exports carry a generic Title the browser shows as the tab name` | PDF /Title trap | Set the PDF title metadata and check the browser tab |
| Any bulk content op | `dry-run every bulk import, no placeholders in bodies, redeploy after CMS-only edits` | Content-operations hygiene | Preview changes, reject unfinished production bodies and rebuild static routes |
| A page live by URL but not in the listing | `hideFromListing for live but unlisted pages and publishedOnSite staging` | Visibility flags | `05_automations/resource-hub-maintenance/runbook_appendix/ssr_detail_and_hide_from_listing.md` |
| Temporarily removing a resource | `reversible isHidden flag in every listing query` | Reversible removal, including spotlights | Apply the visibility filter to every surface that lists resources |
| New CMS content 404s on its detail page | `statically generated detail route only knows slugs that existed at build time` | SSR vs SSG detail pages | R3 below |
| Making a CMS publish go live | `editor flips status to Published and the page is live` | Publish-to-deploy ladder | `05_automations/resource-hub-maintenance/runbook_appendix/redeploy_cloudflare_workers.md` |
| Site review before main | `per-resource preview flag and a review pause before main with idempotent re-ingest` | Preview-first review | Review the preview deployment before merging; make repeated imports safe |
| Linking between sibling pages in one batch | `cross-page slug resolution from sibling CMS patch data` | Cross-page slug resolution | `generator-cross-blog-slug-via-sibling-sanity-patch-not-directory-name-canonical-001` |
| Heavy article pages | `HTML payload size governance for article pages with images` | Performance governance | Measure serialized HTML and move embedded images to hosted assets |

### Library UI

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Filter sidebar and counts | `group library filters into accordion facets with matching counts` | Hub library UI | `sidebar-4-category-structure-001` |
| Related resources block | `use a compact related-resources grid with a consistent card limit` | Related-resources component | Select relevant resources and check the layout at the chosen card limit |
| CTAs on resource pages | `consistent CTA wording with one button and no offers the business does not make` | CTA hygiene | Keep the action truthful and avoid a redundant bottom CTA box |
| Gating a download behind a form | `a gated download thank-you page should confirm success before forwarding and provide a direct link` | Gated content and thank-you routing | Verify submission, forwarding and a visible fallback download link |
| A standalone landing page beside the hub | `standalone indexable framework pages outside the CMS listing` | Campaign landing pages | Give the page its own route and search metadata |
| Brand name casing drifts in imported text | `case-sensitive search on user-visible fields for brand mark casing` | Brand-name casing check | Search visible copy and metadata against the site's chosen spelling |

### Pages we author

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Writing a page we author | `page generator fetches the actual source before writing summaries` | Source-grounded content | `source-grounding-mandatory-for-all-resource-page-generators-001` |
| Naming a competitor in an article | `when a piece names a competitor concede real strengths` | Blog voice | `blog-fair-incumbent-voice-canonical-when-naming-competitor-001` |
| Generating card or hero images | `one locked visual reference for generated imagery` | Image prompting | `05_automations/resource-hub-maintenance/runbook_appendix/new_resource_type.md` |

### Hub page design

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Words over a hero, banner or spotlight image | `grade text over painted art at the worst pixels under the words` | Text-over-imagery checks | Measure contrast where each line actually crosses the image |
| Adding or removing a scrim | `scrim on the subdued background image` | Scrim rules | Judge the final image and overlay together under the text |
| A banner that must work on phones | `art-directed image container switches composition at the content breakpoint` | Cover-fit coverage math | Check cropping and text coverage at each composition change |
| Full-page screenshot looks wrong with sticky layers | `capture viewports at named scroll positions instead of full-page screenshots` | Review captures | Capture the states readers actually see |
| 'Headline in the first screen' on phones | `first-screen budget on small phones` | Small-phone first screen | Budget header, spacing and image height so the headline remains visible |
| A no-JS :target link | `link to the element the reader must see and give it scroll-margin-block` | No-JS target pattern | Account for sticky headers at the destination |
| Interactive legend or filter chips | `figure legend native buttons axe list violation` | Native buttons | Use buttons for actions and valid list markup when grouping them |
| Ambient motion on a page | `WCAG 2.2.2 pause for ambient header motion` | Pause control | Provide a usable pause control and respect reduced motion |
| Browser storage to remember a choice | `govern localStorage and sessionStorage by purpose and applicable consent requirements` | Purpose-based storage decisions | Assess whether persistence is necessary before storing a preference |
| Interactive figures on a hub page | `build-time figure layout solver` | Static-first figures | Compute the initial layout at build time and enhance it in the browser |

### Instruments

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Reading a check's exit status | `piping a check through tail can hide failure` | Preserve the check's exit status | Run the check directly and inspect its captured output afterward |
| Proving a new check with a mutant | `run the old check on the new mutant and compare the finding text` | Old-check control | Show that the added rule detects the intended failure |
| Which build did this check log grade? | `check log first line is the hash of the served tree` | Hash-first logs | Record the served build identity before findings |
| Lighthouse leaves temporary folders behind | `Lighthouse chrome-launcher TEMP folders` | Temporary-directory trap | Use a controlled temporary directory and clean up after the run |
| Waiting on a process to finish | `pgrep -f matches the shell running the check` | Self-match-safe liveness | Check the intended process without matching the checker itself |
| A check answers a nearby question | `cmd piped to tail returns the pipeline status` | Measurement-tool failure patterns | `05_automations/resource-hub-maintenance/runbook_appendix/gate_doctrine_module.md` |

### Accounts, credentials and Cloudflare

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Any Sanity/Cloudflare call where a second account exists | `clean environment allowlist, pinned account, negative test on the real path` | Ambient-credential separation | `05_automations/resource-hub-maintenance/runbook_appendix/second_account_sanity_and_external_writer.md` |
| Reusing a credential-bearing tool with an account flag | `separation by tool not by flag for a second account` | Separate tool entry points | `05_automations/resource-hub-maintenance/runbook_appendix/second_account_sanity_and_external_writer.md` |
| First contact with your Sanity project | `verify a Sanity project live and read-only before any write` | Read-only live verification | `05_automations/resource-hub-maintenance/runbook_appendix/second_account_sanity_and_external_writer.md` |
| Moving keys into protected storage | `one-way key sync that never echoes a value` | Key-sync discipline | `05_automations/resource-hub-maintenance/runbook_appendix/second_account_sanity_and_external_writer.md` |
| Wrangler might hit the wrong account | `wrangler account pin plus wrapper refusal and clean-environment builds` | Two account checks | `05_automations/resource-hub-maintenance/runbook_appendix/second_account_sanity_and_external_writer.md` |
| A Cloudflare deploy watcher reports green | `Workers Builds API may not list Worker Previews builds` | Watcher blind spot | `05_automations/resource-hub-maintenance/runbook_appendix/redeploy_cloudflare_workers.md` |
| Hosting choice for the hub on Cloudflare | `prefer Workers with static assets plus Workers Builds over Pages` | Workers launch hygiene | R0–R2 below |
| Keeping dependencies current | `check dependency releases each maintenance pass and prove green before a redesign` | Two-stage dependency review | Review available updates, then validate chosen upgrades before design changes |

### Capture and self-heal

| Trigger | Recall phrase | What you get | Skill / appendix |
|---|---|---|---|
| Capturing lessons on a long build | `tag maintenance lessons when recording them` | Tag at capture | Record the failure, fix and verification while the evidence is available |

---

## Standing up a resource hub on your own site

These phases apply first-build lessons to a hub added to an existing Astro site. Your repository and hosting project already exist. If they do not, start with `09_guides/GITHUB_SETUP.md` and `09_guides/DEPLOY_CLOUDFLARE.md` or `09_guides/DEPLOY_VERCEL.md`. For a whole new site, use `05_automations/client-site-first-build/comprehensive_guide.md`. Verify Cloudflare, Vercel and Sanity UI locations at execution time.

*Worked example used below (invented):* a garden-supply shop adds a "Garden know-how" hub with how-to articles, demonstration videos and printable planting guides. The same structure can support a kitchen-equipment maker's spec sheets, a bicycle-parts company's guides, a ceramic studio's care articles or a regional bakery chain's customer stories.

**R0: Decide before building (record each decision in the site record and project notes).**
- What it holds: resource **types** such as article, guide, video, case study or datasheet, and the four facets the library filters on. Keep the **four-document polymorphic model**: resource / taxonomy / collection / series. A new kind of content is a new taxonomy term, never a new document type. This keeps schema growth within the platform's attribute limits.
- Which resources get a page: only those with a real body; files and external links link out directly through a hybrid page strategy.
- Routes: `/resources/` for the listing and `/resources/<slug>/` for details. Follow `03_skills/resource-slug-design-canonical/SKILL.md`. Keep published slugs stable or add permanent redirects when they change.
- Render mode: decide it here, using R3, and write down the reason.

**R1: Accounts and credentials.** Follow `05_automations/resource-hub-maintenance/runbook_appendix/second_account_sanity_and_external_writer.md`. Reach each account through its own credentials and dedicated tool entry point, rather than an account flag on a tool carrying another account's credentials. Keep keys in a protected file outside the repository, with mode 600. Parse that file through the package's web tools; never source it as shell code. Inspect the shell for ambient vendor credentials without printing their values, and use `06_web_tools/wrangler-safe` to prevent unintended credential inheritance. Verify the intended project **live and read-only** before any write. With a public-read dataset, **the site build needs no Sanity token at all**. A write token belongs only in the authorized content-writing process and never enters the repository, site build or hosting environment.

**R2: Schema and seed.** Sanity needs no deployed Studio schema to start: documents can be written through the HTTP mutation API, and Studio can come later for the editorial UI. Seed with ONE atomic mutation POST per batch. Use deterministic `_id`s derived from the document role and stable content key, plus `createOrReplace`, so re-runs are idempotent. Seed realistic **placeholder** documents marked `isPlaceholder: true` plus the tag `PLACEHOLDER_REMOVE_BEFORE_LAUNCH`. This gives reviewers representative content and lets launch preparation bulk-delete those documents with one query.

**R3: The read path and render mode.** Build-time reads use a client with `useCdn: false`. Cached query responses can lag writes, so a patch followed immediately by a build can ship stale content. Keep the **listing and detail route in the same render mode**. The classic failure is an on-request listing beside a statically generated detail route: items published after the last build appear in the listing but return 404s when opened. Two options:
- **Static both + deploy hook (recommended start):** prerender both routes and rebuild on every Sanity publish through R4. Publication becomes visible after a successful build and deployment. This avoids a runtime Sanity dependency and runtime cache management.
- **On-request both:** render both routes on request, using `export const prerender = false` and the appropriate Astro adapter, such as `@astrojs/cloudflare` or `@astrojs/vercel`. Verify caching on the chosen host. On Vercel, inspect `s-maxage` behavior and `x-vercel-cache`. On Workers, do not assume generated responses are edge-cached; design and test Cache API usage or applicable cache rules. Inspect Cloudflare cache diagnostics such as `cf-cache-status` where applicable, rather than relying on Vercel headers.

**R4: Publish → deploy.** Build this ladder only as far as needed: (1) create a **deploy hook** for the production branch in Workers Builds or Vercel project settings. Treat its URL as a secret because anyone holding it can trigger builds; store it as `DEPLOY_HOOK_URL` in protected configuration. (2) Configure a Sanity **GROQ-powered webhook** for creation, updates and deletion of `resource`, `taxonomy` and `collection` documents in the production dataset, POSTing to the hook with the payload it requires. (3) Add a scheduled rebuild as a backstop only if webhooks prove unreliable. Verify end to end with a temporary document: publish → a new build appears → the page is live → delete it → another build removes it. **Instrument trap:** the Workers Builds API may not list preview builds. Pair `python3 06_web_tools/builds_watch.py` with a check of the deployed product using `python3 06_web_tools/preview_url_watch.py` and direct inspection of the deployment dashboard.

**R5: The UI, through an ACE loop (9.8 HARD).** Build the library page with four facets, dynamic counts, search and a featured row; detail templates for each page pattern; related resources; and one consistent CTA policy. Start from the site's existing tokens and components, choosing tokens already used successfully elsewhere on the site. Preview on the `preview` branch and use its deployment URL for review. Protect that deployment with Cloudflare Access or Vercel Deployment Protection if the hub must remain private before launch; see the deployment guides. Every hub page inherits the site's agent-readiness surfaces: build-time Markdown equivalents, JSON-LD, sitemap entries and an AI-readable site index. Add the hub to those outputs.

**R6: Graduation.** Bulk-delete placeholders with one query in one atomic transaction. Update the AI-readable site index and sitemap, then **search the built files** to verify the expected entries and confirm that placeholders are gone. Check links, resource visibility, filters, forms, accessibility, metadata and representative mobile layouts before merging `preview` → `main`. Merge only after `npx astro build` and the project's verification checks pass and the preview has been checked visually. Verify which branch protections the repository actually enforces; do not assume a hosting plan prevents a bad merge. Update the site record from "stub" to "live".

---
## Maintenance Workflows

Sanity calls below use the HTTP API with your own token: query
`https://<your-sanity-project-id>.api.sanity.io/v2024-01-01/data/query/production?query=…` (no token needed on a
public-read dataset), mutate `…/data/mutate/production` through `bash 06_web_tools/bearer-curl SANITY_API_TOKEN …`.
Run package commands from the package root. Recipes:
`05_automations/resource-hub-maintenance/runbook_appendix/sanity_content_ops.md`.
The project ID is in the site's Sanity client configuration.

Workflow letters are stable names that other files cite, so the sequence has gaps; there is no missing workflow.

### Workflow A: Add resources
1. Prepare documents with deterministic IDs, taxonomy references and slugs following `03_skills/resource-slug-design-canonical/SKILL.md`. **Dry-run** a batch first: print the mutation body and the slugs, then check for collisions with a GROQ count.
2. Upload files and images to Sanity assets. Asset IDs are content hashes, so identical bytes do not create duplicate assets. Fix exported PDF `/Title` metadata before upload because browsers show it as the tab name.
3. Send one atomic `/data/mutate` POST. Read back with GROQ and check counts by type.
4. Rebuild using Workflow F. Then search the built HTML for import artifacts, such as doubled quotes and page-builder comments, and for placeholder text.

**Content checkpoint:** counts match; no orphan taxonomy references; every card has a link target, whether a body page, file or external URL; CDN URLs resolve.

### Workflow A.1: Gated content (only if the site owner wants gating)
Gating is OFF by default because it adds friction for readers, and most hubs do not need to collect leads from downloads.
If a resource is gated, use a registry module keyed by slug and a landing route that renders the site's own form.
Keep the form flow fail-closed: an unsuccessful submission must not advance to the download step.
Send every successful submission through a per-slug thank-you page with a short forwarding delay, a meta-refresh
fallback and a visible manual link. Never redirect the form straight to the asset or put the asset in a query string.
Use a small set of preview bullets with short titles and one-sentence descriptions. Keep their length consistent
enough to scan.

### Workflow A.2: `llms.txt` and agent surfaces
Whenever hub content changes what the site says about itself, update its `llms.txt` agent summary and any
Markdown equivalents. Build, then **search the generated output** for the new markers AND the absence of removed
ones. Never trust an editor's diff alone. On a mismatch, re-read and rewrite the complete affected file.

### Workflow B: Taxonomies
Taxonomy `title` is Title Case display text; `slug` is kebab-case; `_id` follows a deterministic scheme such as
`facet.<category>.<slug>`. Add terms with `createOrReplace`; retag with patches in one transaction.
Duplicate-looking facets, such as “care guide” and “Care Guide” in a bicycle-parts library, can indicate two
documents sharing a slug under different IDs. Audit with a reference-count subquery, then patch references
and delete the duplicate in one transaction. Tag a guide for an additional use case only when its body
actually covers that use case.

### Workflow C: Collections
A collection binds by `(filterCategory, filterValue)` and fills itself; a product family can use a wildcard
such as `slug.current match 'mixing-tools*'` in a kitchen-equipment library. Featured image 4:3, hero 16:9.
If the collection appears on the hub home, update the home's collection map.

### Workflow D: Import an article series
Upload every image and audio file to Sanity assets; replace every placeholder in the bodies with the CDN URL.
**Prove zero placeholder text** with a GROQ `match` AND a search of the built pages. GROQ `match` tokenizes,
so it is not a substring test. Create the `series` document and set `series` + `seriesOrder` on each part.

### Workflow E: UI tweak to the hub (ACE loop, 9.8 HARD)
1. Create an isolated workspace with a task brief recording scope, routes and acceptance criteria.
2. Use `05_automations/agents/design-generator.md` to implement on a feature branch or `preview`. Use `05_automations/agents/design-reflector.md` to score the five review dimensions, with Lighthouse + axe run on the BUILT pages across the touched routes at 1440 / 768 / 375, plus small phones for first-screen claims. Use `05_automations/agents/design-curator.md` to update the skillbook after every iteration.
3. Plan for three review-and-fix iterations. Require the 9.8 threshold and resolved blocking findings before proceeding to Workflow F.

- For “comment out but keep ready,” use a frontmatter boolean flag gating a JSX block, never an HTML comment.
- If changed copy also appears in `llms.txt`, run Workflow A.2.

### Workflow F: Redeploy (Cloudflare Workers Builds)
Full recipes: `05_automations/resource-hub-maintenance/runbook_appendix/redeploy_cloudflare_workers.md`.

- **Code change:** commit on a feature branch or `preview`; run `npx astro build` locally and require exit 0 before pushing. This catches build failures before the remote deployment. Push, review the platform's preview deployment, then merge to `main` for production.
- **CMS-only change:** use the deploy hook. Call it manually following the redeployment appendix if the Sanity webhook is not wired yet. Do not assume an empty commit will trigger a build; use the hook or a real file change.
- **Verify** a string unique to the new build on the URL a reviewer actually uses. Never treat `curl -L` through a login page as deployment proof because the login page can return 200. For protected previews, use `06_web_tools/preview_url_watch.py` with an Access service token or a browser session.
- **Vercel:** follow the same sequence. If you pin a review alias to a preview, re-point it after every deployment. Setup: `09_guides/DEPLOY_VERCEL.md`.

### Workflow G: Quality verification (after every op)
Use scripted headless Playwright assertions at 1440 / 768 / 375: cards render, filters and search work,
series navigation works, images load, placeholder text is absent and brand-name casing is correct.
Use case-sensitive searches on user-visible fields. Then check every shipped slug against the live URL.
Require 200 responses for all of them. If one fails, check in order: is it published in Sanity, did the build
run, and was the route generated or configured to serve that slug?

### Workflow H: Post-run self-heal
Review failures and corrections after every run. Fix the underlying cause, repeat the affected checks and
record a reusable rule or assertion that will catch the same mistake next time. Do not close the run with
unresolved failures.

### Workflow I: Consent and storage (only if the hub adds tracking)
Assess analytics by what it collects and why, including implementations described as cookieless.
Browser storage needs the same purpose-based review as cookies. A preference saved at a visitor's request
differs from storage used for attribution or measurement; do not assume they have the same consent requirements.
If a hub feature adds non-essential storage or a tracking tag, put it behind a default-denied consent mechanism
before enabling it. Use vanilla-cookieconsent v3 and the consent entries in
`05_automations/resource-hub-maintenance/skillbook.md`, together with
`05_automations/resource-hub-maintenance/runbook_appendix/playwright_cookie_test_harness.md`.
Verify the applicable requirements at execution.

### Workflow K: Strict-fidelity recreation (MODE A)
For supplied, finished articles or pages, assign one design-generator per page. For larger sets, work in
batches small enough to review individually. Give each generator the source location, target, asset directory
and strict rules: byte-faithful prose; every `<img>` either a CDN URL or an `{{ASSET:file}}` placeholder with
`data-original-url`; internal links rewritten relative; external links preserved with
`target="_blank" rel="noopener"`; JSON-LD preserved and stored as a **string array** because Sanity rejects
`@`-prefixed object keys; CSS scoped under `.<slug>-page` using a real CSS parser.

Use a per-page reflector with byte-strict checks for paragraph and heading counts, source links, smart quotes,
alt text, schemas and the scope class. When N ≥ 2, add a final cross-page reflector for slug uniqueness,
the link graph, consistent author and organization URLs, featured images and zero base64 images.
Then bind assets, perform ONE atomic write, build and search the output.
Verify all three layers: source content fidelity, valid CMS storage and the rendered page's appearance and behavior.

### Workflow L: Resource page builder (MODE B, pages we author)
> Classify first. Supplied finished content belongs in Workflow K or U, never L.

1. **Load `03_skills/resource-hub-resource-page-builder/SKILL.md`** and `03_skills/resource-slug-design-canonical/SKILL.md` before anything else.
2. **Mapper:** use one read-only agent to enumerate resources with GROQ. Skip designated reference pages and pages whose body hash is unchanged. Map type to page pattern: a ceramic studio's externally hosted customer story becomes a link-out page with Article metadata; a video becomes a privacy-enhanced embed plus transcript with VideoObject; a document gets an inline preview with Article metadata; a how-to article uses the blog template. Prioritize the work and assign manageable batches. Write a mapping report and **halt for sign-off**.
3. **Batches:** assign one design-generator per page. Require each to fetch and read the real source first. Never write from memory or pretraining; omit a field rather than invent it. Each generator writes `htmlBody`, `htmlStyles`, `htmlSchemas` and a JSON mutation payload into its workspace, then returns. The orchestrator performs the atomic write. Use one design-reflector per page, pairing near-identical siblings where appropriate, while the next batch's generators work.
4. **Cross-page reflector** when N ≥ 2: check slug uniqueness, unchanged filters and search, card links pointing to the new pages, valid related resources, AEO validation and Lighthouse on one page per pattern.
5. Card link precedence: on-hub page → external URL → file → `#`. Treat the final fallback as an incomplete resource that must be resolved before release.
6. Build, push to `preview`, verify, then merge.

Sibling links come from the sibling's mutation payload `.slug.current`, never from a workspace directory name.
Embed generated HTML in mutation payloads with `json.dumps`, never through a `{{HTML}}` placeholder.

### Workflow U: Finished self-contained page (MODE A, no template)
When a site owner supplies a finished landing page that should ship essentially as authored, with its own markup
and CSS plus a normal card:

- **U1 Transform with a reproducible script, never by hand:** strip embedded `@font-face` base64 because the site loads its fonts. Move base64 images to the CDN with width/height and lazy/eager attributes, and rewrite any `<a href="data:…">` copies. Make video embeds privacy-enhanced. Remove HTML comments with bs4 `Comment` removal and `decode_contents()` serialization; assert no `<!--` remains because comments can expose internal notes.
- **U2 Scope the CSS both directions:** prefix every selector with `.<slug>-page` using a real CSS parser such as tinycss2, recursing into `@media` and `@supports`. Also check incoming styles: unscoped site rules can affect reused class names for properties the page never declared. Emit a page-scoped restoration block and a build-time collision detector that halts on layout-breaking properties such as `position`, `pointer-events`, `display`, `inset`, `z-index` and `overflow`.
- **U3 Wrap as `<main class="<slug>-page">`**, never edit the shared template or components for one page.
- **U4 Keep the page's own styles** because there is no template to fall back on. Record necessary deviations in the transformation script.
- **U5 Update new-type touchpoints together:** follow `05_automations/resource-hub-maintenance/runbook_appendix/new_resource_type.md`.
- **U6 Gate it, then prove the gate:** run a binary content-fidelity check over every content node plus `img@alt`, `iframe@title` and an orphan-text sweep, with declared removals and relocations. Mutation-test the check: it must FAIL on a reworded word, a deleted or split paragraph, an added lede or changed alt text, and PASS on non-content attribute-only changes.
- **U7 Interactive reachability:** for every interactive element, scroll it into view, then assert that `document.elementFromPoint(centre)` returns the element or a descendant.
- **U8 Route-local override:** CSS injected per resource must ship only on that route. A rule restricted to that route can fix a shared-chrome defect there without editing shared files. Give it enough specificity to beat Astro's scoped selectors, verify it appears in exactly one built page and report the site-wide defect separately.
- **U9 Choose selectors from the rendered DOM:** use `document.querySelectorAll` on the built page, never infer selectors from a component's stylesheet.
- **Ported geometry:** re-measure every viewport-edge distance, including `scroll-margin-top` and sticky `top`, against the site's real header height. Matching CSS properties does not prove that the resulting positions still fit the host page.

**🔴 BLAST RADIUS (protected):** prefer containing a change within the one page that needs it over editing
shared files, because a shared edit made for one page can silently break every other page. When a new artifact
collides with a shared system, adapt the artifact first. Assess the scope of the change before choosing the
remedy; a pre-existing site-wide defect needs a separate decision.

---

## Wave cycle: the two steps that get skipped

`generate → REFLECT → gate → seed Sanity → WRITE THE RECORD → next wave`.
**Never seed a wave whose predecessor is unreflected.** Good self-verification can be especially persuasive:
generators that check their own numbers and catch their own unsupported statements can make seeding feel
independently verified. Correct values can still express the wrong relationship. For example, a regional
bakery's customer story might attribute a delivery schedule to the wrong location even though both details
appear in the source.

For the record step, update the hub's content registry or editorial manifest in the same wave. Reconcile its
set of slugs against live Sanity in both directions: present in Sanity but missing from the record is a defect;
present in the record but missing from Sanity is a work item. Slugs are the join key.
Full module: `05_automations/resource-hub-maintenance/runbook_appendix/wave_cycle_module.md`.

**The general rule for every correction:** ask “what in the loop will ASK for this next time?” If the answer is
“I will remember,” it is not fixed.
## Gate doctrine (summary)

Every rule records a failure worth preventing. Full text is in `05_automations/resource-hub-maintenance/runbook_appendix/gate_doctrine_module.md`. (0) File a lesson under its
CLASS, not the tool that taught it. (1) One sample page cannot show the whole collection: **survey** every displayed
field (emptiness, shape, geometry, spread) before any batch. (2) Mutants prove a gate can FAIL; only a positive
control proves it can PASS. Ship both. (3) The work being checked may not change the check: keep checks fixed within
a loop and let an independent reviewer decide disputes. (4) A measurement can answer a nearby question: a pipe
reports the last command's status, and a tool's silence is evidence about the tool. (5) A required field with no
source invites invention: make such fields optional. (6) Write down how a number is derived, not just the number.
(7) An assertion only protects what it names. (8) A borrowed rule brings its assumptions: check that the field it
relies on tells entries apart here. (9) When documentation and working code disagree, start from the code and then
fix the documentation. (10) Review your own work independently: a separate reviewer catches shared blind spots.

**Disclosure principle (affiliate links and sponsored posts):** when the site earns money from a link or was paid or
given something for a post, say so next to the link or at the top of the post, in plain words. For an invented bicycle-repair
co-op, a guide that links to a tyre shop through an affiliate link says "We earn a small commission if you buy through this
link" beside that link, and a review of a free sample pump says the pump was a gift. Check both directions: every paid or
gifted link carries its disclosure, and no page claims a sponsorship or partnership that does not exist.

## Three-layer fidelity (CMS-stored HTML)

When a detail page renders CMS-stored `htmlBody` + `htmlStyles` + `htmlSchemas`, all three layers must be wired
or the page silently degrades to unstyled HTML: (1) every GROQ query feeding the page projects all three fields;
(2) the template injects the styles as a scoped `<style>` and the schemas as JSON-LD (hoist the template
strings into frontmatter; nested template literals inside `set:html` break esbuild); (3) `<script>` inside
injected HTML never runs (`set:html` is inert), so interactive behaviour lives in a page-level script gated on
a wrapper-class detector. Verify on the BUILT page (`rg` for the style marker, `application/ld+json` and the
wrapper) and on the deployed preview, not only on a standalone mock. Never put a literal `</script>` inside a script
element, not even in a comment. `htmlStyles` comments are public content: no internal notes in them.

## Hide from listing vs staging

`hideFromListing` keeps a page live and indexable by URL while removing its card from listing, related and
collection queries (detail and series queries stay unfiltered). A reversible `isHidden` removes it everywhere
without deleting content. A staging flag shows a document on previews only; on Workers derive "is this production"
from the build branch (for example, `WORKERS_CI_BRANCH`; verify the variable name at execution), and remember local
builds may not see the same variable. Recipes: `05_automations/resource-hub-maintenance/runbook_appendix/ssr_detail_and_hide_from_listing.md`.

## 🔴 Three-iteration graduation: the iter-1 reflection must be exhaustive

Target every loop at three iterations: generate → ONE exhaustive reflection → one fix round → one verification.
Ask for the full, exhaustive list of changes at the first reflection, because incremental findings cost extra
iterations, time and tokens. A review can identify only valid findings and still waste effort through poor
sequencing: each round names a few issues, then the next surfaces something present all along.

Paste into every design-reflector prompt: (1) **exhaustive, not prioritised**, including one-character items;
(2) **exact fix per item**, stating ADD or REPLACE and quoting both sides; (3) **separate blockers from accepted
residuals** with reasons; (4) sanity-check each prescription against its surrounding text; (5) declare
out-of-scope dependencies in the first reflection. **Stop signal:** shrinking increments with shrinking findings means
polishing; demand the complete remaining list or ship with declared residuals. Attention degrades across
iterations, so short loops support correctness too.

## 🔴 The reflection must come first

Orchestrator review is not independent reflection: the orchestrator wrote the spec and shares its blind spots. Spawn the
reflector after the first generated version, always. Repeated generation before independent review can preserve
the same mistaken assumptions and create avoidable fix rounds.

## 🔴 Geometric vs property collision: scoping has two halves

Scoping protects against *property* collisions, where a competing declaration overrides a value. It does nothing for *geometric* ones: a page
authored for a viewport without a fixed header can retain its small `scroll-margin-top` and sticky `top` offsets,
with nothing overridden, while every in-page jump lands under the site's header. Whenever ported styles are kept,
enumerate every viewport-edge distance and re-measure it against the real header height plus breathing room; test
by measuring where each jump target lands after clicking, at each breakpoint. Write doctrine as the PRINCIPLE
("the page's environment changed, so every assumption about it is unverified"), with the mechanism as an example.
The wording determines whether the next check catches the general failure or only that example.

## 🔴 Instrument discipline: the check is the artifact most likely to be wrong

A deliberately failing fixture proves a gate can detect that chosen failure, not that it covers the population.
A known-good control proves the gate can pass valid input. Probe every member of the
population and report `probed / found / missed`; re-derive the controls when the gate changes; add a structural
invariant that makes silent failure impossible. Enumerate shipped files and inspect their contents, including
a null-byte check when distinguishing text from binary output; never guess with an extension allowlist.
To find internal references in shipped content, extract every comment and judge each one.

Additional checks for misleading green results:

- **Never put a pipe between a gate and its exit status.** Redirect output, capture `$?` immediately, then inspect the log; do not pipe the gate through `tail`.
- **Prove a new rule against the OLD gate too** and compare finding TEXT, not counts.
- **Line 1 of every gate log = hash of the served tree + commit**; re-run any log whose hash differs.
- **A zero-input gate is not a gate:** print the input count beside every PASS.
- **CPU-timed gates are distributions** (≥5 runs, a named statistic, the spread); check Chromium's actual rendering backend and explicitly select the intended device tier before interpreting a fidelity result.
- **Report what the environment cannot run as "not run"**, never as passed.
- **Temporary folders:** Lighthouse/chrome-launcher can create browser-profile folders in the working directory when its temporary-directory variables point somewhere unsuitable; export a short, writable `TMPDIR/TEMP/TMP` in the runner. Check liveness with a self-match-safe pattern such as `[n]ame`, never a broad `pgrep -f` query that can match the checker itself.
- **JS state flags get verb-suffixed names.** For example, use `dataset.figureInitialized` for initialization state so it cannot accidentally reuse an attribute reserved for a live region.
- Probe a shared-config change with a plain invocation; never use `2>/dev/null` on a probe whose empty output could be mistaken for success.

## ACE Loop Refinements

**(a) Curator every iteration:** Generator → Reflector → Curator
each iteration, with small delta passes (ADD/UPDATE/TAG), plus a closing pass. At close, preserve every reusable
skillbook lesson in the project's durable notes, keeping generic patterns only. Per-iteration curation
lets a discovered instrument failure inform the next iteration's checks.

**(b) Paired reflectors:** as many reflectors as generator slices (one per page), then ONE cross-page certifier.

**(c) Build-output isolation:** the orchestrator builds once; each reflector serves the same output read-only on its own port
and never rebuilds.

**(d) Budget, machine limits, governance:**

- Budget the whole verification suite: the generator runs a fast core set on the final build; heavy sweeps run once per iteration in the reflector. A late fix re-runs only the checks its diff can affect; write the `git diff --stat` and the reasoning beside reused logs. Set a verification time budget before starting, then stop and report if it is exceeded. Audit a running agent from its artifacts, not its transcript.
- Machine limits: each agent may add model, indexing or browser processes. Choose concurrency from available memory and observed usage. After a crash, run one background job at a time until stability is established. Every agent prompt asks for incremental writes.
- Retire skills that predict the reviewer's score, because the score becomes a target. A valid counterexample retires a skill as written until it is corrected. Re-copy the skillbook into the next loop AFTER closing curation.
- Reaching the iteration cap with an honestly reported gap is healthy. Show the unresolved issue to the site operator; never bend an instrument or a threshold.

## Hub page design lessons

Resource hubs carry the same surfaces as the site: hero and collection banners, spotlight art, cards over art,
sticky filters and interactive figures. All belong in the ACE loop.

- **Words over imagery:** axe does not grade text over a raster background. Render with text transparent and check each line against BOTH the p99 luminance of its box AND the brightest pixel under the line. Never substitute p95 or a mean. For white text, calculate the applicable contrast ratio against those backgrounds; a luminance ceiling of 0.3 alone does not establish WCAG text contrast.
- **Scrims** mix toward their colour; a light scrim over dark art lifts its luminance. Grade with the scrim on and off, measuring the area beneath the words. Withdraw compensating scrims once the art itself provides sufficient contrast.
- **Art direction follows the content's breakpoint:** the visible share of image width under cover is `min(1, (boxW/boxH)/(imgW/imgH))`. Sweep widths and content states; tall boxes need a portrait source or a suitable focal point. Marks over cover-fit art are sized in displayed units (`scale = max(W/w, H/h)`). For stacked bands, measure the seam as deltaE.
- **Captures:** full-page screenshots can misrender sticky layers; capture viewports at named scroll positions. Test "headline in the first screen" at the actual VISIBLE viewport, including browser chrome, plus 320×568, 360×640 and 375×667. Sticky art windows on phones can use `100lvh` when they must remain stable as browser chrome changes. No-JS `:target` links point at the element the reader must see, with `scroll-margin-block`.
- **Components:** use native `<button>` elements for interactive legends and filters. Astro scoped styles do not reach script-created elements; use `:global()` where needed. Auto-starting motion over 5 seconds needs a visible pause control under WCAG 2.2.2, and should be disabled under reduced motion. axe cannot assess every visual effect of `mask-image`. Read containing-block comments before lifting a layer. Build interactive figures with a static fallback: solve layout at build time, fail on collisions, commit the solved data, provide an HTML equivalent and verify both.
- **Copy we author:** use a fresh reader per round, with rendered visitor text only, a fixed audience description, structured fields for what they understood and one open question. For a kitchen-equipment maker's resource library, a restriction such as "describe only documented features" supplies no product counts or coverage claims. Label operator-approved registry values `signed` in the same edit, and dry-run merges key by key. Treat renames as structural changes and verify them on built output.

## Launch readiness subset (before any major batch ships)

Walk these checks and record each as passed or explicitly waived with a reason: CMS flags (staging, hidden, hide-from-listing)
behave per branch; render mode is unchanged, with listing and detail in the intended mode; forms are untouched or re-tested
(a submission lands where it should, spam protection fails closed, mail is delivered); brand casing is checked; content quality is checked
(images present, dates current, change record written); links and routes pass a per-slug HTTP 200 check with zero failures;
reusable lessons are captured.

## Frontier version check (two tier)

**Tier 1, every run (cheap):** compare installed versions against `npm view <pkg> version` for `astro`, `@astrojs/sitemap`,
`@astrojs/cloudflare` (if on-request routes exist), `tailwindcss`, `@tailwindcss/vite`, `wrangler`,
`@sanity/client` and `typescript`. Also compare the project's pinned Node version against Astro's `engines.node` and the
Workers Builds image. Report IN-SYNC or the mismatches. Run installs inside a clean `env -i`, supplying only the
environment values required for installation, so dependency scripts never see ambient secrets.

**Tier 2, only on mismatch:** read the official migration notes, preserve self-contained notes with source
URLs, search the repository for affected patterns, upgrade on a branch, and prove the existing site builds green
before any other change. Clean the configured build output before running `npm run build`; require zero warnings.

## Cross-automation boundary

| Task | Owner |
|---|---|
| A whole new site | First-build automation (`05_automations/client-site-first-build/comprehensive_guide.md`) |
| A hub on an existing site: setup, ongoing content and hub UI | **This automation** |
| Site-wide edits outside the hub, production go-live, DNS and security headers | Website-maintenance automation (`05_automations/website-maintenance/comprehensive_guide.md`) |
## Self-heal protocol (end of every run)

1. **Flag at capture, not at the end:** every reusable note you store during the run carries the tags `selfheal:resource-hub-maintenance` and `webdev`. Add tags for other relevant automations after asking whether the lesson would help during routine site maintenance. This makes self-healing a targeted lookup instead of a reconstruction.
2. **Store dual-layer notes** as each step lands: `[OBJECTIVE] what happened, with relevant measurements and file names … [SUBJECTIVE/WHY] why it matters / what was confusing / what to do next time.` Batch related notes when your storage tool supports it.
3. **List this run's flagged notes** and, for each lesson that should apply again, **add or update an entry in `05_automations/resource-hub-maintenance/recall_phrases.json` with a tested recall phrase**. Check that the phrase retrieves the intended note among the top 5 results. Use descriptive phrases rather than opaque memory IDs.
4. Update `05_automations/resource-hub-maintenance/skillbook.md` with a curator log entry marked ADD, UPDATE, TAG or RETIRE, and add the run's audit log entry to `05_automations/resource-hub-maintenance/runbook_appendix/client_registry.md`.
5. Store a closing note: "POST-RUN SELF-HEAL COMPLETE: resource-hub-maintenance <site> <date>".

Keep these records within your own site's maintenance workflow.

## Open items (status to verify; not facts)

1. Each new hub starts as a stub: record its real state in the registry and keep this list current per site.
2. Treat on-request rendering with edge caching on Cloudflare Workers as unverified until tested for the site. Start with static rendering and a deploy hook unless the site's requirements justify another approach.
3. Before using an automated text-over-imagery check on a hub page, calibrate it against an already-approved banner.

## Edition history

| Edition | What |
|---|---|
| Public | Voidwright generic web-development edition. See `05_automations/resource-hub-maintenance/EDITION_NOTES.md`. |
