# Appendix: Zip Handoff Convention

> To hand off a design, place the Claude Design or custom HTML archive in the site's inputs folder. The build process detects it before markup work begins.

## Convention

Download the design bundle from Claude Design, or assemble a custom HTML bundle from a prior session. The bundle may be a zip or tar archive.

Keep incoming bundles in a work folder outside the site repository. Use a filename ending in `-handoff.zip` for the detection convention below, even when the downloaded archive contains tar data.

The following paths are illustrative working locations created during the build, not files shipped with Voidwright:

```text
work/<site-slug>/inputs/<descriptive-name>-handoff.zip
```

For example, for an invented ceramic studio:

```text
work/pebble-kiln/inputs/Pebble Kiln Website-handoff.zip
```

## Detection

Run this from the directory containing your `work` folder, replacing `<site-slug>` with your site's folder name:

```bash
INPUTS_DIR="$PWD/work/<site-slug>/inputs"
set -- "$INPUTS_DIR"/*-handoff.zip
if [ ! -e "$1" ]; then
  echo "No handoff zip found in $INPUTS_DIR"
  echo "Drop a *-handoff.zip there and re-run."
  exit 1
elif [ "$#" -eq 1 ]; then
  HANDOFF_ZIP="$1"
else
  echo "Multiple handoff zips found:"
  printf '  %s\n' "$@"
  echo "Which one should be used?"   # ask the person; never guess
  exit 2
fi
echo "Using: $HANDOFF_ZIP"
```

The glob form handles filenames with spaces, which parsing `ls` output does not.

## Extraction Workflow

Extract into a separate working directory outside the site repository. Keep raw handoff files out of the source tree so they do not become part of the deployed artifact.

The commands below create an extraction directory and an asset hash manifest for this build:

```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
ACE_DIR="$(dirname "$INPUTS_DIR")/build-work/${TIMESTAMP}"
EXTRACTED="${ACE_DIR}/extracted"

mkdir -p "$EXTRACTED"
cd "$EXTRACTED"

# Detect format and extract:
ARCHIVE_TYPE=$(file -b "$HANDOFF_ZIP")
case "$ARCHIVE_TYPE" in
  *"Zip archive"*)
    unzip -q "$HANDOFF_ZIP"
    ;;
  *"gzip compressed"*)
    tar -xzf "$HANDOFF_ZIP"
    ;;
  *"tar archive"*)
    tar -xf "$HANDOFF_ZIP"
    ;;
  *)
    echo "Unrecognized archive format: $ARCHIVE_TYPE"
    exit 1
    ;;
esac

# Asset hash manifest, per design-input-003.
# python3 works the same on Linux and macOS.
python3 - <<'PY'
import hashlib, json, pathlib
root = pathlib.Path(".")
rows = [{"hash": hashlib.sha256(p.read_bytes()).hexdigest(), "path": str(p)}
        for p in sorted(root.rglob("*")) if p.is_file() and p.name != "_manifest.json"]
pathlib.Path("_manifest.json").write_text(json.dumps(rows, indent=2))
print(len(rows), "assets hashed")
PY

ls -la
```

## README Recital

Before any markup work, open the bundle's README and restate its key instructions. The following command checks two common filenames in the extraction directory:

```bash
cat "${EXTRACTED}/README.md" 2>/dev/null || cat "${EXTRACTED}/README.txt" 2>/dev/null || echo "No README found at these locations: inspect the bundle and flag any missing instructions"
```

If the archive has a wrapper directory or uses another README filename, locate and read that file.

State to the person, paraphrasing:

> The README describes this design intent: Z. Its key instructions are X and Y. It names these assets: A, B, C; these colors: the supplied hex values; and these fonts: the supplied font families.

If the README references an asset, font, or color that is missing from the bundle and has no documented source, halt:

```text
The README mentions [X], but I cannot find it or its source in the bundle. Should I:
(a) wait for you to provide it,
(b) use an agreed placeholder,
(c) follow another approach?
```

This review is deliberately slow. Restating the instructions exposes missing materials and conflicting assumptions before they become implementation decisions.

## Design Token Extraction (per the design-input-004 skill)

Parse the extracted CSS and HTML for design tokens. Run this from the extraction directory. It creates `_design_tokens.json` as a working build artifact:

```python
import re
import json
from pathlib import Path

extracted = Path(".")
all_css = "\n".join(p.read_text(errors="replace") for p in extracted.rglob("*.css"))
all_html = "\n".join(p.read_text(errors="replace") for p in extracted.rglob("*.html"))

# Color tokens (hex)
hex_colors = sorted(set(re.findall(r"#[0-9a-fA-F]{3,8}\b", all_css + all_html)))
# Font families
fonts = sorted(set(re.findall(r"font-family:\s*([^;]+);", all_css)))
# Spacing scale (px-only first pass)
px_values = sorted(set(int(m.group(1)) for m in re.finditer(r"\b(\d+)px\b", all_css)))
# Border-radius values
radii = sorted(set(re.findall(r"border-radius:\s*([^;]+);", all_css)))
# Box-shadow values
shadows = sorted(set(re.findall(r"box-shadow:\s*([^;]+);", all_css)))

tokens = {
  "colors": hex_colors,
  "fonts": fonts,
  "spacing_px": px_values,
  "radii": radii,
  "shadows": shadows,
}
(extracted / "_design_tokens.json").write_text(json.dumps(tokens, indent=2))
```

Review the extracted values against the bundle and README. This is a first pass, so add any tokens expressed in forms the script does not capture.

The reviewed `_design_tokens.json` becomes the source of truth for the initial implementation. Derive Tailwind theme values, CSS custom properties, and component styles from it to preserve the supplied design.

## Anti-Patterns (DON'T do these)

- Extract directly into the site's source tree: this pollutes the deploy artifact with raw handoff files.
- Skip the README recital because "I'll just look at the HTML": this lets handoff inconsistencies become part of the build.
- Hardcode colors or fonts directly in components before recording the design tokens: silent drift accumulates across revisions.
- Fabricate a missing asset: halt and ask how to resolve it.
- Process multiple zips in parallel "just in case": select one, extract once, and stop with a clear message if several candidates exist.
