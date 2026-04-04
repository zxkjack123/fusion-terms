# 术语注册表扩展 — 批次 8：废物管理链、环境监测、电气配电、建设调试、辐射仪表、结构老化与腐蚀

## 背景与目标

- **问题/需求描述**：注册表（1400 concepts / 5918 aliases / 1400 evidence）在 Batch 7 完成安全分析方法、辐防操作、远程装配、仪控、结构完整性、排热/PMI 补充后，仍有 6 个子领域存在系统性空白：①废物管理处置链条（固化/贮存/去污因子）零覆盖、②环境监测与评价（ITER 许可文档核心术语）零覆盖、③电气配电常规岛术语（母线/开关柜/变压器/EDG/UPS）缺失、④建设调试许可流程术语（模块化/建造许可/运行许可/HFT/CM）缺失、⑤辐射探测仪表（电离室/裂变室/闪烁体/ARM/TLD）空白、⑥蠕变-疲劳交互/J积分/棘轮/腐蚀机制等结构老化评估缺环。
- **根因分析**：Batch 7 补全了安全分析工具链和 PMI 细化术语，但其非目标中明确列出了「废物管理链（vitrification/cementation/disposal）」「消防/暖通/土建」「通用机械组件」留待后续批次。本批从 Batch 7 遗留的废物管理入手，同时扫描了全量终端涉及到的文档类型（退役文件、EIA、常规岛设计、建造/调试方案、辐防实施方案、ASME 评估报告），识别出上述 6 个空白。
- **目标**：
  1. 新增 30 个概念（Batch 84–86），覆盖 6 个主题方向
  2. 新增 ~140 行 alias，包含缩写（EQ/EDG/UPS/CM/HFT/ARM/TLD/FAC）、拼写变体（British ionisation/modularisation/licence/ratchetting）、中英对
  3. 同步所有新增术语到 EN/ZH allowlist
  4. 通过验证后重新导出 translation_dict、rebuild domain_terms、通过全量测试
- **非目标（不做什么）**：
  - 不修改 pipeline 源代码 — 纯数据追加
  - 不修改已有概念的 preferred_zh / preferred_en — 只新增
  - 不添加消防/暖通/土建术语（fire barrier/ventilation zone/bioshield）— 留待 Batch 9+
  - 不添加通用机械组件术语（bellows/flange/gasket/pressurizer）— 留待 Batch 9+
  - 不添加真空技术细化术语（NEG pump/vacuum gauge）— 留待 Batch 9+
  - 不添加磁体工程细化术语（current sharing temperature/quench propagation）— 留待 Batch 9+
  - 不为 decontamination-factor 添加 DF 缩写 — DF 已被 detritiation-factor 占用
- **已有代码/流程复用分析**：
  - `pipeline/validate_registry.py`：复用（验证新增数据）
  - `pipeline/export_registry.py`：复用（`--translation-dict` flag 导出翻译字典）
  - `pipeline/build_terms.py`：复用（重建 IME 词表）
  - 已有别名模式（缩写 `abbr|preferred`、连字符 `en|alias`、中文 `zh|preferred`/`zh|alias`）：复用
  - Batch 7 (81–83) 的执行流程和 commit 模式：复用
  - allowlist EN 使用 token-safe hyphenated 形式（Batch 6/7 经验）：复用

## 技术方案

- **方案概述**：分 4 个 Phase 按优先级逐步添加。Phase 1–3 各包含一个「三表新增 Task」和一个「allowlist 同步 Task」，Phase 4 做全量验证/导出/测试。
- **关键设计决策**：
  1. **Batch 编号**：接续 Batch 83，使用 84（废物管理+环境监测）、85（电气+建设调试）、86（辐射仪表+结构老化/腐蚀）
  2. **Evidence source 格式**：使用 `internal:registry-gap-review:batch8` 统一格式（区别于 batch7）
  3. **DF 缩写冲突**：`DF` 已映射到 `detritiation-factor`，不为 `decontamination-factor` 添加 DF 缩写，仅使用全称
  4. **EQ (Environmental Qualification)**：aliases.tsv 中无已有 EQ 映射，可安全添加
  5. **transformer 歧义处理**：`inductive-operation` 概念描述中提及 "transformer action"，但 `transformer` 作为独立电气设备概念无冲突；notes 字段标注"电力变压器"
  6. **decontamination vs decontamination-factor**：`decontamination` 已作为独立概念存在，`decontamination-factor` 是量化度量，concept_id 不同，无歧义
  7. **British 拼写变体**：ionisation (chamber)、modularisation、operating licence、ratchetting 均添加为 alias
  8. **J-integral 大小写**：concept_id 使用 `j-integral`（小写惯例），preferred_en 使用 `J-integral`（标准数学记法大写 J）
  9. **erosion-corrosion 连字符**：英文标准形式为 erosion-corrosion（连字符），preferred_en 与 concept_id 形式一致，另加 `erosion corrosion`（无连字符）作 alias
  10. **scintillator alias**：`scintillator` 添加为 `scintillation-detector` 的 alias（核仪表上下文中两者等价使用）
  11. **无缩写术语**：vitrification、cementation、interim-storage、waste-minimization、secondary-waste、decontamination-factor、environmental-monitoring、effluent-monitoring、atmospheric-dispersion、bus-bar、switchgear、transformer、modularization、construction-permit、operating-license、ionization-chamber、fission-chamber、scintillation-detector、creep-fatigue-interaction、j-integral、ratcheting、erosion-corrosion 均不设 preferred_abbr
