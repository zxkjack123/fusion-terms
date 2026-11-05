# Repo Hardening v2026.04.14 — Review-Driven Fixes

## 背景与目标

- **问题/需求描述**：2026-04-14 仓库审阅（[full-repo-2026-04-14.md](../reviews/full-repo-2026-04-14.md)）发现 2 🔴 / 8 🟡 / 7 🟢 共 17 项问题。本计划覆盖全部 2 🔴 和 8 🟡，以及 4 项高性价比 🟢。
- **根因分析**：
  - B1/B2：`rime_import_safe.py` 的 backup/rollback 从早期原型演进至今，rollback 路径"先删后拷"若中途失败导致不可恢复的数据丢失
  - Q1-Q3：CI 从"先有再说"演进到 lint/type-check/coverage 全通过，但门禁仍停在初始松阈值
  - Q4-Q6：registry 从 ~200 概念增长到 1493，验证器和导出函数的防御性检查未同步跟上
  - O1：`export_registry.py` 16% 覆盖率——历史上依赖 CLI 集成测试间接触发，缺少直接 unit test
- **目标**：
  1. 消除唯一的用户数据损坏风险路径（B1 + B2）
  2. CI 门禁提升到与当前代码质量匹配的阈值
  3. 补全 `definitions.tsv` 验证 + 导出函数防御性检查
  4. `export_registry.py` 覆盖率从 16% 提升到 ≥50%
  5. 处理低成本高收益的 🟢 项（timeout 处理、swallowed exceptions、plan 归档）
- **非目标（不做什么）**：
  - 不新增 registry 数据（概念/别名/evidence/definitions）
  - 不重构 `extract_candidates.py`（Q1 在上一轮 repo-improvement 中已标注为低优先级）
  - 不将 coverage 门禁提到 60%+ — 本轮只提到 45% 保守值，后续按需再提
  - 不重构 `rime_export.py` 的 0% coverage 统计问题（O2，需要 pytest-subprocess 或 cov-context 配置变更，收益低）
  - 不涉及 `scripts/batches/` 归档（O4，纯组织工作，不影响质量）
  - 不涉及中文定义导入（O5，长期数据建设项目）
- **已有代码/流程复用分析**：
  - `_copy_any()` 辅助：复用，rollback 修复不改变此函数签名
  - `_run_importer_v2()` 辅助：复用，timeout 处理在调用侧添加
  - `_iter_tsv_rows()` 辅助：复用，definitions 验证扩展仍使用此解析器
  - `test_rime_import_safe.py` 现有 8 个测试：复用，新增测试追加到同文件
  - `test_rime_rollback_guard.py` 现有 2 个测试：复用，不修改

## 技术方案

- **方案概述**：分 4 个 Phase，从最高风险（数据安全）到最低风险（文档整理），每 Phase 独立可 commit。
- **关键设计决策**：

  | 决策点 | 选择 | 理由 |
  |--------|------|------|
  | rollback 原子性策略 | restore-to-temp → `os.replace()` | 比"snapshot-before-restore"更简单，对文件可直接原子替换；对目录用 rename（同文件系统内原子） |
  | backup 事务性策略 | build-in-temp-dir → atomic rename | 确保要么完整 snapshot 要么无 snapshot，不留半成品 |
  | CI coverage 提升幅度 | 30% → 45% | 当前实际 47%，45% 留 2% margin 防波动；不激进到 60% 因为 rime_export 0% 统计问题还在 |
  | definitions 验证范围 | schema 4列 + (cid,lang) 唯一 + source 非空 | 与 aliases.tsv / evidence.tsv 验证深度对齐，不引入"每概念必须有定义"约束（当前只 1550/1493 概念有定义） |
  | export 函数防御性检查 | 函数内 raise，不依赖外部 validator | 使函数在测试/脚本直接调用时也安全 |

