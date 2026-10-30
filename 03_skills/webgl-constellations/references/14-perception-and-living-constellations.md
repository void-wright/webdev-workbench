# Perception rules and living constellations

These rules apply to interactive constellations drawn over painted artwork, such as a garden-supply shop's how-to hub. Turn each rule into a build-time check where possible: verify that it fails on a defective layout and passes after the fix. This follows the qa-030 pattern in `05_automations/website-maintenance/skillbook.md`.

## 1. Gestalt beats distance rules
Clearance numbers are easy to pass. The eye still applies **closure, common region and similarity**, which can override numerical clearance.
1. **No two lines cross,** except at a shared end star.
2. **No star lies inside a closed region bounded by lines that do not join it** (a point-in-polygon test). Two strands of one relation routed on opposite sides can enclose a whole cluster, making it read as a selection ring.
3. **A doubled relation is ONE connection drawn as two filaments,** about one core width apart, on the same side, ending on the same two stars.
4. **In a single compact lane, order lanes by span** (longer spans outside), so lines that share an end star never cross.
5. **No two clusters with the same star count are congruent** within 12 units RMS after centring, the best permutation, reflection and rotation. Identical arrangements read as a stamped data-visualisation motif.
6. **No line passes through a star it does not end on.**
7. **One relation endpoint per star while its cluster has a free member.** A hub star silently says "this item is the group's connector".
8. **Layout constants the CSS needs are emitted from the solved layout** as custom properties, never mirrored as literals in two files.

## 2. Draw no relation the data does not hold
- **A star-to-star line invites a star-to-star reading.** If the data says "these groups interact", either distribute endpoints using the rule above, or let words in readouts, an equivalent text view and the legend carry the group-level meaning.
- **Random or decorative lines between groups** must stay inside the true relations: random stars and random direction, but only between groups that actually interact. Make an optional "any two groups" mode an explicit setting, and label it as decorative if it represents no data relationship.

## 3. Match the art at the scale it is displayed
- **Size marks over cover-fit art in DISPLAYED-artwork units,** not the SVG viewBox. Stage width and the artwork's cover scale vary independently. Recipe: `vector-effect: non-scaling-stroke` with widths of c × max(100vw/plateW, 100lvh/plateH).
- **The star half-max is the INTERPOLATED crossing.** A whole-pixel ring quantises by up to 2 artwork px, so values just below and just above a threshold cannot reliably be distinguished.
- **The floor binds in every visible state,** including when a disclosure re-scales the art. A pinned star's deliberate swell is exempt from the size ceiling.
- **At DPR 1, a sub-device-pixel line can occupy a wider raster footprint than its nominal stroke.** Measure that footprint in the target renderer. If an artwork-pixel ceiling falls below it, report the constraint as unachievable there rather than treating it as a layout failure.

## 4. Living constellations: a motion vocabulary
For a bicycle-parts company's guide library, a constellation can group guides by topic. Use a motion brief with measurable limits:
- **Stars float** slightly and subtly: each on its own slow path, ≤ 2.5 CSS px, so fixed 48 px DOM targets still cover them.
- **Stable constellation lines inside each cluster,** in the stars' colour, always present, wobbling slightly. They make each cluster read as a real constellation.
- **Transient signal trails between clusters, never within one:**
  - They form like a shooting star in a random direction, attach, oscillate gently with zero amplitude at the attached ends, then fade.
  - **Staggered:** never two forming at once. The next forms as the previous fades, so two are visible only briefly.
  - Pause new ones while a star is previewed or pinned.
- **Background shooting streaks:** far, thin, faint and occasional (every 7–16 s). They never cross a text box or a hit target.
- **Static design underneath:** no script, no WebGL or reduced motion shows the SVG figure with its constellation lines and the true relations.
- **Testability:** the scheduler's state lives in data attributes (forming/fading counts, the last pair's groups). Tests assert never two forming at once, never the same group, at most two visible, and only allowed pairs.
