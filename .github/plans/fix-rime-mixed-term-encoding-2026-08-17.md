<!--
  Plan: fix-rime-mixed-term-encoding-2026-08-17
  PM Task: #2825 (DE-AI-FIER) 修复 Rime IME 词库混排词短码污染
  Scope Mode: HOLD（bug 修复，严格保持范围）
  generated_at: 2026-08-17
  git_commit: 7a51228（生成时 HEAD；工作区存在与本计划无关的 M README.md，勿提交）
  revision: 1
-->

# 修复 Rime IME 词库混排词短码污染（"dao"→"ITER到DEMO"）

## 背景与目标

- **问题描述**：Rime 输入法打 `dao` 弹出 `ITER到DEMO` 且压过常用字"到"。根因（Repo Reviewer 已定位，证据链已复核，直接采信）：
  1. `pipeline/rime_export.py`（L106-124）读 `artifacts/domain_terms.txt` 并构造子进程调用外部脚本 `~/.local/bin/rime_import_wordlist.py`，生成 `artifacts/.rime_import_rime_ice.txt`，再同步到 `~/.config/fcitx/rime/custom_phrase.txt`（当前 L345 即 `ITER到DEMO	dao	10000`，已实测确认）。
  2. 外部脚本 L43 `lazy_pinyin(term, style=Style.NORMAL, errors="ignore")` 丢弃混排词 ASCII 部分：`'ITER到DEMO'` → `['dao']`。
  3. 同脚本 L208 对所有含 CJK 词统一 weight=10000（最高档），短码 `dao` 与"到/道/刀"竞争胜出。
  4. **实测影响面（本计划生成时复测）**：`artifacts/.rime_import_rime_ice.txt` 共 2188 行，其中**顺序无关**混排词 74 条（用户 ASCII-first 正则计 72 条，另漏 `扩展MHD`、`约化MHD` 两条 CJK-first 混排）；`custom_phrase.txt` 共 2499 行（含 3 行头），混排 75 条（含一条历史残留 `Go程	gocheng`，不在当前 payload 中）。
- **目标**：混排词（同时含 ASCII 字母与 CJK 汉字的词条）整体排除出 IME 词库，三层落点——仓库侧过滤（主修复）、外部脚本侧防御、部署侧清理验证。
- **非目标（不做什么）**：
  - ❌ 不动 `terms/registry/concepts.tsv` 的 iter-to-demo 概念条目（registry 保留翻译对照概念，仅 IME 导出层排除）
  - ❌ 不动其余混排词在 registry 中的定义
  - ❌ 不改 `~/.config/opencode/` 下任何 agent 配置
  - ❌ 不讨论/不实施降权方案（用户已拍板"整体排除"，本计划将之作为硬约束）
  - ❌ 不改 `artifacts/domain_terms.txt` 的生成逻辑（`build_terms.py` 不动；过滤只发生在 IME 导出链路）
  - ❌ 不修 `pipeline/generate_dict_yaml.py`（第三个 importer 调用点，属 Option B 字典路线，见"遗留风险"）

## 技术方案

- **方案概述**：在 `pipeline/rime_export.py`（及同缺陷的仓库内第二调用点 `pipeline/rime_import_safe.py`）读入词表后、构造 importer 子进程 cmd 之前，用顺序无关判定过滤混排词；过滤后内容写入同目录临时文件并改传临时路径给 importer（对 importer 契约零侵入）。外部脚本在 `_contains_cjk` 判定后增加"同时含 ASCII 字母则跳过"作为防御层。部署侧删除 custom_phrase.txt 全部混排行、重新生成 payload、重建并人工验证。
- **过滤判据（顺序无关，实现以意图为准）**：
  ```python
  bool(re.search(r"[A-Za-z]", term)) and bool(re.search(r"[\u4e00-\u9fff]", term))
  ```
  用户给出的 `^.*[A-Za-z]+.*[\u4e00-\u9fff].*$` 为 ASCII-first 近似，实测漏掉 `扩展MHD`、`约化MHD`（CJK-first）。实现必须用上式；验收同时跑用户原命令与补充 lookahead 命令（见 Post-Execution Verification V1/V2）。
- **注入点**：`pipeline/rime_export.py` 读 input 校验存在之后、构造 `cmd` 之前（即 L115 `output_path.parent.mkdir(...)` 与 L117 `cmd = [...]` 之间）。过滤只移除混排词；纯 ASCII 词条保留与否仍由 importer 的 `--include-non-cjk` 语义决定（本过滤器不改变该行为）。
- **关键设计决策**：
  1. **临时文件过滤而非新增 flag 透传**：仓库修复不依赖外部脚本先改（Phase 1 测试先行要求仓库测试可独立验证过滤）；临时文件放在 output 同目录（同文件系统）、try/finally + 定点 unlink 清理。
  2. **顺序无关判定**：覆盖 CJK-first 混排（`扩展MHD`/`全f方法`/`第N台堆`/`线性IFMIF原型加速器`/`超临界CO2循环`/`硬X射线` 等实测存在）。
  3. **共享 helper 放在 `pipeline/rime_export.py`（公开名）**，`rime_import_safe.py` 直接 import 复用，避免两处漂移。
  4. **空结果防护**：过滤后无剩余词条时写空 payload 并正常退出（不依赖 importer 的 exit 1 语义）。
