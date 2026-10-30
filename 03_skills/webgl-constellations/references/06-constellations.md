<!-- Practical guidance for legible constellation diagrams.
     Status markers: VERIFIED means checked against a primary source or recomputed;
     CONTRADICTED means do not rely on the claim; UNSETTLED means further verification is needed;
     ESTIMATE means a starting point that requires measurement on the target device.
     Examples describe an invented garden-supply shop's how-to hub. -->

## 6. Constellations that stay legible

### 6.1 Layout: solved at build time

- Solve the layout in a TypeScript prebuild with a fixed seed: place cluster anchors on an ellipse, run a bounded relaxation pass, scale node size by the represented quantity, and flip labels where needed to avoid collisions. Emit SVG with stable `e-*` / `s-*` / `nd-*` hooks for edges, stars and nodes.
- **Trap**: using the same seed in Python and JavaScript does not guarantee the same coordinates. Python's `random.Random(seed)` uses Mersenne Twister; a different browser generator produces a different sequence. Either share one **SplitMix32** implementation between Node and the browser, or have the runtime **read the coordinates the build emitted**. Reserve runtime randomness for decoration such as dust and twinkle phases.
- Layout alternatives: `d3.forceSimulation().randomSource(d3.randomLcg(seed))` with cluster packing. Keep simulation settings and execution order deterministic.
- Size by area: use `radius = maxRadius * sqrt(count / maxCount)` when circle area should be proportional to count. Adding a minimum radius improves visibility but changes that proportional relationship; document the tradeoff.

### 6.2 Line rendering choices

- **Treat `gl.LINES` as 1 px**: many implementations report `ALIASED_LINE_WIDTH_RANGE = [1,1]`. Query the actual range, and use geometry when the design requires wider lines.
- **Default: instanced SDF capsules**: provide endpoints per instance, use `exp(−d²/σ²)` for soft edge falloff, and use round caps to cover segment joins. Split curves into segments at build time. Implement hover by comparing `u_hoveredId` with the instance ID, travelling light with `exp(−((u − v(t))/σ)²)` or an animated `uv.x`, and draw-in by discarding fragments where `u > progress`.
- **Known downside**: neighbouring quads overlap, so joints can accumulate opacity or brightness and develop visible seams. Premultiplied “over” blending avoids additive blowout but can still accumulate alpha. For consistent coverage, draw each curve's segments into a max-alpha mask and composite the curve once, or construct geometry with explicit joins.
- **Costs require measurement**: shader work, overlap, segment count and resolution can change the comparison between SDF capsules and mesh-based lines. Treat unmeasured timing claims as ESTIMATES. Compare equivalent output on the target devices.
- three.js `Line2` and MeshLine implementations are alternatives when the project already uses three.js. Check the selected package's licence, version compatibility and join behaviour before adopting it.
- **SVG poster draw-in**: use `pathLength="1"` with a staggered `--i`, once per screen, gated on `html.js`. Reduced motion must show the fully drawn state. Dashes and filters can repaint, so start with dozens of paths and check rendering cost.

### 6.3 Linking rules

- **Build-time links: relative neighbourhood graph (RNG)**. It is a useful starting point for spatial constellations: connect two points only when no third point is closer to both than they are to each other. Compare it with alternatives on the actual layout. Delaunay graphs can become dense, a minimum spanning tree can omit useful relationships, and k-nearest-neighbour graphs can form disconnected islands. Claims that RNG reliably reproduces human-drawn constellations remain **UNSETTLED** without accessible supporting evidence.
- **Runtime links** (WebGL layer only): use a squared-radius test, `α ∝ 1 − d²/r²`, seeded acceptance, and trim both endpoints so lines stop short of stars. Choose the trim from node size and spacing. Add hysteresis, for example forming links at 100 px and breaking them at 120 px, with a spatial hash. These distances are ESTIMATES to tune against the layout.
- **No edge bundling when readers must trace individual paths**: merged routes make it harder to follow a particular relationship. Keep individual connections distinct.
- **On a page that sells benefits, topology can be omitted**: connect clusters, name stars after useful outcomes, and curate the visible subset at each level. For a garden-supply how-to hub, stars might represent “Plan a shaded border” or “Keep containers watered”. The equivalent HTML list should describe those outcomes; graph counts and edge details need not appear unless they help readers.

