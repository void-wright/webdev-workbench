---
name: resource-slug-design-canonical
description: Canonical slug derivation algorithm for resource hub pages, blog posts, and any URL-bearing content across every site you run. Enforces kebab-case, ≤80 chars, MAX 5 descriptor words, a content-tracker-as-source-of-truth contract (Notion or similar) with PATCH write-back after slug commit, and once-published-never-change discipline (or set up permanent redirect). Use when designing or deriving a slug for ANY new resource, blog post, landing page, or static page; when assessing whether an existing slug needs to be retired vs rewritten; when planning the tracker Slug column write-back step at the end of a resource-page build. Trigger on: "slug", "URL design", "page URL", "what should this slug be", "is this slug too long", "Notion Slug column", "rewrite slug", "permanent redirect for slug change".
---

# Resource Slug Design Canonical

You design URL slugs for resource hub pages and any other URL-bearing content. The slug IS the URL — it lives forever in SEO indexes, LLM caches, customer bookmarks, and citation graphs. Treat it accordingly.

This skill is invoked by:
- **Wren** (resource-hub-maintenance) during the slug pre-flight of a resource-page build, when deriving missing slugs, and at the final tracker Slug write-back
- **Wren** ingest, when the tracker's Slug column is empty
- **Backus** (client-site-first-build) when scaffolding the initial resource set
- **Cassian** (website-maintenance) when adding new pages or proposing slug changes

## The 5 Rules

1. **Format**: kebab-case, lowercase, ASCII only.
2. **Length**: ≤80 characters total.
3. **Word budget**: MAX 5 descriptor words.
4. **Source of truth**: the content tracker's Slug column FIRST (read before deriving), when the site keeps one (Notion, Airtable, a spreadsheet).
5. **Stability**: once published to production, NEVER change without setting up a permanent (301) redirect.

## Word-Budget Discipline

You have **5 descriptor words** maximum. Use them for the highest-signal terms. Drop everything else.

**Drop unconditionally**:
- Articles: `a`, `an`, `the`
- Conjunctions: `and`, `or`, `of`, `for`, `with`, `in`, `on`, `at`, `to`, `from`, `by`
- Vague qualifiers: `our`, `your`, `new`, `latest`, `complete`, `comprehensive`
- Marketing flourishes: `revolutionary`, `breakthrough`, `cutting-edge`, `next-gen`
- Year/date stamps unless meaningful (e.g., `2025-q3-update` — yes, content recency; `the-2024-method` — no, not relevant)

**Preserve**:
- **Quantifiers** that carry meaning: `10x`, `5g`, `700c`, `3d`
- **Acronyms** in lowercase: `diy`, `gps`, `uv`, `led`, `pdf`, `faq`
- **Version suffixes** when meaningful: `v2`, `gen3`, `2024-update`
- **Domain-anchor terms** that disambiguate: `tire` vs `tube` vs `rim` (on a bicycle-repair co-op's hub)

## Worked Examples

Each example below shows one rule. They come from three invented hubs: an amateur astronomy club, a seed library and a neighbourhood bakery.

**Rule: flourishes never reach a slug.** The bakery's "The Complete, Revolutionary Guide to Laminated Dough at Home" becomes `laminated-dough-home-guide`. "The", "complete", "revolutionary", "to" and "at" are all on the drop list.

**Rule: a format label belongs in the resource type, not the slug.** The seed library's "Recorded Talk: Keeping Bean Varieties Pure Without Cross-Pollination" becomes `bean-varieties-cross-pollination`. The hub already records that it is a talk.

**Rule: a question-style title collapses to `faqs`.** "Your Questions Answered: Borrowing and Returning Seeds" becomes `seed-borrowing-returning-faqs`.

**Rule: a decimal becomes a hyphen and counts as one descriptor.** The astronomy club's "Moons of Jupiter at Magnitude 5.6: Observing From a City Rooftop" becomes `jupiter-moons-magnitude-5-6-rooftop`. "Observing from a city" goes so the slug stays at five descriptors.

**Rule: keep a content type that readers search for as a suffix.** "Case Study: Halving Morning Waste With a Pre-Order Window" becomes `pre-order-window-waste-case-study`.

**Rule: a leading size or count stays as written.** "12-Inch Dobsonian Setup Checklist" becomes `12-inch-dobsonian-setup-checklist`, because that number is how members search for it.

## Algorithm (procedure)

```python
def derive_slug(title: str, max_chars: int = 80, max_words: int = 5) -> str:
    # 1. Lowercase, strip punctuation, normalize whitespace
    s = title.lower()
    s = re.sub(r"[''""`]", "", s)        # smart quotes
    s = re.sub(r"[^\w\s-]", " ", s)       # other punct → space
    s = re.sub(r"\s+", " ", s).strip()

    # 2. Tokenize
    words = s.split()

    # 3. Drop stopwords + flourishes
    DROP = {"a", "an", "the", "and", "or", "of", "for", "with", "in", "on",
            "at", "to", "from", "by", "our", "your", "new", "latest",
            "complete", "comprehensive", "revolutionary", "breakthrough",
            "cutting-edge", "next-gen", "how", "why", "what", "when",
            "frequently", "asked", "questions"}
    words = [w for w in words if w not in DROP]

    # 4. Collapse common multiword phrases to acronym/short form
    # (this requires a per-domain mapping: start with your field's common phrases)
    REWRITES = {
        ("do", "it", "yourself"): "diy",
        ("seed", "saving"): "seed-saving",
        ("wheel", "truing"): "wheel-truing",
        ("price", "list"): "price-list",
        ("recipe", "card"): "recipe-card",
        ("frequently-asked-questions",): "faqs",
        ("white", "paper"): "white-paper",
        ("case", "study"): "case-study",
    }
    # apply rewrites greedily left-to-right
    words = apply_rewrites(words, REWRITES)

    # 5. Cap at max_words descriptors
    words = words[:max_words]

    # 6. Join with hyphens
    slug = "-".join(words)

    # 7. Length check
    if len(slug) > max_chars:
        # truncate at word boundary
        while len(slug) > max_chars and "-" in slug:
            slug = slug.rsplit("-", 1)[0]

    return slug
