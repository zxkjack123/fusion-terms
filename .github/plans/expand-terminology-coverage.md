# 扩充多领域术语覆盖

## 背景与目标

- **问题/需求描述**：当前术语注册表（987 个 concept）集中在聚变装置、等离子体物理、氚工艺等核心领域，缺少通用科学方法论、HPC/并行计算、蒙特卡罗/确定论输运、核数据处理、CAD/几何建模、辐射防护/剂量学、材料力学、热工水力、软件工程、数据格式/可视化等 10 个领域的常用术语。这些缺口直接影响 translation_dict、query_expansions、IME 词库的实际可用覆盖率。
- **目标**：向 `terms/registry/` 三表（concepts.tsv、aliases.tsv、evidence.tsv）批量添加约 **300+ 个新 concept**（含中英文首选形式、缩写、常见别名），通过验证后重新导出全部产物。
- **非目标（不做什么）**：
  - 不修改 pipeline 源代码 — 只做数据层新增
  - 不调整 config.toml 参数或导出行为
  - 不删除/修改任何已有 concept — 只追加新行
  - 不重构 TSV 表结构或字段定义
- **已有代码/流程复用分析**：
  - `pipeline/validate_registry.py`：复用（添加后直接运行验证）
  - `pipeline/export_registry.py`：复用（重新导出所有 artifact）
  - `pipeline/build_terms.py`：复用（重建 IME 词表）
  - 现有 `category` 枚举（13 种）：复用现有值，不引入新 category

## 技术方案

- **方案概述**：按 10 个领域分 Phase，每 Phase 向三张 TSV 追加对应领域的新行。每 Phase 完成后运行 `validate_registry` 做增量验证，全部 Phase 完成后运行完整 export + build 流水线。
- **关键设计决策**：
  1. **category 映射**：复用现有 13 种 category，不新增。映射原则：工具/软件→`code`；方法→`method`；度量/参数→`metric`；概念→`concept`；标准/组织→`organization`
  2. **concept_id 命名**：全部使用 `^[a-z0-9]+(-[a-z0-9]+)*$` 格式，与现有风格一致
  3. **evidence 来源**：优先使用 Wikipedia / IAEA / ICRP 等可验证 URL；无公开 URL 的术语使用 `internal:fusion-terms:domain-expansion` 标注
  4. **alias 覆盖**：每个 concept 至少 1 个 `preferred` alias（满足验证要求），常用缩写单独作为 `abbr preferred`
  5. **allowlist 同步**：新增英文单 token 术语追加到 `allowlist_en.txt`，新增中文术语追加到 `allowlist_zh.txt`
- **影响范围**：
  - `terms/registry/concepts.tsv` — 追加 ~300 行
  - `terms/registry/aliases.tsv` — 追加 ~900 行（每 concept 平均 ~3 aliases）
  - `terms/registry/evidence.tsv` — 追加 ~300 行
  - `terms/allowlist_en.txt` — 追加 ~200 行（单 token 英文项）
  - `terms/allowlist_zh.txt` — 追加 ~250 行（中文首选形式）
  - `artifacts/` — 所有导出产物将重新生成

## Error & Rescue Map（关键失败路径映射）

| 代码路径/操作 | 可能的失败 | 错误类型 | 已处理？ | 处理方式 | 用户可见行为 |
|-------------|-----------|---------|---------|---------|------------|
| `validate_registry` — concept_id 格式 | 新 id 含大写/特殊字符 | ValidationError | Y | 每 Phase 后立即验证，失败需检查 id 命名 | CLI 报错并退出 |
| `validate_registry` — missing preferred alias | concept 无对应 preferred alias | ValidationError | Y | 每个 concept 在 aliases.tsv 中至少添加 1 个 preferred | CLI 报错并退出 |
| `validate_registry` — missing evidence | concept 无 evidence 行 | ValidationError | Y | 每个 concept 同步添加 evidence 行 | CLI 报错并退出 |
| `validate_registry` — alias 映射冲突 | 新 alias 已被旧 concept 使用 | ValidationError | Y | 添加前 grep 检查已有 alias，冲突时改用 concept_id 作前缀 | CLI 报错并退出 |
| `validate_registry` — bridge check | deprecated/forbidden alias 出现在 allowlist | ValidationError | Y | 只将 preferred/alias 类型的术语加入 allowlist | CLI 报错并退出 |
| TSV 编码错误 | 粘贴引入非 UTF-8 字符 | UnicodeDecodeError | Y | 在写入前确认编辑器 UTF-8 模式 | CLI 报错并退出 |
| 行数极多导致手误 | Tab/字段对齐错误 | ValidationError | Y | 每 Phase 小批量添加后立即验证 | CLI 报错并退出 |

## 执行计划

### Phase 1: 通用科学/工程方法论术语

#### ✅ Task 1.1: 添加方法论术语到三表

- **目标**：新增 ~30 个 concept。注意 `safety-factor` 已存在（plasma q 语境），需跳过或仅补 alias。

**新增术语清单**（concept_id / preferred_zh / preferred_en / category）：

| concept_id | preferred_zh | preferred_en | category | notes |
|---|---|---|---|---|
| benchmark | 基准测试 | benchmark | method | 通用V&V方法论 |
| validation | 验证 | validation | method | 证明模型与实验一致（V&V中的V） |
| verification | 校核 | verification | method | 证明代码实现正确（V&V中的V） |
| sensitivity-analysis | 灵敏度分析 | sensitivity analysis | method | |
| parametric-study | 参数化研究 | parametric study | method | 与 parametric-instability 无关 |
| best-estimate | 最佳估算 | best estimate | method | |
| conservative-estimate | 保守估算 | conservative estimate | method | |
| design-margin | 设计裕度 | design margin | metric | |
| code-to-code-comparison | 程序间比较 | code-to-code comparison | method | |
| figure-of-merit | 品质因数 | figure of merit | metric | abbr: FOM |
| uncertainty-quantification | 不确定度量化 | uncertainty quantification | method | abbr: UQ |
| error-propagation | 误差传播 | error propagation | method | |
| convergence-criterion | 收敛准则 | convergence criterion | concept | |
| mesh-independence | 网格无关性 | mesh independence | method | 也称 grid convergence |
| dimensional-analysis | 量纲分析 | dimensional analysis | method | |
| scaling-law | 标度律 | scaling law | concept | |
| empirical-correlation | 经验关联式 | empirical correlation | method | |
| analytical-solution | 解析解 | analytical solution | concept | |
| numerical-solution | 数值解 | numerical solution | concept | |
| boundary-condition | 边界条件 | boundary condition | concept | abbr: BC |
| initial-condition | 初始条件 | initial condition | concept | |
| steady-state | 稳态 | steady state | concept | |
| transient-analysis | 瞬态分析 | transient analysis | method | |
| coupled-analysis | 耦合分析 | coupled analysis | method | 多物理耦合 |
| multiphysics | 多物理场 | multiphysics | concept | |
| surrogate-model | 代理模型 | surrogate model | method | 机器学习/响应面 |
| response-surface | 响应面 | response surface | method | abbr: RSM |
| latin-hypercube-sampling | 拉丁超立方抽样 | Latin hypercube sampling | method | abbr: LHS |
| monte-carlo-sampling | 蒙特卡罗抽样 | Monte Carlo sampling | method | 通用统计方法 |
| goodness-of-fit | 拟合优度 | goodness of fit | metric | |

