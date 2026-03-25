# fusion-terms 仓库改进计划（v2026.03.25 审阅周期）

## 背景与目标

- **问题/需求描述**：2026-03-25 仓库审阅（[full-repo-2026-03-25.md](../reviews/full-repo-2026-03-25.md)）发现 3 🔴 / 7 🟡 / 7 🟢 共 17 项问题。v2026.03.24 加固周期已解决所有旧 🔴 项（路径穿越、rollback 信任、evidence TODO）。当前问题集中在三个维度：
  1. **验证器缺口**：`validate_registry.py` 不检查 `internal:TODO` 来源和 preferred 别名完备性（B1, B2）
  2. **可维护性**：`extract()` 函数 542 行，无法独立测试内部路径（Q1）
  3. **工具链一致性**：`rime_export.py` 不读 config、CI 仅单版本、ruff 版本分裂、静默异常吞掉（Q2–Q5, O1–O3, B3）

- **根因分析**：
  - B1/B2：验证器随 registry 从 v0 演进到 949 概念，但校验规则未同步增长
  - Q1：`extract()` 从早期原型积累至今，未经过分解重构
  - Q4/Q5/O3：增量添加 Rime 脚本时未统一 config 读取模式和版本锁定

- **目标**：
  1. 修复 B1 + B2 验证器缺口（立即保护 registry 数据质量）
  2. 修复 Q2 + Q3 静默异常 + B3 缓存签名测试
  3. 统一 `rime_export.py` config 读取 + 集中 `[rime].import_script` 配置（Q4 + Q5）
  4. 补充 `rime_export.py` 测试（O4）
  5. 升级 CI（Python 矩阵 + coverage + mypy + format 门禁；ruff 版本同步）（O1 + O2 + O3）
  6. 分解 `extract()` 函数（Q1）
  7. 文档收尾（O5 + O6 + IT-2 + IT-3 + Q6 + Q7 + B4）

- **非目标（不做什么）**：
  - 不新增 registry 概念/别名/evidence 数据
  - 不修改 `extract_candidates.py` 的 NLP 算法（仅结构重构）
  - 不引入新框架或外部依赖（mypy 除外，已是标准工具）
  - 不修改 `registry/*.tsv` 的 schema 格式

## 技术方案

- **方案概述**：分 6 Phase、22 个 Task 执行。Phase 1–2 快速修复验证器和静默异常（高保护/低风险），Phase 3 统一 Rime config 模式，Phase 4 升级 CI/工具链，Phase 5 专项分解 `extract()` 函数（最大变更，独立 Phase），Phase 6 文档/杂项收尾。
- **关键设计决策**：
  - Phase 1 先修验证器（阻断损坏数据进入），再改功能代码
  - Phase 5（`extract()` 重构）独立成 Phase，因为它是核心抽词管线且需建立回归基线
  - 每个 Phase 自成一个 commit，可独立回滚
  - `extract()` 重构采用"先提取内部函数→再验证输出等价"策略，避免行为变更
- **影响范围**：
  - `pipeline/validate_registry.py`、`pipeline/extract_candidates.py`、`pipeline/review_pack.py`、`pipeline/rime_export.py`、`pipeline/rime_import_safe.py`、`pipeline/generate_dict_yaml.py`
  - `tests/test_registry_validator.py`（扩展）、`tests/test_rime_export.py`（新建）、`tests/test_extractor_signature.py`（新建）
  - `.github/workflows/ci.yml`、`.pre-commit-config.yaml`、`requirements-dev.txt`、`pyproject.toml`、`config.toml`
  - `README.md`、`CONTRIBUTING.md`（新建）、`docs/dev/06-*.md`、`docs/dev/09-*.md`、`docs/dev/10-*.md`

## 执行计划

### Phase 1: 验证器加固

#### ✅ Task 1.1: 拒绝 `internal:TODO` evidence 来源 (B1)

- **目标**：在 `validate_registry.py` 的 evidence 循环中拒绝以 `internal:` 开头的 source 值，防止占位符来源被静默接受
- **修改内容**：
  - 文件 `pipeline/validate_registry.py`（evidence 循环，在 L159 非空检查之后、L160 `evidence_concept_ids.add()` 之前）：
    - 新增检查：`if source.startswith("internal:"): _fail(evidence_path, r.lineno, f"placeholder evidence source not allowed: {source!r}")`
  - 文件 `tests/test_registry_validator.py`：
    - 新增测试 `test_validate_registry_rejects_internal_todo_evidence()`：构造含 `internal:TODO:xxx` 来源的 evidence.tsv，断言 `SystemExit` 且 stderr 包含 `placeholder evidence source`
    - 新增测试 `test_validate_registry_accepts_url_evidence()`：构造含 `https://...` 来源的 evidence.tsv，断言 return code 0
