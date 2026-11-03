# M4 — 小样目视核验：T0.4 / T0.5 修复后 10 行列语义（PM #5184 / S3 / T3.2）

> 证据来源：`docs/reviews/t5184/m4-sample.tsv`（T3.1，commit `4d8d003`，`concepts.tsv` 表头 + 10 行原样复制）。
> 生成时间：2026-11-03T11:34:08+08:00（`date -Iseconds`）；核验时 HEAD = `4d8d003`。
> 原始列与定义行均由 `awk -F'\t'` / `grep -nP` 现读现取，粘贴于每块的 `原始列:` 与 `定义文本:`，未做改写。

## §0 判定口径（先声明，后判定）

本报告的判定对象是**列语义**（M4 的原始诉求："中文/英文是否各归其位"），即逐列核对五件事：

| 列 | 核对内容 | PASS 口径 |
|---|---|---|
| COL2 `category` | 是否落在 `pipeline/validate_registry.py:_ALLOWED_CATEGORIES` 的 16 类内，且与该概念性质相符 | 类目正确且性质相符 |
| COL3 `preferred_zh` | 是否为中文名 | 含 CJK 且语义为该概念的中文称谓 |
| COL4 `preferred_en` | 是否为英文名/英文语符 | 全 ASCII 且语义为该概念的英文称谓 |
| COL7 `notes` | 是否在描述该概念（非他行内容、非空、非截断） | 描述对象与本行 id 一致 |
| COL8 `source` | 是否合理（与 notes 的文本体裁相符） | 与 notes 的实际来源性质不矛盾 |

**三值含义（严格按计划 D4）**：`PASS` = 列内容与列契约无矛盾；`FAIL` = 错位/错名/缺列/异语言（含类目与性质不符）；`UNDECIDABLE` = 该列的语义无法判定（须写 `待定原因:`）。

**本报告不覆盖**：`definitions.tsv` 的定义质量（占位模板、跨表 source 一致性）属**另一张表**、另一条承接线，逐条登记在 §3（O1–O5 / D1–D2），**不参与 M4 列语义判定**，但必须在汇总与状态行中可见。

## §1 抽样出处（确定性映射，可复现）

抽样口径来自计划 §S3：`category-map-shift99.tsv` 数据行 1/20/40/60/80（文件行 2/21/41/61/81）+ `category-map-sixcol80.tsv` 数据行 1/16/32/48/64（文件行 2/17/33/49/65）。映射落盘于 `/tmp/opencode/t5184-m4-sample-map.tsv`。

| # | 来源 | 数据行 / 文件行 | concept_id | 分配依据（原样） |
|---|---|---|---|---|
| 1 | category-map-shift99.tsv | 1 / 2 | appm | `sibling:dpa=metric（无量纲量）` |
| 2 | category-map-shift99.tsv | 20 / 21 | decay-storage | `fallback:concept（通用技术概念/现象/领域词，无单位非量纲）` |
| 3 | category-map-shift99.tsv | 40 / 41 | gas-production | `rule:metric` |
| 4 | category-map-shift99.tsv | 60 / 61 | neutron-flux-monitor | `sibling:ionization-chamber=device` |
| 5 | category-map-shift99.tsv | 80 / 81 | stiffening-grid | `sibling:back-plate=system（结构部件）` |
| 6 | category-map-sixcol80.tsv | 1 / 2 | poloidal-field-power-supply | `plan:同域系统（供电系统本体，含变流器/开关网络/耗能支路）` |
| 7 | category-map-sixcol80.tsv | 16 / 17 | tallying-efficiency | `rule:量（取得给定 tally 精度所需计算成本）` |
| 8 | category-map-sixcol80.tsv | 32 / 33 | roots-pump | `sibling:cryopump=device（真空泵硬件）` |
| 9 | category-map-sixcol80.tsv | 48 / 49 | divertor-erosion | `sibling:erosion/disruption-erosion/elm-induced-erosion=concept` |
| 10 | category-map-sixcol80.tsv | 64 / 65 | lithium-burnup | `sibling:burnup/burnup-fraction=metric` |

