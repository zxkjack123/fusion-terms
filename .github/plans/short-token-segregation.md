> ✅ **状态：已归档**

# 短 token 隔离：translation_dict.json en2zh 短键污染修复

## 背景与目标

- **问题/需求描述**：`translation_dict.json` 的 `en2zh` 中包含 39 个 ≤2 字符的英文键（其中 7 个是单字母：A, D, T, H, Q, q, W）。下游消费端 `formatGlossaryFromQuery()` 对 `en2zh` 做子串匹配时，短键会误匹配长词内部字符（如 `DAGMC` 被拆为 D→氘、A→纵横比、T→氚），导致错误的术语提示和翻译。
- **根因分析**：`export_translation_dict()` 在将 registry alias 转为 `en2zh` 映射时，没有最小键长过滤。所有 `lang ∈ {en, abbr, mixed}` 且 `kind ∈ {preferred, alias}` 的条目一律进入 `en2zh`，不区分键长度。
- **目标**：将短 ASCII 英文键（长度 < `min_en_key_len`，默认 3）从 `en2zh` 隔离到新的 `en2zh_short` 节，附带 `concept_id` 消歧信息，使朴素子串匹配消费端不受污染，智能消费端仍可利用短键。
- **非目标（不做什么）**：
  - 不修改 registry schema（aliases.tsv / concepts.tsv 格式不变）— 过滤在导出层完成
  - 不修改 `query_expansions.json` 导出逻辑 — 该产物有独立用途
  - 不修改 `zh2en` 方向 — 中文键不存在子串误匹配问题
  - 不修改下游消费端代码（`formatGlossaryFromQuery` 等）— 属于另一个仓库
- **已有代码/流程复用分析**：
  - `export_translation_dict()` 函数：复用（在其内部添加过滤逻辑，不重建）
  - `_iter_alias_rows()` / `_iter_concept_rows()`：复用（无需修改）
  - `_load_config()`：复用（已有 config 读取管线）
  - 测试基础设施（`_write_registry_tables`, `_run_export_translation`）：复用

## 技术方案

- **方案概述**：在 `export_translation_dict()` 中，构建 `en2zh` 后执行二次分区——对所有 ASCII 短键（`key.isascii() and len(key) < min_en_key_len`）迁入 `en2zh_short` 字典。`en2zh_short` 的 value 为 `{"zh": "翻译", "concept_id": "concept-id"}`，提供消歧上下文。`schema_version` 从 1 升至 2（纯增量，`en2zh`/`zh2en` 语义不变）。
- **关键设计决策**：
  1. **隔离而非删除**：短键信息保留在 `en2zh_short`，不丢失翻译对。消费端可选择忽略（等效删除）或做全词匹配。
  2. **ASCII-only 过滤**：`β`、`βp`、`q∥` 等含非 ASCII 字符的键不受影响——它们不会在英文子串匹配中被误命中。
  3. **阈值可配置**：通过 `config.toml [export] min_en_key_len` 控制，默认 3。设为 0 则不过滤（保持旧行为）。
  4. **schema_version=2**：向后兼容——旧消费端只读 `en2zh`/`zh2en`，新字段被忽略。
  5. **`en2zh_short` value 格式选择**：用 `{"zh": str, "concept_id": str}` 而非裸字符串，因为短键的核心问题是歧义，concept_id 提供消歧锚点。
- **影响范围**：
  - `config.toml` — 新增 `[export]` 节
  - `pipeline/export_registry.py` — 修改 `export_translation_dict()` 函数 + `main()` 传参
  - `tests/test_export_registry_translation_dict.py` — 新增测试 + 更新 schema_version 断言
  - `artifacts/translation_dict.json` — 重新生成

## Error & Rescue Map（关键失败路径映射）

| 代码路径/操作 | 可能的失败 | 错误类型 | 已处理？ | 处理方式 | 用户可见行为 |
|-------------|-----------|---------|---------|---------|------------|
| `config.toml` 中 `min_en_key_len` 缺失 | KeyError | 配置解析 | Y | 函数参数默认值 3 | 无影响，使用默认值 |
| `min_en_key_len=0` | 所有键都进 en2zh，en2zh_short 为空 | 逻辑边界 | Y | `len(key) < 0` 恒为 False，无过滤 | 行为等同旧版，无损 |
| `key.isascii()` 对空字符串 | 返回 True | 边界 | Y | 空 alias 不会进入 en2zh（已有前置过滤） | 无影响 |
| schema_version=2 被严格检查的消费端拒绝 | 消费端报错 | 兼容性 | N | 需消费端适配 | **已知局限**：严格校验 schema_version==1 的外部消费端需更新 |
| `concept_id` 在 en2zh_short 中拼写错误 | 消歧失效 | 数据完整性 | Y | concept_id 直接从 alias_rows 复制，无转换 | 无影响 |