- **修改边界**：不得修改 evidence 循环的其他校验逻辑；不得修改 `_fail()` 函数签名；不修改 `terms/registry/evidence.tsv`
- **测试要求**：
  - `python -m pytest tests/test_registry_validator.py -v` → 新增测试通过，现有测试不回归
  - `python -m pytest tests/ -q` → 全部通过（≥69 passed，含新增测试）
  - `python3 -m pipeline.validate_registry` → `registry OK`（当前数据无 `internal:*` 来源）
- **验收标准**：
  - ✅ 含 `internal:TODO:xxx` 来源的 evidence 被拒绝并报告行号
  - ✅ 含正常 URL 来源的 evidence 通过
  - ✅ 当前 registry 数据通过验证（0 条 internal 来源）
  - ✅ 全量测试通过
- **潜在风险**：如果未来有合法的 `internal:` 前缀用途，需要调整正则。当前仅 `internal:TODO` 历史上出现过，前缀匹配足够安全。

#### ✅ Task 1.2: 检查每个 concept 至少有一条 preferred 别名 (B2)

- **目标**：在 `validate_registry.py` 的 alias 循环结束后、evidence 循环之前，检查每个 concept_id 至少有 1 条 `kind=preferred` 的别名
- **修改内容**：
  - 文件 `pipeline/validate_registry.py`（在 aliases 循环结束后，约 L143–L144 之间，evidence 块 L145 之前）：
    - 在 aliases 循环中收集 `concepts_with_preferred: set[str]`（遇到 `kind == "preferred"` 时 add concept_id）
    - 循环结束后检查：`missing_preferred = sorted(concept_ids - concepts_with_preferred)`
    - 若非空：`_fail(aliases_path, 0, f"concepts without preferred alias: {missing_preferred[:10]}...")`
  - 文件 `tests/test_registry_validator.py`：
    - 新增测试 `test_validate_registry_rejects_concept_without_preferred_alias()`：构造概念有 alias 但无 preferred 的 registry，断言 `SystemExit` 且包含 `without preferred alias`
- **修改边界**：不得修改 aliases 循环的其他校验逻辑（kind 校验、冲突检查等保持不变）；不得修改 `pipeline/export_registry.py`
- **测试要求**：
  - `python -m pytest tests/test_registry_validator.py -v` → 新增测试通过
  - `python3 -m pipeline.validate_registry` → `registry OK`（当前所有 949 概念均有 preferred）
  - `python -m pytest tests/ -q` → 全部通过
- **验收标准**：
  - ✅ 缺少 preferred 别名的概念被拒绝并列出概念 ID
  - ✅ 当前 registry 通过（949/949 有 preferred）
  - ✅ 全量测试通过
- **潜在风险**：若用户在 batch 入库时忘记添加 preferred 别名，此检查会立即阻断——这正是期望行为。

#### ✅ Task 1.3: Phase 1 commit

- **目标**：提交验证器加固
- **修改内容**：
  - `git add pipeline/validate_registry.py tests/test_registry_validator.py`
  - `git commit -m "validator: reject internal:TODO sources, require preferred alias per concept (B1+B2)"`
- **修改边界**：仅提交 Phase 1 变更
- **测试要求**：
  - `python -m pytest tests/ -q` → 全部通过
  - `git status` → 干净
- **验收标准**：
  - ✅ commit 存在
  - ✅ 工作目录干净
- **潜在风险**：无

---

### Phase 2: 静默异常修复 + 缓存签名测试

#### ✅ Task 2.1: 为缓存路径的 bare except 添加 warning (Q2)

- **目标**：在 `extract_candidates.py` 的 4 处 bare `except Exception` 中添加 `warnings.warn()`，使缓存损坏可观测
- **修改内容**：
  - 文件 `pipeline/extract_candidates.py`：
    - L246（`_load_cache_index`）：在 `return {}` 前添加 `warnings.warn(f"cache index corrupted, rebuilding: {e}", stacklevel=2)`
    - L267（`_cache_entry_from_dict`）：在 `return None` 前添加 `warnings.warn(f"cache entry malformed: {e}", stacklevel=2)`
    - L431（`extract()` 内 cache hit path）：在 `can_use_cache = False` 前添加 `warnings.warn(f"cache entry unreadable for {rel_posix}: {e}", stacklevel=2)`
    - L509（`extract()` 内 old cache data）：在 `old_zh_counts = {}` 前添加 `warnings.warn(f"old cache data unreadable for {rel_posix}: {e}", stacklevel=2)`
    - 在文件顶部确保 `import warnings`（如尚未导入）
  - 所有 4 处均**保持原有 fallback 行为不变**，仅新增 warning
- **修改边界**：不得修改 fallback 逻辑本身（仍 `return {}`/`return None`/`can_use_cache = False`/`= {}`）；不得修改 `extract()` 的公共接口
- **测试要求**：
  - `python -m pytest tests/ -q` → 全部通过（warning 不影响功能）
  - `python -m ruff check pipeline/extract_candidates.py` → 无新违规
- **验收标准**：
  - ✅ 4 处 bare except 均包含 `warnings.warn()` 调用
  - ✅ 全量测试通过
  - ✅ `import warnings` 存在于文件顶部
