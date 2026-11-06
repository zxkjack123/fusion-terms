# T-5315 — O-6 validator 护栏（首选名一致性 + 缩写反向断言）change note

Audience: repository developers / agents. External-facing de-ai-fier (§0) not applicable.

## 1. What changed

- `pipeline/validate_registry.py`（+64 行）
  1. **O-6 规则**：任一 `aliases.tsv` 的 `zh` / `kind=preferred` 行，其文本必须等于该 concept 的 `concepts.preferred_zh`（当后者非空且该 pair 不在祖父名单内）。违反即 `_fail`，消息含 `contradicts concepts.preferred_zh`。
  2. **缩写反向断言**：`definitions.tsv` 中 `lang=zh` 且 `source` 以 `translated:` 开头的行，其大写缩写 token（`\b[A-Z][A-Z0-9]{1,12}\b`）必须是 `en` 行缩写 ∪ `concepts.preferred_en` 缩写的子集；否则 `_fail`，消息含 `acronym(s) absent from en/preferred_en`。
- `tests/test_registry_validator.py`（+140 行 / +5 测试）：两条规则各自的「必须失败」用例 + 三条「不得误伤」用例（祖父 pair、概念侧空名、合法缩写来源）。
- 常量 `_GRANDFATHERED_ZH_PREFERRED_MISMATCHES`：5 个已知遗留 pair。

## 2. Why

`.github/plans/completed/5184-m3-m1-repair.md` §11.2 的 **O-6**（即 §9.2 的 O-2）指出：M3 那类「同一中文首选名被双声明」的冲突**没有 CI 护栏**，可能在后续数据改动中重现。另：`translated zh` 缩写门禁此前只存在于一次性脚本（5072 附录 B 的 `/tmp/opencode/t5072/apply_translations.py`，已随 `/tmp` 清理消失），且为**单向**（只查缺失、不查新增）⇒ 无法阻止编造缩写。本次把两条都升格为仓库级、可失败的门禁。

## 3. 实测基线（2026-11-07）

| 指标 | 值 |
|---|---|
| `zh`/`preferred` 别名行 | 2032 |
| 与 `concepts.preferred_zh` 不一致 | **9**（4 条概念侧为空 ⇒ 规则跳过；5 条取值不同 ⇒ 祖父名单） |
| `translated:*` 的 zh 定义行 | 747 |
| 缩写反向断言违规 | **0** |

**5 个祖父 pair**：`sawtooth`/锯齿不稳定性、`fusion-triple-product`/三重积、`plasma-detachment`/脱靶、`debye-sheath`/鞘层、`d1s`/直接一步法。
**清单只减不增**：修好其中任一条后，必须从 `_GRANDFATHERED_ZH_PREFERRED_MISMATCHES` 同步删除（数据修复属另一任务，本 commit 零数据改动）。

## 4. 能失败证明（RED→GREEN）

- RED（规则未实现时）：`pytest tests/test_registry_validator.py` → **2 failed, 18 passed**（失败项正是 `..._rejects_zh_preferred_alias_mismatch` 与 `..._rejects_invented_acronym_in_translated_zh`）。
- GREEN（实现后）：**20 passed**；全量 **212 passed**（原 207 + 5）。
- 真实仓库不误伤：`validate_registry` exit 0 → `3075 concepts / 10250 aliases / 3202 evidence / 6150 definitions`。

## 5. 边界

- **零数据改动**：未改 `terms/registry/*`、`terms/allowlist_*`、`artifacts/*`。
- 未改既有失败语义：`_fail` 与退出码约定沿用原实现。
- 未把 9 条差异「修掉」（那会触数据改动与语义裁决）；本任务只加护栏。
