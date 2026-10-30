---
name: webgl-interaction
description: Interaction physics and state wiring for WebGL/canvas layers that sit under real HTML. Covers DOM-owns-state with the canvas following, eased pointers and Gaussian force fields, first- vs second-order springs for overshoot and settling, loop-exact curl-noise displacement, hit-testing (DOM targets, CPU spatial hash, GPU ID buffers), hover-preview and click-pin grammar with readouts, parallax depth layers, and when a signal needs no WebGL at all. Use when a canvas element must respond to pointer, touch, focus or keyboard, or must move in a way that loops or oscillates. Part of the webgl-craft cluster.
---

# WebGL interaction

## When to use this skill (and when another one)
| You are… | Use |
|---|---|
| wiring hover, focus, click, pin, keyboard or touch to a canvas layer; writing motion that follows, springs, flows or loops | **this skill** |
| deciding whether to use WebGL at all, or its cost | `03_skills/webgl-renderer-and-budget/SKILL.md` |
| boot, pause, reduced motion, tests | `03_skills/webgl-hardening-and-testing/SKILL.md` |

## The one rule: the DOM owns state; the canvas follows
- **The SVG/HTML figure holds every lighting state** as class toggles, produced by a build-time layout with zero runtime physics.
- **Meaningful targets are real DOM elements:** transparent 48 px buttons or links with accessible names and visible keyboard focus. The canvas is `pointer-events:none`.
- **One controller toggles classes and ARIA, then emits a small state** (focused id, pinned id, lit edges). The canvas maps it to **one highlight uniform per role.** Hover and `:focus-visible` drive the same uniform.
- **Result:** hover, focus and keyboard share one state across DOM and WebGL rendering. Without JavaScript, the DOM still provides readable content and usable links. The canvas can vanish at any moment without losing essential information or controls.

## Recipes (full detail and sources in `03_skills/webgl-interaction/references/04-interaction-recipes.md`)
- **Eased pointer:** `p += (target − p)·(1 − exp(−dt/τ))`, with τ about 200 ms. Never use a per-frame constant; convert a per-frame retention factor to `k^(60·dt)`, with `dt` in seconds.
- **Force field:** the vertex shader displaces by `dir·A·exp(−d²/σ²)`, with A a few px. On touch, only during a deliberate drag after capture. Under reduced motion, no field.
- **Following vs oscillating:**
  - **Following:** first-order smoothing, which **cannot overshoot** a stationary target.
  - **Oscillating:** motion that overshoots and returns needs a damped **second-order** spring on fixed 1/120 s sub-steps: `v += (ω²(x*−x) − 2ζω·v)·h; x += v·h`, with ζ ≈ 0.6–0.9 for overshoot and ζ = 1 for critical damping. Choose ω so the numerical integration remains stable.
- **Curl-noise flow:**
  - The continuous field is divergence-free, which helps avoid artificial convergence. In 2D, use `v = (∂ψ/∂y, −∂ψ/∂x)`.
  - **Loop exactly** by tracing a circle in two extra noise dimensions: `(R cos 2πt/T, R sin 2πt/T)`.
  - **Displace from rest, never advect,** because accumulated advection does not guarantee that points return to their starting positions.
  - Do not copy a 3D TSL curl implementation without checking for directional bias.
- **Hit-testing:**
  - DOM targets for every meaningful star.
  - A CPU spatial hash for decorative drifting fields: approximately O(1) per move with bounded bucket occupancy, suitable for modest scenes of about 300 stars.
  - A GPU ID buffer with async PBO only for dense scenes.
  - **Never synchronous `readPixels` in the interaction loop:** it can stall the main thread while waiting for the GPU.
- **Drift vs targets:** either interactive stars don't move, or their drift stays inside the slack between the 48 px target and the drawn core (a few px). Never move DOM targets every frame. Closed-form `f(seed, t)` gives exact positions on any thread whenever needed.
- **Preview/pin grammar:**
  - Hover and focus **preview** exactly what a click **pins**; single selection; siblings dim.
  - The readout sits **in flow, with reserved height** (zero CLS), never as a tooltip.
  - Hover preview only under `(hover:hover) and (pointer:fine)`.
  - Escape returns to the **story state**.
  - `aria-live` fires on pin and focus only, never on hover.
  - The legend-as-controller comes before the figure.
  - Debounce neighbour highlights. Runtime links form at 100 px and break at 120 px (hysteresis).
- **Parallax:**
  - Bake the depth into the plate and animate only a sparse foreground.
  - Use three depth tiers in one instanced draw, with offset = eased pointer × depth, capped at a few px.
  - Extend quads past the edges.
  - Hover only: no gyroscope, nothing on touch, and none under reduced motion (a vestibular trigger).
- **When WebGL is the wrong tool:** one moving sprite plus a few lit stars is SVG/CSS (`offset-path` or WAAPI). Never delay a form submit or a navigation for an animation.

## Ambient motion that must not break interaction
- **Floating stars:** amplitude ≤ 2.5 CSS px, each on its own slow path, so the fixed 48 px targets still cover them.
- **Transient signals** (connections between groups that appear, pulse and fade):
  - Schedule them so that none is forming while another forms.
  - Pause new ones while a star is previewed or pinned.
  - Expose the scheduler's state through data attributes, so tests can assert its rules.
- **Validate the finished build:** measure motion and verify target coverage, preview behaviour and scheduler rules before treating the effect as a reusable example.

## Go deeper
- `03_skills/webgl-interaction/references/04-interaction-recipes.md`: the full recipes, including depth effects and lightweight SVG/CSS interaction examples.
- **Licences:** use GPL or unlicensed examples for conceptual study only unless their terms permit the intended reuse. Check `03_skills/webgl-craft/references/10-licence-ledger.md` before copying code or assets.