- **潜在风险**：现有测试如果开启 `warnings.simplefilter("error")`，可能因测试 fixture 不完整触发新 warning。但当前测试使用干净 fixture 且无损坏缓存，不会触发。

#### ✅ Task 2.2: 为 review_pack.py TSV 解析添加 warning (Q3)

- **目标**：在 `review_pack.py` L115 的 `except Exception` 中添加 warning，使损坏 TSV 行可观测
- **修改内容**：
  - 文件 `pipeline/review_pack.py`（L115）：
    - 在 `cnt = 0` 前添加 `warnings.warn(f"non-integer count in TSV row, defaulting to 0: {parts[1]!r}", stacklevel=2)`
    - 确保 `import warnings` 在文件顶部
- **修改边界**：不得修改 fallback 行为（仍设 `cnt = 0`）；不得修改 `_write_rows()` 或其他函数
- **测试要求**：
  - `python -m pytest tests/test_review_pack.py -v` → 通过
  - `python -m pytest tests/ -q` → 全部通过
- **验收标准**：
  - ✅ L115 包含 `warnings.warn()` 调用
  - ✅ 全量测试通过
- **潜在风险**：如果 review pack fixture 有含非整数 count 的行，新 warning 会被触发但不影响结果。

#### ✅ Task 2.3: 添加 `_extractor_signature()` 单元测试 (B3)

- **目标**：验证 `_extractor_signature()` 在参数变化时产生不同签名，防止缓存签名回归
- **修改内容**：
  - 新建文件 `tests/test_extractor_signature.py`：
    - `test_signature_changes_with_min_zh_len()`：同参数仅改 `min_zh_len`，断言两个签名不等
    - `test_signature_changes_with_en_phrases()`：同参数仅改 `en_phrases`（`"rake"` vs `"off"`），断言两个签名不等
    - `test_signature_deterministic()`：同参数调用两次，断言签名相等
    - 导入方式：`from pipeline.extract_candidates import _extractor_signature`
- **修改边界**：不得修改 `_extractor_signature()` 函数本身；仅新建测试文件
- **测试要求**：
  - `python -m pytest tests/test_extractor_signature.py -v` → 3 passed
  - `python -m pytest tests/ -q` → 全部通过（≥72 passed）
- **验收标准**：
  - ✅ 参数变化导致签名变化
  - ✅ 相同参数产生相同签名
  - ✅ 全量测试通过
- **潜在风险**：`_extractor_signature` 以下划线开头为"私有"，但 Python 中可直接导入，测试此类函数是合理的。

#### ✅ Task 2.4: Phase 2 commit

- **目标**：提交静默异常修复和签名测试
- **修改内容**：
  - `git add pipeline/extract_candidates.py pipeline/review_pack.py tests/test_extractor_signature.py`
  - `git commit -m "fix: add warnings for silent cache/TSV exceptions, add extractor signature test (Q2+Q3+B3)"`
- **修改边界**：仅提交 Phase 2 变更
- **测试要求**：
  - `python -m pytest tests/ -q` → 全部通过
  - `git status` → 干净
- **验收标准**：
  - ✅ commit 存在
  - ✅ 工作目录干净
- **潜在风险**：无

---

### Phase 3: Rime 配置统一

#### ✅ Task 3.1: 在 `config.toml` 添加 `[rime].import_script` (Q5 前置)

- **目标**：在 `config.toml` 的 `[rime]` section 中添加 `import_script` 键，将硬编码的 `~/.local/bin/rime_import_wordlist.py` 路径集中管理
- **修改内容**：
  - 文件 `config.toml`（`[rime]` section 末尾，L38 之后）：
    - 添加 `import_script = "~/.local/bin/rime_import_wordlist.py"`
- **修改边界**：不得修改 `[rime]` 的现有键（`dict_name`、`backup_paths`、`sync_dest`）；不得修改 pipeline 代码（本 Task 仅改配置）
- **测试要求**：
  - `python -m pytest tests/ -q` → 全部通过（config 变更不影响测试）
  - `python -c "import tomllib; print(tomllib.loads(open('config.toml').read())['rime']['import_script'])"` → 输出路径
- **验收标准**：
  - ✅ `config.toml` 的 `[rime]` section 包含 `import_script` 键
  - ✅ 全量测试通过
- **潜在风险**：无

#### ✅ Task 3.2: 让 `rime_export.py` 读取 config.toml (Q4)

- **目标**：让 `rime_export.py` 像 `rime_import_safe.py` 和 `sync_to_fcitx.py` 一样从 `config.toml` 加载 `[rime]` 默认值
- **修改内容**：
  - 文件 `pipeline/rime_export.py`：
    - 在 argparser 中添加 `--config` 参数（default: `config.toml`），位于其他参数之前
    - 在 `args = parser.parse_args()` 之后（L69），添加 config 加载逻辑（参考 `rime_import_safe.py` 的实现模式）：
      - 加载 `[rime]` section
      - 用 config 值作为 `--dict-name` 的默认值（如 CLI 未显式指定）
      - 用 config 值作为 `--rime-script` 的默认值（`[rime].import_script`）
    - CLI 显式参数始终覆盖 config 值（保持向后兼容）
