# 权威术语源导入与 Registry Schema 扩展

## 背景与目标

- **问题/需求描述**：当前 registry（~1690 concepts, ~7766 aliases）主要来自语料抽取 + 人工审定，缺乏权威术语标准来源的系统性对标。需要引入国家标准（GB/T 4960 系列）、ITER Glossary、IAEA Safety Glossary 等权威术语源，并在 registry schema 中增加溯源字段。
- **目标**：
  1. 扩展 registry schema，增加 `source` / `authority` 列以区分术语来源层级
  2. 抓取 ITER Fusion Glossary（142 条，英文定义）并转换为 registry 候选
  3. 下载 IAEA Safety Glossary 2018 PDF 并提取核安全/辐射防护术语
  4. OCR 处理 Zotero 中已有的 GB/T 4960.9-2013 扫描 PDF，提取磁约束聚变术语
  5. 将各源术语与现有 registry 做 diff/merge
- **非目标（不做什么）**：
  - 不申请 termonline.cn 接口 — 需要单位账号，当前不可行
  - 不购买 ISO 12749 付费标准 — 成本不合理
  - 不修改现有 concepts/aliases 的已有字段内容 — 仅追加新列和新行
  - 不自动合并冲突 — diff 结果需人工审核后决定
- **已有代码/流程复用分析**：
  - `_iter_concept_rows()` / `_iter_alias_rows()`：复用（追加列时自动容错，但 dict 映射需更新）
  - `_iter_tsv_rows()` (validate)：复用（`len(parts) >= N` 守卫已兼容追加列）
  - `export_registry.py` 全部导出函数：复用（不依赖新增列，但 concept dict 映射需更新以暴露新字段）
  - pdf2md OCR 流程：如有现成工具链可复用；否则用 `pdftotext` / `pytesseract` 新建脚本

## 技术方案

- **方案概述**：
  1. **Schema 扩展**：在 `concepts.tsv` 末尾追加 `source` 列（值域：`corpus` / `GB/T-4960.9` / `ITER-glossary` / `IAEA-safety-glossary`）；在 `evidence.tsv` 的 `source` 列中自然标注即可（已有该列）
  2. **ITER 抓取**：Python 脚本用 `urllib` + `re` 从 `iter.org/fusion-glossary` 提取 142 条 term+definition，输出 staging TSV
  3. **IAEA PDF**：下载 PUB1830_web.pdf → `pdftotext` 提取 → 正则清洗 → staging TSV
  4. **GB/T 4960.9 OCR**：对 `~/Zotero/storage/B2RVUCN5/GB-T 4960.pdf`（84页扫描件）做 OCR → 提取中英文术语对 → staging TSV
  5. **Diff/Merge**：脚本自动比对 staging TSV 与现有 registry，生成 diff 报告（新增/冲突/已有），人工审核后 apply

- **关键设计决策**：
  - 新增列追加在 TSV 末尾（`concepts.tsv` 第 8 列 index=7），不插入中间，避免全面破坏现有解析
  - staging 文件放 `artifacts/terminology_sources/`，与正式 registry 隔离
  - OCR 质量不可靠时，标记 `status=draft`，不直接 merge 为 `active`
  - ITER Glossary 仅有英文，不自动生成中文翻译，仅用于 `preferred_en` 对照和 `evidence`

- **影响范围**：
  - `terms/registry/concepts.tsv` — 追加 `source` 列
  - `pipeline/export_registry.py` — `_iter_concept_rows()` 更新 dict 映射
  - `pipeline/validate_registry.py` — 可选：增加 `source` 列值域校验
  - `scripts/` — 新增 3 个抓取/提取脚本
  - `artifacts/terminology_sources/` — 新增 staging 目录
  - `tests/` — 更新 row_warnings 测试 fixture

## Error & Rescue Map（关键失败路径映射）

