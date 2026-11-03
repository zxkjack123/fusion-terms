# T4.8 组 G7 语义复核（PM #5184 / M1）

- 报告日期: 2026-11-03（`date` 实跑: Tue Nov 3 12:22:26 PM CST 2026）
- 复核范围: `docs/reviews/t5184/m1-sample-manifest.tsv` 中 `group=G7` 的 8 行，逐行原样使用（group / batch_scope / concept_id / sha256_16 未改写、未增删、未替换样本）
- 判定口径: PASS / FAIL / UNDECIDABLE；依据为真实语义（en 定义是否准确刻画概念、zh↔en 是否等价、是否与同族概念冲突或重复登记），非格式
- 只读声明: 本报告为唯一写入文件；术语 / 定义 / 语料文件全部只读；未运行任何写 git 命令（无 add/commit/checkout/stash/restore/push），未改计划

## 路径更正记录（如实）

1. 计划给定证据路径 `.github/plans/t4973-batches/gbt4960_9_diff.tsv` **不成立**：`.github/plans/t4973-batches/` 目录确实存在，但其中**无** `gbt4960_9_diff.tsv`（该目录仅有 `category-map-*.tsv`、`*.ids`、`README.md` 等）。
2. 以实存文件为准：全仓唯一同名文件为 `artifacts/terminology_sources/gbt4960_9_diff.tsv`（562 行，表头 `# term / status / matched_concept_id / term_id / zh / abbr / definition`）。本报告 GB/T 依据一律取自该文件，行号指向该文件。
3. IAEA / ITER 原始表实存路径：`artifacts/terminology_sources/iaea_safety_glossary_raw.tsv`（877 行，表头 `# term, definition`）、`artifacts/terminology_sources/iter_glossary_raw.tsv`（143 行，表头 `# term, definition, fetch_date`）。
4. 概念表 / 定义表实存路径：`terms/registry/concepts.tsv`（表头 `# concept_id, category, preferred_zh, preferred_en, preferred_abbr, status, notes, source`）、`terms/registry/definitions.tsv`（表头 `# concept_id, lang, definition, source`）——与计划一致，无需更正。

## 来源可得性声明（影响 5 字段中的来源子项）

1. **corpus（主导来源）**：8 行 `concepts.tsv` 的 `source` 字段取值均为 `corpus`，故依据按任务规定取该行 `notes` 原文及行号（另附整行逐字）。**8/8 可得**。
2. **GB/T-4960.9（子来源）**：以 `matched_concept_id` 命中为判据，8 个 cid 在 `gbt4960_9_diff.tsv` 的 `matched_concept_id` 列 **0 命中**；再以英文面形（digital engineering / stimulated Raman / scenario development / systems engineering / field-reversed / preferential sputter / cross-beam / grid integration）与中文面形（数字工程 / 受激拉曼散射 / 运行场景开发 / 系统工程 / 场反稳定性 / 择优溅射 / 交叉光束能量传递 / 电网集成）双向复核，562 行内 **0 命中**（唯一近邻为 `gbt4960_9_diff.tsv:523` `term=engineering design activity`，语义域为"工程设计活动"，非本组任何概念）。
3. **IAEA/ITER（子来源）**：IAEA 877 行 term 列对 8 概念 **0 命中**（检得 `human factors engineering`@372、`reference scenario`@669、`scenario`@747 等孤立词条，语境为辐射安全/事件序列分析，与本组概念不同形不等义）；ITER 143 行 term 列对 8 概念 **0 命中**（含 `Beamlines`@11、`Electron Beam`@47、`Neutral Beam Injection`@92 等束系统词条，均非 CBET/SRS 等本组概念）。
4. **http(s) URL**：8 行 `source` 字段均非 URL（=corpus），无 URL 来源可取；本会话无网络取回，一律写 `不可得: 无网络取回`，不虚构片段。
5. **主导一致性**：`原始语料`（source 主导项）不可得条数 = **0**，故 `判定: UNDECIDABLE` 条数 = **0**（硬规则一致）。子来源（GB/T / IAEA / ITER / URL）未命中按任务规定一律记 `不可得: <原因>`，共 24 处（8 样本 × 3 子来源）；**子来源缺失不参与上述等式**（主导项 8/8 可得，不得据此判 UNDECIDABLE），亦不落 PASS 门槛。8 条 PASS 均为主来源（notes）可得且定义语义与 notes 相容的情形，不存在"源不可得却 PASS"的条目。

