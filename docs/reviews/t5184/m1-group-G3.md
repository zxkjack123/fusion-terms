# M1 语义复核 — 组 G3（8 样本，组内 ids = 100）（PM #5184 / S4 / T4.4）

> **计划**：`.github/plans/5184-four-stage-closeout.md` §Phase S4 / Task T4.4（套用「组通用 AC」6 条 + 组特化断言）。
> **生成时间**：2026-11-03T12:01:42+08:00（本次会话 `date` 实测输出 `Tue Nov  3 12:01:42 PM CST 2026`）；核验时 `HEAD = c2d3d3a`。
> **只读声明**：`terms/registry/*` 与 `artifacts/*` 全程只读；本任务**只新建本文件**，未执行任何 git 写命令（未 `add` / `commit` / `checkout` / `stash`），未 push。
> **样本来源**：`docs/reviews/t5184/m1-sample-manifest.tsv` 第 **18–25 行**（`group == G3` 恰 8 行），`group / batch_scope / concept_id / sha256_16` 四列**逐行原样使用**，未增删改。

## §0 复核口径（判定尺度与「不可得」计数约定）

1. **原始语料（依据可得性规则）**：按概念的 `concepts.tsv` `source` 字段分派取依据 —— `corpus` → `concepts.tsv` 该行 notes 逐字原文 + 行号；`GB/T-4960.9` → `gbt4960_9_diff.tsv` 中 `matched_concept_id` 命中行；`IAEA-safety-glossary` / `ITER-glossary` → 对应 `*_raw.tsv` 归一化命中；`http(s)` URL → 无网络访问时写 `不可得`。
2. **本组实况**：G3 的 8 个概念 `source` 字段**全部为 `corpus`**（逐行实测，见 §1），故 8 条的「原始语料」依据**全部可得** ⇒ **`原始语料: 不可得` = 0 条，`判定: UNDECIDABLE` = 0 条**（计数一致）。
3. **计数约定（防歧义）**：`不可得` 一词**仅**用于「原始语料」依据字面不可得的情形；GB/T 与 IAEA/ITER 属**非本概念 source 的旁证通道**，其无命中一律写 **`未命中`**，**不计入** `原始语料: 不可得`，以免破坏「不可得数 == UNDECIDABLE 数」的机械断言。
4. **PASS/FAIL 尺度**：`PASS` = 原始语料可得且 en/zh 定义与之无矛盾（无增义/漏义/误译/同族冲突）；`FAIL` = 有矛盾或增义/漏义/误译/同族冲突；`UNDECIDABLE` = 原始语料不可得或语义无法判定。**源不可得绝不许 PASS。**
5. **路径勘误**：任务书写的 `.github/plans/t4973-batches/gbt4960_9_diff.tsv` **实际不存在**；`gbt4960_9_diff.tsv` 的真实路径是 `artifacts/terminology_sources/gbt4960_9_diff.tsv`（本报告按真实路径取证）。

## §1 抽样出处与可复现性（实测）

**G3 逐行样本（原样取自 manifest:18–25）**

| 序 | 行 | group | batch_scope | concept_id | sha256_16 | sha256_16 复算 |
|---|---|---|---|---|---|---|
| 1 | 18 | G3 | w1_b_b07..w1_b_b11 | orbit-loss | 06a154399f037682 | OK（`printf '%s' orbit-loss \| sha256sum`） |
| 2 | 19 | G3 | w1_b_b07..w1_b_b11 | condenser | 07fd9e8c7c6ef5f3 | OK |
| 3 | 20 | G3 | w1_b_b07..w1_b_b11 | grad-b-drift | 0b05aa92eabff7d7 | OK |
| 4 | 21 | G3 | w1_b_b07..w1_b_b11 | curvature-drift | 0c63d41beda86f56 | OK |
| 5 | 22 | G3 | w1_b_b07..w1_b_b11 | tritium-accountancy | 0d331394ca8a8067 | OK |
| 6 | 23 | G3 | w1_b_b07..w1_b_b11 | gas-balance | 13d57cb9aef2700b | OK |
| 7 | 24 | G3 | w1_b_b07..w1_b_b11 | isotope-effect | 15cf3f6efe641d2c | OK |
| 8 | 25 | G3 | w1_b_b07..w1_b_b11 | cooling-tower | 18dbdca2218a8a4d | OK |