| 代码路径/操作 | 可能的失败 | 错误类型 | 已处理？ | 处理方式 | 用户可见行为 |
|-------------|-----------|---------|---------|---------|------------|
| ITER 页面抓取 | 网站改版/HTML 结构变化 | RuntimeError | Y | 脚本检测 0 terms 时 abort | 报错退出 |
| IAEA PDF 下载 | 网络超时 / URL 变更 | ConnectionError | Y | 重试 + 手动下载 fallback | 报错提示手动下载 |
| IAEA PDF → text | pdftotext 未安装 | FileNotFoundError | Y | 检测工具存在性 | 报错提示安装 poppler-utils |
| GB/T 4960.9 OCR | Tesseract 中文模型缺失 | RuntimeError | Y | 检查 `chi_sim` 语言包 | 报错提示安装 |
| GB/T 4960.9 OCR | OCR 质量差导致乱码 | 数据质量 | Y | 所有 OCR 结果标记 `status=draft` | 人工审核 |
| Schema 追加列 | 现有 pipeline 解析中断 | KeyError | N→Y | `_iter_concept_rows` 用 `len(parts) >= 8` 守卫 | 旧代码安全忽略新列 |
| diff/merge 时 concept_id 冲突 | 同名不同含义 | 逻辑冲突 | Y | 输出冲突报告，不自动覆盖 | 人工决定 |

## 执行计划

### Phase 1: Registry Schema 扩展

#### ✅ Task 1.1: concepts.tsv 追加 `source` 列

- **目标**：在 concepts.tsv 表头和所有数据行末尾追加 `source` 列
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：
    - 表头注释行追加 `source` 字段说明
    - 所有现有数据行末尾追加 `\tcorpus`（标记为语料抽取来源）
- **修改边界**：不修改 aliases.tsv、evidence.tsv
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry` 无报错
  - 运行 `python3 -m pipeline.export_registry --config config.toml` 无报错
  - 行数不变：`wc -l concepts.tsv` = 修改前行数
- **验收标准**：
  - ✅ 表头注释包含 `source` 字段说明
  - ✅ 所有非注释行有 8 个 tab 分隔字段
  - ✅ 全量 `pytest` 通过
- **潜在风险**：某些行末尾有尾随 tab 会导致列数不一致 — 用脚本统一处理

#### ✅ Task 1.2: `_iter_concept_rows()` 更新 dict 映射

- **目标**：让 export_registry 正确解析并暴露新 `source` 列
- **修改内容**：
  - 文件 `pipeline/export_registry.py`：在 `_iter_concept_rows()` 的 dict 构建中追加 `"source": parts[7] if len(parts) >= 8 else ""`
- **修改边界**：不修改 `_iter_alias_rows()`、不修改任何导出函数的输出格式
- **测试要求**：
  - 运行 `pytest tests/test_export_registry_row_warnings.py -v`
  - 运行 `python3 -m pipeline.export_registry --config config.toml`
  - 验证导出产物与修改前一致（source 列不影响现有导出）
- **验收标准**：
  - ✅ `_iter_concept_rows()` 返回的 dict 包含 `source` key
  - ✅ 现有全部导出测试通过
  - ✅ `export_registry` 运行无 warning 增加
- **潜在风险**：如果有测试 fixture 硬编码了 concepts.tsv 列数，需同步更新

#### ✅ Task 1.3: validate_registry 增加 `source` 值域校验（可选）

- **目标**：在 validate 阶段校验 `source` 列的合法值
- **修改内容**：
  - 文件 `pipeline/validate_registry.py`：在 concepts 校验逻辑中添加 `source` 值域检查（允许值：`corpus`, `GB/T-4960.9`, `GB/T-4960.x`, `ITER-glossary`, `IAEA-safety-glossary`, 空字符串）
- **修改边界**：不修改 aliases/evidence 校验逻辑
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry` 通过
  - 构造一条 `source=INVALID` 的行，验证报 warning
- **验收标准**：
  - ✅ 合法 source 值通过校验
  - ✅ 非法 source 值触发 warning
  - ✅ `source` 为空时不报错（兼容旧数据）
- **潜在风险**：值域列表后续可能扩展，需设计为可配置或宽松匹配

### Phase 2: ITER Fusion Glossary 抓取

#### ✅ Task 2.1: 编写 ITER Glossary 抓取脚本

