# `scripts/` — Weekly repo sync automation

Auto-regenerates [`README.md`](../README.md) GICS classification + [`index.html`](../index.html) sector counts based on the current repo list under [github.com/dotku](https://github.com/dotku).

Runs every **Sunday 05:00** via `launchd`. Uses your Claude Max subscription (no separate API cost).

## Files

| File | Role |
|---|---|
| `weekly-sync.py` | Orchestrator: diff repos → `claude --print` for new ones → regenerate docs → commit + push |
| `classify.py` | GICS sector/industry classifier (rule-based keyword matching) |
| `enriched.json` | Source of truth — every repo's metadata + enriched description |
| `gics_section.md` | Generated GICS section, spliced into `README.md` each run |
| `launchd/us.dotku.weekly-sync.plist` | macOS launchd schedule |
| `logs/` | `weekly-sync.out.log` + `weekly-sync.err.log` |

## Install the schedule

```bash
# Copy the plist into the user LaunchAgents dir
cp scripts/launchd/us.dotku.weekly-sync.plist ~/Library/LaunchAgents/

# Load it (runs it on next Sun 05:00)
launchctl load ~/Library/LaunchAgents/us.dotku.weekly-sync.plist

# Verify it's registered
launchctl list | grep weekly-sync
```

## Uninstall

```bash
launchctl unload ~/Library/LaunchAgents/us.dotku.weekly-sync.plist
rm ~/Library/LaunchAgents/us.dotku.weekly-sync.plist
```

## Run manually (dry-run style)

```bash
cd /Users/wlin/dev/dotku.github.io
python3 scripts/weekly-sync.py
```

No-ops if nothing changed — safe to run anytime.

## Prerequisites

- `gh` CLI authenticated (`gh auth status`)
- `claude` CLI authenticated (`claude setup-token`) — one-time
- Git push credentials for `github.com/dotku/dotku.github.io` (the same setup you use for manual `git push`)

## What it does

1. `gh api users/dotku/repos` — fetches all non-fork public repos
2. Diffs against `scripts/enriched.json` — finds new repos and repos whose GitHub description changed
3. For each **new** repo: pulls its README via `gh api`, sends to `claude --print` in a single batched prompt → gets back a concrete one-sentence description
4. Writes updated `enriched.json`
5. Runs `classify.py` → regenerates `gics_section.md`
6. Splices that section into `README.md` between the partners section and `## Contact`
7. Patches sector counts in `index.html` (card numbers + anchor slugs)
8. `git add`, commits with a structured message (lists new repos added), `git push`

## Logs

```bash
tail -50 scripts/logs/weekly-sync.out.log
tail -50 scripts/logs/weekly-sync.err.log
```

launchd runs the script even if you were asleep/laptop closed at 05:00 — it catches up as soon as the Mac wakes.

## Why not daily?

One repo a day isn't worth the noise. Weekly batches keep the git history clean and the Claude subscription quota free for interactive work.
