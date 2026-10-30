# SETUP GUIDE: the Voidwright web-dev workbench, from zero

**This guide is about 850 lines long. Read it in pages (Read with offset and limit) before you run P0.**

**Who this is for:** the Claude Code agent on the person's own computer. By the end of this guide:
- **Voidloom**, a local memory brain for Claude Code, is installed from its public repository, pinned to one
  tested commit;
- the web-craft memory pack from `02_memory/` is loaded into that brain and proven findable;
- the web skills, the reasoning skills, three website automations and the web tools are installed;
- the person has designed their own persona with the Persona Forge;
- if they chose to, GitHub and one host (Cloudflare or Vercel) are set up, and a first small site has a preview link.

Everything runs on the person's own computer and their own accounts. Nothing is sent to the people who made this
package.

---

## How to run this guide (read all of it before P0)

Three facts about your situation shape every command below:

1. **You have no terminal (no TTY).** A program that stops to ask a question gets no answer. So **P0 collects every
   answer from the person first**, in one message, and the commands pass those answers as flags. Never answer a
   question meant for the person yourself. That includes the compute choice, the GPU cards, the overnight thinker,
   approvals and the persona.
2. **Nothing persists between your Bash calls.** An `export`, a `cd` or a `source` in one call is gone in the next.
   So P0.4 writes `~/.webdev-workbench-setup/shell.sh` (the shipped `bin/shell_env.sh`, copied unchanged), and **every
   Bash call from P0.4 on starts with `. ~/.webdev-workbench-setup/shell.sh &&`**. It sets `PKG` (this folder) and,
   once Voidloom is installed, `PATH` and the brain's `WIZARD_*` settings. It READS Voidloom's env file line by line;
   it never sources a file that could hold a key, and it never exports a name containing TOKEN, KEY, SECRET or PASSWORD.
3. **Long steps outlive your Bash timeout.** The Voidloom install and the memory embedding can each take 5 to 20
   minutes. Run them with your Bash tool's **background** option. They write a log and an **rc file**; the step is done
   when the rc file exists, and its content (`rc=0`) is the result.

Working rules:
- **Phase by phase, in order.** Each phase ends with a **PASS line**. Do not start the next phase until it holds. After
  each phase, append one line to the progress file:
  `. ~/.webdev-workbench-setup/shell.sh && echo "PASS P<n> $(date -u +%Y-%m-%dT%H:%MZ)" >> ~/.webdev-workbench-setup/progress.txt`
- **A new session resumes from the progress file.** The person will restart Claude Code more than once (P4, P5). A
  new session reads this guide's *How to run* section, then `~/.webdev-workbench-setup/progress.txt` and
  `answers.md`, and continues at the first phase without a PASS line.
- **HUMAN boxes** (marked 🙋) are things only the person can do: answers, passwords, browser sign-ins, typing a key.
  Stop there, tell them what to do in one or two plain sentences, and wait.
- **Dry run before every write.** Every installer here has a `--dry-run` or plan mode. Run it, read it, show the person
  anything that touches their files, then run it for real. A plan alone has written nothing: the PASS line is always the
  applied run.
- **Read exit codes from the command or from an rc file, never through a pipe.** `cmd | tail` reports tail's exit code.
  The pattern is `cmd > ~/.webdev-workbench-setup/<step>.log 2>&1; echo "rc=$?"`, then read the log with your Read
  tool. Never send stderr into a JSON file the next step parses (`2>` goes to its own file). Never use a pager.
- **Call every script through its interpreter** (`bash x.sh`, `python3 x.py`): downloading as a zip can drop the executable mark.
- **Never print, paste, `source` or commit a secret.** Keys live in one private file the person fills in their own
  terminal (`09_guides/SERVICES.md`). If a command fails, read the error and fix the cause; after two honest tries, stop
  and give the person the exact failing line.
- **Run `voidloom` commands from the home folder** (`cd ~ &&`): `voidloom doctor` also reads the Claude Code settings of
  the folder it runs in.

Labels used below: **PROVEN** means executed end to end on that kind of machine; **SUPPORTED-UNPROVEN** means the
code path exists and was checked, but nobody has run this guide's step on that kind of machine yet. Say these labels to
the person as they are.

What this guide's own steps have been executed on (2026-10-29, Linux under WSL2, x86_64, in a throwaway home folder):
the Voidloom clone from GitHub and its pin check, a keyword-only (Tier 0) install with this guide's flags (both forms of
the `WIZARD_PYTHON_BIN` line), `shell.sh`, the doctor reader, the load plan reader, the recall battery, the update route
in P8.2, and the key file with its helper and hidden-input writer. The semantic (Tier 1) install on Linux with the CPU or an
NVIDIA GPU, and on an Apple Silicon Mac, is labelled PROVEN by Voidloom itself (its README, "Which machines are
proven"). Every macOS step of THIS guide (Miniforge, nvm, the package installer under macOS's bash) is
**SUPPORTED-UNPROVEN**.

Be calm and thorough rather than fast. Nothing here is urgent.

---

## P0. Detect the computer and gather every answer up front

### P0.1 Detect

Run this from the folder that holds this guide (the package folder):

```bash
uname -s; uname -m; (sw_vers 2>/dev/null || head -n 3 /etc/os-release 2>/dev/null); grep -qi microsoft /proc/version 2>/dev/null && echo "WSL"; command -v python3 && python3 -V; df -h "$HOME" | tail -n 1; pwd
```

- **macOS (`Darwin`):** continue. `arm64` is Apple Silicon, `x86_64` is an Intel Mac. Two Mac facts shape everything
  below: the brain needs **Miniforge's Python**, not Apple's (Apple's `/usr/bin/python3` cannot load SQLite extensions,
  so semantic recall could never start; Voidloom README, Requirements), and an Intel Mac always computes on the CPU.
  Homebrew is not needed for any required step.
- **Linux:** continue.
- **WSL (Linux inside Windows):** continue as Linux. If the folder you are in starts with `/mnt/c/`, copy the package
  into the Linux home first: `cp -a "<that folder>" ~/webdev-workbench-package`, then work from there. File
  permissions (the `600` mode that keeps a key file private) do not hold on `/mnt/c`.
- **Windows, not inside WSL** (`uname -s` starts with `MINGW`, `MSYS` or `CYGWIN`, or there is no `uname`): this
  package runs inside **WSL2 Ubuntu**.
  > 🙋 **HUMAN:** "Open PowerShell as Administrator, run `wsl --install -d Ubuntu`, restart when asked, and finish the
  > Ubuntu username and password prompt. Then install Claude Code inside Ubuntu, clone or unzip this package into your Ubuntu
  > home folder, open Claude Code there, and say the starting sentence again." (Microsoft's guide:
  > learn.microsoft.com/windows/wsl/install.) Then restart this guide at P0 inside WSL.

`PKG` is the absolute path of the folder holding this guide: the `pwd` above, or the copy's path on WSL.

### P0.2 Measure what the questions depend on

```bash
mkdir -p ~/.webdev-workbench-setup && chmod 700 ~/.webdev-workbench-setup
SMI="$(command -v nvidia-smi || ls /usr/lib/wsl/lib/nvidia-smi 2>/dev/null)"; if [ -n "$SMI" ]; then "$SMI" --query-gpu=index,name,memory.total,display_active --format=csv,noheader > ~/.webdev-workbench-setup/gpus.txt 2>&1; echo "nvidia-smi rc=$?"; else echo "no NVIDIA GPU" > ~/.webdev-workbench-setup/gpus.txt; echo "no nvidia-smi"; fi
if [ "$(uname -s)" = Darwin ]; then sysctl -n hw.memsize | awk '{printf "RAM_GiB=%.1f\n", $1/1073741824}'; sysctl -n machdep.cpu.brand_string; else awk '/MemTotal/ {printf "RAM_GiB=%.1f\n", $2/1048576}' /proc/meminfo; (lspci 2>/dev/null | grep -iE 'vga|3d|display') || true; fi
df -Pk "$HOME" | awk 'NR==2 {printf "free_GB=%.1f\n", $4/1048576}'
[ "$(uname -s)" = Darwin ] || { python3 -m venv ~/.webdev-workbench-setup/venvtest > ~/.webdev-workbench-setup/venvtest.log 2>&1; echo "venv rc=$?"; rm -rf ~/.webdev-workbench-setup/venvtest; }
ls -d ~/voidloom ~/.claude/memory/claude_memory.db 2>/dev/null; echo "existing-check done"
find ~/.claude/skills -mindepth 1 -maxdepth 1 -type d 2>/dev/null > ~/.webdev-workbench-setup/skills_before.txt; wc -l < ~/.webdev-workbench-setup/skills_before.txt
```

