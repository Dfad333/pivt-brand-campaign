# Running the campaign studio on another machine

## First, the thing that trips people up

**Signing into the same Claude account does not move any of this.** The account carries
your Claude subscription, your connectors and your plugins. It does not carry files.

| Thing | Follows the account? |
|---|---|
| Higgsfield MCP (image generation) | **Yes** — it's a claude.ai connector, not a local config file. Nothing to install. |
| Claude Code itself, plugins, skills | **Yes** |
| The `brand-campaign` folder | **No** — ordinary files on disk |
| The `/pivtcontent` slash command | **No** — a file in the project's `.claude/commands/` |
| Claude's memory of this project | **No** — stored per-machine, keyed to the folder path |

So three things have to travel: **the folder, the command, and the memory.** All three are
in this repo. The sections below move them.

---

## The method: a private GitHub repo

Of the options, this is the one worth the setup:

- **Private GitHub repo** ← recommended. Two-way sync forever: generate on either machine,
  push, pull on the other. Full history of the poster system. ~62 MB, clones in seconds.
- Google Drive / OneDrive — fine for the heavy image archive, bad for code. Sync conflicts
  on a `.py` file are silent and ugly.
- USB / direct copy — one-time only, goes stale the moment you build something.

### On this machine (desktop) — publish once

```bash
cd /e/PivtMedia/brand-campaign
gh repo create pivt-brand-campaign --private --source=. --remote=origin --push
```

That creates the private repo under your account and pushes everything tracked.

### On the laptop — clone and wire up

```bash
gh repo clone Dfad333/pivt-brand-campaign
```

Clone it anywhere you like — a drive letter no longer matters (see *Portability* below).

Then three small steps:

**1. Install the slash command.** Copy `install/pivtcontent.md` into the project's command
folder, creating it if needed:

```bash
mkdir -p .claude/commands && cp install/pivtcontent.md .claude/commands/
```

`/pivtcontent` then works in that folder and carries the whole method with it — the standing
rules, the build commands, the QA checklist, the series state.

**2. Install Python + Pillow**, which is all the studio needs:

```bash
pip install pillow
```

**3. Hand Claude the memory.** Open the folder in Claude Code and say:

> Import `install/memory/*.md` into your memory for this project.

That restores what Claude knows about the campaign — the rejected directions and why, the
prompt traps, the lineage rules — so you don't re-litigate decisions you already made.

### Verify it worked

```bash
cd studio && python contact_sheet.py
```

If it prints a poster count and writes `CONTACT-SHEET.jpg`, fonts and logos resolved
correctly and you're ready to generate.

---

## Working across two machines

Normal git. Before you start on either machine:

```bash
git pull
```

After a session that produced posters you want to keep:

```bash
git add final/ studio/ && git commit -m "feat: add <what you made>" && git push
```

The one rule: **don't build on both machines at once without pulling first.** `final/` is
binary JPEGs, and git cannot merge those — you'd have to pick one side by hand.

---

## What is deliberately left behind

`.gitignore` excludes two folders:

| Folder | Size | Why |
|---|---|---|
| `raw/` | 1.3 GB | The untouched Higgsfield photographs |
| `motion/` | 4.4 GB | Video renders from the motion work |

Neither is needed to **create** new content — new generation writes fresh files into `raw/`.
All 58 finished posters ship in `final/`, so nothing you've made is lost.

The one thing you give up: **`rebuild_all.py` won't run on the laptop without `raw/`**, because
it re-composites type onto those source photographs. If you want to re-cut an existing
poster's headline on the laptop, bring `raw/` across on a USB drive or via Google Drive and
drop it in — it is ignored by git, so it will sit there quietly and everything will work.

If you'd rather have it in the repo despite the weight, delete the `raw/` line from
`.gitignore` and push. GitHub will accept it (largest single file is 28 MB, well under the
100 MB limit); the first clone just takes a while.

---

## Portability — what changed to make this work

The studio used to hardcode `E:\PivtMedia\...` in fifteen files, so it only ran on one
computer. Now:

- **`studio/paths.py`** resolves every folder from its own location on disk. The campaign
  folder can live on any drive, under any name, on any machine.
- **Fonts resolve from a candidate list** — Windows paths first, then macOS and Linux
  equivalents. If none are found it fails with the full list of what it looked for, rather
  than a confusing Pillow error.
- **The logo set now lives in `brand/logo/`**, inside the repo. It used to be read from
  `E:\PivtMedia\Pivt Media Logos\campaign-overlay\`, which the laptop won't have.

Nothing else moved, and all 58 posters rebuild byte-identically.

To point the studio at a copy of the folder somewhere else, set `PIVT_CAMPAIGN_ROOT`.
