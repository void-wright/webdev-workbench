#!/usr/bin/env python3
"""forms-check: look after the form submissions your site stores in a Cloudflare D1 database.

Run it from your site's repository folder (where your wrangler config names the D1 database), through the shim:

  bash forms-check --db <your-d1-db> tables                  every table and its row count
  bash forms-check --db <your-d1-db> summary                 row counts, plus last 7 / 30 days where a created_at column exists
  bash forms-check --db <your-d1-db> list <table> [-n 20]    newest rows of one table (cells cut to 48 characters)
  bash forms-check --db <your-d1-db> export [DIR]            every table as a CSV file (folder mode 700, files mode 600)
  bash forms-check --db <your-d1-db> delete-email <address> [--yes]
                                                            a privacy request: count, then (with --yes) delete, every row
                                                            whose `email` column matches, in every table that has one
Options: --local queries your local development copy instead of the remote database.

It runs `wrangler d1 execute <db> --remote --json --command <SQL>` through wrangler-safe (same folder), so it uses YOUR
account from ~/.config/webtools/keys.env. These rows are real visitors' data: read them only when you need to, and keep
exports out of your repository. delete-email only reaches tables that have an `email` column; rows in other tables
that point at a deleted row (for example by an id) are listed for you to handle, not deleted.
Exit codes: 0 done, 1 a query failed, 64 usage.
"""
import csv
import datetime
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IDENT = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
EMAIL = re.compile(r"^[^\s@'\"\;]+@[^\s@'\"\;]+\.[^\s@'\"\;]{2,}$")
SKIP = ('sqlite_', '_cf_', 'd1_')


def usage(msg=None):
    if msg:
        sys.stderr.write('forms-check: ' + msg + '\n\n')
    print(__doc__)
    sys.exit(64)


def make_query(db, local):
    def q(sql):
        cmd = ['bash', os.path.join(HERE, 'wrangler-safe'), 'd1', 'execute', db,
               '--local' if local else '--remote', '--json', '--command', sql]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            sys.stderr.write('forms-check: query failed (wrangler exit %d)\n%s\n' % (r.returncode, r.stderr[-800:]))
            sys.exit(1)
        try:
            return json.loads(r.stdout)[0]['results']
        except (ValueError, KeyError, IndexError):
            sys.stderr.write('forms-check: could not read wrangler output\n%s\n' % r.stdout[-800:])
            sys.exit(1)
    return q


def tables(q):
    names = [r['name'] for r in q("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    return [n for n in names if IDENT.match(n) and not n.startswith(SKIP)]


def columns(q, t):
    return [r['name'] for r in q('PRAGMA table_info("%s")' % t)]


def show(rows, cols=None):
    if not rows:
        print('  (none)')
        return
    cols = cols or list(rows[0].keys())
    cell = lambda v: ('-' if v is None else str(v)).replace('\n', ' ')[:48]
    w = {c: max(len(c), *(len(cell(r.get(c))) for r in rows)) for c in cols}
    print('  ' + '  '.join(c.ljust(w[c]) for c in cols))
    for r in rows:
        print('  ' + '  '.join(cell(r.get(c)).ljust(w[c]) for c in cols))


def main():
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help', 'help'):
        usage()
    local = '--local' in args
    args = [a for a in args if a != '--local']
    if '--db' not in args or args.index('--db') + 1 >= len(args):
        usage('--db <your-d1-db> is required')
    i = args.index('--db')
    db = args[i + 1]
    del args[i:i + 2]
    if not re.match(r'^[A-Za-z0-9_-]+$', db):
        usage('the database name may contain only letters, digits, - and _')
    if not args:
        usage('no command given')
    cmd, rest = args[0], args[1:]
    q = make_query(db, local)

    if cmd == 'tables':
        show([{'table': t, 'rows': q('SELECT COUNT(*) AS n FROM "%s"' % t)[0]['n']} for t in tables(q)])
    elif cmd == 'summary':
        out = []
        for t in tables(q):
            if 'created_at' in columns(q, t):
                r = q("SELECT COUNT(*) AS n, SUM(created_at >= datetime('now','-7 days')) AS d7, "
                      "SUM(created_at >= datetime('now','-30 days')) AS d30 FROM \"%s\"" % t)[0]
                out.append({'table': t, 'total': r['n'], 'last 7 days': r['d7'] or 0, 'last 30 days': r['d30'] or 0})
            else:
                out.append({'table': t, 'total': q('SELECT COUNT(*) AS n FROM "%s"' % t)[0]['n'],
                            'last 7 days': '-', 'last 30 days': '-'})
        show(out)
    elif cmd == 'list':
        if not rest or rest[0] not in tables(q):
            usage('list needs one of these tables: ' + ', '.join(tables(q)))
        t = rest[0]
        n = int(rest[rest.index('-n') + 1]) if '-n' in rest else 20
        order = 'created_at DESC' if 'created_at' in columns(q, t) else 'rowid DESC'
        show(q('SELECT * FROM "%s" ORDER BY %s LIMIT %d' % (t, order, max(1, min(n, 500)))))
    elif cmd == 'export':
        out = rest[0] if rest and not rest[0].startswith('-') else '%s-export-%s' % (db, datetime.date.today().isoformat())
        os.makedirs(out, exist_ok=True)
        os.chmod(out, 0o700)
        for t in tables(q):
            rows = q('SELECT * FROM "%s"' % t)
            path = os.path.join(out, t + '.csv')
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
            with os.fdopen(fd, 'w', newline='') as fh:
                if rows:
                    wr = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
                    wr.writeheader()
                    wr.writerows(rows)
            os.chmod(path, 0o600)
            print('%s  (%d rows)' % (path, len(rows)))
        print('Keep this folder out of your repository and delete it when you are done.')
    elif cmd == 'delete-email':
        if not rest or not EMAIL.match(rest[0]):
            usage('delete-email needs one valid email address')
        e = rest[0].lower()
        with_email, without = [], []
        for t in tables(q):
            cols = [c for c in columns(q, t) if c.lower() == 'email']
            (with_email if cols else without).append((t, cols[0] if cols else None))
        total = 0
        for t, c in with_email:
            n = q('SELECT COUNT(*) AS n FROM "%s" WHERE lower("%s") = \'%s\'' % (t, c, e))[0]['n']
            total += n
            print('%-32s %d row(s)' % (t, n))
        if without:
            print('Tables without an email column (check them for rows linked to this person): '
                  + ', '.join(t for t, _ in without))
        if '--yes' not in rest:
            print('Nothing deleted. Run again with --yes to delete the %d row(s) above.' % total)
            return
        for t, c in with_email:
            q('DELETE FROM "%s" WHERE lower("%s") = \'%s\'' % (t, c, e))
        print('Deleted %d row(s).' % total)
    else:
        usage('unknown command %r' % cmd)


if __name__ == '__main__':
    main()
