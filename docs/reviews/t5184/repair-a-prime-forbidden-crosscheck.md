# A′ 后 3 条 forbidden 行的 K-1/K-2 补核（计划 §9.1.1 步骤 4 产物）

Audience: repository developers / agents（内部技术产物 ⇒ `[de-ai-fier: N/A — 受众为开发者/agent]`）。

- 日期：`2026-11-06`（`date` 实测）｜基线：`d081e28`
- 依据：`.github/plans/5184-m3-m1-repair.md` §9.1.1（rev 2：**补核已授权、改写未授权**）
- 性质：**只读补核**。本次**未改写任何一条 forbidden 行**（§2.2 第 5 条）。

## 1. 三行现状（`terms/registry/aliases.tsv`）

| # | 行号（现行） | alias | concept | lang | kind | comment |
|---|---|---|---|---|---|---|
| 1 | 3812 | 物理喷溅 | `physical-sputtering` | zh | forbidden | 误译sputtering：正确为 物理溅射 |
| 2 | 3813 | 物理飞溅 | `physical-sputtering` | zh | forbidden | 误译sputtering：正确为 物理溅射 |
| 3 | 7051 | 物理溅射率 | `physical-sputtering` | zh | forbidden | 率暗示时间量纲：正确为 物理溅射(产额) |

> 行号说明：计划原文记 `3812/3813/7050`；`#T-5290`/M1 D6 各插入过行，第 3 行由 7050 位移至 **7051**。**按内容键比对**（非行号）确认三行与基线 `ea5411d` **逐字节相同**（`same_as_base=True`）。

## 2. 逐行判定（§9.1.1 步骤 2）

| # | 「误译 X」指什么 | 「正确为 Y」是否为该 concept 的 zh preferred | 结论 |
|---|---|---|---|
| 1 | `sputtering`（作为被误译的英文词根，非 concept id） | `物理溅射` 是 `physical-sputtering` 的 **zh preferred**（A′ 落地：`5013321`） | **仍成立** |
| 2 | 同上 | 同上 | **仍成立** |
| 3 | `率`（量纲提示：rate ≠ 存量/量） | `物理溅射` 是 zh preferred；注释已自带限定 `(产额)` | **仍成立**（注释本身无需改写） |

## 3. K-2 派生侧效应（§9.1.1 步骤 3）

`artifacts/terminology_substitutions.tsv` 中三条规则的 preferred 列：

| alias | A′ 前 | A′ 后 |
|---|---|---|
| 物理喷溅 | `physical sputtering`（en 回退） | **`物理溅射`**（zh preferred） |
| 物理飞溅 | `physical sputtering` | **`物理溅射`** |
| 物理溅射率 | `physical sputtering` | **`物理溅射`** |

**方向判定：符合预期。** zh 写作规则的正确形式理应是**中文** preferred；A′ 之前因 `物理溅射` 只是 `sputtering` 的 alias（同 concept 无 zh preferred）而回退到英文，属异常态。A′ 后回退消失。

## 4. 结论与建议

- **是否需要改写这 3 条 forbidden 注释：不需要。** 三行在 A′ 后语义均**仍成立**，且与基线逐字节一致。
- **一项遗留建议（不属本文授权范围，需另立任务）**：`物理溅射率` 的 alias 目标 concept 是 `physical-sputtering`（而非 `sputtering-yield`），故其派生替换目标为 `物理溅射` 而不含「产额」；而其注释已写明「正确为 物理溅射(产额)」。若要消除该精度差，应另立任务评估把该 alias 的 concept 改指 `sputtering-yield`（**本次未改动**）。
