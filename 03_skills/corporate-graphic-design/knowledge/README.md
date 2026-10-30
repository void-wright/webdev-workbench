# Corporate Graphic Design Knowledge Base - Complete Usage Guide

**Version**: 1.0  
**Sources**: 104, listed in `sources.json` with title, link and a one-line summary  
**Knowledge**: a research compilation on corporate design, preserved in `complete_document_transcript.json` and split by theme into `categorical_subsets/`

The per-source detail gathered while building this skill is not redistributed; the sources list links to the originals.

## Quick Start

### What Is This?

A citation-backed knowledge base for corporate graphic design covering:
- ✅ Design Principles (hierarchy, contrast, alignment, Gestalt psychology)
- ✅ Color Theory (psychology, RGB/CMYK, 60-30-10 rule, WCAG accessibility)
- ✅ Typography (font selection, pairing, readability, corporate systems)
- ✅ Layout & Grids (grid systems, responsive design, visual flow)
- ✅ Brand Identity (guidelines, consistency, style guides)
- ✅ Persuasion Psychology (Cialdini principles, social proof, scarcity)
- ✅ Production (file formats, prepress, print workflows)

### Directory Structure

```
corporate-graphic-design/knowledge/
├── README.md                                    # This file
├── sources.json                                 # All 104 sources: number, title, link, type, summary, category
├── complete_document_transcript.json            # The research compilation, word for word, with its Works Cited
├── categorical_subsets/                         # 7 thematic files
│   ├── 01_foundational_design_principles.json
│   ├── 02_color_theory_and_accessibility.json
│   ├── 03_corporate_typography.json
│   ├── 04_layout_and_grid_systems.json
│   ├── 05_brand_identity_and_consistency.json
│   ├── 06_psychology_of_persuasion.json
│   └── 07_production_and_file_formats.json
├── citations_database.json                      # Citation number to title, source, URL and access date
├── cross_reference_indexes.json                 # Navigation by category, topic and build status
├── url_extraction_roadmap.json                  # The build plan
└── ...(parent SKILL.md)
```

Each category file holds:
- `sources`: the source numbers for that theme (look them up in `sources.json`)
- `synthesis.sections`: the part of the research compilation that covers the theme, as text, with its section title and line range in the transcript

Run every example below from this `knowledge/` folder.

## Usage Examples

### Example 1: Finding Information About Color Psychology

**Scenario**: You need the guidance on color psychology for a branding project.

```python
import json

# Load the colour category (sources 16-35)
with open('categorical_subsets/02_color_theory_and_accessibility.json', 'r') as f:
    kb = json.load(f)

# The synthesized guidance for this theme
for section in kb["synthesis"]["sections"]:
    print(section["title"], section["line_range"])
    text = section["text"]

# Find the colour psychology passage
start = text.find("Psychology of Color in Marketing")
print(text[start:start + 800])
```

### Example 2: Navigating by Category

**Scenario**: Explore the sources behind the typography guidance.

```python
import json

sources = {s["n"]: s for s in json.load(open('sources.json'))["sources"]}

# Load categorical subset for typography
with open('categorical_subsets/03_corporate_typography.json', 'r') as f:
    typography = json.load(f)

# Overview
print(f"Category: {typography['category_name']}")
print(f"Description: {typography['description']}")
print(f"Total sources: {typography['total_sources']}")

# List every source in this category
print("\nSources in Typography Category:")
for n in typography["sources"]:
    print(f"  {n}. {sources[n]['title']}")
    print(f"     {sources[n]['summary']}")
```

### Example 3: Using Cross-Reference Indexes

**Scenario**: Find all sources related to WCAG accessibility standards.

```python
import json

# Load cross-reference indexes
with open('cross_reference_indexes.json', 'r') as f:
    indexes = json.load(f)

# Find sources by topic keyword
wcag_info = indexes["by_topic_keywords"]["accessibility_wcag"]
print(f"Topic: {wcag_info['topic']}")
print(f"Relevant sources: {wcag_info['url_numbers']}")
print(f"Total: {wcag_info['total_urls']}")

# Get the title and link for each
sources = {s["n"]: s for s in json.load(open('sources.json'))["sources"]}
for n in wcag_info['url_numbers']:
    print(f"\n{n}. {sources[n]['title']}")
    print(f"   URL: {sources[n]['url']}")
```

### Example 4: Finding Citation Source

**Scenario**: The compilation cites source 26 and you need the original.

