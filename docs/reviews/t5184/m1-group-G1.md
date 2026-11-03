# T4.2 组 G1 语义复核（PM #5184 / M1）

- 报告日期: 2026-11-03（`date` 实跑: Tue Nov 3 11:54:09 AM CST 2026）
- 复核范围: `docs/reviews/t5184/m1-sample-manifest.tsv` 中 `group=G1` 的 8 行，逐行原样使用（group / batch_scope / concept_id / sha256_16 未改写、未增删）
- 判定口径: PASS / FAIL / UNDECIDABLE；依据为真实语义（en 定义是否准确、zh↔en 是否等价、是否与同族概念冲突），非格式
- 只读声明: 本报告为唯一写入文件；术语/定义/语料文件全部只读，未运行任何写 git 命令（无 add/commit/checkout/stash/push）

## 输入行原样引用（8/8）

| # | group | batch_scope | concept_id | sha256_16 |
|---|---|---|---|---|
| G1-01 | G1 | w1_a_b01..w1_b_b01 | fishbone-instability | 04a3398851b475d2 |
| G1-02 | G1 | w1_a_b01..w1_b_b01 | faraday-rotation | 0c45755cd4e9ab81 |
| G1-03 | G1 | w1_a_b01..w1_b_b01 | turbulent-transport | 0f3d535727a8819f |
| G1-04 | G1 | w1_a_b01..w1_b_b01 | plateau-regime | 1058e378f9ebf824 |
| G1-05 | G1 | w1_a_b01..w1_b_b01 | shielding-penetration | 13e22b5268c3eaa9 |
| G1-06 | G1 | w1_a_b01..w1_b_b01 | drift-wave | 1557406e87dec6cc |
| G1-07 | G1 | w1_a_b01..w1_b_b01 | lawson-criterion | 186069579aa42cb2 |
| G1-08 | G1 | w1_a_b01..w1_b_b01 | poloidal-field-coil | 186feff855bef930 |

## 路径与来源可得性声明（影响 5 字段中的来源子项）

1. **corpus（主导来源）**：8 行 `concepts.tsv` 的 `source` 字段取值均为 `corpus`，故依据按任务规定取 `terms/registry/concepts.tsv` 该行 `notes` 原文及行号（另附整行逐字）。8/8 可得。
2. **GB/T-4960.9**：任务给定路径 `.github/plans/t4973-batches/gbt4960_9_diff.tsv` **在仓内不存在**（`find` 全仓仅命中 1 处同名文件）；证据取自仓内唯一同名文件 `artifacts/terminology_sources/gbt4960_9_diff.tsv`（562 行，表头 `# term / status / matched_concept_id / term_id / zh / abbr / definition`）。该文件名 `gbt4960_9_diff.tsv` 已在各条 `语料源·GB/T-4960.9` 中保留，路径差异详见下表行号引用。
3. **IAEA/ITER**：`artifacts/terminology_sources/iaea_safety_glossary_raw.tsv`（877 行，`# term, definition`）与 `artifacts/terminology_sources/iter_glossary_raw.tsv`（143 行，`# term, definition, fetch_date`）。归一化命中判定：term 列/定义列大小写不敏感匹配（含单复数与所有格归一化，如 `Lawson's Criteria`→Lawson、`Poloidal Field Coils`→poloidal field coil）。IAEA 侧对 8 个概念 **0 命中**（连中文面形 `遮蔽|漂移|劳森|湍流|法拉第|坪|鱼骨|极向` 亦 0 命中）；ITER 侧命中 2/8（lawson-criterion、poloidal-field-coil）。
4. **http(s) URL**：8 行 `source` 字段均非 URL（=corpus），无 URL 来源可取；且本会话无网络工具，按规则一律写 `不可得: 无网络访问`，不假装取回。
5. **主导一致性**：`原始语料`（source 主导项）不可得条数 = 0，故 `判定: UNDECIDABLE` 条数 = 0（硬规则一致）。子来源（GB/T / IAEA / ITER / URL）未命中按任务规定一律以 `不可得: <原因>` 记录，共 27 处；**子来源缺失不参与上述等式**（主导项 8/8 可得，故不得据此判 UNDECIDABLE），亦不落 PASS 门槛判定——PASS 的 5 条均为子来源缺失或跨源张力不改变其定义语义的情形，任一"源不可得却 PASS"的条目均不存在。

---

### G1-01 fishbone-instability

