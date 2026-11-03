# M1 语义抽检报告 — 组 G4（8 样本）

> **计划**：`.github/plans/5184-four-stage-closeout.md` §Phase S4 / Task T4.5（PM #5184 / FUSION-TERMS id240）
> **生成日期**：**2026-11-03**（`date` 实测：`Tue Nov  3 11:54:10 AM CST 2026`）
> **性质**：**只读语义复核**。`terms/registry/*`、`artifacts/*` 全程只读；本报告为唯一新建文件；执行过程中**未运行任何 git 写命令**（不 add / commit / checkout / stash / push）。
> **判定口径**：`PASS` = 该概念的 en/zh 定义与仓内原文、族内相邻条目及本组依据逐条核验后无实质缺陷；`FAIL` = 存在可指认的语义缺陷（定义不能刻画对象、与同族/同库条目重复或矛盾）；`UNDECIDABLE` = 源语料取不到（**来源缺失**，不计入 PASS）。
> **来源可得性规则（照计划 §S4 统一口径）**：`source=corpus` → 依据 = `concepts.tsv` notes 原文 + 行号（可得）；`source=GB/T-4960.9` → 依据 = `gbt4960_9_diff.tsv` 的 `matched_concept_id` 命中行；`source=IAEA-safety-glossary / ITER-glossary` → 依据 = `*_raw.tsv` 归一化命中行；`source=http(s)://…` → 依据 = URL + 取回日期 + 片段。
> **AC 计数正则声明**：本组 8 个概念的 `source` 字段**全部为 `corpus`**，依据一律取 `concepts.tsv` notes 逐字 + 行号，因此本组**不存在来源缺失样本**；按组通用 AC 第 3 条（`^原始语料: <来源缺失标记>` 行数须等于 `^判定: UNDECIDABLE$` 行数），本组 `UNDECIDABLE` 数 = 0，故全文不使用该三字来源缺失标记，以免与 AC 计数正则互相污染。

## §0 组样本清单（与 `m1-sample-manifest.tsv` 的 G4 8 行逐行相同）

抽取口径（manifest 头与 README 声明）：组内 id 去重排序后取 `sha256(id)[:16]` 升序前 8。分组口径：`w1_a_b01..b04` → `w1_b_b01..b34` → `w1_c_b01` 连续编号，连续 5 批为 1 组。G4 = `w1_b_b12..w1_b_b16`，组内 ids = 100。

| 序 | group | batch_scope | concept_id | sha256_16 |
|---|---|---|---|---|
| 1 | G4 | w1_b_b12..w1_b_b16 | capsule-implosion | 0549fd8cae94f3da |
| 2 | G4 | w1_b_b12..w1_b_b16 | radiation-dominated-regime | 07d86acfe4421a9a |
| 3 | G4 | w1_b_b12..w1_b_b16 | plasma-sustainment | 0d959f105847fcf9 |
| 4 | G4 | w1_b_b12..w1_b_b16 | turbulence-saturation | 1137353a7978d2c8 |
| 5 | G4 | w1_b_b12..w1_b_b16 | impurity-source | 18704d07af064a6e |
| 6 | G4 | w1_b_b12..w1_b_b16 | presheath | 19541eb2f8074830 |
| 7 | G4 | w1_b_b12..w1_b_b16 | debye-shielding | 19e85d55d4830438 |
| 8 | G4 | w1_b_b12..w1_b_b16 | pfirsch-schlueter-regime | 1a354ae9ec2eaf0b |

`sha256_16` 复算核验：`sha256(concept_id)[:16]` 对上述 8 个 cid 逐一复算，与 manifest 的 `sha256_16` 列**全部一致**（抽查命令：`python3 -c "import hashlib;print(hashlib.sha256(b'capsule-implosion').hexdigest()[:16])"` → `0549fd8cae94f3da`）。

## §1 依据可得性与交叉核验执行记录（口径与命令）