- **`sha256_16` 定义反推并复算**：`sha256_16 = sha256(concept_id)` 前 16 位十六进制；8/8 复算与 manifest 一致（`awk -F'\t' '$1=="G3"' … | while read …` 逐行比对，无 MISMATCH）。
- **组级样本 hash 复现**：`sha256("\n".join(sorted(G3 concept_id 列表)))` = `3bc3951d9d73a24a2e39e2f8075020b0aaf3c3b409af8997560415e3395270e2`，与 manifest 第 68 行 `# group_sample_sha256 G3 …` **逐字一致**（样本集可复现）。
- **source 字段实测**：`awk -F'\t' '$1!~/^#/ {print $8}' terms/registry/concepts.tsv` → 8 个 G3 概念均为 `corpus`。
- **旁证通道数据面实测**：`gbt4960_9_diff.tsv` 561 行（`matched_concept_id` 非空 182 行）；`iter_glossary_diff.tsv` 142 行（命中 64）；`iaea_safety_glossary_diff.tsv` 876 行（命中 74）。上述 182 + 64 + 74 条命中中**均无** G3 的 8 个 `concept_id`（见 §3）。

## §2 逐条语义复核（8 条）

### G3-1 · orbit-loss

原始语料: `terms/registry/concepts.tsv:761`（source=`corpus`）notes 列逐字原文 = "Fast ion loss due to large orbit width exceeding confinement"
  - GB/T-4960.9 通道（`matched_concept_id`）：未命中（`grep -cP "\torbit-loss\t" artifacts/terminology_sources/gbt4960_9_diff.tsv` = 0）
  - IAEA/ITER 通道（`*_raw.tsv` term 归一化匹配）：未命中（IAEA 876 行 / ITER 142 行均 0 命中）
定义文本:
  - en（`terms/registry/definitions.tsv:4948`）逐字 = "Fast ion loss caused by a large orbit width exceeding confinement."
  - zh（`terms/registry/definitions.tsv:4949`）逐字 = "轨道损失是轨道宽度超出约束范围的快离子损失。"
适用性推理: ①en 定义与语料 notes 逐义一致（仅 `due to` → `caused by` 的同义改写），关键限定语 **"large orbit width"** 与 **"exceeding confinement"** 两项均被完整保留，准确刻画聚变装置中快离子因轨道宽度大到越过约束边界而被移除的对象，未扩大到全部"快离子损失"。②zh 与 en 等价：主语「轨道损失」= orbit loss，限定语「轨道宽度超出约束范围」承载 "large orbit width exceeding confinement"，属**压缩而非漏义**（en 的 "large" 由「超出约束范围」这一结果性表述隐含承载），未见增义或误译；forbidden 项「轨道丢失」标注「误译 loss：正确为 轨道损失」判定正确。③同族检查：全表 `preferred_zh`/`preferred_en` 各自唯一，alias 文本无跨概念碰撞；与 `prompt-loss`（notes: "Fast ion loss on first orbit after birth"）/`charge-exchange-loss`（"…charge exchange with neutrals"）/`end-loss`/`loss-cone` 均为不同判据，定义不互相矛盾。**观察项（非阻塞）**：alias「fast ion loss」外延大于本概念（快离子损失在文献中另有 Alfvén 本征模与 MHD 诱因，与同族 `prompt-loss` 存在部分外延重叠），属 alias 粒度观察，非定义缺陷。
判定: PASS
证据锚点: concepts.tsv:761

### G3-2 · condenser

