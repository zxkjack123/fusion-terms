# fusion-terms: architecture & design

## Goal
Build a **versioned, reproducible fusion-domain terminology lexicon** that can be reliably consumed by Rime (雾凇拼音 / rime-ice),
and can be upgraded into a multi-consumer **terminology registry** (writing gates / search / tagging / data-dictionary).

For the upgrade path and proposed registry data model, see:

- `docs/dev/06-terminology-registry-upgrade.md`

Key properties:

- **Iterative**: improve coverage over time without losing track of changes.
- **Auditable**: every term can be traced to sources and review decisions.
- **Portable**: works across machines; no reliance on opaque `*.userdb` state.

## Term scope (what we aim to cover)

This lexicon targets fusion / nuclear / plasma engineering terms, including:

- device names and facilities (e.g., ITER, EAST, JET, DIII-D)
- acronyms / abbreviations (ICRH, ECRH, NBI, ELM, H-mode)
- methods & diagnostics (Thomson scattering, interferometry, bolometry)
- English method names / noun phrases beyond acronyms (e.g., neutral beam injection)
- materials and alloys (W, Be, Nb3Sn, RAFM steels, CuCrZr)
- parameters / regimes (q95, \u03b2_N, confinement time, pedestal)
- mixed strings (D-T, W/Be, tokamak-related hyphenations)

## Data-flow (recommended)

We separate the pipeline into 4 layers:

1) **Sources**: readable text (Markdown from pdf2md)
2) **Candidates**: extracted term candidates with evidence (freq + contexts)
3) **Review**: human curation (allowlist / denylist / synonyms)
4) **Artifacts**: final wordlist + optional Rime import payload

The sources live outside this repo by default; only curated lists and build scripts are versioned.

## Extensibility: non-breaking extraction upgrades

The repo is designed to accept additional candidate generators without changing the review/build contract.

Example: add an optional **English phrase enhancement mode** (YAKE/RAKE/spaCy noun chunks) that writes
`artifacts/candidates_en_phrases.tsv` while keeping the existing artifacts unchanged.

## Why this structure works

- `terms/*` are the human-maintained "truth".
- `pipeline/*` makes builds reproducible.
- `artifacts/*` are generated and can be committed (recommended for stability) or regenerated.

## Rime integration options

### Option A — Import into userdb (fastest to adopt)

- Build `artifacts/domain_terms.txt`
- Generate a Rime import file (with pinyin for Chinese)
- Import into `rime_ice.userdb`

Pros: minimal Rime configuration.
Cons: userdb is stateful; still ok if this repo is the canonical source.

### Option B — Baked dictionary (`.dict.yaml`) (most stable)

- Build `fusion_terms.dict.yaml`
- Reference from `rime_ice.dict.yaml` via `import_tables`

Pros: stable ordering/weights; great for team sharing.
Cons: more config; needs deploy/rebuild.

We start with Option A and upgrade when the lexicon stabilizes.
