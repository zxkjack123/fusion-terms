# M1 语义抽检报告 — 组 G6（8 样本）

> **计划**：`.github/plans/5184-four-stage-closeout.md` §Phase S4 / Task T4.7（PM #5184 / FUSION-TERMS id240）
> **生成日期**：**2026-11-03**（`date` 实测：`Tue Nov  3 12:15:09 PM CST 2026`）
> **性质**：**只读语义复核**。`terms/registry/*`、`artifacts/*` 全程只读；本报告为唯一新建文件；执行过程中**未运行任何 git 写命令**（不 add / commit / checkout / stash / restore / push），未修改计划文件与其它任何文件。
> **判定口径**：`PASS` = 该概念的 en/zh 定义与仓内原文（`concepts.tsv` notes、`definitions.tsv`）、`evidence.tsv` 依据引语、同族相邻条目及外部 diff 表逐条核验后，未发现可指认的语义缺陷（薄定义、判据省约等弱项按仓内既有校准记为"保留意见"，不判 FAIL）；`FAIL` = 存在可指认的语义缺陷（定义不能刻画对象 / zh 与 en 不等价且有实质影响 / 与同族或同库条目重复登记或边界互斥）；`UNDECIDABLE` = **源语料取不到**（来源缺失，不计入 PASS）。
> **来源可得性规则（照计划 §S4 统一口径）**：`source=corpus` → 依据 = `concepts.tsv` notes 原文 + 行号（可得）；`source=GB/T-4960.9` → 依据 = `gbt4960_9_diff.tsv` 的 `matched_concept_id` 命中行；`source=IAEA/ITER` → 依据 = 对应 `*_raw.tsv` 归一化命中行；`source=http(s)://…` → 依据 = URL + 取回日期 + 片段。
> **路径更正记录（如实）**：任务给定依据路径 `.github/plans/t4973-batches/`（称"不存在，以实存文件为准"）实测**目录存在**（`ls -1 | wc -l` → **153** 个条目，全部为 `w*.ids` / `category-map-*.tsv` / `*.md` 批次辅助件），但**该目录内不含 `gbt4960_9_diff.tsv`**（`ls .github/plans/t4973-batches/gbt4960_9_diff.tsv` → `No such file or directory`）。本报告据此以仓内实存文件 `artifacts/terminology_sources/gbt4960_9_diff.tsv`（**562 行**，列 `#term / status / matched_concept_id / term_id / zh / abbr / definition`）为准；此即为本次路径更正记录（既不声称计划路径不存在，也不据计划路径取依据）。
> **AC 计数正则声明**：本组 8 个概念的 `source` 字段**全部为 `corpus`**，依据一律取 `concepts.tsv` notes 逐字 + 行号，因此本组**不存在来源缺失样本**；按组通用 AC 第 4 条（"来源缺失标记行数须等于 `UNDECIDABLE` 行数"），本组 `UNDECIDABLE` 数 = 0，故全文不使用该来源缺失标记，以免与 AC 计数正则互相污染（同理，URL 类外部内容一律不引用、不假装取回，见 §1）。

## §0 组样本清单（与 `m1-sample-manifest.tsv` 的 G6 8 行逐行相同）

抽取口径（manifest 头与 README 声明）：组内 id 去重排序后取 `sha256(id)[:16]` 升序前 8。分组口径：`w1_a_b01..b04` → `w1_b_b01..b34` → `w1_c_b01` 连续编号，连续 5 批为 1 组。G6 = `w1_b_b22..w1_b_b26`，组内 ids = 100。

| 序 | group | batch_scope | concept_id | sha256_16 |
|---|---|---|---|---|
| 1 | G6 | w1_b_b22..w1_b_b26 | forced-convection | 037f2df558bb1583 |
| 2 | G6 | w1_b_b22..w1_b_b26 | working-fluid | 0392183b533ddc1b |
| 3 | G6 | w1_b_b22..w1_b_b26 | gasket | 0835a472d8b309f5 |
| 4 | G6 | w1_b_b22..w1_b_b26 | plasma-termination | 0a9eebf8007fc60b |
| 5 | G6 | w1_b_b22..w1_b_b26 | dislocation | 0d5322c22c4b6f6e |
| 6 | G6 | w1_b_b22..w1_b_b26 | rupture-disc | 0e71e187c857a6f2 |
| 7 | G6 | w1_b_b22..w1_b_b26 | grain-boundary | 0eba2d678a288455 |
| 8 | G6 | w1_b_b22..w1_b_b26 | data-pipeline | 0f9c7c732faedd3a |

`sha256_16` 复算核验：`python3 -c "import hashlib;[print(c, hashlib.sha256(c.encode()).hexdigest()[:16]) for c in [...]]"` 对上述 8 个 cid 逐一复算，与 manifest 的 `sha256_16` 列**全部一致**。manifest 末行的 `# group_sample_sha256 G6 c9a9c9fe…` 未能用"cid 换行拼接 / 含 sha16 拼接 / 排序后拼接"等候选口径复现（实得 `adbdc212…` 等），本报告**不据此做任何判定**，仅记录该复现未成功这一事实。

## §1 依据可得性与交叉核验执行记录（口径与命令）