## §2 逐行逐列目视（10 行）

### appm
- 原始列: 1=[appm] 2=[metric] 3=[原子百万分率] 4=[appm] 5=[] 6=[active] 7=[Atomic parts per million: unit for measuring transmutation product concentration (He, H) or impurity levels in irradiated materials] 8=[corpus]
- 定义文本: en = `Fusion/nuclear engineering term corresponding to 'appm'.`；zh = `聚变/核工程术语，指“appm”这一技术概念。`（两行均为模板句，见 D1）
- 逐列适用性推理: COL2 metric 与该概念"原子浓度单位/量"的性质相符（非过程、非硬件）；COL3「原子百万分率」是 appm 的中文全称，确为中文（含 CJK，语义对应 atomic parts per million）；COL4「appm」为英文语符（全 ASCII），落英文列无语言错置；COL7 逐字为 "Atomic parts per million: unit for measuring transmutation product concentration (He, H) or impurity levels in irradiated materials"，描述对象正是本行 id，未串入他行 notes；COL8 corpus 与 notes 的完整描述句体裁一致。定义级语义不可用（模板占位），故本判定只依托列语言归属与 notes；命名形态问题记 O1。
判定: PASS
- 证据锚点: concepts.tsv:3209；definitions.tsv:5841,5842

### decay-storage
- 原始列: 1=[decay-storage] 2=[concept] 3=[衰变贮存] 4=[decay storage] 5=[] 6=[active] 7=[Interim storage period allowing short-lived radionuclides to decay to clearance levels before recycling or disposal] 8=[corpus]
- 定义文本: en = `Fusion/nuclear engineering term corresponding to 'decay storage'.`；zh = `聚变/核工程术语，指“decay storage”这一技术概念。`（模板句，见 D1）
- 逐列适用性推理: COL2 concept 与之相符——它是一种"暂存期/做法"式的通用技术概念，既非可测量值（metric）也非装置（device）；COL3「衰变贮存」为中文（CJK），与 en「decay storage」逐字对应、无增漏；COL4「decay storage」为英文小写短语，落英文列正确；COL7 描述 "Interim storage period allowing short-lived radionuclides to decay to clearance levels before recycling or disposal"，对象与本行 id 一致；COL8 corpus 与 notes 的完整英文描述句一致。注意 zh 定义模板把英文串 "decay storage" 嵌进了中文定义（D1 的表现之一），但那是 definitions 表的问题，不影响本行列归属。
判定: PASS
- 证据锚点: concepts.tsv:3189；definitions.tsv:5883,5884

### gas-production
- 原始列: 1=[gas-production] 2=[metric] 3=[气体产生] 4=[gas production] 5=[] 6=[active] 7=[Generation of helium and hydrogen gas in structural materials by transmutation reactions under neutron irradiation, measured in appm] 8=[corpus]
- 定义文本: en = `Fusion/nuclear engineering term corresponding to 'gas production'.`；zh = `聚变/核工程术语，指“gas production”这一技术概念。`（模板句，见 D1）
- 逐列适用性推理: COL2 metric 可成立——notes 末句 "measured in appm" 明确把它当**可测量的产气量**（同族另有 gas-production-rate=气体产额 表"率"，见 concepts.tsv:811），故类目与其"量"的用法相符，虽其 id 字面像过程；COL3「气体产生」为中文（CJK）且对应 en「gas production」；COL4 英文小写短语，落英文列正确；COL7 描述 "Generation of helium and hydrogen gas ... measured in appm"，对象与本行一致、无串行；COL8 corpus 与 notes 描述句体裁相符。量的中文命名层级（产生 vs 产额）另记 O4，不构成列归属缺陷。
判定: PASS
- 证据锚点: concepts.tsv:3208；definitions.tsv:5947,5948

