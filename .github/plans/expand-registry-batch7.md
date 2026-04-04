# 术语注册表扩展 — 批次 7：安全分析方法、辐射防护运行、远程操维装配、仪控系统、结构完整性、功率排出与 PMI

## 背景与目标

- **问题/需求描述**：Gap 分析（对比 ~200 个核聚变高频术语）识别出 166 个缺口，分布于 12 个子领域。注册表（1370 concepts / 5793 aliases / 1370 evidence）在安全分析方法链条、辐射防护操作层面、远程操维/装配、仪控系统、结构完整性与检验、功率排出与等离子体-材料相互作用方面存在系统性缺口。Batch 6 已补充电气功率、安全概念框架、等离子体运行阶段、PBS 辅助系统、水化学、低温、磁体保护和标准质保，但分析方法论（事件树/故障树/严重事故）、操作层面辐防（待积剂量/个人剂量计）、ITER 装配/维护核心词汇、仪控 CODAC 生态、结构评估方法链以及排热/PMI 细化术语仍然缺失。
- **根因分析**：前 80 批次侧重物理概念、材料、设备命名和工程基础设施。**安全分析方法工具**（事件树/故障树/CCF/安全裕度）是安全评价文档的骨架术语但一直未收录；**辐防操作术语**虽有剂量学度量但缺运行工具词；**远程操维/装配**的 ITER 专用词汇（扇区子装配/IVC/MSM/转运容器）整体空白；**仪控领域**已有 DCS/CODAC/MPS 但缺 PLC/HMI/联锁/全厂控制；**结构评估方法**已有材料性能但缺疲劳分析、断裂力学、老化管理完整链条；**等离子体-材料相互作用**已有基础概念但缺 PMI/功率排出/辐射偏滤器/峰值热流。
- **目标**：
  1. 新增 30 个概念（Batch 81–83），覆盖 6 个主题方向
  2. 新增 ~120 行 alias，包含缩写（ET/FT/SA/CCF/SSA/IVC/MSM/PLC/HMI/PCS/PSI/PMI）、连字符变体、中英对、拼写变体
  3. 同步所有新增术语到 EN/ZH allowlist
  4. 通过验证后重新导出 translation_dict、rebuild domain_terms、通过全量测试
- **非目标（不做什么）**：
  - 不修改 pipeline 源代码 — 纯数据追加
  - 不修改已有概念的 preferred_zh / preferred_en — 只新增
  - 不添加废物管理链术语（vitrification/cementation/disposal）— 留待 Batch 8+
  - 不添加消防/暖通/土建术语（fire barrier/ventilation/bioshield）— 留待 Batch 8+
  - 不添加通用机械组件术语（bellows/flange/brazing/pressurizer）— 留待 Batch 8+
  - 不添加数字工程术语（digital-twin/BIM/plant-simulator）— 已有 digital-twin，其余留待后续
- **已有代码/流程复用分析**：
  - `pipeline/validate_registry.py`：复用（验证新增数据）
  - `pipeline/export_registry.py`：复用（`--translation-dict` flag 导出翻译字典）
  - `pipeline/build_terms.py`：复用（重建 IME 词表）
  - 已有别名模式（缩写 `abbr|preferred`、连字符 `en|alias`、中文 `zh|preferred`/`zh|alias`）：复用
  - Batch 6 (78–80) 的执行流程和 commit 模式：复用
  - allowlist EN 使用 token-safe hyphenated 形式（Batch 6 经验）：复用

## 技术方案

- **方案概述**：分 4 个 Phase 按优先级逐步添加。Phase 1–3 各包含一个「三表新增 Task」和一个「allowlist 同步 Task」，Phase 4 做全量验证/导出/测试。
- **关键设计决策**：
  1. **Batch 编号**：接续 Batch 80，使用 81（安全分析+辐防）、82（远程装配+仪控）、83（结构完整性+排热/PMI）
  2. **Evidence source 格式**：使用 `internal:registry-gap-review:batch7` 统一格式（区别于 batch6）
  3. **ET/FT/SA/CCF 缩写**：核安全领域 IAEA 标准缩写，在聚变语境无歧义
  4. **SA (Severe Accident) 与 SSA (Sector Sub-Assembly)**：不同字符串，不冲突；SA 在 Batch 81，SSA 在 Batch 82
  5. **PMI (Plasma-Material Interaction) 缩写**：ITER 标准用法，与 "Project Management Institute" 在聚变语境下无歧义。同时添加 PWI (Plasma-Wall Interaction) 作为 alias
  6. **PSI (Pre-Service Inspection) 缩写**：ASME Section XI 标准用法；precheck 确认 aliases.tsv 中无已有 PSI → 执行时验证
  7. **PCS (Plant Control System) 缩写**：ITER 标准用法；precheck 确认无已有 PCS → 执行时验证
  8. **aging vs ageing 拼写**：concept_id 使用 `aging-management`（美式，与注册表已有惯例一致），添加 `ageing management` 作为 British 拼写 alias
  9. **committed-dose 概念范围**：通用概念，同时覆盖 committed effective dose 和 committed equivalent dose；添加 `committed effective dose` 作为 alias
  10. **AMP 缩写不设**：aging-management 概念名为方法而非具体计划（aging management programme），不设 AMP 缩写以避免混淆
  11. **无缩写术语**：cliff-edge-effect, off-normal-event, safety-margin, committed-dose, personal-dosimeter, occupational-radiation-exposure, tokamak-assembly, ex-vessel-component, transfer-cask, fatigue-analysis, fracture-mechanics, aging-management, seismic-qualification, structural-integrity, power-exhaust, peak-heat-flux, radiative-divertor 无需设 preferred_abbr
  12. **transfer-cask 变体**：添加 `transfer flask` 作为 alias（英国/欧洲核工业用法）