- **组内依据类分布**：`awk -F'\t' '$1=="G6"' docs/reviews/t5184/m1-sample-manifest.tsv` 取 8 个 cid → `grep -nP "^<cid>\t" terms/registry/concepts.tsv` 第 8 列 → `corpus` × 8。
- **原始语料取法（每样本）**：`grep -nP "^<cid>\t" terms/registry/concepts.tsv` → 该行 notes（第 7 列）逐字 + 行号。
- **定义文本取法（每样本）**：`grep -nP "^<cid>\t(en|zh)\t" terms/registry/definitions.tsv` → en、zh 两行逐字 + 行号；本组每概念各 1 条 en、1 条 zh（共 16 行，全组 `source` 列均为 `corpus`）。
- **GB/T-4960.9 交叉核验**（实存文件，见头部路径更正记录）：`awk -F'\t' -v c="<cid>" '$3==c' artifacts/terminology_sources/gbt4960_9_diff.tsv` 对 8 个 cid 的命中数**全部为 0**；按英文 term 名（`^(gasket|dislocation|grain boundary|working fluid|data pipeline|forced convection|rupture disc|plasma termination)\t`）检索亦**全部为 0**。与本组相关的**旁证**命中 1 处：`:411 plasma shutdown exists plasma-shutdown 2.2.104 等离子体熄灭 在等离子体燃烧末期，等离子体能量衰减为零的过程。`（同文件 `:411` 亦见 `gbt4960_9_terms.tsv`）——GB/T 侧该词条已映射到**另一 cid**（`plasma-shutdown`），未映射到本组样本 `plasma-termination`。此外 `:441 target plate` 的定义文中出现"终止"字样（`磁偏滤器的等离子体排气通道终止的地方。`），属无关语境。
- **IAEA / ITER 交叉核验**：对 8 个概念的英文形式在 `iter_glossary_raw.tsv`（143 行）与 `iaea_safety_glossary_raw.tsv`（877 行）做大小写不敏感归一化检索，**本组 8 个 cid 均 0 命中**；仅两处旁证：`iter_glossary_raw.tsv:98` 载 `Plasma Shutdown` = `The orderly process of extinguishing the plasma at the end of a plasma burn pulse, involving reduction of the plasma thermal energy, and reduction of plasma current to zero.`（`iter_glossary_diff.tsv:98` 该行 `status=new`、`matched_concept_id` **为空**）；`iaea_safety_glossary_raw.tsv` 侧 "dislocation(s)" 仅出现在 `iaea_safety_glossary_diff.tsv:347`（`geological fault` 定义文中的 `deformations and/or dislocations`），属地质位移义，与材料学"位错"无关。
- **http(s) URL 类**：本组 8 个概念的 `source` 均非 URL，该类按 source 分派不适用。需如实说明：`evidence.tsv` 中 `grain-boundary:1212`、`dislocation:1213`、`forced-convection:1237` 三行以 `https://en.wikipedia.org/wiki/...` 为**上游依据 URL**，本环境无网络取回手段，故**未取回、未引用其任何外部原文**；凡涉及外部权威才能定论的判断，本报告一律不作为 `PASS` 依据，亦不作 `FAIL` 依据。
- **独立依据强度注记**：8 个概念的 `evidence.tsv` 依据行分两类——(a) 外部百科 URL：`grain-boundary:1212`、`dislocation:1213`、`forced-convection:1237`（均 `added_at 2026-04-04`，`quote` 列空）；(b) 内部流程依据：`working-fluid:1244` = `internal:fusion-terms:domain-expansion`（引语 `Thermodynamic concept`）、`data-pipeline:1306` = `internal:fusion-terms:domain-expansion`（引语 `Data engineering concept`）、`plasma-termination:1406` = `internal:registry-gap-review:batch6`（引语 `Discharge termination phase`，`copilot`）、`gasket:1494` 与 `rupture-disc:1500` = `internal:registry-gap-review:batch9`（`copilot`，引语分别为 `Sealing element between flanges or joints to prevent fluid leakage` 与 `Non-reclosing pressure relief device that bursts at set pressure differential`）。即：本组 notes/定义出自仓内扩展与缺口复核流程，除 3 条百科 URL（未取回）外**无外部权威可比对**；这限制了对 en 定义做"外部权威一致性"判断的强度，凡判定均基于**仓内可核验事实**（定义文本、同族条目文本、外部 diff 表的映射事实）。
- **所属批次（`concepts.tsv` 内批次头，用于族内定位）**：`grain-boundary`(1315)/`dislocation`(1316) ∈ **Batch 61 Materials Science & Mechanics**（头 `concepts.tsv:1300`）；`forced-convection`(1341)/`working-fluid`(1348) ∈ **Batch 62 Thermal-Hydraulics**（头 `1332`）；`data-pipeline`(1412) ∈ **Batch 64 Data Formats & Visualization**（头 `1389`）；`plasma-termination`(1536) ∈ **Batch 79 plasma operation phases + ITER PBS systems**（头 `1531`）；`gasket`(1639)/`rupture-disc`(1645) ∈ **Batch 88 generic mechanical components / piping / valves**（头 `1636`）。

## §2 逐样本复核（8 样本）

### 样本 1/8 — `forced-convection`

G6	w1_b_b22..w1_b_b26	forced-convection	037f2df558bb1583

