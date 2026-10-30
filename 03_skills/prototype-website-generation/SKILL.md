---
name: prototype-website-generation
description: Spin up a private preview prototype of a website from a template with placeholders, then deploy it to a preview host. Use when a quick site prototype is needed.
---

# Prototype Website Generation Skill

## Purpose

Generate a private preview of a website idea on a subdomain of a domain you own, so you can judge content, design and interactions before you change your real site. This is a one-person workflow: you build the preview, you look at it, you keep it or tear it down. For example, the owner of an invented ceramic studio might preview a new class-booking page at `preview.example.com` before touching the live site.

## Activation Keywords

"prototype", "business prototype", "subdomain", "prototype website", "spin up a site", "demo site"

## Architecture

### Template Source

Use an Astro site you own or an Astro starter you choose. No template ships with this package. Supply the template and destination directories together when copying, because shell variables may not persist between tool calls.

```bash
read -r -p "Astro template directory: " TEMPLATE_DIR
read -r -p "New prototype directory: " PROTOTYPE_DIR
```

### Prototype Destination Pattern

Keep each prototype in a separate project directory. Use a descriptive project name, such as `bicycle-guide-preview`, and keep its setup notes alongside the site source.

### Infrastructure (one possible setup)

A preview needs very little. The setup below is one reasonable way to do it on Cloudflare; adapt it to the host you already use.

| What | Why you need it | Notes |
|------|-----------------|-------|
| A hosting project for the preview | Somewhere to deploy the built site | One small Cloudflare Pages project is enough. If you run several previews at once, give each its own project so tearing one down cannot break another. |
| A DNS record for the preview hostname | So `preview.example.com` reaches that project | Point it at the hostname your host assigns. |
| An API token (optional) | Only if you deploy from the command line | Scope it to the resources the preview uses. Keep it in your own key file (`~/.config/<tool>/keys.env`, mode 600) or the platform's secret store, never in the repo or chat. |
| Bot protection for the form (optional) | Only if the preview has a public form | For example a Cloudflare Turnstile widget with its own site key and secret key. |
| A place for media (optional) | Only if the preview needs large images or video | Files in the site's own `public/` folder are usually enough. Use object storage behind a hostname such as `assets.example.com` only if you already have it. |
| Analytics (optional) | Rarely worth it for a private preview | Skip unless you are testing the analytics itself. |

### Contact Form Behavior (IMPORTANT)

**Preview contact forms do NOT send emails.** The form validates input, verifies bot protection, logs a submission event without personal data, and returns success. No email-provider call is made. This means:

- No email-provider API key is needed.
- No `CONTACT_FROM` or `CONTACT_TO` variables are needed in the deployment configuration.
- The form interaction works, including validation, bot protection, and the success redirect.
- The form and confirmation text clearly explain that this is a demo and no message is delivered.
- Email delivery is configured when you build the real page on your production site.

---

## MANDATORY: ACE Loop for Every Prototype

**NEVER skip the ACE loop.** Every prototype MUST use Generator → Reviewer → Curator.

### ACE Workspace

Keep generation, review, and curation notes together in the prototype's working directory. Separate them from deployable site content.

### ACE Agents

- **Generator**: Copies the template, customizes all configuration points in the checklist below, and replaces content with `REPLACE_WITH_*` placeholders.
- **Reviewer**: Validates every customization point, checks for stale template branding, confirms placeholders are clearly marked, checks CORS and Turnstile settings, verifies email delivery is disabled, and confirms the build succeeds.
- **Curator**: Extracts reusable lessons and updates this skill if gaps are found.

### Satisfaction Threshold

- Overall score >= 8, all dimensions >= 6.
- Maximum review cycles per attempt: 3. If the threshold remains unmet, record the blockers and revise the plan before continuing.

---

## MANDATORY: Platform Setup Guide for Every Prototype

**NEVER skip the guide.** Every prototype gets its own setup guide alongside the project.

The guide covers all infrastructure steps from project creation to teardown, assuming zero prior knowledge. Use the Platform Setup Guide Template below.

---

## Copy Command

When copying the template, EXCLUDE build artifacts, repository history, and local secrets. Supply both directories in the same shell call:

```bash
read -r -p "Astro template directory: " TEMPLATE_DIR
read -r -p "New prototype directory: " PROTOTYPE_DIR

rsync -av --exclude='node_modules' --exclude='dist' --exclude='.astro' \
  --exclude='.env*' --exclude='.git' --exclude='.dev.vars*' \
  "${TEMPLATE_DIR:?}/" "${PROTOTYPE_DIR:?}/"
```