Read what it printed:
- **GPUs.** Read `gpus.txt`. If `nvidia-smi rc` was not 0 (a driver problem), treat the machine as having no usable
  NVIDIA GPU and show the person the file. Otherwise count the lines: 0, 1, or 2 or more. The `lspci` lines (Linux)
  show an AMD or Intel GPU if there is one.
- **RAM.** Voidloom uses its reranker (a model that sharpens ranking) only with a GPU-class accelerator AND at least
  15.0 GiB of RAM; on the CPU it is always off (Voidloom README, "How it works").
- **venv** (Linux/WSL). `venv rc=0` means Python can build a virtual environment, which the semantic tier needs. Not 0
  (often "ensurepip is not available"): P1 has the fix.
- **Existing Voidloom.** If `~/voidloom` or `~/.claude/memory/claude_memory.db` printed, this computer already has a
  Voidloom clone or a brain. Stop and ask the person before going on: the installer keeps an existing brain, but the
  person must decide whether this setup should use it.
- **Skills before.** The last number is how many skill folders `~/.claude/skills` held before this setup.

**Disk.** The installer's own estimates (Voidloom README, Requirements): a Python environment of about **6 GB** on Linux
with an NVIDIA GPU (the CUDA build of PyTorch) or about **1.5 GB** CPU-only, plus about **1.8 GB** of models
downloaded once, plus pip's download cache (a few GB, which can be deleted afterwards). Keyword-only (`--tier0-only`)
needs about 10 MB plus the brain. Plan for **12 GB free** on the NVIDIA path, **6 GB** on the CPU or Mac path, **1 GB**
for keyword-only.

### P0.3 Ask the person everything, in ONE message

> 🙋 **HUMAN: the setup questions.** Send these together, numbered, and wait for every answer. Show what you measured
> (the GPU list, the RAM and the free disk) beside the questions it affects.
>
> 1. **Your computer** (confirm): "I see <OS, chip>. Is that right?"
> 2. **Compute: which processor the memory brain uses for its models.**
>    - **Apple Silicon Mac:** "Your Mac's GPU can run the brain's models (Voidloom labels this PROVEN on Apple Silicon).
>      Use the GPU (recommended), or the CPU only?" GPU → no flag; CPU → `--accelerator cpu`.
>    - **Intel Mac:** nothing to ask: it computes on the CPU (`--accelerator cpu`; Voidloom labels the Intel Mac
>      SUPPORTED-UNPROVEN). Tell them so.
>    - **Linux/WSL, no NVIDIA GPU:** if `lspci` showed an AMD or Intel GPU, ask "Voidloom can try your <AMD/Intel> GPU
>      (SUPPORTED-UNPROVEN: never run on that kind of card yet), or use the CPU only (PROVEN). Which?" Otherwise nothing to
>      ask: `--accelerator cpu`.
>    - **Linux/WSL, one NVIDIA GPU:** "Your one graphics card also drives your screen. If the memory brain uses it for its
>      background jobs, it shares that card with your desktop. GPU (faster, more disk), or CPU only?" CPU →
>      `--accelerator cpu`; GPU → no flag.
>    - **Linux/WSL, two or more NVIDIA GPUs:** first "GPU or CPU only?". CPU only → `--accelerator cpu` and no card
>      questions. GPU → show the list (index, name, memory, `display_active`). On WSL the `display_active` column reads
>      `Disabled` for every card, including the one driving the monitor, so do not trust it there. Then ask, word for
>      word, the installer's two questions:
>      > Which card drives your monitor(s)? (a card number, or 'none')
>
>      > Which card should the brain's background jobs use? (a card number)
>
>      → `--display-gpu <first answer> --gpu <second answer>`. The installer never picks the card, and neither do you.
>      If both answers name the same card, explain that a background model on the monitor's card can starve the desktop
>      without any error, and ask again.
> 3. **The overnight thinker.** Put this to them **word for word** (quoted exactly as Voidloom prints it, punctuation
>    included), and let them choose. Never pick it for them:
>    > **Should your brain think while you sleep, and with which model?**
>    >
>    > a) Claude  
>    > b) Codex  
>    > c) Kimi  
>    > d) Gemini (Google; runs through Google's Antigravity program)  
>    > e) Not now — no model; keep the simple nightly routines  
>    > f) Other (which model?)
>    >
>    > The model you chat with can be a different one: this answer is only about the thinking your brain does on its own, overnight.
>
>    On a Mac, add: "Voidloom says d) Gemini is not yet available on Mac." If they still pick d on a Mac, ask for another
>    letter. "e) Not now" is a perfectly good answer. For f), ask which model and how the brain reaches it (a local
>    server's address and kind, ollama or openai-compatible, or a command template); the model must already be running.
> 4. **Approvals.** Put this to them word for word (the installer's own question):
>    > Approvals. Once a month the brain reviews its own health and proposes improvements.  
>    > a) Automatic (recommended) -- the brain approves its own monthly proposals and names what it  
>    > decided at the start of each session for the next 7 days. Change it any time: voidloom approvals --mode manual  
>    > b) Manual -- each proposal waits for you in: voidloom approvals --tui  
>    > (Belief links and governance holds are not affected by this: they always wait for a person.)
>
>    a → `--approvals auto`; b → `--approvals manual`.
> 5. **Nightly routines.** "Should the brain run its nightly routines on this computer (memory upkeep, and the overnight
>    thinker if you chose one in question 3)? Yes, or not now." Tell them plainly: with "not now", the question 3
>    answer is recorded but **nothing runs at night**. (Yes → P2.8, after the thinker answer is recorded.)
> 6. **Session hook.** "May I wire Voidloom's session-start hook, so every new Claude Code session starts with your
>    brain's guidance and memories, and the first one offers the Persona Forge?" Recommend yes. Yes → `--wire-hooks`;
>    no → `--no-wire-hooks` (P2.6 then offers the hook-free instruction block instead).
> 7. **Administrator rights.** "Can you run `sudo` commands on this computer (do you know your password)? I only need
>    them if something is missing, and you will type the password in your own terminal, not me."
> 8. **GitHub and a host.** "Do you want to set up GitHub plus a host for your sites now, or later? If now: Cloudflare or
>    Vercel? (If you are unsure, `09_guides/CHOOSING_A_HOST.md` compares them in two minutes.)" Now → P6 runs; later →
>    P6 is skipped and P7 builds the first site locally only.

If the free disk is below the plan figure for the path they chose, say so now and offer the CPU path, or keyword-only
(Tier 0) now with the semantic tier later (P2, *Upgrading Tier 0 to Tier 1*).

### P0.4 Write the answers down (four small files)

Run this block **from the package folder** (it is the only block that does not start with `shell.sh`, because it
writes it):

```bash
PKG="$(pwd)"; [ -f "$PKG/SETUP_GUIDE.md" ] && [ -f "$PKG/bin/shell_env.sh" ] || { echo "STOP: run this from the package folder"; exit 1; }
mkdir -p ~/.webdev-workbench-setup && chmod 700 ~/.webdev-workbench-setup && printf '%s\n' "$PKG" > ~/.webdev-workbench-setup/pkg_path && cp "$PKG/bin/shell_env.sh" ~/.webdev-workbench-setup/shell.sh; echo "rc=$?"
```

Then the answers (replace each `<…>`; this file holds no secrets):

```bash
cat > ~/.webdev-workbench-setup/answers.md <<'EOF'
# Setup answers (written at P0 on <date>; no secrets)
OS: <macOS arm64 | macOS x86_64 | Linux | WSL2>; RAM_GiB: <…>; free_GB: <…>
Compute: <auto | cpu>; NVIDIA GPUs: <0 | 1 | 2+: list>; display card: <n | none | n/a>; jobs card: <n | n/a>
Overnight thinker: <a claude | b codex | c kimi | d gemini | e off | f local (model + how reached)>
Approvals: <auto | manual>
Nightly routines: <yes | not now>
Session hook: <yes | no>
sudo available: <yes | no>
GitHub + host: <now: cloudflare | now: vercel | later>
Python for the brain: <system python3 | Miniforge python 3.12>
Tier reached: <filled in at P2>
EOF
```

Then the installer-flags file. It is the **only** place the installer's flags are written, so the dry run, the real
run and any later re-run cannot differ:

