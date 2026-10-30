# Reusable component practices

## Start with project conventions

Read the existing design guidance, shared types, import conventions, installed dependencies, and implementation requirements before building a component. Reuse suitable dependencies before adding a UI library.

Import shared types rather than duplicating component contracts. If a component needs a compatibility adaptation, keep the adapter local and explicitly type its inputs and outputs. Avoid `any` as a shortcut around a mismatch.

## Use semantic styling

Choose styling values from the project's design tokens. Name tokens by purpose, such as `surface`, `text-muted`, `border-subtle`, or `action-primary`, rather than by a particular color.

When the design system has no accent treatment, use font weight, scale, or style to establish emphasis. Do not introduce an unrelated color to solve a hierarchy problem.

When replacing a visual identity, audit more than shared stylesheets. Search for retired literal values with `rg`, including values in component constants, inline styles, SVG attributes, and visualization configuration.

Scope transitions to the properties that should change. Use `transition-colors` when that configured utility matches the interaction. For other effects, specify properties such as opacity or transform explicitly. Inspect hover and focus states for unintended animation of dimensions or spacing.

## Keep display formatting consistent

Centralize number, date, and other display formatting in shared formatters. Handle missing data before formatting so that `null` and `undefined` produce a consistent missing-value marker.

Do not use truthiness to decide whether a numeric value exists. For a garden-supply shop, an inventory count of zero means none are available; a missing count means availability is unknown.

Verify these cases separately:

- `null` and `undefined` display the missing-value marker.
- Zero displays as zero.
- Valid values use the same formatting across components.

## Define stable React boundaries

Place component definitions outside parent render functions. Defining a component inside its parent creates a new component type on each render and can reset child state.

In Next.js, place the client directive at the boundary that needs client-side interaction:

```tsx
'use client';
```

Keep that boundary focused so that code without client-side requirements can remain server-rendered.

Memoize expensive derived computations when their inputs remain stable. Include every relevant input in the dependency list, and treat memoization as an optimization rather than a requirement for correctness.

For conditionally displayed views, declare the lazy component at module scope:

```tsx
const DeferredView = React.lazy(() => import('./view'));
```

Render it inside a `Suspense` boundary with a useful fallback. Keep the surrounding layout stable while the view loads.

## Make interactions accessible and reversible

Give dismissible overlays an accessible opening control and a clearly labeled close button. Support outside-click dismissal and Escape-key dismissal.

Ensure clicks inside the overlay do not count as outside clicks. For stacked overlays, dismiss the active layer rather than every layer. Modal overlays should also manage focus, keep keyboard navigation within the modal, and return focus to the opening control when closed.

Effects that temporarily change document styles must restore the previous value during cleanup:

```tsx
useEffect(() => {
  if (!open) return;
  const previous = document.body.style.overflow;
  document.body.style.overflow = 'hidden';
  return () => { document.body.style.overflow = previous; };
}, [open]);
```

This pattern suits an independently controlled overlay. If multiple overlays can lock scrolling, coordinate ownership so that closing one does not unlock the document while another remains open.

Debounce rapid updates when processing every intermediate value is unnecessary. Keep immediate input feedback responsive, and delay only the dependent work. Clear pending timers when dependencies change and when the component unmounts. Remove event listeners during cleanup as well.

## Share navigation configuration

Drive related navigation controls from one typed configuration. Keep labels, destinations, and associated presentation together so that desktop and compact navigation remain consistent.

Use stable identifiers for rendered items. Keep active-state behavior aligned across the controls that consume the configuration.

Viewport-fixed navigation leaves normal document flow. Reserve enough space for it so that content remains visible, including when navigation text wraps or its height changes.

## Build layouts around their containers

Test each chosen responsive breakpoint below, at, and above its boundary. Check wrapping, overflow, control visibility, and whether content remains reachable in each layout mode.

Size embedded visualizations from their containers rather than assuming viewport dimensions. Use `ResizeObserver` when element dimensions can change independently of the viewport, and disconnect it during cleanup.

A chart beside a collapsible panel, for example, needs to respond to changes in its available width even when the browser window stays the same size.

## Keep graphics legible

Place tooltips outside clipping regions when they must extend beyond a graphic. Use an unclipped overlay layer or a portal, and account for the coordinate system when positioning them. Verify placement near every edge and after scrolling or resizing.

Set SVG presentation properties explicitly when no configured utility expresses the intended state:

```tsx
style={{ strokeOpacity: opacity }}
```

Check that the property reaches the intended SVG element and is not overridden by another styling rule.

## Review before reuse

- Compare styling with the project's design guidance and semantic tokens.
- Verify missing values and zero independently.
- Exercise overlay controls with pointer and keyboard input.
- Confirm cleanup restores document styles and clears pending timers.
- Check for nested component definitions and incomplete computation dependencies.
- Test layout boundaries and container resizing.
- Inspect tooltip clipping, fixed-navigation overlap, and hover and focus transitions.
