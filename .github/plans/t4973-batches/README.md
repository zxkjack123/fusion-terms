# T4973 批次工作集与 id 清单（T0.3 交付）

本目录是 PM 任务 **T4973**（计划：`../terminology-coverage-and-definition-quality.md`）的
**工作集与逐批 id 清单**，使每个批次任务无状态、可独立执行。

> **唯一权威**：批次数与每批大小以本文件为准（计划 §R2-2 已声明）。计划 Phase 1–3 表格中的
> 批次数为规划期估值，与本目录不一致时以本文件为准。

## 生成命令（可复现）

```bash
.venv/bin/python scripts/registry_coverage_report.py \
    --emit-lists .github/plans/t4973-batches --batch-size 20 \
    --json /tmp/cov.json
```

生成时基线：`git rev-parse HEAD` = `3f4e022`（`terms/registry/*` 尚未修复的**修复前**状态）。

## 口径（与 `scripts/registry_coverage_report.py` 一致）

- **total**：`terms/registry/concepts.tsv` 数据行数（跳过 `#` 注释与空行）= **3076**
- **covered**：`concept_id` / `preferred_en` / `preferred_zh` / 该 concept 任一 alias 出现在
  `artifacts/domain_terms.txt`，**或** `preferred_zh` ∈ `allowlist_zh.txt`，**或** `preferred_en`
  （含连字符化形式）∈ `allowlist_en.txt` = **1449**
- **uncovered** = **1627**（覆盖率 **47.11%**；`covered + uncovered == total` 由脚本自校验）
- **proper_excluded** = 未覆盖行中 `category ∈ {company, organization, facility}` = **35**
  （用户裁决：专名不入 IME 词表）
- **W2**（可机械补齐）= 未覆盖 + `preferred_zh` 非空 + 非专名 = **584**
  - `W2_multiword` = **527**（`preferred_en` 含空白 → 须写连字符 token 形式入 `allowlist_en.txt`）
  - `W2_single` = **57**
- **W3a**（须起草中文首选名）= **854**
- **W1**（definitions 工作集，来自 `--ids-file` 口径）：
  - `W1_a.ids` = **67**（en 套话 + 仓内有 zh 出处 `GB/T-4960.9`，可仓内推导）
  - `W1_b.ids` = **679**（须外部权威出处）
  - `W1_c.ids` = **10**（当前完全没有 definitions 的 concept）

## 集合规模与批数（实测）

| 集合 | ids | 批数 | 每批大小 |
|---|---|---|---|
| `w1_a.ids` | 67 | 4 | 20×3 + 7 |
| `w1_b.ids` | 679 | 34 | 20×33 + 19 |
| `w1_c.ids` | 10 | 1 | 10 |
| `w2.ids` | 584 | 30 | 20×29 + 4 |
| `w3.ids` | 854 | 43 | 20×42 + 14 |
| **合计** | **2194** | **112** | — |

目录内文件总数 = 112 个批文件 + 5 个集合文件 = **117**。

**批次大小策略**：`--batch-size` 为单一全局参数，故统一取 **20**。取 20 而非计划估值
（W2 58~59/批、W3 最大 36/批）的理由：`--batch-size` 是**唯一**控制手段，而 W1/W3 是内容密集型
（每条定义/中文名都需查证），20 条/批可稳定落在计划规定的 ≤30 min 内；W2 虽为机械操作，
批变小只增加批次数量、不损害正确性。

## 自检（可复跑，与 T0.3 验收一致）

```bash
cd /home/gw/opt/fusion-terms
wc -l .github/plans/t4973-batches/{w1_a,w1_b,w1_c,w2,w3}.ids      # 67 679 10 584 854
sort .github/plans/t4973-batches/w2.ids .github/plans/t4973-batches/w3.ids | uniq -d | wc -l   # 0
cat .github/plans/t4973-batches/w1_b_b*.ids | wc -l                # 679
# 每批 id 数分布（证明 20/批切分）
wc -l .github/plans/t4973-batches/w2_b*.ids | head -n -1 | awk '{print $1}' | sort -n | uniq -c
```

**能失败证明（变异法）**：在副本上删掉 `w1_b_b34.ids` 一行后
`cat w1_b_b*.ids | wc -l` 由 679 变 **678**（已实测），说明计数断言绑定真实文件而非常量。

## 执行批次时必须注意（实测发现，勿忽略）

1. **10 个 W2 id 的中文首选名在 `terms/denylist.txt` 内**（`halo-current`、`line-radiation`、
   `system`、`calculation`、`material`、`simulation`、`mode`、`device`、`magnetic-moment`、
   `mode-number`）：把这些中文名写入 `allowlist_zh.txt` 是**无效操作**——
   `pipeline/build_terms.py` 会先按 denylist 过滤（`if t in deny`），永远进不了 IME 词表。
   同理 `system` / `mode` 已在 `denylist.txt`，写入 `allowlist_en.txt` 亦无效。
   → 这批行的处置须在 W2 批次内单独标注，不要当成"漏写"。
2. **12 条 allowlist 词不在构建产物 `domain_terms.txt` 里**（zh：`晕电流`、`球马克`、`磁面`、
   `线辐射`；en：`DT,Hmode,Lmode,MMS,SMS,diffusion,pbli,q_95`），其中 4 条被 denylist 过滤。
   这正是 `coverage_pct`（47.11%）与 `allowlist_only_coverage_pct`（45.71%）两个口径差异的来源。
3. **169 个 concept 的 `preferred_zh == preferred_en` 且均不含 CJK**（`rfx-mod`、`c-2w`、`rexie`、
   `kmax`、`exl-50` …，多为装置代号）。当前 `scripts/registry_batch_verify.py --mode names`
   的 CJK 判据是硬要求 → 这些 id **无法通过** names 模式；处理口径待裁决（见计划 D2 区追加项）。
4. **`definitions.tsv` 的 source 白名单是闭合集合**，不含任何 `internal:*`；现有 **4583 行**
   以 `internal:dict-improvements` 为 source。凡进入 W1 批次的行，其 source 必须换成真实出处
   （可 200 的 URL 或 `GB/T-4960.9` / `ITER-glossary` / `IAEA-safety-glossary` / `corpus`）。
5. **畸形行（99 左移 + 80 六列）不得作为 W3 起草依据**：其字段槽位在修复前是错位的。
   W0（`T0.4`/`T0.5`/`T0.6a`）修复后须**重跑**本目录的生成命令（覆盖率与 W2/W3 集合都会变，
   计划 §动态基线约定已要求）。

## 依赖关系

- 本目录由 `T0.3` 产出，依赖 `T0.0`（覆盖率脚本）、`T0.1`（结构审计）、`T0.2`（批验收脚本）—— 三者均已提交。
- 后续每个批次任务：`--ids-file <本目录的某个批文件>` → 用 `scripts/registry_batch_verify.py`
  （对应模式）验收 → commit（message 带 `#T-4973`）。