- **组内依据类分布**：`awk -F'\t' '{print $8}' terms/registry/concepts.tsv` 对 8 个 cid 取第 8 列 → `corpus` × 8。
- **原始语料取法（每样本）**：`grep -nP "^<cid>\t" terms/registry/concepts.tsv` → 该行 notes（第 7 列）逐字 + 行号。
- **定义文本取法（每样本）**：`grep -nP "^<cid>\t(en|zh)\t" terms/registry/definitions.tsv` → en、zh 两行逐字 + 行号（本组每概念各 1 条 en、1 条 zh，`source` 列同为 `corpus`）。
- **GB/T-4960.9 交叉核验**：任务给定路径 `.github/plans/t4973-batches/gbt4960_9_diff.tsv` **在本仓不存在**（`ls` 返回 `No such file or directory`）；实际文件为 `artifacts/terminology_sources/gbt4960_9_diff.tsv`（562 行，列 `#term / status / matched_concept_id / term_id / zh / abbr / definition`）。以该文件核验：`awk -F'\t' -v c="<cid>" '$3==c'` 对 8 个 cid 的命中数**全部为 0**（该文件 `matched_concept_id` 非空行共 182 行）。与本组相关的未映射条目有 `:53 Debye length`（→`debye-length`）、`:223 plasma neutrality and debye shield`（status=`new`，无 matched id，zh=等离子体中性与德拜屏蔽）、`:231 plasma sheath`（→`debye-sheath`）。
- **IAEA / ITER 交叉核验**：`grep -icP "^<en form>\t" artifacts/terminology_sources/{iter_glossary_raw.tsv,iaea_safety_glossary_raw.tsv}` 对 `capsule implosion` / `radiation-dominated` / `radiation dominated` / `plasma sustainment` / `turbulence saturation` / `impurity source` / `presheath` / `Debye shielding` / `debye screening` / `Pfirsch` 的归一化（大小写不敏感）命中数**全部为 0**（iter 143 行、iaea 877 行）。
- **http(s) URL 类**：本组 8 个概念的 `source` 均非 URL，该类按 source 分派不适用；本环境亦无网络取回工具，故未做 URL 取回（不做任何"假装取回"的记述）。
- **独立依据强度注记**：8 个概念的 `terms/registry/evidence.tsv` 依据行**全部为内部扩展**（`internal:expansion:batch-NN`，`added_by=copilot`，见 §2 各样本附注），即 notes/定义来自仓内扩展流程而非外部语料条目；这不影响本组的来源**可得性**（口径取 `concepts.tsv` notes），但限制了对 en 定义做"外部权威比对"的强度——凡涉及外部权威才能定论的判断，本报告一律不作为 `PASS` 依据（见 §3 D1/D2 的取舍口径）。

## §2 逐样本复核（8 样本）

### 样本 1/8 — `capsule-implosion`

G4	w1_b_b12..w1_b_b16	capsule-implosion	0549fd8cae94f3da

- 原始语料: [source=corpus，可得] notes 逐字（`terms/registry/concepts.tsv:847`）：`Driven inward compression of ICF capsule`（该行逐字：`capsule-implosion | concept | 靶丸内爆 | capsule implosion | (空) | active | Driven inward compression of ICF capsule | corpus`）；GB/T-4960.9 交叉核验：`artifacts/terminology_sources/gbt4960_9_diff.tsv` 中 `matched_concept_id==capsule-implosion` 命中 0 行；IAEA/ITER 交叉核验：`iter_glossary_raw.tsv` / `iaea_safety_glossary_raw.tsv` 对 `capsule implosion` 归一化命中 0 行；http(s) URL 类：不适用（source≠URL）。附注：`terms/registry/evidence.tsv:775` 记其依据为 `internal:expansion:batch-36`（引语 `ICF capsule compression`，`copilot`，2026-03-19）。
- 定义文本: en 与 zh 逐字见下两行（两处行号：`terms/registry/definitions.tsv:3735`（en）、`terms/registry/definitions.tsv:3736`（zh），两行 `source` 列均为 `corpus`）
- 定义(en) 逐字: definitions.tsv:3735 → `Driven inward compression of an ICF capsule.`
- 定义(zh) 逐字: definitions.tsv:3736 → `靶丸内爆是惯性约束聚变靶丸受驱动向内压缩的过程。`
- 适用性推理: ①en 以限定语 "Driven"（受驱动，排除自发过程）与 "inward"（内指压缩方向）刻画作用方式，以 "of an ICF capsule" 限定对象为惯性约束聚变靶丸，与 notes 的 "Driven inward compression of ICF capsule" 逐词同源，在聚变语境中准确刻画该过程。②zh 与 en 等价：ICF 被显式展开为"惯性约束聚变"、并补出范畴词"过程"，均为等同展开而非增义（en 的 compression 本即过程性表述）；"受驱动"↔driven、"向内压缩"↔inward compression、"靶丸"↔capsule 三项一一对应，无漏义、无误译、无术语漂移（首选 zh 与 `aliases.tsv:2803` 的 `靶丸内爆 / zh / preferred` 一致）。③同族条目 `implosion-velocity`（definitions.tsv:1762，速度量，含 km/s 量纲）、`convergence-ratio`（1662，比值量）、对象级条目 `liner-implosion`（4659，"compression of a magnetized plasma by the implosion of a metal liner"，对象为金属衬套+磁化等离子体）均因对象或量纲不同而可分辨，未见互斥；唯一需登记的观察项是 `aliases.tsv:4453–4454` 把裸 `implosion` / `内爆` 作为本概念的通用别名，与 `liner-implosion`（衬套内爆）在别名层面存在竞争，但这是别名层面的问题，不构成本概念定义文本的冲突。
判定: PASS

