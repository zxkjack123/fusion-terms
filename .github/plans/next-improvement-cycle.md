# fusion-terms 下一轮开发改进计划

## 背景与目标

- **问题/需求描述**：fusion-terms 术语库已达 925 概念 / 4434 别名（v2026.03.23.7）。上一轮集中维护后存在以下待改进项：
  1. 版本元数据不同步：HEAD tag = v2026.03.23.7，CHANGELOG 最新条目 = v2026.03.23.6，release pack = v2026.03.23.5
  2. Review pack 有 831 新中文 + 1208 新英文候选词未审阅，且候选中噪声显著（前 10 条中文全为虚词"其中/例如/所示/此外…"，英文含 "general/made/measured/near" 等通用词）
  3. 111 个稀疏概念仍只有 ≤2 条正确别名
  4. Forbidden 覆盖率 92%（855/925），距 95% 还差约 28 个概念
  5. evidence.tsv 有 4 条 `internal:TODO` 占位符（tritium-retention, q95, beta-n, tau-e）
  6. Rime/fcitx 词库未同步到本地输入法

- **根因分析**：v2026.03.23.7 只做了 batch 脚本搬迁（代码组织优化），未更新 CHANGELOG 也未重建 release pack。候选词噪声源自提取时未传入 `--zh-stopwords` / `--en-stopwords` 参数。

- **目标**：
  1. 版本号 / CHANGELOG / release pack 三者对齐
  2. 建立中文停用词表，优化候选词过滤质量
  3. 完成一轮候选词审阅并通过 `apply_decisions` 批量纳入
  4. 稀疏概念充实至 ≤80 个
  5. Forbidden 覆盖率 ≥95%
  6. 清除 evidence.tsv 全部 TODO 占位
  7. Rime 输入法词库同步

- **非目标（不做什么）**：
  - 不新增或重构 pipeline 模块代码
  - 不扩充语料库（暂不添加新 Markdown 文件到 staging 目录）
  - 不修改 registry TSV 的 schema 格式

## 技术方案

- **方案概述**：分 5 个 Phase、14 个 Task 渐进执行。每个 Phase 完成后独立可用且可安全回滚到上一 Phase 结束时的 tag。
- **关键设计决策**：
  - 先对齐版本（Phase 1），建立干净基线
  - 先优化过滤（Phase 2）再审阅（Phase 3），避免人工浪费在噪声候选上
  - 审阅使用 `decisions.tsv` → `apply_decisions` 标准流程，保证 AUTO-INBOX 幂等写入
  - 每个 Phase 最后一个 Task 负责 commit + tag + push
- **影响范围**：
  - 会修改的 tracked 文件：`CHANGELOG.md`、`terms/stopwords_zh.txt`（新建）、`terms/stopwords_en.txt`、`terms/denylist.txt`、`terms/allowlist_en.txt`、`terms/allowlist_zh.txt`、`terms/synonyms.tsv`、`terms/registry/aliases.tsv`、`terms/registry/evidence.tsv`
  - 会生成的 gitignored 产物：`artifacts/` 下候选/review_pack 文件、`dist/` 下 release 包
  - **不会修改**：`pipeline/*.py`、`tests/*.py`、`terms/registry/concepts.tsv`

## 执行计划

### Phase 1: 版本对齐

#### ✅ Task 1.1: CHANGELOG 补齐 + commit

- **目标**：在 CHANGELOG.md 中补写 v2026.03.23.7 条目并 commit，为后续 release pack 提供正确的 HEAD SHA
- **修改内容**：
  - 文件 `CHANGELOG.md`：
    - 将 `## Unreleased` 下方、`## v2026.03.23.6` 上方插入 `## v2026.03.23.7` section
    - 内容：`### Changed` → "Batch 脚本归档：25 个 `_batch*.py` 脚本搬迁到 `scripts/batches/` 目录"
    - `## Unreleased` 下三个子标题（Added/Changed/Fixed）保持为空
  - 运行 `git add CHANGELOG.md && git commit -m "docs: add v2026.03.23.7 changelog entry"`
