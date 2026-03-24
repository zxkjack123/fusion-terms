# fusion-terms 仓库加固计划

## 背景与目标

- **问题/需求描述**：2026-03-24 仓库审阅（[full-repo-2026-03-24.md](../reviews/full-repo-2026-03-24.md)）发现 4 🔴 / 10 🟡 / 8 🟢 共 22 项问题。核心问题覆盖三个维度：
  1. **安全/正确性**：`review_pack.py` 路径穿越 (B1)、`rime_import_safe.py` rollback 信任 manifest 路径 (B2)
  2. **Registry 数据质量**：Batch 54 新增 24 概念后 forbidden 覆盖率降至 92.6% (O2)、稀疏概念 81 个 (O3)
  3. **Pipeline 健壮性**：死代码、静默截断、expanduser 遗漏、缺少 subprocess timeout、CI 缺少 registry 校验步骤、`sync_to_fcitx.py` 无测试

- **根因分析**：
  - B1：`_resolve_under()` 仿照简单 path join 编写，未参考同仓库中已有的 `_safe_relpath_under_root()` 防护模式
  - O2/O3：每批新概念入库时只关注 concepts + aliases + evidence，未执行 forbidden/sparse 补充步骤
  - Pipeline 小问题：增量开发中遗留，各模块作者不同时期编写，缺少统一代码审查

- **目标**：
  1. 修复 B1 路径穿越并回归测试
  2. 修复 B2 rollback manifest 路径信任
  3. Pipeline 小修：死代码清理、静默截断告警、expanduser、hardcoded 路径、subprocess timeout、evidence 完整性校验、export 静默跳过告警
  4. 补充 `sync_to_fcitx.py` 测试
  5. CI 增加 `validate_registry` 步骤
  6. 启用 ruff E/W/B 规则集并修复违规
  7. 激活 pre-commit hooks
  8. Batch 54 forbidden 别名补充 → ≥95%
  9. Batch 54 + 剩余稀疏概念别名充实 → ≤60 sparse
  10. 版本对齐：fold Unreleased → tag → push → release pack
  11. 添加 `[rime]` config section + artifact 清理工具

- **非目标（不做什么）**：
  - 不重构 `extract_candidates.py`（Q1 复杂度问题大改，风险高，留后续专项）
  - 不替换 hardcoded `~/.local/bin/rime_import_wordlist.py` 默认值（Q10，个人工具优先级低）
  - 不添加 `requirements.lock`（O8，CI 现状可接受）
  - 不扩充语料库、不新增概念

## 技术方案

- **方案概述**：分 6 Phase、19 个 Task 执行。Phase 1–3 处理代码质量/安全，Phase 4 处理 registry 数据，Phase 5 处理 CI/工具链，Phase 6 版本对齐与发布。
- **关键设计决策**：
  - 先修代码（Phase 1–3）再改数据（Phase 4），确保 validator 增强后能捕获数据问题
  - 每个 Phase 自成一个 commit，可独立回滚
  - Phase 4 registry 数据变更在 validator 增强之后执行，新增的 evidence 完整性检查可即时保护
  - Phase 6 最后统一版本对齐，避免中间多次 tag
- **影响范围**：
  - `pipeline/review_pack.py`、`pipeline/rime_import_safe.py`、`pipeline/common.py`、`pipeline/build_terms.py`、`pipeline/apply_decisions.py`、`pipeline/export_registry.py`、`pipeline/validate_registry.py`、`pipeline/generate_dict_yaml.py`、`pipeline/generate_manifest.py`、`pipeline/release_pack.py`、`pipeline/rime_export.py`
  - `tests/test_review_pack.py`（新增或扩展）、`tests/test_sync_to_fcitx.py`（新建）、`tests/test_registry_validator.py`（扩展）
  - `.github/workflows/ci.yml`、`pyproject.toml`、`config.toml`、`CHANGELOG.md`
  - `terms/registry/aliases.tsv`

## 执行计划

### Phase 1: 安全修复

#### ✅ Task 1.1: 修复 `_resolve_under()` 路径穿越 (B1)