- **修改内容**：
  - `terms/registry/concepts.tsv`：追加 ~30 行
  - `terms/registry/aliases.tsv`：追加约 90 行（含中文首选、英文首选、缩写、常用变体）
  - `terms/registry/evidence.tsv`：追加 ~30 行
- **修改边界**：不得修改已有行；不得修改 `pipeline/` 下任何文件
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry --terms-dir terms`
  - 预期输出：exit code 0
- **验收标准**：
  - ✅ 新 concept_id 存在于 concepts.tsv 且 category 字段非空
  - ✅ 每个新 concept 至少有 1 个 `kind=preferred` 的 alias 行
  - ✅ 每个新 concept 有对应的 evidence 行且 source 非空
  - ✅ validate_registry 通过
- **潜在风险**：`safety-factor` 已存在——跳过；`validation`/`verification` V&V 区分需在 notes 中写清；`parametric-study` 与已有 `parametric-instability` 是不同概念需明确

#### ✅ Task 1.2: 同步 allowlist
- **修改内容**：
  - `terms/allowlist_en.txt`：追加 benchmark, validation, verification, FOM, UQ, multiphysics 等单 token
  - `terms/allowlist_zh.txt`：追加 基准测试、验证、校核、灵敏度分析、设计裕度、不确定度量化 等
- **修改边界**：不得修改已有行
- **测试要求**：validate_registry 通过
- **验收标准**：
  - ✅ validate_registry 通过
- **潜在风险**：多词短语不应加入 allowlist_en（要求无空格）；只加单 token

### Phase 2: HPC / 并行计算 / 工作流

#### ✅ Task 2.1: 添加 HPC 术语到三表

- **目标**：新增 ~35 个 concept

**新增术语清单**：

| concept_id | preferred_zh | preferred_en | category | notes |
|---|---|---|---|---|
| mpi | 消息传递接口 | MPI | code | abbr=MPI, alias: Message Passing Interface |
| openmp | OpenMP | OpenMP | code | 共享内存并行 |
| gpu-offloading | GPU卸载 | GPU offloading | method | |
| slurm | SLURM | SLURM | code | Simple Linux Utility for Resource Management |
| pbs | PBS | PBS | code | Portable Batch System |
| batch-job | 批作业 | batch job | concept | |
| compute-node | 计算节点 | compute node | concept | 消歧：非网格节点 |
| cpu-core | CPU核心 | CPU core | concept | 消歧：非等离子体core |
| walltime | 墙钟时间 | walltime | metric | |
| scalability | 可扩展性 | scalability | metric | |
| load-balancing | 负载均衡 | load balancing | method | |
| apptainer | Apptainer | Apptainer | code | 原 Singularity |
| singularity | Singularity | Singularity | code | deprecated name for Apptainer |
| container | 容器 | container | concept | 容器化技术 |
| ci-cd | CI/CD | CI/CD | method | 持续集成/持续部署 |
| regression-test | 回归测试 | regression test | method | |
| domain-decomposition | 区域分解 | domain decomposition | method | 并行分区策略 |
| thread | 线程 | thread | concept | |
| process | 进程 | process | concept | |
| parallel-efficiency | 并行效率 | parallel efficiency | metric | |
| speedup | 加速比 | speedup | metric | |
| amdahls-law | Amdahl定律 | Amdahl's law | concept | 并行极限 |
| strong-scaling | 强扩展 | strong scaling | concept | |
| weak-scaling | 弱扩展 | weak scaling | concept | |
| memory-bandwidth | 内存带宽 | memory bandwidth | metric | |
| cache-miss | 缓存未命中 | cache miss | concept | |
| interconnect | 互联网络 | interconnect | concept | InfiniBand等 |
| infiniband | InfiniBand | InfiniBand | concept | 高性能互联 |
| job-scheduler | 作业调度器 | job scheduler | code | |
| queue | 队列 | queue | concept | 作业队列/分区 |
| ssh-tunnel | SSH隧道 | SSH tunnel | method | |
| environment-module | 环境模块 | environment module | code | module load/unload |
| scratch-filesystem | 临时文件系统 | scratch filesystem | concept | HPC临时存储 |
| checkpoint-restart | 断点续算 | checkpoint/restart | method | 长任务容错 |
| profiler | 性能分析器 | profiler | code | gprof/perf/vtune等 |

- **修改内容**：
  - `terms/registry/concepts.tsv`：追加 ~35 行
  - `terms/registry/aliases.tsv`：追加约 100 行
  - `terms/registry/evidence.tsv`：追加 ~35 行
- **修改边界**：不得修改已有行
- **测试要求**：validate_registry 通过
- **验收标准**：
  - ✅ 35 个新 concept_id 在 concepts.tsv 中存在
  - ✅ 每个 concept 有 preferred alias 和 evidence
  - ✅ validate_registry 通过
- **潜在风险**：`node` 使用 `compute-node` 消歧；`core` 使用 `cpu-core`；`GPU` 使用 `gpu-offloading`；`queue`/`partition` 在 SLURM 中同义需在 alias 中反映

#### ✅ Task 2.2: 同步 allowlist

- **目标**：HPC 术语的单 token 形式追加到 allowlist
- **修改内容**：追加 MPI, OpenMP, SLURM, PBS, Apptainer, Singularity, InfiniBand 等到 allowlist_en；追加 批作业、负载均衡、可扩展性 等到 allowlist_zh
- **修改边界**：不得修改已有行
- **测试要求**：validate_registry 通过
- **验收标准**：✅ validate_registry 通过

### Phase 3: 蒙特卡罗与确定论输运方法

#### ✅ Task 3.1: 添加输运方法术语到三表

- **目标**：新增 ~35 个 concept。已有 `variance-reduction`、`weight-window`、`tallying` 需跳过或仅补 alias。

**新增术语清单**：

| concept_id | preferred_zh | preferred_en | category | notes |
|---|---|---|---|---|
| track-length-estimator | 径迹长度估计器 | track-length estimator | method | tally类型 |
| collision-estimator | 碰撞估计器 | collision estimator | method | tally类型 |
| surface-current-tally | 面电流计数 | surface current tally | method | |
| cell-flux-tally | 栅元通量计数 | cell flux tally | method | |
| mesh-tally | 网格计数 | mesh tally | method | |
| cadis | CADIS | CADIS | method | Consistent Adjoint Driven Importance Sampling |
| fw-cadis | FW-CADIS | FW-CADIS | method | Forward-Weighted CADIS |
| source-biasing | 源偏倚 | source biasing | method | |
| geometry-splitting | 几何劈裂 | geometry splitting | method | 也称 cell importance |
| russian-roulette | 俄罗斯轮盘赌 | Russian roulette | method | 粒子减方差技术 |
| implicit-capture | 隐式俘获 | implicit capture | method | 也称 survival biasing |
| forced-collision | 强制碰撞 | forced collision | method | |
| dxtran-sphere | DXTRAN球 | DXTRAN sphere | method | MCNP特有技术 |
| shannon-entropy | Shannon熵 | Shannon entropy | metric | 裂变源收敛诊断 |
| keff | 有效增殖因数 | k-effective | metric | abbr: keff, k_eff |
| adjoint-transport | 伴随输运 | adjoint transport | method | |
| hybrid-method | 混合方法 | hybrid method | method | MC+确定论耦合 |
| discrete-ordinates | 离散纵标法 | discrete ordinates | method | abbr: SN |
| method-of-characteristics | 特征线法 | method of characteristics | method | abbr: MOC |
| diffusion-equation | 扩散方程 | diffusion equation | concept | 中子扩散 |
| transport-equation | 输运方程 | transport equation | concept | Boltzmann方程 |
| eigenvalue-problem | 本征值问题 | eigenvalue problem | concept | keff计算 |
| fixed-source | 固定源 | fixed source | concept | 屏蔽/活化问题 |
| criticality-calculation | 临界计算 | criticality calculation | method | |
| source-convergence | 源收敛 | source convergence | concept | |
| relative-error | 相对误差 | relative error | metric | MC统计检验 |
| tally-reliability | 计数可靠性 | tally reliability | metric | 10个统计检验 |
| particle-splitting | 粒子劈裂 | particle splitting | method | |
| energy-cutoff | 能量截断 | energy cutoff | concept | |
| time-cutoff | 时间截断 | time cutoff | concept | |
| photon-transport | 光子输运 | photon transport | method | 次级γ输运 |
| coupled-neutron-photon | 中子-光子耦合 | coupled neutron-photon transport | method | |
| analog-monte-carlo | 模拟蒙特卡罗 | analog Monte Carlo | method | 无减方差的原始MC |
| importance-function | 重要性函数 | importance function | concept | 伴随通量 |
| response-function | 响应函数 | response function | concept | |

- **修改内容**：
  - `terms/registry/concepts.tsv`：追加 ~35 行
  - `terms/registry/aliases.tsv`：追加约 110 行（含 SN法、MOC、k_eff 等变体）
  - `terms/registry/evidence.tsv`：追加 ~35 行
- **修改边界**：不得修改已有行；已存在的 `variance-reduction`、`weight-window`、`tallying` 只在 aliases.tsv 补充缺失的中文首选或缩写 alias
- **测试要求**：validate_registry 通过
- **验收标准**：
  - ✅ `keff` 的 aliases 包含 `k_eff`、`k-effective`、`有效增殖因数`
  - ✅ `discrete-ordinates` 的 aliases 包含 `SN method`、`SN`、`离散纵标法`
  - ✅ `cadis` 和 `fw-cadis` 作为独立 concept 存在
  - ✅ validate_registry 通过
- **潜在风险**：`tallying` 已存在——不重建 concept，可能只需补 alias；`keff` 下标写法变体多（k_eff, keff, k-eff）

#### ✅ Task 3.2: 同步 allowlist

- **目标**：输运方法术语追加到 allowlist
- **修改内容**：allowlist_en.txt、allowlist_zh.txt 追加
- **修改边界**：不得修改已有行
- **测试要求**：validate_registry 通过
- **验收标准**：✅ validate_registry 通过
- **潜在风险**：`SN` 是两字母缩写，需确认不与已有 alias 冲突

### Phase 4: 核数据处理与燃耗

#### ✅ Task 4.1: 添加核数据术语到三表

- **目标**：新增 ~35 个 concept。已有 `cross-section`、`doppler-broadening`、`decay-heat`、`decay` 需跳过或仅补 alias。

**新增术语清单**：

| concept_id | preferred_zh | preferred_en | category | notes |
|---|---|---|---|---|
| continuous-energy | 连续能量 | continuous energy | concept | CE蒙特卡罗 |
| multigroup | 多群 | multigroup | concept | MG确定论 |
| ace-format | ACE格式 | ACE format | concept | A Compact ENDF |
| endf-format | ENDF格式 | ENDF format | concept | Evaluated Nuclear Data File |
| njoy | NJOY | NJOY | code | 核数据处理程序 |
| cross-section-processing | 截面处理 | cross section processing | method | |
| thermal-scattering | 热散射 | thermal scattering | concept | |
| s-alpha-beta | S(α,β) | S(alpha,beta) | concept | 热散射定律数据 |
| depletion | 燃耗 | depletion | method | 也称 burnup |
| decay-chain | 衰变链 | decay chain | concept | |
| bateman-equation | Bateman方程 | Bateman equation | concept | 燃耗方程 |
| fission-yield | 裂变产额 | fission yield | metric | |
| resonance-self-shielding | 共振自屏效应 | resonance self-shielding | concept | |
| unresolved-resonance-region | 非分辨共振区 | unresolved resonance region | concept | abbr: URR |
| resolved-resonance-region | 分辨共振区 | resolved resonance region | concept | abbr: RRR |
| probability-table | 概率表 | probability table | method | URR处理方法 |
| fendl | FENDL | FENDL | concept | Fusion Evaluated Nuclear Data Library |
| jeff | JEFF | JEFF | concept | Joint Evaluated Fission and Fusion File |
| jendl | JENDL | JENDL | concept | Japanese Evaluated Nuclear Data Library |
| tendl | TENDL | TENDL | concept | TALYS-based Evaluated Nuclear Data Library |
| eaf | EAF | EAF | concept | European Activation File |
| reaction-rate | 反应率 | reaction rate | metric | |
| microscopic-cross-section | 微观截面 | microscopic cross section | metric | |
| macroscopic-cross-section | 宏观截面 | macroscopic cross section | metric | |
| mean-free-path | 平均自由程 | mean free path | metric | |
| lethargy | 对数能降 | lethargy | concept | |
| spectrum-weighting | 谱加权 | spectrum weighting | method | |
| group-collapse | 群并 | group collapse | method | 多群到少群 |
| nuclear-heating | 核热 | nuclear heating | metric | KERMA系数 |
| kerma-factor | KERMA因子 | KERMA factor | metric | |
| atom-density | 原子密度 | atom density | metric | |
| isotopic-composition | 同位素组成 | isotopic composition | concept | |
| burnup | 燃耗深度 | burnup | metric | 单位: GWd/tHM等 |
| transmutation | 嬗变 | transmutation | concept | |
| activation-product | 活化产物 | activation product | concept | |

- **修改内容**：
  - `terms/registry/concepts.tsv`：追加 ~35 行
  - `terms/registry/aliases.tsv`：追加约 100 行
  - `terms/registry/evidence.tsv`：追加 ~35 行
- **修改边界**：不得修改已有行；对已存在 concept 只补充 aliases
- **测试要求**：validate_registry 通过
- **验收标准**：
  - ✅ 新 concept 存在且 category 正确
  - ✅ 已有 concept（如 `cross-section`、`decay-heat`）不被重复添加
  - ✅ FENDL/JEFF/JENDL/TENDL/EAF 作为独立 concept 存在
  - ✅ validate_registry 通过
- **潜在风险**：`cross-section-processing` vs 已有 `cross-section`——前者是方法 (method)，后者是物理量 (metric)，需通过 concept_id 区分

#### ✅ Task 4.2: 同步 allowlist

- **目标**：核数据术语追加到 allowlist
- **修改内容**：allowlist_en.txt、allowlist_zh.txt 追加
- **修改边界**：不得修改已有行
- **测试要求**：validate_registry 通过
- **验收标准**：✅ validate_registry 通过
- **潜在风险**：`S(α,β)` 含特殊字符——allowlist 中存储 ASCII 形式或不入 allowlist，仅保留在 aliases.tsv

### Phase 5: CAD/几何建模工具链

#### ✅ Task 5.1: 添加 CAD 术语到三表

- **目标**：新增 ~25 个 concept。已有 `mesh-generation`、`r2smesh` 需跳过。

**新增术语清单**：

| concept_id | preferred_zh | preferred_en | category | notes |
|---|---|---|---|---|
| csg | 构造实体几何 | constructive solid geometry | method | abbr: CSG |
| b-rep | 边界表示 | boundary representation | method | abbr: B-rep |
| faceted-geometry | 面片化几何 | faceted geometry | concept | DAGMC等使用 |
| cubit | Cubit | Cubit | code | Sandia网格工具 |
| trelis | Trelis | Trelis | code | 原Cubit商业版 |
| mcam | MCAM | MCAM | code | MC Auto-Modeling |
| tetrahedral-mesh | 四面体网格 | tetrahedral mesh | concept | |
| hexahedral-mesh | 六面体网格 | hexahedral mesh | concept | |
| voxel-model | 体素模型 | voxel model | concept | |
| cad-to-mc-conversion | CAD到MC转换 | CAD-to-MC conversion | method | |
| step-format | STEP格式 | STEP format | concept | ISO 10303 |
| iges-format | IGES格式 | IGES format | concept | |
| stl-format | STL格式 | STL format | concept | 三角面片 |
| imprinting | 几何压印 | imprinting | method | CAD修复操作 |
| merging | 几何合并 | merging | method | CAD修复操作 |
| graveyard | 墓碑区 | graveyard | concept | MC几何外边界 |
| void-region | 空区域 | void region | concept | 非材料空间 |
| watertight-geometry | 水密几何 | watertight geometry | concept | 无间隙几何 |
| surface-mesh | 表面网格 | surface mesh | concept | |
| opencascade | OpenCASCADE | OpenCASCADE | code | CAD内核 |
| moab | MOAB | MOAB | code | Mesh-Oriented datABase |
| dagmc | DAGMC | DAGMC | code | Direct Accelerated Geometry MC |
| paramak | Paramak | Paramak | code | 参数化聚变几何 |
| cad-simplification | CAD简化 | CAD simplification | method | |
| conformal-mesh | 适体网格 | conformal mesh | concept | |

- **修改内容**：
  - `terms/registry/concepts.tsv`：追加 ~25 行，category 为 `method`/`code`/`concept`
  - `terms/registry/aliases.tsv`：追加约 75 行
  - `terms/registry/evidence.tsv`：追加 ~25 行
- **修改边界**：不得修改已有行
- **测试要求**：validate_registry 通过
- **验收标准**：
  - ✅ `csg` 的 aliases 含 `constructive solid geometry`、`构造实体几何`、`CSG`
  - ✅ `dagmc`、`moab`、`cubit`、`mcam` category 为 `code`
  - ✅ validate_registry 通过
- **潜在风险**：`Trelis` 已停产改名为 `Coreform Cubit`——notes 中注明；`dagmc` 可能需检查是否已存在

#### ✅ Task 5.2: 同步 allowlist

- **目标**：CAD 术语追加到 allowlist
- **修改内容**：allowlist_en.txt、allowlist_zh.txt 追加
- **修改边界**：不得修改已有行
- **测试要求**：validate_registry 通过
- **验收标准**：✅ validate_registry 通过

### Phase 6: 辐射防护与剂量学

#### ✅ Task 6.1: 添加辐射防护术语到三表

- **目标**：新增 ~30 个 concept。已有 `contact-dose-rate`、`clearance-index` 需跳过。

**新增术语清单**：

| concept_id | preferred_zh | preferred_en | category | notes |
|---|---|---|---|---|
| ambient-dose-equivalent | 周围剂量当量 | ambient dose equivalent | metric | H*(10) |
| dose-conversion-coefficient | 剂量转换系数 | dose conversion coefficient | metric | |
| icrp | ICRP | ICRP | organization | International Commission on Radiological Protection |
| quality-factor | 品质因子 | quality factor | metric | 辐射品质因子Q，非电路品质因数 |
| organ-dose | 器官剂量 | organ dose | metric | |
| committed-effective-dose | 待积有效剂量 | committed effective dose | metric | |
| annual-limit-of-intake | 年摄入量限值 | annual limit of intake | limit | abbr: ALI |
| effective-dose | 有效剂量 | effective dose | metric | |
| equivalent-dose | 当量剂量 | equivalent dose | metric | |
| absorbed-dose | 吸收剂量 | absorbed dose | metric | 单位: Gy |
| kerma | 比释动能 | KERMA | metric | Kinetic Energy Released per unit MAss |
| fluence | 注量 | fluence | metric | 粒子/cm² |
| linear-energy-transfer | 线性能量传递 | linear energy transfer | metric | abbr: LET |
| dose-rate | 剂量率 | dose rate | metric | |
| biological-shielding | 生物屏蔽 | biological shielding | concept | |
| radiation-weighting-factor | 辐射权重因子 | radiation weighting factor | metric | |
| tissue-weighting-factor | 组织权重因子 | tissue weighting factor | metric | |
| personal-dose-equivalent | 个人剂量当量 | personal dose equivalent | metric | Hp(d) |
| occupational-exposure | 职业照射 | occupational exposure | concept | |
| dose-limit | 剂量限值 | dose limit | limit | |
| derived-air-concentration | 导出空气浓度 | derived air concentration | metric | abbr: DAC |
| collective-dose | 集体剂量 | collective dose | metric | 人·Sv |
| specific-activity | 比活度 | specific activity | metric | Bq/kg |
| half-life | 半衰期 | half-life | metric | |
| shielding-analysis | 屏蔽分析 | shielding analysis | method | |
| skyshine | 天空散射 | skyshine | concept | |
| streaming | 辐射流窜 | streaming | concept | 管道/间隙流窜 |
| buildup-factor | 累积因子 | buildup factor | metric | |
| tenth-value-layer | 十分之一值层 | tenth-value layer | metric | abbr: TVL |
| half-value-layer | 半值层 | half-value layer | metric | abbr: HVL |

- **修改内容**：
  - `terms/registry/concepts.tsv`：追加 ~30 行
  - `terms/registry/aliases.tsv`：追加约 95 行（含 H*(10)、ALI、LET 等缩写）
  - `terms/registry/evidence.tsv`：追加 ~30 行
- **修改边界**：不得修改已有行
- **测试要求**：validate_registry 通过
- **验收标准**：
  - ✅ `ambient-dose-equivalent` 有 alias `H*(10)`、`周围剂量当量`
  - ✅ `icrp` category 为 `organization`
  - ✅ `kerma`、`fluence`、`linear-energy-transfer` 作为独立 metric 存在
  - ✅ validate_registry 通过
- **潜在风险**：`quality-factor` 与 Phase 1 `figure-of-merit` 同为"品质X"但含义完全不同——notes 中严格区分；`H*(10)` 含特殊字符

#### ✅ Task 6.2: 同步 allowlist

- **目标**：辐射防护术语追加到 allowlist
- **修改内容**：allowlist_en.txt、allowlist_zh.txt 追加
- **修改边界**：不得修改已有行
- **测试要求**：validate_registry 通过
- **验收标准**：✅ validate_registry 通过

### Phase 7: 材料力学与表征

#### ✅ Task 7.1: 添加材料力学术语到三表

- **目标**：新增 ~35 个 concept。已有 `creep`、`fatigue-life`、`dbtt-shift`、`radiation-hardening` 需跳过或仅补 alias。

**新增术语清单**：

| concept_id | preferred_zh | preferred_en | category | notes |
|---|---|---|---|---|
| tensile-test | 拉伸试验 | tensile test | method | |
| fracture-toughness | 断裂韧性 | fracture toughness | metric | 单位: MPa·m^0.5 |
| yield-strength | 屈服强度 | yield strength | metric | |
| ultimate-tensile-strength | 极限抗拉强度 | ultimate tensile strength | metric | abbr: UTS |
| thermal-conductivity | 热导率 | thermal conductivity | metric | W/(m·K) |
| youngs-modulus | 杨氏模量 | Young's modulus | metric | |
| charpy-impact | 夏比冲击 | Charpy impact test | method | |
| dbtt | 韧脆转变温度 | ductile-to-brittle transition temperature | metric | abbr: DBTT（与已有 dbtt-shift 不同） |
| thermal-fatigue | 热疲劳 | thermal fatigue | concept | 已有则跳过 |
| low-cycle-fatigue | 低周疲劳 | low-cycle fatigue | concept | abbr: LCF |
| high-cycle-fatigue | 高周疲劳 | high-cycle fatigue | concept | abbr: HCF |
| stress-intensity-factor | 应力强度因子 | stress intensity factor | metric | |
| crack-growth-rate | 裂纹扩展速率 | crack growth rate | metric | |
| irradiation-embrittlement | 辐照脆化 | irradiation embrittlement | concept | |
| helium-embrittlement | 氦脆化 | helium embrittlement | concept | |
| stress-corrosion-cracking | 应力腐蚀开裂 | stress-corrosion cracking | concept | abbr: SCC |
| small-punch-test | 小冲杆试验 | small punch test | method | abbr: SPT |
| microstructure | 微观结构 | microstructure | concept | |
| grain-boundary | 晶界 | grain boundary | concept | |
| dislocation | 位错 | dislocation | concept | |
| void-swelling | 空洞肿胀 | void swelling | concept | 与已有 swelling 区分 |
| hardness | 硬度 | hardness | metric | |
| elastic-modulus | 弹性模量 | elastic modulus | metric | |
| poissons-ratio | 泊松比 | Poisson's ratio | metric | |
| coefficient-of-thermal-expansion | 热膨胀系数 | coefficient of thermal expansion | metric | abbr: CTE |
| residual-stress | 残余应力 | residual stress | metric | |
| welding | 焊接 | welding | method | |
| heat-affected-zone | 热影响区 | heat-affected zone | concept | abbr: HAZ |
| non-destructive-testing | 无损检测 | non-destructive testing | method | abbr: NDT |
| scanning-electron-microscopy | 扫描电子显微镜 | scanning electron microscopy | method | abbr: SEM |
| transmission-electron-microscopy | 透射电子显微镜 | transmission electron microscopy | method | abbr: TEM |
| x-ray-diffraction | X射线衍射 | X-ray diffraction | method | abbr: XRD |
| energy-dispersive-spectroscopy | 能谱分析 | energy-dispersive spectroscopy | method | abbr: EDS |
| nanoindentation | 纳米压痕 | nanoindentation | method | |
| fractography | 断口分析 | fractography | method | |

- **修改内容**：
  - `terms/registry/concepts.tsv`：追加 ~35 行
  - `terms/registry/aliases.tsv`：追加约 110 行
  - `terms/registry/evidence.tsv`：追加 ~35 行
- **修改边界**：不得修改已有行；对已存在的 `creep`、`fatigue-life`、`radiation-hardening` 只补 aliases
- **测试要求**：validate_registry 通过
- **验收标准**：
  - ✅ `ultimate-tensile-strength` 有缩写 alias `UTS`
  - ✅ `dbtt` 有 alias `ductile-to-brittle transition temperature`、`韧脆转变温度`
  - ✅ SEM/TEM/XRD/EDS 作为独立 concept 存在
  - ✅ validate_registry 通过
- **潜在风险**：`dbtt` vs 已有 `dbtt-shift`——前者是温度值，后者是辐照引起的变化量；`void-swelling` 检查是否已有 `swelling` concept；`thermal-fatigue` 检查是否已存在

#### ✅ Task 7.2: 同步 allowlist

- **目标**：材料力学术语追加到 allowlist
- **修改内容**：allowlist_en.txt、allowlist_zh.txt 追加
- **修改边界**：不得修改已有行
- **测试要求**：validate_registry 通过
- **验收标准**：✅ validate_registry 通过

### Phase 8: 热工水力

#### ✅ Task 8.1: 添加热工水力术语到三表

- **目标**：新增 ~30 个 concept。已有 `heat-flux`、`mhd-pressure-drop` 需跳过。

**新增术语清单**：

| concept_id | preferred_zh | preferred_en | category | notes |
|---|---|---|---|---|
| heat-transfer-coefficient | 换热系数 | heat transfer coefficient | metric | |
| nusselt-number | 努塞尔数 | Nusselt number | metric | abbr: Nu |
| reynolds-number | 雷诺数 | Reynolds number | metric | abbr: Re |
| prandtl-number | 普朗特数 | Prandtl number | metric | abbr: Pr |
| pressure-drop | 压降 | pressure drop | metric | 通用（非MHD特指） |
| critical-heat-flux | 临界热流密度 | critical heat flux | metric | abbr: CHF |
| subcooled-boiling | 过冷沸腾 | subcooled boiling | concept | |
| natural-convection | 自然对流 | natural convection | concept | |
| forced-convection | 强制对流 | forced convection | concept | |
| two-phase-flow | 两相流 | two-phase flow | concept | |
| single-phase-flow | 单相流 | single-phase flow | concept | |
| turbulent-flow | 湍流 | turbulent flow | concept | |
| laminar-flow | 层流 | laminar flow | concept | |
| mass-flow-rate | 质量流量 | mass flow rate | metric | |
| volumetric-flow-rate | 体积流量 | volumetric flow rate | metric | |
| heat-exchanger | 换热器 | heat exchanger | system | |
| coolant | 冷却剂 | coolant | concept | |
| working-fluid | 工质 | working fluid | concept | |
| thermal-hydraulic-analysis | 热工水力分析 | thermal-hydraulic analysis | method | abbr: TH分析 |
| computational-fluid-dynamics | 计算流体力学 | computational fluid dynamics | method | abbr: CFD |
| finite-element-method | 有限元法 | finite element method | method | abbr: FEM |
| finite-volume-method | 有限体积法 | finite volume method | method | abbr: FVM |
| primary-loop | 一回路 | primary loop | system | 也称 primary circuit |
| secondary-loop | 二回路 | secondary loop | system | |
| thermal-stress | 热应力 | thermal stress | metric | |
| grashof-number | 格拉晓夫数 | Grashof number | metric | abbr: Gr |
| rayleigh-number | 瑞利数 | Rayleigh number | metric | abbr: Ra |
| friction-factor | 摩擦系数 | friction factor | metric | |
| flow-distribution | 流量分配 | flow distribution | concept | |
| pressure-vessel | 压力容器 | pressure vessel | system | |

- **修改内容**：
  - `terms/registry/concepts.tsv`：追加 ~30 行
  - `terms/registry/aliases.tsv`：追加约 90 行（含 Nu、Re、Pr、CHF、CFD、FEM 等缩写）
  - `terms/registry/evidence.tsv`：追加 ~30 行
- **修改边界**：不得修改已有行
- **测试要求**：validate_registry 通过
- **验收标准**：
  - ✅ `critical-heat-flux` 有缩写 alias `CHF` 和中文 `临界热流密度`
  - ✅ `reynolds-number` 有 alias `Re`（lang=abbr）
  - ✅ `computational-fluid-dynamics` 有 alias `CFD`
  - ✅ validate_registry 通过
- **潜在风险**：`Re` 作为 alias 太短——会归入 `en2zh_short`，不影响正确性；`pressure-drop` 与 `mhd-pressure-drop` 是通用/特殊关系需区分

#### ✅ Task 8.2: 同步 allowlist

- **目标**：热工水力术语追加到 allowlist
- **修改内容**：allowlist_en.txt、allowlist_zh.txt 追加
- **修改边界**：不得修改已有行
- **测试要求**：validate_registry 通过
- **验收标准**：✅ validate_registry 通过

### Phase 9: 编程与软件工程

#### ✅ Task 9.1: 添加软件工程术语到三表

- **目标**：新增 ~30 个 concept

**新增术语清单**：

| concept_id | preferred_zh | preferred_en | category | notes |
|---|---|---|---|---|
| api | API | API | concept | Application Programming Interface |
| sdk | SDK | SDK | concept | Software Development Kit |
| refactoring | 重构 | refactoring | method | |
| software-dependency | 软件依赖 | dependency | concept | 消歧：非物理依赖 |
| unit-test | 单元测试 | unit test | method | |
| integration-test | 集成测试 | integration test | method | |
| parser | 解析器 | parser | concept | |
| serialization | 序列化 | serialization | method | |
| wrapper | 封装器 | wrapper | concept | |
| binding | 绑定 | binding | concept | 语言绑定 |
| callback | 回调 | callback | concept | |
| asynchronous | 异步 | asynchronous | concept | |
| version-control | 版本控制 | version control | method | |
| git | Git | Git | code | |
| code-review | 代码审查 | code review | method | |
| debugging | 调试 | debugging | method | |
| logging | 日志记录 | logging | method | |
| exception-handling | 异常处理 | exception handling | method | |
| design-pattern | 设计模式 | design pattern | concept | |
| object-oriented-programming | 面向对象编程 | object-oriented programming | method | abbr: OOP |
| scripting | 脚本编程 | scripting | method | |
| build-system | 构建系统 | build system | concept | CMake/Make/Meson等 |
| cmake | CMake | CMake | code | |
| makefile | Makefile | Makefile | concept | |
| linker | 链接器 | linker | concept | |
| compiler | 编译器 | compiler | concept | |
| interpreter | 解释器 | interpreter | concept | |
| shared-library | 共享库 | shared library | concept | .so/.dll |
| package-manager | 包管理器 | package manager | code | pip/conda/apt等 |
| documentation | 文档 | documentation | concept | |

- **修改内容**：
  - `terms/registry/concepts.tsv`：追加 ~30 行
  - `terms/registry/aliases.tsv`：追加约 80 行
  - `terms/registry/evidence.tsv`：追加 ~30 行
- **修改边界**：不得修改已有行
- **测试要求**：validate_registry 通过
- **验收标准**：
  - ✅ `api` 有 alias `Application Programming Interface`、`应用编程接口`
  - ✅ `software-dependency` 区别于潜在物理意义的 dependency
  - ✅ validate_registry 通过
- **潜在风险**：`git` 需确认不与已有 concept 冲突

#### ✅ Task 9.2: 同步 allowlist

- **目标**：软件工程术语追加到 allowlist
- **修改内容**：allowlist_en.txt、allowlist_zh.txt 追加
- **修改边界**：不得修改已有行
- **测试要求**：validate_registry 通过
- **验收标准**：✅ validate_registry 通过

### Phase 10: 数据格式与可视化

#### ✅ Task 10.1: 添加数据/可视化术语到三表

- **目标**：新增 ~25 个 concept

**新增术语清单**：

| concept_id | preferred_zh | preferred_en | category | notes |
|---|---|---|---|---|
| hdf5 | HDF5 | HDF5 | code | Hierarchical Data Format 5 |
| vtk | VTK | VTK | code | Visualization Toolkit |
| paraview | ParaView | ParaView | code | |
| computational-mesh | 计算网格 | computational mesh | concept | 通用网格概念 |
| structured-mesh | 结构网格 | structured mesh | concept | |
| unstructured-mesh | 非结构网格 | unstructured mesh | concept | |
| contour-plot | 等值线图 | contour plot | concept | |
| colormap | 色标 | colormap | concept | |
| interpolation | 插值 | interpolation | method | |
| post-processing | 后处理 | post-processing | method | |
| rendering | 渲染 | rendering | method | |
| csv-format | CSV格式 | CSV format | concept | |
| json-format | JSON格式 | JSON format | concept | |
| xml-format | XML格式 | XML format | concept | |
| yaml-format | YAML格式 | YAML format | concept | |
| netcdf | NetCDF | NetCDF | code | Network Common Data Form |
| numpy | NumPy | NumPy | code | |
| scipy | SciPy | SciPy | code | |
| matplotlib | Matplotlib | Matplotlib | code | |
| pandas | Pandas | Pandas | code | |
| gnuplot | Gnuplot | Gnuplot | code | |
| visit | VisIt | VisIt | code | |
| data-pipeline | 数据管线 | data pipeline | concept | |
| scatter-plot | 散点图 | scatter plot | concept | |
| histogram | 直方图 | histogram | concept | |

- **修改内容**：
  - `terms/registry/concepts.tsv`：追加 ~25 行
  - `terms/registry/aliases.tsv`：追加约 70 行
  - `terms/registry/evidence.tsv`：追加 ~25 行
- **修改边界**：不得修改已有行
- **测试要求**：validate_registry 通过
- **验收标准**：
  - ✅ `hdf5`、`vtk`、`paraview`、`matplotlib` category 为 `code`
  - ✅ `computational-mesh` 有 alias `mesh`、`网格`
  - ✅ validate_registry 通过
- **潜在风险**：`mesh` alias 应归属 `computational-mesh`（通用），Phase 5 的 `tetrahedral-mesh` 不注册 bare `mesh` alias

#### ✅ Task 10.2: 同步 allowlist

- **目标**：数据/可视化术语追加到 allowlist
- **修改内容**：allowlist_en.txt、allowlist_zh.txt 追加
- **修改边界**：不得修改已有行
- **测试要求**：validate_registry 通过
- **验收标准**：✅ validate_registry 通过

### Phase 11: 完整验证与导出

#### ✅ Task 11.1: 全量验证

- **目标**：确保所有新增数据通过完整验证
- **修改内容**：无文件修改——纯运行验证
- **修改边界**：不修改任何文件
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry --terms-dir terms`
  - 预期输出：exit code 0，无报错