原始语料: `terms/registry/concepts.tsv:516`（source=`corpus`）notes 列逐字原文 = "Device condensing exhaust steam back to water"
  - GB/T-4960.9 通道（`matched_concept_id`）：未命中（`grep -cP "\tcondenser\t" artifacts/terminology_sources/gbt4960_9_diff.tsv` = 0）
  - IAEA/ITER 通道（归一化匹配）：未命中（含 "condenser" 的整词行在 IAEA/ITER 两份 raw 中均 0 条）
定义文本:
  - en（`terms/registry/definitions.tsv:3811`）逐字 = "A device that condenses exhaust steam back into water."
  - zh（`terms/registry/definitions.tsv:3812`）逐字 = "凝汽器是将排汽冷凝回水的装置。"
适用性推理: ①en 定义与语料 notes 一致，关键限定语 **"exhaust steam"**（排汽）与 **"back into water"**（冷凝回水）均保留，准确刻画电站/聚变 BOP 蒸汽循环里把汽轮机排汽再凝结为凝结水的设备，未泛化为化学意义上的通用冷凝器。②zh 与 en 等价：「装置」= device、「排汽」= exhaust steam、「冷凝回水」= condenses back into water，无增义/漏义/误译；`preferred_zh`「凝汽器」与 alias preferred 一致，deprecated 项「冷凝器」附注「非标准：电力行业应为 凝汽器」，术语口径正确。③同族检查：与 `cooling-tower`（notes: "Structure rejecting waste heat to atmosphere"，向大气排废热）职责互补而不重合（凝汽器在闭式循环侧换热，冷却塔向环境排热），与 `heat-exchanger`/`rankine-cycle`/`balance-of-plant` 亦不冲突；全表无第二行使用「凝汽器」或 "condenser"，无同族冲突。
判定: PASS
证据锚点: concepts.tsv:516

### G3-3 · grad-b-drift

原始语料: `terms/registry/concepts.tsv:758`（source=`corpus`）notes 列逐字原文 = "Particle drift due to magnetic field gradient"
  - GB/T-4960.9 通道（`matched_concept_id`）：未命中（`grep -cP "\tgrad-b-drift\t" artifacts/terminology_sources/gbt4960_9_diff.tsv` = 0）
  - IAEA/ITER 通道（归一化匹配）：未命中（"grad-B drift"/"gradient drift" 归一化后在两份 raw 中均 0 命中）
定义文本:
  - en（`terms/registry/definitions.tsv:4365`）逐字 = "Particle drift caused by a magnetic field gradient."
  - zh（`terms/registry/definitions.tsv:4366`）逐字 = "∇B漂移是由磁场梯度引起的粒子漂移。"
适用性推理: ①en 定义与语料 notes 逐义一致（`due to` → `caused by`），关键限定语 **"magnetic field gradient"** 完整保留且**单一化**——未混入曲率项，准确刻画导心近似下由磁场强度梯度 ∇B 引起的粒子漂移。②zh 与 en 等价：「由磁场梯度引起的粒子漂移」对应 "caused by a magnetic field gradient"，`preferred_zh` 采用符号形式「∇B漂移」并与定义正文首词一致，无增义/漏义；forbidden 项「磁场梯度偏移」「梯度B偏移」以「误译 drift：正确为 梯度B漂移」标注，指出 drift 不可译作「偏移」，判定正确。③同族检查：与并列机制 `curvature-drift`（notes 锚定 "magnetic field line curvature"）严格互斥——本条限定语只含**梯度**、不含**曲率**，两定义边界不重叠；与 `exb-drift`/`diamagnetic-drift`/`precession-drift`/`drift-kinetics` 分属不同驱动，无冲突；alias「梯度B漂移」「gradient-B drift」「grad B drift」均归本概念，无跨概念碰撞。
判定: PASS
证据锚点: concepts.tsv:758

### G3-4 · curvature-drift