- **修改边界**：不得修改 `CHANGELOG.md` 中 `## v2026.03.23.6` 及更早的条目；不得修改任何其他文件
- **测试要求**：
  - 运行 `python -m compileall pipeline tests && python -m pytest tests/ -q`
  - 预期输出：`60 passed`
- **验收标准**：
  - ✅ `## v2026.03.23.7` section 存在于 `## Unreleased` 与 `## v2026.03.23.6` 之间
  - ✅ `## Unreleased` 下三个子标题均无内容
  - ✅ `git log --oneline -1` 显示 changelog commit
- **潜在风险**：措辞不准确不影响功能，可通过后续 `commit --amend` 修正

#### ✅ Task 1.2: 重建 release pack

- **目标**：基于当前 registry (925 concepts, 4434 aliases) 构建与最新代码匹配的 release pack 并验证合约
- **修改内容**：
  - 运行 `python3 -m pipeline.build_terms --config config.toml`（重建 domain_terms.txt）
  - 运行 `python3 -m pipeline.release_pack --tag v2026.03.23.8 --config config.toml`
  - 运行 `python3 -m pipeline.verify_release_contract --root dist/stage/v2026.03.23.8`
- **修改边界**：不得修改 `pipeline/*.py` 源代码；不得删除 `dist/` 下已有包和 staging 目录
- **测试要求**：
  - 运行 `python3 -m pipeline.verify_release_contract --root dist/stage/v2026.03.23.8`
  - 预期输出：`contract OK: ...` 且 `total` ≥ 2496
- **验收标准**：
  - ✅ `dist/fusion-terms-artifacts-v2026.03.23.8.tar.gz` 存在
  - ✅ `verify_release_contract` 返回 exit code 0
  - ✅ manifest.json 中 `counts.total` ≥ 2496
- **潜在风险**：如 allowlist/denylist 有变化（本 Phase 内不应有），term count 可能偏离预期。build_terms 输出与 v2026.03.23.5 的 2496 应一致。

#### ✅ Task 1.3: Tag + Push

- **目标**：打上 v2026.03.23.8 tag 并推送到 origin，完成版本对齐
- **修改内容**：
  - `git tag v2026.03.23.8`
  - `git push origin master --tags`
- **修改边界**：不 commit 新内容（Task 1.1 已 commit）；不修改任何文件
- **测试要求**：
  - `git log --oneline -3` 包含 Task 1.1 的 commit
  - `git tag -l 'v2026.03.23.8'` 输出该 tag
  - `git log origin/master --oneline -1` 与本地 HEAD 一致
- **验收标准**：
  - ✅ v2026.03.23.8 tag 存在于本地和 origin
  - ✅ `git status` 干净
  - ✅ `origin/master` 与本地 `master` 同步
- **潜在风险**：SSH 连接到 GitHub 偶有超时（尤其从国内网络），如超时可重试

---

### Phase 2: 候选词过滤优化

**前置依赖**：Phase 1 完成

#### ✅ Task 2.1: 创建中文停用词表

- **目标**：创建 `terms/stopwords_zh.txt`，收录从 review pack 中文候选识别出的高频虚词/通用词
- **修改内容**：
  - 新建文件 `terms/stopwords_zh.txt`，格式与 `stopwords_en.txt` 一致（每行一个词，`#` 注释，空行忽略）
  - 添加从 `artifacts/review_pack/new_candidates_zh.filtered.tsv` 前 100 行识别出的非术语中文词
  - 典型候选（依据当前 review pack 数据）：其中、例如、所示、此外、所以、因此、但是、得到、如图、可以、然后、其他、以及、进行、之间、目前、采用、主要、通过、需要、利用、结果、方法、分析、条件、过程、实现、提高、影响、研究
- **修改边界**：不得修改 `terms/stopwords_en.txt`（本 Task 仅处理中文）；不得修改 `pipeline/*.py`；不得修改 `terms/denylist.txt`
- **测试要求**：
  - 运行 `python -m pytest tests/ -q`
  - 预期输出：`60 passed`（停用词文件变化不影响任何测试）
  - 逐词验证：停用词列表中无任何 `terms/registry/aliases.tsv` 中 `kind=preferred` 且 `lang=zh` 的值
