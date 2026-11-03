# M1 语义抽检报告 — 组 G5（8 样本）

> **计划**：`.github/plans/5184-four-stage-closeout.md` §Phase S4 / Task T4.6（PM #5184 / FUSION-TERMS id240）
> **生成日期**：**2026-11-03**（`date` 实测：`Tue Nov  3 12:15:10 PM CST 2026`）
> **性质**：**只读语义复核**。`terms/registry/*`、`artifacts/*` 全程只读；本报告为唯一新建文件；执行过程中**未运行任何 git 写命令**（不 add / commit / checkout / stash / restore / push）。
> **判定口径**：`PASS` = 该概念的 en/zh 定义与仓内原文（该概念 `concepts.tsv` notes）、族内相邻条目及本组依据逐条核验后无实质缺陷；`FAIL` = 存在可指认的语义缺陷（定义不能刻画对象 / 同语反复、误译、与同族或同库条目重复或矛盾）；`UNDECIDABLE` = 源语料取不到（**来源缺失**，不计入 PASS）。
> **来源可得性规则（照计划 §S4 统一口径）**：`source=corpus` → 依据 = `concepts.tsv` 该行 notes 原文 + 行号（可得）；`source=GB/T-4960.9` → 依据 = `gbt4960_9_diff.tsv` 的 `matched_concept_id` 命中行；`source=IAEA/ITER` → 依据 = 对应 `*_raw.tsv` 归一化命中行；`source=http(s)://…` → 依据 = URL + 取回日期 + 片段，取不回写「不可得: 无网络取回」。
> **路径更正记录（如实登记）**：任务书所述 `gbt4960_9_diff.tsv` 位于 `.github/plans/t4973-batches/` —— 该**目录确实存在**（153 个文件，含 `w1_b_b17.ids`…`w1_b_b21.ids`），但**目录内并无 `gbt4960_9_diff.tsv`**（`ls .github/plans/t4973-batches/gbt4960_9_diff.tsv` → `No such file or directory`）。**实存文件**为 `artifacts/terminology_sources/gbt4960_9_diff.tsv`（562 行 / 106 984 B，列 `#term / status / matched_concept_id / term_id / zh / abbr / definition`）。本报告一律以**实存文件**为准。
> **AC 计数正则声明**：本组 8 个概念的 `source` 字段**全部为 `corpus`**（见 §1），依据一律取 `concepts.tsv` notes 逐字 + 行号，故本组**无来源缺失样本** ⇒ 来源缺失标记行数 = 0 = `^判定: UNDECIDABLE$` 行数。为免与 AC 计数正则互相污染，本报告全文**不写出**该来源缺失标记串（`grep -c "^原始语料: <缺失标记>"` 实测 0）。

## §0 组样本清单（与 `m1-sample-manifest.tsv` 的 G5 8 行逐行同序相同）

抽取口径（manifest 头声明）：组内 id 去重排序后取 `sha256(id)[:16]` 升序前 8。分组口径：`w1_a_b01..b04` → `w1_b_b01..b34` → `w1_c_b01` 连续编号，连续 5 批为 1 组。G5 = `w1_b_b17..w1_b_b21`。

| 序 | group | batch_scope | concept_id | sha256_16 |
|---|---|---|---|---|
| 1 | G5 | w1_b_b17..w1_b_b21 | queue | 00b109cf1123a591 |
| 2 | G5 | w1_b_b17..w1_b_b21 | magnetic-pressure | 01a9864fcddec8d3 |
| 3 | G5 | w1_b_b17..w1_b_b21 | nuclide-inventory | 064d61a85632954a |
| 4 | G5 | w1_b_b17..w1_b_b21 | cpu-core | 07bc14e7a3c05b3b |
| 5 | G5 | w1_b_b17..w1_b_b21 | cache-miss | 0ad9e346eab6559a |
| 6 | G5 | w1_b_b17..w1_b_b21 | reactor | 0fdf674dcd7e8566 |
| 7 | G5 | w1_b_b17..w1_b_b21 | nuclear-fusion | 1606537e8ba99ef8 |
| 8 | G5 | w1_b_b17..w1_b_b21 | tetrahedral-mesh | 17e8d2916579dd01 |

**抽样复现**：`cat .github/plans/t4973-batches/w1_b_b1{7,8,9}.ids .github/plans/t4973-batches/w1_b_b2{0,1}.ids | sort -u | wc -l` → **100**（与计划「组内 ids = 100」一致）；对该 100 个 id 逐一算 `sha256(id)[:16]` 后按 hash 升序取前 8，结果**恰为**上表 8 个 cid（同序）。`sha256_16` 列对 8 个 cid 逐一复算**全部一致**（例：`python3 -c "import hashlib;print(hashlib.sha256(b'queue').hexdigest()[:16])"` → `00b109cf1123a591`）。本报告不复现 manifest 中 `group_sample_sha256` 的序列化口径，仅断言 **top-8 抽取结果与 8 个 `sha256_16` 值**逐行相符。