- **影响范围**：

  | 文件 | Phase | 变更类型 |
  |------|-------|----------|
  | `pipeline/rime_import_safe.py` | 1 | 修改 `create_backup()` + `rollback_from_manifest()` |
  | `tests/test_rime_import_safe.py` | 1 | 追加 3 个 partial-failure 测试 |
  | `.github/workflows/ci.yml` | 2 | 修改 3 行（cov 阈值 + 移除 `\|\| true`） |
  | `pipeline/validate_registry.py` | 2 | 修改 definitions 验证区块（~220 行附近） |
  | `tests/test_registry_validator.py` | 2 | 追加 definitions 验证测试 |
  | `pipeline/export_registry.py` | 2 | 修改 `_collect_substitutions()` + `export_query_expansions()` |
  | `tests/test_export_registry_substitutions.py` | 3 | 追加 unit test |
  | `tests/test_export_registry_query_expansions.py` | 3 | 追加 unit test |
  | `pipeline/release_pack.py` | 4 | 追加 `TimeoutExpired` handler |
  | `pipeline/generate_dict_yaml.py` | 4 | 修改 swallowed exception + error context |
  | `pipeline/rime_export.py` | 4 | 修改 error context |
  | `.github/plans/` (5 files) | 4 | 添加归档标记 |
  | `pyproject.toml` | 4 | 添加 `[tool.mypy]` 配置 |

## Error & Rescue Map（关键失败路径映射）

| 操作 | 可能的失败 | 已处理？ | 处理方式 | 用户可见行为 |
|------|-----------|---------|---------|------------|
| 原子 rollback: `os.replace()` 对目录 | 跨文件系统 rename 失败 | Y | fallback 到 `shutil.move()` + 错误消息 | 错误中止，原始文件保留 |
| 原子 backup: temp dir rename | 目标名称已存在（竞态） | Y | `exist_ok=False` 在 mkdir 已保护 | 错误中止，temp 清理 |
| CI cov 提升到 45% | 实际覆盖率因 rime_export 0% 拖低 | Y | 当前 47% > 45%，且 Phase 3 新增 export_registry tests 提高覆盖率 | CI 通过 |
| definitions 验证新增 source 非空检查 | 现有数据有空 source | Y | 已验证全部 1550 行均为 4 列且 source 非空 | 无影响 |
| export 函数冲突检查 | 假阳性——合法的相同 alias 跨 concept | N/A | `validate_registry` 已禁止跨 concept 重复 alias，不会有合法情况 | N/A |

## 执行计划

### Phase 1: 🔴 Critical — Rollback/Backup 原子性修复

#### ✅ Task 1.1: 事务性 `create_backup()`

- **目标**：确保 backup snapshot 要么完整创建，要么完全不存在
- **修改内容**：
  - 文件 `pipeline/rime_import_safe.py`，函数 `create_backup()`（L112-173）：
    1. 在 `backup_root` 下创建临时目录 `_tmp_{backup_name}_{pid}` 替代直接创建 `backup_name` 目录
    2. 所有 `_copy_any()` 操作写入临时目录
    3. manifest 写入使用 `tempfile.mkstemp()` + `os.replace()` 确保原子性
    4. 全部成功后 `os.rename(tmp_dir, snapshot_dir)` 原子化最终目录
    5. 任何异常在 `finally` 中清理临时目录（`shutil.rmtree(tmp_dir, ignore_errors=True)`）
- **修改边界**：不得修改 `rollback_from_manifest()`（Task 1.2 负责）；不得修改 `_copy_any()`；不得修改 `BackupItem` dataclass；不得修改 `_run_importer_v2()`
- **测试要求**：
  - 运行 `python3 -m pytest tests/test_rime_import_safe.py -q`
  - 预期：全部通过（现有 8 个 + Task 1.3 新增的测试）
  - 手动验证：在 `_copy_any` 第 2 次调用处模拟异常 → `backup_root` 下无残留目录
- **验收标准**：
  - ✅ `create_backup()` 成功时 `backup_root / backup_name` 存在且含完整 manifest
  - ✅ `create_backup()` 中途失败时 `backup_root / backup_name` 不存在
  - ✅ manifest.json 经过 temp-file + `os.replace()` 写入
  - ✅ 现有 8 个 test 全部通过
- **潜在风险**：`os.rename()` 不能跨文件系统——但 `tmp_dir` 和 `snapshot_dir` 同在 `backup_root` 下，同文件系统

#### ✅ Task 1.2: 安全 `rollback_from_manifest()`