- **影响范围**：`pipeline/rime_export.py`（+helpers 与接线）、`pipeline/rime_import_safe.py`（复用过滤）、`tests/test_rime_export.py`（+4 测试）、`~/.local/bin/rime_import_wordlist.py`（外部，防御层）、`~/.config/fcitx/rime/custom_phrase.txt`（外部，人工清理）、`docs/dev/acceptance/ime-2026-08-17.md`（验收记录，人工）。

## Error & Rescue Map

| 路径/操作 | 可能失败 | 已处理 | 处理方式 |
|---|---|---|---|
| 临时文件未清理 | 残留 `.filtered_domain_terms.*.txt` | Y | try/finally unlink + `missing_ok=True`；staging 在 payload 同目录 |
| 过滤后词表为空 | importer exit 1 → pipeline 报错 | Y | `kept == 0` 时写空 payload、打印说明、return 0 |
| importer 抛 TimeoutExpired | temp 泄漏 | Y | finally 清理，异常照常传播 |
| CJK-first 混排漏网 | 用户单 regex 不覆盖 | Y | 顺序无关实现 + 补充验收 grep + 测试锁定 `扩展MHD` |
| `rime_import_safe.py` 走老路径再污染 | 第二调用点未修 | Y | T2.2 同源复用过滤；其 stub 测试不读 input，不受影响 |
| 外部脚本被 `generate_dict_yaml.py` 复用 | dict.yaml 也排除混排 | Y（副作用，可接受） | 与"混排词整体排除出 IME"设计一致，见遗留风险 |
| custom_phrase.txt 同步器未知（仓库无写入器） | Phase 4 重新同步卡住 | 部分 | 主修复靠确定性删除命令；重新同步按用户既有 runbook，见 T4.3 |
| 工作区已有 `M README.md` | 误提交无关变更 | Y | 每 task 提交范围写死，见各 task 回滚/提交节 |

## 执行计划

### Phase 1: 测试先行（红）

#### Task 1.1: 扩展 tests/test_rime_export.py — 混排过滤回归测试
- **目标**：先写会失败的测试（红），锁定混排过滤契约（含 CJK-first 混排），为 T2.1 提供验收。
- **依赖**：无
- **frontier**：是
- **执行者**：Task Executor
- **修改内容**：
  - 文件 `tests/test_rime_export.py`：
    1. 顶部新增 `import re`、`import pytest`，并在既有 import 之后新增 `from pipeline.rime_export import filter_mixed_terms, is_mixed_ascii_cjk`（该行在 T2.1 落地前会导致**收集期 ImportError —— 这是预期的红信号**）。
    2. 在 `_write_dummy_importer`（L8-29）之后新增透传 stub 生成器：
       ```python
       MIXED_ROW_RE = re.compile(r"(?=[^\t]*[A-Za-z])(?=[^\t]*[\u4e00-\u9fff])")


       def _write_passthrough_importer(path: Path, log_path: Path) -> None:
           code = f"""#!/usr/bin/env python3
       import argparse
       import json
       from pathlib import Path

       parser = argparse.ArgumentParser()
       parser.add_argument('--input', required=True)
       parser.add_argument('--output', required=True)
       parser.add_argument('--dict-name', default=None)
       parser.add_argument('--rime-user-dir', default=None)
       parser.add_argument('--include-non-cjk', action='store_true')
       parser.add_argument('--no-restart-fcitx', action='store_true')
       parser.add_argument('--import', dest='do_import', action='store_true')
       args = parser.parse_args()

       src = Path(args.input)
       dst = Path(args.output)
       dst.parent.mkdir(parents=True, exist_ok=True)
       dst.write_text(src.read_text(encoding='utf-8'), encoding='utf-8')
       Path({str(log_path)!r}).write_text(json.dumps(vars(args), ensure_ascii=False), encoding='utf-8')
       """
           path.write_text(code, encoding="utf-8")
           path.chmod(0o755)
       ```
    3. 文件末尾追加 3 个测试：
       ```python
       def test_rime_export_filters_mixed_ascii_cjk_terms(tmp_path: Path) -> None:
           repo_root = Path(__file__).resolve().parents[1]

           wordlist = tmp_path / "domain_terms.txt"
           wordlist.write_text(
               "\n".join(
                   [
                       "# 注释行",
                       "托卡马克",
                       "ITER",
                       "ITER到DEMO",
                       "L模",
                       "D-T反应",
                       "扩展MHD",
                       "全f方法",
                       "β输运",
                       "",
                   ]
               )
               + "\n",
               encoding="utf-8",
           )

           importer = tmp_path / "passthrough_importer.py"
           importer_log = tmp_path / "importer_log.json"
           _write_passthrough_importer(importer, importer_log)

           output = tmp_path / ".rime_import.txt"

           p = subprocess.run(
               [
                   sys.executable,
                   "-m",
                   "pipeline.rime_export",
                   "--input",
                   str(wordlist),
                   "--output",
                   str(output),
                   "--rime-script",
                   str(importer),
                   "--include-non-cjk",
               ],
               cwd=str(repo_root),
               text=True,
               capture_output=True,
           )

           assert p.returncode == 0, f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"
           rows = output.read_text("utf-8").splitlines()
           assert not any(MIXED_ROW_RE.search(row) for row in rows)
           assert "托卡马克" in rows
           assert "ITER" in rows
           assert "β输运" in rows


       @pytest.mark.parametrize(
           ("term", "expected"),
           [
               ("托卡马克", False),
               ("ITER", False),
               ("ITER到DEMO", True),
               ("L模", True),
               ("D-T反应", True),
               ("扩展MHD", True),
               ("全f方法", True),
               ("β输运", False),
           ],
       )
       def test_is_mixed_ascii_cjk(term: str, expected: bool) -> None:
           assert is_mixed_ascii_cjk(term) is expected


       def test_filter_mixed_terms_preserves_order_and_counts() -> None:
           terms = ["托卡马克", "ITER到DEMO", "ITER", "扩展MHD"]
           kept, dropped = filter_mixed_terms(terms)
           assert kept == ["托卡马克", "ITER"]
           assert dropped == 2
       ```
  - ⛔ 修改边界：不得改本文件 3 个既有测试（`test_rime_export_writes_output` / `test_rime_export_respects_config_dict_name` / `test_rime_export_cli_overrides_config`）；不得新建其他测试文件。