## §1 依据可得性与交叉核验执行记录（口径与命令）

- **组内依据类分布**：`awk -F'\t' -v c="<cid>" '$1==c{print $8}' terms/registry/concepts.tsv` 对 8 个 cid 取第 8 列 → `corpus` × 8（**全部可得**）。
- **原始语料取法（每样本）**：`grep -nP "^<cid>\t" terms/registry/concepts.tsv` → 该行 notes（第 7 列）逐字 + 行号。
- **定义文本取法（每样本）**：`grep -nP "^<cid>\t(en|zh)\t" terms/registry/definitions.tsv` → en、zh 两行逐字 + 行号（本组每概念各 1 条 en、1 条 zh；除 `reactor` 两行的 `source` 列为 URL 外，其余 14 行 `source` 列均为 `corpus`）。
- **GB/T-4960.9 交叉核验（非 source 通道）**：以实存文件 `artifacts/terminology_sources/gbt4960_9_diff.tsv` 核验，`awk -F'\t' -v c="<cid>" '$3==c'` 对 8 个 cid 的命中数**全部为 0**（该文件 `matched_concept_id` 非空行共 182 行）。与本组相关的**同族**权威行为 `:110 fusion | exists | fusion | 2.1.109 | 聚变`（其 definition 正文即「核聚变 nuclear fusion 轻元素的原子核聚合在一起形成较重元素的原子核并释放出能量的核反应。…」），为样本 7 的关键交叉证据。
- **IAEA / ITER 交叉核验（非 source 通道）**：对 `iter_glossary_raw.tsv`（143 行）/ `iaea_safety_glossary_raw.tsv`（877 行）的 **term 列**做整串归一化匹配（`awk -F'\t' -v t="…" 'NR>1 && tolower($1)==tolower(t)'`），`queue` / `magnetic pressure` / `nuclide` / `cpu core` / `cache` / `reactor` / `nuclear fusion` / `tetrahedral` **8 项 × 2 表 = 16 次命中全部为 0**。相邻（非本组 cid）命中仅 2 处：IAEA `:697 research reactor`（→ cid `research-reactor`，concepts.tsv:2394）、ITER `:37 Deuterium-Tritium Reactions`（其定义正文含 "nuclear fusion"，非独立术语条目）。**未命中 ≠ 不可得**：本组 8 条的 source 均为 `corpus`，notes 可取，故未命中不影响可得性，也不产生 `UNDECIDABLE`。
- **http(s) URL 类**：8 条的 `concepts.tsv` source 均非 URL，该类按 source 分派**不适用**；仅样本 6（`reactor`）的**定义行** `source` 为 URL，已**实际取回成功**（取回日期 2026-11-03），见样本 6 附注。
- **独立依据强度注记**：8 条的 `terms/registry/evidence.tsv` 依据行多为内部扩展（`internal:fusion-terms:domain-expansion` × 4、`internal:translation:*` × 2）或单一外部快照（Wikipedia 1、dify 1、Oxford 1，见 §2 各样本附注）；这不影响来源**可得性**（口径取 `concepts.tsv` notes），但限制了对 en 定义做「外部权威比对」的强度——凡只能由外部权威定论的判断，本报告不作为 `PASS` 依据。
- **批次归属**：`queue` / `cpu-core` / `cache-miss` → `concepts.tsv:1150`「Batch 56: HPC / Parallel Computing / Workflow」；`magnetic-pressure` → `:1054`「Batch 53 P2: General plasma physics」；`nuclide-inventory` / `reactor` / `nuclear-fusion` → `:1058`「Batch 54: Dify KB mining」；`tetrahedral-mesh` → `:1251`「Batch 59: CAD & Geometry Modeling」。

## §2 逐样本复核（8 样本）

### 样本 1/8 — `queue`

G5	w1_b_b17..w1_b_b21	queue	00b109cf1123a591

