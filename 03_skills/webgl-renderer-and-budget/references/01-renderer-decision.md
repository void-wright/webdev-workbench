<!-- Renderer selection guidance for decorative browser graphics.
     Measure the shipped bundle and test representative devices before making performance claims.
     Status markers: VERIFIED (checked against a primary source or recomputed),
     CONTRADICTED (do not build on it), UNSETTLED (a lead),
     ESTIMATE (not measured in the target application).
     See 03_skills/webgl-craft/references/00-how-to-read.md for evidence guidance. -->

## 1. The renderer decision

### 1.1 The options, with measured sizes

Compare gzip sizes for the same application features and production build settings. A package's advertised core size, the size of all its exports and a minimal application's bundle are different measurements. Record the package version, imported modules, measurement method and included dependencies. Until measured in the target build, treat size expectations as estimates.

For example, a regional bakery chain's site might want a light layer of drifting flour motes behind its seasonal menu. That use does not automatically require a scene graph or a full 3D engine.

| Option | Size (gzip) | Status of the size claim | Licence verification | Maintenance | Fit for a decorative panel |
|---|---|---|---|---|---|
| **Raw WebGL2 + a small local helper** | Your helper, shaders and scene code; measure the production output | A helper of a few KB is an ESTIMATE until built | Your code; retain notices for borrowed code | You maintain it | **Strong default** for instanced quads, capsules and analytic particles without loaders or a post-processing chain |
| **OGL** | Measure the actual imports and application code | Advertised module sizes are not equivalent to a shipped bundle | Check the selected release's licence; do not assume MIT | Check recent releases and repository activity | **Runner-up** when mesh and camera helpers simplify the implementation |
| twgl.js | Measure the helper functions included by the build | Package-level estimates need application verification | Check the selected release and retain required notices | Check current activity | Helper-focused middle ground |
| PicoGL.js | Measure the selected release and actual imports | A small bundle alone does not establish suitability | Check the selected release and retain required notices | Check upstream commits; an aggregator's listing date is not a maintenance date | Consider only after checking maintenance and compatibility |
| regl | Measure the renderer and command definitions together | Compare equivalent scenes | Check the selected release and retain required notices | Check releases and repository statements directly | Useful if its command model materially simplifies the scene |
| three.js WebGLRenderer | Measure the selected renderer, core and imported features | Older package measurements do not establish the current build's size | Check the selected release and retain required notices | Check the selected release and supported APIs | Often difficult to justify for a small decorative layer under a tight budget |
| three.js WebGPURenderer + TSL | Measure the complete build and shader startup separately | No size or compile-time estimate transfers reliably between scenes | Check the selected release and retain required notices | Check renderer and backend support for the selected release | Consider when required features justify the additional machinery |
| Raw WebGPU | Your implementation plus any required WebGL2 fallback | Count both paths in the delivery and maintenance budget | Your code; retain notices for borrowed code | You maintain both paths | Usually unnecessary for a small decorative scene without compute requirements |
| Canvas2D | No renderer library; measure application code and assets | Frame rate depends on sprite size, compositing, pixel count and device | No additional renderer package | Browser API | A useful baseline for a moving sprite or a modest field of dots; benchmark the actual scene |

### 1.2 The capability numbers

Support percentages are dated observations about sampled browsers, not guarantees for a visitor's device. Record the source and collection date when using them for planning. At runtime, detect capabilities and test the exact operations the scene needs.