```bash
cat > ~/.webdev-workbench-setup/install_flags.sh <<'EOF'
#!/usr/bin/env bash
# The person's P0 answers as Voidloom installer flags: the ONLY place they live (dry run, real run, later re-runs).
# If the thinker is later changed with `voidloom thinker set`, remove any --thinker flag here, or a re-run replaces it.
# export WIZARD_PYTHON_BIN="$HOME/miniforge3/envs/voidloom/bin/python3"   # Mac (always) or Linux route (b): remove the leading "# "
cd "$HOME" || exit 9
exec bash "$HOME/voidloom/install.sh" <FLAGS> "$@"
EOF
chmod 700 ~/.webdev-workbench-setup/install_flags.sh
```

Replace `<FLAGS>` (with your Edit tool) using this table:

| Answer | Flag(s) |
|---|---|
| Compute: CPU (any machine), an Intel Mac, or no GPU | `--accelerator cpu` |
| Compute: GPU (Apple Silicon, one NVIDIA card, or an AMD/Intel GPU the person chose) | no flag (`auto` is the default) |
| Two or more NVIDIA GPUs, GPU chosen | `--display-gpu <card or none> --gpu <card>` |
| Thinker e) Not now | `--thinker off` |
| Thinker f) Other | `--thinker local --thinker-model <name>` plus either `--thinker-endpoint <http://host:port> --thinker-api <ollama or openai>` or `--thinker-command '<template with {model} and {prompt}>'` |
| Thinker a), b), c) or d) | **no flag here** (P2.3 explains why) |
| Approvals | `--approvals auto` or `--approvals manual` |
| Session hook yes / no | `--wire-hooks` / `--no-wire-hooks` |
| Nightly routines yes | **not on the first run**: P2.8 adds `--with-crons` once the thinker answer is recorded |

Always pass the thinker's NAME (`off`, `local`), never its letter: Voidloom changed what d) and f) mean once, and names
cannot drift (`install.sh --help`, `--thinker`).

Examples. A CPU-only Linux laptop that chose e), automatic approvals and the hook:
`exec bash "$HOME/voidloom/install.sh" --accelerator cpu --thinker off --approvals auto --wire-hooks "$@"`.
An Apple Silicon Mac on its GPU that chose a): `exec bash "$HOME/voidloom/install.sh" --approvals auto --wire-hooks "$@"`,
with the `export WIZARD_PYTHON_BIN=…` line uncommented in P1.

