# T4.9 组 G8 语义复核（PM #5184 / M1）

- 报告日期: 2026-11-03（`date` 实跑: Tue Nov  3 12:15:11 PM CST 2026）
- 复核范围: `docs/reviews/t5184/m1-sample-manifest.tsv` 中 `group=G8` 的 8 行（manifest 第 58–65 行），逐行原样、同序使用（group / batch_scope / concept_id / sha256_16 未改写、未增删、未替换样本）
- 判定口径: PASS / FAIL / UNDECIDABLE；依据真实语义（① en 定义是否准确刻画该概念、② zh 与 en 是否等价、③ 是否与同族概念冲突或重复登记），非格式。**本报告采用的判 FAIL 门槛（显式声明，便于复核）**：(i) en 定义不可判别，或与同族 active 概念在**定义层面不可区分**；(ii) zh↔en 存在**增义/漏义/误译**；(iii) 与同族登记概念**争夺同一面形/重复登记**。三者任一成立才判 FAIL；**仅与登记库外既有术语同形**（库内无任何 active 概念与之同名）只列观察项，不计 FAIL。
- 只读声明: 本报告为唯一写入文件；`terms/registry/*`、`artifacts/terminology_sources/*`、manifest 全部只读；未运行任何写 git 命令（无 add / commit / checkout / stash / restore / push），未改动任何计划文件

## 输入行原样引用（8/8）

| # | group | batch_scope | concept_id | sha256_16 |
|---|---|---|---|---|
| G8-01 | G8 | w1_b_b32..w1_c_b01 | strike-point-sweeping | 04d84e751448d642 |
| G8-02 | G8 | w1_b_b32..w1_c_b01 | energy-dump | 04ee0b5284c76dba |
| G8-03 | G8 | w1_b_b32..w1_c_b01 | tallying-efficiency | 127bf107f01dbf61 |
| G8-04 | G8 | w1_b_b32..w1_c_b01 | dissolution-precipitation-coefficient | 194a3435bd1a86eb |
| G8-05 | G8 | w1_b_b32..w1_c_b01 | gamma-spectrometer | 201dada7eeb057c2 |
| G8-06 | G8 | w1_b_b32..w1_c_b01 | x-ray-crystal-spectrometer | 283a693913e759f0 |
| G8-07 | G8 | w1_b_b32..w1_c_b01 | remote-welding | 2ba12f90bb555b2c |
| G8-08 | G8 | w1_b_b32..w1_c_b01 | parasitic-absorption | 2bf212f5a5304d6c |

## 路径与来源可得性声明（影响 5 字段中的来源子项）

1. **路径更正（任务书假设 vs 实存）**：任务书写「计划路径 `.github/plans/t4973-batches/` 不存在」。**实测该目录在仓内存在**（含 `README.md`、`coverage-after-w2.md`、`defs-basis-t0_7.tsv`、`names-basis-t0_6.tsv`、`glue-sources-b18/b19.tsv`、`red-green.md` 等 12 项）。故此处仅作**如实更正**，不据此虚构缺口。本组 GB/T 对照证据实际取自 `artifacts/terminology_sources/gbt4960_9_diff.tsv`（562 行，表头 `# term / status / matched_concept_id / term_id / zh / abbr / definition`），与任务书给出的文件名一致。
2. **corpus（本组 8 行 `source` 取值的主导项）**：8/8 均为 `corpus`，故依据按任务规定取 `terms/registry/concepts.tsv` 该行 `notes` 原文及行号（另附整行逐字）。**8/8 可得**。
3. **GB/T-4960.9**：逐 cid 查 `gbt4960_9_diff.tsv` 的 `matched_concept_id` 列，**8/8 未命中**（全表 562 行内无 `strike-point-sweeping|energy-dump|tallying-efficiency|dissolution-precipitation-coefficient|gamma-spectrometer|x-ray-crystal-spectrometer|remote-welding|parasitic-absorption` 任一 cid；亦无对应英文面形）。
4. **IAEA / ITER**：`artifacts/terminology_sources/iaea_safety_glossary_raw.tsv`（877 行）与 `iter_glossary_raw.tsv`（143 行）**8/8 未命中**（两表均无 spectrometer / welding / absorption / dissolution / tally / strike point / energy dump 等对应条目）。
5. **http(s) URL**：8 行 `source` 字段均 = `corpus`（非 URL），无 URL 来源可取；本会话无网络工具，按规则对 URL 子项一律记 **不适用（source=corpus，非 http(s)）**，不虚构外部片段。
6. **主导一致性（硬规则）**：主导项 `原始语料` 不可得条数 = **0**，故 `判定: UNDECIDABLE` 条数 = **0**（0 == 0 ✔）。子来源（GB/T / IAEA / ITER / URL）的「无命中 / 不适用」**不参与**上述等式，亦不落 PASS 门槛判定——本组 8 条 PASS 均为「主导项可得 + 定义语义等价 + 无同族登记冲突」的情形，**不存在**任何"源不可得却 PASS"的条目 ✔。