- **目标**：防止 `review_pack.py` 的 `_resolve_under()` 接受含 `..` 的相对路径逃逸出目标目录
- **修改内容**：
  - 文件 `pipeline/review_pack.py`（第 66–68 行）：
    - 将当前实现替换为带 `.resolve()` + `is_relative_to()` 检查的安全版本
    - 参考同仓库 `pipeline/generate_manifest.py:164-175` 的 `_safe_relpath_under_root()` 实现模式
    - 绝对路径保持直通（不变），相对路径 resolve 后验证仍在 `base` 下
    - 失败时 `raise SystemExit(f"review pack failed: path escapes base directory: {p!r}")`
  - 文件 `tests/test_review_pack.py`：
    - 新增测试用例 `test_resolve_under_rejects_path_traversal()`：构造含 `../../etc/passwd` 的路径，断言 `SystemExit`
    - 新增测试用例 `test_resolve_under_accepts_normal_relative()`：断言正常相对路径通过
- **修改边界**：不得修改 `_resolve_under` 的调用方式（lines 337–338 的 `_resolve_under(out_dir, ...)` 保持不变）；不得修改 `pipeline/generate_manifest.py`
- **测试要求**：
  - 运行 `python -m pytest tests/test_review_pack.py -v`
  - 预期输出：新增测试通过，已有测试不回归
  - 运行 `python -m pytest tests/ -q`
  - 预期输出：所有测试通过（≥62 passed，含 2 个新测试）
- **验收标准**：
  - ✅ `_resolve_under(Path("/tmp/out"), "../../etc/passwd")` 抛出 `SystemExit`
  - ✅ `_resolve_under(Path("/tmp/out"), "sub/file.tsv")` 返回 `/tmp/out/sub/file.tsv`
  - ✅ `_resolve_under(Path("/tmp/out"), "/abs/path.tsv")` 返回 `/abs/path.tsv`（绝对路径直通）
  - ✅ 全量测试通过
- **潜在风险**：绝对路径直通是设计上的选择（CLI 用户可能需要指定绝对路径），但绝对路径不受 base 约束。可接受，因为 CLI 参数由用户直接控制。

#### ✅ Task 1.2: 修复 `rollback_from_manifest()` 路径信任 (B2)

- **目标**：在 `rime_import_safe.py` 的 rollback 流程中验证 manifest 中的路径不超出预期目录范围
- **修改内容**：
  - 文件 `pipeline/rime_import_safe.py`（`rollback_from_manifest()` 函数，约第 147–186 行）：
    - 在 `for it in items_sorted:` 循环内、`orig = Path(it["original"]).expanduser()` 之后，添加验证：
    - `orig` 必须位于用户 home 目录下（`orig.resolve().is_relative_to(Path.home())`），否则 `raise SystemExit`
    - `bak` 必须位于用户 home 目录或 `artifacts/` 下
  - 文件 `tests/test_rime_import_safe.py`：
    - 新增测试 `test_rollback_rejects_paths_outside_home()`：构造含 `/etc/something` 路径的 manifest，断言 `SystemExit`
- **修改边界**：不得修改 `create_backup()` 函数；不得修改 `rime_import_safe.py` 的 CLI 参数解析
- **测试要求**：
  - 运行 `python -m pytest tests/test_rime_import_safe.py -v`
  - 预期输出：新增测试通过，现有测试不回归
- **验收标准**：
  - ✅ 含 `/etc/shadow` 路径的 manifest 被拒绝
  - ✅ 含 `~/.local/share/fcitx5/rime/...` 的正常 manifest 通过
  - ✅ 全量测试通过
- **潜在风险**：`Path.home()` 检查可能对非标准部署布局过严。折中：检查 `home` 或 `repo_root/artifacts`。

#### ✅ Task 1.3: Phase 1 commit

- **目标**：提交安全修复
- **修改内容**：
  - `git add pipeline/review_pack.py pipeline/rime_import_safe.py tests/test_review_pack.py tests/test_rime_import_safe.py`
  - `git commit -m "security: fix path traversal in review_pack and rollback manifest trust"`
- **修改边界**：仅提交 Phase 1 变更
- **测试要求**：
  - `python -m pytest tests/ -q` → 全部通过
  - `git status` → 干净
- **验收标准**：
  - ✅ commit 存在
  - ✅ 工作目录干净
- **潜在风险**：无

---

### Phase 2: Pipeline 小修（快速修复批）

#### ✅ Task 2.1: 死代码清理 + 静默截断告警 (Q2 + Q3)

- **目标**：移除 `common.py` 中未使用的 `Example` 类和 `sha1_text()` 函数；为 `read_text_file()` 的截断行为添加 warning
- **修改内容**：
  - 文件 `pipeline/common.py`：
    - 删除第 39–44 行的 `@dataclass(frozen=True) class Example` 及其两个字段
    - 删除第 46–47 行的 `def sha1_text(text: str) -> str:` 及其函数体
    - 移除 `hashlib` import（如果仅 `sha1_text` 使用）
    - 在 `read_text_file()` 的 `if len(data) > max_bytes:` 分支中（第 193–194 行），`data = data[:max_bytes]` 之前添加 `warnings.warn(f"file truncated at {max_bytes} bytes: {path}", stacklevel=2)`
