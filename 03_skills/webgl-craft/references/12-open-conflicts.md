<!-- Status markers: VERIFIED (checked against a primary source or recomputed), CONTRADICTED (do not build on it),
     UNSETTLED (a lead), ESTIMATE (no measurement).
     Recommendations below are implementation choices, not measured GPU performance results. -->

## Appendix B. Conflicts between sources, and how they were ruled

| # | Topic | Position A | Position B | Recommendation |
|---|---|---|---|---|
| 1 | Star halo in SVG | SVG `feGaussianBlur` halo | Radial gradients avoid live blur | Use radial gradients for predictable halo rendering without a live blur filter. |
| 2 | Target size | 48 px interaction target | 44 px test target; 24 px WCAG 2.5.8 minimum, subject to exceptions | Use 48 px targets for comfortable interaction. |
| 3 | DPR cap | 1.5 cap | 1.6 cap | Start with 1.5 to limit pixel workload; validate clarity on the intended displays. |
| 4 | Sibling dim | Apply a fixed dimming multiplier | Multiplying an already translucent star can make it unreadable | Calculate the combined opacity and check contrast against the actual background. Keep essential meaning out of dimmed connecting lines. |
| 5 | Loop banners | Autoplay, muted, looping video | WCAG 2.2.2 requires a pause, stop or hide mechanism for qualifying motion | Provide a visible pause control, or stop the motion by 4.9 s without restarting automatically. |
| 6 | Fade duration | 200 ms transition | Longer transitions of roughly 1 s | Prefer roughly 200 ms for responsive interface feedback; reserve longer fades for deliberate storytelling. |
| 7 | IO threshold / dt clamp | IntersectionObserver threshold 0.1; delta-time clamp 0.1 s | Threshold 0.5; clamp 40 ms | Start with threshold 0.1; choose the delta-time clamp by motion type so resumed animation does not jump or destabilize. |
| 8 | Dynamic resolution | Continuously adapt resolution | Avoid the added complexity | Prefer a one-time reduction to a lower rendering tier when needed, avoiding repeated quality changes. |
| 9 | Glow at crossings | `gl.MAX` blending | HDR rendering with Reinhard tone mapping | Use premultiplied “over” blending for connecting lines and additive blending for halos, keeping line intersections controlled while allowing light to accumulate. |
| 10 | Accent in a focal signal | Fill the signal core with the accent colour | Restrict the accent to small highlights | Use a small accent-coloured core with a halo. Preserve the focal point without turning the surrounding scene into a broad colour wash. |