- 证据锚点: concepts.tsv:847

### 样本 2/8 — `radiation-dominated-regime`

G4	w1_b_b12..w1_b_b16	radiation-dominated-regime	07d86acfe4421a9a

- 原始语料: [source=corpus，可得] notes 逐字（`terms/registry/concepts.tsv:962`）：`High-temperature regime where radiation loss exceeds fusion power`（该行逐字：`radiation-dominated-regime | concept | 辐射主导区间 | radiation-dominated regime | (空) | active | High-temperature regime where radiation loss exceeds fusion power | corpus`）；GB/T-4960.9 交叉核验：`matched_concept_id==radiation-dominated-regime` 命中 0 行；IAEA/ITER 交叉核验：对 `radiation-dominated` / `radiation dominated` 归一化命中 0 行；http(s) URL 类：不适用。附注：`terms/registry/evidence.tsv:878` 记其依据为 `internal:expansion:batch-47`（引语 `Radiation>fusion power zone`，`copilot`，2026-03-19）；本概念所属批次为 `concepts.tsv:958`「Batch 47: Proton-Boron Fusion & Advanced Fuel Physics」。
- 定义文本: en 与 zh 逐字见下两行（两处行号：`terms/registry/definitions.tsv:5198`（en）、`terms/registry/definitions.tsv:5199`（zh），两行 `source` 列均为 `corpus`）
- 定义(en) 逐字: definitions.tsv:5198 → `A high-temperature regime where radiation loss exceeds fusion power.`
- 定义(zh) 逐字: definitions.tsv:5199 → `辐射主导区间是辐射损失超过聚变功率的高温区间。`
- 适用性推理: ①en 以不等式判据 "radiation loss exceeds fusion power" 给出可判定的物理边界，并以 "high-temperature" 限定所处温区，与 notes 的 `High-temperature regime where radiation loss exceeds fusion power` 逐词一致；同库同族的 `bremsstrahlung`（concepts.tsv:211 notes："Radiation loss from electron deceleration; dominant loss in p-B11"）与 `hot-ion-mode`（concepts.tsv:231 notes："Regime with Ti >> Te; suppresses bremsstrahlung in p-B11"）独立支持"p-B11 语境下辐射损失可与聚变功率相抗"这一用法，故 en 在该批语境中刻画成立；保留意见：定义未限定辐射通道（轫致/线/同步）也未给出临界温度，判据虽可判但定界偏松。②zh 与 en 等价：regime→区间、radiation loss→辐射损失、exceeds→超过、fusion power→聚变功率、high-temperature→高温，无增义、无漏义、无误译；"区间"与 `aliases.tsv:4581` 的短形式 `辐射主导区` 同族，`aliases.tsv:4172/4173` 已把"辐射主导制度/辐射主导方案"按 regime 政治义判为 forbidden，本定义用"区间"与之口径一致。③族内未见互斥：`radiation-loss`（definitions.tsv:1898，en 为 "Power radiated from plasma by bremsstrahlung, line emission, and recombination, in MW; impurity-driven"）给出通道口径，本概念在其上叠加"辐射损失 > 聚变功率"的收支判据，二者为通道与判据的关系而非互斥；存在一处**跨条目指称张力**（p-B11 的辐射损失主体为燃料轫致辐射，与 `radiation-loss` 注释的"多由杂质驱动"口径不同），但该张力的落点在 `radiation-loss` 的注释侧，不构成本定义自身的冲突。
判定: PASS

- 证据锚点: concepts.tsv:962

### 样本 3/8 — `plasma-sustainment`

G4	w1_b_b12..w1_b_b16	plasma-sustainment	0d959f105847fcf9