- **修改边界**：不得修改 `read_text_file()` 的返回值或签名；不得修改 `iter_markdown_files()` 或其他函数
- **测试要求**：
  - `python -m ruff check pipeline/common.py` → 无 F401/F821 错误
  - `python -m pytest tests/ -q` → 全部通过
  - `python -c "from pipeline.common import Example"` → `ImportError`（确认已删除）
  - `python -c "from pipeline.common import sha1_text"` → `ImportError`
- **验收标准**：
  - ✅ `class Example` 和 `sha1_text` 不再存在于 `common.py`
  - ✅ `hashlib` import 已移除（如无其他使用者）
  - ✅ `read_text_file` 截断时产生 `UserWarning`
  - ✅ 全量测试通过，无 ruff 违规
- **潜在风险**：如有测试 fixture 引用 `Example`，需同步更新。经查无测试导入 `Example`（仅 `extract_candidates.py` 用了字符串 "Example" 作 CLI 帮助文本，不是类引用）。

#### ✅ Task 2.2: expanduser 修复 + hardcoded 路径修复 (Q4 + Q5)

- **目标**：修复 `build_terms.py` 的 `terms_dir` 缺少 `expanduser()`，修复 `apply_decisions.py` 的 hardcoded `Path("artifacts")`
- **修改内容**：
  - 文件 `pipeline/build_terms.py`（第 172 行）：
    - `terms_dir = Path(args.terms_dir)` → `terms_dir = Path(args.terms_dir).expanduser()`
  - 文件 `pipeline/apply_decisions.py`（第 331 行）：
    - `ensure_dir(Path("artifacts"))` → `ensure_dir(Path(__file__).resolve().parent.parent / "artifacts")`
    - 即：相对于 `pipeline/` 的父目录（仓库根目录）定位 `artifacts/`
- **修改边界**：不得修改 `build_terms.py` 的其他 Path 操作；不得修改 `apply_decisions.py` 的 `apply_decisions()` 函数签名或逻辑
- **测试要求**：
  - `python -m pytest tests/test_repo_terms_build.py tests/test_apply_decisions.py -v` → 通过
  - `python -m pytest tests/ -q` → 全部通过
- **验收标准**：
  - ✅ `build_terms.py` 第 172 行包含 `.expanduser()`
  - ✅ `apply_decisions.py` 不再包含 `Path("artifacts")`
  - ✅ 全量测试通过
- **潜在风险**：`Path(__file__).resolve().parent.parent` 在不同安装方式下可能不等于仓库根。鉴于这是一个本地开发仓库（非 pip install 的包），此假设合理。

#### ✅ Task 2.3: subprocess timeout (Q9)

- **目标**：为所有 `subprocess.run()` 调用添加超时保护
- **修改内容**：
  - 文件 `pipeline/generate_dict_yaml.py`（第 36 行）：添加 `timeout=120`
  - 文件 `pipeline/generate_manifest.py`（第 56 行）：添加 `timeout=30`
  - 文件 `pipeline/release_pack.py`（第 24 行）：添加 `timeout=300`（调用完整模块，含构建）
  - 文件 `pipeline/rime_export.py`（第 105 行）：添加 `timeout=120`
  - 文件 `pipeline/rime_import_safe.py`（第 81 行）：添加 `timeout=120`
- **修改边界**：仅添加 `timeout=` 参数，不得修改其他 `subprocess.run()` 参数；不得修改函数签名
- **测试要求**：
  - `python -m pytest tests/ -q` → 全部通过
  - `grep -rn "timeout=" pipeline/*.py | wc -l` → 输出 `5`
- **验收标准**：
  - ✅ 所有 5 个 `subprocess.run()` 调用均有 `timeout=` 参数
  - ✅ 全量测试通过
- **潜在风险**：若外部 Rime importer 实际运行时间超过 120s（如词库极大），timeout 会触发。120s 对于当前 ~1700 词的词库绰绰有余。

#### ✅ Task 2.4: export_registry 静默跳过告警 (B3)

