# In-Browser Compute Module: running a real language runtime inside a static page

> **Shared guidance for first builds and website maintenance.**
> **Use when:** *"can the visitor run or analyse something on the page?"* · a calculator, converter, validator or sandbox is requested · a site needs an interactive tool without a backend · *"we'd need a serverless function for that"* · visitor input should stay on their device · porting an interactive widget into Astro · a widget works locally and is inert after the Astro build.
> **Recall:** `in-browser compute running a real language runtime inside a static page` · `in-browser compute astro set:html script inertness external script data attributes` · tags `in-browser-compute`, `wasm-runtime`, `static-site-compute`, `progressive-enhancement`
> **Implementation guidance:** use the rules below to build and verify the runtime, fallback and interaction states together.

These rules address defects that arise when an interactive tool becomes part of a static page. Each rule connects a failure mode to a fix and explains why it matters.

---

## THE ONE-PARAGRAPH VERSION

A full CPython runtime (Pyodide, CPython compiled to WebAssembly) can be downloaded from a CDN and executed **inside the visitor's browser tab**, with **no application backend or application build step**. A compatible setup can even work from `file://`. That turns a static page into a place where a visitor types input, presses a button, and gets a real computed answer. Budget for a substantial initial download, potentially around 13 MB depending on the runtime version and packages, then verify the actual transfer size and cache headers. The architectural boundary is firm: **browser-delivered code cannot keep secrets or bypass access controls on a database or private API.** Everything below is how to do it without shipping a hung spinner, a keyboard trap, or a misleading result.

---

## 🔴 RULE 0: THE CLASS, NOT THE INSTANCE

This module is deliberately titled **in-browser compute**, not "the Pyodide runner". A lesson named only after the tool that taught it is harder to find when the same problem appears with a different tool.

The class is: **move computation the visitor initiates into the visitor's own machine, and treat the no-JS path as the design rather than the degradation.** Pyodide is one instance. The same shape holds for a WASM SQLite, a WASM image codec, a WASM PDF renderer, or plain JS doing the work. Every rule about fallbacks, discovery, verdicts and accessibility below is runtime-agnostic.

---

## 1. 🔴 THE FALLBACK IS THE DESIGN, NOT THE DEGRADATION

**The rule:** decide what the page does when the runtime never arrives *before* writing the happy path, and make that state useful.

For a bicycle-parts company's editable sizing example, each run area can be **replaced** by an equivalent terminal command if Pyodide fails for any reason: CDN blocked, offline, WASM disabled, slow link or hard timeout. For visitors who do not use a terminal, provide a worked example or manual calculation as well. No failure state should leave the visitor staring at a spinner.

**Why it matters:** visitors may be comparing parts while working on a repair, with little time to troubleshoot the page. A hung spinner consumes that time while promising a result it may never deliver.

**This extends familiar progressive-enhancement rules:**

- A WebGL hero needs a useful static composition beneath the animation.
- A third-party embed needs readable content when its script fails.
- An interactive widget needs a useful zero-JS base, with JS adding the enhancement.

A language runtime is another enhancement with the same obligation.

**Verify it:** block the CDN host, disable JS entirely, remove the cached `.wasm` response and block its replacement, and throttle to 2G. These are four separate states, all of which must leave a usable page.

---

## 2. 🔴 TWO TIMEOUTS, NOT ONE: advisory then hard

A single cutoff forces a false choice: short enough to protect the user is short enough to discard a working runtime on a merely slow connection.

```
ADVISORY_MS = 12000   // tell them the terminal command works NOW; keep downloading
HARD_MS     = 40000   // give up, swap in the fallback for good
```

**Why:** allowing 12 s for a roughly 13 MB payload requires about 9 Mbps before overhead and initialization. On a slow connection, that cutoff can discard a runtime that would have arrived at 20 s. The advisory message is *true when it fires*: "Still loading; the terminal command below works now." It provides an immediate option while loading continues.

**The class:** when a resource may be slow *or* absent, those are different states and they need different messages.

---

## 3. 🔴 ONE SOURCE OF TRUTH FOR THE FALLBACK COMMAND: plus a second copy that survives total JS failure

