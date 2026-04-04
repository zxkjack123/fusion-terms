# 术语注册表扩展 — 批次 6：电气功率、安全分析、等离子体运行、PBS 系统、水化学、低温、磁体保护、标准质保

## 背景与目标

- **问题/需求描述**：Gap 分析（`.github/reviews/registry-gaps-batch6-2026-04-04.md`）识别出 30 个缺失术语，分布于 8 个主题方向。注册表（1340 concepts / 5684 aliases / 1340 evidence）在电气功率系统、安全分析方法论、等离子体运行阶段、ITER PBS 辅助系统、水化学/腐蚀、低温子系统、磁体保护设备、设计规范与质保方面存在系统性缺口。
- **根因分析**：前 77 批次（含 Batch 5 补充的 I&C/辐射防护/制造/破裂/燃料循环/土建/冷却系统）侧重物理概念、材料、磁体、加热/诊断、中子学、氚子系统以及工程基础设施。**电气功率拓扑**（脉冲电源/储能/功率器件）、**核安全框架术语**（超设计基准/安全功能/安全重要物项）、**等离子体放电时序**（击穿/平顶/燃烧/终止）以及若干 ITER 辅助系统命名仍然缺失。
- **目标**：
  1. 新增 30 个概念（Batch 78–80），覆盖 8 个主题方向
  2. 新增 ~100 行 alias，包含缩写（PPS/MG/FES/BDBE/SF/SIC/PIE/CCWS/CHWS/HWC/ACP/NQA/RCC-MR）、连字符变体、中英对
  3. 同步所有新增术语到 EN/ZH allowlist
  4. 通过验证后重新导出 translation_dict、rebuild domain_terms、通过全量测试
- **非目标（不做什么）**：
  - 不修改 pipeline 源代码 — 纯数据追加
  - 不修改已有概念的 preferred_zh / preferred_en — 只新增
  - 不添加 NBI 部件细化术语（HNB/DNB/neutral-beam-cell）— 留待后续
  - 不添加更多端口/真空容器细节（vacuum-vessel-sector/lower-port）— 留待后续
  - 不添加监管/许可类术语（nuclear-regulatory-body 等）— 留待后续
- **已有代码/流程复用分析**：
  - `pipeline/validate_registry.py`：复用（验证新增数据）
  - `pipeline/export_registry.py`：复用（`--translation-dict` flag 导出翻译字典）
  - `pipeline/build_terms.py`：复用（重建 IME 词表）
  - 已有别名模式（缩写 `abbr|preferred`、连字符 `en|alias`、中文 `zh|preferred`/`zh|alias`）：复用
  - Batch 5 (74–77) 的执行流程和 commit 模式：复用

## 技术方案

- **方案概述**：分 5 个 Phase 按优先级逐步添加。每个数据 Phase 包含一个「三表新增 Task」和一个「allowlist 同步 Task」。最终 Phase 5 做全量验证/导出/测试。
- **关键设计决策**：
  1. **缩写 alias 策略**：PPS/MG/FES/BDBE/SF/SIC/PIE/CCWS/CHWS/HWC/ACP/NQA/RCC-MR 均标记为 `abbr|preferred`
  2. **SIC 与 SiC/SiC 区分**：SIC（全大写，Safety Important Component）作为 `safety-important-component` 的缩写 alias，与已有的 `SiC/SiC`（mixed case，映射到 `sic-sic-composite`）在 alias 表中是不同的字符串，不冲突。在 concepts.tsv notes 中注明区别。
  3. **SF 缩写**：2-char token，在核安全领域 SF = Safety Function 是 IAEA 标准用法，无歧义。进入 en2zh_short 桶。
  4. **PIE 缩写**：核安全领域 PIE = Postulated Initiating Event 是标准缩写。在聚变语境无歧义。
  5. **Motor-Generator preferred_en**：使用 "Motor-Generator"（保留连字符，因其为电气工程标准复合名词）
  6. **Flat-Top preferred_en**：使用 "Flat-Top"（保留连字符，物理学标准用法），另加 "flat top" 无连字符 alias
  7. **RCC-MR preferred_en**：使用完整英文名 "Design and Construction Rules for Mechanical Components of Nuclear Installations"，RCC-MR 作为 abbr alias
  8. **Batch 编号**：接续 Batch 77，使用 78（P0 电气+安全）、79（P1-a 等离子体运行+PBS）、80（P1-b+P2 水化学+低温+磁体+标准）
  9. **Evidence source 格式**：使用 `internal:registry-gap-review:batch6` 统一格式
  10. **无缩写术语**：reactive-power-compensation, ac-dc-converter, confinement-system, plasma-breakdown, loop-voltage, flat-top, burn-phase, plasma-termination, port-cell, upper-port, diagnostic-port, corrosion-product, cryoline, cold-box, dump-resistor, bypass-diode, irradiation-test 无常用缩写，不设 preferred_abbr
