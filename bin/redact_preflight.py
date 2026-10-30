#!/usr/bin/env python3
"""redact_preflight.py: make a shareable copy of preflight.json, with your home folder and user name hidden. (bin/.)

    python3 bin/redact_preflight.py preflight.json preflight_to_send.json

It PARSES the JSON and rewrites every decoded string (keys included): the recipient's home folder becomes "~" and their
user name, where it appears as a path segment, becomes "<user>". It never does a text replace over the file: the
preflight writer escapes non-ASCII characters (json.dump's default), so a home like /home/josé is stored as
/home/jos\\u00e9 and a text replace misses it.
It prints how many strings changed and the output path, never a value. Standard library only; Python 3.8+.

    python3 bin/redact_preflight.py --selftest
Exit 0 written; 1 the input does not parse (nothing written); 2 usage.
"""
import getpass
import json
import os
import re
import sys


def redactor(home, user):
    home = home.rstrip('/') or home
    seg = re.compile(r'(?<=[/\\])' + re.escape(user) + r'(?=[/\\]|$)') if user else None

    def red(s):
        t = s
        if home and home != '/':
            t = t.replace(home, '~')
        if seg is not None:
            t = seg.sub('<user>', t)
        return t
    return red


def walk(o, red, n):
    if isinstance(o, dict):
        return {red(k) if isinstance(k, str) else k: walk(v, red, n) for k, v in o.items()}
    if isinstance(o, list):
        return [walk(v, red, n) for v in o]
    if isinstance(o, str):
        r = red(o)
        if r != o:
            n[0] += 1
        return r
    return o


def redact_file(src, dst, home=None, user=None):
    try:
        doc = json.load(open(src, encoding='utf-8'))
    except (OSError, ValueError) as e:
        print(f'STOP: {src} does not parse as JSON ({e.__class__.__name__}); nothing written')
        return 1
    n = [0]
    out = walk(doc, redactor(home or os.path.expanduser('~'), user or getpass.getuser()), n)
    json.dump(out, open(dst, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print(f'redacted {n[0]} string(s); wrote {dst}. Glance through it before you send it.')
    return 0


def selftest():
    import tempfile
    d = tempfile.mkdtemp(prefix='redact_preflight_', dir=os.path.expanduser('~/.cache') if os.path.isdir(os.path.expanduser('~/.cache')) else None)
    home, user = '/home/josé', 'josé'
    src = os.path.join(d, 'preflight.json'); dst = os.path.join(d, 'out.json')
    doc = {'package': home + '/voidloom_pkg', 'python': home + '/miniforge3/bin/python3', 'cwd': '/srv/x/josé/y',
           'note': 'josé likes tea', 'cpu': 8, 'nested': {home + '/k': [home]}}
    json.dump(doc, open(src, 'w'))               # ensure_ascii=True: the writer's own escaping
    raw = open(src).read()
    bad = 0
    ok = '\\u00e9' in raw and raw.replace(home, '~') == raw
    bad += not ok
    print(('OK   ' if ok else 'FAIL ') + 'control: the file stores /home/jos\\u00e9 escaped, so a text replace changes nothing')
    rc = redact_file(src, dst, home, user)
    got = json.load(open(dst))
    want = {'package': '~/voidloom_pkg', 'python': '~/miniforge3/bin/python3', 'cwd': '/srv/x/<user>/y',
            'note': 'josé likes tea', 'cpu': 8, 'nested': {'~/k': ['~']}}
    ok = rc == 0 and got == want
    bad += not ok
    print(('OK   ' if ok else 'FAIL ') + f'exact expected output after parsing (a user name that is not a path segment stays): {got}')
    open(src, 'w').write('{"broken": ')
    rc = redact_file(src, os.path.join(d, 'none.json'), home, user)
    ok = rc == 1 and not os.path.exists(os.path.join(d, 'none.json'))
    bad += not ok
    print(('OK   ' if ok else 'FAIL ') + 'an unparseable input writes nothing')
    import shutil
    shutil.rmtree(d, ignore_errors=True)
    print(f'3 cases, {bad} failures')
    return 1 if bad else 0


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--selftest']:
        sys.exit(selftest())
    if len(a) != 2:
        print(__doc__); sys.exit(2)
    sys.exit(redact_file(a[0], a[1]))
