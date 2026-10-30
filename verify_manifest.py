"""Check every file listed in MANIFEST.md against its sha256, and report files present but not listed.
Run from the package folder: python3 verify_manifest.py
Exit 0 = every listed file matches and nothing extra; 1 = a problem; 2 = no MANIFEST.md (an unassembled build).

(SHIPS INSIDE EVERY PACKAGE. Standard library only; Python 3.8+; no owner, product or package name in it.
 Self-test: python3 verify_manifest.py --selftest; it builds its own scratch package and needs nothing else.)"""
import hashlib
import os
import sys


def verify(folder):
    os.chdir(folder)
    if not os.path.exists("MANIFEST.md"):
        print("NO MANIFEST.md (unassembled build): nothing to check")
        return 2
    bad = n = 0
    listed = set()
    for line in open("MANIFEST.md", encoding="utf-8"):
        parts = [p.strip().strip("`") for p in line.split("|")]
        if len(parts) == 5 and len(parts[3]) == 64 and parts[1] not in ("path",):
            n += 1
            path, want = parts[1], parts[3]
            listed.add(path)
            try:
                got = hashlib.sha256(open(path, "rb").read()).hexdigest()
            except OSError as e:
                print("MISSING", path, e); bad += 1; continue
            if got != want:
                print("MISMATCH", path); bad += 1
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git")]
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), ".")
            if rel in listed or rel == "MANIFEST.md" or f.endswith((".pyc", ".pyo")):
                continue
            print("EXTRA", rel); bad += 1
    print(("OK %d files" % n) if not bad else ("%d problem(s) in %d listed files" % (bad, n)))
    return 1 if bad else 0


def selftest():
    import shutil
    import subprocess
    here = os.path.dirname(os.path.abspath(__file__))
    base = os.path.join(os.environ.get('VERIFY_MANIFEST_SELFTEST_DIR', os.path.expanduser('~/.cache/verify_manifest_selftest')), f"verify_manifest_{os.getpid()}")
    shutil.rmtree(base, ignore_errors=True)
    os.makedirs(os.path.join(base, "pkg"))
    open(os.path.join(base, "pkg", "a.md"), "w").write("a\n")
    open(os.path.join(base, "pkg", "b.md"), "w").write("b\n")
    rows = ["| path | bytes | sha256 |", "|---|---|---|"]
    for name in ("a.md", "b.md"):
        fp = os.path.join(base, "pkg", name)
        rows.append("| `%s` | %d | `%s` |" % (name, os.path.getsize(fp), hashlib.sha256(open(fp, "rb").read()).hexdigest()))
    open(os.path.join(base, "pkg", "MANIFEST.md"), "w").write("# MANIFEST\n\n" + "\n".join(rows) + "\n")
    cwd = os.getcwd()
    results = []
    results.append(("clean package -> 0", verify(os.path.join(base, "pkg")) == 0))
    os.chdir(cwd); open(os.path.join(base, "pkg", "a.md"), "w").write("changed\n")
    results.append(("an edited file -> MISMATCH, 1", verify(os.path.join(base, "pkg")) == 1))
    os.chdir(cwd); open(os.path.join(base, "pkg", "a.md"), "w").write("a\n"); open(os.path.join(base, "pkg", "extra.md"), "w").write("x\n")
    results.append(("an unlisted file -> EXTRA, 1", verify(os.path.join(base, "pkg")) == 1))
    os.chdir(cwd); os.remove(os.path.join(base, "pkg", "extra.md")); os.remove(os.path.join(base, "pkg", "b.md"))
    results.append(("a missing file -> MISSING, 1", verify(os.path.join(base, "pkg")) == 1))
    os.chdir(cwd); os.remove(os.path.join(base, "pkg", "MANIFEST.md"))
    results.append(("no MANIFEST.md -> 2", verify(os.path.join(base, "pkg")) == 2))
    os.chdir(cwd)
    bad = 0
    for name, ok in results:
        bad += not ok
        print(("OK   " if ok else "FAIL ") + name)
    print("%d cases, %d failures" % (len(results), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(verify(os.path.dirname(os.path.abspath(__file__))))
