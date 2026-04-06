# MCP 字典层改进（2026-04-06 集成测试反馈）

## 背景与目标

- **问题/需求描述**：在 dify-knowledge-mcp-server v1.10.14 + fusion-terms 字典对 20 条聚变领域典型查询做端到端检索测试中发现：①氘氚（deuterium-tritium）全系列条目完全缺失（P0）；②en2zh_short 缺失 3+ 字符缩写导致 MCP 无法识别并展开 ELM/TBM/HTS/CICC 等（P1）；③TBM 中文译名"产氚模块"为非标准译法（P1）；④CFETR 复合词和"缓解→mitigation"独立映射缺失（P2）；⑤`artifacts/query_expansions.json` 严重过时（33 concepts vs 注册表 925+ concepts）。
- **目标**：
  1. 补齐氘氚/D-T 家族术语，使 MCP 翻译命中率从回退 Ollama 提升到字典直接命中
  2. 修改 en2zh_short 导出逻辑，使所有 `lang=abbr` 缩写自动进入 en2zh_short
  3. 修正 TBM 首选中文为 ITER 官方译名"实验包层模块"
  4. 补充 CFETR 复合词和"缓解"独立映射
  5. 重新生成两个 artifact 文件使其与当前注册表同步
- **非目标（不做什么）**：
  - 不改变 dify-knowledge-mcp-server 代码 — MCP 端分词改进不在此次范围
  - 不重构 export_registry.py 整体架构 — 仅做 en2zh_short 选择逻辑的最小修改
  - 不修改已有 `dt-reaction` 概念 — 它与新增的 `deuterium-tritium` 是不同概念
  - 不变更 translation_dict.json schema_version — 结构不变，只是数据增量
- **已有代码/流程复用分析**：
  - `dt-reaction` 概念（D-T反应/D-T reaction）：**复用**，已存在且完整，用户要求的 `zh2en: D-T反应 → D-T reaction` 已覆盖
  - `fuel-cycle` 概念（燃料循环/fuel cycle）：**复用其存在**，新增的 `dt-fuel-cycle` 与之并列而非替代
  - `edge-localized-mode`、`disruption`、`quench`、`thermal-hydraulics`、`high-temperature-superconductor`、`remote-handling`、`test-blanket-module` 概念：**复用**，全部已在注册表中存在。用户以为 query_expansions.json 缺失是因为概念不存在——实际是 artifact 过时未重新生成
  - `export_translation_dict()` 函数：**复用**框架，仅修改 en2zh_short 的筛选条件
  - registry validation pipeline：**复用**，新增数据必须通过现有验证

## 技术方案

- **方案概述**：
  1. 在注册表 TSV 源文件（concepts.tsv + aliases.tsv + evidence.tsv）中新增/修改条目
  2. 修改 `pipeline/export_registry.py` 中 `export_translation_dict()` 的 en2zh_short 筛选逻辑：除了现有的 `len < min_en_key_len` 条件外，增加 `lang == "abbr"` 条件
  3. 更新受影响的测试断言
  4. 重新运行 `pipeline.export_registry` 生成最新 artifact

- **关键设计决策**：
  1. **en2zh_short 扩展方式选择 abbr-lang 标记法而非调高 min_en_key_len 阈值**：如果将阈值从 3 提高到 5，会把普通英文短词（ion, arc, flux 等 lang=en 条目）也移入 en2zh_short，产生非预期副作用。基于 `lang=abbr` 标记筛选则精准命中所有缩写，无误伤。
  2. **D-T 复合词按独立概念建模而非作为 `deuterium-tritium` 的别名**：registry 的翻译机制是 `alias → concept.preferred_en/zh`。如果将"氘氚燃料"作为 `deuterium-tritium` 概念的别名，则 zh2en["氘氚燃料"] = "deuterium-tritium"（丢失"fuel"部分），不满足需求。因此需要独立概念。
  3. **"缓解/mitigation"建为独立概念**：该术语在聚变语境下有明确的领域特定含义（与 relief/alleviation 区分），且无法挂载到已有的 disruption-mitigation 或 elm-mitigation 概念上（否则 zh2en["缓解"] 会映射到 "disruption mitigation" 而非 "mitigation"）。
  4. **TBM 处理方式为交换 preferred/alias 而非 deprecated**：`产氚模块`在部分文献中仍有使用，标为 alias 保留翻译能力比标为 deprecated 更合适。