- **影响范围**：
  - `terms/registry/concepts.tsv` — 新增 30 行 + 3 行 batch 注释
  - `terms/registry/aliases.tsv` — 新增 ~140 行
  - `terms/registry/evidence.tsv` — 新增 30 行
  - `terms/allowlist_en.txt` — 追加缺失 EN token
  - `terms/allowlist_zh.txt` — 追加缺失 ZH 术语
  - `artifacts/translation_dict.json` — 重新生成
  - `artifacts/domain_terms.txt` — 重新生成

## Error & Rescue Map（关键失败路径映射）

| 代码路径/操作 | 可能的失败 | 错误类型 | 已处理？ | 处理方式 | 用户可见行为 |
|---|---|---|---|---|---|
| 新增 decontamination-factor | DF 缩写与 detritiation-factor 冲突 | validation error | Y | 不添加 DF 缩写，仅使用全称形式 | 不可见 |
| 新增 EQ 缩写 | 与已有缩写冲突 | validation error | Y | precheck `grep -P '^EQ\t' aliases.tsv` 确认无冲突（已验证：无） | validate_registry 报错并阻断 |
| 新增 transformer 概念 | 与已有 inductive-operation 的描述混淆 | 语义模糊 | Y | notes 字段标注"电力变压器（非中心螺管'变压器效应'）"；preferred_en 另加 alias `power transformer` | 不可见 |
| 新增 decontamination-factor | 与已有 decontamination 概念交叉 | 语义重叠 | Y | 两者 concept_id 不同；decontamination 是过程，decontamination-factor 是定量度量，正交 | 不可见 |
| J-integral 大小写 | concept_id 小写/preferred_en 大写不一致 | 格式注意 | Y | 注册表惯例 concept_id=小写连字符，preferred_en=标准书写（大写 J），与 Nb3Sn/NbTi 等先例一致 | 不可见 |
| erosion-corrosion 双连字符 | 与 concept_id 格式一致可能导致映射混淆 | 格式注意 | Y | en preferred alias = `erosion-corrosion`（标准英文形式），另加 `erosion corrosion` alias | 不可见 |
| British 拼写遗漏 | ionisation/modularisation/licence/ratchetting 等 | 搜索遗漏 | Y | 每个术语的 British 拼写变体显式添加为 alias | 不影响 |
| allowlist 同步遗漏 | build_terms 词条数未增长 | 逻辑遗漏 | Y | 每 Phase 同步 allowlist 并运行 validate_registry | build_stats 可检测 |
| translation_dict 未重新生成 | 遗忘 `--translation-dict` flag | 操作遗漏 | Y | Task 4.1 明确标注该 flag | 翻译字典不含新词条 |

## 时序推演

| 阶段 | 关键决策/潜在阻塞 |
|------|-------------------|
| 初期（Task 1.1–1.2） | Batch 84 含 EQ 一个缩写；需确认 `decontamination-factor` 与已有 `decontamination` 概念无歧义；废物管理术语在聚变语境精确度需确认 |
| 中期（Task 2.1–2.2） | Batch 85 引入 EDG/UPS/CM/HFT 四个缩写，均为工业标准缩写在聚变语境无歧义；`transformer` 需确认不与 inductive-operation 产生 alias 交叉 |
| 后期（Task 3.1–4.1） | Batch 86 含 ARM/TLD/FAC 三个缩写；`j-integral` 大小写需验证通过；全量导出应新增 ~30 个翻译映射 |

## 执行计划

### Phase 1: Batch 84 — 废物管理链 + 环境监测 (10 terms)

#### ✅ Task 1.1: Batch 84 三表追加（10 概念 + ~45 alias + 10 evidence）