原始语料: `terms/registry/concepts.tsv:759`（source=`corpus`）notes 列逐字原文 = "Particle drift due to magnetic field line curvature"
  - GB/T-4960.9 通道（`matched_concept_id`）：未命中（`grep -cP "\tcurvature-drift\t" artifacts/terminology_sources/gbt4960_9_diff.tsv` = 0）
  - IAEA/ITER 通道（归一化匹配）：未命中（"curvature drift" 归一化后在两份 raw 中均 0 命中）
定义文本:
  - en（`terms/registry/definitions.tsv:3924`）逐字 = "Particle drift caused by magnetic field line curvature."
  - zh（`terms/registry/definitions.tsv:3925`）逐字 = "曲率漂移是由磁力线曲率引起的粒子漂移。"
适用性推理: ①en 定义与语料 notes 逐义一致，关键限定语 **"magnetic field line curvature"**（磁力线曲率，而非真空室几何曲率或压强曲率）完整保留，准确刻画弯曲磁力线导致的导心漂移，未与梯度项混写。②zh 与 en 等价：「由磁力线曲率引起的粒子漂移」给出了限定语源头（磁力线曲率），`preferred_zh`「曲率漂移」与定义正文一致，无增义/漏义；forbidden 项「曲率偏移」（drift 误译为偏移）、「弯曲漂移」（curvature 误译为弯曲）标注理由均正确，且 alias「曲率漂移速度」限定为 velocity form 形式，未改变概念外延。③同族检查：与 `grad-b-drift` 构成一对并列漂移机制且两定义各自只引用各自限定语（曲率 vs 梯度），无定义冲突；与 `exb-drift`/`diamagnetic-drift` 亦不冲突；「曲率漂移」在全表唯一，无重名。
判定: PASS
证据锚点: concepts.tsv:759

### G3-5 · tritium-accountancy

原始语料: `terms/registry/concepts.tsv:601`（source=`corpus`）notes 列逐字原文 = "Quantitative tracking of tritium inventory for nuclear safeguards"
  - GB/T-4960.9 通道（`matched_concept_id`）：未命中（`grep -cP "\ttritium-accountancy\t" artifacts/terminology_sources/gbt4960_9_diff.tsv` = 0）
  - IAEA/ITER 通道（归一化匹配）：未命中（"tritium accountancy"/"tritium accountability" 归一化后 0 命中）
定义文本:
  - en（`terms/registry/definitions.tsv:5694`）逐字 = "Quantitative tracking of the tritium inventory for nuclear safeguards."
  - zh（`terms/registry/definitions.tsv:5695`）逐字 = "氚衡算是为核保障目的对氚存量进行的定量跟踪。"
适用性推理: ①en 定义与语料 notes 一致（仅加定冠词 the），关键限定语 **"quantitative tracking"**（定量跟踪=衡算行为）与 **"for nuclear safeguards"**（核保障目的）均保留，准确刻画聚变厂氚管理的量测/记账职能，而非单纯的存量描述。②zh 与 en 等价：「定量跟踪」= quantitative tracking、「氚存量」= tritium inventory、「为核保障目的」= for nuclear safeguards；「accountancy」译「衡算」符合核材料衡算（nuclear material accountancy, 核材料衡算）的中文惯用口径，无增义/漏义；forbidden 项「氚会计」「氚核算」标注「误译 accountancy」判定正确，alias「氚账目管理」限定为 management form。③同族检查：与 `tritium-inventory`（notes: "Total tritium quantity in a system" 存量实体）、`tritium-inventory-control`（存量控制）、`tritium-accounting-area`（notes: "tritium-accountancy 设施级补充" 区域对象）按「行为 / 实体量 / 空间对象」分层，本概念以 "quantitative tracking" 锚定行为层，定义不与实体量层冲突；「氚衡算」全表唯一，无同族冲突。
判定: PASS
证据锚点: concepts.tsv:601

### G3-6 · gas-balance

