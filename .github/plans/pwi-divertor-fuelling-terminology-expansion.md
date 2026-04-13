# PWI / 偏滤器 / 加料 / 壁调理 / 加热 / 标度律 — 术语扩展

## 背景与目标

- **问题/需求描述**：当前 registry 对"等离子体-壁相互作用 (PWI)""偏滤器物理""充气/加料""壁调理""加热与电流驱动标度律"6 个子领域覆盖不足。部分已有条目的 preferred_zh 与领域惯用译法偏离，且大量常见错误/不规范译法尚未录入 forbidden/deprecated 别名。
- **目标**：
  1. 新增 8 个 concept（chemical-sputtering, sputtering-yield, desorption, implantation-range, parallel-cooling, cross-field-cooling, attached-regime, coating-degradation）。
  2. 修正 4 个现有 concept 的 preferred_zh（wall-conditioning, bakeout, lithium-coating, wall-pumping）。
  3. 新增约 50 条 aliases（preferred / alias / deprecated / forbidden），覆盖用户列出的全部错误/不规范变体。
  4. 修改约 10 条已有 alias 行（调整 concept_id、kind 或 comment）。
  5. 新增 8 条 evidence 行。
- **非目标（不做什么）**：
  - 不删除任何已有 concept 或 alias — 只添加或修改正向覆盖
  - 不修改 pipeline 代码、测试文件或构建脚本
  - 不调整 allowlist/denylist/synonyms.tsv — 那些是提取阶段文件，不在此次范围
  - 不处理用户提到的"已在 registry 中完全覆盖"的条目（如"回收系数→再循环系数"已 forbidden）
- **已有代码/流程复用分析**：
  - concepts.tsv / aliases.tsv / evidence.tsv 三文件 TSV 格式：复用（直接追加/修改行）
  - `pipeline.validate_registry`：复用（每个 Task 完成后运行验证）
  - `pipeline.export_registry`：复用（最终运行确认导出正常）

## 技术方案

- **方案概述**：直接编辑 `terms/registry/` 下三个 TSV 文件。按 6 个子领域分 Phase 实施，每个 Phase 包含 concept 新增/修改 + alias 新增/修改 + evidence 新增。最后运行验证 + 导出。
- **关键设计决策**：
  - `chemical-sputtering` 从 `sputtering` 和 `chemical-erosion` 各夺回一条 alias（validator 禁止同一 alias 映射多个 concept_id）。
  - preferred_zh 变更时，旧 preferred alias 行降级为 deprecated/alias（不删除），新 preferred 行新增。
  - 所有 forbidden/deprecated alias 的 comment 引用修正后的 preferred_zh（如"应为 壁调理"而非"应为 壁面处理"）。
- **影响范围**：
  - `terms/registry/concepts.tsv` — 新增 8 行 + 修改 4 行
  - `terms/registry/aliases.tsv` — 新增 ~50 行 + 修改 ~10 行
  - `terms/registry/evidence.tsv` — 新增 8 行
- **审查姿态**：`EXPANSION`（新领域覆盖）

## Error & Rescue Map（关键失败路径映射）

| 代码路径/操作 | 可能的失败 | 错误类型 | 已处理？ | 处理方式 | 用户可见行为 |
|-------------|-----------|---------|---------|---------|------------|
| aliases.tsv: 同一 alias 映射多个 concept_id | `validate_registry` 报 "maps to multiple concept_ids" | 数据冲突 | Y | Task 2.1 显式要求修改旧行的 concept_id 再添加新行 | 验证报错，阻断后续导出 |
| concepts.tsv: concept_id 重复 | `validate_registry` 报 "duplicate concept_id" | 数据重复 | Y | 每个新 concept_id 已通过 grep 确认不存在 | 验证报错 |
| preferred alias 缺失 | `validate_registry` 报 "concepts without preferred alias" | 数据不完整 | Y | 每个新 concept 至少有 en preferred + zh preferred alias | 验证报错 |
| evidence 行缺失 | `validate_registry` 不报错但数据不完整 | 数据遗漏 | Y | 每个新 concept 同步添加 evidence 行 | 无直接报错，但数据质量下降 |
| 旧 forbidden/deprecated comment 引用旧 preferred_zh | 语义不一致 | 注释过时 | Y | Task 中逐条更新受影响的 comment | 导出的 substitutions note 显示旧名称 |

## 执行计划