- **目标**：确保 rollback 过程中任一步骤失败时原始文件不丢失
- **修改内容**：
  - 文件 `pipeline/rime_import_safe.py`，函数 `rollback_from_manifest()`（L176-262）：
    1. 对每个 restore item，将 backup 先恢复到同级临时路径（`orig.parent / (orig.name + "._restore_tmp")`）
    2. 验证临时路径存在且完整
    3. 用 `os.replace()` 原子替换目标路径（文件级别原子）；对目录用 `os.rename()`（同文件系统原子）
    4. 如果 `os.rename()` 失败（跨文件系统），fallback：保留原始 + 报错，不执行删除
    5. 清理：成功时删除临时路径残留（如有）
- **修改边界**：不得修改 `create_backup()`（Task 1.1 负责）；不得修改路径安全检查逻辑（protected_roots、path-escape 检查保持不变）；不得修改 manifest 解析逻辑
- **测试要求**：
  - 运行 `python3 -m pytest tests/test_rime_import_safe.py -q`
  - 预期：全部通过
- **验收标准**：
  - ✅ rollback 成功时原始路径恢复到 backup 状态
  - ✅ rollback 中 restore-temp 创建失败时原始路径不变
  - ✅ rollback 中 rename 失败时原始路径不变 + 明确错误消息
  - ✅ 现有 test（含 type-drift、outside-home 等）全部通过
- **潜在风险**：`os.replace()` 对目录非 POSIX 标准，部分平台可能不支持 → 用 `os.rename()` 替代（同文件系统安全）

#### ✅ Task 1.3: 补充 partial-failure 测试

- **目标**：为 backup/rollback 原子性添加针对性测试
- **修改内容**：
  - 文件 `tests/test_rime_import_safe.py`，追加 3 个测试函数：
    1. `test_create_backup_cleans_up_on_copy_failure`：monkeypatch `_copy_any` 在第 2 次调用时 raise `OSError` → 断言 `backup_root / backup_name` 不存在
    2. `test_rollback_preserves_original_on_restore_failure`：构造包含 2 个 item 的 manifest，monkeypatch 使 item 2 的 restore 失败 → 断言 item 1 的 original 仍为 rollback 之前的状态（或已恢复）
    3. `test_rollback_handles_file_restore_atomically`：构造 file-type backup item，验证 restore 后原始文件内容与 backup 一致
- **修改边界**：不得修改 `pipeline/` 代码；不得修改 `conftest.py`；不得删除现有测试
- **测试要求**：
  - 运行 `python3 -m pytest tests/test_rime_import_safe.py -q`
  - 预期：全部通过（现有 8 + 新增 3 = 11 个）
- **验收标准**：
  - ✅ 3 个新测试均通过
  - ✅ 原有 8 个测试不受影响
  - ✅ 每个新测试覆盖一个特定的 partial-failure 场景
- **潜在风险**：monkeypatch `_copy_any` 需要精确定位 import path —— `pipeline.rime_import_safe._copy_any`

### Phase 2: 🟡 CI + 验证器 + 防御性检查

#### ✅ Task 2.1: CI 门禁加固

- **目标**：将 CI 门禁提升到与当前代码质量匹配的水平
- **修改内容**：
  - 文件 `.github/workflows/ci.yml`：
    1. L31：`--cov-fail-under=30` → `--cov-fail-under=45`
    2. L34：`mypy pipeline/ --ignore-missing-imports --no-error-summary || true` → `mypy pipeline/ --ignore-missing-imports --no-error-summary`
    3. L40：`ruff format --check . || true` → `ruff format --check .`
- **修改边界**：不得修改 CI 的 Python 版本矩阵、checkout、install 步骤；不得修改 ruff check（L37，已是阻塞的）
- **测试要求**：
  - 本地运行 `python3 -m pytest tests/ --cov=pipeline --cov-fail-under=45 -q` → 预期通过
  - 本地运行 `mypy pipeline/ --ignore-missing-imports --no-error-summary` → 预期 `Success: no issues found`
  - 本地运行 `ruff format --check .` → 预期返回码 0
- **验收标准**：
  - ✅ `ci.yml` 不含 `|| true`
  - ✅ `--cov-fail-under=45`
  - ✅ 本地三项检查全部通过
- **潜在风险**：`ruff format` 若有文件未格式化会阻塞 CI → 本地先 `ruff format --check .` 验证

#### ✅ Task 2.2: `definitions.tsv` 验证补全