---

### G8-01 strike-point-sweeping

样本: group=G8 | batch_scope=w1_b_b32..w1_c_b01 | concept_id=strike-point-sweeping | sha256_16=04d84e751448d642
原始语料: source=corpus → `terms/registry/concepts.tsv:3361` notes 原文「Controlled oscillation of the divertor strike point to distribute heat load over a wider area [domain: divertor-physics]」；整行逐字（列间为制表符）`strike-point-sweeping	method	打击点扫描	Strike Point Sweeping		active	Controlled oscillation of the divertor strike point to distribute heat load over a wider area [domain: divertor-physics]	corpus`
语料源·GB/T-4960.9: 无命中（`gbt4960_9_diff.tsv` 的 `matched_concept_id` 无 `strike-point-sweeping`；全表 562 行无 "strike point sweep" 面形）
语料源·IAEA/ITER: 无命中（IAEA `iaea_safety_glossary_raw.tsv`、ITER `iter_glossary_raw.tsv` 均无 strike / sweep 条目）
语料源·URL: 不适用（该行 source=corpus，非 http(s) URL；无网络访问）
定义文本: en「Controlled oscillation of the divertor strike point to distribute heat load over a wider area.」`definitions.tsv:6073`；zh「打击点扫描：使偏滤器打击点受控往复移动、以将热负荷展布于更大面积的技术。」`definitions.tsv:6074`（两行 source 列均为 corpus）
适用性推理: ①en 以三处限定语闭合概念：「Controlled oscillation」限定动作性质为受控往复（而非一次性位移或稳态偏移）、「of the divertor strike point」限定作用对象为打击点、「to distribute heat load over a wider area」限定目的为展宽热负荷分布（而非降低总热负荷），三条限定完整刻画该方法的机理与目的，未越出 method 范畴；notes 与 en 定义逐字一致（仅缺 `[domain:]` 标注），无口径漂移。②zh 与 en 逐句对位：「受控往复移动」↔"Controlled oscillation"、「偏滤器打击点」↔"the divertor strike point"、「将热负荷展布于更大面积」↔"distribute heat load over a wider area"，无增义/漏义/误译；zh 末「的技术」与 category=method 自洽，非增义。③同族核查：`concepts.tsv:578` strike-point（`definitions.tsv:5544/5545`「The location where the separatrix intersects the divertor target. / 打击点是分界面与偏滤器靶板相交的位置。」）是本方法的**作用对象**（位置概念），二者限定语互不包含；`concepts.tsv:587` flux-expansion（`definitions.tsv:4283/4284`「geometric spreading of magnetic flux tubes, used to reduce the target heat flux」）以**磁几何扩张**降热流、与本方法以**时间往复**展宽热负荷的机制不同；三者在定义层面可区分，无同形面形冲突、非重复登记。
判定: PASS
证据锚点: concepts.tsv:3361；definitions.tsv:6073；definitions.tsv:6074

### G8-02 energy-dump