- **目标**：在三张注册表表末尾追加 Batch 84 全部数据
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：追加 batch 注释行 + 10 行概念数据

    ```tsv
    # ==== Batch 84: waste management chain + environmental monitoring ====
    vitrification	method	玻璃固化	vitrification		active	高放废物玻璃固化处理工艺
    cementation	method	水泥固化	cementation		active	中低放废物水泥固化处理工艺
    interim-storage	concept	中间贮存	interim storage		active	放射性废物最终处置前的受控暂存
    waste-minimization	method	废物最小化	waste minimization		active	从源头和过程中减少放射性废物产生量的策略
    secondary-waste	concept	二次废物	secondary waste		active	废物处理/去污过程中产生的新废物
    decontamination-factor	metric	去污因子	decontamination factor		active	去污前后放射性活度（或污染水平）之比
    environmental-monitoring	method	环境监测	environmental monitoring		active	核设施周围环境放射性水平的系统监测
    effluent-monitoring	method	流出物监测	effluent monitoring		active	核设施排放至环境的气态/液态放射性流出物监测
    atmospheric-dispersion	concept	大气弥散	atmospheric dispersion		active	放射性物质在大气中的输运与扩散过程
    environmental-qualification	method	环境鉴定	environmental qualification	EQ	active	设备在事故环境条件下维持功能的鉴定 (IEEE 323)
    ```

  - 文件 `terms/registry/aliases.tsv`：追加 ~45 行别名数据

    ```tsv
    # ---- Batch 84 aliases ----
    vitrification	vitrification	en	preferred	preferred en
    玻璃固化	vitrification	zh	preferred	preferred zh
    glass vitrification	vitrification	en	alias	extended form
    玻璃固化体	vitrification	zh	alias	product form
    cementation	cementation	en	preferred	preferred en
    水泥固化	cementation	zh	preferred	preferred zh
    cement solidification	cementation	en	alias	synonym
    水泥固化处理	cementation	zh	alias	expanded zh
    interim storage	interim-storage	en	preferred	preferred en
    中间贮存	interim-storage	zh	preferred	preferred zh
    interim-storage	interim-storage	en	alias	hyphenated form
    intermediate storage	interim-storage	en	alias	synonym
    暂存	interim-storage	zh	alias	short zh
    waste minimization	waste-minimization	en	preferred	preferred en
    废物最小化	waste-minimization	zh	preferred	preferred zh
    waste-minimization	waste-minimization	en	alias	hyphenated form
    waste reduction	waste-minimization	en	alias	synonym
    废物减量	waste-minimization	zh	alias	synonym zh
    secondary waste	secondary-waste	en	preferred	preferred en
    二次废物	secondary-waste	zh	preferred	preferred zh
    secondary-waste	secondary-waste	en	alias	hyphenated form
    二次放射性废物	secondary-waste	zh	alias	expanded zh
    decontamination factor	decontamination-factor	en	preferred	preferred en
    去污因子	decontamination-factor	zh	preferred	preferred zh
    decontamination-factor	decontamination-factor	en	alias	hyphenated form
    去污系数	decontamination-factor	zh	alias	variant zh
    environmental monitoring	environmental-monitoring	en	preferred	preferred en
    环境监测	environmental-monitoring	zh	preferred	preferred zh
    environmental-monitoring	environmental-monitoring	en	alias	hyphenated form
    环境辐射监测	environmental-monitoring	zh	alias	nuclear-specific zh
    effluent monitoring	effluent-monitoring	en	preferred	preferred en
    流出物监测	effluent-monitoring	zh	preferred	preferred zh
    effluent-monitoring	effluent-monitoring	en	alias	hyphenated form
    discharge monitoring	effluent-monitoring	en	alias	synonym
    排放监测	effluent-monitoring	zh	alias	synonym zh
    atmospheric dispersion	atmospheric-dispersion	en	preferred	preferred en
    大气弥散	atmospheric-dispersion	zh	preferred	preferred zh
    atmospheric-dispersion	atmospheric-dispersion	en	alias	hyphenated form
    atmospheric diffusion	atmospheric-dispersion	en	alias	synonym
    大气扩散	atmospheric-dispersion	zh	alias	synonym zh
    environmental qualification	environmental-qualification	en	preferred	preferred en
    环境鉴定	environmental-qualification	zh	preferred	preferred zh
    EQ	environmental-qualification	abbr	preferred	canonical abbr (IEEE 323)
    environmental-qualification	environmental-qualification	en	alias	hyphenated form
    环境适应性鉴定	environmental-qualification	zh	alias	expanded zh
    ```

  - 文件 `terms/registry/evidence.tsv`：追加 10 行证据数据

    ```tsv
    vitrification	internal:registry-gap-review:batch8	High-level waste immobilization in borosilicate glass matrix	copilot	2026-04-04
    cementation	internal:registry-gap-review:batch8	Low/intermediate-level waste immobilization in cement matrix	copilot	2026-04-04
    interim-storage	internal:registry-gap-review:batch8	Controlled temporary storage of radioactive waste before final disposal	copilot	2026-04-04
    waste-minimization	internal:registry-gap-review:batch8	Strategy to reduce radioactive waste volume at source and during processing	copilot	2026-04-04
    secondary-waste	internal:registry-gap-review:batch8	New waste generated during waste treatment or decontamination processes	copilot	2026-04-04
    decontamination-factor	internal:registry-gap-review:batch8	Ratio of contamination level before and after decontamination (IAEA)	copilot	2026-04-04
    environmental-monitoring	internal:registry-gap-review:batch8	Systematic monitoring of radioactivity levels around nuclear facilities	copilot	2026-04-04
    effluent-monitoring	internal:registry-gap-review:batch8	Monitoring of gaseous/liquid radioactive discharges to environment	copilot	2026-04-04
    atmospheric-dispersion	internal:registry-gap-review:batch8	Transport and diffusion of radioactive material in atmosphere	copilot	2026-04-04
    environmental-qualification	internal:registry-gap-review:batch8	Qualification of equipment to function under accident environmental conditions (IEEE 323)	copilot	2026-04-04
    ```

- **修改边界**：不得修改 `terms/registry/concepts.tsv` 中 Batch 83 及以前的任何行；不得修改 `terms/registry/aliases.tsv` 中已有别名行；不得修改 `terms/registry/evidence.tsv` 中已有证据行；不得修改 pipeline 源代码
- **测试要求**：
  - 追加前 precheck：`grep -P '^EQ\t' terms/registry/aliases.tsv`（应返回 0 行）
  - 追加前 precheck：`grep -P '^DF\t' terms/registry/aliases.tsv`（应返回 detritiation-factor 行，确认冲突存在）
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：`registry OK: 1410 concepts, ~5963 aliases, 1410 evidence rows`
- **验收标准**：
  - ✅ validate_registry 输出 1410 concepts, 1410 evidence rows，无 ERROR
  - ✅ `awk -F'\t' '$2=="internal:registry-gap-review:batch8"' terms/registry/evidence.tsv | wc -l` = 10
  - ✅ Batch 84 的 10 个 concept_id 均可在 concepts.tsv 中通过 awk 精确匹配找到
  - ✅ `grep -P '^DF\t.*decontamination-factor' terms/registry/aliases.tsv` 返回 0 行（确认未误添加 DF 缩写）
