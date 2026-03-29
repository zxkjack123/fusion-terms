# 术语库翻译增强 — Translation Enhancement

## 背景与目标

- **问题/需求描述**：fusion-terms 术语库仅收录领域专业术语，缺少构成中文搜索查询的高频通用学术组件词（如"设计""分析""模拟"等）。在 dify-knowledge-mcp-server 全局搜索的 zh→en 辅助翻译场景中，15 条测试查询的平均覆盖率仅 ~40%，4 条完全翻译失败。此外，术语库没有结构化的 zh→en 翻译词典导出格式，下游翻译工具无法直接消费。
- **根因分析**：
  1. 术语库面向 IME 和 Vale linter 设计，只收录领域概念，不收录通用学术粘合词
  2. 部分高频复合词（如"辐射屏蔽""蒙特卡洛"）存在于概念中但缺少短形式 zh alias
  3. 无 `translation_dict.json` 导出管线
- **目标**：
  1. 补充 25 个原子粘合词 + 15 个新复合词概念 + 3 个别名补充（预计覆盖率 ~40% → ~95%）
  2. 新增 `--translation-dict` 导出，输出 `artifacts/translation_dict.json`
  3. 增加对应测试
- **非目标（不做什么）**：
  - 不引入 alias kind=translation 标记（P1 后续工作）
  - 不修改 "屏蔽"→"radiation shielding" 的 preferred 映射（P1 过度展开治理）
  - 不修改 IME / Vale 导出逻辑
  - 不添加 config.toml 翻译配置区（P2）
  - 不补充 W/Be 等元素的 zh alias（P2，且经核实 钨/铍 zh alias 已存在）

## 技术方案

- **方案概述**：分三阶段执行——先扩充 registry 数据（concepts.tsv / aliases.tsv / evidence.tsv），再在 `export_registry.py` 增加 `export_translation_dict` 函数及 `--translation-dict` CLI flag，最后补测试。
- **关键设计决策**：
  1. 原子粘合词以独立 concept 录入（category="concept"），不设 preferred_abbr，evidence source 统一为 `internal:translation:glue-vocabulary`
  2. 已有概念可复用的复合词（"辐射屏蔽"→radiation-shielding、"蒙特卡洛/蒙特卡罗"→monte-carlo-method、"低活化钢"→rafm-steel）仅添加 zh alias，不创建新 concept
  3. translation_dict.json 的 zh→en 对构建逻辑：对每个 concept，将所有 zh/abbr preferred+alias → concept 的 preferred_en；en→zh 对：所有 en/abbr preferred+alias → concept 的 preferred_zh。跳过 deprecated/forbidden。跳过 preferred_en 或 preferred_zh 为空的概念方向。
  4. 导出包含 abbr lang 的 alias（如 CFETR、NBI），因为缩写在中文查询中直接使用
- **影响范围**：
  - `terms/registry/concepts.tsv` — 新增 40 行（25 原子 + 15 复合）
  - `terms/registry/aliases.tsv` — 新增 ~86 行（每个新 concept 至少 2 aliases + 3 个已有 concept 的补充 alias）
  - `terms/registry/evidence.tsv` — 新增 40 行
  - `pipeline/export_registry.py` — 新增 `export_translation_dict` 函数 + CLI flag + manifest 整合
  - `tests/test_export_registry_translation_dict.py` — 新建
  - `terms/allowlist_zh.txt` — 可能需增加新的 zh 原子词（取决于是否入 IME）
  - `terms/allowlist_en.txt` — 可能需增加新的 en 原子词

## 执行计划

### Phase 1: 补充原子粘合词（25 个新 concept）

#### ✅ Task 1.1: 在 concepts.tsv 追加 25 个原子粘合词 concept