- 原始语料: [source=corpus，可得] notes 逐字（`terms/registry/concepts.tsv:1180`）：`Job scheduling queue/partition`（该行逐字：`queue | concept | 队列 | queue | (空) | active | Job scheduling queue/partition | corpus`）；GB/T-4960.9 交叉核验：`matched_concept_id==queue` 命中 0 行（term 列 `queue` 命中 0）；IAEA/ITER 交叉核验：term 列 `queue` 命中 0/0 行；http(s) URL 类：不适用（source≠URL）。附注：`terms/registry/evidence.tsv:1082` 记其为 `internal:fusion-terms:domain-expansion`（无 quote 文本，2026-04-04）。
- 定义文本: en 与 zh 逐字见下两行（两处行号：`terms/registry/definitions.tsv:5186`（en）、`terms/registry/definitions.tsv:5187`（zh），两行 `source` 列均为 `corpus`）
- 定义(en) 逐字: definitions.tsv:5186 → `A job scheduling queue, also referred to as a partition.`
- 定义(zh) 逐字: definitions.tsv:5187 → `队列是用于作业调度的队列，也称作分区。`
- 适用性推理: ①en 以限定语 "job scheduling" 指定该队列的用途域（作业调度，而非通用数据结构队列），并以 "also referred to as a partition" 给出 SLURM 语境的同义名，与 notes 的 `Job scheduling queue/partition` 逐项同源，在 Batch 56（HPC/并行计算，用于提交 MCNP/OpenMC 类作业）语境中准确刻画「调度队列/分区」这一对象；保留意见：属名 "queue" 与词条本身同名，界定时序为同语反复式（"a queue is a queue for job scheduling"），未额外给出与通用 FIFO 队列的判别语——但该句式与库内同批条目（`structured-mesh` definitions.tsv:5553/5554、`unstructured-mesh` 5750/5751）同构，属库级风格而非本条独有缺陷。②zh 与 en 等价：job scheduling→作业调度、queue→队列、partition→分区，句式亦与 en 同构；未增义、未漏义、无误译；zh 用"分区"承接 partition 与 `terms/registry/aliases.tsv:5666–5667`（`partition`/`分区` 登记为 alias，注 `SLURM terminology`）口径一致。③族内未见重复或互斥：`batch-job`（concepts.tsv:1156，notes「Non-interactive queued computational job」）是**被调度物**、`job-scheduler`（1179，category=`code`，notes「Software managing HPC job queue」）是**管理软件**、`compute-node`（1157）是**执行位置**，与本条（调度队列本身）在「物/软件/位置/对象」四层可分辨；zh 表面 `队列`、`分区` 在别名表内仅由本条占用（`grep -P "^队列\t|^分区\t" aliases.tsv` 共 2 行，均属本条）。
判定: PASS

- 证据锚点: concepts.tsv:1180

### 样本 2/8 — `magnetic-pressure`

G5	w1_b_b17..w1_b_b21	magnetic-pressure	01a9864fcddec8d3

- 原始语料: [source=corpus，可得] notes 逐字（`terms/registry/concepts.tsv:1057`）：`Pressure exerted by magnetic field, B²/(2μ₀)`（该行逐字：`magnetic-pressure | concept | 磁压 | magnetic pressure | (空) | active | Pressure exerted by magnetic field, B²/(2μ₀) | corpus`）；GB/T-4960.9 交叉核验：`matched_concept_id==magnetic-pressure` 命中 0 行（GB/T 侧同族压强条目为 `plasma pressure`、`kinetic pressure`，经 concepts.tsv:2719 / :2669 落库，均非本条）；IAEA/ITER 交叉核验：term 列 `magnetic pressure` 命中 0/0 行；http(s) URL 类：不适用。附注：`terms/registry/evidence.tsv:962` 记其依据为 Wikipedia URL `https://en.wikipedia.org/wiki/Magnetic_pressure`（2026-03-23，无 quote 列内容）。
- 定义文本: en 与 zh 逐字见下两行（两处行号：`terms/registry/definitions.tsv:4716`（en）、`terms/registry/definitions.tsv:4717`（zh），两行 `source` 列均为 `corpus`）
- 定义(en) 逐字: definitions.tsv:4716 → `Pressure exerted by the magnetic field, equal to B²/(2μ₀).`
- 定义(zh) 逐字: definitions.tsv:4717 → `磁压是磁场施加的压力，其值为 B²/(2μ₀)。`
- 适用性推理: ①en 以限定语 "exerted by the magnetic field" 指定压力来源为磁场（而非粒子热运动），并以定量式 "equal to B²/(2μ₀)" 给出可计算的对应量，与 notes 的 `Pressure exerted by magnetic field, B²/(2μ₀)` 逐项同源；该式即等离子体物理中磁压的标准形式，与等离子体热压构成 MHD 力平衡两侧，故在核聚变/核工程语境中准确刻画该量（定界清晰、可判定）。②zh 与 en 等价：磁压↔magnetic pressure、"磁场施加的压力"↔pressure exerted by the magnetic field、"其值为 B²/(2μ₀)"↔equal to B²/(2μ₀)；未增义、未漏义、无误译；zh 首选"磁压"与 `terms/registry/aliases.tsv:5103–5104`（`magnetic pressure`/`磁压` preferred）一致，且 `aliases.tsv:5130–5132` 已把"磁力压力"（magnetic≠磁力）、"磁性压力"（magnetic≠磁性）、"磁场压强"（pressure≠压强）判为 forbidden — 本定义正文用"压力"而非"压强"，与禁项口径自洽。③族内未见重复或互斥：`plasma-pressure`（concepts.tsv:2719，zh 首选"等离子体压强"，GB/T 来源）为等离子体热压、`kinetic-pressure`（2669，"动理学压强"）为粒子热运动标量压、`base-pressure`（798，"本底气压"）、`neutral-pressure`（901，"中性气压"）各属不同压强种类，`magnetic-stored-energy`（132）为能量而非压力；本条的 B²/(2μ₀) 与上述并列而不重复。
判定: PASS

- 证据锚点: concepts.tsv:1057

