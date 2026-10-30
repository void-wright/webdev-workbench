---
name: aeo-optimization
description: Answer engine optimization (AEO): structure pages, FAQs and schema so AI answer engines can find, quote and cite a site. Use when writing or auditing content for AI search visibility.
---

# Answer Engine Optimization (AEO) Skill v1.0

## Skill Overview

**Purpose**: Comprehensive knowledge base and strategic guidance for Answer Engine Optimization (AEO) — the practice of optimizing content to appear in AI-generated responses from ChatGPT, Perplexity, Google AI Overviews, and other conversational AI platforms.

**Knowledge**: our AEO source guide and master knowledge base (`source_documents/`), split by topic into `knowledge/01_*.json` to `knowledge/08_*.json`  
**Sources**: 68 public pages, listed in `knowledge/sources.json` with title, link and a one-line summary each

The per-source detail gathered while building this skill is not redistributed; the sources list links to the originals.

## Core Definition

**Answer Engine Optimization (AEO)** is the practice of optimizing digital content to increase its chances of being selected, featured, and cited as a direct answer by AI-powered answer engines, voice assistants, and conversational search platforms.

## Critical Business Case

- **Zero-click answers**: a growing share of searches end on the results page because the AI answer is enough, so being the cited source matters more than winning the click
- **Higher-intent visitors**: people who do click through from an AI answer arrive further along in their decision
- **Large and growing platforms**: ChatGPT, Perplexity, Copilot and Google's AI features now answer questions for very large audiences
- **Measured case studies**: the source guide (Part VI) and the master knowledge base (`business_integration.case_studies`) give case-study figures, each with its citation

## Knowledge Base Structure

Each category file holds the synthesized guidance (`source_document_content`) and a `sources` list of entry numbers in `knowledge/sources.json`.

### 1. Core Concepts (`knowledge/01_core_concepts.json`)
- AEO vs. SEO vs. GEO definitions
- Zero-click search paradigm
- Micro-AEO framework
- Business case for AEO investment
- **Sources**: 13 listed

### 2. AI Platforms (`knowledge/02_ai_platforms.json`)
- Google AI Overviews (6.71% of queries)
- ChatGPT Search (GPT-4o + Bing integration)
- Perplexity AI (transparent citations)
- Microsoft Copilot (enterprise integration)
- **Sources**: 11 listed

### 3. Strategic Pillars (`knowledge/03_strategic_pillars.json`)
- Topical authority (hub-and-spoke model)
- E-E-A-T framework (Experience, Expertise, Authoritativeness, Trustworthiness)
- Brand mentions and off-site signals
- Entity consistency
- **Sources**: 2 listed, plus the source guide

### 4. Content Optimization (`knowledge/04_content_optimization.json`)
- Answer-first principle (40-60 word direct answers)
- Structured content elements
- Conversational language tactics
- Question-based content strategy
- **Sources**: 8 listed

### 5. Technical Foundation (`knowledge/05_technical_foundation.json`)
- Priority schema markup (FAQPage, HowTo, Article, Product)
- Crawlability fundamentals
- JavaScript rendering solutions
- Core Web Vitals optimization
- AI bot allowlist (robots.txt)
- **Sources**: the source guide and master knowledge base

### 6. Business Integration (`knowledge/06_business_integration.json`)
- B2B lead generation (5.5X multiplier)
- E-commerce optimization
- Local business AEO
- ROI measurement framework
- **Sources**: 3 listed, plus case studies from the source guide

### 7. Measurement Tools (`knowledge/07_measurement_tools.json`)
- Comprehensive AEO platforms (Atomic AGI, Writesonic, Semrush)
- 30+ specialized tools documented
- Schema implementation tools
- Technical SEO tools
- **Sources**: the source guide and master knowledge base

### 8. Future Trends (`knowledge/08_future_trends.json`)
- Multimodal search evolution
- Hyper-personalization
- AI agents and autonomous search
- Ambient information retrieval
- **Sources**: the source guide and master knowledge base

## Where the Figures Live

Adoption figures, case-study results and tool prices are kept in `source_documents/AI-Era_SEO_AEO_Documentation_Guide.md` and `source_documents/AEO_Master_Knowledge_Base.json`, each with its citation. Resolve a citation number in `knowledge/sources.json`, and check the original page before quoting a figure: these numbers date quickly.

## Implementation Roadmap

### Phase 1: Foundation (Months 1-3)
- Technical SEO audit
- Schema markup implementation
- Content audit and gap analysis
- Establish baseline metrics

### Phase 2: Content Optimization (Months 4-6)
- Rewrite high-priority pages (answer-first)
- Build topic clusters
- Voice search optimization

### Phase 3: Expansion (Months 7-12)
- New content creation
- Off-site signal building
- Platform-specific optimization

### Phase 4: Maturity (Ongoing)
- Performance monitoring
- Content refresh cycle
- Algorithm adaptation

## Critical Success Factors

1. **Answer-First Principle**: Direct answer in first 40-60 words
2. **Comprehensive Schema**: FAQPage, HowTo, Article, Product schemas
3. **Topical Authority**: Hub-and-spoke content clusters
4. **E-E-A-T Signals**: Experience, expertise, authoritativeness, trustworthiness
5. **Content Freshness**: AI platforms favour recently published or updated pages, so refresh content and show a visible update date
6. **Brand Mentions**: Unlinked brand mentions across authoritative sites
7. **Technical Excellence**: Fast Core Web Vitals, mobile-first, crawlable