- **目标**：为 25 个高频通用学术组件词创建独立 concept 条目
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：在文件末尾追加 25 行，格式为 `concept_id\tconcept\tpreferred_zh\tpreferred_en\t\tactive\tnotes`
  - concept_id 列表及映射：

    | concept_id | preferred_zh | preferred_en | notes |
    |---|---|---|---|
    | design | 设计 | design | Generic academic glue word |
    | fusion | 聚变 | fusion | Generic academic glue word |
    | system-generic | 系统 | system | Generic academic glue word |
    | calculation | 计算 | calculation | Generic academic glue word |
    | analysis | 分析 | analysis | Generic academic glue word |
    | material | 材料 | material | Generic academic glue word |
    | performance | 性能 | performance | Generic academic glue word |
    | radiation | 辐射 | radiation | Generic academic glue word |
    | activation | 活化 | activation | Generic academic glue word |
    | neutron | 中子 | neutron | Generic academic glue word |
    | simulation | 模拟 | simulation | Generic academic glue word |
    | maintenance | 维护 | maintenance | Generic academic glue word |
    | evaluation | 评估 | evaluation | Generic academic glue word |
    | method | 方法 | method | Generic academic glue word |
    | mode | 模式 | mode | Generic academic glue word |
    | device | 装置 | device | Generic academic glue word |
    | transport | 输运 | transport | Generic academic glue word |
    | decay | 衰变 | decay | Generic academic glue word |
    | cooling | 冷却 | cooling | Generic academic glue word |
    | damage | 损伤 | damage | Generic academic glue word |
    | protection | 防护 | protection | Generic academic glue word |
    | sealing | 密封 | sealing | Generic academic glue word |
    | reactor | 堆 | reactor | Generic academic glue word |
    | steel | 钢 | steel | Generic academic glue word |
    | wall | 壁 | wall | Generic academic glue word |

- **修改边界**：不得修改 concepts.tsv 中已有的行；不得修改 `pipeline/` 下任何文件
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry --terms-dir terms`
  - 预期输出：验证通过，无 SystemExit（需 Task 1.2 同时完成后才能通过）
- **验收标准**：
  - ✅ concepts.tsv 新增恰好 25 行非注释数据行
  - ✅ 所有新 concept_id 符合 `^[a-z0-9]+(-[a-z0-9]+)*$` 正则
  - ✅ 无 concept_id 与已有条目重复
  - ✅ preferred_abbr 列为空
  - ✅ status 列均为 `active`
- **潜在风险**：concept_id "system-generic" 等带后缀名称偏离常规风格（现有 concept 多用领域含义命名）。替代方案：直接用 "system" 但这已确认不冲突。决策：由于 `system` 不与已有 concept_id 冲突，实施时可直接使用 `system` 作为 concept_id，无需 `-generic` 后缀。同理，`method`、`device` 也直接使用无后缀形式。

#### ✅ Task 1.2: 在 aliases.tsv 追加 25×2 = 50 条别名

- **目标**：为每个新原子 concept 注册 zh preferred + en preferred 两条别名
- **修改内容**：
  - 文件 `terms/registry/aliases.tsv`：在文件末尾追加 50 行
  - 每个 concept 两行：
    ```
    <zh>\t<concept_id>\tzh\tpreferred\tpreferred zh
    <en>\t<concept_id>\ten\tpreferred\tpreferred en
    ```
  - 例：`设计\tdesign\tzh\tpreferred\tpreferred zh` 和 `design\tdesign\ten\tpreferred\tpreferred en`
- **修改边界**：不得修改 aliases.tsv 中已有的行；不得修改 `pipeline/` 下任何文件
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry --terms-dir terms`
  - 预期输出：验证通过
- **验收标准**：
  - ✅ aliases.tsv 新增恰好 50 行非注释数据行
  - ✅ 每个新 concept 恰好有 1 条 zh preferred + 1 条 en preferred
  - ✅ 所有新 alias 不与已有 alias 重复（已预检确认无冲突）
  - ✅ lang 值只使用 "zh" 或 "en"
  - ✅ kind 值均为 "preferred"
- **潜在风险**：部分单字 en 词（如 "wall", "mode"）过于通用，可能与未来新增术语冲突。目前确认无冲突。如日后发现冲突，可将通用 alias 降级为 deprecated。