### 样本 3/8 — `nuclide-inventory`

G5	w1_b_b17..w1_b_b21	nuclide-inventory	064d61a85632954a

- 原始语料: [source=corpus，可得] notes 逐字（`terms/registry/concepts.tsv:1066`）：`Radioisotope composition and activity of activated materials`（该行逐字：`nuclide-inventory | concept | 核素产额 | nuclide inventory | (空) | active | Radioisotope composition and activity of activated materials | corpus`）；GB/T-4960.9 交叉核验：`matched_concept_id==nuclide-inventory` 命中 0 行（term 列 `nuclide`、`inventory` 命中 0）；IAEA/ITER 交叉核验：term 列 `nuclide` 整串命中 0/0 行（IAEA 侧仅有 `fissile nuclide`（:319）、`fissionable nuclide`（:323）、`radionuclides of artificial origin`（:657）等，均非"核素产额/存量"）；http(s) URL 类：不适用。附注：`terms/registry/evidence.tsv:970` 记其依据为 `dify:Neutronics/ActivationInventory:Ma_Huang_2018`（2026-03-24）。
- 定义文本: en 与 zh 逐字见下两行（两处行号：`terms/registry/definitions.tsv:4915`（en）、`terms/registry/definitions.tsv:4916`（zh），两行 `source` 列均为 `corpus`）
- 定义(en) 逐字: definitions.tsv:4915 → `The radioisotope composition and activity of activated materials.`
- 定义(zh) 逐字: definitions.tsv:4916 → `核素产额是活化材料中放射性同位素的组成与活度。`
- 适用性推理: ①en 以限定语 "of activated materials"（活化材料）限定对象域，以 "radioisotope composition and activity" 指出所刻画内容，与 notes 逐词同源；但 `inventory` 在活化/中子学语境中义为**存量/总量**（同族并列证据：`tritium-inventory` concepts.tsv:254 notes「Total tritium quantity in a system or component」、`dust-inventory` concepts.tsv:989 notes「Total mobilizable dust quantity inside vacuum vessel」，二者 zh 首选分别落在"氚**存量**""粉尘**存量**"），本条却把 inventory 界定为"组成与活度"（composition/activity），漏掉"量"这一核心义，属**定义不能准确刻画对象**。②zh 与 en 虽逐词对应（"活化材料中放射性同位素的组成与活度"↔the radioisotope composition and activity of activated materials），但**首选 zh 术语"核素产额"是 `nuclide inventory` 的误译**：`产额` = yield/production，与 `inventory` 不同义（inventory = 存量/总量/清单）；该误译与库内既有的 "‑inventory → ‑存量" 命名范式（254 / 484 / 989）不一致，且本条自身已登记 alias `核素清单`（`aliases.tsv:5313`）——较"产额"更贴近 inventory 反而被降为 alias；此外 zh 定义正文（"组成与活度"）与首选中文字面（"产额"）亦不自洽：任何"产额"都不会被定义为"组成与活度"。③族内未出现同物理对象的第三条重复登记（非重复登记），但与同族 inventory 条目的**术语范式冲突**已构成可指认缺陷。综合 ①②③ 判 FAIL。
- 缺陷/待定原因: 首选 zh `核素产额` 是 `nuclide inventory` 的**误译**（产额=yield ≠ inventory=存量），与同族 `tritium-inventory`（concepts.tsv:254，"氚存量"）、`tritium-startup-inventory`（484，"氚启动存量"）、`dust-inventory`（989，"粉尘存量"）的"‑inventory→‑存量"范式冲突，亦与本条自设 alias `核素清单`（aliases.tsv:5313）口径相左；en/zh 定义正文把 inventory 界定为"组成与活度"（composition and activity）而非"存量/总量"，偏离 inventory 的"量"义，属定义不能准确刻画对象。
判定: FAIL

- 证据锚点: concepts.tsv:1066

### 样本 4/8 — `cpu-core`

G5	w1_b_b17..w1_b_b21	cpu-core	07bc14e7a3c05b3b

