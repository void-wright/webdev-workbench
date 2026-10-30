<!-- Licence ledger for evaluating third-party WebGL code and assets.
     Treat the entries as starting points. Check the licence and notices for the exact version and files before reuse.
     Keep attribution and licence records with the project. -->

## 10. Licence ledger

Rule: learn techniques; never copy code without permission. When adapting MIT or similarly licensed code, retain the required copyright and licence notices and record its source.

### 10.1 May be adapted (with attribution or notice)

| Source | Licence to confirm before reuse | What may be taken |
|---|---|---|
| PavelDoGreat/WebGL-Fluid-Simulation | MIT | `Program`/`Material`/`blit` pattern, 4×4 format probe, soft-knee bloom, dissipation, splat Gaussian, `alpha=max(rgb)`, dither use |
| Christoph Peters' blue-noise textures | CC0 1.0 | Textures covered by the dedication; credit is still helpful |
| OGL | Unlicense | Code covered by the licence; credit is still helpful |
| basementstudio/shader-lab | Apache-2.0 | Curl/simplex maths, subject to applicable licence, modification and NOTICE requirements |
| twgl.js, PicoGL.js, regl | MIT | Patterns or the libraries, with required notices |
| three.js (including `Line2`) | MIT | Patterns or the library, if it fits the project's bundle budget |
| MeshLine variants (spite, pmndrs, Makio64) | MIT; check each repository separately | Patterns or implementations, accounting for their three.js dependency |
| bryc PRNGs | Public-domain dedication with MIT fallback; confirm the source text rather than relying on GitHub's licence classification | SplitMix32 |
| webgl2fundamentals | BSD-3-Clause | Picking patterns, with required notices |
| `@usephase/core` (Vercel Phase) | Confirm that package metadata and repository licence terms agree | Ideas only until reuse permission is confirmed |

### 10.2 Learn only (read, never copy code or assets)

For this workbench's default reuse policy, study the following sources for techniques. Copy only after separately confirming permission and compatibility with the intended distribution.

| Source | Why |
|---|---|
| mrdoob "Or so they say" (xplsv), Harmony | GPL-3.0 requires a separate compatibility review |
| mrdoob Clouds, Sporel | No reuse licence established here |
| AlteredQualia XG pieces | Proprietary minified engine |
| shone.dev thick lines; greggman picking gist | No reuse licence established here |
| Three.js Roadmap noise guide | An all-rights-reserved notice does not grant reuse permission |
| henrywithu.com (`dither8Bit`) | CC BY-NC-SA 4.0 includes a non-commercial restriction |
| Red Blob Games (mapgen4) | Confirm explicit reuse terms; a copyright notice alone is not permission |
| Gargantua; wonjyou/morphing-particle-swarm | No reuse licence established here |
| Codrops articles; 21st.dev | Check the exact article, component or repository; platform availability alone is not permission |
| Commercial showcase sites without linked source licences | Publicly visible code and assets do not establish permission to reuse them |

### 10.3 Off-limits

- Pasting GPL code into a site without reviewing and satisfying the applicable copyleft obligations.
- Using CC BY-NC-SA text or code on a commercial site without separate permission.
- Copying code or assets from an unlicensed repository or commercial site without permission.
- Loading libraries or textures from a third-party CDN when the project's CSP and cross-origin requirements prohibit it. Bundle permitted dependencies locally.
- Shipping a handoff's unused heavy assets. Remove unused media so it does not inflate the delivered package.
- Carrying demo-only extras such as dat.gui, analytics or promotional elements into production without a deliberate need and review.

---