## 输入行原样引用（8/8，与 manifest G7 行逐行同序）

| # | group | batch_scope | concept_id | sha256_16 |
|---|---|---|---|---|
| G7-01 | G7 | w1_b_b27..w1_b_b31 | digital-engineering | 00a313ddf25439a9 |
| G7-02 | G7 | w1_b_b27..w1_b_b31 | stimulated-raman-scattering | 00ababc52522d792 |
| G7-03 | G7 | w1_b_b27..w1_b_b31 | scenario-development | 0268ed907f5640e0 |
| G7-04 | G7 | w1_b_b27..w1_b_b31 | systems-engineering | 082e2ccdbe2b4b1a |
| G7-05 | G7 | w1_b_b27..w1_b_b31 | frc-stability | 0922cc3d1a69f092 |
| G7-06 | G7 | w1_b_b27..w1_b_b31 | preferential-sputtering | 09ffc870f02bbad4 |
| G7-07 | G7 | w1_b_b27..w1_b_b31 | cbet | 0ad9ede50c8a160a |
| G7-08 | G7 | w1_b_b27..w1_b_b31 | grid-integration | 0dfbea5067066532 |

---

### G7-01 digital-engineering

样本: group=G7 | batch_scope=w1_b_b27..w1_b_b31 | concept_id=digital-engineering | sha256_16=00a313ddf25439a9
原始语料: source=corpus → `terms/registry/concepts.tsv:3130` notes 原文「Model-based engineering approach using integrated digital models for fusion plant design and lifecycle management」；整行逐字（列间为制表符）`digital-engineering	concept	数字工程	digital engineering		active	Model-based engineering approach using integrated digital models for fusion plant design and lifecycle management	corpus`
语料源·GB/T-4960.9: 不可得: matched_concept_id 未命中；`gbt4960_9_diff.tsv` 562 行以英文面形 `digital`/`engineering` 与中文面形 `数字工程` 检索 0 命中（唯一近邻 `gbt4960_9_diff.tsv:523` `term=engineering design activity | status=new | id=2.4.34 | zh=工程设计活动`，语义域为工程设计活动，非本概念）
语料源·IAEA/ITER: 不可得: IAEA `iaea_safety_glossary_raw.tsv`（877 行）term 列无 digital engineering 命中；ITER `iter_glossary_raw.tsv`（143 行）无命中
语料源·URL: 不可得: 该行 source=corpus 非 http(s) URL，无 URL 来源可取；本会话无网络取回
定义文本: en「A model-based engineering approach that uses integrated digital models for plant design and lifecycle management.」`definitions.tsv:4013`；zh「数字工程：以集成数字模型开展电站设计与全寿期管理的模型化工程方法。」`definitions.tsv:4014`（两行 source 列均为 corpus）
适用性推理: ①en 以三个限定语闭合概念：方法类型限定 "A model-based engineering approach"、手段限定 "uses integrated digital models"、对象限定 "for plant design and lifecycle management"；与 notes 逐词对位，唯 notes 的 "fusion plant" 在 en 中被简化为 "plant"（丢失 "fusion" 域限定），属域泛化而非失准（该表为聚变术语表，域已隐含）。②zh 与 en 逐句对位：「以集成数字模型」「开展电站设计与全寿期管理」「模型化工程方法」分别对应 "uses integrated digital models"/"for plant design and lifecycle management"/"A model-based engineering approach"，无增义、漏义或误译；zh 同样未带"聚变"限定。③同族核对：`concepts.tsv:3123` systems-engineering notes「Interdisciplinary approach to design, integrate, and manage complex fusion plant systems over their life cycles」与本概念共享 "over their life cycles / 全寿期" 措辞，但判别性限定语不同（"model-based … integrated digital models" vs "interdisciplinary approach"），二者在定义层可切分；`concepts.tsv:929` digital-twin「Real-time digital simulation mirror of fusion device」是不同对象（孪生体实例 vs 工程方法），不构成冲突。残余观察（不改变判定）：en/zh 一并丢失 notes 的 "fusion" 限定，建议后续在定义中补回 "fusion plant" 以固化域边界。
判定: PASS
证据锚点: concepts.tsv:3130；definitions.tsv:4013；definitions.tsv:4014

