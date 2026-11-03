# T4.10 M1 8 组抽检汇总 · 缺陷台账 · 来源可得率 · 状态写回（PM #5184 / S4）

- 报告日期: 2026-11-03（`date` 实跑: `Tue Nov  3 12:39:13 PM CST 2026`）
- 汇总基线: `git rev-parse HEAD` = `495f904`（基线 `115da74`）；本汇总读取 `m1-sample-manifest.tsv` 与 8 组实际报告 `m1-group-G1..G8.md`，不重算组内判定、不改任何报告。
- 只读声明: 本汇总为 T4.10 唯一新建文件 + 父计划 M1 单行；`terms/`、`artifacts/`、`pipeline/`、`scripts/`、`category-map-*.tsv` 全程只读；未改 `docs/reviews/t5184/README.md`、未改执行计划、未改任何数据；未 push。
- 汇总口径: 三值 `PASS` / `FAIL` / `UNDECIDABLE`；`UNDECIDABLE` 不计入 PASS。**本汇总只做计数与台账归并，不重判语义、不改写组报告结论。**
- **审查性质声明**: 本报告全部内容为**审查结果**，不构成对任何 `terms/` 数据的修复授权；缺陷台账各项需另行裁决。

---

## §1 覆盖声明（抽检 ≠ 全量）

- **抽检规模: 64 / 756 = 8.5%**（W1 共 39 批 / 756 唯一 id；8 组 × 8 行确定性样本）。
- 抽样口径: 组内 id 去重后按 `sha256(id)[:16]` 升序取前 8；样本集 hash 落 `m1-sample-manifest.tsv`（8 条 `# group_sample_sha256`）。
- 组划分（编号 1–39，连续 5 批为 1 组，余 4 批为 G8）与组内 id 数: G1=87、G2=100、G3=100、G4=100、G5=100、G6=100、G7=100、G8=69。
- **明确声明: 抽检 ≠ 全量语义保证。** 本汇总的 55/64 PASS 只覆盖上述 64 行样本；不得外推为 W1 全量 756 ids 的语义正确性结论。机械门禁（格式/占位/长度）亦不覆盖语义正确性。

## §2 8 组三值计数（G1–G8）

| 组 | 批范围 | 组内 id 数 | 抽检 | PASS | FAIL | UNDECIDABLE | 组报告 |
|---|---|---|---|---|---|---|---|
| G1 | w1_a_b01..w1_b_b01 | 87 | 8 | 5 | 3 | 0 | `m1-group-G1.md` |
| G2 | w1_b_b02..w1_b_b06 | 100 | 8 | 8 | 0 | 0 | `m1-group-G2.md` |
| G3 | w1_b_b07..w1_b_b11 | 100 | 8 | 8 | 0 | 0 | `m1-group-G3.md` |
| G4 | w1_b_b12..w1_b_b16 | 100 | 8 | 6 | 2 | 0 | `m1-group-G4.md` |
| G5 | w1_b_b17..w1_b_b21 | 100 | 8 | 6 | 2 | 0 | `m1-group-G5.md` |
| G6 | w1_b_b22..w1_b_b26 | 100 | 8 | 6 | 2 | 0 | `m1-group-G6.md` |
| G7 | w1_b_b27..w1_b_b31 | 100 | 8 | 8 | 0 | 0 | `m1-group-G7.md` |
| G8 | w1_b_b32..w1_c_b01 | 69 | 8 | 8 | 0 | 0 | `m1-group-G8.md` |
| **合计** | 39 批 | 756 | 64 | 55 | 9 | 0 | PASS 55 / FAIL 9 / UNDECIDABLE 0 |

## §3 三值合计与逐组一致性

- **合计: 抽检 64 / PASS 55 / FAIL 9 / UNDECIDABLE 0**（55 + 9 + 0 = 64）。
- 逐组明细之和 = 5+8+8+6+6+6+8+8（PASS）= 55；3+0+0+2+2+2+0+0（FAIL）= 9；0（UNDECIDABLE）——与本汇总表逐组一致（已按 8 份报告 `^判定: PASS$` / `^判定: FAIL$` / `^判定: UNDECIDABLE$` 逐文件重数核对）。
- **主导项一致性（各组硬规则）**: 8 组均满足「`原始语料` 主渠道不可得条数(0) == `判定: UNDECIDABLE` 条数(0)」；各组报告均声明「不存在源不可得却判 PASS 的条目」。
- **无假通过**: 全部 64 条判定落于 `PASS`/`FAIL`，无一条以「源不可得」为由判 PASS；本组三值中 `UNDECIDABLE = 0` 成立。