### Phase 1: PWI 等离子体-壁相互作用

#### ✅ Task 1.1: 修正 wall-pumping preferred_zh + 添加 PWI 泵浦相关 aliases

- **目标**：将 wall-pumping preferred_zh 从"壁抽气效应"改为"壁抽气"，添加泵浦误译 forbidden aliases
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：第 974 行，`壁抽气效应` → `壁抽气`
  - 文件 `terms/registry/aliases.tsv`：
    - 修改第 3074 行：`壁抽气效应	wall-pumping	zh	preferred` → `壁抽气效应	wall-pumping	zh	alias	含效应的变体`
    - 修改第 3075 行：`壁抽气	wall-pumping	zh	alias` → `壁抽气	wall-pumping	zh	preferred	preferred zh`
    - 修改第 3982 行：comment 中"正确为 壁抽气效应" → "正确为 壁抽气"
    - 追加：`壁面泵浦	wall-pumping	zh	forbidden	误译pumping(光学义泵浦)：正确为 壁抽气`
    - 追加：`壁泵浦	wall-pumping	zh	forbidden	误译pumping(光学义泵浦)：正确为 壁抽气`
- **修改边界**：不得修改 `sputtering`、`fuel-retention` 等其他 concept 的行（本 task 仅 wall-pumping）
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期：不因 wall-pumping 相关行报错（其他预存错误 `ABAQUS` 等属于已知问题，忽略）
- **验收标准**：
  - ✅ concepts.tsv 中 wall-pumping 行的 preferred_zh 为"壁抽气"
  - ✅ aliases.tsv 中"壁抽气"行 kind=preferred，"壁抽气效应"行 kind=alias
  - ✅ "壁面泵浦"和"壁泵浦"为 forbidden alias 且 comment 包含"正确为 壁抽气"
  - ✅ "壁泵送"行 comment 已更新为引用"壁抽气"
- **潜在风险**：下游 `terminology_substitutions.tsv` 导出会将"壁泵送→壁抽气效应"变为"壁泵送→壁抽气"——属于正确行为

#### ✅ Task 1.2: 新增 chemical-sputtering 概念 + 调整已有 alias 归属

- **目标**：创建 `chemical-sputtering` concept，将现有的"chemical sputtering"和"化学溅射" alias 从 sputtering / chemical-erosion 移至新 concept
- **执行顺序注意**：先在 concepts.tsv 追加 concept 行，再修改 aliases.tsv 中的 alias 行（确保 alias 指向的 concept_id 已存在）
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：紧接末尾追加注释块和数据行：
    ```
    # ---- PWI: chemical sputtering (化学溅射)
    chemical-sputtering	concept	化学溅射	chemical sputtering		active	Chemical ejection of surface atoms via reactive hydrogen species
    ```
  - 文件 `terms/registry/aliases.tsv`：
    - 修改第 398 行：`chemical sputtering	sputtering	en	alias	chemical sputtering variant` → `chemical sputtering	chemical-sputtering	en	preferred	preferred en (phrase)`
    - 修改第 4478 行：`化学溅射	chemical-erosion	zh	alias	sputtering form` → `化学溅射	chemical-sputtering	zh	preferred	preferred zh`
    - 追加：`chemical-sputtering	chemical-sputtering	en	alias	IME token-only form`
    - 追加：`化学刻蚀	chemical-erosion	zh	alias	chemical erosion 的刻蚀译法`
  - 文件 `terms/registry/evidence.tsv`：追加：
    ```
    chemical-sputtering	internal:registry-gap-review:pwi-expansion	Chemical sputtering of surface atoms by reactive hydrogen species	copilot	2026-04-13
    ```
- **修改边界**：
  - 不得修改 `chemical-erosion` concept 行本身（preferred_zh"化学腐蚀"保持不变）
  - 不得修改 `sputtering` concept 行
  - 不得删除任何现有 alias 行——仅修改 concept_id 和 kind
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期：无"maps to multiple concept_ids"错误
  - `grep "chemical-sputtering" terms/registry/concepts.tsv` — 恰好 1 行
- **验收标准**：
  - ✅ `chemical-sputtering` 出现在 concepts.tsv 且 status=active
  - ✅ "chemical sputtering" alias 指向 `chemical-sputtering`（非 `sputtering`）
  - ✅ "化学溅射" alias 指向 `chemical-sputtering`（非 `chemical-erosion`）
  - ✅ "化学刻蚀" 为 `chemical-erosion` 的 alias
  - ✅ evidence.tsv 包含 `chemical-sputtering` 行