```

## Tracker-as-Source-of-Truth Contract

This section applies when the site keeps a content tracker. Notion is the worked example; the same order works for any tracker with an API. Without a tracker, skip steps 1, 2 and 7.

**Read order** (ALWAYS):

1. **READ the tracker's Slug column FIRST** (before any derivation logic).
2. **If Slug present**: use it verbatim. Governance respected. Do NOT re-derive.
3. **If Slug empty**: derive via the algorithm above.
4. **Verify uniqueness in Sanity** via GROQ: `count(*[_type=='resource' && slug.current=='<candidate>']) == 0`
5. **If collision**: append disambiguator (`-2`, `-part-2`, year `-2025`, or pattern type `-guide`).
6. **Reserve in Sanity**: set `slug.current = <derived>`.
7. **Write back to the tracker**: PATCH the Slug column.

**Notion API write-back** (the last step of a resource-page build; keep `NOTION_TOKEN` in your own key file, for example `~/.config/notion/keys.env` with mode 600, never in the repo or chat):

```bash
curl -X PATCH "https://api.notion.com/v1/pages/<page-id>" \
  -H "Authorization: Bearer ${NOTION_TOKEN}" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "Slug": {
        "rich_text": [{"type":"text","text":{"content":"<canonical-slug>"}}]
      }
    }
  }'
```

**Skip rules** for write-back:
- Notion already matches canonical → SKIP.
- Notion empty AND we derived → WRITE.
- Notion set AND differs from canonical → SKIP (governance: we used Notion's value).

**Batching**: parallelize 6-10 PATCH calls at once via background bash + wait. Notion API rate limit is 3 requests/sec/integration but bursts are tolerated (as of October 2026; re-check before relying on it).

## Stability Rule

**Once a slug is published to production, NEVER change it without setting up a permanent (301) redirect.**

Slug churn breaks:
- SEO indexes (search engines treat new slug as new page; old equity is lost or penalized)
- Customer bookmarks
- LLM-cached references in training corpora
- Citations in academic / industry publications
- Cross-linked content within the hub itself

If a slug genuinely must change:
1. Add the OLD slug to a redirect map (Cloudflare `public/_redirects`, Vercel `vercel.json` `redirects[]`, or Astro middleware).
2. Configure 301 (permanent) redirect from OLD → NEW.
3. Update all internal links to NEW.
4. Notify Cassian (website-maintenance) of the redirect addition for promote-to-production validation.

## Edge Cases

Check these in order: the first two can break a build or a live link, the rest only change the spelling.

1. **The slug would collide with a framework route** (`api`, `_astro`): prefix it with its content area, for example `guides-api` or `talks-api`.
2. **The slug already exists in the CMS**: add a disambiguator (the year, `-part-2`, or the content type). Never reuse a published slug for new content.
3. **A comparison sign or a decimal** (`<5%`, `5.6`): `<` becomes `lt` and `.` becomes `-`, giving `lt-5-percent` and `5-6`.
4. **A slash** (`f/8`, `24/7`): `/` becomes `-`, giving `f-8` and `24-7`.
5. **A case-sensitive catalogue or part code** (`NGC 7000`, `M31`): lowercase it but keep it whole, for example `ngc-7000-nebula-imaging`.
6. **A maker's model name** (for example "Acme Skytracker"): lowercase it, giving `acme-skytracker-review`.
7. **A title that is mostly a year** ("2025 Members Report"): the year is a descriptor, giving `2025-members-report`.
8. **A question** ("Why do sourdough starters go flat?"): drop the question words and keep the noun phrase, giving `sourdough-starter-going-flat`.

## Anti-Patterns

❌ **Don't include the site owner's name in slug**: `ridgeway-ceramics-glaze-guide`. The slug is hub-relative; the domain already encodes the owner.

❌ **Don't include content type in slug unless disambiguating**: `blog-post-wheel-truing` — pattern is clear from rendering; only add `-guide`, `-video`, `-checklist` when needed for disambiguation.

❌ **Don't include date stamps for evergreen content**: `wheel-truing-2024-update` — only add date if content is genuinely time-bound.

❌ **Don't use camelCase or snake_case**: `wheelTruing` or `wheel_truing` — kebab-case is the SEO convention.

❌ **Don't auto-append numeric suffixes for "prettiness"**: `spoke-tension-2`, `spoke-tension-3` — only when collision genuinely exists.

❌ **Don't change slug to "improve" SEO mid-cycle**: once published, stability beats optimization. Use the redirect path instead.

## Cross-References

- Skill `resource-hub-resource-page-builder/SKILL.md` (this package)
- Skill `resource-hub-thinking/SKILL.md` (this package)
- The resource-hub-maintenance automation (`05_automations/resource-hub-maintenance/`): its resource-page build ends with the tracker Slug write-back, and its ingest reads the tracker Slug first