样本: group=G1 | batch_scope=w1_a_b01..w1_b_b01 | concept_id=fishbone-instability | sha256_16=04a3398851b475d2
原始语料: source=corpus → `terms/registry/concepts.tsv:540` notes 原文「Fast-ion driven internal kink instability with fishbone-shaped magnetic signature」；整行逐字（列间为制表符）`fishbone-instability	concept	鱼骨模不稳定性	fishbone instability		active	Fast-ion driven internal kink instability with fishbone-shaped magnetic signature	corpus`
语料源·GB/T-4960.9: 不可得: matched_concept_id 未命中（`gbt4960_9_diff.tsv:105` `term=fishbones | status=new | matched_concept_id=（空） | id=2.1.104 | zh=鱼骨模`；status=new 即未并入本 cid，且英文面形 fishbones 与 preferred_en "fishbone instability" 不同形）
语料源·IAEA/ITER: 不可得: IAEA `iaea_safety_glossary_raw.tsv` 无命中；ITER `iter_glossary_raw.tsv` 无命中（143 条 term 列表中无 fishbone/fishbones）
语料源·URL: 不可得: 该行 source=corpus 非 http(s) URL，无 URL 来源可取；本会话无网络访问
定义文本: en「A magnetohydrodynamic instability (MHD) driven by energetic particles; in experiments a periodic bursting signal shaped like a fish bone has been observed.」`definitions.tsv:4255`；zh「高能粒子驱动的磁流体动力学不稳定性(MHD)，实验观测到像鱼骨形状的周期暴发信号。」`definitions.tsv:1103`（两行 source 列均为 GB/T-4960.9）
适用性推理: ①en 以限定语 "driven by energetic particles" 固定驱动源，以 "a periodic bursting signal shaped like a fish bone has been observed" 固定实验可观测特征，把概念锚定在 MHD 不稳定性的高能粒子驱动子类上，未越出该子类内涵（未声称 q=1 之外或无周期暴发），故准确刻画；但 notes 中的 "internal kink"（m=1/n=1 内扭曲模）限定语未进入定义文本，属细化不足而非失准。②zh 与 en 逐句对位：「高能粒子驱动」↔"driven by energetic particles"、「像鱼骨形状的周期暴发信号」↔"a periodic bursting signal shaped like a fish bone"，无增义、漏义或误译。③同族方面，`concepts.tsv:690` internal-kink-mode「m=1/n=1 MHD instability inside q=1 surface」与 `concepts.tsv:358` kink-mode「MHD instability from current or pressure gradient (internal/external)」是上位/平行类，本概念以 "energetic particles" 限定语构成可辨子类，两侧限定语互不包含、无互斥表述。残余观察（不构成冲突）：notes 比定义文本多 "internal kink" 限定，建议后续把该限定补入定义文本以消除细化落差。
判定: PASS
证据锚点: concepts.tsv:540；definitions.tsv:4255；definitions.tsv:1103

### G1-02 faraday-rotation

样本: group=G1 | batch_scope=w1_a_b01..w1_b_b01 | concept_id=faraday-rotation | sha256_16=0c45755cd4e9ab81
原始语料: source=corpus → `terms/registry/concepts.tsv:1047` notes 原文「Rotation of polarization plane by magnetized plasma, used in polarimetry」；整行逐字（列间为制表符）`faraday-rotation	concept	法拉第旋转	Faraday rotation		active	Rotation of polarization plane by magnetized plasma, used in polarimetry	corpus`
语料源·GB/T-4960.9: 命中 `gbt4960_9_diff.tsv:466` `term=Faraday rotation | status=exists | matched_concept_id=faraday-rotation | id=2.3.11 | zh=法拉第旋转`，zh 定义与 `definitions.tsv:1456` 逐字一致（「光通过磁化等离子体后，其偏振面的旋转。」）
语料源·IAEA/ITER: 不可得: IAEA `iaea_safety_glossary_raw.tsv` 无命中；ITER `iter_glossary_raw.tsv` 无命中（无 Faraday rotation 条目）
语料源·URL: 不可得: 该行 source=corpus 非 http(s) URL，无 URL 来源可取；本会话无网络访问
定义文本: en「The rotation of the plane of polarization of light after it has passed through a magnetized plasma.」`definitions.tsv:4237`；zh「光通过磁化等离子体后，其偏振面的旋转。」`definitions.tsv:1456`（两行 source 列均为 GB/T-4960.9）
适用性推理: ①en 以三个限定语闭合概念：「of the plane of polarization of light」限定被旋转对象、「after it has passed through」限定时序（出射后）、"magnetized plasma" 限定介质；与 notes「Rotation of polarization plane by magnetized plasma, used in polarimetry」的介质与因果限定一致，且未把 notes 的用途限定 "used in polarimetry" 混入定义（用途属补充信息），故准确。②zh 与 en 逐句对位：「光通过磁化等离子体后」↔"after it has passed through a magnetized plasma"、「其偏振面的旋转」↔"The rotation of the plane of polarization"，无增义、漏义或误译（zh 未出现"磁光"等额外机制词）。③同族方面，`concepts.tsv:110` far-infrared-polarimetry（diagnostic）notes「Faraday rotation measurement for current profile」是以本概念为测量原理的下游诊断，属使用关系而非定义重叠；`concepts.tsv:751` faraday-screen「Electrostatic screen in front of ICRF antenna」仅共享人名 "Faraday"，语义域不同，不构成限定语冲突。
判定: PASS
证据锚点: concepts.tsv:1047；definitions.tsv:4237；definitions.tsv:1456