### neutron-flux-monitor
- 原始列: 1=[neutron-flux-monitor] 2=[device] 3=[中子通量监测器] 4=[neutron flux monitor] 5=[] 6=[active] 7=[Detector system for real-time monitoring of neutron flux levels in and around a fusion device, used for power calibration and safety interlocks] 8=[corpus]
- 定义文本: en = `Fusion/nuclear engineering term corresponding to 'neutron flux monitor'.`；zh = `聚变/核工程术语，指“neutron flux monitor”这一技术概念。`（模板句，见 D1）
- 逐列适用性推理: COL2 device 与之相符——notes 称其为 "Detector system"，属硬件装置（同族 ionization-chamber 亦为 device）；COL3「中子通量监测器」为中文（CJK），对应 en「neutron flux monitor」，无增漏；COL4 英文小写短语落英文列正确；COL7 描述实时监测中子通量水平、用于功率刻度与安全联锁，对象与本行一致；COL8 corpus 与 notes 完整描述句相符。判定仅涉列归属，模板定义问题归 D1。
判定: PASS
- 证据锚点: concepts.tsv:3248；definitions.tsv:6001,6002

### stiffening-grid
- 原始列: 1=[stiffening-grid] 2=[system] 3=[加强筋格栅] 4=[stiffening grid] 5=[] 6=[active] 7=[Internal grid of ribs or plates within a blanket module providing structural rigidity against electromagnetic and pressure loads] 8=[corpus]
- 定义文本: en = `Fusion/nuclear engineering term corresponding to 'stiffening grid'.`；zh = `聚变/核工程术语，指“stiffening grid”这一技术概念。`（模板句，见 D1）
- 逐列适用性推理: COL2 system 与之相符——notes 明确是包层模块内部的"ribs or plates 组成的格栅"，属结构子系统（同族 back-plate 亦为 system）；COL3「加强筋格栅」为中文（CJK），对应 en「stiffening grid」；COL4 英文小写短语落英文列正确；COL7 描述其抵抗电磁与压力载荷、提供结构刚度，对象与本行一致、未串行；COL8 corpus 与 notes 描述句相符。模板定义归 D1，不影响列归属。
判定: PASS
- 证据锚点: concepts.tsv:3237；definitions.tsv:6069,6070

### poloidal-field-power-supply
- 原始列: 1=[poloidal-field-power-supply] 2=[system] 3=[极向场电源] 4=[Poloidal Field Power Supply] 5=[] 6=[active] 7=[Power supply system for PF coils [domain: electrical-power-systems]] 8=[corpus]
- 定义文本: en = `The electrical power supply system for the poloidal field coils.`；zh = `极向场电源：为极向场线圈供电的电源系统。`（definitions.tsv:6021/6022，source=corpus，非模板）
- 逐列适用性推理: COL2 system 与"电源系统"本体相符（category-map 依据为 plan:同域系统，含变流器/开关网络/耗能支路）；COL3「极向场电源」为中文（CJK），与 zh 定义逐字一致；COL4「Poloidal Field Power Supply」为英文（全 ASCII）落英文列正确，仅大小写风格另记 O2；COL7 描述 PF 线圈供电系统并以 `[domain: electrical-power-systems]` 标注域（T0.5 修复的预期形态，抽样 5 行均含该标记）；COL8 corpus 与该行 definitions 的 source=corpus 一致，来源自洽。
判定: PASS
- 证据锚点: concepts.tsv:3316；definitions.tsv:6021,6022

