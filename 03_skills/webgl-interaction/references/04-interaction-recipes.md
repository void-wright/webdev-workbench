# Progressive interactions and browser graphics

Build the page so its content and controls remain useful when decorative rendering is unavailable. Add motion and graphics around that foundation, then verify that the enhancement preserves the same interaction model.

## Keep HTML and SVG in charge

Keep meaningful content, controls, and interaction state in HTML or SVG. Decorative rendering should subscribe to that state. A canvas can reflect which item is selected, but it should not be the only place that selection exists.

For a seed library, seed names, availability, descriptions, and links belong in the document. Decorative artwork can respond to the selected seed without becoming necessary to understand or use the catalogue.

Use native links for navigation and native buttons for actions. Give each control an accessible name, a visible focus indicator, and a sufficiently large hit area. Prevent decorative canvases from intercepting input:

```css
canvas { pointer-events: none; }
```

Keep transparent overlays focusable and visibly focused. Making an entire control transparent with `opacity: 0` also hides its focus indicator. Use a transparent background instead:

```css
button { background: transparent; }
button:focus-visible { outline: 2px solid currentColor; }
```

Check the outline against every background the control can occupy. Choose named colour tokens by their role, such as text, surface, focus, and selection, and verify their contrast over the actual artwork.

Apply hover, focus, and selection styles to the shared HTML or SVG layer. Do not restrict them to a fallback that disappears when enhancement starts.

## Make interaction understandable across inputs

Give preview and selection distinct, consistent meanings:

- Hover and keyboard focus preview the same content.
- Activation commits a selection.
- Selection is exposed through the appropriate semantics, such as `aria-pressed` for a toggle button or `aria-selected` within a compatible selection widget.
- Escape or a clearly labelled reset control restores the default state when the interaction supports clearing.

Keep essential explanations in document flow. The default view should explain what the interaction does before anyone touches it. Tooltips may supplement this explanation, but should not contain the only instructions.

Reserve space for changing readouts so previews and selections do not move surrounding content. Allow that space to grow when text wraps or users enlarge text.

Enable pointer-hover enhancements only where hover and a fine pointer are available:

```css
@media (hover: hover) and (pointer: fine) { /* Enable pointer-hover enhancements. */ }
```

Use the equivalent capability check for JavaScript hover behavior. Touch users should be able to tap controls normally. Preserve page scrolling outside deliberate captured drags.

Announce meaningful focus-driven changes and committed selections when native semantics do not already communicate them. Do not update a live region for every hover preview. Test with a screen reader while moving the pointer to catch announcement floods.

Keep transient pointer positions, hover previews, and decorative impulses in page memory. Persist them only when remembering them serves a user need.

## Preserve truthful feedback and normal actions

Never delay navigation or submission to finish an animation. A link should retain normal browser behavior without JavaScript, and navigation should be free to interrupt decoration.

Separate an operation's pending, successful, and failed states. Show successful completion only after the underlying operation confirms it. Starting a request is not confirmation that it succeeded.

Keep purely decorative effects outside the accessibility tree. Decorative elements can use `aria-hidden="true"`, but never hide a container that also contains meaningful controls or messages. Retain semantic validation and status messages independently of any animation, and avoid duplicate announcements from decorative feedback.

## Choose a rendering layer that can disappear

Start with CSS or SVG when they can provide the required behavior. Use Canvas or WebGL when the effect requires their capabilities.

Keep static artwork visible if the enhancement cannot start. When reduced motion is requested, disable decorative motion, including pointer forces and simulated depth. The decorative GPU layer should not start in that mode. If the preference changes while the page is open, stop the enhancement and restore the static presentation.

Choose imagery from the site's subject. Possible directions include typography, diagrams, textures, illustrations, photography, or abstract forms. Treat these as options, not a required visual vocabulary.

Put detailed static artwork outside the per-frame simulation. Animate only the parts that need movement, starting with a modest moving population.

Before adapting graphics code, inspect:

- The installed source to confirm that the helper exists.
- Its renderer, backend, and runtime requirements.
- Its licence and any required notices.

If you need a helper, use a small WebGL helper of your own with a clearly defined interface; none ships with this package. If a wrapper component holds the graphics and their fallback, give it a descriptive name (for example `LayeredArt`).

## Make motion depend on elapsed time

Use elapsed time in seconds rather than assuming a fixed frame rate.

For smooth movement toward a target, choose a positive time constant `tau`:

```js
const weight = 1 - Math.exp(-dt / tau);
position += (target - position) * weight;
```

A smaller `tau` follows the target more closely. This first-order smoothing approaches a fixed target without overshooting.

Convert a decay factor defined at a reference frame rate into an elapsed-time factor:

```js
const decay = Math.pow(referenceDecay, referenceFps * dt);
```

Apply `decay` to the quantity being attenuated. For ordinary decay, `referenceDecay` lies between zero and one.

### Use a spring for overshoot

When motion should pass its target and settle back, use a damped second-order spring:

```js
velocity += (omega * omega * (target - position) - 2 * dampingRatio * omega * velocity) * step;
position += velocity * step;
```