**PASS P0** (a new Bash call):
```bash
. ~/.webdev-workbench-setup/shell.sh && ls ~/.webdev-workbench-setup && echo "PKG=$PKG" && cmp "$PKG/bin/shell_env.sh" ~/.webdev-workbench-setup/shell.sh && echo "shell.sh is the shipped parser" && grep -c '<FLAGS>' ~/.webdev-workbench-setup/install_flags.sh; bash -n ~/.webdev-workbench-setup/install_flags.sh; echo "syntax rc=$?"
```
`ls` lists `answers.md`, `install_flags.sh`, `pkg_path` and `shell.sh` (plus P0.2's files); `PKG=` prints the package
folder; `shell.sh is the shipped parser` prints; the `<FLAGS>` count is `0`; `syntax rc=0`. Show the person
`answers.md` and the `exec` line.

---

## P1. Prerequisites (check each; install only what is missing)

Run each check as `. ~/.webdev-workbench-setup/shell.sh && <check>`.

| Tool | Check | If missing |
|---|---|---|
| git | `git --version` | macOS: `xcode-select --install` (opens a dialog: the person clicks Install). Ubuntu/WSL: `sudo apt-get install -y git` |
| curl | `curl --version` | Ubuntu/WSL: `sudo apt-get install -y curl` |
| Python 3.10 or newer (the installer's floor) | `python3 -V` | macOS: the Miniforge route below (always, on every Mac). Ubuntu/WSL: `sudo apt-get install -y python3 python3-venv` |
| Python venv (Linux/WSL) | P0.2 printed `venv rc=0` | the box below |
| nvm + Node.js 22 (for building sites in P7) | `. "$HOME/.nvm/nvm.sh" && node --version` prints `v22.` | below |

**`sudo` is the person's act.** A `sudo` command from your Bash tool has no terminal to ask for the password, so it
fails. Give the person the exact command, ask them to run it in their own terminal window (on WSL, the Ubuntu window),
then re-run the check yourself.

**The Mac route: Miniforge's Python (every Mac; no Homebrew, no sudo; SUPPORTED-UNPROVEN in this guide).** This is
Voidloom's own Mac route (`~/voidloom/docs/ONBOARDING_GUIDE.md`, "On a Mac"), written so the installer runs only if
the checksum passes:
```bash
. ~/.webdev-workbench-setup/shell.sh && cd ~/.webdev-workbench-setup && rm -f Miniforge3-*.sh Miniforge3-*.sh.sha256 && TAG="$(curl -fsSL https://api.github.com/repos/conda-forge/miniforge/releases/latest | /usr/bin/python3 -c 'import json,sys; print(json.load(sys.stdin)["tag_name"])')" && F="Miniforge3-${TAG}-MacOSX-$(uname -m).sh" && echo "$F" && curl -fsSLO "https://github.com/conda-forge/miniforge/releases/download/${TAG}/${F}" && curl -fsSLO "https://github.com/conda-forge/miniforge/releases/download/${TAG}/${F}.sha256" && shasum -a 256 -c "${F}.sha256" > miniforge_sha.log 2>&1 && bash "$F" -b -p "$HOME/miniforge3" > miniforge.log 2>&1 && "$HOME/miniforge3/bin/conda" create -y -p "$HOME/miniforge3/envs/voidloom" python=3.12 > conda_env.log 2>&1; echo "chain rc=$?"
```
- `chain rc=0`, and `miniforge_sha.log` reading `<file>: OK`, means every link passed. Otherwise read the logs in order
  (`miniforge_sha.log`, `miniforge.log`, `conda_env.log`) and stop at the first failure. A checksum that is not OK means
  stop and show the person. (If `/usr/bin/python3` asks to install the Command Line Tools, that is the same install
  `git` needs.)
- Then remove the leading `# ` from the `# export WIZARD_PYTHON_BIN=…` line in `install_flags.sh` (it sits before
  `exec`, so the installer inherits it: `install.sh` builds its venv from `WIZARD_PYTHON_BIN` first), run
  `bash -n ~/.webdev-workbench-setup/install_flags.sh`, and write "Miniforge python 3.12" into `answers.md`.
- Python **3.12** on purpose: an Intel Mac's last PyTorch (2.2.2) has no build for Python 3.13, and the brain would then
  stay keyword-only (ONBOARDING_GUIDE, "An Intel Mac").

> 🙋 **HUMAN (Linux/WSL): STOP if Python venv is missing** (`venv rc` not 0, or "ensurepip is not available").
> Without it Voidloom installs at **Tier 0**: keyword recall only. Everything still works at Tier 0, but match-by-meaning
> recall needs **Tier 1**, which needs a venv. Ask which route they prefer:
>
> **(a) The administrator route.** In their own terminal: `sudo apt-get update && sudo apt-get install -y python3-venv`.
> If the venv test still says *ensurepip is not available*, the versioned package it names, for example
> `sudo apt-get install -y python3.12-venv` (match `python3 -V`). Fedora: `sudo dnf install -y python3`.
> Then re-run the P0.2 venv line.
>
> **(b) The home-folder route, no sudo** (SUPPORTED-UNPROVEN in this guide). You can run it yourself:
> ```bash
> . ~/.webdev-workbench-setup/shell.sh && cd ~/.webdev-workbench-setup && rm -f miniforge.sh miniforge.sh.sha256 && V="$(curl -fsSL https://api.github.com/repos/conda-forge/miniforge/releases/latest | python3 -c 'import json,sys; print(json.load(sys.stdin)["tag_name"])')" && echo "miniforge $V" && curl -fsSL -o miniforge.sh "https://github.com/conda-forge/miniforge/releases/download/$V/Miniforge3-$V-Linux-$(uname -m).sh" && curl -fsSL -o miniforge.sh.sha256 "https://github.com/conda-forge/miniforge/releases/download/$V/Miniforge3-$V-Linux-$(uname -m).sh.sha256" && awk '{print $1"  miniforge.sh"}' miniforge.sh.sha256 | sha256sum -c - > miniforge_sha.log 2>&1 && bash miniforge.sh -b -p "$HOME/miniforge3" > miniforge.log 2>&1 && "$HOME/miniforge3/bin/conda" create -y -p "$HOME/miniforge3/envs/voidloom" python=3.12 > conda_env.log 2>&1 && "$HOME/miniforge3/envs/voidloom/bin/python3" -m venv venvtest > venvtest.log 2>&1; echo "chain rc=$?"; rm -rf venvtest
> ```
> The checksum is published only under the versioned file name, which is why the release tag is read first.
> `chain rc=0` means every link passed (`miniforge_sha.log` reads `miniforge.sh: OK`). Then uncomment the
> `WIZARD_PYTHON_BIN` line in `install_flags.sh` exactly as on a Mac, check it with `bash -n`, and write
> "Miniforge python 3.12" into `answers.md`. Never use a shim that pretends to be apt.
>
> **If neither is possible now:** continue at Tier 0. Append `--tier0-only` before `"$@"` on the `exec` line and write
> "Tier 0 for now" into `answers.md`. *Upgrading Tier 0 to Tier 1* (end of P2) adds the semantic tier later.

**nvm and Node.js** (no sudo; the macOS run of these lines is SUPPORTED-UNPROVEN). Download first, then run, so each
exit code is the command's own:
```bash
. ~/.webdev-workbench-setup/shell.sh && curl -fsSL -o ~/.webdev-workbench-setup/nvm-install.sh https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh; echo "download rc=$?"
. ~/.webdev-workbench-setup/shell.sh && PROFILE=/dev/null bash ~/.webdev-workbench-setup/nvm-install.sh > ~/.webdev-workbench-setup/nvm.log 2>&1; echo "nvm rc=$?"
. ~/.webdev-workbench-setup/shell.sh && . "$HOME/.nvm/nvm.sh" && nvm install 22 > ~/.webdev-workbench-setup/node.log 2>&1; echo "node rc=$?"; . "$HOME/.nvm/nvm.sh" && nvm alias default 22 && node --version
```
`PROFILE=/dev/null` stops the nvm installer from editing the person's shell profile; every command in this guide that
needs Node starts with `. "$HOME/.nvm/nvm.sh" &&` instead. (If the person wants `node` in their own terminals, they can
add `. "$HOME/.nvm/nvm.sh"` to `~/.bashrc` or `~/.zshrc` themselves.)

**PASS P1:** `git --version`, `curl --version` and `python3 -V` (3.10 or newer) each print a version; on Linux/WSL
`venv rc=0` or `answers.md` says "Miniforge python 3.12" or "Tier 0 for now"; on a Mac `chain rc=0` and the
`WIZARD_PYTHON_BIN` line is uncommented; `node --version` prints `v22.`.

---

## P2. Voidloom, the memory brain

Voidloom is installed from its public repository, https://github.com/void-wright/voidloom (Apache-2.0), at commit
`7cfa8e6` (release v1.0.0 plus four fixes on public main). This package's memory pack and battery were checked against
that commit. Never edit anything inside `~/voidloom`.

### P2.1 Clone and pin

```bash
. ~/.webdev-workbench-setup/shell.sh && cd ~ && [ ! -e ~/voidloom ] && git clone https://github.com/void-wright/voidloom.git ~/voidloom > ~/.webdev-workbench-setup/clone.log 2>&1 && git -C ~/voidloom -c advice.detachedHead=false checkout 7cfa8e6 >> ~/.webdev-workbench-setup/clone.log 2>&1; echo "rc=$?"
. ~/.webdev-workbench-setup/shell.sh && git -C ~/voidloom rev-parse HEAD && git -C ~/voidloom remote get-url origin
```
If `~/voidloom` already existed, the first line stops with a non-zero rc and clones nothing: ask the person (P0.2).

**PASS P2.1:** `rc=0`, then exactly `7cfa8e610997e0c627c48114266238a425858d72` and
`https://github.com/void-wright/voidloom.git`. Any other commit: stop; do not install.

### P2.2 The preflight (recommended on a Mac, an AMD or Intel GPU, or when unsure; optional elsewhere)

The preflight builds a throwaway venv in a scratch folder, installs PyTorch from the channel this machine needs, checks
that `sqlite-vec` loads, embeds a fixed set of texts on the CPU and on the chosen accelerator, compares them with
reference vectors, deletes the scratch folder, and writes **one file, `preflight.json`** (`~/voidloom/install/preflight.py`).
It installs nothing into the home. It takes about ten minutes, so run it in the background. `--preflight` must be the
FIRST argument:
```bash
. ~/.webdev-workbench-setup/shell.sh && PY="${WIZARD_PYTHON_BIN:-$(command -v python3)}"; [ -x "$HOME/miniforge3/envs/voidloom/bin/python3" ] && PY="$HOME/miniforge3/envs/voidloom/bin/python3"; rm -f ~/.webdev-workbench-setup/preflight.rc; mkdir -p ~/.webdev-workbench-setup/preflight_work && bash ~/voidloom/install.sh --preflight --python "$PY" --workdir ~/.webdev-workbench-setup/preflight_work --out ~/.webdev-workbench-setup/preflight.json > ~/.webdev-workbench-setup/preflight.log 2>&1; echo "rc=$?" > ~/.webdev-workbench-setup/preflight.rc
```
On a machine with two or more NVIDIA GPUs where the person chose the GPU, put `CUDA_VISIBLE_DEVICES=<their jobs card>`
right before `bash ~/voidloom/install.sh` in that line, so the test never touches the monitor's card. Where they chose
the CPU, put `CUDA_VISIBLE_DEVICES=` (empty) there instead.

The rc is `0` GREEN, `1` RED (the log's `verdict:` line and the file name the first failure), `2` the preflight itself
could not run (the log says why).
- **GREEN:** continue.
- **RED naming the accelerator** (a step ending in `-mps`, `-cuda`, `-rocm` or `-xpu`): the install will still work; if
  the device proof fails again during the install, Voidloom moves the brain to the CPU by itself, says so, and records
  `FAILED-ON-THIS-MACHINE`. Tell the person, and continue.
- **RED naming `sqlite-extensions`:** the Python cannot load SQLite extensions (Apple's own Python): fix P1's Mac route.
- **RED naming `venv`, `pip`, `torch` or `stack`:** read the error line; it is usually the P1 venv box or the network.
  Fix it and run the preflight again.
- **RED naming none of these:** continue to the install, and tell the person the exact reason line. A healthy machine
  can read RED on a check nobody anticipated; what counts is the real install's verdict (P2.5) and the doctor (P2.6).

The file is for the person's own benefit; nothing is sent anywhere. If they ever want to share it (for example when
asking for help in a public issue), share the redacted copy, which replaces their home folder with `~` and their user
name with `<user>`:
```bash
. ~/.webdev-workbench-setup/shell.sh && python3 "$PKG/bin/redact_preflight.py" ~/.webdev-workbench-setup/preflight.json ~/.webdev-workbench-setup/preflight_to_share.json; echo "rc=$?"
```
It prints `redacted <n> string(s); wrote …` and never a value. Write the verdict (GREEN or RED and its reason) into
`answers.md`.

### P2.3 What the thinker answer means for the install

- **e) Not now:** `--thinker off` is in `install_flags.sh`. Nothing thinks overnight; the simple nightly routines stay.
- **f) Other:** the model must already be running. The installer proves it with two test requests before recording
  it; if the proof fails, the install is refused and touches nothing. Ask the person whether to fix the model or
  answer e) for now.
- **a) Claude, b) Codex, c) Kimi, d) Gemini:** each needs a one-time sign-in that only the person can do at a real
  terminal (a key typed twice into a hidden prompt for Claude and Kimi; a browser sign-in for Codex and Gemini), and a
  key must never pass through this chat. Without a terminal the installer cannot run that sign-in: it proves the answer
  with `--no-login` (`install.sh` line 2172), so on a new machine the proof fails and the whole install is refused. So
  **do not pass `--thinker` for a, b, c or d.** Without the flag the installer records nothing and prints
  `Thinker:      not asked (no terminal) and no timer that thinks is armed`. That is expected. After P2.6:
  > 🙋 **HUMAN:** "In your own terminal, run `~/.local/bin/voidloom thinker set claude` (or `codex`, `kimi`,
  > `gemini`). It does the one sign-in step, proves it with a small test question, and records it. The steps for each
  > model are in `~/voidloom/docs/OVERNIGHT_THINKER_SETUP.md`: Part C (Claude), Part B (Codex), Part A (Kimi),
  > Part E (Gemini)."
  >
  > Then check it yourself: `. ~/.webdev-workbench-setup/shell.sh && cd ~ && voidloom thinker status`.

  The company's program must be on the computer first (`claude`, `codex`, `kimi`, or `agy` for Gemini); if it is
  missing, the person installs it with the company's own command from OVERNIGHT_THINKER_SETUP.md, "Get the program
  first" (never with sudo). Gemini on Linux/WSL also needs the bubblewrap sandbox (`sudo apt install bubblewrap`, the
  person's act). Tell them, from Part E, that Google may use what the brain sends overnight to improve its products.