- 原始语料: [source=corpus，可得] notes 逐字（`terms/registry/concepts.tsv:1341`）：`Pump/fan-driven flow`（该行逐字：`forced-convection | concept | 强制对流 | forced convection | (空) | active | Pump/fan-driven flow | corpus`）；GB/T-4960.9 交叉核验：`matched_concept_id==forced-convection` 命中 0 行，英文 term `forced convection` 亦 0 行；IAEA/ITER 交叉核验：对 `forced convection` 归一化命中 0 行；http(s) URL 类：不适用（source≠URL）。附注：`terms/registry/evidence.tsv:1237` 记其依据为 `https://en.wikipedia.org/wiki/Forced_convection`（`quote` 列空，`added_at 2026-04-04`，无取回记录）；该 URL 本环境未取回、未引用其原文（见 §1）。所属批次 `concepts.tsv:1332`「Batch 62: Thermal-Hydraulics」，同批含 `natural-convection`(1340)、`turbulent-flow`(1346)、`laminar-flow`(1347)。
- 定义文本: en 与 zh 逐字见下两行（两处行号：`terms/registry/definitions.tsv:4293`（en）、`terms/registry/definitions.tsv:4294`（zh），两行 `source` 列均为 `corpus`）
- 定义(en) 逐字: definitions.tsv:4293 → `Fluid flow that is driven by a pump or fan.`
- 定义(zh) 逐字: definitions.tsv:4294 → `强制对流是由泵或风机驱动的流体流动。`
- 适用性推理: ①en 以限定语 `driven by a pump or fan`（外力驱动来源）给出与自然对流相区分的判据，与 notes 的 `Pump/fan-driven flow` 逐词同源，能唯一定位"外驱"这一族内分轴，故定义可用；但范畴词写作 `Fluid flow`（流动），而 `forced convection` 的对象范畴是传热/输运机制（对流换热带走壁面热量），定义**未出现任何传热限定语**，属范畴滑移——按仓内既有校准（同族 `natural-convection`（`concepts.tsv:1340` notes `Buoyancy-driven flow`；`definitions.tsv:4830` `Fluid flow that is driven by buoyancy forces.`）采取完全相同的"以驱动机制定义流动"写法，族内口径自洽、且该写法与 notes 严格同源），记为**保留意见**而不判缺陷。②zh 与 en 等价：`由泵或风机驱动`↔`driven by a pump or fan`、`流体流动`↔`fluid flow`，无增义、无漏义、无误译；zh 首选与 `aliases.tsv:6029`（`强制对流 / forced-convection / zh / preferred`）一致，`grep -n "^forced-convection" terms/registry/aliases.tsv` 仅此 1 条 zh 记录，别名层无竞争。③族内未见互斥或重复登记：与 `natural-convection`（1340）靠驱动机制可分辨；需登记的观察项是**正交轴重叠**——因两条例目均以"流动"为范畴，本条目与同批 `turbulent-flow`（1346 notes `High-Re chaotic flow`）、`laminar-flow`（1347 notes `Low-Re ordered flow`）、`single-phase-flow`（1344 notes `Single-phase fluid flow`）的字面描述可被同一物理情形（泵驱动的单相湍流）同时满足，边界须由读者自行用"传热模式 vs 流态"补齐；建议后续在定义中补出"对流换热"限定语，此观察不改变本条判定。
判定: PASS

- 证据锚点: concepts.tsv:1341

### 样本 2/8 — `working-fluid`

G6	w1_b_b22..w1_b_b26	working-fluid	0392183b533ddc1b

- 原始语料: [source=corpus，可得] notes 逐字（`terms/registry/concepts.tsv:1348`）：`Fluid in thermodynamic cycle`（该行逐字：`working-fluid | concept | 工质 | working fluid | (空) | active | Fluid in thermodynamic cycle | corpus`）；GB/T-4960.9 交叉核验：`matched_concept_id==working-fluid` 命中 0 行，英文 term `working fluid` 亦 0 行；IAEA/ITER 交叉核验：对 `working fluid` 归一化命中 0 行；http(s) URL 类：不适用。附注：`terms/registry/evidence.tsv:1244` 记其依据为 `internal:fusion-terms:domain-expansion`（引语 `Thermodynamic concept`，`added_at 2026-04-04`）；所属批次 `concepts.tsv:1332`「Batch 62: Thermal-Hydraulics」。
- 定义文本: en 与 zh 逐字见下两行（两处行号：`terms/registry/definitions.tsv:5826`（en）、`terms/registry/definitions.tsv:5827`（zh），两行 `source` 列均为 `corpus`）
- 定义(en) 逐字: definitions.tsv:5826 → `The fluid that carries energy through a thermodynamic cycle.`
- 定义(zh) 逐字: definitions.tsv:5827 → `工质是在热力循环中输运能量的流体。`
- 适用性推理: ①en 以功能判据 `carries energy`（载能）+ 场域限定 `through a thermodynamic cycle`（热力循环）刻画对象，把"工质"与"仅用于移热的流体"区分开，较 notes 的压缩式 `Fluid in thermodynamic cycle` 更有信息量且方向一致，准确刻画该概念。②zh 与 en 等价：`输运能量`↔`carries energy`、`热力循环`↔`thermodynamic cycle`、`流体`↔`the fluid`，无增义、无漏义、无误译；zh 首选与 `aliases.tsv:6043`（`工质 / working-fluid / zh / preferred`）一致。③族内无重复登记，但存在**术语重叠观察**：同库 `coolant`（`concepts.tsv:2911`，notes `Generic coolant working fluid concept`；`definitions.tsv:3857` 引外部词典 `A liquid that is used for cooling, such as an engine or a nuclear reactor.`）与本条职能不同（移热 vs 循环载能）可分辨；然而同族 `helium-coolant`（`concepts.tsv:1426` notes `Helium as blanket/coolant working fluid`）与 `water-coolant`（`concepts.tsv:1457` notes `包层/偏滤器冷却工质（与 helium-coolant 对应）`）在 notes 中直接用"工质"指称冷却剂，说明库内对"工质 / 冷却剂"的界线尚未在本条目定义中声明；这是可登记的边界建议（WCLL/DCLL 中两者可为同一流体），不构成冲突或重复登记。
判定: PASS