- **质量检查方式**：`ruff check tests/test_rime_export.py && ruff format --check tests/test_rime_export.py`
- **验收标准**：
  - ✅ `pytest tests/test_rime_export.py -q` 失败，失败原因 = `ImportError: cannot import name 'is_mixed_ascii_cjk'`（红信号，收集期失败亦可接受）
  - ✅ 文件通过 ruff check/format
- **潜在风险**：pytest 收集期失败会连带本文件 3 个既有测试无法运行——属预期，T2.1 后全绿。
- **回滚方式**：`git checkout -- tests/test_rime_export.py`
- **提交**（T2.1 之后与本 task 一并提交）：`git add tests/test_rime_export.py`，commit message `[Plan: fix-rime-mixed-term-encoding-2026-08-17] Task 1.1+2.1: rime_export 混排词过滤 + 回归测试`。⛔ 不得提交 `README.md`。

### Phase 2: 仓库侧过滤（绿）

#### Task 2.1: pipeline/rime_export.py 注入混排过滤（helpers + main 接线）
- **目标**：仓库侧主修复——读 input 后、构造 cmd 前过滤混排词，使 T1.1 转绿。
- **依赖**：T1.1
- **frontier**：是
- **执行者**：Task Executor
- **修改内容**：
  - 文件 `pipeline/rime_export.py`：
    1. 顶部 import 区（L3-6）改为：
       ```python
       import argparse
       import os
       import re
       import subprocess
       import sys
       import tempfile
       from pathlib import Path
       ```
    2. 在 `_load_config` 函数定义（L14-18）之后、`main()` 之前，新增 4 个模块级函数（公开名，供 rime_import_safe 复用）：
       ```python
       def is_mixed_ascii_cjk(term: str) -> bool:
           """True when *term* contains both ASCII letters and CJK ideographs.

           Mixed terms (e.g. ``ITER到DEMO``, ``扩展MHD``, ``D-T反应``) are excluded
           from the IME payload: the importer's pinyin conversion drops the ASCII
           part, producing lossy short codes (``ITER到DEMO`` -> ``dao``) that
           outrank common characters in the candidate list.
           """

           return bool(re.search(r"[A-Za-z]", term)) and bool(
               re.search(r"[\u4e00-\u9fff]", term)
           )


       def filter_mixed_terms(terms: list[str]) -> tuple[list[str], int]:
           """Return ``(kept_terms, dropped_count)`` with original order preserved."""

           kept = [t for t in terms if not is_mixed_ascii_cjk(t)]
           return kept, len(terms) - len(kept)


       def read_wordlist_lines(path: Path) -> list[str]:
           """Read a one-term-per-line wordlist; skip blanks and ``#`` comments."""

           terms: list[str] = []
           for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
               s = raw.strip()
               if not s or s.startswith("#"):
                   continue
               terms.append(s)
           return terms


       def prepare_importer_input(
           input_path: Path, staging_dir: Path
       ) -> tuple[Path, int, int]:
           """Filter mixed terms; return ``(importer_input_path, kept_count, dropped_count)``.

           When nothing is dropped, returns the original *input_path*. Otherwise a
           filtered temporary file is created under *staging_dir* (same filesystem
           as the payload); the caller owns its cleanup.
           """

           all_terms = read_wordlist_lines(input_path)
           kept, dropped = filter_mixed_terms(all_terms)
           if not dropped:
               return input_path, len(kept), 0

           fd, tmp_name = tempfile.mkstemp(
               prefix=".filtered_domain_terms.",
               suffix=".txt",
               dir=str(staging_dir),
           )
           with os.fdopen(fd, "w", encoding="utf-8") as f:
               f.write("\n".join(kept) + ("\n" if kept else ""))
           return Path(tmp_name), len(kept), dropped
       ```
    3. `main()` 中 L115 `output_path.parent.mkdir(parents=True, exist_ok=True)` 与 L117 `cmd = [` 之间，插入：
       ```python
           # Exclude mixed ASCII+CJK terms BEFORE handing the wordlist to the
           # importer (see is_mixed_ascii_cjk for rationale). This keeps the repo
           # safe regardless of the external importer script's behavior.
           importer_input, kept, dropped = prepare_importer_input(
               input_path, output_path.parent
           )
           if dropped:
               print(f"rime_export: excluded {dropped} mixed ASCII+CJK term(s)")
           if kept == 0:
               output_path.write_text("", encoding="utf-8")
               print("rime_export: no terms remain after mixed-term filtering; "
                     "wrote empty payload")
               if importer_input != input_path:
                   importer_input.unlink(missing_ok=True)
               return
       ```
    4. 将 `cmd` 中 `"--input", str(input_path),`（L121）改为 `"--input", str(importer_input),`。
    5. 将 `proc = subprocess.run(...)` 块（L140-146）改为 try/finally 包裹以确保 temp 清理：
       ```python
           try:
               proc = subprocess.run(
                   cmd,
                   check=False,
                   capture_output=True,
                   text=True,
                   timeout=120,
               )
           finally:
               if importer_input != input_path:
                   try:
                       importer_input.unlink()
                   except FileNotFoundError:
                       pass
       ```
       （其后的 `if proc.stdout:` / `if proc.returncode != 0:` 逻辑不变，保持原位。）
