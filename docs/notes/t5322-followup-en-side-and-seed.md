# T-5322 后续 — en 侧落点对齐 + 一次性 seed 脚本同步 change note

Audience: repository developers / agents. External-facing de-ai-fier (§0) not applicable.

承接 `docs/notes/t5322-sputtering-yield-retarget.md`（不改动该 note，按「一经提交即冻结」）。

## 1. What changed

| 文件 | 改动 |
|---|---|
| `terms/registry/aliases.tsv:4567` | `physical sputtering yield`：`physical-sputtering` → **`sputtering-yield`**（en / alias，comment 仍 `yield form`） |
| `artifacts/translation_dict.json` | `en2zh['physical sputtering yield']`：`物理溅射` → **`溅射产额`** |
| `scripts/batches/_batch_enrich_aliases.py` | ① 段头 `# physical-sputtering` → `# sputtering-yield (retargeted from physical-sputtering, #5322)`；② seed `("物理溅射产额","physical-sputtering",…)` → `sputtering-yield`；③ seed `("physical sputtering yield","physical-sputtering",…)` → `sputtering-yield` |

## 2. Why

独立验收（`10e921a` 的 acceptance-verifier，PASS）提出两条非阻塞 caution：

1. **en 侧不对称**：中文侧两个「产额/率」形态已改指 `sputtering-yield`，但 en 侧 `physical sputtering yield` 仍挂 `physical-sputtering`，导致 `en2zh['physical sputtering yield'] = '物理溅射'`（应为「溅射产额」）。
2. **一次性脚本会回滚本次修复**：`scripts/batches/_batch_enrich_aliases.py` 的去重键是 `(alias.lower(), concept_id)`，其 seed 仍为旧落点 ⇒ **一旦重跑该脚本会重新追加旧映射**（因为 `concept_id` 变了，键不同）。

## 3. 验证

- 投影：`en2zh['physical sputtering yield']='溅射产额'`；`alias_index[...]='sputtering-yield'`；该面 ∈ `all_terms['sputtering-yield']` 且 **不再** ∈ `all_terms['physical-sputtering']`（后者 all_terms 仅余 2 条：`物理溅射` / `physical sputtering`）。
- 本地 gitignored 缓存同步：`artifacts/tag_rules.jsonl` 中该面现为 `metric / sputtering-yield`。
- 门禁：`validate_registry` exit 0（3075/10250/3202/6150）；`row_audit` `is_clean: true`；`self-test` 27/27；M3 护栏 5 passed；全量 **212 passed**；`ruff format`/`check` 全绿。
- 未改动：`physical-sputtering` / `sputtering-yield` 概念行与定义、其他别名、`terms/allowlist_*`、`pipeline/`。
- 可逆：单 commit `git revert`。
