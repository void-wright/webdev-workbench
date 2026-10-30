#!/usr/bin/env python3
"""builds_watch.py: watch Cloudflare Workers Builds for one commit until its builds finish (READ-ONLY).

Usage:
  python3 builds_watch.py --worker <your-worker> --commit <sha> [--branch <branch>] [--max-seconds 480]

  --worker       the Worker's name as shown in the Cloudflare dashboard (Workers & Pages)
  --commit       the commit you pushed; the first 7 characters are enough
  --branch       pass it when the same commit was pushed to two branches (for example main and preview);
                 otherwise a finished build on the other branch can end the watch early
  --max-seconds  give up after this many seconds (default 480)

Keys read from ~/.config/webtools/keys.env (parsed, never printed): CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID.
The token needs two account permission rows in Cloudflare's token editor: Workers Scripts (Read or Edit; used to
find the Worker's tag) and Workers Builds Configuration > Edit (Cloudflare's Builds API reference names Edit for the
Builds API; this tool only reads). Create the token under My Profile > API Tokens: the Builds API does not accept
account-owned tokens. Permission names, API paths and field names are as of October 2026; re-check before relying on them.

Prints one line each time a build's state changes, with the full build uuid (use it with cf-api to read that
build's logs). Exit codes: 0 every matching build succeeded, 1 a build failed,
2 timeout (or no build for that commit appeared), 3 the Worker was not found, 4 an API call failed.
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from webtools_keys import load_keys, require  # noqa: E402

API = 'https://api.cloudflare.com/client/v4'


def main():
    ap = argparse.ArgumentParser(description='Watch Workers Builds for one commit (read-only).')
    ap.add_argument('--worker', required=True)
    ap.add_argument('--commit', required=True)
    ap.add_argument('--branch', default=None)
    ap.add_argument('--max-seconds', type=int, default=480)
    a = ap.parse_args()

    keys = load_keys()
    token, account = require(keys, 'CLOUDFLARE_API_TOKEN'), require(keys, 'CLOUDFLARE_ACCOUNT_ID')

    def get(path):
        req = urllib.request.Request(API + path, headers={'Authorization': 'Bearer ' + token})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode('utf-8'))
        except (urllib.error.URLError, ValueError) as e:
            code = getattr(e, 'code', '')
            print('API call failed %s %s' % (path.split('?')[0], code), file=sys.stderr)
            sys.exit(4)

    scripts = get('/accounts/%s/workers/scripts' % account).get('result') or []
    tags = [s.get('tag') for s in scripts if s.get('id') == a.worker]
    if not tags:
        print('Worker %r not found in this account. Check the name in the dashboard.' % a.worker, file=sys.stderr)
        return 3
    tag = tags[0]

    t0, last = time.time(), {}
    while time.time() - t0 < a.max_seconds:
        res = get('/accounts/%s/builds/workers/%s/builds?per_page=10' % (account, tag)).get('result') or []
        builds = []
        for b in res:
            meta = b.get('build_trigger_metadata') or {}
            if not (meta.get('commit_hash') or '').startswith(a.commit):
                continue
            if a.branch is not None and meta.get('branch') != a.branch:
                continue
            builds.append(b)
        for b in builds:
            k = b.get('build_uuid', '?')
            st = (b.get('status'), b.get('build_outcome'))
            if last.get(k) != st:
                print('%4ds build %s branch=%-10s status=%s outcome=%s' % (
                    time.time() - t0, k, (b.get('build_trigger_metadata') or {}).get('branch'), st[0], st[1]),
                    flush=True)
                last[k] = st
        if builds and all(b.get('status') == 'stopped' for b in builds):
            return 0 if all(b.get('build_outcome') == 'success' for b in builds) else 1
        time.sleep(15)
    print('TIMEOUT after %ss (no finished build for commit %s)' % (a.max_seconds, a.commit), flush=True)
    return 2


if __name__ == '__main__':
    sys.exit(main())