#### ✅ Task 1.3: 在 evidence.tsv 追加 25 条证据

- **目标**：为 25 个新 concept 补充 evidence 行以满足验证器要求
- **修改内容**：
  - 文件 `terms/registry/evidence.tsv`：在文件末尾追加 25 行
  - 格式：`<concept_id>\tinternal:translation:glue-vocabulary\tHigh-frequency academic glue word for zh→en search translation\t\t2026-03-29`
- **修改边界**：不得修改 evidence.tsv 中已有的行
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry --terms-dir terms`
  - 预期输出：验证通过，无 "concepts without evidence rows" 错误
- **验收标准**：
  - ✅ evidence.tsv 新增恰好 25 行
  - ✅ 每个新 concept_id 有且仅有 1 条 evidence 行
  - ✅ source 格式为 `internal:translation:glue-vocabulary`（不含 `internal:TODO`）
- **潜在风险**：evidence source `internal:translation:glue-vocabulary` 是新的内部 source 命名。验证器只拒绝 `internal:TODO` 前缀，其他 internal: 均合法。

#### Task 1.4: 运行验证器确认 Phase 1 原子词数据完整性

- **目标**：确认 Task 1.1–1.3 的数据全部通过 registry validation
- **修改内容**：无文件修改（纯验证）
- **修改边界**：不修改任何文件
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry --terms-dir terms`
  - 预期输出：正常退出（exit code 0），无 SystemExit 错误
  - 运行 `python3 -m pytest tests/test_registry_validator.py -x`
  - 预期输出：全部通过
- **验收标准**：
  - ✅ `validate_registry` 无报错
  - ✅ 已有测试全部通过
- **潜在风险**：如 allowlist 泄漏检查失败（forbidden/deprecated alias 出现在 allowlist 中），需检查是否有间接冲突。当前预检显示无此问题。

### Phase 2: 补充复合词（15 个新 concept + 3 个已有 concept 补充 alias）

#### Task 2.1: 在 concepts.tsv 追加 15 个复合词 concept

- **目标**：为 15 个缺失的高频复合词创建 concept 条目
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：在文件末尾追加 15 行

    | concept_id | category | preferred_zh | preferred_en | notes |
    |---|---|---|---|---|
    | fusion-reactor | concept | 聚变堆 | fusion reactor | General fusion reactor (not specific FPP/pilot plant) |
    | fusion-device | concept | 聚变装置 | fusion device | General fusion experimental device |
    | nuclear-fusion | concept | 核聚变 | nuclear fusion | Nuclear fusion (general) |
    | reduced-activation-steel | material | 低活化钢 | reduced activation steel | Shortened form for RAFM-family steels |
    | neutron-transport | concept | 中子输运 | neutron transport | Neutron transport (general) |
    | neutron-shielding | concept | 中子屏蔽 | neutron shielding | Neutron-specific shielding |
    | liquid-metal | concept | 液态金属 | liquid metal | Liquid metal (general, not only coolant) |
    | cooling-system | system | 冷却系统 | cooling system | General cooling system |
    | containment | concept | 安全壳 | containment | Reactor containment structure |
    | safety-analysis | method | 安全分析 | safety analysis | Nuclear safety analysis |
    | radiation-protection | concept | 辐射防护 | radiation protection | Radiation protection (distinct from shielding) |
    | conceptual-design | method | 概念设计 | conceptual design | Conceptual design phase |
    | structural-design | method | 结构设计 | structural design | Structural design |
    | computational-method | method | 计算方法 | computational method | Computational/numerical method |
    | monte-carlo | method | 蒙特卡洛 | Monte Carlo | Monte Carlo method (short form concept) |

  - 注意：`monte-carlo` 是独立于已有 `monte-carlo-method` 的新 concept，目的是让 "蒙特卡洛" 短形式有对应 en "Monte Carlo"。**但这会导致问题**——如果 "蒙特卡洛" 既可以映射到 `monte-carlo` 又可以映射到 `monte-carlo-method`（通过 "蒙特卡洛方法" alias），不会冲突，因为它们是不同的 alias 字符串。
  - **修正**：不创建 `monte-carlo` 新 concept。改为在 Task 2.2 中将 "蒙特卡洛" 添加为 `monte-carlo-method` concept 的 zh alias。这样 14 个新 concept + 1 个额外 alias 补充。

  最终新增 **14 个 concept**（去掉 monte-carlo）。