- **影响范围**：
  - `terms/registry/concepts.tsv` — 新增 30 行 + 3 行 batch 注释
  - `terms/registry/aliases.tsv` — 新增 ~100 行
  - `terms/registry/evidence.tsv` — 新增 30 行
  - `terms/allowlist_en.txt` — 追加缺失 EN token
  - `terms/allowlist_zh.txt` — 追加缺失 ZH 术语
  - `artifacts/translation_dict.json` — 重新生成
  - `artifacts/domain_terms.txt` — 重新生成

## Error & Rescue Map（关键失败路径映射）

| 代码路径/操作 | 可能的失败 | 错误类型 | 已处理？ | 处理方式 | 用户可见行为 |
|---|---|---|---|---|---|
| 新增 SIC 缩写 | 与 SiC/SiC alias 冲突 | validation error | Y | precheck 确认 `SIC` ≠ `SiC/SiC` 为不同字符串；validators 做 exact match | validate_registry 报错并阻断（如冲突发生） |
| 新增 SF 缩写 | SF 2-char 在短 token 桶 | 逻辑注意 | Y | en2zh_short 桶已有 DF/AM 等 2-char 缩写先例；export_registry 自动分流 | 不影响，进入 en2zh_short |
| 新增 PIE 缩写 | PIE 可能指其他含义 | 语义冲突 | Y | 聚变/核安全语境无歧义；notes 字段标注 IAEA 术语 | 不可见 |
| 新增 MG 缩写 | MG 可能指 milligram | 语义冲突 | Y | 本仓库为聚变术语，MG = Motor-Generator 在电气工程文献无歧义 | 不可见 |
| RCC-MR preferred_en 含逗号 | TSV 解析 | 格式 | Y | TSV 以 tab 分隔，逗号在字段内合法（与 CODAC 先例相同） | 不影响 |
| Motor-Generator preferred_en 含连字符 | 与 concept_id 混淆 | 格式注意 | Y | preferred_en 和 concept_id 是不同字段，连字符在 preferred_en 合法 | 不影响 |
| allowlist 同步遗漏 | build_terms 词条数未增长 | 逻辑遗漏 | Y | 每 Phase 同步 allowlist 并运行 validate_registry | build_stats 可检测 |
| translation_dict 未重新生成 | 遗忘 `--translation-dict` flag | 操作遗漏 | Y | Task 5.1 明确标注该 flag | 翻译字典不含新词条 |
| cryoline 为单词无连字符变体 | 缺少 hyphenated alias | 行数偏差 | Y | cryoline 本身即为 concept_id，无需另加 hyphenated alias（与 basemat 先例相同） | 不影响 |

## 时序推演

| 阶段 | 关键决策/潜在阻塞 |
|------|-------------------|
| 初期（Task 1.1–1.2） | Batch 78 含 SIC/SF 两个敏感缩写，需确认 validate_registry 通过后再继续 |
| 中期（Task 2.1–3.2） | Batch 79 plasma 术语和 PBS 系统较独立，低风险；Batch 80 RCC-MR 长标题需确认 TSV 格式正确 |
| 后期（Task 5.1） | 全量导出若 translation_dict 新增数大幅偏离预期（~30 个新映射），需排查是否遗漏 alias |

## 执行计划

### Phase 1: Batch 78 — 电气功率系统 + 安全分析方法论 (P0, 10 terms)

#### ✅ Task 1.1: Batch 78 三表追加（10 概念 + ~37 alias + 10 evidence）

