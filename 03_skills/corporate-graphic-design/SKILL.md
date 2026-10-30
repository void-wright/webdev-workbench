---
name: corporate-graphic-design
description: Corporate graphic design knowledge: layout, grids, typography, colour, persuasion and print and file formats. Use when designing or reviewing visual business materials.
---

# Corporate Graphic Design Skill

**Version**: 1.0  
**Knowledge**: a research compilation on corporate design (in full in `knowledge/complete_document_transcript.json`), split by theme into 7 category files  
**Sources**: 104 public pages, listed in `knowledge/sources.json` with title, link and a one-line summary each

The per-source detail gathered while building this skill is not redistributed; the sources list links to the originals.

## Overview

The Corporate Graphic Design skill provides comprehensive, evidence-based knowledge for professional corporate design across all dimensions: design principles, color theory, typography, layout systems, brand identity, persuasion psychology, and production workflows.

### Core Capabilities

- **Design Principles Mastery**: Hierarchy, contrast, alignment, proximity, repetition, balance, white space, Gestalt psychology
- **Color Theory Expertise**: Color psychology, RGB/CMYK models, 60-30-10 rule, brand color strategies, WCAG accessibility
- **Typography Systems**: Font selection, pairing strategies, readability optimization, corporate typography best practices
- **Layout & Grid Systems**: Professional layout techniques, responsive design, grid frameworks, visual flow
- **Brand Identity**: Brand guidelines, consistency strategies, style guide creation, multi-platform branding
- **Persuasion Psychology**: Cialdini's principles, social proof, scarcity, authority, visual trust-building
- **Production Workflows**: File formats (raster vs vector), prepress checklists, print production, technical specifications

## Traceability

The research compilation cites a numbered source after each claim. `knowledge/sources.json` resolves every number to the source's title, link and a one-line summary of what it covers.

### Knowledge Base Structure

```
knowledge/
├── complete_document_transcript.json     # The research compilation, word for word, with its Works Cited
├── sources.json                         # Every source: number, title, link, type, one-line summary, category
├── categorical_subsets/                 # 7 thematic files: the matching part of the compilation plus the source numbers
├── citations_database.json              # Citation number to title, source and URL
├── cross_reference_indexes.json         # Navigation by category, topic and build status
├── url_extraction_roadmap.json          # The build plan
└── README.md                            # Complete usage guide
```

## Sources by Category (104 sources across 7 categories)

| Category file | Source numbers | Core topics |
|---|---|---|
| `01_foundational_design_principles` | 1-15 | Hierarchy, contrast, alignment, proximity, repetition, balance, white space, Gestalt psychology |
| `02_color_theory_and_accessibility` | 16-35 | Color models, harmony schemes, 60-30-10 rule, color psychology, WCAG contrast |
| `03_corporate_typography` | 36-52 | Font psychology, classification, pairing, hierarchy, kerning and spacing, document fonts |
| `04_layout_and_grid_systems` | 53-63 | Grid types and anatomy, report and presentation layout |
| `05_brand_identity_and_consistency` | 64-74 | Brand guidelines, style guides, consistency across channels |
| `06_psychology_of_persuasion` | 75-88 | Cialdini's principles, social proof, scarcity and urgency, trust |
| `07_production_and_file_formats` | 89-104 | Raster vs vector, file formats, prepress checklists |

Titles, links and summaries for every number are in `knowledge/sources.json`.

## Usage Instructions

### Accessing Knowledge

All knowledge is stored in JSON files. Run these examples from this skill's folder.

```python
import json

# Every source, by number
sources = {s["n"]: s for s in json.load(open("knowledge/sources.json"))["sources"]}
print(sources[34]["title"], sources[34]["url"])

# Load a categorical subset: the synthesized guidance plus the sources behind it
with open("knowledge/categorical_subsets/02_color_theory_and_accessibility.json") as f:
    color_knowledge = json.load(f)
print(color_knowledge["sources"])
for section in color_knowledge["synthesis"]["sections"]:
    print(section["title"])
    print(section["text"][:300])
```

### Navigation Systems

**By Category**:
```python
import json

# Load cross-reference indexes
with open("knowledge/cross_reference_indexes.json") as f:
    indexes = json.load(f)

# Get all source numbers in the color theory category
color_urls = indexes["by_category"]["02_color_theory_and_accessibility"]["url_numbers"]
print(color_urls)  # [16, 17, 18, ..., 35]
```

**By Topic**:
```python
import json

indexes = json.load(open("knowledge/cross_reference_indexes.json"))

# Find source numbers about specific topics
gestalt_urls = indexes["by_topic_keywords"]["gestalt_psychology"]["url_numbers"]
wcag_urls = indexes["by_topic_keywords"]["accessibility_wcag"]["url_numbers"]
print(gestalt_urls, wcag_urls)
```

**By Citation**:
```python
import json

# Load citations database
with open("knowledge/citations_database.json") as f:
    citations = json.load(f)

# Find the source for citation 21
cite_21 = citations["citation_to_url_mapping"]["21"]
print(cite_21["title"], cite_21["source"], cite_21["url"], cite_21["access_date"])
```

## Key Facts From the Compilation

- **WCAG contrast (1.4.3, Level AA)**: normal text needs at least 4.5:1 against its background; large text and non-text UI components need at least 3:1 (sources 32-35)
- **60-30-10 rule**: a dominant color for about 60% of the design, a secondary for 30% and an accent for 10% (source 25)
- **RGB vs CMYK**: RGB is additive and for screens; CMYK is subtractive and for print (sources 16-19)
- **Raster vs vector**: vector art is resolution-independent; raster images depend on resolution, so supply print images at print resolution (sources 89-98)
- **Bleed**: artwork that prints to the edge must extend past the trim line (sources 100-104)

The full reasoning, and every other point, is in the category files' `synthesis` sections.

## Quality Assurance

- ✅ **104 sources listed** in `knowledge/sources.json`, numbered as in the compilation's Works Cited
- ✅ **Citation traceability**: every citation number in the compilation resolves to a listed source
- ✅ **7 Categorical Subsets** (organized by theme, each with its part of the compilation)
- ✅ **6 Cross-Reference Indexes** (multi-dimensional navigation)

## Technical Specifications

**Data Formats**:
- JSON: All structured knowledge
- UTF-8 encoding throughout
- ISO 8601 dates
- Semantic versioning

## Integration with Other Skills

This skill pairs well with:
- **design-architect-thinking** and **prototype-website-generation** (both in this package): apply the colour, type and layout rules when designing a site
- **Technical documentation**: Visual communication strategies

The knowledge base was built with a URL-by-URL knowledge-distillation method; that build skill is not included in this package, and you do not need it to use the knowledge here.

## Maintenance and Updates

**Version**: 1.0 (Initial Release)  
**Next Update**: As needed for new design trends or standards  
**Update Triggers**: WCAG updates, major design framework changes, new research findings

## Citations and Sources

All 104 sources are listed in `knowledge/sources.json` with:
- Title and link
- The kind of source (article, documentation, community discussion and so on)
- A one-line summary of what the source covers
- The category it supports

`knowledge/citations_database.json` also gives the date each source was accessed when the knowledge base was compiled (re-check a source before relying on it).

See `knowledge/README.md` for complete usage guide and examples.

---

**Architecture**: Synthesized guidance with numbered citations | Sources list with links  
**Status**: Production Ready ✅