- **影响范围**：
  - `terms/registry/concepts.tsv` — 新增 30 行 + 3 行 batch 注释
  - `terms/registry/aliases.tsv` — 新增 ~120 行
  - `terms/registry/evidence.tsv` — 新增 30 行
  - `terms/allowlist_en.txt` — 追加缺失 EN token
  - `terms/allowlist_zh.txt` — 追加缺失 ZH 术语
  - `artifacts/translation_dict.json` — 重新生成
  - `artifacts/domain_terms.txt` — 重新生成

## Error & Rescue Map（关键失败路径映射）

| 代码路径/操作 | 可能的失败 | 错误类型 | 已处理？ | 处理方式 | 用户可见行为 |
|---|---|---|---|---|---|
| 新增 SA 缩写 | 与已有缩写冲突 | validation error | Y | SA 在 aliases.tsv 中 precheck `grep -P '^SA\t'`，确认无冲突 | validate_registry 报错并阻断 |
| 新增 SSA 缩写 | 与 SA 混淆（视觉近似） | 语义注意 | Y | SA ≠ SSA 为不同字符串，聚变领域 SSA = Sector Sub-Assembly 无歧义 | 不可见 |
| 新增 PSI 缩写 | PSI 可指压力单位 | 语义冲突 | Y | PSI 在核安全/ASME 上下文 = Pre-Service Inspection，注册表为聚变术语；precheck aliases.tsv | 不可见 |
| 新增 PCS 缩写 | PCS 可指其他含义 | 语义冲突 | Y | PCS = Plant Control System 是 ITER 标准；precheck aliases.tsv 确认无冲突 | 不可见 |
| 新增 PMI 缩写 | PMI = Project Management Institute | 语义冲突 | Y | 聚变语境 PMI = Plasma-Material Interaction 是 ITER 标准用法；notes 字段标注 | 不可见 |
| aging vs ageing 拼写 | 搜索遗漏一种拼写 | 覆盖遗漏 | Y | 同时添加 American `aging` 和 British `ageing` alias | 不影响 |
| committed-dose 语义过宽 | 与已有 effective-dose 交叉 | 语义重叠 | Y | committed-dose 是独立概念（时间积分剂量），与 effective-dose（加权方式）正交 | 不影响 |
| plasma-material-interaction vs plasma-wall-interaction | 两个常用术语 | 命名选择 | Y | PMI 作为 concept_id，PWI 作为 alias；概念等价 | 不影响 |
| allowlist 同步遗漏 | build_terms 词条数未增长 | 逻辑遗漏 | Y | 每 Phase 同步 allowlist 并运行 validate_registry | build_stats 可检测 |
| translation_dict 未重新生成 | 遗忘 `--translation-dict` flag | 操作遗漏 | Y | Task 4.1 明确标注该 flag | 翻译字典不含新词条 |

## 时序推演

| 阶段 | 关键决策/潜在阻塞 |
|------|-------------------|
| 初期（Task 1.1–1.2） | Batch 81 含 ET/FT/SA/CCF 四个缩写，需在追加前 precheck aliases.tsv 确认无冲突；cliff-edge-effect / off-normal-event 无缩写，低风险 |
| 中期（Task 2.1–2.2） | Batch 82 引入 SSA/IVC/MSM/PLC/HMI/PCS 六个缩写，PLC/HMI 是通用 I&C 缩写，需确认与其他领域 alias 不冲突；plant-control-system 概念需确认与已有 codac 的层级区分（PCS 是功能描述，CODAC 是 ITER 特有实现） |
| 后期（Task 3.1–4.1） | Batch 83 含 PSI/PMI 缩写和 British 拼写变体 ageing；PSI 需 precheck 确认；全量导出若 translation_dict 新增数大幅偏离预期（~30 个新映射），需排查是否遗漏 alias |

## 执行计划

### Phase 1: Batch 81 — 安全分析方法 + 辐射防护运行层面 (10 terms)

#### ✅ Task 1.1: Batch 81 三表追加（10 概念 + ~40 alias + 10 evidence）