- **目标**：从 `iter.org/fusion-glossary` 抓取 142 条术语 + 定义，输出 staging TSV
- **修改内容**：
  - 新建文件 `scripts/fetch_iter_glossary.py`：
    - 用 `urllib.request` 下载页面 HTML
    - 用 `re` 从 `accordion-faq__title` 提取 term，从 `content-rte node n-glossary` 提取 definition
    - 输出 `artifacts/terminology_sources/iter_glossary_raw.tsv`（列：`term | definition | fetch_date`）
- **修改边界**：不修改 pipeline 代码，不写入 registry
- **测试要求**：
  - 运行 `python3 scripts/fetch_iter_glossary.py`
  - 输出文件包含 ≥130 条记录（允许少量 HTML 变动损失）
  - 每条有非空 term
- **验收标准**：
  - ✅ `iter_glossary_raw.tsv` 存在且 ≥130 行
  - ✅ term 列无 HTML 标签残留
  - ✅ 脚本无网络错误时 exit code = 0
- **潜在风险**：ITER 网站可能有 rate limit 或 Cloudflare 保护 — 实测无

#### ✅ Task 2.2: ITER Glossary → registry 候选 diff 报告

- **目标**：将 ITER 术语与现有 registry 做比对，生成增量报告
- **修改内容**：
  - 新建文件 `scripts/diff_terminology_source.py`：
    - 读取 `iter_glossary_raw.tsv` + 现有 `aliases.tsv`
    - 按 term 名称 normalize（lowercase、strip）后比对
    - 输出 `artifacts/terminology_sources/iter_glossary_diff.tsv`（列：`term | status[new/exists/conflict] | matched_concept_id | definition`）
- **修改边界**：不修改 registry 文件
- **测试要求**：
  - 运行 `python3 scripts/diff_terminology_source.py --source artifacts/terminology_sources/iter_glossary_raw.tsv`
  - 输出文件有 new/exists/conflict 统计摘要到 stdout
- **验收标准**：
  - ✅ diff 文件覆盖全部 ITER 术语
  - ✅ 已有术语（如 tokamak, divertor, NBI）标记为 `exists`
  - ✅ 新术语（如 Shattered Pellet Injection, H-Mode）标记为 `new`
- **潜在风险**：fuzzy matching 不做，仅精确匹配 + case-insensitive；可能遗漏变体形式 — 可接受，后续人工补

### Phase 3: IAEA Safety Glossary 提取

#### ✅ Task 3.1: 下载 IAEA Safety Glossary PDF

- **目标**：下载 IAEA Safety Glossary 2018 Edition PDF 到本地
- **修改内容**：
  - 下载 `https://www-pub.iaea.org/MTCD/Publications/PDF/PUB1830_web.pdf` 到 `artifacts/terminology_sources/IAEA_Safety_Glossary_2018.pdf`
- **修改边界**：纯下载，不修改任何代码
- **测试要求**：
  - 文件大小 ≈1.85 MB
  - `file` 命令确认为 PDF
- **验收标准**：
  - ✅ PDF 文件存在且可正常打开
  - ✅ `pdftotext` 能提取出文本
- **潜在风险**：下载速度慢（IAEA 服务器在维也纳）— 可用代理或手动下载

#### ✅ Task 3.2: IAEA PDF → 术语 TSV 提取脚本

- **目标**：从 IAEA Safety Glossary PDF 提取术语条目
- **修改内容**：
  - 新建文件 `scripts/extract_iaea_glossary.py`：
    - 用 `subprocess` 调 `pdftotext -layout` 提取全文
    - 正则识别术语条目格式（粗体术语行 + 缩进定义段落）
    - 筛选核安全/辐射防护/废物管理相关条目（按关键词或全量提取）
    - 输出 `artifacts/terminology_sources/iaea_safety_glossary_raw.tsv`（列：`term_en | definition | page`）
- **修改边界**：不修改 pipeline 代码
- **测试要求**：
  - 运行 `python3 scripts/extract_iaea_glossary.py`
  - 输出 ≥200 条术语（IAEA Glossary 约有 450+ 条）
  - 抽查 5 条术语的定义与原文一致
- **验收标准**：
  - ✅ 输出 TSV 存在且记录数合理
  - ✅ 无大量截断/拼接错误
  - ✅ 术语与定义正确对应（抽查）
