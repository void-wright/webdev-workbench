"""webtools_keys.py: read YOUR keys from ~/.config/webtools/keys.env for the Python web tools in this folder.

The file is PARSED line by line (KEY=value, optional `export `, optional quotes, # comments). It is never executed,
never sourced and no value is ever printed. It must be a regular file owned by you with mode 600 (or 400).
Set WEBTOOLS_KEYS=/other/path to use another file with the same rules.
"""
import os
import stat
import sys

KEYS_PATH = os.path.expanduser(os.environ.get('WEBTOOLS_KEYS', '~/.config/webtools/keys.env'))


def _fail(msg, code=66):
    sys.stderr.write('[webtools] ' + msg + '\n')
    sys.exit(code)


def load_keys(path=KEYS_PATH):
    """Return {name: value} for every KEY=value line. Stops the program with a clear message on an unsafe file."""
    try:
        st = os.lstat(path)
    except FileNotFoundError:
        _fail('no key file at %s. Create it with: mkdir -p ~/.config/webtools && touch ~/.config/webtools/keys.env '
              '&& chmod 600 ~/.config/webtools/keys.env  (then add your keys with a text editor; see README.md)' % path)
    if stat.S_ISLNK(st.st_mode):
        _fail('%s is a symbolic link. Use a regular file.' % path)
    if not stat.S_ISREG(st.st_mode):
        _fail('%s is not a regular file.' % path)
    if st.st_mode & 0o077:
        _fail('%s can be read by other users. Fix it with: chmod 600 %s' % (path, path))
    if hasattr(os, 'getuid') and st.st_uid != os.getuid():
        _fail('%s belongs to another user. Use your own key file.' % path)
    out = {}
    with open(path, encoding='utf-8') as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('export '):
                line = line[len('export '):].strip()
            if '=' not in line:
                continue
            k, v = line.split('=', 1)
            k, v = k.strip(), v.strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in ('"', "'"):
                v = v[1:-1]
            if k and all(c.isalnum() or c == '_' for c in k):
                out[k] = v
    return out


def require(keys, name):
    """The value of one key, or stop with a message naming the key (never its value)."""
    v = keys.get(name, '')
    if not v:
        _fail('key %s is missing or empty in %s. Add a line: %s=<value>  (see README.md)' % (name, KEYS_PATH, name))
    return v