## §4 缺陷台账（全部 FAIL/UNDECIDABLE，统一编号 D1–D9）

行数 = FAIL + UNDECIDABLE = 9 + 0 = **9**（与 §3 合计一致）。以下逐条为**审查发现**（供后续补证/裁决），**不是修复授权**。

| D | 组 | concept_id | 判定 | 原因（摘自对应组报告，未改写） |
|---|---|---|---|---|
| D1 | G1 | turbulent-transport | FAIL | 定义文本缺判别性限定，与同族 `anomalous-transport`（`concepts.tsv:557`、`definitions.tsv:3606/1017` "exceeding neoclassical prediction, driven by turbulence"）在定义层面不可区分；notes 的 "Anomalous … micro-turbulence" 限定未进入任何定义文本 |
| D2 | G1 | lawson-criterion | FAIL | 定义文本把判据写成「T > 10 keV 且 n·τ_E > 2×10^20 m^-3 s」两并列条件，与 notes "Minimum n·τ·T product" 非同一判据结构（`iter_glossary_raw.tsv:83` 以三参量 T/n/τ 限定）；且与同族 `fusion-triple-product`（`concepts.tsv:682`）边界重叠、无区分限定 |
| D3 | G1 | poloidal-field-coil | FAIL | 与同族 `poloidal-field-coils`（`concepts.tsv:1747`，zh「极向场线圈系统」）争夺同一中文面形「极向场线圈」且层级不一（`definitions.tsv:1404` zh 单数线圈 vs `definitions.tsv:103` en 六线圈系统）；GB/T 权威映射 `gbt4960_9_diff.tsv:413` 将该面形指向 1747，本 cid 未命中 |
| D4 | G4 | debye-shielding | FAIL | en 定义无机制/无特征尺度（未提 Debye 长度），以 "shielding / screening" 斜杠同义替换自我注释、作用对象表述不精确；与 GB/T 导入条目 `plasma-neutrality-and-debye-shield`（`concepts.tsv:2716`、`definitions.tsv:1217`）的同物理内容机制性定义不相称 |
| D5 | G4 | pfirsch-schlueter-regime | FAIL | 与 GB/T-4960.9 导入条目 `pfirsch-schulueter-regime`（`concepts.tsv:2711`、`definitions.tsv:2264/1206`）重复登记同一新经典输运区；人名拼写（Schlüter / Schulueter）与音译处置（`aliases.tsv:8953` preferred 对比 `aliases.tsv:4242` forbidden）互相矛盾；本条缺同族普遍给出的 ν* 区界判据 |
| D6 | G5 | nuclide-inventory | FAIL | 首选 zh「核素产额」为 `nuclide inventory` 的误译（inventory=存量 ≠ yield=产额），与同族 `tritium-inventory`（`concepts.tsv:254` 氚存量）、`tritium-startup-inventory`(484)、`dust-inventory`(989) 的「‑inventory→‑存量」范式冲突，亦与本条自设 alias「核素清单」(`aliases.tsv:5313`) 口径相左 |
| D7 | G5 | nuclear-fusion | FAIL | en/zh 定义均为同语反复（"核聚变指最一般意义上的核聚变"），无机制、无判别语；且与 `fusion`（`concepts.tsv:1084`）重复登记同一"最一般义的核聚变"，中文面「核聚变」归属与 GB/T-4960.9 权威映射（`gbt4960_9_diff.tsv:110` → cid `fusion`）冲突 |
| D8 | G6 | plasma-termination | FAIL | 与同库 `plasma-shutdown`（`concepts.tsv:1744`，zh「等离子体熄灭」，ITER+GB/T 双源）重复登记同一放电终止过程；本条在 `iter_glossary_diff.tsv:98` 与 `gbt4960_9_diff.tsv:411` 均无匹配；与 `plasma-ramp-down`（`concepts.tsv:781`）边界互斥、相位序颠倒；自身 en/zh（`definitions.tsv:5068/5069`）仅一句位置标签，无可判定限定语 |
| D9 | G6 | rupture-disc | FAIL | zh 定义（`definitions.tsv:5352`）含「主动破裂」，en（`definitions.tsv:5351`）及依据引语（`evidence.tsv:1500`）均无对应词，且与库内「主动」= actively- 用法（`concepts.tsv:894`）及同批 `relief-valve` 的「自动开启」（`definitions.tsv:5293`）互斥；反向 en 相对依据引语漏掉动作定值限定语 "at set pressure differential" |