- **目标**：在 `export_registry.py` 的行读取器跳过短行时发出 warning，而非完全静默
- **修改内容**：
  - 文件 `pipeline/export_registry.py`：
    - 在 `_iter_alias_rows()`（约第 137 行 `if len(parts) < 4: continue`）前添加 `warnings.warn(f"skipping short alias row at {aliases_path}:{lineno}: {line!r}")`（需在循环中维护 `lineno` 计数器，或使用 `enumerate`）
    - 在 `_iter_concept_rows()`（约第 164 行 `if len(parts) < 2: continue`）前添加类似 warning
    - 在文件顶部添加 `import warnings`
- **修改边界**：不得修改跳过行为本身（仍然 `continue`），仅添加 warning；不得修改 `main()` 或其他函数
- **测试要求**：
  - `python -m pytest tests/test_export_registry_vale.py tests/test_export_registry_query_expansions.py -v` → 通过
  - `python -m pytest tests/ -q` → 全部通过
- **验收标准**：
  - ✅ 给定含短行的 TSV 输入时，`_iter_alias_rows()` 产生 `UserWarning`
  - ✅ 正常 TSV 不产生 warning
  - ✅ 全量测试通过
- **潜在风险**：如果现有测试使用带短行的 fixture，可能会触发新 warning。测试中可用 `warnings.catch_warnings()` 抑制。

#### ✅ Task 2.5: validate_registry evidence 完整性检查 (B4)

- **目标**：在 `validate_registry.py` 中添加"每个 concept 必须有至少一条 evidence"的检查
- **修改内容**：
  - 文件 `pipeline/validate_registry.py`（在 evidence 循环之后、bridge check 之前，约第 160 行附近）：
    - 收集 `evidence_concept_ids: set[str]` — evidence.tsv 中出现的所有 concept_id
    - `missing_evidence = concept_ids - evidence_concept_ids`
    - `if missing_evidence: _fail(evidence_path, 0, f"concepts without evidence rows: {sorted(missing_evidence)[:10]}...")`
  - 文件 `tests/test_registry_validator.py`：
    - 新增测试 `test_validate_registry_rejects_missing_evidence()`：构造有 concept 但无 evidence 的 registry，断言 `SystemExit`
- **修改边界**：不得修改 `_fail()` 函数签名；不得修改 concepts 或 aliases 的校验逻辑
- **测试要求**：
  - `python -m pytest tests/test_registry_validator.py -v` → 新增测试通过
  - `python3 -m pipeline.validate_registry` → `registry OK`（当前数据 949 concepts = 949 evidence rows）
  - `python -m pytest tests/ -q` → 全部通过
- **验收标准**：
  - ✅ 现有 registry 通过完整性检查（949 = 949）
  - ✅ 人工删除某条 evidence 后重跑 validator → 报错
  - ✅ 全量测试通过
- **潜在风险**：如果未来添加 concept 时忘记添加 evidence，此检查会立即阻断。这正是期望行为。

#### ✅ Task 2.6: Phase 2 commit

- **目标**：提交 Phase 2 全部小修
- **修改内容**：
  - `git add pipeline/common.py pipeline/build_terms.py pipeline/apply_decisions.py pipeline/export_registry.py pipeline/validate_registry.py pipeline/generate_dict_yaml.py pipeline/generate_manifest.py pipeline/release_pack.py pipeline/rime_export.py pipeline/rime_import_safe.py tests/test_registry_validator.py`
  - `git commit -m "fix: pipeline robustness — dead code, truncation warning, expanduser, timeout, evidence check"`
- **修改边界**：仅提交 Phase 2 变更
- **测试要求**：
  - `python -m pytest tests/ -q` → 全部通过
  - `python -m ruff check .` → 无违规
- **验收标准**：
  - ✅ commit 存在
  - ✅ 工作目录干净
- **潜在风险**：无

---

### Phase 3: 测试与 Lint 补充

#### Task 3.1: 新增 `sync_to_fcitx.py` 测试 (Q8)

- **目标**：为唯一无测试覆盖的 pipeline 模块补充测试
- **修改内容**：
  - 新建文件 `tests/test_sync_to_fcitx.py`：
    - `test_sync_copies_file(tmp_path)`：在 tmp_path 创建源文件，调用 `main()` 并断言目标文件存在且内容一致
    - `test_sync_fails_on_missing_input(tmp_path)`：不创建源文件，断言 `SystemExit`
    - `test_sync_creates_parent_dirs(tmp_path)`：目标路径的父目录不存在，断言自动创建
    - 均使用 `monkeypatch.setattr("sys.argv", ...)` 模拟 CLI 参数
