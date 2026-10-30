# Changelog

All notable changes to Voidwright's webdev workbench are recorded here. Versions follow
[Semantic Versioning](https://semver.org): a **major** version changes how you install or what the
automation harnesses expect; a **minor** version adds skills, harness abilities or pack memories; a
**patch** fixes something without changing how you use it. Each release is a git tag (`vX.Y.Z`) with a
GitHub release, and `VERSION` holds the current number.

## Unreleased

- **Removed** the `webgl-constellations` and `webgl-cosmic-art-direction` skills. Both were written
  for one particular site's look rather than for web work in general. The WebGL craft cluster is now
  a router plus five skills, and the package carries 18 skills (the README's prose, tables and
  diagram all say 18).
- **Fixed** the README's sequence diagram, which failed to render on GitHub (a semicolon in a note
  ended the statement early).
- **Changed** the README and START HERE to name the tool generically: the workbench runs through any AI coding
  agent (Claude Code, Codex, Antigravity, Kimi Code, or a local model through a tool such as Ollama), and you can
  start the agent in the package folder or point it at the folder.

## 1.0.0 (2026-10-30)

The first public release.

- **Memory pack:** 1,666 web-craft memories in 34 clusters for a Voidloom brain, with a 276-phrase
  recall battery.
- **Skills (20):** the WebGL craft cluster (a router and seven skills), scroll journeys, Astro page
  creation, web-app building, prototype sites, answer-engine optimization, agent readiness, resource
  libraries, slug design, corporate graphic design, and three reasoning layers for the harnesses.
- **Automation harnesses (3):** first build of a site or resource hub, website maintenance, and
  resource-hub maintenance, each with a guide, a skillbook, a memory map and a review loop at a hard
  9.8 out of 10.
- **Reasoning aids:** the Inner Council (`/inner-council`) and the planning-cognition skill.
- **Tools and guides:** Cloudflare and preview web tools, nexus tools for the brain, and assume-nothing
  guides for GitHub, Cloudflare, Vercel, choosing a host, and services and keys.
- **Voidloom** is cloned at setup from https://github.com/void-wright/voidloom at a pinned commit.