### tallying-efficiency
- 原始列: 1=[tallying-efficiency] 2=[metric] 3=[计数效率] 4=[Tallying Efficiency] 5=[] 6=[active] 7=[Metric quantifying the computational cost to achieve a given tally precision [domain: computational-methods]] 8=[corpus]
- 定义文本: en = `A metric quantifying the computational cost to achieve a given tally precision.`；zh = `计数效率：衡量达到给定计数精度所需计算成本的量度。`（definitions.tsv:6079/6080，source=corpus）
- 逐列适用性推理: COL2 metric 与之相符（en 定义直陈 "A metric quantifying the computational cost"）；COL3「计数效率」为中文（CJK）且与 zh 定义首词逐字一致，落中文列无错置；COL4「Tallying Efficiency」为英文（全 ASCII）落英文列正确，大小写风格记 O2；COL7 复述该量衡量取得给定 tally 精度所需计算成本，并带 `[domain: computational-methods]`，对象与本行一致；COL8 corpus 与该行 definitions 的 source=corpus 自洽。中文名与仪器学 counting efficiency 同形的歧义记 O3，不影响列归属。
判定: PASS
- 证据锚点: concepts.tsv:3331；definitions.tsv:6079,6080

### roots-pump
- 原始列: 1=[roots-pump] 2=[device] 3=[罗茨泵] 4=[Roots Pump] 5=[] 6=[active] 7=[Positive displacement vacuum pump using counter-rotating lobed rotors [domain: vacuum-technology]] 8=[corpus]
- 定义文本: en = `A positive displacement vacuum pump using counter-rotating lobed rotors.`；zh = `罗茨泵：利用反向旋转叶形转子实现容积式抽气的真空泵。`（definitions.tsv:6057/6058，source=corpus）
- 逐列适用性推理: COL2 device 与"真空泵硬件"相符（同族 cryopump=device）；COL3「罗茨泵」为中文（CJK），与 zh 定义首词逐字一致；COL4「Roots Pump」为英文（全 ASCII）落英文列正确，大小写记 O2；COL7 描述容积式真空泵与对转叶形转子，带 `[domain: vacuum-technology]`，对象与本行一致；COL8 corpus 与该行 definitions 的 source=corpus 一致。
判定: PASS
- 证据锚点: concepts.tsv:3347；definitions.tsv:6057,6058

### divertor-erosion
- 原始列: 1=[divertor-erosion] 2=[concept] 3=[偏滤器侵蚀] 4=[Divertor Erosion] 5=[] 6=[active] 7=[Material removal from divertor target surfaces due to plasma particle and heat flux bombardment [domain: divertor-physics]] 8=[corpus]
- 定义文本: en = `Material removal from divertor target surfaces due to plasma particle and heat flux bombardment.`；zh = `偏滤器侵蚀：偏滤器靶板表面在等离子体粒子与热流轰击下发生材料去除的过程。`（definitions.tsv:5901/5902，source=corpus）
- 逐列适用性推理: COL2 concept 与"材料去除过程/现象"相符（同族 erosion / disruption-erosion / elm-induced-erosion 均为 concept）；COL3「偏滤器侵蚀」为中文（CJK），与 zh 定义首词逐字一致；COL4「Divertor Erosion」为英文（全 ASCII）落英文列正确，大小写记 O2；COL7 完整描述靶板在粒子与热流轰击下的材料去除，带 `[domain: divertor-physics]`，对象与本行一致；COL8 corpus 与该行 definitions 的 source=corpus 一致。
判定: PASS
- 证据锚点: concepts.tsv:3363；definitions.tsv:5901,5902

### lithium-burnup
- 原始列: 1=[lithium-burnup] 2=[metric] 3=[锂消耗] 4=[Lithium Burnup] 5=[] 6=[active] 7=[Depletion of lithium-6 in breeding material due to neutron transmutation reactions [domain: breeding-material]] 8=[corpus]
- 定义文本: en = `Depletion of lithium-6 in ceramic breeder or liquid metal blankets caused by the 6Li(n,t)4He transmutation reaction during neutron irradiation.`；zh = `中子辐照过程中由 6Li(n,t)4He 嬗变反应引起的陶瓷增殖剂或液态金属包层中锂-6的消耗。`（definitions.tsv:1568/1569，source=internal:dict-improvements）
- 逐列适用性推理: COL2 metric 与"锂-6 贫化程度"的量性质相符（同族 burnup / burnup-fraction 均为 metric）；COL3「锂消耗」为中文（CJK）且与其 zh 定义末词"消耗"逐字对应；COL4「Lithium Burnup」为英文（全 ASCII）落英文列正确，大小写记 O2；COL7 描述增殖材料中锂-6 因嬗变反应的贫化，带 `[domain: breeding-material]`，对象与本行一致；COL8 corpus 与 notes 描述句体裁相符，但该行 definitions 的 source 为 internal:dict-improvements，跨表来源不一致记 D2。中文名与同族"燃耗"词族的偏差记 O5，属命名一致性、不属列归属缺陷。
判定: PASS
- 证据锚点: concepts.tsv:3379；definitions.tsv:1568,1569