**分组台账行数一致性**: G1=3、G4=2、G5=2、G6=2、其余 0 → 3+2+2+2 = 9 = §3 合计 FAIL。各组报告内台账行数亦等于该组 (FAIL + UNDECIDABLE)。

## §5 来源可得率（概念 source 主渠道 与 定义外部来源**必须区分**）

> 口径区分: **「概念 source 主渠道」= `concepts.tsv` 第 8 列 `source`**（决定 notes 原始语料是否可得）；**「定义外部来源」= `definitions.tsv` 第 4 列 `source`**（决定 en/zh 定义文本所引外部来源是否可得）。两者**不是同一指标**，不得混算。

### 5.1 概念 source 主渠道可得率

- 64 个样本的 `concepts.tsv` `source` 列**全部为 `corpus`**（`corpus` 64 / 64 = **100%**），故 notes 逐字原文 + 行号**全部可得**。
- 结论: **概念 source 主渠道可得率 = 64/64 = 100%（可得）**；这也正是 8 组 `原始语料: 不可得 = 0`、`UNDECIDABLE = 0` 的直接原因。

### 5.2 定义外部来源可得性（**不得声称外部验证通过**）

- 64 个样本共 128 条定义行（每 cid 各 1 条 en + 1 条 zh）的 `definitions.tsv` `source` 列分布（本次只读实测）:

| 定义 source | 行数 | 占比 | 涉及 cid |
|---|---|---|---|
| `corpus`（仓内扩展，非外部） | 114 | 89.1% | — |
| `GB/T-4960.9`（外部） | 12 | 9.4% | drift-wave、faraday-rotation、fishbone-instability、lawson-criterion、plateau-regime、turbulent-transport |
| `https://…oxfordlearnersdictionaries.com…/reactor`（外部 URL） | 2 | 1.6% | reactor |

- 即**仅 14/128 = 10.9%** 的定义行标注外部来源；其余 114 行为仓内扩展（`corpus`）。
- **外部来源可得性（按旁证通道实测，取自 8 组报告）**:
  - **GB/T-4960.9**: 仓内快照 `artifacts/terminology_sources/gbt4960_9_diff.tsv`（562 行）**可得**；但按 `matched_concept_id` 交叉命中仅 **4/64**（faraday-rotation、turbulent-transport、drift-wave、lawson-criterion），其余 60 个样本该通道**未命中**。
  - **IAEA**: `iaea_safety_glossary_raw.tsv` 对 64 样本 **0/64 命中**。
  - **ITER**: `iter_glossary_raw.tsv` 对 64 样本 **2/64 命中**（lawson-criterion；poloidal-field-coil 的命中面形实为复数/系统级条目、指向 `concepts.tsv:1747`，非本 cid）。
  - **http(s) URL**: 本汇总**无独立复核网络通道**；`reactor` 的 2 行 URL 定义由 G5 组**自报**「实际取回成功（取回日期 2026-11-03）」，本 T4.10 汇总**未独立复核**该取回。
- **结论（关键，防止过度声明）**: 上述数字只说明「外部来源是否在仓内快照/自报渠道**可得**」，**不等于**「定义与外部权威已比对且一致」。因此:
  - **外部来源验证未建立**（0 个样本在本次汇总中取得经独立复核的外部权威原文比对结论）；
  - **不得声称「外部验证通过」**；凡依赖外部权威才能定论者，与 8 组报告一致，一律不作为 PASS 依据。

## §6 M1 状态判定（保持未勾）