- 证据锚点: concepts.tsv:1348

### 样本 3/8 — `gasket`

G6	w1_b_b22..w1_b_b26	gasket	0835a472d8b309f5

- 原始语料: [source=corpus，可得] notes 逐字（`terms/registry/concepts.tsv:1639`）：`法兰或接头间防止流体泄漏的密封元件`（该行逐字：`gasket | concept | 密封垫片 | gasket | (空) | active | 法兰或接头间防止流体泄漏的密封元件 | corpus`）；GB/T-4960.9 交叉核验：`matched_concept_id==gasket` 命中 0 行，英文 term `gasket` 亦 0 行；IAEA/ITER 交叉核验：对 `gasket` 归一化命中 0 行；http(s) URL 类：不适用。附注：`terms/registry/evidence.tsv:1494` 记其依据为 `internal:registry-gap-review:batch9`（引语 `Sealing element between flanges or joints to prevent fluid leakage`，`copilot`，`added_at 2026-04-04`）；所属批次 `concepts.tsv:1636`「Batch 88: generic mechanical components / piping / valves」。
- 定义文本: en 与 zh 逐字见下两行（两处行号：`terms/registry/definitions.tsv:4351`（en）、`terms/registry/definitions.tsv:4352`（zh），两行 `source` 列均为 `corpus`）
- 定义(en) 逐字: definitions.tsv:4351 → `A sealing element between flanges or joints that prevents fluid leakage.`
- 定义(zh) 逐字: definitions.tsv:4352 → `密封垫片是法兰或接头间防止流体泄漏的密封元件。`
- 适用性推理: ①en 以安装位置限定 `between flanges or joints`（法兰或接头之间）+ 功能限定 `prevents fluid leakage`（阻止流体泄漏）+ 范畴词 `sealing element`（密封元件）刻画静密封件，与 notes 及本条依据引语（`Sealing element between flanges or joints to prevent fluid leakage`）逐词同源，准确刻画该概念；未区分软垫片/金属缠绕垫等型式，属同批条目普遍的粒度省约。②zh 与 en 等价：`密封垫片`↔`sealing element`、`法兰或接头间`↔`between flanges or joints`、`防止流体泄漏`↔`prevents fluid leakage`，无增义、无漏义、无误译；zh 首选与 `aliases.tsv:6944`（`密封垫片 / gasket / zh / preferred`）一致。③族内无冲突、无重复登记：`flange`（`concepts.tsv:1638`，连接承载件）、`bellows`（1637，柔性补偿件）、`lip-seal`（`concepts.tsv:2809`，source=GB/T-4960.9，动态唇形密封，与本条静密封分属不同密封型式）、`sealing`（`concepts.tsv:1104`，notes `Generic academic glue word for translation`，是过程词非元件）均可与本条分辨；同批 `relief-valve`/`check-valve`/`expansion-joint` 等亦无指称重叠。
判定: PASS

- 证据锚点: concepts.tsv:1639

### 样本 4/8 — `plasma-termination`

G6	w1_b_b22..w1_b_b26	plasma-termination	0a9eebf8007fc60b