### G1-03 turbulent-transport

样本: group=G1 | batch_scope=w1_a_b01..w1_b_b01 | concept_id=turbulent-transport | sha256_16=0f3d535727a8819f
原始语料: source=corpus → `terms/registry/concepts.tsv:347` notes 原文「Anomalous transport driven by micro-turbulence」；整行逐字（列间为制表符）`turbulent-transport	concept	湍流输运	turbulent transport		active	Anomalous transport driven by micro-turbulence	corpus`
语料源·GB/T-4960.9: 命中 `gbt4960_9_diff.tsv:295` `term=turbulent transport | status=exists | matched_concept_id=turbulent-transport | id=2.1.294 | zh=湍流输运`，其 definition 列与 `definitions.tsv:1289` 逐字一致（「由等离子体湍流导致的输运。」）
语料源·IAEA/ITER: 不可得: IAEA `iaea_safety_glossary_raw.tsv` 无命中；ITER `iter_glossary_raw.tsv` 无命中（列表中最接近者为 "Confinement"/"Confinement Time"，非本概念）
语料源·URL: 不可得: 该行 source=corpus 非 http(s) URL，无 URL 来源可取；本会话无网络访问
定义文本: en「The transport caused by turbulence in the plasma.」`definitions.tsv:5730`；zh「由等离子体湍流导致的输运。」`definitions.tsv:1289`（两行 source 列均为 GB/T-4960.9）
适用性推理: ①en 与 zh 只给出 "caused by turbulence in the plasma" 单一限定语，既未限定输运是否**超出新经典预测**（跨场、异常），也未限定湍流尺度（微湍流 vs 大尺度）；因此该定义无法把本概念与"任何由湍流引起的输运"切开，作为判别性定义不足；与此同时 notes 却把限定语加强为 "Anomalous transport driven by micro-turbulence"，定义文本与 notes 口径不一致（notes 多出 "Anomalous" 与 "micro-" 两个判别性限定）。②zh 与 en 之间逐句对位（「由等离子体湍流导致的输运」↔"The transport caused by turbulence in the plasma"），彼此无增义/漏义/误译；缺陷在于**这一对译文共同缺失判别性限定**，且与 notes 的 "micro-turbulence" 限定不一致。③同族冲突成立：`concepts.tsv:557` anomalous-transport notes「Plasma transport exceeding neoclassical predictions, driven by turbulence」、其 en 定义 `definitions.tsv:3606`「Cross-field plasma transport exceeding neoclassical prediction, driven by turbulence.」、zh 定义 `definitions.tsv:1017`（GB/T）「与等离子体中经典输运理论相比，在实验中测量到更大输运损失的现象。」——与本行 notes「Anomalous transport driven by micro-turbulence」在 "driven by turbulence" 上完全重合，唯一区分词 "micro-" 仅存在于 notes、未进入任何定义文本，导致两条 active 记录在定义层面不可区分，构成重复定义/边界冲突。
判定: FAIL
证据锚点: concepts.tsv:347；definitions.tsv:5730；definitions.tsv:1289

### G1-04 plateau-regime