### G7-02 stimulated-raman-scattering

样本: group=G7 | batch_scope=w1_b_b27..w1_b_b31 | concept_id=stimulated-raman-scattering | sha256_16=00ababc52522d792
原始语料: source=corpus → `terms/registry/concepts.tsv:2984` notes 原文「Laser-plasma instability: scattering from electron plasma waves」；整行逐字（列间为制表符）`stimulated-raman-scattering	concept	受激拉曼散射	stimulated Raman scattering	SRS	active	Laser-plasma instability: scattering from electron plasma waves	corpus`
语料源·GB/T-4960.9: 不可得: matched_concept_id 未命中；英文面形 `stimulated Raman`/`Raman`/`brillouin` 与中文面形 `受激拉曼散射` 在 562 行内 0 命中
语料源·IAEA/ITER: 不可得: IAEA term 列无 Raman 命中；ITER 143 行 term 列无 Raman 命中
语料源·URL: 不可得: 该行 source=corpus 非 http(s) URL，无 URL 来源可取；本会话无网络取回
定义文本: en「A laser-plasma instability involving scattering of laser light from electron plasma waves.」`definitions.tsv:5531`；zh「受激拉曼散射：激光受电子等离子体波散射的一类激光—等离子体不稳定性。」`definitions.tsv:5532`（两行 source 列均为 corpus）
适用性推理: ①en 以 "A laser-plasma instability" 定类属、"involving scattering of laser light from electron plasma waves" 锁定散射介质（电子等离子体波）；相比 notes 多出 "of laser light"（明确被散射对象为激光），语义一致，准确刻画 SRS 在 LPI 语境中的对象，且未把三波耦合、频率下移等附加机制混入定义。②zh 与 en 逐句对位：「激光受电子等离子体波散射」↔"scattering of laser light from electron plasma waves"、「一类激光—等离子体不稳定性」↔"A laser-plasma instability"，无增义、漏义或误译。③同族核对：`concepts.tsv:2983` stimulated-brillouin-scattering（en `definitions.tsv:5529`「A laser-plasma instability involving backward scattering of laser light from ion acoustic waves.」）与本概念仅以散射介质限定语区隔（"electron plasma waves" vs "ion acoustic waves"），互斥可辨；`concepts.tsv:191` laser-plasma-interaction、`definitions.tsv:4968` parametric-instability 均为上位类，本概念为其子类，无重复登记。残余观察：SBS 定义带方向限定 "backward"，本概念 en 未给方向限定（SRS 可前/后向散射），差异属颗粒度不一致、不构成冲突。
判定: PASS
证据锚点: concepts.tsv:2984；definitions.tsv:5531；definitions.tsv:5532

### G7-03 scenario-development

