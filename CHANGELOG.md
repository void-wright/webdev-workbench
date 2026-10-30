# Changelog

All notable changes to Voidwright's webdev workbench are recorded here. Versions follow
[Semantic Versioning](https://semver.org): a **major** version changes how you install or what the
automation harnesses expect; a **minor** version adds skills, harness abilities or pack memories; a
**patch** fixes something without changing how you use it. Each release is a git tag (`vX.Y.Z`) with a
GitHub release, and `VERSION` holds the current number.

## Unreleased

Nothing yet.

## 1.0.1 (2026-10-30)

Cleanup after the first public release.

- **Removed** the `webgl-constellations` and `webgl-cosmic-art-direction` skills. Both were written
  for one particular site's look rather than for web work in general. The WebGL craft cluster is now
  a router plus five skills, and the package carries 18 skills (the README's prose, tables and
  diagram all say 18).
- **Changed** the agent wording to say exactly what is known, in a new README section, "Which agents
  it runs on": setup is written for Claude Code; Codex works (Voidloom's Codex hook, one command plus a
  trust step); Antigravity has been used as a called agent, not yet as the setup tool; Kimi Code reads
  `AGENTS.md`; other routes such as a local model through Ollama are not yet tested. You start your agent
  in the package folder, or point it at the folder.
- **Fixed** the README's sequence diagram, which failed to render on GitHub (a semicolon in a note
  ended the statement early).

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