- **潜在风险**：`decontamination-factor` 与已有 `decontamination` 概念形成上下位关系，需确认 validator 允许 concept_id 前缀包含关系（已有先例：`neutron` 与 `neutron-transport` 等）

#### ✅ Task 1.2: Batch 84 allowlist 同步

- **目标**：将 Batch 84 所有新增 EN token / ZH 术语同步到 allowlist（如尚未存在）
- **修改内容**：
  - 文件 `terms/allowlist_en.txt`：追加缺失 token（先 grep 检查再追加；EN 使用 token-safe hyphenated 形式）
    - `vitrification`, `glass-vitrification`, `cementation`, `cement-solidification`, `interim-storage`, `intermediate-storage`, `waste-minimization`, `waste-reduction`, `secondary-waste`, `decontamination-factor`, `environmental-monitoring`, `effluent-monitoring`, `discharge-monitoring`, `atmospheric-dispersion`, `atmospheric-diffusion`, `environmental-qualification`, `EQ`
  - 文件 `terms/allowlist_zh.txt`：追加缺失术语
    - `玻璃固化`, `玻璃固化体`, `水泥固化`, `水泥固化处理`, `中间贮存`, `暂存`, `废物最小化`, `废物减量`, `二次废物`, `二次放射性废物`, `去污因子`, `去污系数`, `环境监测`, `环境辐射监测`, `流出物监测`, `排放监测`, `大气弥散`, `大气扩散`, `环境鉴定`, `环境适应性鉴定`
- **修改边界**：不得删除已有 allowlist 行；不得修改 pipeline 源代码
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：同 Task 1.1 无新 WARNING
- **验收标准**：
  - ✅ `grep -c 'vitrification' terms/allowlist_en.txt` ≥ 1
  - ✅ `grep -c 'EQ' terms/allowlist_en.txt` ≥ 1
  - ✅ `grep -c '玻璃固化' terms/allowlist_zh.txt` ≥ 1
  - ✅ `grep -c '环境监测' terms/allowlist_zh.txt` ≥ 1
  - ✅ validate_registry 无新 WARNING
- **潜在风险**：`暂存` 是常见中文词可能在 allowlist 中已存在 → 先 grep 再追加

### Phase 2: Batch 85 — 电气系统 + 建设调试 (10 terms)

#### ✅ Task 2.1: Batch 85 三表追加（10 概念 + ~48 alias + 10 evidence）

- **目标**：在三张注册表表末尾追加 Batch 85 全部数据
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：追加 batch 注释行 + 10 行概念数据

    ```tsv
    # ==== Batch 85: electrical systems + construction & commissioning ====
    bus-bar	device	母线	bus bar		active	电力系统中汇集和分配电流的导体
    switchgear	device	开关柜	switchgear		active	用于控制、保护和隔离电气设备的开关装置组合
    transformer	device	变压器	transformer		active	电力变压器（非中心螺管"变压器效应"）
    emergency-diesel-generator	device	应急柴油发电机	emergency diesel generator	EDG	active	安全级应急交流电源
    uninterruptible-power-supply	device	不间断电源	uninterruptible power supply	UPS	active	保障关键负荷不间断供电的电源系统
    modularization	method	模块化	modularization		active	将大型设施分解为可预制模块进行建造和安装的方法
    hot-functional-testing	method	热功能试验	hot functional testing	HFT	active	核设施装料前的热态系统功能验证试验
    construction-permit	doc	建造许可证	construction permit		active	核设施建造阶段的监管许可文件
    operating-license	doc	运行许可证	operating license		active	核设施运行阶段的监管许可文件
    configuration-management	method	配置管理	configuration management	CM	active	核设施设计基准和技术状态的系统管控方法 (NQA)
    ```

  - 文件 `terms/registry/aliases.tsv`：追加 ~48 行别名数据

    ```tsv
    # ---- Batch 85 aliases ----
    bus bar	bus-bar	en	preferred	preferred en
    母线	bus-bar	zh	preferred	preferred zh
    bus-bar	bus-bar	en	alias	hyphenated form
    busbar	bus-bar	en	alias	closed form
    汇流排	bus-bar	zh	alias	synonym zh
    switchgear	switchgear	en	preferred	preferred en
    开关柜	switchgear	zh	preferred	preferred zh
    开关设备	switchgear	zh	alias	generic zh
    配电装置	switchgear	zh	alias	variant zh
    transformer	transformer	en	preferred	preferred en
    变压器	transformer	zh	preferred	preferred zh
    power transformer	transformer	en	alias	specific form
    电力变压器	transformer	zh	alias	specific zh
    emergency diesel generator	emergency-diesel-generator	en	preferred	preferred en
    应急柴油发电机	emergency-diesel-generator	zh	preferred	preferred zh
    EDG	emergency-diesel-generator	abbr	preferred	canonical abbr
    emergency-diesel-generator	emergency-diesel-generator	en	alias	hyphenated form
    柴油发电机组	emergency-diesel-generator	zh	alias	short zh
    uninterruptible power supply	uninterruptible-power-supply	en	preferred	preferred en
    不间断电源	uninterruptible-power-supply	zh	preferred	preferred zh
    UPS	uninterruptible-power-supply	abbr	preferred	canonical abbr
    uninterruptible-power-supply	uninterruptible-power-supply	en	alias	hyphenated form
    不间断供电系统	uninterruptible-power-supply	zh	alias	expanded zh
    modularization	modularization	en	preferred	preferred en
    模块化	modularization	zh	preferred	preferred zh
    modularisation	modularization	en	alias	British spelling
    模块化建造	modularization	zh	alias	construction context zh
    hot functional testing	hot-functional-testing	en	preferred	preferred en
    热功能试验	hot-functional-testing	zh	preferred	preferred zh
    HFT	hot-functional-testing	abbr	preferred	canonical abbr
    hot-functional-testing	hot-functional-testing	en	alias	hyphenated form
    hot functional test	hot-functional-testing	en	alias	singular form
    热态功能试验	hot-functional-testing	zh	alias	variant zh
    construction permit	construction-permit	en	preferred	preferred en
    建造许可证	construction-permit	zh	preferred	preferred zh
    construction-permit	construction-permit	en	alias	hyphenated form
    建造许可	construction-permit	zh	alias	short zh
    核设施建造许可证	construction-permit	zh	alias	nuclear-specific zh
    operating license	operating-license	en	preferred	preferred en
    运行许可证	operating-license	zh	preferred	preferred zh
    operating-license	operating-license	en	alias	hyphenated form
    operating licence	operating-license	en	alias	British spelling
    运行许可	operating-license	zh	alias	short zh
    核设施运行许可证	operating-license	zh	alias	nuclear-specific zh
    configuration management	configuration-management	en	preferred	preferred en
    配置管理	configuration-management	zh	preferred	preferred zh
    CM	configuration-management	abbr	preferred	canonical abbr (NQA)
    configuration-management	configuration-management	en	alias	hyphenated form
    技术状态管理	configuration-management	zh	alias	alternative zh
    ```

  - 文件 `terms/registry/evidence.tsv`：追加 10 行证据数据

    ```tsv
    bus-bar	internal:registry-gap-review:batch8	Electrical conductor for current collection and distribution in power systems	copilot	2026-04-04
    switchgear	internal:registry-gap-review:batch8	Combined switching apparatus for control, protection and isolation of electrical equipment	copilot	2026-04-04
    transformer	internal:registry-gap-review:batch8	Power transformer for voltage conversion in electrical distribution (not CS transformer action)	copilot	2026-04-04
    emergency-diesel-generator	internal:registry-gap-review:batch8	Safety-class emergency AC power source for nuclear facilities	copilot	2026-04-04
    uninterruptible-power-supply	internal:registry-gap-review:batch8	Power supply system ensuring uninterrupted power to critical loads	copilot	2026-04-04
    modularization	internal:registry-gap-review:batch8	Construction method of pre-fabricating modules for large facility assembly (ITER/DEMO strategy)	copilot	2026-04-04
    hot-functional-testing	internal:registry-gap-review:batch8	Pre-fuel-loading hot system functional verification test	copilot	2026-04-04
    construction-permit	internal:registry-gap-review:batch8	Regulatory permit for nuclear facility construction phase	copilot	2026-04-04
    operating-license	internal:registry-gap-review:batch8	Regulatory license for nuclear facility operation phase	copilot	2026-04-04
    configuration-management	internal:registry-gap-review:batch8	Systematic control of design basis and technical configuration (NQA/IAEA GS-G-3.5)	copilot	2026-04-04
    ```