样本: group=G7 | batch_scope=w1_b_b27..w1_b_b31 | concept_id=scenario-development | sha256_16=0268ed907f5640e0
原始语料: source=corpus → `terms/registry/concepts.tsv:3093` notes 原文「Design and optimization of tokamak operational scenarios」；整行逐字（列间为制表符）`scenario-development	concept	运行场景开发	scenario development		active	Design and optimization of tokamak operational scenarios	corpus`
语料源·GB/T-4960.9: 不可得: matched_concept_id 未命中；英文面形 `scenario` 与中文面形 `运行场景开发`/`场景` 在 562 行内 0 命中
语料源·IAEA/ITER: 不可得: IAEA term 列含孤立词条 `scenario`（`iaea_safety_glossary_raw.tsv:747`）与 `reference scenario`（:669），但语境为事件序列/安全分析（`:706` "the probability of occurrence of scenario or event sequence i"），非 "scenario development"，归一化后不同形不等义；ITER 143 行无 scenario 命中
语料源·URL: 不可得: 该行 source=corpus 非 http(s) URL，无 URL 来源可取；本会话无网络取回
定义文本: en「The design and optimization of tokamak operational scenarios.」`definitions.tsv:5392`；zh「运行场景开发：托卡马克运行场景的设计与优化。」`definitions.tsv:5393`（两行 source 列均为 corpus）
适用性推理: ①en 以 "of tokamak operational scenarios" 限定对象域（托卡马克 + 运行场景），把概念锚定为放电运行方案的设计与寻优活动，未越界到装置设计或运行实施阶段；但定义主体 "design and optimization" 与概念名 "development" 构成同义展开，判别性信息主要来自 "tokamak operational" 这一域限定，属定义颗粒度偏粗（近循环），非失准。②zh 与 en 逐句对位：「托卡马克运行场景的设计与优化」↔"The design and optimization of tokamak operational scenarios"，无增义、漏义或误译；zh 首选名「运行场景开发」与 en "scenario development" 术语一致。③同族核对：`concepts.tsv:324` hybrid-scenario、`concepts.tsv:323` advanced-tokamak、`concepts.tsv:698` steady-state-high-beta、`concepts.tsv:321` steady-state-operation 描述的是**具体运行场景**，本概念描述的是**场景开发活动**（过程概念），上位/实例关系清晰，无重复登记；`concepts.tsv:1127` parametric-study 是通用扫描方法，域不同。残余观察：定义近似名称展开，建议补入场景交付物要素（电流爬升、位形、加热配比）以提高判别力。
判定: PASS
证据锚点: concepts.tsv:3093；definitions.tsv:5392；definitions.tsv:5393

### G7-04 systems-engineering

样本: group=G7 | batch_scope=w1_b_b27..w1_b_b31 | concept_id=systems-engineering | sha256_16=082e2ccdbe2b4b1a
原始语料: source=corpus → `terms/registry/concepts.tsv:3123` notes 原文「Interdisciplinary approach to design, integrate, and manage complex fusion plant systems over their life cycles」；整行逐字（列间为制表符）`systems-engineering	concept	系统工程	systems engineering		active	Interdisciplinary approach to design, integrate, and manage complex fusion plant systems over their life cycles	corpus`
语料源·GB/T-4960.9: 不可得: matched_concept_id 未命中；英文面形 `systems engineering` 与中文面形 `系统工程` 在 562 行内 0 命中（唯一近邻仍为 `:523` engineering design activity）
语料源·IAEA/ITER: 不可得: IAEA term 列有 `human factors engineering`（`iaea_safety_glossary_raw.tsv:372`），系人因工程另一学科，非 systems engineering；ITER 143 行无命中
语料源·URL: 不可得: 该行 source=corpus 非 http(s) URL，无 URL 来源可取；本会话无网络取回
定义文本: en「An interdisciplinary approach to designing, integrating and managing complex fusion plant systems over their life cycles.」`definitions.tsv:5598`；zh「系统工程：在寿期内设计、集成并管理复杂聚变电站系统的跨学科方法。」`definitions.tsv:5599`（两行 source 列均为 corpus）
适用性推理: ①en 以 "An interdisciplinary approach" 定方法属性、"complex fusion plant systems" 定作用对象、"over their life cycles" 定时间跨度，三点与 notes 逐词对位（design/integrate/manage ↔ designing/integrating/managing），准确刻画聚变电厂全寿期系统工程这一过程学科，且未混入数字模型手段。②zh 与 en 逐句对位：「在寿期内设计、集成并管理复杂聚变电站系统的跨学科方法」↔"An interdisciplinary approach to designing, integrating and managing complex fusion plant systems over their life cycles"，无增义、漏义或误译。③同族核对：`concepts.tsv:3130` digital-engineering 与本概念共享 "life cycle(s)/全寿期" 措辞，但判别语为 "model-based … integrated digital models"，属手段层子类，非同一概念；`concepts.tsv:2156` life-cycle-management（zh 全寿期管理，来源 IAEA）是管理活动、`concepts.tsv:525` balance-of-plant 是对象集合，均不与本定义等义。无重复登记或互斥冲突。残余观察：与 digital-engineering 存在"全寿期"措辞重叠，建议二者定义各补一条 is-a / 手段-对象 互指以固化边界。
判定: PASS
证据锚点: concepts.tsv:3123；definitions.tsv:5598；definitions.tsv:5599