- **修改边界**：不得改 argparse 参数定义（L44-102）；不得改 `--include-non-cjk` 的透传逻辑（L125-126）与 `--import` 分支（L127-138）；不得删除 L147-152 的 stdout/stderr 打印与 SystemExit 语义。
- **质量检查方式**：`ruff check pipeline/rime_export.py && ruff format --check pipeline/rime_export.py`
- **验收标准**：
  - ✅ `pytest tests/test_rime_export.py -q` 全绿（4 新 + 3 既有）
  - ✅ `python3 -m pipeline.rime_export --input artifacts/domain_terms.txt --output /tmp/probe_rime_export.txt`（真实外部脚本）退出 0，且 stdout 含 `excluded 74 mixed ASCII+CJK term(s)`
  - ✅ `/tmp/probe_rime_export.txt` 混排行数为 0（用 V1、V2 两条 grep 验证），`rm /tmp/probe_rime_export.txt`
- **潜在风险**：外部脚本在用户机器上存在且可运行（已核实 pypinyin 0.50.0）；若不可用则验收第 2 条跳过，以 stub 测试为准。
- **回滚方式**：`git checkout -- pipeline/rime_export.py`
- **提交**：与 T1.1 合并提交（见 T1.1 提交节）。

#### Task 2.2: pipeline/rime_import_safe.py 复用过滤（仓库内第二调用点）
- **目标**：`docs/dev/03-rime-integration.md` 推荐的安全导入路径同源修复，杜绝部署链走此入口时复发。
- **依赖**：T2.1（复用其公开 helper）
- **frontier**：否（依赖 T2.1）
- **执行者**：Task Executor
- **修改内容**：
  - 文件 `pipeline/rime_import_safe.py`：
    1. 在 `from pathlib import Path`（L12）之后新增 `from pipeline.rime_export import prepare_importer_input`。
    2. `main()` 中，L467 `output_path.parent.mkdir(parents=True, exist_ok=True)` 与 L469 `# Step 1) Always generate payload` 之间插入：
       ```python
           # Exclude mixed ASCII+CJK terms before payload generation (shared
           # logic with rime_export; see pipeline.rime_export.is_mixed_ascii_cjk).
           importer_input, kept, dropped = prepare_importer_input(
               input_path, output_path.parent
           )
           if dropped:
               print(f"rime_import_safe: excluded {dropped} mixed ASCII+CJK term(s)")
           if kept == 0:
               output_path.write_text("", encoding="utf-8")
               print("rime_import_safe: no terms remain after mixed-term filtering; "
                     "wrote empty payload")
               if importer_input != input_path:
                   importer_input.unlink(missing_ok=True)
               return
       ```
       ⚠️ 插入点必须在 L455-456 的 `--rollback` 早退分支**之后**。
    3. 将两处 `_run_importer_v2(... input_path=input_path ...)` 调用的实参改为 `input_path=importer_input`（L471-482 payload 生成处、L526-537 import 处）。
    4. 临时文件清理共 3 个点：
       - L495-502 dry-run 早退分支：`print(f"generated import payload: ...")` 之前加：
         ```python
               if importer_input != input_path:
                   try:
                       importer_input.unlink()
                   except FileNotFoundError:
                       pass
         ```
       - L487-492 payload 生成失败分支：`raise SystemExit(gen.returncode)` 之前加同款清理。
       - L561 `print("import OK")` 之前（import 成功路径）加同款清理；L548-559 import 失败自动回滚分支中 `raise SystemExit(imp.returncode)` 之前加同款清理。
- **修改边界**：不得改 `create_backup` / `rollback_from_manifest`（L114-329）任何逻辑；不得改 `--rollback` 分支；不得改 CLI 参数定义。
- **质量检查方式**：`ruff check pipeline/rime_import_safe.py && ruff format --check pipeline/rime_import_safe.py`
- **验收标准**：
  - ✅ `pytest tests/test_rime_import_safe.py -q` 全绿（11 个既有测试不破坏）
  - ✅ 手工探针：`python3 -m pipeline.rime_import_safe --input artifacts/domain_terms.txt --output /tmp/probe_safe.txt --dry-run` 退出 0，stdout 含 `excluded 74 mixed ASCII+CJK term(s)`，`/tmp/probe_safe.txt` 混排数为 0，`rm /tmp/probe_safe.txt`