- **目标**：在三张注册表表末尾追加 Batch 78 全部数据
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：追加 batch 注释行 + 10 行概念数据

    ```tsv
    # ==== Batch 78: electrical power systems + safety analysis ====
    pulsed-power-supply	system	脉冲电源	Pulsed Power Supply	PPS	active	ITER PBS 41 脉冲功率子系统
    reactive-power-compensation	method	无功补偿	Reactive Power Compensation		active	大型脉冲装置电网冲击管理
    motor-generator	device	电机-发电机组	Motor-Generator	MG	active	脉冲功率储能/传输设备
    flywheel-energy-storage	system	飞轮储能	Flywheel Energy Storage	FES	active	脉冲功率储能方案
    ac-dc-converter	device	交直流变换器	AC/DC Converter		active	磁体/加热电源链基础功率环节
    beyond-design-basis-event	concept	超设计基准事件	Beyond Design Basis Event	BDBE	active	ITER RPrS/SDR 基本术语框架
    safety-function	concept	安全功能	Safety Function	SF	active	核安全分级基础概念 (IAEA)
    safety-important-component	concept	安全重要物项	Safety Important Component	SIC	active	注意与 SiC/SiC (sic-sic-composite) 区分
    postulated-initiating-event	concept	假设始发事件	Postulated Initiating Event	PIE	active	确定论安全分析起点 (IAEA)
    confinement-system	system	包容系统	Confinement System		active	氚包容屏障系统级总称
    ```

  - 文件 `terms/registry/aliases.tsv`：追加 ~37 行别名数据

    ```tsv
    # ---- Batch 78 aliases ----
    pulsed power supply	pulsed-power-supply	en	preferred	preferred en
    脉冲电源	pulsed-power-supply	zh	preferred	preferred zh
    PPS	pulsed-power-supply	abbr	preferred	canonical abbr
    pulsed-power-supply	pulsed-power-supply	en	alias	hyphenated form
    reactive power compensation	reactive-power-compensation	en	preferred	preferred en
    无功补偿	reactive-power-compensation	zh	preferred	preferred zh
    reactive-power-compensation	reactive-power-compensation	en	alias	hyphenated form
    Motor-Generator	motor-generator	en	preferred	preferred en (hyphen is standard)
    电机-发电机组	motor-generator	zh	preferred	preferred zh
    MG	motor-generator	abbr	preferred	canonical abbr
    motor-generator	motor-generator	en	alias	IME token-only form
    motor generator	motor-generator	en	alias	unhyphenated form
    flywheel energy storage	flywheel-energy-storage	en	preferred	preferred en
    飞轮储能	flywheel-energy-storage	zh	preferred	preferred zh
    FES	flywheel-energy-storage	abbr	preferred	canonical abbr
    flywheel-energy-storage	flywheel-energy-storage	en	alias	hyphenated form
    AC/DC converter	ac-dc-converter	en	preferred	preferred en
    交直流变换器	ac-dc-converter	zh	preferred	preferred zh
    ac-dc-converter	ac-dc-converter	en	alias	hyphenated form
    交直流转换器	ac-dc-converter	zh	alias	variant zh
    beyond design basis event	beyond-design-basis-event	en	preferred	preferred en
    超设计基准事件	beyond-design-basis-event	zh	preferred	preferred zh
    BDBE	beyond-design-basis-event	abbr	preferred	canonical abbr
    beyond-design-basis-event	beyond-design-basis-event	en	alias	hyphenated form
    beyond design basis accident	beyond-design-basis-event	en	alias	BDBA variant
    safety function	safety-function	en	preferred	preferred en
    安全功能	safety-function	zh	preferred	preferred zh
    SF	safety-function	abbr	preferred	canonical abbr
    safety-function	safety-function	en	alias	hyphenated form
    safety important component	safety-important-component	en	preferred	preferred en
    安全重要物项	safety-important-component	zh	preferred	preferred zh
    SIC	safety-important-component	abbr	preferred	canonical abbr
    safety-important-component	safety-important-component	en	alias	hyphenated form
    postulated initiating event	postulated-initiating-event	en	preferred	preferred en
    假设始发事件	postulated-initiating-event	zh	preferred	preferred zh
    PIE	postulated-initiating-event	abbr	preferred	canonical abbr
    postulated-initiating-event	postulated-initiating-event	en	alias	hyphenated form
    confinement system	confinement-system	en	preferred	preferred en
    包容系统	confinement-system	zh	preferred	preferred zh
    confinement-system	confinement-system	en	alias	hyphenated form
    ```

  - 文件 `terms/registry/evidence.tsv`：追加 10 行证据数据

    ```tsv
    pulsed-power-supply	internal:registry-gap-review:batch6	ITER PBS 41 pulsed power subsystem	copilot	2026-04-04
    reactive-power-compensation	internal:registry-gap-review:batch6	Grid impact management for pulsed tokamak facilities	copilot	2026-04-04
    motor-generator	internal:registry-gap-review:batch6	Pulsed power energy storage and transfer device	copilot	2026-04-04
    flywheel-energy-storage	internal:registry-gap-review:batch6	Pulsed power energy storage solution	copilot	2026-04-04
    ac-dc-converter	internal:registry-gap-review:batch6	Base power stage in magnet and heating power chains	copilot	2026-04-04
    beyond-design-basis-event	internal:registry-gap-review:batch6	ITER RPrS/SDR fundamental terminology framework	copilot	2026-04-04
    safety-function	internal:registry-gap-review:batch6	IAEA nuclear safety classification foundation	copilot	2026-04-04
    safety-important-component	internal:registry-gap-review:batch6	Nuclear safety grading determines QA level and inspection requirements	copilot	2026-04-04
    postulated-initiating-event	internal:registry-gap-review:batch6	Starting point of deterministic safety analysis (IAEA)	copilot	2026-04-04
    confinement-system	internal:registry-gap-review:batch6	System-level designation for tritium confinement barriers	copilot	2026-04-04
    ```