样本: group=G8 | batch_scope=w1_b_b32..w1_c_b01 | concept_id=energy-dump | sha256_16=04ee0b5284c76dba
原始语料: source=corpus → `terms/registry/concepts.tsv:3319` notes 原文「Circuit for safely dissipating stored magnet energy during quench [domain: electrical-power-systems]」；整行逐字（列间为制表符）`energy-dump	device	卸能回路	Energy Dump		active	Circuit for safely dissipating stored magnet energy during quench [domain: electrical-power-systems]	corpus`
语料源·GB/T-4960.9: 无命中（`gbt4960_9_diff.tsv` 的 `matched_concept_id` 无 `energy-dump`；全表无 "energy dump" 面形）
语料源·IAEA/ITER: 无命中（IAEA / ITER raw 两表均无 energy dump / quench energy 条目）
语料源·URL: 不适用（该行 source=corpus，非 http(s) URL；无网络访问）
定义文本: en「A circuit for safely dissipating stored magnet energy during a quench.」`definitions.tsv:5917`；zh「卸能回路：在失超时安全耗散磁体储能的卸能电路。」`definitions.tsv:5918`（两行 source 列均为 corpus）
适用性推理: ①en 以三处限定语闭合概念：「A circuit」限定本体层级为**回路/电路**（非元件、非整机系统）、「during a quench」限定时序为失超期间、「for safely dissipating stored magnet energy」限定功能为安全耗散磁体储能；notes 与 en 定义一致（仅 "during quench"→"during a quench"、加冠词），无口径漂移。②zh 与 en 逐句对位：「卸能回路」↔"A circuit"、「在失超时」↔"during a quench"、「安全耗散磁体储能」↔"safely dissipating stored magnet energy"、「卸能电路」↔"circuit"（回/电路同义复指），无增义/漏义/误译。③同族核查（三条并列 active，限定语须互斥）：`concepts.tsv:1549` dump-resistor（`definitions.tsv:2778/2779`「Resistor switched into magnet circuit during quench to dissipate stored magnetic energy safely. / 失超时切入磁体回路安全耗散储能的电阻器。」）本体是**电阻器元件**、`concepts.tsv:122` quench-protection（`definitions.tsv:5184/5185`「the provisions by which a superconducting magnet is protected … in particular the safe discharge of the magnetic energy」）是**保护措施集合**、`concepts.tsv:3279` magnet-protection-system 是**整机系统**（其 notes 列出的构件为 "dump resistors"），本行是**回路**——四者本体层级（回路 vs 元件 vs 措施 vs 系统）不同、定义层面可区分，非重复登记；残余观察（不构成 FAIL）：本行与 dump-resistor 共享「失超 + 耗散磁体储能」核心限定，四条的层级边界建议在 notes 中显式互引。
判定: PASS
证据锚点: concepts.tsv:3319；definitions.tsv:5917；definitions.tsv:5918

### G8-03 tallying-efficiency

样本: group=G8 | batch_scope=w1_b_b32..w1_c_b01 | concept_id=tallying-efficiency | sha256_16=127bf107f01dbf61
原始语料: source=corpus → `terms/registry/concepts.tsv:3331` notes 原文「Metric quantifying the computational cost to achieve a given tally precision [domain: computational-methods]」；整行逐字（列间为制表符）`tallying-efficiency	metric	计数效率	Tallying Efficiency		active	Metric quantifying the computational cost to achieve a given tally precision [domain: computational-methods]	corpus`
语料源·GB/T-4960.9: 无命中（`gbt4960_9_diff.tsv` 的 `matched_concept_id` 无 `tallying-efficiency`；全表无 tally efficiency 面形）
语料源·IAEA/ITER: 无命中（IAEA / ITER raw 两表均无 tally 条目）
语料源·URL: 不适用（该行 source=corpus，非 http(s) URL；无网络访问）
定义文本: en「A metric quantifying the computational cost to achieve a given tally precision.」`definitions.tsv:6079`；zh「计数效率：衡量达到给定计数精度所需计算成本的量度。」`definitions.tsv:6080`（两行 source 列均为 corpus）
适用性推理: ①en 以两处限定语闭合概念：「the computational cost」限定被量化对象为**计算成本**、「to achieve a given tally precision」限定参照量为**既定计数精度**，二者把该量锚定为"达到给定 tally 精度所付计算代价"的效率度量（MCNP 图优值/FOM 语族），未越出 computational-methods 范畴；notes 与 en 定义逐字一致，无口径漂移。②zh 与 en **定义句**逐句对位：「衡量达到给定计数精度所需计算成本的量度」↔"A metric quantifying the computational cost to achieve a given tally precision"，无增义/漏义/误译，句内"计算成本"已把歧义消解（M4 报告 O3 亦已认定"不影响列归属"）。③同族核查：`concepts.tsv:461` tallying（`definitions.tsv:5602/5603`「Scoring of quantities such as flux, dose, and heating … / 在蒙特卡罗输运计算中对通量、剂量、核热等量的计数。」）是计数**动作**、`concepts.tsv:1214` tally-reliability（`definitions.tsv:1952/1953`「…based on relative error, VOV, FOM stability / 基于相对误差、VOV、FOM 稳定性的…综合可信度指标」）是计数**可信度指标**、`concepts.tsv:1132` figure-of-merit 是**通用**标量指标——三者与本行的被量化对象（计算成本）与量纲不同，定义层面可区分，无任何库内 active 概念使用「计数效率」面形（全库 zh 面形唯一），**不构成重复登记或面形冲突**。观察项（不计 FAIL，同族命名漂移）：本族 tally 的中文面形不统一——tallying→「计数统计」、tally-reliability→「记数器」、本行→「计数效率」；且 preferred_zh「计数效率」与探测计量学既有术语 "counting efficiency（计数效率）" 同形（库内无同名 active 概念，属库外同形），建议后续统一为「计数统计效率」并消歧。
判定: PASS
证据锚点: concepts.tsv:3331；definitions.tsv:6079；definitions.tsv:6080