- **目标**：在三张注册表表末尾追加 Batch 81 全部数据
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：追加 batch 注释行 + 10 行概念数据

    ```tsv
    # ==== Batch 81: safety analysis methods + radiation protection operations ====
    event-tree	method	事件树	Event Tree	ET	active	概率安全评价核心工具 (IAEA)
    fault-tree	method	故障树	Fault Tree	FT	active	系统可靠性分析核心工具 (IAEA)
    severe-accident	concept	严重事故	Severe Accident	SA	active	超出设计基准的低概率高后果事故
    common-cause-failure	concept	共因失效	Common Cause Failure	CCF	active	同一原因导致多重冗余失效 (PSA 关键输入)
    cliff-edge-effect	concept	断崖效应	Cliff Edge Effect		active	参数小幅变化导致后果骤变 (后福岛评审术语)
    off-normal-event	concept	非正常事件	Off-Normal Event		active	偏离正常运行的事件统称 (ITER 分类)
    safety-margin	concept	安全裕度	Safety Margin		active	设计值与安全限值之间的余量
    committed-dose	metric	待积剂量	Committed Dose		active	摄入放射性核素后的时间积分剂量
    personal-dosimeter	device	个人剂量计	Personal Dosimeter		active	辐射工作人员随身佩戴的剂量监测仪器
    occupational-radiation-exposure	concept	职业辐射照射	Occupational Radiation Exposure		active	工作过程中受到的辐射照射
    ```

  - 文件 `terms/registry/aliases.tsv`：追加 ~40 行别名数据

    ```tsv
    # ---- Batch 81 aliases ----
    event tree	event-tree	en	preferred	preferred en
    事件树	event-tree	zh	preferred	preferred zh
    ET	event-tree	abbr	preferred	canonical abbr
    event-tree	event-tree	en	alias	hyphenated form
    event tree analysis	event-tree	en	alias	extended form (ETA)
    事件树分析	event-tree	zh	alias	extended zh
    fault tree	fault-tree	en	preferred	preferred en
    故障树	fault-tree	zh	preferred	preferred zh
    FT	fault-tree	abbr	preferred	canonical abbr
    fault-tree	fault-tree	en	alias	hyphenated form
    fault tree analysis	fault-tree	en	alias	extended form (FTA)
    故障树分析	fault-tree	zh	alias	extended zh
    severe accident	severe-accident	en	preferred	preferred en
    严重事故	severe-accident	zh	preferred	preferred zh
    SA	severe-accident	abbr	preferred	canonical abbr
    severe-accident	severe-accident	en	alias	hyphenated form
    common cause failure	common-cause-failure	en	preferred	preferred en
    共因失效	common-cause-failure	zh	preferred	preferred zh
    CCF	common-cause-failure	abbr	preferred	canonical abbr
    common-cause-failure	common-cause-failure	en	alias	hyphenated form
    共模故障	common-cause-failure	zh	alias	variant zh
    cliff edge effect	cliff-edge-effect	en	preferred	preferred en
    断崖效应	cliff-edge-effect	zh	preferred	preferred zh
    cliff-edge-effect	cliff-edge-effect	en	alias	hyphenated form
    off-normal event	off-normal-event	en	preferred	preferred en
    非正常事件	off-normal-event	zh	preferred	preferred zh
    off-normal-event	off-normal-event	en	alias	hyphenated form
    异常事件	off-normal-event	zh	alias	variant zh
    safety margin	safety-margin	en	preferred	preferred en
    安全裕度	safety-margin	zh	preferred	preferred zh
    safety-margin	safety-margin	en	alias	hyphenated form
    committed dose	committed-dose	en	preferred	preferred en
    待积剂量	committed-dose	zh	preferred	preferred zh
    committed-dose	committed-dose	en	alias	hyphenated form
    committed effective dose	committed-dose	en	alias	specific subtype (CED)
    待积有效剂量	committed-dose	zh	alias	CED zh
    personal dosimeter	personal-dosimeter	en	preferred	preferred en
    个人剂量计	personal-dosimeter	zh	preferred	preferred zh
    personal-dosimeter	personal-dosimeter	en	alias	hyphenated form
    occupational radiation exposure	occupational-radiation-exposure	en	preferred	preferred en
    职业辐射照射	occupational-radiation-exposure	zh	preferred	preferred zh
    occupational-radiation-exposure	occupational-radiation-exposure	en	alias	hyphenated form
    职业照射	occupational-radiation-exposure	zh	alias	short zh
    ```

  - 文件 `terms/registry/evidence.tsv`：追加 10 行证据数据

    ```tsv
    event-tree	internal:registry-gap-review:batch7	Core tool of probabilistic safety assessment (IAEA SSG-3)	copilot	2026-04-04
    fault-tree	internal:registry-gap-review:batch7	System reliability analysis tool for PSA (IAEA SSG-3)	copilot	2026-04-04
    severe-accident	internal:registry-gap-review:batch7	Beyond-design-basis low-probability high-consequence accident	copilot	2026-04-04
    common-cause-failure	internal:registry-gap-review:batch7	Multiple redundant system failures from single root cause	copilot	2026-04-04
    cliff-edge-effect	internal:registry-gap-review:batch7	Post-Fukushima safety assessment term for abrupt consequence escalation	copilot	2026-04-04
    off-normal-event	internal:registry-gap-review:batch7	ITER event classification for deviations from normal operation	copilot	2026-04-04
    safety-margin	internal:registry-gap-review:batch7	Margin between design value and safety limit	copilot	2026-04-04
    committed-dose	internal:registry-gap-review:batch7	Time-integrated dose from intake of radioactive material (ICRP)	copilot	2026-04-04
    personal-dosimeter	internal:registry-gap-review:batch7	Wearable radiation dose monitoring device for workers	copilot	2026-04-04
    occupational-radiation-exposure	internal:registry-gap-review:batch7	Radiation exposure received during work activities (ICRP/IAEA)	copilot	2026-04-04
    ```

