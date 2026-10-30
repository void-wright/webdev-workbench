#!/usr/bin/env python3
"""Recall battery: proves a memory pack is findable BY SEARCH in this brain. (SHIPS INSIDE A PACKAGE as 02_memory/run_battery.py.)

For each {"phrase", "expect_anchor"} in recall_battery.json (next to this file) it runs ONE batched
`voidloom batch-recall` over every phrase, then checks that a memory carrying `anchor:<expect_anchor>` (as a tag, or
inside its content when the brain's consolidation moved the anchor there) is in the top K results for its phrase.
Prints PASS/FAIL per phrase and a TOTAL line. Read-only on the brain file (the recall itself is VOIDLOOM's own).

Usage: run_battery.py [--top-k 5] [--battery FILE] [--db PATH] [--min-rate 0.95] [--gate-tier0]
Exit:  0  at least --min-rate of the phrases found their memory at Tier 1 on a FULLY embedded brain (or Tier 0 without
          --gate-tier0: informational, no anchor missing)
       1  below --min-rate at the gated tier; an expected anchor is missing (load the pack first); or Tier 1 while ANY
          memory lacks a vector or the count is unknown (never a Tier-1 PASS on keyword evidence)
       2  voidloom could not run, or the brain voidloom recalls from is not --db (ids from two brains are never compared)
Tier 1 (semantic, after embed_backfill) GATES. Tier 0 (keyword) prints its numbers as information, unless
--gate-tier0 is given (use it when the recipient may stay on Tier 0). Tier 0 matches every word of a phrase, so long
natural phrases often return nothing there. Re-run the battery after ANY change to the pack (its sha changes).
"""
import argparse
import json
import os
import re
import sqlite3
import subprocess
import sys

sys.dont_write_bytecode = True
# No device handling here: Voidloom's own device chooser (from your install answers) decides; this script never forces a device.


def meta(db, key):
    try:
        r = db.execute('SELECT value FROM metadata WHERE key=?', (key,)).fetchone()
        return r[0] if r else None
    except sqlite3.Error:
        return None