### 6.4 Dimming, contrast and the 0.35 trap

Evaluate the final composited colour, not the foreground token alone. Name your palette by role: a dark ground, a line colour, a star colour and one accent. An invented example might use a deep plum ground `#2A1830`, a pale butter line `#F6E7A1`, a sage accent `#9DB89A` and white `#FFFFFF` stars. No contrast ratio is assumed for these combinations.

For each foreground, test alpha values such as 0.35, 0.40, 0.50, 0.60 and 0.90 against the actual background. For ordinary sRGB alpha compositing over an opaque background, blend each encoded channel first:

`C_result = α × C_foreground + (1 − α) × C_background`

Then convert the resulting sRGB channels to linear light using the WCAG formula, calculate relative luminance, and evaluate `(L_lighter + 0.05) / (L_darker + 0.05)`. Graphical objects needed to understand the content generally need 3:1 against adjacent colours under WCAG 1.4.11.

What it means:
1. Dimmed **lines may lose required contrast**. A line that fails the threshold may provide decoration or redundant context, but must not be the only visible representation of a meaningful relationship. Verify the lit state separately; alpha 0.9 does not guarantee a pass.
2. **The compounding trap**: a star token set to `rgba(255,255,255,.9)` and dimmed with `opacity:0.35` has effective alpha 0.315 over an otherwise transparent layer. If measurement establishes a required absolute alpha of `a_min`, the multiplicative opacity must be at least `a_min / 0.9`. Alternatively, set an absolute alpha for the dimmed state. Include parent opacity and any intermediate compositing layers in the check.
3. Brighter parts of a painted background can reduce contrast. Measure beneath each meaningful star and line, including the effect of scrims and background tokens such as `--demo-background-deep`. A flat-colour calculation does not establish contrast across an image.
4. Colour must not be the only carrier of a cluster or state. Use labels, shapes, outlines or other visible cues as well.

### 6.5 Ranked light, focus plus context, readout bands

- **Ranked light**: perceived brightness is nonlinear and depends on target size, background and adaptation. A rough point-source model uses perceived brightness ∝ `I^0.5`, under which “twice as bright” requires **4× the luminance**. Treat this as an ESTIMATE for visual tuning, not a universal law. Establish visibly distinct tiers in the rendered scene without letting halos obscure labels or neighbours.
- **Twinkle**: 0.1-0.5 Hz and opacity 0.7-1.0 are ESTIMATES for a gentle starting range. WCAG 2.3.1 permits no more than three flashes in a one-second period unless the flashing stays below the applicable thresholds. Timing heuristics from a design system are not WCAG rules. Respect reduced motion and provide a way to pause persistent automatic animation.
- **Focus plus context**: dim siblings to a verified safe level, raise relevant edges to a tested highlight alpha, and reserve a readout band for details. Escape restores the default view. Debounce neighbour highlighting so pointer movement does not cause distracting flicker. Highlighting can help readers follow relationships, but do not attach an unverified numerical improvement to it.
- **Keyboard**: use roving tabindex within a suitable composite widget, with cluster-to-star navigation and neighbour relations available in an equivalent HTML table. Use tree semantics only when the interaction is genuinely hierarchical; an arbitrary graph is not automatically a tree. The SVG already draws the edges, so duplicate CSS connector lines are unnecessary. In WCAG 2.2, 2.4.11 is Focus Not Obscured (Minimum, AA); Focus Appearance is 2.4.13 (AAA).
- **Mobile**: redraw, don't shrink. Repack clusters and labels for the available width; tap to focus and tap again to clear. Adopt **48 CSS px** interaction targets and test that size explicitly. A check for 44 px would not verify the chosen requirement. WCAG 2.5.8 uses a 24 CSS px minimum with specified exceptions; that minimum does not replace the larger design target.

---