- **验收标准**：
  - ✅ `terms/stopwords_zh.txt` 存在，包含 ≥25 个中文虚词/通用词
  - ✅ 文件首部有注释说明用途
  - ✅ 与 registry preferred_zh 无交集
- **潜在风险**：部分动词如"分析/影响/研究"在特定上下文可能是术语成分。应仅添加在核聚变领域明确无术语含义的虚词。如有疑问，宁可不加。

#### Task 2.2: 扩充英文停用词和 denylist

- **目标**：扩充 `terms/stopwords_en.txt` 和 `terms/denylist.txt`，过滤英文候选中的常见非术语词
- **修改内容**：
  - 文件 `terms/stopwords_en.txt`：从 `artifacts/review_pack/new_candidates_en.filtered.tsv` 前 100 行识别并添加常见英语词
  - 典型候选：general, made, measured, near, present, provided, based, found, given, observed, obtained, described, considered, determined, known, shown, compared, related, recently, reported, discussed, performed, proposed, used, applied, developed, studied, during, between, within, through, along, around, about, using
  - 文件 `terms/denylist.txt`：添加明确的英文噪声词（如 PDF 处理残留 artifacts）
- **修改边界**：不得修改 `pipeline/*.py`；不得修改 `terms/stopwords_zh.txt`（由 Task 2.1 负责）
- **测试要求**：
  - 运行 `python -m pytest tests/ -q`
  - 预期输出：`60 passed`
  - 交叉验证：新增停用词与 `terms/registry/aliases.tsv` 中 `kind=preferred` 且 `lang=en` 的值无交集
- **验收标准**：
  - ✅ `terms/stopwords_en.txt` 新增 ≥25 个英文停用词
  - ✅ `terms/denylist.txt` 如有新增，每条都是明确的噪声
  - ✅ 与 registry preferred_en 无交集
- **潜在风险**：像 "near" 可能出现在术语短语中 "near-field"，但 stopwords 只做完全匹配，不影响短语内组成词。单独的 "near" 出现在候选中确为噪声。

#### Task 2.3: 重新提取候选词并更新 review pack

- **目标**：传入新的停用词重新提取候选词，更新 review pack，验证噪声显著减少
- **修改内容**：
  - 运行：
    ```bash
    python3 -m pipeline.extract_candidates \
      --source-root /home/gw/ComputeData/pdf2md/ZoteroIngest/staging \
      --min-count-zh 3 --min-count-en 5 \
      --topk-zh 2000 --topk-en 2000 \
      --zh-stopwords terms/stopwords_zh.txt \
      --en-stopwords terms/stopwords_en.txt \
      --config config.toml
    ```
  - 运行 `python3 -m pipeline.review_pack --exclude-known-terms`
- **修改边界**：不得修改 `pipeline/*.py`；不得修改 `terms/registry/` 下任何文件；只更新 gitignored 产物
- **测试要求**：
  - 检查 `artifacts/review_pack/summary.json`：`new_zh` < 800，`new_en` < 1100
  - 检查 `head -5 artifacts/review_pack/new_candidates_zh.filtered.tsv`：前 5 条中不含"其中"、"例如"、"所示"等虚词
  - 检查 `head -5 artifacts/review_pack/new_candidates_en.filtered.tsv`：前 5 条中不含 "general"、"made"、"measured" 等通用词
- **验收标准**：
  - ✅ `new_zh` < 800（至少减少 30 条噪声）
  - ✅ `new_en` < 1100（至少减少 100 条噪声）
  - ✅ 中文候选前 10 行不含此前识别出的虚词
  - ✅ 英文候选前 10 行不含此前识别出的通用词
- **潜在风险**：如停用词过于激进，有效候选可能被误删。可通过对比 .filtered.tsv 与无停用词版本的差集来检查是否有误删的领域术语。

#### Task 2.4: Phase 2 commit + tag

- **目标**：提交停用词文件变更并打 tag
- **修改内容**：
  - 更新 `CHANGELOG.md`：在 Unreleased 下记录停用词新增
  - `git add terms/stopwords_zh.txt terms/stopwords_en.txt terms/denylist.txt CHANGELOG.md`
  - `git commit -m "terms: add zh stopwords, expand en stopwords/denylist for candidate filtering"`
  - `git tag vYYYY.MM.DD.N`（依据当天日期）
  - `git push origin master --tags`