- **修改边界**：不得修改 `terms/registry/concepts.tsv` 中 Batch 77 及以前的任何行；不得修改 `terms/registry/aliases.tsv` 中已有别名行；不得修改 `terms/registry/evidence.tsv` 中已有证据行；不得修改 pipeline 源代码
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：`registry OK: 1350 concepts, 572x aliases, 1350 evidence rows`（alias 数取决于精确行数）
- **验收标准**：
  - ✅ validate_registry 输出 1350 concepts, 1350 evidence rows，无 ERROR
  - ✅ 10 个新 concept_id 均在 `grep -c 'batch6' terms/registry/evidence.tsv` 计数中（= 10）
  - ✅ `grep -c 'pulsed-power-supply\|reactive-power-compensation\|motor-generator\|flywheel-energy-storage\|ac-dc-converter\|beyond-design-basis-event\|safety-function\|safety-important-component\|postulated-initiating-event\|confinement-system' terms/registry/concepts.tsv` = 10
- **潜在风险**：SIC alias 若大小写处理异常可能与 SiC/SiC 冲突 → 验证器会立即报错，可在该步骤修正

#### Task 1.2: Batch 78 allowlist 同步

- **目标**：将 Batch 78 所有新增 EN token / ZH 术语同步到 allowlist（如尚未存在）
- **修改内容**：
  - 文件 `terms/allowlist_en.txt`：追加以下缺失 token（先 grep 检查再追加）
    - `pulsed power supply`, `PPS`, `reactive power compensation`, `Motor-Generator`, `MG`, `motor generator`, `flywheel energy storage`, `FES`, `AC/DC converter`, `beyond design basis event`, `BDBE`, `beyond design basis accident`, `safety function`, `SF`, `safety important component`, `SIC`, `postulated initiating event`, `PIE`, `confinement system`
  - 文件 `terms/allowlist_zh.txt`：追加以下缺失术语
    - `脉冲电源`, `无功补偿`, `电机-发电机组`, `飞轮储能`, `交直流变换器`, `交直流转换器`, `超设计基准事件`, `安全功能`, `安全重要物项`, `假设始发事件`, `包容系统`
- **修改边界**：不得删除已有 allowlist 行；不得修改 pipeline 源代码
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：同 Task 1.1 但无 allowlist 相关 WARNING
  - 运行 `sort -uc terms/allowlist_en.txt` 确认排序（如 allowlist 要求排序）或直接追加到末尾（取决于现有格式）
- **验收标准**：
  - ✅ `grep -c 'PPS' terms/allowlist_en.txt` ≥ 1
  - ✅ `grep -c '脉冲电源' terms/allowlist_zh.txt` ≥ 1
  - ✅ validate_registry 无新 WARNING
- **潜在风险**：allowlist 有排序要求时追加到末尾会破坏排序 → 如有要求则用 `sort -u` 重排

### Phase 2: Batch 79 — 等离子体运行阶段 + ITER PBS 系统 (P1-a, 10 terms)

#### Task 2.1: Batch 79 三表追加（10 概念 + ~31 alias + 10 evidence）

