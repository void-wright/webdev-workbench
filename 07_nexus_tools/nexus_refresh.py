#!/usr/bin/env python3
"""nexus_refresh.py: keep a nexus memory's index matrix CURRENT from the tags in your own Voidloom brain.

A nexus is ONE index memory that sits above a group of related memories (for example everything you know about
WebGL). It holds a hand-written part (learning path, warnings, the why) and an index matrix between two marker lines:

    == SEGMENTED INDEX MATRIX ...
    == END MATRIX ==

This tool never guesses the index. It reads the brain (read-only), finds the member memories by their topic tag,
groups them by the cluster tags in a config file, and regenerates ONLY the block between the markers. Everything
outside the markers is kept byte for byte.

Dry-run by default: it prints the new matrix and what would change, and writes nothing. With --commit it:
  1. updates the nexus content with `claude_memory.py update --id N --content ...` (which re-embeds it);
  2. links every member not yet linked: `claude_memory.py link --source M --target N --type elaborates`.
With --create --commit and no nexus yet, it first stores a new nexus memory (title from the config, the two markers,
tags `anchor:<anchor>` and the topic tag) and then fills it.
The nexus is found by its `anchor:<anchor>` TAG, because memory ids differ from brain to brain and tags do not.

Usage:  python3 nexus_refresh.py --config configs/<name>.json [--commit] [--create] [--db PATH]
Exit:   0 ok, 2 nexus not found, 3 markers missing, 4 a write failed
Config: {"anchor": "...", "topic_tag": "...", "title": "...", "clusters": [{"tag", "theme", "read_when"}, ...]}
"""
import argparse, json, os, sqlite3, subprocess, sys, datetime

BEGIN = "== SEGMENTED INDEX MATRIX"
END = "== END MATRIX =="
HOME = os.path.expanduser("~")
CM = os.environ.get("VOIDLOOM_CM", os.path.join(HOME, ".claude/memory/organs/claude_memory.py"))
def _py():
    """The interpreter that can run claude_memory.py's update (it re-embeds): VOIDLOOM's Tier-1 venv when present."""
    if os.environ.get("VOIDLOOM_PY"):
        return os.environ["VOIDLOOM_PY"]
    for c in (".claude/memory/venv/bin/python", ".claude/memory/.venv/bin/python", ".voidloom/venv/bin/python"):
        if os.path.exists(os.path.join(HOME, c)):
            return os.path.join(HOME, c)
    return sys.executable