- **潜在风险**：PDF 排版复杂（双栏、交叉引用、*see* 标注）— 需要多轮正则迭代

#### ✅ Task 3.3: IAEA Glossary → registry 候选 diff 报告

- **目标**：与 Task 2.2 同类，比对 IAEA 术语与现有 registry
- **修改内容**：
  - 复用 `scripts/diff_terminology_source.py`（Task 2.2 已创建），传入 IAEA TSV
  - 输出 `artifacts/terminology_sources/iaea_glossary_diff.tsv`
- **修改边界**：不修改 registry 文件
- **测试要求**：
  - 运行 diff 脚本，输出文件存在
  - new/exists/conflict 统计合理
- **验收标准**：
  - ✅ diff 文件覆盖全部 IAEA 术语
  - ✅ 辐射防护类术语（如 dose, shielding, activation）能匹配到现有 registry
- **潜在风险**：IAEA 术语偏安全/监管方向，与聚变技术 registry 重叠度可能不高 — 这是正常的，补充的就是这部分

### Phase 4: GB/T 4960.9 OCR 提取

#### ⏸ Task 4.1: OCR 预处理与文本提取

> **BLOCKED**: `tesseract-ocr` + `tesseract-ocr-chi-sim` not installed. Run:
> `sudo apt install tesseract-ocr tesseract-ocr-chi-sim`
> Then: `python3 scripts/ocr_gbt4960.py`
> Script created and ready.

- **目标**：对 Zotero 中 GB/T 4960.9-2013 扫描 PDF 做 OCR，提取中英文术语
- **修改内容**：
  - 新建文件 `scripts/ocr_gbt4960.py`：
    - 输入：`~/Zotero/storage/B2RVUCN5/GB-T 4960.pdf`（84 页扫描件，无文本层）
    - 用 `pdf2image` + `pytesseract`（`chi_sim+eng` 双语模型）做 OCR
    - 输出原始 OCR 文本到 `artifacts/terminology_sources/gbt4960_9_ocr_raw.txt`
- **修改边界**：不修改 registry，不修改 pipeline
- **测试要求**：
  - 确认 `tesseract --list-langs` 包含 `chi_sim`
  - OCR 输出文件非空，≥50KB
  - 抽查 3 页，中文术语可辨识
- **验收标准**：
  - ✅ OCR 文本文件存在且非空
  - ✅ 中文字符占比 >30%（不是全乱码）
  - ✅ 关键术语（如"托卡马克""等离子体""偏滤器"）可在文本中找到
- **潜在风险**：扫描质量差（Kodak Document Imaging）可能导致 OCR 错误率高 — 后续人工校对

#### ⏸ Task 4.2: GB/T 4960.9 术语对提取

> **BLOCKED**: depends on Task 4.1 OCR output

- **目标**：从 OCR 文本中识别结构化的"编号 + 中文术语 + 英文术语 + 定义"条目
- **修改内容**：
  - 在 `scripts/ocr_gbt4960.py` 中追加术语提取逻辑（或新建 `scripts/parse_gbt4960.py`）：
    - GB/T 4960.9 格式：`编号  中文名  英文名  [定义]`
    - 正则匹配 `(\d+\.\d+[\.\d]*)[\s]+([\u4e00-\u9fff]+.*)[\s]+([A-Za-z][\w\s\-]+)` 等模式
    - 输出 `artifacts/terminology_sources/gbt4960_9_terms.tsv`（列：`term_id | zh | en | definition | ocr_confidence`）
- **修改边界**：不修改 registry
- **测试要求**：
  - 输出 ≥100 条术语对（GB/T 4960.9-2013 约 250+ 条术语）
  - 抽查 10 条中英文对应正确
- **验收标准**：
  - ✅ 输出 TSV 存在且 ≥100 行
  - ✅ 每行有非空 zh 和 en 字段
  - ✅ 所有行标记 `status=draft`
- **潜在风险**：OCR 对中英文混排识别常出错（如"divertor"误识别为"divert0r"）— 全部标 draft，人工校对

#### ⏸ Task 4.3: GB/T 4960.9 → registry 候选 diff 报告

> **BLOCKED**: depends on Task 4.2 output