### G7-05 frc-stability

样本: group=G7 | batch_scope=w1_b_b27..w1_b_b31 | concept_id=frc-stability | sha256_16=0922cc3d1a69f092
原始语料: source=corpus → `terms/registry/concepts.tsv:2946` notes 原文「Stability properties of field-reversed configurations including tilt and rotational modes」；整行逐字（列间为制表符）`frc-stability	concept	场反稳定性	FRC stability		active	Stability properties of field-reversed configurations including tilt and rotational modes	corpus`
语料源·GB/T-4960.9: 不可得: matched_concept_id 未命中；英文面形 `field-reversed` 与中文面形 `场反稳定性` 在 562 行内 0 命中
语料源·IAEA/ITER: 不可得: IAEA term 列无命中；ITER 143 行 term 列无 field-reversed 命中
语料源·URL: 不可得: 该行 source=corpus 非 http(s) URL，无 URL 来源可取；本会话无网络取回
定义文本: en「The stability properties of a field-reversed configuration, including tilt and rotational modes.」`definitions.tsv:4297`；zh「场反稳定性：场反位形的稳定性性质，包括倾斜模与旋转模。」`definitions.tsv:4298`（两行 source 列均为 corpus）
适用性推理: ①en 以 "of a field-reversed configuration" 定对象结构、"including tilt and rotational modes" 以穷举式限定把不稳定模具体化，将概念锚定为 FRC 位形的稳定性性质集合；与 notes 逐词对位（仅 configurations→configuration 单复数归一），准确且具判别力。②zh 与 en 逐句对位：「场反位形的稳定性性质，包括倾斜模与旋转模」↔"The stability properties of a field-reversed configuration, including tilt and rotational modes"，"properties/性质"、"including/包括" 一一对应，无增义、漏义或误译。③同族核对：`concepts.tsv:168` rotational-instability（en `definitions.tsv:5343`「An n=2 rotational mode that can grow in a field-reversed configuration and, if uncontrolled, degrades the plasma and limits its lifetime.」）与 `concepts.tsv:948` tilt-instability（en `definitions.tsv:5656`「A global CT/spheromak MHD instability of magnetic axis tilt.」）正是本定义 "including" 列举的两个具体模，属聚合性质 vs 具体模的上下位关系，列举内容与两行模名逐一对齐，不构成定义层重复；`concepts.tsv:162` field-reversed-configuration 为位形本体，对象不同。残余观察：tilt-instability 定义域写作 CT/spheromak（比 FRC 宽），两处域限定颗粒度不一致属他行问题，不改本判定。
判定: PASS
证据锚点: concepts.tsv:2946；definitions.tsv:4297；definitions.tsv:4298

