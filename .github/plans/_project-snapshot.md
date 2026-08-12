# Project Snapshot — fusion-terms

**Generated**: 2026-08-12
**Git HEAD**: 09840e0

## Architecture

```
fusion-terms/
├── terms/
│   ├── allowlist_zh.txt        # 2303 lines — Chinese approved terms
│   ├── allowlist_en.txt        # 1353 lines — English approved terms
│   ├── synonyms.tsv            # 53 lines — alias→preferred mappings
│   ├── denylist.txt            # 639 lines — noise/boilerplate tokens
│   ├── stopwords_zh.txt        # Chinese stopwords
│   ├── stopwords_en.txt        # English stopwords
│   └── registry/               # Deeper terminology metadata
│       ├── concepts.tsv        # 3064 concepts
│       ├── definitions.tsv     # 6128 definitions (bilingual)
│       ├── evidence.tsv        # 3156 evidence rows
│       └── aliases.tsv         # 10212 alias mappings
├── pipeline/                   # Python package: build, validation, indexing
├── tests/                      # pytest test suite
├── scripts/                    # Data import/extraction utilities
│   ├── import_approved_terms.py
│   ├── extract_gbt4960_md.py
│   ├── extract_iaea_glossary.py
│   ├── fetch_iter_glossary.py
│   ├── diff_terminology_source.py
│   └── ocr_gbt4960.py
├── pyproject.toml              # pytest + ruff + mypy config
└── .github/workflows/ci.yml    # CI: pytest, mypy, ruff, validate_registry
```

## Key Modules

| Module | Responsibility |
|--------|---------------|
| `pipeline/` | Core terminology processing: build tokens, validate registry, manage allowlist/synonyms/denylist |
| `pipeline/validate_registry` | CI gate: validates concepts, aliases, definitions, evidence integrity |

## Test Commands

```bash
pytest --cov=pipeline --cov-fail-under=45          # Run tests
python3 -m pipeline.validate_registry               # Validate registry integrity
ruff check . && ruff format --check .               # Lint + format check
```

## CI

- Runs on PR + push to main/master
- Python 3.10/3.11/3.12 matrix
- Gates: pytest (45% cov), mypy, ruff, compileall, validate_registry

## Dependencies

- Python 3.10+ with pytest, mypy, ruff
- No external services required for local dev

## Tag Convention

- Semantic versioning: `vYYYY.MM.DD[.N]`
- Latest tags: v2026.04.17, v2026.04.14.1
