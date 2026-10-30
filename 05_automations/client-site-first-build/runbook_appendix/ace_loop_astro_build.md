# Appendix: ACE Loop for the Astro Build Phase

> The Astro build phase ALWAYS runs through an ACE design loop with a 9.8/10 HARD threshold and empirical Lighthouse + axe checks.

## Why the ACE Loop Here (Not Elsewhere)

Scaffolding, running CLI commands, setting environment variables, and pushing to Git are procedural work. Once their inputs and choices are settled, they do not need repeated subjective design review.

HTML-to-Astro decomposition is the part of the build where:

- Multiple valid implementations exist for the same handoff.
- Subtle quality issues, such as heading order, color contrast, and semantic HTML, determine whether the implementation clears the quality threshold.
- Iteration helps when the Reflector's prioritized change list, called the P-list, gives specific corrections.

So the Astro implementation gets the loop. Other procedures run once unless a check fails or an input changes.

## Workspace

The following is a generated workspace layout, not a set of files included with Voidwright. Replace the placeholders with values for your own build.

```text
<your-site-repo>/ACE_Workspaces/site_build_<slug>_<run-id>/
├── extracted/                          # unzipped design handoff
│   ├── index.html                      # supplied page design
│   └── design-tokens.json              # supplied design tokens
├── task_spec.md                        # build mode, requirements, tokens, review rubric
├── workspace_manifest.json             # files written across iterations
├── iteration_N/
│   ├── generation_report.json          # changes made and strategies applied
│   ├── reflection_N.json               # scores, P-list, and classifications
│   ├── build.log
│   ├── preview.log
│   ├── playwright/                     # Lighthouse, axe, and visual artifacts
│   └── change_log.jsonl
└── skillbook.md                         # local strategies, merged into the automation skillbook
```

Keep this workspace in the repository's `ACE_Workspaces/` directory, exclude it from version control, and **never place it inside** the deployable source tree. Review artifacts and working notes must not become public site assets.

## Stopping Conditions

| Condition | Decision |
|-----------|----------|
| Score 9.8/10 or above (HARD), all 5 dimensions at 9.5 or above, and all empirical checks passing | SATISFACTORY: exit the loop and continue the build workflow |
| Score below 9.8, any dimension below 9.5, or any empirical check failed or not run | CONTINUE: run another iteration with the P-list |
| No improvement of 0.1 or more across 2 consecutive iterations | STALLED: pause for a human decision |
| Iteration count = 5 without meeting the acceptance conditions | MAX_ITERATIONS: pause for a human decision |

**No rounding**: 9.79 is CONTINUE, not SATISFACTORY. If a review accepts a score below the threshold, reopen the loop.

**Empirical scans required for 9.8+**: code inspection alone cannot establish that the rendered build meets the acceptance conditions. Lighthouse and axe results provide evidence that subjective review cannot supply.

## Iteration N Cycle (Generator, Reflector, Curator)

### Generator pass (design-generator agent)

**Inputs**:

- `task_spec.md`: build mode, requirements, design tokens, and scoring dimensions.
- Workspace `skillbook.md`: current strategies, including relevant resource-hub skills.
- After the first iteration: the previous reflection's P-list with specific change instructions.

**Outputs to `iteration_N/`**:

- A report describing new or updated files in `<your-site-repo>/`.
- `generation_report.json` documenting strategies applied and the manifest of files written.

**Iter-1 starting point**:

- Start from a clean Astro scaffold configured for the chosen host. Never copy another site's repository with its Git history.
- If using a finished site as a template, remove its identity, content, analytics identifiers, and service configuration first. Move reusable settings into configuration constants. Wire the Sanity client only for builds that use the resource hub.
- Decompose `extracted/index.html` into a base layout, hero, and section components.
- Apply `extracted/design-tokens.json` to the Tailwind theme and global CSS custom properties.
- Add the AEO schemas through the base layout's `<slot name="head" />`.
- On Workers previews, send `X-Robots-Tag: noindex, nofollow` on every response. Use the static header configuration for assets and response code for Worker-generated pages. Leave the crawler rules crawlable so crawlers can see the header, and omit a redundant robots meta tag. For a Vercel preview, use robots meta, `Disallow: /`, and platform authentication.

**Iter-2+ targeting**:

- Address ONLY the items in the previous iteration's P-list.
- Do NOT introduce unrequested changes.

### Reflector pass (design-reflector agent)

**Inputs**:

- All build artifacts in `<your-site-repo>/`.
- `task_spec.md`, including the dimension rubric.
- The previous reflection for comparison.

**Five Dimensions (scored 0-10 each)**:

