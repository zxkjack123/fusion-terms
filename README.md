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

## Terminology Registry

In addition to IME wordlists, this repo maintains a structured terminology
registry under `terms/registry/`:

- `concepts.tsv` — canonical concept records (`concept_id`, category, preferred forms)
- `aliases.tsv` — preferred/alias/deprecated/forbidden variants bound to a concept
- `evidence.tsv` — traceable source rows per concept

Current snapshot (as of v2026.03.25.1):

- concepts: **949**
- aliases: **4637**
- evidence rows: **949**

Registry schema/design reference:

- `docs/dev/06-terminology-registry-upgrade.md`

Version history:

- `CHANGELOG.md`

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

Rime integration notes:

- The safe importer/exporter now supports pass-through options commonly needed in practice:
	- selecting target dict name (default: `rime_ice`)
	- overriding Rime user dir (e.g. `~/.config/fcitx/rime`)
	- optionally including non-CJK tokens
	- optionally disabling auto-restart of fcitx when the userdb is locked
- Import payload files (`artifacts/.rime_import_*.txt`), backup manifests (`artifacts/rime_backups/`), and `*.userdb/` directories are **machine-local state** and are not meant to be committed.

## de-ai-fier integration (release contract)

This repo can also be consumed as a **versioned, verifiable terminology data product** by downstream tooling (e.g. de-ai-fier).

- Contract (what the files mean): `docs/dev/07-de-ai-fier-interface-contract.md`
- Execution plan (how to produce them): `docs/dev/08-de-ai-fier-interface-execution-plan.md`

Design principle:

- Integration/build stage may run Python / fetch tags or release assets.
- Runtime quality gate should be **offline** and only **read local files**.

### What to consume

Minimum (v1):

- `domain_terms.txt` — token-only wordlist (one term per line; no whitespace inside a term)
- `fusion_terms_manifest.json` — sha256 + counts + version/commit metadata

Strongly recommended (v1.1):

- `artifacts/terminology_substitutions.tsv` — strong-semantic substitutions derived from registry(kind)
- `artifacts/vale/terminology_substitute.yml` — Vale-ready convenience layer (swap mapping)

### Method A: pin tag and build (deterministic)

In your integration/build pipeline, pin a tag and build a self-contained release root (or a tarball) with the manifest generated and verified.

```bash
TAG=v2026.03.25.1

git clone https://github.com/zxkjack123/fusion-terms.git
cd fusion-terms
git checkout "$TAG"

python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

# Build a staged release root + tar.gz (includes v1.1 substitution exports)
python3 -m pipeline.release_pack \
	--tag "$TAG" \
	--include-registry-exports \
	--substitutions \
	--vale-substitute

# (Optional) verify again using the staged directory printed by release_pack
python3 -m pipeline.verify_release_contract --root "dist/stage/$TAG"
```

After this, your downstream project can copy the required files into its own repo/runtime image and keep runtime checks offline.

### Method B: download release asset and verify

If you prefer not to run the fusion-terms build pipeline, download the release tarball built by fusion-terms and verify locally.

```bash
TAG=v2026.03.25.1
ASSET="fusion-terms-artifacts-${TAG}.tar.gz"
URL="https://github.com/zxkjack123/fusion-terms/releases/download/${TAG}/${ASSET}"

mkdir -p third_party/fusion-terms/${TAG}
cd third_party/fusion-terms/${TAG}

curl -L -o "$ASSET" "$URL"
tar -xzf "$ASSET"

# Verify contract (requires the verifier code; you can vendor it or run it from a pinned tag)
python3 -m pipeline.verify_release_contract --root .
```

## Notes

- This repo is the **source of truth**. Do not treat `*.userdb` as your canonical lexicon.
- High-precision extraction first; you can expand recall later (see `docs/dev/`).

Tip: if your pdf2md pipeline generates derived Markdown like `*.qa_report.md` / `*.autofix.md`, you can exclude them via `config.toml` (`[sources].exclude_globs`) or CLI flags (`--exclude-glob`).