- **修改边界**：不得修改 `rime_export.py` 的输出格式或 Rime 导入行为；不得修改 `rime_import_safe.py` 或 `sync_to_fcitx.py`
- **测试要求**：
  - `python -m pipeline.rime_export --help` → 显示 `--config` 参数
  - `python -m pytest tests/ -q` → 全部通过
  - 无 config 文件时模块仍能正常运行（回退到硬编码默认值）
- **验收标准**：
  - ✅ `rime_export.py --help` 包含 `--config` 选项
  - ✅ config 中 `[rime].dict_name` 被作为 `--dict-name` 的默认值
  - ✅ config 中 `[rime].import_script` 被作为 `--rime-script` 的默认值
  - ✅ CLI 参数可覆盖 config值
  - ✅ 全量测试通过
- **潜在风险**：`rime_export.py` 当前使用 `sys.executable` 调用子进程，config 加载不影响此路径。

#### ✅ Task 3.3: 统一 3 个脚本的 `import_script` 默认值来源 (Q5)

- **目标**：让 `rime_import_safe.py` 和 `generate_dict_yaml.py` 也从 `[rime].import_script` 读取默认 rime script 路径，消除 3 处硬编码
- **修改内容**：
  - 文件 `pipeline/rime_import_safe.py`（L290）：
    - 将 `--rime-script` 的 `default=str(Path("~/.local/bin/rime_import_wordlist.py"))` 改为从 config 加载的值（如 config 可用），否则回退到现有默认值
  - 文件 `pipeline/generate_dict_yaml.py`（L153）：
    - 同上模式
  - 确保两个脚本在无 config 时仍正常工作
- **修改边界**：不得修改脚本的功能行为；不得移除 CLI `--rime-script` 参数（保持向后兼容）
- **测试要求**：
  - `python -m pytest tests/ -q` → 全部通过
  - `python -m pipeline.rime_import_safe --help` 和 `python -m pipeline.generate_dict_yaml --help` → 均显示 `--rime-script` 参数
- **验收标准**：
  - ✅ `grep -rn "~/.local/bin/rime_import_wordlist.py" pipeline/` → 0 匹配（硬编码已消除）
  - ✅ CLI `--rime-script` 仍可覆盖 config 值
  - ✅ 全量测试通过
- **潜在风险**：如果 config.toml 不存在（如 CI 环境），脚本需优雅 fallback。参考 `rime_import_safe.py` 现有的 config fallback 模式。

#### ✅ Task 3.4: 新建 `tests/test_rime_export.py` (O4)

- **目标**：为唯一缺少专用测试的 pipeline 模块补充单元测试
- **修改内容**：
  - 新建文件 `tests/test_rime_export.py`：
    - `test_rime_export_writes_output(tmp_path)`：创建简单 domain_terms.txt，调用 rime_export，断言输出文件存在且内容包含预期行
    - `test_rime_export_respects_config_dict_name(tmp_path)`：创建 config.toml 含 `[rime].dict_name = "test_dict"`，验证输出中使用了 config 的 dict_name
    - `test_rime_export_cli_overrides_config(tmp_path)`：传入 `--dict-name other` 同时有 config，验证 CLI 优先
    - 使用 `monkeypatch.setattr("sys.argv", ...)` 或 subprocess 调用
- **修改边界**：不得修改 `pipeline/rime_export.py`（本 Task 仅新增测试）；测试仅操作 `tmp_path`
- **测试要求**：
  - `python -m pytest tests/test_rime_export.py -v` → ≥3 passed
  - `python -m pytest tests/ -q` → 全部通过（≥75 passed）
- **验收标准**：
  - ✅ `tests/test_rime_export.py` 存在，包含 ≥3 个测试函数
  - ✅ 全量测试通过
- **潜在风险**：`rime_export.py` 在无 `--rime-script` 路径指向有效脚本时会跳过 import 步骤，测试需仅验证输出文件生成（不触发实际 Rime 导入）。

#### ✅ Task 3.5: Phase 3 commit

- **目标**：提交 Rime 配置统一
- **修改内容**：
  - `git add config.toml pipeline/rime_export.py pipeline/rime_import_safe.py pipeline/generate_dict_yaml.py tests/test_rime_export.py`
  - `git commit -m "config: unify rime script path via [rime].import_script, add config support to rime_export (Q4+Q5+O4)"`
- **修改边界**：仅提交 Phase 3 变更
- **测试要求**：
  - `python -m pytest tests/ -q` → 全部通过
  - `git status` → 干净
- **验收标准**：
  - ✅ commit 存在
  - ✅ 工作目录干净
- **潜在风险**：无

---

### Phase 4: CI/工具链升级

#### Task 4.1: 扩展 CI Python 矩阵 + 添加 coverage/mypy/format (O1 + O2)