- 原始语料: [source=corpus，可得] notes 逐字（`terms/registry/concepts.tsv:1158`）：`Processor core (distinct from plasma core)`（该行逐字：`cpu-core | concept | CPU核心 | CPU core | (空) | active | Processor core (distinct from plasma core) | corpus`）；GB/T-4960.9 交叉核验：`matched_concept_id==cpu-core` 命中 0 行；IAEA/ITER 交叉核验：term 列 `cpu core` 命中 0/0 行；http(s) URL 类：不适用。附注：`terms/registry/evidence.tsv:1060` 记其为 `internal:fusion-terms:domain-expansion`（2026-04-04）。
- 定义文本: en 与 zh 逐字见下两行（两处行号：`terms/registry/definitions.tsv:3879`（en）、`terms/registry/definitions.tsv:3880`（zh），两行 `source` 列均为 `corpus`）
- 定义(en) 逐字: definitions.tsv:3879 → `A processor core, distinct from a plasma core.`
- 定义(zh) 逐字: definitions.tsv:3880 → `CPU核心是处理器核心，区别于等离子体核心。`
- 适用性推理: ①en 以限定语 "processor" 把属类锚定在计算硬件侧（处理器核），并以 "distinct from a plasma core" 显式排除聚变语境的"等离子体核心"义，与 notes 的 `Processor core (distinct from plasma core)` 逐词同源；本条为消歧条目，与同批 `compute-node`（concepts.tsv:1157 notes「HPC cluster worker node (distinct from mesh node)」，definitions.tsv:3805/3806）**句式同构**，在 Batch 56（HPC/并行计算）语境中准确刻画"CPU 核"这一对象。②zh 与 en 等价：CPU核心↔CPU core、处理器核心↔processor core、"区别于等离子体核心"↔distinct from a plasma core；未增义、未漏义、无误译；`aliases.tsv:5616–5617`（`CPU core`/`CPU核心` preferred）与本条首选一致，`aliases.tsv:5618` 把 `处理器核心` 登记为 alias（variant），与定义正文以"处理器核心"作属类相符。③族内未见重复或互斥：库内**无**独立 `plasma-core` / `core` / `nuclear-reactor` 类同形条目（"芯部"相关仅 `core-confinement` concepts.tsv:2597，category=`nuclear-fusion`，zh 首选"芯部约束"，非核心硬件义），故本条消歧的对照面不与他条争名；`compute-node`（节点）与本条（核心）分属不同抽象层，不重复。
判定: PASS

- 证据锚点: concepts.tsv:1158

### 样本 5/8 — `cache-miss`

G5	w1_b_b17..w1_b_b21	cache-miss	0ad9e346eab6559a

- 原始语料: [source=corpus，可得] notes 逐字（`terms/registry/concepts.tsv:1176`）：`Failed cache lookup requiring main memory access`（该行逐字：`cache-miss | concept | 缓存未命中 | cache miss | (空) | active | Failed cache lookup requiring main memory access | corpus`）；GB/T-4960.9 交叉核验：`matched_concept_id==cache-miss` 命中 0 行（term 列 `cache` 命中 0）；IAEA/ITER 交叉核验：term 列 `cache` 命中 0/0 行；http(s) URL 类：不适用。附注：`terms/registry/evidence.tsv:1078` 记其为 `internal:fusion-terms:domain-expansion`（2026-04-04）。
- 定义文本: en 与 zh 逐字见下两行（两处行号：`terms/registry/definitions.tsv:3723`（en）、`terms/registry/definitions.tsv:3724`（zh），两行 `source` 列均为 `corpus`）
- 定义(en) 逐字: definitions.tsv:3723 → `A failed cache lookup that requires access to main memory.`
- 定义(zh) 逐字: definitions.tsv:3724 → `缓存未命中是需要访问主存的缓存查找失败。`
- 适用性推理: ①en 以限定语 "failed … lookup" 指定事件类型（查找失败，而非缓存本身或其容量），并以 "requires access to main memory" 给出后果判据（必须回主存取数），与 notes 的 `Failed cache lookup requiring main memory access` 逐项同源；两项判据合起来给出可判定的事件边界，准确刻画该性能事件（Batch 56，HPC 性能分析语境）。②zh 与 en 等价：cache miss→缓存未命中、failed lookup→查找失败、main memory→主存；未增义、未漏义、无误译；zh 首选"缓存未命中"与 `aliases.tsv:5657–5658` 一致，且正文用"主存"而非泛化的"内存"，与 en "main memory"（主存储器）逐词对应，术语精度保持。③族内未见重复或互斥：`memory-bandwidth`（concepts.tsv:1175，notes「Data transfer rate between memory and CPU」，definitions.tsv:1794 给出 GB/s 量纲）是**带宽量**、`openmp`（1152，category=`code`）是**并行编程接口**，与本条（缺失事件）在"量/接口/事件"三层面可分辨；库内无第二条 cache 相关条目，无 zh 表面争用。
判定: PASS

- 证据锚点: concepts.tsv:1176

### 样本 6/8 — `reactor`

G5	w1_b_b17..w1_b_b21	reactor	0fdf674dcd7e8566

