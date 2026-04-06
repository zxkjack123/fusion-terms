# Registry Gap Review — Batch 3 Candidate Terms

> Generated 2026-04-04 · Scope: terminology coverage gaps in `terms/registry/`

## Executive Summary

- Findings: 0 🔴 / 18 🟡 / 3 🟢
- Project Profile: fusion-terms terminology registry (1278 active concepts, 5455 aliases)
- Overall Health: mature registry; remaining gaps are **family-level sibling omissions** rather than broad coverage failures

## Review Method

Cross-referenced five data sources to find systematic gaps:
1. `terms/registry/concepts.tsv` — category distribution & sibling analysis
2. `terms/registry/aliases.tsv` — partial coverage check
3. `artifacts/translation_dict.json` — en2zh / zh2en missing-key scan
4. `artifacts/candidates_en.filtered.tsv` — corpus-extracted candidate terms
5. `artifacts/candidates_zh.filtered.tsv` — Chinese candidate terms

All 21 proposed terms below are **confirmed absent** from both concepts.tsv and aliases.tsv.

## Context: What the Previous Two Batches Covered

- **Batch 65** (12 P0 concepts): lithium-ceramic, ceramic-pebble-bed, lithium-ceramic-pebble-bed, in-vessel, ex-vessel, reduced-activation, beryllium-pebble-bed, beryllium-neutron-multiplier, tungsten-armor, helium-coolant, safety-analysis-report, plasma-facing-component
- **Batch 66** (5 P1 concepts): wcpb, beryllium-pebble, lithium-metatitanate, lithium-metazirconate, primary-heat-transfer
- **Batch 67** (50 dehyphenated EN alias variants)

---

## Recommended New Concepts

### Theme A — 增殖材料同族补全 (Breeder Material Siblings)

Registry already covers `lithium-titanate`, `lithium-orthosilicate`, `lithium-metazirconate`, `lithium-lead`, but is missing these well-established peers:

| # | concept_id | category | preferred_zh | preferred_en | preferred_abbr | 置信度 | 依据 |
|---|-----------|----------|-------------|-------------|----------------|--------|------|
| 1 | `flibe` | material | 氟化锂铍 | FLiBe | FLiBe | HIGH | 主要熔盐增殖/冷却材料 Li₂BeF₄，候选词频繁出现 |
| 2 | `lithium-aluminate` | material | 铝酸锂 | lithium aluminate | | HIGH | LiAlO₂，与已有锂陶瓷系列平行 |
| 3 | `lithium-metasilicate` | material | 偏硅酸锂 | lithium metasilicate | | HIGH | Li₂SiO₃，lithium-orthosilicate 的同族 |
| 4 | `lithium-oxide` | material | 氧化锂 | lithium oxide | | HIGH | Li₂O，经典增殖材料，候选频次高 |
| 5 | `lithium-rich-zirconate` | material | 富锂锆酸盐 | lithium-rich zirconate | | MEDIUM | Li₈ZrO₆，已有 lithium-metazirconate 但缺此变体 |
| 6 | `breeder-material` | concept | 增殖材料 | breeder material | | HIGH | 上位概念缺失；en2zh/zh2en 均无覆盖 |

**预期 alias 增量**（含化学式）：~18 rows（preferred en/zh + LiAlO₂ / Li₂SiO₃ / Li₂O / Li₈ZrO₆ / Li₂BeF₄ 等）

### Theme B — 包层模块架构 (Blanket Module Architecture)

| # | concept_id | category | preferred_zh | preferred_en | preferred_abbr | 置信度 | 依据 |
|---|-----------|----------|-------------|-------------|----------------|--------|------|
| 7 | `multi-module-segment` | system | 多模块段 | multi-module segment | MMS | HIGH | DCLL/HCPB 系统建模中反复出现 |
| 8 | `single-module-segment` | system | 单模块段 | single-module segment | SMS | HIGH | 与 MMS 成对使用 |

**预期 alias 增量**：~8 rows

### Theme C — IFMIF/锂靶生态 (IFMIF Lithium-Target Ecosystem)

Registry 已有 `ifmif` 和 `dones`，但缺少关键子设施和工艺概念：