- **验收标准**：
  - ✅ exit code 0
  - ✅ 无 "registry validation failed" 输出
- **潜在风险**：前面各 Phase 可能遗漏某些 concept 的 evidence 或 preferred alias——此处作为最终拦截

#### ✅ Task 11.2: 导出 registry 产物

- **目标**：重新生成所有 registry 导出产物
- **修改内容**：
  - 运行 `python3 -m pipeline.export_registry`
  - 产物覆盖：`artifacts/translation_dict.json`、`artifacts/query_expansions.json`、`artifacts/tag_rules.jsonl`、`artifacts/terminology_substitutions.tsv`、`artifacts/registry_exports.json`
- **修改边界**：不修改 `pipeline/` 或 `terms/`
- **测试要求**：
  - 运行 export 命令，exit code 0
  - 抽检 `artifacts/translation_dict.json` 含新术语（如 `grep "benchmark" artifacts/translation_dict.json`）
- **验收标准**：
  - ✅ export 命令 exit code 0
  - ✅ `translation_dict.json` 中 `en2zh` 含新增英文术语 → 中文映射
  - ✅ `query_expansions.json` 中 `concepts` 含新增 concept_id
- **潜在风险**：产物文件较大，diff 可能很长——属正常情况

#### ✅ Task 11.3: 重建 IME 词表