- 勾选门槛（计划 T4.10）: `sum(PASS) == 64 && sum(FAIL) == 0 && sum(UNDECIDABLE) == 0` 才可 `[x]`。
- 实测: `sum(PASS) = 55 ≠ 64`、`sum(FAIL) = 9 > 0`、`sum(UNDECIDABLE) = 0`。**双向状态断言 → 走 else 分支。**
- **判定: M1 保持未勾（`- [ ] M1`）**；父计划 M1 单行追加「T4.10 抽检完成但未达全 PASS」注记，**不改为 `[x]`**。
- 附: 已勾项 `M4`（S3 完成）与未勾项 `M3`（S2 查证完成、待裁决）均**不在本 Task 改动范围**；本 Task 只允许 M1 单行变化。

## §7 G1 计数更正（口头错报以文件为准）

- **先前口头汇报称 G1 为「2 FAIL」——与文件不符。** 以 `docs/reviews/t5184/m1-group-G1.md` 为准，G1 实为 **3 FAIL**:
  - `grep -c '^判定: FAIL$' m1-group-G1.md` = **3**（`turbulent-transport`、`lawson-criterion`、`poloidal-field-coil`，行号 64 / 112 / 124）；
  - 该报告 §判定汇总（第 132 行）与缺陷台账（D1–D3，第 141–143 行）均记 **3**；
  - 组报告第 135 行原文亦自述「8 条中 **3 条**存在真实语义缺陷」。
- 影响: 三值合计 FAIL = **9**（非按错报的 8）；M1 未勾结论不变（FAIL > 0）。
- **以文件为准；口头/记忆计数不作为证据。**

## §8 观察项汇总（非阻塞，**不计入三值、不改变判定、非修复授权**）

以下为各组报告中标注的不构成 FAIL/UNDECIDABLE 的观察建议，仅供后续术语治理参考:

- G2: 4 条（`hccb` 模板归属歧义、`实验/试验` 用字、`用于调节` 语气差、zh 漏译 `toroidal`）。
- G3: 3 条（`fast ion loss` alias 外延偏宽、`气体平衡` 同形歧义、`isotope effect` 无语境外延偏宽）。
- G4: 3 处族内重叠/别名层竞争观察（`implosion` 裸别名、`plasma-sustainment` 限定语跨域、`impurity-source` 边界偏薄）。
- G6: 3 处（`forced-convection` 范畴滑移、`working-fluid`/冷却剂界线、`data-pipeline`/`workflow-automation` 重叠）。
- G7: 4 条派生观察（grid 类边界、systems/digital 共享措辞、tilt/frc 定义域、`cbet` 命名）。
- G8: 6 条 O1–O6（能量耗散族边界、`计数效率` 同形、命名一致性/格式、XICS 别名、远程焊接别名过窄、波吸收交叠）。
- G1 / G5: 报告以「残余观察」形式并入推理段，未单列台账项。
- 这些观察项**不属于本汇总的三值计数**，也不构成对任何数据的修改授权。

## §9 AC 自检（T4.10 实跑，先验收后提交）

| AC 项 | 命令 | 期望 | 实测 |
|---|---|---|---|
| T-A 组行数 | `grep -c '^| G[1-8] ' docs/reviews/t5184/m1-summary.md` | = 8 | 见提交前验收日志 |
| T-A 总计行含三值 | 总计行同时出现 `PASS`/`FAIL`/`UNDECIDABLE` | 是 | 见 §3 |
| T-B 三值合计一致 | 本表逐组 hand-sum vs 8 组报告 `grep -c '^判定: …$'` 相加 | 55 / 9 / 0 | 55 / 9 / 0 |
| T-B 双向状态 | `sum(PASS)==64 && FAIL==0 && UNDEC==0` ⇒ M1 `[x]`，否则 `[ ]` | 未勾 | M1 = `[ ]`（`grep -c '^- \[x\] M1:'` = 0） |
| T-B 不假通过 | `UNDECIDABLE==0` 但 `FAIL>0` ⇒ 不得勾 | 未勾 | 未勾 |
| T-C 父计划仅 M1 行变 | `git diff --unified=0 HEAD~1 HEAD -- 父计划 \| grep -cE '^[+-].*M[34]:'` | = 0 | 见提交前验收日志 |

**文件范围（T4.10 声明）**: `docs/reviews/t5184/m1-summary.md`（新建）+ 父计划 M1 单行；数据零写（`git diff --stat -- terms/ artifacts/ pipeline/ scripts/` 为空）。

**手顺**: `→ handoff: USER`（T4.10 完成；M1 保持未勾，缺陷台账 D1–D9 待裁决/补证；组间互不阻断）。