- **潜在风险**：将"chemical sputtering"从 sputtering concept 移走后，sputtering concept 丢失一个 alias——但 sputtering 本身仍有"sputtering" preferred alias，不受影响

#### ✅ Task 1.3: 新增 sputtering-yield、desorption、implantation-range 概念

- **目标**：添加 3 个 PWI 新概念及其 preferred/forbidden aliases
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：追加：
    ```
    sputtering-yield	metric	溅射产额	sputtering yield		active	Number of surface atoms ejected per incident ion (dimensionless)
    desorption	concept	脱附	desorption		active	Release of adsorbed species from a surface
    implantation-range	metric	注入射程	implantation range		active	Mean penetration depth of implanted ions into a material
    ```
  - 文件 `terms/registry/aliases.tsv`：追加（含批次注释头）：
    ```
    # ==== PWI expansion: sputtering-yield, desorption, implantation-range ====
    sputtering yield	sputtering-yield	en	preferred	preferred en (phrase)
    sputtering-yield	sputtering-yield	en	alias	IME token-only form
    溅射产额	sputtering-yield	zh	preferred	preferred zh
    溅射率	sputtering-yield	zh	forbidden	率暗示时间量纲：正确为 溅射产额
    物理溅射率	physical-sputtering	zh	forbidden	率暗示时间量纲：正确为 物理溅射(产额)
    desorption	desorption	en	preferred	preferred en
    脱附	desorption	zh	preferred	preferred zh
    解吸	desorption	zh	deprecated	非标准：应为 脱附
    implantation range	implantation-range	en	preferred	preferred en (phrase)
    implantation-range	implantation-range	en	alias	IME token-only form
    注入射程	implantation-range	zh	preferred	preferred zh
    注入深度	implantation-range	zh	forbidden	误译range(射程≠深度)：正确为 注入射程
    ```
  - 文件 `terms/registry/aliases.tsv`：另追加 co-deposition 和 fuel-retention 补充 alias：
    ```
    共堆积	co-deposition	zh	alias	co-deposition 变体
    扣留	fuel-retention	zh	forbidden	误译retention：正确为 滞留
    ```
  - 文件 `terms/registry/evidence.tsv`：追加：
    ```
    sputtering-yield	internal:registry-gap-review:pwi-expansion	Dimensionless yield of ejected atoms per incident ion	copilot	2026-04-13
    desorption	internal:registry-gap-review:pwi-expansion	Release of adsorbed atoms/molecules from a surface	copilot	2026-04-13
    implantation-range	internal:registry-gap-review:pwi-expansion	Mean penetration depth of implanted ions	copilot	2026-04-13
    ```
- **修改边界**：不得修改 `physical-sputtering` concept 行（仅添加 forbidden alias "物理溅射率"）；不得修改已有的"物理溅射产额"和"physical sputtering yield" alias 行
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - `grep -c "sputtering-yield\|desorption\|implantation-range" terms/registry/concepts.tsv` — 输出 3
- **验收标准**：
  - ✅ 3 个新 concept 出现在 concepts.tsv
  - ✅ 每个 concept 至少有 en preferred + zh preferred alias
  - ✅ "溅射率"为 sputtering-yield 的 forbidden，"物理溅射率"为 physical-sputtering 的 forbidden
  - ✅ "解吸"为 desorption 的 deprecated，"注入深度"为 implantation-range 的 forbidden
  - ✅ "共堆积"为 co-deposition 的 alias
  - ✅ "扣留"为 fuel-retention 的 forbidden
  - ✅ evidence.tsv 包含 3 条新行
- **潜在风险**：desorption 的"解析"变体未加入 forbidden，因为"解析"在数学/编程语境含义不同，加入会产生误匹配

### Phase 2: 偏滤器物理

#### ✅ Task 2.1: 新增 parallel-cooling、cross-field-cooling、attached-regime + 偏滤器 alias 补充