- **修改边界**：仅提交本 Phase 变更的文件
- **测试要求**：
  - `python -m pytest tests/ -q` → `60 passed`
  - `git status` → 干净
- **验收标准**：
  - ✅ 新 tag 存在于 origin
  - ✅ CHANGELOG 记录了停用词变更
- **潜在风险**：SSH push 超时可重试

---

### Phase 3: 候选词审阅与纳入

**前置依赖**：Phase 2 完成（review pack 已更新且噪声已大幅减少）

#### Task 3.1: 创建 decisions.tsv — 审阅中文候选

- **目标**：从更新后的 review pack 中文候选中筛选应纳入的词条，创建 decisions.tsv
- **修改内容**：
  - 人工或半自动审阅 `artifacts/review_pack/new_candidates_zh.filtered.tsv`
  - 创建 `artifacts/review_pack/decisions.tsv`（UTF-8，tab 分隔），格式：
    ```
    # action	value	preferred	lang	comment
    allow_zh	聚变堆		
    deny	所示		
    synonym	氚增殖	tritium-breeding	zh
    ```
  - 允许的 action：`allow_zh`（纳入中文允许列表）、`deny`（加入黑名单）、`synonym`（建立同义映射）
  - 审阅策略：
    - count ≥10 且为核聚变/核工程领域术语 → `allow_zh`
    - 明显的虚词/通用词（漏过停用词的） → `deny`
    - 与 registry 中已有概念同义的 → `synonym`（preferred 必须存在于 registry 或 allowlist）
- **修改边界**：不得直接修改 `terms/` 下的任何列表文件（由 Task 3.3 的 `apply_decisions` 统一写入）
- **测试要求**：
  - 运行 dry-run：`python3 -m pipeline.apply_decisions --terms-dir terms --decisions artifacts/review_pack/decisions.tsv`
  - 预期输出：exit code 0，无 error/conflict 报告
- **验收标准**：
  - ✅ `decisions.tsv` 包含 ≥30 条中文决策（allow_zh + deny + synonym 合计）
  - ✅ dry-run 退出码 0，无 error
  - ✅ 每个 `synonym` 行的 preferred 值在 registry aliases.tsv 或 allowlist 中存在
- **潜在风险**：synonym 目标词不在 registry 中会被 apply_decisions 拒绝。需在写入 decisions.tsv 前验证 preferred 值的存在性。

#### Task 3.2: 追加 decisions.tsv — 审阅英文候选

- **目标**：从 review pack 英文候选中筛选应纳入的词条，追加到 decisions.tsv
- **修改内容**：
  - 审阅 `artifacts/review_pack/new_candidates_en.filtered.tsv`
  - 向 `artifacts/review_pack/decisions.tsv` 追加英文决策行（`allow_en`、`deny`、`synonym`）
  - 审阅策略同 Task 3.1，语言换为英文
- **修改边界**：不得修改 decisions.tsv 中已有的中文决策行（仅追加）；不得直接修改 `terms/` 文件
- **测试要求**：
  - 运行 dry-run：`python3 -m pipeline.apply_decisions --terms-dir terms --decisions artifacts/review_pack/decisions.tsv`
  - 预期输出：exit code 0，无 error/conflict
- **验收标准**：
  - ✅ decisions.tsv 总行数（含注释行）≥60（中英合计有效决策 ≥50）
  - ✅ dry-run 退出码 0
  - ✅ 无跨决策冲突（同一 value 不同时出现在 allow 和 deny 中）
- **潜在风险**：英文候选中可能存在与 `allowlist_en.txt` 已有项的重复，apply_decisions 会自动跳过已存在项，不会报错

#### Task 3.3: 应用决策并 commit