- **目标**：补齐 definitions 验证：4 列 schema、`(concept_id, lang)` 唯一性、`source` 非空
- **修改内容**：
  - 文件 `pipeline/validate_registry.py`，definitions 验证区块（约 L206-221）：
    1. 将 `if len(r.fields) < 3` 改为 `if len(r.fields) != 4`（强制 4 列）
    2. 提取 `source = r.fields[3]`，检查 `if not source.strip(): _fail(…, "source is empty")`
    3. 新增 `seen_defs: set[tuple[str,str]] = set()`，检查 `(cid, lang)` 重复：`if (cid, lang) in seen_defs: _fail(…, f"duplicate definition for ({cid}, {lang})")`
- **修改边界**：不得修改 aliases/concepts/evidence 验证区块；不得修改 `_fail()` 函数签名
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry` → 预期 OK（当前数据无问题）
  - 运行现有 `python3 -m pytest tests/test_registry_validator.py -q` → 预期全部通过
- **验收标准**：
  - ✅ 3 列定义行被拒绝（schema check）
  - ✅ 空 source 被拒绝
  - ✅ 重复 `(concept_id, lang)` 被拒绝
  - ✅ 当前 registry 通过验证
- **潜在风险**：若个别定义行因导入时遗漏 source 列而只有 3 列 → 已验证全 1550 行均为 4 列

#### ✅ Task 2.3: 新增 definitions 验证测试

- **目标**：为 Task 2.2 新增的验证逻辑添加回归测试
- **修改内容**：
  - 文件 `tests/test_registry_validator.py`，追加 3 个测试函数：
    1. `test_definitions_rejects_wrong_column_count`：构造 3 列定义行 → 断言 `SystemExit`
    2. `test_definitions_rejects_empty_source`：构造 4 列但 source 为空 → 断言 `SystemExit`
    3. `test_definitions_rejects_duplicate_concept_lang`：构造两行相同 `(cid, en)` → 断言 `SystemExit`
- **修改边界**：不得修改 `pipeline/` 代码；不得删除现有测试
- **测试要求**：
  - 运行 `python3 -m pytest tests/test_registry_validator.py -q`
  - 预期全部通过
- **验收标准**：
  - ✅ 3 个新测试通过
  - ✅ 现有 validator 测试不受影响
- **潜在风险**：测试需使用 `tmp_path` 构造临时 registry — 参照现有 `test_registry_validator.py` 中的 `_run_validate` 辅助函数模式

#### ✅ Task 2.4: 导出函数防御性冲突检查

- **目标**：在 `_collect_substitutions()` 和 `export_query_expansions()` 中添加跨 concept 冲突检查
- **修改内容**：
  - 文件 `pipeline/export_registry.py`：
    1. `_collect_substitutions()`（约 L84-87）：在 coalescing 逻辑中，当 `existing` 非 None 且 `existing["concept_id"] != r["concept_id"]` 时 raise `SystemExit(f"export_registry failed: alias {alias!r} is deprecated/forbidden in multiple concepts: {existing['concept_id']!r} and {r['concept_id']!r}")`
    2. `export_query_expansions()`（约 L288）：在 `alias_index[alias] = concept_id` 前，检查 `if alias in alias_index and alias_index[alias] != concept_id: raise SystemExit(f"export_registry failed: alias {alias!r} maps to multiple concepts: {alias_index[alias]!r} and {concept_id!r}")`
- **修改边界**：不得修改 `_iter_alias_rows()`；不得修改 `validate_registry.py`；不得修改导出函数的输出格式
- **测试要求**：
  - 运行 `python3 -m pytest tests/test_export_registry_substitutions.py tests/test_export_registry_query_expansions.py -q`
  - 预期全部通过（正常数据无冲突）
  - 运行 `python3 -m pipeline.export_registry --substitutions --query-expansions` → 预期正常完成
- **验收标准**：
  - ✅ `_collect_substitutions()` 对跨 concept 同 alias 的 deprecated/forbidden 行 raise
  - ✅ `export_query_expansions()` 对跨 concept 同 alias raise
  - ✅ 现有导出测试全部通过
  - ✅ 当前 registry 数据导出正常
- **潜在风险**：如果当前 registry 存在跨 concept 同 alias 的 deprecated/forbidden 行则会暴露——但 `validate_registry` 已禁止此类数据

### Phase 3: 🟡 `export_registry.py` 测试覆盖提升

#### ✅ Task 3.1: `_collect_substitutions` + substitution TSV 导出 unit test

- **目标**：为 `_collect_substitutions()`、`export_substitutions_tsv()` 添加直接 unit test
- **修改内容**：
  - 文件 `tests/test_export_registry_substitutions.py`，追加测试：
    1. `test_collect_substitutions_basic`：构造含 preferred + forbidden + deprecated 的 rows 列表，直接调用 `_collect_substitutions(rows)`，验证输出
    2. `test_collect_substitutions_forbidden_beats_deprecated`：同 alias 有 forbidden 和 deprecated → 验证 forbidden 胜出
    3. `test_collect_substitutions_rejects_cross_concept_conflict`：同 alias 不同 concept_id 的 forbidden → 验证 `SystemExit`（Task 2.4 新增检查）
    4. `test_export_substitutions_tsv_writes_correct_format`：用 `tmp_path` 构造临时 registry，调用 `export_substitutions_tsv()`，验证输出文件内容
- **修改边界**：不得修改 `pipeline/` 代码；不得删除现有测试
- **测试要求**：
  - 运行 `python3 -m pytest tests/test_export_registry_substitutions.py -q` → 全部通过
- **验收标准**：
  - ✅ 4 个新测试通过
  - ✅ 覆盖 `_collect_substitutions` 的 coalescing、preferred 选择、conflict 检查路径
  - ✅ 覆盖 `export_substitutions_tsv` 的文件写入路径
- **潜在风险**：`_collect_substitutions` 是模块私有函数，需 `from pipeline.export_registry import _collect_substitutions` — Python 允许但需确认 ruff 不会 lint 报错（_前缀私有导入）

#### ✅ Task 3.2: query_expansions + vale_substitute + translation_dict 导出 unit test

- **目标**：为其余低覆盖率导出函数添加 unit test
- **修改内容**：
  - 文件 `tests/test_export_registry_query_expansions.py`，追加测试：
    1. `test_export_query_expansions_basic`：用 `tmp_path` 构造临时 registry，调用 `export_query_expansions()`，验证 JSON 文件 schema 正确
    2. `test_export_query_expansions_rejects_cross_concept_alias`：构造跨 concept 同 alias → 验证 `SystemExit`
  - 文件 `tests/test_export_registry_vale_substitute.py`，追加测试：
    1. `test_export_vale_substitute_basic`：用 `tmp_path` 构造临时 registry，调用 `export_vale_substitute_yaml()`，验证 YAML 内容
  - 文件 `tests/test_export_registry_translation_dict.py`，追加测试：
    1. `test_export_translation_dict_basic_structure`：用 `tmp_path` 构造临时 registry，调用 `export_translation_dict()`，验证 JSON 包含 `en2zh` / `zh2en` / `en2zh_short` keys
- **修改边界**：不得修改 `pipeline/` 代码；不得删除现有测试
- **测试要求**：
  - 运行 `python3 -m pytest tests/test_export_registry_query_expansions.py tests/test_export_registry_vale_substitute.py tests/test_export_registry_translation_dict.py -q` → 全部通过
- **验收标准**：
  - ✅ 4 个新测试通过
  - ✅ `export_registry.py` 覆盖率 ≥ 50%（从 16% 提升）
- **潜在风险**：构造临时 registry 需包含 concepts.tsv + aliases.tsv 且通过最低验证；参照 `test_export_registry_translation_dict.py` 现有的 `_make_registry` 辅助模式

#### ✅ Task 3.3: 覆盖率验证

- **目标**：确认 Phase 3 新增测试后整体覆盖率达标
- **修改内容**：无文件手动修改；运行命令
- **修改边界**：无
- **测试要求**：
  1. `python3 -m pytest tests/ --cov=pipeline --cov-fail-under=45 -q` → 通过
  2. `python3 -m pytest tests/ --cov=pipeline --cov-report=term-missing -q 2>&1 | grep export_registry` → 覆盖率 ≥ 50%
- **验收标准**：
  - ✅ 全量测试通过
  - ✅ `--cov-fail-under=45` 通过
  - ✅ `export_registry.py` 覆盖率 ≥ 50%
- **潜在风险**：如果新增 unit test 未覆盖主函数中的某些分支，可能低于 50% → Task 3.1/3.2 的 `export_*_tsv` / `export_*_yaml` 测试应走完主函数全路径

### Phase 4: 🟢 + 🟡 低成本加固

#### ✅ Task 4.1: Timeout 异常处理（B3 + B4）

- **目标**：捕获 `TimeoutExpired` 并提供上下文错误消息
- **修改内容**：
  - 文件 `pipeline/release_pack.py`，`_run_module()`（L23-37）：
    1. 在 `subprocess.run(...)` 调用周围添加 `try/except subprocess.TimeoutExpired as te`
    2. handler 中 raise `SystemExit(f"release_pack failed: module {module} timed out after {te.timeout}s")`
  - 文件 `pipeline/rime_import_safe.py`，`main()` 中 payload generation 调用（约 L419-432）：
    1. 在 `_run_importer_v2(...)` 调用周围添加 `try/except subprocess.TimeoutExpired as te`
    2. handler 中 raise `SystemExit(f"safe import failed: payload generation timed out after {te.timeout}s")`
- **修改边界**：不得修改 `_run_importer_v2()` 函数本体；不得修改 import step 的已有 timeout handler（L476-496）
- **测试要求**：
  - 运行 `python3 -m pytest tests/test_rime_import_safe.py tests/test_release_pack.py -q` → 全部通过
- **验收标准**：
  - ✅ `_run_module()` 中 `TimeoutExpired` 被捕获并转为 contextual `SystemExit`
  - ✅ payload generation timeout 被捕获
  - ✅ 现有测试不受影响
- **潜在风险**：无——纯增加异常 handler，不改变正常路径

#### ✅ Task 4.2: 停止吞异常 + 改进错误上下文（Q7 + Q8）

- **目标**：消除 `except Exception: pass` 和缺少上下文的错误消息
- **修改内容**：
  - 文件 `pipeline/generate_dict_yaml.py`：
    1. L130-133：将 `except Exception: pass` 改为 `except Exception: warnings.warn(f"failed to clean up temp file: {payload_path}", RuntimeWarning, stacklevel=2)`
    2. L102-105：在 `raise SystemExit(proc.returncode)` 前添加 contextual 消息——`raise SystemExit(f"generate_dict_yaml: importer {rime_script} failed (exit {proc.returncode}) for input {input_wordlist} → output {output_yaml}")`
  - 文件 `pipeline/rime_export.py`：
    1. L153-156：将 `raise SystemExit(proc.returncode)` 改为 `raise SystemExit(f"rime_export: importer failed (exit {proc.returncode})")`
- **修改边界**：不得修改 subprocess 调用参数；不得修改正常路径逻辑
- **测试要求**：
  - 运行 `python3 -m pytest tests/ -q` → 全部通过
- **验收标准**：
  - ✅ `generate_dict_yaml.py` 不含 `except Exception: pass`
  - ✅ subprocess 失败消息包含脚本路径和输入/输出路径
  - ✅ `rime_export.py` 失败消息包含 exit code
- **潜在风险**：`warnings.warn()` 需要 `import warnings`——检查是否已导入

#### ✅ Task 4.3: `[tool.mypy]` 配置 + Plan 归档标记（Q9 + O6）

- **目标**：添加 mypy 配置、归档已完成的 plan 文件
- **修改内容**：
  - 文件 `pyproject.toml`，在 `[tool.ruff.lint]` 之后追加：
    ```toml
    [tool.mypy]
    python_version = "3.11"
    ignore_missing_imports = true
    warn_return_any = true
    warn_unused_configs = true
    ```
  - 5 个 plan 文件（`translation-enhancement.md`、`short-token-segregation.md`、`fix-translation-dict-gaps.md`、`mcp-dict-improvements-2026-04.md`、`repo-improvement-2026-03-25.md`）：在第 1 行前插入归档标记 `> ✅ **状态：已归档**`
- **修改边界**：不得修改 `pyproject.toml` 的 ruff 配置；不得修改 plan 内容
- **测试要求**：
  - 运行 `mypy pipeline/ --ignore-missing-imports` → `Success: no issues found`
  - 运行 `grep -l '状态：已归档' .github/plans/*.md | wc -l` → 预期 6（含已有的 `next-improvement-cycle.md`）
- **验收标准**：
  - ✅ `pyproject.toml` 含 `[tool.mypy]` 节
  - ✅ mypy 通过
  - ✅ 6 个 plan 文件标记为归档
- **潜在风险**：无

#### ✅ Task 4.4: 全量验证 + Commit

- **目标**：全量回归测试 + 提交
- **修改内容**：无手动修改；运行命令
- **测试要求**：
  1. `python3 -m pipeline.validate_registry` → OK
  2. `python3 -m pytest tests/ --cov=pipeline --cov-fail-under=45 -q` → 全部通过
  3. `mypy pipeline/ --ignore-missing-imports --no-error-summary` → Success
  4. `ruff check .` → All checks passed
  5. `ruff format --check .` → 返回码 0
  6. `python3 -m compileall -q pipeline tests` → 无错误
- **验收标准**：
  - ✅ 所有 6 项检查通过
  - ✅ `git add` + `git commit` 成功
- **潜在风险**：pre-commit hook 包含 pytest，大量文件变更时运行较慢

## 回归检查清单

- [ ] `python3 -m pipeline.validate_registry` → OK（1493+ concepts, definitions validated）
- [ ] `python3 -m pytest tests/ --cov=pipeline --cov-fail-under=45 -q` → all passed
- [ ] `mypy pipeline/ --ignore-missing-imports --no-error-summary` → Success
- [ ] `ruff check .` → All checks passed
- [ ] `ruff format --check .` → exit 0
- [ ] `python3 -m compileall -q pipeline tests` → 无错误
- [ ] `ci.yml` 不含 `|| true`
- [ ] `export_registry.py` 覆盖率 ≥ 50%
- [ ] `rime_import_safe.py` rollback 测试含 partial-failure 场景
- [ ] `generate_dict_yaml.py` 不含 `except Exception: pass`

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
| 背景与目标 | 完整 |
| 技术方案 | 完整（含 5 项设计决策） |
| Error & Rescue Map | 5 路径，0 CRITICAL GAP |
| 执行计划 | 4 Phase、13 Task |
| 回归检查清单 | 10 项（全部项目特定） |
| 已知局限 | 无 |

### R1 Issues — 结构完整性
- **Issue R1-1**: 原始草案中 Phase 2 Task 2.4 缺少"修改边界"字段 → 已补充 ✅ 已修正
- **Issue R1-2**: Error & Rescue Map 缺少 `os.rename()` 跨文件系统 fallback 条目 → 已添加 ✅ 已修正
- **Issue R1-3**: 缺少"已有代码/流程复用分析"section → 已在背景目标中补充 ✅ 已修正
- **Issue R1-4**: Phase 编号连续但缺少 Phase 3 与 Phase 2 Task 2.4 的依赖关系说明 → Task 3.1 中 conflict 测试依赖 Task 2.4 的检查逻辑，已在 Task 3.1 中明确标注 ✅ 已修正

### R2 Issues — 可执行性
- **Issue R2-1**: Task 2.2 验收标准中"3 列定义行被拒绝"不够二元 → 改为"`if len(r.fields) != 4` 触发 `_fail()`" ✅ 已修正
- **Issue R2-2**: Task 3.3 覆盖率验证的"≥50%"目标缺少 fallback — 若 rime_export 0% 拖累总分怎么办 → 目标是 export_registry 单模块 ≥50%，与总分 ≥45% 分别验证 ✅ 已修正
- **Issue R2-3**: Task 4.2 需确认 `warnings` 是否已导入 → 已在潜在风险中标注检查项 ✅ 已修正

### R3 Issues — 风险与边缘
- **Issue R3-1**: Task 1.2 的 `os.replace()` 对目录不可靠 → 改用 `os.rename()` 并标注同文件系统约束（backup 和 target 一般在同 `$HOME` 下） ✅ 已修正
- **Issue R3-2**: Task 2.4 防御性检查若当前 registry 有隐藏的跨 concept 同 alias（仅在 deprecated/forbidden 中） → 预先运行导出命令验证无报错，已在验收标准中要求 ✅ 已修正

## Pre-Delivery Audit (Level: L1-Lite)

| § | Check | Status | Note |
|---|-------|--------|------|
| 1 | Factual accuracy | ✅ PASS | 行号来自工具输出，覆盖率数字来自 `pytest --cov` 实跑，代码片段来自 read_file |
Auditor: Plan Architect | Date: 2026-04-14
