#!/usr/bin/env python3
"""Generate README.md and CHANGELOG.md.

Inputs are the fetched pages in _sources/, the prompt files in prompts/, the
LLM summaries in _summary/, and the git history. Run after extract_prompts.py
and summarize_commits.py so links and summaries resolve:

    python3 build_readme.py
"""

import html
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import extract_prompts as ep
import summarize_commits as sc

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


def repo_slug():
    url = git("remote", "get-url", "origin")
    m = re.match(r"(?:git@github\.com:|https://github\.com/)([^/]+/[^/]+?)(?:\.git)?$", url)
    if not m:
        sys.exit(f"Cannot derive GitHub URL from remote {url!r}")
    return m.group(1)


def repo_url():
    return f"https://github.com/{repo_slug()}"


def pages_url():
    owner, repo = repo_slug().split("/")
    return f"https://{owner}.github.io/{repo}/"


def anchor(heading):
    """GitHub's anchor for a markdown heading."""
    text = re.sub(r"[^\w\- ]", "", heading.lower())
    return text.replace(" ", "-")


def bullets_to_html(markdown):
    items = []
    for line in markdown.splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        text = html.escape(line[2:])
        text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
        items.append(f"<li>{text}</li>")
    return "<ul>" + "".join(items) + "</ul>"


def commit_for(name, descriptor):
    """Sha of the newest commit to prompts/<name> whose subject is "<name>: <descriptor>".

    A later "(revised)" commit for the same revision shares that prefix and
    wins, so the link always shows the text as currently published.
    """
    out = git("log", "-1", "--format=%H", "-F", f"--grep={name}: {descriptor}",
              "--", f"prompts/{name}")
    return out or None


def created_in(path):
    """Sha of the commit that first added path."""
    return git("log", "--diff-filter=A", "--format=%H", "--", path)


def label(family):
    return FAMILY_LABELS.get(family, family)


def short_date(text):
    """"November 19, 2025" -> "Nov 19, 2025"."""
    d = datetime.strptime(text, "%B %d, %Y")
    return f"{d:%b} {d.day}, {d.year}"


def split_title(title):
    """"Claude Fable 5 — June 9, 2026" -> ("Fable 5", "Jun 9, 2026")."""
    model, _, date = title.partition(" — ")
    return model.removeprefix("Claude "), short_date(date)


def change_heading(change):
    """"Fable 5 → Fable 5.1 on Sep 1, 2026", or for a new revision of the
    same model "Haiku 4.5 (Nov 19, 2025) → Haiku 4.5 (Jan 18, 2026)"."""
    prev_model, prev_date = split_title(change.prev_title)
    new_model, new_date = split_title(change.new_title)
    if prev_model == new_model:
        return f"{new_model} ({prev_date}) → {new_model} ({new_date})"
    return f"{prev_model} → {new_model} on {new_date}"


def compared_with(change):
    prev_model, prev_date = split_title(change.prev_title)
    new_model, _ = split_title(change.new_title)
    if prev_model == new_model:
        return f"Compared with the {prev_date} revision"
    return f"Compared with {prev_model}"


def summary_block(change):
    text = change.summary() if change else None
    return text if text else "*Summary not generated yet.*"