- **目标**：CI 覆盖 Python 3.10/3.11/3.12，并添加 coverage、mypy 类型检查、ruff format 门禁
- **修改内容**：
  - 文件 `.github/workflows/ci.yml`：
    - 替换 `python-version: "3.11"` 为 `strategy.matrix.python-version: ["3.10", "3.11", "3.12"]`
    - 在 `Install dependencies` 步骤中添加 `pip install pytest-cov mypy`
    - 修改 `Run tests` 步骤为 `pytest --cov=pipeline --cov-fail-under=75`（起始阈值保守设为 75）
    - 新增步骤 `Mypy type check`：`mypy pipeline/ --ignore-missing-imports --no-error-summary`（初始宽松；后续可收紧）
    - 新增步骤 `Ruff format check`：`ruff format --check .`
  - 文件 `requirements-dev.txt`：
    - 添加 `pytest-cov>=4.0` 和 `mypy>=1.8`
- **修改边界**：不得修改 pipeline 源代码；不得修改测试（仅 CI + dev dependencies）
- **测试要求**：
  - 本地验证：`python -m pytest --cov=pipeline tests/ -q` → 通过（coverage ≥75%）
  - 本地验证：`mypy pipeline/ --ignore-missing-imports` → 无致命错误
  - 本地验证：`ruff format --check .` → 通过
  - YAML 语法检查：`python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"` → 无错误
- **验收标准**：
  - ✅ CI workflow 使用 matrix: `["3.10", "3.11", "3.12"]`
  - ✅ CI 包含 coverage、mypy、format check 步骤
  - ✅ 本地 `pytest --cov` 通过且 coverage ≥ 75%
  - ✅ 本地 `mypy` 无致命错误
  - ✅ 本地 `ruff format --check .` 通过
- **潜在风险**：mypy 可能在 pipeline 模块中发现类型不匹配。用 `--ignore-missing-imports` 和初轮宽松模式降低阻断风险。如果 mypy 报错过多（>20 条），则改为 `mypy pipeline/ || true`（仅报告，不阻断），在后续专项修复。

#### Task 4.2: 同步 ruff 版本 (O3)

- **目标**：确保 pre-commit 和 requirements-dev.txt 使用一致的 ruff 版本
- **修改内容**：
  - 文件 `requirements-dev.txt`：
    - `ruff>=0.6.0` → `ruff>=0.15.0`（与 pre-commit hook 的 `rev: v0.15.0` 对齐）
  - 文件 `.pre-commit-config.yaml`：保持 `rev: v0.15.0` 不变
- **修改边界**：不得修改 ruff 的 lint 规则配置（`pyproject.toml` 不变）；不得修改其他 hooks
- **测试要求**：
  - `pip install ruff>=0.15.0` → 安装成功
  - `ruff check .` → 通过
  - `pre-commit run --all-files` → 全部通过
- **验收标准**：
  - ✅ `requirements-dev.txt` 中 ruff 下限 ≥ 0.15.0
  - ✅ pre-commit ruff hook 和 requirements-dev 声明的版本区间有交集
  - ✅ `pre-commit run --all-files` 通过
- **潜在风险**：如果用户环境中 pip 缓存了旧 ruff，需 `pip install --upgrade ruff`。

#### Task 4.3: Phase 4 commit

- **目标**：提交 CI/工具链升级
- **修改内容**：
  - `git add .github/workflows/ci.yml requirements-dev.txt .pre-commit-config.yaml`
  - `git commit -m "ci: Python matrix 3.10/3.11/3.12, add coverage+mypy+format gates, sync ruff version (O1+O2+O3)"`
- **修改边界**：仅提交 Phase 4 变更
- **测试要求**：
  - `python -m pytest tests/ -q` → 全部通过
  - `pre-commit run --all-files` → 通过
  - `git status` → 干净
- **验收标准**：
  - ✅ commit 存在
  - ✅ 工作目录干净
- **潜在风险**：无

---

### Phase 5: `extract()` 函数分解重构 (Q1)

**前置依赖**：Phase 2 完成（缓存 warning 已就位，重构期间可观测异常行为）

#### Task 5.1: 建立回归基线

- **目标**：在重构前用当前代码对 test fixture corpus 执行一次完整抽词，保存输出快照作为回归基准
- **修改内容**：
  - 新建文件 `tests/test_extract_regression.py`：
    - `test_extract_output_matches_baseline(tmp_path)`：
      - 调用 `extract()` 以 `tests/fixtures/corpus` 为 source root，写入 `tmp_path`
      - 比对 `candidates_zh.tsv` 和 `candidates_en.tsv` 的行数和前 20 行内容与预存基线
    - `test_extract_stats_keys(tmp_path)`：
      - 验证 `extract_stats.json` 包含预期 key 集合
  - 新建文件 `artifacts/_smoke_run/baseline_extract_zh_head.tsv`：当前 fixture 输出的前 20 行
  - 新建文件 `artifacts/_smoke_run/baseline_extract_en_head.tsv`：当前 fixture 输出的前 20 行
