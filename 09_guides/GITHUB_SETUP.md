# GitHub, from zero

## What you will have at the end

- An account protected against someone stealing your password.
- A private repository for your site's code.
- A computer that can securely upload changes.
- A branch workflow for reviewing changes before publication.
- Local secret checks and a clear understanding of online protection limits.

## Before you start

Allow about 60 to 90 minutes.
You need an email address you can access, a browser, and your own terminal.
A terminal is the window where you type commands.
Use bash on Linux, WSL2 Ubuntu, or macOS.

You need Git, which records changes to files, and Python 3 for the local secret-checking tool.
You also need your site's folder.
This guide uses the invented Crumb & Crust Bakery and its repository name, `bakery-site`.

Your coding agent can explain errors and edit ordinary project files.
You must handle passwords, recovery codes, private keys, and sign-in prompts yourself.
Never put those values in an AI chat.

Service keys belong only in `~/.config/webtools/keys.env`, with permission mode `600`, or the hosting platform's secret store.
Mode `600` means only your operating-system account can read or write the file.
Never print, copy, paste, or `source` that file.
Type or paste individual service keys only in your own editor or terminal when following `SERVICES.md`.

SSH authentication uses a separate public/private key pair managed by SSH.
The public half is safe to register with the service.
Never display or share the private half.

Replace every angle-bracket placeholder before running its command.
Keep surrounding quotation marks when the example includes them.
Run commands one block at a time.

**In your own terminal:**
```bash
git --version
python3 --version
ssh -V
```

Each command should report a version.
If one is missing, install it using your operating system's supported instructions before continuing.

## 1. Understand where your site lives

A repository, often shortened to repo, is a project's files and recorded history.
A commit is a saved snapshot of changes.
A branch is a separate line of work.
Here, `main` will hold changes approved for the live site.

