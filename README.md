# fusion-terms

A versioned, reproducible terminology lexicon for **fusion / nuclear / plasma engineering** that can be reliably imported into **Rime (雾凇拼音 / rime-ice)**.

This repo treats “terms” as a data product:

- **sources (external)** → Markdown corpus (your pdf2md output)
- **candidates** → extracted candidate terms (counts + contexts)
- **review** → allowlist/denylist/synonyms
- **artifacts** → final wordlist + optional Rime import file

## Folder layout

- `docs/dev/` — design notes and workflow
- `pipeline/` — scripts (extract, build, export)
- `terms/` — human-reviewed inputs (allow/deny/synonyms)
- `artifacts/` — generated outputs (final wordlist, import files)
- `sources/` — optional pointers (we do not copy your whole corpus here)

## Quick start

1) Extract candidate terms from your Markdown corpus:

- Uses the default source root from `config.toml` (edit if needed).
- Outputs `artifacts/candidates_zh.tsv` and `artifacts/candidates_en.tsv`.

Encoding note:

- Files under `terms/` and `terms/registry/` are expected to be **valid UTF-8** (strict).
- Your external Markdown corpus may contain bad bytes; the extractor will warn and replace invalid bytes with `U+FFFD` so you can fix the upstream source.

Important: `candidates_*.tsv` are **discovery artifacts only**. They are not
automatically included in the final wordlist.

2) Review candidates and curate:

- Add accepted terms into `terms/allowlist_zh.txt` / `terms/allowlist_en.txt`
- Add rejected/noise terms into `terms/denylist.txt`
- (Optional) normalize aliases in `terms/synonyms.tsv`

Only the curated lists under `terms/` are used to build the final wordlist, so
you (the human reviewer) are always the final arbiter.

3) Build final wordlist:

- Writes `artifacts/domain_terms.txt`

Optional: sync to your local Fcitx/Rime wordlists path:

- Copies to `~/.config/fcitx/rime/wordlists/domain_terms.txt`

4) (Optional) Generate Rime import file and import:

- If you already use `~/.local/bin/rime_import_wordlist.py`, you can generate `artifacts/.rime_import_rime_ice.txt`.
- For importing into your Rime userdb, prefer the safer flow (`pipeline.rime_import_safe`) which creates backups and supports rollback.

## Notes

- This repo is the **source of truth**. Do not treat `*.userdb` as your canonical lexicon.
- High-precision extraction first; you can expand recall later (see `docs/dev/`).

Tip: if your pdf2md pipeline generates derived Markdown like `*.qa_report.md` / `*.autofix.md`, you can exclude them via `config.toml` (`[sources].exclude_globs`) or CLI flags (`--exclude-glob`).
