#!/usr/bin/env bash
# install_skills.sh: lays the web-dev workbench (skills, reasoning skills, ACE agents, automations, guides, web tools,
# nexus tools and a short block in ~/.claude/CLAUDE.md) onto this machine. Run it AFTER Voidloom is installed.
#
#   bash bin/install_skills.sh --dry-run               print every action, change nothing
#   bash bin/install_skills.sh                         install
#   bash bin/install_skills.sh --uninstall             undo the install exactly (restores anything it replaced)
#   bash bin/install_skills.sh --uninstall --dry-run   print what the undo would do, change nothing
#
# Additive and reversible: anything already at a target is MOVED to ~/.webdev-workbench/backups/<time>/ (outside
# ~/.claude/skills, so Claude Code never loads a backup as a skill) and every change, including each folder it had to
# create, is recorded in ~/.webdev-workbench/uninstall_manifest.jsonl (one JSON object per line).
# Exit codes: 0 done, 2 unknown argument, 3 Voidloom not found, 4 package incomplete, 5 an install is already
# recorded, 6 the undo could not finish (the manifest keeps what is left).
set -eu
set -o pipefail

PKG="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TS="$(date +%Y%m%d%H%M%S)"
DRY=0; UNINSTALL=0
for a in "$@"; do
  case "$a" in
    --dry-run) DRY=1 ;;
    --uninstall) UNINSTALL=1 ;;
    -h|--help) sed -n '2,15p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "[workbench] unknown argument: $a (try --help)"; exit 2 ;;
  esac
done

STATE="$HOME/.webdev-workbench"
MAN="$STATE/uninstall_manifest.jsonl"
BAKROOT="$STATE/backups"
BAK="$BAKROOT/$TS"
SK="$HOME/.claude/skills"
CMDS="$HOME/.claude/commands"
AGENTS="$HOME/.claude/agents"
SHARE="$HOME/.local/share/webdev-workbench"
CLAUDE_MD="$HOME/.claude/CLAUDE.md"
BLOCK="$PKG/08_claude_md/webdev_workbench_block.md"
say() { echo "[workbench] $*"; }

# ---------------------------------------------------------------------------------------------------------- uninstall
if [ "$UNINSTALL" = 1 ]; then
  [ -f "$MAN" ] || { say "no install recorded at $MAN, nothing to undo"; exit 0; }
  python3 - "$MAN" "$DRY" "$STATE" <<'PY'
import hashlib, json, os, re, shutil, sys
man, dry, state = sys.argv[1], sys.argv[2] == '1', sys.argv[3]
entries = [json.loads(l) for l in open(man) if l.strip()]
pre = '[workbench] ' + ('[dry] ' if dry else '')
BLOCK_RE = re.compile(r'\n*# >>> WEBDEV WORKBENCH BEGIN >>>.*?# <<< WEBDEV WORKBENCH END <<<\n?', re.S)

def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def remove(p):
    if os.path.isdir(p) and not os.path.islink(p):
        shutil.rmtree(p)
    elif os.path.lexists(p):
        os.remove(p)

def in_state(p):
    return p == state or p.startswith(state + os.sep)

left, failed = [], 0
for e in reversed(entries):
    op, t, b = e['op'], e['target'], e.get('backup')
    if op == 'mkdir' and in_state(t):
        left.append(e)          # the state folders go last, after the manifest itself
        continue
    try:
        if op == 'place':
            print(pre + 'remove ' + t + (' and restore it from ' + b if b else ''))
            if not dry:
                remove(t)
                if b and os.path.lexists(b):
                    os.rename(b, t)
        elif op == 'block':
            if not os.path.exists(t):
                print(pre + t + ' is gone already')
                if not dry and b and os.path.lexists(b):
                    os.rename(b, t)
            elif sha(t) == e['sha256']:
                print(pre + 'restore ' + t + (' from ' + b if b else ' (remove: it did not exist before)'))
                if not dry:
                    os.remove(t)
                    if b and os.path.lexists(b):
                        os.rename(b, t)
            else:
                print(pre + t + ' was edited after the install: removing only the workbench block, keeping your edits')
                if not dry:
                    txt = BLOCK_RE.sub('\n', open(t).read()).strip('\n')
                    if txt:
                        open(t, 'w').write(txt + '\n')
                    elif not b:
                        os.remove(t)
                    else:
                        open(t, 'w').write('')
                    if b and os.path.lexists(b):
                        os.remove(b)
        elif op == 'mkdir':
            if os.path.isdir(t) and not os.listdir(t):
                print(pre + 'remove empty folder ' + t)
                if not dry:
                    os.rmdir(t)
            elif os.path.isdir(t):
                print(pre + 'keep ' + t + ' (it now holds files that are not ours)')
    except OSError as x:
        failed += 1
        print('[workbench] FAILED on ' + t + ': ' + str(x))
        left.append(e)

if dry:
    print('[workbench] [dry] then remove ' + man + ' and the empty workbench state folders. Nothing changed.')
    sys.exit(0)
if failed:
    with open(man, 'w') as fh:
        for e in reversed(left):
            fh.write(json.dumps(e) + '\n')
    print('[workbench] %d step(s) failed; %s now lists what is left. Fix the cause and run --uninstall again.' % (failed, man))
    sys.exit(6)
os.remove(man)
for e in left:   # already in reverse order: deepest state folder first
    t = e['target']
    if os.path.isdir(t) and not os.listdir(t):
        os.rmdir(t)
print('[workbench] undone. Start a new Claude Code session so the removed skills unload.')
PY
  exit $?
fi

