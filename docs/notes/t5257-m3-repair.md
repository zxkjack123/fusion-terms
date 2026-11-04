# T-5257 — M3 A′ repair change note (`物理溅射` ownership)

Audience: repository developers / agents. External-facing de-ai-fier (§0) not applicable.

## 1. What changed

- `terms/registry/aliases.tsv`
  - removed the row `物理溅射 <TAB> sputtering <TAB> zh <TAB> alias <TAB> physical sputtering zh`
  - inserted `物理溅射 <TAB> physical-sputtering <TAB> zh <TAB> preferred <TAB> zh preferred (M3 A': moved from sputtering alias)`
    directly after the anchor row `physical sputtering <TAB> physical-sputtering <TAB> en <TAB> preferred`
  - net line delta: 1 removed / 1 added (`git diff --numstat` = `1 1`)
- Release projections rebuilt with `pipeline.export_registry` (see §3).
- Derived side effect (expected): in `artifacts/terminology_substitutions.tsv` the replacement target of the three forbidden entries (`物理喷溅`, `物理飞溅`, `物理溅射率`) moves from `physical sputtering` to `物理溅射`, because a same-language (zh) preferred row now exists for the concept. Delta = 3 lines.

## 2. Why

A single zh string `物理溅射` was simultaneously owned by two concepts: it was an `alias` of `sputtering` and the `preferred_zh` of `physical-sputtering`. The A′ option (user adjudication 2026-11-04, plan §0 / §0.3 R6–R10) removes the duplicate ownership and restores the zh→en label direction as well as the zh→concept-id direction.

## 3. Rebuild command

```bash
python3 -m pipeline.export_registry --config config.toml --query-expansions --tag-rules --substitutions --vale-substitute --translation-dict
```

Tracked projections: `artifacts/translation_dict.json`, `artifacts/terminology_substitutions.tsv`.
Ignored projections regenerated locally only: `artifacts/query_expansions.json`, `artifacts/tag_rules.jsonl`, `artifacts/vale/*`.

## 4. Scope of this commit

Commit ② of `#T-5257` contains exactly:

- `terms/registry/aliases.tsv`
- `artifacts/translation_dict.json`
- `artifacts/terminology_substitutions.tsv`
- `tests/test_registry_physical_sputtering_projection.py`
- `docs/reviews/t5184/repair-g0-preflight.md`
- `docs/notes/t5257-m3-repair.md` (this file)

No `git push`, no tag, no `dist/` rebuild, no `CHANGELOG.md` change. Concurrent files (`.github/plans/publication-program-lre-scientificdata.md`, `docs/publication/`, `evaluation/`) are outside this task and are not staged.

## 5. Evidence

- RED (before repair, baseline registry copy): `/tmp/opencode/t5184-repair/failfirst-rev3.txt`
- GREEN + gates after repair: `/tmp/opencode/t5184-repair/gates-after-rev3.txt`
- Execution report: `docs/reviews/t5184/repair-m3-execution.md` (M3-5)
- Rollback credential: `/tmp/opencode/t5184-repair/backup/` (single location; may be cleaned).
