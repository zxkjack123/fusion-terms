# Contributing to fusion-terms

## 1) Development setup

1. Clone and enter the repo.
2. Create and activate a virtualenv.
3. Install dev dependencies.

```bash
git clone <repo-url>
cd fusion-terms
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

## 2) Validate changes locally

Run the full test suite before committing:

```bash
pytest tests/ -q
```

Run lint/format checks:

```bash
ruff check .
ruff format --check .
```

Run all hooks exactly as CI expects:

```bash
pre-commit run --all-files
```

## 3) Commit conventions

- Keep each commit focused on one task/intent.
- Write imperative commit messages, with a clear scope.
- Include tests for any behavior change.
- Do not commit generated machine-local state (`*.userdb`, local backups, temp outputs).

## 4) Registry contribution workflow

For terminology registry updates in `terms/registry/`, follow this order:

1. Add/modify concept rows in `concepts.tsv`.
2. Add/modify aliases in `aliases.tsv` (ensure each concept has `kind=preferred`).
3. Add/modify traceable evidence in `evidence.tsv` (no placeholder `internal:TODO` sources).
4. Validate registry:

```bash
python3 -m pipeline.validate_registry
```

5. Rebuild related exports/tests as needed.

## 5) Release flow overview

- Build candidate terms from corpus (`pipeline.extract_candidates`).
- Curate allow/deny/synonyms under `terms/`.
- Build final domain terms (`pipeline.build_terms`).
- Optionally generate/import Rime artifacts (`pipeline.rime_import_safe`).
- For distributable bundles, use `pipeline.release_pack` and verify with `pipeline.verify_release_contract`.

## 6) Pull request checklist

- [ ] Scope is minimal and intentional
- [ ] Tests added/updated for changed behavior
- [ ] `pytest tests/ -q` passes
- [ ] `pre-commit run --all-files` passes
- [ ] Docs/config updated if behavior or interface changed