```python
import json

# Option 1: the sources list (title, link, summary)
sources = {s["n"]: s for s in json.load(open('sources.json'))["sources"]}
print(sources[26]["title"])
print(sources[26]["url"])
print(sources[26]["summary"])

# Option 2: the citations database (adds the access date)
with open('citations_database.json', 'r') as f:
    citations = json.load(f)
cite_26 = citations["citation_to_url_mapping"]["26"]
print(f"Citation Number: {cite_26['citation_number']}")
print(f"Title: {cite_26['title']}")
print(f"Source: {cite_26['source']}")
print(f"URL: {cite_26['url']}")
print(f"Access Date: {cite_26['access_date']}")
```

### Example 5: Checking Build Status

**Scenario**: See which source pages could be read when the knowledge base was built.

```python
import json

# Load cross-reference indexes
with open('cross_reference_indexes.json', 'r') as f:
    indexes = json.load(f)

# Group sources by build status
statuses = indexes["by_extraction_status"]

print("Build Status Summary:")
for status, url_list in statuses.items():
    print(f"\n{status}: {len(url_list)} sources")
    if len(url_list) <= 10:  # Show details for small groups
        print(f"  Numbers: {url_list}")
```

The index keeps the build's own record numbers. They match the numbers in `sources.json` for 87 of the 104 entries; the `numbering` note in `sources.json` lists the 17 that differ.

## Navigation Strategies

### By Category (7 Categories)

Access categorical subsets for focused exploration:

```python
categories = {
    "01_foundational_design_principles": "sources 1-15",
    "02_color_theory_and_accessibility": "sources 16-35",
    "03_corporate_typography": "sources 36-52",
    "04_layout_and_grid_systems": "sources 53-63",
    "05_brand_identity_and_consistency": "sources 64-74",
    "06_psychology_of_persuasion": "sources 75-88",
    "07_production_and_file_formats": "sources 89-104"
}
```

The same ranges are stored under `categories` in `sources.json`.

### By Topic Keywords (19 Topics)

`cross_reference_indexes.json` groups source numbers under 19 topics: `design_principles`, `hierarchy_contrast_alignment`, `gestalt_psychology`, `color_psychology`, `color_models_rgb_cmyk`, `color_palettes_603010`, `accessibility_wcag`, `typography_fonts`, `font_pairing`, `layout_grid_systems`, `responsive_design`, `brand_guidelines`, `brand_consistency`, `style_guides`, `persuasion_psychology`, `cialdini_principles`, `social_proof_scarcity`, `file_formats_raster_vector`, `prepress_print_production`.

```python
import json

indexes = json.load(open('cross_reference_indexes.json', 'r'))
for topic, entry in indexes["by_topic_keywords"].items():
    print(topic, entry["url_numbers"])
```

## Technical Specifications

### Data Format Standards

**`sources.json` entry**:
```json
{
  "n": 34,
  "title": "Understanding Success Criterion 1.4.3: Contrast (Minimum) | WAI - W3C",
  "url": "https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum",
  "type": "official documentation",
  "summary": "The official W3C explanation of the WCAG minimum contrast success criterion, its intent and how to meet it.",
  "category": "02_color_theory_and_accessibility"
}
```

**Category file fields**:
- `category_id`, `category_name`, `description`, `creation_date`
- `total_sources`: how many sources the theme draws on
- `sources`: their numbers (integers)
- `synthesis.sections[]`: `section`, `title`, `line_range` (in `complete_document_transcript.json`), `text`

### Encoding

- UTF-8 throughout
- JSON indentation: 2 spaces
- Line endings: LF (\n)
- No BOM markers

## Quality Metrics

```
✅ Sources listed: 104/104 in sources.json
✅ Categorical Organization: 7/7 categories, each with its part of the compilation
✅ Citations Mapping: 104/104 citation numbers resolve
✅ Cross-Reference Indexes: 6/6 types
```

### Data Integrity

- ✅ All JSON files validate
- ✅ Every citation number in the compilation resolves in `sources.json`
- ✅ All categories have assigned sources

## Advanced Use Cases

### Use Case 1: Building a Corporate Brand Style Guide

**Step 1**: Read the design principles
```python
import json

principles = json.load(open('categorical_subsets/01_foundational_design_principles.json', 'r'))
for section in principles["synthesis"]["sections"]:
    print(section["title"])
```