- **目标**：添加 3 个偏滤器物理新概念，补充已有 divertor-target / sol-width / plasma-detachment 的 deprecated/forbidden aliases
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：追加：
    ```
    # ---- Divertor physics (偏滤器物理)
    parallel-cooling	concept	平行冷却	parallel cooling		active	Cooling via heat transport along magnetic field lines in SOL/divertor
    cross-field-cooling	concept	横向冷却	cross-field cooling		active	Cooling via heat transport perpendicular to magnetic field lines
    attached-regime	concept	贴靠模式	attached regime		active	Divertor operating regime with direct plasma-surface contact on target plate
    ```
  - 文件 `terms/registry/aliases.tsv`：追加（含批次注释头）：
    ```
    # ==== Divertor physics expansion: parallel/cross-field cooling, attached regime, alias patches ====
    parallel cooling	parallel-cooling	en	preferred	preferred en (phrase)
    parallel-cooling	parallel-cooling	en	alias	IME token-only form
    平行冷却	parallel-cooling	zh	preferred	preferred zh
    并行冷却	parallel-cooling	zh	forbidden	误译parallel(非并行)：正确为 平行冷却
    并联冷却	parallel-cooling	zh	forbidden	误译parallel(非并联)：正确为 平行冷却
    cross-field cooling	cross-field-cooling	en	preferred	preferred en (phrase)
    cross-field-cooling	cross-field-cooling	en	alias	IME token-only form
    perpendicular cooling	cross-field-cooling	en	alias	synonym
    横向冷却	cross-field-cooling	zh	preferred	preferred zh
    垂直冷却	cross-field-cooling	zh	forbidden	误译perpendicular(非垂直)：正确为 横向冷却
    attached regime	attached-regime	en	preferred	preferred en (phrase)
    attached-regime	attached-regime	en	alias	IME token-only form
    贴靠模式	attached-regime	zh	preferred	preferred zh
    接触模式	attached-regime	zh	forbidden	误译attached：正确为 贴靠模式
    打击板	divertor-target	zh	forbidden	非标准：聚变应为 靶板/偏滤器靶板
    衰减长度	sol-width	zh	deprecated	笼统化：应为 SOL宽度/热流衰减宽度
    离靶	plasma-detachment	zh	deprecated	非标准：应为 脱靶
    ```
  - 文件 `terms/registry/evidence.tsv`：追加：
    ```
    parallel-cooling	internal:registry-gap-review:divertor-expansion	Heat removal along field lines in SOL/divertor	copilot	2026-04-13
    cross-field-cooling	internal:registry-gap-review:divertor-expansion	Heat removal across field lines in SOL/divertor	copilot	2026-04-13
    attached-regime	internal:registry-gap-review:divertor-expansion	Divertor regime with direct plasma contact (vs detachment)	copilot	2026-04-13
    ```
- **修改边界**：不得修改 `plasma-detachment`、`divertor-target`、`sol-width` 的 concept 行；不得修改 `parallel-heat-flux` 相关行
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - `grep -c "parallel-cooling\|cross-field-cooling\|attached-regime" terms/registry/concepts.tsv` — 输出 3
- **验收标准**：
  - ✅ 3 个新 concept 出现在 concepts.tsv，status=active
  - ✅ "并行冷却"和"并联冷却"为 parallel-cooling 的 forbidden
  - ✅ "垂直冷却"为 cross-field-cooling 的 forbidden
  - ✅ "接触模式"为 attached-regime 的 forbidden
  - ✅ "打击板"为 divertor-target 的 forbidden
  - ✅ "衰减长度"为 sol-width 的 deprecated
  - ✅ "离靶"为 plasma-detachment 的 deprecated
  - ✅ evidence.tsv 包含 3 条新行
- **潜在风险**：`parallel-cooling` 与已有 `parallel-heat-flux` 语义相近但不同（前者是冷却过程，后者是热流度量）——不构成冲突

### Phase 3: 充气/加料与粒子控制

#### ✅ Task 3.1: 补充 gas-puffing、pellet-injection、exhaust-processing、burn-fraction 的错误变体 aliases