- **潜在风险**：双重过滤（repo 层 + 外部脚本层）幂等，无累积问题。
- **回滚方式**：`git checkout -- pipeline/rime_import_safe.py`
- **提交**：`git add pipeline/rime_import_safe.py`，commit message `[Plan: fix-rime-mixed-term-encoding-2026-08-17] Task 2.2: rime_import_safe 复用混排过滤`。⛔ 不得提交 `README.md`。

#### Task 2.3: 全量回归验证
- **目标**：仓库侧修复收口——全量测试 + 静态检查 + determinism 专项。
- **依赖**：T2.1、T2.2
- **frontier**：否
- **执行者**：Task Executor
- **修改内容**：无（纯验证）
- **验收标准**：
  - ✅ `pytest tests/ -q` 退出 0（含 `tests/test_determinism_pipeline.py`——其 e2e fixture 词表无混排词，过滤为 no-op，hash 断言不受影响）
  - ✅ `ruff check .` 退出 0
  - ✅ `ruff format --check .` 退出 0
  - ✅ `mypy pipeline/ --ignore-missing-imports --no-error-summary` 退出 0
  - ✅ `python -m compileall -q pipeline tests` 退出 0
- **潜在风险**：pytest 全量（39 文件）耗时较长，超时阈值 ≥300s。
- **回滚方式**：同 T2.1/T2.2。
- **提交**：无（验证阶段）。

### Phase 3: 外部脚本侧防御性修复

#### Task 3.1: 备份并修改 ~/.local/bin/rime_import_wordlist.py
- **目标**：脚本独立使用（含被 `generate_dict_yaml.py` 复用）时不复发。
- **依赖**：T2.3（仓库全绿后再动外部脚本）
- **frontier**：否
- **执行者**：Task Executor（外部文件，非 git 管理，必须先用 cp 备份）
- **修改内容**：
  - 文件 `~/.local/bin/rime_import_wordlist.py`（仓库外，235 行）：
    1. 备份：`cp -a ~/.local/bin/rime_import_wordlist.py ~/.local/bin/rime_import_wordlist.py.bak-20260817`
    2. 锚点 A：L29-31 `_contains_cjk` 定义之后，新增：
       ```python
       def _contains_ascii_letter(s: str) -> bool:
           return bool(re.search(r"[A-Za-z]", s))
       ```
    3. 锚点 B：L204 `if _contains_cjk(term):` 与 L205 `code = _to_pinyin_no_tone(term)` 之间插入：
       ```python
           if _contains_cjk(term):
               if _contains_ascii_letter(term):
                   # Mixed ASCII+CJK terms: pinyin conversion drops the ASCII part
                   # (lossy codes like "ITER到DEMO" -> "dao"). Excluded by design.
                   continue
               code = _to_pinyin_no_tone(term)
       ```
       （L205-208 原逻辑保留，此时仅作用于纯 CJK 词。）
- **修改边界**：不得改 `--weight` / `--weight-non-cjk` 默认值与语义；不得改 `--include-non-cjk` 分支（L209-211）；不得改 `_to_pinyin_no_tone` 的 `errors="ignore"` 参数。
- **质量检查方式**：`python3 -m py_compile ~/.local/bin/rime_import_wordlist.py`
- **验收标准**：
  - ✅ 备份文件存在：`ls -la ~/.local/bin/rime_import_wordlist.py.bak-20260817`
  - ✅ py_compile 无输出（语法通过）
- **潜在风险**：脚本为多消费者共享（本仓库 + dict.yaml 生成器），混排全局排除与该设计决策一致（已确认）。
- **回滚方式**：`cp -a ~/.local/bin/rime_import_wordlist.py.bak-20260817 ~/.local/bin/rime_import_wordlist.py`

#### Task 3.2: 脚本直调验证（与仓库测试解耦）
- **目标**：用临时词表直接验证脚本过滤行为（仓库测试不覆盖外部脚本）。
- **依赖**：T3.1
- **frontier**：否
- **执行者**：Task Executor
- **修改内容**：无（纯验证，命令如下）：
  ```bash
  printf '托卡马克\nITER\nITER到DEMO\nL模\nD-T反应\n扩展MHD\nβ输运\n' > /tmp/rime_mixed_probe_in.txt
  python3 ~/.local/bin/rime_import_wordlist.py --input /tmp/rime_mixed_probe_in.txt --output /tmp/rime_mixed_probe_out.txt --include-non-cjk
  ```
- **验收标准**：
  - ✅ 上条命令退出 0
  - ✅ `grep -cP '^(?=[^\t]*[A-Za-z])(?=[^\t]*[\x{4e00}-\x{9fff}])[^\t]*\t' /tmp/rime_mixed_probe_out.txt` 输出 `0`
  - ✅ `grep -c '^托卡马克\t' /tmp/rime_mixed_probe_out.txt` 输出 `1`；`grep -c '^ITER\t' /tmp/rime_mixed_probe_out.txt` 输出 `1`
  - ✅ 清理：`rm /tmp/rime_mixed_probe_in.txt /tmp/rime_mixed_probe_out.txt`
- **潜在风险**：无。
- **回滚方式**：同 T3.1。
- **提交**：无（外部文件不入 git）。

### Phase 4: 部署侧清理与验证（人工执行为主）