## 执行计划

### Phase 1: 导出函数与配置修改

#### ✅ Task 1.1: config.toml 新增 `[export]` 节
- **目标**：提供 `min_en_key_len` 配置项
- **修改内容**：
  - 文件 `config.toml`：在 `[artifacts]` 节之后新增 `[export]` 节，包含 `min_en_key_len = 3` 及注释说明
- **修改边界**：不得修改 `[sources]`、`[extract]`、`[artifacts]`、`[rime]` 节
- **测试要求**：
  - 运行 `python3 -c "import tomllib; print(tomllib.load(open('config.toml','rb'))['export'])"`
  - 预期输出：`{'min_en_key_len': 3}`
- **验收标准**：
  - ✅ `config.toml` 包含 `[export]` 节且 `min_en_key_len = 3`
  - ✅ TOML 语法合法（上述命令无异常）
- **潜在风险**：其他管线代码可能用 `cfg["export"]` 做了意外判断——实际 grep 确认无此情况

#### ✅ Task 1.2: 修改 `export_translation_dict()` 实现短键隔离
- **目标**：将短 ASCII en 键分流到 `en2zh_short`，附带 concept_id
- **修改内容**：
  - 文件 `pipeline/export_registry.py`，函数 `export_translation_dict()`（约 L496-556）：
    1. 函数签名新增 `min_en_key_len: int = 3` 参数
    2. 在 en2zh 填充循环中，额外记录 `en2zh_concept: dict[str, str]`，映射 `alias → concept_id`
    3. 循环结束后，分区 en2zh：
       ```python
       en2zh_short: dict[str, dict[str, str]] = {}
       for key in list(en2zh):
           if key.isascii() and len(key) < min_en_key_len:
               en2zh_short[key] = {"zh": en2zh.pop(key), "concept_id": en2zh_concept[key]}
       ```
    4. payload 中 `schema_version` 改为 2，新增 `en2zh_short` 字段
    5. metadata 新增 `pairs_en2zh_short: len(en2zh_short)`
    6. return dict 新增 `pairs_en2zh_short`
- **修改边界**：不得修改 `export_vale_terms`、`export_query_expansions`、`export_tag_rules`、`export_substitutions_tsv`、`export_vale_substitute_yaml` 等其他导出函数。不得修改 `_iter_alias_rows` / `_iter_concept_rows`。不得修改 `zh2en` 构建逻辑。
- **测试要求**：
  - 运行 `pytest tests/test_export_registry_translation_dict.py -v`
  - 预期输出：全部通过（在 Task 2.2 更新断言后）
- **验收标准**：
  - ✅ `en2zh` 中不包含任何 `key.isascii() and len(key) < 3` 的键
  - ✅ `en2zh_short` 中每个 value 都有 `zh` 和 `concept_id` 两个字段
  - ✅ `en2zh` 与 `en2zh_short` 的键集合不相交
  - ✅ `en2zh` 键数 + `en2zh_short` 键数 = 原 en2zh 键数（无丢失）
  - ✅ `schema_version == 2`
- **潜在风险**：`en2zh_concept` 字典可能遗漏某些 alias（如果 alias 被跳过但已进入 en2zh）——实际上跳过条件与进入 en2zh 的条件互斥，不会发生；但应在循环中同步维护两个 dict

#### ✅ Task 1.3: `main()` 传递 config 中的 `min_en_key_len`
- **目标**：将 config.toml 中的阈值传入导出函数
- **修改内容**：
  - 文件 `pipeline/export_registry.py`，函数 `main()`（约 L640-643）：
    - 在 `do_translation` 分支中，从 `cfg` 读取 `min_en_key_len`：
      ```python
      min_en_key_len = cfg.get("export", {}).get("min_en_key_len", 3)
      ```
    - 传给 `export_translation_dict(..., min_en_key_len=min_en_key_len)`
- **修改边界**：不得修改 `main()` 中其他导出调用（vale、query-expansions、tag-rules 等）。不得新增 CLI 参数。
- **测试要求**：
  - 运行 `pytest tests/test_export_registry_translation_dict.py::test_translation_dict_cli_flag -v`
  - 预期输出：通过