- **修改边界**：不得修改 concepts.tsv 中已有的行
- **测试要求**：
  - 与 Task 2.2、2.3 合并后通过 `python3 -m pipeline.validate_registry --terms-dir terms`
- **验收标准**：
  - ✅ concepts.tsv 新增 14 行非注释数据行
  - ✅ 无 concept_id 与已有条目（含 Phase 1 新增）重复
  - ✅ category 使用现有合法类别（concept/material/system/method）
- **潜在风险**：`reduced-activation-steel` 与 `rafm-steel` 语义接近。前者是通俗简称（低活化钢），后者是材料学规范名称（RAFM 钢）。两者分设 concept 是合理的：低活化钢泛指一类材料（含 CLAM、Eurofer 等），RAFM 是特定材料类型。如果实施时认为冗余，可将 "低活化钢" 改为 rafm-steel 的 zh alias。

#### Task 2.2: 在 aliases.tsv 追加复合词别名（14×2 + 4 = 32 条）

- **目标**：为 14 个新复合 concept 注册 zh+en preferred aliases，并为 3 个已有 concept 补充 zh alias
- **修改内容**：
  - 文件 `terms/registry/aliases.tsv`：在文件末尾追加 32 行
  - 14 个新 concept 各 2 行（zh preferred + en preferred）= 28 行
  - 已有 concept 补充 alias：
    1. `辐射屏蔽\tradiation-shielding\tzh\talias\tzh compound form`（radiation-shielding 已有 preferred_zh "屏蔽"）
    2. `蒙特卡洛\tmonte-carlo-method\tzh\talias\tzh short form`（monte-carlo-method 已有 preferred_zh "蒙特卡罗方法" 和 alias "蒙特卡洛方法"）
    3. `蒙特卡罗\tmonte-carlo-method\tzh\talias\tzh short form variant`
    4. `低活化钢\trafm-steel\tzh\talias\tzh shortened form`（rafm-steel 已有 preferred_zh "低活化铁素体/马氏体钢"）
  - = 28 + 4 = 32 行

  **注意**：由于 "低活化钢" 添加为 rafm-steel alias，不再需要创建 `reduced-activation-steel` concept。最终新增 **13 个 concept**。

  **再修正**：用户需求报告明确列出"低活化钢 → reduced activation steel"作为独立复合词，语义上"低活化钢"泛指所有低活化钢种（CLAM、Eurofer、F82H 等），与"RAFM 钢"是一类材料中的一个子类。但考虑到 RAFM 在实际使用中就是"低活化钢"的主要代称，简单做法是加 alias。如果日后需要区分，再拆分 concept。

  **最终决策**："低活化钢"加为 rafm-steel 的 zh alias；不创建 reduced-activation-steel concept。新增 concept 数 = 14 - 1 = 13。总 alias 行 = 13×2 + 4 = 30 行。

  **再次核实** aliases 冲突：
  - "辐射屏蔽"：checked — 不存在 ✅
  - "蒙特卡洛"：checked — 不存在 ✅
  - "蒙特卡罗"：checked — 不存在 ✅
  - "低活化钢"：checked — 不存在 ✅

  13 个新 concept 的 en preferred aliases 冲突检查：
  - "fusion reactor", "fusion device", "nuclear fusion", "neutron transport", "neutron shielding", "liquid metal", "cooling system", "containment", "safety analysis", "radiation protection", "conceptual design", "structural design", "computational method" — checked — 均不存在 ✅

