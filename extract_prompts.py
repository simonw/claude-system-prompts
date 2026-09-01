#!/usr/bin/env python3
"""Turn the pages in _sources/ into prompt files with backdated git commits.

Every model page in _sources/ is split on its "## <Month Day, Year>" headings.
Each dated revision writes up to three files into prompts/, and each file
gets its own commit, authored and committed on the published date, so that a commit's diff
shows exactly one file changing:

  <model-slug>-YYYY-MM-DD.md   the prompt as published on that date (written once)
  <model-slug>.md              the latest prompt for that model
  claude-<family>.md           the latest prompt for that family (opus, sonnet, ...)

Commit subjects start with the file name, e.g.
"claude-opus.md: Claude Opus 5 — July 24, 2026".

Revisions already recorded in git (same dated file, same content) are skipped,
so re-running after a fresh fetch only adds what is new. If Anthropic changes
the text of an already-published revision, the files are rewritten in commits
dated today with "(revised)" in the subject.

Usage:
    python3 extract_prompts.py             # write files and commit
    python3 extract_prompts.py --dry-run   # report what would be committed
"""

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCES = ROOT / "_sources"
PROMPTS_DIR = ROOT / "prompts"
BASE_URL = "https://platform.claude.com/docs/en/release-notes/system-prompts/"

AUTHOR_NAME = "Claude"
AUTHOR_EMAIL = "noreply@anthropic.com"

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
DATE_HEADING_RE = re.compile(r"^## (.+?)\s*$", re.MULTILINE)
CARD_HREF_RE = re.compile(r'<Card\b[^>]*\bhref="([^"]+)"')
FAMILY_RE = re.compile(r"^Claude\s+([A-Za-z]+)")
FENCE_OPEN = "```text wrap"
FENCE_CLOSE = "```"


class Revision:
    def __init__(self, model, slug, family, date, date_title, variants, order):
        self.model = model            # "Claude Opus 4.5"
        self.slug = slug              # "claude-opus-4-5"
        self.family = family          # "claude-opus"
        self.date = date              # datetime
        self.date_title = date_title  # "January 18, 2026"
        self.variants = variants      # [(label or None, prompt_text), ...]
        self.order = order            # position of model in overview.md

    @property
    def dated_name(self):
        return f"{self.slug}-{self.date:%Y-%m-%d}.md"

    @property
    def descriptor(self):
        return f"{self.model} — {self.date_title}"

    def render(self):
        parts = [f"# {self.descriptor}\n"]
        for label, text in self.variants:
            if label:
                parts.append(f"## {label}\n")
            parts.append(text.rstrip("\n") + "\n")
        return "\n".join(parts)


def parse_blocks(section):
    """Parse one dated section into [(label, text), ...].

    A short line ending in ":" (e.g. "Text only:") labels the next block.
    A fenced block that directly follows another, with nothing but blank
    lines between, is a continuation of it: the docs site splits a prompt
    into two blocks when the prompt text trips its own fence parsing.
    """
    variants = []
    lines = section.split("\n")
    i = 0
    label = None
    saw_text_since_block = True
    while i < len(lines):
        line = lines[i]
        if line.strip() == FENCE_OPEN:
            j = i + 1
            while j < len(lines) and lines[j].strip() != FENCE_CLOSE:
                j += 1
            text = "\n".join(lines[i + 1 : j])
            if variants and not saw_text_since_block and label is None:
                prev_label, prev_text = variants[-1]
                variants[-1] = (prev_label, prev_text + "\n" + text)
            else:
                variants.append((label, text))
            label = None
            saw_text_since_block = False
            i = j + 1
            continue
        if line.strip():
            saw_text_since_block = True
            if line.rstrip().endswith(":") and len(line) < 60:
                label = line.strip().rstrip(":")
        i += 1
    return variants


def parse_page(path, order):
    text = path.read_text(encoding="utf-8")
    fm = FRONTMATTER_RE.match(text)
    if not fm:
        raise ValueError(f"{path.name}: missing frontmatter")
    title = re.search(r"^title:\s*(.+)$", fm.group(1), re.MULTILINE).group(1).strip()
    model = re.sub(r"\s+system prompts?$", "", title)
    fam = FAMILY_RE.match(model)
    if not fam:
        raise ValueError(f"{path.name}: cannot determine family from {model!r}")
    family = f"claude-{fam.group(1).lower()}"
    body = text[fm.end():]

    headings = list(DATE_HEADING_RE.finditer(body))
    revisions = []
    for k, h in enumerate(headings):
        start = h.end()
        end = headings[k + 1].start() if k + 1 < len(headings) else len(body)
        date_title = h.group(1).strip()
        date = datetime.strptime(date_title, "%B %d, %Y")
        variants = parse_blocks(body[start:end])
        if not variants:
            raise ValueError(f"{path.name}: no prompt block under {date_title!r}")
        revisions.append(
            Revision(model, path.stem, family, date, date_title, variants, order)
        )
    return revisions