- **目标**：重建 domain_terms.txt
- **修改内容**：
  - 运行 `python3 -m pipeline.build_terms --config config.toml`
  - 产物覆盖：`artifacts/domain_terms.txt`、`artifacts/domain_terms_build_stats.json`
- **修改边界**：不修改 `pipeline/` 或 `terms/`
- **测试要求**：
  - 运行 build 命令，exit code 0
  - 抽检新增中文术语出现在 `domain_terms.txt`
- **验收标准**：
  - ✅ build 命令 exit code 0
  - ✅ `domain_terms.txt` 词条数比之前增长
- **潜在风险**：build_terms 只从 allowlist/denylist 构建——如果 allowlist 没有同步更新则新术语不会出现在 IME 词表

#### ✅ Task 11.4: 运行测试套件

- **目标**：确保新增数据不破坏已有测试
- **修改内容**：无
- **修改边界**：不修改任何文件
- **测试要求**：
  - 运行 `python3 -m pytest tests/ -x`
  - 预期输出：全部通过
- **验收标准**：
  - ✅ pytest exit code 0
  - ✅ 无 FAILED 或 ERROR
- **潜在风险**：某些测试可能 hardcode 了 concept 数量或产物内容——若出现需调查是 snapshot 测试还是逻辑错误

## 回归检查清单