- 原始语料: [source=corpus，可得] notes 逐字（`terms/registry/concepts.tsv:1536`）：`放电结束阶段`（该行逐字：`plasma-termination | concept | 等离子体终止 | Plasma Termination | (空) | active | 放电结束阶段 | corpus`）；GB/T-4960.9 交叉核验：`matched_concept_id==plasma-termination` 命中 0 行，英文 term `plasma termination` 亦 0 行；但该文件 `:411` 载 `plasma shutdown | exists | plasma-shutdown | 2.2.104 | 等离子体熄灭 | | 在等离子体燃烧末期，等离子体能量衰减为零的过程。`（`gbt4960_9_terms.tsv:411` 同），即 GB/T 侧该相位词条已映射到**另一个 cid**（`plasma-shutdown`，`concepts.tsv:1744`），未映射到本条；IAEA/ITER 交叉核验：本条英文形式 0 命中，而 `iter_glossary_raw.tsv:98` 载 `Plasma Shutdown` = `The orderly process of extinguishing the plasma at the end of a plasma burn pulse, involving reduction of the plasma thermal energy, and reduction of plasma current to zero.`（`iter_glossary_diff.tsv:98` 该行 `status=new`、`matched_concept_id` 为空）；http(s) URL 类：不适用。附注：`terms/registry/evidence.tsv:1406` 记其依据为 `internal:registry-gap-review:batch6`（引语 `Discharge termination phase`，`copilot`，`added_at 2026-04-04`）；所属批次 `concepts.tsv:1531`「Batch 79: plasma operation phases + ITER PBS systems」。
- 定义文本: en 与 zh 逐字见下两行（两处行号：`terms/registry/definitions.tsv:5068`（en）、`terms/registry/definitions.tsv:5069`（zh），两行 `source` 列均为 `corpus`）
- 定义(en) 逐字: definitions.tsv:5068 → `The phase at the end of a plasma discharge.`
- 定义(zh) 逐字: definitions.tsv:5069 → `等离子体终止是放电结束的阶段。`
- 适用性推理: ①en 仅给出位置标签 `The phase at the end of a plasma discharge`，**无任何可判定限定语**（未涉电流/热能的衰减路径、未涉触发条件、未区分与降流的先后），与 notes `放电结束阶段` 同源但同属"薄定义"；对照同一现象在库内已有的权威口径（`iter_glossary_raw.tsv:98` 的 `Plasma Shutdown` 写明 `involving reduction of the plasma thermal energy, and reduction of plasma current to zero`；`gbt4960_9_diff.tsv:411` 的 GB/T 2.2.104 写明"在等离子体燃烧末期，等离子体能量衰减为零的过程"），本条目既未采用这些限定语、也未声明与它们的对应关系，定义的可判定性弱于库内同物条目。②zh 与 en 等价：`放电结束的阶段`↔`the phase at the end of a plasma discharge`，无增义、无漏义、无误译；zh 首选与 `aliases.tsv:6546`（`等离子体终止 / plasma-termination / zh / preferred`）一致，且 `aliases.tsv:7704–7706` 已把 `等离子体终端`（AI 误译 termination）、`血浆终止`（AI 误译 plasma）、`等离子体结束` 判 forbidden，命名处置本身自洽（注：`aliases.tsv:6547` 把 cid 自身标为 `alias / hyphenated form`，属别名表填写冗余，非缺陷）。③**存在重复登记与边界互斥**：(a) 同库 `plasma-shutdown`（`concepts.tsv:1744`，`preferred_zh=等离子体熄灭`，source=ITER-glossary，notes 为空；`definitions.tsv:98` en 为 ITER 原文、`definitions.tsv:1402` zh 料出自 GB/T-4960.9）与本条指**同一放电终止过程**，两者并列为独立概念、zh 名分歧（终止 vs 熄灭），库内未声明界线，而两条外部 diff 表分别把 GB/T 2.2.104 映射给 `plasma-shutdown`（`gbt4960_9_diff.tsv:411`）、把 ITER `Plasma Shutdown` 留给 `plasma-shutdown`（`iter_glossary_diff.tsv:98`，`status=new`），本条在该两表中**均无匹配**，即本条的独立存在缺乏外部锚点；(b) 同族 `plasma-ramp-down`（`concepts.tsv:781`；`definitions.tsv:5054` en `The ramp-down phase of plasma current termination.`）把自身声明为"plasma current **termination** 的下降阶段"，与本条名实正相冲——托卡马克相位序通常为 `plasma-ramp-up`(780)→`flat-top`(1534)→`burn-phase`(1535)→降流→终止（同族 `plasma-start-up`(3368)、`current-quench`(1488) 亦在库），降流应先于终止，而该条却把降流置于"termination"之内；三条例目（终止 1536 / 熄灭 1744 / 降流 781）挤在同一"放电结束"相位槽内且互相矛盾，读者无法据定义判定某放电工况应标 终止、熄灭 还是 降流。缺陷落在 ①③。
- 缺陷/待定原因: 与同库 `plasma-shutdown`（`concepts.tsv:1744`，zh `等离子体熄灭`，ITER+GB/T 双源）重复登记同一放电终止过程且 zh 名分歧、未声明界线，本条在 `iter_glossary_diff.tsv` 与 `gbt4960_9_diff.tsv` 中均无映射（相对 `gbt4960_9_diff.tsv:411` 已映射到 `plasma-shutdown`）；与 `plasma-ramp-down`（`concepts.tsv:781` / `definitions.tsv:5054`）边界互斥（后者把自身写成"电流终止的下降阶段"，相位序被颠倒）；自身 en/zh 仅 `The phase at the end of a plasma discharge` / `放电结束的阶段` 一句位置标签，无任何可判定限定语，亦未采用库内已载的 ITER/GB-T 限定语。
判定: FAIL

- 证据锚点: concepts.tsv:1536

### 样本 5/8 — `dislocation`

G6	w1_b_b22..w1_b_b26	dislocation	0d5322c22c4b6f6e

- 原始语料: [source=corpus，可得] notes 逐字（`terms/registry/concepts.tsv:1316`）：`Crystal lattice line defect`（该行逐字：`dislocation | concept | 位错 | dislocation | (空) | active | Crystal lattice line defect | corpus`）；GB/T-4960.9 交叉核验：`matched_concept_id==dislocation` 命中 0 行，英文 term `dislocation` 亦 0 行；IAEA/ITER 交叉核验：对 `dislocation` 归一化命中 0 行（`iaea_safety_glossary_diff.tsv:347` 的 `deformations and/or dislocations` 为地质位移义，见 §1，非材料学义）；http(s) URL 类：不适用。附注：`terms/registry/evidence.tsv:1213` 记其依据为 `https://en.wikipedia.org/wiki/Dislocation`（`quote` 列空，`added_at 2026-04-04`，未取回）；所属批次 `concepts.tsv:1300`「Batch 61: Materials Science & Mechanics」（同批相邻 1315 `grain-boundary`、1314 `microstructure`）。
- 定义文本: en 与 zh 逐字见下两行（两处行号：`terms/registry/definitions.tsv:4025`（en）、`terms/registry/definitions.tsv:4026`（zh），两行 `source` 列均为 `corpus`）
- 定义(en) 逐字: definitions.tsv:4025 → `A line defect in the crystal lattice of a material.`
- 定义(zh) 逐字: definitions.tsv:4026 → `位错是材料晶格中的线缺陷。`
- 适用性推理: ①en 以缺陷几何限定语 `line defect`（一维线状缺陷）+ 场域限定 `in the crystal lattice of a material`（材料晶格内）刻画对象，与 notes 的 `Crystal lattice line defect` 逐词同源且未越界；未给 Burgers 矢量/刃型-螺型分类等定量判据，属该批 notes 一行式粒度的省约（同批 `grain-boundary`、`microstructure` 同粒度），不构成缺陷。②zh 与 en 等价：`位错`↔`dislocation`、`材料晶格中的线缺陷`↔`a line defect in the crystal lattice of a material`，无增义、无漏义、无误译；zh 首选与 `aliases.tsv:5970`（`位错 / dislocation / zh / preferred`）一致。③族内无冲突、无重复登记：`grain-boundary`（1315，面状界面缺陷）、`microstructure`（1314，组织尺度）、`recrystallization`（878，形核长大过程）、`hydrogen-trapping`（`concepts.tsv:1681`，其 notes 把 `dislocations` 列为捕获位点之一）分属不同层级与范畴，均不构成本条的重复登记；本条与相邻 `grain-boundary` 一为线缺陷、一为面缺陷，可分辨。
判定: PASS