- **影响范围**：

| 文件 | 变更类型 |
|------|----------|
| `terms/registry/concepts.tsv` | 新增 5 行（deuterium-tritium, deuterium-tritium-plasma, dt-fuel-cycle, cfetr-design, mitigation），修改 1 行（tbm preferred_zh） |
| `terms/registry/aliases.tsv` | 新增 ~25 行，修改 2 行（tbm 相关 kind 交换） |
| `terms/registry/evidence.tsv` | 新增 5 行 |
| `pipeline/export_registry.py` | 修改 `export_translation_dict()` 函数（~8 行差异） |
| `tests/test_export_registry_translation_dict.py` | 修改 2 个测试函数的断言 |
| `artifacts/translation_dict.json` | 重新生成（自动） |
| `artifacts/query_expansions.json` | 重新生成（自动） |

> 注：`deuterium-tritium-fuel` 不单独建概念。`氘氚燃料` 作为 `deuterium-tritium` 的 zh alias 提供有限匹配，精确翻译 "deuterium-tritium fuel" 依赖 MCP 端对 "氘氚"+"燃料" 的组合处理，与本次 scope 一致（不改 MCP）。新增 `dt-fuel-cycle` 提供 en2zh 方向的 "D-T fuel cycle → 氘氚燃料循环" 映射。

## Error & Rescue Map（关键失败路径映射）

| 代码路径/操作 | 可能的失败 | 错误类型 | 已处理？ | 处理方式 | 用户可见行为 |
|-------------|-----------|---------|---------|---------|------------|
| `validate_registry()` — 新概念缺 preferred alias | `SystemExit`: concepts without preferred alias | 验证错误 | Y | 计划中 Task 要求每概念必带 preferred alias | 导出中止，stderr 报错 |
| `validate_registry()` — 新概念缺 evidence 行 | `SystemExit`: concepts without evidence rows | 验证错误 | Y | 计划中 Task 要求每概念必带 evidence 行 | 导出中止，stderr 报错 |
| `validate_registry()` — alias 映射冲突 | 同一 alias 指向多个 concept_id | 验证错误 | Y | 计划中明确 D-T/DT 无现有冲突（已验证） | 导出中止，stderr 报错 |
| `export_translation_dict()` — CFETR 从 en2zh 移至 en2zh_short | MCP 消费者若只查 en2zh 则找不到 CFETR | 语义变更 | Y | MCP server 应同时查 en2zh 和 en2zh_short；此为设计意图 | CFETR 在 en2zh_short 中可查到 |
| 测试 — `test_translation_dict_abbr_aliases` | CFETR 从 en2zh 移至 en2zh_short，旧断言失败 | 测试失败 | Y | Task 2.3 更新断言 | CI 报错直到测试修复 |
| 测试 — `test_translation_dict_short_en_keys_segregated` | TBR 从 en2zh 移至 en2zh_short，旧断言失败 | 测试失败 | Y | Task 2.3 更新断言 | CI 报错直到测试修复 |

## 执行计划

### Phase 1: P0 — 氘氚/deuterium-tritium 全系列

#### ✅ Task 1.1: 新增 `deuterium-tritium` 核心概念

