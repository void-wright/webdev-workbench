# Appendix: Old Website Archive

> Use after backlink discovery and again after redirect verification. Runs ONLY when `IS_SITE_PORT == true`. Defines a persistent archive convention for each site.

## Purpose

All backlink-discovery and redirect-authoring artifacts MUST be archived in a durable, site-specific location outside the repository and temporary build directory. The archive must survive build-folder cleanup and serve as the canonical reference for:

- Future redirect adjustments during maintenance
- Later migrations, using the recorded evidence to verify decisions
- Investigating broken links reported by external referrers months later
- Improving migration guidance with lessons from review and maintenance

## Folder Layout (canonical, the same for every site)

The following are generated archive artifacts defined by this appendix, not files supplied with the workbench. Choose an archive root on storage you retain and back up.

```text
<archive-root>/<site-slug>/
├── README.md                          (generated overview with contents, dates, and counts)
├── MAPPING_SUMMARY.md                 (human-readable migration digest, template below)
├── discovery/
│   ├── sitemap_urls.json              (sitemap discovery)
│   ├── wayback_urls.json              (Wayback discovery)
│   ├── gsc_backlinks.csv              (site owner's Google Search Console export)
│   ├── cc_own_captures.json            (Common Crawl captures of the old domain)
│   ├── cc_referrers.json              (Common Crawl referrer discovery)
│   ├── github_refs.json               (optional public GitHub references)
│   ├── trade_directory_refs.json      (optional business-directory references)
│   ├── community_guide_refs.json      (optional references from community guides)
│   ├── manual_outreach_list.csv       (site-owner follow-up list)
│   └── legacy_redirect_chains.json    (existing redirect-chain inventory)
├── verification/
│   └── backlinks_verified.json        (verified backlink results)
├── final/
│   └── backlinks_discovered.json      (comprehensive categorized map)
├── redirects/
│   ├── redirects.json                (approved redirect manifest)
│   ├── redirects_review.csv          (redirect review document)
│   ├── mapping_decisions.md           (rationale for non-obvious mappings)
│   ├── redirects_applied.md           (curl test results)
│   └── placed_assets.json            (asset-placement audit trail)
└── handoff/
    └── migration_review_notes.md      (review questions, answers, and lessons)
```

## MAPPING_SUMMARY.md Template

Generate this human-readable digest when creating or refreshing the archive.

```markdown
# <SiteName>: Site Port Mapping Summary

## Port Metadata
- **OLD domain**: <old-domain>
- **NEW stack**: <actual framework, host, and content platform>
- **Build mode**: <WEBSITE_ONLY | RESOURCE_HUB_ONLY | COMBINED>
- **Discovery date**: <YYYY-MM-DD>
- **Discovery scope**: <sources used and optional sources omitted>
- **Skip GSC?**: <yes/no, with reason if yes>
- **Cutover date**: <YYYY-MM-DD or "pending">

## Discovery Totals (A): Own-URL Inventory
- Sitemap: <N> URLs
- Wayback CDX: <M> URLs (deduplicated, <D> new versus sitemap)
- Common Crawl own-domain captures: <X> URLs (deduplicated, <Y> new versus sitemap and Wayback)
- **Combined inventory: <T> unique URLs**

## Discovery Totals (B): Third-Party Referrers
- GSC: <G> referrer pages (or "skipped")
- Common Crawl referrers: <C> pages
- Optional sources used: <source names and counts, or "none">
- **Combined referrer count: <R> unique third-party pages**

## Verification
- Verified URLs: <V>
- Removed (broken or no longer pointing to OLD): <B>

## Categorization
- HIGH-priority redirects (owned URLs with verified third-party backlinks): <H>
- LOW-priority redirects (owned URLs without verified third-party backlinks): <L>
- 410 Gone (intentionally retired content with no suitable replacement): <G410>
- External outreach (references requiring correction by another site): <EO>
- WordPress URL pattern breakdown:
    - Uploaded assets: <U>
    - Numeric permalink queries: <Q>
    - Category and tag archives: <T>
    - RSS feeds: <F>
    - Administration and login routes: <A>
    - Other: <O>

## Redirect Manifest
- Total manifest entries: <R>
- 301 permanent: <R301>
- 302 temporary: <R302>
- 410 Gone: <R410>
- Worker lookup table used because host redirect-file limits were exceeded: <yes/no>

## Asset Placement
- Files placed on Sanity CDN: <S>
- Files placed in the site's public asset directory: <P>
- Files marked 410 because no source copy or suitable replacement was available: <U410>
- Source breakdown: Wayback <SW>, live OLD site <SL>, site owner <SO>

## Curl Test Results
- Total tests: <T>
- Pass: <Tp>
- Failures resolved before cutover: <Tf>
- Skipped pattern rules requiring separate representative tests: <Ts>
- **Pre-cutover preview pass rate: 100% of required tests**
- Cutover remains blocked while required tests fail or required pattern coverage is missing.

## Decisions Worth Knowing
- <Non-obvious mappings, consolidations, or retirement decisions, with rationale>
- <Reference to redirects/mapping_decisions.md for the full explanation>

## External Outreach Items
- <Third-party links requiring correction, including links to assets that could not be recovered>
- These are **site-owner follow-up items**. A redirect can only be applied on a domain the site owner controls.

## Migration Methodology Notes
- <Populate after handoff with review findings and lessons for future migrations>

## Post-Graduation Monitoring
- GSC property on OLD domain: <verified | not verified>
- Watch for 404 trends after cutover; refresh discovery if external referrers report broken links.
- Recommended re-audit cadence: every 6 months for the first year.
```