- **目标**：为 4 个已有概念添加 forbidden/deprecated aliases 覆盖常见误译
- **修改内容**：
  - 文件 `terms/registry/aliases.tsv`：追加：
    ```
    # ==== Fuelling & particle control: forbidden/deprecated variant coverage ====
    注气	gas-puffing	zh	deprecated	非标准变体：应为 充气
    吹气	gas-puffing	zh	forbidden	误译gas puffing：正确为 充气
    冲气	gas-puffing	zh	forbidden	误译gas puffing：正确为 充气
    弹丸注射	pellet-injection	zh	forbidden	误译injection(注入非注射)：正确为 弹丸注入
    冰丸注射	pellet-injection	zh	forbidden	误译：正确为 弹丸注入
    冰丸注入	pellet-injection	zh	deprecated	非标准(冰丸→弹丸)：应为 弹丸注入
    尾气处理	tokamak-exhaust-processing-system	zh	alias	聚变氚循环短缩形式
    废气处理	tokamak-exhaust-processing-system	zh	forbidden	误译exhaust(环保义)：聚变应为 排气/尾气处理
    exhaust processing	tokamak-exhaust-processing-system	en	alias	generic short form
    燃耗率	burn-fraction	zh	forbidden	混淆burn fraction与burnup：正确为 燃烧份额
    ```
- **修改边界**：不得修改 concepts.tsv 或 evidence.tsv；仅 aliases.tsv 追加行
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - `grep "注气\|吹气\|冲气" terms/registry/aliases.tsv | wc -l` — 输出 3
- **验收标准**：
  - ✅ "注气"为 gas-puffing 的 deprecated
  - ✅ "吹气"和"冲气"为 gas-puffing 的 forbidden
  - ✅ "弹丸注射"和"冰丸注射"为 pellet-injection 的 forbidden
  - ✅ "冰丸注入"为 pellet-injection 的 deprecated
  - ✅ "尾气处理"为 tokamak-exhaust-processing-system 的 alias
  - ✅ "废气处理"为 tokamak-exhaust-processing-system 的 forbidden
  - ✅ "燃耗率"为 burn-fraction 的 forbidden
  - ✅ validate_registry 不因本 task 新增行报错
- **潜在风险**："尾气处理"是否会与未来"尾气"相关的独立 concept 冲突——当前无此 concept，风险低

### Phase 4: 壁调理/壁处理

#### Task 4.1: 修正 wall-conditioning、bakeout、lithium-coating preferred_zh

- **目标**：将 3 个 concept 的 preferred_zh 更新为领域标准译法
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：
    - 第 717 行 `wall-conditioning`：preferred_zh `壁面处理` → `壁调理`
    - 第 800 行 `bakeout`：preferred_zh `真空烘烤` → `烘烤除气`
    - 第 985 行 `lithium-coating`：preferred_zh `锂涂覆` → `锂化`
  - 文件 `terms/registry/aliases.tsv`：
    - 修改第 2514 行：`壁面处理	wall-conditioning	zh	preferred` → `壁面处理	wall-conditioning	zh	deprecated	非推荐：应为 壁调理`
    - 修改第 3244 行：comment "非标准：应为 壁面处理" → "非标准：应为 壁调理"
    - 修改第 4683 行：`壁处理	wall-conditioning	zh	alias	short form` → `壁处理	wall-conditioning	zh	deprecated	笼统化：应为 壁调理`
    - 修改第 2700 行：`真空烘烤	bakeout	zh	preferred` → `真空烘烤	bakeout	zh	alias	保留的替代表述`
    - 修改第 3440 行：comment "缺修饰：应为 真空烘烤" → "缺修饰：应为 烘烤除气"
    - 修改第 3098 行：`锂涂覆	lithium-coating	zh	preferred` → `锂涂覆	lithium-coating	zh	alias	原始preferred变体`
    - 修改第 4013 行：comment "应为 锂涂覆" → "应为 锂化"
    - 追加新 preferred + forbidden/deprecated alias 行：
    ```
    # ==== Wall conditioning: preferred_zh corrections + variant coverage ====
    壁调理	wall-conditioning	zh	preferred	preferred zh
    壁清洁	wall-conditioning	zh	forbidden	不规范：正确为 壁调理
    烘烤除气	bakeout	zh	preferred	preferred zh
    低温烘烤	bakeout	zh	deprecated	非标准：应为 烘烤除气
    bake-out	bakeout	en	alias	hyphenated variant
    锂化	lithium-coating	zh	preferred	preferred zh
    辉光清洗	glow-discharge-cleaning	zh	deprecated	缩略：应为 辉光放电清洗
    辉光放电清理	glow-discharge-cleaning	zh	deprecated	非标准：应为 辉光放电清洗
    硼涂覆	boronization	zh	deprecated	非标准：应为 硼化
    ```
