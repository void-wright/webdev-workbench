# Responsive layout and build validation

Validate the page as readable content first, then test its enhanced behavior. Keep evidence tied to the exact build being served. Use `05_automations/website-maintenance/skillbook.md` to organize recurring maintenance checks and their evidence.

## Navigation that works without JavaScript

Essential navigation should use fragment links whose targets are the content readers need. A fragment can activate the intended styles while scrolling its subject out of view, so a correct selected state is not enough.

Disable JavaScript and follow every essential fragment link. Confirm that the destination heading and relevant content remain visible, including when a sticky header is present.

Keep fragment offsets in CSS. Account for changes in header height at responsive breakpoints. For example, a destination that needs generous surrounding space could use:

```css
.demo-section {
  scroll-margin-block: 40svh;
}
```

Treat this as a contextual example, not a universal offset. Choose spacing based on the header and the destination, then test it at each header layout breakpoint.

Budget the total height of sticky headers, navigation, and controls. At narrow widths, wrapped navigation can occupy most of a short screen. Verify that enough content remains visible to read and interact comfortably.

## Viewport sizing and mobile browser controls

Test combinations of viewport width and visible height. Include narrow screens, short landscape views, and changes caused by mobile browser toolbars.

For a sticky visual region that must remain stable and cover the screen as toolbars retract, use the large viewport height:

```css
.demo-sticky-visual {
  height: 100lvh;
}
```

The large viewport can extend behind expanded browser controls. Check essential content and controls separately rather than assuming everything inside this region is visible.

Use consistent viewport units for dimensions that must remain aligned. If a visual region and its positioning calculations depend on the same height, mixing small, large, and dynamic viewport units can make them drift during toolbar transitions.

Desktop emulation establishes layout behavior at chosen dimensions. It does not establish how a real mobile browser handles toolbar changes. Mark those results as conditional until verified on a device.

## Decorative animation as an enhancement

Keep essential content readable and usable before graphics initialize and when graphics are unavailable. If a wrapper component holds the canvas and its fallback, give it a descriptive name (for example `LayeredArt`). If you need rendering utilities, use a small WebGL helper of your own; none ships with this package.

When automatic ambient motion is required, initialize it only after all three conditions are satisfied:

- The page has loaded.
- An idle opportunity is available.
- The animated region is visible.

Recheck visibility before starting work. Loading only after user interaction may be appropriate for some experiences, but it does not satisfy a requirement for automatic ambient motion.

Define explicit, measurable budgets before implementation:

| Resource | Budget to record | Validation |
|---|---|---|
| Animation loader | Maximum compressed bytes | Inspect the delivered loader |
| Graphics code | Maximum compressed bytes, including dependencies | Inspect all graphics chunks |
| Pixel density | Maximum rendering scale and drawing-buffer dimensions | Check actual canvas dimensions |
| Frame execution | Maximum JavaScript time per frame | Profile under documented CPU throttling |

Choose limits appropriate to the page and target devices. Measure initialization when the region becomes visible, including the work needed to create graphics resources and produce the first frame.

## Motion controls and suspension

Continuous decorative motion needs both reduced-motion support and a page-level pause control.

With reduced motion enabled, show a still presentation and stop animation loops. Respond to preference changes while the page is open. The pause control must stop every decorative loop, and scrolling or returning to the tab must not override the user's paused state.

Suspend animation whenever its region is off screen or the browser tab is hidden. Resume only when the region is visible, the tab is active, and motion is permitted.

Verify these behaviors directly:

- Scroll the animated region out of view and confirm frame work stops.
- Hide the tab and confirm frame work stops.
- Enable reduced motion and confirm the still presentation remains usable.
- Pause motion, leave and return to the region, and confirm it stays paused.

## Measure loading, startup, and scrolling separately

A navigation-load audit may never activate graphics outside its configured viewport. Record the audit viewport and identify which enhancements actually ran.

Exercise visibility-triggered startup separately. Scroll the animated region into view, capture its initialization work, and then measure scrolling with animation active. Include CPU throttling and record the conditions used.

A passing load audit is evidence about that load scenario. It does not establish animation startup cost, scrolling behavior, or mobile toolbar handling.

## Tie evidence to the final build

Record the source commit with:

```sh
git rev-parse HEAD
```

Also record a content hash of the served build, covering the files that determine the page's behavior and appearance. A commit identifies source history; the build hash identifies the delivered artifact. Timestamps alone do neither reliably.

Use this sequence:

1. Commit the intended changes and let commit hooks finish.
2. Check whether hooks changed tracked files. Resolve and commit those changes before continuing.
3. Build from the final committed source.
4. Serve that build and record its content hash and source commit.
5. Run validation against that served build.
6. Capture final snapshots from the same build and attach its identity to the evidence.

If the served content changes, rebuild and repeat validation before treating the evidence as current.

Test the identity check in a disposable copy: change one byte in a served file and confirm that the recorded hash no longer matches. Restore the content, rebuild, and rerun validation.

## Make validation commands trustworthy

Capture a command's own exit status before filtering or displaying its output:

```sh
command > validation.log 2>&1
result=$?
```

Replace `command` with the actual validation command. Inspect the log only after capturing `result`, and propagate failure to the calling workflow. Ensure the shell's error-handling configuration allows the status capture to execute.

Avoid relying on a pipeline's final exit status when an earlier command is the one being checked. A successful output filter does not prove successful validation.

Before launching audit tools, verify that their temporary directory exists and is writable in their execution environment. Check inherited temporary-directory settings and use an appropriate location for that invocation.

Before terminating a process, inspect its identity, arguments, and relationship to the task. Act only on verified process IDs. Broad command-line matching can select unrelated processes or the checking shell itself.

## Prove that checks detect failures

A successful exit status is useful only if the check examined the intended inputs and can detect its target fault.

For each important check:

- Report what it examined and how many inputs it found.
- Reject unexpectedly empty input.
- Introduce a representative fault in a disposable fixture or build.
- Confirm failure for the expected reason.
- Remove the fault and confirm the valid case passes.

For example, a fragment-navigation check should fail when a required destination is missing. A build-identity check should fail when served bytes change. Neither should pass merely because no pages or files were discovered.

Keep these fault checks focused on the validation mechanism. Their purpose is to establish that a passing result carries meaningful evidence.
