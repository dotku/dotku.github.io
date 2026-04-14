#!/usr/bin/env python3
"""Weekly dotku repo sync.

Runs from launchd every Sunday 5am. Steps:
  1. Fetch current dotku repos from GitHub.
  2. Diff against scripts/enriched.json.
  3. For each new/changed repo, pull README and ask Claude Code (headless)
     for a one-sentence description. Uses your Claude Max subscription, no API cost.
  4. Rewrite enriched.json + re-run classify.py.
  5. Splice the new GICS section into README.md.
  6. Update sector counts in index.html.
  7. git add + commit + push to origin master.

Exits cleanly with no-op if nothing changed.
"""
import base64
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
ENRICHED = HERE / 'enriched.json'
GICS_SECTION = HERE / 'gics_section.md'
README_MD = REPO / 'README.md'
INDEX_HTML = REPO / 'index.html'
LOG_DIR = HERE / 'logs'
LOG_DIR.mkdir(exist_ok=True)

CLAUDE_BIN = os.environ.get('CLAUDE_BIN') or '/Users/wlin/.nvm/versions/node/v20.17.0/bin/claude'
GH_BIN = os.environ.get('GH_BIN') or '/usr/local/bin/gh'

ORG = 'dotku'


def log(*args):
    print(f'[{dt.datetime.now().isoformat(timespec="seconds")}]', *args, flush=True)


def run(cmd, **kw):
    kw.setdefault('check', True)
    kw.setdefault('text', True)
    return subprocess.run(cmd, **kw)


def fetch_all_repos():
    """Return list of non-fork public repos: [{n, d, l, t}, ...]."""
    repos = []
    for page in range(1, 20):
        res = run(
            [GH_BIN, 'api', f'users/{ORG}/repos?per_page=100&page={page}',
             '--jq', '.[] | {n: .name, d: .description, l: .language, t: .topics, fork: .fork}'],
            capture_output=True,
        )
        lines = [ln for ln in res.stdout.strip().split('\n') if ln]
        if not lines:
            break
        for ln in lines:
            r = json.loads(ln)
            if not r.pop('fork', False):
                repos.append(r)
        if len(lines) < 100:
            break
    return repos


def load_enriched():
    if ENRICHED.exists():
        return json.loads(ENRICHED.read_text())
    return []


def fetch_readme(name):
    try:
        res = subprocess.run(
            [GH_BIN, 'api', f'repos/{ORG}/{name}/readme', '--jq', '.content'],
            capture_output=True, text=True, timeout=15,
        )
        if res.returncode != 0:
            return None
        return base64.b64decode(res.stdout.strip()).decode('utf-8', errors='replace')
    except Exception:
        return None


def claude_describe(repos):
    """One claude --print call to generate descriptions for a batch. Returns {name: desc}."""
    if not repos:
        return {}
    parts = [
        "You are writing client-facing portfolio blurbs for a business-solutions provider.",
        "For each GitHub repo below, write ONE concrete English sentence (max 130 chars)",
        "that positions what the project DOES (its purpose / domain), not its tech stack.",
        "",
        "Rules (IMPORTANT — this is for a customer-facing page):",
        "- Confident, professional tone. Never use: 'experimental', 'personal project',",
        "  'toy', 'demo', 'playground', 'unclear', 'likely', 'maybe'.",
        "- If README is boilerplate (create-next-app, StackBlitz default, Create React App),",
        "  IGNORE it and infer the project's purpose from the repo name.",
        "- Don't lead with the tech stack ('A Next.js application that...').",
        "  Lead with the business purpose ('A wedding planning checklist for couples.').",
        "- Even when signal is thin, commit to a confident, domain-oriented one-liner",
        "  derived from the words in the name. Prefer concrete over vague.",
        "- Cap at 130 chars, plain text, no trailing period is fine, no em-dashes needed.",
        "",
        "Output ONLY a JSON array, no markdown fences, no commentary:",
        '[{"n": "repo-name", "d": "description"}, ...]',
        "",
    ]
    for r in repos:
        parts.append(f'--- Repo: {r["n"]}')
        parts.append(f'Language: {r.get("l") or "unknown"}')
        parts.append(f'Topics: {", ".join(r.get("t") or []) or "(none)"}')
        parts.append(f'Existing description: {r.get("d") or "(none)"}')
        readme = fetch_readme(r['n'])
        if readme:
            parts.append(f'README excerpt:\n{readme[:1500]}')
        parts.append('')
    prompt = '\n'.join(parts)

    log(f'Calling claude --print for {len(repos)} repo(s)...')
    res = subprocess.run(
        [CLAUDE_BIN, '--print', prompt],
        capture_output=True, text=True, timeout=600,
    )
    if res.returncode != 0:
        log('claude failed:', res.stderr[:500])
        return {}
    out = res.stdout.strip()
    m = re.search(r'\[\s*\{.*?\}\s*\]', out, re.DOTALL)
    if not m:
        log('no JSON array in claude output:', out[:300])
        return {}
    try:
        data = json.loads(m.group())
        return {item['n']: item['d'] for item in data if item.get('n') and item.get('d')}
    except Exception as e:
        log('JSON parse failed:', e)
        return {}


