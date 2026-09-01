#!/usr/bin/env python3
"""Fetch Anthropic's published Claude system prompt pages into _sources/.

Reads the overview page, finds every linked model page, and downloads the
markdown version of each (the page URL with ".md" appended). Files are
written to _sources/<slug>.md, plus _sources/overview.md for the index.

Usage:
    python3 fetch_sources.py            # fetch everything
    python3 fetch_sources.py --quiet    # only print changed/new files
"""

import argparse
import re
import sys
import urllib.request
from pathlib import Path

OVERVIEW_URL = (
    "https://platform.claude.com/docs/en/release-notes/system-prompts/overview.md"
)
SOURCES_DIR = Path(__file__).resolve().parent / "_sources"
USER_AGENT = "claude-system-prompts fetcher (https://github.com/simonw/claude-system-prompts)"

CARD_HREF_RE = re.compile(r'<Card\b[^>]*\bhref="([^"]+)"')


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8")


def write_if_changed(path: Path, text: str) -> str:
    """Write text to path; return 'new', 'changed', or 'unchanged'."""
    if path.exists():
        if path.read_text(encoding="utf-8") == text:
            return "unchanged"
        path.write_text(text, encoding="utf-8")
        return "changed"
    path.write_text(text, encoding="utf-8")
    return "new"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--quiet", action="store_true", help="only report new or changed files")
    args = parser.parse_args()

    SOURCES_DIR.mkdir(exist_ok=True)

    overview = fetch(OVERVIEW_URL)
    status = write_if_changed(SOURCES_DIR / "overview.md", overview)
    if not args.quiet or status != "unchanged":
        print(f"{status:9} overview.md")

    hrefs = CARD_HREF_RE.findall(overview)
    if not hrefs:
        print("error: no <Card href=...> links found in overview page", file=sys.stderr)
        return 1

    seen = set()
    for href in hrefs:
        slug = href.rstrip("/").rsplit("/", 1)[-1]
        if slug in seen:
            continue
        seen.add(slug)
        url = href if href.endswith(".md") else href + ".md"
        text = fetch(url)
        status = write_if_changed(SOURCES_DIR / f"{slug}.md", text)
        if not args.quiet or status != "unchanged":
            print(f"{status:9} {slug}.md")

    print(f"Fetched {len(seen)} model page(s) into {SOURCES_DIR.relative_to(Path.cwd())}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
