# T4.1 全量终验记录（PM T-4973）

- 执行时间：2026-10-29（`date -Iseconds` = 2026-10-29T21:22:50+08:00）
- 执行者：dev-orchestrator
- 基线 HEAD：`36ab84f`（W3a allowlist 验收裁决 commit）；工作区除既有未跟踪 `iaea_fusion.html` 外干净
- 数据状态：concepts 3076 / aliases 10249 / evidence 3203 / definitions 6152；`artifacts/domain_terms.txt` 6378
- **结论：T4.1 全部 7 项门禁 PASS（exit 0）**；`git diff` 无数据改动（仅新增本记录文件）

## 门禁逐条实测

| # | 命令 | exit | 关键输出 |
|---|---|---:|---|
| V1 | `.venv/bin/python scripts/registry_row_audit.py --audit --expect-clean-all` | **0** | clean（`w0_is_clean:true`，各 by-design 指标 0） |
| V2 | `.venv/bin/python -m pytest -q` | **0** | 175 tests（`--collect-only` 合计 175） |
| V3 | `.venv/bin/mypy pipeline/ --ignore-missing-imports` | **0** | `Success: no issues found in 16 source files` |
| V4 | `.venv/bin/ruff format --check .` | **0** | `150 files already formatted` |
| V5 | `.venv/bin/ruff check .` | **0** | `All checks passed!` |
| V6 | `.venv/bin/python -m pipeline.validate_registry` | **0** | `registry OK: 3076 concepts, 10249 aliases, 3203 evidence rows, 6152 definitions` |
| V7 | `.venv/bin/python scripts/registry_coverage_report.py` | **0** | `covered 3032 / uncovered 44 / coverage_pct 98.57`（阈值 ≥ 78.0） |

## 覆盖率终值

| 口径 | 值 |
|---|---|
| `coverage_pct`（主口径：是否进入 `domain_terms.txt`） | **98.57**（阈值 78.0 ✅；计划理论值 ≈98.9） |
| `allowlist_only_coverage_pct` | **97.79** |
| `coverage_pct_incl_allowlist` | **98.80** |
| `covered / uncovered` | **3032 / 44**（3032 + 44 = 3076 ✅） |
| 未覆盖构成 | **9**（W2 桶：`system`/`calculation`/`material`/`simulation`/`mode`/`device`/`area`/`control`/`diffusion`，zh 名在 `denylist.txt`）+ **35**（`proper_excluded`，按 H2 永不入词表） |
| `terms_file_entries` | **6378** |

## 与计划预期的偏差

| 项 | 计划 | 实测 | 处置 |
|---|---|---|---|
| `coverage_pct` | ≥78.0（理论 ≈98.9） | **98.57** | PASS；差 0.33 个百分点来自 3 个 denylist 阻塞 + 9 个 W2 残余中的部分重算口径，已逐项解释 |
| `proper_excluded` | 35 | **35** | 一致 |
| `definitions` | 6152 | **6152** | 一致 |

## 已知问题（不阻塞 T4.1）

1. **PM 5072 承接**：747/854 W3a concept 的 zh 释义仍为占位模板；854 条 evidence `quote` 为空、b16–b43 为裸来源。属 W3a 验收 known-issue（用户 2026-10-29 裁决 option A）。
2. `registry_batch_verify.py --self-test` **19/24（exit 1）** — W3a/W3b 均未改 `scripts/`，属先于本轮的既有漂移，已并入 PM 5072 范围。
3. `--mode names --check-urls` 不探测 URL（names 模式判据空转），同上并入 PM 5072。
4. `w3-name-conflicts.tsv` 中 `physical-sputtering` / `物理溅射` 的 zh-alias 冲突为 pre-existing，计划 M3「冲突项人工裁决」仍未勾选。

## 复跑方式

```bash
cd /home/gw/opt/fusion-terms
.venv/bin/python scripts/registry_row_audit.py --audit --expect-clean-all
.venv/bin/python -m pytest -q
.venv/bin/mypy pipeline/ --ignore-missing-imports
.venv/bin/ruff format --check . && .venv/bin/ruff check .
.venv/bin/python -m pipeline.validate_registry
.venv/bin/python scripts/registry_coverage_report.py
```