def update_index_counts(sector_counts, subind_counts):
    """Patch sector-card counts + sub-industry chip counts in index.html.
    sector_counts: {slug: (count, new_count)} — we just rewrite based on current counts.
    """
    html = INDEX_HTML.read_text()
    # Replace href anchors + big number spans per sector.
    # Anchors look like: repos.html#/?id=information-technology-432
    # Big numbers look like: >432<   (matched preceded by the anchor's card)
    # Safer: use regex anchored to the href.
    for slug, (_, new_total) in sector_counts.items():
        # Update anchor
        html = re.sub(
            rf'repos\.html#/\?id={re.escape(slug)}-\d+',
            f'repos.html#/?id={slug}-{new_total}', html)
        # Update the big number for this card. Find the card containing this anchor + replace the nearest span `>NUM<`.
        # We'll do a loose match: the card's big number span follows the anchor within ~300 chars.
        pat = re.compile(
            rf'(href="repos\.html#/\?id={re.escape(slug)}-{new_total}"[\s\S]{{0,400}}?text-3xl font-extrabold[^>]*>)(\d+)(<)',
        )
        html = pat.sub(lambda m: f'{m.group(1)}{new_total}{m.group(3)}', html)
    # Sub-industry chips: replace "Label · NUM" patterns. These are low-priority; skip if not trivially present.
    for label, num in subind_counts.items():
        pat = re.compile(rf'({re.escape(label)} · )\d+')
        html = pat.sub(lambda m: f'{m.group(1)}{num}', html)
    INDEX_HTML.write_text(html)


def batched(seq, size):
    buf = []
    for item in seq:
        buf.append(item)
        if len(buf) >= size:
            yield buf
            buf = []
    if buf:
        yield buf


def upgrade_ollama(existing, batch_size=20):
    """One-shot catch-up: re-describe every repo currently sourced from Ollama
       using Claude (the same prompt used for new repos).
    """
    targets = [r for r in existing if r.get('d_source') == 'ollama']
    log(f'Upgrade-ollama mode: {len(targets)} repos to re-describe via Claude')
    if not targets:
        return 0
    updated = 0
    for i, batch in enumerate(batched(targets, batch_size), 1):
        log(f'Batch {i}/{(len(targets) + batch_size - 1) // batch_size} '
            f'({len(batch)} repos)...')
        descs = claude_describe(batch)
        for r in batch:
            if r['n'] in descs:
                r['d_enriched'] = descs[r['n']]
                r['d_source'] = 'claude'
                updated += 1
    return updated


def _sync_index_counts(new_section):
    sector_slug = {
        'Energy': 'energy', 'Industrials': 'industrials',
        'Consumer Discretionary': 'consumer-discretionary',
        'Consumer Staples': 'consumer-staples', 'Health Care': 'health-care',
        'Financials': 'financials', 'Information Technology': 'information-technology',
        'Communication Services': 'communication-services',
        'Utilities': 'utilities', 'Real Estate': 'real-estate',
        'Materials': 'materials',
    }
    sector_totals = {}
    for name, slug in sector_slug.items():
        m = re.search(rf'^### {re.escape(name)} \((\d+)\)', new_section, re.M)
        if m:
            sector_totals[slug] = (None, int(m.group(1)))
    update_index_counts(sector_totals, {})
    log(f'index.html counts updated for {len(sector_totals)} sectors')