**Step 2**: Determine color strategy
```python
import json

color = json.load(open('categorical_subsets/02_color_theory_and_accessibility.json', 'r'))
text = color["synthesis"]["sections"][0]["text"]

# The 60-30-10 rule (source 25)
start = text.find("The 60-30-10 Rule")
print(text[start:start + 700])
```

**Step 3**: Select typography system
```python
import json

typography = json.load(open('categorical_subsets/03_corporate_typography.json', 'r'))
print(typography["synthesis"]["sections"][0]["text"][:1000])
```

**Step 4**: Create brand guidelines framework
```python
import json

brand_identity = json.load(open('categorical_subsets/05_brand_identity_and_consistency.json', 'r'))
print(brand_identity["synthesis"]["sections"][0]["text"][:1000])
```

### Use Case 2: WCAG-Compliant Design Research

```python
import json

sources = {s["n"]: s for s in json.load(open('sources.json'))["sources"]}
indexes = json.load(open('cross_reference_indexes.json', 'r'))

# The WCAG sources, with links to read the standards themselves
for n in indexes["by_topic_keywords"]["accessibility_wcag"]["url_numbers"]:
    print(n, sources[n]["title"], sources[n]["url"])

# The compilation's summary of the contrast ratios
color = json.load(open('categorical_subsets/02_color_theory_and_accessibility.json', 'r'))
text = color["synthesis"]["sections"][0]["text"]
start = text.find("The Ratios (WCAG 1.4.3")
print(text[start:start + 600])
```

## Troubleshooting

### Issue: Cannot Find a Specific Source

**Solution**:
```python
import json

sources = {s["n"]: s for s in json.load(open('sources.json'))["sources"]}
print(sources[5])

# Or search titles and summaries
for s in sources.values():
    if "kerning" in (s["title"] + s["summary"]).lower():
        print(s["n"], s["title"])
```

### Issue: Want to See Where a Source Is Cited

**Solution**:
```python
import json

transcript = json.load(open('complete_document_transcript.json', 'r'))
lines = transcript["complete_text"]["full_document_lines"]

# The compilation puts citation numbers straight after the punctuation, as in "...background.32"
import re
body = lines[:transcript["sections"]["works_cited"]["line_range"][0] - 1]
for i, line in enumerate(body, start=1):
    if re.search(r"[.:)*]32\b", line):
        print(i, line.strip()[:120])
```

### Issue: Need Original Source Document

**Solution**:
```python
import json

# Load complete document transcript (the research compilation)
transcript = json.load(open('complete_document_transcript.json', 'r'))

# Access full text
original_text = transcript["complete_text"]["full_document_lines"]

# Access metadata
print(f"Source: {transcript['metadata']['source_file']}")
print(f"Total Lines: {transcript['metadata']['total_lines']}")
print(f"Total Citations: {transcript['metadata']['total_citations']}")
```

## Integration Examples

### With Claude Code Skills

```python
import json, glob

# 1. Load all seven themes
graphic_design_kb = {json.load(open(f))["category_id"]: json.load(open(f))
                     for f in sorted(glob.glob('categorical_subsets/*.json'))}

# 2. Cross-reference with technical documentation skill
# (if available in your environment)

# 3. Apply design principles to technical documentation
design_principles = graphic_design_kb["01_foundational_design_principles"]["synthesis"]["sections"]

# 4. Use color theory for branding
color_theory = graphic_design_kb["02_color_theory_and_accessibility"]["synthesis"]["sections"][0]["text"]
print(len(design_principles), len(color_theory))
```

## Maintenance and Updates

### Version History

- **v1.0**: Initial release
  - 104 sources listed with links and summaries
  - 7 thematic files carrying the research compilation
  - Complete citation system
  - 6-way cross-reference indexes

### Future Updates

Planned updates will address:
- New WCAG standards (when released)
- Emerging design trends
- Additional academic research
- User-contributed enhancements

### Contributing

To suggest improvements:
1. Review existing content
2. Identify gaps or outdated information
3. Provide source URLs for new content
4. Keep every claim traceable to a cited source

## License and Attribution

**Source Document**: a research compilation on corporate graphic design. It is not shipped as a separate file; its full text and Works Cited list are preserved in `complete_document_transcript.json`.

**Sources**: 104 (see `sources.json`). Each is credited by title and link; the source pages themselves are not reproduced.

## Support

For questions or issues:
1. Check this README
2. Review `../SKILL.md` for technical details
3. Inspect JSON files directly
4. Use cross-reference indexes for navigation

---

**Status**: Production Ready ✅  
**Architecture**: Synthesized guidance with numbered citations | Sources list with links