- **修改边界**：不得修改 `terms/registry/concepts.tsv` 中 Batch 80 及以前的任何行；不得修改 `terms/registry/aliases.tsv` 中已有别名行；不得修改 `terms/registry/evidence.tsv` 中已有证据行；不得修改 pipeline 源代码
- **测试要求**：
  - 追加前 precheck：`grep -P '^ET\t|^FT\t|^SA\t|^CCF\t' terms/registry/aliases.tsv`（应返回 0 行或已存在的其他映射）
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：`registry OK: 1380 concepts, 58xx aliases, 1380 evidence rows`
- **验收标准**：
  - ✅ validate_registry 输出 1380 concepts, 1380 evidence rows，无 ERROR
  - ✅ `awk -F'\t' '$2=="internal:registry-gap-review:batch7"' terms/registry/evidence.tsv | wc -l` = 10
  - ✅ 10 个新 concept_id 均可在 concepts.tsv 中通过 `awk -F'\t'` 精确匹配找到
- **潜在风险**：SA 缩写若已被其他概念占用（如 Sensitivity Analysis），precheck 会发现；若冲突则改用 full form 或 `sev-acc` 缩写

#### ✅ Task 1.2: Batch 81 allowlist 同步

- **目标**：将 Batch 81 所有新增 EN token / ZH 术语同步到 allowlist（如尚未存在）
- **修改内容**：
  - 文件 `terms/allowlist_en.txt`：追加以下缺失 token（先 grep 检查再追加；EN 使用 token-safe hyphenated 形式）
    - `event-tree`, `ET`, `event-tree-analysis`, `fault-tree`, `FT`, `fault-tree-analysis`, `severe-accident`, `SA`, `common-cause-failure`, `CCF`, `cliff-edge-effect`, `off-normal-event`, `safety-margin`, `committed-dose`, `committed-effective-dose`, `personal-dosimeter`, `occupational-radiation-exposure`
  - 文件 `terms/allowlist_zh.txt`：追加以下缺失术语
    - `事件树`, `事件树分析`, `故障树`, `故障树分析`, `严重事故`, `共因失效`, `共模故障`, `断崖效应`, `非正常事件`, `异常事件`, `安全裕度`, `待积剂量`, `待积有效剂量`, `个人剂量计`, `职业辐射照射`, `职业照射`
- **修改边界**：不得删除已有 allowlist 行；不得修改 pipeline 源代码
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：同 Task 1.1 但无 allowlist 相关 WARNING
- **验收标准**：
  - ✅ `grep -c 'ET' terms/allowlist_en.txt` ≥ 1
  - ✅ `grep -c 'CCF' terms/allowlist_en.txt` ≥ 1
  - ✅ `grep -c '事件树' terms/allowlist_zh.txt` ≥ 1
  - ✅ validate_registry 无新 WARNING
- **潜在风险**：`ET` 为 2-char token，确认 allowlist 无最小长度限制（已有 SF/MG 等 2-char 先例）

### Phase 2: Batch 82 — 远程操维装配 + 仪控系统 (10 terms)

#### ✅ Task 2.1: Batch 82 三表追加（10 概念 + ~42 alias + 10 evidence）