- **验收标准**：
  - ✅ `main()` 读取 `cfg["export"]["min_en_key_len"]` 且缺失时回退默认值 3
  - ✅ 该值传入 `export_translation_dict()` 的 `min_en_key_len` 参数
- **潜在风险**：config 中 `min_en_key_len` 为非整数（如字符串）会导致比较异常——TOML 的 `min_en_key_len = 3` 解析为 int，无此问题

### Phase 2: 测试更新

#### ✅ Task 2.1: 新增 `test_translation_dict_short_en_keys_segregated`
- **目标**：验证短键隔离逻辑的正确性
- **修改内容**：
  - 文件 `tests/test_export_registry_translation_dict.py`：新增测试函数，创建包含以下场景的 mini registry：
    - 一个 concept 有单字母 abbr alias（如 `D → deuterium`）
    - 一个 concept 有 2 字母 abbr alias（如 `CS → central-solenoid`）
    - 一个 concept 有 3 字母 abbr alias（如 `TBR → tritium-breeding-ratio`）
    - 一个 concept 有非 ASCII 短键（如 `β → beta`）
  - 断言：
    - `D` 和 `CS` 出现在 `en2zh_short`，不出现在 `en2zh`
    - `TBR` 出现在 `en2zh`，不出现在 `en2zh_short`
    - `β` 出现在 `en2zh`，不出现在 `en2zh_short`
    - `en2zh_short["D"]` 有 `zh` 和 `concept_id` 字段
    - `schema_version == 2`
    - `metadata["pairs_en2zh_short"]` 等于 `len(en2zh_short)`
- **修改边界**：不得修改已有测试函数的核心逻辑。仅在此测试函数内动作。
- **测试要求**：
  - 运行 `pytest tests/test_export_registry_translation_dict.py::test_translation_dict_short_en_keys_segregated -v`
  - 预期输出：1 passed
- **验收标准**：
  - ✅ 测试函数通过
  - ✅ 覆盖单字母、双字母、阈值边界（3 字母）、非 ASCII 四种场景
- **潜在风险**：测试中创建的 evidence.tsv 格式需与 validator 期望一致（2 列格式）——已有其他测试证实这行

#### ✅ Task 2.2: 更新已有测试的 schema_version 断言
- **目标**：已有测试适配 schema_version=2
- **修改内容**：
  - 文件 `tests/test_export_registry_translation_dict.py`：
    - `test_translation_dict_basic`（L81）：将 `assert data["schema_version"] == 1` 改为 `== 2`
    - 同测试：验证 `en2zh_short` 存在且为 dict（即使在 basic 测试的 registry 中所有 en 键 ≥3 字符，`en2zh_short` 应为空 dict）
    - 检查其他测试函数是否有 schema_version 断言——仅 basic 有
- **修改边界**：不得修改测试的 registry 数据（concepts/aliases/evidence 内容）。仅修改断言。
- **测试要求**：
  - 运行 `pytest tests/test_export_registry_translation_dict.py -v`
  - 预期输出：全部 passed（≥ 7 个测试 + 1 个新增）
- **验收标准**：
  - ✅ 所有已有测试通过
  - ✅ `test_translation_dict_basic` 断言 `schema_version == 2`
  - ✅ `test_translation_dict_basic` 断言 `"en2zh_short" in data`
- **潜在风险**：`test_translation_dict_abbr_aliases` 中 "CFETR"（5 字符）不受影响，但需确认 "CFETR" 不会意外进入 en2zh_short——len("CFETR")=5 ≥ 3，安全

### Phase 3: 产物重建与验证

#### ✅ Task 3.1: 重新生成 translation_dict.json 并验证
- **目标**：用更新后的代码生成新产物，验证短键已隔离
- **修改内容**：
  - 运行导出命令生成新的 `artifacts/translation_dict.json`
- **修改边界**：不得修改 `artifacts/` 目录下的其他文件
- **测试要求**：
  - 运行 `python3 -m pipeline.export_registry --terms-dir terms --out-dir artifacts --translation-dict --no-vale`
  - 验证命令：
    ```bash
    python3 -c "
    import json
    d = json.load(open('artifacts/translation_dict.json'))
    short = [k for k in d['en2zh'] if k.isascii() and len(k) < 3]
    print(f'en2zh: {len(d[\"en2zh\"])} pairs')
    print(f'en2zh_short: {len(d[\"en2zh_short\"])} pairs')
    print(f'Leaked short keys in en2zh: {short}')
    assert not short, f'Short keys leaked: {short}'
    assert d['schema_version'] == 2
    print('OK')
    "
    ```
  - 预期输出：`en2zh: ~1880 pairs`、`en2zh_short: ~39 pairs`、`Leaked short keys in en2zh: []`、`OK`