def load_revisions():
    overview = (SOURCES / "overview.md").read_text(encoding="utf-8")
    slugs = [h.rstrip("/").rsplit("/", 1)[-1] for h in CARD_HREF_RE.findall(overview)]
    revisions = []
    for order, slug in enumerate(slugs):
        page = SOURCES / f"{slug}.md"
        if not page.exists():
            print(f"warning: {page.name} listed in overview but not fetched", file=sys.stderr)
            continue
        revisions.extend(parse_page(page, order))
    # Same-day ties: the overview lists newest models first, so reverse that
    # order so the newest model is committed last and ends up in the
    # rolling per-family file.
    revisions.sort(key=lambda r: (r.date, -r.order))
    return revisions


def git(*args, env=None):
    return subprocess.run(
        ["git", *args], cwd=ROOT, env=env, check=True, capture_output=True, text=True
    ).stdout


def committed_content(name):
    """Content of prompts/<name> at HEAD, or None if it is not tracked there."""
    try:
        return git("show", f"HEAD:prompts/{name}")
    except subprocess.CalledProcessError:
        return None


def commit(paths, subject, body, when):
    env = os.environ.copy()
    stamp = when.strftime("%Y-%m-%dT%H:%M:%S%z")
    env.update(
        GIT_AUTHOR_NAME=AUTHOR_NAME,
        GIT_AUTHOR_EMAIL=AUTHOR_EMAIL,
        GIT_COMMITTER_NAME=AUTHOR_NAME,
        GIT_COMMITTER_EMAIL=AUTHOR_EMAIL,
        GIT_AUTHOR_DATE=stamp,
        GIT_COMMITTER_DATE=stamp,
    )
    git("add", "--", *paths)
    git("commit", "-q", "-m", subject, "-m", body, env=env)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--dry-run", action="store_true", help="report without writing or committing")
    args = parser.parse_args()

    revisions = load_revisions()

    # Decide what needs committing by comparing against git HEAD.
    pending = []  # (revision, "new" | "revised")
    for rev in revisions:
        existing = committed_content(rev.dated_name)
        if existing is None:
            pending.append((rev, "new"))
        elif existing != rev.render():
            pending.append((rev, "revised"))
    pending_ids = {id(rev) for rev, _ in pending}

    # A rolling file (per-model, per-family) is rewritten by a revision only
    # if every later revision for that model/family is also being written in
    # this run. Otherwise an edit to an old revision would clobber newer text.
    def is_latest(rev, key):
        later = [r for r in revisions if key(r) == key(rev) and (r.date, -r.order) > (rev.date, -rev.order)]
        return all(id(r) in pending_ids for r in later)

    if not pending:
        print("Nothing to do: every revision in _sources/ is already committed.")
        return 0

    now = datetime.now(timezone.utc).replace(microsecond=0)
    for ordinal, (rev, kind) in enumerate(pending):
        paths = [rev.dated_name]
        if is_latest(rev, lambda r: r.slug):
            paths.append(f"{rev.slug}.md")
        if is_latest(rev, lambda r: r.family):
            paths.append(f"{rev.family}.md")

        if kind == "new":
            when = rev.date.replace(hour=12, minute=ordinal % 60, tzinfo=timezone.utc)
            descriptor = rev.descriptor
        else:
            when = now
            descriptor = f"{rev.descriptor} (revised)"

        print(f"{kind:8} {when:%Y-%m-%d}  {descriptor}  ->  {', '.join(paths)}")
        if args.dry_run:
            continue

        content = rev.render()
        body = f"Source: {BASE_URL}{rev.slug}"
        if kind == "revised":
            body += "\n\nThe published text of this dated revision changed after it was first recorded."
        # One commit per file. Successive seconds keep git's date order
        # identical to the commit order.
        PROMPTS_DIR.mkdir(exist_ok=True)
        for n, name in enumerate(paths):
            (PROMPTS_DIR / name).write_text(content, encoding="utf-8")
            commit([f"prompts/{name}"], f"{name}: {descriptor}", body, when + timedelta(seconds=n))

    print(f"\n{'Would commit' if args.dry_run else 'Committed'} {len(pending)} revision(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