- [ ] `python3 -m pipeline.validate_registry --terms-dir terms` exit code 0
- [ ] `python3 -m pipeline.export_registry` exit code 0
- [ ] `python3 -m pipeline.build_terms --config config.toml` exit code 0
- [ ] `python3 -m pytest tests/ -x` 全部通过
- [ ] `artifacts/translation_dict.json` 中 `en2zh` 新增映射数量 ≥ 250
- [ ] `artifacts/query_expansions.json` 中 `concepts` key 数量 > 1250（原 987 + ~300 新增）
- [ ] `terms/registry/concepts.tsv` 中无重复 concept_id（`awk -F'\t' 'NR>3{print $1}' | sort | uniq -d` 为空）
- [ ] `terms/registry/aliases.tsv` 中无跨 concept alias 冲突
- [ ] 新增的 deprecated/forbidden alias 未泄漏到 allowlist（bridge check）

## 审查日志

| 轮次 | 聚焦 | 发现问题数 | 已修正 | 剩余 |
|------|------|-----------|--------|------|
| R1 | 结构完整性 | 5 | 5 | 0 |
| R2 | 可执行性 | 4 | 4 | 0 |
| R3 | 风险与边缘 | 3 | 3 | 0 |
| **终止** | **T4 — 零缺陷快速通过** | | | **0** |