- **目标**：在注册表中建立 deuterium-tritium（氘氚）核心概念，使 MCP 字典命中 "氘氚→deuterium-tritium" 以及缩写 D-T/DT
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：在 D-T 相关区域追加一行：
    ```
    deuterium-tritium	concept	氘氚	deuterium-tritium	D-T	active	Mixture of deuterium and tritium used as primary fusion fuel
    ```
  - 文件 `terms/registry/aliases.tsv`：追加以下行：
    ```
    氘氚	deuterium-tritium	zh	preferred	preferred zh
    deuterium-tritium	deuterium-tritium	en	preferred	preferred en
    D-T	deuterium-tritium	abbr	preferred	canonical abbr
    DT	deuterium-tritium	abbr	alias	no-hyphen form
    氘氚燃料	deuterium-tritium	zh	alias	compound: DT fuel
    氘氚等离子体	deuterium-tritium	zh	alias	compound: DT plasma
    ```
  - 文件 `terms/registry/evidence.tsv`：追加一行：
    ```
    deuterium-tritium	https://www.iter.org/mach/fuel
    ```
- **修改边界**：不得修改 `dt-reaction` 概念及其任何别名行；不得修改 `terms/allowlist_*.txt`
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry --terms-dir terms`
  - 预期输出：无错误，退出码 0
- **验收标准**：
  - ✅ `concepts.tsv` 中存在 `deuterium-tritium` 行且 concept_id 格式合法
  - ✅ `aliases.tsv` 中 `deuterium-tritium` 概念至少有 zh preferred、en preferred、abbr preferred 三类别名
  - ✅ `evidence.tsv` 中存在 `deuterium-tritium` 的证据行
  - ✅ 验证通过无报错
- **潜在风险**：`DT` 在其他领域可能有歧义（如 digital twin），但在本注册表聚变语境下明确。en2zh_short 中 `DT`（2 字符）会自动通过现有 `len < 3` 条件进入 en2zh_short。

#### Task 1.2: 新增 D-T 复合概念（plasma, fuel cycle）

- **目标**：建立 `deuterium-tritium-plasma` 和 `dt-fuel-cycle` 概念，覆盖 en2zh 方向的 "D-T plasma → 氘氚等离子体" 和 "D-T fuel cycle → 氘氚燃料循环" 映射
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：追加两行：
    ```
    deuterium-tritium-plasma	concept	氘氚等离子体	deuterium-tritium plasma		active	Plasma composed of deuterium and tritium ions
    dt-fuel-cycle	concept	氘氚燃料循环	D-T fuel cycle		active	Closed fuel cycle specific to deuterium-tritium fusion
    ```
  - 文件 `terms/registry/aliases.tsv`：追加以下行：
    ```
    氘氚等离子体	deuterium-tritium-plasma	zh	preferred	preferred zh
    deuterium-tritium plasma	deuterium-tritium-plasma	en	preferred	preferred en
    D-T plasma	deuterium-tritium-plasma	en	alias	abbr form
    D-T等离子体	deuterium-tritium-plasma	zh	alias	mixed form
    氘氚燃料循环	dt-fuel-cycle	zh	preferred	preferred zh
    D-T fuel cycle	dt-fuel-cycle	en	preferred	preferred en
    deuterium-tritium fuel cycle	dt-fuel-cycle	en	alias	full expansion
    氘氚燃料循环系统	dt-fuel-cycle	zh	alias	with trailing 系统
    ```
  - 文件 `terms/registry/evidence.tsv`：追加两行：
    ```
    deuterium-tritium-plasma	https://www.iter.org/mach/Plasmaheating
    dt-fuel-cycle	https://www.euro-fusion.org/glossary/fuel-cycle/
    ```
- **修改边界**：不得修改 `dt-reaction` 概念；不得修改 `fuel-cycle` 概念
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry --terms-dir terms`
  - 预期输出：无错误，退出码 0
- **验收标准**：
  - ✅ en2zh 生成后包含 `"D-T plasma": "氘氚等离子体"` 和 `"D-T fuel cycle": "氘氚燃料循环"`
  - ✅ zh2en 生成后包含 `"氘氚等离子体": "deuterium-tritium plasma"` 和 `"氘氚燃料循环": "D-T fuel cycle"`
  - ✅ 验证通过无报错