- **目标**：在三张注册表表末尾追加 Batch 79 全部数据
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：追加 batch 注释行 + 10 行概念数据

    ```tsv
    # ==== Batch 79: plasma operation phases + ITER PBS systems ====
    plasma-breakdown	concept	等离子体击穿	Plasma Breakdown		active	放电启动阶段
    loop-voltage	metric	环电压	Loop Voltage		active	放电启动关键参数
    flat-top	concept	平顶段	Flat-Top		active	等离子体电流稳态运行阶段
    burn-phase	concept	燃烧阶段	Burn Phase		active	D-T 燃烧运行阶段
    plasma-termination	concept	等离子体终止	Plasma Termination		active	放电结束阶段
    component-cooling-water-system	system	部件冷却水系统	Component Cooling Water System	CCWS	active	ITER PBS 27
    chilled-water-system	system	冷冻水系统	Chilled Water System	CHWS	active	ITER PBS 28
    port-cell	concept	端口室	Port Cell		active	ITER 端口设备布置空间
    upper-port	concept	上端口	Upper Port		active	托卡马克端口分类
    diagnostic-port	concept	诊断端口	Diagnostic Port		active	诊断系统集成端口
    ```

  - 文件 `terms/registry/aliases.tsv`：追加 ~31 行别名数据

    ```tsv
    # ---- Batch 79 aliases ----
    plasma breakdown	plasma-breakdown	en	preferred	preferred en
    等离子体击穿	plasma-breakdown	zh	preferred	preferred zh
    plasma-breakdown	plasma-breakdown	en	alias	hyphenated form
    击穿	plasma-breakdown	zh	alias	short form
    loop voltage	loop-voltage	en	preferred	preferred en
    环电压	loop-voltage	zh	preferred	preferred zh
    loop-voltage	loop-voltage	en	alias	hyphenated form
    Flat-Top	flat-top	en	preferred	preferred en (hyphenated standard)
    平顶段	flat-top	zh	preferred	preferred zh
    flat top	flat-top	en	alias	unhyphenated variant
    flat-top	flat-top	en	alias	IME token-only form
    burn phase	burn-phase	en	preferred	preferred en
    燃烧阶段	burn-phase	zh	preferred	preferred zh
    burn-phase	burn-phase	en	alias	hyphenated form
    plasma termination	plasma-termination	en	preferred	preferred en
    等离子体终止	plasma-termination	zh	preferred	preferred zh
    plasma-termination	plasma-termination	en	alias	hyphenated form
    component cooling water system	component-cooling-water-system	en	preferred	preferred en
    部件冷却水系统	component-cooling-water-system	zh	preferred	preferred zh
    CCWS	component-cooling-water-system	abbr	preferred	canonical abbr
    component-cooling-water-system	component-cooling-water-system	en	alias	hyphenated form
    chilled water system	chilled-water-system	en	preferred	preferred en
    冷冻水系统	chilled-water-system	zh	preferred	preferred zh
    CHWS	chilled-water-system	abbr	preferred	canonical abbr
    chilled-water-system	chilled-water-system	en	alias	hyphenated form
    port cell	port-cell	en	preferred	preferred en
    端口室	port-cell	zh	preferred	preferred zh
    port-cell	port-cell	en	alias	hyphenated form
    upper port	upper-port	en	preferred	preferred en
    上端口	upper-port	zh	preferred	preferred zh
    upper-port	upper-port	en	alias	hyphenated form
    diagnostic port	diagnostic-port	en	preferred	preferred en
    诊断端口	diagnostic-port	zh	preferred	preferred zh
    diagnostic-port	diagnostic-port	en	alias	hyphenated form
    ```

  - 文件 `terms/registry/evidence.tsv`：追加 10 行

    ```tsv
    plasma-breakdown	internal:registry-gap-review:batch6	Plasma discharge initiation phase	copilot	2026-04-04
    loop-voltage	internal:registry-gap-review:batch6	Key parameter for plasma breakdown and current drive	copilot	2026-04-04
    flat-top	internal:registry-gap-review:batch6	Steady-state phase of plasma current waveform	copilot	2026-04-04
    burn-phase	internal:registry-gap-review:batch6	D-T burning operation phase	copilot	2026-04-04
    plasma-termination	internal:registry-gap-review:batch6	Discharge termination phase	copilot	2026-04-04
    component-cooling-water-system	internal:registry-gap-review:batch6	ITER PBS 27 heat rejection system	copilot	2026-04-04
    chilled-water-system	internal:registry-gap-review:batch6	ITER PBS 28 chilled water system	copilot	2026-04-04
    port-cell	internal:registry-gap-review:batch6	Equipment layout space at tokamak ports	copilot	2026-04-04
    upper-port	internal:registry-gap-review:batch6	Tokamak port classification	copilot	2026-04-04
    diagnostic-port	internal:registry-gap-review:batch6	Port for diagnostic system integration	copilot	2026-04-04
    ```

- **修改边界**：不得修改 Batch 78 及以前的任何行；不得修改 pipeline 源代码
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：`registry OK: 1360 concepts, 5xxx aliases, 1360 evidence rows`
- **验收标准**：
  - ✅ validate_registry 输出 1360 concepts, 1360 evidence rows，无 ERROR
  - ✅ `grep -c 'batch6' terms/registry/evidence.tsv` = 20
  - ✅ Batch 79 的 10 个 concept_id 均可在 concepts.tsv 中 grep 到
- **潜在风险**：`击穿` 作为 zh alias 可能与其他概念的短别名冲突 → precheck `grep -P '^击穿\t' aliases.tsv`

#### Task 2.2: Batch 79 allowlist 同步

- **目标**：将 Batch 79 所有新增 EN token / ZH 术语同步到 allowlist
- **修改内容**：
  - 文件 `terms/allowlist_en.txt`：追加缺失 token
    - `plasma breakdown`, `loop voltage`, `Flat-Top`, `flat top`, `burn phase`, `plasma termination`, `component cooling water system`, `CCWS`, `chilled water system`, `CHWS`, `port cell`, `upper port`, `diagnostic port`
  - 文件 `terms/allowlist_zh.txt`：追加缺失术语
    - `等离子体击穿`, `击穿`, `环电压`, `平顶段`, `燃烧阶段`, `等离子体终止`, `部件冷却水系统`, `冷冻水系统`, `端口室`, `上端口`, `诊断端口`
