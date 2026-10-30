# Organizing Implementation and Review

Use this reference to plan web-development tasks, review completed work, and maintain guidance that prevents recurring mistakes.

## Define tasks and ownership

Before implementation, identify dependencies, shared files, and acceptance criteria. Parallelize tasks only when they can proceed independently or depend on an interface that has already been agreed.

Give every delegated task a self-contained specification that includes:

- The intended behavior and relevant context.
- The files or areas the worker owns.
- Required interfaces, data contracts, and dependencies.
- Constraints and acceptance criteria.
- The checks needed to demonstrate completion.

Coordinate edits to shared files. If multiple tasks need to change the same file, assign one owner to combine the changes or sequence the edits. Do not assume workers can see one another’s conversations or unfinished work.

## Check data boundaries and contracts

Validate external data before treating it as an application type. This includes API responses, submitted forms, stored records, and third-party events. A type assertion does not validate a value at runtime. Check required fields, allowed values, and relevant constraints, then handle invalid input explicitly.

Verify that schema-to-type mappings cover every supported field. Check optional fields, null values, defaults, and conversions as well as required fields. Make intentional omissions explicit so they cannot be confused with missing support.

For a bicycle-parts company, a product mapping should account for supported compatibility fields as well as basic product details. A valid product name does not establish that the whole record has been mapped correctly.

When adapting an API integration, compare the result with its documented contract. Review supported query patterns, parameter formats, response shapes, pagination, and error behavior where applicable. Mechanical changes to method names or argument shapes are not sufficient evidence of correctness.

## Verify routes and interactive behavior

Check route wiring explicitly:

- Route parameters reach the intended component in the expected form.
- Props match the component’s contract.
- Links and navigation lead to the intended destination.
- Direct entry and navigation within the application both work.
- Missing or invalid parameters produce an appropriate response.

Exercise interactive state beyond the normal success path. Test rapid input, repeated actions, overlapping requests, failures, and recovery. Confirm that stale responses cannot overwrite newer results, loading states settle correctly, and a failed action does not leave the interface stuck. Use debounce behavior where it fits the interaction, and verify that it preserves the user’s final input.

Reuse verified patterns for repeated interactions. Compare equivalent controls and flows for consistent loading, validation, error, retry, and completion behavior. Share implementation where it reduces drift while preserving meaningful differences.

## Inspect browser output and loading

Review rendered graphics and generated styles in the browser. Source inspection alone cannot establish that SVG references, clipping, inherited styles, responsive layout, or generated CSS behave correctly.

Inspect the final output at relevant viewport sizes and interaction states. When styling fails, examine the generated CSS and computed styles as well as the source rules.

Review imports and loading boundaries. Remove unused imports and identify substantial features or assets that should load on demand. Verify that deferred content has suitable loading and failure states and remains reachable through its intended route or interaction.

## Verify recurring server work

An implemented recurring task still needs a working schedule. Inspect its scheduling configuration and confirm that it points to the correct task, runs at the intended cadence and time zone, and is enabled in the intended deployment.

Check how execution and failure become visible. Consider whether overlapping runs, retries, or missed executions require explicit handling, and verify the behavior required by the task’s contract.

## Reconcile security behavior and documentation

Review comparisons involving sensitive values. Where timing resistance is required, use a suitable timing-safe comparison provided by the platform or an established cryptographic library. Follow its input and length requirements, and inspect surrounding branches for behavior that could undermine the comparison.

Compare security documentation with the implementation. The data inventory should reflect the information the application actually collects, stores, transmits, and exposes. Review applicable security advisories against the dependencies and behavior in use, and document relevant mitigations or unresolved exposure.

Treat documentation and code as evidence to reconcile. Neither should be assumed correct solely because the other refers to it.

## Review the integrated application

Review the combined application after independently reviewed tasks are integrated. Local correctness does not establish that interfaces, routes, styles, and state work together.

Follow representative user flows across the completed work. Verify data movement between layers, route inputs, shared interactions, loading boundaries, and failure recovery. Pay particular attention to assumptions made at task boundaries and changes to shared files.

## Write actionable findings

Each review finding should identify:

- **Location:** the file and line containing the defect.
- **Failure:** what goes wrong and under what conditions.
- **Expected behavior:** what should happen instead.
- **Verification:** how to confirm the correction.

For example:

> `src/components/ProductSearch.tsx:48`: An earlier search response can replace results for the current query when requests finish out of order. Only results matching the latest query should update the list. Verify by delaying the first response and entering a second query before it completes.

Keep separate defects in separate findings. Explain the consequence clearly, and distinguish observed failures from concerns that still need verification.

## Maintain reusable guidance

Maintain guidance for relevance and coverage, not length. Before work begins, identify the rules that apply. During review, check whether the implementation follows them.

When updating guidance:

- Consolidate entries that describe the same safeguard.
- Preserve distinct checks even when they concern the same topic.
- Replace vague advice with a clear trigger, expected behavior, and verification method.
- Remove or revise guidance that no longer applies.
- Add a rule when it closes a meaningful gap in coverage.

A concise reference is useful only if it retains the safeguards needed for the work.
