# In-Browser Compute Module: running a real language runtime inside a static page

> **Site-agnostic. Shared by first-build and website-maintenance workflows.**
> **Recall trigger:** *"can the visitor run or analyse something on the page?"* · a calculator, converter, validator or sandbox is requested · a site owner wants an interactive tool but has no backend · *"we'd need a serverless function for that"* · the visitor's input should stay on their machine · porting an interactive widget into Astro · a widget works locally and is inert after the Astro build.
> **Recall:** `interactive tool in the visitor browser with WASM no serverless function` · `client-side runtime static site`
> **Implementation scope:** a browser runner with editor, run controls, results and static fallback instructions. Every rule needed to implement that pattern is described below.

These rules address failures that can hide behind a working demo. Test the loading, execution and fallback paths as carefully as the computed answer.

---

## THE ONE-PARAGRAPH VERSION

A full CPython runtime (Pyodide, CPython compiled to WebAssembly) can be downloaded from a CDN and executed **inside the visitor's browser tab**, with **no application backend or build step**. A compatible setup can also work from `file://`; verify that mode in the browsers you support. That turns a static page into a place where a visitor types input, presses a button, and gets a real computed answer. The cost is a substantial initial download, whose size and caching depend on the runtime version, packages and host. The architectural boundary is clear: **browser code cannot keep a secret or bypass access controls on a private service.** Local computation can keep input on the device, provided the implementation does not transmit it. Everything below is how to do it without shipping a hung spinner, a keyboard trap, or a misleading result.

---

## 🔴 RULE 0: THE CLASS, NOT THE INSTANCE

This module is deliberately titled **in-browser compute**, not "the Pyodide runner". A lesson named only after the tool that taught it can be hard to find when another tool presents the same problem.

The class is: **move computation the visitor initiates into the visitor's own machine, and treat the no-JS path as the design rather than the degradation.** Pyodide is one instance. The same shape holds for a WASM SQLite database, a WASM image codec, a WASM PDF renderer, or plain JS doing the work. Every rule about fallbacks, discovery, verdicts and accessibility below applies across runtimes.

---

## 1. 🔴 THE FALLBACK IS THE DESIGN, NOT THE DEGRADATION

**The rule:** decide what the page does when the runtime never arrives *before* writing the happy path, and make that state useful.

For a kitchen-equipment maker's resource library, a tray-capacity calculator could provide a worked example and a terminal command that performs the same calculation. If Pyodide fails for any reason, such as a blocked CDN, an offline connection, disabled WASM or a hard timeout, replace the loading controls with those instructions. There must be no state in which the visitor waits indefinitely at a spinner.

**Why it matters:** a visitor may need an answer while planning a purchase or preparing an order. A hung spinner consumes time while promising a result it will not deliver. A useful static alternative lets the visitor continue.

**This is the same progressive-enhancement rule used elsewhere:**

- A WebGL hero needs a complete static visual underneath it.
- A third-party embed needs useful content when its script never arrives.
- An interactive widget needs a usable zero-JS base, with JavaScript adding the enhancement.

The additional case here is that **the enhancement is a language runtime**.

**Verify it:** block the CDN host, disable JS entirely, remove the runtime's `.wasm` asset from cache and test a fresh load, and throttle to 2G. These are four separate states, all of which must leave a usable page.

---

## 2. 🔴 TWO TIMEOUTS, NOT ONE: advisory then hard

A single cutoff forces a false choice: short enough to protect the user is short enough to throw away a working runtime on a merely slow connection.

```
ADVISORY_MS = 12000   // tell them the terminal command works NOW; keep downloading
HARD_MS     = 40000   // give up, swap in the fallback for good
```

**Why:** a large runtime may still be downloading after 12 seconds on a slow connection. It might arrive shortly afterward. The advisory message is *true when it fires*: "Still loading. If Python is installed, the terminal command below works now." That makes it useful instead of another request to wait.

At the hard timeout, commit to the fallback. A late download must not unexpectedly replace the instructions the visitor has started using.

**The class:** when a resource may be slow *or* absent, those are different states and they need different messages.

---

## 3. 🔴 ONE SOURCE OF TRUTH FOR THE FALLBACK COMMAND: plus a second copy that survives total JS failure

Each run container carries a `data-fallback` command. For example, a bicycle-parts company's guide could demonstrate counting a parts list:

```html
<div class="pyrun" data-fallback="python3 -c &quot;parts = ['spoke', 'nipple', 'washer']; print(len(parts))&quot;">
  <p class="fallback">
    With Python installed, run:
    <code>python3 -c "parts = ['spoke', 'nipple', 'washer']; print(len(parts))"</code>
  </p>
</div>
```

The attribute is authoritative. The static pane also contains a hand-written copy of the same command.

**That duplication protects a distinct failure path.** If JavaScript is enabled but the runner script itself fails to load, `<noscript>` does not appear. There is no injected fallback and no self-repair. Removing the static copy can leave a permanently disabled "Loading Python…" button with no usable instructions.