原始语料: `terms/registry/concepts.tsv:806`（source=`corpus`）notes 列逐字原文 = "Balance of gas injection, recycling and pumping in device"
  - GB/T-4960.9 通道（`matched_concept_id`）：未命中（`grep -cP "\tgas-balance\t" artifacts/terminology_sources/gbt4960_9_diff.tsv` = 0）
  - IAEA/ITER 通道（归一化匹配）：未命中（"gas balance" 归一化后在两份 raw 中均 0 命中）
定义文本:
  - en（`terms/registry/definitions.tsv:4347`）逐字 = "The balance of gas injection, recycling and pumping in a device."
  - zh（`terms/registry/definitions.tsv:4348`）逐字 = "气体平衡是装置内气体注入、再循环与抽气的平衡。"
适用性推理: ①en 定义与语料 notes 一致（补冠词 a），关键限定语 **"gas injection, recycling and pumping"** 三通道项与 **"in a device"**（装置内，非开放式边界）均完整保留，准确刻画聚变装置燃料气体收支平衡。②zh 与 en 等价：「注入」= injection、「再循环」= recycling、「抽气」= pumping（抽气系真空/偏滤器语境惯用译法，未误作「泵送」）、「装置内」= in a device，无增义/漏义；forbidden 项「气态平衡」标注「误译 gas（气体≠气态）：正确为 气体平衡」，正确区分了 gas 的物质态与 gas 作为工质/燃料的用法；alias「气体平衡分析」限定为 analysis form。③同族检查：与 `power-balance`（notes: "Balance of heating, fusion power, and loss channels" 能量口径）、`balance-of-plant`（系统范围）、`critical-balance`/`laser-energy-balance` 口径不同，registry 无 `particle-balance` 类近义概念，`gas-balance` 的「气体」限定与 `recycling`/`wall-pumping`/`divertor-pumping`（单通道过程）呈聚合-分解关系而非冲突。**观察项（非阻塞）**：中文「气体平衡」在热力学/化学中亦可指气相同形歧义（气相平衡），但本条定义已用「注入、再循环与抽气」三通道限定消歧，`preferred_zh` 全表唯一，不构成定义缺陷。
判定: PASS
证据锚点: concepts.tsv:806

### G3-7 · isotope-effect

原始语料: `terms/registry/concepts.tsv:769`（source=`corpus`）notes 列逐字原文 = "Confinement dependence on hydrogen isotope mass"
  - GB/T-4960.9 通道（`matched_concept_id`）：未命中（`grep -cP "\tisotope-effect\t" artifacts/terminology_sources/gbt4960_9_diff.tsv` = 0）
  - IAEA/ITER 通道（归一化匹配）：未命中（"isotope effect"/"isotope mass effect" 归一化后 0 命中）
定义文本:
  - en（`terms/registry/definitions.tsv:4590`）逐字 = "Dependence of confinement on hydrogen isotope mass."
  - zh（`terms/registry/definitions.tsv:4591`）逐字 = "同位素效应是约束性能对氢同位素质量的依赖关系。"
适用性推理: ①en 定义与语料 notes 逐义一致（default 语序归一为 "Dependence of X on Y"），关键限定语 **"confinement"** 与 **"hydrogen isotope mass"**（H/D/T 质量，而非任意元素同位素）均保留，准确刻画聚变语境中约束品质随氢同位素质量变化的效应，未泛化为化学动力学同位素效应。②zh 与 en 等价：「约束性能对氢同位素质量的依赖关系」中「约束性能」对应 "confinement"（聚变语境下约束即约束品质，属译法惯用而非新增主张）、「氢同位素质量」对应 "hydrogen isotope mass"，无实质增义/漏义；forbidden 项「同位素效果」标注「误译 effect（效应≠效果）」正确，alias「同位素效应系数」限定为 coefficient form。③同族检查：与 `hydrogen-isotope`（实体）、`isotope-separation`/`isotope-separation-system`（分离工艺）、`isotope-production`、`hydrogen-isotope-exchange`（交换反应）分属不同概念，无定义冲突；「同位素效应」全表唯一。**观察项（非阻塞）**：英文 headword "isotope effect" 无内建语境，其外延大于本条定义（聚变约束依赖语义），本条已用 "confinement" 限定完成收敛。
判定: PASS
证据锚点: concepts.tsv:769