- 证据锚点: concepts.tsv:1316

### 样本 6/8 — `rupture-disc`

G6	w1_b_b22..w1_b_b26	rupture-disc	0e71e187c857a6f2

- 原始语料: [source=corpus，可得] notes 逐字（`terms/registry/concepts.tsv:1645`）：`超压时主动破裂泄放压力的非重闭式安全装置`（该行逐字：`rupture-disc | concept | 爆破片 | rupture disc | (空) | active | 超压时主动破裂泄放压力的非重闭式安全装置 | corpus`）；GB/T-4960.9 交叉核验：`matched_concept_id==rupture-disc` 命中 0 行，英文 term `rupture disc` 亦 0 行；IAEA/ITER 交叉核验：对 `rupture disc` 归一化命中 0 行；http(s) URL 类：不适用。附注：`terms/registry/evidence.tsv:1500` 记其依据为 `internal:registry-gap-review:batch9`（引语 `Non-reclosing pressure relief device that bursts at set pressure differential`，`copilot`，`added_at 2026-04-04`）；所属批次 `concepts.tsv:1636`「Batch 88: generic mechanical components / piping / valves」，同批相邻 `relief-valve`（1644）、`check-valve`（1646）、`isolation-valve`（1647）。
- 定义文本: en 与 zh 逐字见下两行（两处行号：`terms/registry/definitions.tsv:5351`（en）、`terms/registry/definitions.tsv:5352`（zh），两行 `source` 列均为 `corpus`）
- 定义(en) 逐字: definitions.tsv:5351 → `A non-reclosing safety device that ruptures on overpressure to relieve pressure.`
- 定义(zh) 逐字: definitions.tsv:5352 → `爆破片是超压时主动破裂泄放压力的非重闭式安全装置。`
- 适用性推理: ①en 保留了 `non-reclosing`（非重闭）与 `ruptures on overpressure to relieve pressure`（超压破裂泄压）两项要义，方向正确；但相对**本条自己的依据引语**（`evidence.tsv:1500`：`…that bursts at **set pressure differential**`）漏掉了动作定值限定语（按设定压差爆破），而该限定语正是爆破片与 `relief-valve` 在动作定值上的分界，属**实质漏义**（对照同批 `relief-valve` 的 en（`definitions.tsv:5292`）亦未给定值，属同批共性省约，但本条依据引语本已提供该限定语而定义未采纳）。②zh 与 en **不等价**：zh 含 `主动破裂`，而 en 及本条依据引语均**无对应词**（en 侧为 `ruptures on overpressure`，无 active/automatic 之类修饰）；且库内 `主动` 已固定用于 `actively-` 语义——`concepts.tsv:894` `actively-cooled-component` 的 zh 首选即 `主动冷却部件`——故 zh `主动破裂` 会把自破式（无外部驱动、纯被动触发）的泄压装置读成"主动"动作装置，与核安全语境"主动/被动"（active/passive）的装置分类相抵触；横向对照同批同功能条目 `relief-valve`（`concepts.tsv:1644`；`definitions.tsv:5293` zh `安全阀是超压时**自动**开启泄放流体以保护设备的压力安全装置。`，其 en（5292）有 `opens **automatically**` 对应），同一"由压力自行触发"的被动动作在 Batch 88 内被一处写作 `自动`、一处写作 `主动`，限定语用法不一致。注：`主动` 一词源自 `concepts.tsv:1645` 的 notes 原文，而 notes 与 `evidence.tsv:1500` 引语不一致，故该缺陷同时是**条目内部依据不一致**（notes 相对 evidence 引语增义、en 相对 evidence 引语漏义）。③族内无重复登记：本条与 `relief-valve`（1644）以重闭/非重闭相区分，边界本身可辨；缺陷落在 ①②。
- 缺陷/待定原因: zh 定义含 `主动破裂`，en 及本条依据引语（`evidence.tsv:1500`）均无对应词，且与库内 `主动`=actively- 的既有用法（`concepts.tsv:894` `actively-cooled-component` / `主动冷却部件`）及同批 `relief-valve` 的 `自动开启`（`definitions.tsv:5293`）用词互斥，构成 zh/en 不等价与条目内依据不一致；反向 en 相对依据引语漏掉动作定值限定语 `at set pressure differential`（设定压差）。
判定: FAIL