## Generation Code

Run after discovery and verification, then again after redirect tests pass. The caller supplies the generated summary and overview as Markdown strings. The source directory is a prepared collection of the artifacts named above. Populate it with the approved versions before archiving; do not select a version merely because it is the first matching file.

```python
import shutil
from pathlib import Path


def archive_port_artifacts(
    site_slug,
    source_dir,
    archive_root,
    mapping_summary,
    archive_readme,
):
    """Copy migration evidence into a durable archive outside the build tree."""
    if (
        not site_slug
        or site_slug in {".", ".."}
        or "/" in site_slug
        or "\\" in site_slug
    ):
        raise ValueError("site_slug must be a single directory name")

    source = Path(source_dir).resolve()
    target = (Path(archive_root) / site_slug).resolve()

    if source == target or source in target.parents or target in source.parents:
        raise ValueError("Source and archive directories must be separate")

    artifact_groups = {
        "discovery": (
            "sitemap_urls.json",
            "wayback_urls.json",
            "gsc_backlinks.csv",
            "cc_own_captures.json",
            "cc_referrers.json",
            "github_refs.json",
            "trade_directory_refs.json",
            "community_guide_refs.json",
            "manual_outreach_list.csv",
            "legacy_redirect_chains.json",
        ),
        "verification": ("backlinks_verified.json",),
        "final": ("backlinks_discovered.json",),
        "redirects": (
            "redirects.json",
            "redirects_review.csv",
            "mapping_decisions.md",
            "redirects_applied.md",
            "placed_assets.json",
        ),
        "handoff": ("migration_review_notes.md",),
    }

    copied = []
    missing = []

    for group, filenames in artifact_groups.items():
        destination = target / group
        destination.mkdir(parents=True, exist_ok=True)

        for filename in filenames:
            src = source / filename
            if src.is_file():
                shutil.copy2(src, destination / filename)
                copied.append(f"{group}/{filename}")
            else:
                missing.append(f"{group}/{filename}")

    (target / "MAPPING_SUMMARY.md").write_text(
        mapping_summary, encoding="utf-8"
    )

    inventory = "\n\n## Files Copied in This Run\n\n"
    inventory += "\n".join(f"- {name}" for name in copied) or "- None"
    inventory += "\n\n## Files Not Supplied in This Run\n\n"
    inventory += "\n".join(f"- {name}" for name in missing) or "- None"
    inventory += (
        "\n\nMissing inputs do not remove files retained from an earlier run. "
        "Review omitted sources and confirm that every required artifact "
        "is present before finalizing the archive.\n"
    )

    (target / "README.md").write_text(
        archive_readme.rstrip() + inventory, encoding="utf-8"
    )

    print(f"Archive written to: {target}")
    return target
```

This routine refreshes the working archive during migration. After cutover, preserve the finalized snapshot and record later changes separately.

## When Archive Runs

- **First archive**: After discovery, verification, and categorization complete. Populate the discovery, verification, and final-map sections. The redirect section may still be empty.
- **Second archive**: After redirect application and curl tests pass. Add the approved manifest, review document, mapping rationale, test results, and asset-placement audit. Regenerate the summary with complete counts.
- **Third archive**: After cutover completes. Update the summary's cutover date and monitoring details, then finalize the snapshot.

## Read-Only Discipline

After finalization, archived evidence should remain unchanged. Limit later additions to:

- Dated monitoring records
- A separate archive for a later migration
- Appended migration-review questions, answers, and lessons

If a redirect needs to change after cutover, change the live repository's redirect configuration, not the archived manifest. The archive records what was deployed at the time.

Document later changes in a new timestamped summary, using the generated filename pattern `MAPPING_SUMMARY_<YYYY-MM-DD>.md`. Describe the differences and leave the original summary and evidence intact.

## Why a Persistent Archive Matters

Start a first migration with a manageable scope so the discovery and redirect process can be checked thoroughly. The archive preserves those decisions and their evidence. A later migration can reuse the procedure while verifying its own URLs, assets, and destinations.

For example, a kitchen-equipment maker's resource library may consolidate several older care guides into one current how-to article. Recording the source URLs, replacement page, and mapping rationale makes later maintenance easier without relying on anyone's memory.

If an external referrer reports a broken link months later, search the archived final map to see whether the URL was captured and categorized correctly. If it was, inspect the redirect rule and its current destination. If it was not, investigate the discovery gap and update the migration guidance. Without that record, each investigation has to reconstruct the original decisions.
