# Optional WebGL enhancements

Build a complete HTML page first. WebGL can enrich its presentation, but understanding the content, using controls, and following navigation must never depend on a working renderer.

## Keep content and interaction in HTML

Put essential text, labels, relationships, and navigation in ordinary HTML. Accessible alternatives must be present in the page, not confined to `noscript`. For a neighbourhood climbing gym, an illustrated route map could accompany an HTML list of routes with difficulty and location.

Use semantic buttons for enhancement controls. Expose toggle state with `aria-pressed`, and use `aria-live` for meaningful updates that would otherwise be conveyed only visually. Avoid announcing information already communicated by a focus change.

Keep input handling separate from decorative rendering. A purely decorative canvas should have `aria-hidden="true"` and should not receive pointer events:

```css
.demo-canvas {
  pointer-events: none;
}
```

Attach any intentional interaction to appropriate HTML controls or a separate interaction surface. Preserve native scrolling through the enhanced region. For an area that supports horizontal gestures while retaining vertical page scrolling, use:

```css
.demo-interaction {
  touch-action: pan-y;
}
```

Capture a pointer only after deliberate interaction. Handle `pointercancel` and lost pointer capture by clearing drag state and releasing any interaction that could remain stuck. Test touch scrolling directly through the artwork.

## Make the static presentation complete

Use a stable layer order:

1. Static artwork at the bottom.
2. An initially transparent canvas above it.
3. HTML content and controls above both.

If the layers live in a wrapper component, give it a descriptive name (for example `LayeredArt`). Keep the fallback beneath the canvas throughout the enhancement's lifetime.

Choose imagery to suit the site's subject. Possible approaches include abstract forms, diagrams, textures, landscapes, objects, or restrained patterns. These are options, not a required visual vocabulary. Choose colours from the artwork and content needs, then name tokens by purpose, such as surface, text, accent, and decorative glow. Verify contrast against the actual background.

The static state must remain useful when scripts are disabled, WebGL is unavailable, a module fails to load, renderer creation throws, or execution is constrained.

## Apply visitor preferences before loading

Check reduced motion and data saving before importing optional rendering modules or fetching decorative loop videos:

```js
const reducedMotion =
  matchMedia('(prefers-reduced-motion: reduce)').matches;

const saveData =
  navigator.connection?.saveData === true;
```

An unavailable data-saving API is not evidence that a visitor has no bandwidth constraints. Keep optional assets modest regardless.

Honor reduced motion in both CSS and JavaScript. CSS should remove decorative animation and transitions. JavaScript should prevent decorative renderer loading when the preference is active. Listen for preference changes so active motion stops and the static presentation returns. Hiding a canvas does not stop its callbacks or undo a download.

Provide a pause, stop, or hide mechanism for nonessential automatic motion lasting more than five seconds alongside other content, as required by WCAG 2.2.2. Muting video does not address motion.

Describe preference persistence accurately. An in-memory choice lasts only for the current page instance. If persistent storage is prohibited, provide controls on each page and do not promise that a choice survives navigation.

## Load and initialize cautiously

Load optional rendering code on interaction intent, such as focus or pointer entry. Keep those handlers small. Recheck preferences and component lifetime between asynchronous startup steps so initialization can be abandoned safely.

Bundle dependencies under the site's deployment and security policy. Inspect the resulting payload and confirm that dynamic imports work with the deployed Content Security Policy. Use a suitable renderer or your own small WebGL helper.

Context creation can return `null` or throw. Handle both:

```js
canvas.getContext('webgl2', {
  alpha: true,
  premultipliedAlpha: true,
  antialias: false,
  depth: false,
  stencil: false,
  preserveDrawingBuffer: false,
  failIfMajorPerformanceCaveat: true,
  powerPreference: 'low-power'
})
```

These options express preferences and constraints. They do not guarantee a particular GPU or exclude every software renderer. Leave the static presentation visible if creation fails.

Split expensive initialization into stages, yielding between them where practical:

```js
await new Promise(resolve => setTimeout(resolve, 0));
```

A yield gives the browser another opportunity to process work; it does not make an individual synchronous operation interruptible. Feature-detect optional scheduling APIs and parallel shader-compilation support before using them.

Choose quality from observed frame cost and visual results rather than hardware names. Test software-renderer behavior. If renderer identification is necessary, read it once, keep it local, and do not log or transmit it.

Only probe off-screen render-target formats when the effect needs them. Check both required channels and framebuffer completeness:

```js
gl.checkFramebufferStatus(gl.FRAMEBUFFER) ===
  gl.FRAMEBUFFER_COMPLETE
```

A complete framebuffer is not sufficient if its format lacks channels the effect requires.

## Validate the handover

Make the first animated frame agree with the static representation:

- Share deterministic layout inputs and geometry.
- Match colour interpretation, transparency, and compositing.
- Start motion at zero displacement.
- Compare the initial rendered result with the static artwork.

Draw while the canvas is hidden, then inspect the result before marking the enhancement ready. Successful construction, a delayed callback, or several elapsed frames does not prove usable output. A single-pixel readback is only a narrow check and cannot establish whole-image correctness.

Reveal the canvas with a brief handover after validation succeeds. Preserve the fallback beneath it. Inspect for flashes, empty areas, and changes in geometry or colour. Under reduced motion, retain the static state without an animated transition.

## Treat lifecycle changes explicitly

Represent loading, validation, readiness, suspension, context loss, failure, and disposal as distinct states. Define which states may schedule frames or reveal the canvas.

On context loss:

- Stop rendering and expose the fallback.
- Prevent the loss event's default behavior if restoration will be supported.
- Discard assumptions that GPU resources remain valid.

On restoration, rebuild resources from CPU copies, repeat initial-frame validation, and reveal the canvas only after success. Use `WEBGL_lose_context` when available to exercise this path.

Suspend animation when either the document is hidden or the enhanced region is off-screen. Combine document visibility handling with `IntersectionObserver`. A visible tab can contain an invisible canvas, and CSS visibility alone does not stop callbacks.

Resume only when visibility, visitor preferences, pause state, and renderer readiness all permit it.

## Keep animation time-based and finite

Use `requestAnimationFrame` and elapsed time rather than per-frame increments. Reset timing after suspension and clamp elapsed steps so a long gap cannot cause a large jump.

For exponential easing, use elapsed time and a time constant in matching units:

```js
const easing = 1 - Math.exp(-dt / tau);
```

Use fixed substeps for spring integration and limit catch-up work after long gaps. Compare motion duration across different refresh rates.

Stop requesting frames when motion falls below a defined settling threshold. Restart only when an input, resize, or other meaningful state change makes another frame necessary. An unchanged scene does not need a continuous loop.

## Measure the container and clean up

Measure the rendering container after layout settles. Use `ResizeObserver` because container dimensions can change without a window resize.

Handle zero-sized or initially unmeasurable containers by deferring initialization or resizing. Resize only when the effective dimensions or pixel ratio change. Verify sizing on initial load, `pageshow`, history restoration, and orientation changes.

When removing the enhancement:

- Cancel animation frames and scheduled callbacks.
- Disconnect observers and remove event listeners.
- Release renderer resources.
- Ensure pending asynchronous startup work cannot revive the removed component.

## Control rendering cost and visual weight

Measure frame cost and inspect image quality while adjusting pixel ratio, antialiasing, sprite dimensions, and sprite count. High pixel density increases rendered pixel count, while large overlapping translucent sprites increase overdraw. Reduce quality when observed cost exceeds the chosen frame budget.

Choose point textures deliberately. Untextured three.js points appear square. Inspect shared sprite textures and their alpha falloff against the static artwork.

Configure blending for the actual page background. For a transparent three.js layer, use a transparent clear:

```js
renderer.setClearColor(0x000000, 0);
```

This clear value specifies transparency, not a site palette. Check that overlapping light does not wash out nearby text or controls.

Use geometry-based lines when consistent width matters. Native WebGL line-width support varies and is often limited to one pixel. Verify appearance on supported implementations rather than assuming a requested width is honored.

Reserve strong visual emphasis for a clear purpose. Inspect content contrast and control prominence during the busiest animation state, not only when the artwork is still.

## Verify the complete experience

Before considering the enhancement ready, check:

- **Content:** With JavaScript disabled, essential text, relationships, labels, and navigation remain available.
- **Controls:** Keyboard and assistive-technology users can operate controls and understand state changes.
- **Touch:** Scrolling works through the artwork, and canceled gestures leave no stuck interaction.
- **Preferences:** Reduced motion and Save-Data prevent optional fetches; preference changes stop active motion.
- **Failure:** Module failures, null contexts, renderer errors, and context loss expose the complete static design.
- **Handover:** The validated first frame agrees with the fallback and appears without flashes.
- **Lifecycle:** Hidden, off-screen, settled, and removed enhancements stop requesting frames.
- **Layout and quality:** Container changes are handled correctly, and the busiest rendered state preserves readable content.