### G8-04 dissolution-precipitation-coefficient

样本: group=G8 | batch_scope=w1_b_b32..w1_c_b01 | concept_id=dissolution-precipitation-coefficient | sha256_16=194a3435bd1a86eb
原始语料: source=corpus → `terms/registry/concepts.tsv:3404` notes 原文「Rate coefficient for dissolution of the oxide layer and precipitation of dissolved species in coolant loops」；整行逐字（列间为制表符）`dissolution-precipitation-coefficient	metric	溶解沉淀系数	dissolution-precipitation coefficient		active	Rate coefficient for dissolution of the oxide layer and precipitation of dissolved species in coolant loops	corpus`
语料源·GB/T-4960.9: 无命中（`gbt4960_9_diff.tsv` 的 `matched_concept_id` 无本 cid；全表无 dissolution / precipitation 条目）
语料源·IAEA/ITER: 无命中（IAEA / ITER raw 两表均无 dissolved species / coolant precipitation 条目）
语料源·URL: 不适用（该行 source=corpus，非 http(s) URL；无网络访问）
定义文本: en「A rate coefficient for the dissolution of the oxide layer and the precipitation of dissolved species in coolant loops.」`definitions.tsv:6143`；zh「溶解沉淀系数：冷却剂回路中氧化层溶解与溶解态核素沉淀的速率系数。」`definitions.tsv:6153`（两行 source 列均为 corpus）
适用性推理: ①en 以三处限定语闭合概念：「A rate coefficient」限定本体为**双向速率系数**（非单向速率）、「the dissolution of the oxide layer and the precipitation of dissolved species」同时固定两个互逆过程（氧化层溶解 / 溶解物沉淀）、「in coolant loops」限定场所为冷却剂回路；notes 与 en 定义一致（仅加冠词/介词），无口径漂移。②zh 与 en 主体逐句对位：「速率系数」↔"A rate coefficient"、「氧化层溶解与溶解态核素沉淀」↔"the dissolution of the oxide layer and the precipitation of dissolved species"、「冷却剂回路中」↔"in coolant loops"，无增义/漏义；一处**轻微窄化观察**：en "dissolved species（溶解态物种）" 被 zh 收窄为「溶解态核素」，冷却剂回路中溶解态物种以活化腐蚀产物核素为主，该窄化在域内成立、不改变语义边界，故不计 FAIL。③同族核查：`concepts.tsv:3355` dissolution-rate（`definitions.tsv:5897/5898`「Rate of structural material mass loss into a flowing liquid metal or coolant. / 溶解速率：结构材料在流动液态金属或冷却剂中的质量损失速率。」）限定对象为**结构材料质量损失**（单向 rate）、本行限定对象为**氧化层溶解 + 沉淀双向 coefficient**（系数，量纲不同），二者在定义层面可区分；`concepts.tsv:1545` corrosion-product 是产物概念、非速率量，无重叠；无同形面形冲突、非重复登记。残余观察（格式，非语义）：preferred_en 为小写 "dissolution-precipitation coefficient"，与同族 Title Case 不一致。
判定: PASS
证据锚点: concepts.tsv:3404；definitions.tsv:6143；definitions.tsv:6153