### G3-8 · cooling-tower

原始语料: `terms/registry/concepts.tsv:517`（source=`corpus`）notes 列逐字原文 = "Structure rejecting waste heat to atmosphere"
  - GB/T-4960.9 通道（`matched_concept_id`）：未命中（`grep -cP "\tcooling-tower\t" artifacts/terminology_sources/gbt4960_9_diff.tsv` = 0）
  - IAEA/ITER 通道（归一化匹配）：未命中（"cooling tower" 归一化后在两份 raw 中均 0 命中）
定义文本:
  - en（`terms/registry/definitions.tsv:3866`）逐字 = "A structure that rejects waste heat to the atmosphere."
  - zh（`terms/registry/definitions.tsv:3867`）逐字 = "冷却塔是向大气排放废热的构筑物。"
适用性推理: ①en 定义与语料 notes 一致，关键限定语 **"waste heat"**（废热，排除工艺用热）与 **"to the atmosphere"**（向大气，排除水冷换热器等闭式路径）均保留，准确刻画聚变/电站 BOP 中向环境排废热的构筑物。②zh 与 en 等价：「构筑物」对应 structure、「向大气排放废热」对应 rejects waste heat to the atmosphere，无增义/漏义/误译；`preferred_zh`「冷却塔」与 alias preferred 一致，forbidden 项「冷却水塔」标注误译正确。③同族检查：与 `condenser`（排汽冷凝回水，闭式循环侧）、`waste-heat-recovery`（余热回收，回收而非排放）在热流方向上互补且互斥（排放 vs 回收），与 `cooling-system`/`magnet-cooling`/`cooling-channel`（系统与部件级冷却）粒度不同，无同族冲突；「冷却塔」全表唯一。
判定: PASS
证据锚点: concepts.tsv:517

## §3 交叉通道抽查（GB/T-4960.9 与 IAEA/ITER 非 source 通道；`未命中` ≠ `不可得`）

| 序 | concept_id | GB/T-4960.9 `matched_concept_id` | IAEA raw 归一化 | ITER raw 归一化 |
|---|---|---|---|---|
| C1 | orbit-loss | 未命中（0/561 行） | 未命中（0/876 行） | 未命中（0/142 行） |
| C2 | condenser | 未命中（0/561 行） | 未命中（0/876 行） | 未命中（0/142 行） |
| C3 | grad-b-drift | 未命中（0/561 行） | 未命中（0/876 行） | 未命中（0/142 行） |
| C4 | curvature-drift | 未命中（0/561 行） | 未命中（0/876 行） | 未命中（0/142 行） |
| C5 | tritium-accountancy | 未命中（0/561 行） | 未命中（0/876 行） | 未命中（0/142 行） |
| C6 | gas-balance | 未命中（0/561 行） | 未命中（0/876 行） | 未命中（0/142 行） |
| C7 | isotope-effect | 未命中（0/561 行） | 未命中（0/876 行） | 未命中（0/142 行） |
| C8 | cooling-tower | 未命中（0/561 行） | 未命中（0/876 行） | 未命中（0/142 行） |

