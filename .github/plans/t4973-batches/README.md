# T4973 批次工作集与 id 清单（T0.3 交付，W0 收尾后重生成）

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

- **本版生成时基线**：`git rev-parse HEAD` = `c3e7f5c`（`terms/registry/*` 为 **W0 修复后**状态）
- **首版（T0.3）基线**：HEAD `3f4e022`（修复前）—— 该版数字（W2 584 / 30 批）**已作废**，
  因畸形行修复后变为可计数，W2 由 584 → **738**
- 生成器只增不删：重生成后若批数下降，须人工清理残留的 `*_b*.ids`（本次重生成批数上升，无残留）

## 口径（与 `scripts/registry_coverage_report.py` 一致）

- **total**：`terms/registry/concepts.tsv` 数据行数（跳过 `#` 注释与空行）= **3076**
- **covered**：`concept_id` / `preferred_en` / `preferred_zh` / 该 concept 任一 alias 出现在
  `artifacts/domain_terms.txt`，**或** `preferred_zh` ∈ `allowlist_zh.txt`，**或** `preferred_en`
  （含连字符化形式）∈ `allowlist_en.txt` = **1449**
- **uncovered** = **1627**（覆盖率 **47.11%**；`covered + uncovered == total` 由脚本自校验）
- **proper_excluded** = 未覆盖行中 `category ∈ {company, organization, facility}` = **35**
  （用户裁决：专名不入 IME 词表）
- **W2**（可机械补齐）= 未覆盖 + `preferred_zh` 非空 + 非专名 = **738**
  - `W2_multiword` = **668**（`preferred_en` 含空白 → 须写连字符 token 形式入 `allowlist_en.txt`）
  - `W2_single` = **70**
- **W3a**（须起草中文首选名）= **854**
- **W1**（definitions 工作集，来自 `--ids-file` 口径）：
  - `w1_a.ids` = **67**（en 套话 + 仓内有 zh 出处 `GB/T-4960.9`，可仓内推导）
  - `w1_b.ids` = **679**（en 套话 + 无仓内出处 → 须给出来源；**D2-8=A：允许仓内依据 `corpus`**）
  - `w1_c.ids` = **10**（当前完全没有 definitions 的 concept → 新增 en + zh）

## 集合规模与批数（实测，2026-10-26 W0 后重生成）

| 集合 | ids | 批数 | 每批大小 |
|---|---|---|---|
| `w1_a.ids` | 67 | 4 | 20×3 + 7 |
| `w1_b.ids` | 679 | 34 | 20×33 + 19 |
| `w1_c.ids` | 10 | 1 | 10 |
| `w2.ids` | 738 | 37 | 20×36 + 18 |
| `w3.ids` | 854 | 43 | 20×42 + 14 |
| **合计** | **2348** | **119** | — |

- 目录内 `.ids` 文件 = **128**（119 批 + 9 集合：`w1_a/w1_b/w1_c/w2/w3` + W0 用的 `t0_6a/t0_6b/t0_7a/t0_7b`）
- 另含 6 个非 `.ids` 文件：`README.md`、`red-green.md`、`category-map-shift99.tsv`、
  `category-map-sixcol80.tsv`、`names-basis-t0_6.tsv`、`defs-basis-t0_7.tsv`

**批次大小策略**：`--batch-size` 为单一全局参数，故统一取 **20**。取 20 而非计划估值
（W2 58~59/批、W3 最大 36/批）的理由：`--batch-size` 是**唯一**控制手段，而 W1/W3 是内容密集型
（每条定义/中文名都需查证），20 条/批可稳定落在计划规定的 ≤30 min 内；W2 虽为机械操作，
批变小只增加批次数量、不损害正确性。

> ⚠️ **D2-7=A 对 W1 批量的影响**：W1 每批须**同时**改写该批 id 的 en 行与 zh 行（含 `指“X”` 模板行），
> 故每批实际改动行数 ≈ id 数 × 2（W1 合计 ≈ 1500 行）。批**数**不变（4/34/1），但**每批墙钟**高于
> 计划原始估值（原估值按「W1 只负责 en 行」计算）。执行时以实测为准，超 30 min 必须按
> §Step 0a-2 拆分粒度门处理。