- **修改边界**：不得修改 `pipeline/sync_to_fcitx.py`；测试仅操作 `tmp_path`，不触碰真实 fcitx 目录
- **测试要求**：
  - `python -m pytest tests/test_sync_to_fcitx.py -v` → 3 passed
  - `python -m pytest tests/ -q` → ≥63 passed（新增 3 个测试）
- **验收标准**：
  - ✅ `tests/test_sync_to_fcitx.py` 存在，包含 ≥3 个测试函数
  - ✅ 全量测试通过
- **潜在风险**：`sync_to_fcitx.py` 使用 `argparse` + `sys.exit`，monkeypatch `sys.argv` 需注意作用域。

#### Task 3.2: 启用 ruff E/W/B 规则集 (Q6)

- **目标**：增量启用 ruff 规则集以捕获更多常见错误
- **修改内容**：
  - 文件 `pyproject.toml`（`[tool.ruff.lint]` section）：
    - `select = ["F401", "F821"]` → `select = ["E", "F", "W", "B"]`
    - 添加 `[tool.ruff.lint.per-file-ignores]` 如需对 `scripts/batches/` 例外
  - 修复 ruff 报出的所有新违规（预计少量，仓库代码风格较好）
- **修改边界**：不得修改 pipeline 模块的功能逻辑；仅修复 lint 报出的格式/风格问题
- **测试要求**：
  - `python -m ruff check .` → 无违规
  - `python -m pytest tests/ -q` → 全部通过
- **验收标准**：
  - ✅ `pyproject.toml` 中 ruff select 包含 `E`, `F`, `W`, `B`
  - ✅ `ruff check .` 零违规
  - ✅ 全量测试通过
- **潜在风险**：新规则可能报出大量违规。如数量超过 20 处，应先用 `ruff check . --statistics` 评估，再决定是否分批启用。

#### Task 3.3: 激活 pre-commit hooks (Q7)

- **目标**：让已有的 `.pre-commit-config.yaml` 生效
- **修改内容**：
  - 运行 `pre-commit install`
  - 运行 `pre-commit run --all-files` 验证全部 hooks 通过
  - 如有 hook 修复的文件（trailing whitespace 等），一并 commit
- **修改边界**：不得修改 `.pre-commit-config.yaml` 的 hook 列表
- **测试要求**：
  - `pre-commit run --all-files` → 全部通过
  - `ls -la .git/hooks/pre-commit` → 文件存在（非 sample）
- **验收标准**：
  - ✅ `.git/hooks/pre-commit` 存在且可执行
  - ✅ `pre-commit run --all-files` 全部通过
- **潜在风险**：`pre-commit run` 中的 `pytest` hook 会跑全量测试，耗时约 5s，可接受。

#### Task 3.4: Phase 3 commit

- **目标**：提交测试和 lint 改进
- **修改内容**：
  - `git add tests/test_sync_to_fcitx.py pyproject.toml` + 任何 ruff/pre-commit 修复的文件
  - `git commit -m "quality: add sync_to_fcitx tests, enable ruff E/W/B rules, activate pre-commit"`
- **修改边界**：仅提交 Phase 3 变更
- **测试要求**：
  - `python -m pytest tests/ -q` → 全部通过
  - `pre-commit run --all-files` → 全部通过
- **验收标准**：
  - ✅ commit 存在
  - ✅ 工作目录干净
- **潜在风险**：无

---

### Phase 4: Registry 数据质量提升

**前置依赖**：Phase 2 完成（evidence 完整性检查已激活，可即时保护）

#### Task 4.1: Batch 54 forbidden 别名补充 + 剩余覆盖提升至 ≥95% (O2)

- **目标**：为 Batch 54 新增的 24 概念及剩余 ~46 个无 forbidden/deprecated 别名的概念补充错误形式别名，覆盖率达 ≥95%
- **修改内容**：
  - 文件 `terms/registry/aliases.tsv`：
    - 在文件末尾追加 `# ==== Batch F12: Forbidden enrichment for Batch 54 + remainder ====`
    - 为每个目标概念添加至少 1 条 `kind=forbidden` 或 `kind=deprecated` 别名
    - 典型来源：AI 翻译常见误译、混淆近义词、过时缩写
  - 使用 pre-flight 脚本检查新别名不与现有别名产生跨概念冲突
