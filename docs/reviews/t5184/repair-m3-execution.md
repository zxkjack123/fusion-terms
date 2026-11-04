# T-5257 — M3 A′ execution report (evidence)

Audience: repository developers / agents. External-facing de-ai-fier (§0) not applicable.

- Date: `2026-11-04T23:33:19+08:00` (run `date -Iseconds`; recorded in `gates-after-rev3.txt`)
- Baseline commit under repair: `6c051ed` (plan baseline)
- Commits produced (both `#T-5257`):
  - `ef9cd4e` — `chore(artifacts): refresh stale translation_dict from HEAD registry (generated_at 2026-10-26 -> 2026-11-04) (#T-5257)` (M3-4 ① baseline refresh; 1 file)
  - `5013321` — `fix(registry): move 物理溅射 from sputtering alias to physical-sputtering preferred (M3 A') (#T-5257)` (M3-4 ② A′ atomic; 6 files)
- Adjudication: user 2026-11-04, plan §0 / §0.3 R6–R10; option A′ only (B/C excluded). Local workspace + local commit only.

## 1. Registry change (verbatim before/after)

Removed row (was `terms/registry/aliases.tsv:397`):

```
物理溅射	sputtering	zh	alias	physical sputtering zh
```

Added row (inserted after the unique anchor `physical sputtering	physical-sputtering	en	preferred`):

```
物理溅射	physical-sputtering	zh	preferred	zh preferred (M3 A': moved from sputtering alias)
```

`git diff --numstat -- terms/registry/aliases.tsv` = `1	1`. File length 11568 → 11568 (net 0).

## 2. Projection before/after (12 checks)

`before` = export of the HEAD-side registry (`/tmp/opencode/t5184-repair/head-export/`, proven to equal the baseline refresh committed in `ef9cd4e`); `after` = export of the A′ registry (`artifacts/`, re-verified by V8 idempotency).

| # | Projection / assertion | before (baseline) | after (A′) |
|---|---|---|---|
| 1 | `aliases.tsv` row `物理溅射 → sputtering` exists | yes | no |
| 2 | `aliases.tsv` rows `物理溅射 / physical-sputtering / zh / preferred` | 0 | 1 |
| 3 | `translation_dict.zh2en['物理溅射']` | `sputtering` | `physical sputtering` |
| 4 | `translation_dict.zh2en['溅射']` | `sputtering` | `sputtering` |
| 5 | `translation_dict.en2zh['physical sputtering']` | `物理溅射` | `物理溅射` |
| 6 | `translation_dict.en2zh['sputtering']` | `溅射` | `溅射` |
| 7 | `query_expansions.alias_index['物理溅射']` | `sputtering` | `physical-sputtering` |
| 8 | `物理溅射 ∈ all_terms['physical-sputtering']` | no | yes |
| 9 | `物理溅射 ∈ all_terms['sputtering']` | yes | no |
| 10 | `terminology_substitutions` target of `物理溅射率` | `physical sputtering` | `物理溅射` |
| 11 | `forbidden['physical-sputtering']` | `['物理喷溅','物理溅射率','物理飞溅']` | unchanged |
| 12 | `aliases.tsv` line count | 11568 | 11568 |

Row 10 is the expected derived side effect K-2: the same-language preferred target (zh) replaces the earlier en fallback for the three forbidden entries. The three forbidden rows `aliases.tsv:3812/3813/7050` were **not** rewritten (plan §2.2 item 5 / AC-5); their field text is byte-identical to the baseline.

## 3. Post-repair projection assertion (V6, 8 assertions)

```
PROJECTION_OK
```

Reproduced by:

```python
import json
d=json.load(open('artifacts/translation_dict.json',encoding='utf-8'))
q=json.load(open('artifacts/query_expansions.json',encoding='utf-8'))
assert d['zh2en']['物理溅射']=='physical sputtering'
assert d['zh2en']['溅射']=='sputtering'
assert d['en2zh']['physical sputtering']=='物理溅射'
assert d['en2zh']['sputtering']=='溅射'
assert q['alias_index']['物理溅射']=='physical-sputtering'
assert '物理溅射' in q['concepts']['physical-sputtering']['all_terms']
assert '物理溅射' not in q['concepts']['sputtering']['all_terms']
assert sum(1 for v in d['zh2en'].values() if v=='physical sputtering') >= 1
print('PROJECTION_OK')
```

## 4. Gates (each with recorded exit code)

Evidence file: `/tmp/opencode/t5184-repair/gates-after-rev3.txt`.

| # | Command | Observed | Exit |
|---|---|---|---:|
| 1 | `python3 -m pipeline.validate_registry` | `registry OK: 3076 concepts, 10249 aliases, 3203 evidence rows, 6152 definitions` | 0 |
| 2 | `python3 scripts/registry_row_audit.py --audit` | `"is_clean": true` | 0 |
| 3 | `python3 scripts/registry_batch_verify.py --self-test` | `self-test: 27/27 assertions passed` | 0 |
| 4 | `python3 -m pytest -o addopts="" -q` | `191 passed in 7.44s` (= baseline 186 + 5 new) | 0 |
| 5 | `python3 -m pytest -o addopts="" -q tests/test_registry_physical_sputtering_projection.py` | `5 passed` (GREEN) | 0 |

V8 idempotency: a second full export produced no tracked diff (`git status --porcelain` clean apart from declared untracked files).

## 5. RED → GREEN pairing

- RED (before repair, baseline registry copy): `/tmp/opencode/t5184-repair/failfirst-rev3.txt` — the actual new test run against a baseline copy reports `3 failed, 2 passed`, including the corrected projection assertion (`zh2en['物理溅射'] == "physical sputtering"` observed `sputtering`).
- GREEN (after repair): gate 5 above.

## 6. Commit scope check

- `git show --numstat --format= HEAD` → 6 declared paths only (aliases, both tracked projections, new test, preflight report, this task's change note).
- `git show --numstat --format= HEAD~1` → `artifacts/translation_dict.json` only.
- `git tag --points-at HEAD` → 0.
- `git status -sb` → `ahead`.

## 7. Scope declaration (§0.2 R5)

No `git push`, no tag created, no `dist/` rebuild, no `CHANGELOG.md` change. Concurrent files (`.github/plans/publication-program-lre-scientificdata.md`, `docs/publication/`, `evaluation/`) were not read as evidence, not modified, and not staged.

## 8. Rollback

`git revert 5013321` (A′). Rollback credential: `/tmp/opencode/t5184-repair/backup/` — single location, may be cleaned.