| Capability | What to check | Consequence |
|---|---|---|
| WebGL2 `EXT_color_buffer_float` | Extension availability and framebuffer completeness for the requested format | Texture allocation alone does not prove that rendering into it works |
| WebGL2 `EXT_color_buffer_half_float` | Support in the actual context and completeness of the chosen half-float target | Do not substitute a WebGL1 support table for a WebGL2 decision |
| WebGL1 `EXT_color_buffer_half_float` | Only relevant if a WebGL1 fallback is being implemented | Keep fallback capability checks separate from the WebGL2 path |
| WebGL2 `OES_texture_float_linear` | Availability when linear filtering of 32-bit float textures is required | Rendering to a float target does not imply that it supports linear filtering |
| WebGL2 `EXT_float_blend` | Availability when blending into 32-bit float targets is required | Float renderability and float blending are separate capabilities |
| WebGL2 `KHR_parallel_shader_compile` | Extension availability and program completion status | Keep a fallback startup path; parallel compilation is not universal |

Consequences:

- **Render targets**: prefer **RGBA16F** for filtered or blended effects when supported. Reserve **RGBA32F** for unfiltered, unblended state unless the required operations are explicitly supported and tested. Probe the actual format instead of building a fallback ladder from the wrong API's support table.
- **Shader compile**: use parallel compilation where available, but keep shaders small and avoid unnecessary variants. Support varies across browsers and devices.
- **Scheduling**: feature-detect `scheduler.yield` and `requestIdleCallback`. Provide a `setTimeout` or `MessageChannel` fallback for sliced startup work. Do not assume a scheduling API is universally available because some modern browsers implement it.
- **WebGPU**: distinguish full support, partial support and actual use. A fraction must be multiplied by 100 to become a percentage. Broad availability alone does not justify another rendering path.
- **WebGL2 on mobile**: distinguish texture sampling, rendering into a texture, filtering and blending. Support for an older half-float texture extension does not establish support for WebGL2 or every half-float operation.

### 1.3 Recommendation

**For a small decorative layer, start with raw WebGL2 and your own small WebGL helper (a short local module you write; no such helper ships with this package).** Include only the program, material, buffer and draw helpers the scene needs. Use a small 4×4 render-target probe to verify candidate formats, and retain attribution and licence notices for borrowed implementations. Runner-up: OGL when its abstractions reduce meaningful implementation work.

Reasons:

1. **The live layer needs no engine.** Instanced sprites, SDF capsule lines and closed-form particles can often be drawn in a few calls. A bicycle-parts guide with a subtle animated route graphic does not need model loaders or a scene graph unless the design actually uses them.
2. **Pixel work can dominate the cost.** Large translucent layers, repeated overdraw and bloom may cost more than API overhead. Compare reduced render scale, fewer overlapping layers and disabled post-processing on representative devices. Measure the result before claiming a speedup.
3. **Budget.** Count the renderer, framework runtime, helper code, shaders and scene logic against the same compressed JavaScript budget. A library that consumes most of the allowance leaves little room for the application.
4. **Startup and maintenance stay manageable.** A small implementation can reduce downloaded and parsed code while keeping one rendering path. This is a design expectation to verify, not a guarantee of lower shader compile time or better frame rate.
5. **A strict site requires deliberate asset delivery.** If the site's policy allows `script-src 'self'` plus approved hashes for inline scripts, bundle the renderer from the site's own origin. Check that loaders and other dependencies do not introduce undeclared cross-origin requests. Replacing a CDN import requires verifying the complete request chain.

Reject heavier options when their features do not justify their costs:

- **three.js or React Three Fiber with `client:only="react"`**: account for both renderer and framework costs. Use them when the scene needs their capabilities and the measured build fits the budget.
- **OffscreenCanvas + Worker as a promise of “0 ms INP”**: moving rendering off the main thread does not remove startup, event handling or DOM synchronization costs. Measure the complete interaction path before adding worker complexity.
- **A mesh-line package plus half-resolution bloom and tone mapping**: count the underlying engine and post-processing dependencies. A visually small effect can still bring a substantial bundle and render cost.

**Proposed bundle target**: ≤30 KB gzip per decorative layer, with ≤200 KB as the hard ceiling for this example budget. These are planning constraints, not measured results or universal web standards. A compact helper, shaders and scene code may fit comfortably within the target; confirm that with the production bundle.

---