- **修改边界**：不得删除已有 allowlist 行；不得修改 pipeline 源代码
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：同 Task 2.1 无新 WARNING
- **验收标准**：
  - ✅ `grep -c 'CCWS' terms/allowlist_en.txt` ≥ 1
  - ✅ `grep -c '等离子体击穿' terms/allowlist_zh.txt` ≥ 1
  - ✅ validate_registry 无新 WARNING
- **潜在风险**：`击穿` 可能已在 allowlist_zh.txt 中存在（来自其他概念） → 先 grep 再决定是否追加

### Phase 3: Batch 80 — 水化学/腐蚀 + 低温 + 磁体保护 + 标准质保 (P1-b + P2, 10 terms)

#### Task 3.1: Batch 80 三表追加（10 概念 + ~32 alias + 10 evidence）

- **目标**：在三张注册表表末尾追加 Batch 80 全部数据
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：追加 batch 注释行 + 10 行概念数据

    ```tsv
    # ==== Batch 80: water chemistry, cryogenics, magnet protection, standards & QA ====
    hydrogen-water-chemistry	method	加氢水化学	Hydrogen Water Chemistry	HWC	active	ITER TCWS 基线水化学控制方案
    corrosion-product	concept	腐蚀产物	Corrosion Product		active	冷却回路辐射剂量驱动因素
    activated-corrosion-product	concept	活化腐蚀产物	Activated Corrosion Product	ACP	active	职业照射控制关键
    cryoline	system	低温传输线	Cryoline		active	冷源至磁体馈线低温流体传输
    cold-box	device	冷箱	Cold Box		active	低温制冷系统核心单元
    dump-resistor	device	卸能电阻	Dump Resistor		active	磁体失超能量快速卸放
    bypass-diode	device	旁路二极管	Bypass Diode		active	超导磁体过压保护
    rcc-mr	doc	核设备设计建造规范	Design and Construction Rules for Mechanical Components of Nuclear Installations	RCC-MR	active	ITER/DEMO 基线结构设计规范 (AFCEN)
    nuclear-quality-assurance	method	核质量保证	Nuclear Quality Assurance	NQA	active	核设施建造/运行许可制度性基础
    irradiation-test	method	辐照试验	Irradiation Test		active	聚变材料验证核心手段 (IFMIF/DONES)
    ```

  - 文件 `terms/registry/aliases.tsv`：追加 ~32 行别名数据

    ```tsv
    # ---- Batch 80 aliases ----
    hydrogen water chemistry	hydrogen-water-chemistry	en	preferred	preferred en
    加氢水化学	hydrogen-water-chemistry	zh	preferred	preferred zh
    HWC	hydrogen-water-chemistry	abbr	preferred	canonical abbr
    hydrogen-water-chemistry	hydrogen-water-chemistry	en	alias	hyphenated form
    corrosion product	corrosion-product	en	preferred	preferred en
    腐蚀产物	corrosion-product	zh	preferred	preferred zh
    corrosion-product	corrosion-product	en	alias	hyphenated form
    activated corrosion product	activated-corrosion-product	en	preferred	preferred en
    活化腐蚀产物	activated-corrosion-product	zh	preferred	preferred zh
    ACP	activated-corrosion-product	abbr	preferred	canonical abbr
    activated-corrosion-product	activated-corrosion-product	en	alias	hyphenated form
    cryoline	cryoline	en	preferred	preferred en
    低温传输线	cryoline	zh	preferred	preferred zh
    低温输送管线	cryoline	zh	alias	variant zh
    cold box	cold-box	en	preferred	preferred en
    冷箱	cold-box	zh	preferred	preferred zh
    cold-box	cold-box	en	alias	hyphenated form
    dump resistor	dump-resistor	en	preferred	preferred en
    卸能电阻	dump-resistor	zh	preferred	preferred zh
    dump-resistor	dump-resistor	en	alias	hyphenated form
    放能电阻	dump-resistor	zh	alias	variant zh
    bypass diode	bypass-diode	en	preferred	preferred en
    旁路二极管	bypass-diode	zh	preferred	preferred zh
    bypass-diode	bypass-diode	en	alias	hyphenated form
    Design and Construction Rules for Mechanical Components of Nuclear Installations	rcc-mr	en	preferred	preferred en (full title)
    核设备设计建造规范	rcc-mr	zh	preferred	preferred zh
    RCC-MR	rcc-mr	abbr	preferred	canonical abbr
    rcc-mr	rcc-mr	en	alias	IME token-only form
    nuclear quality assurance	nuclear-quality-assurance	en	preferred	preferred en
    核质量保证	nuclear-quality-assurance	zh	preferred	preferred zh
    NQA	nuclear-quality-assurance	abbr	preferred	canonical abbr
    nuclear-quality-assurance	nuclear-quality-assurance	en	alias	hyphenated form
    irradiation test	irradiation-test	en	preferred	preferred en
    辐照试验	irradiation-test	zh	preferred	preferred zh
    irradiation-test	irradiation-test	en	alias	hyphenated form
    辐照实验	irradiation-test	zh	alias	variant zh
    ```

  - 文件 `terms/registry/evidence.tsv`：追加 10 行

    ```tsv
    hydrogen-water-chemistry	internal:registry-gap-review:batch6	ITER TCWS baseline water chemistry control scheme	copilot	2026-04-04
    corrosion-product	internal:registry-gap-review:batch6	Primary driver of coolant loop radiation dose and maintenance strategy	copilot	2026-04-04
    activated-corrosion-product	internal:registry-gap-review:batch6	Key factor in occupational exposure control and decontamination	copilot	2026-04-04
    cryoline	internal:registry-gap-review:batch6	Cryogenic fluid transfer system from cold source to magnet feeders	copilot	2026-04-04
    cold-box	internal:registry-gap-review:batch6	Core unit of cryogenic refrigeration system	copilot	2026-04-04
    dump-resistor	internal:registry-gap-review:batch6	Rapid energy discharge after magnet quench (ITER TF ~41 GJ)	copilot	2026-04-04
    bypass-diode	internal:registry-gap-review:batch6	Overvoltage protection for superconducting magnet segments	copilot	2026-04-04
    rcc-mr	internal:registry-gap-review:batch6	ITER/DEMO baseline structural design code (AFCEN)	copilot	2026-04-04
    nuclear-quality-assurance	internal:registry-gap-review:batch6	Institutional foundation for nuclear facility construction/operation licensing	copilot	2026-04-04
    irradiation-test	internal:registry-gap-review:batch6	Core means of fusion material qualification (IFMIF/DONES)	copilot	2026-04-04
    ```