Review the source for any other secret-bearing files before copying.

---

## Complete Customization Checklist

Every item below MUST be addressed. The Generator checks them off; the Reviewer verifies them. Locate the equivalent configuration and components in your chosen template.

### 1. Site Configuration: Brand Identity

```typescript
export const SITE = {
  name: 'REPLACE_WITH_BUSINESS_NAME',
  tagline: 'REPLACE_WITH_BUSINESS_TAGLINE',
  url: 'https://preview.example.com',
  mediaUrl: 'https://assets.example.com',
  description: 'REPLACE_WITH_BUSINESS_DESCRIPTION',
  author: 'REPLACE_WITH_BUSINESS_NAME',
  locale: 'en-US',
  themeColor: 'REPLACE_WITH_BUSINESS_PRIMARY_COLOR',
} as const;

export const NAV_LINKS = [
  { label: 'Home', href: '/' },
] as const;

export const SOCIAL = {
  linkedin: '',
  twitter: '',
} as const;
```

**Changes**: name, tagline, url, mediaUrl, description, author, themeColor. Remove template-only pages from `NAV_LINKS`. Confirm that remaining links resolve.

### 2. Deployment Configuration: Cloudflare Config

The following is a configuration template. Replace the compatibility-date placeholder with a valid date supported by the runtime and tested with your project.

```toml
name = "resource-preview"
compatibility_date = "REPLACE_WITH_COMPATIBILITY_DATE"
pages_build_output_dir = "dist"

[vars]
SITE_URL = "https://preview.example.com"
R2_PUBLIC_URL = "https://assets.example.com"
ENVIRONMENT = "preview"
BRAND_COLOR = "REPLACE_WITH_BUSINESS_PRIMARY_COLOR"

[env.dev.vars]
SITE_URL = "http://localhost:4321"
ENVIRONMENT = "development"
```

**Changes**: project name, compatibility date, `SITE_URL`, and `BRAND_COLOR`. Keep `R2_PUBLIC_URL` only if you serve media from object storage; otherwise delete it, along with any bucket binding. Remove email variables and unused KV namespace comments.

### 3. Package Metadata: Project Identity

**Changes**:

- `"name"`: `"resource-preview"`
- `"description"`: `"Prototype resource library for an independent business"`

Choose a package name that distinguishes this prototype from other projects.

### 4. Design Tokens: Color System

**Changes**: Set CSS custom properties to the business's chosen colors. Introduce the primary color through a neutral token rather than a token named after the template's branding:

- `--color-primary`: primary color, initially marked `REPLACE_WITH_BUSINESS_PRIMARY_COLOR`.
- `--color-primary-700`: darker variant.
- `--color-primary-100`: lighter variant.

Resolve color placeholders before visual review and verify contrast in the actual foreground and background combinations.

Replace the template's logo with the business's logo or an explicit placeholder. If the business has a logomark, wire it explicitly. An inline SVG using `currentColor` can inherit its color from CSS. Never leave the template's mark as a stand-in.

### 5. Contact Form: Turnstile Site Key

**Changes**: Replace the template's Turnstile site key with a placeholder:

```html
data-sitekey="REPLACE_WITH_TURNSTILE_SITE_KEY"
```

### 6. Content Pages: Strip to Placeholders

All page content must be replaced with clearly marked placeholders:

| Page | Action |
|------|--------|
| Home page | Replace hero text, value propositions, and FAQ items with `REPLACE_WITH_*` |
| Template-only pages, such as an unrelated customer story | **Remove entirely** or replace with a minimal placeholder page |
| Contact page | Keep the form structure and replace headings and copy with `REPLACE_WITH_*`; retain the demo notice |
| Contact confirmation page | Replace brand references with `REPLACE_WITH_*` and state that no message was delivered |

### 7. Crawler Configuration: Subdomain URL

Update any sitemap declaration to use the preview hostname and the sitemap route actually generated by the build. For example:

```text
Sitemap: https://preview.example.com/sitemap-index.xml
```

A sitemap declaration does not prevent indexing. Apply the intended preview indexing policy separately.

### 8. Response Headers: CSP Policy

Update `Access-Control-Allow-Origin` if present. Ensure the Content Security Policy allows the Turnstile resources required by the form.

### 9. Astro Configuration: Site URL

```javascript
site: 'https://preview.example.com',
```

### 10. Static Assets

- Replace the favicon with the business's favicon or an explicit placeholder.
- Replace the social-sharing image with the business's image or an explicit placeholder.
- Remove static assets specific to the template's original branding.

### 11. AEO Schema / JSON-LD