- **目标**：使用 `apply_decisions --apply` 将审阅决策持久化到 `terms/` 下的列表文件，并 commit
- **修改内容**：
  - 运行 `python3 -m pipeline.apply_decisions --terms-dir terms --decisions artifacts/review_pack/decisions.tsv --apply`
  - 以下文件的 `# --- AUTO-INBOX` 区块将被更新（如对应 action 存在）：
    - `terms/allowlist_en.txt`
    - `terms/allowlist_zh.txt`
    - `terms/denylist.txt`
    - `terms/synonyms.tsv`
  - 更新 `CHANGELOG.md`
  - `git add terms/ CHANGELOG.md && git commit -m "terms: apply review decisions (allow/deny/synonym)"`
  - `git tag vYYYY.MM.DD.N && git push origin master --tags`
- **修改边界**：不得修改 `# --- AUTO-INBOX` 标记以上的手动维护内容；不得修改 `terms/registry/` 下任何文件
- **测试要求**：
  - 运行 `python -m pytest tests/ -q` → `60 passed`
  - 运行二次 dry-run：`python3 -m pipeline.apply_decisions --terms-dir terms --decisions artifacts/review_pack/decisions.tsv`
  - 预期输出：所有 new addition counts 为 0（幂等验证）
- **验收标准**：
  - ✅ `--apply` 退出码 0
  - ✅ 二次 dry-run 显示 0 new additions（幂等）
  - ✅ 全量测试通过
  - ✅ `terms/allowlist_zh.txt` 包含 AUTO-INBOX 区块（如有 `allow_zh` 决策）
  - ✅ 新 tag 已推送到 origin
- **潜在风险**：如 Task 3.1/3.2 中有 synonym 冲突未被 dry-run 捕获，`--apply` 会报错终止。此时需回到 decisions.tsv 修正冲突行后重试。

---

### Phase 4: Registry 质量提升

**前置依赖**：Phase 3 完成（allowlist/denylist 已更新）

#### Task 4.1: 稀疏概念第二轮充实

- **目标**：为 ≥30 个稀疏概念（≤2 正确别名，排除纯代号 code 类）补充正确别名，将稀疏概念数降至 ≤80
- **修改内容**：
  - 文件 `terms/registry/aliases.tsv`：为选定概念添加正确别名行（alias/preferred kind）
  - 可选：新建脚本 `scripts/batches/_batch55_enrichment.py` 用于批量写入
  - 别名来源：中文简称/变体/全称、英文 synonym/plural/abbreviation
- **修改边界**：不得修改 `terms/registry/concepts.tsv`（不新增概念）；不得修改 `terms/registry/evidence.tsv`；不得修改 `pipeline/*.py`
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：`OK: 925 concepts, ≥4464 aliases, 925 evidence`
  - 运行 `python -m pytest tests/ -q` → `60 passed`
  - 冲突预检：新别名与全库现有别名交叉检查，确认无跨概念冲突
- **验收标准**：
  - ✅ 稀疏概念数 ≤ 80（当前 111，需消解 ≥31）
  - ✅ `validate_registry` 通过
  - ✅ 无跨概念别名冲突
  - ✅ 全量测试通过
- **潜在风险**：新别名可能与现有别名在其他概念下冲突。必须用 pre-flight 脚本逐条检查 `aliases.tsv` 中是否已有同文本指向不同 `concept_id` 的记录。

#### Task 4.2: Forbidden 覆盖率提升至 ≥95%

- **目标**：为 ≥28 个无 forbidden/deprecated 别名的概念补充错误形式别名，覆盖率达 ≥95%
- **前置依赖**：Task 4.1 完成（两个 Task 均修改 `aliases.tsv`，必须顺序执行避免冲突）
- **修改内容**：
  - 文件 `terms/registry/aliases.tsv`：为选定概念添加 `kind=forbidden` 或 `kind=deprecated` 别名行
  - 可选：新建脚本 `scripts/batches/_batch_f11_forbidden.py`
  - 典型错误形式来源：AI 翻译典型误译、易混淆的近似中文译名、过时缩写