- **修改边界**：不得修改 `pipeline/extract_candidates.py` 源代码；仅新增测试和基线文件
- **测试要求**：
  - `python -m pytest tests/test_extract_regression.py -v` → 2 passed
  - `python -m pytest tests/ -q` → 全部通过
- **验收标准**：
  - ✅ 回归测试文件存在且通过
  - ✅ 基线快照文件存在
  - ✅ 全量测试通过
- **潜在风险**：fixture corpus 如果变化，基线需重新生成。测试应在 assert 之前检查基线是否存在并给出明确错误信息。

#### Task 5.2: 提取缓存管理函数

- **目标**：将 `extract()` 中的缓存加载/保存/查询逻辑提取为独立的顶层函数
- **修改内容**：
  - 文件 `pipeline/extract_candidates.py`：
    - 新建函数 `_load_cached_results(cache_dir, index, extractor_sig, rel_posix, md_path) -> tuple[dict|None, bool]`：
      - 封装 L385–L436（缓存命中判断 + 结果读取）的逻辑
      - 返回 `(data_dict, cache_hit)` 或 `(None, False)` 表示未命中
    - 新建函数 `_save_file_cache(cache_dir, index, extractor_sig, rel_posix, md_path, result_dict) -> None`：
      - 封装 L660–L700 的缓存写入逻辑
    - 更新 `extract()` 调用新函数替代内联代码
    - **行为必须完全等价**：缓存命中/未命中路径、warning 触发、结果数据完全一致
- **修改边界**：不得修改 `extract()` 的参数列表或返回值；不得修改 NLP 提取逻辑；不得修改输出文件格式
- **测试要求**：
  - `python -m pytest tests/test_extract_regression.py -v` → 基线回归通过（输出不变）
  - `python -m pytest tests/test_incremental_cache.py -v` → 缓存测试通过
  - `python -m pytest tests/ -q` → 全部通过
- **验收标准**：
  - ✅ 回归测试通过（输出与基线一致）
  - ✅ 缓存测试通过
  - ✅ `_load_cached_results` 和 `_save_file_cache` 作为独立函数存在
  - ✅ `extract()` 行数减少 ≥60 行
- **潜在风险**：缓存逻辑依赖 `extract()` 内部状态（`index`、`extractor_sig`）。需通过参数传递。

#### Task 5.3: 提取输出写入函数

- **目标**：将 `extract()` 末尾的 TSV/JSON 输出写入逻辑提取为独立函数
- **修改内容**：
  - 文件 `pipeline/extract_candidates.py`：
    - 新建函数 `_write_extract_outputs(out_dir, zh_counts, en_counts, en_phrase_counts, ...) -> dict`：
      - 封装 L700–L820 的 `write_tsv` 内部函数调用、stats JSON 写入、delta JSON 写入
      - 返回 stats dict（给调用方日志使用）
    - 将 `extract()` 中的 nested `write_tsv` 函数提升为模块级 `_write_tsv()`
    - 更新 `extract()` 调用新函数
- **修改边界**：不得修改输出文件格式或内容；不得修改 NLP 逻辑
- **测试要求**：
  - `python -m pytest tests/test_extract_regression.py -v` → 基线回归通过
  - `python -m pytest tests/test_extract_filtered_outputs.py -v` → filter 测试通过
  - `python -m pytest tests/ -q` → 全部通过
- **验收标准**：
  - ✅ 回归测试通过
  - ✅ 过滤输出测试通过
  - ✅ `_write_extract_outputs` 和 `_write_tsv` 作为独立函数存在
  - ✅ `extract()` 行数减少 ≥80 行（累计减少 ≥140 行）
- **潜在风险**：`write_tsv` nested function 捕获了外部变量（`out_dir` 等），提取时需改为参数传递。

#### Task 5.4: 提取 per-file 处理函数

- **目标**：将 `extract()` 中按文件处理的主循环体（文本读取→NLP 提取→计数合并）提取为独立函数
- **修改内容**：
  - 文件 `pipeline/extract_candidates.py`：
    - 新建函数 `_process_single_file(md_path, rel_posix, zh_re, ...) -> tuple[Counter, Counter, Counter, list]`：
      - 封装 L500–L660 的 per-file 处理逻辑（文本读取、clean_markdown、NLP 提取、计数）
      - 返回 `(file_zh_counts, file_en_counts, file_en_phrase_counts, file_examples)`
    - 更新 `extract()` 主循环调用新函数
- **修改边界**：不得修改 NLP 提取算法；不得修改缓存逻辑（已在 Task 5.2 提取）
- **测试要求**：
  - `python -m pytest tests/test_extract_regression.py -v` → 基线回归通过
  - `python -m pytest tests/ -q` → 全部通过
- **验收标准**：
  - ✅ 回归测试通过
  - ✅ `_process_single_file` 作为独立函数存在
  - ✅ `extract()` 最终行数 ≤ 200 行（从 542 行降至 ≤200 行）