> 本阶段命令由 **人工（用户）** 执行；Task Executor 负责输出命令清单与验收记录模板。原因：操作目标在仓库外（`~/.config/fcitx/rime/`），且仓库内无 custom_phrase.txt 写入器，同步方式为用户本地 runbook。

#### Task 4.1: 备份并清理 custom_phrase.txt 混排条目
- **依赖**：T3.2
- **frontier**：是（与 T4.2 可并行，文件不冲突）
- **执行者**：人工
- **修改内容**（命令，逐条执行）：
  ```bash
  cp -a ~/.config/fcitx/rime/custom_phrase.txt ~/.config/fcitx/rime/custom_phrase.txt.bak-20260817
  grep -vP '^(?=[^\t]*[A-Za-z])(?=[^\t]*[\x{4e00}-\x{9fff}])[^\t]*\t' ~/.config/fcitx/rime/custom_phrase.txt > /tmp/custom_phrase.clean.txt
  mv /tmp/custom_phrase.clean.txt ~/.config/fcitx/rime/custom_phrase.txt
  ```
  （3 行头不含 CJK，天然保留；预期删除 75 条，含历史残留 `Go程	gocheng` 与第 345 行 `ITER到DEMO	dao	10000`。）
- **验收标准**：
  - ✅ `grep -cP '^(?=[^\t]*[A-Za-z])(?=[^\t]*[\x{4e00}-\x{9fff}])[^\t]*\t' ~/.config/fcitx/rime/custom_phrase.txt` 输出 `0`
  - ✅ 文件首 3 行仍为 `# Rime table` / `# coding: utf-8` / `#@/db_name	custom_phrase.txt`
- **回滚方式**：`cp -a ~/.config/fcitx/rime/custom_phrase.txt.bak-20260817 ~/.config/fcitx/rime/custom_phrase.txt`

#### Task 4.2: 重跑 pipeline 重新生成 payload 并验收
- **依赖**：T2.3、T3.2
- **frontier**：是
- **执行者**：人工（仓库内命令，也可由 Task Executor 执行）
- **修改内容**（命令，在仓库根 `/home/gw/opt/fusion-terms` 执行）：
  ```bash
  python3 -m pipeline.rime_export
  grep -cP '^[^\t]*[A-Za-z]+[^\t]*[\x{4e00}-\x{9fff}][^\t]*\t' artifacts/.rime_import_rime_ice.txt
  grep -cP '^(?=[^\t]*[A-Za-z])(?=[^\t]*[\x{4e00}-\x{9fff}])[^\t]*\t' artifacts/.rime_import_rime_ice.txt
  ```
- **验收标准**：
  - ✅ 第一条 grep（用户原验收命令）输出 `0`
  - ✅ 第二条 grep（补充，覆盖 CJK-first）输出 `0`
  - ✅ stdout 含 `excluded 74 mixed ASCII+CJK term(s)`
- **回滚方式**：payload 为生成物（gitignored），回滚 = `git checkout -- pipeline/`（仓库代码）+ 恢复 T4.1 备份文件。

#### Task 4.3: 重新同步 + 重建 + 人工打字验证
- **依赖**：T4.1、T4.2
- **frontier**：否
- **执行者**：人工
- **修改内容**：
  1. 按你的既有同步 runbook 把修复后的 payload 同步进 Rime（仓库内唯一同步器 `pipeline/sync_to_fcitx.py` 只写 `wordlists/domain_terms.txt`，不写 custom_phrase.txt；若你的同步方式为"合并 payload 新增行进 custom_phrase.txt"，重新执行该合并即可，修复后 payload 已无混排行，不会引入新污染）。
  2. 重建词库：`rime_deployer --build ~/.config/fcitx/rime`
  3. 重启输入法（`fcitx-remote -r` 或注销重登）。
  4. 打字验证：输入 `dao`（候选应为首位"到"，且不再出现 ITER到DEMO）、`mo`（不再出现 L模/I模/H模）、`qiu`（不再出现 DXTRAN球）。
  5. 写入验收记录 `docs/dev/acceptance/ime-2026-08-17.md`（模板参照 `artifacts/ime_acceptance_report.md`，注明：环境、同步方式命令、dao/mo/qiu 三项结果、附件 grep 输出）。
- **验收标准**：
  - ✅ `docs/dev/acceptance/ime-2026-08-17.md` 存在且含 dao/mo/qiu 三项人工结果
  - ✅ custom_phrase.txt 混排计数为 0（复跑 T4.1 验收命令）
  - ✅ 人工打字 dao/mo/qiu 候选正常
- **回滚方式**：恢复 T4.1 备份 → `rime_deployer --build ~/.config/fcitx/rime` → `fcitx-remote -r`。
- **提交**（可选，由人工确认后）：`git add docs/dev/acceptance/ime-2026-08-17.md`。

## Execution Wave（并行执行波次）

| Wave | 可并行 Task | Frontier | 依赖已完成 |
|------|------------|----------|------------|
| W1 | T1.1 | T1.1 | — |
| W2 | T2.1 | T2.1 | W1 |
| W3 | T2.2 | T2.2 | W2 |
| W4 | T2.3 | T2.3 | W3 |
| W5 | T3.1 | T3.1 | W4 |
| W6 | T3.2 | T3.2 | W5 |
| W7 | T4.1、T4.2 | T4.1、T4.2 | W6 |
| W8 | T4.3 | T4.3 | W7 |

## Post-Execution Verification

### Automated Verification（Task Executor 自动执行）