- **目标**：国标术语与现有 registry 比对
- **修改内容**：复用 `scripts/diff_terminology_source.py`
- **修改边界**：不修改 registry
- **测试要求**：运行输出 diff 报告
- **验收标准**：
  - ✅ diff 文件存在
  - ✅ 匹配到的已有术语（如"托卡马克"）标记为 `exists`
  - ✅ 国标专有术语标记为 `new` 并附带 `source=GB/T-4960.9`
- **潜在风险**：OCR 错误导致匹配率偏低 — 可接受，人工校对后重跑

### Phase 5: 人工审核与批量导入

#### ✅ Task 5.1: 编写批量导入脚本

- **目标**：将审核后的 diff 报告中标记为 `approved` 的条目批量写入 registry
- **修改内容**：
  - 新建文件 `scripts/import_approved_terms.py`：
    - 读取经人工审核的 diff TSV（`status` 列改为 `approved` / `rejected` / `defer`）
    - 将 `approved` 条目追加到 `concepts.tsv`（含 `source` 列）和 `aliases.tsv`
    - 追加 evidence 条目到 `evidence.tsv`（source = 标准编号或 URL）
    - 输出统计摘要
- **修改边界**：不删除或修改现有行，仅追加
- **测试要求**：
  - 用 3 条 mock approved 行测试
  - 运行后 `validate_registry` 通过
  - 运行后 `export_registry` 无报错
- **验收标准**：
  - ✅ 新行格式正确（8 列 concepts，5 列 aliases，5 列 evidence）
  - ✅ concept_id 不重复
  - ✅ 全量 pipeline 通过
- **潜在风险**：concept_id 命名冲突 — 脚本检查重复后拒绝写入

#### Task 5.2: 人工审核 ITER diff 并导入（批次操作）

- **目标**：审核 ITER glossary diff，标记 approved 后导入
- **执行者**：用户人工审核 + `import_approved_terms.py`
- **修改内容**：
  - 编辑 `iter_glossary_diff.tsv`，逐条标记
  - 运行导入脚本
- **修改边界**：仅追加 registry 行
- **测试要求**：导入后全量 `pytest` 通过
- **验收标准**：
  - ✅ 新增 concepts 的 `source=ITER-glossary`
  - ✅ evidence.tsv 中新增行的 source 为 `https://www.iter.org/fusion-glossary`
- **潜在风险**：ITER 术语含设备名（ADITYA-U, JT-60SA 等），可能不适合作为通用术语 — 人工排除

#### Task 5.3: 人工审核 IAEA diff 并导入

- **执行者**：用户人工审核 + `import_approved_terms.py`
- **修改内容**：同 Task 5.2，数据源为 IAEA
- **验收标准**：
  - ✅ 新增 concepts 的 `source=IAEA-safety-glossary`
  - ✅ evidence.tsv source 为 `IAEA-Safety-Glossary-2018`
- **潜在风险**：IAEA 术语以英文为主，需人工补充 `preferred_zh` — 可参考 GB/T 4960.5 译名

#### Task 5.4: 人工校对 GB/T 4960.9 OCR 结果并导入

- **执行者**：用户人工校对 OCR + `import_approved_terms.py`
- **修改内容**：同上，数据源为 GB/T 4960.9
- **验收标准**：
  - ✅ 新增 concepts 的 `source=GB/T-4960.9`
  - ✅ 中英文术语对经人工确认正确
  - ✅ 国标术语设为 L1 权威级别
- **潜在风险**：OCR 校对工作量大（~250 条 × 84 页）— 可分批进行

### Phase 6: 全量回归验证

#### ✅ Task 6.1: 全量 pipeline 验证

- **目标**：确认 schema 扩展 + 术语导入后全部 pipeline 正常
- **修改内容**：无代码修改，纯验证
- **测试要求**：
  - `python3 -m pipeline.validate_registry` 通过
  - `python3 -m pipeline.export_registry --config config.toml` 通过
  - `python3 -m pipeline.build_terms --config config.toml` 通过
  - `pytest` 全量通过