def anchor_ids(db, anchor):
    tag = 'anchor:' + anchor
    rows = db.execute('SELECT m.id FROM memory_tags t JOIN memories m ON m.id = t.memory_id '
                      'WHERE t.tag = ? AND m.is_archived = 0', (tag,)).fetchall()
    if rows:
        return {r[0] for r in rows}
    rx = re.compile(re.escape(tag) + r'(?![A-Za-z0-9_])')
    cand = db.execute("SELECT id, content FROM memories WHERE is_archived = 0 AND content LIKE ?", ('%' + tag + '%',)).fetchall()
    return {i for i, c in cand if rx.search(c or '')}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--top-k', type=int, default=5)
    ap.add_argument('--battery', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recall_battery.json'))
    ap.add_argument('--db', default=os.environ.get('WIZARD_LIBRARY_DB', os.path.expanduser('~/.claude/memory/claude_memory.db')))
    ap.add_argument('--min-rate', type=float, default=0.95)
    ap.add_argument('--gate-tier0', action='store_true')
    a = ap.parse_args(argv)
    bat = json.load(open(a.battery, encoding='utf-8'))
    items = bat['items'] if isinstance(bat, dict) else bat
    db = sqlite3.connect(f'file:{a.db}?mode=ro', uri=True)
    table, t0only = meta(db, 'active_embedding_table'), meta(db, 'tier0_only')
    tier = 0 if (not table or (t0only or '').lower() in ('1', 'true', 'yes')) else 1
    want = [anchor_ids(db, b['expect_anchor']) for b in items]
    missing = sum(1 for w in want if not w)
    unembedded = None
    if tier == 1:
        try:
            unembedded = db.execute(f'SELECT COUNT(*) FROM memories m WHERE m.is_archived = 0 AND m.id NOT IN '
                                    f'(SELECT id FROM "{table}_rowids")').fetchone()[0]
        except sqlite3.Error:
            unembedded = None
    print(f'brain: {a.db} | tier {tier}' + (f' ({table}; memories without a vector: {unembedded})' if tier else ' (keyword-only)'))
    if missing:
        print(f'{missing} expected anchors are not in this brain: load the pack first.')
    # the ids compared must come from the brain the anchors were resolved in: point voidloom at --db, and prove it.
    env = dict(os.environ, WIZARD_LIBRARY_DB=a.db)
    try:
        d = subprocess.run(['voidloom', 'doctor', '--json'], capture_output=True, text=True, env=env)
        recall_db = json.loads(d.stdout)['data']['checks']['db_path']
    except (OSError, ValueError, KeyError, TypeError):
        print('voidloom doctor did not run or did not name its database: cannot prove which brain recall reads')
        return 2
    if os.path.realpath(os.path.expanduser(recall_db)) != os.path.realpath(a.db):
        print(f'STOP: recall brain {recall_db} is not --db {a.db}; the ids would come from two different brains')
        return 2
    phrases = sorted({b['phrase'] for b in items})
    try:
        p = subprocess.run(['voidloom', 'batch-recall', '--items', '-', '--top-k', str(a.top_k), '--json'],
                           input=json.dumps(phrases), capture_output=True, text=True, env=env)
    except OSError:
        print('voidloom batch-recall could not run')
        return 2
    try:
        out = json.loads(p.stdout)
    except ValueError:
        print(f'voidloom batch-recall did not return JSON (rc {p.returncode}); see its stderr above this line in a terminal')
        return 2
    res = {r.get('query'): [m.get('id') or m.get('memory_id') for m in r.get('results', [])]
           for r in out.get('data', {}).get('results', [])}
    ok = 0
    for b, w in zip(items, want):
        got = res.get(b['phrase'], [])
        hit = bool(w) and any(x in w for x in got)
        ok += hit
        print(('PASS' if hit else 'FAIL') + f"  {b['phrase']!r} -> {b['expect_anchor']}"
              + ('' if hit else f"  (in brain: {bool(w)}; got {len(got)} results)"))
    rate = ok / max(1, len(items))
    print(f'TOTAL {ok}/{len(items)} = {rate:.1%} (top-{a.top_k}, tier {tier})')
    if tier == 0 and not a.gate_tier0:
        print('Tier 0: informational only. Upgrade to Tier 1, embed the pack, then re-run.')
        return 1 if missing else 0
    if tier == 1 and (unembedded is None or unembedded > 0):
        print(f'FAIL: tier 1 gates only on a fully embedded brain (memories without a vector: {unembedded}); '
              'run embed_backfill.py, then re-run')
        return 1
    return 0 if rate >= a.min_rate and not missing else 1


def selftest():
    """A synthetic brain + a stub `voidloom` first on PATH (doctor names $WIZARD_LIBRARY_DB unless STUB_OTHER_BRAIN is set).
    States enumerated from main()'s branches: tag + content anchors at Tier 1 fully embedded (0);
    a missing anchor (1); Tier 1 with one memory unembedded (1, the positive control) and the same brain embedded
    (0); recall reading another brain (2); voidloom absent (2); Tier 0 informational (0); Tier 0 with --gate-tier0 (1)."""
    import shutil
    base = os.path.join(os.environ.get('BATTERY_SELFTEST_DIR', os.path.expanduser('~/.cache/run_battery_selftest')), f'run_battery_{os.getpid()}')
    shutil.rmtree(base, ignore_errors=True); os.makedirs(os.path.join(base, 'bin'))
    db = os.path.join(base, 'brain.db')
    c = sqlite3.connect(db)
    c.executescript("CREATE TABLE memories (id INTEGER PRIMARY KEY, content TEXT, is_archived INTEGER DEFAULT 0);"
                    "CREATE TABLE memory_tags (id INTEGER PRIMARY KEY, memory_id INTEGER, tag TEXT);"
                    "CREATE TABLE metadata (key TEXT, value TEXT); CREATE TABLE vt_rowids (id INTEGER);"
                    "INSERT INTO memories VALUES (1, 'tagged', 0); INSERT INTO memory_tags (memory_id, tag) VALUES (1, 'anchor:seed_t_a_001');"
                    "INSERT INTO memories VALUES (2, '[OBJECTIVE] anchor:seed_t_a_002 merged', 0);"
                    "INSERT INTO metadata VALUES ('active_embedding_table', 'vt'); INSERT INTO vt_rowids VALUES (1), (2);")
    c.commit(); c.close()
    stub = os.path.join(base, 'bin', 'voidloom')
    open(stub, 'w').write('#!/usr/bin/env python3\nimport json,os,sys\n'
                          'if sys.argv[1] == "doctor":\n'
                          '    print(json.dumps({"data":{"checks":{"db_path": os.environ.get("STUB_OTHER_BRAIN") or os.environ.get("WIZARD_LIBRARY_DB","")}}})); sys.exit(0)\n'
                          'q=json.load(sys.stdin)\n'
                          'm={"phrase one":[1,9],"phrase two":[7,2],"phrase three":[5]}\n'
                          'print(json.dumps({"data":{"results":[{"query":x,"results":[{"id":i} for i in m.get(x,[])]} for x in q]}}))\n')
    os.chmod(stub, 0o755)
    path0 = os.environ['PATH']
    os.environ['PATH'] = os.path.join(base, 'bin') + os.pathsep + path0
    b1 = os.path.join(base, 'b1.json')
    json.dump({'items': [{'phrase': 'phrase one', 'expect_anchor': 'seed_t_a_001'}, {'phrase': 'phrase two', 'expect_anchor': 'seed_t_a_002'}]}, open(b1, 'w'))
    b2 = os.path.join(base, 'b2.json')
    json.dump({'items': [{'phrase': 'phrase one', 'expect_anchor': 'seed_t_a_001'}, {'phrase': 'phrase three', 'expect_anchor': 'seed_t_a_009'}]}, open(b2, 'w'))
    bad = 0
    rows = []

    def case(name, args, want):
        nonlocal bad
        rc = main(args)
        ok = rc == want; bad += not ok
        rows.append(('OK   ' if ok else 'FAIL ') + f'{name}: rc {rc} (want {want})')
    case('Tier 1, fully embedded, tag + content (consolidated) anchors', ['--battery', b1, '--db', db], 0)
    case('a missing anchor fails the gate', ['--battery', b2, '--db', db, '--min-rate', '0.5'], 1)
    c = sqlite3.connect(db); c.execute('DELETE FROM vt_rowids WHERE id = 2'); c.commit(); c.close()
    case('positive control: Tier 1 with one memory WITHOUT a vector fails even at 100%', ['--battery', b1, '--db', db], 1)
    c = sqlite3.connect(db); c.execute('INSERT INTO vt_rowids VALUES (2)'); c.commit(); c.close()
    case('the same brain, embedded again, passes', ['--battery', b1, '--db', db], 0)
    os.environ['STUB_OTHER_BRAIN'] = '/home/someone/.claude/memory/claude_memory.db'
    case('recall reads a different brain than --db -> STOP', ['--battery', b1, '--db', db], 2)
    del os.environ['STUB_OTHER_BRAIN']
    os.environ['PATH'] = '/usr/bin:/bin'
    case('voidloom absent -> cannot run', ['--battery', b1, '--db', db], 2)
    os.environ['PATH'] = os.path.join(base, 'bin') + os.pathsep + path0
    c = sqlite3.connect(db); c.execute("DELETE FROM metadata"); c.commit(); c.close()
    case('Tier 0 is informational', ['--battery', b1, '--db', db], 0)
    json.dump({'items': [{'phrase': 'phrase three', 'expect_anchor': 'seed_t_a_001'}]}, open(b2, 'w'))
    case('--gate-tier0 gates a Tier-0 brain', ['--battery', b2, '--db', db, '--gate-tier0'], 1)
    os.environ['PATH'] = path0
    print('\n'.join(rows))
    print(f'{len(rows)} cases (enumerated from main() branches: 8), {bad} failures')
    return 1 if bad else 0


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    sys.exit(main())