- **验收标准**：
  - ✅ `en2zh` 中无 ASCII 短键（长度 < 3）
  - ✅ `en2zh_short` 包含原来的 39 个短键项
  - ✅ `en2zh` 键数 + `en2zh_short` 键数 ≈ 原 en2zh 键数 1919
  - ✅ schema_version == 2
  - ✅ JSON 文件语法正确、UTF-8 编码
- **潜在风险**：registry 数据自上次生成后可能有变动，导致计数略有偏差——以实际 pair 数为准，关键是 short keys 为空

## 回归检查清单

- [ ] 全量测试通过：`pytest tests/ -v`
- [ ] 无新增 lint 警告：`ruff check pipeline/export_registry.py`
- [ ] `translation_dict.json` 的 `en2zh` 无 ≤2 字符 ASCII 键
- [ ] `en2zh_short` 每个 value 包含 `zh` + `concept_id` 两个字段
- [ ] `zh2en` 内容不变（与修改前对比确认）
- [ ] `registry_exports.json` 包含 `pairs_en2zh_short` 计数
- [ ] 其他导出产物（vale、query_expansions、tag_rules 等）不受影响

## 审查日志

| 轮次 | 聚焦 | 发现问题数 | 已修正 | 剩余 |
|------|------|-----------|--------|------|
| R1 | 结构完整性 | 9 | 9 | 0 |
| R2 | 可执行性 | 4 | 4 | 0 |
| R3 | 风险与边缘 | 3 | 3 | 0 |
| R4 | 自由审查 | 0 | 0 | 0 |
| **终止** | **T5 — 指标驱动收敛** | | | **0** |

### Completion Summary

| 维度 | 结果 |
|------|------|
| 背景与目标 | 完整（含非目标 4 项 + 复用分析 4 项） |
| 技术方案 | 完整（5 个设计决策 + 4 文件影响范围） |
| Error & Rescue Map | 5 条路径已覆盖，0 CRITICAL GAP |
| 执行计划 | 3 Phase、6 Task |
| 回归检查清单 | 7 项（含项目特定检查） |
| 已知局限 | 外部消费端若严格校验 schema_version==1 需自行适配 |

### R1 Issues
- **Issue R1-1**: 缺"非目标"节 → 补充 4 项非目标 ✅ 已修正
- **Issue R1-2**: Task 1.1 缺测试/验收/风险字段 → 补全 ✅ 已修正
- **Issue R1-3**: Task 1.2 缺具体测试命令和验收标准 → 补全 5 条验收标准 ✅ 已修正
- **Issue R1-4**: Task 1.3 缺具体测试和验收 → 补全 ✅ 已修正
- **Issue R1-5**: Task 2.1/2.2 缺具体测试命令 → 补全 pytest 命令 ✅ 已修正
- **Issue R1-6**: Task 3.1 缺具体验证命令 → 补全 python 验证脚本 ✅ 已修正
- **Issue R1-7**: 缺回归检查清单 → 新增 7 项 ✅ 已修正
- **Issue R1-8**: 缺 Error & Rescue Map → 新增 5 条路径 ✅ 已修正
- **Issue R1-9**: 缺代码复用分析 → 列出 4 项复用决策 ✅ 已修正

### R2 Issues
- **Issue R2-1**: Task 1.2 修改边界过于笼统 → 显式列出 5 个不得修改的函数 ✅ 已修正
- **Issue R2-2**: Task 1.3 修改边界过于笼统 → 明确不修改其他导出调用 ✅ 已修正
- **Issue R2-3**: Task 1.1 缺 TOML 语法验证 → 添加 python 验证命令 ✅ 已修正
- **Issue R2-4**: 需确认已有测试 fixture 不会因短键隔离而 break → 逐一核查：basic 测试中 "design"(6), "tritium breeding ratio"(23), "TBR"(3) 均 ≥3，safe ✅ 已修正

### R3 Issues
- **Issue R3-1**: `min_en_key_len=0` 边缘行为未说明 → 在 Error & Rescue Map 中补充（`len(key) < 0` 恒 False） ✅ 已修正
- **Issue R3-2**: `lang=="mixed"` 的短键处理需确认 → 分析确认仅 en2zh 侧受影响，zh2en 不变 ✅ 已修正
- **Issue R3-3**: schema_version=2 兼容性风险 → 在"已知局限"中明确记录 ✅ 已修正
