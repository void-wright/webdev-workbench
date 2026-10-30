# Client state, requests, and cleanup in React

## Organize state by responsibility

Keep related values and the actions that change them together. A request's records, loading status, error, and update actions usually belong together. Separate stores when their responsibilities are independent, such as user preferences and fetched inventory.

Subscribe to individual values and actions through selectors:

```js
const records = useStore((state) => state.records);
const loading = useStore((state) => state.loading);
const error = useStore((state) => state.error);
const setRecords = useStore((state) => state.setRecords);
```

This makes each component's dependencies explicit. Avoid subscribing to the entire store when the component needs only a few fields.

Outside rendering, use the store's supported imperative API to read current state. For a store that exposes `getState()`:

```js
const currentFilter = useStore.getState().filter;
```

Read it when the callback runs if you need the latest value. A value captured before an asynchronous operation may no longer be current. Use selectors for values that should trigger React renders.

## Persist preferences deliberately

Persist an explicit subset of user preferences. For a bicycle-parts company, this could include a preferred measurement unit or inventory display mode.

Keep fetched records, loading flags, errors, timers, and request controllers out of preference storage.

When persistence supports `partialize`, use an allowlist:

```js
partialize: (state) => ({
  measurementUnit: state.measurementUnit,
  displayMode: state.displayMode,
})
```

Inspect the returned object whenever you add store fields. Adding a field to the store should not automatically make it persistent.

## Make request transitions explicit

Ordinary asynchronous functions can manage requests through explicit state updates. Thunks and reducers are optional architectural choices, not prerequisites for fetching data.

Use a consistent sequence:

1. Check that required inputs exist.
2. Set loading to `true` and clear the previous error.
3. Fetch and check the HTTP response status.
4. Commit successful data only if the request is still current.
5. Put failures into visible error state.
6. Clear loading when the current request succeeds or fails.

Console output can help debugging, but users need an error message in the interface. Provide a recovery action, such as retrying, when appropriate.

## Tie requests to their inputs and lifecycle

Declare every reactive input used by an effect in its dependency array. Guard missing prerequisites before starting a request. When inputs change or the component unmounts, cancel the obsolete request and prevent it from committing results.

This example assumes `url` is absent until the required inputs are available, and that the selected store actions have stable identities:

```js
useEffect(() => {
  if (!url) {
    setLoading(false);
    return;
  }

  const controller = new AbortController();

  async function load() {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(url, {
        signal: controller.signal,
      });

      if (!response.ok) throw new Error('Request failed');

      const records = await response.json();

      if (controller.signal.aborted) return;

      setRecords(records);
    } catch (error) {
      if (controller.signal.aborted) return;

      setError(
        error instanceof Error ? error.message : 'Request failed'
      );
    } finally {
      if (!controller.signal.aborted) {
        setLoading(false);
      }
    }
  }

  void load();

  return () => {
    controller.abort();
  };
}, [url, setRecords, setLoading, setError]);
```

Checking `response.ok` matters because an HTTP error response does not necessarily reject `fetch`. Checking cancellation after parsing prevents obsolete results from reaching state. Expected cancellation should not appear as a user-facing failure.

Give shared request state a clear owner. If several components can write to the same request fields, use a request identity as well: only the current request may commit data, errors, or loading changes. A cancelled older request must not clear a newer request's loading flag.

## Debounce input changes without delaying the first request

Start the first request as soon as its required inputs become available. When rapid subsequent changes would produce unnecessary requests, debounce those changes.

Track whether an eligible request has actually started. Do not mark the initial request as started merely because a timer was scheduled. Define when that tracking resets, such as when the component begins working with a different resource.

Each effect execution should own its timer and controller. Its cleanup should clear pending work and abort any request it started:

```js
return () => {
  clearTimeout(timer);
  controller.abort();
};
```

When inputs change during the delay, cleanup removes the old timer. When they change during a request, cleanup aborts it. The next effect execution schedules work for the new inputs.

## Give polling one owner

Keep the interval handle with the operation that owns it. Before creating or replacing an interval, clear the existing one:

```js
clearInterval(interval);
```

Stop polling when the operation completes, required inputs disappear, or the owner unmounts. Clear the handle after stopping so the lifecycle remains explicit.

One interval can still create overlapping requests if a response takes longer than the polling period. Skip ticks while a request is in flight, or schedule the next poll with a timeout after the current request finishes.

Clearing an interval only stops future ticks. It does not cancel a request already running. Abort in-flight polling requests during cleanup and check cancellation or operation identity before every asynchronous state update.

## Review checklist

- Components select only the store values and actions they need.
- Store boundaries follow related responsibilities.
- Persistence includes only intended preferences.
- Effects guard required inputs and declare their dependencies.
- HTTP failures reach visible error state.
- Success and failure clear loading for the current request.
- Obsolete requests cannot commit data, errors, or loading changes.
- The first eligible request starts immediately; later changes are debounced where useful.
- Cleanup clears timers, stops polling, and aborts in-flight work.
- Polling has one owner and prevents overlapping requests.