# ------------------------------------------------------------------------------------------------------------ install
command -v voidloom >/dev/null 2>&1 || { say "Voidloom is not on PATH. Install and verify Voidloom first (SETUP_GUIDE.md)."; exit 3; }
for need in 03_skills 04_reasoning 04_reasoning/commands 05_automations/agents 05_automations/client-site-first-build \
            05_automations/website-maintenance 05_automations/resource-hub-maintenance 06_web_tools 07_nexus_tools \
            09_guides 08_claude_md/webdev_workbench_block.md; do
  [ -e "$PKG/$need" ] || { say "package incomplete: $PKG/$need is missing. Nothing was changed."; exit 4; }
done
[ -f "$MAN" ] && { say "an install is already recorded in $MAN. Run --uninstall first."; exit 5; }

N=0
record() {  # record <op> <target> [backup] [sha256]: append one JSON line to the manifest
  [ "$DRY" = 1 ] && return 0
  python3 -c 'import json, sys
op, t, b, h = sys.argv[1:5]
d = {"op": op, "target": t, "backup": b or None}
if h: d["sha256"] = h
print(json.dumps(d))' "$1" "$2" "${3:-}" "${4:-}" >> "$MAN"
}
mkdir_rec() {  # mkdir_rec <dir>: create a folder and every missing parent, recording each one it created
  local d="$1" todo="" p
  while [ ! -d "$d" ]; do todo="$d
$todo"; d="$(dirname "$d")"; done
  [ -n "$todo" ] || return 0
  printf '%s' "$todo" | while IFS= read -r p; do
    [ -n "$p" ] || continue
    if [ "$DRY" = 1 ]; then say "[dry] create folder $p"; else mkdir "$p"; record mkdir "$p"; fi
  done
}
place() {  # place <src> <target>: copy src to target; move anything already there into the backup folder first
  local src="$1" dst="$2" bak=""
  N=$((N + 1))
  if [ -e "$dst" ] || [ -L "$dst" ]; then bak="$BAK/$N.$(basename "$dst")"; fi
  if [ "$DRY" = 1 ]; then
    say "[dry] $src -> $dst${bak:+ (existing one moved to $bak)}"
    return 0
  fi
  mkdir_rec "$(dirname "$dst")"
  if [ -n "$bak" ]; then mkdir_rec "$BAK"; mv "$dst" "$bak"; fi
  cp -R "$src" "$dst"
  record place "$dst" "$bak"
  say "ok  $dst"
}

if [ "$DRY" = 0 ]; then
  if [ ! -d "$STATE" ]; then mkdir "$STATE"; : > "$MAN"; record mkdir "$STATE"; else : > "$MAN"; fi
  mkdir_rec "$BAKROOT"
fi

# skills: 03_skills/* and the reasoning skills (every folder in 04_reasoning except commands)
for d in "$PKG"/03_skills/*/; do place "${d%/}" "$SK/$(basename "$d")"; done
for d in "$PKG"/04_reasoning/*/; do
  [ "$(basename "$d")" = "commands" ] && continue
  place "${d%/}" "$SK/$(basename "$d")"
done
for f in "$PKG"/04_reasoning/commands/*.md; do [ -e "$f" ] && place "$f" "$CMDS/$(basename "$f")"; done
# ACE design agents and the automations
for f in "$PKG"/05_automations/agents/*.md; do [ -e "$f" ] && place "$f" "$AGENTS/$(basename "$f")"; done
for d in "$PKG"/05_automations/*/; do
  [ "$(basename "$d")" = "agents" ] && continue
  place "${d%/}" "$SHARE/automations/$(basename "$d")"
done
# guides, web tools, nexus tools
place "$PKG/09_guides" "$SHARE/guides"
place "$PKG/06_web_tools" "$SHARE/web_tools"
place "$PKG/07_nexus_tools" "$SHARE/nexus_tools"

# ~/.claude/CLAUDE.md: the workbench block between its markers (replaced in place if one is already there)
if [ "$DRY" = 1 ]; then
  say "[dry] add the WEBDEV WORKBENCH block to $CLAUDE_MD${CLAUDE_MD:+ (a copy of the current file goes to the backup folder)}"
else
  mkdir_rec "$(dirname "$CLAUDE_MD")"
  cbak=""
  if [ -e "$CLAUDE_MD" ]; then mkdir_rec "$BAK"; N=$((N + 1)); cbak="$BAK/$N.CLAUDE.md"; cp -p "$CLAUDE_MD" "$cbak"; fi
  python3 - "$CLAUDE_MD" "$BLOCK" <<'PY'
import os, re, sys
p, b = sys.argv[1], open(sys.argv[2]).read().strip() + '\n'
t = open(p).read() if os.path.exists(p) else ''
pat = re.compile(r'# >>> WEBDEV WORKBENCH BEGIN >>>.*?# <<< WEBDEV WORKBENCH END <<<\n?', re.S)
t = pat.sub(lambda m: b, t) if pat.search(t) else (t.rstrip('\n') + '\n\n' + b if t.strip() else b)
open(p, 'w').write(t)
PY
  h="$(python3 -c 'import hashlib, sys; print(hashlib.sha256(open(sys.argv[1], "rb").read()).hexdigest())' "$CLAUDE_MD")"
  record block "$CLAUDE_MD" "$cbak" "$h"
  say "ok  workbench block in $CLAUDE_MD"
fi

if [ "$DRY" = 0 ]; then
  rmdir "$BAK" 2>/dev/null || true   # nothing needed backing up: leave no empty folder behind
  lines="$(python3 -c 'import json, sys; print(len([json.loads(l) for l in open(sys.argv[1]) if l.strip()]))' "$MAN")"
  say "undo record: $MAN ($lines steps). Undo everything with: bash bin/install_skills.sh --uninstall"
  say "DONE. Start a NEW Claude Code session so the skills, agents and command load."
else
  say "dry run: $N placements + the CLAUDE.md block. Nothing changed."
fi
