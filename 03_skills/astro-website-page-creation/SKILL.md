---
name: astro-website-page-creation
description: Build and edit pages on an Astro website with Claude: page structure, components, content collections, verification. Use when creating or changing Astro pages.
---

# Skill: Claude-Centered Astro Website Page Creation

## Version: 1.0.0
## Last Updated: See the package revision history

## Purpose
Defines the end-to-end workflow for creating website pages where Claude is the central controller, from fully rendered HTML preview through ACE-vetted Astro decomposition to live deployment.

## Core Principle: Render First, Decompose Second
**NEVER start by writing Astro components directly.** Always generate a complete, self-contained HTML page first so the user (and Claude via Playwright) can review the full visual result before any framework decomposition.

---

## Workflow: 6 Stages

### Stage 1: Content & Messaging Alignment
1. Read the project's audience description, business goals, and approved messaging
2. Read the page's content brief or campaign plan, if one exists
3. Read the project's design tokens for colors, typography, and spacing
4. Identify which messaging themes, value propositions, and supported claims apply to this page
5. Draft a page content outline with sections, headings, and copy aligned to that messaging

### Stage 2: Fully Rendered HTML Generation
1. Generate a **complete standalone HTML file** with ALL CSS inlined
2. Use the design system tokens for colors, typography, spacing, shadows, and transitions
3. Include responsive breakpoints (mobile 639px, tablet 1023px, desktop)
4. Load the project's selected web fonts; if a licensed font is not available yet, use a suitably licensed substitute and note the swap
5. Include scroll-reveal animations and interactive elements, with reduced-motion support
6. Save the file in a dedicated preview location outside generated build output

**The fully rendered HTML is the "source of truth" for visual review.**

### Stage 3: Visual Review with Playwright
1. Use Playwright MCP (`browser_navigate`, `browser_screenshot`) to open the rendered HTML
2. Take screenshots at 3 viewport widths: 1440px (desktop), 768px (tablet), 375px (mobile)
3. Inspect for:
   - Color accuracy against the design system
   - Typography hierarchy and spacing
   - Layout grid alignment
   - Button/CTA styling
   - Responsive behavior
   - Text overflow or squished content
   - Visual rhythm and whitespace
4. Document issues found
5. Fix issues in the HTML and re-screenshot until clean

### Stage 4: User Review
1. Present the fully rendered HTML location to the user
2. User opens it in a browser and provides feedback
3. Iterate on HTML until the user approves
4. Keep this feedback loop in a single file so changes are immediately visible

### Stage 5: ACE Loop on Rendered HTML
1. Deploy **Reflector agent** to score the approved HTML across quality dimensions:
   - Design System Compliance
   - AEO Schema Validity
   - Responsive Behavior
   - Content/Messaging Alignment
   - Accessibility (WCAG)
   - Editorial Consistency
2. Deploy **Curator agent** to extract learnings into the project's skillbook
3. If score < 8.0 or any dimension < 6.0, iterate

### Stage 6: Astro Decomposition
1. **Only after the HTML is approved and ACE-vetted**, decompose it into Astro components
2. Extract reusable sections into Astro components, reusing existing components where appropriate
3. Create the page in the Astro project's page directory
4. Import existing layout, navigation, and footer components
5. Add applicable AEO structured data for the organization, breadcrumbs, FAQs, and speakable content
6. Run `npx astro build` to verify
7. Check generated pages and validate their structured data using the project's available checks
8. Serve the generated build output for a final visual comparison
9. Deploy when approved

---

## Key Rules

### Content Rules
- Every page's content MUST trace to the approved page brief and business messaging
- Follow the project's editorial guidance in ALL content
- Hero copy expresses the approved primary message
- Value sections develop relevant benefits for the intended audience
- Proof points come from verified product information, customer stories, or other documented evidence

### Visual Rules
- Use ONLY design system tokens for governed visual properties, never arbitrary replacement values
- 3-column desktop → 2-column tablet → 1-column mobile
- All interactive elements get `:focus-visible` styling
- Buttons use shared primary and secondary button classes
- Use the approved logo asset with its intended proportions and colors. Never redraw it from an older version: retired logo variants are a common source of drift

