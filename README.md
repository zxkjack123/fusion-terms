# fusion-terms

[中文文档](README.zh-CN.md)

A versioned, reproducible **terminology data product and toolchain** for
**fusion / nuclear / plasma engineering**. It imports reliably into the
**Rime (雾凇拼音 / rime-ice)** input method and powers downstream workflows:
automatic fusion translation, bilingual corpus search, report terminology
check & replacement, knowledge-graph building, and OCR extraction quality
control.

## Data-Product Philosophy

This repository manages terminology as a **data product**: every stage of the
pipeline is versioned, reproducible, and auditable.

1. **sources (external corpus)** → Markdown corpus (e.g. pdf2md output)
2. **candidates** → candidate terms with frequency and context (for discovery only — never imported directly)
3. **review (human adjudication)** → allowlist / denylist / synonyms; humans are the final authority
4. **artifacts (generated outputs)** → wordlists, bilingual dictionaries, substitution rules, registry exports, etc.

Every term can be traced back to its source and its review decision.

## Six Application Scenarios

### 1. Automatic Fusion Translation

- `artifacts/translation_dict.json` — a bidirectional zh↔en translation
  dictionary with `zh2en` / `en2zh` directions; short keys are segregated into
  `en2zh_short` to avoid ambiguity (see `[export].min_en_key_len` in
  `config.toml`).
- `artifacts/terminology_substitutions.tsv` — strong-semantic substitution
  pairs (`alias / preferred / status / lang / note`); `status=forbidden` rows
  are used for **correction**, forcing common mistranslations back to their
  canonical forms (e.g. `ASDEX升级 → ASDEX Upgrade`).

### 2. Bilingual Corpus Search

- `artifacts/query_expansions.json` — a query-expansion table composed of
  `concepts` (concept index) and `alias_index` (alias index). It supports
  **bidirectional zh↔en expansion**: querying in Chinese automatically pulls
  in English aliases, and vice versa.
- Retrieved content can be auto-translated into a bilingual corpus, so a
  single search covers both Chinese and English sources.

### 3. IME Wordlist (Rime / rime-ice)

- `artifacts/domain_terms.txt` — the final wordlist, one term per line
  (mixed zh/en, no whitespace inside a term), ready to drop into a Rime
  wordlist directory.
- A **safe import** flow (automatic backup + rollback) feeds it into your
  Rime user dictionary — see "Rime / rime-ice Integration" below.

### 4. Report Terminology Check & Replacement

- `artifacts/vale/terminology_substitute.yml` — a Vale-ready terminology rule
  file (`extends: substitution` swap mapping) that plugs into a Vale gate for
  reports and manuscripts, flagging non-canonical terms with replacement
  suggestions.
- The machine-readable source of truth for the swap pairs is
  `terminology_substitutions.tsv`; both are exported from the same Registry
  and stay in sync.

### 5. Knowledge-Graph Building

The four tables under `terms/registry/` are themselves a **graph data model**:

| Table | Graph role | Fields (header) |
|---|---|---|
| `concepts.tsv` | concept nodes | `concept_id, category, preferred_zh, preferred_en, preferred_abbr, status, notes, source` |
| `aliases.tsv` | alias→concept edges | `alias, concept_id, lang, kind, comment` (`kind`: preferred / alias / deprecated / forbidden) |
| `evidence.tsv` | concept→evidence edges | `concept_id, source, quote, added_by, added_at` |
| `definitions.tsv` | definition attributes | `concept_id, lang, definition, source` |

- `artifacts/registry_exports.json` — a one-stop export: concept and alias
  counts, `query_expansions`, `tag_rules`, `terminology_substitutions`, Vale
  accept/reject wordlists, and more. Feed it directly into a downstream
  knowledge-graph or retrieval system.
- `artifacts/tag_rules.jsonl` — concept tagging rules (with `category`,
  `kind`, `match`), ready for entity-annotation / tagging pipelines.

### 6. OCR Extraction Quality Check & Correction