| # | concept_id | category | preferred_zh | preferred_en | preferred_abbr | 置信度 | 依据 |
|---|-----------|----------|-------------|-------------|----------------|--------|------|
| 9 | `lithium-target` | system | 锂靶 | lithium target | | HIGH | IFMIF 核心组件 |
| 10 | `free-surface-lithium-target` | system | 自由表面锂靶 | free-surface lithium target | | MEDIUM | IFMIF/ELTL 靶设计专用表述 |
| 11 | `eltl` | device | EVEDA锂试验回路 | EVEDA Lithium Test Loop | ELTL | HIGH | IFMIF 验证装置，候选频繁出现 |
| 12 | `lipac` | device | 线性IFMIF原型加速器 | Linear IFMIF Prototype Accelerator | LIPAc | HIGH | IFMIF 主要子设施 |
| 13 | `eveda` | concept | 工程验证与工程设计活动 | Engineering Validation and Engineering Design Activities | EVEDA | MEDIUM | IFMIF 项目阶段名称 |
| 14 | `lithium-loop` | system | 锂回路 | lithium loop | | MEDIUM | 液态锂输运/净化系统通称 |
| 15 | `liquid-lithium-purification` | concept | 液态锂纯化 | liquid lithium purification | | MEDIUM | ELTL/IFMIF 关键工艺 |

**预期 alias 增量**：~20 rows

### Theme D — 冷却与工质补全 (Coolant & Working Fluid)

| # | concept_id | category | preferred_zh | preferred_en | preferred_abbr | 置信度 | 依据 |
|---|-----------|----------|-------------|-------------|----------------|--------|------|
| 16 | `water-coolant` | concept | 水冷却剂 | water coolant | | MEDIUM | 有 helium-coolant 但缺 water-coolant |
| 17 | `coolant-purification` | concept | 冷却剂纯化 | coolant purification | | MEDIUM | 包层冷却系统配套工艺 |

**预期 alias 增量**：~6 rows

### Theme E — 氚工艺补充 (Tritium Process Supplement)

| # | concept_id | category | preferred_zh | preferred_en | preferred_abbr | 置信度 | 依据 |
|---|-----------|----------|-------------|-------------|----------------|--------|------|
| 18 | `tritium-carrier` | concept | 氚载体 | tritium carrier | | MEDIUM | DCLL 描述 PbLi 三重角色之一 |

**预期 alias 增量**：~3 rows

### 🟢 Reserve (Lower Priority)

以下仅在需要更大批次时考虑：

| # | concept_id | category | preferred_zh | preferred_en | 置信度 | 说明 |
|---|-----------|----------|-------------|-------------|--------|------|
| 19 | `target-chamber` | system | 靶室 | target chamber | LOW | IFMIF 具体组件 |
| 20 | `test-cell` | system | 测试间 | test cell | LOW | IFMIF 辐照测试区域 |
| 21 | `lifus` | device | LIFUS | LIFUS | LOW | 锂回路验证小型装置 |

---

## Impact Estimate

| Metric | Current | After Batch 3 (18 🟡) | After Batch 3 (all 21) |
|--------|---------|----------------------|----------------------|
| concepts.tsv rows | 1278 | 1296 (+18) | 1299 (+21) |
| aliases.tsv rows (est.) | 5455 | ~5510 (+55) | ~5520 (+65) |
| en2zh pairs (est.) | 2333 | ~2390 | ~2400 |
| domain_terms.txt (est.) | 2901 | ~2950 | ~2960 |

## Remediation Roadmap

### Priority 1 — Theme A (增殖材料同族) ← 建议首先执行

- 收益最高：6 个概念补全锂陶瓷增殖材料系列，直接修复翻译字典中 LiAlO₂/Li₂SiO₃/Li₂O 等化学式无法查译的问题
- 实施成本最低：纯数据追加，无结构争议

### Priority 2 — Theme B + C (包层架构 + IFMIF 生态)

- MMS/SMS 为工程设计常用术语对
- ELTL/LIPAc/EVEDA 为 IFMIF 关键子设施，候选语料支持强

### Priority 3 — Theme D + E (冷却 + 氚工艺)

- 覆盖率改善型，非直接翻译错误修复

### 🟢 Optional — Reserve 3 terms

- 仅在追求全面覆盖时添加

## Next Steps

- 切换到实施模式，按 Theme A → B → C → D → E 顺序逐批添加到 registry
- 每批完成后运行 `validate_registry` → `export_registry --translation-dict` → `build_terms` → `pytest`
- 或者先生成 `.github/plans/expand-registry-batch3.md` 详细执行计划后再动手