## 自检（可复跑）

```bash
cd /home/gw/opt/fusion-terms
wc -l .github/plans/t4973-batches/{w1_a,w1_b,w1_c,w2,w3}.ids      # 67 679 10 738 854
sort .github/plans/t4973-batches/w2.ids .github/plans/t4973-batches/w3.ids | uniq -d | wc -l   # 0
cat .github/plans/t4973-batches/w1_b_b*.ids | wc -l                # 679
# 批数（每集合）
for s in w1_a w1_b w1_c w2 w3; do echo "$s $(find .github/plans/t4973-batches -maxdepth 1 -name "${s}_b*.ids" | wc -l)"; done
# 期望：w1_a 4 / w1_b 34 / w1_c 1 / w2 37 / w3 43
# 每批 id 数分布（证明 20/批切分）
wc -l .github/plans/t4973-batches/w2_b*.ids | head -n -1 | awk '{print $1}' | sort -n | uniq -c
# 确定性：重复生成必须零差异
.venv/bin/python scripts/registry_coverage_report.py --emit-lists .github/plans/t4973-batches --batch-size 20 >/dev/null
git status --porcelain .github/plans/t4973-batches/   # 应无输出（幂等）
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
   这正是 `coverage_pct`（47.11%）与 `allowlist_only_coverage_pct`（46.26%）两个口径差异的来源。
3. **169 个 concept 的 `preferred_zh == preferred_en` 且均不含 CJK**（`rfx-mod`、`c-2w`、`rexie`、
   `kmax`、`exl-50` …）。**裁决 D2-6=A**：`--mode names` 的 CJK 硬判据**保持字面不变**，
   由 **W3 为这 169 个 id 补中文首选名**（不豁免、不改判据）。
   **实测归属（2026-10-26 复核）**：这批 id **不在** `w3.ids`（交集 **0**），其中 **9** 个在 `w2.ids`、
   **4** 个在 W1 集、**156** 个不在任何现存工作集。
   按 category：`code` **97** / `device` 30 / `company` 23 / `organization` 6 / `facility` 1 /
   `material` 5 / `concept` 5 / `method` 2。其中 **30 个为专名**（company/organization/facility）。
   ⇒ 关闭 D2-6=A **需要新增工作集 `w3b.ids`（169 个 id，按 20/批 = 9 个批文件）**，
   由计划 **T3.0** 生成并验收（现存 5 个集合均无法承接）。生成前不得开始 W3 的 D2-6 部分。
   **注意**：30 个专名即使被补上中文首选名，**仍不得进入 IME 词表**（用户裁决②：专名不入 IME 词表）
   —— 这是两条互不冲突的口径（前者管 `--mode names` 的 CJK 判据，后者管 `allowlist_*.txt` 的构建）。
4. **`definitions.tsv` 的来源白名单在批验收器内是闭合集合**（接受 `corpus` / `GB/T-` / `ITER-` /
   `IAEA-` 前缀，**不含任何 `internal:*`**）；现有 **4535 行**以 `internal:dict-improvements` 为 source。
   **裁决 D2-8=A**：进入 W1 批次的行可用 **`corpus`**（该 concept 的 registry `notes` / 既有 zh 释义
   为依据）；仅当释义**显式引用外部权威**时才要求可 200 的 URL 或 `GB/T` / `ITER` / `IAEA`。
5. **畸形行（99 左移 + 80 六列）不得作为 W3 起草依据**：其字段槽位在修复前是错位的。
   W0（`T0.4`/`T0.5`/`T0.6a/b`）修复后**已重跑**本目录的生成命令（见本文档「本版生成时基线」），
   W2 584 → 738 已反映修复结果。
6. **W0 修复后 `concepts.tsv` 全为 8 列**（3076/3076），`evidence.tsv` 全为 5 列（3168/3168），
   `zh_en_corruption = 0` ⇒ 不会再出现"畸形行当依据"的问题（该风险已关闭，保留本条作历史记录）。

## 依赖关系

- 本目录由 `T0.3` 产出，依赖 `T0.0`（覆盖率脚本）、`T0.1`（结构审计）、`T0.2`（批验收脚本）—— 三者均已提交。
- 后续每个批次任务：`--ids-file <本目录的某个批文件>` → 用 `scripts/registry_batch_verify.py`
  （对应模式）验收 → commit（message 带 `#T-4973`）。