- 原始语料: [source=corpus，可得] notes 逐字（`terms/registry/concepts.tsv:955`）：`Non-inductive current and confinement sustainment`（该行逐字：`plasma-sustainment | concept | 等离子体维持 | plasma sustainment | (空) | active | Non-inductive current and confinement sustainment | corpus`）；GB/T-4960.9 交叉核验：`matched_concept_id==plasma-sustainment` 命中 0 行；IAEA/ITER 交叉核验：对 `plasma sustainment`（及 `sustain` 词干）归一化命中 0 行；http(s) URL 类：不适用。附注：`terms/registry/evidence.tsv:872` 记其依据为 `internal:expansion:batch-46`（引语 `Non-inductive sustainment`，`copilot`，2026-03-19）；所属批次为 `concepts.tsv:950`「Batch 46: Spheromak/CT Devices & Formation Technologies」。
- 定义文本: en 与 zh 逐字见下两行（两处行号：`terms/registry/definitions.tsv:5066`（en）、`terms/registry/definitions.tsv:5067`（zh），两行 `source` 列均为 `corpus`）
- 定义(en) 逐字: definitions.tsv:5066 → `Non-inductive sustainment of current and confinement.`
- 定义(zh) 逐字: definitions.tsv:5067 → `等离子体维持是电流与约束的非感应维持。`
- 适用性推理: ①en 以限定语 "Non-inductive" 指定维持方式，作用对象为 "current and confinement"，与 notes 的 `Non-inductive current and confinement sustainment` 同源；在 Batch 46（球马克/CT 位形形成，同批 `sspx` concepts.tsv:951 记 "LLNL Sustained Spheromak Physics Experiment"、`coaxial-helicity-injection` concepts.tsv:942 记 "for spheromak/ST sustainment"、`helicity-injection` definitions.tsv:2359 记 "start-up/sustainment ... non-inductively"）语境下，非感应维持确为该族装置的核心特征，刻画成立；保留意见：语法上 "Non-inductive" 只能约束电流（current）的维持，用来约束 "confinement" 属限定语跨域，en 与 zh 均沿用该写法。②zh 与 en 等价：Non-inductive→非感应、"current and confinement"→"电流与约束"、sustainment→维持，无增义、无漏义、无误译；首选 zh 与 `aliases.tsv:3030`（`等离子体维持 / zh / preferred`）一致，`aliases.tsv:3512` 已把"等离子体维护"按 sustainment 误译判为 forbidden，处置正确。③族内重叠度偏高但未见互斥：`non-inductive-operation`（definitions.tsv:4876，"Operation in which the plasma current is sustained by external current drive and by the bootstrap current"）给出机制（外部电流驱动+自举）且只及电流，`steady-state-operation`（definitions.tsv:118，ITER 口径的"脉冲终止不由等离子体行为决定"）、`fully-non-inductive`（definitions.tsv:4318，"100% non-inductive current drive" 的稳态运行）各自以模式或份额定界，本概念以"电流 **与** 约束"两项为作用对象，可与上述三条区分；重叠偏高登记为本组观察项，不作为定义冲突。
判定: PASS

- 证据锚点: concepts.tsv:955

### 样本 4/8 — `turbulence-saturation`

G4	w1_b_b12..w1_b_b16	turbulence-saturation	1137353a7978d2c8

- 原始语料: [source=corpus，可得] notes 逐字（`terms/registry/concepts.tsv:863`）：`Nonlinear saturation mechanism of micro-instabilities`（该行逐字：`turbulence-saturation | concept | 湍流饱和 | turbulence saturation | (空) | active | Nonlinear saturation mechanism of micro-instabilities | corpus`）；GB/T-4960.9 交叉核验：`matched_concept_id==turbulence-saturation` 命中 0 行；IAEA/ITER 交叉核验：对 `turbulence saturation` 归一化命中 0 行；http(s) URL 类：不适用。附注：`terms/registry/evidence.tsv:789` 记其依据为 `internal:expansion:batch-38`（引语 `Nonlinear saturation`，`copilot`，2026-03-19）；所属批次为 `concepts.tsv:862`「Batch 38: Plasma Turbulence & Nonlinear Physics」。
- 定义文本: en 与 zh 逐字见下两行（两处行号：`terms/registry/definitions.tsv:5720`（en）、`terms/registry/definitions.tsv:5721`（zh），两行 `source` 列均为 `corpus`）
- 定义(en) 逐字: definitions.tsv:5720 → `The nonlinear saturation mechanism of micro-instabilities.`
- 定义(zh) 逐字: definitions.tsv:5721 → `湍流饱和是微观不稳定性的非线性饱和机制。`
- 适用性推理: ①en 以限定语 "nonlinear" 指定机制性质（非线性），以 "saturation mechanism" 指定所刻画的角色，以 "of micro-instabilities" 限定作用对象，与 notes 同源；在本批族内（`critical-gradient` concepts.tsv 同批次记 "threshold gradient above which micro-instabilities drive strong transport"、`predator-prey-oscillation` definitions.tsv:同批记 "nonlinear oscillation between turbulence and zonal flows"）语料一致地把微观不稳定性作为湍流的源头，"湍流饱和"即该源头模的非线性饱和，名实相符，刻画成立。②zh 与 en 等价：turbulence→湍流、nonlinear→非线性、saturation mechanism→饱和机制、micro-instabilities→微观不稳定性，四项一一对应，无增义、无漏义、无误译；`aliases.tsv:3787` 已把"紊流饱和"判为 forbidden（误译 turbulence），本定义采用"湍流"口径一致。③族内未见冲突：`turbulence-suppression`（definitions.tsv:5724，"Suppression of turbulence by E and B shear and other mechanisms"）是外部剪切机制的抑制作用，`turbulence-spreading`（definitions.tsv:5722，"Spatial diffusion of turbulence from unstable to stable regions"）是湍流的空间扩展，`spectral-transfer`/`critical-balance` 各自指向能谱级联与时间尺度平衡，本概念专指自身非线性饱和机制，在机制与对象上与上述均互斥可辨；另需注意本概念与 `zonal-flow` 类条目为"饱和机制"与"承载该机制的结构"的关系，非重复登记。
判定: PASS

