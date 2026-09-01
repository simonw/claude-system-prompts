# Claude system prompts

Anthropic publishes the system prompts used by claude.ai and the Claude mobile apps at [platform.claude.com](https://platform.claude.com/docs/en/release-notes/system-prompts/overview), one page per model, with a dated section for every revision. This repository turns those pages into files with a git history: **every published revision is a commit dated the day Anthropic says it went live**, so `git log`, `git diff`, and GitHub's history and compare views show how the prompts have changed over time.

The files here are generated. Do not edit them by hand.

## Files

- `claude-<family>.md` — one file per model family, rewritten with each new prompt in that family. Its history shows the lineage from one model generation to the next.
- `claude-<model>.md` — one file per model, rewritten with each new revision of that model's prompt.
- `claude-<model>-YYYY-MM-DD.md` — one file per published revision, written once and never changed. Permalink to a prompt as it was on a given date.
- `_sources/` — the pages fetched from Anthropic, committed on the day they were fetched.

## Family histories

Each link is the commit history of one family file. Every commit's diff is the change from the previous prompt in that family, including across model generations.

- [Fable](https://github.com/simonw/claude-system-prompts/commits/main/claude-fable.md) — Claude Fable 5 → Claude Fable 5.1
- [Opus](https://github.com/simonw/claude-system-prompts/commits/main/claude-opus.md) — Claude Opus 3 → Claude Opus 5
- [Sonnet](https://github.com/simonw/claude-system-prompts/commits/main/claude-sonnet.md) — Claude Sonnet 3.5 → Claude Sonnet 4.6
- [Haiku](https://github.com/simonw/claude-system-prompts/commits/main/claude-haiku.md) — Claude Haiku 3 → Claude Haiku 4.5

## Latest prompt for each model

Newest first. Each revision is committed one file at a time, so every **what changed** link is a commit whose diff is exactly one comparison: against the previous revision of the same model where there is one, and against the previous prompt in the same family, whichever model that was.

| Model | Published | Prompt | What changed |
| --- | --- | --- | --- |
| Claude Fable 5.1 | 2026-09-01 | [claude-fable-5-1.md](https://github.com/simonw/claude-system-prompts/blob/main/claude-fable-5-1.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/claude-fable-5-1.md)) | [vs previous Fable](https://github.com/simonw/claude-system-prompts/commit/fe9fd66af14d79896e66cc0314047a1155d674db) |
| Claude Opus 5 | 2026-07-24 | [claude-opus-5.md](https://github.com/simonw/claude-system-prompts/blob/main/claude-opus-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/claude-opus-5.md)) | [vs previous Opus](https://github.com/simonw/claude-system-prompts/commit/f3a018b4a4a2d9297df9af2efb6dc5418b093730) |
| Claude Fable 5 | 2026-06-09 | [claude-fable-5.md](https://github.com/simonw/claude-system-prompts/blob/main/claude-fable-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/claude-fable-5.md)) | first Fable prompt ([commit](https://github.com/simonw/claude-system-prompts/commit/1be8fdd096396c39b247d954a378a1119530b055)) |
| Claude Opus 4.8 | 2026-05-28 | [claude-opus-4-8.md](https://github.com/simonw/claude-system-prompts/blob/main/claude-opus-4-8.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/claude-opus-4-8.md)) | [vs previous Opus](https://github.com/simonw/claude-system-prompts/commit/ce6bb1b10d4c6bd96618a569ca1ec1c50711f197) |
| Claude Opus 4.7 | 2026-04-16 | [claude-opus-4-7.md](https://github.com/simonw/claude-system-prompts/blob/main/claude-opus-4-7.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/claude-opus-4-7.md)) | [vs previous Opus](https://github.com/simonw/claude-system-prompts/commit/7138649aa089d30cf54323b138545adbbaee3601) |
| Claude Sonnet 4.6 | 2026-02-17 | [claude-sonnet-4-6.md](https://github.com/simonw/claude-system-prompts/blob/main/claude-sonnet-4-6.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/claude-sonnet-4-6.md)) | [vs previous Sonnet](https://github.com/simonw/claude-system-prompts/commit/5652294b305ac885d31a1c99e920bb70cd430ba1) |
| Claude Opus 4.6 | 2026-02-05 | [claude-opus-4-6.md](https://github.com/simonw/claude-system-prompts/blob/main/claude-opus-4-6.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/claude-opus-4-6.md)) | [vs previous Opus](https://github.com/simonw/claude-system-prompts/commit/03a2088ad302496e42f1cb67e1fd03f97d83a00b) |
| Claude Opus 4.5 | 2026-01-18 | [claude-opus-4-5.md](https://github.com/simonw/claude-system-prompts/blob/main/claude-opus-4-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/claude-opus-4-5.md)) | [vs previous Claude Opus 4.5](https://github.com/simonw/claude-system-prompts/commit/f3d0c8f50df67b2a370b6b5957d1931a68b06992) · [vs previous Opus](https://github.com/simonw/claude-system-prompts/commit/5f8e0f0b4fb8153d5cae4249ab403b89baab0aab) |
| Claude Haiku 4.5 | 2026-01-18 | [claude-haiku-4-5.md](https://github.com/simonw/claude-system-prompts/blob/main/claude-haiku-4-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/claude-haiku-4-5.md)) | [vs previous Claude Haiku 4.5](https://github.com/simonw/claude-system-prompts/commit/732e2de5266c935a7a239912354c4fa1853a049e) · [vs previous Haiku](https://github.com/simonw/claude-system-prompts/commit/1bc846860e3ae58397e35d20acb7ad0817b8c8c4) |
| Claude Sonnet 4.5 | 2026-01-18 | [claude-sonnet-4-5.md](https://github.com/simonw/claude-system-prompts/blob/main/claude-sonnet-4-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/claude-sonnet-4-5.md)) | [vs previous Claude Sonnet 4.5](https://github.com/simonw/claude-system-prompts/commit/7df53dd6da67d0aafd5d8676151a387006de9231) · [vs previous Sonnet](https://github.com/simonw/claude-system-prompts/commit/c5359989dd7fe42aa6ab6d488a5fd8257e49180f) |
| Claude Opus 4.1 | 2025-08-05 | [claude-opus-4-1.md](https://github.com/simonw/claude-system-prompts/blob/main/claude-opus-4-1.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/claude-opus-4-1.md)) | [vs previous Opus](https://github.com/simonw/claude-system-prompts/commit/ea10fa540fd280346679d179c7f6fb60a8314ea0) |
| Claude Opus 4 | 2025-08-05 | [claude-opus-4.md](https://github.com/simonw/claude-system-prompts/blob/main/claude-opus-4.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/claude-opus-4.md)) | [vs previous Claude Opus 4](https://github.com/simonw/claude-system-prompts/commit/77d8430891c1edaa537b3bdb5421e54ae9b2fba5) · [vs previous Opus](https://github.com/simonw/claude-system-prompts/commit/e340dbd63c88e0aa059a70cfebd266121928075d) |
| Claude Sonnet 4 | 2025-08-05 | [claude-sonnet-4.md](https://github.com/simonw/claude-system-prompts/blob/main/claude-sonnet-4.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/claude-sonnet-4.md)) | [vs previous Claude Sonnet 4](https://github.com/simonw/claude-system-prompts/commit/26e83116618e3625e5390189b5e7d7068fe25be1) · [vs previous Sonnet](https://github.com/simonw/claude-system-prompts/commit/b4fc0a8cc1b136d2b3256b83c17e630bd6f29a04) |
| Claude Sonnet 3.7 | 2025-02-24 | [claude-sonnet-3-7.md](https://github.com/simonw/claude-system-prompts/blob/main/claude-sonnet-3-7.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/claude-sonnet-3-7.md)) | [vs previous Sonnet](https://github.com/simonw/claude-system-prompts/commit/b679ce9ce60f68a82338ce450628d0132666d862) |
| Claude Sonnet 3.5 | 2024-11-22 | [claude-sonnet-3-5.md](https://github.com/simonw/claude-system-prompts/blob/main/claude-sonnet-3-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/claude-sonnet-3-5.md)) | [vs previous Claude Sonnet 3.5](https://github.com/simonw/claude-system-prompts/commit/3d5893a88e6fa8eb4b429fa88de2b90ee0d0349e) · [vs previous Sonnet](https://github.com/simonw/claude-system-prompts/commit/199aea114cf995ec7dbd87b4d39d2f52665b85ec) |
| Claude Haiku 3.5 | 2024-10-22 | [claude-haiku-3-5.md](https://github.com/simonw/claude-system-prompts/blob/main/claude-haiku-3-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/claude-haiku-3-5.md)) | [vs previous Haiku](https://github.com/simonw/claude-system-prompts/commit/40b7050371e8b03aaed5e584b8b212bdb8f17d7c) |
| Claude Opus 3 | 2024-07-12 | [claude-opus-3.md](https://github.com/simonw/claude-system-prompts/blob/main/claude-opus-3.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/claude-opus-3.md)) | first Opus prompt ([commit](https://github.com/simonw/claude-system-prompts/commit/4be7aec7909c97cb67d69a5a5aeb6795ee66cac3)) |
| Claude Haiku 3 | 2024-07-12 | [claude-haiku-3.md](https://github.com/simonw/claude-system-prompts/blob/main/claude-haiku-3.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/claude-haiku-3.md)) | first Haiku prompt ([commit](https://github.com/simonw/claude-system-prompts/commit/bb78873d5faba1223dd694d265fca136e1737981)) |

## Every revision

- 2026-09-01 — [Claude Fable 5.1](https://github.com/simonw/claude-system-prompts/blob/main/claude-fable-5-1-2026-09-01.md)
- 2026-07-24 — [Claude Opus 5](https://github.com/simonw/claude-system-prompts/blob/main/claude-opus-5-2026-07-24.md)
- 2026-06-09 — [Claude Fable 5](https://github.com/simonw/claude-system-prompts/blob/main/claude-fable-5-2026-06-09.md)
- 2026-05-28 — [Claude Opus 4.8](https://github.com/simonw/claude-system-prompts/blob/main/claude-opus-4-8-2026-05-28.md)
- 2026-04-16 — [Claude Opus 4.7](https://github.com/simonw/claude-system-prompts/blob/main/claude-opus-4-7-2026-04-16.md)
- 2026-02-17 — [Claude Sonnet 4.6](https://github.com/simonw/claude-system-prompts/blob/main/claude-sonnet-4-6-2026-02-17.md)
- 2026-02-05 — [Claude Opus 4.6](https://github.com/simonw/claude-system-prompts/blob/main/claude-opus-4-6-2026-02-05.md)
- 2026-01-18 — [Claude Opus 4.5](https://github.com/simonw/claude-system-prompts/blob/main/claude-opus-4-5-2026-01-18.md)
- 2026-01-18 — [Claude Haiku 4.5](https://github.com/simonw/claude-system-prompts/blob/main/claude-haiku-4-5-2026-01-18.md)
- 2026-01-18 — [Claude Sonnet 4.5](https://github.com/simonw/claude-system-prompts/blob/main/claude-sonnet-4-5-2026-01-18.md)
- 2025-11-24 — [Claude Opus 4.5](https://github.com/simonw/claude-system-prompts/blob/main/claude-opus-4-5-2025-11-24.md)
- 2025-11-19 — [Claude Haiku 4.5](https://github.com/simonw/claude-system-prompts/blob/main/claude-haiku-4-5-2025-11-19.md)
- 2025-11-19 — [Claude Sonnet 4.5](https://github.com/simonw/claude-system-prompts/blob/main/claude-sonnet-4-5-2025-11-19.md)
- 2025-10-15 — [Claude Haiku 4.5](https://github.com/simonw/claude-system-prompts/blob/main/claude-haiku-4-5-2025-10-15.md)
- 2025-09-29 — [Claude Sonnet 4.5](https://github.com/simonw/claude-system-prompts/blob/main/claude-sonnet-4-5-2025-09-29.md)
- 2025-08-05 — [Claude Opus 4.1](https://github.com/simonw/claude-system-prompts/blob/main/claude-opus-4-1-2025-08-05.md)
- 2025-08-05 — [Claude Opus 4](https://github.com/simonw/claude-system-prompts/blob/main/claude-opus-4-2025-08-05.md)
- 2025-08-05 — [Claude Sonnet 4](https://github.com/simonw/claude-system-prompts/blob/main/claude-sonnet-4-2025-08-05.md)
- 2025-07-31 — [Claude Opus 4](https://github.com/simonw/claude-system-prompts/blob/main/claude-opus-4-2025-07-31.md)
- 2025-07-31 — [Claude Sonnet 4](https://github.com/simonw/claude-system-prompts/blob/main/claude-sonnet-4-2025-07-31.md)
- 2025-05-22 — [Claude Opus 4](https://github.com/simonw/claude-system-prompts/blob/main/claude-opus-4-2025-05-22.md)
- 2025-05-22 — [Claude Sonnet 4](https://github.com/simonw/claude-system-prompts/blob/main/claude-sonnet-4-2025-05-22.md)
- 2025-02-24 — [Claude Sonnet 3.7](https://github.com/simonw/claude-system-prompts/blob/main/claude-sonnet-3-7-2025-02-24.md)
- 2024-11-22 — [Claude Sonnet 3.5](https://github.com/simonw/claude-system-prompts/blob/main/claude-sonnet-3-5-2024-11-22.md)
- 2024-10-22 — [Claude Sonnet 3.5](https://github.com/simonw/claude-system-prompts/blob/main/claude-sonnet-3-5-2024-10-22.md)
- 2024-10-22 — [Claude Haiku 3.5](https://github.com/simonw/claude-system-prompts/blob/main/claude-haiku-3-5-2024-10-22.md)
- 2024-09-09 — [Claude Sonnet 3.5](https://github.com/simonw/claude-system-prompts/blob/main/claude-sonnet-3-5-2024-09-09.md)
- 2024-07-12 — [Claude Sonnet 3.5](https://github.com/simonw/claude-system-prompts/blob/main/claude-sonnet-3-5-2024-07-12.md)
- 2024-07-12 — [Claude Opus 3](https://github.com/simonw/claude-system-prompts/blob/main/claude-opus-3-2024-07-12.md)
- 2024-07-12 — [Claude Haiku 3](https://github.com/simonw/claude-system-prompts/blob/main/claude-haiku-3-2024-07-12.md)

## Notes on the data

- Anthropic marks changes between dated versions of the same model with `**` around the changed text. Those markers are kept as published and are not part of the prompt sent to the model.
- Claude Sonnet 3.5 and Claude Haiku 3.5 have separate "Text only" and "Text and images" prompts under one date. Both are kept, as subsections of the same file.
- Commit dates are the dates on Anthropic's pages, which may lag the day a prompt actually changed in production.

## How it works

- [`fetch_sources.py`](fetch_sources.py) downloads the overview page and every model page it links to into `_sources/`.
- [`extract_prompts.py`](extract_prompts.py) splits each page on its dated headings and commits each revision one file at a time, with author and committer dates set to the published date, so every commit's diff is a single comparison. Rerunning it only adds revisions not already in git. If Anthropic edits an already-published revision, the change is committed on the day it was noticed with "(revised)" in the subject.
- [`build_readme.py`](build_readme.py) regenerates this README from the sources and the git history.
- The [update workflow](.github/workflows/update.yml) runs all three on manual dispatch and pushes the result.

To update locally:

```bash
python3 fetch_sources.py && python3 extract_prompts.py && python3 build_readme.py
```