- 证据锚点: concepts.tsv:1645

### 样本 7/8 — `grain-boundary`

G6	w1_b_b22..w1_b_b26	grain-boundary	0eba2d678a288455

- 原始语料: [source=corpus，可得] notes 逐字（`terms/registry/concepts.tsv:1315`）：`Interface between crystalline grains`（该行逐字：`grain-boundary | concept | 晶界 | grain boundary | (空) | active | Interface between crystalline grains | corpus`）；GB/T-4960.9 交叉核验：`matched_concept_id==grain-boundary` 命中 0 行，英文 term `grain boundary` 亦 0 行；IAEA/ITER 交叉核验：对 `grain boundary` 归一化命中 0 行；http(s) URL 类：不适用。附注：`terms/registry/evidence.tsv:1212` 记其依据为 `https://en.wikipedia.org/wiki/Grain_boundary`（`quote` 列空，`added_at 2026-04-04`，未取回）；所属批次 `concepts.tsv:1300`「Batch 61: Materials Science & Mechanics」（同批相邻 1314 `microstructure`、1316 `dislocation`）。
- 定义文本: en 与 zh 逐字见下两行（两处行号：`terms/registry/definitions.tsv:4369`（en）、`terms/registry/definitions.tsv:4370`（zh），两行 `source` 列均为 `corpus`）
- 定义(en) 逐字: definitions.tsv:4369 → `The interface between two crystalline grains.`
- 定义(zh) 逐字: definitions.tsv:4370 → `晶界是两个晶粒之间的界面。`
- 适用性推理: ①en 以范畴词 `interface`（界面）+ 对象限定 `between two crystalline grains`（两个晶粒之间）给出结构判据，与 notes 的 `Interface between crystalline grains` 逐词同源，准确刻画该概念；未区分小角/大角/孪晶界与界面厚度量级，属该批一行式 notes 粒度的省约。②zh 与 en 等价：`两个晶粒之间的界面`↔`the interface between two crystalline grains`，无增义、无漏义、无误译；zh 首选与 `aliases.tsv:5968`（`晶界 / grain-boundary / zh / preferred`）一致，且 `aliases.tsv:7390/7391` 已把 `晶粒边界`/`晶粒界` 判 `deprecated`、`aliases.tsv:7392` 把 `晶间边界` 判 `forbidden`（注明"误译 grain boundary(晶界≠晶间边界)"），命名处置与本定义口径自洽。③族内无冲突、无重复登记：`microstructure`（1314，组织尺度对象）、`dislocation`（1316，线缺陷）、`recrystallization`（878，晶粒形核长大过程）、`hydrogen-trapping`（1681，缺陷处氢滞留）均不在同一指称层级；本条与 `dislocation` 同批相邻但一为面缺陷、一为线缺陷，可分辨。
判定: PASS

- 证据锚点: concepts.tsv:1315

### 样本 8/8 — `data-pipeline`

G6	w1_b_b22..w1_b_b26	data-pipeline	0f9c7c732faedd3a

- 原始语料: [source=corpus，可得] notes 逐字（`terms/registry/concepts.tsv:1412`）：`Automated data processing workflow`（该行逐字：`data-pipeline | concept | 数据管线 | data pipeline | (空) | active | Automated data processing workflow | corpus`）；GB/T-4960.9 交叉核验：`matched_concept_id==data-pipeline` 命中 0 行，英文 term `data pipeline` 亦 0 行；IAEA/ITER 交叉核验：对 `data pipeline` 归一化命中 0 行；http(s) URL 类：不适用。附注：`terms/registry/evidence.tsv:1306` 记其依据为 `internal:fusion-terms:domain-expansion`（引语 `Data engineering concept`，`added_at 2026-04-04`）；所属批次 `concepts.tsv:1389`「Batch 64: Data Formats & Visualization」（同批 `gnuplot`(1410)、`visit`(1411)、`scatter-plot`(1413)、`histogram`(1414)）。
- 定义文本: en 与 zh 逐字见下两行（两处行号：`terms/registry/definitions.tsv:3930`（en）、`terms/registry/definitions.tsv:3931`（zh），两行 `source` 列均为 `corpus`）
- 定义(en) 逐字: definitions.tsv:3930 → `An automated workflow for data processing.`
- 定义(zh) 逐字: definitions.tsv:3931 → `数据管线是自动化的数据处理工作流。`
- 适用性推理: ①en 以范畴词 `workflow`（工作流）+ 限定语 `automated`（自动化）+ 功能 `for data processing`（用于数据处理）三项刻画对象，与 notes 的 `Automated data processing workflow` 逐词同源，准确且可定位；未界定与 ETL 工具链/工作流引擎的界线，属同批（可视化与数据格式批次）普遍粒度，不构成缺陷。②zh 与 en 等价：`数据管线`↔`data pipeline`、`自动化的数据处理工作流`↔`an automated workflow for data processing`，无增义、无漏义、无误译；zh 首选与 `aliases.tsv:6173`（`数据管线 / data-pipeline / zh / preferred`）一致。③族内**存在重叠观察但不构成重复登记**：`workflow-automation`（`concepts.tsv:937`，category=`method`；`definitions.tsv:2727` en `Orchestration of multi-step computational tasks via scripts or pipeline frameworks (Snakemake, Nextflow).`、`definitions.tsv:2728` zh 对应句）与本条同用"自动化管线/工作流"措辞，但被自动化对象不同（多步**计算任务**的编排 vs **数据处理**工作流）、category 不同（method vs concept），可由"被自动化对象"分辨；本条与同批 `gnuplot`/`visit`（工具）、`scatter-plot`/`histogram`（图表对象）亦无指称重叠。建议后续在任一条目中显式声明二者界线（本条与 `workflow-automation` 的定义句在字面上高度相似，是本组唯一需要登记的边界观察项），不影响本条判定。
判定: PASS

