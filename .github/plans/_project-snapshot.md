# Project Snapshot — fusion-terms

**Generated**: 2026-10-25
**Updated**: 2026-10-29 (T-4973 W3a naming + allowlist and T4.1/T4.2/T4.3 re-verified; PM 5072 evidence/释义 follow-up remains open; snapshot counts re-verified against `pipeline.validate_registry`)
**Release**: `v2026.10.25` (tag → commit 8299146); registry counts below are that release's

## Architecture

```
fusion-terms/
├── terms/
│   ├── allowlist_zh.txt        # 3929 raw lines — Chinese approved terms
│   ├── allowlist_en.txt        # 2817 raw lines — English approved terms
│   ├── synonyms.tsv            # 53 lines — alias→preferred mappings
│   ├── denylist.txt            # 639 lines — noise/boilerplate tokens
│   ├── stopwords_zh.txt        # Chinese stopwords
│   ├── stopwords_en.txt        # English stopwords
│   └── registry/               # Deeper terminology metadata
│       ├── concepts.tsv        # 3076 concepts
│       ├── definitions.tsv     # 6152 definitions (bilingual)
│       ├── evidence.tsv        # 3203 evidence rows
│       └── aliases.tsv         # 10249 alias mappings
├── pipeline/                   # Python package: build, validation, indexing
├── tests/                      # pytest test suite
├── scripts/                    # Data import/extraction utilities
│   ├── import_approved_terms.py
│   ├── extract_gbt4960_md.py
│   ├── extract_iaea_glossary.py
│   ├── fetch_iter_glossary.py
│   ├── diff_terminology_source.py
│   ├── ocr_gbt4960.py
│   └── registry_evidence_bundle.py  # read-only registry gate evidence bundle (--profile/--compare/--reuse)
├── pyproject.toml              # pytest + ruff + mypy config
└── .github/workflows/ci.yml    # CI: pytest, mypy, ruff, validate_registry
```

Registry counts above come from `python3 -m pipeline.validate_registry`
(authoritative); `allowlist_*` / `synonyms` / `denylist` counts are raw `wc -l`.

## Key Modules

| Module | Responsibility |
|--------|---------------|
| `pipeline/` | Core terminology processing: build tokens, validate registry, manage allowlist/synonyms/denylist |
| `pipeline/validate_registry` | CI gate: validates concepts, aliases, definitions, evidence integrity |
| `pipeline/export_registry` | Exports multi-consumer artifacts: translation dict, query expansions, substitutions, Vale rules |
| `pipeline/build_terms` | Builds the IME wordlist (`artifacts/domain_terms.txt`) from the curated allowlists |
| `pipeline/sync_to_fcitx` | Syncs the wordlist into the local Rime/fcitx user wordlist |
| `pipeline/release_pack` + `verify_release_contract` | Release staging, manifest and artifact contract verification |

## Downstream rebuild chain

```bash
python3 -m pipeline.export_registry --terms-dir terms --out-dir artifacts \
    --query-expansions --substitutions --translation-dict
python3 -m pipeline.build_terms --config config.toml
python3 -m pipeline.sync_to_fcitx
python3 -m pipeline.release_pack --tag vYYYY.MM.DD --translation-dict --substitutions --query-expansions
python3 -m pipeline.verify_release_contract --root dist/stage/vYYYY.MM.DD
```

## Test Commands

```bash
pytest --cov=pipeline --cov-fail-under=45          # Run tests
python3 -m pipeline.validate_registry               # Validate registry integrity
ruff check . && ruff format --check .               # Lint + format check
```

## CI

- Runs on PR + push to main/master
- Python 3.10/3.11/3.12 matrix
- Gates: pytest (45% cov), mypy (`pipeline/` only), ruff, compileall, validate_registry
- Evidence bundle (read-only gate capture): `scripts/registry_evidence_bundle.py --compare` (default
  `--profile w0`) captures gate inputs/outputs into `artifacts/registry-evidence/<UTC-stamp>/`;
  bundles are machine-local and gitignored (only `artifacts/registry-evidence/README.md` is
  tracked). `--profile all` now passes (T-4973 W1 complete; verified `--compare --profile all`
  ⇒ exit 0, `status=pass`) and is the stricter pre-release profile.
- **`ruff format --check .` also covers fenced code blocks inside Markdown.** ruff is
  pinned (`ruff==0.17.2` in `requirements-dev.txt`, `ruff-pre-commit` rev in
  `.pre-commit-config.yaml`) because an unpinned floor silently reddened CI for two
  months (runs #39–#42) when ruff ≥ 0.16 changed code-block formatting.

## Dependencies

- Python 3.10+ with pytest, mypy, ruff (`ruff==0.17.2`, pinned — keep in lockstep with
  `.pre-commit-config.yaml`)
- No external services required for local dev
- `pipeline/generate_dict_yaml` additionally needs `~/.local/bin/rime_import_wordlist.py`
  (absent on this machine; the fcitx path via `sync_to_fcitx` works without it)

## Tag Convention

- Semantic versioning: `vYYYY.MM.DD[.N]`
- Latest tags: v2026.10.25, v2026.08.12
