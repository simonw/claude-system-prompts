#!/usr/bin/env python3
"""Generate README.md from _sources/ and the git history.

Run after extract_prompts.py so the commit links resolve:

    python3 build_readme.py
"""

import re
import subprocess
import sys
from pathlib import Path

import extract_prompts as ep

ROOT = Path(__file__).resolve().parent
SOURCE_URL = "https://platform.claude.com/docs/en/release-notes/system-prompts/overview"

FAMILY_LABELS = {
    "claude-fable": "Fable",
    "claude-opus": "Opus",
    "claude-sonnet": "Sonnet",
    "claude-haiku": "Haiku",
}


def git(*args):
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def repo_url():
    url = git("remote", "get-url", "origin")
    m = re.match(r"(?:git@github\.com:|https://github\.com/)([^/]+/[^/]+?)(?:\.git)?$", url)
    if not m:
        sys.exit(f"Cannot derive GitHub URL from remote {url!r}")
    return f"https://github.com/{m.group(1)}"


def commit_for(name, descriptor):
    """Sha of the newest commit to `name` whose subject is "<name>: <descriptor>".

    A later "(revised)" commit for the same revision shares that prefix and
    wins, so the link always shows the text as currently published.
    """
    out = git("log", "-1", "--format=%H", "-F", f"--grep={name}: {descriptor}", "--", name)
    return out or None


def created_in(path):
    """Sha of the commit that first added path."""
    return git("log", "--diff-filter=A", "--format=%H", "--", path)


def main():
    base = repo_url()
    revisions = ep.load_revisions()

    latest = {}          # slug -> Revision
    count = {}           # slug -> number of revisions
    for rev in revisions:
        latest[rev.slug] = rev
        count[rev.slug] = count.get(rev.slug, 0) + 1
    families = []  # newest family first, following the order of the overview page
    for rev in sorted(revisions, key=lambda r: r.order):
        if rev.family not in families:
            families.append(rev.family)
    family_created = {f: created_in(f"{f}.md") for f in families}

    lines = []
    w = lines.append

    w("# Claude system prompts")
    w("")
    w(
        "Anthropic publishes the system prompts used by claude.ai and the Claude mobile "
        f"apps at [platform.claude.com]({SOURCE_URL}), one page per model, with a dated "
        "section for every revision. This repository turns those pages into files with a "
        "git history: **every published revision is a commit dated the day Anthropic "
        "says it went live**, so `git log`, `git diff`, and GitHub's history and compare "
        "views show how the prompts have changed over time."
    )
    w("")
    w("The files here are generated. Do not edit them by hand.")
    w("")

    w("## Files")
    w("")
    w("- `claude-<family>.md` — one file per model family, rewritten with each new prompt in that family. Its history shows the lineage from one model generation to the next.")
    w("- `claude-<model>.md` — one file per model, rewritten with each new revision of that model's prompt.")
    w("- `claude-<model>-YYYY-MM-DD.md` — one file per published revision, written once and never changed. Permalink to a prompt as it was on a given date.")
    w("- `_sources/` — the pages fetched from Anthropic, committed on the day they were fetched.")
    w("")

    w("## Family histories")
    w("")
    w("Each link is the commit history of one family file. Every commit's diff is the change from the previous prompt in that family, including across model generations.")
    w("")
    for fam in families:
        models = []
        for rev in revisions:
            if rev.family == fam and rev.model not in models:
                models.append(rev.model)
        span = models[0] if len(models) == 1 else f"{models[0]} → {models[-1]}"
        w(f"- [{FAMILY_LABELS.get(fam, fam)}]({base}/commits/main/{fam}.md) — {span}")
    w("")

    w("## Latest prompt for each model")
    w("")
    w("Newest first. Each revision is committed one file at a time, so every **what changed** link is a commit whose diff is exactly one comparison: against the previous revision of the same model where there is one, and against the previous prompt in the same family, whichever model that was.")
    w("")
    w("| Model | Published | Prompt | What changed |")
    w("| --- | --- | --- | --- |")
    ordered = sorted(latest.values(), key=lambda r: (r.date, -r.order), reverse=True)
    for rev in ordered:
        fam_label = FAMILY_LABELS.get(rev.family, rev.family)
        changes = []
        if count[rev.slug] > 1:
            sha = commit_for(f"{rev.slug}.md", rev.descriptor)
            if sha:
                changes.append(f"[vs previous {rev.model}]({base}/commit/{sha})")
        sha = commit_for(f"{rev.family}.md", rev.descriptor)
        if sha and sha != family_created[rev.family]:
            changes.append(f"[vs previous {fam_label}]({base}/commit/{sha})")
        if not changes:
            sha = commit_for(rev.dated_name, rev.descriptor)
            changes.append(f"first {fam_label} prompt ([commit]({base}/commit/{sha}))")
        w(
            f"| {rev.model} | {rev.date:%Y-%m-%d} | "
            f"[{rev.slug}.md]({base}/blob/main/{rev.slug}.md) "
            f"([history]({base}/commits/main/{rev.slug}.md)) | "
            + " · ".join(changes) + " |"
        )
    w("")

    w("## Every revision")
    w("")
    for rev in sorted(revisions, key=lambda r: (r.date, -r.order), reverse=True):
        w(f"- {rev.date:%Y-%m-%d} — [{rev.model}]({base}/blob/main/{rev.dated_name})")
    w("")

    w("## Notes on the data")
    w("")
    w("- Anthropic marks changes between dated versions of the same model with `**` around the changed text. Those markers are kept as published and are not part of the prompt sent to the model.")
    w("- Claude Sonnet 3.5 and Claude Haiku 3.5 have separate \"Text only\" and \"Text and images\" prompts under one date. Both are kept, as subsections of the same file.")
    w("- Commit dates are the dates on Anthropic's pages, which may lag the day a prompt actually changed in production.")
    w("")

    w("## How it works")
    w("")
    w("- [`fetch_sources.py`](fetch_sources.py) downloads the overview page and every model page it links to into `_sources/`.")
    w("- [`extract_prompts.py`](extract_prompts.py) splits each page on its dated headings and commits each revision one file at a time, with author and committer dates set to the published date, so every commit's diff is a single comparison. Rerunning it only adds revisions not already in git. If Anthropic edits an already-published revision, the change is committed on the day it was noticed with \"(revised)\" in the subject.")
    w("- [`build_readme.py`](build_readme.py) regenerates this README from the sources and the git history.")
    w("- The [update workflow](.github/workflows/update.yml) runs all three on manual dispatch and pushes the result.")
    w("")
    w("To update locally:")
    w("")
    w("```bash")
    w("python3 fetch_sources.py && python3 extract_prompts.py && python3 build_readme.py")
    w("```")

    (ROOT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote README.md ({len(lines)} lines, {len(latest)} models, {len(revisions)} revisions)")


if __name__ == "__main__":
    main()