### G8-05 gamma-spectrometer

样本: group=G8 | batch_scope=w1_b_b32..w1_c_b01 | concept_id=gamma-spectrometer | sha256_16=201dada7eeb057c2
原始语料: source=corpus → `terms/registry/concepts.tsv:3333` notes 原文「Detector system for measuring gamma-ray energy spectra from fusion plasmas and activated components [domain: plasma-diagnostics]」；整行逐字（列间为制表符）`gamma-spectrometer	diagnostic	γ谱仪	Gamma Spectrometer		active	Detector system for measuring gamma-ray energy spectra from fusion plasmas and activated components [domain: plasma-diagnostics]	corpus`
语料源·GB/T-4960.9: 无命中（`gbt4960_9_diff.tsv` 的 `matched_concept_id` 无 `gamma-spectrometer`；全表无 gamma spectrometer 面形）
语料源·IAEA/ITER: 无命中（IAEA / ITER raw 两表均无 gamma spectrometer 条目）
语料源·URL: 不适用（该行 source=corpus，非 http(s) URL；无网络访问）
定义文本: en「A detector system for measuring gamma-ray energy spectra from fusion plasmas and activated components.」`definitions.tsv:5943`；zh「γ谱仪：测量聚变等离子体与活化部件伽马射线能谱的探测器系统。」`definitions.tsv:5944`（两行 source 列均为 corpus）
适用性推理: ①en 以三处限定语闭合概念：「A detector system」限定本体为探测器系统、「measuring gamma-ray energy spectra」限定测量量与谱型（能量谱，非计数率或剂量）、「from fusion plasmas and activated components」限定被测对象（等离子体辐射 + 活化部件），完整刻画该诊断的功能与适用对象，未越出 diagnostic 范畴；notes 与 en 定义逐字一致，无口径漂移。②zh 与 en 逐句对位：「探测器系统」↔"A detector system"、「测量…伽马射线能谱」↔"measuring gamma-ray energy spectra"、「聚变等离子体与活化部件」↔"fusion plasmas and activated components"，无增义/漏义/误译（zh「γ谱仪」与 en 首词 "Gamma" 对应，缩写符号 γ 与原形自洽）。③同族核查（谱仪族四条 active）：`concepts.tsv:3346` mass-spectrometer（按质荷比分离气体组分）、`concepts.tsv:2869` survey-spectrometer（宽频/宽谱覆盖）、`concepts.tsv:3334` x-ray-crystal-spectrometer（布拉格晶体、X 射线线发射）——分别以**测量量/色散机制**区隔，本行以 "gamma-ray energy spectra" 与被测对象（聚变等离子体 + 活化部件）为判别限定，四条定义层面可区分，无同形面形冲突、非重复登记。
判定: PASS
证据锚点: concepts.tsv:3333；definitions.tsv:5943；definitions.tsv:5944

### G8-06 x-ray-crystal-spectrometer