GitHub stores the online copy of your repository (as of October 2026; re-check before relying on it). See [GitHub's repository documentation](https://docs.github.com/en/repositories).
Git stores the local copy on your computer.
A push uploads local commits to the online copy.

Your host is the service that publishes the website.
After you connect the repository and configure deployments, Cloudflare (through Workers Builds) or Vercel can build branch previews and publish your production branch (as of October 2026; re-check before relying on it). See [Cloudflare Workers Builds](https://developers.cloudflare.com/workers/ci-cd/builds/) and [Vercel Git deployments](https://vercel.com/docs/git).
A build turns your source files into the files needed to run the site.
A preview is a temporary version you can inspect before publication.

For this workbench, configure previews for each working branch and production deployment from `main`.
Creating the repository alone does not connect a host.
Complete your hosting guide before expecting preview links.

**Check:** You can explain the route: local edits, commit, push, preview, then merge into `main`.

## 2. Create and protect your account

**In your browser:** Open [github.com/signup](https://github.com/signup), create an account, and complete email verification (as of October 2026; re-check before relying on it). See [GitHub account documentation](https://docs.github.com/en/account-and-profile).
Choose a unique password and save it in your password manager.

Two-factor authentication, or 2FA, requires additional proof beyond a password.
A stolen password must not be enough to change your live site.

**In your browser:** Open your account's **Settings > Password and authentication** and enable two-factor authentication (as of October 2026; re-check before relying on it). Follow [GitHub's 2FA instructions](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication).
An authenticator app generates short-lived sign-in codes.
Complete its setup and save recovery codes somewhere private and accessible if you lose your phone.

A passkey uses your device or security key to prove your identity.
You can add one after completing the required initial 2FA setup (as of October 2026; re-check before relying on it). Follow the passkey section of [GitHub's 2FA instructions](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication).
Do not send your agent the setup QR code or recovery codes.

**Check:** Your email is verified, 2FA is enabled, and you can find your recovery codes without opening your repository.

## 3. Tell Git who you are

Git records an author name and email in each commit.
These settings identify your work. They do not sign you in.
The `--global` option applies to repositories used by your operating-system account.

Decide whether you want your real email recorded before making your first commit.
Changing it later does not change old commits.

**In your browser:** For email privacy, open **Settings > Emails**, enable **Keep my email address private**, and copy the provided `noreply` address (as of October 2026; re-check before relying on it). See [GitHub commit email instructions](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/setting-your-commit-email-address).
Use that exact address instead of your real email below.
The privacy setting alone does not change your local Git configuration.

Replace `<Your Name>` with your chosen public author name.
Replace `<the email on your GitHub account>` with your verified email or the provided private address.

**In your own terminal:**
```bash
git config --global user.name "<Your Name>"
git config --global user.email "<the email on your GitHub account>"
git config --global init.defaultBranch main
git config --global --get user.name
git config --global --get user.email
git config --global --get init.defaultBranch
```

**Check:** The last three commands show your chosen identity and `main`. Use the private address if you do not want your real email in public commits.

## 4. Sign in from this computer

Choose route A or route B.
SSH is a secure connection method that proves your identity using a key pair.

### Route A: use the command-line tool

GitHub CLI, called `gh`, manages account and repository tasks from a terminal (as of October 2026; re-check before relying on it). See [the official CLI documentation](https://cli.github.com/manual/).

On macOS, if Homebrew is already installed, use its package installer.
**In your own terminal:**
```bash
brew install gh
```

**In your browser:** On Linux, WSL2, or a Mac without Homebrew, follow the appropriate [official installation instructions](https://github.com/cli/cli#installation) (as of October 2026; re-check before relying on it).
**In your own terminal:** Run the installation commands for your operating system, then:
```bash
gh auth login --git-protocol ssh --web
```

The web flow gives you a one-time code and directs you to browser authorization.
It can detect or create an SSH key and offer to upload its public half (as of October 2026; re-check before relying on it). See [`gh auth login`](https://cli.github.com/manual/gh_auth_login).
**In your browser:** Complete only the sign-in flow you just started.
**In your own terminal:** Complete the SSH key prompts and use a passphrase if creating a key.
Do not use a manual token or insecure-storage fallback for this guide.

**In your own terminal:**
```bash
gh auth status
```

Continue to the SSH connection check below.

### Route B: create an SSH key yourself

Replace `<your email>` with your chosen commit email.
This checks for an existing public key before creating a pair.

**In your own terminal:**
```bash
ls ~/.ssh/id_ed25519.pub 2>/dev/null || ssh-keygen -t ed25519 -C "<your email>" -f ~/.ssh/id_ed25519
```

If asked to overwrite an existing private key, answer no and stop.
An existing private key without its public companion needs recovery, not replacement.
For a new pair, use a passphrase, which protects the private key if someone obtains the file.

Start the SSH agent, the background process that holds unlocked keys.
**In your own terminal:**
```bash
eval "$(ssh-agent -s)"
```

On Linux or WSL2:
**In your own terminal:**
```bash
ssh-add ~/.ssh/id_ed25519
```

On macOS, use the system SSH tools and the keychain option (as of October 2026; re-check before relying on it). See [GitHub's SSH key setup instructions](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent).
**In your own terminal:**
```bash
/usr/bin/ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

Open `~/.ssh/id_ed25519.pub` in your own editor.
Copy its single line. This is the PUBLIC key.
Never open or copy `~/.ssh/id_ed25519` to share it.

**In your browser:** Open account **Settings > SSH and GPG keys > New SSH key**, choose an authentication key, and paste the public line (as of October 2026; re-check before relying on it). See [GitHub SSH documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).
Give it a label that identifies this computer.

### Check the SSH connection for either route

A host fingerprint identifies the server's SSH key.
Verify it before trusting a new server connection.

**In your browser:** Open [GitHub's published SSH key fingerprints](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints) (as of October 2026; re-check before relying on it).
**In your own terminal:**
```bash
ssh -o StrictHostKeyChecking=ask -T git@github.com
```

If prompted, compare the displayed fingerprint with the published fingerprint for that key type.
Type `yes` only if they match.
If they differ, stop. Do not turn off host checking.

After establishing trust, run the requested repeatable check.
**In your own terminal:**
```bash
ssh -o StrictHostKeyChecking=accept-new -T git@github.com
```

The expected success message is “Hi `<user>`! You've successfully authenticated, but GitHub does not provide shell access.”
The command exits with code `1` even on success because no shell is provided (as of October 2026; re-check before relying on it). See [GitHub's connection test](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/testing-your-ssh-connection).

**Check:** The message names your account. For route A, `gh auth status` also confirms your login.

## 5. Prepare the repository

Private is the safe starting choice for a site under construction.
This choice concerns the code. It does not guarantee that a deployed preview is private.

Open your terminal in the site's folder.
Alternatively, replace `<path-to-bakery-site>` with its full path.

**In your own terminal:**
```bash
cd "<path-to-bakery-site>"
pwd
ls -a
git rev-parse --show-toplevel
git remote -v
```

A remote is a named address for an online repository.
`origin` is the conventional name for your project's remote.
For a folder without Git history, the last two commands may report that it is not a repository.

If the reported top-level folder is a parent folder, stop and choose a separate project location.
If you copied another site's folder, its hidden `.git` directory may still contain that site's history and remote.
For a genuinely new site, exclude `.git` when copying, or remove only the copied `.git` directory using your file manager.
Do not remove the original project's history.

Choose one creation route:

**In your browser:** Use **New repository**, name it `bakery-site`, and select **Private** (as of October 2026; re-check before relying on it). See [GitHub repository creation](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository).
Leave README, license, and ignore-file initialization off because you will push an existing folder.
Create the empty repository.

Alternatively, choose the CLI route if you completed route A.
Wait until Step 7 has created your first local commit, then run the `gh repo create` command shown there.
It will create the private repository and set `origin` (as of October 2026; re-check before relying on it). See [`gh repo create`](https://cli.github.com/manual/gh_repo_create).

**Check:** You are in the intended site folder. You either created an empty private repository or selected the deferred CLI route.

## 6. Keep secrets and generated files out

A `.gitignore` file lists files Git should leave untracked.
Create it in the site's top-level folder using your editor.
For an Astro and Node site, use this complete baseline.
If the file already exists, preserve any additional project-specific rules.

```gitignore
node_modules/
dist/
.astro/
.vercel/
.wrangler/
.env
.env.*
!.env.example
.dev.vars
.dev.vars.*
!.dev.vars.example
*.pem
*.key
keys.env
.DS_Store
npm-debug.log*
coverage/
```

This is file content, not a terminal command.
Generated files are files tools can recreate, such as dependencies and build output.
The `!` rules allow the two example files through.

`.env.example` and `.dev.vars.example` are committed, value-free templates.
They document variable names using empty values or obvious replacement markers.
Never place working credentials in them.
Actual service keys stay in the private workbench file or hosting secret store.

An ignore rule does not remove a file Git already tracks.
Replace `<file>` with an actual tracked path that should become untracked.

**In your own terminal:**
```bash
git rm --cached -- "<file>"
```

This preserves the local file while staging its removal from the repository.
It does not erase earlier commits.
A secret that was ever pushed must be ROTATED, meaning replaced and the old value revoked at its issuing vendor.

**Check:** `.gitignore` contains every baseline rule, and both example files contain no real values.

## 7. Make the first commit and push

Initialize Git if Step 5 showed that this folder has no repository.
**In your own terminal:**
```bash
git init
```

Before the first commit, complete Step 10's local hook setup if possible.
Then return here.
At minimum, inspect the staged files carefully before sending anything online.

Stage the files, which selects changes for the next commit.
**In your own terminal:**
```bash
git add -A
git status
git diff --cached --stat
```

READ the list before continuing.
There must be no real `.env` files, `keys.env`, `node_modules`, private keys, or credentials.
The value-free `.env.example` and `.dev.vars.example` files are allowed.
If something private is staged, stop and fix it first.

**In your own terminal:**
```bash
git commit -m "First commit"
git branch -M main
```

For the deferred CLI route only:
**In your own terminal:**
```bash
gh repo create bakery-site --private --source . --remote origin
```

For the website route only, replace `<you>` with your account username.
Skip this command if the CLI already created `origin`.
**In your own terminal:**
```bash
git remote add origin "git@github.com:<you>/bakery-site.git"
```

Check the destination before uploading.
**In your own terminal:**
```bash
git remote -v
```

Both addresses must point to your intended `bakery-site` repository.
If they point to an older project, stop and follow Troubleshooting.

**In your own terminal:**
```bash
git push -u origin main
```

The `-u` option remembers which online branch this local branch follows.
**In your browser:** Refresh your repository page and inspect its file list.

**Check:** The online repository contains your intended files and first commit, with no secrets or generated dependencies.

## 8. Work on branches and review previews

Start from an up-to-date `main`.
**In your own terminal:**
```bash
git switch main
git pull --ff-only
git switch -c add-opening-hours
```

Edit the bakery's opening hours with your agent.
Run the project's documented build and checks.
Do not assume the project has a test command unless its instructions say so.

**In your own terminal:**
```bash
git add -A
git status
git commit -m "Add bakery opening hours"
git push -u origin add-opening-hours
```

A pull request, or PR, proposes merging one branch into another.
**In your browser:** Open the repository's **Pull requests** page and create a PR from `add-opening-hours` into `main` (as of October 2026; re-check before relying on it). See [GitHub pull request documentation](https://docs.github.com/en/pull-requests).
Alternatively, use the CLI route.
**In your own terminal:**
```bash
gh pr create --base main --head add-opening-hours --title "Add opening hours" --body "Adds bakery opening hours for review."
```

Once hosting integration is configured, find the branch deployment and its preview link (as of October 2026; re-check before relying on it). See [Cloudflare Workers Builds](https://developers.cloudflare.com/workers/ci-cd/builds/) or [Vercel Git deployments](https://vercel.com/docs/git).
**In your browser:** Open the preview. Check the text, links, and phone-sized layout.
Merge only after the preview looks right and the build and checks pass.

**In your browser:** Use the PR's merge control when review is complete (as of October 2026; re-check before relying on it). See [GitHub pull request documentation](https://docs.github.com/en/pull-requests).
Never force-push a shared branch with `git push --force`.
For a non-fast-forward rejection, follow Troubleshooting.

**Check:** Your change was reviewed on a branch before reaching `main`. If hosting is connected, verify the resulting live deployment too.

## 9. Protect `main` where your plan allows it

Branch protection can prevent force pushes and deletion, and require a PR and passing checks (as of October 2026; re-check before relying on it). See [protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).
A check is an automated result, such as whether the site built successfully.

**Important:** Free personal accounts and free organizations cannot enforce branch protection or branch rulesets on PRIVATE repositories (as of October 2026; re-check before relying on it). See [ruleset availability](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets).
An upgrade response may include HTTP `403`, meaning the request was refused.
The response may say “Upgrade to GitHub Pro or make this repository public to enable this feature” (as of October 2026; re-check before relying on it). Check the current [plan requirements](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).

Choose one approach:
- Make the repository public only after checking that all files and history are safe to publish.
- Pay for a plan that supports protection for the repository's owner.
- Keep it private and follow written discipline: build and checks green, inspect the preview, then merge.

For an eligible repository, create a minimal rule.
**In your browser:** Open **Settings > Rules > Rulesets** and create a branch ruleset targeting `main` (as of October 2026; re-check before relying on it). See [ruleset documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets).
Set enforcement to active, block force pushes, restrict deletion, and require a pull request.
Avoid adding a bypass for routine work.
Add a required passing status check once your real build check exists and has run.
Do not require another person's approval if you have no other reviewer.

**In your browser:** **Settings > Branches** offers the classic branch-protection route instead (as of October 2026; re-check before relying on it). See [protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).

**Check:** Confirm the rule is active and applies to `main`. If your plan blocks it, record your manual review checklist instead.

## 10. Add two layers of secret checks

### Layer A: check locally before each commit

A pre-commit hook is a program Git runs before accepting a commit.
Install the hook manager using one route.

**In your own terminal:**
```bash
python3 -m pip install --user pre-commit
```

If Python reports an externally managed environment, do not override that protection.
If `pipx` is installed, use this alternative.
**In your own terminal:**
```bash
pipx install pre-commit
```

If neither route works, ask your agent to help install the tool for your operating system.
Do not use `sudo pip` to work around the error.

**In your browser:** Look up a released tag on the [official Gitleaks releases page](https://github.com/gitleaks/gitleaks/releases).
A tag is a name for a particular version.
Create `.pre-commit-config.yaml` in your project using your editor.
Replace the entire angle-bracket placeholder below with the released tag you checked.

```yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: <a release tag from github.com/gitleaks/gitleaks/releases, e.g. v8.x.y>
    hooks:
      - id: gitleaks
```

This is configuration content, not a bash command.
Do not leave `v8.x.y` or the placeholder in the saved file.
The official hook uses this repository and hook identifier (as of October 2026; re-check before relying on it). See [Gitleaks pre-commit instructions](https://github.com/gitleaks/gitleaks#pre-commit).

**In your own terminal:**
```bash
pre-commit install
pre-commit run --all-files
```

If the command is not found, fix your executable search path before continuing.
The first hook run may also need the build prerequisites described by the hook's installation instructions.
Each collaborator must install the hook in their own checkout.

Test it with nothing else staged.
In your editor, create `fake-secret-test.txt`.
Type `test_token=` followed by a MADE-UP string starting with `ghp_` and exactly 36 random letters and digits.
Never use a real token.

**In your own terminal:**
```bash
git add -- fake-secret-test.txt
git commit -m "Test local secret blocker"
```

Look for a Gitleaks finding and a blocked commit.
A download error or missing executable is not a successful detection test.
Delete the fake file in your editor, then unstage its entry.
**In your own terminal:**
```bash
git rm --cached --ignore-unmatch -- fake-secret-test.txt
git status
```

If the test commit unexpectedly succeeded, do not push it.
Ask your agent to remove that test commit safely and fix the hook.
The emergency bypass `git commit --no-verify` skips hooks.
Never use it to bypass a secret finding or make a failed detection test appear successful.

Install the standalone Gitleaks executable using its [official installation instructions](https://github.com/gitleaks/gitleaks#installing).
Hook installation alone does not guarantee that `gitleaks` is available in your terminal.
Scan committed history once, with output redacted so detected values remain hidden.
The newer command is `gitleaks git .`; older versions use `gitleaks detect` (as of October 2026; re-check before relying on it). See [Gitleaks commands](https://github.com/gitleaks/gitleaks).
**In your own terminal:** Use the newer form:
```bash
gitleaks git . --redact
```

For an older installation only:
**In your own terminal:**
```bash
gitleaks detect --redact
```

### Layer B: enable online protections where available

Secret scanning looks for exposed credentials. Push protection can stop supported secrets during upload.
Public repositories receive these features free; ordinary private organization repositories require the paid GitHub Secret Protection add-on on an eligible organization plan (as of October 2026; re-check before relying on it). See [secret-scanning availability](https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning) and [push protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection).
A paid personal account alone does not provide that private-organization add-on.

**In your browser:** Look in repository **Settings**, under **Security**, for **Advanced Security** or **Code security** and enable the available secret-scanning and push-protection controls (as of October 2026; re-check before relying on it). See [GitHub security documentation](https://docs.github.com/en/code-security).
**In your browser:** Also inspect your account's **Code security and analysis** settings for personal push protection, described as **Push protection for yourself** (as of October 2026; re-check before relying on it). See [personal push protection](https://docs.github.com/en/code-security/secret-scanning/working-with-secret-scanning-and-push-protection/push-protection-for-users).
This personal protection concerns pushes to public repositories; it is not a substitute for private-repository scanning (as of October 2026; re-check before relying on it). See the same documentation.

No scanner detects every secret.
**Check:** The fake commit was blocked by detection, the fake file is gone, and you know which online protections are actually enabled.

## 11. Invite a collaborator, if needed

Ask for the collaborator's exact account username.
Confirm the spelling with them before sending an invitation.

**In your browser:** Open repository **Settings > Collaborators > Add people**, or **Collaborators & teams**, and search for their username (as of October 2026; re-check before relying on it). See [managing repository access](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/managing-teams-and-people-with-access-to-your-repository).
Where a role selector is available, choose **Write**, not **Admin**.
Personal repositories use owner and collaborator permissions rather than the full organization role selector (as of October 2026; re-check before relying on it). See [personal repository permissions](https://docs.github.com/en/account-and-profile/reference/permission-levels-for-a-personal-account-repository).

Share the branch workflow and ask them to install the local hook.
**Check:** The intended username accepted the invitation and has only the access needed.

## Troubleshooting

### Permission denied (publickey)

**Cause:** The public key is not registered, the wrong account is in use, or the SSH agent is not holding the key.
**Fix:** Recheck Step 4's public-key registration. If the agent is not running, start it using Step 4.
**In your own terminal:**
```bash
ssh-add ~/.ssh/id_ed25519
```
On macOS, use Step 4's keychain variant.
**Check:** Repeat the SSH connection test and confirm the account name.

### Host key verification failed

**Cause:** The saved server key conflicts with the presented key, or trust was never established.
**Fix:** Compare against the published fingerprints linked in Step 4.
Do not blindly delete the saved key or disable checking.
Only after confirming a legitimate change should you remove the old record and repeat verified setup.
**Check:** The fingerprint matches the official publication before you accept it.

### Rejected, non-fast-forward

**Cause:** The online branch has commits your local branch does not contain.
**Fix:** Finish or safely save your local edits first, then rebase, which reapplies your commits after the remote changes.
**In your own terminal:**
```bash
git pull --rebase
```
If conflicts appear, ask your agent to help resolve them. Follow Git's instructions to continue.
To cancel the rebase, use `git rebase --abort`.
After a successful rebase, run your checks again.
**In your own terminal:**
```bash
git push
```
**Check:** The push succeeds without force, and both people's changes remain.

### You pushed a secret

**Cause:** A credential entered a commit and reached the online repository.
**Fix:** Revoke or rotate it at the issuing vendor FIRST. Update only the private workbench file or hosting secret store.
Then remove it from tracked files and arrange history cleanup using `git filter-repo`, a tool for rewriting repository history.
Coordinate with collaborators before rewriting shared history.
Forks, which are separate repository copies, and caches may retain old content even after cleanup (as of October 2026; re-check before relying on it). Follow [GitHub's sensitive-data removal guide](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository).
**Check:** The old credential no longer works. Removing the visible file alone is not enough.

### Remote origin already exists

**Cause:** A remote was already configured, possibly by copying an older project folder.
**In your own terminal:**
```bash
git remote -v
git log -5 --oneline
```
**Fix:** If the history belongs to another site, return to Step 5 and separate the copied project properly.
If the history is correct and only the destination is wrong, replace `<you>` with your username.
**In your own terminal:**
```bash
git remote set-url origin "git@github.com:<you>/bakery-site.git"
git remote -v
```
**Check:** The history belongs to this site and both remote addresses identify the intended repository.

## Undo / remove

Delete only a working branch whose useful changes are saved or merged.
Replace `<branch>` with its actual name. Do not use `main`.
**In your own terminal:**
```bash
git switch main
git pull --ff-only
git push origin --delete "<branch>"
git branch -d "<branch>"
```
If local deletion is refused, inspect the unmerged work instead of forcing deletion.
**In your browser:** The repository's branches page also offers branch deletion controls (as of October 2026; re-check before relying on it). See [branch management](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-branches-in-your-repository).

**In your browser:** To revoke this computer's SSH access, remove its key under account **Settings > SSH and GPG keys** (as of October 2026; re-check before relying on it). See [SSH key review](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/reviewing-your-ssh-keys).
Check the label carefully so you remove the intended computer's key.

**In your own terminal:** To sign out of the CLI:
```bash
gh auth logout
```
Local CLI logout does not revoke the SSH key or every existing authorization (as of October 2026; re-check before relying on it). See [`gh auth logout`](https://cli.github.com/manual/gh_auth_logout).

Before deleting a repository, keep a safe local copy and check whether your host still needs it.
**In your browser:** Open repository **Settings > General > Danger Zone > Delete this repository**, then read the confirmation carefully (as of October 2026; re-check before relying on it). See [repository deletion](https://docs.github.com/en/repositories/creating-and-managing-repositories/deleting-a-repository).
Deleting the repository is separate from removing the deployed site. Follow the hosting guide to remove that deployment.

**Check:** Only the intended branch, key, login, or repository was removed.