### Decomposition Rules
- Shared types belong in a central type module
- No `any` types in component props
- Scoped styles for component-specific CSS only
- Global styles, including buttons and utilities, stay in the shared stylesheet
- React islands only for interactive components; use `client:visible` when viewport-triggered hydration suits the interaction

---

## Playwright Inspection Commands
```
browser_navigate: <URL of the served HTML preview>
browser_screenshot: (no args, captures current viewport)
browser_resize: { width: 1440, height: 900 }  # desktop
browser_resize: { width: 768, height: 1024 }   # tablet
browser_resize: { width: 375, height: 812 }    # mobile
```

---

## File Locations
- Fully rendered previews: a dedicated preview directory outside generated build output
- Astro pages: the project's page directory
- Components: the project's shared component directory
- Design tokens: the project's shared stylesheet or token source
- Build output: the directory generated by the Astro build

## AEO Schema Checklist (MANDATORY for every indexable page)

For every indexable page, check the following:
1. **Organization schema**: Confirm the shared layout supplies accurate organization information without duplication
2. **Breadcrumb schema**: Represent the actual navigation hierarchy, such as Home → Guides → Bicycle Chain Care
3. **Speakable schema**: Where applicable, target the page's most useful text, such as the main heading and concise introductory content
4. **FAQ schema**: Where the page contains a genuine FAQ, mark up its visible questions and answers accurately

**Exception**: Pages marked as non-indexable, such as thank-you pages, drafts, and previews, should omit additional discovery-oriented schemas beyond any organization data supplied by the shared layout.

**FAQ Content Rules**:
- Home page: business-identity questions, such as what the business offers and whom it serves
- Content pages: topic-specific questions, such as how to choose a container size in a garden-supply guide
- Contact page: process and logistics questions
- NEVER copy-paste the same FAQ across pages

**Validation**: After building, verify that structured data is valid JSON-LD with `@context`, `@type`, and the required properties for each chosen type. Confirm that it matches visible page content.

---

## MANDATORY: ACE Loop Cross-Reference

**Before ANY website page creation, modification, or maintenance work:**
1. READ the three ACE design agents shipped in this package: `05_automations/agents/design-generator.md`, `05_automations/agents/design-reflector.md`, and `05_automations/agents/design-curator.md`
2. ALL website files that are created or significantly modified MUST go through the full ACE loop (Generator → Reflector → Curator)
3. Create ACE workspaces outside the website source tree so review artifacts cannot accidentally become site content
4. Give each workspace a descriptive task name and a unique suffix
5. Satisfaction threshold: overall >= 8.0, all dimensions >= 6.0

---

## Navigation Architecture

- **Shared navigation list**: Contains content pages, such as Home, Classes, and Gallery on a ceramic studio site. Keep Contact separate when it serves as the primary navigation CTA
- **CTA Button**: "Contact the Studio" leads to the contact page and remains visible in the navigation bar
- **Footer**: Iterates the shared navigation list and adds an explicit Contact link separately
- **Rule**: In this pattern, do not duplicate Contact in the shared navigation list. Provide it through the CTA button and footer

---

## Contact Form Infrastructure

When building pages with contact forms:
- **Cloudflare Turnstile** for bot protection, using a managed widget and server-side verification
- **Resend API** for email delivery through a simple fetch without an SDK; keep the interface responsive and confirm delivery handling before reporting success
- **Pages Functions** for server-side handlers when deploying to Cloudflare Pages. A separate Worker requires its own deployment and routing configuration
- **Shared layout** provides a named head slot for per-page injection, such as the Turnstile script
- **CSP headers** must allow `challenges.cloudflare.com` in `script-src` and `frame-src`
- **Secrets** managed via `npx wrangler pages secret put NAME --project-name PROJECT`
- **Documentation** lives outside the website source tree so operational notes are not accidentally published

---

## File Locations (Reinforced)

| What | Where | NEVER put it in |
|------|-------|-----------------|
| Self-contained previews | A dedicated preview directory | Generated build output or mixed content staging |
| ACE workspaces | A separate review workspace | The website source tree |
| Documentation guides | A dedicated project documentation area | Publicly served website content |
| Pages Functions | The handler location required by Cloudflare Pages | A standalone Worker location without separate deployment configuration |

---

## Activation Keywords
"create a page", "new website page", "build a page", "website page", "landing page for website", "astro page"