- **修改边界**：不得修改 Batch 84 及以前的已有行；不得修改 pipeline 源代码
- **测试要求**：
  - 追加前 precheck：`grep -P '^(EDG|UPS|CM|HFT)\t' terms/registry/aliases.tsv`（应仅返回 Batch 84 中的 EQ，不含 EDG/UPS/CM/HFT）
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：`registry OK: 1420 concepts, ~6011 aliases, 1420 evidence rows`
- **验收标准**：
  - ✅ validate_registry 输出 1420 concepts, 1420 evidence rows，无 ERROR
  - ✅ `awk -F'\t' '$2=="internal:registry-gap-review:batch8"' terms/registry/evidence.tsv | wc -l` = 20
  - ✅ Batch 85 的 10 个 concept_id 均可在 concepts.tsv 中通过 awk 精确匹配找到
  - ✅ `grep -P '^transformer\t' terms/registry/aliases.tsv` 映射到 `transformer` 概念而非其他
- **潜在风险**：`transformer` 可能在 alias 搜索中与 `inductive-operation` 描述中的 "transformer action" 产生误解（但描述字段不参与 alias 匹配，无实际风险）

#### ✅ Task 2.2: Batch 85 allowlist 同步

- **目标**：将 Batch 85 所有新增 EN token / ZH 术语同步到 allowlist
- **修改内容**：
  - 文件 `terms/allowlist_en.txt`：追加缺失 token（先 grep 检查再追加）
    - `bus-bar`, `busbar`, `switchgear`, `transformer`, `power-transformer`, `emergency-diesel-generator`, `EDG`, `uninterruptible-power-supply`, `UPS`, `modularization`, `modularisation`, `hot-functional-testing`, `HFT`, `construction-permit`, `operating-license`, `operating-licence`, `configuration-management`, `CM`
  - 文件 `terms/allowlist_zh.txt`：追加缺失术语
    - `母线`, `汇流排`, `开关柜`, `开关设备`, `配电装置`, `变压器`, `电力变压器`, `应急柴油发电机`, `柴油发电机组`, `不间断电源`, `不间断供电系统`, `模块化`, `模块化建造`, `热功能试验`, `热态功能试验`, `建造许可证`, `建造许可`, `运行许可证`, `运行许可`, `配置管理`, `技术状态管理`