- **目标**：在三张注册表表末尾追加 Batch 82 全部数据
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：追加 batch 注释行 + 10 行概念数据

    ```tsv
    # ==== Batch 82: remote handling & assembly + instrumentation & control ====
    tokamak-assembly	concept	托卡马克装配	Tokamak Assembly		active	ITER 主机装配工程统称
    sector-sub-assembly	concept	扇区子装配	Sector Sub-Assembly	SSA	active	真空室扇区与热屏蔽/面向等离子体部件的预组装
    in-vessel-component	concept	真空室内部件	In-Vessel Component	IVC	active	真空室内所有可更换/不可更换部件统称
    ex-vessel-component	concept	真空室外部件	Ex-Vessel Component		active	真空室外但生物屏蔽内的部件统称
    master-slave-manipulator	device	主从机械手	Master-Slave Manipulator	MSM	active	热室/远程维护用力反馈操作器
    transfer-cask	device	转运容器	Transfer Cask		active	活化部件在厂房间转运的屏蔽容器
    interlock-system	system	联锁系统	Interlock System		active	防止误操作的硬件/软件保护逻辑
    programmable-logic-controller	device	可编程逻辑控制器	Programmable Logic Controller	PLC	active	工业控制基础硬件单元
    human-machine-interface	device	人机界面	Human-Machine Interface	HMI	active	操作员与控制系统交互终端
    plant-control-system	system	全厂控制系统	Plant Control System	PCS	active	ITER CODAC 架构下的全厂级控制系统
    ```

  - 文件 `terms/registry/aliases.tsv`：追加 ~42 行别名数据

    ```tsv
    # ---- Batch 82 aliases ----
    tokamak assembly	tokamak-assembly	en	preferred	preferred en
    托卡马克装配	tokamak-assembly	zh	preferred	preferred zh
    tokamak-assembly	tokamak-assembly	en	alias	hyphenated form
    sector sub-assembly	sector-sub-assembly	en	preferred	preferred en
    扇区子装配	sector-sub-assembly	zh	preferred	preferred zh
    SSA	sector-sub-assembly	abbr	preferred	canonical abbr
    sector-sub-assembly	sector-sub-assembly	en	alias	hyphenated form
    扇区子组件	sector-sub-assembly	zh	alias	variant zh
    in-vessel component	in-vessel-component	en	preferred	preferred en
    真空室内部件	in-vessel-component	zh	preferred	preferred zh
    IVC	in-vessel-component	abbr	preferred	canonical abbr
    in-vessel-component	in-vessel-component	en	alias	hyphenated form
    堆内构件	in-vessel-component	zh	alias	variant zh (fission-style)
    ex-vessel component	ex-vessel-component	en	preferred	preferred en
    真空室外部件	ex-vessel-component	zh	preferred	preferred zh
    ex-vessel-component	ex-vessel-component	en	alias	hyphenated form
    master-slave manipulator	master-slave-manipulator	en	preferred	preferred en
    主从机械手	master-slave-manipulator	zh	preferred	preferred zh
    MSM	master-slave-manipulator	abbr	preferred	canonical abbr
    master-slave-manipulator	master-slave-manipulator	en	alias	hyphenated form
    transfer cask	transfer-cask	en	preferred	preferred en
    转运容器	transfer-cask	zh	preferred	preferred zh
    transfer-cask	transfer-cask	en	alias	hyphenated form
    transfer flask	transfer-cask	en	alias	UK/EU variant
    转运屏蔽容器	transfer-cask	zh	alias	variant zh (explicit shielding)
    interlock system	interlock-system	en	preferred	preferred en
    联锁系统	interlock-system	zh	preferred	preferred zh
    interlock-system	interlock-system	en	alias	hyphenated form
    interlock	interlock-system	en	alias	short form
    联锁	interlock-system	zh	alias	short zh
    programmable logic controller	programmable-logic-controller	en	preferred	preferred en
    可编程逻辑控制器	programmable-logic-controller	zh	preferred	preferred zh
    PLC	programmable-logic-controller	abbr	preferred	canonical abbr
    programmable-logic-controller	programmable-logic-controller	en	alias	hyphenated form
    human-machine interface	human-machine-interface	en	preferred	preferred en
    人机界面	human-machine-interface	zh	preferred	preferred zh
    HMI	human-machine-interface	abbr	preferred	canonical abbr
    human-machine-interface	human-machine-interface	en	alias	hyphenated form
    人机接口	human-machine-interface	zh	alias	variant zh
    plant control system	plant-control-system	en	preferred	preferred en
    全厂控制系统	plant-control-system	zh	preferred	preferred zh
    PCS	plant-control-system	abbr	preferred	canonical abbr
    plant-control-system	plant-control-system	en	alias	hyphenated form
    ```

  - 文件 `terms/registry/evidence.tsv`：追加 10 行

    ```tsv
    tokamak-assembly	internal:registry-gap-review:batch7	ITER tokamak machine assembly engineering	copilot	2026-04-04
    sector-sub-assembly	internal:registry-gap-review:batch7	Pre-assembly of VV sector with thermal shield and PFCs	copilot	2026-04-04
    in-vessel-component	internal:registry-gap-review:batch7	Collective term for all components inside the vacuum vessel	copilot	2026-04-04
    ex-vessel-component	internal:registry-gap-review:batch7	Components outside VV but inside bioshield	copilot	2026-04-04
    master-slave-manipulator	internal:registry-gap-review:batch7	Force-feedback manipulator for hot cell and remote maintenance	copilot	2026-04-04
    transfer-cask	internal:registry-gap-review:batch7	Shielded container for inter-building transfer of activated components	copilot	2026-04-04
    interlock-system	internal:registry-gap-review:batch7	Hardware/software protection logic preventing operator error	copilot	2026-04-04
    programmable-logic-controller	internal:registry-gap-review:batch7	Basic industrial control hardware unit	copilot	2026-04-04
    human-machine-interface	internal:registry-gap-review:batch7	Operator interaction terminal for control systems	copilot	2026-04-04
    plant-control-system	internal:registry-gap-review:batch7	Plant-wide control system under ITER CODAC architecture	copilot	2026-04-04
    ```

- **修改边界**：不得修改 Batch 81 及以前的任何行；不得修改 pipeline 源代码
- **测试要求**：
  - 追加前 precheck：`grep -P '^SSA\t|^IVC\t|^MSM\t|^PLC\t|^HMI\t|^PCS\t' terms/registry/aliases.tsv`（应返回 0 行）
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：`registry OK: 1390 concepts, 58xx aliases, 1390 evidence rows`
- **验收标准**：
  - ✅ validate_registry 输出 1390 concepts, 1390 evidence rows，无 ERROR
  - ✅ `awk -F'\t' '$2=="internal:registry-gap-review:batch7"' terms/registry/evidence.tsv | wc -l` = 20
  - ✅ Batch 82 的 10 个 concept_id 均可在 concepts.tsv 中通过 awk 精确匹配找到
- **潜在风险**：PCS 缩写若与已有 aliases 冲突（如 poloidal current strap 等） → precheck 发现后可改用 `plant-control` 无缩写

#### Task 2.2: Batch 82 allowlist 同步