- **修改边界**：不得修改 `glow-discharge-cleaning`、`boronization` 的 concept 行（preferred_zh 已正确）；不得修改 evidence.tsv
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - `grep "wall-conditioning" terms/registry/concepts.tsv` — preferred_zh 为"壁调理"
  - `grep "bakeout" terms/registry/concepts.tsv` — preferred_zh 为"烘烤除气"
  - `grep "lithium-coating" terms/registry/concepts.tsv` — preferred_zh 为"锂化"
- **验收标准**：
  - ✅ concepts.tsv 中 3 个 concept 的 preferred_zh 分别为"壁调理""烘烤除气""锂化"
  - ✅ "壁面处理""壁处理"降级为 deprecated（非 preferred）
  - ✅ "壁调理"为 wall-conditioning 唯一 zh preferred
  - ✅ "真空烘烤"降级为 alias（非 preferred），"烘烤除气"为唯一 zh preferred
  - ✅ "锂涂覆"降级为 alias，"锂化"为唯一 zh preferred
  - ✅ "壁清洁"为 forbidden，"低温烘烤"和"辉光清洗""辉光放电清理""硼涂覆"为 deprecated
  - ✅ 所有受影响 deprecated 行的 comment 引用新 preferred_zh
  - ✅ validate_registry 不因本 task 新增/修改行报错
- **潜在风险**：
  - `terminology_substitutions.tsv` 导出会将旧替换目标（如"壁泵送→壁面处理"）变为"壁泵送→壁调理"——属于预期行为
  - "壁调节"行（第 3244 行）的 comment 需同步更新，否则 comment 与实际 preferred_zh 不一致

#### Task 4.2: 新增 coating-degradation 概念

- **目标**：添加"涂层退化 (coating degradation)"概念及 aliases
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：追加：
    ```
    coating-degradation	concept	涂层退化	coating degradation		active	Gradual deterioration of wall conditioning coatings under plasma exposure
    ```
  - 文件 `terms/registry/aliases.tsv`：追加：
    ```
    # ==== Wall conditioning: coating-degradation ====
    coating degradation	coating-degradation	en	preferred	preferred en (phrase)
    coating-degradation	coating-degradation	en	alias	IME token-only form
    涂层退化	coating-degradation	zh	preferred	preferred zh
    涂层侵蚀	coating-degradation	zh	deprecated	非标准：应为 涂层退化
    ```
  - 文件 `terms/registry/evidence.tsv`：追加：
    ```
    coating-degradation	internal:registry-gap-review:wall-conditioning-expansion	Gradual deterioration of boronization/lithization coatings under plasma exposure	copilot	2026-04-13
    ```
- **修改边界**：不得修改任何已有行
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - `grep "coating-degradation" terms/registry/concepts.tsv` — 恰好 1 行
- **验收标准**：
  - ✅ `coating-degradation` 出现在 concepts.tsv，status=active
  - ✅ "涂层退化"为 zh preferred，"涂层侵蚀"为 deprecated
  - ✅ evidence.tsv 包含 coating-degradation 行
- **潜在风险**：无重大风险

### Phase 5: 加热与电流驱动

#### Task 5.1: 补充加热/电流驱动领域 forbidden/deprecated aliases

- **目标**：为 ECRH、NBI、RF heating、bootstrap current 添加常见错误变体 aliases
- **修改内容**：
  - 文件 `terms/registry/aliases.tsv`：追加：
    ```
    # ==== Heating & current drive: forbidden/deprecated variant coverage ====
    ECRH加热	electron-cyclotron-resonance-heating	zh	forbidden	冗余(ECRH已含heating)：正确为 电子回旋共振加热 或 ECRH
    中性束注入加热	neutral-beam-injection	zh	deprecated	冗余(注入已隐含加热)：应为 中性粒子束注入
    波加热	radio-frequency-heating	zh	deprecated	笼统化：应为 射频加热
    靴带电流	bootstrap-current	zh	forbidden	误译bootstrap(靴带→自举)：正确为 自举电流
    ```
- **修改边界**：不得修改 concepts.tsv 或 evidence.tsv；不得修改已有 alias 行
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - `grep "ECRH加热\|靴带电流\|波加热\|中性束注入加热" terms/registry/aliases.tsv | wc -l` — 输出 4
- **验收标准**：
  - ✅ "ECRH加热"为 electron-cyclotron-resonance-heating 的 forbidden
  - ✅ "中性束注入加热"为 neutral-beam-injection 的 deprecated
  - ✅ "波加热"为 radio-frequency-heating 的 deprecated
  - ✅ "靴带电流"为 bootstrap-current 的 forbidden
  - ✅ validate_registry 不因本 task 新增行报错