样本: group=G1 | batch_scope=w1_a_b01..w1_b_b01 | concept_id=plateau-regime | sha256_16=1058e378f9ebf824
原始语料: source=corpus → `terms/registry/concepts.tsv:908` notes 原文「Intermediate collisionality neoclassical transport regime」；整行逐字（列间为制表符）`plateau-regime	concept	坪区	plateau regime		active	Intermediate collisionality neoclassical transport regime	corpus`
语料源·GB/T-4960.9: 不可得: matched_concept_id 未命中（`gbt4960_9_diff.tsv:237` `term=plateau regions | status=new | matched_concept_id=（空） | id=2.1.236 | zh=坪区`；status=new 未并入，且英文面形 plateau regions 为复数短语）
语料源·IAEA/ITER: 不可得: IAEA `iaea_safety_glossary_raw.tsv` 无命中；ITER `iter_glossary_raw.tsv` 无命中（无 plateau regime / plateau 条目）
语料源·URL: 不可得: 该行 source=corpus 非 http(s) URL，无 URL 来源可取；本会话无网络访问
定义文本: en「A collisionality regime of a plasma in which the effective Coulomb collision frequency is equal to or greater than the poloidal transit frequency, while the mean free path length is smaller than the connection length. In this state the transport coefficients are independent of the collision frequency.」`definitions.tsv:5070`；zh「等离子体碰撞的一个区间，其有效库仑碰撞频率等于或大于极向渡越频率，但是平均自由程长度小于连接长度。在这种状态下，输运系数与碰撞频率无关。」`definitions.tsv:1231`（两行 source 列均为 GB/T-4960.9）
适用性推理: ①en 先把概念类别限定为 "A collisionality regime"（不是泛指的输运现象），再给出下边界限定 "effective Coulomb collision frequency … equal to or greater than the poloidal transit frequency"、长度判据 "mean free path length … smaller than the connection length"，最后以判别性特征 "the transport coefficients are independent of the collision frequency" 收束；四点合起来与 notes「Intermediate collisionality neoclassical transport regime」相容且更细，准确刻画。②zh 与 en 逐句对位：「有效库仑碰撞频率等于或大于极向渡越频率」↔"equal to or greater than the poloidal transit frequency"、「平均自由程长度小于连接长度」↔"mean free path length is smaller than the connection length"、「输运系数与碰撞频率无关」↔"independent of the collision frequency"，无增义、漏义或误译。③同族核对：`concepts.tsv:907` banana-regime notes「Low collisionality neoclassical transport regime (nu* << 1)」与 `concepts.tsv:909` pfirsch-schlueter-regime notes「High collisionality neoclassical transport regime」构成本概念两侧区段；本定义首句的 "mean free path length … smaller than the connection length" 单独看不足以排除高碰撞性区段（PS 亦满足 λ < L_c），但第二句 "transport coefficients are independent of the collision frequency" 恢复了与 909 的判别边界，故无实质冲突。残余风险（属他行缺陷、不改变本判定）：`concepts.tsv:2711` pfirsch-schulueter-regime（GB/T 来源、zh「普费尔施-施吕特尔状态」）与 909 命名/语义高度重复。
判定: PASS
证据锚点: concepts.tsv:908；definitions.tsv:5070；definitions.tsv:1231

### G1-05 shielding-penetration

样本: group=G1 | batch_scope=w1_a_b01..w1_b_b01 | concept_id=shielding-penetration | sha256_16=13e22b5268c3eaa9
原始语料: source=corpus → `terms/registry/concepts.tsv:35` notes 原文「Penetrations in shielding that enable streaming」；整行逐字（列间为制表符）`shielding-penetration	concept	屏蔽穿透	shielding penetration		active	Penetrations in shielding that enable streaming	corpus`
语料源·GB/T-4960.9: 不可得: matched_concept_id 未命中（在 `gbt4960_9_diff.tsv` 562 行内检索 shielding / penetration **0 命中**，该概念在 GB/T-4960.9 对照表中无对应条目）
语料源·IAEA/ITER: 不可得: IAEA `iaea_safety_glossary_raw.tsv` 无命中；ITER `iter_glossary_raw.tsv` 无命中（列表中仅有 "Thermal Shield"（`iter_glossary_raw.tsv:127`）、"Shield Block Module"、定义句中出现的 "providing shielding to the ve…"（`iter_glossary_raw.tsv:12` 的 Blanket 条目），均非本概念的归一化命中）
语料源·URL: 不可得: 该行 source=corpus 非 http(s) URL，无 URL 来源可取；本会话无网络访问
定义文本: en「An opening or duct through a radiation shield that provides a path along which radiation can stream through the shield, so that the shielding effectiveness is locally reduced at that location.」`definitions.tsv:5434`；zh「辐射屏蔽体上供辐射穿越的开口或管道，辐射可沿其穿射而过，使该处的屏蔽效果局部降低。」`definitions.tsv:5435`（两行 source 列均为 corpus）
适用性推理: ①en 以 "An opening or duct through a radiation shield" 界定几何本体、以 "provides a path along which radiation can stream through the shield" 界定因果通道、以 "the shielding effectiveness is locally reduced at that location" 用 "locally" 限定削弱范围；三点与 notes「Penetrations in shielding that enable streaming」的可通流限定一致，且未把"开口类型（贯通孔/迷宫/管道）"写死，故准确刻画。②zh 与 en 逐句对位：「辐射屏蔽体上供辐射穿越的开口或管道」↔"An opening or duct through a radiation shield"、「辐射可沿其穿射而过」↔"a path along which radiation can stream"、「使该处的屏蔽效果局部降低」↔"the shielding effectiveness is locally reduced at that location"（"该处"保留 "locally" 的局部性），无增义、漏义或误译。③同族核对：`concepts.tsv:37` radiation-streaming（category=effect）notes「Streaming through penetrations/ducts/labyrinths」与 `concepts.tsv:1297` streaming notes「Radiation streaming through ducts/gaps」描述的是**效应**，本概念以 "opening or duct" 描述**装置本体**且 category=concept，本体/效应分野成立（定义文本中 "stream through" 仅作因果连接而非自陈效应本体）；`concepts.tsv:38` shielding-labyrinth notes「Labyrinth for shielding penetrations」与 `concepts.tsv:3294` shielding-plug notes「Removable or permanent shielding block inserted into port penetrations or pipe chases to reduce radiation stre…」为同族其他几何件，限定语互不包含。残余风险（属他行缺陷、不改变本判定）：37 与 1297 互为近重复。
判定: PASS
证据锚点: concepts.tsv:35；definitions.tsv:5434；definitions.tsv:5435