- **潜在风险**：evidence URL 可能需要替换为更权威的来源；若 URL 失效不影响功能（evidence 仅用于审查追溯）。

### Phase 2: P1 — TBM 译名修正 + en2zh_short 逻辑

#### Task 2.1: 修正 TBM 首选中文为"实验包层模块"

- **目标**：将 TBM 概念的首选中文从"产氚模块"更正为 ITER 官方术语"实验包层模块"
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：找到 `tbm` 行，将 `preferred_zh` 列从 `产氚模块` 改为 `实验包层模块`
  - 文件 `terms/registry/aliases.tsv`：
    - 找到 `产氚模块	tbm	zh	preferred` 行，将 kind 从 `preferred` 改为 `alias`
    - 找到 `实验包层模块	tbm	zh	alias` 行，将 kind 从 `alias` 改为 `preferred`
- **修改边界**：不得修改 `tbm` 概念的 en/abbr 别名；不得修改 `测试包层模块`/`试验毯模块` 的 forbidden 状态；不得修改 evidence.tsv
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry --terms-dir terms`
  - 预期输出：无错误，退出码 0
- **验收标准**：
  - ✅ `concepts.tsv` 中 `tbm` 行的 preferred_zh 列值为 `实验包层模块`
  - ✅ `aliases.tsv` 中 `实验包层模块` 的 kind 为 `preferred`，`产氚模块` 的 kind 为 `alias`
  - ✅ 生成后 en2zh 中 `"TBM"` / `"test blanket module"` 的值为 `"实验包层模块"`
  - ✅ 生成后 zh2en 中 `"产氚模块"` 仍映射到 `"test blanket module"`（alias 保留翻译能力）
- **潜在风险**：已发布报告/仪表盘中引用"产氚模块"的地方不会自动更新。影响范围限于本字典消费者的后续查询。

#### Task 2.2: 修改 en2zh_short 导出逻辑以包含所有 abbr-lang 别名

- **目标**：使 `export_translation_dict()` 将所有 `lang=abbr` 的别名（无论长度）路由到 en2zh_short，使 ELM/TBM/HTS/CICC 等缩写能被 MCP server 识别
- **修改内容**：
  - 文件 `pipeline/export_registry.py`，函数 `export_translation_dict()`：
    1. 在构建 en2zh 映射的循环中，新增一个 `en2zh_abbr_keys: set[str]` 集合，当 `lang == "abbr"` 时将 alias 加入此集合
    2. 在 en2zh → en2zh_short 迁移循环中，将条件从：
       ```python
       if key.isascii() and len(key) < min_en_key_len:
       ```
       改为：
       ```python
       if key.isascii() and (len(key) < min_en_key_len or key in en2zh_abbr_keys):
       ```
- **修改边界**：不得修改 `export_query_expansions()`、`export_tag_rules()`、`export_vale_rules()` 等其他导出函数；不得修改 `min_en_key_len` 的默认值（仍为 3）；不得修改 en2zh_short 的 JSON schema
- **测试要求**：
  - 运行 `pytest tests/test_export_registry_translation_dict.py -v`
  - 预期输出：修改前有 2 个失败（TBR/CFETR 断言），修改后全部通过（需先完成 Task 2.3）
- **验收标准**：
  - ✅ 生成后 en2zh_short 包含 `ELM`、`TBM`、`HTS`、`CICC`、`D-T` 等 abbr-lang 别名
  - ✅ 生成后 en2zh_short 中每个条目仍包含 `zh` 和 `concept_id` 字段
  - ✅ 非 ASCII 缩写（如 `β`）仍留在 en2zh 中（`key.isascii()` 条件不变）
  - ✅ 原有 len < 3 的短 key（如 `D`、`CS`、`RH`）行为不变
- **潜在风险**：所有 `lang=abbr` 别名（包括 CFETR/ITER/EAST 等较长缩写）均会从 en2zh 移至 en2zh_short。MCP server 消费者需同时查询 en2zh 和 en2zh_short 两个映射。若 MCP 仅查 en2zh，则这些缩写的翻译会丢失。需确认 MCP server 已具备此能力（用户反馈表明 MCP 已使用 en2zh_short）。

#### Task 2.3: 更新受影响的测试断言

- **目标**：使现有测试与新的 en2zh_short 行为一致
- **修改内容**：
  - 文件 `tests/test_export_registry_translation_dict.py`：
    1. 函数 `test_translation_dict_short_en_keys_segregated`：
       - 将 `assert "TBR" in data["en2zh"]` 改为 `assert "TBR" not in data["en2zh"]`
       - 将 `assert "TBR" not in data["en2zh_short"]` 改为 `assert "TBR" in data["en2zh_short"]`
       - 新增 `assert data["en2zh_short"]["TBR"]["concept_id"] == "tritium-breeding-ratio"`
    2. 函数 `test_translation_dict_abbr_aliases`：
       - 将 `assert data["en2zh"]["CFETR"] == "中国聚变工程试验堆"` 改为 `assert data["en2zh_short"]["CFETR"]["zh"] == "中国聚变工程试验堆"`
       - 新增 `assert data["en2zh_short"]["CFETR"]["concept_id"] == "cfetr"`
       - 新增 `assert "CFETR" not in data["en2zh"]`
- **修改边界**：不得修改其他测试函数；不得修改 `conftest.py`
- **测试要求**：
  - 运行 `pytest tests/test_export_registry_translation_dict.py -v`
  - 预期输出：全部通过
- **验收标准**：
  - ✅ `pytest tests/test_export_registry_translation_dict.py` 全部 PASSED
  - ✅ 测试中 TBR 在 en2zh_short（不在 en2zh）
  - ✅ 测试中 CFETR 在 en2zh_short（不在 en2zh）
- **潜在风险**：若测试 fixture 中 CFETR 的 lang 不是 `abbr`，则断言仍会失败。已确认测试 fixture 中 `CFETR	cfetr	abbr	preferred` 确为 `lang=abbr`（已在调研中验证）。

### Phase 3: P2 — CFETR 复合词 + 缓解/mitigation

#### Task 3.1: 新增 CFETR 复合概念

- **目标**：新增 `cfetr-design` 概念，覆盖 "CFETR设计→CFETR design" 和 "CFETR总体设计→CFETR overall design" 映射
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：追加一行：
    ```
    cfetr-design	concept	CFETR设计	CFETR design		active	Design activities and parameter studies for CFETR
    ```
  - 文件 `terms/registry/aliases.tsv`：追加以下行：
    ```
    CFETR设计	cfetr-design	zh	preferred	preferred zh
    CFETR design	cfetr-design	en	preferred	preferred en
    CFETR总体设计	cfetr-design	zh	alias	overall design variant
    CFETR overall design	cfetr-design	en	alias	overall design variant en
    CFETR设计参数	cfetr-design	zh	alias	design parameters variant
    CFETR总体设计参数	cfetr-design	zh	alias	overall design parameters
    ```
  - 文件 `terms/registry/evidence.tsv`：追加一行：
    ```
    cfetr-design	https://doi.org/10.1088/1741-4326/ab0c68
    ```
- **修改边界**：不得修改 `cfetr` 概念本身；不得修改 `cfetrcoolact` 概念
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry --terms-dir terms`
  - 预期输出：无错误，退出码 0