Update all `<script type="application/ld+json">` blocks in page files:

- Organization name → `REPLACE_WITH_BUSINESS_NAME`.
- URL → `https://preview.example.com`.
- Logo → the business's logo URL or an explicit placeholder.

Resolve placeholders before enabling indexing or publishing production content.

### 12. Environment Variable Documentation

Create an example environment-variable document containing names and placeholders only:

```dotenv
# Cloudflare Pages secret, set using wrangler pages secret put
TURNSTILE_SECRET_KEY=REPLACE_WITH_TURNSTILE_SECRET_KEY
```

Document public configuration separately from secrets. Prototype forms do not need an email-provider key.

---

## Placeholder Convention

All business-specific placeholder values follow this pattern:

```text
REPLACE_WITH_BUSINESS_{FIELD}
```

Examples:

- `REPLACE_WITH_BUSINESS_TAGLINE`
- `REPLACE_WITH_BUSINESS_DESCRIPTION`
- `REPLACE_WITH_BUSINESS_PRIMARY_COLOR`
- `REPLACE_WITH_TURNSTILE_SITE_KEY`

Use a repository search to find everything that still needs filling in:

```bash
rg -n "REPLACE_WITH_" .
```

---

## Reviewer Validation Checklist

The Reviewer agent MUST verify:

1. **No stale references**: Search the source for the template's original name and branding. Resolve every match; retain only necessary technical references.
2. **No hardcoded template colors**: Search content and configuration for current and retired template colors. Remove unintended matches. Old values can linger in components after a redesign; intentional business color tokens are acceptable.
3. **All placeholders present**: Search for `REPLACE_WITH_` and compare the results with the expected field inventory.
4. **CORS correct**: The contact handler reads `SITE_URL` from the environment rather than a hardcoded origin.
5. **Wrangler correct**: Project name and `SITE_URL` are updated, email variables are absent, and the form cannot send email.
6. **Build succeeds**: `npm install && npm run build` completes without errors.
7. **No copied dependencies**: The copy excluded `node_modules`. Dependencies created by the install step are expected.
8. **Template-only pages handled**: Each is either removed or replaced with a placeholder.

---

## Platform Setup Guide Template

Every prototype gets a guide alongside its project covering:

1. **Cloudflare Pages**: Create a project using `npx wrangler pages project create resource-preview`, or use Dashboard Direct Upload with placeholder content.
2. **Cloudflare DNS**: Document the CNAME from the preview hostname to the assigned Pages hostname. Coordinate this with the custom-domain setup and verify the proxy setting.
3. **Cloudflare Pages Custom Domain**: Attach `preview.example.com` and complete the displayed DNS instructions.
4. **Cloudflare Turnstile**: Create a widget for `preview.example.com`.
5. **Set Secrets**: Use `npx wrangler pages secret put TURNSTILE_SECRET_KEY --project-name resource-preview`. No email-provider secret is needed because previews do not send emails.
6. **Update Turnstile Site Key**: Replace the placeholder in the contact form.
7. **Install & Build**: Run `npm install && npm run build`.
8. **Deploy**: Run `npx wrangler pages deploy dist/ --project-name resource-preview`.
9. **Verify**: Confirm the page loads, Turnstile works, and the form validates input and displays a clearly labeled demo confirmation.
10. **GA4 (Optional)**: Create a property, add the tracking snippet, and update CSP and consent behavior as needed.
11. **Teardown**: Delete the Pages project, DNS record, and Turnstile widget; archive or delete the local project.

Replace example project names and hostnames with the values chosen for the prototype.

---

## Memory Update Requirements

**MANDATORY at every phase:**

| Phase | What to Store | Where |
|-------|---------------|-------|
| Template fixes | Reusable patterns, such as dynamic site names, `currentColor` SVGs, and environment-driven contact handlers | Project notes |
| Prototype creation | Project location, configuration state, and placeholder inventory | Project notes |
| Setup guide | Guide location and platform setup status | Project notes |
| Post-deployment | Live URL, secret names only, and verification status | Project notes and the prototype's guide |

Keep notes useful to whoever maintains the site later, which is usually you. Never record secret values or submitted contact details.

---

## Teardown Procedure

When a prototype period ends:

1. **Cloudflare Pages**: Delete the prototype's project.
2. **Cloudflare DNS**: Remove its preview CNAME record from your domain's zone.
3. **Cloudflare Turnstile**: Delete its widget.
4. **Local files**: Archive the project outside the active working directory or delete it.
5. **Memory**: Record the teardown date and reason in the project notes.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| Public edition | Not recorded | Generic workflow for a private preview of your own site |