def ro(db):
    return sqlite3.connect(f"file:{db}?mode=ro", uri=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--commit", action="store_true")
    ap.add_argument("--create", action="store_true", help="with --commit: store the nexus first when it does not exist")
    ap.add_argument("--db", default=os.environ.get("WIZARD_LIBRARY_DB", os.path.join(HOME, ".claude/memory/claude_memory.db")))
    a = ap.parse_args()
    cfg = json.load(open(a.config))
    conn = ro(a.db)
    row = conn.execute(
        "SELECT m.id, m.content FROM memories m JOIN memory_tags t ON t.memory_id=m.id "
        "WHERE t.tag=? AND m.is_archived=0 ORDER BY m.id DESC LIMIT 1", (f"anchor:{cfg['anchor']}",)).fetchone()
    if not row and a.create and a.commit:
        conn.close()
        title = cfg.get("title") or f"Nexus: {cfg['topic_tag']}"
        seed = (f"{title}. Index of every memory tagged '{cfg['topic_tag']}', grouped by theme. "
                f"Read the matrix to find the right cluster, then recall by its tag.\n\n{BEGIN} ==\n{END}\n")
        r = subprocess.run([_py(), CM, "store", "--content", seed, "--category", "project_knowledge",
                            "--summary", title, "--importance", "0.8",
                            "--tags", f"anchor:{cfg['anchor']},nexus,{cfg['topic_tag']}"],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print(f"CREATE FAILED rc={r.returncode}: {r.stderr[-400:]}")
            return 4
        print(f"CREATED nexus for anchor:{cfg['anchor']}")
        conn = ro(a.db)
        row = conn.execute(
            "SELECT m.id, m.content FROM memories m JOIN memory_tags t ON t.memory_id=m.id "
            "WHERE t.tag=? AND m.is_archived=0 ORDER BY m.id DESC LIMIT 1", (f"anchor:{cfg['anchor']}",)).fetchone()
    if not row:
        print(f"NEXUS NOT FOUND for anchor:{cfg['anchor']}. Create it with --create --commit "
              f"(or store a memory tagged anchor:{cfg['anchor']} whose content holds the two matrix marker lines).")
        return 2
    nid, content = row
    if BEGIN not in content or END not in content:
        print(f"MARKERS MISSING in nexus #{nid}: need a line starting '{BEGIN}' and a line '{END}'.")
        return 3
    members = conn.execute(
        "SELECT DISTINCT m.id FROM memories m JOIN memory_tags t ON t.memory_id=m.id "
        "WHERE t.tag=? AND m.is_archived=0 AND m.id<>? ORDER BY m.id", (cfg["topic_tag"], nid)).fetchall()
    member_ids = [r[0] for r in members]
    tags_by_id = {}
    for mid in member_ids:
        tags_by_id[mid] = {r[0] for r in conn.execute("SELECT tag FROM memory_tags WHERE memory_id=?", (mid,))}
    lines = [f"{BEGIN} (auto, regenerated by nexus_refresh.py; derived "
             f"{datetime.date.today().isoformat()}; members tagged '{cfg['topic_tag']}' = {len(member_ids)}) ==",
             "| theme | recall TAG (durable key) | count | ids (this brain only) | read this when |",
             "|---|---|---|---|---|"]
    mapped = set()
    for c in cfg["clusters"]:
        ids = [i for i in member_ids if c["tag"] in tags_by_id[i]]
        mapped.update(ids)
        rng = f"#{min(ids)}–#{max(ids)}" if ids else "-"
        lines.append(f"| {c['theme']} | {c['tag']} | {len(ids)} | {rng} | {c['read_when']} |")
    unmapped = [i for i in member_ids if i not in mapped]
    if unmapped:
        lines.append(f"| UNMAPPED (add a cluster row or tag them) | {cfg['topic_tag']} | {len(unmapped)} | "
                     f"{', '.join('#'+str(i) for i in unmapped[:20])}{' …' if len(unmapped) > 20 else ''} | triage on next refresh |")
    lines.append(END)
    new_block = "\n".join(lines)
    pre, rest = content.split(BEGIN, 1)
    _, post = rest.split(END, 1)
    new_content = pre + new_block + post
    linked = {r[0] for r in conn.execute(
        "SELECT source_id FROM memory_links WHERE target_id=? AND link_type='elaborates'", (nid,))}
    to_link = [i for i in member_ids if i not in linked]
    conn.close()
    changed = new_content != content
    print(f"nexus #{nid} anchor:{cfg['anchor']} members={len(member_ids)} unmapped={len(unmapped)} "
          f"content_changed={changed} links_missing={len(to_link)}")
    print(new_block)
    if not a.commit:
        print("DRY-RUN: nothing written. Re-run with --commit to update the nexus and link members.")
        return 0
    if changed:
        r = subprocess.run([_py(), CM, "update", "--id", str(nid), "--content", new_content],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print(f"UPDATE FAILED rc={r.returncode}: {r.stderr[-400:]}")
            return 4
        print(f"UPDATED nexus #{nid}")
    failed = 0
    for mid in to_link:
        r = subprocess.run([_py(), CM, "link", "--source", str(mid), "--target", str(nid),
                            "--type", "elaborates", "--strength", "0.8"], capture_output=True, text=True)
        if r.returncode != 0:
            failed += 1
    print(f"LINKED {len(to_link) - failed} of {len(to_link)} missing members → #{nid}")
    return 4 if failed else 0

if __name__ == "__main__":
    sys.exit(main())
