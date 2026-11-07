# T-5326 — O-6 祖父名单清零（5 条「一概念两个 zh preferred」）change note

Audience: repository developers / agents. External-facing de-ai-fier (§0) not applicable.

## 1. What changed

| 文件 | 改动 |
|---|---|
| `terms/registry/aliases.tsv` | ① 5 条多余的同义 `zh/preferred` 行降为 `alias`（comment 标「同义（非首选）」）：`锯齿不稳定性`(sawtooth)、`三重积`(fusion-triple-product)、`脱靶`(plasma-detachment)、`鞘层`(debye-sheath)、`直接一步法`(d1s) ② 为 `d1s` **补一条**规范首选行 `D1S直接一步法 / zh / preferred`（该概念此前无与 `preferred_zh` 一致的 preferred 行） |
| `pipeline/validate_registry.py` | 删除 `_GRANDFATHERED_ZH_PREFERRED_MISMATCHES` 常量及其在 O-6 规则中的豁免分支 ⇒ **O-6 自此无任何豁免** |
| `tests/test_registry_validator.py` | 删除 `test_validate_registry_allows_grandfathered_mismatch`（该豁免机制已不存在） |
| `artifacts/terminology_substitutions.tsv` | 2 条规则的替换目标由同义词改为规范名：`聚变三参数 → 聚变三乘积`、`聚变三重积 → 聚变三乘积` |
| `artifacts/translation_dict.json` | 新增 `zh2en['D1S直接一步法']='D1S'`；`pairs_zh2en` 3418 → 3419 |

## 2. Why

O-6 规则要求「`aliases` 的 `zh/preferred` 行 == 该概念的 `concepts.preferred_zh`」。当时 5 个概念存在**两条 zh preferred**（一条等于 `concepts.preferred_zh`、另一条是同义长短形式），属「一个概念两个首选名」的重复声明。方向判定依据：

- 同义文本**均不在** `terms/allowlist_zh` ⇒ 若改 `concepts.preferred_zh` 会破坏「`preferred_zh ∈ allowlist_zh`」契约；
- 4 个概念**已存在**与 `preferred_zh` 一致的 preferred 行 ⇒ 只需把多余那条降级，**不丢同义词**；
- `d1s` 唯一 preferred 行与 `preferred_zh` 不一致 ⇒ 降级同义行 + 补规范行。

## 3. 验证

- 全库重算：`zh/preferred` 与 `concepts.preferred_zh` 不一致 **0** 条（此前 5 条）；`alias→多概念` 冲突 **0** 条。
- 5 个概念各恰有 1 条 zh preferred 且等于 `preferred_zh`。
- 门禁：`validate_registry` exit 0（3075 concepts / **10251** aliases / 3202 evidence / 6150 definitions）；`row_audit` `is_clean: true`；`self-test` 27/27；`pytest` **211 passed**（212 − 删除的 1 个豁免测试）；`ruff format`/`check` 全绿。
- 派生意涵：`terminology_substitutions` 的 2 条规则改为指向规范名（同义词不再被当作「正确写法」推荐）。
- 未改动：`concepts.tsv`、`terms/allowlist_*`、其他别名、`pipeline/` 其他逻辑。
- 可逆：单 commit `git revert`（含派生重建）。