- **GB/T 通道检索式**：`grep -cP "^\t?.*\t<cid>\t" artifacts/terminology_sources/gbt4960_9_diff.tsv` 及 `awk -F'\t' '$3=="<cid>"'` 双式复核，8×0 命中；GB/T 全表 182 条非空 `matched_concept_id` 中无 G3 概念。
- **IAEA/ITER 通道检索式**：脚本对 `*_raw.tsv` 的 term 列做 `[^a-z0-9]` 剥离 + 小写归一化后做整串匹配，并附加同义/展开形式（orbit loss / grad-B drift / gradient-B drift / curvature drift / tritium accountancy / tritium accountability / gas balance / isotope mass effect / cooling tower / steam condenser 等），8×0 命中。
- **结论**：G3 概念全部**未经** GB/T 与 IAEA/ITER 归一化为已登记概念；故其依据只来自 `corpus` 通道（本就可得），本组不存在因「源不可得」而须判 `UNDECIDABLE` 的条目。

## §4 缺陷与待定台账（D 表）

| 编号 | concept_id | FAIL/UNDECIDABLE | 原因 |
|---|---|---|---|

（无条目：本组 `FAIL = 0`、`UNDECIDABLE = 0`，故 D 表数据行数 = 0。数据行格式固定为 `| D1 | <cid> | <FAIL\|UNDECIDABLE> | 原因 |`；为避免表头本身被计数，表头首列不写 `D<n>`。§5 机械断言 `grep -c '^| D'` == `FAIL + UNDECIDABLE` == 0 成立。）

## §5 组通用 AC 实跑自检（本文件）

| # | AC 断言 | 实测 | 结果 |
|---|---|---|---|
| T-A1 | `grep -c '^### '` = 8 | 8 | PASS |
| T-A2 | `grep -c '^判定: \(PASS\|FAIL\|UNDECIDABLE\)$'` = 8 | 8 | PASS |
| T-B1 | 四字段各 ≥8 | 原始语料 8（另在口径/自检节出现，`grep -c` 合计 11）/ 定义文本 8 / 适用性推理 8 / 证据锚点 8 | PASS |
| T-B2 | `grep -c '^原始语料: 不可得'` == `grep -c '^判定: UNDECIDABLE'` | 0 == 0 | PASS |
| T-B3 | D 台账行数（`grep -c '^| D'`） == FAIL + UNDECIDABLE | 0 == 0 | PASS |
| T-B4 | `grep -c 'concepts.tsv:[0-9]'` ≥8；`grep -c 'definitions.tsv:[0-9]'` ≥16 | 16；16 | PASS |
| T-C | `git diff --stat -- terms/ artifacts/` 为空；本任务只新建本 md | 空（0 行）；本人新增仅 `docs/reviews/t5184/m1-group-G3.md` | PASS |
| 组特化 | G3 8 行与 manifest 逐行相同；`awk '$1=="G3"' manifest \| wc -l` = 8 | `diff <(manifest G3 cid) <(报告 8 个 ### 标题 cid)` 无差异；8 | PASS |

**git 状态声明（实测 `git status --porcelain`）**：4 条 `??` 未跟踪项 —— `.github/plans/5184-four-stage-closeout.md`（S1 执行计划，mtime 09:00:44）、`docs/reviews/t5184/m1-group-G1.md`（12:03:42）、`docs/reviews/t5184/m1-group-G2.md`（12:03:41）**均为本会话之前或并行兄弟任务产出，非本任务新建**；**本任务唯一新增文件 = `docs/reviews/t5184/m1-group-G3.md`**。`git diff --stat -- terms/ artifacts/` 为空（0 行）；本会话未执行任何 git 写命令（未 add / commit / checkout / stash），未 push。

**三值统计**：`PASS = 8`，`FAIL = 0`，`UNDECIDABLE = 0`（合计 8）。

**观察项（非阻塞，不计入三值）**：G3-1 alias「fast ion loss」外延偏宽、与同族 `prompt-loss` 存在部分外延重叠；G3-6 中文 headword「气体平衡」存在同形歧义；G3-7 英文 headword "isotope effect" 无语境时外延偏宽。三项均不构成定义与原始语料的矛盾，故维持 `PASS`，供 T4.10 汇总与后续术语治理参考。

**手顺**：`→ handoff: USER`（T4.4 完成；组间互不阻断，等待 T4.10 汇总与用户抽核）。