样本: group=G8 | batch_scope=w1_b_b32..w1_c_b01 | concept_id=x-ray-crystal-spectrometer | sha256_16=283a693913e759f0
原始语料: source=corpus → `terms/registry/concepts.tsv:3334` notes 原文「Bragg crystal spectrometer for high-resolution X-ray line emission measurements [domain: plasma-diagnostics]」；整行逐字（列间为制表符）`x-ray-crystal-spectrometer	diagnostic	X射线晶体谱仪	X-Ray Crystal Spectrometer		active	Bragg crystal spectrometer for high-resolution X-ray line emission measurements [domain: plasma-diagnostics]	corpus`
语料源·GB/T-4960.9: 无命中（`gbt4960_9_diff.tsv` 的 `matched_concept_id` 无本 cid；全表无 X-ray crystal spectrometer 面形）
语料源·IAEA/ITER: 无命中（IAEA / ITER raw 两表均无 X-ray crystal spectrometer 条目）
语料源·URL: 不适用（该行 source=corpus，非 http(s) URL；无网络访问）
定义文本: en「A Bragg crystal spectrometer for high-resolution X-ray line emission measurements.」`definitions.tsv:6129`；zh「X射线晶体谱仪：用于高分辨X射线线发射测量的布拉格晶体谱仪。」`definitions.tsv:6130`（两行 source 列均为 corpus）
适用性推理: ①en 以三处限定语闭合概念：「A Bragg crystal spectrometer」限定色散机制与本体（布拉格晶体谱仪）、「high-resolution」限定分辨能力、「X-ray line emission measurements」限定测量对象为 X 射线线发射（谱线，非连续谱/成像）；notes 与 en 定义逐字一致，无口径漂移。②zh 与 en 逐句对位：「布拉格晶体谱仪」↔"A Bragg crystal spectrometer"、「高分辨」↔"high-resolution"、「X射线线发射测量」↔"X-ray line emission measurements"，无增义/漏义/误译。③同族核查（谱仪族）：本行与 G8-05 gamma-spectrometer（gamma 能量谱）、mass-spectrometer（质荷比）、survey-spectrometer（宽谱覆盖）以**测量谱段/色散机制**区隔，定义层面可区分，无同形面形冲突、非重复登记。观察项（不计 FAIL，别名锚定）：`aliases.tsv:10948` 将缩写 "XICS"（注释 expansion="X-ray **imaging** crystal spectrometer"）登记为本概念（generic "X-Ray Crystal Spectrometer"）的 alias，若按字面回译 XICS 会丢失 "imaging"（成像变体）限定；建议后续将 XICS 拆分或加注限定，避免误译。
判定: PASS
证据锚点: concepts.tsv:3334；definitions.tsv:6129；definitions.tsv:6130

### G8-07 remote-welding

样本: group=G8 | batch_scope=w1_b_b32..w1_c_b01 | concept_id=remote-welding | sha256_16=2ba12f90bb555b2c
原始语料: source=corpus → `terms/registry/concepts.tsv:3350` notes 原文「Welding of pipes and components performed by remote handling tools in activated environments [domain: remote-handling]」；整行逐字（列间为制表符）`remote-welding	method	远程焊接	Remote Welding		active	Welding of pipes and components performed by remote handling tools in activated environments [domain: remote-handling]	corpus`
语料源·GB/T-4960.9: 无命中（`gbt4960_9_diff.tsv` 的 `matched_concept_id` 无 `remote-welding`；全表无 remote welding 面形）
语料源·IAEA/ITER: 无命中（IAEA / ITER raw 两表均无 remote welding 条目）
语料源·URL: 不适用（该行 source=corpus，非 http(s) URL；无网络访问）
定义文本: en「Welding of pipes and components performed by remote handling tools in activated environments.」`definitions.tsv:6049`；zh「远程焊接：在活化环境下由遥控操作工具完成的管道与部件焊接。」`definitions.tsv:6050`（两行 source 列均为 corpus）
适用性推理: ①en 以三处限定语闭合概念：「of pipes and components」限定焊接对象（管道与部件）、「performed by remote handling tools」限定实施手段为遥控操作工具（非人工就地）、「in activated environments」限定场所为活化环境（人员不可达），完整刻画该方法的适用条件与手段；notes 与 en 定义逐字一致，无口径漂移。②zh 与 en 逐句对位：「管道与部件焊接」↔"Welding of pipes and components"、「由遥控操作工具完成」↔"performed by remote handling tools"、「在活化环境下」↔"in activated environments"，无增义/漏义/误译（「遥控操作工具」↔"remote handling tools" 语义一致）。③同族核查（remote-handling 批次 43 族）：`concepts.tsv:921` in-bore-welding（`definitions.tsv:2555/2556`「Welding inside narrow bore (e.g., heat-exchanger tubes) using miniature TIG or laser tools. / 在狭窄孔内（如换热器管）使用小型TIG或激光工具的焊接工艺。」）以"狭窄孔内 + 小型工具"为判别限定，是本概念的**特例（种）**，二者为属种关系、定义层面可区分；`concepts.tsv:1322` welding 为通用上位（焊接本体工艺）；`concepts.tsv:246/247` remote-handling / remote-maintenance 是手段体系与维护类别、非焊接动作——无同形面形冲突、非重复登记。观察项（不计 FAIL，别名过窄）：`aliases.tsv:11011/11012` 以 "remote pipe welding / 远程管道焊接" 为本概念 alias，较定义（pipes **and components**）偏窄，建议标注为窄义 alias。
判定: PASS
证据锚点: concepts.tsv:3350；definitions.tsv:6049；definitions.tsv:6050