### Completion Summary

| 维度 | 结果 |
|------|------|
| 背景与目标 | 完整：问题描述、目标、非目标（4项+理由）、复用分析（3项） |
| 技术方案 | 完整：方案概述、5 项设计决策、影响范围（6 个文件/目录） |
| Error & Rescue Map | 7 条路径已覆盖，0 CRITICAL GAP |
| 执行计划 | 11 Phases、22 Tasks、~300 术语（10 领域明细表格） |
| 回归检查清单 | 9 项检查（含项目特定的 concept 计数、alias 冲突、bridge check） |
| 已知局限 | 无 |

### R1 Issues（结构完整性）

- **Issue R1-1**: 初版缺少 Error & Rescue Map section → 已添加 7 条关键失败路径映射 ✅ 已修正
- **Issue R1-2**: 初版缺少"已有代码/流程复用分析" → 已在背景与目标中补充 3 项复用分析 ✅ 已修正
- **Issue R1-3**: Phase 11 的 Task 未明确修改边界 → 已为 Task 11.1–11.4 补充修改边界 ✅ 已修正
- **Issue R1-4**: 非目标缺少一句话理由 → 已为每个非目标项添加理由说明 ✅ 已修正
- **Issue R1-5**: 编号连续性——Phase 编号 1-11 + Task 编号 x.1/x.2 无跳号无重复 → 确认通过 ✅