- **潜在风险**：无重大风险

### Phase 6: 标度律与约束模式

#### Task 6.1: 补充标度律/约束相关 deprecated/forbidden aliases

- **目标**：为 greenwald-density、h-factor、confinement-scaling、tau-e 添加常见变体 aliases
- **修改内容**：
  - 文件 `terms/registry/aliases.tsv`：追加：
    ```
    # ==== Scaling & confinement: variant alias coverage ====
    Greenwald极限	greenwald-density	zh	deprecated	混淆density与limit：应为 格林沃尔德密度
    Greenwald限制	greenwald-density	zh	deprecated	混淆density与limit：应为 格林沃尔德密度
    约束增强因子	h-factor	zh	alias	confinement enhancement factor 对应 zh
    约束改善因子	h-factor	zh	deprecated	非标准(改善→增强)：应为 H因子/约束增强因子
    增强因子	h-factor	zh	deprecated	缺修饰(约束)：应为 H因子/约束增强因子
    定标律	confinement-scaling	zh	deprecated	非标准：应为 标度律/约束标度律
    标度率	confinement-scaling	zh	forbidden	误译law(律≠率)：正确为 标度律
    约束时间	tau-e	zh	deprecated	歧义(缺'能量')：应为 能量约束时间
    ```
- **修改边界**：不得修改 concepts.tsv 或 evidence.tsv；不得修改已有 alias 行
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - `grep "Greenwald极限\|Greenwald限制\|约束增强因子\|定标律\|标度率\|约束时间" terms/registry/aliases.tsv | wc -l` — 输出不少于 6（可能有已存在的部分）
- **验收标准**：
  - ✅ "Greenwald极限"和"Greenwald限制"为 greenwald-density 的 deprecated
  - ✅ "约束增强因子"为 h-factor 的 alias，"约束改善因子"和"增强因子"为 deprecated
  - ✅ "定标律"为 confinement-scaling 的 deprecated，"标度率"为 forbidden
  - ✅ "约束时间"为 tau-e 的 deprecated
  - ✅ validate_registry 不因本 task 新增行报错
- **潜在风险**："约束时间"也可泛指粒子约束时间——此处 deprecated 指向 tau-e 是合理的，因为未加"粒子"修饰时默认指能量约束时间

### 时序推演

- **实施初期**（Phase 1-2）：核心变更集中在 concepts.tsv 新增 + aliases.tsv 行修改。关键决策点：Task 1.2 的 chemical-sputtering alias 迁移——若 validator 报 multi-concept 错误，需检查旧 alias 行的 concept_id 是否已正确修改。
- **实施中期**（Phase 3-4）：preferred_zh 变更是最敏感操作，涉及 concepts.tsv 行内修改和 aliases.tsv 多行 kind/comment 更新。潜在阻塞：若修改行定位错误（行号偏移），需回退并以内容匹配定位。
- **实施后期**（Phase 5-7）：纯追加操作，风险最低。验证阶段若发现问题需回溯到具体 Phase 修复。

### Phase 7: 验证与导出

#### Task 7.1: 全量验证 + 导出 + 测试