### G7-06 preferential-sputtering

样本: group=G7 | batch_scope=w1_b_b27..w1_b_b31 | concept_id=preferential-sputtering | sha256_16=09ffc870f02bbad4
原始语料: source=corpus → `terms/registry/concepts.tsv:1679` notes 原文「Preferential ejection of lighter element from multi-component target」；整行逐字（列间为制表符）`preferential-sputtering	concept	择优溅射	preferential sputtering		active	Preferential ejection of lighter element from multi-component target	corpus`
语料源·GB/T-4960.9: 不可得: matched_concept_id 未命中；英文面形 `sputter` 与中文面形 `择优溅射` 在 562 行内 0 命中
语料源·IAEA/ITER: 不可得: IAEA term 列无 sputter 命中；ITER 143 行 term 列无 sputter 命中
语料源·URL: 不可得: 该行 source=corpus 非 http(s) URL，无 URL 来源可取；本会话无网络取回
定义文本: en「The preferential ejection of the lighter element from a multi-component target.」`definitions.tsv:5101`；zh「择优溅射：多组分靶中较轻元素被优先溅射出去。」`definitions.tsv:5102`（两行 source 列均为 corpus）
适用性推理: ①en 以 "preferential ejection" 定机制、"of the lighter element" 定成分选择性、"from a multi-component target" 定靶体条件，三限定语合起来准确刻画"溅射偏好随靶成分差异而偏向轻元素"这一现象，与 notes 逐词对位（仅补足冠词），未与一般溅射混淆。②zh 与 en 逐句对位：「多组分靶中较轻元素被优先溅射出去」↔"The preferential ejection of the lighter element from a multi-component target"，"preferential/优先"、"lighter element/较轻元素"、"multi-component/多组分" 对齐，无增义、漏义或误译。③同族核对：`concepts.tsv:82` sputtering（en `definitions.tsv:5503`「The ejection of atoms from a surface as a result of the impact of energetic particles…」）、`concepts.tsv:712` physical-sputtering（en `definitions.tsv:5021`「Ejection of surface atoms by energetic ion bombardment.」）、`concepts.tsv:1659` chemical-sputtering、`concepts.tsv:1674` self-sputtering 均不含"成分择优"限定，本概念凭 "lighter element"/"multi-component" 限定构成可辨子类，无定义层重合。残余观察：本概念 target/靶 与 ICF 语境 `concepts.tsv:178` fuel-capsule（zh 靶丸）存在"靶/target"词面碰撞，建议后续统一为"溅射靶/material target"以免跨域歧义（属术语面，不改判定）。
判定: PASS
证据锚点: concepts.tsv:1679；definitions.tsv:5101；definitions.tsv:5102

### G7-07 cbet