def main():
    base = repo_url()
    revisions = ep.load_revisions()
    changes = sc.list_changes()          # newest first
    by_sha = {c.sha: c for c in changes}

    latest, count = {}, {}
    for rev in revisions:
        latest[rev.slug] = rev
        count[rev.slug] = count.get(rev.slug, 0) + 1
    families = []  # newest family first, following the order of the overview page
    for rev in sorted(revisions, key=lambda r: r.order):
        if rev.family not in families:
            families.append(rev.family)
    family_created = {f: created_in(f"prompts/{f}.md") for f in families}

    def commit_link(sha):
        return f"{base}/commit/{sha}"

    # ------------------------------------------------------------ README
    out = []
    w = out.append
    feed_url = pages_url() + "feed.atom"
    w("# Claude system prompts revision history")
    w("")
    w(f"[![Atom feed](https://img.shields.io/badge/Atom-feed-orange?logo=rss&logoColor=white)]({feed_url})")
    w("")
    w(
        "Anthropic publishes the system prompts used by claude.ai and the Claude mobile "
        f"apps at [platform.claude.com]({SOURCE_URL}), one page per model, with a dated "
        "section for every revision. This repository turns those pages into files in "
        "[`prompts/`](prompts/) with a git history: **every published revision is a commit "
        "dated the day Anthropic says it went live**, so `git log`, `git diff`, and "
        "GitHub's history views show how the prompts have changed over time. Each change "
        "also gets a short LLM-written summary of what is new."
    )
    w("")
    w(
        "[Transcript from building this repo]"
        "(https://gisthost.github.io/?f1399e27b6a832f0e790b696af812c9b/index.html) "
        "using Claude Fable 5.1. See [this blog post]"
        "(https://simonwillison.net/2026/Sep/2/claudes-new-system-prompt/#how-i-m-tracking-these-prompts) "
        "for background on this project."
    )
    w("")

    w("## Latest changes")
    w("")
    w("The most recent change to each model family, summarized from the diff by "
      f"`{sc.MODEL}`. [CHANGELOG.md](CHANGELOG.md) has every change, and the "
      f"[Atom feed]({feed_url}) delivers new ones.")
    w("")
    for fam in families:
        newest = next((c for c in changes if c.path == f"prompts/{fam}.md"), None)
        if newest is None:
            first = next(r for r in revisions if r.family == fam)
            w(f"### {first.model.removeprefix('Claude ')} on {short_date(first.date_title)}")
            w("")
            w(f"First prompt in the {label(fam)} family, so there is no earlier prompt to compare against. "
              f"[Read the prompt](prompts/{fam}.md).")
            w("")
            continue
        w(f"### {change_heading(newest)}")
        w("")
        w(summary_block(newest))
        w("")
        w(f"[Diff]({commit_link(newest.sha)}) · [prompt](prompts/{fam}.md) · "
          f"[history]({base}/commits/main/prompts/{fam}.md)")
        w("")

    w("## Files")
    w("")
    w("Everything lives in [`prompts/`](prompts/):")
    w("")
    w("- `claude-<family>.md` — one file per model family, rewritten with each new prompt in that family. Its history shows the lineage from one model generation to the next.")
    w("- `claude-<model>.md` — one file per model, rewritten with each new revision of that model's prompt.")
    w("- `claude-<model>-YYYY-MM-DD.md` — one file per published revision, written once and never changed. Permalink to a prompt as it was on a given date.")
    w("")
    w("Alongside it:")
    w("")
    w("- `_sources/` — the pages fetched from Anthropic, committed on the day they were fetched.")
    w("- `_summary/<commit>.md` — the LLM-written summary of one commit's diff.")
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
        w(f"- [{label(fam)}]({base}/commits/main/prompts/{fam}.md) — {span}")
    w("")

    w("## Latest prompt for each model")
    w("")
    w("Newest first. Each revision is committed one file at a time, so every **what changed** link is a commit whose diff is exactly one comparison: against the previous revision of the same model where there is one, and against the previous prompt in the same family, whichever model that was. **Summary** links go to the LLM-written summary of that diff.")
    w("")
    w("| Model | Published | Prompt | What changed |")
    w("| --- | --- | --- | --- |")
    ordered = sorted(latest.values(), key=lambda r: (r.date, -r.order), reverse=True)
    for rev in ordered:
        items = []
        if count[rev.slug] > 1:
            sha = commit_for(f"{rev.slug}.md", rev.descriptor)
            if sha:
                items.append((f"vs previous {rev.model}", sha))
        sha = commit_for(f"{rev.family}.md", rev.descriptor)
        if sha and sha != family_created[rev.family]:
            items.append((f"vs previous {label(rev.family)}", sha))
        cells = []
        for text, sha in items:
            change = by_sha.get(sha)
            cell = f"[{text}]({commit_link(sha)})"
            if change and change.summary():
                cell += f" ([summary](_summary/{change.canonical_sha}.md))"
            cells.append(cell)
        if not cells:
            sha = commit_for(rev.dated_name, rev.descriptor)
            cells.append(f"first {label(rev.family)} prompt ([commit]({commit_link(sha)}))")
        w(
            f"| {rev.model} | {rev.date:%Y-%m-%d} | "
            f"[{rev.slug}.md](prompts/{rev.slug}.md) "
            f"([history]({base}/commits/main/prompts/{rev.slug}.md)) | "
            + " · ".join(cells) + " |"
        )
    w("")

    w("## Notes on the data")
    w("")
    w("- Anthropic marks changes between dated versions of the same model with `**` around the changed text. Those markers are kept as published and are not part of the prompt sent to the model.")
    w("- Claude Sonnet 3.5 and Claude Haiku 3.5 have separate \"Text only\" and \"Text and images\" prompts under one date. Both are kept, as subsections of the same file.")
    w("- Commit dates are the dates on Anthropic's pages, which may lag the day a prompt actually changed in production.")
    w("- Summaries are written by a language model from the diff and can miss things or misread a rewording as a change. The diff is the source of truth.")
    w("")

    w("## How it works")
    w("")
    w("- [`fetch_sources.py`](fetch_sources.py) downloads the overview page and every model page it links to into `_sources/`.")
    w("- [`extract_prompts.py`](extract_prompts.py) splits each page on its dated headings and commits each revision one file at a time, with author and committer dates set to the published date, so every commit's diff is a single comparison. Rerunning it only adds revisions not already in git. If Anthropic edits an already-published revision, the change is committed on the day it was noticed with \"(revised)\" in the subject.")
    w(f"- [`summarize_commits.py`](summarize_commits.py) finds commits that change a per-model or per-family file and, for each one without a summary, pipes the word-level diff plus both full prompts through [`llm`](https://llm.datasette.io/) using `{sc.MODEL}`. The result is saved to `_summary/<commit>.md`.")
    w("- [`build_readme.py`](build_readme.py) regenerates this README, CHANGELOG.md, and the Atom feed from all of the above.")
    w("- The [update workflow](.github/workflows/update.yml) runs everything on manual dispatch and pushes the result.")
    w("")
    w("To update locally:")
    w("")
    w("```bash")
    w("python3 fetch_sources.py && python3 extract_prompts.py && python3 summarize_commits.py && python3 build_readme.py")
    w("```")
    (ROOT / "README.md").write_text("\n".join(out) + "\n", encoding="utf-8")

    # ------------------------------------------- CHANGELOG and Atom feed
    entries = []  # (rev, [(canonical change, suffix), ...])
    for rev in sorted(revisions, key=lambda r: (r.date, -r.order), reverse=True):
        rev_changes = [c for c in changes
                       if c.descriptor.replace(" (revised)", "") == rev.descriptor]
        items, seen = [], set()
        for c in sorted(rev_changes, key=lambda c: (c.kind != "family", c.sha)):
            if c.canonical_sha in seen:
                continue
            seen.add(c.canonical_sha)
            suffix = " (revised)" if "(revised)" in c.descriptor else ""
            items.append((by_sha[c.canonical_sha], suffix))
        entries.append((rev, items))

    def entry_heading(rev):
        return f"{rev.date:%Y-%m-%d}: {rev.model}"

    def entry_title(rev, items):
        if items:
            return change_heading(items[0][0])
        return f"{rev.model.removeprefix('Claude ')} on {short_date(rev.date_title)} (first {label(rev.family)} prompt)"

    out = []
    w = out.append
    w("# Changelog")
    w("")
    w("Every published revision of Claude's claude.ai system prompt, newest first, with an "
      f"LLM-written summary of each diff (generated by `{sc.MODEL}` from the word-level diff "
      "and both full prompts; see [README.md](README.md) for how). Summaries can miss things "
      "or misread a rewording as a change: the linked diff is the source of truth. "
      f"Subscribe to the [Atom feed]({feed_url}) for new entries.")
    w("")
    summaries_used = 0
    for rev, items in entries:
        w(f"## {entry_heading(rev)}")
        w("")
        w(f"[Full prompt](prompts/{rev.dated_name})")
        w("")
        for canonical, suffix in items:
            w(f"**{compared_with(canonical)}**{suffix} · [diff]({commit_link(canonical.sha)})")
            w("")
            w(summary_block(canonical))
            w("")
            if canonical.summary():
                summaries_used += 1
        if not items:
            w(f"First prompt in the {label(rev.family)} family.")
            w("")
    (ROOT / "CHANGELOG.md").write_text("\n".join(out) + "\n", encoding="utf-8")

    def atom_date(d):
        return d.replace(hour=12, tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    x = []
    w = x.append
    w('<?xml version="1.0" encoding="utf-8"?>')
    w('<feed xmlns="http://www.w3.org/2005/Atom">')
    w("  <title>Claude system prompts revision history</title>")
    w(f"  <subtitle>Every published revision of the claude.ai system prompt, with an LLM-written summary of what changed</subtitle>")
    w(f'  <link href="{html.escape(feed_url)}" rel="self" type="application/atom+xml"/>')
    w(f'  <link href="{html.escape(base)}" rel="alternate" type="text/html"/>')
    w(f"  <id>{html.escape(pages_url())}</id>")
    w(f"  <updated>{atom_date(entries[0][0].date)}</updated>")
    w("  <author><name>Anthropic, via simonw/claude-system-prompts</name></author>")
    for rev, items in entries:
        page = f"{base}/blob/main/CHANGELOG.md#{anchor(entry_heading(rev))}"
        parts = []
        for canonical, suffix in items:
            parts.append(
                f"<p><strong>{html.escape(compared_with(canonical))}{suffix}</strong> · "
                f'<a href="{html.escape(commit_link(canonical.sha))}">diff</a></p>'
            )
            summary = canonical.summary()
            parts.append(bullets_to_html(summary) if summary else "<p><em>Summary not generated yet.</em></p>")
        if not items:
            parts.append(f"<p>First prompt in the {html.escape(label(rev.family))} family.</p>")
        parts.append(f'<p><a href="{html.escape(base)}/blob/main/prompts/{rev.dated_name}">Full prompt</a></p>')
        w("  <entry>")
        w(f"    <title>{html.escape(entry_title(rev, items))}</title>")
        w(f'    <link href="{html.escape(page)}" rel="alternate" type="text/html"/>')
        w(f"    <id>{html.escape(base)}/blob/main/prompts/{rev.dated_name}</id>")
        w(f"    <updated>{atom_date(rev.date)}</updated>")
        w(f"    <published>{atom_date(rev.date)}</published>")
        w(f'    <content type="html">{html.escape("".join(parts))}</content>')
        w("  </entry>")
    w("</feed>")
    (ROOT / "feed.atom").write_text("\n".join(x) + "\n", encoding="utf-8")

    print(f"Wrote README.md, CHANGELOG.md, and feed.atom: {len(latest)} models, {len(revisions)} revisions, "
          f"{summaries_used} summaries embedded")


if __name__ == "__main__":
    main()