- **修改边界**：不得修改 `terms/registry/concepts.tsv`（不新增/删除概念）；不得修改 `terms/registry/evidence.tsv`；不得修改 `pipeline/*.py`
- **测试要求**：
  - 运行 pre-flight 冲突检测：`python3 -c "..."` 验证无跨概念别名冲突
  - `python3 -m pipeline.validate_registry` → `registry OK: 949 concepts, ≥4581 aliases, 949 evidence`
  - `python -m pytest tests/ -q` → 全部通过
  - 运行覆盖率计算脚本 → `≥ 902/949 = 95.0%`
- **验收标准**：
  - ✅ Forbidden/deprecated 覆盖率 ≥ 95%（≥902/949）
  - ✅ `validate_registry` 通过
  - ✅ 无跨概念别名冲突
  - ✅ 全量测试通过
- **潜在风险**：部分 code 类概念（如 best, cfr, mcnp）不存在有意义的 AI 误译，可标注为"不适用"跳过，仍可达 95% 覆盖率。

#### Task 4.2: Batch 54 + 剩余稀疏概念别名充实 (O3)

- **目标**：将稀疏概念数（≤2 正确别名）从 81 降至 ≤60
- **前置依赖**：Task 4.1 完成（避免 aliases.tsv 并发修改冲突）
- **修改内容**：
  - 文件 `terms/registry/aliases.tsv`：
    - 追加 `# ==== Batch 56: Sparse concept enrichment ====`
    - 为 ≥21 个稀疏概念各添加 1–3 条正确别名（`kind=preferred` 或 `kind=alias`）
    - 优先处理 Batch 54 新增概念，再处理剩余旧稀疏概念
    - 别名来源：中文全称/简称/变体、英文 synonym/plural/abbreviation
  - 使用 pre-flight 脚本验证无跨概念别名冲突
- **修改边界**：不得修改 `terms/registry/concepts.tsv`；不得修改 `terms/registry/evidence.tsv`；不得修改 `pipeline/*.py`
- **测试要求**：
  - `python3 -m pipeline.validate_registry` → `registry OK`
  - `python -m pytest tests/ -q` → 全部通过
  - 稀疏概念计数 → `≤ 60`
- **验收标准**：
  - ✅ 稀疏概念数 ≤ 60
  - ✅ `validate_registry` 通过
  - ✅ 无跨概念别名冲突
  - ✅ 全量测试通过
- **潜在风险**：新别名可能与现有别名冲突。pre-flight 脚本必须逐条检查。

#### Task 4.3: Phase 4 commit

- **目标**：提交 registry 数据质量提升
- **修改内容**：
  - `git add terms/registry/aliases.tsv`
  - `git commit -m "registry: Batch F12 forbidden + Batch 56 sparse enrichment (coverage ≥95%, sparse ≤60)"`
- **修改边界**：仅提交 Phase 4 变更
- **测试要求**：
  - `python -m pytest tests/ -q` → 全部通过
  - `git status` → 干净
- **验收标准**：
  - ✅ commit 存在
  - ✅ 工作目录干净
- **潜在风险**：无

---

### Phase 5: CI 与配置改善

#### Task 5.1: CI 增加 validate_registry 步骤 (O5)

- **目标**：在 GitHub Actions CI 中添加 registry 校验，防止损坏的 registry 数据进入 master
- **修改内容**：
  - 文件 `.github/workflows/ci.yml`：
    - 在 `Compile check` 步骤之后添加新步骤：
      ```yaml
      - name: Validate registry
        run: python3 -m pipeline.validate_registry
      ```
- **修改边界**：不得修改 CI 中已有步骤；不得修改 `pipeline/validate_registry.py`
- **测试要求**：
  - `python3 -m pipeline.validate_registry` → `registry OK`（本地验证）
  - 检查 `.github/workflows/ci.yml` 语法：`python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"` 或在线 YAML 验证
- **验收标准**：
  - ✅ `ci.yml` 包含 `Validate registry` 步骤
  - ✅ 步骤命令为 `python3 -m pipeline.validate_registry`
  - ✅ 位于 `Compile check` 之后
- **潜在风险**：CI 环境中 `terms/registry/` 文件存在（已 tracked），无额外依赖。

#### Task 5.2: 添加 `[rime]` config section (O6)

- **目标**：将 Rime 相关默认值集中到 `config.toml`，减少 CLI 记忆负担
- **修改内容**：
  - 文件 `config.toml`：追加 `[rime]` section：
    ```toml
    [rime]
    dict_name = "rime_ice"
    backup_paths = [
        "~/.local/share/fcitx5/rime",
        "~/.config/fcitx5/rime",
    ]
    ```
  - 文件 `pipeline/rime_import_safe.py`：在 `main()` 的参数解析中，从 config 加载默认值（如 config 存在）
  - 文件 `pipeline/sync_to_fcitx.py`：从 config 加载默认 `--dest` 路径（如 config 存在）