- Authoritative-glossary extraction under `scripts/`:
  - `extract_gbt4960_md.py` — extracts GB/T 4960.9-2013 *Nuclear Science and Technology Terminology* from Markdown
  - `extract_iaea_glossary.py` — IAEA Safety Glossary 2018 (PDF layout parsing)
  - `fetch_iter_glossary.py` — fetches the ITER Fusion Glossary
  - `ocr_gbt4960.py` — OCR for scanned PDFs (tesseract, chi_sim+eng) + term-pair parsing
- `scripts/diff_terminology_source.py` — **difference review** of
  authoritative glossaries against the Registry: surfaces added, missing, and
  inconsistent entries for human revision.
- `terms/denylist.txt` — human-reviewed **forbidden / correction entries**
  (noise, OCR misreads, deprecated terms), excluded when building the
  wordlist.

## Registry Size

Current size (counted from data rows in `terms/registry/`, excluding comment
and blank lines; as of
[v2026.08.12](https://github.com/zxkjack123/fusion-terms/tree/v2026.08.12)):

| Table | Data rows |
|---|---|
| `concepts.tsv` | 3064 |
| `aliases.tsv` | 10232 |
| `evidence.tsv` | 3156 |
| `definitions.tsv` | 6128 |

Historical snapshot
[v2026.04.14.1](https://github.com/zxkjack123/fusion-terms/tree/v2026.04.14.1)
(see `CHANGELOG.md`): concepts **2697** / aliases **8373** / evidence rows
**2729** / definitions **1549**.

Design doc: `docs/dev/06-terminology-registry-upgrade.md`; version history:
`CHANGELOG.md` (CalVer versioning scheme `vYYYY.MM.DD`).

## Directory Structure

```
fusion-terms/
├── pipeline/     # generation toolchain (extract, build, export, release, validate)
├── terms/        # human-reviewed inputs: allowlist/denylist/synonyms + registry
│   └── registry/ # the four registry tables (concepts/aliases/evidence/definitions)
├── artifacts/    # generated outputs (wordlists, dictionaries, substitution rules, registry exports)
├── sources/      # pointers to the external corpus (does not copy the whole corpus)
├── scripts/      # IAEA / ITER / GB/T 4960 glossary extraction + OCR quality checks
├── docs/dev/     # architecture & design docs
├── tests/        # tests and fixture corpus
└── config.toml   # global configuration
```

## Installation

```bash
git clone https://github.com/zxkjack123/fusion-terms.git
cd fusion-terms
pip install -r requirements.txt
```

Python 3.11+ works out of the box (`requirements.txt` only pins the
low-version compatibility package `tomli`).

## Quick Start

### 1) Extract candidate terms from Markdown corpus

The extractor reads the corpus directory pointed to by `[sources].root` in
`config.toml` (defaults to the in-repo fixtures; change the config or
override via CLI). Outputs:

- `artifacts/candidates_zh.tsv` — Chinese candidates (Han spans of 2–8 characters, with frequency and context)
- `artifacts/candidates_en.tsv` — English / mixed candidates

Encoding rules:

- Files under `terms/` and `terms/registry/` must be **strict UTF-8**; the pipeline fails fast otherwise.
- External corpus may contain bad bytes; the extractor warns and replaces them with `U+FFFD` so upstream problems are easy to locate.

Note: `candidates_*.tsv` are **discovery artifacts** and are never
automatically added to the final wordlist.

### 2) Human review of candidates

- Accepted terms → `terms/allowlist_zh.txt` / `terms/allowlist_en.txt`
- Rejected noise → `terms/denylist.txt`
- (Optional) alias normalization → `terms/synonyms.tsv`

Only the human-reviewed lists under `terms/` take part in the final build —
**humans are the final authority**.

### 3) Build the final wordlist

- Outputs `artifacts/domain_terms.txt`.

Optional: sync to the local Fcitx/Rime wordlist path (default
`~/.config/fcitx/rime/wordlists/domain_terms.txt`, see `config.toml`).

### 4) (Optional) Generate the Rime import file and import

- Generates `artifacts/.rime_import_rime_ice.txt`;
- importing into the user dictionary should prefer the **safe flow**
  (automatic backup + rollback), described in the next section.

## Rime / rime-ice Integration

The safe import/export supports common pass-through options:

- choose the target dictionary name (default `rime_ice`)
- override the Rime user directory (e.g. `~/.config/fcitx/rime`)
- optionally include non-CJK entries
- optionally disable the fcitx auto-restart when the user dictionary is locked

The import payload files (`artifacts/.rime_import_*.txt`), the backup manifest
(`artifacts/rime_backups/`) and the `*.userdb/` directories are **local
machine state** and must not be committed. This repository is the **single
source of truth** — do not treat `*.userdb` as a canonical wordlist.

## Downstream Consumption & Release Contract

This repository is also consumed as a **versioned, verifiable terminology
data product** by downstream toolchains (e.g. the release contract of the
terminology-check / de-AI-fication tool de-ai-fier).

- Contract (what the files mean): `docs/dev/07-de-ai-fier-interface-contract.md`
- Execution plan (how they are produced): `docs/dev/08-de-ai-fier-interface-execution-plan.md`

Design principle: integration/build stages may run Python and pull tags or
release assets; **runtime quality gates must work offline**, reading local
files only.

### Recommended artifacts

Basic (v1):

- `domain_terms.txt` — the plain wordlist (one term per line, no whitespace inside a term)
- `fusion_terms_manifest.json` — sha256 + counts + version/commit metadata

Strongly recommended (v1.1):

- `artifacts/terminology_substitutions.tsv` — strong-semantic substitution pairs derived from the Registry `kind` field
- `artifacts/vale/terminology_substitute.yml` — the Vale-ready substitution rule layer

### Method A: pin a tag and build locally (deterministic)

Pin the tag in your integration/build pipeline, build a self-contained
release root (or tarball), and generate & verify the manifest.

```bash
TAG=v2026.08.12

git clone https://github.com/zxkjack123/fusion-terms.git
cd fusion-terms
git checkout "$TAG"

python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

# Build the release root + tar.gz (including v1.1 substitution-rule exports)
python3 -m pipeline.release_pack \
	--tag "$TAG" \
	--include-registry-exports \
	--substitutions \
	--vale-substitute

# (Optional) re-verify the staged directory that release_pack prints
python3 -m pipeline.verify_release_contract --root "dist/stage/$TAG"
```

After this, downstream projects copy the files they need into their own
repository / runtime image; runtime verification stays offline.

### Method B: download a release asset and verify

If you do not want to run the build pipeline, download the release tarball
published by this repository and verify it locally.

```bash
TAG=v2026.03.29
ASSET="fusion-terms-artifacts-${TAG}.tar.gz"
URL="https://github.com/zxkjack123/fusion-terms/releases/download/${TAG}/${ASSET}"

mkdir -p third_party/fusion-terms/${TAG}
cd third_party/fusion-terms/${TAG}

curl -L -o "$ASSET" "$URL"
tar -xzf "$ASSET"

# Verify the contract (requires the verifier code; vendor it or run from a pinned tag)
python3 -m pipeline.verify_release_contract --root .
```

Note: release tarballs are currently published through `v2026.03.29`; later
versions (up to `v2026.08.12`) exist as git tags only. For the latest data,
prefer Method A.

## Development & Contribution

Contributions of terms and code are welcome. See
[CONTRIBUTING.md](CONTRIBUTING.md) for the dev setup, the registry
contribution workflow, commit conventions, and the pull-request checklist.

Core flow at a glance:

- extract candidates (`pipeline.extract_candidates`)
- review allow/deny/synonyms (`terms/`)
- build the wordlist (`pipeline.build_terms`)
- optionally generate / import Rime artifacts (`pipeline.rime_import_safe`)
- release packaging & verification (`pipeline.release_pack` + `pipeline.verify_release_contract`)

All registry changes must pass `python3 -m pipeline.validate_registry` first.

## License

This project is open-sourced under the [MIT License](LICENSE)
(Copyright (c) 2026 Xiaokang Zhang). You are free to use, modify, and
distribute this project, including for commercial purposes, provided the
original copyright notice and license text are retained.

## Notes

- The extraction strategy is **precision first, then recall expansion**;
  extension designs live in `docs/dev/`.
- If your pdf2md pipeline generates derived Markdown (`*.qa_report.md` /
  `*.autofix.md`, etc.), exclude them via `config.toml`
  (`[sources].exclude_globs`) or the CLI `--exclude-glob`.