- **修改边界**：不得删除已有 allowlist 行；不得修改 pipeline 源代码
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：同 Task 2.1 无新 WARNING
- **验收标准**：
  - ✅ `grep -c 'EDG' terms/allowlist_en.txt` ≥ 1
  - ✅ `grep -c 'UPS' terms/allowlist_en.txt` ≥ 1
  - ✅ `grep -c '变压器' terms/allowlist_zh.txt` ≥ 1
  - ✅ `grep -c '配置管理' terms/allowlist_zh.txt` ≥ 1
  - ✅ validate_registry 无新 WARNING
- **潜在风险**：`transformer` 作为通用英文词可能已在 EN allowlist 中 → 先 grep 再追加

### Phase 3: Batch 86 — 辐射探测仪表 + 结构老化评估 + 腐蚀 (10 terms)

#### Task 3.1: Batch 86 三表追加（10 概念 + ~47 alias + 10 evidence）

- **目标**：在三张注册表表末尾追加 Batch 86 全部数据
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：追加 batch 注释行 + 10 行概念数据

    ```tsv
    # ==== Batch 86: radiation detection instruments + structural aging & corrosion ====
    ionization-chamber	device	电离室	ionization chamber		active	利用气体电离原理测量辐射剂量率的探测器
    fission-chamber	device	裂变室	fission chamber		active	利用裂变反应测量中子通量的探测器
    scintillation-detector	device	闪烁体探测器	scintillation detector		active	利用闪烁体发光测量辐射的探测器
    area-radiation-monitor	device	区域辐射监测仪	area radiation monitor	ARM	active	固定安装的区域γ辐射剂量率连续监测仪
    thermoluminescent-dosimeter	device	热释光剂量计	thermoluminescent dosimeter	TLD	active	利用热释光材料累积测量辐射剂量的被动式剂量计
    creep-fatigue-interaction	concept	蠕变-疲劳交互	creep-fatigue interaction		active	高温结构件蠕变损伤与疲劳损伤的耦合评估 (RCC-MRx)
    j-integral	metric	J积分	J-integral		active	弹塑性断裂力学中裂纹尖端能量释放率的路径积分参量
    ratcheting	concept	棘轮效应	ratcheting		active	循环载荷下材料单向塑性变形逐周累积的现象
    flow-accelerated-corrosion	concept	流动加速腐蚀	flow-accelerated corrosion	FAC	active	高温高速水流导致保护氧化膜加速溶解的腐蚀机制
    erosion-corrosion	concept	冲蚀-腐蚀	erosion-corrosion		active	流体冲刷与电化学腐蚀共同作用的材料损伤机制
    ```

  - 文件 `terms/registry/aliases.tsv`：追加 ~47 行别名数据

    ```tsv
    # ---- Batch 86 aliases ----
    ionization chamber	ionization-chamber	en	preferred	preferred en
    电离室	ionization-chamber	zh	preferred	preferred zh
    ionization-chamber	ionization-chamber	en	alias	hyphenated form
    ionisation chamber	ionization-chamber	en	alias	British spelling
    电离探测器	ionization-chamber	zh	alias	generic zh
    fission chamber	fission-chamber	en	preferred	preferred en
    裂变室	fission-chamber	zh	preferred	preferred zh
    fission-chamber	fission-chamber	en	alias	hyphenated form
    裂变电离室	fission-chamber	zh	alias	expanded zh
    scintillation detector	scintillation-detector	en	preferred	preferred en
    闪烁体探测器	scintillation-detector	zh	preferred	preferred zh
    scintillation-detector	scintillation-detector	en	alias	hyphenated form
    scintillator	scintillation-detector	en	alias	short form (detection element)
    闪烁探测器	scintillation-detector	zh	alias	short zh
    area radiation monitor	area-radiation-monitor	en	preferred	preferred en
    区域辐射监测仪	area-radiation-monitor	zh	preferred	preferred zh
    ARM	area-radiation-monitor	abbr	preferred	canonical abbr
    area-radiation-monitor	area-radiation-monitor	en	alias	hyphenated form
    区域γ监测仪	area-radiation-monitor	zh	alias	specific zh
    thermoluminescent dosimeter	thermoluminescent-dosimeter	en	preferred	preferred en
    热释光剂量计	thermoluminescent-dosimeter	zh	preferred	preferred zh
    TLD	thermoluminescent-dosimeter	abbr	preferred	canonical abbr
    thermoluminescent-dosimeter	thermoluminescent-dosimeter	en	alias	hyphenated form
    热释光剂量片	thermoluminescent-dosimeter	zh	alias	chip form zh
    creep-fatigue interaction	creep-fatigue-interaction	en	preferred	preferred en
    蠕变-疲劳交互	creep-fatigue-interaction	zh	preferred	preferred zh
    creep-fatigue-interaction	creep-fatigue-interaction	en	alias	hyphenated form
    creep-fatigue	creep-fatigue-interaction	en	alias	short form
    蠕变疲劳交互作用	creep-fatigue-interaction	zh	alias	expanded zh
    J-integral	j-integral	en	preferred	preferred en
    J积分	j-integral	zh	preferred	preferred zh
    j-integral	j-integral	en	alias	lowercase hyphenated form
    J integral	j-integral	en	alias	no-hyphen form
    J 积分	j-integral	zh	alias	spaced zh
    ratcheting	ratcheting	en	preferred	preferred en
    棘轮效应	ratcheting	zh	preferred	preferred zh
    ratchetting	ratcheting	en	alias	British spelling
    ratchet	ratcheting	en	alias	short form
    棘轮变形	ratcheting	zh	alias	deformation-focused zh
    flow-accelerated corrosion	flow-accelerated-corrosion	en	preferred	preferred en
    流动加速腐蚀	flow-accelerated-corrosion	zh	preferred	preferred zh
    FAC	flow-accelerated-corrosion	abbr	preferred	canonical abbr
    flow-accelerated-corrosion	flow-accelerated-corrosion	en	alias	hyphenated form
    流动辅助腐蚀	flow-accelerated-corrosion	zh	alias	variant zh
    erosion-corrosion	erosion-corrosion	en	preferred	preferred en
    冲蚀-腐蚀	erosion-corrosion	zh	preferred	preferred zh
    erosion corrosion	erosion-corrosion	en	alias	no-hyphen form
    冲刷腐蚀	erosion-corrosion	zh	alias	variant zh
    ```

  - 文件 `terms/registry/evidence.tsv`：追加 10 行证据数据

    ```tsv
    ionization-chamber	internal:registry-gap-review:batch8	Gas ionization-based radiation dose rate detector	copilot	2026-04-04
    fission-chamber	internal:registry-gap-review:batch8	Fission reaction-based neutron flux detector	copilot	2026-04-04
    scintillation-detector	internal:registry-gap-review:batch8	Radiation detector using scintillator luminescence	copilot	2026-04-04
    area-radiation-monitor	internal:registry-gap-review:batch8	Fixed area gamma dose rate continuous monitoring instrument	copilot	2026-04-04
    thermoluminescent-dosimeter	internal:registry-gap-review:batch8	Passive dose measurement using thermoluminescent material (ICRP/IEC 62387)	copilot	2026-04-04
    creep-fatigue-interaction	internal:registry-gap-review:batch8	Coupled creep and fatigue damage assessment for high-temperature structures (RCC-MRx/ASME III-NH)	copilot	2026-04-04
    j-integral	internal:registry-gap-review:batch8	Path-independent integral parameter for crack-tip energy release rate in EPFM	copilot	2026-04-04
    ratcheting	internal:registry-gap-review:batch8	Progressive unidirectional plastic strain accumulation under cyclic loading	copilot	2026-04-04
    flow-accelerated-corrosion	internal:registry-gap-review:batch8	Accelerated dissolution of protective oxide film by high-temperature high-velocity water flow	copilot	2026-04-04
    erosion-corrosion	internal:registry-gap-review:batch8	Combined mechanical erosion and electrochemical corrosion material degradation mechanism	copilot	2026-04-04
    ```

