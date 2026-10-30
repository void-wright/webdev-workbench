# Accessible, restrained web animation

Animation should clarify an interaction, explain a relationship, or establish a deliberate point of emphasis. Build a finished static page first, then add motion where it improves the experience.

## Preserve structure and access

Keep titles, navigation, labels, and controls in semantic HTML. Canvas can supplement the document, but it cannot replace its structure.

Pair interactive graphics with named DOM controls. Anything available through hovering, dragging, or selecting a graphical element must also be available through keyboard-accessible controls and readable text. Make keyboard focus visible and keep labels meaningful outside the graphic.

Treat relationship graphics used for navigation as information interfaces. Readers must be able to identify each destination, trace its connections, and understand what those connections mean. Evaluate link readability and accessibility separately from decorative appearance.

For a regional bakery chain, an interactive location graphic could sit beside an HTML list of branches. Selecting a branch through either interface should expose the same information.

## Design the static experience first

Provide a complete static composition for reduced motion, disabled JavaScript, unavailable WebGL, and the static quality tier. Preserve content, navigation, and access to information in every case.

Include the fallback in the initial document. Keep it visible while the renderer starts, and hide it only after the first successful rendered frame. Successful context creation alone is insufficient.

If the WebGL context is lost:

- Stop animation work.
- Restore the static composition immediately.
- Rebuild rendering resources if recovery is supported.
- Hide the fallback again only after rendering succeeds.

Test startup and failure transitions for empty areas, flashes, layout shifts, and lost controls. Honor changes to reduced-motion preferences while the page is open.

If a component wraps the canvas and its fallback, give it a descriptive name (for example `LayeredArt`). Keep meaningful HTML content available independently of renderer initialization.

## Choose the smallest suitable rendering approach

Choose technology according to what must change and whether the user influences it live.

| Requirement | Suitable starting point |
|---|---|
| Static composition | HTML, CSS, SVG, or an image |
| Simple interface transitions | CSS or browser animation APIs |
| Predetermined visual sequence | Rendered media with a static poster |
| Live graphical interaction | Canvas or WebGL, when justified |

Bake detailed, unchanged imagery into a static asset. Animate only the elements that need to respond or move. If WebGL is appropriate, use your own small WebGL helper where that is sufficient.

Choose motifs from the site's subject. Possible directions include photography, illustration, material textures, typography, geometric forms, or diagrams. Treat these as options, not a required visual vocabulary.

Give each animated region a purpose. Avoid several regions competing for attention at once, and keep navigation and primary actions visually dominant.

## Prove the loop before implementing it

Define a loop duration and express each repeating behavior relative to it. Check the combined cycle, not just each motion in isolation.

If two motions repeat every four and six seconds, their combined state repeats every twelve seconds. More generally, periods with rational ratios have a finite common repeat period. Periods with irrational ratios do not have an exact finite common repeat period.

A loop boundary must match every visible property, including:

- Position, orientation, size, and opacity.
- Color, lighting, texture phase, and noise phase.
- Trails, accumulated buffers, and particle lifecycle state.

Matching positions alone may still produce a visible jerk. Match velocity at the boundary when smooth motion requires it, and consider acceleration for more sensitive transitions.

### Use symmetry carefully

Rotational symmetry can shorten the visible cycle. An evenly spaced arrangement of identical elements may look unchanged after rotating through one element's spacing.

That equivalence holds only if the repeated elements are visually indistinguishable. Different colors, labels, sizes, trails, or lifecycle phases can reveal the permutation and restore the longer cycle.

Verify the complete visible state at the proposed shorter boundary.

### Prefer analytic motion for repeatability

When exact endpoints matter, evaluate positions directly from time or normalized progress. This avoids accumulated integration drift.

For assigned start and destination positions, use interpolation:

```text
mix(from, to, progress)
```

The scalar equivalent is:

```text
start + change * progress
```

With progress equal to zero or one, these expressions reach their respective endpoints. Easing can shape the journey, but must retain those endpoint values if arrival must remain exact.