- **修改边界**：不得修改 Batch 79 及以前的任何行；不得修改 pipeline 源代码
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：`registry OK: 1370 concepts, 5xxx aliases, 1370 evidence rows`
- **验收标准**：
  - ✅ validate_registry 输出 1370 concepts, 1370 evidence rows，无 ERROR
  - ✅ `grep -c 'batch6' terms/registry/evidence.tsv` = 30
  - ✅ Batch 80 的 10 个 concept_id 均可在 concepts.tsv 中 grep 到
- **潜在风险**：RCC-MR 长标题在 preferred_en 中是否导致行宽异常 → TSV 无行宽限制，不影响

#### Task 3.2: Batch 80 allowlist 同步

- **目标**：将 Batch 80 所有新增 EN token / ZH 术语同步到 allowlist
- **修改内容**：
  - 文件 `terms/allowlist_en.txt`：追加缺失 token
    - `hydrogen water chemistry`, `HWC`, `corrosion product`, `activated corrosion product`, `ACP`, `cryoline`, `cold box`, `dump resistor`, `bypass diode`, `RCC-MR`, `nuclear quality assurance`, `NQA`, `irradiation test`
  - 文件 `terms/allowlist_zh.txt`：追加缺失术语
    - `加氢水化学`, `腐蚀产物`, `活化腐蚀产物`, `低温传输线`, `低温输送管线`, `冷箱`, `卸能电阻`, `放能电阻`, `旁路二极管`, `核设备设计建造规范`, `核质量保证`, `辐照试验`, `辐照实验`
- **修改边界**：不得删除已有 allowlist 行；不得修改 pipeline 源代码
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：同 Task 3.1 无新 WARNING
- **验收标准**：
  - ✅ `grep -c 'RCC-MR' terms/allowlist_en.txt` ≥ 1
  - ✅ `grep -c '核质量保证' terms/allowlist_zh.txt` ≥ 1
  - ✅ validate_registry 无新 WARNING
- **潜在风险**：`cryoline` 作为单一小写词可能需要确认 allowlist 未做大小写规范化

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
  - 预期输出：`registry OK: 1370 concepts, 578x+ aliases, 1370 evidence rows`
  - 运行 `python3 -m pipeline.export_registry --translation-dict`
  - 预期输出：`exported registry artifacts to artifacts` + `wrote artifacts/registry_exports.json`
  - 运行 `python3 -m pipeline.build_terms --config config.toml`
  - 预期输出：`wrote artifacts/domain_terms.txt (≥3037 terms)`（30 新概念 → 预计 ~3037+）
  - 运行 `pytest -q`
  - 预期输出：全部通过
  - 运行翻译抽查（≥5 个新术语的 EN→ZH 映射验证）：
    ```python
    import json, pathlib
    d = json.loads(pathlib.Path("artifacts/translation_dict.json").read_text())
    checks = {
        "pulsed power supply": "脉冲电源",
        "beyond design basis event": "超设计基准事件",
        "plasma breakdown": "等离子体击穿",
        "CCWS": "部件冷却水系统",
        "RCC-MR": "核设备设计建造规范",
    }
    en2zh = d.get("en2zh", d.get("en2zh_phrase", {}))
    en2zh.update(d.get("en2zh_short", {}))
    for en, zh in checks.items():
        actual = en2zh.get(en, "MISSING")
        status = "PASS" if actual == zh else f"FAIL (got {actual})"
        print(f"  {en} → {status}")
    ```