- **依赖**：Phase 1-6 全部完成
- **目标**：确保所有变更通过 registry 验证和单元测试
- **修改内容**：无文件修改，仅运行命令
- **修改边界**：不得修改任何文件
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry` — 记录输出（已知 `ABAQUS`/`B2`/`CENDL`/`CFX`/`CuCrZr`/`RAMI` IME 问题应仍存在且不变）
  - 运行 `python3 -m pipeline.export_registry --config config.toml` — 确认导出无新错误
  - 运行 `python3 -m pytest tests/ -x -q` — 确认全量测试通过
- **验收标准**：
  - ✅ validate_registry 输出与变更前仅差异在新增统计数字（concept/alias/evidence 计数增加）
  - ✅ export_registry 运行成功
  - ✅ pytest 全量通过（若有预存失败，确认非本变更引入）
- **潜在风险**：
  - `export_registry` 导出的 `terminology_substitutions.tsv` 会新增多个替换行（来自新 forbidden/deprecated alias）——属于预期行为
  - 若有测试硬编码了 alias 数量或特定 alias 指向，可能需要更新——发现后按实际修复

## 回归检查清单

- [ ] `python3 -m pipeline.validate_registry` 无新增错误（仅已知 IME allowlist 问题）
- [ ] `python3 -m pipeline.export_registry --config config.toml` 成功完成
- [ ] `python3 -m pytest tests/ -x -q` 全量通过
- [ ] `grep -c '^[^#]' terms/registry/concepts.tsv` 增加 8（从 1465 → 1473）
- [ ] `grep -c '^[^#]' terms/registry/aliases.tsv` 增加约 50 行
- [ ] `grep -c '^[^#]' terms/registry/evidence.tsv` 增加 8（从 1465 → 1473）
- [ ] 无 "maps to multiple concept_ids" 错误
- [ ] 新增 chemical-sputtering 后，"chemical sputtering" 和 "化学溅射" 唯一映射到 chemical-sputtering

## 审查日志

| 轮次 | 聚焦 | 发现问题数 | 已修正 | 剩余 |
|------|------|-----------|--------|------|
| R1 | 结构完整性 | 4 | 4 | 0 |
| R2 | 可执行性 | 5 | 5 | 0 |
| R3 | 风险与边缘 | 3 | 3 | 0 |
| **终止** | **T1 — 收敛终止（R3 issue=0）** | | | **0** |

### Completion Summary

| 维度 | 结果 |
|------|------|
| 背景与目标 | 完整 |
| 技术方案 | 完整 |
| Error & Rescue Map | 5 条路径已覆盖，0 CRITICAL GAP |
| 执行计划 | 7 Phase, 9 Task |
| 回归检查清单 | 8 项（含项目特定检查） |
| 已知局限 | 无 |

### R1 Issues
- **Issue R1-1**: Task 4.1 缺少 `壁调节` 行 comment 更新指令 → ✅ 已补充修改第 3244 行 comment 的指令
- **Issue R1-2**: 缺少 Error & Rescue Map → ✅ 已添加
- **Issue R1-3**: Task 1.3 缺少 `共堆积`（co-deposition alias）和 `扣留`（fuel-retention forbidden）条目 → ✅ 已添加到 Task 1.3
- **Issue R1-4**: Task 7.1 缺少回归检查清单中的数量变化断言 → ✅ 已添加到回归检查清单

### R2 Issues
- **Issue R2-1**: Task 1.2 修改 alias 398 行时需确认修改后的行格式完整（5 列 TSV）→ ✅ 已在 Task 1.2 修改指令中写出完整替换行
- **Issue R2-2**: Task 4.1 修改多达 7 行已有 alias + 追加 9 行 — 正好 alias 行涉及，仍在 ≤3 文件限制内但边界紧张 → ✅ 确认 Task 4.1 仅涉及 concepts.tsv + aliases.tsv = 2 文件
- **Issue R2-3**: Task 6.1 中"约束时间"若已存在于其他 concept alias 会触发 validator multi-concept 错误 → ✅ 已通过 grep 确认"约束时间"不存在于 aliases.tsv
- **Issue R2-4**: Task 1.2 执行顺序未明确——alias 修改前 concept 行必须已存在 → ✅ 已在 Task 1.2 添加执行顺序注意事项
- **Issue R2-5**: 缺少时序推演 section → ✅ 已在 Phase 7 前添加时序推演

### R3 Issues
- **Issue R3-1**: chemical-sputtering 从 sputtering 移走 "chemical sputtering" alias 后，sputtering concept 是否仍有足够 alias — 检查确认 sputtering 还有 "sputtering"(en preferred), "溅射"(zh preferred) → ✅ 无风险
- **Issue R3-2**: "bake-out" alias 追加到 bakeout 是否会与现有 en preferred "bakeout" 冲突 — 确认 validator 允许同 concept 多个 en alias → ✅ 无冲突
- **Issue R3-3**: Task 1.2 partial execution risk — 若 aliases.tsv 修改成功但 concepts.tsv 未追加，alias 指向非存在 concept → validator 报错。回滚策略：executor 应先追加 concept 行再修改 alias 行 → ✅ 已在 Task 1.2 添加执行顺序指令

## Pre-Delivery Audit (Level: L1-Lite)

| § | Check | Status | Note |
|---|-------|--------|------|
| 1 | Unit consistency | ✅ PASS | 纯术语/文本计划，不含数值参数 |
Auditor: Plan Architect | Date: 2026-04-13
