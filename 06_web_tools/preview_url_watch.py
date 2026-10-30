#!/usr/bin/env python3
"""preview_url_watch.py: watch a preview URL until it serves the build you expect (READ-ONLY).

A build log saying "success" is not proof; the page is. This polls <url><probe> every 20 seconds until it answers
200 AND its body contains <marker> (a string you know only the new build has, such as a new heading or a build id).

Usage:
  python3 preview_url_watch.py --url <preview-url> --probe /<path> --marker '<text>' [--max-seconds 720] [--no-token]

Protected previews: if your previews sit behind Cloudflare Access, add a service token to
~/.config/webtools/keys.env as CF_ACCESS_CLIENT_ID and CF_ACCESS_CLIENT_SECRET (see the Cloudflare deploy guide).
When both keys are present they are sent as headers from inside this program (never on a command line, never printed),
and the watcher also reports what an anonymous visitor gets at "/" (a protected preview should answer 302 or 403).
Without those keys, or with --no-token, it watches the URL as a public visitor.

Redirects are NOT followed, so a login redirect shows up as 302 instead of a misleading 200.
Exit codes: 0 the expected build is live, 2 timeout, 64 usage.
"""
import argparse
import os
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from webtools_keys import KEYS_PATH, load_keys  # noqa: E402


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


OPENER = urllib.request.build_opener(_NoRedirect)


def fetch(url, headers):
    """(status code as text, body text). Network errors come back as code 'ERR'."""
    req = urllib.request.Request(url, headers=dict(headers, **{'User-Agent': 'preview_url_watch/1'}))
    try:
        with OPENER.open(req, timeout=30) as r:
            return str(r.status), r.read(5_000_000).decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return str(e.code), ''
    except (urllib.error.URLError, OSError):
        return 'ERR', ''


def main():
    ap = argparse.ArgumentParser(description='Watch a preview URL until it serves the expected build.')
    ap.add_argument('--url', required=True, help='the preview base URL, for example https://<preview-host>')
    ap.add_argument('--probe', required=True, help='a path that changed in this build, starting with /')
    ap.add_argument('--marker', required=True, help='text that only the new build contains')
    ap.add_argument('--max-seconds', type=int, default=720)
    ap.add_argument('--no-token', action='store_true', help='never send an Access service token')
    a = ap.parse_args()
    if not a.probe.startswith('/'):
        ap.error('--probe must start with /')
    base = a.url.rstrip('/')

    headers = {}
    if not a.no_token and os.path.exists(KEYS_PATH):
        keys = load_keys()
        cid, sec = keys.get('CF_ACCESS_CLIENT_ID', ''), keys.get('CF_ACCESS_CLIENT_SECRET', '')
        if cid and sec:
            headers = {'CF-Access-Client-Id': cid, 'CF-Access-Client-Secret': sec}
    mode = 'with your Access service token' if headers else 'as a public visitor'
    print('watching %s%s %s' % (base, a.probe, mode), flush=True)

    t0, last = time.time(), None
    while time.time() - t0 < a.max_seconds:
        el = int(time.time() - t0)
        code, body = fetch(base + a.probe, headers)
        has = a.marker in body
        anon = fetch(base + '/', {})[0] if headers else '-'
        state = (code, anon, has)
        if state != last:
            extra = (' | / without token=%s' % anon) if headers else ''
            print('[%4ds] %s answered %s | marker present=%s%s' % (el, a.probe, code, has, extra), flush=True)
            last = state
        if code == '200' and has:
            print('[%4ds] LIVE: the expected build is serving at %s' % (el, base), flush=True)
            return 0
        time.sleep(max(0, min(20, a.max_seconds - (time.time() - t0))))
    print('TIMEOUT after %ss' % a.max_seconds, flush=True)
    return 2


if __name__ == '__main__':
    sys.exit(main())
