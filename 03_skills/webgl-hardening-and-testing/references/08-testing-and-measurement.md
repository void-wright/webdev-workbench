# Verifying progressively enhanced WebGL interfaces

Treat graphics as an enhancement to a usable HTML page. Verify content, interaction, failure recovery and visual fidelity before interpreting performance measurements.

## Define acceptance criteria

Before testing, record:

- Essential content and controls that must work without JavaScript.
- Accessibility requirements for labels, keyboard use, target size and rendered contrast.
- Allowed visual and positional differences between fallback artwork and enhanced rendering.
- Budgets for compressed graphics code, startup work, interaction responsiveness and rendering.
- Approved network origins and the expected loading trigger.
- Browser, viewport, device and preference combinations to test.

Choose tolerances before capturing results. Use repeated performance runs under consistent conditions and report their median alongside the individual results. Inspect automated accessibility findings for every tested page, then verify behavior manually where automation cannot establish equivalence or usability.

## Keep content independent of rendering

Essential content must remain available when JavaScript is disabled, WebGL is unavailable or the graphics module fails.

Keep meaningful labels, descriptions and relationships in HTML. For a bicycle-parts company, a graphical comparison of parts should have an equivalent HTML list or table containing the information needed to compare them. Decorative graphics do not need duplicate descriptions.

Test these conditions independently:

- Disable JavaScript.
- Force the graphics module to fail.
- Simulate unavailable WebGL.

For each condition, inspect the DOM and capture screenshots. Confirm that content remains readable, controls remain usable and the fallback occupies the intended space. Compare the underlying content data with the DOM to detect missing meaningful labels.

## Respect motion preferences and navigation

Apply reduced-motion preferences before navigation or initialization:

```js
await page.emulateMedia({ reducedMotion: 'reduce' });
```

Verify that animation code is not requested and animated media does not begin playing. A visually still result is insufficient if animation resources still load or playback continues invisibly.

Provide a keyboard-operable pause control for ongoing motion. Check that it has an understandable accessible name and communicates its current state. Activate it using only the keyboard, then verify that animation progress and media playback stop. Resume deliberately and confirm that motion does not jump forward.

On touch devices, swipe directly over the graphics area and verify that the page scroll position changes. Graphics interactions must preserve ordinary page navigation.

At representative narrow viewport widths, measure the bounding boxes of interactive targets against the chosen accessibility requirements. Check adjacent controls as well as isolated ones.

## Verify contrast and layout stability

Measure meaningful graphical elements against the background actually rendered at their location. Transparency, compositing and changing imagery can make nominal style values misleading. Test relevant animation and interaction states against the applicable contrast requirement.

Choose named color tokens by their role, such as foreground, surface and focus indicator. Validate those roles in the final composition rather than assuming a token guarantees sufficient contrast everywhere.

Reserve space for fallback artwork, canvas startup and changing text. Inspect raw layout-shift entries:

```js
new PerformanceObserver(list => console.log(list.getEntries())).observe({ type: 'layout-shift', buffered: true });
```

Exercise startup and representative interactions. Include shifts associated with recent input, even when they are excluded from the cumulative layout shift metric. Repeat layout checks with JavaScript disabled.

## Make lifecycle behavior observable

Expose enough diagnostic state for tests to distinguish waiting, loading, ready, paused, failed and recovering states. Include a rendering-progress counter.

Synchronize tests with explicit state changes and advancing frame counts. Fixed delays alone do not establish readiness. When motion is intentionally disabled, assert the expected static state instead of waiting for frames.

Verify the following lifecycle cases:

| Case | Evidence to collect |
| --- | --- |
| Before the loading trigger | No premature graphics requests or context creation |
| Data-saving preference enabled | Requests and initialization follow the declared data-saving behavior |
| Graphics scrolled off-screen | Frame counter stops |
| Document hidden | Frame counter stops |
| Visibility restored | Rendering resumes without a time jump |
| Context lost | Fallback becomes visible and content remains usable |
| Context restored | Resources reinitialize successfully and rendering resumes |
| Refresh or history restoration | Initialization state is valid and canvas dimensions match the container |

Force context loss and restoration rather than waiting for an accidental failure. Repeat refresh and back/forward traversal across viewport sizes. Account for the configured pixel ratio when comparing canvas backing dimensions with its displayed size.

## Test timing and visual fidelity

Base animation progress on elapsed time, not frame count. Supply different mocked animation-frame timestamp sequences and compare positions at equal elapsed times using the predefined tolerance.

Separate active animation time from time spent paused or hidden so that resuming does not introduce a discontinuity.

Compare fallback artwork with the initial enhanced frame at matching viewport dimensions and states. Evaluate alignment, geometry, cropping and meaningful labels against the declared visual tolerances.

When porting an interface, use both source comparison and live rendering:

- Diff geometry, timing and interaction constants against the supplied source.
- Exercise the rendered result across multiple viewport sizes.
- Verify responsive layout and input behavior directly.

A matching screenshot does not establish matching timing, and matching constants do not establish a correct responsive result.

## Measure performance under known conditions

Record the browser version, renderer string, device, viewport, pixel ratio and test conditions. Inspect browser graphics diagnostics to establish whether rendering uses hardware or software. Keep measurements from those paths separate.

Use CPU throttling to investigate startup work, interaction handling and long tasks. It does not emulate another device’s graphics capabilities. Validate rendering budgets on representative physical devices; label budgets without that validation as estimates.

For interaction-triggered enhancements, record the triggering interaction explicitly. Use an interaction-based performance flow that actually activates the enhancement. Collect Interaction to Next Paint where applicable, and distinguish individual interaction timings from a page-level metric.

Run representative interaction sequences under CPU throttling. Inspect long-task and long-animation-frame entries to identify work that disrupts use after loading.

Inspect the performance trace to identify the visible element supplying Largest Contentful Paint. Confirm that the intended primary content has an eligible representation. Do not assume canvas drawing contributes to that measurement.

## Check delivery and automation

Compare captured network destinations with the declared origin list and content security policy. Measure the compressed enhancement bundle against its budget, including deferred dependencies needed to activate it.

Configure browser automation before navigation:

- Set the intended viewport dimensions.
- Apply media preferences and other required test conditions.
- Use distinct server ports for concurrent test servers.
- Write evidence to permitted artifact destinations.
- Configure screenshot timeouts when capture requires them.

Serve files over local HTTP when required by module loading or browser security behavior:

```sh
python3 -m http.server
```

Invoke tools directly in scripts so interactive aliases cannot alter their behavior. If repository HTML retrieval is rate-limited, use the GitHub API to retrieve repository content.

Retain screenshots, traces, network logs and lifecycle observations with the test conditions and acceptance criteria. Report failures and unverified cases explicitly so the evidence supports the conclusion.
