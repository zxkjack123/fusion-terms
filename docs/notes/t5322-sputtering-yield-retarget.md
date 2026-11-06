# T-5322 — `物理溅射产额` / `物理溅射率` 落点改指 `sputtering-yield` change note

Audience: repository developers / agents. External-facing de-ai-fier (§0) not applicable.

## 1. What changed

| 文件 | 改动 |
|---|---|
| `terms/registry/aliases.tsv` | ① `物理溅射产额` 的 concept：`physical-sputtering` → **`sputtering-yield`**（kind 仍 `alias`，comment 仍 `yield form`）② `物理溅射率` 的 concept：`physical-sputtering` → **`sputtering-yield`**，comment 由「正确为 物理溅射(产额)」→「正确为 **溅射产额**」（与同族 `溅射率` 的 `:7050` 对齐） |
| `artifacts/terminology_substitutions.tsv` | 规则目标 `物理溅射率 → 物理溅射` 改为 `→ 溅射产额`（1 行） |
| `artifacts/translation_dict.json` | `zh2en['物理溅射产额']`：`physical sputtering` → **`sputtering yield`**（+ `generated_at` 刷新） |
| `tests/test_registry_physical_sputtering_projection.py` | 1 条断言由 `物理溅射率\t物理溅射\t` 改为 `物理溅射率\t溅射产额\t`，并加 3 行注释说明：该测试原先固化的是 M3 时点的派生副作用，本次按语义修正 |

## 2. Why

「物理溅射」家族此前存在**族内不对称**：纯「溅射」家族的率/产额形态（`溅射产额`、`溅射率`、`溅射系数`、`溅射产率`、`溅射收率`）均已正确归到 metric 概念 `sputtering-yield`，而 `物理溅射产额` / `物理溅射率` 仍挂在现象概念 `physical-sputtering` 上。两处可核验的下游损害：

1. **写作门禁给错建议**：`terminology_substitutions` 指示把「物理溅射率」写成「物理溅射」，丢掉「率/产额」的量纲语义；
2. **中英词典误译入口**：`zh2en['物理溅射产额'] = "physical sputtering"`，英文写作时被译成现象而非 `sputtering yield`。

## 3. 证据

| 依据 | 内容 |
|---|---|
| 概念定义 | `sputtering-yield`：`Y, atoms emitted per incident projectile from solid surface`（无量纲量）；`physical-sputtering`：`Ejection of surface atoms by energetic ion bombardment`（现象） |
| 族内一致性 | `溅射率`/`溅射系数`/`溅射产率`/`溅射收率` 均 → `sputtering-yield`，且 comment 明写「率暗示时间量纲：正确为 溅射产额」 |
| 外部权威快照 | GB/T / ITER / IAEA 快照对 `sputtering yield` **0 命中** ⇒ 依据为仓内定义 + 族内一致性（已在任务 notes 声明强度） |
| allowlist | `物理溅射率` / `物理溅射产额` 均 **0 命中** ⇒ 无 bridge-check 风险；`sputtering-yield` 已在 `allowlist_en` |
| 未改动 | `physical-sputtering` / `sputtering-yield` 的概念行、定义、其他别名、`terms/allowlist_*`、`pipeline/` |

## 4. 验证

- 投影断言：`zh2en['物理溅射产额']='sputtering yield'`；`alias_index['物理溅射产额']` 与 `['物理溅射率']` 均为 `sputtering-yield`；`物理溅射产额 ∈ all_terms['sputtering-yield']` 且 **不再** ∈ `all_terms['physical-sputtering']`；`物理溅射率\t溅射产额\t` 存在于 substitutions。
- 门禁：`validate_registry` exit 0（3075/10250/3202/6150）；`row_audit` `is_clean: true`；`self-test` 27/27；M3 护栏 5 passed；全量 **212 passed**；`ruff format`/`check` 全绿。
- 可逆：单 commit `git revert`。
