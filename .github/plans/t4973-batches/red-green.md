# T4973 — W0 门禁 RED→GREEN 可复跑记录（T0.11）

> 任务：PM **T4973** / 计划 `.github/plans/terminology-coverage-and-definition-quality.md` §T0.9–T0.11
> 录制日期：**2026-10-26**（`date` 实测 `Mon Oct 26 07:02 PM CST 2026`）
> 依赖产物：T0.1 `scripts/registry_row_audit.py`、T0.9 `pipeline/validate_registry.py`、T0.10 用例与 fixture
> 涉及 commit：本记录追加前 `HEAD = 08a2e98`（T0.9+T0.10）；加严前基线 `1e2cf30`；污点引入点 `f90e903`
> 复跑要求：下文每条命令均可由第三方逐字复跑，输出为**实测原文**（非转述）。

---

## 0. 门禁剖面（本任务的前置修正，必须先读）

`--expect-clean` 原先把 **定义质量类** 指标（`definitions.en_boilerplate`、`definitions.concepts_without_defs`）
也纳入 gate。这两项是 **Phase 1（W1）** 的工作量本体（746 行 en 套话改写 + 10 个零释义概念新增），
而计划 §Phase 0 的完成定义只列举结构完整性指标：

> `.venv/bin/python scripts/registry_row_audit.py --audit --expect-clean` → exit 0
> （`malformed=0, shifted=0, sixcol=0, evidence_cols_non5=0, zh_en_corruption=0`）

若沿用原 gate，**Phase 0 在 Phase 0 阶段永远无法 exit 0**，其完成定义不可判定。
故本任务把 gate 拆成两个**显式命名**的剖面（**未削弱任何检查**：全部指标仍由 `--audit` 报告，
且新增了覆盖全集、更严格的 `--expect-clean-all`）：

| 剖面 | 覆盖指标 | 用途 |
|------|----------|------|
| `--expect-clean` | `concepts.malformed_cols`、`concepts.bad_category`、`evidence.non5_cols`、`evidence.glued_source_rows`、`definitions.zh_en_corruption` | **Phase 0 完成定义**（= 计划列举的结构集） |
| `--expect-clean-all` | 上述 5 项 **+** `definitions.en_boilerplate`、`definitions.concepts_without_defs` | Phase 1（W1）完成时的全指标门禁（严格超集） |

JSON 新增字段：`w0_clean_metrics` / `w0_non_zero_metrics` / `w0_is_clean` / `deferred_w1_metrics`；
`clean_metrics` / `non_zero_metrics` / `is_clean` **语义不变**（仍为全集），故无消费者受影响。

---

## 1. RED / GREEN 汇总

| # | 断言 | RED 侧 | GREEN 侧 |
|---|------|--------|----------|
| 1 | 结构门禁能失败 | 修复前三表 → `--expect-clean` **exit 1**（5 项非零） | HEAD → `--expect-clean` **exit 0** |
| 2 | 错位行（真实语料）被拒 | 旧 validator → **exit 0**（静默通过 ← 缺陷） | 新 validator → **exit 1** |
| 3 | 6 列行（真实语料）被拒 | 旧 validator → **exit 0**（静默通过） | 新 validator → **exit 1** |
| 4 | 4 列 evidence 行被拒 | 旧 validator → **exit 0**（静默通过） | 新 validator → **exit 1** |
| 5 | 未变异对照不被误杀 | — | 旧/新 validator → **exit 0** |

---

## 2. 命令与实测输出

### A) 修复前（`f90e903` 三表）— RED，exit 1

```console
$ .venv/bin/python scripts/registry_row_audit.py \
    --concepts /tmp/opencode/pre0b/terms/registry/concepts.tsv \
    --evidence /tmp/opencode/pre0b/terms/registry/evidence.tsv \
    --definitions /tmp/opencode/pre0b/terms/registry/definitions.tsv \
    --expect-clean
exit=1
registry_row_audit: --expect-clean FAILED — 5 non-zero W0 structural metric(s):
  concepts.malformed_cols = 80
  concepts.bad_category = 99
  evidence.non5_cols = 215
  evidence.glued_source_rows = 427
  definitions.zh_en_corruption = 48
  (deferred to W1, not gated here: definitions.en_boilerplate = 746)
```

> 该 5 项与计划 §T0.1 记录的修复前基线**逐项一致**（80 / 99 / 215 / 427 / 48），
> 即 RED 语料确为被修复的真实污染态，而非自造样本。

### B) 修复后（HEAD）— GREEN，exit 0

```console
$ .venv/bin/python scripts/registry_row_audit.py --audit --expect-clean
exit=0
# stdout 为审计 JSON（3057 bytes），stderr 无输出
# 关键字段：w0_is_clean=true；w0_non_zero_metrics={}；
#           deferred_w1_metrics={"definitions.concepts_without_defs":10,
#                                 "definitions.en_boilerplate":746}
#           is_clean=false（全集语义保留，未被改动）
```

### C) 修复后 · 完整门禁 `--expect-clean-all` — W1 未完成的诚实结果，exit 1

```console
$ .venv/bin/python scripts/registry_row_audit.py --audit --expect-clean-all
exit=1
registry_row_audit: --expect-clean-all FAILED — 2 non-zero metric(s):
  definitions.en_boilerplate = 746
  definitions.concepts_without_defs = 10
```