def _commit_and_maybe_push(msg, no_push=False):
    status = run(['git', 'status', '--porcelain'], capture_output=True).stdout.strip()
    if not status:
        log('Working tree clean after updates — nothing to commit')
        return
    run(['git', 'add', 'README.md', 'index.html', 'scripts/enriched.json'])
    run(['git', 'commit', '-m', msg + '\n\nGenerated by scripts/weekly-sync.py'])
    log('Committed.')
    if no_push:
        log('--no-push set; not pushing to origin')
    else:
        log('Pushing...')
        run(['git', 'push', 'origin', 'master'])


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--upgrade-ollama', action='store_true',
                    help='One-time catch-up: re-run Claude on all existing Ollama-sourced descriptions.')
    ap.add_argument('--no-push', action='store_true',
                    help="Don't git push (useful for dry runs).")
    ap.add_argument('--no-commit', action='store_true',
                    help="Don't git commit (implies --no-push).")
    args = ap.parse_args()

    log('--- Weekly sync start ---')
    os.chdir(REPO)

    if args.upgrade_ollama:
        # Catch-up path: don't fetch from GitHub, just upgrade existing entries.
        existing = load_enriched()
        updated = upgrade_ollama(existing)
        log(f'Upgraded {updated} descriptions via Claude')
        if not updated:
            return 0
        existing.sort(key=lambda r: r['n'].lower())
        ENRICHED.write_text(json.dumps(existing, ensure_ascii=False, indent=2))

        # Regenerate classify output + README + index counts
        log('Running classify.py...')
        run([sys.executable, str(HERE / 'classify.py')])
        readme = README_MD.read_text()
        new_section = GICS_SECTION.read_text()
        updated_readme = re.sub(
            r'## GitHub Repositories by GICS[\s\S]*?(?=## Contact)',
            new_section + '\n', readme, count=1,
        )
        README_MD.write_text(updated_readme)
        log(f'README.md updated ({len(updated_readme)} bytes)')

        # index.html sector counts
        _sync_index_counts(new_section)

        if args.no_commit:
            log('--no-commit set; skipping git')
            return 0
        _commit_and_maybe_push(
            f'chore: upgrade {updated} Ollama-sourced descriptions to Claude-level quality',
            no_push=args.no_push,
        )
        log('--- Upgrade-ollama catch-up complete ---')
        return 0

    # --- Normal weekly diff mode ---
    current = fetch_all_repos()
    log(f'Fetched {len(current)} non-fork repos from github.com/{ORG}')

    existing = load_enriched()
    existing_names = {r['n'] for r in existing}
    current_names = {r['n'] for r in current}

    new_repos = [r for r in current if r['n'] not in existing_names]
    removed = existing_names - current_names
    if removed:
        log(f'Removed/renamed repos ({len(removed)}): {sorted(removed)[:5]}...')

    existing_by_name = {r['n']: r for r in existing}
    changed_desc = []
    for r in current:
        prev = existing_by_name.get(r['n'])
        if prev and (prev.get('d') or '') != (r.get('d') or ''):
            changed_desc.append(r)

    if not new_repos and not changed_desc and not removed:
        log('No changes detected — exiting')
        return 0

    log(f'New: {len(new_repos)}, desc changed: {len(changed_desc)}')

    # --- Claude enrichment for new repos, batched ---
    descs = {}
    for batch in batched(new_repos, 20):
        descs.update(claude_describe(batch))
    for r in new_repos:
        if r['n'] in descs:
            r['d_enriched'] = descs[r['n']]
            r['d_source'] = 'claude'

    # --- Rebuild enriched.json from current list, preserving enriched fields for existing ---
    merged = []
    for r in current:
        prev = existing_by_name.get(r['n'])
        if prev:
            # Preserve prior enrichment
            if prev.get('d_enriched'):
                r.setdefault('d_enriched', prev['d_enriched'])
                r.setdefault('d_source', prev.get('d_source', 'readme'))
        merged.append(r)

    merged.sort(key=lambda r: r['n'].lower())
    ENRICHED.write_text(json.dumps(merged, ensure_ascii=False, indent=2))
    log(f'Wrote {ENRICHED} ({len(merged)} repos)')

    # --- Re-run classifier ---
    log('Running classify.py...')
    run([sys.executable, str(HERE / 'classify.py')])

    # --- Splice GICS section into README.md ---
    readme = README_MD.read_text()
    new_section = GICS_SECTION.read_text()
    updated = re.sub(
        r'## GitHub Repositories by GICS[\s\S]*?(?=## Contact)',
        new_section + '\n', readme, count=1,
    )
    README_MD.write_text(updated)
    log(f'README.md updated ({len(updated)} bytes)')

    # --- index.html sector counts ---
    # Count per sector from merged + classifier output.
    # Simplest: re-parse the regenerated GICS section to pull sector totals.
    sector_slug = {
        'Energy': 'energy', 'Industrials': 'industrials',
        'Consumer Discretionary': 'consumer-discretionary',
        'Consumer Staples': 'consumer-staples', 'Health Care': 'health-care',
        'Financials': 'financials', 'Information Technology': 'information-technology',
        'Communication Services': 'communication-services',
        'Utilities': 'utilities', 'Real Estate': 'real-estate',
        'Materials': 'materials',
    }
    sector_totals = {}
    for name, slug in sector_slug.items():
        m = re.search(rf'^### {re.escape(name)} \((\d+)\)', new_section, re.M)
        if m:
            sector_totals[slug] = (None, int(m.group(1)))
    subind_labels = {}  # skip sub-industry precision; sector-level is enough
    update_index_counts(sector_totals, subind_labels)
    log(f'index.html counts updated for {len(sector_totals)} sectors')

    # --- git commit + push ---
    status = run(['git', 'status', '--porcelain'], capture_output=True).stdout.strip()
    if not status:
        log('Working tree clean after updates — nothing to commit')
        return 0

    run(['git', 'add', 'README.md', 'index.html', 'scripts/enriched.json'])
    header_lines = [f'- {r["n"]}: {r.get("d_enriched") or r.get("d") or "(no description)"}'
                    for r in new_repos[:20]]
    if len(new_repos) > 20:
        header_lines.append(f'- ... and {len(new_repos) - 20} more')
    body = '\n'.join(header_lines) if header_lines else 'Metadata / description updates.'
    msg = (f'weekly: sync {len(new_repos)} new + {len(changed_desc)} changed repo(s)\n\n'
           f'{body}\n\nGenerated by scripts/weekly-sync.py')
    run(['git', 'commit', '-m', msg])
    log('Committed. Pushing...')
    run(['git', 'push', 'origin', 'master'])
    log('--- Weekly sync complete ---')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        log('FATAL:', e)
        import traceback; traceback.print_exc()
        sys.exit(1)