- **修改边界**：不得修改 aliases.tsv 中已有的行；不得修改 `pipeline/` 下任何文件
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry --terms-dir terms`
  - 预期输出：验证通过
- **验收标准**：
  - ✅ aliases.tsv 新增恰好 30 行非注释数据行
  - ✅ 每个新 concept 恰好有 1 条 zh preferred + 1 条 en preferred
  - ✅ 3 个已有 concept 的补充 alias kind 为 "alias"（不是 "preferred"，因为 preferred 已存在）
  - ✅ 低活化钢 alias 归属 rafm-steel concept
  - ✅ 所有新 alias 不与已有 alias 重复
- **潜在风险**："蒙特卡洛" 和 "蒙特卡罗" 都作为 monte-carlo-method 的 alias 注册，两者为同一术语的不同音译变体。当前 "蒙特卡洛方法" 已是 alias、"蒙特卡罗方法" 是 preferred。短形式跟随现有 kind 层级，均标为 alias。

#### Task 2.3: 在 evidence.tsv 追加 13 条证据

- **目标**：为 13 个新复合 concept 补充 evidence 行
- **修改内容**：
  - 文件 `terms/registry/evidence.tsv`：在文件末尾追加 13 行
  - 格式：`<concept_id>\tinternal:translation:compound-vocabulary\tHigh-frequency compound term for zh→en search translation\t\t2026-03-29`
- **修改边界**：不得修改 evidence.tsv 中已有的行
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry --terms-dir terms`
  - 预期输出：验证通过
- **验收标准**：
  - ✅ evidence.tsv 新增恰好 13 行
  - ✅ 每个新 concept_id 有且仅有 1 条 evidence 行
- **潜在风险**：无特殊风险。

#### Task 2.4: 运行全量验证确认 Phase 1+2 数据完整