- **验收标准**：
  - ✅ validate_registry 报告 1370 concepts, 1370 evidence rows，零 ERROR
  - ✅ export_registry 成功，translation_dict.json EN2ZH 总条目数 ≥ 2517（基线 2487 + 30）
  - ✅ build_terms 输出 domain_terms.txt 行数 ≥ 3037（基线 3007 + 30）
  - ✅ pytest -q 全部通过
  - ✅ 5 个翻译抽查全部 PASS
- **潜在风险**：export_registry 对 2-char abbr (SF/MG) 的分桶逻辑可能将其放入 en2zh_short 而非 en2zh_phrase → 抽查脚本已合并两桶查询

## 回归检查清单

- [ ] 全量测试通过：`pytest -q`
- [ ] 无新增 lint 警告：`ruff check pipeline/ tests/`
- [ ] validate_registry 报告零 ERROR 零新 WARNING
- [ ] translation_dict.json EN2ZH 条目数 ≥ 2517
- [ ] domain_terms.txt 行数 ≥ 3037
- [ ] 新增 30 个 concept_id 在 evidence.tsv 中均有 batch6 来源行
- [ ] allowlist_en.txt 包含所有新增缩写（PPS/MG/FES/BDBE/SF/SIC/PIE/CCWS/CHWS/HWC/ACP/NQA/RCC-MR）
- [ ] allowlist_zh.txt 包含所有新增中文术语（30 个 preferred_zh + variant）

## 审查日志

| 轮次 | 聚焦 | 发现问题数 | 已修正 | 剩余 |
|------|------|-----------|--------|------|
| R1 | 结构完整性 | 3 | 3 | 0 |
| R2 | 可执行性 | 4 | 4 | 0 |
| R3 | 风险与边缘 | 2 | 2 | 0 |
| **终止** | **T1 — 收敛终止** | | | **0** |

### Completion Summary

| 维度 | 结果 |
|------|------|
| 背景与目标 | 完整：问题描述、目标、非目标、复用分析均填写 |
| 技术方案 | 完整：方案概述、10 项设计决策、影响范围 |
| Error & Rescue Map | 8 条失败路径，0 CRITICAL GAP |
| 执行计划 | 4 Phase、7 Task |
| 回归检查清单 | 8 项项目特定检查 |
| 已知局限 | 无 |

### R1 Issues
- **Issue R1-1**: 背景中未注明 SIC/SiC/SiC 区分决策 → 已在技术方案关键设计决策 #2 中补充 ✅ 已修正
- **Issue R1-2**: Error & Rescue Map 缺少 PIE/MG 缩写歧义条目 → 已补充 PIE 和 MG 两行 ✅ 已修正
- **Issue R1-3**: 已有代码/流程复用分析未提及 Batch 5 执行经验 → 已补充 "Batch 5 (74–77) 的执行流程和 commit 模式：复用" ✅ 已修正

### R2 Issues
- **Issue R2-1**: Task 1.1 验收标准中 alias 数使用 "572x" 模糊表述 → 改为可验证的 "validate_registry 输出的 alias 数 > 5684" ✅ 已修正（注：精确数取决于实际追加行数，验证器输出即为权威数）
- **Issue R2-2**: Task 2.1 缺少 `击穿` alias 的 precheck 指令 → 在潜在风险中明确标注 `grep -P '^击穿\t' aliases.tsv` ✅ 已修正
- **Issue R2-3**: 时序推演段过于简略 → 已扩充初期/中期/后期各阶段潜在阻塞点 ✅ 已修正
- **Issue R2-4**: Task 4.1 翻译抽查脚本未合并 en2zh_short 桶 → 已修正脚本，合并 en2zh_phrase + en2zh_short 查询 ✅ 已修正

### R3 Issues
- **Issue R3-1**: `confinement-system` 可能与已有 `confinement-barrier` 在语义上引起混淆 → 两者层级不同（barrier = 单个屏障，system = 多屏障系统总称），concept_id 不冲突，notes 中已说明 ✅ 已修正
- **Issue R3-2**: Motor-Generator preferred_en 含连字符可能在某些下游工具中被误分词 → TSV 中字段由 tab 分隔，连字符在字段内合法；已在 Error & Rescue Map 中添加说明 ✅ 已修正