A journey from one position to another is not automatically a loop. Design the return journey or reset transition explicitly.

### Check stateful resets separately

Simulation can be appropriate when its behavior matters, but integration does not guarantee an exact loop. Particle respawning, trail history, random state, and accumulated buffers can all introduce discontinuities.

Inspect the reset itself and several consecutive cycles. Deterministic randomness makes behavior reproducible; it does not by itself make the boundary seamless.

Avoid simulation complexity that adds no useful visual behavior.

## Shape motion to match the interaction

Choose follower dynamics deliberately. First-order easing approaches a target and does not inherently provide overshoot or crossing. Second-order dynamics can produce those behaviors, depending on damping and other parameters.

When particles must arrive at assigned destinations, interpolation provides a direct way to guarantee endpoint positions. It does not guarantee collision-free paths. Assess intersections separately if they affect readability or meaning.

Use stagger and easing to communicate the intended transition:

- Spatially coherent delays can suggest direction or progression.
- Independent random delays can suggest dispersal, but may appear noisy.
- Overshooting easing gives arrival a different character and can temporarily carry elements beyond their destinations.

Keep the motion model as simple as the intended behavior allows.

## Control color and glow explicitly

Choose colors from the site's identity, content, and contrast requirements. Name tokens by role, such as background, surface, primary text, muted text, accent, and focus indicator. Derive graphical colors from those roles.

Document how the rendering pipeline handles input color spaces, blending, and output conversion. Check texture interpretation, alpha conventions, and any tone mapping. Compare the live rendering with the static reference rather than assuming matching source values will look identical.

Use additive glow sparingly. Broad translucent effects can overwhelm text and controls while increasing overdraw. Limit their coverage and overlap, then compare visual emphasis between static and animated versions.

## Measure the finished composition

Geometry counts alone do not describe rendering cost. Fragment coverage, stroke width, line length, transparency, overlap, and drawing-buffer resolution can dominate a small scene.

Measure the completed composition on desktop and representative mobile hardware. CPU throttling does not reproduce a mobile GPU. Record the device, viewport, resolution, quality tier, and interaction being measured so results are interpretable.

Update continuous animation parameters directly through renderer state, uniforms, or mutable references. Avoid forcing framework renders on every animation frame. Keep meaningful application state and accessible controls synchronized through normal application mechanisms.

Offer quality tiers with explicit differences, such as resolution, particle count, effect coverage, and update frequency. Include a usable static tier. Pause unnecessary animation when its region is offscreen or the document is hidden.

### Estimate buffer payload honestly

Calculate attribute payload as:

```text
element count × sum(attribute components × bytes per component)
```

For example, 10,000 elements with three position components and four color components, all stored as four-byte values, require 280,000 bytes of attribute payload.

This is not total renderer memory. Account separately for index buffers, padding, duplicate CPU or GPU copies, textures, framebuffers, and other allocations. State which items the estimate excludes.

## Prepare data and evaluate alternatives

Generate public visualization data through read-only extraction so the source remains unchanged. Before committing the export, validate its schema, identifiers, relationships, and expected coverage. Scan for secrets, personal information, internal fields, and material unsuitable for publication.

Compare alternative implementations using the same brief, assets, content, and test conditions. Conceal authorship during evaluation. Assess visual preference, rendering performance, bundle size, accessibility, fallback behavior, and fidelity separately so one attractive result does not obscure a failure elsewhere.

A publicly viewable example does not grant reuse permission. Check code and asset licenses independently, follow applicable obligations, and preserve required notices. Verify claims about an implementation before repeating them.

## Final verification

- Navigate with a keyboard and access all information exposed by pointer interactions.
- Test reduced motion, disabled JavaScript, unavailable WebGL, and the static tier.
- Inspect startup and simulate context loss.
- Check loop boundaries, return transitions, trails, and resets.
- Verify destination positions and assess path collisions where relevant.
- Compare live color and visual emphasis with the static composition.
- Measure the finished rendering on representative desktop and mobile devices.
- Validate exported data and confirm reuse permissions.