1. **Completeness**: every documented build requirement is implemented.
2. **Correctness**: Astro renders, Sanity GROQ works where used, and the browser reports no console errors.
3. **Quality**: code is idiomatic, components are reusable, and CSS is organized.
4. **Convention adherence**: the build uses the Tailwind v4 Vite plugin rather than `@astrojs/tailwind`, includes the required AEO schemas, uses the base layout slot pattern, and exposes design tokens through CSS custom properties.
5. **Skillbook utilization**: relevant strategies are applied without introducing harmful patterns.

**Empirical Gates**: run these checks AFTER dimension scoring. ALL must pass before SATISFACTORY. Run them from the repository root. `N` is the iteration number, `WS` is the generated workspace path, and `WORKBENCH_ROOT` is the location of your Voidwright installation. Capture each exit status directly, never through a pipe.

The commands below define generated build artifacts under `dist/`, including `dist/index.html` and `dist/_headers`; these are outputs of your site build, not shipped package files.

```bash
# Run from your site repository.
# Set WORKBENCH_ROOT to your Voidwright installation directory beforehand.
: "${WORKBENCH_ROOT:?Set WORKBENCH_ROOT to your Voidwright installation directory}"
WS="ACE_Workspaces/site_build_example_local"
N=1
mkdir -p "$WS/iteration_$N/playwright"

# 1. Clean build, zero warnings.
rm -rf dist
npm run build > "$WS/iteration_$N/build.log" 2>&1
build_rc=$?
echo "build rc=$build_rc"
rg -ci 'warn' "$WS/iteration_$N/build.log"
# Expect no matching warning lines; rg returns 1 when no match exists.

# 2. Sanity GROQ test, only for builds that use Sanity.
# Configure SANITY_API_TOKEN using the packaged credential setup.
bash "$WORKBENCH_ROOT/06_web_tools/bearer-curl" SANITY_API_TOKEN -sS \
  'https://<your-sanity-project-id>.api.sanity.io/v2025-02-19/data/query/production?query=*%5B_type%3D%3D%22resource%22%5D%5B0..2%5D'
groq_rc=$?
echo "groq rc=$groq_rc"
# Expect JSON with a "result" array; an empty array is fine before seeding.
# A successful HTTP request alone does not prove the query returned valid data.

# 3. Lighthouse on the local preview server.
npx astro preview --port 4321 > "$WS/iteration_$N/preview.log" 2>&1 &
PREVIEW_PID=$!
sleep 5

# Run five times and gate on the median category scores.
for run in 1 2 3 4 5; do
  npx lighthouse http://localhost:4321/ \
    --output=json \
    --output-path="$WS/iteration_$N/playwright/lighthouse-$run.json" \
    --quiet --chrome-flags="--headless --no-sandbox --disable-gpu"
  lh_rc=$?
  echo "lighthouse run=$run rc=$lh_rc"
  test -s "$WS/iteration_$N/playwright/lighthouse-$run.json" ||
    echo "NOT RUN: Lighthouse wrote no report"
done

LH_DIR="$WS/iteration_$N/playwright" node -e '
const fs = require("fs");
const path = require("path");
const targets = {
  performance: 90,
  accessibility: 95,
  "best-practices": 95,
  seo: 90
};
const reports = [1, 2, 3, 4, 5].map(n =>
  JSON.parse(fs.readFileSync(
    path.join(process.env.LH_DIR, `lighthouse-${n}.json`), "utf8"
  ))
);
let failed = false;
for (const [category, target] of Object.entries(targets)) {
  const scores = reports.map(report => {
    const score = report.categories?.[category]?.score;
    if (typeof score !== "number" || !Number.isFinite(score)) {
      throw new Error(`NOT RUN: missing score for ${category}`);
    }
    return score * 100;
  }).sort((a, b) => a - b);
  const median = scores[2];
  console.log(`${category}: median=${median}, target=${target}`);
  if (median < target) failed = true;
}
process.exit(failed ? 1 : 0);
'
lh_gate_rc=$?
echo "lighthouse median check rc=$lh_gate_rc"

# 4. axe-core scan via Playwright, following qa-007.
AXE_OUT="$WS/iteration_$N/playwright/axe.json" node -e '
const { chromium } = require("playwright");
const axeSource = require("axe-core").source;
(async () => {
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage();
    await page.goto("http://localhost:4321/");
    await page.evaluate(axeSource);
    const results = await page.evaluate(async () => await window.axe.run(document));
    require("fs").writeFileSync(process.env.AXE_OUT, JSON.stringify(results, null, 2));
    const bad = results.violations.filter(
      v => v.impact === "critical" || v.impact === "serious"
    );
    console.log("axe critical+serious:", bad.length);
    process.exitCode = bad.length ? 1 : 0;
  } finally {
    await browser.close();
  }
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
'
axe_rc=$?
echo "axe rc=$axe_rc"
kill "$PREVIEW_PID"

# 5. AEO schema validation for the generated homepage.
node -e '
const html = require("fs").readFileSync("dist/index.html", "utf8");
const schemas = [...html.matchAll(/<script type="application\/ld\+json">(.*?)<\/script>/gs)]
  .map(m => JSON.parse(m[1]));
const nodes = schemas.flatMap(s =>
  Array.isArray(s["@graph"]) ? s["@graph"] : [s]
);
const types = nodes.flatMap(s =>
  Array.isArray(s["@type"]) ? s["@type"] : [s["@type"]]
);
console.log("AEO schemas:", types);
const required = ["Organization", "WebSite", "BreadcrumbList"];
const missing = required.filter(r => !types.includes(r));
if (missing.length) {
  console.error("MISSING SCHEMAS:", missing);
  process.exit(1);
}
'
aeo_rc=$?
echo "aeo rc=$aeo_rc"

# 6. Workers preview indexing posture in the generated static header file.
rg -q 'X-Robots-Tag: noindex' dist/_headers
hdr_rc=$?
echo "noindex header rc=$hdr_rc (0 = present)"
# Also inspect actual preview responses, including Worker-generated responses.
# For Vercel, verify the preview controls described above instead.
```