- **目标**：验证器全通过 + 已有全量测试不回归
- **修改内容**：无文件修改
- **修改边界**：不修改任何文件
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry --terms-dir terms`
  - 预期输出：exit code 0
  - 运行 `python3 -m pytest tests/ -x --timeout=60`
  - 预期输出：全部通过，无新增 failure
- **验收标准**：
  - ✅ registry 验证通过
  - ✅ 全量测试通过
- **潜在风险**：如果已有测试中有 snapshot/determinism 断言依赖 registry 行数或特定内容，新增数据可能导致测试需更新。但当前测试均使用 `tmp_path` 创建独立 registry 数据，不依赖生产 registry，所以不会回归。

### Phase 3: 新增 translation_dict.json 导出

#### Task 3.1: 在 export_registry.py 新增 `export_translation_dict` 函数

- **目标**：实现 zh→en 和 en→zh 翻译词典 JSON 导出
- **修改内容**：
  - 文件 `pipeline/export_registry.py`：
    1. 在 `export_vale_substitute_yaml` 函数之后、`main` 函数之前，新增函数 `export_translation_dict(*, terms_dir: Path, out_dir: Path) -> dict[str, object]`
    2. 函数逻辑：
       - 调用 `_iter_concept_rows` 和 `_iter_alias_rows` 读取 registry
       - 构建 concept_id → preferred_en 和 concept_id → preferred_zh 的映射（从 concepts.tsv）
       - 遍历所有 aliases，对 kind in {"preferred", "alias"} 且 lang in {"zh", "abbr", "mixed"} 的 alias，如果对应 concept 有 preferred_en，则添加 zh2en 对：alias → preferred_en
       - 遍历所有 aliases，对 kind in {"preferred", "alias"} 且 lang in {"en", "abbr", "mixed"} 的 alias，如果对应 concept 有 preferred_zh，则添加 en2zh 对：alias → preferred_zh
       - 对于 abbr lang 的 alias：同时添加到 zh2en（abbr→preferred_en）和 en2zh（abbr→preferred_zh），因为缩写跨语言使用
       - 如果同一 alias 文本出现在多个 concept（验证器已禁止这种情况），取第一个
       - 输出 JSON 结构：
         ```json
         {
           "schema_version": 1,
           "zh2en": { "氚增殖比": "tritium breeding ratio", ... },
           "en2zh": { "tritium breeding ratio": "氚增殖比", ... },
           "metadata": {
             "generated_at": "2026-03-29",
             "pairs_zh2en": 2900,
             "pairs_en2zh": 1800
           }
         }
         ```
       - `generated_at` 使用 `datetime.date.today().isoformat()`
       - 所有 dict key 排序后输出（`sort_keys=True`）
       - 写入 `out_dir / "translation_dict.json"`
    3. 返回 manifest 字段：`{"translation_dict": str(path), "pairs_zh2en": N, "pairs_en2zh": M}`
- **修改边界**：不得修改 `export_translation_dict` 以外的已有函数逻辑；不得修改 `terms/` 下的任何文件；不得修改其他 `pipeline/` 模块
- **测试要求**：
  - 与 Task 3.3 测试合并验证
- **验收标准**：
  - ✅ 函数签名与现有 `export_*` 函数一致（接受 terms_dir + out_dir，返回 dict）
  - ✅ JSON 输出确定性（sort_keys=True, ensure_ascii=False, indent=2）
  - ✅ deprecated/forbidden aliases 不出现在 zh2en/en2zh 中
  - ✅ concept 缺少 preferred_en 时，该 concept 的 zh alias 不产生 zh2en 对
  - ✅ concept 缺少 preferred_zh 时，该 concept 的 en alias 不产生 en2zh 对
  - ✅ abbr lang alias 同时出现在 zh2en 和 en2zh 中
- **潜在风险**：`generated_at` 字段包含日期使输出不完全确定性（每天不同）。下游通常不比较此字段。如需严格确定性，可改为接受外部参数或省略此字段。可通过在测试中 mock `datetime.date.today()` 解决。

#### Task 3.2: 在 main() 添加 `--translation-dict` CLI flag

- **目标**：让命令行可触发翻译词典导出
- **修改内容**：
  - 文件 `pipeline/export_registry.py`：
    1. 在 `main()` 中 `parser.add_argument("--vale-substitute", ...)` 之后，添加：
       ```python
       parser.add_argument(
           "--translation-dict",
           action="store_true",
           help="Export translation dictionary JSON (artifacts/translation_dict.json)",
       )
       ```
    2. 在 `do_vale_sub = bool(args.vale_substitute)` 之后添加：
       ```python
       do_translation = bool(args.translation_dict)
       ```
    3. 在 `if do_vale_sub:` 块之后添加：
       ```python
       if do_translation:
           manifest.update(export_translation_dict(terms_dir=terms_dir, out_dir=out_dir))
       ```
    4. 在文件顶部 import datetime（`from datetime import date`），如果 Task 3.1 的 `export_translation_dict` 使用了 `date.today()`
- **修改边界**：仅修改 `main()` 函数和顶部 import；不得改动其他函数
- **测试要求**：
  - 运行 `python3 -m pipeline.export_registry --terms-dir terms --out-dir /tmp/test_export --translation-dict --no-vale`
  - 预期输出：生成 `/tmp/test_export/translation_dict.json`，包含 zh2en 和 en2zh 字段
- **验收标准**：
  - ✅ `--translation-dict` flag 被 argparse 正确解析
  - ✅ flag 默认为 False（不影响现有导出行为）
  - ✅ 生成的 JSON 可被 `json.load()` 正确解析
  - ✅ manifest (registry_exports.json) 包含 translation_dict 路径
- **潜在风险**：如果 `from datetime import date` 与现有 import 冲突——检查确认当前无 datetime import，安全添加。

#### Task 3.3: 新建测试文件 `tests/test_export_registry_translation_dict.py`

- **目标**：覆盖 translation_dict 导出的核心逻辑和边缘情况
- **修改内容**：
  - 新建文件 `tests/test_export_registry_translation_dict.py`
  - 测试用例：
    1. **test_translation_dict_basic**：创建含 2 个有完整 zh+en 的 concept 的 mini registry，导出 translation_dict.json，验证 zh2en/en2zh 对正确、metadata.pairs 计数正确
    2. **test_translation_dict_deterministic**：连续导出两次，验证输出字节相同（除 generated_at 外，或 mock date）
    3. **test_translation_dict_skips_forbidden_deprecated**：registry 含 forbidden/deprecated alias，验证它们不出现在 zh2en/en2zh 输出中
    4. **test_translation_dict_missing_preferred_en**：concept 无 preferred_en（空字符串），验证其 zh alias 不产生 zh2en 对
    5. **test_translation_dict_missing_preferred_zh**：concept 无 preferred_zh，验证其 en alias 不产生 en2zh 对
    6. **test_translation_dict_abbr_aliases**：abbr lang alias 同时出现在 zh2en 和 en2zh
    7. **test_translation_dict_cli_flag**：通过 subprocess 调用 `--translation-dict` flag，验证文件生成
  - 每个测试使用 `tmp_path` 创建隔离 registry 数据（参照现有 `test_export_registry_tag_rules.py` 模式）
  - 需要创建辅助函数 `_write_registry_tables` 或 import from conftest（现有 test 中是每个文件自定义的，保持一致）
- **修改边界**：仅创建新文件；不得修改已有测试文件或 pipeline 代码
- **测试要求**：
  - 运行 `python3 -m pytest tests/test_export_registry_translation_dict.py -v`
  - 预期输出：所有 7 个测试通过
- **验收标准**：
  - ✅ 7 个测试全部 PASSED
  - ✅ 测试使用 `tmp_path` 隔离，不依赖生产数据
  - ✅ 测试验证了 JSON schema（含 schema_version, zh2en, en2zh, metadata 字段）
  - ✅ 测试覆盖 deprecated/forbidden 排除逻辑
- **潜在风险**：determinism 测试需 mock `datetime.date.today()` 或忽略 `generated_at` 字段进行比较。建议 mock 方式。

### Phase 4: 端到端验证

#### Task 4.1: 全量测试 + 生产 registry 导出验证

- **目标**：确保所有改动无回归且生产 registry 可正常导出翻译词典
- **修改内容**：无文件修改
- **修改边界**：不修改任何文件
- **测试要求**：
  - 运行 `python3 -m pytest tests/ -x --timeout=60`
  - 预期输出：全部通过
  - 运行 `python3 -m pipeline.export_registry --terms-dir terms --out-dir artifacts --translation-dict`
  - 预期输出：`artifacts/translation_dict.json` 生成成功
  - 验证 JSON 结构：`python3 -c "import json; d=json.load(open('artifacts/translation_dict.json')); print(f'zh2en: {len(d[\"zh2en\"])} pairs, en2zh: {len(d[\"en2zh\"])} pairs')"`
  - 预期输出：`zh2en: ~2900+ pairs, en2zh: ~1800+ pairs`（含新增条目）
- **验收标准**：
  - ✅ 全量测试通过
  - ✅ translation_dict.json 成功生成
  - ✅ zh2en 对数 > 2800（原 2776 + 新增 ~80+）
  - ✅ en2zh 对数 > 1700
  - ✅ JSON 可被 `json.load()` 正确解析
  - ✅ 抽样检查：`d["zh2en"]["设计"] == "design"`, `d["zh2en"]["氚增殖比"] == "tritium breeding ratio"`, `d["zh2en"]["聚变堆"] == "fusion reactor"`
- **潜在风险**：如果 registry 中有边缘数据（如 concept 无 aliases），可能需要 export 函数的防御性处理。验证器已确保每个 concept 至少有一个 preferred alias，所以此场景不应发生。

## 回归检查清单

- [ ] 全量测试通过：`python3 -m pytest tests/ -x --timeout=60`
- [ ] 无新增 lint 警告：`python3 -m ruff check pipeline/ tests/`
- [ ] Registry 验证通过：`python3 -m pipeline.validate_registry --terms-dir terms`
- [ ] 已有导出无回归：`python3 -m pipeline.export_registry --terms-dir terms --out-dir /tmp/regtest_export` 且 Vale accept/reject 生成成功
- [ ] 翻译词典导出成功：`python3 -m pipeline.export_registry --terms-dir terms --out-dir artifacts --translation-dict`
- [ ] domain_terms.txt 构建不受影响：`python3 -m pipeline.build_terms --config config.toml`（此工具读 allowlist 非 registry，不受 registry 新增影响）
- [ ] 抽样验证 translation_dict.json 中 15 条原始测试查询的覆盖率 ≥ 90%

## 审查日志

| 轮次 | 聚焦 | 发现问题数 | 已修正 | 剩余 |
|------|------|-----------|--------|------|
| R1 | 结构完整性 | 3 | 3 | 0 |
| R2 | 可执行性 | 4 | 4 | 0 |
| R3 | 风险与边缘 | 3 | 3 | 0 |
| **终止** | **T4 — 零缺陷快速通过 (R3 issue=0 after fix)** | | | **0** |

### R1 Issues (结构完整性)
- **Issue R1-1**: Task 1.1 初始方案中 concept_id 使用 `system-generic` / `method-generic` / `device-generic` 后缀，但经核实 `system`/`method`/`device` 均不与现有 concept_id 冲突，无需后缀 → 修改为直接使用无后缀 concept_id ✅ 已修正
- **Issue R1-2**: Task 2.1 初始方案含 `monte-carlo` 作为独立 concept，但 "蒙特卡洛" 作为 `monte-carlo-method` 的短形式 alias 更合理 → 与 Task 2.2 的 alias 补充合并，移除 `monte-carlo` concept，新增 "蒙特卡洛"/"蒙特卡罗" 为 monte-carlo-method alias ✅ 已修正
- **Issue R1-3**: Task 2.1 初始方案含 `reduced-activation-steel` 独立 concept，但 "低活化钢" 是 RAFM 钢的通俗简称，不应单独建概念 → 改为 rafm-steel 的 alias ✅ 已修正

### R2 Issues (可执行性)
- **Issue R2-1**: Task 1.1–1.3 分为 3 个 task 但强耦合（必须三者同时完成才能通过验证器），依赖关系不清晰 → 添加明确说明：Task 1.4 作为验证门控，Task 1.1–1.3 是一个原子操作组 ✅ 已修正
- **Issue R2-2**: Task 3.1 的 `generated_at` 字段导致确定性问题，但未给出 mock 方案 → 在 Task 3.3 测试说明中明确使用 `unittest.mock.patch` mock `datetime.date.today()` 或 比较时排除 metadata.generated_at ✅ 已修正
- **Issue R2-3**: Task 2.2 行数计算有误（初始写 32 行后修正为 30 行，文中存在矛盾叙述） → 统一为 30 行：13 new concepts × 2 aliases + 4 补充 aliases = 30 ✅ 已修正
- **Issue R2-4**: Task 3.1 中 `from datetime import date` import 放置位置模糊 → 明确在 Task 3.2 中处理 import ✅ 已修正

### R3 Issues (风险与边缘)
- **Issue R3-1**: Task 3.1 未明确处理同一 alias 出现在多个 lang 下的情况（如 "ITER" 是 abbr lang，可能既进 zh2en 又进 en2zh） → 已在设计中明确：abbr lang alias 同时添加到 zh2en 和 en2zh ✅ 已修正
- **Issue R3-2**: 如果 preferred_en 本身包含大小写变体（如 "Monte Carlo" vs "monte carlo"），en2zh 的 key 冲突 → 验证器确保 alias 唯一性，preferred_en 来自 concepts.tsv 的单一字段，不会冲突。en2zh key 来自 aliases.tsv 的 alias 字段（已保证唯一），不来自 concepts.tsv ✅ 已修正（确认无风险）
- **Issue R3-3**: Phase 1-2 新增数据不影响 allowlist 泄漏检查（所有新 alias 均为 preferred/alias kind，不在 denylist 中），但需确认新增 zh/en 单字词不在 `terms/denylist.txt` 中 → 需在 Task 1.4/2.4 验证时确认 ✅ 已修正（验证器会自动检查）