| ID | Description | Command | Expected |
|----|-------------|---------|----------|
| V1 | 用户原验收 grep（ASCII-first） | `grep -cP '^[^\t]*[A-Za-z]+[^\t]*[\x{4e00}-\x{9fff}][^\t]*\t' artifacts/.rime_import_rime_ice.txt` | `0` |
| V2 | 补充验收 grep（顺序无关，覆盖 CJK-first） | `grep -cP '^(?=[^\t]*[A-Za-z])(?=[^\t]*[\x{4e00}-\x{9fff}])[^\t]*\t' artifacts/.rime_import_rime_ice.txt` | `0` |
| V3 | 全量测试 | `pytest tests/ -q` | exit 0 |
| V4 | 静态检查 | `ruff check . && ruff format --check . && mypy pipeline/ --ignore-missing-imports --no-error-summary` | exit 0 |

### Deferred (needs restart / deployment)
- [ ] D1: `rime_deployer --build ~/.config/fcitx/rime` 后重启 fcitx（`fcitx-remote -r`），随后才能验证打字

### Probe (best-effort, run if available)
- [ ] P1: `ls ~/.config/fcitx/rime/custom_phrase.txt.bak-20260817 ~/.local/bin/rime_import_wordlist.py.bak-20260817` 两者存在
- [ ] P2: `grep -cP '^(?=[^\t]*[A-Za-z])(?=[^\t]*[\x{4e00}-\x{9fff}])[^\t]*\t' ~/.config/fcitx/rime/custom_phrase.txt` 输出 `0`

### Manual（真正需要人工判断）
- [ ] M1: 打 `dao` → 候选首位"到"，无 ITER到DEMO
- [ ] M2: 打 `mo` → 无 L模/I模/H模；打 `qiu` → 无 DXTRAN球
- [ ] M3: 阅读 `docs/dev/acceptance/ime-2026-08-17.md` 验收记录，确认三项结果均已勾选

## Task Executor 按序执行清单

1. `T1.1` → 完成信号：`pytest tests/test_rime_export.py` 报 ImportError（红）且 ruff 通过
2. `T2.1` → 完成信号：`pytest tests/test_rime_export.py` 全绿 + 真实探针 stdout 含 `excluded 74`；commit `Task 1.1+2.1`
3. `T2.2` → 完成信号：`pytest tests/test_rime_import_safe.py` 全绿 + 探针 `excluded 74`；commit `Task 2.2`
4. `T2.3` → 完成信号：V3、V4 全绿（本阶段无 commit）
5. `T3.1` → 完成信号：备份文件存在 + py_compile 通过
6. `T3.2` → 完成信号：探针输出混排计数 `0`、`托卡马克`/`ITER` 各 `1`，临时文件已清理
7. `T4.1`（人工）→ 完成信号：custom_phrase 混排计数 `0` 且 3 行头保留
8. `T4.2`（人工）→ 完成信号：V1、V2 均输出 `0`
9. `T4.3`（人工）→ 完成信号：验收文档存在 + M1/M2 通过 + PM 任务 #2825 可标记完成

## 遗留风险 / 后续跟进（不在本计划范围）

- `pipeline/generate_dict_yaml.py`（第三个 importer 调用点，Option B 字典路线）：Phase 3 后外部脚本自身已排除混排，故其生成物同步受益；但其 `_run_importer` 未复用 `prepare_importer_input`，若未来 importer 回退需再评估。建议独立小任务跟进。
- `~/.config/fcitx/rime/wordlists/domain_terms.txt`（`sync_to_fcitx.py` 目标）仍含 74 条混排原文（无 pinyin 编码，不产生短码污染）；若该 wordlist 被 schema 直接 import_tables 引用则需另行评估，本计划不处理。
- 用户原验收 grep（V1）不覆盖 CJK-first 混排，长期应以 V2 为准；建议后续把 V2 固化进 `tests/test_registry_ime_compat.py` 或 CI。

## 审查日志

| 轮次 | 聚焦 | 发现问题数 | 已修正 | 剩余 |
|------|------|-----------|--------|------|
| R1 | 结构完整性（4 阶段 9 任务、锚点/验收/回滚齐全） | 0 | 0 | 0 |
| R1.5 | 外部引用事实核查（行号、工具、grep 命令实测、PM #2825 核对） | 2 | 2 | 0 |
| R2 | 可执行性（命令干跑：混排计数 72/74/75 实测；pypinyin/rime_deployer 存在性） | 1 | 1 | 0 |
| R2.8 | LLM 可执行性（逐字段消歧：锚点行号+符号名双写、代码块完整、提交范围写死） | 0 | 0 | 0 |
| R3 | 风险与边缘（temp 清理、CJK-first 覆盖、同步器未知、README.md 未提交、determinism 不破坏） | 0 | 0 | 0 |
| **终止** | **T5 — 全部审查轮次问题清零** | | | **0** |

R1.5 修正记录：
- ①用户 ASCII-first regex 实测漏 2 条 CJK-first 混排（`扩展MHD`/`约化MHD`）→ 实现改为顺序无关判定，验收增补 V2。
- ②custom_phrase.txt 混排实测 75 条（含历史残留 `Go程`），非 73 → T4.1 预期删除数修正。
R2 修正记录：
- ①同步器 gap：仓库内无 custom_phrase.txt 写入器 → Phase 4 改为主修复=确定性删除命令，重新同步按用户既有 runbook，并在 T4.3 明确标注。