So: `data-fallback` is the source of truth, the static copy is the survival copy, and the runner **repairs** the pane if the two disagree (`pane.textContent.indexOf(cmd) === -1` → rewrite it). Check that the copies agree before shipping as well, because runtime repair cannot help when the script never loads.

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
  await pyodide.runPythonAsync(src, { globals: ns, filename: 'calc.py' });
} finally {
  ns.destroy();
}
```

Without this, globals leak between runs *and between different editors on the same page*. Broken code can appear to work because a previous run defined the name it needs. In a ceramic studio's editable cost calculator, that could make an incomplete calculation appear valid and prevent someone else from reproducing the result.

**Note the hosting constraint:** a page opened through `file://` cannot assume ordinary Worker loading will work. If that requirement leads to a main-thread runtime, several editors may share one runtime, so namespace isolation must be explicit. Serialize runs that share output handlers or virtual files.

A fresh namespace does not reset the entire runtime or protect the interface from an infinite loop. For hosted pages that execute arbitrary visitor code, a Worker provides a way to keep the interface responsive and terminate execution.

---

## 7. 🔴 AUTOSIZE, OR THE WIDGET LIES ABOUT ITS CONTENT

A fixed editor height can show only part of a template, leave awkward empty space around it, and push the Run button below the fold. Measure the rendered editor instead of assuming its line count predicts its height.

```js
ta.style.height = 'auto';                 // lets scrollHeight report content height
var want = ta.scrollHeight + 2;           // +2 absorbs sub-pixel rounding
ta.style.height = Math.min(Math.max(want, MIN), MAX) + 'px';
```

Four non-obvious dependencies can each produce a separate defect:

- **`height='auto'` first.** Without it, the existing box height can prevent the editor from shrinking to its content.
- **Re-fit on `document.fonts.ready`.** The first measurement uses fallback monospace metrics; the loaded font can change the height.
- **Debounced re-fit on `resize`** (120 ms). The box is only correct for the width it was measured at. A CSS breakpoint that changes padding changes wrapping and therefore the required height.
- **`MIN`/`MAX` must stay in sync with the CSS.** `max-height` clamps a JS-set height, so a disagreement can silently truncate the box. Add an explicit check that the limits agree.

A guessed ceiling can clip the initial template before the visitor types anything. **Set bounds from the measured artifact, never from a round number.** If a deliberate maximum requires internal scrolling, make that scrolling usable and apparent.

---

## 8. 🔴 DO NOT DEDUPLICATE TWO KEYBINDINGS THAT COVER EACH OTHER

`Escape` (focus the Run button) and `Ctrl+Enter` (run without needing Run visible) look redundant. They are not, and the reason is geometric:

> A tall editor can put Run below the fold. **Escape focuses Run and brings it into view. Ctrl+Enter needs no button visibility at all.**

Removing Escape loses the direct route from editing to the button. Removing Ctrl+Enter makes keyboard execution depend on moving focus. Keep normal Tab navigation available too. Advertise both shortcuts in **visible** text, such as an injected `.runhint`. Inject the hint only when its handlers work, because with JS off it would promise unavailable behavior.

In the fallback state, a `dead` flag **releases every captured key**, so `Tab` moves focus normally instead of trapping it in an editor whose Run button is hidden. A keyboard trap violates WCAG 2.1.2.

For Tab/indent editing, preserve the **native undo stack**: Ctrl+Z must still work. `document.execCommand('insertText', …)` can preserve undo in supporting browsers, but it is deprecated. Test its behavior and provide a fallback that does not trap focus or silently break editing.

---
## 9. 🔴 DISCOVERY MUST SURVIVE AN AUTHOR'S OMISSION

`querySelectorAll('.pyrun')`, then **create** any missing part rather than assume it:

```js
var bar = container.querySelector('.runbar');
if (!bar) { bar = make('div','runbar'); container.appendChild(bar); }
```

**Why:** a regional bakery chain may reuse an ordering calculator across several hand-authored guides. Even when one person maintains them, copied markup can drift. Assuming a complete DOM lets an omitted element break an entire widget.

Surface a missing `data-fallback` **on screen** (`[template bug: no data-fallback]`), not only in a console that the author may never open. Do not invent a command that looks runnable but cannot work. Treat the visible diagnostic as a defect to fix before publication.

**The class:** a widget consumed by many hand-authored pages is an API, and an API validates its input.

---

## 10. 🔴 THE LINE-BUDGET TRAP

A browser runner can grow beyond its initial estimate because loading states, keyboard behavior, traceback handling and fallback repair each require code. Keep additions tied to verified behavior. Document the blocks most likely to look redundant and the specific failures they prevent.

**Why this belongs in a reusable module:** a future maintenance pass may see a long vanilla JS file and try to simplify it. Simplification is useful, but deleting a backup copy of fallback content or merging distinct failure states can reopen defects. Put the explanation beside the implementation so the next maintainer can distinguish necessary behavior from accidental complexity.