### P2.4 Read the usage, then the dry run

```bash
. ~/.webdev-workbench-setup/shell.sh && bash ~/voidloom/install.sh --help > ~/.webdev-workbench-setup/install_help.txt 2>&1; echo "rc=$?"
. ~/.webdev-workbench-setup/shell.sh && bash ~/.webdev-workbench-setup/install_flags.sh --dry-run > ~/.webdev-workbench-setup/install_dry.log 2>&1; echo "rc=$?"
. ~/.webdev-workbench-setup/shell.sh && bash ~/.webdev-workbench-setup/install_flags.sh --print-write-set > ~/.webdev-workbench-setup/write_set.txt 2>&1; echo "rc=$?"
```
Read `install_help.txt` (its Usage block explains every flag used here), then `install_dry.log`. Look for:
- **`Compute:`** and the sentence under it: the machine (chip and RAM), the backend (`cuda`, `mps`, `cpu`, …), its
  label (**PROVEN** or **SUPPORTED-UNPROVEN**), where PyTorch comes from, and whether the reranker is on, with the reason;
- **`Thinker:`**: the person's answer, or `not asked (no terminal)` for a to d;
- `No brain on this machine yet, and none bundled: starting a fresh one`;
- **`REFUSED`** anywhere: the line says why and that nothing was touched. Fix the cause (usually a missing or
  contradicting flag) in `install_flags.sh` and dry-run again.

The dry run's closing banner says `Session-start hook wired: no` even with `--wire-hooks`, because a dry run wires
nothing; the real run says `yes`. The dry run also cannot tell whether a venv can be built; P0.2 and the preflight can.
`write_set.txt` lists every path outside `~/.claude` the install may touch. Tell the person, in two or three sentences,
what it writes: `~/.claude/memory` (the brain and its code), `~/.claude/skills/persona-forge` and
`~/.claude/skills/memory-operator`, the `voidloom` command in `~/.local/bin`, `~/.voidloom/` (settings), and, with the
hook answer yes, one entry in `~/.claude/settings.json` (backed up first).

**PASS P2.4:** `rc=0` on all three, no `REFUSED` in `install_dry.log`, and the person has heard what will be written.

### P2.5 The real install (background, logged, rc file)

Run this with your Bash tool's **background** option:
```bash
. ~/.webdev-workbench-setup/shell.sh && rm -f ~/.webdev-workbench-setup/install.rc && bash ~/.webdev-workbench-setup/install_flags.sh > ~/.webdev-workbench-setup/install.log 2>&1; echo "rc=$?" > ~/.webdev-workbench-setup/install.rc
```
Check progress every minute or two by reading the end of the log (`tail -n 15 ~/.webdev-workbench-setup/install.log` is
fine for reading). It is finished when `install.rc` exists. What you will see:
- a line starting `pip next:`, then a quiet stretch while pip downloads (minutes; quiet is normal);
- possibly a Hugging Face warning that "a new version of the following files was downloaded" from `nomic-ai/…`: the CPU
  embedder ships its own model code from its official repository; it is expected;
- **the device proof**: before embedding anything the installer checks the chosen device against reference vectors. If
  it computes wrong, it prints one line starting `SAFETY:`, records `WIZARD_ACCELERATOR=cpu`, proves the CPU instead and
  writes `proof_label=FAILED-ON-THIS-MACHINE` into `~/.claude/memory/INSTALL_RECORD`. That is a correct, slower brain,
  not a failure. Tell the person;
- **success at Tier 1:** a line starting `  Tier 1 VERIFIED`, then `self_check PASSED`, then the
  `MANDATORY NEXT STEP: open Claude Code in any folder and type /persona-forge` banner (that is P5; not yet);
- **success at Tier 0:** a box starting `Tier 0 is ACTIVE` with a `reason:` line, then `self_check PASSED`.

```bash
. ~/.webdev-workbench-setup/shell.sh && cat ~/.webdev-workbench-setup/install.rc; grep -c 'self_check PASSED' ~/.webdev-workbench-setup/install.log; grep -m 1 -o 'Tier 1 VERIFIED\|Tier 0 is ACTIVE' ~/.webdev-workbench-setup/install.log; grep -m 1 'Session-start hook wired' ~/.webdev-workbench-setup/install.log
```

**PASS P2.5:** `rc=0`; the `self_check PASSED` count is at least `1`; one tier line; and the hook line reads `yes`
(or `no` when the person declined). Any other rc: read the last 40 lines, fix the named cause, and re-run P2.5. The
installer is idempotent and keeps the brain (`brain DB already exists …; leaving it in place (idempotent)`).

> 🙋 **HUMAN: if the install fails twice:** give them the exact failing line and ask whether to continue at Tier 0
> (append `--tier0-only` before `"$@"` in `install_flags.sh`) or to stop.

### P2.6 Check the brain (from the home folder)

```bash
. ~/.webdev-workbench-setup/shell.sh && cd ~ && voidloom doctor --json > ~/.webdev-workbench-setup/doctor.json 2> ~/.webdev-workbench-setup/doctor.err; echo "rc=$?"
. ~/.webdev-workbench-setup/shell.sh && python3 - ~/.webdev-workbench-setup/doctor.json <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))["data"]
c = d.get("checks", {}); e = c.get("embedding_coherence") or {}; g = c.get("gpu_pin") or {}
a = c.get("accelerator") or {}; r = c.get("reranker") or {}
print("brain_healthy  :", d.get("brain_healthy"))
print("db_path        :", c.get("db_path"))
print("embedding      : table", e.get("recorded_table"), "|", e.get("reason") or "")
print("accelerator    :", a.get("line") or a.get("error") or a)
print("reranker       :", r.get("line") or r.get("error") or r)
print("gpu pin        :", g.get("not_used") or g.get("value"), "|", g.get("line") if g.get("refused") else "")
print("persona        :", (d.get("persona") or {}).get("status"))
print("thinker        :", (d.get("thinker") or {}).get("line"))
print("hook states    :", d.get("hook_states"))
print("models_present :", c.get("models_present"))
print("promise_healthy:", d.get("promise_healthy"))
print("warnings       :", len(d.get("warnings") or []), d.get("warnings") or "")
PY
```

The line that decides this step is **`brain_healthy  : True`**, with `db_path` under the home folder
(`…/.claude/memory/claude_memory.db`). These are expected on a new install and are **not** failures:
- `promise_healthy: False` and hook states `{'claude-code': 'INSTALLED_NEVER_FIRED', 'codex': 'NOT_INSTALLED'}`: no
  session has started since the install;
- `persona: absent`: the forge is P5;
- at Tier 0: `embedding : table None | the brain records no active_embedding_table`, and `models_present: False`;
- `accelerator`: the person's choice and its label; `reranker`: `OFF` on any CPU machine or under 15.0 GiB of RAM.

**The hook-free route** (only if the person said no to the hook): the instruction block carries the same guidance for
tools without hooks. Plan first, then apply after the person says yes:
```bash
. ~/.webdev-workbench-setup/shell.sh && cd ~ && voidloom instructions install --dry-run > ~/.webdev-workbench-setup/instructions_plan.txt 2>&1; echo "rc=$?"
. ~/.webdev-workbench-setup/shell.sh && cd ~ && voidloom instructions install --yes > ~/.webdev-workbench-setup/instructions.log 2>&1; echo "rc=$?"
```
It writes a marked block into `~/.agents/AGENTS.md` (creating it if absent) and an import line into
`~/.claude/CLAUDE.md`. If the hook was wanted but `hook states` reads `NOT_INSTALLED`, run
`voidloom hooks install --platform claude` (the plan), then the same with `--yes`.

**PASS P2.6:** `brain_healthy  : True` and `db_path` under the home folder; the hook (or the instruction block) is in
place, or the person declined both.

### P2.7 First recall