- **潜在风险**：per-file 循环体引用了大量外部变量（计数器、缓存索引、config 参数）。需仔细列出所有依赖，通过参数传递。如遗漏任何捕获变量，回归测试会立即捕获。

#### Task 5.5: Phase 5 commit

- **目标**：提交 `extract()` 重构
- **修改内容**：
  - `git add pipeline/extract_candidates.py tests/test_extract_regression.py artifacts/_smoke_run/baseline_extract_*.tsv`
  - `git commit -m "refactor: decompose extract() from 542 lines to ≤200 lines (Q1)"`
- **修改边界**：仅提交 Phase 5 变更
- **测试要求**：
  - `python -m pytest tests/ -q` → 全部通过
  - `git status` → 干净
- **验收标准**：
  - ✅ commit 存在
  - ✅ 工作目录干净
  - ✅ `wc -l` 确认 `extract()` 函数体 ≤ 200 行
- **潜在风险**：大重构可能遗留间距/import 问题。commit 前跑 `ruff` 和 `pre-commit`。

---

### Phase 6: 文档与杂项收尾

#### Task 6.1: README 版本锚定 + CONTRIBUTING.md (O5 + O6)

- **目标**：在 README 中锚定 registry 统计版本，并创建 CONTRIBUTING.md
- **修改内容**：
  - 文件 `README.md`：
    - 将 "Current snapshot (as of this hardening cycle)" 替换为 "Current snapshot (as of v2026.03.24.1)"
  - 新建文件 `CONTRIBUTING.md`：
    - 包含：环境搭建（clone + venv + requirements-dev）、运行测试、pre-commit、commit 规范、registry 数据入库流程（concepts→aliases→evidence→validate）、release 流程概述
    - 简洁风格，不超过 80 行
- **修改边界**：不得修改 README 的 Quick Start 或 de-ai-fier 集成部分
- **测试要求**：
  - Markdown 格式正确（无语法错误）
  - `pre-commit run --all-files` → 通过
- **验收标准**：
  - ✅ README 包含具体版本号引用
  - ✅ `CONTRIBUTING.md` 存在，包含环境搭建、测试、commit、registry 约定
  - ✅ pre-commit 通过
- **潜在风险**：CONTRIBUTING.md 内容需后续随流程演进更新。初版写清核心即可。

#### Task 6.2: 标记历史文档为已完成 (IT-2 + IT-3)

- **目标**：在已实现的计划文档顶部添加状态标记，避免新读者误以为待办
- **修改内容**：
  - 文件 `docs/dev/06-terminology-registry-upgrade.md`：在标题行之后添加 `> ✅ **状态：已实现** — registry 于 v2026.03.16 上线，949 concepts / 4647 aliases（截至 v2026.03.24.1）。本文保留为设计参考。`
  - 文件 `docs/dev/09-release-v2026.02.09.md`：在第 4 行 `状态：已发布` 后无需修改（已标记为已发布）
  - 文件 `docs/dev/10-execution-plan.md`：在标题行之后添加 `> ✅ **状态：已完成** — 本计划所有阶段均已执行，保留为执行记录。`
- **修改边界**：仅在文件顶部追加状态标注，不得修改原文内容
- **测试要求**：
  - 检查 Markdown 格式正确
- **验收标准**：
  - ✅ `docs/dev/06-*.md` 包含"已实现"状态标记
  - ✅ `docs/dev/10-*.md` 包含"已完成"状态标记
- **潜在风险**：无

#### Task 6.3: 次要修复 (Q6 + Q7 + B4)

- **目标**：处理低优先级的常量暴露、清理日志、文档补充
- **修改内容**：
  - 文件 `pipeline/common.py`（L180 `read_text_file`）：将 `max_bytes` 默认值注释中标注来源（`# 10 MB per-file limit; override via caller`）——不暴露到 config（config 变更收益低于复杂度）
  - 文件 `pipeline/generate_dict_yaml.py`（L117）：将 `except Exception: pass` 改为 `except Exception: pass  # best-effort temp cleanup`（仅添加行内注释，无需 logging/warning）
  - 文件 `pipeline/extract_candidates.py`（`_extract_en_phrases_rake` 函数上方）：在 docstring 中添加一行说明内部 RAKE stopword set 的行为
- **修改边界**：不得修改任何函数的逻辑行为
- **测试要求**：
  - `python -m pytest tests/ -q` → 全部通过
- **验收标准**：
  - ✅ `read_text_file` 的 `max_bytes` 有注释说明
  - ✅ `generate_dict_yaml.py` L117 有注释
  - ✅ `_extract_en_phrases_rake` docstring 描述了内部 stopword 行为
  - ✅ 全量测试通过
- **潜在风险**：无

#### Task 6.4: Phase 6 commit + 版本对齐 + push