- **修改边界**：不得修改 `terms/registry/concepts.tsv`；不得修改 `terms/registry/evidence.tsv`；不得修改 `pipeline/*.py`
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry` → OK
  - 运行 `python -m pytest tests/ -q` → `60 passed`
  - 计算覆盖率：`≥879 / 925 = 95%`
- **验收标准**：
  - ✅ Forbidden 覆盖率 ≥ 95%（≥879/925 概念有 forbidden 或 deprecated 别名）
  - ✅ `validate_registry` 通过
  - ✅ 全量测试通过
- **潜在风险**：部分纯代号概念（如 code 类 best、cfr 等）不存在有意义的 AI 误译形式，可跳过并计入"不适用"名单。需在实施时记录跳过原因。

#### Task 4.3: Phase 4 commit + tag

- **目标**：提交 registry 充实和 forbidden 覆盖变更
- **修改内容**：
  - 更新 `CHANGELOG.md`
  - `git add terms/registry/aliases.tsv scripts/batches/ CHANGELOG.md`
  - `git commit -m "registry: sparse enrichment + forbidden coverage ≥95%"`
  - `git tag vYYYY.MM.DD.N && git push origin master --tags`
- **修改边界**：仅提交 Phase 4 变更
- **测试要求**：
  - `python -m pytest tests/ -q` → `60 passed`
  - `git status` → 干净
- **验收标准**：
  - ✅ CHANGELOG 记录稀疏充实和 forbidden 覆盖变更
  - ✅ 新 tag 存在于 origin
- **潜在风险**：如 aliases.tsv 体积较大导致 diff 不易审阅，可在 commit message 中附上统计摘要

---

### Phase 5: 收尾与同步

**前置依赖**：Phase 4 完成

#### Task 5.1: evidence.tsv TODO 占位符清理

- **目标**：替换 evidence.tsv 中 4 条 `internal:TODO` 占位符为实际文献来源
- **修改内容**：
  - 文件 `terms/registry/evidence.tsv`：修改以下 4 行的 `source` 列
    - `tritium-retention`：将 `internal:TODO:add-paper-or-standard` 替换为权威来源（如 IAEA Nuclear Fusion 综述 DOI、或 Wikipedia URL）
    - `q95`：将 `internal:TODO:add-definition-source` 替换为等离子体物理教材/标准来源
    - `beta-n`：将 `internal:TODO:add-definition-source` 替换为定义来源
    - `tau-e`：将 `internal:TODO:add-definition-source` 替换为定义来源
- **修改边界**：仅修改这 4 行的 `source` 列；不得修改 evidence.tsv 的其他行；不得修改其他文件
- **测试要求**：
  - `grep "internal:TODO" terms/registry/evidence.tsv | wc -l` → 输出 `0`
  - `python3 -m pipeline.validate_registry` → OK
  - `python -m pytest tests/ -q` → `60 passed`
- **验收标准**：
  - ✅ evidence.tsv 不含任何 `internal:TODO` 字符串
  - ✅ 4 个替换来源均为合法的 DOI（如 `https://doi.org/10.xxx`）、URL、或标准编号
  - ✅ `validate_registry` 通过
- **潜在风险**：需人工查找正确的文献来源。如暂时无法找到权威论文 DOI，可用 Wikipedia 物理词条 URL 作为过渡（如 `https://en.wikipedia.org/wiki/Safety_factor_(plasma_physics)`）。

#### Task 5.2: Rime/fcitx 词库同步

- **目标**：将当前 domain_terms.txt 同步到本地 Rime 输入法
- **修改内容**：
  - 先重建 domain_terms：`python3 -m pipeline.build_terms --config config.toml`
  - 运行同步：
    ```bash
    python3 -m pipeline.rime_import_safe --import \
      --backup-path ~/.local/share/fcitx5/rime \
      --backup-path ~/.config/fcitx5/rime
    ```
    （根据实际 fcitx 安装路径调整 `--backup-path`）
- **修改边界**：不得修改 `pipeline/*.py`；仅影响用户 home 目录下的 Rime 配置文件（会自动备份到 `artifacts/rime_backups/`）
- **测试要求**：
  - 检查 `artifacts/.rime_import_rime_ice.txt` 存在且行数 ≥ 1676
  - 检查 `ls artifacts/rime_backups/` 有新的备份目录
  - 重启输入法后输入"等离子体"等术语能触发候选
- **验收标准**：
  - ✅ `rime_import_safe` 退出码 0
  - ✅ Rime 备份已生成
  - ✅ fcitx5 重新部署后输入法正常工作