- **目标**：将 Batch 82 所有新增 EN token / ZH 术语同步到 allowlist
- **修改内容**：
  - 文件 `terms/allowlist_en.txt`：追加缺失 token（先 grep 检查再追加；EN 使用 token-safe hyphenated 形式）
    - `tokamak-assembly`, `sector-sub-assembly`, `SSA`, `in-vessel-component`, `IVC`, `ex-vessel-component`, `master-slave-manipulator`, `MSM`, `transfer-cask`, `transfer-flask`, `interlock-system`, `interlock`, `programmable-logic-controller`, `PLC`, `human-machine-interface`, `HMI`, `plant-control-system`, `PCS`
  - 文件 `terms/allowlist_zh.txt`：追加缺失术语
    - `托卡马克装配`, `扇区子装配`, `扇区子组件`, `真空室内部件`, `堆内构件`, `真空室外部件`, `主从机械手`, `转运容器`, `转运屏蔽容器`, `联锁系统`, `联锁`, `可编程逻辑控制器`, `人机界面`, `人机接口`, `全厂控制系统`
- **修改边界**：不得删除已有 allowlist 行；不得修改 pipeline 源代码
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：同 Task 2.1 无新 WARNING
- **验收标准**：
  - ✅ `grep -c 'PLC' terms/allowlist_en.txt` ≥ 1
  - ✅ `grep -c 'SSA' terms/allowlist_en.txt` ≥ 1
  - ✅ `grep -c '联锁系统' terms/allowlist_zh.txt` ≥ 1
  - ✅ validate_registry 无新 WARNING
- **潜在风险**：`interlock` 作为单词已可能在某些 EN alias 中存在 → 先 grep 再追加

### Phase 3: Batch 83 — 结构完整性评估 + 功率排出与 PMI (10 terms)

#### Task 3.1: Batch 83 三表追加（10 概念 + ~38 alias + 10 evidence）

- **目标**：在三张注册表表末尾追加 Batch 83 全部数据
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：追加 batch 注释行 + 10 行概念数据

    ```tsv
    # ==== Batch 83: structural integrity assessment + power exhaust & PMI ====
    fatigue-analysis	method	疲劳分析	Fatigue Analysis		active	结构部件疲劳寿命评估
    fracture-mechanics	method	断裂力学	Fracture Mechanics		active	含裂纹结构安全性分析方法
    aging-management	method	老化管理	Aging Management		active	长寿命核设施结构/设备老化监控与维护策略
    seismic-qualification	method	抗震鉴定	Seismic Qualification		active	设备/结构在地震载荷下功能完好性验证
    pre-service-inspection	method	役前检查	Pre-Service Inspection	PSI	active	运行前建立结构基线的无损检测 (ASME XI)
    structural-integrity	concept	结构完整性	Structural Integrity		active	结构在所有工况下保持安全功能的能力
    power-exhaust	concept	功率排出	Power Exhaust		active	将等离子体热功率安全导出至偏滤器/壁的过程
    peak-heat-flux	metric	峰值热流密度	Peak Heat Flux		active	面向等离子体部件表面承受的最大热流
    radiative-divertor	concept	辐射偏滤器	Radiative Divertor		active	通过杂质辐射降低偏滤器靶板热载荷的运行模式
    plasma-material-interaction	concept	等离子体-材料相互作用	Plasma-Material Interaction	PMI	active	等离子体与面向等离子体材料表面的物理/化学相互作用
    ```

  - 文件 `terms/registry/aliases.tsv`：追加 ~38 行别名数据

    ```tsv
    # ---- Batch 83 aliases ----
    fatigue analysis	fatigue-analysis	en	preferred	preferred en
    疲劳分析	fatigue-analysis	zh	preferred	preferred zh
    fatigue-analysis	fatigue-analysis	en	alias	hyphenated form
    fracture mechanics	fracture-mechanics	en	preferred	preferred en
    断裂力学	fracture-mechanics	zh	preferred	preferred zh
    fracture-mechanics	fracture-mechanics	en	alias	hyphenated form
    破裂力学	fracture-mechanics	zh	alias	variant zh
    aging management	aging-management	en	preferred	preferred en
    老化管理	aging-management	zh	preferred	preferred zh
    aging-management	aging-management	en	alias	hyphenated form
    ageing management	aging-management	en	alias	British spelling
    seismic qualification	seismic-qualification	en	preferred	preferred en
    抗震鉴定	seismic-qualification	zh	preferred	preferred zh
    seismic-qualification	seismic-qualification	en	alias	hyphenated form
    pre-service inspection	pre-service-inspection	en	preferred	preferred en
    役前检查	pre-service-inspection	zh	preferred	preferred zh
    PSI	pre-service-inspection	abbr	preferred	canonical abbr (ASME XI)
    pre-service-inspection	pre-service-inspection	en	alias	hyphenated form
    structural integrity	structural-integrity	en	preferred	preferred en
    结构完整性	structural-integrity	zh	preferred	preferred zh
    structural-integrity	structural-integrity	en	alias	hyphenated form
    power exhaust	power-exhaust	en	preferred	preferred en
    功率排出	power-exhaust	zh	preferred	preferred zh
    power-exhaust	power-exhaust	en	alias	hyphenated form
    功率排除	power-exhaust	zh	alias	variant zh
    peak heat flux	peak-heat-flux	en	preferred	preferred en
    峰值热流密度	peak-heat-flux	zh	preferred	preferred zh
    peak-heat-flux	peak-heat-flux	en	alias	hyphenated form
    峰值热流	peak-heat-flux	zh	alias	short zh
    radiative divertor	radiative-divertor	en	preferred	preferred en
    辐射偏滤器	radiative-divertor	zh	preferred	preferred zh
    radiative-divertor	radiative-divertor	en	alias	hyphenated form
    辐射型偏滤器	radiative-divertor	zh	alias	variant zh
    plasma-material interaction	plasma-material-interaction	en	preferred	preferred en
    等离子体-材料相互作用	plasma-material-interaction	zh	preferred	preferred zh
    PMI	plasma-material-interaction	abbr	preferred	canonical abbr
    plasma-material-interaction	plasma-material-interaction	en	alias	hyphenated form
    plasma-wall interaction	plasma-material-interaction	en	alias	PWI synonym
    等离子体-壁相互作用	plasma-material-interaction	zh	alias	PWI zh
    ```

  - 文件 `terms/registry/evidence.tsv`：追加 10 行

    ```tsv
    fatigue-analysis	internal:registry-gap-review:batch7	Fatigue life assessment of structural components (RCC-MR/SDC-IC)	copilot	2026-04-04
    fracture-mechanics	internal:registry-gap-review:batch7	Safety analysis of cracked structures under nuclear loading	copilot	2026-04-04
    aging-management	internal:registry-gap-review:batch7	Long-life nuclear facility structural/equipment aging strategy (IAEA NS-G-2.12)	copilot	2026-04-04
    seismic-qualification	internal:registry-gap-review:batch7	Equipment/structure functional integrity verification under seismic loads	copilot	2026-04-04
    pre-service-inspection	internal:registry-gap-review:batch7	Baseline NDE before operation per ASME Section XI	copilot	2026-04-04
    structural-integrity	internal:registry-gap-review:batch7	Ability of structures to maintain safety function under all conditions	copilot	2026-04-04
    power-exhaust	internal:registry-gap-review:batch7	Safe removal of plasma thermal power to divertor/wall	copilot	2026-04-04
    peak-heat-flux	internal:registry-gap-review:batch7	Maximum heat flux on plasma-facing component surfaces	copilot	2026-04-04
    radiative-divertor	internal:registry-gap-review:batch7	Operating regime using impurity radiation to reduce target plate heat load	copilot	2026-04-04
    plasma-material-interaction	internal:registry-gap-review:batch7	Physical/chemical interaction between plasma and PFC surfaces	copilot	2026-04-04
    ```