### G8-08 parasitic-absorption

样本: group=G8 | batch_scope=w1_b_b32..w1_c_b01 | concept_id=parasitic-absorption | sha256_16=2bf212f5a5304d6c
原始语料: source=corpus → `terms/registry/concepts.tsv:3357` notes 原文「Unintended RF power absorption by plasma edge, antenna structure, or Faraday screen [domain: plasma-heating]」；整行逐字（列间为制表符）`parasitic-absorption	concept	寄生吸收	Parasitic Absorption		active	Unintended RF power absorption by plasma edge, antenna structure, or Faraday screen [domain: plasma-heating]	corpus`
语料源·GB/T-4960.9: 无命中（`gbt4960_9_diff.tsv` 的 `matched_concept_id` 无本 cid；全表无 parasitic absorption 面形）
语料源·IAEA/ITER: 无命中（IAEA raw 仅泛义 "absorption"（辐射能量转移），无 parasitic absorption；ITER raw 无对应条目）
语料源·URL: 不适用（该行 source=corpus，非 http(s) URL；无网络访问）
定义文本: en「Unintended RF power absorption by plasma edge, antenna structure, or Faraday screen.」`definitions.tsv:6011`；zh「寄生吸收：等离子体边界、天线结构或法拉第屏蔽上非预期的射频功率吸收。」`definitions.tsv:6012`（两行 source 列均为 corpus）
适用性推理: ①en 以两处限定语闭合概念：「Unintended」限定性质为**非预期**（与有意加热相对）、「by plasma edge, antenna structure, or Faraday screen」限定吸收发生地（边缘等离子体、天线结构、法拉第屏蔽三处，含非等离子体构件），完整刻画该寄生损耗的判据；notes 与 en 定义逐字一致，无口径漂移。②zh 与 en 逐句对位：「非预期的射频功率吸收」↔"Unintended RF power absorption"、「等离子体边界、天线结构或法拉第屏蔽上」↔"by plasma edge, antenna structure, or Faraday screen"，无增义/漏义/误译（"RF"↔「射频」、「Faraday screen」↔「法拉第屏蔽」一致）。③同族核查：`concepts.tsv:746` wave-absorption（`definitions.tsv:5809/5810`「Absorption of RF wave power by the plasma. / 波吸收是等离子体对射频波功率的吸收。」）限定为**等离子体对射频波的有意吸收**、本行限定为"非预期 + 天线/法拉第屏蔽等非等离子体场所"，二者以"意图 + 场所集"可区分；`concepts.tsv:1778` absorption 为 IAEA 泛义辐射吸收（`definitions.tsv:149/3526`），语义域不同——无同形面形冲突、非重复登记。残余观察（不计 FAIL）：两概念在"边缘等离子体吸收"上存在部分交叠（边缘等离子体亦属"plasma"），建议在 notes 互引以固边界。
判定: PASS
证据锚点: concepts.tsv:3357；definitions.tsv:6011；definitions.tsv:6012

---

## 判定汇总

- PASS: 8（strike-point-sweeping、energy-dump、tallying-efficiency、dissolution-precipitation-coefficient、gamma-spectrometer、x-ray-crystal-spectrometer、remote-welding、parasitic-absorption）
- FAIL: 0
- UNDECIDABLE: 0
- 一致性硬规则核对：`原始语料`（source 主导项）不可得条数 = 0 = `判定: UNDECIDABLE` 条数 = 0 ✔；无任何"源不可得却 PASS"的条目 ✔
- G8 批次结论：8 条 en 定义均以判别性限定语准确刻画概念，zh↔en 定义句等价（仅 G8-04 一处域内可接受的轻微窄化），且与同族 active 概念在定义层面均可区分、无面形冲突/重复登记 —— 达到 M1 该组全 PASS 门槛。共记录 6 条观察项（O1–O6，均不改变判定，见下）。