```bash
. ~/.webdev-workbench-setup/shell.sh && cd ~ && voidloom recall --query "how do I use this memory system" --top-k 3 > ~/.webdev-workbench-setup/recall_p2.txt 2>&1; echo "rc=$?"
```
Expect `[ok] voidloom recall` and Voidloom's own onboarding memories. At Tier 0 the output carries a line starting
`⚠ DEGRADED`, naming tier 0: the honest label for keyword-only recall, not an error. `voidloom bootstrap` prints what the
machine has (OS, GPU, brain, models) and loads nothing; its `tier` field is the machine's hardware tier, so it can say
`gpu` on a brain the person put on the CPU.

**PASS P2.7:** `rc=0` and the file lists memories. Write the tier you reached (0 or 1) into `answers.md`.

### P2.8 Nightly routines (only if the person said yes to question 5)

The timers that run the nightly routines (and the thinker) are armed by re-running the install with `--with-crons`.
**Order matters:** the thinker answer must be recorded first, or the install refuses (`install.sh`: an install that arms
thinking timers with no recorded answer is refused, rc 2, before anything is touched).
1. Confirm the record: `. ~/.webdev-workbench-setup/shell.sh && cd ~ && voidloom thinker status`. For e) or f) the
   install recorded it. For a) to d), the person's `voidloom thinker set …` (P2.3) did.
2. Check that the computer can run user timers:
   - **Linux:** `systemctl --user show-environment > ~/.webdev-workbench-setup/systemd.txt 2>&1; echo "rc=$?"`. `rc=0`
     means user timers work. They run only while the person is logged in, unless they run
     `loginctl enable-linger $USER` in their own terminal.
   - **WSL:** the same check. If it fails, WSL is running without systemd.
     > 🙋 **HUMAN (sudo):** "Add these two lines to `/etc/wsl.conf` (`sudo nano /etc/wsl.conf`): `[boot]` and
     > `systemd=true`. Then in Windows PowerShell run `wsl --shutdown`, reopen Ubuntu and Claude Code."
     Then repeat the check. This WSL step is SUPPORTED-UNPROVEN in this guide.
   - **macOS:** the timers are launchd agents in `~/Library/LaunchAgents`; no check needed (SUPPORTED-UNPROVEN here).
3. Add `--with-crons` before `"$@"` in `install_flags.sh`. Dry-run it (P2.4) and read the `DRY-UNIT:` lines, then run it
   for real as in P2.5.
4. Check: Linux/WSL
   `systemctl --user list-timers 'wizard-library-*' --no-pager > ~/.webdev-workbench-setup/timers.txt 2>&1; echo "rc=$?"`;
   macOS `launchctl list > ~/.webdev-workbench-setup/timers.txt 2>&1; echo "rc=$?"`, then look for labels starting
   `voidloom.`. Nine jobs are armed by default (Voidloom README, "Scheduled jobs"); `~/voidloom/docs/FIRST_NIGHT.md`
   says what each one does and sends.

If the person said "not now", tell them plainly: nothing runs at night until this step is done.

### Upgrading Tier 0 to Tier 1 (later, any time)

1. Fix the cause the Tier 0 box named (usually the P1 venv box).
2. If an earlier try left a half-built `~/.claude/memory/venv` and the retry reports *venv creation failed*, delete that
   folder (it holds no memories; the brain is `claude_memory.db` beside it).
3. Remove `--tier0-only` from `install_flags.sh`. Dry-run (P2.4), then run P2.5 again.
4. Expect `brain DB already exists …; leaving it in place (idempotent)` and finally a `Tier 1 VERIFIED` line. The
   answers already recorded are reused.
5. Re-run P2.6, then P3.3 and P3.4 (the vectors and the battery).

**PASS P2:** P2.1, P2.4, P2.5, P2.6 and P2.7 each passed; P2.8 is done or the person chose "not now".

---

## P3. The web-craft memory pack

`02_memory/PACK_MANIFEST.md` states the pack's file name, version and entry count on its first lines. The load is an
**anchor delta** (`claude_memory_lite.py`, `load-seed`): only new and changed entries are written, a changed entry's
older memory is archived (never deleted), and loading again adds zero.

### P3.1 Find the pack, then plan (writes nothing)

```bash
. ~/.webdev-workbench-setup/shell.sh && ls "$PKG"/02_memory/*.json | grep -v '/recall_battery\.json$' > ~/.webdev-workbench-setup/pack_path; wc -l < ~/.webdev-workbench-setup/pack_path; cat ~/.webdev-workbench-setup/pack_path
. ~/.webdev-workbench-setup/shell.sh && PYB="$HOME/.claude/memory/venv/bin/python3"; [ -x "$PYB" ] || PYB=python3; "$PYB" ~/.claude/memory/organs/claude_memory_lite.py load-seed --file "$(cat ~/.webdev-workbench-setup/pack_path)" --plan > ~/.webdev-workbench-setup/pack_plan.json 2> ~/.webdev-workbench-setup/pack_plan.err; echo "rc=$?"
```
The first line must print `1` and the pack's path (the file `PACK_MANIFEST.md` names). Read every load with this reader
(change the file name each time):
```bash
python3 - ~/.webdev-workbench-setup/pack_plan.json <<'PY'
import json, sys
t = open(sys.argv[1]).read()
try:
    d = json.loads(t)
except ValueError:
    print("not JSON; first lines:"); print("\n".join(t.splitlines()[:40])); raise SystemExit(1)
n = lambda k: len(d.get(k) or []) if isinstance(d.get(k), list) else d.get(k)
print("status", d.get("status"), "| mode", d.get("mode"), "| version", d.get("seed_pack_version"), "| entries", d.get("entries"),
      "| new", n("new"), "| changed", n("changed"), "| present", d.get("present"), "| held_untagged", n("held_untagged"),
      "| skipped_invalid", d.get("skipped_invalid"), "| total_now", d.get("total_memories_now"))
PY
```
**PASS P3.1:** `status ok | mode plan`, `entries` equal to PACK_MANIFEST's figure, `skipped_invalid 0`, and on a first
load `new` equal to `entries`.

### P3.2 Load, then load again

The same command without `--plan`, into `pack_load.json`; then once more into `pack_reload.json`:
```bash
. ~/.webdev-workbench-setup/shell.sh && PYB="$HOME/.claude/memory/venv/bin/python3"; [ -x "$PYB" ] || PYB=python3; "$PYB" ~/.claude/memory/organs/claude_memory_lite.py load-seed --file "$(cat ~/.webdev-workbench-setup/pack_path)" > ~/.webdev-workbench-setup/pack_load.json 2> ~/.webdev-workbench-setup/pack_load.err; echo "rc=$?"
. ~/.webdev-workbench-setup/shell.sh && PYB="$HOME/.claude/memory/venv/bin/python3"; [ -x "$PYB" ] || PYB=python3; "$PYB" ~/.claude/memory/organs/claude_memory_lite.py load-seed --file "$(cat ~/.webdev-workbench-setup/pack_path)" > ~/.webdev-workbench-setup/pack_reload.json 2> ~/.webdev-workbench-setup/pack_reload.err; echo "rc=$?"
```
**PASS P3.2:** the load reads `mode anchor-delta`, `skipped_invalid 0`, `new` equal to `entries`; the reload reads
`new 0 | changed 0 | present <entries>`.

> 🙋 **HUMAN: stop and ask if** the load reports `skipped_invalid` above 0, `held_untagged` above 0, or a mode other
> than `anchor-delta`. Give the person the exact line.

### P3.3 Vectors (Tier 1 only; background, rc file)

At Tier 0, skip this step: keyword recall works on the pack at once. At Tier 1 the pack's memories need vectors for
match-by-meaning recall. `embed_backfill.py` is idempotent (it touches only memories with no vector) and refuses rather
than guessing if the brain declares no embedding tier. On a CPU it takes minutes to tens of minutes, depending on the
pack size. Run it with the **background** option:
```bash
. ~/.webdev-workbench-setup/shell.sh && rm -f ~/.webdev-workbench-setup/backfill.rc && ~/.claude/memory/venv/bin/python3 ~/.claude/memory/organs/embed_backfill.py ~/.claude/memory/claude_memory.db > ~/.webdev-workbench-setup/backfill.log 2>&1; echo "rc=$?" > ~/.webdev-workbench-setup/backfill.rc
```
Done when `backfill.rc` exists. Exit codes (`embed_backfill.py`, `main`): `0` ok, `1` incomplete (some memories failed:
re-run it; it continues where it stopped), `3` refused (nothing written, nothing broken: the log names why, for example
`encoder_unavailable` or `tier_unresolved`). `shell.sh` exports the env file's card settings, so on a two-GPU machine
the job runs on the person's jobs card.

