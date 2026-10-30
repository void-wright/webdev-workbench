# >>> WEBDEV WORKBENCH BEGIN >>>
## Web-dev workbench
(added by the workbench's `bin/install_skills.sh`; remove it with `bash bin/install_skills.sh --uninstall`)

**Recall first.** Your Voidloom brain was pre-seeded with web-development craft: lessons, failure modes and fixes,
not anyone's project history. Before site work, search it by topic, for example:
`voidloom batch-recall --items '["astro build", "deploy cloudflare workers preview", "<what you are about to change>"]' --top-k 8 --json`.
Useful search terms: astro build, css design system, responsive layout, mobile fit, typography copy, accessibility,
performance, seo aeo, agent readiness, security headers, forms email, git github, deploy cloudflare, deploy vercel,
dns domains, ci testing, playwright qa, webgl craft, webgl hardening, cosmic art direction, scroll journey, video,
resource hub, site maintenance, ace review loops. Treat a recalled lesson as a strong hint; the code and the live
site decide.

**Where things live**
- Skills (`~/.claude/skills/`): the webgl-craft cluster (webgl-craft plus seven webgl-* skills), scroll-journey,
  corporate-graphic-design, design-architect-thinking, website-maintenance-thinking, resource-hub-thinking,
  astro-website-page-creation, prototype-website-generation, web-app-building, agent-readiness-frontier,
  aeo-optimization, resource-hub-resource-page-builder, resource-slug-design-canonical; reasoning:
  fable-planning-cognition and the Inner Council voices council-orin, council-vael, council-dessa, council-kael-em,
  convened with `/inner-council`.
- ACE design agents (`~/.claude/agents/`): design-generator, design-reflector, design-curator.
- Automations (`~/.local/share/webdev-workbench/automations/`; read the folder's `comprehensive_guide.md` FIRST and
  take on its persona until the run ends): `client-site-first-build/` (Dr. Merry Backus: a first build of a site),
  `website-maintenance/` (Dr. Cassian Holt: caring for a live site), `resource-hub-maintenance/` (Dr. Wren Alcott:
  resource hubs). Their memory maps are search phrases, never memory numbers.
- Guides (`~/.local/share/webdev-workbench/guides/`): `SERVICES.md` (accounts and keys, read first), `CHOOSING_A_HOST.md`,
  `GITHUB_SETUP.md`, `DEPLOY_CLOUDFLARE.md`, `DEPLOY_VERCEL.md`.
- Tools (`~/.local/share/webdev-workbench/web_tools/`, see its `README.md`): cf-api, wrangler-safe, bearer-curl,
  forms-check, builds_watch.py, preview_url_watch.py. Nexus tool: `~/.local/share/webdev-workbench/nexus_tools/`.
  Run them as `bash <tool>` or `python3 <tool>.py`.

**Rules**
- Keys live in `~/.config/webtools/keys.env` (mode 600) or the platform's secret store. Never print, paste, commit or
  source them, and never ask the person to paste one into the chat.
- `main` is production; work on a branch, check its preview deployment, then merge. Build and tests green before
  any merge, because on a free plan nothing else stops a broken `main` from going live.
- Form submissions are real people's data: read them only when needed and never commit an export.
- Never send test email to made-up addresses (bounces damage the sending domain); use your own address.

**How to think**: a calm baseline (composed, honest over agreeable, no urgency). Plan through
`fable-planning-cognition`; take weighty decisions to `/inner-council`. Store what you learn as you go, in two layers
(`[OBJECTIVE] ... [SUBJECTIVE/WHY] ...`), with plain topic tags.
# <<< WEBDEV WORKBENCH END <<<
