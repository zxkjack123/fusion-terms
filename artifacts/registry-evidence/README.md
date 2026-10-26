# Registry evidence bundles

## Purpose
Capture mechanical registry checks and their inputs; this does not replace bilingual semantic review.

## Commands
Run `python3 scripts/registry_evidence_bundle.py --compare` (default `--profile w0`).
Use `--profile all` to check full quality; unfinished W1 work currently makes it fail.
Use `--reuse <bundle>` with the original profile to revalidate saved evidence.

## Layout
New bundles contain `manifest.json`, `baseline/`, `batch/`, and `snapshot/`.
`backups/` preserves earlier source versions. Older schemas are historical experiments, not current acceptance evidence.

## Reuse
Reuse checks the fingerprint, snapshot hashes, evidence hashes, parsed results and comparison.
Top-level success text alone is not sufficient. Hashes detect accidental changes, not authenticated authorship.

## Invalidation
Data, checker code, profile, Python environment and git-status changes can invalidate reuse.
Regenerate evidence for the new execution state; retain old bundles as history, without claiming current acceptance.

## Retention
The `.gitignore` rule excludes generated bundles and backups; only this README is tracked.
Historical bundles are preserved, not deleted. Cleanup requires a separate decision.