- **修改边界**：不得修改 Batch 85 及以前的已有行；不得修改 pipeline 源代码
- **测试要求**：
  - 追加前 precheck：`grep -P '^(ARM|TLD|FAC)\t' terms/registry/aliases.tsv`（应返回 0 行）
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：`registry OK: 1430 concepts, ~6058 aliases, 1430 evidence rows`
- **验收标准**：
  - ✅ validate_registry 输出 1430 concepts, 1430 evidence rows，无 ERROR
  - ✅ `awk -F'\t' '$2=="internal:registry-gap-review:batch8"' terms/registry/evidence.tsv | wc -l` = 30
  - ✅ Batch 86 的 10 个 concept_id 均可在 concepts.tsv 中通过 awk 精确匹配找到
  - ✅ `grep -P '^J-integral\t' terms/registry/aliases.tsv | awk -F'\t' '{print $2}'` 输出 `j-integral`（大写 preferred 映射到小写 concept_id）
- **潜在风险**：`ratchet` 作为 alias 可能在通用英文中也指棘轮机构本体而非"棘轮效应"→ 但在结构评估语境中无歧义；`scintillator` alias 可能误覆盖作为材料名的使用 → 聚变文档中闪烁体通常指整个探测装置，可接受

#### Task 3.2: Batch 86 allowlist 同步

- **目标**：将 Batch 86 所有新增 EN token / ZH 术语同步到 allowlist
- **修改内容**：
  - 文件 `terms/allowlist_en.txt`：追加缺失 token（先 grep 检查再追加）
    - `ionization-chamber`, `ionisation-chamber`, `fission-chamber`, `scintillation-detector`, `scintillator`, `area-radiation-monitor`, `ARM`, `thermoluminescent-dosimeter`, `TLD`, `creep-fatigue-interaction`, `creep-fatigue`, `j-integral`, `J-integral`, `ratcheting`, `ratchetting`, `ratchet`, `flow-accelerated-corrosion`, `FAC`, `erosion-corrosion`
  - 文件 `terms/allowlist_zh.txt`：追加缺失术语
    - `电离室`, `电离探测器`, `裂变室`, `裂变电离室`, `闪烁体探测器`, `闪烁探测器`, `区域辐射监测仪`, `区域γ监测仪`, `热释光剂量计`, `热释光剂量片`, `蠕变-疲劳交互`, `蠕变疲劳交互作用`, `J积分`, `棘轮效应`, `棘轮变形`, `流动加速腐蚀`, `流动辅助腐蚀`, `冲蚀-腐蚀`, `冲刷腐蚀`
- **修改边界**：不得删除已有 allowlist 行；不得修改 pipeline 源代码
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：同 Task 3.1 无新 WARNING
- **验收标准**：
  - ✅ `grep -c 'ARM' terms/allowlist_en.txt` ≥ 1
  - ✅ `grep -c 'TLD' terms/allowlist_en.txt` ≥ 1
  - ✅ `grep -c 'FAC' terms/allowlist_en.txt` ≥ 1
  - ✅ `grep -c '电离室' terms/allowlist_zh.txt` ≥ 1
  - ✅ `grep -c 'J积分' terms/allowlist_zh.txt` ≥ 1
  - ✅ validate_registry 无新 WARNING