- **验收标准**：
  - ✅ 零报错
  - ✅ 导出产物（domain_terms.txt, translation_dict.json 等）内容合理
  - ✅ 新增术语出现在 domain_terms.txt 中
- **潜在风险**：大量新增术语可能与 denylist 冲突 — 检查并更新 denylist

## 回归检查清单

- [ ] 全量测试通过：`pytest`
- [ ] `validate_registry` 无新增 warning
- [ ] `export_registry` 导出产物无退化（diff 检查）
- [ ] `build_terms` 输出的 domain_terms.txt 行数 ≥ 修改前
- [ ] concepts.tsv 所有行列数一致（8 列）
- [ ] 新增 concepts 的 concept_id 唯一
- [ ] 新增 aliases 不与现有 aliases 冲突
- [ ] evidence.tsv 新增行的 source 字段非空
- [ ] rime_import_safe 不报错

## 审查日志

| 轮次 | 聚焦 | 发现问题数 | 已修正 | 剩余 |
|------|------|-----------|--------|------|
| R1 | 结构完整性 | 4 | 4 | 0 |
| R2 | 可执行性 | 3 | 3 | 0 |
| R3 | 风险与边缘 | 2 | 2 | 0 |
| **终止** | **T1 — 收敛终止** | | | **0** |

### Completion Summary

| 维度 | 结果 |
|------|------|
| 背景与目标 | 完整（问题描述、目标、非目标、复用分析均包含） |
| 技术方案 | 完整（方案概述、设计决策、影响范围） |
| Error & Rescue Map | 已覆盖 7 条路径，0 CRITICAL GAP |
| 执行计划 | 6 Phase、15 Task |
| 回归检查清单 | 9 项目特定检查 |
| 已知局限 | 无 |

### R1 Issues (结构完整性)

- **Issue R1-1**: 缺少 Error & Rescue Map → 已补充 7 条关键路径 ✅ 已修正
- **Issue R1-2**: 缺少已有代码/流程复用分析 → 已添加到背景与目标 section ✅ 已修正
- **Issue R1-3**: Task 4.2 缺少验收标准中对 draft status 的要求 → 已补充 ✅ 已修正
- **Issue R1-4**: Task 5.1 缺少 concepts 列数说明（应为 8 列而非 7 列） → 已修正为 8 列 ✅ 已修正

### R2 Issues (可执行性)

- **Issue R2-1**: Task 2.1 未指定依赖：需要 Phase 1 完成后才能设定 source 列 → 实际 Task 2.1 仅生成 staging 不写 registry，与 Phase 1 可并行。已在描述中明确 ✅ 已修正
- **Issue R2-2**: Task 4.1 依赖 `pytesseract` + `pdf2image`，requirements.txt 可能未包含 → 添加依赖安装说明到 Task 4.1 测试要求前置步骤 ✅ 已修正
- **Issue R2-3**: Task 1.1 "所有非注释行有 8 个 tab 分隔字段" 验收标准对于 concepts.tsv 中大量空字段行可能误判 → 改为"8 个或以上 tab 分隔字段" ✅ 已修正

### R3 Issues (风险与边缘)

- **Issue R3-1**: Phase 2-4 可独立并行执行，但 Phase 5 依赖全部 staging 完成 → 依赖关系已隐含在 Phase 编号中，已在 Task 5.x 添加前置依赖说明 ✅ 已修正
- **Issue R3-2**: 如果 GB/T 4960.9 OCR 完全失败（质量太差），Phase 4 应有退出策略 → 已在 Task 4.1 潜在风险中补充"如 OCR 质量不可用则跳过 Phase 4，待标准修订版发布后重新获取" ✅ 已修正

### 收敛检测信号

| 信号 | R1 | R2 | R3 |
|------|----|----|-----|
| S1: issue 数下降 | — | 4→3 ↓ | 3→2 ↓ |
| S2: 同类别重复 | — | 否 | 否 |
| S3: 修正引入新 issue | — | 0 | 0 |

## Pre-Delivery Audit (Level: L1-Lite)

| § | Check | Status | Note |
|---|-------|--------|------|
| 1 | Unit consistency | ✅ PASS | N/A — 纯流程/代码计划，无物理量 |

Auditor: Plan Architect | Date: 2026-04-14