样本: group=G7 | batch_scope=w1_b_b27..w1_b_b31 | concept_id=cbet | sha256_16=0ad9ede50c8a160a
原始语料: source=corpus → `terms/registry/concepts.tsv:2982` notes 原文「Laser energy redistribution between crossing beams in hohlraum」；整行逐字（列间为制表符）`cbet	concept	交叉光束能量传递	cross-beam energy transfer	CBET	active	Laser energy redistribution between crossing beams in hohlraum	corpus`
语料源·GB/T-4960.9: 不可得: matched_concept_id 未命中；英文面形 `cross-beam`/`energy transfer` 与中文面形 `交叉光束能量传递` 在 562 行内 0 命中
语料源·IAEA/ITER: 不可得: IAEA term 列无命中；ITER 143 行 term 列含 `Beamlines`@11、`Electron Beam`@47、`Neutral Beam Injection`@92 等束系统词条，但均非 cross-beam energy transfer，不等义
语料源·URL: 不可得: 该行 source=corpus 非 http(s) URL，无 URL 来源可取；本会话无网络取回
定义文本: en「The redistribution of laser energy between beams that cross inside a hohlraum.」`definitions.tsv:3747`；zh「交叉光束能量传递：黑腔内相交光束之间的激光能量再分配。」`definitions.tsv:3748`（两行 source 列均为 corpus）
适用性推理: ①en 以 "redistribution of laser energy" 定现象、"between beams that cross" 定几何条件（相交）、"inside a hohlraum" 定环境；与 notes 逐词对位（crossing beams→beams that cross；in hohlraum→inside a hohlraum），准确刻画间接驱动黑腔内交叉光束间能量转移，且未把其物理机制（受激布里渊散射）混入定义。②zh 与 en 逐句对位：「黑腔内相交光束之间的激光能量再分配」↔"The redistribution of laser energy between beams that cross inside a hohlraum"、"黑腔"↔"hohlraum"，无增义、漏义或误译；zh 首选名「交叉光束能量传递」与 en "cross-beam energy transfer" 对应。③同族核对：`concepts.tsv:177` hohlraum（en `definitions.tsv:4448`「A high-Z cylindrical cavity used in indirect-drive inertial confinement fusion…」）是发生场所本体；`concepts.tsv:2983` stimulated-brillouin-scattering 是同一物理过程的 LPI 机制视角（SBS 限定 "backward scattering … from ion acoustic waves"，本概念限定 "beams that cross inside a hohlraum"），二者限定语不重叠，属"现象-机制"互补，无重复登记。残余观察：concept_id 取缩写 "cbet" 而非 preferred_en 全 slug "cross-beam-energy-transfer"，与同表 `stimulated-raman-scattering`/`stimulated-brillouin-scattering` 的全 slug 命名不一致（属 id 命名一致性，不涉语义）。
判定: PASS
证据锚点: concepts.tsv:2982；definitions.tsv:3747；definitions.tsv:3748

### G7-08 grid-integration

样本: group=G7 | batch_scope=w1_b_b27..w1_b_b31 | concept_id=grid-integration | sha256_16=0dfbea5067066532
原始语料: source=corpus → `terms/registry/concepts.tsv:3051` notes 原文「Technical and regulatory process of connecting a power plant to the grid」；整行逐字（列间为制表符）`grid-integration	concept	电网集成	grid integration		active	Technical and regulatory process of connecting a power plant to the grid	corpus`
语料源·GB/T-4960.9: 不可得: matched_concept_id 未命中；英文面形 `grid integration` 与中文面形 `电网集成` 在 562 行内 0 命中
语料源·IAEA/ITER: 不可得: IAEA term 列无 grid 命中；ITER 143 行 term 列无 grid 命中
语料源·URL: 不可得: 该行 source=corpus 非 http(s) URL，无 URL 来源可取；本会话无网络取回
定义文本: en「The technical and regulatory process of connecting a power plant to the electrical grid.」`definitions.tsv:4374`；zh「电网集成：把电站接入电网的技术与监管过程。」`definitions.tsv:4375`（两行 source 列均为 corpus）
适用性推理: ①en 以 "technical and regulatory process" 定概念类型（活动/过程，而非设施）、"of connecting a power plant to the electrical grid" 定对象与终态；与 notes 逐词对位（仅补 "electrical" 明确电网性质），准确刻画电厂并网这一技术与监管活动。②zh 与 en 逐句对位：「把电站接入电网的技术与监管过程」↔"The technical and regulatory process of connecting a power plant to the electrical grid"，"technical and regulatory/技术与监管"、"power plant/电站"、"electrical grid/电网" 对齐，无增义、漏义或误译。③同族核对（本组张力最强项）：`concepts.tsv:530` electrical-grid-connection（en `definitions.tsv:4104`「The interface between a fusion plant and the external power grid.」；zh `definitions.tsv:4105`「电网接入是聚变电厂与外部电网之间的接口。」）是本概念最邻近登记项，二者共享 "power plant ↔ grid" 对象，但定义类型限定语不同——本概念为 "process"（过程），530 为 "interface"（接口实体），故定义层可切分，不构成重复定义。残余观察：zh 首选名「电网集成」与 530 的「电网接入」在本语境近义，且 530 定义未限定为"接口点/接口规范"，存在边界漂移风险；建议 530 定义补 "physical/regulatory interface point" 类限定以固化与"过程"的区分（属他行建议，不改本判定）。
判定: PASS
证据锚点: concepts.tsv:3051；definitions.tsv:4374；definitions.tsv:4375