- 门禁 RED→GREEN 证据（T0.11 交付）：见同目录 `red-green.md`。

## W3b（D2-6=A 工作集，T3.0 产出，2026-10-28）

**为什么需要独立工作集**：D2-6=A 要求为 **169 个** `preferred_zh == preferred_en` 且不含 CJK 的
concept 补中文首选名；实测这批 id **全部不在 `w3.ids`**（交集 0），其中 **9** 个在 `w2.ids`、
**28** 个为专名（`company`/`organization`/`facility`，`proper_excluded`）。既有 5 个集合均无法承接
⇒ 新增 `w3b.ids`（169 → 9 批：20×8 + 9）。

| 项 | 值 |
|---|---|
| `w3b.ids` | **169** |
| 批文件 | `w3b_b01.ids` … `w3b_b09.ids` |
| 每批大小 | 20×8 + 9 |
| `w2.ids ∩ w3b.ids` | **9**（`vmec`/`desc`/`simsopt`/`c-2u`/`eu-demo`/`gamma-10`/`helion-trenta`/`k-demo`/`start-device`） |
| `w3.ids ∩ w3b.ids` | **0** |
| category 构成 | code 97 / device 30 / company 23 / organization 6 / material 5 / concept 5 / method 2 / facility 1 |

生成命令（确定性、可复跑；`split` 序号从 00 起，需 +1 重命名为 `b01…b09`）：

```bash
python3 -c "import re;rows=[l.rstrip('\n').split('\t') for l in open('terms/registry/concepts.tsv',encoding='utf-8') if not l.startswith('#') and l.strip()];ids=[r[0] for r in rows if len(r)==8 and r[2]==r[3] and r[2] and not re.search(r'[\u3400-\u9fff]',r[2])];open('/tmp/opencode/t4973-w3b/w3b.ids','w').write('\n'.join(ids)+'\n');print(len(ids))"
split -l 20 -d -a 2 --additional-suffix=.ids /tmp/opencode/t4973-w3b/w3b.ids /tmp/opencode/t4973-w3b/w3b_b
```

> ⚠️ 不要用 `mv` 顺序重命名 `b00→b01…`（会级联覆盖，只剩 1 个文件）；必须 `cp` 到目标名（见 T3.0 执行记录）。

自检：

```bash
wc -l .github/plans/t4973-batches/w3b.ids                                  # 169
find .github/plans/t4973-batches -maxdepth 1 -name 'w3b_b*.ids' | wc -l    # 9
cat .github/plans/t4973-batches/w3b_b*.ids | wc -l                         # 169
comm -12 <(sort .../w2.ids) <(sort .../w3b.ids) | wc -l                     # 9
comm -12 <(sort .../w3.ids) <(sort .../w3b.ids) | wc -l                     # 0
```

**能失败证明（变异法）**：副本中删 `w3b_b01.ids` 一行 → 合计 169 → **168**（已实测）。

**执行约束**：
- 批验收 `.venv/bin/python scripts/registry_batch_verify.py --mode names --ids-file <w3b_bNN.ids> --expect <N> --check-urls` → exit 0；**禁止** `--allow-latin-names`。
- 只改 `terms/registry/concepts.tsv` 的 `preferred_zh` 槽位；不得改 `preferred_en`/`category`/`notes`。
- **30 个专名**（company 23 / organization 6 / facility 1）补中文名后**仍不得进入 IME 词表**（`proper_excluded` 口径不变；计划 improve 轮原记「28」经实测更正）。
- 中文名须为**可读中文术语名**（不得以拉丁串/拼音/无意义音译充数），且**不含空白**（`build_terms` 空白禁令）。