**PASS P3.3:** `rc=0` and the log line `  unembedded  : <n> before, 0 after`. Then re-run the P2.6 reader:
`embedding : table <name>` (no "records no active_embedding_table").

### P3.4 The recall battery

```bash
. ~/.webdev-workbench-setup/shell.sh && cd ~ && python3 "$PKG/02_memory/run_battery.py" > ~/.webdev-workbench-setup/battery.log 2>&1; echo "rc=$?"
```
It runs one batched recall over every phrase in `02_memory/recall_battery.json` and checks that each phrase finds its
memory in the top 5. Flags (`run_battery.py --help`): `--top-k` (default 5), `--min-rate` (default 0.95), `--db`,
`--battery`, `--gate-tier0`. Exit codes: `0` pass, `1` below the rate, an expected memory missing (load the pack
first), or a Tier 1 brain with any memory still lacking a vector (finish P3.3); `2` `voidloom` could not run, or it reads
a different brain than `--db`.
- **Tier 1:** it gates. `rc=0` means at least 95% of the phrases found their memory.
- **Tier 0:** it prints its numbers as information and ends `Tier 0: informational only.`; `rc=0` unless a memory is
  missing. Keyword recall matches every word of a phrase, so long natural phrases often find nothing at Tier 0; that is
  expected, not a failure.

**PASS P3.4:** `rc=0` and the `TOTAL <k>/<n> = <rate> (top-5, tier <t>)` line; at Tier 1 the rate is 95% or more.
Report any `FAIL` lines to the person.

### P3.5 First pack recall

```bash
. ~/.webdev-workbench-setup/shell.sh && cd ~ && voidloom batch-recall --items '["deploy an Astro site preview branch", "keep secrets out of a git repository"]' --top-k 3 --json > ~/.webdev-workbench-setup/first_recall.json 2> ~/.webdev-workbench-setup/first_recall.err; echo "rc=$?"
```
Read the results in full: this is what the brain now knows about the work ahead. (At Tier 0, query with words that
appear in the memories.)

**PASS P3:** P3.1, P3.2 and P3.4 passed; at Tier 1 also P3.3.

---

## P4. Skills, reasoning, automations and tools

```bash
. ~/.webdev-workbench-setup/shell.sh && bash "$PKG/bin/install_skills.sh" --help > ~/.webdev-workbench-setup/skills_help.txt 2>&1; echo "rc=$?"
. ~/.webdev-workbench-setup/shell.sh && bash "$PKG/bin/install_skills.sh" --dry-run > ~/.webdev-workbench-setup/skills_dry.log 2>&1; echo "rc=$?"
```
Read the help, then the dry run. It prints one `[workbench] [dry] <source> -> <target>` line per placement (with the
backup it would make when something of the same name already exists) and ends
`[workbench] dry run: <n> placements + the CLAUDE.md block. Nothing changed.` Show the person the list. It places:
- the skills from `03_skills/` (including `scroll-journey`) and the reasoning skills from `04_reasoning/` into
  `~/.claude/skills/`;
- the `/inner-council` command from `04_reasoning/commands/` into `~/.claude/commands/`;
- the design-loop agents into `~/.claude/agents/`;
- the three website automations, the guides from `09_guides/`, the web tools and the nexus tools into
  `~/.local/share/webdev-workbench/` (`automations/`, `guides/`, `web_tools/`, `nexus_tools/`);
- the short block from `08_claude_md/webdev_workbench_block.md` into `~/.claude/CLAUDE.md`, between
  `WEBDEV WORKBENCH` markers.

It wires no hook into `~/.claude/settings.json` (Voidloom's own installer owns the session hook). Exit codes
(`--help`): `0` done, `2` unknown argument, `3` Voidloom not found (finish P2 first), `4` package incomplete, `5` an
install is already recorded (run `--uninstall` first), `6` the undo could not finish.

After the person says yes:
```bash
. ~/.webdev-workbench-setup/shell.sh && bash "$PKG/bin/install_skills.sh" > ~/.webdev-workbench-setup/skills.log 2>&1; echo "rc=$?"
```
It copies (never symlinks). Anything already at a target is MOVED to `~/.webdev-workbench/backups/<time>/` (outside
`~/.claude/skills`, so Claude Code never loads a backup as a skill), and every change is recorded in
`~/.webdev-workbench/uninstall_manifest.jsonl`; `--uninstall` puts everything back (preview it first with
`--uninstall --dry-run`).

Count the skills instead of trusting a typed number:
```bash
. ~/.webdev-workbench-setup/shell.sh && echo "package skills: $(find "$PKG/03_skills" -mindepth 1 -maxdepth 1 -type d | wc -l) in 03_skills; before=$(wc -l < ~/.webdev-workbench-setup/skills_before.txt) now=$(find ~/.claude/skills -mindepth 1 -maxdepth 1 -type d | wc -l)"
```
`now` should be `before`, plus Voidloom's two (`memory-operator`, `persona-forge`), plus the `ok  ` lines in
`skills.log` that end in a folder directly under `~/.claude/skills/`, minus any of those that replaced a folder that
already existed (it was moved to the backups folder, not added).

> 🙋 **HUMAN:** "Please start a new Claude Code session (type `/exit`, then `claude` again in the package folder), so
> the new skills, commands and hooks load. Then say: *Continue the workbench setup from SETUP_GUIDE.md.*"

**PASS P4:** `rc=0`, and `skills.log` ends with `[workbench] undo record: …/.webdev-workbench/uninstall_manifest.jsonl (<n> steps). …`
and `[workbench] DONE. Start a NEW Claude Code session …`. In the **new**
session: the session start shows Voidloom's preamble (if the hook was wired), the skills list includes the `webgl-*`
skills and `scroll-journey`, and `/inner-council` resolves.

---

## P5. The Persona Forge (a persona of the person's own)

Voidloom ships **no** persona and this package ships none. The person designs one in a short conversation (about ten
minutes), and you bring it to life. "Not now" is allowed: new sessions keep offering the forge until it is done or
declined (`voidloom persona decline`, undone with `--undo`).

**The name rule.** The persona's name must not be **Backus, Cassian or Wren** (the three website automations' personas,
installed in P4) or **Orin, Vael, Dessa or Kael-Em** (the Inner Council's voices), or "act as Wren" becomes ambiguous.
The forge itself refuses only existing skill folder names, names starting `council-`, and a short reserved list
(claude, anthropic, voidloom, persona, persona-forge, council, memory-operator, wizard-library:
`organs/voidloom_persona.py`, `RESERVED_NAMES`), so the first check is yours.

1. > 🙋 **HUMAN:** "Type `/persona-forge` (or accept the offer at the start of this session). Pick any name except
   > Backus, Cassian, Wren, Orin, Vael, Dessa or Kael-Em."

   The forge is plain files: `~/.claude/skills/persona-forge/SKILL.md` with `QUESTIONNAIRE.md`, `TEMPLATES/` and
   `validate_persona.py` beside it. It explains the calm baseline every persona starts from, asks short multiple-choice
   rounds, shows a one-screen card, revises until the person approves, writes the files, runs its validator and declares
   the persona (`voidloom persona declare`).
2. Verify:
   ```bash
   . ~/.webdev-workbench-setup/shell.sh && cd ~ && voidloom persona status > ~/.webdev-workbench-setup/persona.txt 2>&1; echo "rc=$?"
   ```

**PASS P5:** `persona.txt` reads `persona: forged` with the chosen name (or the person chose "not now", written into
`answers.md`). The next new session's preamble starts `=== <NAME> SESSION START (Voidloom memory brain) ===`.

---

## P6. GitHub and a host (only if the person said "now" to question 8)

The detailed, assume-nothing steps are in `09_guides/`. Read the relevant guide in full first, then walk the person
through it; the browser steps and sign-ins are theirs.

1. **Keys first, the safe way.** `09_guides/SERVICES.md`, Section A: the one private key file
   `~/.config/webtools/keys.env` (mode 600; every workbench web tool reads it, parsed and never sourced) and the helper
   `~/.config/webtools/with_keys.py`, which gives any other command a key without ever showing it. The person types each key in their own terminal. You check presence without reading a value:
   ```bash
   . ~/.webdev-workbench-setup/shell.sh && ls -l ~/.config/webtools/keys.env && python3 ~/.config/webtools/with_keys.py --check CLOUDFLARE_API_TOKEN,CLOUDFLARE_ACCOUNT_ID; echo "rc=$?"
   ```
   (For Vercel: `--check VERCEL_TOKEN`.) The mode reads `-rw-------`, each name reads `present`, `rc=0`. A key is
   optional on both hosts: each guide's git-integration route deploys with no key on this computer.
2. **GitHub:** `09_guides/GITHUB_SETUP.md` (account, two-factor, sign-in or SSH key, a private repository, the
   `.gitignore`, secret scanning). Run this check only after the person has finished `GITHUB_SETUP.md` Step 4,
   including the fingerprint comparison in their own terminal; never accept a host key on their behalf. Then check
   the SSH sign-in yourself:
   ```bash
   . ~/.webdev-workbench-setup/shell.sh && ssh -o StrictHostKeyChecking=yes -T git@github.com > ~/.webdev-workbench-setup/ssh.log 2>&1; echo "rc=$?"
   ```
   Success is the text `Hi <user>! You've successfully authenticated` in `ssh.log`; the exit code is `1` even then,
   because GitHub offers no shell. `Host key verification failed` (exit code `255`) means the fingerprint step was
   not done yet: send the person back to Step 4; do not loosen host checking.
3. **The host:** `09_guides/DEPLOY_CLOUDFLARE.md` or `09_guides/DEPLOY_VERCEL.md`, as the person chose. Spending caps
   are set before anything that could bill (each guide says where).

**PASS P6:** `ssh.log` greets the person by username; the host account exists with two-factor on; the spending setting
the guide asks for is in place; and the key check printed `present` for the host's names (or the person chose the
git-integration route with no key).