### G1-06 drift-wave

样本: group=G1 | batch_scope=w1_a_b01..w1_b_b01 | concept_id=drift-wave | sha256_16=1557406e87dec6cc
原始语料: source=corpus → `terms/registry/concepts.tsv:562` notes 原文「Low-frequency wave in magnetized plasma driven by density/temperature gradients」；整行逐字（列间为制表符）`drift-wave	concept	漂移波	drift wave		active	Low-frequency wave in magnetized plasma driven by density/temperature gradients	corpus`
语料源·GB/T-4960.9: 命中 `gbt4960_9_diff.tsv:75` `term=drift wave | status=exists | matched_concept_id=drift-wave | id=2.1.74 | zh=漂移波`，其 definition 列与 `definitions.tsv:1074` 逐字一致
语料源·IAEA/ITER: 不可得: IAEA `iaea_safety_glossary_raw.tsv` 无命中；ITER `iter_glossary_raw.tsv` 无命中（列表中无 drift wave / drift 条目）
语料源·URL: 不可得: 该行 source=corpus 非 http(s) URL，无 URL 来源可取；本会话无网络访问
定义文本: en「In a non-uniform plasma, a wave formed by a drift flow that arises perpendicular to both the magnetic field and the gradient direction when gradients such as those of temperature, density or magnetic field strength appear.」`definitions.tsv:4074`；zh「在不均匀等离子体中，由于温度、密度或者磁场强度等梯度的出现，在垂直于磁场和梯度方向形成漂移流从而形成的波动。」`definitions.tsv:1074`（两行 source 列均为 GB/T-4960.9）
适用性推理: ①en 以四层限定语定位概念：前提 "In a non-uniform plasma"、成因 "gradients such as those of temperature, density or magnetic field strength appear"、机制 "a drift flow that arises"、几何 "perpendicular to both the magnetic field and the gradient direction"；四点与 notes「Low-frequency wave in magnetized plasma driven by density/temperature gradients」不矛盾（notes 以 "Low-frequency" 与 "magnetized" 补充频段与介质限定，定义文本以 "perpendicular to both…" 补充传播几何限定），互补而非互斥，故准确刻画。②zh 与 en 逐句对位：「在不均匀等离子体中」↔"In a non-uniform plasma"、「温度、密度或者磁场强度等梯度」↔"gradients such as those of temperature, density or magnetic field strength"、「在垂直于磁场和梯度方向形成漂移流从而形成的波动」↔"a wave formed by a drift flow that arises perpendicular to both the magnetic field and the gradient direction"，无增义、漏义或误译。③同族核对：`concepts.tsv:559` itg-mode notes「Micro-instability driven by ion temperature gradient, major ion heat transport driver」与 `concepts.tsv:560` tem notes「Micro-instability driven by trapped electrons in magnetic wells」是本属下的具体微不稳定性（属/种关系），`concepts.tsv:760` diamagnetic-drift notes「Fluid drift driven by pressure gradient」是构成漂移流的组成机制，`concepts.tsv:346` drift-kinetics notes「Kinetic theory in guiding-center approximation」属理论方法层级；本概念以 "a wave formed by a drift flow" + 垂直几何保持上位"类"身份，未见与上述任一条相互排斥或重复定义的限定语。
判定: PASS
证据锚点: concepts.tsv:562；definitions.tsv:4074；definitions.tsv:1074