For a ceramic studio's packing calculator, a run container might carry `data-fallback="python3 -c 'print((37 + 7) // 8)'"`. The command calculates how many eight-item boxes are needed for an illustrative order of 37 pieces. That attribute is authoritative. The static pane also contains a hand-written copy of the same command.

**That looks like unnecessary duplication, but it serves a purpose.** Removing the static copy breaks an important branch: **JS enabled + the runner script itself failing to load** yields no `<noscript>`, no injected fallback, no self-heal, and a permanently disabled "Loading Python…" button. Deduplication has created the forbidden state.

So: `data-fallback` is the source of truth, the static copy is the survival copy, and the runner **self-heals** the pane if the two disagree (`pane.textContent.indexOf(cmd) === -1` → rewrite it). When the runner loads, it repairs drift; when it does not, the static instruction remains available.

**The class:** the invariant is *"a usable instruction is on screen in every failure state"*, not *"the string appears once"*. Count invariants, not occurrences.

---

## 4. 🔴 READ THE RESULT FROM AN EXPLICIT CONTRACT, AND FAIL CLOSED

The page and the code it runs need an agreed way to say "here is the answer" and "this went wrong". For a calculator, a simple contract is one marker per outcome:

```
answer  -> print a line beginning  RESULT:
problem -> raise an exception, or print a line beginning  ERROR:
```

Show the answer only when **the code raised no exception AND printed a RESULT line AND printed no ERROR line**. Anything else is shown as a problem. If the runtime stops without printing anything, the page must not display an empty or stale answer as if it were current.

**Match on the start of a trimmed line, not on a substring and not on the whole line.** A substring check for `ERROR` misreads a valid line such as `RESULT: 12 pots, no ERROR margin needed`. An exact whole-line check rejects a useful line such as `RESULT: 12 pots (rounded up)`. Checking whether a trimmed line *begins* with the marker handles both. Write tests for both cases and for output that contains a RESULT line and an ERROR line together.

**The class:** any text-based contract between two systems needs its matching rule chosen against plausible awkward output, not only against the tidy example.

---

## 5. 🔴 SHOW THE VISITOR THEIR OWN ERROR, NOT THE RUNTIME'S PLUMBING

Pyodide runs visitor code from inside its own machinery, so a Python traceback can begin with internal runtime frames. Their number and paths vary with the runtime version and the error type. A visitor who edited a formula should see the frame that points at *their* code first.

The fix has three cooperating pieces, and all three are needed. Here, `calc.py` is a virtual file created inside the browser runtime:

```js
pyodide.FS.writeFile('calc.py', src);   // so linecache can echo the source line
pyodide.runPython('import linecache; linecache.clearcache()');
pyodide.runPythonAsync(src, { globals: ns, filename: 'calc.py' });
```

Then show the trace from the first `File "calc.py"` frame onward. Keep the virtual file name and the execution filename identical, and confirm the name resolves against the runtime's working directory.

Pass everything from that frame downward through unchanged: carets, the echoed source line and the exception line. If no such frame exists (the failure happened inside the runtime itself), show the full trace so the problem stays diagnosable.

**The class:** when you host someone else's execution, decide which stack frames help them fix the failure, and remove only the ones that hide it.

---

## 6. 🔴 FRESH NAMESPACE PER RUN

```js
const ns = pyodide.runPython('{"__name__": "__main__", "__file__": "calc.py"}');
try {
  // ... run in it ...
} finally {
  ns.destroy();
}
```

Without this, globals leak between runs *and between different editors on the same page*, so broken code can appear to work because a previous run defined the name it needs. On a garden-supply shop's editable coverage calculator, that can produce an answer that cannot be reproduced from the visible inputs.

**Note the deployment constraint:** a setup intended to work from `file://` may need main-thread execution because ordinary Worker loading is restricted there. One shared runtime serving several editors needs explicit namespace isolation. A fresh namespace does not reset every imported module or virtual file, so define and test those boundaries too. For hosted pages, a Worker also provides a way to keep computation off the UI thread and terminate a stuck run.

---

## 7. 🔴 AUTOSIZE, OR THE WIDGET LIES ABOUT ITS CONTENT

A fixed editor box can show only a small portion of its template, leave unused space elsewhere, and push the Run button below the fold. Measure the rendered page rather than inferring its usability from CSS values.

```js
ta.style.height = 'auto';                 // lets scrollHeight reflect content height
var want = ta.scrollHeight + 2;           // +2 absorbs sub-pixel rounding
ta.style.height = Math.min(Math.max(want, MIN), MAX) + 'px';
```

Four non-obvious dependencies can each cause a separate defect:

- **`height='auto'` first.** Without it, the current box height can prevent the measurement from shrinking with the content.
- **Re-fit on `document.fonts.ready`.** The first measurement uses fallback monospace metrics; the loaded font can change the height.
- **Debounced re-fit on `resize`** (120 ms). The box is only correct for the width it was measured at. A CSS breakpoint that changes padding changes wrapping and therefore the required height.
- **`MIN`/`MAX` must stay in sync with the CSS.** `max-height` clamps a JS-set height, so a disagreement can produce an unexpectedly truncated box. Verify that the bounds agree.

A ceiling chosen from a guess can clip the initial template before the visitor types anything. **Set bounds from the measured artifact, never from a round number.** If a deliberate maximum requires scrolling, make that scrolling usable and keep the run controls reachable.

---

## 8. 🔴 DO NOT DEDUPLICATE TWO KEYBINDINGS THAT COVER EACH OTHER

`Escape` (focus the Run button) and `Ctrl+Enter` (run without needing Run visible) look redundant. They are not, and the reason is geometric:

> A tall editor can place Run below the fold. **Escape focuses Run and focusing scrolls it into view. Ctrl+Enter needs no visibility at all.**

Removing Escape loses a direct route out of an editor that captures Tab for indentation. Removing Ctrl+Enter makes running depend on moving to the button. Advertise both in **visible** text, such as an injected `.runhint`. Inject the hint only after the handlers are ready, because with JS off it would promise unavailable behavior.

Also: in the fallback state a `dead` flag **releases every captured key**, so `Tab` moves focus normally instead of trapping it in a box whose Run button is hidden. A failed runtime must not create a keyboard trap.

Where supported, `document.execCommand('insertText', …)` can preserve the **native undo stack** when handling Tab or indentation. It is deprecated, so verify the behavior in supported browsers and provide an alternative where needed. Ctrl+Z must still work.

---
## 9. 🔴 DISCOVERY MUST SURVIVE AN AUTHOR'S OMISSION

`querySelectorAll('.pyrun')`, then **create** any missing part rather than assume it exists:

```js
var bar = container.querySelector('.runbar');
if (!bar) { bar = make('div','runbar'); container.appendChild(bar); }
```

Here, `make` is a helper supplied by the widget that creates an element and assigns its class.

**Why:** a regional bakery chain may reuse one calculator template across several how-to pages, each edited separately. Assuming every page has a complete DOM makes an omitted element a runtime failure. Surface a missing `data-fallback` **on screen** (`[template bug: no data-fallback]`), not only in a console nobody opens. Otherwise, the page may confidently present a command that cannot run.

**The class:** a widget consumed by many hand-authored pages is an API, and an API validates its input.

## 10. 🔴 THE LINE-BUDGET TRAP

An in-browser compute script can outgrow its initial line estimate because each addition provides a *verified behaviour*. Its header should identify the blocks most likely to be mistaken for padding and explain which measured defects would return if they were removed.

**Why this belongs in a doctrine module:** a future maintenance pass may see a long vanilla JS implementation and feel an urge to simplify. That instinct is useful, but line count alone cannot distinguish unnecessary complexity from necessary safeguards. The file must **explain** which reductions were already tested and what they broke. *"If you are here to shorten this file: measure first, and preserve the verified behaviours."*

**The class:** an estimate made before measurement is not a budget. When you deliberately exceed one, ship the reason in the artifact.

---

## PORTING INTO ASTRO: the four things that actually matter

**(1) This is NOT an island, and needs no framework.** No React, no `client:*` directive, no hydration. It is a plain `<script src>` plus semantic markup plus `data-` attributes. Serve the compute script as a static asset and reference it; or use `<script is:inline>` if you must inline it. A bare `<script>` is normally processed by Astro, which is usually fine but changes how the script is delivered.

**(2) The architecture avoids the script-inertness trap in injected HTML, and that is a strong argument for it.** Scripts inserted through browser-side `innerHTML` are parsed but never executed. Astro's `set:html` can render HTML on the server, so it is not universally equivalent to browser-side `innerHTML`. Even so, a widget that depends on a script embedded in an HTML string is fragile when that content later moves through client-side injection.

This pattern survives because the behaviour lives in an **external script that queries the DOM**, and the injected markup is inert data. A block marked with `data-compute` can be rendered through `set:html`, come from Sanity, or be authored in MDX, provided initialization runs after the markup is present.

**Design consequence, stated as a rule:** *for any interactive widget destined for Astro, put behaviour in an external script keyed on `data-` attributes, never in an inline `<script>` inside injected markup.*

**(3) The one real limitation.** If `init()` runs at `DOMContentLoaded` and scans once, markup injected **client-side afterwards** will not be adopted. This includes a modal, a client-routed page transition, or a framework re-render. If your site needs that, expose a re-scan function or use a `MutationObserver`. Make repeated initialization safe so existing widgets do not gain duplicate handlers.

**(4) Static hosting is preserved, which is the commercial point.** Cloudflare Pages, Vercel static hosting, or another CDN can serve the widget. Execution needs no serverless function, no server-side per-run compute, and no server cold start. The visitor's device does the work. Hosting bandwidth, asset delivery, and device capacity still have limits and costs.

---

## WHEN TO REACH FOR THIS: and when not to

**Strong fit**

- Interactive teaching or documentation where the reader edits and runs real code
- Calculators and converters whose logic is complex enough that reimplementing it in JS would fork the source of truth: a kitchen-equipment maker's capacity planner, a bicycle-parts company's gearing calculator, or a garden-supply shop's planting-layout tool
- Format validators and linters over a file the visitor supplies
- Anything where **the visitor's data must not leave their machine**: see below
- Reusing an existing, trusted Python implementation instead of porting it to JS

**Wrong fit, do not use it**

- Anything needing a database, a secret, an API key, or a private endpoint. **Client-side code cannot hold a secret.** This is architectural, not a configuration gap.
- Anything whose result must be trusted by the server. The client controls the runtime; treat every result as user input.
- Small logic that plain JS does in 20 lines. Downloading a multi-megabyte runtime to avoid writing `x * 1000` is unjustified.
- Pages where first-paint budget is the priority and the widget is incidental. Load it lazily, on interaction, or not at all.

**The privacy argument, which is a commercial argument.** A ceramic studio checking a private order file or a regional bakery chain planning deliveries may prefer a tool that processes inputs entirely in the browser. That can reduce the need to upload, store, and delete sensitive business data. Make that promise only after checking the complete page, including analytics and third-party scripts. Verify network activity during input and execution: runtime downloads may occur, but user data must not be transmitted. Browser-side processing alone does not prove privacy.

**Scaling up:** Pyodide supports packages such as `numpy`, `pandas`, and `scipy`, with `micropip` available for compatible Python packages. This can turn a small calculator into a substantial planning or data-analysis tool. Package compatibility and larger downloads need checking, so gate heavy loading behind an explicit user action.

---

## PRE-FLIGHT CHECKLIST: before shipping any in-browser compute widget

1. **Fallback state authored first**, and useful on its own. Verify with the CDN blocked, JS off, WASM unavailable, and a throttled link: **four states, tested separately.**
2. **Two timeouts** wired: advisory, which keeps trying and tells the truth, and hard, which gives up.
3. **The result fails closed.** No RESULT line, or any ERROR line or exception, means no answer is shown.
4. **Bounds measured from the real artifact**, and JS/CSS bounds asserted equal.
5. **Autosize** with `height:auto` first, a `fonts.ready` refit, and a debounced `resize` refit.
6. **Keyboard**: no trap; every captured key released in the fallback state; escapes advertised in visible text.
7. **Discovery creates missing parts** and surfaces author error on screen.
8. **Fresh namespace per execution.**
9. **Traceback belongs to the user's code**, not the sandbox.
10. **Behaviour in an external script keyed on `data-` attributes**: never an inline `<script>` in injected markup.
11. **Confirm no secret, key, or private endpoint** is anywhere near it.
12. If markup can appear after load, **expose a re-scan**.