---

## P7. A first real job: a one-page site for an invented bakery

This proves the whole chain on something harmless: an invented business, "Crumb & Crust Bakery". No real company, no
real domain.

1. Find the first-build automation the P4 install placed:
   ```bash
   . ~/.webdev-workbench-setup/shell.sh && ls ~/.local/share/webdev-workbench/automations/client-site-first-build/comprehensive_guide.md
   ```
   Read that `comprehensive_guide.md` (the first build automation's persona is Backus) in pages, as its own
   startup steps say.
2. > 🙋 **HUMAN:** "Ask me: *Make a one-page site for an invented bakery called Crumb & Crust Bakery, in
   > ~/Sites/bakery-site, and deploy a preview.*" (If the host was set to "later", leave out "and deploy a preview".)
3. Run the automation as its guide says, for a website-only first build, with the person's answers to its questions.
   The site lives in `~/Sites/bakery-site`. It builds locally first:
   ```bash
   . ~/.webdev-workbench-setup/shell.sh && . "$HOME/.nvm/nvm.sh" && cd ~/Sites/bakery-site && npm run build > ~/.webdev-workbench-setup/bakery_build.log 2>&1; echo "build rc=$?"
   ```
4. **With a host (P6 done):** a git repository, a branch other than `main` (for example `first-preview`), a push, and
   the host builds a preview link (the deploy guide, "preview links per branch"). Hand the person the **branch** link,
   not a one-off version link.
   > 🙋 **HUMAN:** "Here is your first preview link: <link>. Please open it (sign in if the guide set up preview
   > protection) and tell me whether the page loads."
5. **Without a host:** stop at the local build and a local look (`npm run preview`, then open the address it prints;
   stop it with Ctrl-C in your own terminal). That is this run's first hand-off.

**PASS P7:** `build rc=0`, and either the person opened the preview link and saw the page, or (no host) the local
preview showed it. Nothing went to `main` and nothing was spent.

---

## P8. Done check, updating later, and removing

### P8.1 Done check

| # | Check | Expect |
|---|---|---|
| 1 | P2.1 pin | `7cfa8e610997e0c627c48114266238a425858d72` |
| 2 | P2.6 doctor reader (from `~`) | `brain_healthy  : True`, `db_path` under the home folder |
| 3 | Tier (from `answers.md`) | Tier 1 with `unembedded … 0 after`, or Tier 0 with its reason written down |
| 4 | pack reload (P3.2) | `new 0` |
| 5 | battery (P3.4) | `rc=0` (at Tier 1, 95% or more) |
| 6 | `voidloom persona status` | `forged` (not one of the seven reserved names), or "not now" recorded |
| 7 | P4 install | `DONE.`, undo record named; `/inner-council` resolves in a new session |
| 8 | thinker | `voidloom thinker status` matches the person's answer (or a to d awaiting their `thinker set`) |
| 9 | timers (if question 5 was yes) | `timers.txt` lists `wizard-library-*` timers (Linux/WSL) or `voidloom.*` labels (Mac) |
| 10 | two or more GPUs, GPU chosen | `grep -n '^WIZARD_CUDA_DEVICE=\|^WIZARD_DISPLAY_INDEX=' ~/.voidloom/wizard-library-env` shows the person's two answers |
| 11 | keys | `with_keys.py --check` prints `present`; the key file is `-rw-------`; no key in git, chat or memory |
| 12 | first job | `build rc=0`; the preview (or local preview) was seen |

**PASS P8.1:** every row holds, or its failure is written into `answers.md` and told to the person.

> 🙋 **HUMAN:** give them a short summary in plain words: what is installed, the tier reached, anything that failed and
> what it means, and where the guides are (`~/.local/share/webdev-workbench/guides/`, the same files as `09_guides/`).

Finish with one memory in the person's brain:
```bash
. ~/.webdev-workbench-setup/shell.sh && cd ~ && voidloom store --content "[OBJECTIVE] Web-dev workbench installed <date> at Tier <0|1>: <what passed, anything that failed> [SUBJECTIVE/WHY] <what was hard, what to remember>" --category campaign_state --importance 0.85 --tags "workbench,setup"
```

### P8.2 Updating Voidloom later

The clone was pinned to a tested commit, so it sits on a "detached HEAD": a bare `git pull` there fails with "You are
not currently on a branch". Back up first, move to `main`, then pull and re-run the same installer flags (Voidloom
README, "Back up and upgrade"):
```bash
. ~/.webdev-workbench-setup/shell.sh && cd ~ && python3 -c "import sqlite3, os; src = sqlite3.connect(os.path.expanduser('~/.claude/memory/claude_memory.db')); dst = sqlite3.connect(os.path.expanduser('~/voidloom-backup.db')); src.backup(dst); dst.close(); os.chmod(os.path.expanduser('~/voidloom-backup.db'), 0o600)"; echo "backup rc=$?"
. ~/.webdev-workbench-setup/shell.sh && git -C ~/voidloom checkout main > ~/.webdev-workbench-setup/update.log 2>&1 && git -C ~/voidloom pull --ff-only >> ~/.webdev-workbench-setup/update.log 2>&1; echo "rc=$?"; git -C ~/voidloom log --oneline -1
. ~/.webdev-workbench-setup/shell.sh && bash ~/.webdev-workbench-setup/install_flags.sh --dry-run > ~/.webdev-workbench-setup/update_dry.log 2>&1; echo "rc=$?"
```
Read `~/voidloom/CHANGELOG.md` and the dry run, then run P2.5 again (the brain is kept; schema changes only ever add),
then P2.6 and P3.4. Answers recorded before (thinker, approvals, GPU) are reused; the thinker is proven again, not asked
again. Updating moves past the commit this package was tested on: the battery (P3.4) is how to see that the pack still
recalls well.

### P8.3 Removing

1. **The workbench** (skills, automations, tools, the CLAUDE.md block): dry-run the undo, then run it.
   ```bash
   . ~/.webdev-workbench-setup/shell.sh && bash "$PKG/bin/install_skills.sh" --uninstall --dry-run > ~/.webdev-workbench-setup/uninstall_dry.log 2>&1; echo "rc=$?"
   . ~/.webdev-workbench-setup/shell.sh && bash "$PKG/bin/install_skills.sh" --uninstall > ~/.webdev-workbench-setup/uninstall.log 2>&1; echo "rc=$?"
   ```
2. **Voidloom** (Voidloom README, "Uninstall"): `bash ~/voidloom/uninstall.sh` previews and changes nothing;
   `bash ~/voidloom/uninstall.sh --yes` removes the scheduled jobs, the hooks and instruction blocks, the `voidloom`
   command and the installed code, and **keeps the memories** and the env file. Deleting the memories too
   (`--yes --remove-brain`) asks the person to type a confirmation phrase, so it is theirs to run in their own
   terminal. It never touches model caches, a forged persona, or the AI tools themselves.
3. **Keys:** revoke each key at its vendor first, then delete `~/.config/webtools/keys.env`
   (`09_guides/SERVICES.md`, "Removing everything").
4. **This setup's notes:** `~/.webdev-workbench-setup/` holds no secrets; the person may delete it when done.