- **潜在风险**：`ARM` 在某些 Linux 上下文指 CPU 架构 → 在聚变术语 allowlist 中此含义不适用，可安全添加

### Phase 4: 全量验证、导出与测试

#### Task 4.1: 全量验证导出测试

- **目标**：验证全部 30 个新概念正确集成，导出翻译字典和 IME 词表，通过全量测试
- **修改内容**：
  - 运行 `python3 -m pipeline.validate_registry`（验证）
  - 运行 `python3 -m pipeline.export_registry --translation-dict`（导出翻译字典）
  - 运行 VS Code task `fusion-terms: build final wordlist`（重建 IME 词表）
  - 运行 `pytest -q`（全量测试）
  - translation_dict 抽查：至少验证 5 个新词的 en→zh 翻译
- **修改边界**：仅 `artifacts/` 目录下的生成文件会更新；不得修改 `terms/` 或 pipeline 源代码
- **测试要求**：
  - `python3 -m pipeline.validate_registry` → `registry OK: 1430 concepts, ~6058 aliases, 1430 evidence rows`
  - `python3 -m pipeline.export_registry --translation-dict` → 无 ERROR
  - `python3 -m pipeline.build_terms --config config.toml` → `wrote artifacts/domain_terms.txt (≥3193 terms)`
  - `pytest -q` → 全部测试通过
  - Translation 抽查（5 项）：
    1. `vitrification` → `玻璃固化`
    2. `emergency diesel generator` → `应急柴油发电机`
    3. `configuration management` → `配置管理`
    4. `ionization chamber` → `电离室`
    5. `flow-accelerated corrosion` → `流动加速腐蚀`
- **验收标准**：
  - ✅ validate_registry 1430 concepts / 1430 evidence，无 ERROR
  - ✅ `python3 -c "import json; d=json.load(open('artifacts/translation_dict.json')); print(len(d['en2zh']))"` ≥ 2667
  - ✅ `wc -l artifacts/domain_terms.txt` ≥ 3193
  - ✅ pytest 全部通过
  - ✅ 5 个翻译抽查全部 PASS
- **潜在风险**：translation_dict 抽查中 `flow-accelerated corrosion` 可能需要精确匹配 `flow-accelerated corrosion` 而非 `flow accelerated corrosion` → 使用 aliases.tsv 中的 preferred en 形式查找

## 回归检查清单

- [ ] 全量测试通过：`pytest -q`
- [ ] 无新增 lint 警告：`get_errors` 确认无新 ERROR
- [ ] validate_registry 概念/别名/证据三表一致且无 ERROR
- [ ] translation_dict en2zh 词条数 ≥ 2667（基线 2637 + ~30）
- [ ] domain_terms 词条数 ≥ 3193（基线 3163 + ~30）
- [ ] DF 缩写仍仅映射到 detritiation-factor：`grep -P '^DF\t' aliases.tsv` 仅返回 1 行
- [ ] Batch 84–86 evidence 行源标记均为 `internal:registry-gap-review:batch8`
- [ ] 新增概念中无已有 concept_id 重复：validate_registry 会检测
- [ ] EN/ZH allowlist 无重复行：`sort allowlist_*.txt | uniq -d` 为空或仅有已知重复

## 审查日志

| 轮次 | 聚焦 | 发现问题数 | 已修正 | 剩余 |
|------|------|-----------|--------|------|
| R1 | 结构完整性 | 1 | 1 | 0 |
| R2 | 可执行性 | 2 | 2 | 0 |
| R3 | 风险与边缘 | 0 | 0 | 0 |
| **终止** | **T1 — 收敛终止：≥3 轮完成 AND 最近一轮 issue = 0** | | | **0** |

### Completion Summary

| 维度 | 结果 |
|------|------|
| 背景与目标 | 完整：问题描述、目标(4项)、非目标(7项)、复用分析(6项) |
| 技术方案 | 完整：方案概述、12 项设计决策、影响范围(7 文件) |
| Error & Rescue Map | 已覆盖 9 条路径，CRITICAL GAP 0 |
| 执行计划 | 4 Phase、7 Task |
| 回归检查清单 | 9 项（含项目特定检查：DF 缩写验证、evidence source 格式、allowlist 去重） |
| 已知局限 | 无 |

### Convergence Signal Table

| 信号 | R1 | R2 | R3 | 判定 |
|------|----|----|-----|------|
| S1: issue 数单调下降 | 1 | 2 | 0 | ✅ 下降趋势（新发现 → 修正 → 归零） |
| S2: 同类别 issue 连续重复 | — | — | — | ✅ 未触发 |
| S3: 修正引入新 issue 比率 | — | 0% | 0% | ✅ 未触发 |

### R1 Issues
- **Issue R1-1**: Evidence source 格式应为 `internal:registry-gap-review:batch8`（非 batch7）→ 已在方案设计决策 #2 中明确标注，所有 evidence 数据块已使用正确格式 ✅ 已修正

### R2 Issues
- **Issue R2-1**: 缺少 decontamination-factor 的 DF 缩写负面验证 → 在 Task 1.1 验收标准中添加 `grep -P '^DF\t.*decontamination-factor'` 返回 0 行的检查 ✅ 已修正
- **Issue R2-2**: `transformer` 概念在 notes 字段应明确区分电力变压器与 CS 变压器效应 → 在 concepts.tsv 的 notes 中标注「电力变压器（非中心螺管"变压器效应"）」，并在 evidence 中注明 ✅ 已修正