## §3 观察项与跨表缺陷（不属 M4 列语义缺陷类别）

以下为本次逐行核验中**实际读到**的问题。它们不属于"错位/错名/缺列/异语言"四类列语义缺陷，故不改变 §2 的判定，但必须留痕并移交对应承接线；本节不授权任何数据修改。

| 编号 | 对象 | 事实（可复现） | 类别 | 建议承接 |
|---|---|---|---|---|
| O1 | appm | `concepts.tsv:3209` COL4=`appm`、COL5（abbr）为空；同类单位 `dpa`（`concepts.tsv:286`）为 en=`displacement per atom` + abbr=`dpa` | 命名形态口径不一致 | 术语规范化（不阻断 M4） |
| O2 | 6/10 行 | sixcol80 五行的 COL4 均为 Title Case（`Poloidal Field Power Supply` / `Tallying Efficiency` / `Roots Pump` / `Divertor Erosion` / `Lithium Burnup`），仓内多数 en 为小写短语 | 命名风格 | 术语规范化 |
| O3 | tallying-efficiency | COL3=`计数效率` 与仪器学 counting efficiency 同形，而本概念实为"取得给定 tally 精度所需计算成本" | 术语歧义 | 术语规范化 |
| O4 | gas-production | COL3=`气体产生` 为动作短语，同族 metric `gas-production-rate`（`concepts.tsv:811`）用"气体产额" | 量的中文命名层级不稳 | 术语规范化 |
| O5 | lithium-burnup | COL3=`锂消耗`，而同族 `burnup`=`燃耗深度`、`burnup-fraction`=`燃耗份额` 用"燃耗"词族 | 术语族一致性 | 术语规范化 |
| D1 | definitions.tsv（跨表） | en 模板占位 `Fusion/nuclear engineering term corresponding to '<X>'.` 共 **99** 行；zh 模板占位 `聚变/核工程术语，指“<X>”这一技术概念。` 共 **131** 行（=`grep -c` 实测）。本次 10 行样本命中 **5** 行：appm / decay-storage / gas-production / neutron-flux-monitor / stiffening-grid（definitions.tsv:5841-5842 / 5883-5884 / 5947-5948 / 6001-6002 / 6069-6070，source 均 `internal:dict-improvements`） | **定义质量（严重）** | 定义质量线（M1 / 5072 承接）；与 W1 无关：占位 id 集（131）与 W1 的 756 id 交集 = **0**，B7「W1 占位 0」仍成立 |
| D2 | lithium-burnup | `concepts.tsv:3379` COL8=`corpus`，而 `definitions.tsv:1568/1569` source=`internal:dict-improvements` | 跨表 source 不一致 | 定义质量线 |

- 交叉核对说明：D1 的 5 行占位均**不在** W1（`comm -12` 交集 0），说明该缺陷位于 W1 之外的 dict-improvements 批量，不推翻 B7；同时也说明 §2 中这 5 行的"定义级语义"不可用，故其判定只依托列语言归属与 `notes`——这一点已在各行 `逐列适用性推理` 内逐条写明，未以"定义正确"作为 PASS 依据。
- 观察项均**不阻断** M4：M4 的判据是列归属，而 O1–O5 是同一语言内的命名偏好/一致性，D1–D2 是另一张表的问题；三者都不构成"中文写进英文列"或"列错位/缺列"。