- 原始语料: [source=corpus，可得] notes 逐字（`terms/registry/concepts.tsv:1105`）：`Generic academic glue word for translation`（该行逐字：`reactor | concept | 堆 | reactor | (空) | active | Generic academic glue word for translation | corpus`）；GB/T-4960.9 交叉核验：`matched_concept_id==reactor` 命中 0 行（GB/T 侧同族为 `fusion reactor`→`fusion-reactor`、`thermal nuclear fusion` 等，均非本条）；IAEA/ITER 交叉核验：term 列 `reactor` 整串命中 0/0 行（最近相邻条目为 IAEA `:697 research reactor` → cid `research-reactor`，concepts.tsv:2394，非本条）；**http(s) URL 类（本条定义行专属）**：definitions.tsv:5251–5252 的 `source` 列 = `https://www.oxfordlearnersdictionaries.com/definition/english/reactor`，本次**实际取回成功**（取回日期 **2026-11-03**），页面逐字片段为 `reactor noun (also nuclear reactor) a large structure used to produce nuclear energy`——与 en 定义正文逐词相符；`terms/registry/evidence.tsv:3231` 亦记同一 URL 的 quote "a large structure used to produce nuclear energy"（`copilot`，2026-10-27）。附注：`evidence.tsv:1009` 另记 `internal:translation:glue-vocabulary`（quote「High-frequency academic glue word for zh→en search translation」，2026-03-29）。
- 定义文本: en 与 zh 逐字见下两行（两处行号：`terms/registry/definitions.tsv:5251`（en）、`terms/registry/definitions.tsv:5252`（zh），两行 `source` 列均为上述 Oxford URL）
- 定义(en) 逐字: definitions.tsv:5251 → `A large structure used to produce nuclear energy, also called a nuclear reactor.`
- 定义(zh) 逐字: definitions.tsv:5252 → `堆是用于产生核能的大型结构（装置），又称核反应堆。`
- 适用性推理: ①en 以 "produce nuclear energy" 限定用途、以 "large structure" 给出属类、以 "also called a nuclear reactor" 给出同义全称，与所引 Oxford 词条逐词相符（取回片段 `(also nuclear reactor) a large structure used to produce nuclear energy`），亦与 notes 的"通用翻译粘合词"定位相容（粘合词取其最一般义），故在核/聚变语境中准确刻画"堆"这一对象，判据可判定。②zh 与 en 等价："堆"↔reactor、"用于产生核能的大型结构"↔a large structure used to produce nuclear energy、"又称核反应堆"↔also called a nuclear reactor；唯一差异是 zh 在"大型结构"后加括注"（装置）"，属对同义范畴的括注式补足（structure 在工程中文可作"结构/装置"，不改变指称），**不构成增义、漏义或误译**；zh 首选 `堆` 与 `aliases.tsv:5484` 一致，且库内 preferred_zh 为 `堆` 的条目**仅此 1 条**（`awk -F'\t' '$3=="堆"' concepts.tsv | wc -l` = 1），无 zh 表面争用。③族内未见重复或互斥：`fusion-reactor`（concepts.tsv:1108，notes「General fusion reactor (not specific FPP/pilot plant)」）、`prototype-reactor`（824）、`modular-fusion-reactor`（3020）、`thermonuclear-reactor`（2904）、`research-reactor`（2394）在语义上均为本条**下位**（本条不排除聚变堆等"产生核能"的堆），属上下位关系而非重复登记；`fusion-device`（1109，notes「General fusion experimental device」）以"实验装置"而非"产生核能"为判据，与本条可分辨。
判定: PASS

- 证据锚点: concepts.tsv:1105

### 样本 7/8 — `nuclear-fusion`

G5	w1_b_b17..w1_b_b21	nuclear-fusion	1606537e8ba99ef8

- 原始语料: [source=corpus，可得] notes 逐字（`terms/registry/concepts.tsv:1110`）：`Nuclear fusion (general)`（该行逐字：`nuclear-fusion | concept | 核聚变 | nuclear fusion | (空) | active | Nuclear fusion (general) | corpus`）；GB/T-4960.9 交叉核验：`matched_concept_id==nuclear-fusion` 命中 0 行，**但存在直接相关的同族权威行 `artifacts/terminology_sources/gbt4960_9_diff.tsv:110`**：`fusion | exists | fusion | 2.1.109 | 聚变 | | 核聚变 nuclear fusion 轻元素的原子核聚合在一起形成较重元素的原子核并释放出能量的核反应。最易实现的核聚变是在氢的两个同位素(氘和氚)之间的反应。…` —— 即 GB/T 把中文面「聚变/核聚变」映射到 cid **`fusion`**（concepts.tsv:1084），而非本条；IAEA/ITER 交叉核验：term 列 `nuclear fusion` 命中 0/0 行（ITER `:37` 的 `Deuterium-Tritium Reactions` 仅在**定义正文**中出现 "nuclear fusion"，非独立术语条目）；http(s) URL 类：不适用。附注：`terms/registry/evidence.tsv:1014` 记其为 `internal:translation:compound-vocabulary`（quote「High-frequency compound term for zh→en search translation」，2026-03-29）。
- 定义文本: en 与 zh 逐字见下两行（两处行号：`terms/registry/definitions.tsv:4904`（en）、`terms/registry/definitions.tsv:4905`（zh），两行 `source` 列均为 `corpus`）
- 定义(en) 逐字: definitions.tsv:4904 → `Nuclear fusion in the most general sense.`
- 定义(zh) 逐字: definitions.tsv:4905 → `核聚变指最一般意义上的核聚变。`
- 适用性推理: ①en **不能刻画该概念**：定义全由「词条名（nuclear fusion）+ 模糊限定语（in the most general sense）」构成，既未给出反应机制（轻核聚合为重核并释放能量），亦无任何判别语，属典型同语反复（"nuclear fusion is nuclear fusion in the most general sense"）；对照同库同族 cid `fusion`（`terms/registry/definitions.tsv:58`，ITER 逐字 `The merging of two light atomic nuclei into a heavier nucleus, with a resultant loss in the combined mass and a massive release of energy.`）可见本条未做任何定义化加工，定义力为零。②zh 与 en 逐字等价，但也逐字同语反复（"核聚变指最一般意义上的核聚变"），同样不能刻画对象；故 ② 不构成独立缺陷，但与 ① 叠加使本条完全无定义力。③**存在重复登记与中文面归属冲突**：本条（`nuclear-fusion`，preferred_zh `核聚变`，concepts.tsv:1110）与 `fusion`（concepts.tsv:1084，preferred_zh `聚变`，notes 同为"for translation"类）指**同一物理现象（最一般义的核聚变）**；而 GB/T-4960.9 的权威行（gbt4960_9_diff.tsv:110）已把「聚变/核聚变」映射到 **`fusion`**，且 `fusion` 的 zh 定义正文即以「核聚变 nuclear fusion …」开篇；registry 却把中文面 `核聚变` 划归本条（`aliases.tsv:5494` preferred）、`聚变` 划归 `fusion`（`aliases.tsv:5442` preferred），两 cid 同义并存、定义质量悬殊，且中文面归属与权威映射相左，属**重复登记 + 中文面归属冲突**。综合 ①③ 判 FAIL。
- 缺陷/待定原因: en/zh 定义均为同语反复（"核聚变指最一般意义上的核聚变"），无机制、无判别语，不能刻画对象；且与 `fusion`（concepts.tsv:1084，另含 ITER en 定义 + GB/T zh 定义）**重复登记**同一"最一般义的核聚变"，中文面 `核聚变` 归属与 GB/T-4960.9 权威映射（gbt4960_9_diff.tsv:110 → cid `fusion`，其定义正文即「核聚变 nuclear fusion …」）冲突。
判定: FAIL