- **目标**：提交文档/杂项收尾，更新 CHANGELOG，tag + push
- **修改内容**：
  - 更新 `CHANGELOG.md`：fold Unreleased 条目到新版本号（按当天日期）
  - `git add` 所有 Phase 6 变更
  - `git commit -m "docs: version-anchor README, add CONTRIBUTING.md, mark historical docs, minor fixes (O5+O6+IT2+IT3+Q6+Q7+B4)"`
  - `git tag vYYYY.MM.DD`（按当天日期确定版本号）
  - `git push origin master --tags`
- **修改边界**：仅提交 Phase 6 变更
- **测试要求**：
  - `python -m pytest tests/ -q` → 全部通过
  - `pre-commit run --all-files` → 通过
  - `git status` → 干净
- **验收标准**：
  - ✅ 新 tag 存在于 origin
  - ✅ CHANGELOG 包含新版本记录
  - ✅ 工作目录干净
- **潜在风险**：SSH push 超时可重试

---

## 回归检查清单

- [ ] `python -m pytest tests/ -q` → 全部通过（≥75 passed）
- [ ] `python -m ruff check .` → 零违规
- [ ] `python3 -m pipeline.validate_registry` → `registry OK: 949 concepts, ≥4647 aliases, 949 evidence`
- [ ] `python3 -m compileall -q pipeline tests` → 无错误
- [ ] `pre-commit run --all-files` → 全部通过
- [ ] `python -m pytest --cov=pipeline tests/ -q` → coverage ≥ 75%
- [ ] `mypy pipeline/ --ignore-missing-imports` → 无致命错误（或 `|| true`）
- [ ] `ruff format --check .` → 通过
- [ ] `grep -rn "~/.local/bin/rime_import_wordlist.py" pipeline/` → 0 匹配
- [ ] `wc -l` 确认 `extract()` 函数体 ≤ 200 行
- [ ] CONTRIBUTING.md 存在
- [ ] `git log origin/master --oneline -1` 与本地 HEAD 一致

## 审查日志

| 轮次 | 聚焦 | 发现问题数 | 已修正 | 剩余 |
|------|------|-----------|--------|------|
| R1 | 结构完整性 | 4 | 4 | 0 |
| R2 | 可执行性 | 5 | 5 | 0 |
| R3 | 风险与边缘 | 3 | 3 | 0 |
| **终止** | **T4 — 零缺陷快速通过** | | | **0** |

### R1 Issues
- **Issue R1-1**: Task 5.1 缺少"修改边界"字段 → 已补充 ✅ 已修正
- **Issue R1-2**: 回归检查清单缺少项目特定检查项（只有通用项）→ 已添加 coverage ≥ 75%、硬编码消除验证、`extract()` 行数验证、CONTRIBUTING.md 存在 ✅ 已修正
- **Issue R1-3**: Task 4.1 缺少"潜在风险"字段 → 已补充 mypy 报错过多应对方案 ✅ 已修正
- **Issue R1-4**: Task 6.2 的 `docs/dev/09-*` 在审阅中标注为"已发布"但 Task 仍列为修改 → 确认无需修改，调整描述 ✅ 已修正

### R2 Issues
- **Issue R2-1**: Task 5.4 修改超过 3 个文件 → 确认仅修改 1 个文件 `extract_candidates.py`，审阅误判 ✅ 已修正（描述已明确）
- **Issue R2-2**: Task 4.1 的 "coverage ≥ 75%" 阈值缺少验证命令 → 已添加本地验证命令 `python -m pytest --cov=pipeline tests/` ✅ 已修正
- **Issue R2-3**: Task 3.3 的验收标准 `grep` 命令要求输出 0 匹配——需确认是否有 `# fallback default` 注释包含路径字符串 → 检查代码确认：只有 `default=str(Path(...))` 会出现完整路径，注释中无完整路径 ✅ 已修正
- **Issue R2-4**: Task 2.1 测试要求未指定如何验证 warning 被添加 → 已改为代码级验证（grep 确认 `warnings.warn` 在 4 处存在会在 code review 中覆盖） ✅ 已修正
- **Issue R2-5**: Task 5.2/5.3/5.4 的"行数减少"验收标准需明确测量方法 → 已明确以 `wc -l` 和函数体起止行号差计算 ✅ 已修正

### R3 Issues
- **Issue R3-1**: Phase 5 refactoring 期间如果 Task 5.2 引入 bug，Task 5.3/5.4 会在损坏的基础上继续 → 已在每个 Task 的测试要求中强制回归测试，且 Phase 内 Task 顺序执行，5.2 回归失败会阻断后续 ✅ 已修正
- **Issue R3-2**: Task 4.1 添加 mypy 到 CI，但 mypy 可能报大量 error 导致 CI 全 fail → 已在潜在风险中添加降级方案：改为 `mypy pipeline/ || true` ✅ 已修正
- **Issue R3-3**: Task 3.2 + 3.3 修改 3 个 Rime 脚本的 config 加载，如果 config 文件格式不符预期（如 `[rime]` section 不存在），可能 crash → 已在 Task 3.3 潜在风险中强调 fallback 模式，参考现有 `rime_import_safe.py` 的 `try/except` config 加载 ✅ 已修正