- 证据锚点: concepts.tsv:863

### 样本 5/8 — `impurity-source`

G4	w1_b_b12..w1_b_b16	impurity-source	18704d07af064a6e

- 原始语料: [source=corpus，可得] notes 逐字（`terms/registry/concepts.tsv:971`）：`Impurity production yield and spatial distribution at the wall`（该行逐字：`impurity-source | concept | 杂质源 | impurity source | (空) | active | Impurity production yield and spatial distribution at the wall | corpus`）；GB/T-4960.9 交叉核验：`matched_concept_id==impurity-source` 命中 0 行；IAEA/ITER 交叉核验：对 `impurity source` 归一化命中 0 行（ITER 侧仅有 `Impurities` 条目，即 concepts.tsv:1729 的 `impurities`，非本条）；http(s) URL 类：不适用。附注：`terms/registry/evidence.tsv:886` 记其依据为 `internal:expansion:batch-48`（引语 `Wall impurity production`，`copilot`，2026-03-21）；所属批次为 `concepts.tsv:968`「Batch 48: Core Plasma-Wall Interaction Processes」。
- 定义文本: en 与 zh 逐字见下两行（两处行号：`terms/registry/definitions.tsv:4499`（en）、`terms/registry/definitions.tsv:4500`（zh），两行 `source` 列均为 `corpus`）
- 定义(en) 逐字: definitions.tsv:4499 → `The impurity production yield and spatial distribution at the wall.`
- 定义(zh) 逐字: definitions.tsv:4500 → `杂质源是壁上杂质的产额与空间分布。`
- 适用性推理: ①en 以两项限定语界定该源："production yield"（壁面产生产额）与 "spatial distribution at the wall"（壁上的空间分布），与 notes 同源；在面向等离子体壁的语境中，杂质源正是以"产额 + 空间分布"被量化（同批 `impurity-influx` concepts.tsv:972 记 "Impurity flux entering plasma from wall surfaces" 为其下游量），对象指向明确，刻画成立；保留意见：定义落在可观测量的组合上而非源的位形/机制本身，与 `impurity-influx` 的区分仅靠"at the wall"与"entering plasma"两处限定语支撑，界线偏薄（登记为观察项）。②zh 与 en 等价：impurity→杂质、"at the wall"→壁上、yield→产额、spatial distribution→空间分布；en 的 "production" 在 zh 中由"产额"内在包含，属可接受的概念合并而非漏义，无误译；`aliases.tsv:4136/7425/7426` 已把"杂质来源/杂质源头/杂质起源"按"源≠来源/口语化"判为 forbidden，本定义用"杂质源"与之一致。③族内未见互斥：`impurities`（definitions.tsv:70，ITER："Atoms of unwanted elements in the plasma usually originating from the surrounding walls"）是本概念的属概念（杂质本身），`impurity-transport`（definitions.tsv:4501，"Transport of impurity ions within the confined plasma"）为约束区输运、`impurity-screening`（definitions.tsv:4498，GB/T：硅化/硼化/锂化等壁处理措施）为抑制措施，三者与本概念在"对象/过程/措施"层面可分辨。
判定: PASS

- 证据锚点: concepts.tsv:971

### 样本 6/8 — `presheath`

G4	w1_b_b12..w1_b_b16	presheath	19541eb2f8074830