- 证据锚点: concepts.tsv:1110

### 样本 8/8 — `tetrahedral-mesh`

G5	w1_b_b17..w1_b_b21	tetrahedral-mesh	17e8d2916579dd01

- 原始语料: [source=corpus，可得] notes 逐字（`terms/registry/concepts.tsv:1258`）：`Tet mesh for FEM/MC`（该行逐字：`tetrahedral-mesh | concept | 四面体网格 | tetrahedral mesh | (空) | active | Tet mesh for FEM/MC | corpus`）；GB/T-4960.9 交叉核验：`matched_concept_id==tetrahedral-mesh` 命中 0 行（term 列 `tetrahedral`、`mesh` 命中 0）；IAEA/ITER 交叉核验：term 列 `tetrahedral` 命中 0/0 行；http(s) URL 类：不适用。附注：`terms/registry/evidence.tsv:1157` 记其为 `internal:fusion-terms:domain-expansion`（quote「Standard FEM mesh type」，2026-04-04）。
- 定义文本: en 与 zh 逐字见下两行（两处行号：`terms/registry/definitions.tsv:5625`（en）、`terms/registry/definitions.tsv:5626`（zh），两行 `source` 列均为 `corpus`）
- 定义(en) 逐字: definitions.tsv:5625 → `A tetrahedral mesh used for FEM and Monte Carlo calculations.`
- 定义(zh) 逐字: definitions.tsv:5626 → `四面体网格是用于有限元与蒙特卡罗计算的网格划分。`
- 适用性推理: ①en 以限定语 "tetrahedral" 指定单元形状（而非拓扑或维数），以 "used for FEM and Monte Carlo calculations" 指定用途域（有限元与蒙特卡罗），与 notes 的 `Tet mesh for FEM/MC` 逐项对应（MC 展开为 Monte Carlo，与 en 全称口径一致）；在 Batch 59（CAD 与几何建模）及输运计算语境（四面体网格用于 DAGMC/非结构网格 tally 类工作流）中准确刻画该网格类型。②zh 与 en 等价：tetrahedral mesh→四面体网格、FEM→有限元、Monte Carlo→蒙特卡罗、used for→用于；zh 末以范畴词"网格划分"收束（en 的 mesh 本即名词性网格），未增义、未漏义、无误译；首选 `四面体网格`/`tetrahedral mesh` 与 `aliases.tsv:5837–5838` 一致，短形 `tet mesh` 登记为 alias（5839），与 notes 用短形、定义用全称的写法相符。③族内未见重复或互斥：`hexahedral-mesh`（concepts.tsv:1259，notes「Hex mesh for FEM」；definitions.tsv:4426 仅覆盖 FEM）为**形状对照**条目（本条额外覆盖 MC，判据不同但互不矛盾）、`computational-mesh`（1393）为上位通用网格、`structured-mesh`（1394）/`unstructured-mesh`（1395）按**拓扑**分类、`conformal-mesh`（1276）/`surface-mesh`（1270）按适配性与维度分类、`mesh-generation`（458）/`mesh-independence`（1135）/`mesh-tally`（1192）为**流程/方法**条目；本条在"单元形状"这一分类轴上唯一，未见与其余条目重复或互斥。
判定: PASS