---

## 台账（FAIL / UNDECIDABLE）

本组 8 样本判定分布：PASS 8、FAIL 0、UNDECIDABLE 0。**无 FAIL / UNDECIDABLE 记录，故下表 0 行**（行数 = FAIL + UNDECIDABLE = 0，与硬规则"不可得行数(=0) == UNDECIDABLE 行数(=0)"一致）。

| D<n> | <cid> | <FAIL\|UNDECIDABLE> | 原因 |
|---|---|---|---|

（表内 0 条数据行；行数 = FAIL + UNDECIDABLE = 0）

## 备注与后续动作

1. 本报告**未**新建 .bib/引用，**未**修改任何术语数据文件；8 条 PASS 的"残余观察"属建议修复项（是否执行由 orchestrator/作者裁决），本 agent 只复核、不改术语数据。
2. 路径更正（任务给定 `.github/plans/t4973-batches/gbt4960_9_diff.tsv` 不成立；实际 `artifacts/terminology_sources/gbt4960_9_diff.tsv`）已在头部声明；建议后续任务书修正路径引用。
3. 派生观察（不改变本组判定、供他组/后续参考）：①`concepts.tsv:530` electrical-grid-connection 与 `concepts.tsv:3051` grid-integration 边界仅靠 "interface" vs "process" 区分，建议强化限定；②`concepts.tsv:3123` systems-engineering 与 `concepts.tsv:3130` digital-engineering 共享"全寿期"措辞，建议补互指；③`concepts.tsv:948` tilt-instability 定义域（CT/spheromak）比 `concepts.tsv:2946` frc-stability 的列举域（FRC）宽，建议统一；④`concepts.tsv:2982` cbet 的 concept_id 用缩写、与同族全 slug 命名不一致。

## AC 自检（实跑记录）

| AC 项 | 命令 | 实测 |
|---|---|---|
| 样本标题数 = 8 | `grep -c '^### ' <report>` | 8 |
| 判定三值行数 = 8 | `grep -cE '^判定: (PASS\|FAIL\|UNDECIDABLE)$' <report>` | 8（PASS 8 / FAIL 0 / UNDECIDABLE 0） |
| 四字段各 ≥8 | `grep -c '^样本: '` / `'^原始语料: '` / `'^定义文本: '` / `'^适用性推理: '` | 8 / 8 / 8 / 8（另 `^判定: ` 8、`^证据锚点: ` 8） |
| concepts.tsv 锚点 ≥8 | `grep -c 'concepts\.tsv:' <report>` | 24 |
| definitions.tsv 锚点 ≥16 | `grep -c 'definitions\.tsv:' <report>` | 21 |
| 不可得数 == UNDECIDABLE 数 | 主导项 `grep -c '^原始语料: 不可得'` vs `grep -c '^判定: UNDECIDABLE$'` | 0 == 0 |
| 台账行数 == FAIL+UNDECIDABLE | 台账数据行计数 vs 0 | 0 == 0 |
| git status 仅本 md 为新文件 | `git status --short` | 实测 2 行：`?? docs/reviews/t5184/m1-group-G7.md`（本次新增，唯一写入）、`?? .github/plans/5184-four-stage-closeout.md`（**既有未跟踪计划文件**，会话开始时即为此状态，本会话未改动）；本会话未改任何已跟踪文件（`git diff --stat` 为空） |
| 未运行写 git 命令 | — | 无 add/commit/checkout/stash/restore/push |
