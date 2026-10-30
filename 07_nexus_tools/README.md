# Nexus tools

A **nexus** is one index memory in your Voidloom brain that sits above a group of related memories and tells you
which tag to recall for which need. `nexus_refresh.py` keeps its index matrix in step with the tags actually in your
brain, so the map never drifts from the territory.

After `bash bin/install_skills.sh` this folder lives in `~/.local/share/webdev-workbench/nexus_tools/`.

```bash
# 1. First time only: create the nexus memory and fill it.
#    On a brain with no nexus yet, a run without --create --commit stops with exit 2 (NEXUS NOT FOUND).
python3 ~/.local/share/webdev-workbench/nexus_tools/nexus_refresh.py --config ~/.local/share/webdev-workbench/nexus_tools/configs/webgl.json --create --commit

# 2. Any time later: preview what a refresh would change (reads the brain, writes nothing)
python3 ~/.local/share/webdev-workbench/nexus_tools/nexus_refresh.py --config ~/.local/share/webdev-workbench/nexus_tools/configs/webgl.json

# 3. After you have stored more memories on the topic: apply the refresh
python3 ~/.local/share/webdev-workbench/nexus_tools/nexus_refresh.py --config ~/.local/share/webdev-workbench/nexus_tools/configs/webgl.json --commit
```

Then recall it with `voidloom recall --query "WebGL craft nexus" --top-k 5`.

| Config | Members | Rows |
|---|---|---|
| `configs/webgl.json` | memories tagged `webgl` | performance, testing, progressive enhancement, accessibility, interaction, compositing, visualization, art direction |
| `configs/scroll-journey.json` | memories tagged `scroll` | performance, accessibility, contrast, responsive design |

A config is plain JSON: `anchor` (the nexus's own tag, stored as `anchor:<anchor>`), `topic_tag` (which memories are
members), `title`, and `clusters` (one row per `tag`, with a `theme` and a `read_when`). Members carrying none of the
row tags appear in an **UNMAPPED** row: add a row for them, or tag them. Copy a config to make a nexus for any topic.

What it needs: Voidloom installed (it reads `~/.claude/memory/claude_memory.db` read-only, or `--db PATH`, and writes
only through Voidloom's own `claude_memory.py store`, `update` and `link`). Exit codes: 0 ok, 2 nexus not found,
3 markers missing, 4 a write failed.
