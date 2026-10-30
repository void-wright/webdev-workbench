# START HERE: the Voidwright web-dev workbench

*A free release by Voidwright.*

**To the person.** This package turns your computer into a web-development workbench for your **AI coding agent**
(setup is written for Claude Code, and Codex works too; the README's "Which agents it runs on" has the details):
- **Voidloom**, a memory brain for coding agents. It remembers what you and your agent learn, so later sessions can recall it.
  It is downloaded from its public repository during setup (it is not inside this package).
- **A memory pack of web craft**, loaded into that brain, so your agent starts out knowing how modern sites are built,
  checked and deployed.
- **Skills, reasoning aids and three website automations**: designing and building a first site, looking after a site,
  and running a resource library, plus a scroll-journey skill for scroll-driven pages.
- **Plain guides** for GitHub and for putting a site online with Cloudflare or Vercel.

Everything runs on **your own** computer and **your own** accounts. Nothing is sent to the people who made this
package. **You do not need any keys at all:** every service the skills can use has a **manual route**, where your
agent writes the prompt and settings into a handoff file, you make the thing in the vendor's website, and you drop the file
back. If you do choose a paid service, you set its spending limit in the vendor's own website first.

**Your few jobs:**
1. Get the package into your home folder. The simplest way, in a terminal:
   `git clone https://github.com/void-wright/webdev-workbench.git ~/webdev-workbench-package`.
   Without git, download the repository as a zip from its GitHub page (Code, then Download ZIP) and unzip it to
   `~/webdev-workbench-package`: `unzip <the zip file> -d ~` and rename the folder, or
   `python3 -m zipfile -e <the zip file> ~`. On Windows, install WSL2 Ubuntu first and do this inside Ubuntu (your
   agent explains this at the start of the setup if you need it).
2. Start your coding agent **in that folder** (or start it anywhere and tell it where the folder is) and say:
   > "Read 00_START_HERE.md and SETUP_GUIDE.md, then take it from here."
3. Answer your agent's questions. It asks everything **in one message** before it installs anything: your computer, which
   processor the brain may use, whether the brain should think overnight (and with which model), how its monthly
   self-review is approved, whether it runs nightly routines, whether to wire its session hook, whether you can use
   `sudo`, and whether you want GitHub plus Cloudflare or Vercel set up now or later.
4. Do the few steps that are yours alone, when your agent stops and asks: typing a password, signing in through a browser,
   typing a key into **your own terminal** (never into the chat), setting a spending limit, starting a new agent
   session, and designing your own persona with `/persona-forge` (about ten minutes).

Setup takes about an hour of your attention, plus waiting time while things download. Some ways of downloading drop the
"executable" mark on scripts; that is harmless, because every command runs a script through `bash` or `python3`.

**About the preflight.** For some computers (a Mac, or a machine with an AMD or Intel graphics card), your agent may run
Voidloom's "preflight", a ten-minute test of your machine that writes `preflight.json`. It is for **your own benefit**
and stays on your computer; nothing needs to be sent to anyone. If you ever want to share it, for example when asking
for help in a public issue, share the redacted copy your agent can make, which hides your home folder and user name.

---

**To the agent.** You are setting up the Voidwright web-dev workbench for a person who may know nothing about any of
this. Read `SETUP_GUIDE.md` in full (in pages: it is long) before you run anything, especially *How to run this guide*:
- you have no terminal, so P0 collects every answer from the person first, in one message, and the commands pass them
  as flags. Ask the thinker, approvals and GPU questions **word for word**, and never choose an answer for the person;
- nothing persists between your Bash calls, so every call from P0.4 on starts with `. ~/.webdev-workbench-setup/shell.sh &&`;
- long steps run in the background and are done when their rc file exists;
- each phase (P0 to P8) ends with a PASS line, and progress is recorded so a new session can resume.

Stop at every 🙋 HUMAN box and wait. Never ask for a key in the chat, never print one, never `source` a key file.
Keep a calm, thorough pace: nothing here is urgent.

---

**What is in this folder**

| Item | What it is |
|---|---|
| `SETUP_GUIDE.md` | the agent's runbook, P0 to P8 |
| `02_memory/` | the web-craft memory pack (its file name, version and entry count are on the first lines of `02_memory/PACK_MANIFEST.md`), plus `run_battery.py` and `recall_battery.json`, which prove the pack is findable after loading |
| `03_skills/` | the web skills (WebGL craft, graphic design, Astro pages, resource hubs, answer-engine optimisation, agent readiness and more), including **`scroll-journey`** |
| `04_reasoning/` | Fable planning cognition and the four Inner Council voices, plus the `/inner-council` command |
| `05_automations/` | three website automations (first build, website maintenance, resource-hub maintenance) and the three design-loop agents they use |
| `06_web_tools/` | small web tools (`cf-api`, `wrangler-safe`, `bearer-curl`, `forms-check`, build and preview watchers); they read your one key file, `~/.config/webtools/keys.env`, and never print a value |
| `07_nexus_tools/` | keeps the pack's map memories pointing at your own brain's memory numbers |
| `08_claude_md/webdev_workbench_block.md` | the short block the installer adds to `~/.claude/CLAUDE.md` |
| `09_guides/` | assume-nothing guides: `GITHUB_SETUP.md`, `DEPLOY_CLOUDFLARE.md`, `DEPLOY_VERCEL.md`, `CHOOSING_A_HOST.md`, `SERVICES.md` (keys, spending limits, manual routes), with `keys.env.example` and the key helper `with_keys.py` |
| `bin/install_skills.sh` | installs 03 to 09 into `~/.claude/` and `~/.local/share/webdev-workbench/`: additive, backed up, reversible (`--dry-run` first; `--uninstall` undoes it) |
| `bin/shell_env.sh` | the per-call shell setup the guide copies to `~/.webdev-workbench-setup/shell.sh` |
| `bin/redact_preflight.py` | makes a shareable copy of `preflight.json` with your home folder and user name hidden |
| `MANIFEST.md`, `verify_manifest.py` | every file with its checksum; `python3 verify_manifest.py` checks them all |

There is no Voidloom folder here: setup clones Voidloom from https://github.com/void-wright/voidloom (Apache-2.0) and
pins it to the commit this package was tested with.