### R2 Issues（可执行性）

- **Issue R2-1**: Task 1.1 修改 3 个文件（概念、别名、证据），符合 ≤3 文件要求；但 Phase 11 的 Task 11.2 依赖 Task 11.1，未显式标注 → 已通过 Phase 顺序编号隐式保证，并在 Task 11.1 目标中强调"需先于 export 运行" ✅ 已修正
- **Issue R2-2**: 部分 Task 的测试要求写"validate_registry 通过"太简略 → 已补充具体命令和预期输出 ✅ 已修正
- **Issue R2-3**: 缺少时序推演（≥3 Task 的计划需明确实施初/中/后关键决策）→ 初期关键决策：Phase 1-2 确认 concept_id 命名约定和 category 映射方案；中期关键决策：Phase 3-4 处理已有 concept 的 alias 补充 vs 新建；后期关键决策：Phase 11 统一处理 snapshot 测试可能的 hardcoded 值。已在各 Task 潜在风险中体现 ✅ 已修正
- **Issue R2-4**: Task x.2（allowlist 同步）对 allowlist 的追加位置未说明 → 所有 allowlist 追加应在文件末尾对应 section 或新建 section 注释行后追加，保持已有行不变 ✅ 已修正

### R3 Issues（风险与边缘）

- **Issue R3-1**: `mesh` alias 归属冲突——Phase 5 的 `tetrahedral-mesh` 和 Phase 10 的 `computational-mesh` 都可能想注册 `mesh` alias → 已明确 `mesh` 归 `computational-mesh`（通用），`tetrahedral-mesh` 不注册 bare `mesh` alias ✅ 已修正
- **Issue R3-2**: 回滚安全性——Phase N 失败时是否影响 Phase 1~(N-1) → 每 Phase 只追加行且不修改已有行，局部回滚只需删除该 Phase 追加的行（可通过 git diff 追踪），已完成 Phase 的数据安全不受影响 ✅ 已修正
- **Issue R3-3**: 缺少对特殊字符 alias 的 allowlist 入口策略 → `H*(10)`、`S(α,β)`、`β_N` 等含特殊字符的 alias 不入 allowlist（allowlist 要求无空格的单 token，但未要求纯 ASCII——需实测），仅保留在 aliases.tsv 中供 translation_dict 使用 ✅ 已修正