## 假设清单

1. `[假设: domain_terms.txt 一行一词、词条内无内嵌 tab]` — 已核实（3404 行、grep 正常）。低影响。
2. `[假设: 混排判定只需半角 `[A-Za-z]`，无需全角字母]` — 词表未见全角混排。低影响。
3. `[假设: 外部脚本为用户所有、非 git 管理]` — 已核实（无仓库副本）；Phase 3 内置 cp 备份。
4. `[假设: custom_phrase.txt 的同步方式为用户本地 runbook]` — 仓库 grep 无写入器；高影响若错（T4.3 会卡），已通过"删除命令不依赖同步器 + T4.3 按既有 runbook"缓解。
5. `[假设: 部署重跑入口为 `python3 -m pipeline.rime_export`（默认 input/output）]` — 与用户背景链路一致，已实测可运行。

## Execution Log

### Post-Execution Verification Log（2026-08-18，Task Executor，Phase 1-3 执行后）

| ID | Command | Result |
|----|---------|--------|
| V1 | `grep -cP '^[^\t]*[A-Za-z]+[^\t]*[\x{4e00}-\x{9fff}][^\t]*\t' artifacts/.rime_import_rime_ice.txt` | ⏸ PENDING T4.2（当前 payload 为 2026-04-22 旧产物，值 72；重新生成前无法为 0。过滤正确性已由 T2.1/T2.2 探针证明：/tmp/probe_rime_export.txt 与 /tmp/probe_safe.txt 均 V1=0） |
| V2 | `grep -cP '^(?=[^\t]*[A-Za-z])(?=[^\t]*[\x{4e00}-\x{9fff}])[^\t]*\t' artifacts/.rime_import_rime_ice.txt` | ⏸ PENDING T4.2（当前值 74，与计划背景"混排 74 条"一致；探针均已 V2=0） |
| V3 | `pytest tests/ -q` | ✅ PASS exit=0（159 全绿） |
| V4 | `ruff check . && ruff format --check . && mypy pipeline/ --ignore-missing-imports --no-error-summary` | ✅ PASS exit=0 |

Probe（best-effort）：
- P1: `ls ~/.config/fcitx/rime/custom_phrase.txt.bak-20260817 ~/.local/bin/rime_import_wordlist.py.bak-20260817` → 部分通过：`~/.local/bin/rime_import_wordlist.py.bak-20260817` 存在（T3.1 完成）；`custom_phrase.txt.bak-20260817` 不存在（T4.1 人工步骤未执行）。
- P2: `grep -cP ... ~/.config/fcitx/rime/custom_phrase.txt` → 当前值 **75**，与计划背景"custom_phrase.txt 混排 75 条（含历史残留 Go程）"完全一致；清理依赖 T4.1（人工）。

Deferred / Manual：
- D1: ⏸ PENDING RESTART（Phase 4 人工）
- M1/M2/M3: ⚠️ PENDING MANUAL（Phase 4 人工）

### 执行记录（Task Executor，2026-08-18）

- T1.1 ✅ 红信号达成（pytest 收集期 ImportError: cannot import name 'filter_mixed_terms'——计划预期报 is_mixed_ascii_cjk，二者同属该 import 行，性质相同）；ruff check/format 通过。与 T2.1 合并提交 bde53e8。
- T2.1 ✅ 4 新测试 + 3 既有全绿；真实探针 exit 0、stdout `excluded 74 mixed ASCII+CJK term(s)`（与计划预期 74 一致）；探针输出 V1=0/V2=0；temp 无残留。提交 bde53e8。
- T2.2 ✅ 11 既有测试全绿；探针 exit 0、`excluded 74`、V1=0/V2=0、temp 无残留。提交 0bb6657。
- T2.3 ✅ pytest 全量/ruff/mypy/compileall 全绿。无提交。
- T3.1 ✅ 备份 `~/.local/bin/rime_import_wordlist.py.bak-20260817` 与原文件 diff 一致；py_compile 通过。外部文件不入 git。
- T3.2 ✅ 脚本直调 exit 0；输出仅 3 行（托卡马克/ITER/β输运），混排 4 条全排除；混排计数（-P）0。
- 偏差记录 ①：计划 T3.2 验收命令 `grep -c '^托卡马克\t'` 在 GNU grep BRE 模式下 `\t` 按字面 `t` 解释，实测输出 0（计划预期 1）；改用 PCRE（-P）或字面 tab 后计数为 1，过滤行为正确。**建议**：后续将该验收命令改为 `grep -cP` 或 `$'^托卡马克\t'`。
- 偏差记录 ②：T2.2 计划"临时文件清理共 3 个点"实际列了 4 处位置（dry-run 早退、payload 失败、import 成功、import 失败回滚），均按计划字面实现。计划未点名的两个 SystemExit 路径（payload 生成 TimeoutExpired、--import 无 --backup-path 早退）未加清理——若未来需彻底无残留，建议后续小任务补齐。已按"不擅自改计划"原则原样实现并在此记录。
- 偏差记录 ③：README.md 全程未纳入任何提交（工作区仍为 M 状态，属开源准备变更集）。
- 未执行 Phase 4（T4.1-T4.3）——按用户指令属人工部署侧步骤。