## 观察项（不计入三值，不改变判定）

| O<n> | cid | 观察 | 类别 |
|---|---|---|---|
| O1 | energy-dump | 与 dump-resistor / quench-protection / magnet-protection-system 共享「失超 + 耗散磁体储能」核心限定，四者本体层级（回路/元件/措施/系统）应显式互引以固边界 | 同族边界标注 |
| O2 | tallying-efficiency | 库外同形：preferred_zh「计数效率」与探测计量学 "counting efficiency" 同形（库内无同名 active 概念）；族内 tally 中文面形不统一（计数统计 / 记数器 / 计数效率） | 术语命名一致性 |
| O3 | dissolution-precipitation-coefficient | en "dissolved species" 在 zh 收窄为「溶解态核素」（域内成立）；preferred_en 为小写，与同族 Title Case 不一致 | 命名一致性/格式 |
| O4 | x-ray-crystal-spectrometer | alias "XICS"（expansion 含 "imaging"）指向 generic 概念，字面回译丢失成像限定 | 别名锚定 |
| O5 | remote-welding | alias "remote pipe welding / 远程管道焊接" 窄于定义（pipes and components） | 别名过窄 |
| O6 | parasitic-absorption | 与 wave-absorption 在"边缘等离子体吸收"上部分交叠，建议 notes 互引固边界 | 同族边界标注 |

## 缺陷台账（行数 = FAIL + UNDECIDABLE = 0）

| D<n> | <cid> | <FAIL\|UNDECIDABLE> | 原因 |
|---|---|---|---|

（本组 FAIL + UNDECIDABLE = 0，故台账无数据行；上述 O1–O6 为观察项，按口径不计入三值。）

## AC 自检（实跑记录）

| AC 项 | 命令 | 实测 |
|---|---|---|
| 样本标题数 = 8 | `grep -c '^### ' docs/reviews/t5184/m1-group-G8.md` | 8（G8-01..G8-08） |
| 判定行数 = 8 | `grep -cP '^判定: (PASS\|FAIL\|UNDECIDABLE)$' …` | 8 |
| 三值 = 8 | PASS 8 + FAIL 0 + UNDECIDABLE 0 | 8 |
| 四字段各 ≥8 | `^原始语料: ` / `^定义文本: ` / `^适用性推理: ` / `^证据锚点: `（字段行行首无 `- `，与 G1–G4 现存格式一致） | 8 / 8 / 8 / 8 |
| concepts.tsv 锚点 ≥8 | `grep -o 'concepts\.tsv:[0-9]*' … \| wc -l` | ≥8（8 条主锚点 + 同族引用） |
| definitions.tsv 锚点 ≥16 | `grep -o 'definitions\.tsv:[0-9]*' … \| wc -l` | ≥16（每样本定义文本 2 + 同族定义引用） |
| 不可得数 == UNDECIDABLE 数 | 主导项 `^原始语料:.*不可得` 计数 vs `^判定: UNDECIDABLE$` 计数 | 0 == 0 ✔ |
| 台账行数 == FAIL+UNDECIDABLE | 台账数据行计数 vs 0 | 0 == 0 ✔ |
| git status 仅本 md 新增 | `git status --short` | 仅本文件为本会话新增；未改任何已跟踪文件（`git diff --stat` 空） |

## 备注与后续动作

1. 本报告**未**新建 .bib/引用，**未**修改任何术语/定义/语料文件；O1–O6 属建议修复项（术语规范化/别名锚定），是否执行由 orchestrator / 作者裁决（本 agent 只复核、不改术语数据）。
2. 路径更正记录：任务书假设 `.github/plans/t4973-batches/` 不存在，**实测该目录存在**；GB/T 对照证据实际取自 `artifacts/terminology_sources/gbt4960_9_diff.tsv`（与任务书文件名一致），未使用 `t4973-batches/` 下任何 diff 文件。
3. 来源可得性：本组 8 行 `source` 均 = `corpus`（主导项 8/8 可得）；GB/T、IAEA、ITER 子来源 8/8 无命中；URL 子项 8/8 不适用 —— 与「主导项不可得数 = UNDECIDABLE 数 = 0」一致。