`require("playwright")` and `require("axe-core")` need both packages in the repository's devDependencies: `npm install -D playwright axe-core`. A check whose required output file is empty is "not run", never a pass. Record every failed command even if later commands succeed. These homepage checks are a starting point; review representative routes and interactive states as well.

**Outputs to `iteration_N/`**:

- `reflection_N.json` containing dimension scores, total score, classification of each prior strategy as helpful, harmful, neutral, or missed, the P-list, and the stopping decision.
- Specific file-and-line corrections in the P-list, phrased as “change X to Y.”
- `playwright/` artifacts, including the Lighthouse reports, `axe.json`, and screenshots when visual checks use Playwright.

### Curator pass (design-curator agent)

**Inputs**:

- `iteration_N/reflection_N.json`.
- Workspace `skillbook.md`.

**Operations**:

- ADD: new strategies surfaced by the Reflector.
- UPDATE: existing strategy text refined by iteration evidence.
- TAG: classify strategies as helpful, incrementing H by 1, or harmful, marking them for retirement.
- REMOVE: retire harmful strategies that have no remediation.
- PROTECT: promote strategies with H of 5 or more and Harm = 0 to `[PROTECTED]`.

**Store the skills**: after every Curator cycle, save each new or updated skill as a separate entry in the local skillbook. If using a persistent memory store, mirror each entry there with generic tags such as `ace-curator`, `site-build`, and `webdev`. Keep one entry per skill, and retain only reusable patterns.

**Outputs**:

- Updated `05_automations/client-site-first-build/skillbook.md`.
- A Curator log entry appended to the current iteration's `change_log.jsonl`.

## Iteration Convergence Pattern (empirical)

Use the reflection evidence to determine what needs work. This progression is a planning aid, not a measured score forecast or a reason to skip checks.

| Iteration | Review Focus | What Tends To Be Wrong |
|-----------|--------------|-----------------------|
| Initial pass | Structure | Component boundaries, token organization, missing AEO schemas |
| Correction pass | P-list fixes | axe violations, contrast issues, missing schemas, build warnings |
| Final verification | Acceptance evidence | Heading order, dynamic-state contrast, incomplete or failed checks |

Allow time for corrections and verification. A build that meets every acceptance condition can stop immediately; a planned number of iterations never establishes quality by itself.

## Escalation Paths

### MAX_ITERATIONS reached

After 5 iterations without SATISFACTORY:

1. Halt the loop.
2. Summarize all 5 reflection P-lists for the person responsible for the site.
3. Identify the dimensions consistently below threshold.
4. Ask whether to accept the current state with a documented sub-9.8 exception, provide additional design guidance for a sixth attempt, or revisit the original handoff because its inputs may be incomplete. An exception must not be labeled SATISFACTORY.

### STALLED detected

After 2 consecutive iterations with no improvement of 0.1 or more:

1. Halt the loop.
2. Identify what the Reflector keeps flagging that the Generator keeps missing.
3. Check whether the P-list lacks specific instructions or the skillbook lacks a needed strategy.
4. Add concrete human guidance or a new strategy to the skillbook, then rerun.

### False-SATISFACTORY caught

If any reviewer catches a SATISFACTORY decision below 9.8 or without all required evidence, reopen the loop. Run the missing empirical checks. If they fail, rerun the Generator using specific corrections in the P-list. The threshold is hard.