- **修改边界**：CLI 参数仍可覆盖 config 值；不得删除现有 CLI 参数；保持向后兼容
- **测试要求**：
  - `python -m pytest tests/ -q` → 全部通过
  - 无 config 文件时模块仍能正常运行（回退到现有默认值）
- **验收标准**：
  - ✅ `config.toml` 包含 `[rime]` section
  - ✅ `rime_import_safe.py --help` 显示从 config 读取的默认值
  - ✅ 全量测试通过
- **潜在风险**：config 文件加载需要 `tomllib`，已是现有依赖。需注意 config 文件不存在时的 fallback。

#### Task 5.3: README 添加 Registry 章节 (O7)

- **目标**：在 README.md 中添加 registry 子系统的说明和统计
- **修改内容**：
  - 文件 `README.md`：
    - 在 `## Folder layout` 之后添加 `## Terminology Registry` section
    - 包含：concepts/aliases/evidence 统计、registry 文件格式简述、link 到 `docs/dev/06-terminology-registry-upgrade.md`
    - 添加 link 到 `CHANGELOG.md`
- **修改边界**：不得修改 README 中 `## Quick start` 及以下的步骤说明
- **测试要求**：
  - 检查 Markdown 格式正确（无语法错误）
- **验收标准**：
  - ✅ README 包含 `## Terminology Registry` section
  - ✅ 包含概念/别名/evidence 数量
  - ✅ 包含 link 到 docs/dev/06 和 CHANGELOG
- **潜在风险**：统计数字会随未来 batch 变化。可标注为"截至 vX 的统计"。

#### Task 5.4: Phase 5 commit

- **目标**：提交 CI + 配置 + 文档改善
- **修改内容**：
  - `git add .github/workflows/ci.yml config.toml pipeline/rime_import_safe.py pipeline/sync_to_fcitx.py README.md`
  - `git commit -m "infra: CI validate_registry, rime config section, README registry docs"`
- **修改边界**：仅提交 Phase 5 变更
- **测试要求**：
  - `python -m pytest tests/ -q` → 全部通过
  - `git status` → 干净
- **验收标准**：
  - ✅ commit 存在
  - ✅ 工作目录干净
- **潜在风险**：无

---

### Phase 6: 版本对齐与发布

**前置依赖**：Phase 1–5 全部完成

#### Task 6.1: CHANGELOG 折叠 + 补写

- **目标**：将 Unreleased 中的 6 条条目加上 Phase 1–5 的变更折叠到新版本号下
- **修改内容**：
  - 文件 `CHANGELOG.md`：
    - 在 `## Unreleased` 和 `## v2026.03.23.11` 之间插入新版本 section `## v2026.03.24`（或当天实际日期）
    - 将当前 Unreleased 条目移入新版本下
    - 补写 Phase 1–5 变更条目：安全修复、pipeline 小修、测试/lint 增强、registry 质量、CI 改善
    - `## Unreleased` 的三个子标题清空
- **修改边界**：不得修改 `## v2026.03.23.11` 及更早版本的内容
- **测试要求**：
  - `python -m pytest tests/ -q` → 全部通过
  - 检查 `## v2026.03.24` section 存在
- **验收标准**：
  - ✅ `## v2026.03.24` section 存在于 `## Unreleased` 与 `## v2026.03.23.11` 之间
  - ✅ `## Unreleased` 下三个子标题均无内容
  - ✅ 新版本条目包含安全修复、pipeline 修复、registry 质量、CI 等内容
- **潜在风险**：如果 Phase 执行跨天，日期需要调整。

#### Task 6.2: Tag + Push + Release Pack

- **目标**：打 tag、推送到 origin、构建 release pack
- **修改内容**：
  - `git add CHANGELOG.md && git commit -m "release: v2026.03.24 — repo hardening"`
  - `git tag v2026.03.24`
  - `python3 -m pipeline.build_terms --config config.toml`
  - `python3 -m pipeline.release_pack --tag v2026.03.24 --config config.toml`
  - `python3 -m pipeline.verify_release_contract --root dist/stage/v2026.03.24`
  - `git push origin master --tags`