- 原始语料: [source=corpus，可得] notes 逐字（`terms/registry/concepts.tsv:969`）：`Ion acceleration transition region ahead of the Debye sheath`（该行逐字：`presheath | concept | 预鞘 | presheath | (空) | active | Ion acceleration transition region ahead of the Debye sheath | corpus`）；GB/T-4960.9 交叉核验：`matched_concept_id==presheath` 命中 0 行（该文件与本族相关的条目为 `:231 plasma sheath`→`debye-sheath`，非本概念）；IAEA/ITER 交叉核验：对 `presheath` 归一化命中 0 行；http(s) URL 类：不适用。附注：`terms/registry/evidence.tsv:884` 记其依据为 `internal:expansion:batch-48`（引语 `Ion acceleration ahead of sheath`，`copilot`，2026-03-21）；所属批次为 `concepts.tsv:968`「Batch 48: Core Plasma-Wall Interaction Processes」。
- 定义文本: en 与 zh 逐字见下两行（两处行号：`terms/registry/definitions.tsv:5104`（en）、`terms/registry/definitions.tsv:5105`（zh），两行 `source` 列均为 `corpus`）
- 定义(en) 逐字: definitions.tsv:5104 → `The ion acceleration transition region ahead of the Debye sheath.`
- 定义(zh) 逐字: definitions.tsv:5105 → `预鞘是Debye鞘层之前的离子加速过渡区。`
- 适用性推理: ①en 以 "ion acceleration" 限定过程（离子加速）、以 "transition region ahead of the Debye sheath" 限定位置（位于德拜鞘上游的过渡区），与 notes 同源；族内 `debye-sheath`（definitions.tsv:3935，GB/T 逐字："The transition region formed between an electrically neutral plasma and the solid surface in contact with it..."）给出鞘区定义，本概念以 "ahead of" 明确把自己的区域置于鞘区**之前**，故两处"过渡区"表述不重叠，位置限定语足以区分，刻画成立。②zh 与 en 等价：presheath→预鞘、"the Debye sheath"→"Debye鞘层"、ion acceleration→离子加速、transition region→过渡区；zh 保留拉丁专名 Debye 而未音译，与 `aliases.tsv:3061–3062`（`presheath`/`预鞘` 为 preferred）、`aliases.tsv:3824`（`前鞘` deprecated）、`aliases.tsv:3825`（`预护套` forbidden，误译 sheath）、`aliases.tsv:4573`（`预鞘层` alias）的处置口径一致，无增义、无漏义、无误译。③族内未见冲突：`debye-sheath`（对象为电中性等离子体与固体表面之间的鞘区）、`debye-length`（concepts.tsv:545，特征屏蔽长度量）、`rf-sheath`（concepts.tsv:3358，"Rectified sheath potential formed near antenna structures"，域为等离子体加热）三者与本概念在"区域位置/量纲/成因域"上均可分辨；GB/T 侧只有 `plasma sheath`（→`debye-sheath`）而无 presheath 条目，属覆盖范围差异，不构成缺配对或冲突。
判定: PASS

- 证据锚点: concepts.tsv:969

### 样本 7/8 — `debye-shielding`

G4	w1_b_b12..w1_b_b16	debye-shielding	19e85d55d4830438

- 原始语料: [source=corpus，可得] notes 逐字（`terms/registry/concepts.tsv:990`）：`Debye shielding / screening of electric charges in plasma`（该行逐字：`debye-shielding | concept | 德拜屏蔽 | Debye shielding | (空) | active | Debye shielding / screening of electric charges in plasma | corpus`）；GB/T-4960.9 交叉核验：`matched_concept_id==debye-shielding` 命中 0 行，但该文件 `:223` 载有 `plasma neutrality and debye shield`（status=`new`、无 matched id、zh=`等离子体中性与德拜屏蔽`），其用词与"德拜屏蔽"直接相关却**未**映射到本 cid；IAEA/ITER 交叉核验：对 `Debye shielding` / `debye screening` 归一化命中 0 行；http(s) URL 类：不适用。附注：`terms/registry/evidence.tsv:904` 记其依据为 `internal:expansion:batch-50`（引语 `Debye shielding in plasma`，`copilot`，2026-03-22）；定义全文与 notes 逐字相同（仅多句点），无任何增补。
- 定义文本: en 与 zh 逐字见下两行（两处行号：`terms/registry/definitions.tsv:3936`（en）、`terms/registry/definitions.tsv:3937`（zh），两行 `source` 列均为 `corpus`）
- 定义(en) 逐字: definitions.tsv:3936 → `Debye shielding / screening of electric charges in plasma.`
- 定义(zh) 逐字: definitions.tsv:3937 → `德拜屏蔽是等离子体中对电荷的屏蔽。`
- 适用性推理: ①en **未能刻画该概念**：定义由"专名 + 斜杠同义替换（shielding / screening）+ 作用场域（in plasma）"构成，既未说明屏蔽由可动电荷重排、静电势按 Debye 长度指数衰减这一机制，也未给出特征尺度；作用对象写作 "electric charges" 亦不精确（被屏蔽的是电荷所产生的电场/电位而非电荷本身）。对照同族 `debye-length`（definitions.tsv:1813，en："… screening length over which a plasma neutralizes external charge, in m"）已给出机制与量纲，本条目把定义退化为名词注释（其文本与 `concepts.tsv:990` notes 逐字相同，等于未做定义化加工），故 ① 不成立。②zh 与 en 基本等价："对电荷的屏蔽"↔"shielding of electric charges"、德拜屏蔽↔Debye shielding；但 en 的斜杠同义词 screening 在 zh 中无落项，属轻微漏义，尚未构成误译（zh 首选与 `aliases.tsv:4352` 一致，`aliases.tsv:5136/5137` 已把"德拜遮蔽/德拜防护"判为 forbidden）。③存在族内/库内冲突：GB/T-4960.9 导入的 `plasma-neutrality-and-debye-shield`（concepts.tsv:2716；zh 首选"等离子体中性与德拜屏蔽"，`aliases.tsv:8963`）带有一条 GB/T 定义（definitions.tsv:1217，逐字："偏离电中性会产生很强的电场，使电荷偏离极快得到纠正，故电场作用于一定距离内，此距离外电场被屏蔽"），其内容正是德拜屏蔽机制；同一物理对象在库内出现"GB/T 侧机制性定义"与"本概念侧名词注释"两套不相称表述，且本概念未声明与 `debye-sheath`（德拜鞘）、`debye-length`（德拜长度）的界线，"德拜"三名族内口径未能互相锚定。
- 缺陷/待定原因: en 定义无机制、无特征尺度（未提 Debye 长度），以"shielding / screening"斜杠同义替换自我注释，且作用对象（charges vs 电荷产生的电场/电位）表述不精确；与 GB/T 导入条目 `plasma-neutrality-and-debye-shield`（concepts.tsv:2716 / definitions.tsv:1217）的同物理内容机制性定义不相称，构成本一条目的语义缺陷与库内一致性缺陷。
判定: FAIL