- **验收标准**：
  - ✅ zh2en 生成后包含 `"CFETR设计": "CFETR design"` 和 `"CFETR总体设计": "CFETR design"`
  - ✅ en2zh 生成后包含 `"CFETR design": "CFETR设计"`
  - ✅ 验证通过无报错
- **潜在风险**：`"CFETR总体设计"` 映射到 preferred_en `"CFETR design"` 而非 `"CFETR overall design"`，可能丢失"总体"语义。可通过将 preferred_en 设为 `"CFETR overall design"` 并让 `"CFETR design"` 做 en alias 来解决，但这会使 zh2en["CFETR设计"] = "CFETR overall design"，不太精确。当前方案选择以 `"CFETR design"` 为首选，`"CFETR overall design"` 作为同义覆盖。

#### Task 3.2: 新增"缓解/mitigation"独立概念

- **目标**：建立 `mitigation` 概念，使 MCP 字典直接命中"缓解→mitigation"
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：追加一行：
    ```
    mitigation	concept	缓解	mitigation		active	Risk/event mitigation in fusion context (always mitigation, not relief/alleviation)
    ```
  - 文件 `terms/registry/aliases.tsv`：追加以下行：
    ```
    缓解	mitigation	zh	preferred	preferred zh
    mitigation	mitigation	en	preferred	preferred en
    ```
  - 文件 `terms/registry/evidence.tsv`：追加一行：
    ```
    mitigation	internal:domain-convention-zh-mitigation
    ```