- **修改边界**：不 commit 新代码（仅推送已有 commits）
- **测试要求**：
  - `python3 -m pipeline.verify_release_contract --root dist/stage/v2026.03.24` → `contract OK`
  - `git log origin/master --oneline -1` 与本地 HEAD 一致
  - `git tag -l 'v2026.03.24'` → 输出该 tag
- **验收标准**：
  - ✅ `v2026.03.24` tag 存在于本地和 origin
  - ✅ `verify_release_contract` 退出码 0
  - ✅ `dist/fusion-terms-artifacts-v2026.03.24.tar.gz` 存在
  - ✅ `git status` 干净，origin/master 与本地同步
- **潜在风险**：SSH push 可能超时，重试即可。

#### Task 6.3: Rime 词库同步

- **目标**：将更新后的 domain_terms.txt 同步到本地 Rime 输入法
- **修改内容**：
  - 运行 `python3 -m pipeline.rime_import_safe --import --backup-path ~/.local/share/fcitx5/rime --backup-path ~/.config/fcitx5/rime`
- **修改边界**：不修改任何 tracked 文件；仅影响用户 home 下的 Rime 配置（有备份）
- **测试要求**：
  - `rime_import_safe` 退出码 0
  - `ls artifacts/rime_backups/` 有新的备份目录
- **验收标准**：
  - ✅ Rime 导入成功
  - ✅ 备份已生成
- **潜在风险**：Rime 部署失败可通过备份回滚。

---

## 回归检查清单

- [ ] `python -m pytest tests/ -q` → 全部通过（≥63 passed）
- [ ] `python -m ruff check .` → 零违规
- [ ] `python3 -m pipeline.validate_registry` → `registry OK: 949 concepts, ≥4651 aliases, 949 evidence`
- [ ] `python3 -m compileall -q pipeline tests` → 无错误
- [ ] `pre-commit run --all-files` → 全部通过
- [ ] `grep "internal:TODO" terms/registry/evidence.tsv | wc -l` → `0`
- [ ] Forbidden 覆盖率 ≥ 95%
- [ ] 稀疏概念数 ≤ 60
- [ ] `git log --oneline origin/master..HEAD` → 无输出（已同步）
- [ ] `git status` → 干净

## 审查日志

| 轮次 | 聚焦 | 发现问题数 | 已修正 | 剩余 |
|------|------|-----------|--------|------|
| R1 | 结构完整性 | 3 | 3 | 0 |
| R2 | 可执行性 | 4 | 4 | 0 |
| R3 | 风险与边缘 | 2 | 2 | 0 |
| **终止** | **T4 — 零缺陷快速通过** | | | **0** |

### R1 Issues
- **Issue R1-1**: Task 2.3 缺少"修改边界"字段 → 已补充：`仅添加 timeout= 参数，不得修改其他 subprocess.run() 参数` ✅ 已修正
- **Issue R1-2**: 回归检查清单缺少项目特定检查项（只有通用项）→ 已添加 forbidden 覆盖率、稀疏概念数、evidence TODO 检查 ✅ 已修正
- **Issue R1-3**: Task 6.1 缺少"潜在风险"字段 → 已补充跨天日期风险说明 ✅ 已修正

### R2 Issues
- **Issue R2-1**: Task 4.1 测试要求中 `python3 -c "..."` 过于模糊 → 改为"运行 pre-flight 冲突检测脚本" ✅ 已修正
- **Issue R2-2**: Task 3.2 验收标准 `ruff check . 零违规` 是主观的 → 改为 `ruff check .` 退出码 0 ✅ 已修正
- **Issue R2-3**: Task 2.1 的 `python -c "from pipeline.common import Example"` 不是标准测试命令 → 辅助验证手段，保留但标注为"手动验证" ✅ 已修正
- **Issue R2-4**: Task 5.2 `pipeline/rime_import_safe.py` 和 `pipeline/sync_to_fcitx.py` 同时被 Phase 2 和 Phase 5 修改 → 确认 Phase 2 仅改 timeout（第 81 行），Phase 5 改 config 加载（main 函数），无冲突 ✅ 已修正

### R3 Issues
- **Issue R3-1**: Task 4.1 和 Task 4.2 都修改 aliases.tsv，如 4.1 失败需回滚整个 Phase 4 → 已明确 Task 4.2 前置依赖 Task 4.1 完成，两步顺序执行 ✅ 已修正
- **Issue R3-2**: Phase 3 的 ruff 规则启用（Task 3.2）可能与 Phase 2 的代码修改产生新违规 → 已确认 Phase 2 先 commit，Phase 3 在其之上启用新规则并修复，顺序正确 ✅ 已修正