- **修改边界**：不得修改 Batch 82 及以前的任何行；不得修改 pipeline 源代码
- **测试要求**：
  - 追加前 precheck：`grep -P '^PSI\t|^PMI\t' terms/registry/aliases.tsv`（应返回 0 行）
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：`registry OK: 1400 concepts, 59xx aliases, 1400 evidence rows`
- **验收标准**：
  - ✅ validate_registry 输出 1400 concepts, 1400 evidence rows，无 ERROR
  - ✅ `awk -F'\t' '$2=="internal:registry-gap-review:batch7"' terms/registry/evidence.tsv | wc -l` = 30
  - ✅ Batch 83 的 10 个 concept_id 均可在 concepts.tsv 中通过 awk 精确匹配找到
- **潜在风险**：PSI 若已存在为其他概念的 alias → precheck 发现后可移除 PSI 缩写（pre-service-inspection 全称仍可识别）

#### Task 3.2: Batch 83 allowlist 同步

- **目标**：将 Batch 83 所有新增 EN token / ZH 术语同步到 allowlist
- **修改内容**：
  - 文件 `terms/allowlist_en.txt`：追加缺失 token（先 grep 检查再追加；EN 使用 token-safe hyphenated 形式）
    - `fatigue-analysis`, `fracture-mechanics`, `aging-management`, `ageing-management`, `seismic-qualification`, `pre-service-inspection`, `PSI`, `structural-integrity`, `power-exhaust`, `peak-heat-flux`, `radiative-divertor`, `plasma-material-interaction`, `PMI`, `plasma-wall-interaction`
  - 文件 `terms/allowlist_zh.txt`：追加缺失术语
    - `疲劳分析`, `断裂力学`, `破裂力学`, `老化管理`, `抗震鉴定`, `役前检查`, `结构完整性`, `功率排出`, `功率排除`, `峰值热流密度`, `峰值热流`, `辐射偏滤器`, `辐射型偏滤器`, `等离子体-材料相互作用`, `等离子体-壁相互作用`
- **修改边界**：不得删除已有 allowlist 行；不得修改 pipeline 源代码
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：同 Task 3.1 无新 WARNING
- **验收标准**：
  - ✅ `grep -c 'PMI' terms/allowlist_en.txt` ≥ 1
  - ✅ `grep -c 'PSI' terms/allowlist_en.txt` ≥ 1
  - ✅ `grep -c '疲劳分析' terms/allowlist_zh.txt` ≥ 1
  - ✅ validate_registry 无新 WARNING
- **潜在风险**：`plasma-wall-interaction` 可能与已有 `plasma-wall interaction` 概念在 allowlist 中部分重复 → 先 grep 再追加

### Phase 4: 全量验证、导出与测试

#### Task 4.1: 全量验证导出测试

- **目标**：全量通过 validate → export → build → pytest，确保数据完整性和管线兼容性
- **修改内容**：
  - 文件 `artifacts/translation_dict.json`：重新生成（由 export_registry 产生）
  - 文件 `artifacts/domain_terms.txt`：重新生成（由 build_terms 产生）
  - 文件 `artifacts/domain_terms_build_stats.json`：重新生成