- 证据锚点: concepts.tsv:1412

## §3 缺陷/待定台账（行数 = FAIL + UNDECIDABLE = 2 + 0 = 2）

| 编号 | concept_id | 判定 | 原因 |
|---|---|---|---|
| D1 | plasma-termination | FAIL | 与同库 `plasma-shutdown`（concepts.tsv:1744，zh `等离子体熄灭`，ITER+GB/T 双源）重复登记同一放电终止过程、zh 名分歧且未声明界线，本条在 `iter_glossary_diff.tsv:98` 与 `gbt4960_9_diff.tsv:411` 中均无匹配（GB/T 2.2.104 已映射到 `plasma-shutdown`）；与 `plasma-ramp-down`（concepts.tsv:781 / definitions.tsv:5054"电流终止的下降阶段"）边界互斥、相位序颠倒；自身 en/zh（definitions.tsv:5068/5069）仅为一句位置标签，无任何可判定限定语 |
| D2 | rupture-disc | FAIL | zh 定义（definitions.tsv:5352）含 `主动破裂`，en（definitions.tsv:5351）及本条依据引语（evidence.tsv:1500）均无对应词，且与库内 `主动`=actively- 用法（concepts.tsv:894 `actively-cooled-component`/`主动冷却部件`）及同批 `relief-valve` 的 `自动开启`（definitions.tsv:5293）互斥；反向 en 相对依据引语漏掉动作定值限定语 `at set pressure differential` |

## §4 组内统计与 AC 自检（实跑结果）

组内统计：**8 样本 / PASS 6 / FAIL 2 / UNDECIDABLE 0**（FAIL 与 UNDECIDABLE 不计入 PASS；本组不满足 64/64 PASS 的组内条件，M1 不得因本组而勾选）。

| AC 项 | 命令（实跑） | 期望 | 实测 |
|---|---|---|---|
| T-A 样本数 | `grep -c '^### ' docs/reviews/t5184/m1-group-G6.md` | = 8 | 8 |
| T-A 三值单行 | `grep -c '^判定: \(PASS\|FAIL\|UNDECIDABLE\)$' <报告>` | = 8 | 8（PASS 6 / FAIL 2 / UNDECIDABLE 0） |
| T-B 四字段齐全 | `for k in '原始语料:' '定义文本:' '适用性推理:' '证据锚点:'; do grep -c "$k" <报告>; done` | 各 ≥ 8 | 9 / 9 / 9 / 9 |
| T-B 来源缺失行与 UNDECIDABLE 一致 | 来源缺失标记行数 对比 `grep -c '^判定: UNDECIDABLE$'` | 相等 | 0 == 0 |
| T-B 台账行数 | 末节台账表（四列：编号 / concept_id / 判定 / 原因）的行数 = `awk '/^## §3/,/^## §4/' <报告> \| grep -c '^\| D[0-9]'` | = FAIL + UNDECIDABLE | 2 = 2 + 0 |
| T-B 证据锚点行数 | `grep -c 'concepts.tsv:[0-9]' <报告>` | ≥ 8 | 28 |
| T-B 定义行号行数 | `grep -c 'definitions.tsv:[0-9]' <报告>` | ≥ 16 | 33 |
| T-C 术语数据只读 | `git diff --stat -- terms/ artifacts/` | 空 | 空（无输出）；`git diff --cached --stat` 亦空 |
| T-C 工作区范围 | `git status --porcelain` | 本任务仅本报告为新增 | 本任务仅新增 `?? docs/reviews/t5184/m1-group-G6.md`；同一工作区另有 `?? .github/plans/5184-four-stage-closeout.md`（**会话开始前已存在**）、`?? docs/reviews/t5184/m1-group-G7.md` 与 `?? docs/reviews/t5184/m1-group-G8.md`（**本会话执行期间由并行任务出现**）——三者为他人/并行产物，本任务未创建、未修改、未 add |
| 组特化 manifest 对齐 | `awk -v g=G6 '$1==g' docs/reviews/t5184/m1-sample-manifest.tsv \| wc -l` | = 8 | 8；报告 8 个样本的 `concept_id` 与 manifest 该组 8 行**同序逐行相同**（§0 与各样本首行） |

**报告范围与限制声明**：本报告只覆盖 manifest 指定的 G6 8 个样本，是**抽检**，不构成对 `terms/registry/` 全量的语义保证；判定仅基于仓内可核验事实（定义文本、notes、`evidence.tsv` 引语、同族条目文本、`aliases.tsv` 命名处置、外部 diff 表映射事实），不推断条目写入成因/流程/时间，也不评估上游 GB/T-4960.9 / ITER 原文本身是否正确。`evidence.tsv` 中的 3 条百科 URL 无网络取回，凡只有外部权威才能定论的事项本报告一律不作 PASS 依据。本阶段无数据写权限，D1/D2 的修法建议不在本报告范围内。