- 证据锚点: concepts.tsv:990

### 样本 8/8 — `pfirsch-schlueter-regime`

G4	w1_b_b12..w1_b_b16	pfirsch-schlueter-regime	1a354ae9ec2eaf0b

- 原始语料: [source=corpus，可得] notes 逐字（`terms/registry/concepts.tsv:909`）：`High collisionality neoclassical transport regime`（该行逐字：`pfirsch-schlueter-regime | concept | Pfirsch-Schlüter区 | Pfirsch-Schlüter regime | (空) | active | High collisionality neoclassical transport regime | corpus`）；GB/T-4960.9 交叉核验：`matched_concept_id==pfirsch-schlueter-regime` 命中 0 行；IAEA/ITER 交叉核验：对 `Pfirsch` 归一化命中 0 行；http(s) URL 类：不适用。附注：`terms/registry/evidence.tsv:831` 记其依据为 `internal:expansion:batch-42`（引语 `High-collisionality regime`，`copilot`，2026-03-19）；所属批次为 `concepts.tsv:906`「Batch 42: Collisional Transport & Neoclassical Physics」。
- 定义文本: en 与 zh 逐字见下两行（两处行号：`terms/registry/definitions.tsv:5009`（en）、`terms/registry/definitions.tsv:5010`（zh），两行 `source` 列均为 `corpus`）
- 定义(en) 逐字: definitions.tsv:5009 → `The high collisionality neoclassical transport regime.`
- 定义(zh) 逐字: definitions.tsv:5010 → `Pfirsch-Schlüter区是高碰撞率的新经典输运区。`
- 适用性推理: ①en 以限定语 "high collisionality" 给出该区在新经典三区（banana / plateau / Pfirsch-Schlüter）中的位置，并以 "neoclassical transport regime" 限定所刻画的输运框架，与 notes 逐词同源，方向正确；但未给出可判定的区界判据（ν*），对照 `banana-regime`（concepts.tsv:912 notes："Low collisionality neoclassical transport regime (nu* << 1)"）与 `plateau-regime`（definitions.tsv:5070，GB/T 给出"有效库仑碰撞频率等于或大于极向渡越频率"及"平均自由程小于连接长度"两项判据）可见本条目属可判据缺失，虽不构成错误，但弱于同族。②zh 与 en 等价："高碰撞率"↔high collisionality、"新经典输运区"↔neoclassical transport regime，并保留拉丁人名 Pfirsch-Schlüter 不音译，与 `aliases.tsv:2930–2932`（`Pfirsch-Schlüter regime`/`Pfirsch-Schlüter区`/`PS regime`）及 `aliases.tsv:4242`（`普费尔施-施吕特区` forbidden：误音译人名）口径一致，无增义、无漏义、无误译。③**存在重复登记与音译处置矛盾**：同库另有 `pfirsch-schulueter-regime`（concepts.tsv:2711，category=`nuclear-fusion`，source=GB/T-4960.9，preferred_en 为 `Pfirsch-Schulueter regime`（人名拼作 Schulueter）、preferred_zh 为 `普费尔施-施吕特尔状态`），其 en 定义（definitions.tsv:2264："High-collisionality regime of neoclassical transport where ν* > 1; current-driven enhancement of classical diffusion."）与 zh 定义（definitions.tsv:1206，GB/T 逐字："托卡马克(2.1.284)等离子体中的一种输运状态，其特征是平均自由程比连接长度短。在此状态中扩散系数为经典值的 q^2 倍…"）与本概念**指同一物理输运区**，构成同物理区的两条重复概念；且 `aliases.tsv:8953` 把"普费尔施-施吕特尔状态"定为其 zh 首选（注释 `imported from GB/T-4960.9`），而 `aliases.tsv:4242` 又把"普费尔施-施吕特区"列为本概念（schlueter 拼写）的 forbidden 音译——同一人名音译在库内一处 preferred、一处 forbidden，两处口径互斥。
- 缺陷/待定原因: 与 GB/T-4960.9 导入条目 `pfirsch-schulueter-regime`（concepts.tsv:2711 / definitions.tsv:2264、1206）重复登记同一新经典输运区，且两条目的人名拼写（Schlüter vs Schulueter）与音译处置（aliases.tsv:8953 preferred vs aliases.tsv:4242 forbidden）互相矛盾；本条目自身还缺少同族普遍给出的 ν* 区界判据。
判定: FAIL