- **修改边界**：不得修改 `terms/` 目录下的任何文件；不得修改 pipeline 源代码；仅 `artifacts/` 被管线工具重新生成
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：`registry OK: 1400 concepts, 59xx+ aliases, 1400 evidence rows`
  - 运行 `python3 -m pipeline.export_registry --translation-dict`
  - 预期输出：`exported registry artifacts to artifacts` + `wrote artifacts/registry_exports.json`
  - 运行 `python3 -m pipeline.build_terms --config config.toml`
  - 预期输出：`wrote artifacts/domain_terms.txt (≥3111 terms)`（30 新概念 → 预计 3081+30=~3111+）
  - 运行 `pytest -q`
  - 预期输出：全部通过
  - 运行翻译抽查（≥5 个新术语的 EN→ZH 映射验证）：
    ```python
    import json, pathlib
    d = json.loads(pathlib.Path("artifacts/translation_dict.json").read_text())
    checks = {
        "event tree": "事件树",
        "severe accident": "严重事故",
        "in-vessel component": "真空室内部件",
        "PLC": "可编程逻辑控制器",
        "plasma-material interaction": "等离子体-材料相互作用",
    }
    en2zh = {}
    for bucket in ("en2zh", "en2zh_phrase", "en2zh_short"):
        en2zh.update(d.get(bucket, {}))
    for en, zh in checks.items():
        actual = en2zh.get(en, "MISSING")
        status = "PASS" if actual == zh else f"FAIL (got {actual})"
        print(f"  {en} → {status}")
    ```
- **验收标准**：
  - ✅ validate_registry 报告 1400 concepts, 1400 evidence rows，零 ERROR
  - ✅ export_registry 成功，translation_dict.json en2zh 总条目数（en2zh + en2zh_short）≥ 2640（基线 2610 + ~30）
  - ✅ build_terms 输出 domain_terms.txt 行数 ≥ 3111（基线 3081 + 30）
  - ✅ pytest -q 全部通过
  - ✅ 5 个翻译抽查全部 PASS
- **潜在风险**：export_registry 对 2-char abbr (ET/FT/SA) 的分桶逻辑可能将其放入 en2zh_short 而非 en2zh → 抽查脚本已合并所有桶查询

## 回归检查清单

- [ ] 全量测试通过：`pytest -q`
- [ ] 无新增 lint 警告：pre-commit hooks (ruff) 在 commit 时自动运行
- [ ] validate_registry 报告零 ERROR 零新 WARNING
- [ ] translation_dict.json en2zh 总条目数 ≥ 2640
- [ ] domain_terms.txt 行数 ≥ 3111
- [ ] 新增 30 个 concept_id 在 evidence.tsv 中均有 batch7 来源行
- [ ] allowlist_en.txt 包含所有新增缩写（ET/FT/SA/CCF/SSA/IVC/MSM/PLC/HMI/PCS/PSI/PMI）
- [ ] allowlist_zh.txt 包含所有新增中文术语（30 个 preferred_zh + variant）

## 审查日志

| 轮次 | 聚焦 | 发现问题数 | 已修正 | 剩余 |
|------|------|-----------|--------|------|
| R1 | 结构完整性 | 2 | 2 | 0 |
| R2 | 可执行性 | 2 | 2 | 0 |
| R3 | 风险与边缘 | 2 | 2 | 0 |
| **终止** | **T1 — 收敛终止** | | | **0** |

### Completion Summary

| 维度 | 结果 |
|------|------|
| 背景与目标 | 完整：问题描述、根因分析、目标（4 条）、非目标（6 条）、复用分析（6 项）均填写 |
| 技术方案 | 完整：方案概述、12 项设计决策、影响范围（7 个文件） |
| Error & Rescue Map | 10 条失败路径，0 CRITICAL GAP |
| 执行计划 | 4 Phase、7 Task |
| 回归检查清单 | 8 项项目特定检查 |
| 已知局限 | 无 |

### R1 Issues
- **Issue R1-1**: AMP (Aging Management Programme) 缩写决策未在设计决策中记录 → 已在设计决策 #10 中明确说明不设 AMP 的理由 ✅ 已修正
- **Issue R1-2**: Error & Rescue Map 缺少 PSI/PCS 缩写冲突条目 → 已补充 PSI 和 PCS 两行 ✅ 已修正

### R2 Issues
- **Issue R2-1**: Task 2.1 中 plant-control-system 与已有 codac 的关系需在潜在风险中说明 → 已在时序推演「中期」段落补充层级区分说明（PCS 是功能描述，CODAC 是 ITER 特有实现） ✅ 已修正
- **Issue R2-2**: Task 4.1 翻译抽查脚本的 bucket 合并逻辑需同时覆盖 en2zh_phrase → 已在脚本中合并 en2zh + en2zh_phrase + en2zh_short 三桶 ✅ 已修正

### R3 Issues
- **Issue R3-1**: PMI 缩写可能已被其他概念占用 → 已在 Task 3.1 测试要求中加入 `grep -P '^PMI\t'` precheck ✅ 已修正
- **Issue R3-2**: transfer-cask 缺少 UK/EU 变体 `transfer flask` → 已在 aliases 和 allowlist 中补充 ✅ 已修正