Before shortening a block, test the failure paths it protects. If a smaller implementation preserves them, use it.

**The class:** an estimate made before measurement is not a budget. When you deliberately exceed one, ship the reason in the artifact.

---
## PORTING INTO ASTRO: the four things that actually matter

**(1) This is NOT an island, and needs no framework.** No React, no `client:*` directive, no hydration. It is a plain `<script src>` plus semantic markup plus `data-` attributes. Serve the runner as a static JavaScript asset and reference it; or use `<script is:inline>` if you must inline it directly in an Astro template. A bare `<script>` is processed by Astro, which is usually fine but can change how it is delivered.

**(2) The architecture avoids the `set:html` script-inertness trap, and that is the strongest argument for it.** Scripts inserted client-side through `innerHTML` are parsed but never executed. A widget that carries its own inline `<script>` inside injected HTML can therefore appear correctly while its controls do nothing. Server-rendered `set:html` output and later client-side HTML insertion have different execution behavior, so do not rely on embedded scripts surviving every rendering path.

This pattern works because the behaviour lives in an **external script that queries the DOM**, and the injected markup is inert data. A widget identified by `data-` attributes can come through `set:html`, from Sanity, or from MDX, provided the runner scans it after it enters the DOM.

**Design consequence, stated as a rule:** *for any interactive widget destined for Astro, put behaviour in an external script keyed on `data-` attributes, never in an inline `<script>` inside injected markup.*

**(3) The one real limitation.** If initialization runs at `DOMContentLoaded` and scans once, markup injected **client-side afterwards** will not be adopted. This includes a modal, a client-routed page transition, or a framework re-render. If a site needs that, expose a re-scan function or use a `MutationObserver`. A page whose markup is present at initial load may not need either.

**(4) Static hosting is preserved, which is the commercial point.** Cloudflare Pages, Vercel static hosting, or another static host can serve the widget. There is no serverless function or server-side compute charge per execution. The visitor's device does the work, so execution capacity does not depend on a compute service you operate. Hosting and bandwidth limits still apply, and runtime downloads and startup time still matter.

---

## WHEN TO REACH FOR THIS: and when not to

**Strong fit**

- Interactive teaching / documentation where the reader edits and runs real code
- Calculators and converters whose logic is non-trivial enough that reimplementing it in JS would fork the source of truth: kiln-load planning for a ceramic studio, gear comparisons for a bicycle-parts company, or material estimates for a garden-supply shop
- Format validators and linters over a file the visitor supplies
- Anything where **the visitor's data must not leave their machine**: see below
- Reusing an existing, trusted Python implementation instead of porting it to JS

**Wrong fit, do not use it**

- Anything needing a database, a secret, an API key, or a private endpoint. **Client-side code cannot hold a secret.** This is architectural, not a configuration gap.
- Anything whose result must be trusted by the server. The client controls the runtime; treat every result as user input.
- Small logic that plain JS does in 20 lines. A multi-megabyte runtime to avoid writing `x * 1000` is an unnecessary download.
- Pages where first-paint budget is the priority and the widget is incidental. Load it lazily, on interaction, or not at all.

**The privacy argument, which is a commercial argument.** A kitchen-equipment maker could let visitors compare equipment layouts without uploading their planning files. Keeping inputs in the browser reduces the data the site needs to receive, store, and protect. Describe that benefit only after verifying it: inspect network traffic during file selection, execution, and error handling, including requests from analytics and third-party scripts. Runtime downloads may still occur; the promise is that visitor inputs and results are not transmitted.

**Scaling up:** Pyodide supports packages such as `numpy`, `pandas`, and `scipy`, with package loading and `micropip` available for supported dependencies. That can turn a simple calculator into a substantial planning or data-analysis tool, at the cost of a larger download. Gate that download behind an explicit user action.

---

## PRE-FLIGHT CHECKLIST: before shipping any in-browser compute widget

1. **Fallback state authored first**, and useful on its own. Verify with the CDN blocked, JS off, WASM unavailable, and a throttled link. **Test these four states separately.**
2. **Two timeouts** wired: advisory (keeps trying, tells the truth) and hard (gives up).
3. **The result fails closed.** No RESULT line, or any ERROR line or exception, means no answer is shown.
4. **Bounds measured from the real artifact**, and JS/CSS bounds asserted equal.
5. **Autosize** with `height:auto` first, a `fonts.ready` refit, and a debounced `resize` refit.
6. **Keyboard**: no trap; every captured key released in the fallback state; escapes advertised in visible text.
7. **Discovery creates missing parts** and surfaces author error on screen.
8. **Fresh namespace per execution.**
9. **Traceback belongs to the user's code**, not the execution wrapper.
10. **Behaviour in an external script keyed on `data-` attributes**, never an inline `<script>` in injected markup.
11. **Confirm no secret, key, or private endpoint** is anywhere near it.
12. If markup can appear after load, **expose a re-scan**.