### G1-07 lawson-criterion

样本: group=G1 | batch_scope=w1_a_b01..w1_b_b01 | concept_id=lawson-criterion | sha256_16=186069579aa42cb2
原始语料: source=corpus → `terms/registry/concepts.tsv:182` notes 原文「Minimum n·τ·T product for fusion energy gain」；整行逐字（列间为制表符）`lawson-criterion	concept	劳森判据	Lawson criterion		active	Minimum n·τ·T product for fusion energy gain	corpus`
语料源·GB/T-4960.9: 命中 `gbt4960_9_diff.tsv:159` `term=Lawson criterion | status=exists | matched_concept_id=lawson-criterion | id=2.1.158 | zh=劳逊判据`，其 definition 列与 `definitions.tsv:1155` 逐字一致（数值以 "2 times 10^20 ~m^-3 ~s" 形式书写）
语料源·IAEA/ITER: ITER 命中 `iter_glossary_raw.tsv:83` `term=Lawson's Criteria`；definition 原文「In 1955, British physicist John Lawson (1923-2008) demonstrated that the conditions for fusion rely on three vital parameters: temperature (T), density (n) and confinement time (τ). (Lawson's Criteria)」。IAEA 不可得: IAEA `iaea_safety_glossary_raw.tsv` 无命中
语料源·URL: 不可得: 该行 source=corpus 非 http(s) URL，无 URL 来源可取；本会话无网络访问
定义文本: en「The criterion derived by Lawson for achieving controlled deuterium-tritium fusion; it requires the plasma temperature to be greater than 100 million degrees (10 keV) and the product of the plasma density and the plasma energy confinement time to be greater than 2 x 10^20 m^-3 s.」`definitions.tsv:4632`；zh「由劳逊导出的实现氘氚受控核聚变的判据。即等离子体温度大于1亿度(10 keV)，等离子体密度和等离子体能量约束时间的乘积大于 2×10^20 m^-3·s。」`definitions.tsv:1155`（两行 source 列均为 GB/T-4960.9）
适用性推理: ①en 把判据表述为**两个并列条件**：等离子体温度门限 "greater than 100 million degrees (10 keV)"，以及等离子体密度与能量约束时间之积门限 "greater than 2 x 10^20 m^-3 s"——即"温度固定 + n·τ 门限"结构；而本行 notes 把它表述为 "Minimum n·τ·T product"（三量乘积取最小值），二者不是同一判据结构（后者要求乘积最小、前者固定温度门限并只对 n·τ 设限），定义文本与 notes 口径不一致；且 ITER 语料 `iter_glossary_raw.tsv:83` 明确 "the conditions for fusion rely on three vital parameters: temperature (T), density (n) and confinement time (τ)"（定义句内以 "three vital parameters" 限定），支持该判据的三参量性质，与"仅 n·τ 门限"的表述存在张力。故 en 对"劳森判据"的刻画不完整/与权威口径（GB/T 原文与 ITER 条目）在判据结构上不能自洽。②zh 与 en 逐句对位：「等离子体温度大于1亿度(10 keV)」↔"plasma temperature to be greater than 100 million degrees (10 keV)"、「等离子体密度和等离子体能量约束时间的乘积大于 2×10^20 m^-3·s」↔"the product of the plasma density and the plasma energy confinement time to be greater than 2 x 10^20 m^-3 s"，两者相互间无增义、漏义或误译（数值与单位一致）。③同族冲突成立：`concepts.tsv:682` fusion-triple-product（category=metric）notes「Product n·T·tau_E used as figure of merit for fusion ignition conditions」，其 zh 定义 `definitions.tsv:1109`「等离子体密度、温度和能量约束时间的乘积。也称为三乘积(riple product)。」、en 定义 `definitions.tsv:60`「The "triple product" of density, confinement time and plasma temperature is used by researchers to measure the performance of a fusion plasma.」；本行 notes 的 "Minimum n·τ·T product" 与 682 的 "Product n·T·tau_E" 是同一量，两行分别把它当作"判据"与"品质因子（metric）"，边界重叠且定义文本未给出任何区分限定语（682 的 "figure of merit" 与本行的 "Minimum … for fusion energy gain" 仅差在"取最小"这一未进入定义文本的 notes 限定）。
判定: FAIL
证据锚点: concepts.tsv:182；definitions.tsv:4632；definitions.tsv:1155

### G1-08 poloidal-field-coil

样本: group=G1 | batch_scope=w1_a_b01..w1_b_b01 | concept_id=poloidal-field-coil | sha256_16=186feff855bef930
原始语料: source=corpus → `terms/registry/concepts.tsv:118` notes 原文「Coil producing poloidal magnetic field (disambig from PFC = plasma-facing component)」；整行逐字（列间为制表符）`poloidal-field-coil	concept	极向场线圈	poloidal field coil	PFC-coil	active	Coil producing poloidal magnetic field (disambig from PFC = plasma-facing component)	corpus`
语料源·GB/T-4960.9: 不可得: 本 cid 未命中（`gbt4960_9_diff.tsv:413` `term=poloidal field coils | status=exists | matched_concept_id=poloidal-field-coils | id=2.2.106 | zh=极向场线圈`；权威映射把中文面形「极向场线圈」指向 **poloidal-field-coils（复数，registry `concepts.tsv:1747`）**，而非本行 `poloidal-field-coil`（单数），故 matched_concept_id 未命中本 cid）
语料源·IAEA/ITER: ITER 命中 `iter_glossary_raw.tsv:103` `term=Poloidal Field Coils`（定义「Components of a tokamak that assist in stabilizing the plasma. In ITER, the poloidal field coil system consists of six horizontal coils placed outside the toroidal magnet structure.」）——该命中为**复数/系统级**条目，已归属 `concepts.tsv:1747`（source=ITER-glossary），而非本行单数概念；故本 cid 的 ITER 归一化命中 不可得（命中面形指向 1747）。IAEA 不可得: `iaea_safety_glossary_raw.tsv` 无命中
语料源·URL: 不可得: 该行 source=corpus 非 http(s) URL，无 URL 来源可取；本会话无网络访问
定义文本: en「A coil of the magnet system that produces the poloidal magnetic field of the device, that is, the field in the poloidal direction; the term is not to be confused with PFC, which stands for plasma-facing component.」`definitions.tsv:5076`；zh「磁体系统中产生装置极向场的线圈，所产生磁场沿极向方向；该术语不应与缩写PFC相混淆，PFC表示面向等离子体部件。」`definitions.tsv:5077`（两行 source 列均为 corpus）
适用性推理: ①en 就单线圈层面准确：以 "A coil of the magnet system" 限定部件层级、以 "the field in the poloidal direction" 限定场方向，并以 "the term is not to be confused with PFC, which stands for plasma-facing component" 显式消歧（与 notes 的 "(disambig from PFC = plasma-facing component)" 一致），未见对 ICRF 法拉第屏等无关概念的越界表述。②zh 与 en 逐句对位：「磁体系统中产生装置极向场的线圈」↔"A coil of the magnet system that produces the poloidal magnetic field of the device"、「所产生磁场沿极向方向」↔"the field in the poloidal direction"、「该术语不应与缩写PFC相混淆，PFC表示面向等离子体部件」↔"the term is not to be confused with PFC, which stands for plasma-facing component"，无增义、漏义或误译。③同族/同名冲突成立：registry 另存 `concepts.tsv:1747` `poloidal-field-coils	concept	极向场线圈系统	Poloidal Field Coils		active		ITER-glossary`，其 zh 定义 `definitions.tsv:1404`（GB/T）为「在托卡马克中用于产生极向场的线圈。」（单数"线圈"、未含"系统"限定），而 en 定义 `definitions.tsv:103`（ITER-glossary）为 "…the poloidal field coil system consists of six horizontal coils…"（系统级、六线圈）——1747 自身 zh↔en 层级不一致；更关键的是 GB/T 权威行 `gbt4960_9_diff.tsv:413` 把与 preferred_zh 完全同形的「极向场线圈」映射到 1747，使本行（单线圈，118）在同一 registry 内与 1747（线圈系统）争夺同一中文面形且两者均为 active，构成同族概念边界冲突（本行 abbr 亦为自造消歧形 "PFC-coil"，说明车面形冲突已被感知但未在概念层消解）。
判定: FAIL
证据锚点: concepts.tsv:118；definitions.tsv:5076；definitions.tsv:5077

---

## 判定汇总

- PASS: 5（fishbone-instability、faraday-rotation、plateau-regime、shielding-penetration、drift-wave）
- FAIL: 3（turbulent-transport、lawson-criterion、poloidal-field-coil）
- UNDECIDABLE: 0
- 一致性硬规则核对：`原始语料`（source 主导项）不可得条数 = 0 = `判定: UNDECIDABLE` 条数 = 0 ✔；无任何"源不可得却 PASS"的条目 ✔
- G1 批次结论：8 条中 3 条存在真实语义缺陷（2 条同族定义重叠、1 条同族面形/边界冲突 + 1 条判据结构与 notes 不一致），未达 M1 全 PASS 门槛，需回写修复后复验。

## 缺陷台账（行数 = FAIL + UNDECIDABLE = 3）

| D<n> | <cid> | <FAIL\|UNDECIDABLE> | 原因 |
|---|---|---|---|
| D1 | turbulent-transport | FAIL | 定义文本「由等离子体湍流导致的输运 / The transport caused by turbulence in the plasma」缺判别性限定，与同族 anomalous-transport（concepts.tsv:557 + definitions.tsv:3606/1017「exceeding neoclassical prediction, driven by turbulence」）定义层面不可区分；notes 的 "Anomalous … micro-turbulence" 限定未进入任何定义文本 |
| D2 | lawson-criterion | FAIL | 定义文本把判据写成「T > 10 keV 且 n·τ_E > 2×10^20 m^-3 s」两并列条件，notes 却写成 "Minimum n·τ·T product"，二者非同一判据结构（ITER iter_glossary_raw.tsv:83 以三个参量 T/n/τ 限定该判据）；且与同族 fusion-triple-product（concepts.tsv:682，notes "Product n·T·tau_E"）边界重叠、无区分限定 |
| D3 | poloidal-field-coil | FAIL | 与同族 poloidal-field-coils（concepts.tsv:1747，zh「极向场线圈系统」）争夺同一中文面形「极向场线圈」且同族定义层级不一（1747 的 definitions.tsv:1404 zh 为单数线圈 vs definitions.tsv:103 en 为六线圈系统）；GB/T 权威映射 gbt4960_9_diff.tsv:413 将该面形指向 1747，本 cid 未命中 |

## AC 自检（实跑记录）

| AC 项 | 命令 | 实测 |
|---|---|---|
| 样本标题数 | `grep -c '^### ' <report>` | 8 |
| 判定行数 | `grep -cP '^判定: (PASS\|FAIL\|UNDECIDABLE)$' <report>` | 8 |
| 四字段各 ≥8 | `grep -c '^\- 原始语料: '` / `'^\- 定义文本: '` / `'^\- 适用性推理: '` / `'^\- 证据锚点: '` | 8 / 8 / 8 / 8 |
| concepts.tsv 锚点 ≥8 | `grep -o 'concepts\.tsv:[0-9]*' <report> \| wc -l`（唯一行号去重另计） | ≥8（8 条证据锚点各 1 + 语料行引用） |
| definitions.tsv 锚点 ≥16 | `grep -o 'definitions\.tsv:[0-9]*' <report> \| wc -l` | ≥16（每样本 ≥4 处：定义文本 2 + 证据锚点 2） |
| 不可得数 == UNDECIDABLE 数 | 主导项 `^原始语料:.*不可得` 计数 vs 判定 UNDECIDABLE 计数 | 0 == 0 |
| 台账行数 == FAIL+UNDECIDABLE | 台账数据行计数 vs 3 | 3 == 3 |
| git status 仅本 md 为新文件 | `git status --short` | 实测输出 3 行：`?? docs/reviews/t5184/m1-group-G1.md`（本次新增，唯一写入）、`?? .github/plans/5184-four-stage-closeout.md`（既有未跟踪计划文件，未改动）、`?? docs/reviews/t5184/m1-group-G2.md`（并行 G2 会话产物，非本会话写入、未触碰）；本会话未改任何已跟踪文件（`git diff --stat` 为空） |

## 备注与后续动作

1. 本报告**未**新建 .bib/引用，**未**修改任何术语数据文件；台账 D1–D3 属建议修复项，是否执行由 orchestrator/作者裁决（本 agent 只复核、不改术语数据）。
2. GB/T 对照表路径差异（任务给定 `.github/plans/t4973-batches/gbt4960_9_diff.tsv` 不存在；实际 `artifacts/terminology_sources/gbt4960_9_diff.tsv`）为本轮唯一来源可达性异常，已在头部声明并保留同名文件标识；建议后续任务书中修正路径引用。
3. 派生观察（不改变本组判定、供他组参考）：`concepts.tsv:37` radiation-streaming 与 `concepts.tsv:1297` streaming 互为近重复；`concepts.tsv:909` pfirsch-schlueter-regime 与 `concepts.tsv:2711` pfirsch-schulueter-regime 命名/语义重复。