- 证据锚点: concepts.tsv:1258

## §3 缺陷/待定台账（行数 = FAIL + UNDECIDABLE = 2 + 0 = 2）

| 编号 | concept_id | 判定 | 原因 |
|---|---|---|---|
| D1 | nuclide-inventory | FAIL | 首选 zh `核素产额` 为 `nuclide inventory` 的误译（产额=yield ≠ inventory=存量），与同族 `tritium-inventory`（concepts.tsv:254 氚存量）、`tritium-startup-inventory`（484 氚启动存量）、`dust-inventory`（989 粉尘存量）的「‑inventory→‑存量」范式冲突，亦与本条自设 alias `核素清单`（aliases.tsv:5313）口径相左；en/zh 定义正文（"放射性同位素的组成与活度"）把 inventory 界定为组成与活度而非存量/总量，属定义不能准确刻画对象 |
| D2 | nuclear-fusion | FAIL | en/zh 定义均为同语反复（"核聚变指最一般意义上的核聚变"），无机制、无判别语；且与 `fusion`（concepts.tsv:1084）重复登记同一"最一般义的核聚变"，中文面 `核聚变` 归属与 GB/T-4960.9 权威映射（artifacts/terminology_sources/gbt4960_9_diff.tsv:110 → cid `fusion`）冲突 |

## §4 组内统计与 AC 自检（实跑结果）

组内统计：**8 样本 / PASS 6 / FAIL 2 / UNDECIDABLE 0**（FAIL 与 UNDECIDABLE 均不计入 PASS；本组不满足"64/64 PASS"的组内条件，M1 **不得**因本组而勾选）。

| AC 项 | 命令（实跑） | 期望 | 实测 |
|---|---|---|---|
| T-A 样本数 | `grep -c '^### ' docs/reviews/t5184/m1-group-G5.md` | = 8 | 8 |
| T-A 三值单行 | `grep -c '^判定: \(PASS\|FAIL\|UNDECIDABLE\)$' docs/reviews/t5184/m1-group-G5.md` | = 8 | 8（PASS 6 / FAIL 2 / UNDECIDABLE 0） |
| T-B 四字段齐全 | `for k in '原始语料:' '定义文本:' '适用性推理:' '证据锚点:'; do grep -c "$k" <报告>; done` | 各 ≥ 8 | 8 / 8 / 8 / 8 |
| T-B 来源缺失行与 UNDECIDABLE 一致 | `grep -c "^原始语料: <缺失标记>" <报告>` 对比 `grep -c '^判定: UNDECIDABLE$' <报告>`（缺失标记串见上引声明，全文未写出） | 相等 | 0 == 0 |
| T-B 台账行数 | 末节台账表（`grep -c '^\| D'`）行数 | = FAIL + UNDECIDABLE | 2 = 2 + 0 |
| T-B 证据锚点行数 | `grep -c 'concepts.tsv:[0-9]' <报告>` | ≥ 8 | ≥ 8（每条 证据锚点 至少 1 处，另有正文引用） |
| T-B 定义行号行数 | `grep -c 'definitions.tsv:[0-9]' <报告>` | ≥ 16 | ≥ 16（每样本 定义文本 行 2 处 + 定义(en)/定义(zh) 2 处） |
| T-C 术语数据只读 | `git diff --stat -- terms/ artifacts/` | 空 | 空（未运行任何写命令；未 add/commit/checkout/stash/restore/push） |
| T-C 提交范围 | `git status --porcelain` | 仅本 md 新增 | 仅 `docs/reviews/t5184/m1-group-G5.md` 新增（未跟踪） |
| 组特化 manifest 对齐 | `awk -F'\t' '$1=="G5"' docs/reviews/t5184/m1-sample-manifest.tsv \| wc -l` | = 8 | 8；报告 8 个样本的 `concept_id` 与 manifest 该组 8 行**同序逐行相同**（§0 表与各样本首行） |
| 组特化抽样复现 | 100 个组内 id 按 `sha256(id)[:16]` 升序取前 8 | = manifest 8 行 | 完全一致（见 §0） |

**报告范围与限制声明**：本报告只覆盖 manifest 指定的 G5 8 个样本，是**抽检**，不构成对 `terms/registry/` 全量（756 条）的语义保证；D1/D2 只陈述可由行号定位、可复核的库内事实（首选 zh 词形、定义正文、别名表登记、GB/T 映射落点），不推断这些条目的写入成因/流程/时间，也不评估上游 GB/T-4960.9 原文或 Oxford 词条本身是否正确。本阶段无数据写权限，D1/D2 的修法建议（如 `nuclide-inventory` 首选 zh 改判、`nuclear-fusion` 与 `fusion` 合并/划界）不在本报告执行范围内，需用户裁决。