> 这是**预期**结果：这两项正是 Phase 1（W1）的工作量，W0 不得也无法清空。
> 它同时证明剖面对比不是"把 gate 关掉"——更严格的 `--expect-clean-all` 依然红。

---

## 3. ④ 加严前后 exit 码对比（受控实验）

**设计**：固定语料，只更换 validator（旧 = `1e2cf30:pipeline/validate_registry.py`，新 = `08a2e98`）。
语料 = 当前 HEAD 的 `terms/`，仅注入 fixture 中的畸形行，因此两次运行的**唯一变量是加严规则本身**，
排除其它检查（如 alias 引用一致性）造成的混淆。

```console
$ PYTHONPATH=/home/gw/opt/fusion-terms .venv/bin/python /tmp/opencode/matrix/old_validator.py --terms-dir <corpus>
$ .venv/bin/python -m pipeline.validate_registry --terms-dir <corpus>
```

| 用例（语料来源） | 旧 validator `1e2cf30` | 新 validator `08a2e98` | 判定 |
|---|---|---|---|
| `shift` = HEAD + `pre_fix_concepts_shift.tsv` 3 行 | exit 0（静默通过） | **exit 1** | 加严生效 |
| `sixcol` = HEAD + `pre_fix_concepts_sixcol.tsv` 3 行 | exit 0（静默通过） | **exit 1** | 加严生效 |
| `ev4` = HEAD + 1 行 4 列 evidence | exit 0（静默通过） | **exit 1** | 加严生效 |
| `green` = HEAD 未变异对照 | exit 0 | exit 0 | 无误杀 |

新 validator 的失败消息（逐字）：

```text
[shift]   registry validation failed: .../concepts.tsv:3171: invalid category '能源安全'
[sixcol]  registry validation failed: .../concepts.tsv:3316: expected 8 columns: concept_id, category, preferr…
[ev4]     registry validation failed: .../evidence.tsv:2: expected 5 columns: concept_id, source, quote, added_by, added_at
```

> **注意（测试自身的坑，已修正）**：`ev4` 首轮构造时误截断了 evidence.tsv 的**注释表头行**
> （该行恰有 5 个 tab 分隔字段），validator 正确地未报错——那是**用例缺陷**而非门禁失效。
> 修正为"跳过 `#`/空行后截断首个数据行"后得到上表的正确 RED。

**敏感性（当前干净语料 + 单行变异）**：把 HEAD 语料的首个 8 列 concept 行截为 6 列 →
`--expect-clean` **exit 1**（`concepts.malformed_cols = 1`）；未变异同语料 **exit 0**。
证明当前 gate 处于活跃状态、非空转。

---

## 4. ⑤ fixture ↔ `git show f90e903` 行号对应

| fixture | 历史来源 | 列数 | 校验 |
|---|---|---|---|
| `tests/fixtures/registry/pre_fix_concepts_shift.tsv` | `git show f90e903:terms/registry/concepts.tsv \| sed -n '3171,3173p'` | 8,8,8 | `diff` 字节一致 ✅ |
| `tests/fixtures/registry/pre_fix_concepts_sixcol.tsv` | `git show f90e903:terms/registry/concepts.tsv \| sed -n '3316,3318p'` | 6,6,6 | `diff` 字节一致 ✅ |

RED 语料真实性（T0.11 验收第 3 条）：

```console
$ git show f90e903:terms/registry/concepts.tsv | sed -n '3316p' | awk -F'\t' '{print NF}'
6
```

**能失败证明（反例锚定）**：若上述命令输出变为 `8`，说明 fixture 来源已被改写／失效，
本任务判定 **FAIL** 并回溯 fixture 出处（计划 §T0.11「能失败证明」）。

---

## 5. 复跑清单（第三方逐条可复现）

```console
# 1) RED：修复前三表 → 结构门禁必须失败
.venv/bin/python scripts/registry_row_audit.py \
  --concepts /tmp/opencode/pre0b/terms/registry/concepts.tsv \
  --evidence /tmp/opencode/pre0b/terms/registry/evidence.tsv \
  --definitions /tmp/opencode/pre0b/terms/registry/definitions.tsv --expect-clean   # exit 1

# 2) GREEN：HEAD → 结构门禁通过
.venv/bin/python scripts/registry_row_audit.py --audit --expect-clean               # exit 0

# 3) 严格集：W1 未完成 ⇒ 必红（证明剖面未"关掉 gate"）
.venv/bin/python scripts/registry_row_audit.py --audit --expect-clean-all           # exit 1

# 4) 门禁加严的受控对比（旧 vs 新 validator，同语料）
PYTHONPATH=. .venv/bin/python /tmp/opencode/matrix/old_validator.py --terms-dir /tmp/opencode/vfy/shift/terms  # exit 0（旧，静默通过）
.venv/bin/python -m pipeline.validate_registry --terms-dir /tmp/opencode/vfy/shift/terms                        # exit 1（新）

# 5) fixture 与历史行号
git show f90e903:terms/registry/concepts.tsv | sed -n '3316p' | awk -F'\t' '{print NF}'   # 6

# 6) 全量门禁
.venv/bin/python -m pytest -q && .venv/bin/python -m pipeline.validate_registry && \
  .venv/bin/ruff format --check . && .venv/bin/ruff check . && \
  .venv/bin/mypy pipeline/ --ignore-missing-imports                                        # 全部 exit 0
```