Here, `omega` controls the spring's response rate, `dampingRatio` controls damping, and `step` is the simulation interval in seconds. An underdamped spring can overshoot; exponential smoothing cannot provide that behavior on its own.

Run this integration with bounded fixed simulation steps. Limit catch-up work after a long pause and choose parameters conservatively. This numerical update can become unstable with an overly large step or a stiff spring, so inspect behavior during frame gaps as well as normal playback.

### Scale forces to the scene

Define pointer distances and forces in the scene's coordinate system. Constants suitable for pixels may be inappropriate for normalized coordinates or world-space units.

Handle zero distance explicitly before normalizing a direction vector. At the interaction center, use a defined result such as zero force instead of dividing by zero. Check the force at the center, near its boundary, and across the full scene scale.

Use hysteresis when proximity effects flicker near a threshold. For example, activate inside one radius and deactivate only outside a larger radius. Debouncing can help with noisy changes, but adds delay. Test both slow boundary movement and fast pointer sweeps.

## Keep visuals and targets aligned

A moving object should not drift away from the place where users can select it.

Prefer stationary interactive objects with decorative motion around them. Otherwise, constrain displacement to the target's coverage. If hit-testing follows live positions, calculate those positions using the same time, inputs, coordinate transforms, and mathematics as the renderer.

Account for maximum displacement when sizing graphics. Extend rendering coverage beyond the visible panel where necessary, and inspect every edge at the greatest expected movement. Check primitive bounds as well as viewport boundaries to catch clipping and visible popping.

## Choose custom picking deliberately

Native HTML and SVG targets provide browser hit-testing and keyboard access. Use custom picking only when those targets cannot adequately represent the scene, and retain an accessible control model alongside it.

| Technique | Useful when | What to verify |
| --- | --- | --- |
| Direct CPU distance tests | The selectable population is small | Coordinate conversion, displacement, and the full input-to-feedback path |
| CPU spatial index | Local candidate counts remain manageable | Dense clusters, index updates, and worst-case occupancy |
| GPU ID picking | Selection needs to follow complex rendered geometry | Readback behavior, delayed results, and stale responses |

A spatial index does not guarantee low cost when many objects occupy the same region. Test densely clustered cases, not just evenly distributed scenes.

Avoid synchronous GPU pixel readback during continuous hover handling. It can stall the rendering pipeline, and its cost depends on the device and workload. Asynchronous picking can return later, so discard stale results and decide whether that delay is acceptable for the interaction.

Measure the complete picking path on target devices, including candidate lookup or rendering, result transfer, state updates, and visible feedback. Do not assume a fixed readback duration.

Before storing pointer history or other interaction data on the GPU, check the applicable uniform limits and supported texture formats. Verify any filtering or render-target capabilities the storage design requires.

## Use flow mathematics that fits the scene

For two-dimensional flow, a scalar potential `ψ` can define a curl-like velocity field:

```text
v = (∂ψ/∂y, -∂ψ/∂x)
```

For three-dimensional flow, use the curl of a vector potential:

```text
v = ∇ × A
```

Do not repeat one scalar field across all components of the vector potential without examining the resulting constraints. That construction can impose unintended preferred directions.

Choose finite-difference spacing relative to the scene's coordinate scale. Very small spacing can amplify numerical error; overly large spacing can erase useful variation.

A continuously divergence-free field does not guarantee that numerically simulated particles remain free of clumps. Inspect actual trajectories for clustering and constrained movement, especially after repeated integration steps.

### Make exact loops from rest positions

For an exactly repeating procedural displacement, evaluate the field from fixed rest positions rather than accumulating velocity:

```text
θ = 2πt / period
q = (cos θ, sin θ)
position(t) = restPosition + amplitude × field(restPosition, q)
```

Use circular time coordinates as parameters to the field. When evaluating spatial derivatives, hold those time parameters fixed.

This construction repeats because the field receives the same inputs at each period boundary. Advection through a periodic velocity field does not provide the same guarantee: particles may finish a cycle somewhere else.

Compare simpler motion fields and lower-resolution simulations against the required appearance. Inspect visual quality and measure actual computational cost. A reduced setting alone does not demonstrate an improvement.

## Verify the complete experience

Check the shared interaction layer as carefully as the graphics:

- Disable JavaScript and WebGL separately. Useful content and working links must remain.
- Test keyboard navigation, accessible names, visible focus, hit areas, selection semantics, and reset behavior.
- Verify hover, focus, and selected styles with enhancement enabled and disabled.
- Test touch input and ordinary page scrolling.
- Confirm that essential explanations remain visible and changing readouts do not shift surrounding content.
- Enable reduced motion and verify that the static presentation remains visible without starting decorative GPU rendering.
- Test pending, successful, failed, and invalid operations. Success feedback must follow confirmation.
- Inspect target alignment, zero-distance forces, clipping, dense picking cases, threshold flicker, and motion after frame gaps.

The enhancement is ready when it adds visual response while preserving useful content, clear controls, and dependable actions.