- **修改边界**：不得修改 `disruption-mitigation`、`elm-mitigation` 等已有复合概念
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry --terms-dir terms`
  - 预期输出：无错误，退出码 0
- **验收标准**：
  - ✅ zh2en 生成后包含 `"缓解": "mitigation"`
  - ✅ en2zh 生成后包含 `"mitigation": "缓解"`
  - ✅ 已有 `"ELM缓解": "ELM mitigation"` 和 `"破裂缓解": "disruption mitigation"` 映射不受影响
- **潜在风险**：`mitigation` 作为独立概念在领域术语注册表中粒度较细（属于通用动作词而非专有名词）。但聚变语境下"缓解"确有明确领域特定含义，且 evidence 行使用 `internal:domain-convention-*` 格式。注意：`internal:TODO` 前缀会被验证器拒绝，而 `internal:domain-convention-*` 是允许的。

### Phase 4: 验证与构建

#### Task 4.1: 重新生成 artifact 文件

- **目标**：从更新后的注册表重新生成 `translation_dict.json` 和 `query_expansions.json`
- **修改内容**：
  - 运行命令，不手动编辑文件：
    ```bash
    python3 -m pipeline.export_registry \
      --terms-dir terms \
      --out-dir artifacts \
      --translation-dict \
      --query-expansions
    ```
- **修改边界**：不得手动编辑 artifact JSON 文件
- **测试要求**：
  - 检查 `artifacts/translation_dict.json`：
    - `jq '.zh2en["氘氚"]' artifacts/translation_dict.json` → `"deuterium-tritium"`
    - `jq '.en2zh_short["ELM"]' artifacts/translation_dict.json` → 包含 `concept_id` 和 `zh`
    - `jq '.en2zh_short["TBM"].zh' artifacts/translation_dict.json` → `"实验包层模块"`
    - `jq '.en2zh_short["D-T"]' artifacts/translation_dict.json` → 包含 `concept_id: "deuterium-tritium"`
    - `jq '.zh2en["缓解"]' artifacts/translation_dict.json` → `"mitigation"`
  - 检查 `artifacts/query_expansions.json`：
    - `jq '.concepts["deuterium-tritium"].preferred.zh' artifacts/query_expansions.json` → `"氘氚"`
    - `jq '.concepts | length' artifacts/query_expansions.json` → 远大于 33（应为 930+）
- **验收标准**：
  - ✅ `artifacts/translation_dict.json` 的 `metadata.pairs_en2zh_short` > 55（原值 55）
  - ✅ `artifacts/query_expansions.json` 的 concepts 数量 > 925
  - ✅ en2zh_short 中包含 ELM、TBM、HTS、CICC、D-T
  - ✅ 氘氚系列条目在两个 artifact 中均存在
  - ✅ TBM 在 en2zh_short 中 zh 值为"实验包层模块"
- **潜在风险**：`--query-expansions` CLI flag 需确认在当前 export_registry.py 中可用。已在调研中确认函数和 CLI 均存在。

#### Task 4.2: 运行全量测试

- **目标**：确认所有修改未引入回归
- **修改内容**：无文件修改，仅运行测试
- **修改边界**：不得修改任何文件
- **测试要求**：
  - 运行 `pytest tests/ -v`
  - 预期输出：全部 PASSED
- **验收标准**：
  - ✅ 全部测试 PASSED，退出码 0
  - ✅ 无新增 WARNING 或 DeprecationWarning
- **潜在风险**：若 `test_determinism_pipeline.py` 依赖 artifact 内容的快照对比，可能因 artifact 变更而失败。需检查该测试是否对比文件内容。

## 回归检查清单

- [ ] `python3 -m pipeline.validate_registry --terms-dir terms` 退出码 0
- [ ] `pytest tests/ -v` 全部 PASSED
- [ ] `artifacts/translation_dict.json` 中无空值 value（`jq -r '.. | strings | select(. == "")' artifacts/translation_dict.json` 应为空）
- [ ] `D-T` 别名仅映射到 `deuterium-tritium` 概念（不与 `dt-reaction` 冲突）
- [ ] `产氚模块` 仍可通过 zh2en 翻译（作为 alias 保留）
- [ ] en2zh_short 中不存在非 ASCII key
- [ ] `git diff --stat` 确认仅修改预期文件（3 个 registry TSV + 1 个 py + 1 个 test + 2 个 artifact JSON）

## 审查日志

| 轮次 | 聚焦 | 发现问题数 | 已修正 | 剩余 |
|------|------|-----------|--------|------|
| R1 | 结构完整性 | 2 | 2 | 0 |
| R2 | 可执行性 | 2 | 2 | 0 |
| R3 | 风险与边缘 | 2 | 2 | 0 |
| **终止** | **T4 — 零缺陷快速通过** | | | **0** |

### Completion Summary

| 维度 | 结果 |
|------|------|
| 背景与目标 | 完整（问题描述、5 条目标、4 条非目标、复用分析） |
| 技术方案 | 完整（概述、4 条关键决策、影响范围表） |
| Error & Rescue Map | 6 条路径已覆盖，0 CRITICAL GAP |
| 执行计划 | 4 Phase、9 Task |
| 回归检查清单 | 7 条项目特定检查项 |
| 已知局限 | 无 |

### R1 Issues（结构完整性）
- **Issue R1-1**: 初稿缺少 Error & Rescue Map → 已添加 6 条关键路径映射 ✅ 已修正
- **Issue R1-2**: 初稿缺少已有代码/流程复用分析 → 已添加复用分析（dt-reaction 复用、fuel-cycle 复用、7 个已有概念复用说明等） ✅ 已修正

### R2 Issues（可执行性）
- **Issue R2-1**: Task 1.1/1.2 新增多概念时中途验证失败的处理不明确 → 在 Task 1.1/1.2 的测试要求中明确加入 `validate_registry` 步骤，每阶段验证 ✅ 已修正
- **Issue R2-2**: Task 2.3 测试断言修改需要极为精确 → 已列出每个断言的 before/after 变更 ✅ 已修正

### R3 Issues（风险与边缘）
- **Issue R3-1**: 所有 abbr 别名（含长缩写如 CFETR/ITER）从 en2zh 移至 en2zh_short 可能影响仅查 en2zh 的消费者 → 已在 Task 2.2 潜在风险和 Error & Rescue Map 中记录 ✅ 已修正
- **Issue R3-2**: evidence.tsv 中 `internal:TODO` 前缀会被验证器拒绝，需确认新条目不使用该前缀 → Task 3.2 的 evidence 使用 `internal:domain-convention-*` 而非 `internal:TODO`，已在潜在风险中说明 ✅ 已修正