- **潜在风险**：Rime 词库格式不兼容可能导致部署失败。`rime_import_safe` 有备份机制，可通过还原 `artifacts/rime_backups/` 中的备份回滚。

#### Task 5.3: 最终 release pack + tag

- **目标**：构建包含所有改进的最终 release pack 并推送
- **修改内容**：
  - 更新 `CHANGELOG.md`：汇总 Phase 5 内容（evidence 清理 + Rime 同步说明）
  - `git add terms/registry/evidence.tsv CHANGELOG.md && git commit -m "registry: clear evidence TODO placeholders"`
  - 运行 `python3 -m pipeline.build_terms --config config.toml`
  - 运行 `python3 -m pipeline.release_pack --tag vYYYY.MM.DD.N --config config.toml`
  - `python3 -m pipeline.verify_release_contract --root dist/stage/vYYYY.MM.DD.N`
  - `git tag vYYYY.MM.DD.N && git push origin master --tags`
- **修改边界**：仅 commit Phase 5 变更文件
- **测试要求**：
  - `python -m pytest tests/ -q` → `60 passed`
  - `verify_release_contract` → exit code 0
  - `git status` → 干净
- **验收标准**：
  - ✅ CHANGELOG 最新条目与 HEAD tag 一致
  - ✅ dist/ 最新 tarball 与 HEAD tag 一致
  - ✅ Release pack 合约验证通过
  - ✅ 所有变更已推送到 origin
  - ✅ `git status` 干净
- **潜在风险**：最终 release pack 的 term count 可能因 Phase 3 的 allow/deny 决策而与 Phase 1 的 2496 有偏差。如 count 变化剧烈需检查 decisions 是否引入了异常。

---

## 回归检查清单

- [ ] 全量测试通过：`python -m pytest tests/ -q`（≥60 passed）
- [ ] Registry 验证通过：`python3 -m pipeline.validate_registry`（925 concepts, ≥4434 aliases, 925 evidence）
- [ ] Release 合约通过：`python3 -m pipeline.verify_release_contract --root dist/stage/<latest>`（exit code 0）
- [ ] 无新增 lint 警告：`python -m ruff check pipeline/ tests/`
- [ ] CHANGELOG.md 最新条目与 HEAD tag 一致
- [ ] dist/ 下最新 tarball 版本号与 HEAD tag 一致
- [ ] `terms/registry/evidence.tsv` 无 `internal:TODO` 占位
- [ ] Forbidden 覆盖率 ≥ 95%（≥879/925 concepts）
- [ ] 稀疏概念数 ≤ 80
- [ ] `terms/stopwords_zh.txt` 存在且内容与 registry preferred_zh 无交集
- [ ] `git status` 干净，local master 与 origin/master 同步

## 审查日志

| 轮次 | 聚焦 | 发现问题数 | 已修正 | 剩余 |
|------|------|-----------|--------|------|
| R1 | 结构完整性 | 0 | 0 | 0 |
| R2 | 可执行性 | 1 | 1 | 0 |
| R3 | 风险与边缘 | 2 | 2 | 0 |
| **终止** | **T1 — 收敛终止** | | | **0** |

### R2 Issues
- **Issue R2-1**: Task 1.2（release pack）原先排在 CHANGELOG commit 之前，导致 manifest 中的 commit SHA 不是最终 tag 对应的 commit。→ 将 git commit 合并到 Task 1.1，确保 Task 1.2 在 commit 之后运行，manifest SHA 正确。 ✅ 已修正

### R3 Issues
- **Issue R3-1**: Task 4.1 和 4.2 均修改 `aliases.tsv` 但未声明顺序依赖，可能导致并行执行冲突。→ 在 Task 4.2 前置依赖中明确标注"Task 4.1 完成后方可执行"。 ✅ 已修正
- **Issue R3-2**: 需验证 `extract_candidates.py` 是否支持 `--zh-stopwords` 参数。→ 已验证：argparse 定义了 `--zh-stopwords` 参数，加载逻辑与 `--en-stopwords` 对称，用于过滤 `.filtered.tsv` 输出。方案无需调整。 ✅ 已确认