## Platform-Specific Playbooks

### Google AI Overviews
- Implement comprehensive schema markup
- Target long-tail conversational queries
- Create passage-level content chunks (micro-AEO)
- Build topical authority with topic clusters
- Ensure fast Core Web Vitals

### ChatGPT Search
- Demonstrate E-E-A-T through author credentials
- Create comprehensive, in-depth content (2,500+ words)
- Optimize for conversational queries
- Include authoritative citations
- Maintain content freshness

### Perplexity AI
- Prioritize content recency
- Create fact-dense content with statistics
- Use clear source attribution
- Structure for direct question-answer format

### Microsoft Copilot
- Optimize for Bing SEO fundamentals
- Create enterprise-focused content
- Structure for business decision-making use cases

## Measurement Framework

### Visibility Metrics
- Featured snippet ownership
- AI Overview presence
- Knowledge Panel acquisition
- People Also Ask appearances
- AI platform citations

### Engagement Metrics
- Zero-click retention
- Post-click engagement
- Answer sufficiency score
- Micro-conversion rate

### Business Impact Metrics
- Answer-to-pipeline contribution
- Customer Acquisition Cost (CAC)
- Brand lift
- Revenue from AI traffic

## Traceability

Every claim in the source guide carries a numbered citation, and the master knowledge base lists source URLs beside its entries. `knowledge/sources.json` resolves each guide citation number to its title, link and a one-line summary of what the page covers.

## Usage Instructions

This skill provides:
1. **Strategic Guidance**: AEO principles and implementation frameworks
2. **Technical Specifications**: Schema markup, crawlability, technical requirements
3. **Platform Tactics**: Google AI Overviews, ChatGPT, Perplexity, Copilot optimization
4. **Measurement Tools**: 30+ specialized AEO analytics platforms
5. **Case Studies**: Real-world results summarised in the source guide, each cited

When generating AEO strategies or recommendations:
- Reference `knowledge/complete_knowledge_base.json` (the two source documents in full, plus the sources list) for authoritative facts
- Cite specific sources for all claims, using `knowledge/sources.json` for titles and links
- Use the category JSON files (`knowledge/01_*.json` to `knowledge/08_*.json`) for focused domain knowledge
- Keep every claim traceable to a cited source

### Loading the knowledge (run from this skill's folder)

```python
import json

sources = {s["n"]: s for s in json.load(open("knowledge/sources.json"))["sources"]}

# Resolve a citation number from the source guide, for example [39]
print(sources[39]["title"], sources[39]["url"])

# Read one category: the synthesized guidance plus the sources behind it
core = json.load(open("knowledge/01_core_concepts.json"))
print(sorted(core["source_document_content"]))
for n in core["sources"]:
    print(n, sources[n]["title"])
```

## File Structure

```
aeo-optimization/
├── SKILL.md (this file)
├── README.md (user-facing documentation)
├── knowledge/
│   ├── sources.json (every source: title, link, type, one-line summary)
│   ├── complete_knowledge_base.json (both source documents in full, plus the sources list)
│   ├── complete_document_transcript.json (both source documents, word for word)
│   ├── 01_core_concepts.json
│   ├── 02_ai_platforms.json
│   ├── 03_strategic_pillars.json
│   ├── 04_content_optimization.json
│   ├── 05_technical_foundation.json
│   ├── 06_business_integration.json
│   ├── 07_measurement_tools.json
│   ├── 08_future_trends.json
│   ├── category_analysis.json (which sources fed each planning category)
│   └── url_extraction_roadmap.json (the build plan)
└── source_documents/ (the source guide, the master knowledge base, a Google Ads companion guide and the build QA report)
```

Each category file's `sources` field lists the entries in `knowledge/sources.json` that informed it. The planning files (`category_analysis.json`, `url_extraction_roadmap.json` and `category_summary` in `complete_knowledge_base.json`) still group sources by the nine planning categories; tools and measurement were later merged into `07_measurement_tools.json`, and challenges and future trends into `08_future_trends.json`.

## Knowledge Distillation Methodology

**How the sources were gathered**: each of the 67 sources cited by the source guide was looked up on its public web page, and one further page was read during the build. Some pages could not be read (404s, redirects to a home page, security blocks); `read_when_built` in `knowledge/sources.json` records which. The notes taken from the pages are not shipped; the synthesized guidance is.

**Results**:
- Sources listed: 68 (the guide's 67 plus one)
- Read when built: 38
- Not readable when built: 30
- A further 26 pages from the build roadmap could not be read and are listed under `roadmap_only`

## Verification Standards

- **Source Count**: 68 sources listed
- **Citation Coverage**: every guide citation resolves in `knowledge/sources.json`
- **Maintenance Schedule**: Quarterly review recommended (AI landscape evolves rapidly)

---

**Version**: 1.0  
**Knowledge Base**: source guide and master knowledge base, split into 8 topic files  
**Traceability**: every guide citation resolves to a listed source
