---
name: webgl-handoff-and-porting
description: Use when preparing a visual implementation handoff or porting interactive graphics into a production website.
---

# Visual implementation handoff and porting

A handoff should give the receiving developer enough information to reproduce the intended appearance, preserve its behavior, and verify the running result.

## Define the implementation contract

Write the brief and acceptance checks before handing over the implementation. Specify:

- **Purpose and scope:** what the visual communicates, where it appears, and which elements the developer may change.
- **Visual tokens:** named roles for color, typography, spacing, opacity, and emphasis. Choose colors from the site's subject, existing identity, and contrast requirements, then name tokens by purpose, such as `surface`, `text`, and `accent`.
- **Layer order:** the relationship between background artwork, graphics, semantic content, and controls, including which layers receive pointer input.
- **Interaction:** pointer, touch, keyboard, scrolling, idle, and focus behavior where applicable.
- **Controls and modes:** visitor controls, supported optional modes, and temporary development controls.
- **Rendering budgets:** explicit limits for pixel density, scene complexity, asset size, and animation work.
- **Fallbacks:** the static appearance, reduced-motion behavior, and behavior when graphics cannot initialize.
- **Acceptance:** automated checks and live inspection criteria across viewport sizes.

Concentrate visual emphasis around the content or action that matters most. Choose imagery from an open menu guided by the site's subject: photography, illustration, diagrams, abstract forms, textures, or other suitable treatments. Assess the associations each choice may create for the intended audience.

For a garden-supply shop, a plant illustration might support a growing guide, while a diagram might explain irrigation. Let the page's purpose determine the treatment.

## Package assets and references

Give every supplied asset an explicit path and an intended role. Distinguish:

| Role | What to document |
|---|---|
| Source artwork | Editable material used to derive production assets |
| Visual reference | An appearance or composition to compare against |
| Production asset | A file intended for direct use on the website |
| Static fallback or poster | The image shown before rendering or when motion is disabled |

Record dimensions, transparency, cropping expectations, and any relationship between assets. Do not leave the developer to infer whether a reference image belongs in the deployed page.

Keep the brief, asset inventory, implementation, porting notes, and acceptance checks together. For broader specification context, consult `03_skills/webgl-craft/references/09-original-single-skill-spec.md`.

## Choose the medium

Use generated video when preserving existing artwork's texture and composition is central and the motion can be authored in advance. Use WebGL when the visual must respond programmatically to interaction or changing state.

If WebGL needs a utility layer, use your own small WebGL helper where appropriate. Document its responsibilities and dependencies.

### Specify generated video

Document the goal, asset paths and roles, scene composition, motion, constraints, duration, and aspect ratio. Consult the chosen model's current documentation for supported inputs and controls before preparing the generation request.

Design loops around motion with a natural return path. Use matching start and end imagery or seal the transition with a cross-fade. Inspect the seam during repeated playback.

Prepare decorative video for web delivery:

- Provide H.264 and VP9 versions.
- Use muted, inline playback and looping where appropriate.
- Omit embedded text and audio.
- Use the first frame as the poster.
- Show a still image when reduced motion is requested.

Keep meaningful text in semantic page markup regardless of the chosen medium.

## Port the visual faithfully

Preserve the mathematical behavior before simplifying the surrounding infrastructure. Constants, curves, timing, and coordinate relationships are part of the appearance.

Compare the port against the supplied source for:

- Constants and scaling relationships.
- Keyframes, easing curves, and animation durations.
- Gradient stops and opacity.
- Breakpoints and layout behavior.
- Required strings in page content and controls.

Keep headings, descriptions, labels, and calls to action in semantic HTML. Inspect the implementation for text drawn into the canvas and move page content into markup.

If you need one, a wrapper component holds the canvas and its fallback; give it a descriptive name (for example `LayeredArt`). Give it clear ownership of initialization, resizing, animation, and cleanup.

Remove development controls, unnecessary framework wrappers, unused imports, and unused assets. Review dependencies introduced by the authoring environment before carrying them into production.

Distinguish temporary controls from supported authored modes. Keep an inactive supported mode recoverable behind one explicit feature flag, with its purpose and default documented.

## Adapt sizing and resolution

Size focal graphics using both container dimensions:

```js
const focalSize = Math.min(
  width * horizontalScale,
  height * verticalScale
);
```

Validate that dimensions and scale factors are finite and positive before rendering. If a container has zero width or height, defer rendering until it has usable dimensions. Avoid passing invalid or zero sizes into rendering calculations.

Use `ResizeObserver` to respond to container changes, including changes that do not trigger a window resize. Update the drawing buffer, viewport, and scene sizing, or reinitialize rendering when required.

Cap device pixel ratio using an explicit rendering budget. Keep CSS dimensions separate from drawing-buffer dimensions so high-density displays do not increase rendering cost without a bound.

## Control animation lifecycle

Treat motion preferences, visibility, and cleanup as part of the implementation contract.

- **Reduced motion:** render a deliberate static frame without starting a continuous animation loop. Respond if the preference changes.
- **Off screen:** use `IntersectionObserver` to stop animation scheduling when the visual leaves view.
- **Resume:** reset the timestamp before restarting and clamp elapsed time.
- **Cleanup:** cancel pending frames, disconnect observers, remove listeners, and release graphics resources.

Use the supplied timing and scheduling primitives consistently:

```js
// On resume, after confirming that no loop is already active:
lastTime = performance.now();
frameId = requestAnimationFrame(render);

// Inside render, before advancing motion:
const now = performance.now();
const elapsed = Math.min(
  Math.max(now - lastTime, 0),
  maxElapsed
);
lastTime = now;

// On pause or cleanup:
cancelAnimationFrame(frameId);
```

Keep elapsed time and `maxElapsed` in the same units. Schedule the next frame only while animation remains enabled and the visual is visible. Resetting the timestamp prevents a pause from becoming a large simulation step; clamping also bounds unusually long frame intervals.

For production lifecycle and fallback checks, use `03_skills/webgl-hardening-and-testing/SKILL.md`.

## Verify the running result

Source comparisons establish fidelity of inputs. Live inspection establishes whether the result looks and moves as intended. Require both.

Include Playwright checks for:

- Semantic text and usable controls.
- Narrow, wide, and unusually proportioned containers.
- Container resizing and bounded drawing-buffer resolution.
- Reduced-motion rendering with a visible static result.
- Off-screen suspension with no continuing `requestAnimationFrame` scheduling.
- Resume behavior without a large elapsed-time step.
- Supported feature-flag behavior.
- Cleanup and remounting without duplicate loops.

Use observable scheduling instrumentation where needed to verify that work stops. A screenshot alone cannot prove that an animation loop is paused.

Inspect the running visual at multiple viewport sizes. Watch motion through several cycles, move the visual out of view and back, and inspect the first resumed frame for a jump. Check visual emphasis, cropping, text legibility, pointer behavior, and video loop seams.

Finish with a production review for leftover development machinery, unnecessary dependencies, and unused assets.

## Record reusable lessons

Keep handoff notes under clear topic labels such as **Asset roles**, **Sizing**, **Motion**, **Accessibility**, **Rendering budgets**, and **Porting constraints**.

For each lesson, record the condition, the implementation decision, and the check that verifies it. Separate reusable guidance from choices specific to the current visual.