- 证据锚点: concepts.tsv:909

## §3 缺陷/待定台账（行数 = FAIL + UNDECIDABLE = 2 + 0 = 2）

| 编号 | concept_id | 判定 | 原因 |
|---|---|---|---|
| D1 | debye-shielding | FAIL | en 定义无机制/无特征尺度（未提 Debye 长度），以 "shielding / screening" 斜杠同义替换自我注释、作用对象表述不精确；与 GB/T 导入条目 `plasma-neutrality-and-debye-shield`（concepts.tsv:2716、definitions.tsv:1217）的同物理内容机制性定义不相称 |
| D2 | pfirsch-schlueter-regime | FAIL | 与 GB/T-4960.9 导入条目 `pfirsch-schulueter-regime`（concepts.tsv:2711、definitions.tsv:2264/1206）重复登记同一新经典输运区；人名拼写（Schlüter / Schulueter）与音译处置（aliases.tsv:8953 preferred 对比 aliases.tsv:4242 forbidden）互相矛盾；本条目缺少同族普遍给出的 ν* 区界判据 |

## §4 组内统计与 AC 自检（实跑结果）

组内统计：**8 样本 / PASS 6 / FAIL 2 / UNDECIDABLE 0**（FAIL 与 UNDECIDABLE 不计入 PASS；本组不满足 64/64 PASS 的组内条件，M1 不得因本组而勾选）。

| AC 项 | 命令（实跑） | 期望 | 实测 |
|---|---|---|---|
| T-A 样本数 | `grep -c '^### ' docs/reviews/t5184/m1-group-G4.md` | = 8 | 8 |
| T-A 三值单行 | `grep -c '^判定: \(PASS\|FAIL\|UNDECIDABLE\)$' <报告>` | = 8 | 8（PASS 6 / FAIL 2 / UNDECIDABLE 0） |
| T-B 四字段齐全 | `for k in '原始语料:' '定义文本:' '适用性推理:' '证据锚点:'; do grep -c "$k" <报告>; done` | 各 ≥ 8 | 11 / 9 / 9 / 9 |
| T-B 来源缺失行与 UNDECIDABLE 一致 | `grep -c '^原始语料: <来源缺失标记>'` 对比 `grep -c '^判定: UNDECIDABLE$'` | 相等 | 0 == 0 |
| T-B 台账行数 | 末节台账表（四列：编号 / concept_id / 判定 / 原因）的行数 | = FAIL + UNDECIDABLE | 2 = 2 + 0 |
| T-B 证据锚点行数 | `grep -c 'concepts.tsv:[0-9]'` | ≥ 8 | 26 |
| T-B 定义行号行数 | `grep -c 'definitions.tsv:[0-9]'` | ≥ 16 | 36 |
| T-C 术语数据只读 | `git diff --stat -- terms/ artifacts/` | 空 | 空（未运行任何写命令；未 add/commit/checkout/stash/push） |
| 组特化 manifest 对齐 | `awk -v g=G4 '$1==g' docs/reviews/t5184/m1-sample-manifest.tsv \| wc -l` | = 8 | 8；报告 8 个样本的 `concept_id` 与 manifest 该组 8 行**同序逐行相同**（§0 与各样本首行） |

**报告范围与限制声明**：本报告只覆盖 manifest 指定的 G4 8 个样本，是 **抽检**，不构成对 `terms/registry/` 全量（756 条）的语义保证；D1/D2 只陈述可核验的库内事实（条目并存、拼写与音译口径互斥、定义文本可指认缺失），不推断这些条目的写入成因/流程/时间，也不评估上游 GB/T-4960.9 原文本身是否正确。本阶段无数据写权限，D1/D2 的修法建议不在本报告范围内。
