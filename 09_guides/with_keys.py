#!/usr/bin/env python3
"""with_keys.py - run one command with named keys from your private key file, without ever showing them.

    python3 with_keys.py --check NAME[,NAME...]
    python3 with_keys.py NAME[,NAME...] -- <command> [args...]

It reads ~/.config/webtools/keys.env (override with WEBTOOLS_KEYS=/abs/path), the same file and the same rules the
workbench web tools use: plain KEY=value lines ("#" starts a comment line; a leading "export " and one pair of
surrounding quotes are tolerated and removed); a regular file you own, not a link, with no group or other access
(chmod 600). It never sources the file and never prints a value. The command receives your current environment
unchanged plus ONLY the keys you list from the key file (a listed key replaces any same-named variable already in
your environment); no other key in the file reaches the command. Variables already exported in your shell still pass
through, so unset any you do not want the command to see (for example: env -u NAME python3 with_keys.py ...).
The command line holds names, never values, so the process list and your chat transcript never show a key.

--check prints, for each name: "present", "missing" (absent or empty) or "placeholder" (a value still starting
REPLACE_WITH), and the file's permission bits. Exit 0 when every name is present and the file is private (no group or other access).

Exit codes: 0 ok (or the command's own exit code); 2 usage; 3 the key file is missing, a link, another user's, or
readable by others;
4 a named key is missing or still a placeholder (nothing was run).
Standard library only; Python 3.8+.
"""
import os
import stat
import sys

DEFAULT = os.path.join(os.path.expanduser("~"), ".config", "webtools", "keys.env")


def load(path):
    keys = {}
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip()
            if k.startswith("export "):
                k = k[len("export "):].strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                v = v[1:-1]
            keys[k] = v
    return keys


def private(path):
    mode = stat.S_IMODE(os.stat(path).st_mode)
    return mode & 0o077 == 0, oct(mode)


def main(argv):
    path = os.environ.get("WEBTOOLS_KEYS") or DEFAULT
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 2
    check = argv[0] == "--check"
    if check:
        argv = argv[1:]
    if not argv:
        print(__doc__)
        return 2
    names = [n for n in argv[0].split(",") if n]
    cmd = argv[2:] if len(argv) > 1 and argv[1] == "--" else None
    if not check and not cmd:
        print("usage: python3 with_keys.py NAME[,NAME...] -- <command> [args...]")
        return 2
    if not os.path.lexists(path):
        print(f"STOP: no key file at {path}. Make it with SERVICES.md, Section A.")
        return 3
    st = os.lstat(path)
    if stat.S_ISLNK(st.st_mode) or not stat.S_ISREG(st.st_mode):
        print(f"STOP: {path} is not a regular file (a link or a folder). Use a regular file.")
        return 3
    if hasattr(os, "getuid") and st.st_uid != os.getuid():
        print(f"STOP: {path} belongs to another user. Use your own key file.")
        return 3
    ok_mode, mode = private(path)
    if not ok_mode:
        print(f"STOP: {path} is mode {mode}; others can read it. Run: chmod 600 {path}")
        return 3
    keys = load(path)
    bad = 0
    for n in names:
        v = keys.get(n)
        state = "missing" if not v else ("placeholder" if v.startswith("REPLACE_WITH") else "present")
        bad += state != "present"
        if check:
            print(f"{n}: {state}")
    if check:
        print(f"key file: {path} (mode {mode}, private)")
        return 4 if bad else 0
    if bad:
        print("STOP: " + ", ".join(n for n in names if not keys.get(n) or keys[n].startswith("REPLACE_WITH"))
              + " missing or still a placeholder in the key file. Nothing was run. (Values are never shown.)")
        return 4
    env = dict(os.environ)
    for n in names:
        env[n] = keys[n]
    try:
        os.execvpe(cmd[0], cmd, env)
    except OSError as e:
        print(f"STOP: could not run {cmd[0]}: {e.strerror}")
        return 127


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
