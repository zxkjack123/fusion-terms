---
plan_schema_version: "1.0"
linked_spec: null
scope_mode: "HOLD"
generated_at: "2026-10-26T12:05:00Z"
git_commit: "66197f2"
mode: "improve"
pm_tasks: ["T-4973"]
files_sha256:
  terms/registry/concepts.tsv: "auto (执行时实测)"
  terms/registry/definitions.tsv: "auto (执行时实测)"
  terms/registry/evidence.tsv: "auto (执行时实测)"
  terms/registry/aliases.tsv: "auto (执行时实测)"
  terms/allowlist_en.txt: "auto (执行时实测)"
  terms/allowlist_zh.txt: "auto (执行时实测)"
  artifacts/translation_dict.json: "auto (执行时实测)"
---

> 🔵 **状态：Phase 0（W0）✅ DONE（2026-10-26，收尾 commit `b175bab`）；D2-1 ~ D2-8 全部已裁决（选项 A，见文末《待裁决落地记录》）⇒ Phase 1（W1）**进行中**（2026-10-27 11:25 实测：`w1_a` **4/4 批 ✅**；`w1_b` **3/34 批**（`b01` ✅ commits `b578047`+`f58f0ff`；`b02` ✅ commits `7024be1`+`e67af8c`；`b03` ✅ commits `45313cc`+本节）；`w1_c` / W2 / W3 未开始；off-plan `--self-test` 重锚已完成 `471ab41`）。** — 本文件由 Plan Architect `mode=refine` 基于 PM 任务 **#T-4973** 的既有批次细化而来，并于 **`mode=improve`（2026-10-26，基线 `66197f2`）** 依据 W0 实测现实改口径：D2-7=A（W1 双侧重写 ⇒ 每批拆为 en/zh 两个 ≤30 min 子任务）、D2-8=A（来源白名单收窄）、D2-6=A（169 个拉丁名 id 补中文首选名）、批清单以 `.github/plans/t4973-batches/README.md` 为唯一权威（**119 批 / 2348 ids**）。
> W0 执行记录见文末 `## Execution Log` §「W0 数据完整性修复 + 门禁加严 — T0.4 ~ T0.13」；门禁 RED→GREEN 可复跑证据见 `.github/plans/t4973-batches/red-green.md`。
> ~~所有基线数字为 **2026-10-26 在 HEAD `3cb3837`** 实测~~ → **W0 后的权威数字以文末「W0 收口数字」为准**（覆盖率 47.11%、W2 738、W3a 854 等）。

# Plan: 术语注册表数据完整性修复 + definitions 质量重写 + allowlist 覆盖补齐（#T-4973）

## 背景与目标

- **问题/需求描述**：
  1. **数据完整性缺陷（最高优先）**：`terms/registry/concepts.tsv` 有 **179/3076** 行畸形（99 行缺 `category` 列导致列左移、80 行仅 6 列），静默穿过 `pipeline/validate_registry.py` 门禁，污染下游已发布产物。
  2. **definitions 质量缺陷**：746 行 en 通用套话 + 48 行 zh 模板残留（把语言标签 `en` 当术语名渲染；**已于 W0 清零**）+ 10 个 concept 无任何 definitions。
  3. **registry → allowlist 覆盖率仅 47.11%**：1627/3076 行未进入 IME 词表（W0 前为 46.3%/1652 行；64 行畸形行走 alias 已覆盖，故 W0 修复后未覆盖数下降 25 行）。
- **根因分析（已取证，verdict=SURVIVED）**：
  - 唯一引入者 = commit **`f90e903`**（"registry: complete bilingual definition retrofit for all 3064 concepts"）。该 commit 对 `concepts.tsv` 是**纯追加**（`+472/-0`，其中 358 行数据行）。实测：父提交 `f2308c0` 畸形 **0**、`f90e903` 畸形 **179**、HEAD 畸形 **179**。
  - 机制 = 追加源列序与 8 字段表头不一致，且门禁只校验 `len(fields) >= 2`，无 schema/取值校验 → 静默通过。
  - 下游污染链（同一根因，全部机械可解释）：`pipeline/export_registry.py:_iter_concept_rows` 按**位置**取列（`parts[2]` → `preferred_zh`），6 字段行的 `parts[2]` 是字面量 `en` → `translation_dict.json` 出现 **166** 条值为 `'en'` 的 `en2zh` 条目；99 行左移行的 `parts[1]`（中文）被当 `category` → `query_expansions.json` 出现 **99** 个中文 `category`。
  - 48 条 zh 释义损坏**全部落在 80 行 6 字段块内**（48/48），机制 = 生成器把该行的 `preferred_zh` 槽位值（= `en`）渲染进模板 `聚变/核工程术语，指“X”这一技术概念。`。既有 2706 行与 f90e903 同步新增的 179 行规范队列**污染率 0**，故非生成器普遍缺陷，而是**该 80 行块的输入畸形**所致。
- **目标**：
  1. **W0**：179 行畸形全部归零；48 条损坏 zh 释义归零；`evidence.tsv` 列数/来源规范化；`validate_registry` 门禁加严到**可机械判定且能失败**（RED 证据来自真实畸形语料）；重跑导出链使已污染产物指标归零。
  2. **W1**：**756** 个 concept 的 definitions 重写（用户裁决：**全部重写**，不接受保留套话）；**D2-7=A：en/zh 双侧同时重写**（每批 en 侧 + zh 侧各一个 ≤30 min 子任务）。
  3. **W2**：**738** 行 registry→allowlist 机械补齐（排除 **35** 专名），重跑 `export_registry` → `build_terms` → `sync_to_fcitx`。
  4. **W3**：854 个 concept 的中文首选名起草（用户裁决：并入本批次），**另含 D2-6=A 要求的 169 个拉丁装置代号补中文首选名**，要求可核验产出 + 抽检比例 + 分批 ≤30 min。
- **非目标（不做什么）**：
  - **不**把专名（company 25 / organization 7 / facility 3，共 35 行）写入 IME 词表 —— 用户已裁决专名不入 IME 词表。
  - **不**改写 W1 工作集**之外**的 zh 模板释义 —— D2-7=A 已把落在 `w1_a∪w1_b∪w1_c` 内的 **631** 行 `指“X”` 模板纳入 W1；**剩余 886 行**（131 `指“X”` + 755 `对应英文“X”`）本批不动，仅登记为后续候选（见 §待裁决 D2-3）。
  - **不**在 W2/W3 批次中扩大 16 类之外的结构改动，也**不**为通过验收而启用 `--allow-latin-names`（D2-6=A：判据保持字面）。
  - **不**重构 `pipeline/` 的导出架构 —— 只做 schema 解析加固所需的最小改动（列数/取值门禁），不改导出语义。
  - **不**新增 pipeline 之外的第三方工具；不使用 verl 等无关工具（PCI 约束）。
  - **不**本批次处理 `aliases.tsv`（未发现结构性缺陷；仅做只读校验）。
- **已有代码/流程复用分析**（先查已有能力，不另起炉灶）：
  - `pipeline/validate_registry.py`：复用并**加严**（concepts 精确 8 列 + category 取值域；evidence 精确 5 列）。
  - `pipeline/export_registry.py`（`--translation-dict --query-expansions --substitutions --tag-rules`）：复用，重跑消除污点。
  - `pipeline/build_terms.py`：复用；**硬约束** = EN 词表项不得含空白（`validate_no_whitespace_terms`，`SystemExit`），多词短语须以**连字符 token** 形式入库（仓库既有一半 EN 词条为连字符形态）。
  - `pipeline/sync_to_fcitx.py`、`pipeline/release_pack.py` + `pipeline/verify_release_contract.py`：复用（发布前验证）。
  - `tests/test_registry_validator.py`（12 个用例，`tmp_path` 内联 TSV 模式）、`tests/fixtures/`（`corpus/`、`terms/`）：复用为门禁 RED/GREEN 的落地位置。
  - `artifacts/terminology_sources/{iter_glossary_raw.tsv, iaea_safety_glossary_raw.tsv, gbt4960_9_terms.tsv}`（142/876/561 条）：复用为 W1/W3 的**仓内可核验出处**。

## 数据基线（W0 修复前快照 @ HEAD `3cb3837`；D/E 已按 W0 后权威值更新）

> **时效口径（improve 轮新增，务必先读）**：
> - §A/§B/§C/§F/§G 为 **W0 修复前**（`3cb3837`）的实测基线，保留作历史对照与 RED 证据；W0 后现状另见文末 §「W0 收口数字」。
> - §D/§E 中影响后续 Phase 规模的行（D1–D4、E2–E4）**已按 W0 后权威值更新**；若与文末 §「W0 收口数字」冲突，**一律以「W0 收口数字」为准**。
> - 一切数字在执行时重测（见 §动态基线约定）；本轮 improve 未改动 §Execution Log 任何历史条目，历史条目逐字可追溯。

### A. concepts.tsv 结构性缺陷

| # | 断言 | 实测值 | 复现命令（bash，仓根执行） |
|---|------|--------|---------------------------|
| A1 | concepts.tsv 数据行数 | **3076** | `awk -F'\t' '!/^#/ && NF>0' terms/registry/concepts.tsv \| wc -l` |
| A2 | 列数分布 | **6 列 = 80 行；8 列 = 2996 行** | `awk -F'\t' '!/^#/ && NF>0 {print NF}' terms/registry/concepts.tsv \| sort \| uniq -c` |
| A3 | 8 列但 `category` 非法（列左移） | **99** 行，行号 **3171–3315** | `awk -F'\t' '!/^#/ && NF==8 && $2 !~ /^(concept\|nuclear-fusion\|metric\|method\|code\|device\|system\|material\|diagnostic\|company\|organization\|doc\|limit\|effect\|facility\|principle)$/' terms/registry/concepts.tsv \| wc -l` |
| A4 | 完全规范行（8 列 + 合法 category） | **2897** | 3076 − 99 − 80 |
| A5 | 6 列块行号范围（连续） | **3316–3395** | `awk -F'\t' '!/^#/ && NF==6 {print NR}' terms/registry/concepts.tsv \| head -1` / `tail -1` |
| A6 | 6 列行样例 | `poloidal-field-power-supply␉electrical-power-systems␉en␉Poloidal Field Power Supply␉␉<notes>` | `sed -n '3316p' terms/registry/concepts.tsv \| cat -A` |
| A7 | 左移行样例 | `energy-security␉能源安全␉energy security␉␉␉active␉<notes>␉corpus` | `sed -n '3171p' terms/registry/concepts.tsv \| cat -A` |
| A8 | 引入 commit 唯一性 | `f2308c0`=0 / `f90e903`=**179** / HEAD=**179** | `for c in f2308c0 f90e903 HEAD; do echo -n "$c "; git show $c:terms/registry/concepts.tsv \| awk -F'\t' '!/^#/ && NF>0 && NF!=8' \| wc -l; done` |
| A9 | f90e903 对该文件为纯追加 | `+472/-0`（358 行数据行） | `git show f90e903 --numstat -- terms/registry/concepts.tsv` |
| A10 | `-S` 探针跨 `--all` 仅命中该 commit | 1 个 commit | `git log --all --oneline -S 'poloidal-field-power-supply' -- terms/registry/concepts.tsv` |

### B. 下游产物污染（由 A 机械推出）

| # | 断言 | 实测值 | 复现命令 |
|---|------|--------|----------|
| B1 | `translation_dict.json` 中 `en2zh` 值为字面 `'en'` | **166** | `python3 -c "import json;d=json.load(open('artifacts/translation_dict.json'));print(sum(1 for v in d['en2zh'].values() if v=='en'))"` |
| B2 | 同一性映射（`k==v`）总数 / 其中全小写短语式（左移行指纹） | **249** / **97** | `python3 -c "import json,re;d=json.load(open('artifacts/translation_dict.json'))['en2zh'];print(sum(1 for k,v in d.items() if k==v), sum(1 for k,v in d.items() if k==v and re.match(r'^[a-z][a-z0-9 -]*$',k)))"` |
| B3 | `query_expansions.json` 中非 ASCII `category` | **99** | `python3 -c "import json;d=json.load(open('artifacts/query_expansions.json'));print(sum(1 for c in d['concepts'].values() if not c['category'].isascii()))"` |
| B4 | `tag_rules.jsonl`（gitignored）非规范 category 行 / 命中畸形 concept 行 | **720** / **814** | `grep -c . artifacts/tag_rules.jsonl`；见 W0 T0.9 审计脚本 |
| B5 | `terminology_substitutions.tsv`（**git tracked**）是否被污染 | **未污染（0 行命中 179 畸形 concept）** | 见 W0 T0.9 审计脚本 `--audit` |
| B6 | 公开可见性口径修正 | 仅 `translation_dict.json` 提交入库（GitHub 可见 166 条）；`query_expansions.json`/`tag_rules.jsonl` 被 `.gitignore` 忽略；v2026.10.25 发布包仅含 `domain_terms.txt`+manifest+`terms/*`，**不含** registry 导出物 | `git ls-files artifacts`；`tar -tzf dist/fusion-terms-artifacts-v2026.10.25.tar.gz` |

### C. validate_registry 门禁缺口

| # | 断言 | 实测值 | 复现命令 |
|---|------|--------|----------|
| C1 | concepts 门禁仅要求 ≥2 列 | `if len(r.fields) < 2`（`pipeline/validate_registry.py:87`） | `grep -n "len(r.fields) < 2" pipeline/validate_registry.py` |
| C2 | definitions 门禁已要求精确 4 列（可加严先例） | `expected 4 columns`（`:255`） | `grep -n "expected 4 columns" pipeline/validate_registry.py` |
| C3 | 179 行畸形当前静默通过 | `registry OK: 3076 concepts, 10249 aliases, 3168 evidence rows, 6132 definitions`，exit **0** | `python3 -m pipeline.validate_registry; echo $?` |
| C4 | 门禁加严后 RED 锚点可用 | 前 179 行为**真实语料**，可 `git show f90e903:terms/registry/concepts.tsv` 逐行捕获为 fixture | `git show f90e903:terms/registry/concepts.tsv \| sed -n '3171,3173p'` |

### D. registry → allowlist 覆盖率（分母 = 3076；覆盖口径见下）

**覆盖口径（本计划唯一定义，禁止再用旧口径）**：某 concept 视为**已覆盖** ⟺ `concept_id`、`preferred_en`、`preferred_zh`、**或其任一条 alias** 出现在 `artifacts/domain_terms.txt`（即真正 build 出来的 IME 词表）中。复现：`python3 scripts/registry_coverage_report.py`（W0 T0.0 产出；执行前口径判定的历史值见下表）。

| # | 断言 | 实测值（口径见上） | 参照口径差异 |
|---|------|-------------------|-------------|
| D1 | 未覆盖（**W0 修复后权威值**） | **1627 / 3076 → 覆盖率 47.11%**（W0 前为 1652/46.3%，系"179 畸形行必然全未覆盖"的误算：实测其中 25 行经中文 alias 已覆盖）⇒ `uncovered = 1473(规范) + 154(畸形)` | `allowlist_only_coverage_pct` = **46.26**（W0 后权威值；任务书 1670/45.7% 属该口径，**已作废**） |
| D2 | **W2**（可机械补齐）：未覆盖 ∩ `preferred_zh` 非空 ∩ 非专名（**W0 后权威值**） | **738**（其中 `preferred_en` 含空格 **668**、单词形 **70**） | W0 前为 584（527/57）；**738 为权威值**（畸形行修复后变为可计数） |
| D3 | 专名排除 | **35**（company 25 / organization 7 / facility 3） | 任务书 36 |
| D4 | **W3a**（需起草中文首选名）：未覆盖规范行 ∩ `preferred_zh` 为空 | **854**（其中 107 行已有**真实 zh 释义**可推导；747 行仅 `对应英文“X”` 模板） | 任务书 860 系旧口径 |
| D5 | W3 组合口径修正 | **本计划 W3 = 854**（**不含** 99 左移行与 80 六列行，理由见 §基线修正 R-1/R-2） | 任务书 1039 = 860+99+80 |

### E. definitions.tsv 质量基线

| # | 断言 | 实测值 | 复现命令 |
|---|------|--------|----------|
| E1 | 数据行 / 列数 | **6132** 行，全部 4 列 | `awk -F'\t' '!/^#/ && NF>0 {print NF}' terms/registry/definitions.tsv \| sort \| uniq -c` |
| E2 | en 通用套话 | **746** 行（746 个 concept） | `grep -c "Fusion/nuclear engineering term referring to" terms/registry/definitions.tsv` |
| E3 | zh 模板残留 `指“en”`（**W0 后权威值**） | **0**（W0 前 48 行，⊂ E2 的 concept 集，全部落在 80 行 6 列块内；已由 `T0.7a`/`T0.7b` 重写清零，commit `a0cdab5`/`c2c4b7e`） | `grep -cP '\tzh\t.*指“en”' terms/registry/definitions.tsv` → `0` |
| E4 | zh 模板族总量（`聚变/核工程术语` 标记；**W0 后权威值**） | **1517** = 762 `指“X”` + 755 `对应英文“X”`（W0 前为 1565 = 810 + 755；差值 48 = E3 已修复的 `指“en”` 行）。**其中 631 行落在 W1 工作集内**（实测：`w1_a∪w1_b∪w1_c` 的 746 条 zh 行中 631 行匹配该标记）⇒ 由 D2-7=A 并入 W1 重写；**剩余 886 行**（131 `指“X”` + 755 `对应英文“X”`）仍属 D2-3 延后范围 | `grep -c "聚变/核工程术语" terms/registry/definitions.tsv` |
| E5 | 完全无 definitions 的 concept | **10**：`cate`,`pactole`,`pactiter`,`tract`,`oscar`,`acp-source-term`,`acp-deposition-coefficient`,`acp-erosion-coefficient`,`dissolution-precipitation-coefficient`,`acp-filter-model` | `comm -23 <(awk -F'\t' '!/^#/&&NF>0{print $1}' terms/registry/concepts.tsv \| sort -u) <(awk -F'\t' '!/^#/&&NF>0{print $1}' terms/registry/definitions.tsv \| sort -u)` |
| E6 | W1 的仓内出处可分性 | 746 en 套话中 **67** 行有真实 zh 释义（源 `GB/T-4960.9`）→ 可仓内推导；**679** 行仅有 zh 模板 → 须外部出处。**87** 行已带 http 证据 URL，**659** 行仅有 `internal:` 引用 | W0 T0.1 审计脚本 `--audit` |
| E7 | 来源字段现状 | `definitions.tsv` source 分布：`internal:dict-improvements` 4583 / `IAEA-safety-glossary` 856 / `GB/T-4960.9` 551 / `ITER-glossary` 142 | `cut -f4 terms/registry/definitions.tsv \| sort \| uniq -c \| sort -rn \| head` |

### F. evidence.tsv schema/来源卫生

| # | 断言 | 实测值 | 复现命令 |
|---|------|--------|----------|
| F1 | 数据行 / 列数分布（表头为 5 列） | **3168** 行：5 列 2953 / **4 列 213** / **2 列 2** | `awk -F'\t' '!/^#/ && NF>0 {print NF}' terms/registry/evidence.tsv \| sort \| uniq -c` |
| F2 | `source` 粘入 domain id（`internal:dict-improvements:<domain>`） | **427** 行，64 个 domain 后缀（均 concept-id 形态） | `grep -c "internal:dict-improvements:" terms/registry/evidence.tsv` |
| F3 | 仓内约定只承认 `internal:dict-improvements`（不带后缀） | `memories/repo/dict-improvement-workflow.md:39` | `grep -n "internal:dict-improvements" memories/repo/dict-improvement-workflow.md` |

### G. 工程门禁基线（改动后必须保持）

| # | 门禁 | 实测 | 命令 |
|---|------|------|------|
| G1 | `pytest -q` | **159 passed**，exit 0（≈6 s） | `.venv/bin/python -m pytest -q` |
| G2 | `mypy pipeline/` | `Success: no issues found in 16 source files`，exit 0 | `.venv/bin/mypy pipeline/ --ignore-missing-imports` |
| G3 | `ruff format --check .`（**0.17.2**，会格式化 Markdown 内 python 代码块） | `136 files already formatted`，exit 0 | `.venv/bin/ruff format --check .` |
| G4 | `ruff check .` | `All checks passed!`，exit 0 | `.venv/bin/ruff check .` |
| G5 | `validate_registry` | exit 0（但见 C1/C3 缺口） | `.venv/bin/python3 -m pipeline.validate_registry` |
| G6 | `verify_release_contract` | `--root .` **失败**（缺根级 `domain_terms.txt`）；须对 stage 目录执行：`dist/stage/v2026.10.25` → `contract OK: terms=3462 version=v2026.10.25` | `.venv/bin/python -m pipeline.verify_release_contract --root dist/stage/v2026.10.25` |
| G7 | CI（`.github/workflows/ci.yml`，py3.10/3.11/3.12 矩阵） | `pytest --cov-fail-under=45` → mypy → ruff check → ruff format check → compileall → validate_registry | `cat .github/workflows/ci.yml` |

### H. 用户裁决基线（本计划据此执行，不再重新征求）

| # | 裁决项 | 裁决内容 | 来源 |
|---|--------|---------|------|
| H1 | definitions 质量 | **全部重写** 746 行 en 套话（含其 48 行 zh 损坏的孪生行） | 父代理委派 prompt 明示 |
| H2 | 专名 | **不入** IME 词表（company/organization/facility = 35 行排除） | 同上 |
| H3 | W3 | **并入本批次**（不拆到后续批次） | 同上 |

> **授权归因**：H1–H3 三要素齐全（主体 = 用户；时点/载体 = 本计划任务的父代理委派 prompt；范围 = 上述三句逐字范围）。除此之外本计划**不含**任何"已授权"声明；`code` 类与其它新发现项一律进 §待裁决，不得自行裁决。

## 与任务书基线的差异（基线修正，附复核）

| # | 任务书基线 | 实测复核 | 结论与处置 |
|---|-----------|---------|-----------|
| R-1 | 99 左移行"其'中文名'实为英文串，须重新命名" | 99 行的**第 1 列就是正确中文**（如 `energy-security␉能源安全␉energy security`）；被当成"中文名"的英文串是**下游按位取列**（`parts[2]`）的投影，不是文件内容 | 99 行**无需重新命名**，只需列对齐（T0.2 补 `category` 并删多余空列）。W3 因此不含这 99 行 |
| R-2 | W3 = 1039（含 +80 六列行） | 80 六列行的 `preferred_zh` 槽位被 `en` 占据，且其 48 行的 zh 释义损坏**依赖这些中文名**才能修 | 80 行的中文名与 schema 修复**同批放在 W0**（破环依赖），W3 = 854（108 偏移已在 §D5 说明） |
| R-3 | 覆盖率 45.7%（1670 行未覆盖） | W0 后权威口径（含 `concept_id`/alias 命中 `domain_terms.txt`）：**1627 未覆盖 → 47.11%**；`allowlist_only` 口径 46.26% | **本计划以"是否进入 build 出的 `domain_terms.txt`"为唯一口径**（最贴近"IME 是否覆盖"），**值 47.11%**；W2/W3 规模按该口径重算（**738 / 854**），与任务书差 ≤2% |
| R-4 | `definitions.tsv` 747 行 en 套话 | 严格模板匹配（`^Fusion/nuclear engineering term referring to '.*' in technical context\.$`）为 **746** 行；宽松前缀 `grep -c "in technical context"` 亦为 746 | 取 **746**；旧"747"多计的 1 行不存在（无变体模板，`grep -v` 反查为 0 行） |
| R-5 | "已发布产物消费者可见" | `translation_dict.json` 入库（公开可见）；`query_expansions.json`/`tag_rules.jsonl` 被 gitignore；v2026.10.25 发布包**不含** registry 导出物（见 B6） | 污染**公开可见面**仅为 `translation_dict.json`；重跑导出链仍必要（本地/未来发布包） |
| R-6 | `code` 类 9 个概念待裁决（含 `opencascade`） | `opencascade` **已覆盖**（其 alias `OCC` 在 `allowlist_en.txt`），真正未覆盖的是 **8** 个：`vmec,desc,simsopt,cate,pactole,pactiter,tract,oscar`；且 `code` 类共 107 个 concept 中 **99 个已覆盖**；`MCNP` 在 `allowlist_en.txt` 与 `allowlist_zh.txt` **都**存在（`mcnp` 小写不存在） | 待裁决清单收敛为 8 个 id，且**先例强度**已量化（99/107 已入表）→ §待裁决 D2-1 |
| R-7 | W2 595 行 | **738** 行（W0 后权威值；W0 前为 584）；其中 **668** 行 `preferred_en` 含空格（须连字符 token 化），**70** 行为单词形（其中 D2-2 列出的 21 个通用英文词为 W0 前口径，W0 后单词形总数以实测 70 为权威、通用词清单以 §D2-2 列举为准），且 `system`、`mode` 已在 `denylist.txt` 中 | 见 §待裁决 D2-2（通用词是否入 EN 词表） |

## 风险与对策表

| # | 风险 | 概率 | 影响 | 对策 | 触发信号 |
|---|------|------|------|------|---------|
| RK1 | W0 修 179 行时误改规范行 | 中 | 高（数据回归） | 只做**定点行替换**（行号 + concept_id 双锚），改后跑 `scripts/registry_row_audit` 断言 `规范行=2897+179=3076` 且 concept_id 集合与改动前 `diff` 为空 | audit 报 concept_id 集合变化 |
| RK2 | 门禁加严导致 CI 变红（本仓 CI 曾连续 4 次红灯，刚于 run #43 恢复） | 中 | 高 | 顺序纪律：**先修数据（T0.2–T0.5）再改门禁（T0.6–T0.7）**；每次 commit 前本地跑全量 G1–G5 | `ruff format --check`/CI 红 |
| RK3 | `ruff format --check .` 会格式化 **Markdown 内 python 代码块**（0.17.2 行为）→ 新计划/脚本被记为未格式化 | 高 | 中 | 新脚本按 `ruff format` 输出写；本计划文件提交前跑 `ruff format .github/plans/terminology-coverage-and-definition-quality.md`（先例 commit `8f51d52`） | `ruff format --check .` 报本文件 |
| RK4 | W1/W3 定义/名称的来源不可核验（"看起来对"） | 高 | 高 | 每批强制过 `scripts/registry_batch_verify.py`（模板正则黑名单 + 最小长度 + 来源白名单）；**来源口径按 D2-8=A 收窄**：接受仓内依据 `corpus`（该 concept 的 registry `notes` / 既有 zh 释义）与 `GB/T-4960.9`/`ITER-glossary`/`IAEA-safety-glossary`；**仅当释义显式引用外部权威时**才要求可 200 的 URL（此时才跑 `--check-urls`，无网环境用 `--no-net` 并标 `[NO-NET]`） | 批验收 exit ≠ 0 |
| RK5 | W2 向 `allowlist_en.txt` 注入空白项 → `build_terms` `SystemExit` | 中 | 高 | W2 仅写**连字符 token**（含空格者用 `concept_id`）；批验收含 `grep -v '^#' terms/allowlist_en.txt \| grep -c ' '` = 0 | `build_terms` 抛 whitespace |
| RK6 | W2/W3 批量追加引入重复行 | 中 | 中 | 追加前 `sort | uniq -d` 断言；批验收含唯一性检查 | 重复行非空 |
| RK7 | 修复后导出物数量大幅变化触发 snapshot 测试红 | 中 | 中 | 先跑 `pytest -q tests/test_export_registry*`；如为 hardcode 基线则按数据事实更新并记录 | pytest 相关用例失败 |
| RK8 | 47 处"隐式依赖"：179 行被 alias/evidence 引用 | 低 | 中 | 只改 `concepts.tsv` 列结构，不动 `concept_id`，故 alias/evidence 外键不变（`validate_registry` 会校验 `concepts without evidence`） | validate_registry 报缺失 evidence |
| RK9 | W3 起草 854 个中文名产生"机翻腔"或与既有别名冲突 | 中 | 中 | 与 `aliases.tsv` 既有 zh 别名做冲突检查（先例：`grep -P '^击穿\t'`）；抽检 ≥10% 且抽检不通过则整批返工 | 抽检 FAIL 行数 > 0 |
| RK10 | 长时间批处理会话上下文耗尽（**119 批**，以 `.github/plans/t4973-batches/README.md` 为权威） | 高 | 中 | 每批次独立 session（批清单落地为文件，会话无状态依赖）；每 5 批一次 `git status` + 全量门禁 | 批次验收命令报错 |

### Error & Rescue Map（关键失败路径映射）

| 代码路径/操作 | 可能的失败 | 错误类型 | 已处理？ | 处理方式 | 用户可见行为 |
|---|---|---|---|---|---|
| 修复 99 左移行 | 删列位置错（多删/少删） | 数据回归 | Y | 逐行断言「8 列 + `$2` ∈ 16 类 + `$3` 为中文」；回归计数 `2897+99` | audit 报错并回滚该行 |
| 修复 80 六列行 | category 取值越界 | 门禁红 | Y | 16 类白名单 + 兄弟 concept 对照（同 domain 已有规范行） | `validate_registry` 报错 |
| 修 48 zh 释义 | 中文名与 `preferred_zh` 不一致 | 语义漂移 | Y | 断言 zh 释义中出现的术语名 == 该 concept 的 `preferred_zh` | 批验收 exit 1 |
| evidence 列数规范化 | 插入空列破坏 `quote` 语义 | 语义漂移 | Y | 只做「列数 4→5 / 2→5」的**空 `quote` 补齐**，不改 `source`/`added_by`/`added_at` 值 | diff 仅新增空字段 |
| 门禁加严 | 现有 11 处测试 fixture 仍用 ≤4 列 evidence | 测试红 | Y | T0.7 同步更新 `_MINIMAL_EVIDENCE` 等 fixture（声明文件内改动）—— **实际由 `T0.9`+`T0.10` 同一 commit `08a2e98` 落地**；实际范围含 8 个测试文件的机械补 tab + 1 行陈旧 fixture 修正（`component`→`concept`），**以 §Execution Log（commit `08a2e98`）记的偏差为准**（用户已追认，见《W0 收尾裁决与追认》追认 1） | pytest 红 → 按 T0.7 修复 |
| 导出链重跑 | `--translation-dict` 等 flag 遗漏 | 产物不更新 | Y | 固定命令串（见 T0.9）；断言三项污点指标归零 | 断言失败 |
| W1 定义 | 出现 `internal:TODO` 占位 | 门禁红 | Y | `validate_registry` 已存在 `internal:TODO` 检查（`test_registry_validator.py:190`） | 报错阻断 |
| W2 allowlist | 与 `denylist.txt` 冲突（`system`/`mode`） | 静默无效 | Y | 先 `grep -x` 查 deny；冲突项记入 D2-2 决策清单而非强写 | 无 |
| W3 中文名 | 与既有 zh 别名冲突（同名多 concept） | 歧义 | Y | 冲突清单交人工裁决（不得静默择一） | 冲突清单输出 |
| Rime 同步 | `sync_to_fcitx` 覆盖本机词表 | 环境副作用 | Y | 仅在 Phase 4 执行，且先备份目标文件（脚本自身有 temp 写入逻辑）；无 `~/.config/fcitx` 时用 `--dest` 指向临时目录做 smoke | 本机词表更新 |

## 待裁决项（D2 — 须用户裁决，执行时不得自行决定）

| # | 裁决点 | 现状数据 | 选项（推荐置首） | 阻塞的下游任务 |
|---|--------|---------|-----------------|---------------|
| D2-1 | `code` 类 8 个概念（`vmec`,`desc`,`simsopt`,`cate`,`pactole`,`pactiter`,`tract`,`oscar`）是否入 IME 词表 | `code` 类共 107 个 concept，**99 个已覆盖**（其中 `opencascade` 靠 alias `OCC` 入表）；`MCNP` 在 `allowlist_en.txt`+`allowlist_zh.txt` 均有 | **A. 入表**（连字符/大写代号形式，与 99/107 既有先例一致）<br>B. 不入表（仅保留 `MCNP` 先例） | W2 批次 T2.1（含 code 6 行）；W1 的 10 个缺失概念定义不受影响 |
| D2-2 | W2 中 **21 个通用英文单词形 concept**（`design`,`system`,`material`,`performance`,`simulation`,`calculation`,`maintenance`,`evaluation`,`method`,`mode`,`device`,`mitigation`,`decay`,`cooling`,`damage`,`protection`,`sealing`,`steel`,`wall`,`lining`,`fuels`）是否写入 `allowlist_en.txt` | 其中 `system`、`mode` 已存在于 `denylist.txt`（写入即被 deny 覆盖，属无效操作）；其余 19 个为通用英文词，入表会扩大 EN 词表 1246→1265+ | **A. 只入领域专指项（36 个：`thermodiffusion`,`glovebox`,`embrittlement`,`plasmoid`,`recuperator`,`omicron…` 等 + 8 code），通用词不动**<br>B. 21 个全入<br>C. 全不入 | W2 批次 T2.2（单词形批次） |
| D2-3 | 剩余 1517 行"低信息但未损坏"的 zh 模板释义（762 行 `指“X”` + 755 行 `对应英文“X”`）是否在后续批次重写 | 用户裁决的本批 W1 范围为 757 concept（746 en + 10 缺失 + 48 zh 损坏）；1517 行**不在**本批范围 | **A. 本批不动，登记为后续批次（推荐）**<br>B. 本批顺带重写（W1 规模 ×2 ≈ 1514 行） | 无（本批 W1 任务不受阻） |
| D2-4 | W1 的**抽检比例与验收人** | 用户口径"须设计可核验产出 + 抽检比例" | **A. 每批 100% 过机械门禁 + 每 5 批抽检 10%（≥8 行）由独立 agent 复核语义**（推荐）<br>B. 全量人工复核（成本 ≈ 766 行）<br>C. 仅机械门禁 | W1 批次验收（T1.x） |
| D2-5 | W3 中文名的**来源等级**要求 | 854 个 concept：107 行可从仓内 `GB/T-4960.9` zh 释义推导；747 行无仓内出处 | **A. 允许 `preferred_en` + 权威仓外来源（Wikipedia/IAEA/ITER URL）作为命名依据，URL 须 200（推荐）**<br>B. 仅允许仓内出处（则 747 行无法完成，需缩范围） | W3 批次（T3.x） |
| D2-6 | `--mode names` 的 **CJK 硬要求** 对 169 个 `preferred_zh == preferred_en` 且无 CJK 的 id（装置代号 `rfx-mod`/`c-2w`/`rexie`/`kmax`/`exl-50` …）如何处置（T0.2 执行时发现） | 169 个 id 实测各 1 个、含 CJK **0** 个；`--allow-latin-names` 名单**救不了**（按字面实现：CJK 为无条件要求） | **A. 维持字面 + 由 W3 为这 169 个补中文首选名（推荐，保真计划）**<br>B. 令 `--allow-latin-names` 名单同时豁免 CJK（装置代号保留拉丁名；一处改动，可逆） | W3 批次（T3.x）+ W3 验收 |
| D2-7 | W1 批次**是否连 zh 行一起重写**（T0.0/T0.2 执行时发现的口径冲突） | W1 集合由 **en 套话**构成（746 条）；这些 concept 的 zh 行多为 `指“X”` 模板（属 D2-3 延后的 1517 行）。而 `--mode definitions` 要求该 id 的 en/zh **同时**合规 → 冲突 | **A. W1 连 zh 一起重写**（本批 +≈700 行、预估 +≈18 h，一次到位）<br>**B. W1 批次改用 `--lang en` 验收**，zh 模板留给后续批次（本批不扩范围） | W1 全部批次（T1.x） |
| D2-8 | W1 释义的**来源白名单**是否接纳**仓内依据 `corpus`**（T0.7 执行时发现） | `definitions.tsv`（4 列 `concept_id/lang/definition/source`）共 **6132** 行，来源实测分布：`internal:dict-improvements` **4535** / `IAEA-safety-glossary` 856 / `GB/T-4960.9` 551 / `ITER-glossary` 142 / `corpus` **48**（后者为本次 T0.7a/b 新增）。批验收器 `registry_batch_verify.py` 的 `def_source_unknown` 为**闭合白名单**（接受 `corpus`/`GB/T-`/`ITER-`/`IAEA-` 前缀，**不接受任何 `internal:*`**）⇒ 与既有 4535 行同源的做法会在批验收处变红 | **A. 允许 `corpus` 作为仓内依据**（释义来自该 concept 的 registry `notes` / 既有 zh 释义；**仅当释义显式引用外部权威时**才要求 URL / `GB/T` / `ITER` / `IAEA`）（推荐）<br>B. 只接受外部权威出处（`corpus` 不算）→ W1 的 679 行须**逐条**取得外部来源，工期与来源可达性风险显著 | W1 全部批次（T1.x） |

> 上述 D2-1~D2-8 由父代理（或用户）裁决后回写本节；未裁决前按"推荐项"执行**但**在 commit message 与本节标注 `[默认取推荐项，待追认]`。
>
> **✅ 2026-10-26：D2-1 ~ D2-8 已全部裁决（用户选项 A），见文末《待裁决落地记录》。执行时按裁决口径，无遗留"待追认"项。**

## 时序推演

| 阶段 | 关键决策/潜在阻塞 |
|------|------------------|
| 初期（T0.0–T0.5） | 先固化口径与审计脚本，再做数据修复。**先修数据后改门禁**（RK2）；T0.2/T0.3a 改列结构后立即跑全量门禁，确认无规范行回归 |
| 中期（T0.6–T0.9） | 门禁加严是"能失败"的证明点：先录 RED（真实 179 行语料 fixture 必须 FAIL），再录 GREEN（修复后 live registry PASS）。导出链重跑后三项污点指标须归零，否则回溯 parse 位置 |
| 后期（Phase 1–3） | W1/W3 是**人力密集型**（W1 39 批 ×2 侧重写、W3 43 批 + D2-6 的 9 批；批数以 `.github/plans/t4973-batches/README.md` 为唯一权威），阻塞点 = 来源可达性（仅当释义显式引用外部权威时才需 URL 200）与批验收；W2 依赖 W0 的 `concepts.tsv` 修复结果（W2 清单口径须在 W0 后重算 —— 已由 commit `66197f2` 重生成）。W3 依赖 W0（不得基于畸形行起草名字） |
| 收尾（Phase 4） | 发布包验证（`release_pack` + `verify_release_contract`）在最后；`sync_to_fcitx` 有本机副作用，放最后且先备份 |

## 执行计划

### Phase 0: W0 — 数据完整性修复 + 门禁加严（最高优先，Phase 1–3 的前置）

> **Phase 0 首步（强制）**：`git rev-parse HEAD` + `git status --porcelain` 实测；若 HEAD ≠ `3cb3837` 或工作区非空，先按 §动态基线约定重测 T0.1 审计基线并更新锚点（**行号锚点 3171/3316 仅在 HEAD `3cb3837` 成立**）。
> **Phase 0 完成定义（一条命令）**：`.venv/bin/python scripts/registry_row_audit.py --audit --expect-clean` → exit 0（`malformed=0, shifted=0, sixcol=0, evidence_cols_non5=0, zh_en_corruption=0`）。
> **门禁剖面（以 T0.11 落地记录为准，见 commit `a4ac8d8`）**：`--expect-clean` = **W0 结构集**（即本完成定义的 5 项 + `bad_category`/`glued_source_rows`）；`--expect-clean-all` = **全集**（W0 结构集 ∪ W1 质量指标 `en_boilerplate`/`concepts_without_defs`），**在 Phase 1 完成时使用**。原文"`--expect-clean` = 全部指标为 0"的字面表述**已作废**。

#### Task T0.0: 覆盖率口径固化脚本（消除 45.6%/45.7%/46.3% 三套口径争议）

- **目标**：把 §数据基线 D 的口径固化为可重复脚本，输出 W2/W3/W1 三个工作集与总覆盖率。
- **依赖**：无
- **frontier**：是
- **执行者**：Simulation Builder（数据脚本类）
- **预估墙钟**：25 min
- **修改内容**：
  - 新增文件 `/home/gw/opt/fusion-terms/scripts/registry_coverage_report.py`：读取 `terms/registry/concepts.tsv`、`terms/registry/aliases.tsv`、`terms/denylist.txt`、`artifacts/domain_terms.txt`；按「`concept_id`/`preferred_en`/`preferred_zh`/任一 alias 出现在 `domain_terms.txt`」判定已覆盖；打印 `total/covered/uncovered/W2/W2_multiword/W2_single/W3a/proper_excluded/coverage_pct`；`--json PATH` 输出机器可读结果；`--emit-lists DIR` 落地工作集文件。
- **修改边界**：不得修改 `terms/` 与 `artifacts/` 下任何数据文件；不得修改 `pipeline/`；脚本只读。
- **质量检查方式**：
  - 脚本输出必须能复现 §D1–D4 的实测值（1473/1652/46.3%/584/527/57/854/35）。
    > **✅ 已完成（commit `40ae0ea`，见 §Execution Log T0.0）**：本条的期望值是**规划期（W0 前）**口径；W0 后现行值为 `covered 1449 / uncovered 1627 / coverage_pct 47.11 / W2 738 (668+70) / W3a 854 / proper_excluded 35`。两者差异已由 §D1/D2 与「W0 收口数字」记录，**以「W0 收口数字」为准**。
  - `ruff format --check scripts/registry_coverage_report.py` 与 `ruff check scripts/registry_coverage_report.py` 通过。
- **验收标准**：
  - ✅ [脚本存在且可执行] `[T-A]` `.venv/bin/python scripts/registry_coverage_report.py` → exit 0，stdout 含 `coverage_pct: 46.3`（±0.1）且 `W2: 584`、`W3a: 854`（在 HEAD `3cb3837` 未修数据时）
  - ✅ [口径单调性] `[T-B]` `assert covered + uncovered == total == 3076`
  - ✅ [格式门禁] `[T-A]` `.venv/bin/ruff format --check scripts/registry_coverage_report.py` → exit 0
- **能失败证明（反例锚定法）**：临时把 `--terms-file` 指向 `/dev/null`（覆盖率应变为 0），命令非 0 结束或 `coverage_pct: 0.0`；若能仍报 46.3 则脚本写死数字 → 判 FAIL。
- **潜在风险**：`domain_terms.txt` 陈旧（未随 allowlist 重建）→ 本任务只读，若与 allowlist 不一致由 W2 尾任务 **T2.38** 重建后重算。
- **预留歧义标注**：
  - [ ] 无歧义：所有字段可直接执行，无需额外推断

#### Task T0.1: 结构审计脚本（RED 证据与回归计数的唯一来源）

- **目标**：把 §A/§E/§F 全部结构断言固化为一条命令，供修复前后对照。
- **依赖**：无
- **frontier**：是
- **执行者**：Simulation Builder
- **预估墙钟**：25 min
- **修改内容**：
  - 新增文件 `/home/gw/opt/fusion-terms/scripts/registry_row_audit.py`：对 `concepts.tsv` 输出 `data_rows / cols_dist / malformed_cols / bad_category / shifted_rows(行号区间) / sixcol_rows(行号区间) / concept_ids_sha256`；对 `evidence.tsv` 输出 `cols_dist / non5_cols / glued_source_rows`；对 `definitions.tsv` 输出 `en_boilerplate / zh_en_corruption / concepts_without_defs`；参数 `--audit`（打印 JSON）、`--expect-clean`（**W0 结构集**指标全为 0 时 exit 0，否则 exit 1）、`--expect-clean-all`（**全集**指标为 0 时 exit 0；Phase 1 完成时使用）、`--json PATH`。
- **修改边界**：只读脚本；不得写 `terms/`、`artifacts/`。
- **质量检查方式**：`concept_ids_sha256` 用于证明「修复只改列结构、未增删 concept」。
- **验收标准**：
  - ✅ [复现全部结构基线] `[T-A]` `.venv/bin/python scripts/registry_row_audit.py --audit` → exit 0，且字段 `data_rows=3076`、`malformed_cols=80`、`bad_category=99`、`en_boilerplate=746`、`zh_en_corruption=48`、`glued_source_rows=427`、`non5_cols=215`（与 §A/§E/§F 实测一致）
  - ✅ [能失败] `[T-A]` `.venv/bin/python scripts/registry_row_audit.py --expect-clean` → **exit 1**（未修复前必须失败；若 exit 0 说明规则为空转）
  - ✅ [格式门禁] `[T-A]` `.venv/bin/ruff format --check scripts/registry_row_audit.py` → exit 0
- **能失败证明（变异法）**：复制 `concepts.tsv` 到临时目录，人为把一行 8 列改成 6 列 → `--audit` 的 `malformed_cols` 必须 +1（证明规则绑定真实语料而非常量）。
- **潜在风险**：行号区间在 HEAD 变化后失效 → 脚本输出以 `concept_id` 为准、行号仅作提示。
- **预留歧义标注**：
  - [ ] 无歧义

#### Task T0.2: 批验收脚本（W1/W2/W3 每批的唯一验收入口）

- **目标**：为 W1（definitions 重写）、W3（中文名起草）、W2（allowlist 追加）提供机械可判定的批次验收。
- **依赖**：无
- **frontier**：是
- **执行者**：Simulation Builder
- **预估墙钟**：30 min
- **修改内容**：
  - 新增文件 `/home/gw/opt/fusion-terms/scripts/registry_batch_verify.py`，三种模式：
    - `--mode definitions --ids-file F --expect N`：断言每个 id 的 en/zh 行恰各 1 条；文本不匹配套话正则 `^Fusion/nuclear engineering term referring to '.*' in technical context\.$` 与 `聚变/核工程术语`；长度 en ≥ 40 字符、zh ≥ 12 字符；`source` ∈ {`http(s)://…`, `GB/T-4960.9`, `ITER-glossary`, `IAEA-safety-glossary`, `corpus`}；禁止 `internal:TODO`；`--check-urls` 时对 http 来源发 HTTP 请求并要求 200（`--no-net` 可跳过并打印 `SKIPPED-NET`）。
    - `--mode names --ids-file F --expect N`：断言每个 id 的 `preferred_zh` 非空、含 CJK 字符、无空白、与 `preferred_en` 不全等（除非在 `--allow-latin-names` 名单内）。
    - `--mode allowlist --ids-file F --expect N`：断言每个 id 的 `preferred_zh` ∈ `allowlist_zh.txt`，且（`preferred_en` 含空格时）`concept_id` ∈ `allowlist_en.txt`；断言 `grep -v '^#' terms/allowlist_en.txt | grep -c ' '` == 0。
  - 未通过时 exit 1 并打印全部违规行（含 `file:line`）。
- **修改边界**：只读校验脚本；不得写 `terms/`、`artifacts/`（`--json` 仅写调用方指定路径）。
- **质量检查方式**：`--self-test` 子命令（内置 3 条真实畸形样例 + 3 条合规样例，断言各模式判定正确）。
- **验收标准**：
  - ✅ [自检通过] `[T-A]` `.venv/bin/python scripts/registry_batch_verify.py --self-test` → exit 0
    > **注记（2026-10-26，裁决 4=A，off-plan 修复）**：本条在 T0.2 落地时成立（24/24）。W0 修好该自检的 3 处**真实语料锚点行**后（`concepts.tsv:3316` 六列行、`:3171` 左移行、`definitions.tsv:5838` `指“en”` 行），断言因**规则不再触发**而变红 → 实测 **18/24 exit 1**（规则本身有效，已由 W1 逐批仓外变异法复证）。已按裁决 A 以临时副本地重建缺陷的方式重锚（规则一条未改），**现状重新为 24/24 exit 0**。证据见 `.github/plans/t4973-batches/self-test-reanchor.md`。
  - ✅ [能失败] `[T-A]` 用未修复的 6 列 concept id 造 ids 文件跑 `--mode names`（该 id 的 `preferred_zh` 为空）→ **exit 1**
  - ✅ [格式门禁] `[T-A]` `.venv/bin/ruff format --check scripts/registry_batch_verify.py` → exit 0
- **能失败证明（实现回退法）**：把套话正则替换为 `^$`（永不匹配）后 `--self-test` 必须失败 → 证明该规则真的在起作用。
- **潜在风险**：`--check-urls` 在无网环境全批失败 → 明确降级路径（改用仓内出处），不得静默放宽。
- **预留歧义标注**：
  - [ ] 无歧义

#### Task T0.3: 工作集与批次清单落地（可审计、可复现）

- **目标**：把 W1-A/W1-B/W2/W3 的工作集与逐批 id 清单提交入库，使每个批次任务无状态、可独立执行。
- **依赖**：T0.0、T0.1、T0.2
- **frontier**：否
- **执行者**：Simulation Builder
- **预估墙钟**：20 min
- **修改内容**：
  - 新增目录与文件 `/home/gw/opt/fusion-terms/.github/plans/t4973-batches/`：
    - `w1_a.ids`（67 行，仓内可推导）、`w1_b.ids`（679 行，来源按 D2-8=A 可为仓内 `corpus`）、`w1_c.ids`（10 行，缺失 definitions）
    - `w1_a_b01.ids`…`w1_a_b04.ids`（20/20/20/7）、`w1_b_b01.ids`…`w1_b_b34.ids`（每批 20，尾批 19）
    - `w2.ids`（738）、`w2_b01.ids`…`w2_b37.ids`（每批 20，尾批 18）
    - `w3.ids`（854）、`w3_b01.ids`…`w3_b43.ids`（每批 20，尾批 14；**内/外部依据不再按批文件分组**，混排）
    - `README.md`（清单口径、生成命令、批次总数）
  - 生成命令：`.venv/bin/python scripts/registry_coverage_report.py --emit-lists .github/plans/t4973-batches --batch-size 20`
- **🔄 W0 后重生成（2026-10-26，commit `66197f2`；本条为本任务的唯一现行口径）**：W0 修复畸形行后该目录**已重生成**，规模变为 `w1_a 67→4 批` / `w1_b 679→34 批` / `w1_c 10→1 批` / **`w2 738→37 批`** / `w3 854→43 批` = **119 批 / 2348 ids**（`.ids` 文件 128 个 + 6 个非 `.ids` 文件）。**批数与每批大小一律以 `.github/plans/t4973-batches/README.md` 为唯一权威**；下方验收标准中的旧数字（`584` 等）为规划期实测值，**已被 README 取代**。生成器只增不删：重生成后若批数下降须人工清理残留 `*_b*.ids`（本次批数上升，无残留）。
- **修改边界**：只新增 `.github/plans/t4973-batches/` 下文件；不得改动任何 `terms/`、`pipeline/`、`artifacts/` 文件。
- **质量检查方式**：清单总行数与 §D 实测对齐；每批文件行数 == 批大小。
- **验收标准**（旧数字保留作历史对照；现行批数以 README 为准）：
  - ✅ [集合规模] `[T-A]` `wc -l .github/plans/t4973-batches/{w1_a,w1_b,w1_c,w2,w3}.ids` → 规划期为 `67 679 10 584 854`；**W0 后现行值为 `67 679 10 738 854`**
  - ✅ [无重复无交集] `[T-A]` `sort .github/plans/t4973-batches/w2.ids .github/plans/t4973-batches/w3.ids | uniq -d | wc -l` → `0`
  - ✅ [批次无遗漏] `[T-A]` `cat .github/plans/t4973-batches/w1_b_b*.ids | wc -l` → `679`
  - ✅ [批数与 README 一致] `[T-A]` `for s in w1_a w1_b w1_c w2 w3; do echo "$s $(find .github/plans/t4973-batches -maxdepth 1 -name "${s}_b*.ids" | wc -l)"; done` → `4 / 34 / 1 / 37 / 43`（合计 **119**）
- **能失败证明（反例锚定）**：故意删掉 `w1_b_b34.ids` 中一行 → 上一条断言必须变 678 而 FAIL。
- **潜在风险**：`--batch-size` 与 Phase 表不一致 → 本任务的 `README.md` 记录实际批数与每批大小，Phase 1–3 的表格以它为准。
- **预留歧义标注**：
  - [ ] 无歧义

#### Task T0.4: 修复 99 行左移行（补 `category`、删 2 个多余空列）

- **目标**：`concepts.tsv` 中 99 行（HEAD `3cb3837` 的行 3171–3315）恢复 8 列语义，`category` 取合法值，中文名与英文名各归其位。
- **依赖**：T0.1、T0.2、T0.3
- **frontier**：是（与 T0.5 不冲突：行区间不重叠）
- **执行者**：Simulation Builder
- **预估墙钟**：30 min
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：对 99 行执行定点改写 ——
    - 现状列序：`cid␉<中文名>␉<英文名>␉␉␉active␉<notes>␉corpus`（8 列但语义错位）
    - 目标列序：`cid␉<category>␉<中文名>␉<英文名>␉␉active␉<notes>␉corpus`（8 列）
    - **`category` 取值规则**（禁止自造）：① 该 id 在 `terms/registry/aliases.tsv` 有同域兄弟概念 → 取兄弟的 category；② 无法对照时按语义判定（如 `nuclear-heating-rate`,`transmutation-rate`,`erosion-rate`,`leak-rate`,`pumping-speed`,`wall-plug-efficiency`,`recycling-rate` → `metric`；`life-cycle-assessment`,`tungsten-inert-gas-welding`,`laser-welding`,`weld-inspection` → `method`；`thermocouple`,`strain-gauge`,`flowmeter`,`ion-source`,`rf-window`,`dummy-load`,`quench-heater`,`helium-refrigerator`,`shielding-plug`,`area-monitor` → `device`；其余通用/能源/防扩散类 → `concept`）；③ 全部 99 行的取值必须落在 16 类白名单内。
  - 记录：把 99 行的 `id → category` 对照写入 `.github/plans/t4973-batches/category-map-shift99.tsv`（列为 `concept_id␉category␉依据`）。
- **修改边界**：只改这 99 行；不得改动其它任何行的列结构；**不得增删 concept_id**（用 T0.1 的 `concept_ids_sha256` 证明）。
- **质量检查方式**：
  - 修复后 `scripts/registry_row_audit.py --audit` 的 `bad_category=0`、`shifted_rows=0`、`data_rows=3076` 且 `concept_ids_sha256` 与修复前一致。
  - 目视抽检 ≥10 行（`sed -n` 打印，人工确认中文归位）。
- **验收标准**：
  - ✅ [结构归零] `[T-A]` `.venv/bin/python scripts/registry_row_audit.py --audit` → exit 0 且 `bad_category=0 && shifted_rows=0`
  - ✅ [集合不变] `[T-B]` `assert audit_before["concept_ids_sha256"] == audit_after["concept_ids_sha256"]`
  - ✅ [门禁不退化] `[T-A]` `.venv/bin/python -m pipeline.validate_registry` → exit 0
  - ✅ [对照表完整] `[T-A]` `wc -l .github/plans/t4973-batches/category-map-shift99.tsv` → `99`（不含表头则 `100`，README 中固定口径）
- **能失败证明（变异法）**：把任一行 `category` 改成 `能源安全` → `bad_category` 必须回到 1。
- **潜在风险**：`notes`/`source` 列本身也可能错位（需实测：修复后对 99 行逐列断言 `$6 == active && $8 == corpus`）。
- **预留歧义标注**：
  - [ ] 无歧义

#### Task T0.5: 修复 80 行 6 列块（补 `category`/`status`/`source`，domain 标签转存）

- **目标**：80 行（HEAD `3cb3837` 行 3316–3395 连续块）恢复 8 列，domain 标签不丢。
- **依赖**：T0.1、T0.2、T0.3
- **frontier**：是
- **执行者**：Simulation Builder
- **预估墙钟**：30 min
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：对 80 行改写 ——
    - 现状：`cid␉<domain-label>␉en␉<英文名>␉␉<notes>`（6 列）
    - 目标：`cid␉<category>␉␉<英文名>␉␉active␉<notes> [domain: <domain-label>]␉corpus`（8 列；`preferred_zh` **暂留空**，由 T0.6 填）
    - `category` 规则：`domain-label ∈ {nuclear-fusion, metric}` 时直接采用（共 16 行）；其余按「同 domain-label 组内已存在的规范兄弟概念」对照，取最常见 category（例：`poloidal-field-power-supply`→`system`，`thyristor-converter`/`switching-network`/`energy-dump`→`device`，`weight-window-generator`→`code`）；无法对照时按语义判定。
    - domain 标签**必须保留**（追加进 `notes`，格式 `[domain: <label>]`），`source` 统一 `corpus`。
  - 记录：`.github/plans/t4973-batches/category-map-sixcol80.tsv`（`concept_id␉domain␉category␉依据`）。
  - 同时生成 4 个批次 id 清单（供 T0.6a/T0.6b/T0.7a/T0.7b 使用，保证下游零推断）：
    - `.github/plans/t4973-batches/t0_6a.ids`（80 行前 40 个 id）、`t0_6b.ids`（后 40 个 id）
    - `.github/plans/t4973-batches/t0_7a.ids`（48 个 `指“en”` 损坏 id 的前 24）、`t0_7b.ids`（后 24）
    - 生成方式：`.venv/bin/python scripts/registry_row_audit.py --json /tmp/audit.json` 输出的 80/48 个 id 列表按行序切分，**顺序即唯一权威**。
- **修改边界**：只改这 80 行；不得改动其它行；不得删除 domain 标签信息。
- **质量检查方式**：修复后 `sixcol_rows=0`；每行断言 `$2 ∈ 16 类`、`$6 == active`、`$8 == corpus`、`notes` 含 `[domain: `。
- **验收标准**：
  - ✅ [结构归零] `[T-A]` `.venv/bin/python scripts/registry_row_audit.py --audit` → exit 0 且 `sixcol_rows=0 && malformed_cols=0`
  - ✅ [取值合规] `[T-B]` `assert all(r["category"] in CANON16 and r["status"] == "active" and r["source"] == "corpus" for r in sixcol_rows)`
  - ✅ [domain 保留] `[T-A]` `grep -c "\[domain: " terms/registry/concepts.tsv` → `80`
  - ✅ [ids 清单就位] `[T-A]` `wc -l .github/plans/t4973-batches/t0_6{a,b}.ids .github/plans/t4973-batches/t0_7{a,b}.ids` → `40 40 24 24`（exit 0）
  - ✅ [门禁不退化] `[T-A]` `.venv/bin/python -m pipeline.validate_registry` → exit 0
- **能失败证明（变异法）**：删除任一行的 `[domain: ` 注记 → 上一条 `grep -c` 变 79 而 FAIL。
- **潜在风险**：`preferred_zh` 暂空会让这些行在下游导出中缺中文（`query_expansions.category` 为空）；此为**临时态**，T0.6 完成后消失，期间不得重跑导出链（导出链统一在 T0.12）。
- **预留歧义标注**：
  - [ ] 无歧义

#### Task T0.6a: 起草 80 个中文首选名（前半 40 行）

- **目标**：为 6 列块的 80 个 concept 补齐 `preferred_zh`（用户裁决：并入本批次；放在 W0 以解 T0.7 的依赖环）。
- **依赖**：T0.5
- **frontier**：是（与 T0.6b 分批不冲突）
- **执行者**：Academic Writer（术语命名）/ Simulation Builder 辅助落表
- **预估墙钟**：30 min
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：为 `w1_c` 补集无关的 **40** 个 id 填 `preferred_zh`（本批 id 清单 = `.github/plans/t4973-batches/t0_6a.ids`，由 T0.5 记录的 80 行按行号前 40 生成）。
  - 命名依据（**必须可核验**）：① 该 concept 若已有真实 zh 释义（48 行块外的 32 行）→ 直接取释义中的术语名；② 否则取权威来源（`artifacts/terminology_sources/*.tsv` 仓内词条，或 Wikipedia/ITER/IAEA URL）；依据 URL 写入 `terms/registry/evidence.tsv`（`concept_id␉<url>␉␉copilot␉<today>`）。
- **修改边界**：只填 `preferred_zh` 与新增 evidence 行；不得改 `preferred_en`/`category`；不得动其它行。
- **质量检查方式**：名字不得是英文字面串；不得与既有 zh 别名冲突（`grep -P '^<name>\t' terms/registry/aliases.tsv` 先查）。
- **验收标准**：
  - ✅ [命名合规] `[T-A]` `.venv/bin/python scripts/registry_batch_verify.py --mode names --ids-file .github/plans/t4973-batches/t0_6a.ids --expect 40` → exit 0
  - ✅ [出处可核验] `[T-A]` 同上加 `--check-urls`（或 `--no-net` 时全部依据为仓内出处）→ exit 0
  - ✅ [门禁不退化] `[T-A]` `.venv/bin/python -m pipeline.validate_registry` → exit 0
- **能失败证明（反例锚定）**：把任一行的 `preferred_zh` 改成 `en` → `--mode names` 必须 exit 1。
- **潜在风险**：40 行/30 min 偏紧 → 允许拆为 20+20 并同步更新 README 批号（须在计划 Execution Log 记录）。
- **预留歧义标注**：
  - [ ] 无歧义

#### Task T0.6b: 起草 80 个中文首选名（后半 40 行）

- **目标**：同 T0.6a，覆盖剩余 40 个 id。
- **依赖**：T0.5、T0.6a（仅顺序，无产物依赖）
- **frontier**：否（避免同文件并发写）
- **执行者**：Academic Writer
- **预估墙钟**：30 min
- **修改内容**：文件 `terms/registry/concepts.tsv`（补后 40 行 `preferred_zh`）+ `terms/registry/evidence.tsv`（对应出处）。
- **修改边界**：同 T0.6a。
- **质量检查方式**：同 T0.6a。
- **验收标准**：
  - ✅ `.venv/bin/python scripts/registry_batch_verify.py --mode names --ids-file .github/plans/t4973-batches/t0_6b.ids --expect 40` → exit 0
  - ✅ [80 行全满] `[T-A]` `.venv/bin/python scripts/registry_row_audit.py --audit` → `sixcol_preferred_zh_empty=0`（audit 需含该字段，T0.1 中定义）
- **能失败证明**：同 T0.6a。
- **潜在风险**：与 T0.6a 撞车 → 严格串行（frontier=否）。
- **预留歧义标注**：
  - [ ] 无歧义

#### Task T0.7a: 修复 48 条 `指“en”` 损坏 zh 释义（前 24 条）

- **目标**：把 48 条把语言标签当术语名的 zh 释义重写为真实释义（**W0 范围**，属根因修复）。
  > **口径更新（D2-7=A，2026-10-26）**：本条原文"W1 只负责 en 行"的前提**已作废** —— W1 依 D2-7=A **en/zh 双侧同时重写**。相位分工仍清晰：**W0 修的是"损坏"**（48 条字面 `指“en”`，语言标签被当术语名，已清零）；**W1 面对的是"低信息模板"**（`指“X”` / `对应英文“X”`），其中落在 `w1_a∪w1_b∪w1_c` 内的 **631 行** `指“X”` 由 D2-7=A 纳入本批（其余 **886 行**仍属 D2-3 延后）。两者不重叠、不重复研究。
- **依赖**：T0.6a/T0.6b（需要中文名）
- **frontier**：是
- **执行者**：Academic Writer
- **预估墙钟**：25 min
- **修改内容**：
  - 文件 `terms/registry/definitions.tsv`：改写 24 条 `zh` 行（id 清单 = `.github/plans/t4973-batches/t0_7a.ids`，取自 T0.1 输出的 48 个损坏 id 前半），格式 `concept_id␉zh␉<中文释义>␉<source>`；`source` ∈ {`http(s)://…`, `GB/T-4960.9`, `ITER-glossary`, `IAEA-safety-glossary`}，**禁止** `internal:dict-improvements`（该 tag 正是缺陷来源的标记）。
  - 必要时同步补 `terms/registry/evidence.tsv` 出处行。
- **修改边界**：只改这 24 条 zh 行；不得改任何 en 行（en 行属 W1）；不得改其它 concept 的行。
- **质量检查方式**：释义不得再含 `指“en”`；释义中出现的术语名须 == 该 concept 的 `preferred_zh`。
- **验收标准**：
  - ✅ [损坏归零（本批）] `[T-A]` `.venv/bin/python scripts/registry_batch_verify.py --mode definitions --ids-file .github/plans/t4973-batches/t0_7a.ids --expect 24 --lang zh` → exit 0
  - ✅ [模板黑名单] `[T-A]` `grep -P '\tzh\t.*指“en”' terms/registry/definitions.tsv | wc -l` → 本批后 ≤ 24
  - ✅ [门禁不退化] `[T-A]` `.venv/bin/python -m pipeline.validate_registry` → exit 0
- **能失败证明（反例锚定）**：保留一条未修的 `指“en”` 行在 ids 文件内 → 该命令必须 exit 1。
- **潜在风险**：24 条外部出处抓取耗时 → 允许以仓内 `GB/T-4960.9`/`ITER-glossary` 出处优先（这些 concept 多为电气/计算方法类，ITER 词条覆盖有限，须留足抓取时间）。
- **预留歧义标注**：
  - [ ] 无歧义

#### Task T0.7b: 修复剩余 24 条 `指“en”` 损坏 zh 释义

- **目标**：同 T0.7a，覆盖后 24 条。
- **依赖**：T0.6b、T0.7a
- **frontier**：否
- **执行者**：Academic Writer
- **预估墙钟**：25 min
- **修改内容**：文件 `terms/registry/definitions.tsv`（后 24 条 zh 行）+ 必要时 `terms/registry/evidence.tsv`。
- **修改边界**：同 T0.7a。
- **质量检查方式**：同 T0.7a。
- **验收标准**：
  - ✅ `.venv/bin/python scripts/registry_batch_verify.py --mode definitions --ids-file .github/plans/t4973-batches/t0_7b.ids --expect 24 --lang zh` → exit 0
  - ✅ [全量归零] `[T-A]` `grep -cP '\tzh\t.*指“en”' terms/registry/definitions.tsv` → `0`（grep 无匹配时 exit 1 属正常，断言计数值为 0）
- **能失败证明**：同 T0.7a。
- **潜在风险**：`grep -c` 返回码语义（无匹配 = 1）→ 验收脚本以计数而非 exit code 判定。
- **预留歧义标注**：
  - [ ] 无歧义

#### Task T0.8: `evidence.tsv` 列数与来源规范化

- **目标**：`evidence.tsv` 全表 5 列；`internal:dict-improvements:<domain>` 的 domain 后缀移入 `quote`（保留信息、恢复约定 tag）。
- **依赖**：T0.1、T0.2
- **frontier**：是
- **执行者**：Simulation Builder
- **预估墙钟**：25 min
- **修改内容**：
  - 文件 `terms/registry/evidence.tsv`：
    - 213 行 4 列（`cid␉source␉<added_by>␉<added_at>`）→ 补齐**空 `quote`**：`cid␉source␉␉<added_by>␉<added_at>`；
    - 2 行 2 列（`cid␉source`）→ 补齐为空 `quote`/空 `added_by` + `added_at`（`cfetr-design` 已有 DOI source；`mitigation` 的 `internal:domain-convention-zh-mitigation` 原样保留在 `source`）；
    - 427 行 `internal:dict-improvements:<domain>` → `source` 改回 `internal:dict-improvements`，`<domain>` 原文移入 `quote`，格式 `domain: <domain>`。
- **修改边界**：不得删除任何行；不得改动不属于上述三类的问题行；不得改 concept_id。
- **质量检查方式**：改后 `non5_cols=0`；`grep -c "internal:dict-improvements:"` == 0；行数仍为 3168。
- **验收标准**：
  - ✅ [列数归零] `[T-A]` `.venv/bin/python scripts/registry_row_audit.py --audit` → `non5_cols=0`（exit 0）
  - ✅ [后缀归零] `[T-A]` `grep -c "internal:dict-improvements:" terms/registry/evidence.tsv` → `0`（计数值为 0）
  - ✅ [行数不变] `[T-A]` `.venv/bin/python scripts/registry_row_audit.py --audit` → **`evidence.data_rows == 3168`**（口径：audit 数据行数；`evidence.tsv` **文件** `wc -l` 恒为 **3217**，含 47 空行 + 2 注释行，修复前后均如此 —— 不得用文件 `wc -l` 断言 3168）
  - ✅ [门禁不退化] `[T-A]` `.venv/bin/python -m pipeline.validate_registry` → exit 0
- **能失败证明（变异法）**：把一行改回 4 列 → `non5_cols` 必须变 1。
- **潜在风险**：`quote` 字段被下游消费者误读为引用原文 → 本仓库 `quote` 现状多为空，语义为备注位；在 CHANGELOG 说明（T0.13）。
- **预留歧义标注**：
  - [ ] 无歧义

#### Task T0.9: 加严 `pipeline/validate_registry.py` 门禁

- **目标**：让 179 行畸形**无法再静默通过**，且规则可机械判定（concepts 精确 8 列 + `category` 白名单；evidence 精确 5 列）。
- **依赖**：T0.4、T0.5、T0.8（**必须先修数据**，否则 CI 立即红，违反 RK2）
- **frontier**：否
- **执行者**：Simulation Builder / Dev Orchestrator
- **预估墙钟**：30 min
- **修改内容**：
  - 文件 `pipeline/validate_registry.py`：
    - 新增模块级常量 `_ALLOWED_CATEGORIES`（16 类，与 §数据基线 A3 的枚举一致）；
    - concepts 校验：`len(r.fields) != 8` → `_fail(..., "expected 8 columns: concept_id, category, preferred_zh, preferred_en, preferred_abbr, status, notes, source")`；`r.fields[1] not in _ALLOWED_CATEGORIES` → `_fail(..., f"invalid category {r.fields[1]!r}")`；
    - evidence 校验：`len(r.fields) != 5` → `_fail(..., "expected 5 columns: concept_id, source, quote, added_by, added_at")`；
    - 保留既有 `internal:TODO` 与 URL 校验不变。
- **修改边界**：不得改 `pipeline/export_registry.py` 的解析语义；不得改 aliases/definitions 既有规则；不得放宽任何现有检查。
  > **⚠️ 实际范围以 §Execution Log（commit `08a2e98`）记的偏差为准（用户已追认，见《W0 收尾裁决与追认》追认 1）**：本条原声明"只改 `pipeline/validate_registry.py`"；实际落地时**同一 commit 另含** 8 个测试文件的合成 fixture 机械补 tab 改动（无逻辑/断言改动）与 1 行陈旧 fixture 的 `category` 修正（`component` → `concept`，真实语料 `central-solenoid` 实为 `concept`）。理由是本任务验收要求全仓 `pytest` exit 0 且 RK2 禁止红 CI。**本条不构成对 `pipeline/validate_registry.py` 声明以外的写入授权**；后续相位仍按原边界执行。
- **质量检查方式**：`mypy pipeline/ --ignore-missing-imports` 0 错；本地全量门禁 G1–G5 全绿。
- **验收标准**：
  - ✅ [GREEN：真实数据通过] `[T-A]` `.venv/bin/python -m pipeline.validate_registry` → exit 0，输出 `registry OK: 3076 concepts, …`
  - ✅ [RED：畸形语料必须失败] `[T-A]` 用 `tests/fixtures/registry/pre_fix_concepts_shift.tsv`（T0.10 产出）构造临时 terms 目录 → validator **exit ≠ 0** 且 stderr 含 `invalid category`
  - ✅ [RED：6 列行必须失败] `[T-A]` 同上用 `pre_fix_concepts_sixcol.tsv` → **exit ≠ 0** 且 stderr 含 `expected 8 columns`
  - ✅ [类型门禁] `[T-A]` `.venv/bin/mypy pipeline/ --ignore-missing-imports` → exit 0
- **能失败证明（实现回退法）**：临时把 `_ALLOWED_CATEGORIES` 或列数断言注释掉 → RED 用例必须转为 PASS（说明 RED 断言确实由新规则驱动，而非其它原因失败）。
- **潜在风险**：现有测试 fixture 用 ≤4 列 evidence（`tests/test_registry_validator.py:270` `_MINIMAL_EVIDENCE`）→ 会在 T0.10 前造成 pytest 红；**因此 T0.9 与 T0.10 必须同一 commit**（见 T0.10）。
- **预留歧义标注**：
  - [ ] 无歧义

#### Task T0.10: 更新 validator 测试 fixture + 真实语料锚定用例

- **目标**：门禁加严后 pytest 全绿，且 RED 用例**锚定真实畸形行**（不得自造畸形样本）。
- **依赖**：T0.9（同一 commit）
- **frontier**：否
- **执行者**：Simulation Builder
- **预估墙钟**：30 min
- **修改内容**：
  - 新增 fixture 文件（内容取自真实历史语料，逐字节保留）：
    - `/home/gw/opt/fusion-terms/tests/fixtures/registry/pre_fix_concepts_shift.tsv` ← `git show f90e903:terms/registry/concepts.tsv | sed -n '3171,3173p'`
    - `/home/gw/opt/fusion-terms/tests/fixtures/registry/pre_fix_concepts_sixcol.tsv` ← `git show f90e903:terms/registry/concepts.tsv | sed -n '3316,3318p'`
  - 修改 `tests/test_registry_validator.py`：更新 `_MINIMAL_EVIDENCE` 为 5 列；新增 `test_validate_registry_rejects_shifted_category_row`、`test_validate_registry_rejects_six_column_row`、`test_validate_registry_rejects_four_column_evidence`；每个用例从上述 fixture **按行读取真实文本**（用 `Path(...).read_text().splitlines()`，不得手写复制），并断言 stderr 含特定消息。
- **修改边界**：只改 `tests/test_registry_validator.py` 与新增 `tests/fixtures/registry/` 下 2 个 fixture；不得改其它测试文件。
  > **⚠️ 实际范围以 §Execution Log（commit `08a2e98`）记的偏差为准（用户已追认，见《W0 收尾裁决与追认》追认 1）**：实际另机械补 tab 修改 **8 个**测试文件的合成 fixture（无逻辑/断言改动），并把 1 行陈旧 fixture 的 `category` 由 `component` 改为 `concept`（真实语料 `central-solenoid` 实为 `concept`；`component` 不在 16 类白名单内，仅作为 `preferred_en` 出现）。**本条声明为计划期边界；实际已发生的扩展以 Execution Log 为准，不追溯放宽。**
- **质量检查方式**：`pytest -q tests/test_registry_validator.py -v` 全绿；新增用例能对 fixture 内容变化**响亮失败**（fixture 被删/被改则用例 error）。
- **验收标准**：
  - ✅ [全绿] `[T-A]` `.venv/bin/python -m pytest -q tests/test_registry_validator.py` → exit 0
  - ✅ [全仓测试] `[T-A]` `.venv/bin/python -m pytest -q` → exit 0（G1）
  - ✅ [用例数与锚定] `[T-A]` `.venv/bin/python -m pytest -q tests/test_registry_validator.py --collect-only | tail -1` → 用例数 ≥ 15；且 `grep -c "pre_fix_concepts" tests/test_registry_validator.py` ≥ 2
  - ✅ [格式门禁] `[T-A]` `.venv/bin/ruff format --check . && .venv/bin/ruff check .` → exit 0
- **能失败证明（实现回退法）**：把 fixture 文件临时改名 → 新用例必须 error（证明用例真的在读真实语料，而不是内联字符串）。
- **潜在风险**：`ruff format` 可能重排测试文件 → 先 `ruff format` 再 `ruff format --check`。
- **预留歧义标注**：
  - [ ] 无歧义

#### Task T0.11: RED/GREEN 证据录制（门禁"能失败"的可审计证明）

- **目标**：把 T0.9/T0.10 的 RED→GREEN 全过程落成可复跑记录。
- **依赖**：T0.10
- **frontier**：是
- **执行者**：Simulation Builder
- **预估墙钟**：20 min
- **修改内容**：
  - 新增文件 `/home/gw/opt/fusion-terms/.github/plans/t4973-batches/red-green.md`：记录 ① 命令原文；② 修复前 `--expect-clean` 的 exit 1 输出；③ 修复后 exit 0 输出；④ RED 用例（真实语料）在加严前后 exit 码对比表；⑤ fixture 与 `git show f90e903:…` 的行号对应关系。
- **修改边界**：只新增该 md 文件；不得改数据文件。
- **质量检查方式**：记录中的命令可由第三方逐条复跑。
- **验收标准**：
  - ✅ [记录完整] `[T-A]` `grep -c "exit" .github/plans/t4973-batches/red-green.md` ≥ 6
  - ✅ [可复跑性] `[T-A]` `.venv/bin/python scripts/registry_row_audit.py --expect-clean` → exit 0（修复后）
  - ✅ [RED 复现] `[T-A]` `git stash list >/dev/null; git show f90e903:terms/registry/concepts.tsv | sed -n '3316p' | awk -F'\t' '{print NF}'` → `6`（证明 RED 语料真实）
- **能失败证明（反例锚定）**：若 RED 语料行数变为 8，本任务判定 FAIL 并回溯 fixture 来源。
- **潜在风险**：无。
- **预留歧义标注**：
  - [ ] 无歧义

#### Task T0.12: 重跑导出链并断言污点归零

- **目标**：消除 `translation_dict.json`（166 条 `'en'`）、`query_expansions.json`（99 个中文 category）、`tag_rules.jsonl`（720 行非规范 category）三处污染。
- **依赖**：T0.4、T0.5、T0.6a、T0.6b、T0.7a、T0.7b、T0.8
- **frontier**：否
- **执行者**：Simulation Builder
- **预估墙钟**：25 min
- **修改内容**：
  - 运行（命令串固定，顺序不可换）：
    1. `.venv/bin/python -m pipeline.export_registry --translation-dict --query-expansions --substitutions --tag-rules`
    2. `.venv/bin/python -m pipeline.build_terms --config config.toml`
  - 产物：`artifacts/translation_dict.json`（git tracked，须提交）、`artifacts/query_expansions.json`、`artifacts/tag_rules.jsonl`、`artifacts/terminology_substitutions.tsv`、`artifacts/domain_terms.txt`、`artifacts/domain_terms_build_stats.json`。
- **修改边界**：不手改 `artifacts/` 下任何文件（只由管线生成）；不改 `terms/`；不改 `pipeline/`。
- **质量检查方式**：
  - 三项污点断言（下表）；`domain_terms.txt` 行数变化须能被 `terms/` 数据解释（W0 不增删 allowlist，故应恒为 3462）。
- **验收标准**：
  - ✅ [污点 1 归零] `[T-A]` `python3 -c "import json;d=json.load(open('artifacts/translation_dict.json'));print(sum(1 for v in d['en2zh'].values() if v=='en'))"` → `0`
  - ✅ [污点 2 归零] `[T-A]` `python3 -c "import json;d=json.load(open('artifacts/query_expansions.json'));print(sum(1 for c in d['concepts'].values() if not c['category'].isascii()))"` → `0`
  - ✅ [污点 3 归零] `[T-B]` 断言 `tag_rules.jsonl` 中 `category ∉ 16 类` 的行数 == 0
  - ✅ [IME 词表不变] `[T-A]` `wc -l artifacts/domain_terms.txt` → `3462`
  - ✅ [门禁不退化] `[T-A]` `.venv/bin/python -m pytest -q && .venv/bin/python -m pipeline.validate_registry` → exit 0
- **能失败证明（变异法）**：临时把一行 `concepts.tsv` 的 `preferred_zh` 改成 `en` 后重跑导出 → 污点 1 断言必须变 ≥1。
- **潜在风险**：`translation_dict.json` diff 很大（3825 条）→ 属正常；提交时只说明指标变化（166→0、249→?）。
- **预留歧义标注**：
  - [ ] 无歧义

#### Task T0.13: W0 收尾（CHANGELOG + 计划 Execution Log + commit）

- **目标**：W0 成果可追溯；Phase 0 完成定义可判定。
- **依赖**：T0.11、T0.12
- **frontier**：否
- **执行者**：Dev Orchestrator
- **预估墙钟**：20 min
- **修改内容**：
  - 文件 `CHANGELOG.md`：新增 W0 条目（数据修复 179 行、48 条 zh 释义、evidence 规范化 **429 行**、门禁加严、三项污点归零）。
    > **口径**：`evidence.tsv` 规范化行数原文写「642 行」为**误计**，实测 **429 行**（`git diff --numstat 1e2cf30^ 1e2cf30` = `429 429`），以 §Execution Log「W0 收口数字」为准。
  - 文件 `.github/plans/terminology-coverage-and-definition-quality.md`：在 `## Execution Log` 追加 W0 记录（每条含命令与实测输出）。
  - commit（message 带 `#T-4973`），**一次 commit 只含本节声明的文件**。
- **修改边界**：不得夹带未声明文件；`git diff --stat` 必须只含 `CHANGELOG.md`、计划文件、`terms/registry/*.tsv`、`pipeline/validate_registry.py`、`tests/test_registry_validator.py`、`tests/fixtures/registry/*`、`scripts/registry_*.py`、`artifacts/translation_dict.json`。
- **质量检查方式**：`git diff --stat` 与声明清单逐项比对。
- **验收标准**：
  - ✅ [提交范围] `[T-A]` `git show --stat HEAD | tail -20` 只含声明文件
  - ✅ [Phase 0 完成定义] `[T-A]` `.venv/bin/python scripts/registry_row_audit.py --audit --expect-clean` → exit 0
  - ✅ [全量门禁] `[T-A]` `.venv/bin/python -m pytest -q && .venv/bin/ruff format --check . && .venv/bin/ruff check . && .venv/bin/mypy pipeline/ --ignore-missing-imports && .venv/bin/python -m pipeline.validate_registry` → 全部 exit 0
- **能失败证明（实现回退法）**：故意保留 1 行 6 列 concept → `--expect-clean` exit 1，T0.13 不得标记完成。
- **潜在风险**：commit message 若含 `fix` 关键词不会触发 PM 完成语义（按仓库约定 `fix` 不是完成词）→ 本条为 W0 中间提交，使用 `feat(registry): … #T-4973`。
- **预留歧义标注**：
  - [ ] 无歧义

### Phase 1: W1 — definitions 质量重写（用户裁决：全部重写）

**范围清算（与任务书口径的对账；W0 后权威值）**

| 组 | 内容 | 概念数 | 双侧行数 | 依据 |
|----|------|-------|---------|------|
| W1-A | 746 行 en 套话中**已有真实 zh 释义**（源 `GB/T-4960.9`）的 67 个 concept → en 释义由仓内 zh 释义改写；zh 侧同步合规化 | 67 | 134（en 67 + zh 67） | §E6 + README |
| W1-B | 746 行 en 套话中**仅有 zh 模板**的 679 个 concept → 释义依据按 **D2-8=A** 可为仓内 `corpus` | 679 | 1358（en 679 + zh 679） | §E6 + README |
| W1-C | 10 个**完全无 definitions** 的 concept → 新增 en+zh 各 10 行 | 10 | 20（新增） | §E5 |
| 小计 | **756 concept / ≈1512 行**（en 746 + zh 746 + W1-C 新增 20） | **756** | **1512** | W1-A+B+C |
| 其中 zh 侧必改 | 本批 zh 行中匹配 `聚变/核工程术语` 模板者（**D2-7=A 纳入本批**） | — | **631** | improve 轮实测 |
| （非目标） | 剩余 zh 模板（131 `指“X”` + 755 `对应英文“X”`） | — | 886 | 见 §待裁决 D2-3 |

> **口径演进的账**（旧 → 新，供对账）：
> - 任务书"795 行（747 en + 48 zh）" → 首次 refine 记为 **766 行**（746 en + 20 新增），48 zh 归 W0；差值 1 行 = §R-4（746 vs 747）。
> - **本 improve 轮按 D2-7=A 更正为 ≈1512 行**：W1 每批 en/zh 双侧同时重写（en 746 + zh 746 + W1-C 新增 20）。**批数不变**（仍 README 的 4/34/1 = 39 批），但**每批墙钟**由"仅 en"上升到"双侧"，故按粒度门把每批拆为 `-EN` / `-ZH` 两个 ≤30 min 子任务（见下表）。
> - `w1_b` 的 679 行来源要求**已收窄**（D2-8=A）：以该 concept 的 registry `notes` / 既有 zh 释义为依据时记为 `corpus`，**不再强制**逐条外部出处。

**批次任务统一规格（D2-7=A：每批拆为 `-EN` / `-ZH` 两个 ≤30 min 子任务）**

- **目标**：为该批 concept 的 `definitions.tsv` 行写出**真实、带可核验出处**的释义；**en 侧与 zh 侧均须合规**（D2-7=A）。
- **依赖**：Phase 0 全部完成（T0.13 已 DONE）；同批内 `-ZH` 子任务依赖同批 `-EN` 子任务完成（zh 释义需与 en 释义语义一致）；跨批无依赖（但见下 frontier 说明）。
- **frontier**：**否**（`definitions.tsv` 为**同一文件** → 实际执行必须串行；同 wave 内即使 id 集合不相交也不得并发写同一文件）。
- **执行者**：Academic Writer（技术释义）；Simulation Builder 负责落表与批验收。
- **修改内容**：
  - `-EN` 子任务：文件 `terms/registry/definitions.tsv` —— **定点替换**该批全部 id 的 `en` 行。
  - `-ZH` 子任务：同文件 —— **定点重写**该批全部 id 的 `zh` 行（含 `指“X”` 模板行）；W1-C 的 10 个 id 另**新增** en/zh 各 1 行。
  - 仅在释义**显式引用外部权威**时，追加 `terms/registry/evidence.tsv` 出处行。
- **修改边界**：
  - 不得修改非本批 concept 的任何行；不得改 `preferred_zh`/`preferred_en`/`category`。
  - **禁止** `internal:dict-improvements`、`internal:TODO` 作为新释义出处。
  - 不得改动 `terms/registry/concepts.tsv`。
  - **来源口径（D2-8=A，收窄）**：`source` ∈ {`corpus`, `GB/T-4960.9`, `ITER-glossary`, `IAEA-safety-glossary`, `http(s)://…`}；以该 concept 的 registry `notes` / 既有 zh 释义为依据时标 **`corpus`** 即可，**不要求** URL；**仅当释义显式引用外部权威时**才要求可 200 的 URL 或 `GB/T`/`ITER`/`IAEA`。
- **质量检查方式**：批验收脚本（机械）+ 抽检（D2-4）。
- **验收标准（每批同构；`-EN` 子任务跑前 3 条，`-ZH` 子任务跑 4~6 条）**：
  - ✅ [EN 侧合规] `[T-A]` `.venv/bin/python scripts/registry_batch_verify.py --mode definitions --ids-file .github/plans/t4973-batches/<batch>.ids --expect <N> --lang en` → **exit 0**（**不默认加** `--check-urls`；仅当本批存在 http 来源时追加，无网环境加 `--no-net` 并在批记录标 `[NO-NET]`）
  - ✅ [套话黑名单] `[T-B]` `assert 本批 en 行无一匹配 ^Fusion/nuclear engineering term referring to '.*' in technical context\.$`
  - ✅ [门禁不退化] `[T-A]` `.venv/bin/python -m pipeline.validate_registry` → **exit 0**
  - ✅ [ZH 侧合规] `[T-A]` `.venv/bin/python scripts/registry_batch_verify.py --mode definitions --ids-file .github/plans/t4973-batches/<batch>.ids --expect <N> --lang zh` → **exit 0**
  - ✅ [zh 模板黑名单] `[T-B]` `assert 本批 zh 行无一含 聚变/核工程术语 标记`
  - ✅ [**批收口：双侧同时合规**] `[T-A]` `.venv/bin/python scripts/registry_batch_verify.py --mode definitions --ids-file .github/plans/t4973-batches/<batch>.ids --expect <N>`（默认 `--lang both`）→ **exit 0**；`.venv/bin/python -m pytest -q` → **exit 0**
- **能失败证明（反例锚定）**：任取一批，把 1 行新释义改回套话（en）或改回 `指“X”` 模板（zh）→ 对应侧批验收必须 exit 1，且**批收口（`--lang both`）必须 exit 1**。

| Task | 组 | ids 文件 | ids 数 | 预估墙钟 | 修改文件 |
|------|----|---------|-------|---------|---------|
| T1.A1-EN … T1.A4-EN（4 个） | W1-A 仓内可推导 | `w1_a_b01.ids`…`w1_a_b04.ids` | 20 / 20 / 20 / 7 | 各 25 min | `terms/registry/definitions.tsv` |
| T1.A1-ZH … T1.A4-ZH（4 个） | W1-A | 同上（与 `-EN` 同批同文件） | 同上 | 各 20 min | 同上 |
| T1.B01-EN … T1.B34-EN（34 个） | W1-B | `w1_b_b01.ids`…`w1_b_b34.ids` | 20×33 / 19（尾批） | 各 25 min | `definitions.tsv`（+`evidence.tsv` 仅当显式引用外部权威） |
| T1.B01-ZH … T1.B34-ZH（34 个） | W1-B | 同上 | 同上 | 各 20 min | 同上 |
| T1.C1-EN | W1-C 无 definitions | `w1_c.ids` | 10 | 20 min | `definitions.tsv`（新增 en 10 行）+ `evidence.tsv` |
| T1.C1-ZH | W1-C | `w1_c.ids` | 10 | 20 min | `definitions.tsv`（新增 zh 10 行） |
| **小计** | — | — | — | **78 个 Task / 1755 min（≈29.3 h）** | — |

> **展开规则（消除下游猜测，逐字可执行）**：
> - 序号↔文件一一对应：`T1.A<i>-{EN,ZH}` ↔ `.github/plans/t4973-batches/w1_a_b0<i>.ids`（i=1..4）；`T1.B<nn>-{EN,ZH}` ↔ `w1_b_b<nn>.ids`（nn=01..34，两位零填充）；`T1.C1-{EN,ZH}` ↔ `w1_c.ids`。
> - `<N>` = 该 ids 文件行数（`wc -l` 实测：`w1_a` = 20/20/20/7；`w1_b` = 20×33 与尾批 19；`w1_c` = 10）。**批数与每批大小以 `.github/plans/t4973-batches/README.md` 为唯一权威**（合计 119 批 / 2348 ids）。
> - `-EN` 子任务只改该批 id 的 `en` 行；`-ZH` 只改该批 id 的 `zh` 行；**批收口（`--lang both` 双侧同时合规）并入 `-ZH` 子任务的最后两条验收**。
> - 拆分理由（粒度门）：D2-7=A 后每批实际改动 ≈ id 数 × 2 行（W1 合计 ≈1512 行），单任务墙钟 >30 min ⇒ 按 §Step 0a-2 拆为两个 ≤30 min 子任务，**验收标准不变**（批收口仍要求双侧同时合规）。尾批（7/19/10 id）估值偏保守，不另拆分。
> - **串行纪律**：`definitions.tsv` 单文件 ⇒ 同批 `-EN`→`-ZH` 串行，跨批亦串行（frontier 均为否）。

**Phase 1 完成定义（一条命令；`--expect-clean-all` = 全集闸门）**：

- ✅ `[T-A]` `.venv/bin/python scripts/registry_row_audit.py --audit --expect-clean-all` → exit 0（`en_boilerplate=0 && concepts_without_defs=0`，且 W0 结构集仍为 0）
- ✅ `[T-A]` **本批 zh 模板清零**（D2-7=A 的交付闸门；当前实测 631 行模板）：
  ```bash
  python3 -c "import csv;ids={l.strip() for f in ['w1_a','w1_b','w1_c'] for l in open(f'.github/plans/t4973-batches/{f}.ids') if l.strip()};rows=[r for r in csv.reader(open('terms/registry/definitions.tsv',encoding='utf-8'),delimiter='\t') if r and len(r)>2 and r[0] in ids];print(sum(1 for r in rows if r[1]=='zh' and '聚变/核工程术语' in r[2]))"
  # 期望：0（W1 收尾时必须为 0；非 0 ⇒ 本 Phase 未完成）
  ```
- ✅ `[T-A]` `.venv/bin/python -m pipeline.validate_registry` → exit 0，且输出 `… 6132 + 20 = 6152 definitions`
- ✅ `[T-A]` `.venv/bin/python -m pytest -q` → exit 0

**逐 Task 验收命令展开规则（消除下游猜测；上表每一行条目按展开规则生成具体 Task）**：把统一规格中的 `<batch>` 换为该子任务的 `ids 文件` 名、`<N>` 换为该文件的 `wc -l`。**worked example（T1.B01-EN / T1.B01-ZH）**：

```bash
# T1.B01-EN：改 en 行，EN 侧闸门
.venv/bin/python scripts/registry_batch_verify.py --mode definitions \
  --ids-file .github/plans/t4973-batches/w1_b_b01.ids --expect 20 --lang en
# T1.B01-ZH：改 zh 行，ZH 侧闸门
.venv/bin/python scripts/registry_batch_verify.py --mode definitions \
  --ids-file .github/plans/t4973-batches/w1_b_b01.ids --expect 20 --lang zh
# 批收口（并入 T1.B01-ZH 验收）：双侧同时合规
.venv/bin/python scripts/registry_batch_verify.py --mode definitions \
  --ids-file .github/plans/t4973-batches/w1_b_b01.ids --expect 20   # 默认 --lang both
# 三条均期望 exit 0。出处按 D2-8=A：仓内依据标 corpus 即可；仅当显式引用外部权威时加 --check-urls
# （无网环境：--check-urls --no-net，并在批记录标 [NO-NET]）
```

**批次提交纪律**：每个子任务单独 commit（`-EN`、`-ZH` 各一次），message 形如 `feat(registry): rewrite definitions W1-B-01 en (#T-4973)` / `… zh (#T-4973)`；`git diff --stat` 只含 `terms/registry/definitions.tsv`（显式引用外部权威时才 +`evidence.tsv`）。

**Phase 1 说明（抽检，落实 D2-4）**：每完成 5 个**批**（即 10 个子任务；批序 ~~B05/B10/B15/B20/B25/B30/C1~~ **该列已废弃** —— 未计入 `w1_a` 的 4 批，整体偏移 4 批；**定稿 cadence**：首组 `A1–A4 + B01` 已 PASS，后续 `B02–B06`、`B07–B11`、`B12–B16`、`B17–B21`、`B22–B26`、`B27–B31`、`B32–B34 + C1`，见 §「会话恢复 — Bookkeeping 纠正」第 3 条）执行一次抽检：
`.venv/bin/python scripts/registry_batch_verify.py --mode definitions --ids-file <最近 5 批的 ids 文件并集> --expect <并集行数> --lang both` → exit 0，另取 **≥8 行**产出摘要交独立 agent 复核语义（zh 侧须与 en 侧同义、且与该 concept 的 `preferred_zh` 一致）；复核 FAIL > 0 → 该 5 批返工（不得只改被抽中的行）。

### Phase 2: W2 — allowlist 机械补齐（738 行，排除 35 专名）

> 依据 §D2（**W0 后权威值**）：`preferred_zh` 非空且非专名的未覆盖行 **738** 条；其中 **668** 条 `preferred_en` 含空格（→ 入 `allowlist_en.txt` 时必须用**连字符 token**，禁止空白，见 RK5），**70** 条单词形（其中通用英文词清单见 §待裁决 D2-2；`system`/`mode` 已在 `denylist.txt`，写入无效）。W0 前为 584（527/57），**738 为权威值**。
> **批清单唯一权威** = `.github/plans/t4973-batches/README.md`（W0 后已重生成，commit `66197f2`）：`w2.ids` = **738** → **37 批**（20×36 + 18）。计划期旧值（584 行 / 10 批 / 每批 58~59）**已作废**。
> **⚠️ denylist 交互（README「执行批次时必须注意」第 1~2 条，实测）**：`W2_zh_in_denylist = 10`（`halo-current`/`line-radiation`/`system`/`calculation`/`material`/`simulation`/`mode`/`device`/`magnetic-moment`/`mode-number`）—— 这些 id 的中文名写入 `allowlist_zh.txt` 是**无效操作**（`build_terms` 先按 denylist 过滤）；`W2_denylist_en_conflicts = 2`（`system`/`mode`）。**须在批记录中单独标注，不得当成"漏写"**。

**批次任务统一规格**

- **目标**：把该批 concept 的 `preferred_zh` 追加进 `terms/allowlist_zh.txt`，把 EN token 追加进 `terms/allowlist_en.txt`。
- **依赖**：Phase 0 全部完成（W2 清单须基于**已修复**的 `concepts.tsv` 重算 —— T2.0）；T0.0/T0.2。
- **执行者**：Simulation Builder
- **修改内容**：文件 `terms/allowlist_zh.txt`、`terms/allowlist_en.txt`（**追加**，末尾带 `# --- T-4973 W2 batch NN ---` 节注释）。
- **修改边界**：不得删除/改写既有行；不得写含空白的 EN 项；不得写 `denylist.txt` 已有项；不得改 `terms/registry/`。
- **质量检查方式**：追加前 `grep -x` 冲突预检（allowlist 双表 + denylist + synonyms）。
- **验收标准（每批同构）**：
  - ✅ [批验收] `[T-A]` `.venv/bin/python scripts/registry_batch_verify.py --mode allowlist --ids-file .github/plans/t4973-batches/<ids> --expect <N>` → **exit 0**
  - ✅ [无空白 EN 项] `[T-A]` `grep -v '^#' terms/allowlist_en.txt | grep -c ' '` → `0`
  - ✅ [无重复] `[T-A]` `sort terms/allowlist_zh.txt | uniq -d | wc -l` → `0`
  - ✅ [IME 构建不炸] `[T-A]` `.venv/bin/python -m pipeline.build_terms --config config.toml` → **exit 0**
- **能失败证明（变异法）**：临时向 `allowlist_en.txt` 追加一行 `corrosion product`（含空白）→ `build_terms` 必须 `SystemExit` 非 0。
- **潜在风险**：批量 20 行/批（README 权威）；T2.0 须先把 denylist 冲突项（10 zh + 2 en）与 D2-1/D2-2 决策项标出，避免把它们计入"应写未写"。

| Task | ids 文件 | ids 数 | 预估墙钟 | 修改文件 |
|------|---------|-------|---------|---------|
| T2.0（预检+重算） | — | — | 20 min | `.github/plans/t4973-batches/w2-denylist-conflicts.tsv`（**只读复算，不改 ids 文件**：清单已由 commit `66197f2` 生成） |
| T2.1 … T2.36（36 个） | `w2_b01.ids` … `w2_b36.ids` | 各 20 | 各 25 min | `terms/allowlist_zh.txt`、`terms/allowlist_en.txt` |
| T2.37（尾批） | `w2_b37.ids` | 18 | 25 min | 同上 |
| T2.38 | 全量复算 | — | 25 min | `artifacts/domain_terms.txt`（重建）、`.github/plans/t4973-batches/coverage-after-w2.md` |
| **小计** | — | **738** | **39 个 Task / 985 min（≈16.4 h）** | — |

> **展开规则**：`T2.<nn>` ↔ `.github/plans/t4973-batches/w2_b<nn>.ids`（nn=01..37，两位零填充）；`<N>` = `wc -l` 实测（b01..b36 = 20，b37 = 18）。**批数以 README 为唯一权威**。
> **D2-1（8 个 code id，已裁决 A=入表）与 D2-2（36 个领域专指 + 8 code，通用词不入）** 的具体 id **分散在各批中**（非集中在前两批），批号须实测：
> ```bash
> for i in vmec desc simsopt cate pactole pactiter tract oscar; do \
>   echo -n "$i: "; grep -l -x "$i" .github/plans/t4973-batches/w2_b*.ids; done   # 定位 D2-1 的 8 个 code id 所在批
> ```
> D2-1/D2-2 **不是**整批开关：命中批内**其余 id 照常写入**，仅对决策项按裁决处置（D2-1 = 写代号形式；D2-2 = 通用词不写 EN 侧），并在批记录标注。
> **⚠️ 与 D2-6 的顺序耦合（Phase 3 的 W3b 集）**：W2 的 9 个 id 其 `preferred_zh` 目前是**拉丁串**（`vmec`/`desc`/`simsopt`/`c-2u`/`eu-demo`/`gamma-10`/`helion-trenta`/`k-demo`/`start-device`），而 D2-6=A 要求 W3b 为它们补中文首选名 ⇒ **对含这 9 个 id 的 W2 批次，须先完成 W3b 对它们的命名，再写 allowlist**（否则会写入随后作废的 zh 词条；若已先写，则须在 W3b 后重跑 T2.38 复算并清理）。定位命令：
> ```bash
> for i in vmec desc simsopt c-2u eu-demo gamma-10 helion-trenta k-demo start-device; do \
>   echo -n "$i: "; grep -l -x "$i" .github/plans/t4973-batches/w2_b*.ids; done
> ```

**T2.0 验收**：
- ✅ `[T-A]` `.venv/bin/python scripts/registry_coverage_report.py --json /tmp/cov-w2.json` → exit 0 且 **`W2=738`**（W0 后权威值；W2_multiword 668 / W2_single 70 / total 3076 / coverage_pct 47.11）；差值须能逐行解释。
- ✅ `[T-B]` 断言 `w2.ids` 与 `denylist.txt` 的 EN 侧交集 == `{"system","mode"}`（实测 `W2_denylist_en_conflicts = 2`），且 zh 侧冲突清单 == README 所列 **10** 个 id。

**T2.38 验收（全量复算）**：

- ✅ [覆盖率提升] `[T-A]` `.venv/bin/python scripts/registry_coverage_report.py` → `coverage_pct ≥ **70.0**`（新基线 47.11 + 738/3076 = 71.10 为理论上限；取 70.0 留 ~1.1 pp 给 denylist 过滤（10 个 zh 冲突 id 无法入表）与去重损耗。**该下限相对新基线为收紧换算，不构成门槛放宽**；旧值 65.0 系基于 46.3 基线，已作废。若 D2-1/D2-2 取保守项则按实际 N 折算并在记录中写明）
- ✅ [IME 词表增长] `[T-A]` `.venv/bin/python -m pipeline.build_terms --config config.toml && wc -l artifacts/domain_terms.txt` → 行数 ≈ `3462 + 738`（允许 zh/EN 冲突去重与 denylist 过滤造成的少量偏差，偏差须逐条解释）
- ✅ [发布契约不破] `[T-A]` `.venv/bin/python -m pytest -q` → exit 0

**Phase 2 完成定义**：`.venv/bin/python scripts/registry_coverage_report.py --json /tmp/cov.json && python3 -c "import json;d=json.load(open('/tmp/cov.json'));assert d['coverage_pct'] >= 70.0"` → exit 0。

**逐 Task 验收命令展开规则**：把统一规格中的 `<ids>` 换为该行 `ids 文件` 名、`<N>` 换为该行 `ids 数`。**worked example（T2.3）**：

```bash
.venv/bin/python scripts/registry_batch_verify.py --mode allowlist \
  --ids-file .github/plans/t4973-batches/w2_b03.ids --expect 20
grep -v '^#' terms/allowlist_en.txt | grep -c ' '        # 期望 0
sort terms/allowlist_zh.txt | uniq -d | wc -l            # 期望 0
.venv/bin/python -m pipeline.build_terms --config config.toml   # 期望 exit 0
```

**批次提交纪律**：每批单独 commit，message 形如 `feat(registry): allowlist fill W2-batch-03 (#T-4973)`；`git diff --stat` 只含 `terms/allowlist_zh.txt` + `terms/allowlist_en.txt`。

### Phase 3: W3 — 中文首选名起草（W3a 854 个 + D2-6 集 169 个 = 1023 个 concept）

> 依据 §D4/D5：**W3a = 854**（未覆盖 ∩ `preferred_zh` 空 ∩ 非专名）。其中 **107** 行可从仓内 `GB/T-4960.9` zh 释义推导；**747** 行无仓内出处（仅 `对应英文“X”` 模板）⇒ 依 **D2-5=A** 允许 `preferred_en` + 权威仓外 URL（须 200）。
> 任务书口径 1039（含 99 左移行 + 80 六列行）已按 §R-1/R-2 修正：99 行中文名**本就存在**（无需起草）；80 行中文名在 Phase 0 T0.6a/b 完成。
> **D2-6=A（本轮 improve 新增范围，用户已裁决）**：`--mode names` 的 **CJK 硬判据保持字面不变**，由 W3 为 **169 个** `preferred_zh == preferred_en` 且无 CJK 的 id 补中文首选名；**不得走 `--allow-latin-names` 豁免**（该名单**不**得在 Phase 3 的任何批验收中出现）。
> **⚠️ 实测构成（improve 轮核实，务必先读）**：这 169 个 id **全部不在** `w3.ids` 内（与 README「执行批次时必须注意」第 3 条的表述不符，以本条实测为准）。其分布：**132 个已覆盖**（未进入任何工作集）/ **9 个在 `w2.ids`**（`vmec`/`desc`/`simsopt`/`c-2u`/`eu-demo`/`gamma-10`/`helion-trenta`/`k-demo`/`start-device`）/ **28 个为专名**（`company`/`organization`/`facility`，属 `proper_excluded`，本批仅补中文首选名，**H2 仍禁止其入 IME 词表**）。因此该 169 集须**新增独立工作集 `w3b.ids`**（由 **T3.0** 生成）——既有 `w3.ids` 不含它们，直接对 `w3.ids` 跑 W3 无法覆盖 D2-6=A。
> 复现命令（当前应输出 169；D2-6=A 完成后应为 0）：
> ```bash
> python3 -c "import csv,re;rows=[r for r in csv.reader(open('terms/registry/concepts.tsv',encoding='utf-8'),delimiter='\t') if r and not r[0].startswith('#')];print(sum(1 for r in rows if len(r)==8 and r[2]==r[3] and r[2] and not re.search(r'[\u3400-\u9fff]',r[2])))"
> ```
> **批清单唯一权威** = `.github/plans/t4973-batches/README.md`：`w3.ids` = **854** → **43 批**（20×42 + 14）；计划期旧值（`w3_a_b*`/`w3_b_b*` 命名、36/27 行每批、31 批）**已作废** —— 实际文件名统一为 `w3_b01.ids`…`w3_b43.ids`，**内/外部依据不再按批分组**（同一批内混排，执行时按该 id 是否有仓内 `GB/T` 出处选择依据）。

**批次任务统一规格**

- **目标**：为每个 concept 填 `preferred_zh`（中文首选名），并附可核验依据。
- **依赖**：Phase 0 完成（不得基于畸形行起草）；T0.2/T0.3。
- **执行者**：Academic Writer（命名）；Simulation Builder 落表。
- **修改内容**：文件 `terms/registry/concepts.tsv`（**定点填 `preferred_zh`**）；必要时 `terms/registry/evidence.tsv`（追加依据 URL）。
- **修改边界**：只填 `preferred_zh`；不得改 `preferred_en`/`category`/`notes`；不得与 `aliases.tsv` 既有 zh 别名冲突（冲突须列入 `w3-name-conflicts.tsv` 并交裁决，**不得静默择一**）。
- **质量检查方式**：批验收 `--mode names`；每批结束后与 `aliases.tsv` 做冲突扫描。
- **验收标准（每批同构）**：
  - ✅ [批验收] `[T-A]` `.venv/bin/python scripts/registry_batch_verify.py --mode names --ids-file .github/plans/t4973-batches/<ids> --expect <N>` → **exit 0**
  - ✅ [依据可核验] `[T-A]` 同上加 `--check-urls`（`--no-net` 时须为仓内出处）→ **exit 0**；**禁止**追加 `--allow-latin-names`（D2-6=A：CJK 判据字面有效）
  - ✅ [无冲突未登记] `[T-A]` `wc -l .github/plans/t4973-batches/w3-name-conflicts.tsv` 与批记录中的冲突数一致（不允许"零冲突但输出非空"）
  - ✅ [门禁不退化] `[T-A]` `.venv/bin/python -m pipeline.validate_registry` → **exit 0**
- **能失败证明（反例锚定）**：把某行 `preferred_zh` 改为英文串（如 `en`/`OpenCASCADE`）→ `--mode names` 必须 exit 1。
- **潜在风险**：854 个命名的质量风险最高（RK9）→ 强制抽检。

| Task | 组 | ids 文件 | ids 数 | 预估墙钟 | 修改文件 |
|------|----|---------|-------|---------|---------|
| T3.0 | **D2-6 集清单生成** | 生成 `w3b.ids` + `w3b_b01.ids`…`w3b_b09.ids` | 169 | 20 min | `.github/plans/t4973-batches/w3b*.ids`、`README.md`（新增 W3b 节） |
| T3.1 … T3.43（43 个） | W3a（仓内 GB/T 或仓外权威，混排） | `w3_b01.ids` … `w3_b43.ids` | 20×42 / 14（尾批） | 各 30 min | `terms/registry/concepts.tsv`（+`evidence.tsv`） |
| T3.44 … T3.52（9 个） | **D2-6 集**（拉丁装置代号补中文名） | `w3b_b01.ids` … `w3b_b09.ids` | 20×8 / 9（尾批） | 各 30 min | 同上 |
| **小计** | — | — | **1023** | **53 个 Task / 1580 min（≈26.3 h）** | — |

> **展开规则**：`T3.<nn>` ↔ `.github/plans/t4973-batches/w3_b<nn>.ids`（nn=01..43，两位零填充）；`T3.(43+<k>)` ↔ `w3b_b<k>.ids`（k=01..09）；`<N>` = `wc -l` 实测（w3：b01..b42 = 20、b43 = 14；w3b：b01..b08 = 20、b09 = 9）。**批数以 README 为唯一权威**。
> **T3.0 生成规则（确定性、可复跑）**：
> ```bash
> mkdir -p /tmp/opencode/t4973-w3b
> python3 -c "import csv,re;rows=[r for r in csv.reader(open('terms/registry/concepts.tsv',encoding='utf-8'),delimiter='\t') if r and not r[0].startswith('#')];ids=[r[0] for r in rows if len(r)==8 and r[2]==r[3] and r[2] and not re.search(r'[\u3400-\u9fff]',r[2])];open('/tmp/opencode/t4973-w3b/w3b.ids','w').write('\n'.join(ids)+'\n');print(len(ids))"   # 期望 169
> split -l 20 -d -a 2 --additional-suffix=.ids /tmp/opencode/t4973-w3b/w3b.ids /tmp/opencode/t4973-w3b/w3b_b
> # 序号从 00 起 ⇒ 重命名为 w3b_b01.ids…w3b_b09.ids 后复制进 .github/plans/t4973-batches/，并同步更新 README（新增 W3b 节）
> ```
> **T3.0 验收**：✅ `[T-A]` `wc -l .github/plans/t4973-batches/w3b.ids` → `169`；✅ `[T-A]` 批数 `9`、大小 `20×8 + 9`；✅ `[T-A]` `comm -12 <(sort .github/plans/t4973-batches/w2.ids) <(sort .github/plans/t4973-batches/w3b.ids) | wc -l` → `9`（**实测交集**，与上条构成说明一致）；✅ `[T-A]` `comm -12 <(sort .github/plans/t4973-batches/w3.ids) <(sort .github/plans/t4973-batches/w3b.ids) | wc -l` → `0`。
> **能失败证明（变异法）**：副本中删 `w3b_b01.ids` 一行 → `wc -l` 合计由 169 变 **168** 而 FAIL。

**Phase 3 完成定义（一条命令）**：

- ✅ `[T-A]` `.venv/bin/python scripts/registry_row_audit.py --audit --expect-clean-all` → exit 0（含 `w3a_empty_zh=0`；Phase 1/2 已完成，故全集闸门可满足）
- ✅ `[T-A]` **D2-6=A 闸门**（169 → 0，命令见本节开头）：
  ```bash
  python3 -c "import csv,re;rows=[r for r in csv.reader(open('terms/registry/concepts.tsv',encoding='utf-8'),delimiter='\t') if r and not r[0].startswith('#')];print(sum(1 for r in rows if len(r)==8 and r[2]==r[3] and r[2] and not re.search(r'[\u3400-\u9fff]',r[2])))"
  # 期望：0（非 0 ⇒ D2-6=A 未完成）
  ```

**Phase 3 抽检（≥10%，落实 D2-5）**：每 5 批抽检 ≥10%（≥14 行）由独立 agent 复核命名准确性（对照该 concept 的 `preferred_en` + 依据 URL 摘要）；抽检 FAIL → 该 5 批返工；`w3-name-conflicts.tsv` 中的冲突项**全部**须人工裁决后才能收尾。**D2-6 集（T3.44…T3.52）额外要求**：抽检须确认中文名**确为可读中文术语名**（如装置代号 `rfx-mod` → 中文首选名），不得以拉丁串、拼音或无意义音译充数。

**逐 Task 验收命令展开规则**：把统一规格中的 `<ids>` 换为该子任务 `ids 文件` 名、`<N>` 换为该文件 `wc -l`。**worked example（T3.4）**：

```bash
.venv/bin/python scripts/registry_batch_verify.py --mode names \
  --ids-file .github/plans/t4973-batches/w3_b04.ids --expect 20 --check-urls
# 期望 exit 0；**禁止**追加 --allow-latin-names（D2-6=A）
# 另需确认本批新增冲突已全部登记：wc -l .github/plans/t4973-batches/w3-name-conflicts.tsv
```

**批次提交纪律**：每批单独 commit，message 形如 `feat(registry): zh preferred names W3-外部-batch-01 (#T-4973)`；`git diff --stat` 只含 `terms/registry/concepts.tsv`（必要时 +`evidence.tsv`）。

### Phase 4: 导出链终跑 + 发布前全量验证

#### Task T4.1: 全量终验（一条命令的"全绿"入口）

- **目标**：Phase 0–3 全部完成后，做一次全量终验与覆盖率终值记录。
- **依赖**：Phase 0/1/2/3 全部完成
- **frontier**：否
- **执行者**：Dev Orchestrator
- **预估墙钟**：25 min
- **修改内容**：无数据修改；产出记录 `.github/plans/t4973-batches/final-verification.md`（命令 + 实测输出）。
- **修改边界**：不修改任何 `terms/`、`pipeline/`、`artifacts/` 文件（除导出链重跑产物）。
- **质量检查方式**：逐条跑下表。
- **验收标准**：
  - ✅ `[T-A]` `.venv/bin/python scripts/registry_row_audit.py --audit --expect-clean-all` → exit 0
  - ✅ `[T-A]` `.venv/bin/python -m pytest -q` → exit 0
  - ✅ `[T-A]` `.venv/bin/mypy pipeline/ --ignore-missing-imports` → exit 0
  - ✅ `[T-A]` `.venv/bin/ruff format --check .` → exit 0（含本计划文件；否则先 `ruff format` 本文件）
  - ✅ `[T-A]` `.venv/bin/ruff check .` → exit 0
  - ✅ `[T-A]` `.venv/bin/python3 -m pipeline.validate_registry` → exit 0（输出 `6152 definitions`）
  - ✅ `[T-A]` `.venv/bin/python scripts/registry_coverage_report.py` → `coverage_pct ≥ 78.0`（**下限保持 78.0 不因基线更新而下调**；新理论值 = 47.11（W0 后基线）+ 738/3076 + 854/3076 ≈ **98.9%**，故 78.0 = 严格高于"W2+W3 潜力的一半（73.0）"的保守闸门。实际以 D2-1/D2-2/D2-5 裁决与去重为准）
- **能失败证明**：任一门禁命令非 0 → T4.1 不得标记完成。
- **潜在风险**：`coverage_pct` 与预期偏差大 → 逐项核对 W2/W3 是否被专名排除规则误吞。
- **预留歧义标注**：
  - [ ] 无歧义

#### Task T4.2: 发布包构建 + 契约验证

- **目标**：证明数据修复与覆盖扩充未破坏发布契约。
- **依赖**：T4.1
- **frontier**：否
- **执行者**：Dev Orchestrator
- **预估墙钟**：25 min
- **修改内容**：
  - 运行 `.venv/bin/python -m pipeline.release_pack --tag v2026.10.26 --include-registry-exports --substitutions --vale-substitute --force`
  - 运行 `.venv/bin/python -m pipeline.verify_release_contract --root dist/stage/v2026.10.26`
- **修改边界**：只新增 `dist/` 下产物（已 gitignore）；不得改 `terms/`。
- **质量检查方式**：契约输出 `contract OK`。
- **验收标准**：
  - ✅ `[T-A]` `.venv/bin/python -m pipeline.verify_release_contract --root dist/stage/v2026.10.26` → **exit 0** 且含 `contract OK`
  - ✅ `[T-A]` `python3 -m pytest -q tests/test_release_pack.py tests/test_verify_release_contract.py` → exit 0
- **能失败证明（变异法）**：临时改 `dist/stage/v2026.10.26/domain_terms.txt` 一行 → 契约验证必须 exit ≠ 0。
- **潜在风险**：`--tag` 名与真实 tag 不一致 → 仅用于本地 stage，不 push tag（发布由人工决定）。
- **预留歧义标注**：
  - [ ] 无歧义

#### Task T4.3: IME 同步（有本机副作用，放最后）

- **目标**：把新词表同步到本机 Fcitx/Rime 词表目录。
- **依赖**：T4.1
- **frontier**：否
- **执行者**：Dev Orchestrator
- **预估墙钟**：15 min
- **修改内容**：运行 `.venv/bin/python -m pipeline.sync_to_fcitx --input artifacts/domain_terms.txt --dest ~/.config/fcitx/rime/wordlists/domain_terms.txt`（先备份原文件到 `/tmp/opencode/domain_terms.txt.bak`）。
- **修改边界**：不得改仓库内文件（除 `artifacts/domain_terms.txt` 已由管线生成）。
- **质量检查方式**：目标文件行数 == `artifacts/domain_terms.txt` 行数。
- **验收标准**：
  - ✅ `[T-A]` `wc -l ~/.config/fcitx/rime/wordlists/domain_terms.txt artifacts/domain_terms.txt` → 两值相同（exit 0）
  - ✅ `[T-A]` `python3 -m pytest -q tests/test_sync_to_fcitx.py` → exit 0
- **能失败证明**：把 `--dest` 指向只读路径 → 命令必须非 0。
- **潜在风险**：无 `~/.config/fcitx` 环境 → 用 `--dest /tmp/opencode/domain_terms_smoke.txt` 做 smoke 并标注 `[SKIPPED-LOCAL]`。
- **预留歧义标注**：
  - [ ] 无歧义

#### Task T4.4: 收尾（CHANGELOG / 快照 / 计划归档）

- **目标**：文档与快照与数据一致。
- **依赖**：T4.1、T4.2
- **frontier**：否
- **执行者**：Dev Orchestrator → handoff `doc-maintainer`
- **预估墙钟**：20 min
- **修改内容**：
  - `CHANGELOG.md`（新增 v2026.10.26 段：数据修复/定义重写/覆盖扩充）
  - `.github/plans/_project-snapshot.md`（刷新 registry 计数：concepts 3076、definitions 6152、aliases、evidence；`git_commit` 为生成时快照）
  - 本计划文件：追加 `## Execution Log` 与完成勾选；完成后按惯例移入 `.github/plans/completed/`
- **修改边界**：只改上述 3 个文件；不得夹带未声明改动（`git diff --stat` 校验）。
- **质量检查方式**：快照计数与 `pipeline.validate_registry` 输出一致。
- **验收标准**：
  - ✅ `[T-A]` `grep -c "6152" .github/plans/_project-snapshot.md` ≥ 1
  - ✅ `[T-A]` `git diff --stat` 只含声明的 3 个文件
  - ✅ `[T-A]` `rg -c "T-4973" .github/plans/completed/terminology-coverage-and-definition-quality.md` ≥ 1（归档后）
- **能失败证明**：故意把快照计数改成 `9999` → 与 validate_registry 输出不一致，本任务判定 FAIL。
- **潜在风险**：快照为"生成时快照"，使用者须重测（已在本文件 §动态基线约定说明）。
- **预留歧义标注**：
  - [ ] 无歧义

## Execution Wave（并行执行波次）

| Wave | 可并行 Task | Frontier（无人挡即刻开工） | 依赖已完成 | 说明 |
|------|------------|--------------------------|------------|------|
| W0-1 | T0.0、T0.1、T0.2 | T0.0、T0.1、T0.2 | — | 三个只读脚本互不冲突（**并行上限 3**：同为本机 IO 轻任务） |
| W0-2 | — | T0.3 | W0-1 | 清单生成依赖三脚本 |
| W0-3 | T0.4、T0.5 | T0.4、T0.5 | W0-2 | 行区间不重叠（99 行 vs 80 行）；**但同写 `concepts.tsv` → 实际必须串行**（同文件冲突）；标"可并行"仅指无逻辑依赖 |
| W0-4 | — | T0.6a | T0.5 | 需 80 行 schema 就位 |
| W0-5 | — | T0.6b | T0.6a | 同文件串行 |
| W0-6 | — | T0.7a | T0.6b | 需中文名 |
| W0-7 | T0.8 | T0.7b、T0.8 | T0.6b / W0-2 | T0.7b 写 definitions、T0.8 写 evidence → **不同文件，可真并行**（≤2） |
| W0-8 | — | T0.9+T0.10（同一 commit） | T0.4、T0.5、T0.8 | 门禁与测试同批落地，否则 CI 红（RK2） |
| W0-9 | T0.11 | T0.11 | W0-8 | RED/GREEN 录制 |
| W0-10 | — | T0.12 | T0.7b、T0.8、W0-8 | 导出链需数据全静 |
| W0-11 | — | T0.13 | T0.11、T0.12 | W0 收尾 |
| W1 | T1.A*/T1.B*/T1.C* 全部串行 | `T1.A1-EN` | W0-11 | `definitions.tsv` 单文件 → **串行**（同批 `-EN` → `-ZH`，跨批亦串行）；无并行机会 |
| W2 | T2.1…T2.37 串行 | T2.1 | W0-11、T2.0 | allowlist 两文件 → 串行；T2.38 依赖全部批（**若 W3b 先于含 9 个拉丁 id 的 W2 批执行，则 T2.38 须在 W3b 后复跑一次**，见 Phase 2 顺序耦合说明） |
| W3 | T3.1…T3.52 串行 | T3.0 | W0-11、T3.0 | `concepts.tsv` 单文件 → 串行；W3a 43 批与 D2-6 集 9 批无相互依赖，但同文件 ⇒ 仍串行 |
| W4 | T4.2、T4.3 | T4.1 | 全部 | T4.2/T4.3 在 T4.1 后**可真并行**（不同目标） |

> **并行上限**：本次计划全程受"单文件写入"约束，实质并发度 ≈1（除 W0-1 的三脚本、W0-7 的两个不同文件、W4 的两项）。**不得为追求并发而拆分同一文件的批量写入**。

## 动态基线约定（禁止硬编码）

- 本计划所有 `HEAD`/行号/计数均为 **2026-10-26 @ `3cb3837`** 的**生成时快照**；执行时**必须重测**：`git rev-parse HEAD`、`git status --porcelain`、`.venv/bin/python scripts/registry_row_audit.py --audit`。
- 行号锚点（99 行 = 3171–3315、80 行 = 3316–3395）**仅在 `3cb3837` 成立**；实现时以 `concept_id` 为锚，行号仅作提示。
- 前端数字（W2 738 / W3a 854 / en_boilerplate 746 / zh 模板 1517 / 631 / 169 等）为 **W0 后权威值**；每相位开始时用 `scripts/registry_coverage_report.py` 与 `registry_row_audit.py --audit` 重算，差值必须能逐行解释后再动手。

## Post-Execution Verification

### Automated Verification（Dev Orchestrator / TE 自动执行）

| ID | Description | Command | Expected |
|----|-------------|---------|----------|
| V1 | 结构完整性 + W1 质量（Phase 1 起用全集闸门） | `.venv/bin/python scripts/registry_row_audit.py --audit --expect-clean-all` | exit 0；`malformed_cols=0, bad_category=0, sixcol_rows=0, non5_cols=0, en_boilerplate=0, zh_en_corruption=0, concepts_without_defs=0` |
| V2 | registry 门禁 | `.venv/bin/python -m pipeline.validate_registry` | exit 0；`registry OK: 3076 concepts, …, 6152 definitions` |
| V3 | 单元测试（CI 同口径） | `.venv/bin/python -m pytest -q` | exit 0（≥159 + 新增用例） |
| V4 | 覆盖率终值 | `.venv/bin/python scripts/registry_coverage_report.py` | exit 0；`coverage_pct ≥ 78.0`（下限不因基线更新而下调，见 T4.1） |
| V5 | 类型检查 | `.venv/bin/mypy pipeline/ --ignore-missing-imports` | exit 0 |
| V6 | 格式门禁（含 Markdown 内 python 块） | `.venv/bin/ruff format --check . && .venv/bin/ruff check .` | exit 0 |
| V7 | 编译检查（CI 同口径） | `.venv/bin/python -m compileall -q pipeline tests` | exit 0 |
| V8 | 产物污点归零 | 三条 JSON 断言（§T0.12） | 三项均 0 |
| V9 | 发布契约 | `.venv/bin/python -m pipeline.verify_release_contract --root dist/stage/v2026.10.26` | exit 0；`contract OK` |

### Deferred (needs restart / deployment)

- [ ] D1: 无（本仓库无服务进程；`release_pack` 产物为静态文件，不需要重启）

### Probe (best-effort, run if available)

- [ ] P1: `.venv/bin/python scripts/registry_batch_verify.py --mode definitions --ids-file .venv-nonexistent --expect 0` → 应 exit ≠ 0（负向探针：确认脚本对缺失 ids 文件报错而非静默 PASS）
- [ ] P2: `git rev-parse HEAD` 与 `git status --porcelain`（每批提交前）；若有脏文件 → 先解释来源

### Manual（真正需要人工判断）

- [ ] M1: W1 抽检（每 5 批 ≥8 行）语义正确性复核 —— 由独立 agent/人判读释义是否真的定义该术语（机械门禁无法判语义）
- [ ] M2: W3 抽检（每 5 批 ≥10%，≥14 行）命名准确性复核
- [ ] M3: `w3-name-conflicts.tsv` 中的冲突项人工裁决
- [ ] M4: 目视抽检 T0.4（99 行）/T0.5（80 行）修复后 10 行的列语义（中文/英文是否各归其位）

## 验收清单（Phase → 一条命令的完成判定）

| Phase | 完成判定命令 | 期望 |
|-------|-------------|------|
| W0 | `.venv/bin/python scripts/registry_row_audit.py --audit --expect-clean` | exit 0（全部畸形指标 0） |
| W1 | `.venv/bin/python scripts/registry_row_audit.py --audit` → 检查 `en_boilerplate=0 && concepts_without_defs=0` | exit 0 |
| W2 | `.venv/bin/python scripts/registry_coverage_report.py --json /tmp/c.json && python3 -c "import json;d=json.load(open('/tmp/c.json'));assert d['coverage_pct'] >= 70.0"` | exit 0 |
| W3 | `.venv/bin/python scripts/registry_row_audit.py --audit --expect-clean-all` | exit 0（含 `w3a_empty_zh=0`；另须 D2-6 闸门 = 0，见 Phase 3） |
| 全量 | V1–V9 全绿 | 全部 exit 0 |

## 回归检查清单

- [ ] `pytest -q` 全绿（G1/V3）
- [ ] `mypy pipeline/ --ignore-missing-imports` 0 错（G2/V5）
- [ ] `ruff format --check .` + `ruff check .` exit 0（G3/G4/V6；**含本计划文件**）
- [ ] `python3 -m pipeline.validate_registry` exit 0（G5/V2）
- [ ] `python3 -m pipeline.verify_release_contract --root dist/stage/<tag>` → `contract OK`（G6/V9）
- [ ] 公开 CI 绿（本仓 CI 曾连续 4 次红灯，run #43 刚恢复）
- [ ] `concepts.tsv` 数据行仍为 **3076**、`concept_ids` 集合未变（sha256 比对）
- [ ] `definitions.tsv` 行数 = **6152**（6132 + 20）
- [ ] **D2-6 闸门**：`preferred_zh == preferred_en` 且无 CJK 的 id 数 = **0**（当前 169；命令见 §Phase 3）
- [ ] W1 工作集（`w1_a∪w1_b∪w1_c`）内 zh 行匹配 `聚变/核工程术语` 模板者 = **0**（当前 631；命令见 §Phase 1 完成定义）
- [ ] `evidence.tsv` 列数全部为 5、**audit** `data_rows` 仍 **3168**（文件 `wc -l` = 3217，含 47 空行 + 2 注释）
- [ ] `translation_dict.json`：值为 `'en'` 的条目 **0**；全小写同一性映射 **0**
- [ ] `query_expansions.json`：非 ASCII `category` **0**
- [ ] `tag_rules.jsonl`：16 类之外的 `category` **0**
- [ ] `allowlist_en.txt` 无空白项；`allowlist_zh.txt` 无重复行
- [ ] 每个 commit message 带 `#T-4973`；`git diff --stat` 只含声明文件
- [ ] 专名（company/organization/facility）**未**进入 IME 词表

## 审查日志

| 轮次 | 聚焦 | 发现问题数 | 已修正 | 剩余 |
|------|------|-----------|--------|------|
| R1 | 结构完整性（Phase/Task 齐全、文件清单、边界） | 5 | 5 | 0 |
| R1.5 | 外部引用事实核查（脚本/命令/路径/字段名/基线数字） | 7 | 7 | 0 |
| R2 | 可执行性（每条验收命令实测可跑 + 期望 exit code） | 6 | 6 | 0 |
| R2.8 | LLM 可执行性（下游是否需要额外推断）+ 粒度门（≤30 min / ≤3 文件） | 5 | 5 | 0 |
| R3 | 风险与边缘（含跨轮一致性、回滚、并行安全） | 4 | 4 | 0 |
| **终止** | **T1 — 收敛终止（issue 清零）** | | | **0** |
| **IMPR-1（mode=improve）** | W0 实测漂移对齐：口径/数字（47.11% / W2 738 / W3a 854 / 631 模板 / 429 行）、README 批数权威（119 批 / 2348 ids）、D2-6=A 范围（新增 w3b 集）、D2-7=A 双侧拆分（78 子任务）、D2-8=A 白名单收窄、粒度门复算 | **11** | **11** | **0** |

### IMPR-1 Issues（mode=improve，2026-10-26，基线 `66197f2`）

- **IMPR-1-1**：§D1–D4/§E3–E4/§R-3/§R-7 仍是 W0 前数字（46.3% / 584 / 527+57 / proper 36 / 1565 模板）→ 已全部改为 W0 后权威值（47.11% / 738 / 668+70 / 35 / 1517 且标注 631 在 W1 内）✅
- **IMPR-1-2**：Phase 1–4 批数与 README 不符（W1 38 批、W2 10 批、W3 31 批及 `w3_a_*` 文件名）→ 已按 README 重写为 39 / 39 / 53 个 Task，并声明 README 为唯一权威 ✅
- **IMPR-1-3**：D2-6=A 在计划中无可执行落点（169 个 id 不在任何工作集）→ 已实测核实（132 覆盖 / 9 在 w2 / 28 专名 / 0 在 w3）并在 Phase 3 新增 T3.0 + T3.44…T3.52 与 169→0 闸门；**同时标注与 README 第 3 条的表述冲突（以实测为准）** ✅
- **IMPR-1-4**：D2-7=A 的"批数不变但每批墙钟上升"未落到任务拆分 → 已把 39 批拆为 78 个 en/zh 子任务（各 ≤30 min），批收口保留 `--lang both` 双侧合规，**未放宽任何验收** ✅
- **IMPR-1-5**：§Phase 1 仍要求"每批强制来源白名单 + `--check-urls`"（与 D2-8=A 冲突）→ 已收窄为"仅当显式引用外部权威时才需 URL/`--check-urls`"，`corpus` 明确接受；RK4 同步收窄 ✅
- **IMPR-1-6**：T0.7 的 rationale 以"W1 只负责 en 行"为前提（已作废）→ 已改为 D2-7=A 口径，并区分"W0 修损坏（48 条 `指“en”`，已清零）"与"W1 重写模板（631 行 `指“X”`）" ✅
- **IMPR-1-7**：T0.9/T0.10 修改边界低估（实际另动 8 个测试文件 fixture + 1 行 category 修正）→ **未改写任务声明**，仅在受影响处标注"以 §Execution Log（commit `08a2e98`）记的偏差为准（用户追认 1）"，并在 Error & Rescue Map 同步标注 ✅
- **IMPR-1-8**：`--expect-clean` 口径与剖面拆分不一致 → 已统一为"`--expect-clean` = W0 结构集（= Phase 0 完成定义）/ `--expect-clean-all` = 全集（Phase 1 完成起使用）"，T0.1 描述、Phase 1/3 完成定义、V1、验收清单同步 ✅
- **IMPR-1-9**：T0.8 的 `wc -l == 3168` 口径错误（文件恒为 3217）→ 已改为 audit `data_rows == 3168` 并说明 3217 的构成，回归清单同步 ✅
- **IMPR-1-10**：T0.3 清单已在 W0 后重生成（commit `66197f2`）但计划未标注 → 已加"🔄 W0 后重生成"块 + 批数验收（4/34/1/37/43 = 119）✅
- **IMPR-1-11**：frontmatter 陈旧（`mode=refine`、`git_commit=3cb3837`）→ 已更新为 `mode=improve` / `git_commit=66197f2` / 当前时间戳 ✅

### R1 Issues（结构完整性）

- **R1-1**：初版未把"证据要求（URL 200 / 仓内出处）"转成可执行验收 → 已把 `--check-urls` 写入每批验收命令与 V1 之外的批闸门 ✅
- **R1-2**：W1 原按"每 concept 一个任务"展开（757 个任务）→ 收敛为 38 个批量任务（每批 ≤20 行 + 批 ids 文件），并在表中逐行给出 ids 文件与数量 ✅
- **R1-3**：缺"Phase 完成定义"→ 已补 §验收清单（每 Phase 一条命令）✅
- **R1-4**：`evidence.tsv` 修复原只提"source 污染"，漏了 213 行 4 列 + 2 行 2 列 → 已并入 T0.8（并给出精确计数）✅
- **R1-5**：缺抽检设计（用户明确要求"可核验产出方式 + 抽检比例"）→ 已补 W1/W3 的每 5 批抽检比例与返工规则（D2-4/D2-5）✅

### R1.5 Issues（外部引用事实核查）

- **R1.5-1**：`verify_release_contract --root .` **实测失败**（缺根级 `domain_terms.txt`）；正确用法是对 stage 目录 → 已改写 G6/V9 与 T4.2 ✅
- **R1.5-2**：任务书 `definitions.tsv` "747 行 en 套话"与实测 746 不符 → 已在 §R-4 记录并取 746（宽松/严格两种匹配均 746）✅
- **R1.5-3**：任务书"99 行中文名实为英文串须重命名"与实测不符（中文在第 1 列）→ §R-1 修正，W3 不含这 99 行 ✅
- **R1.5-4**：`build_terms` 的空白约束确认为 `SystemExit`（`pipeline/build_terms.py:66-83`）→ 已写成 W2 的 RK5 + 能失败证明 ✅
- **R1.5-5**：`export_registry` 的列解析是**按位**（`_iter_concept_rows`）→ 已作为污染机制的机械解释写入 §背景与目标（附带文件/函数名）✅
- **R1.5-6**：`validate_registry` 的 concepts 门禁位置（`:87`）与 definitions 的"精确 4 列"先例（`:255`）已逐一核对 ✅
- **R1.5-7**：`tests/test_registry_validator.py:270` 的 `_MINIMAL_EVIDENCE` 为 2 列 evidence，加严后会红 → 已并入 T0.10 同一 commit ✅

### R2 Issues（可执行性）

- **R2-1**：初版把 `grep -c` 当 exit code 判定（无匹配时 grep 返回 1）→ 已统一改为"断言计数值" ✅
- **R2-2**：W2 批大小 59 与 `--batch-size 20` 不一致 → 已在 T0.3 说明"实际批数以 README 为唯一权威" ✅
- **R2-3**：T4.1 的覆盖率下限最初写成 93%（理论上限）→ 改为保守闸门 78%，并说明实际值取决于 D2 裁决 ✅
- **R2-4**：`ruff format --check .` 会覆盖 Markdown 内 python 块（0.17.2）→ 已写入 RK3，并在 T4.1 前置 `ruff format` 本计划文件 ✅
- **R2-5**：T0.12 导出命令原缺 `--tag-rules`/`--query-expansions` 等 flag → 已补固定命令串，并断言三项污点 ✅
- **R2-6**：`sync_to_fcitx` 无 `--dest` 时写用户目录 → 已加备份步骤与 `--dest` smoke 降级路径 ✅

### R2.8 Issues（LLM 可执行性 + 粒度门）

- **R2.8-1**：`category` 取值"按语义判定"过于开放 → 已补三步规则（兄弟对照 → 语义白名单示例 → 16 类硬约束）并产出 `category-map-*.tsv` 对照表 ✅
- **R2.8-2**：W1 批次的 ids 来源未固定 → 已固定为 `.github/plans/t4973-batches/*.ids`（T0.3 产出）✅
- **R2.8-3**：粒度门：全部 Task 预估 ≤30 min；无 >60 min 单步；单 Task 修改文件 ≤3（W1/W3 为 1~2 个）✅
- **R2.8-4**：T0.9+T0.10 拆成两个 Task 但会各自造成 CI 红 → 已显式标注"同一 commit"（消除下游猜测）✅
- **R2.8-5**：D2-1/D2-2/D2-5 未裁决时的默认行为未定义 → 已约定"取推荐项并在 commit/计划中标注 `[默认取推荐项，待追认]`" ✅

### R3 Issues（风险与边缘）

- **R3-1**：回滚安全性 —— W0 的定点行改写若失败，是否影响其它行？→ 每 Task 只做定点改写 + `concept_ids_sha256` 不变断言；回滚 = `git revert <该 Task commit>`（行区间/ids 清单均入库）✅
- **R3-2**：What-If —— 改 `concepts.tsv` 列结构会波及哪些未声明依赖？→ 实测：`export_registry`（产物三类）、`validate_registry`、`aliases/evidence` 外键（不变）、`tag_rules/query_expansions`。已全部纳入 T0.12 断言 ✅
- **R3-3**：并行安全 —— W0-3 名义并行但同文件 → 已在 Execution Wave 显式降级为串行，避免并发写冲突 ✅
- **R3-4**：跨项目依赖 —— 检查 PM：本计划全部文件在 `fusion-terms` 仓内，无跨项目依赖；PM 任务 **T-4973** 归属本项目（`fusion-terms`），commit 带 `#T-4973` 即可关联 ✅

### Completion Summary

| 维度 | 结果 |
|------|------|
| 背景与目标 | 完整：问题描述、根因（含 commit/机制/取证）、目标、非目标（5 项含理由）、复用分析（6 项） |
| 数据基线 | 8 组（A–H）共 40 条断言，每条附复现命令；历史基线 @ `3cb3837`，**影响后续规模的行（D1–D4、E2–E4）已按 W0 后权威值更新**，冲突以「W0 收口数字」为准 |
| 与任务书差异 | 7 条（R-1 ~ R-7），每条给复现与处置（R-3/R-7 数字已按 W0 后权威值更新） |
| 风险与对策 | 10 条风险 + Error & Rescue Map 10 条路径，0 CRITICAL GAP |
| 待裁决 | **8 项（D2-1 ~ D2-8），全部已裁决＝选项 A**（含 D2-6/D2-7/D2-8 的实施口径） |
| 执行计划 | 4 Phase + 1 收尾相位；**190 个 Task** —— W0: 16（✅ 全部 DONE）／W1: **78**（39 批 × en/zh 两侧）／W2: **39**（T2.0 + 37 批 + T2.38）／W3: **53**（T3.0 + W3a 43 批 + D2-6 集 9 批）／W4: 4 —— 每个 Task 均有 ≤30 min 预估 + 修改文件清单 + 可执行验收命令/期望 exit code |
| 验收清单 | 5 条 Phase 级"一条命令"判定 + 18 项回归检查 |
| 已知局限 | ① 内容密集工作量：W1 ≈1512 行（双侧，631 行为 zh 模板重写）+ W3a 854 名 + D2-6 集 169 名 ≈ **2535 行内容产出**；② 覆盖率终值取决于 D2-1/D2-2/D2-5 裁决与去重；③ 抽检语义判定（M1/M2）无法完全机械化；④ **墙钟估算（计划级）**：全量 ≈ **80.5 h**（W0 已完成 ≈7.3 h ⇒ 剩余 ≈ **73.2 h**），较 refine 版（101 Task / ≈45 h）上升 —— 主因是 (a) 批数按 README 权威值修正（W2 10→37 批、W3 31→43 批）、(b) D2-7=A 使 W1 双侧拆分（38→78 个子任务）、(c) D2-6=A 新增 169 名 / 9 批 |

## 待裁决落地记录（由父代理/用户回写）

| # | 裁决 | 日期 | 载体 |
|---|------|------|------|
| D2-1 | **A. 入表** —— `vmec`/`desc`/`simsopt`/`cate`/`pactole`/`pactiter`/`tract`/`oscar` 8 个 code 以代号形式写入 allowlist（先例 99/107） | 2026-10-26 | 用户在本会话显式裁决（question 工具，选项 A） |
| D2-2 | **A. 只入领域专指项** —— W2 的 EN 侧只写 36 个领域专指概念 + 8 个 code；21 个通用英文词（`design`/`system`/`method`/`wall`/`steel`…）**不写入** `allowlist_en.txt` | 2026-10-26 | 同上 |
| D2-3 | **A. 后续批次** —— 剩余 1517 行「低信息但未损坏」zh 模板释义（762 行 `指“X”` + 755 行 `对应英文“X”`）**不在本批范围**，登记为独立后续批次 | 2026-10-26 | 同上 |
| D2-4 | **A. 每批 100% 机械门禁 + 每 5 批抽检 10%（≥8 行）由独立 agent 复核语义**；抽检 FAIL → 该 5 批返工 | 2026-10-26 | 同上 |
| D2-5 | **A. 允许仓外权威来源** —— W3 命名依据可用 `preferred_en` + Wikipedia/IAEA/ITER 等权威 URL（须实测 HTTP 200）；仓内 `GB/T-4960.9` 释义为优先来源 | 2026-10-26 | 同上 |
| D2-6 | **A. 维持字面 CJK 判据** —— `--mode names` 的「必须含 CJK」不变；169 个拉丁名装置代号由 **W3 补中文首选名**（不豁免、不改判据）。**实施口径（improve 轮实测）**：这 169 个 id **不在** `w3.ids` 内（132 已覆盖 / 9 在 `w2.ids` / 28 为专名）⇒ 须新增独立工作集 `w3b.ids`（**T3.0** 生成）与 9 个批任务（**T3.44…T3.52**），详见 §Phase 3 | 2026-10-26 | 同上（question 工具，选项 A） |
| D2-7 | **A. W1 连 zh 行一起重写** —— W1 每批同时改写该 id 的 en 行与 zh 行（含 `指“X”` 模板行），使语言侧一致；**本批规模由 ≈766 行增至 ≈1512 行**（实测：en 746 + zh 746 + W1-C 新增 20）。**批数不变**（4/34/1 = 39 批），但每批须拆为 en/zh 两个 ≤30 min 子任务（**共 78 个子任务**，见 §Phase 1）；门禁不变（批收口仍要求 `--lang both` 双侧同时合规） | 2026-10-26 | 同上 |
| D2-8 | **A. 允许仓内依据 `corpus`** —— W1 释义可以该 concept 的 registry `notes` / 既有 zh 释义为依据（标 `corpus`）；仅当释义**显式引用外部权威**时才要求 URL / `GB/T` / `ITER` / `IAEA` | 2026-10-26 | **用户显式裁决（本会话 question 工具，选项 A）** |

> **裁决状态：D2-1 ~ D2-8 全部已裁决（2026-10-26，用户在本会话以结构化选项选定 A）**。以下前置的用户口径同样构成本计划的执行前提：
> ① W1 口径 = **重写全部**（含 746 条 en 通用套话，非删除；**D2-7=A：en/zh 双侧**）；② **专名不入 IME 词表**（company 25 / organization 7 / facility 3 共 **35** 个排除；W0 后权威值，任务书与早期文本写 36 已作废）；③ **W3 并入本批次**（不独立排期）；④ 先落本计划文件、再由 Dev Orchestrator 逐任务闭环执行。

## improve 轮变更记录（`mode=improve`，2026-10-26，基线 `66197f2`）

> 本节只记录**计划文本**的口径/数字/拆分变更。**§Execution Log 的任何历史条目（T0.0–T0.13、W0 收口数字、追认表）未被改写**，逐字可追溯；凡本文件别处表述与 Execution Log 冲突，**以 Execution Log 为准**。

| # | 变更项 | before → after |
|---|--------|----------------|
| I1 | 覆盖率 / 未覆盖 | 46.3% (1652) → **47.11% (1627)**；`allowlist_only` → **46.26** |
| I2 | W2 规模 | 584（527+57）→ **738（668+70）**；批数 10 → **37** |
| I3 | §E3/§E4 zh 模板 | 48 行 `指“en”` / 1565 行模板 → **0 行 / 1517 行**，并标注其中 **631** 行落在 W1 工作集内 |
| I4 | 批清单权威 | 计划期估值（30/31 批等）→ **README = 119 批 / 2348 ids**（`w1_a 67→4`、`w1_b 679→34`、`w1_c 10→1`、`w2 738→37`、`w3 854→43`；生成 commit `66197f2`） |
| I5 | W1 任务粒度（D2-7=A） | 38 批任务 → **78 个 en/zh 子任务**（各 ≤30 min），批收口仍 `--lang both` 双侧合规 |
| I6 | W1 规模与墙钟 | 766 行 / 38×30 min → **≈1512 行 / 1755 min（≈29.3 h）** |
| I7 | D2-6=A 落点 | 无（169 个 id 不在任何工作集）→ **T3.0 生成 `w3b.ids` + T3.44…T3.52 共 9 批**，闸门 169 → 0 |
| I8 | W3 任务粒度 | 31 批（`w3_a_*`/`w3_b_*` 混命名）→ **53 个 Task**（T3.0 + `w3_b01…b43` + `w3b_b01…b09`） |
| I9 | 来源白名单（D2-8=A） | 每批强制来源白名单 + `--check-urls` → **仅当显式引用外部权威时才要求 URL/`--check-urls`**；仓内依据标 `corpus` 即合规 |
| I10 | 门禁剖面 | `--expect-clean` = 全部指标为 0 → **`--expect-clean` = W0 结构集 / `--expect-clean-all` = 全集**（Phase 1 完成起用） |
| I11 | T0.8 evidence 行数口径 | 文件 `wc -l == 3168` → **audit `data_rows == 3168`**（文件 `wc -l` = 3217） |
| I12 | T0.13 evidence 规范化行数 | 642 → **429**（以 Execution Log / `git diff --numstat` 为准） |
| I13 | T0.9/T0.10 边界 | "只改 1 个测试文件" → **标注"以 Execution Log（commit `08a2e98`）记的偏差为准"**（另动 8 个测试文件 fixture + 1 行 `component`→`concept`，用户追认 1）；**未改写原声明** |
| I14 | Task 总数 / 墙钟 | 101 Task / ≈45 h → **190 Task / ≈80.5 h**（W0 已完成 16 Task ≈7.3 h ⇒ 剩余 174 Task ≈73.2 h） |
| I15 | frontmatter | `mode: refine` / `git_commit: 3cb3837` → **`mode: improve` / `git_commit: 66197f2`** |

**未解决项（交父代理裁决，未在本文件内自行决定）**：

1. **D2-6=A 的 169 集不在现存任何工作集内**（实测：132 已覆盖 / 9 在 `w2.ids` / 28 为专名 / **0 在 `w3.ids`**）。关闭该项必须**新增** `w3b.ids` 及其 9 个批文件 —— 本 improve 会话仅被授权修改本计划文件，**未生成任何清单文件**（T3.0 已写入计划，待有写权限的执行者落地）。
2. `.github/plans/t4973-batches/README.md` §「执行批次时必须注意」第 3 条称"这 169 个 id 属 W3 的必做项"，与本轮实测**冲突**（0 个在 `w3.ids`）；建议由 T3.0 一并修正 README（本会话无权改该文件）。
3. **W2 的 9 个拉丁名 id 与 W3b 的顺序耦合**：计划内已给出确定性处置（先完成 W3b 对这 9 个 id 的命名再写其 allowlist；若已先写则 W3b 后复跑 T2.38 清理），但"W3b 是否整体提前到 Phase 2 之前"属排期决策，**待父代理确认**。

## Execution Log

> 由 Dev Orchestrator / Task Executor 在执行过程中追加；每条含 `[YYYY-MM-DD HH:MM] Task X.Y — [STATUS]` + 命令原文 + 实测输出（≥3 行）。
> 结构化失败项请用 ```json fenced block 落 `error_id/error_type/summary/root_cause_guess/confidence/retry_suggestion/blocked_downstream/task_id/attempted_fixes`，供 `mode=improve` 解析。

### T0.0 — ✅ DONE（2026-10-26 15:50）
- 委派 `simulation-builder`；交付 `scripts/registry_coverage_report.py`（700 行，sha256 `527ea6b808195f8c6bd3c30b352dcc544392509dfaf0a587a6cfb062ce8f41ae`）
- 命令：`.venv/bin/python scripts/registry_coverage_report.py` → exit 0
  实测：`total 3076 | covered 1449 | uncovered 1627 | coverage_pct 47.11 | W2 584 (multiword 527 / single 57) | W3a 854 | proper_excluded 35 | allowlist_only_coverage_pct 45.71 | covered_plus_uncovered_check PASS`
- **计划 §D1 更正（权威数字以本条为准）**：原 `46.3%` 系误算——假设「179 行畸形必然全未覆盖」，实测其中 **25 行**经中文 alias 已存在于 `domain_terms.txt`（如 `structural-material` ← `结构材料`），故 `uncovered = 1473(规范) + 154(畸形) = 1627`。另 `proper_excluded` 为 **35**（非任务书所述 36）。
- 能失败证明：`--terms-file /dev/null` → `coverage_pct 0.0`（证明非硬编码）
- ruff format/check exit 0；commit `40ae0ea`

### T0.1 — ✅ DONE（2026-10-26 16:00）
- 委派 `simulation-builder`；交付 `scripts/registry_row_audit.py`（460 行，sha256 `94386631b22da695c3e5357d7bab7d69b8db00678e6adf0dd9a96154d0a48a25`）
- `.venv/bin/python scripts/registry_row_audit.py --audit` → exit 0
  实测：`data_rows 3076 | cols_dist {8: 2996, 6: 80} | malformed_cols 80 | bad_category 99 | en_boilerplate 746 | zh_en_corruption 48 | glued_source_rows 427 | non5_cols 215 | concepts_without_defs 10`
  **修复前锚点**：`concept_ids_sha256 = c1c4e359d22283dace5c872512c905c2d6c377844bfd943d9f9b1c288f9e259b`（T0.4/T0.5 修复后必须不变）
- `--expect-clean` → **exit 1**（未修复前必须失败，RED 证据已录）
- 能失败证明（变异法）：副本中 1 行 8 列改 6 列 → `malformed_cols 80 → 81`
- commit `b88e97c`

### T0.2 — ✅ DONE（2026-10-26 16:20）
- 委派 `simulation-builder`；交付 `scripts/registry_batch_verify.py`（972 行，sha256 `6fa9f254a7e880c5660d761cf5bc5bee37c80c9cf4ea3e272fbc7644fe08c7b3`）
- `--self-test` → exit 0（24/24 断言）；`poloidal-field-power-supply`（真实 6 列行）→ **FAIL exit 1**（输出 `concepts.tsv:3316: concept_cols … expected 8 columns, found 6`）；`half-value-layer` → PASS exit 0
- **⚠ 后记（2026-10-26，裁决 4=A）**：上述 24/24 依赖 3 处**真实语料锚点行**仍为畸形。W0 把它们修好后（`:3316` 六列、`:3171` 左移、`definitions.tsv:5838` `指“en”`），`--self-test` 退化为 **18/24 exit 1**——**坏的是自检夹具，不是规则**（规则有效性由 W1 逐批仓外变异法复证）。已按裁决 A 独立 commit 重锚（临时副本地重建缺陷，规则一条未改），现回到 **24/24 exit 0**；证据见 `.github/plans/t4973-batches/self-test-reanchor.md`。本条其余实测值（972 行 / sha256 `6fa9f254…`）为 T0.2 交付时点的事实，**保持原样不追改**（修复后的脚本为 1057 行 / sha256 `35d234b3…`）
- 能失败证明（实现回退）：套话正则改 `^$` → self-test 22/24 失败；改回后 sha256 与交付一致
- 超出字面规格的 3 条守卫（加强，非放宽）：`concept_cols`（必须恰 8 列）、`def_lang_placeholder`（zh 含 `指“en”`）、`def_source_unknown`（source 白名单为闭合集合，**不含任何 `internal:*`**）
- **口径澄清（本执行者独立复核）**：占位符为**拉丁串**的 zh 定义数量很大（`infiniband`/`makefile`/`marfe`/`s-alpha-beta`/`sdk` …），属 D2-3 已裁决**延后**的「低信息但未损坏」类，**不是** 48 行损坏类；W1 的 zh 损坏口径维持 **48 行**（`指“en”` 字面语言标签）
- commit `3f4e022`

### T0.3 — ✅ DONE（2026-10-26 16:30）
- 交付 `.github/plans/t4973-batches/`（117 文件 = 112 批文件 + 5 集合文件 + README）
- 生成命令：`.venv/bin/python scripts/registry_coverage_report.py --emit-lists .github/plans/t4973-batches --batch-size 20`
- `wc -l {w1_a,w1_b,w1_c,w2,w3}.ids` → `67 679 10 584 854`；`sort w2.ids w3.ids | uniq -d | wc -l` → `0`；`cat w1_b_b*.ids | wc -l` → `679`
- 批数实测：`w1_a 4 / w1_b 34 / w1_c 1 / w2 30 / w3 43` = **112 批**（`--batch-size` 为单一全局参数，故统一取 20；README 为批数唯一权威）
- 能失败证明（变异法）：副本删 `w1_b_b34.ids` 一行 → `679 → 678`
- commit `2bd593b`

### ⏸ 待裁决（阻塞 W1/W3 批次口径，未裁决前不进入 Phase 1/3）
1. **169 个 `preferred_zh == preferred_en` 且无 CJK 的 id**（`rfx-mod`/`c-2w`/`rexie`/`kmax`/`exl-50` …，多为装置代号）：`--mode names` 的 CJK 是硬要求 → 这些 id 永远无法通过；`--allow-latin-names` 按字面实现救不了。选项 A：维持字面 + 由 W3 为其补中文名；选项 B：令该名单同时豁免 CJK。
2. **W1 批次是否连 zh 行一起重写**：W1 的 `--mode definitions` 验收要求该 id 的 en/zh 行**同时**合规，而 W1 集合由 **en 套话**构成；这些 concept 的 zh 行多为 `指“X”` 模板（属 D2-3 延后的 1517 行）→ 若不重写 zh，**W1 批次无法通过验收**（口径冲突）。选项 A：W1 连 zh 一起重写（本批 +≈700 行、预估 +≈18 h）；选项 B：W1 批次改用 `--lang en` 验收，zh 模板留给后续批次。

### 已识别的环境/流程事实（跨会话须知）
- `scripts/batch_verify` 的 `def_source_unknown` 使 `internal:dict-improvements`（现有 **4583 行**）在 W1 批次内不可接受 → W1 改写时必须换为真实出处（与 D2-5 一致）
- PM 服务当前延迟劣化（p50 ≈ 9.6 s，偶发 15 s 超时）→ PM 写操作须先读回、避免批量

### W0 数据完整性修复 + 门禁加严 — T0.4 ~ T0.13

> 时间戳取自各 commit 的实际提交时间（`git log --format='%h %ci'`）。下方每条命令均可第三方复跑，输出为实测原文。
> 批次/映射/依据文件位于 `.github/plans/t4973-batches/`；门禁 RED→GREEN 全过程另见 `.github/plans/t4973-batches/red-green.md`。

#### T0.4 — ✅ DONE（2026-10-26 16:36）commit `e8012d8`
- 修复 99 行 category 左移（`bad_category 99 → 0`）；映射表 `.github/plans/t4973-batches/category-map-shift99.tsv`（按兄弟 concept / 规则 / 计划三分来源）
- `.venv/bin/python scripts/registry_row_audit.py --audit` → exit 0；实测 `data_rows 3076 | malformed_cols 80 | bad_category 0 | shifted_rows.count 0`
- **锚点不变**：`concept_ids_sha256 = c1c4e359…`（修复前后逐字一致 ⇒ 只改列结构，未增删 concept）
- 类别分布（99 行）：concept 40 / metric 17 / system 12 / device 11 / method 9 / material 9 / effect 1；抽检 12 行（8 列 + `$2 ∈ 16 类` + `$3` 为中文）→ 12/12 PASS
- 能失败证明（变异法）：副本中把一行 category 改回中文值 → `bad_category 0 → 1`，`--expect-clean` exit 1

#### T0.5 — ✅ DONE（2026-10-26 16:39）commit `dbfbc71`
- 80 行 6 列 → 8 列（补 `category` / `status` / `source`），原 `[domain: <label>]` 标记保留进 `notes`；映射表 `category-map-sixcol80.tsv`（39 兄弟推断 / 20 规则 / 21 计划）
- 复跑：`grep -c '\[domain: ' terms/registry/concepts.tsv` → `80`；`awk -F'\t' '!/^#/&&NF>0{print NF}' terms/registry/concepts.tsv | sort -u` → `8`；audit `cols_dist {8: 3076} | malformed_cols 0`
- 同批落地工作集清单 `t0_6{a,b}.ids`（40/40）与 `t0_7{a,b}.ids`（24/24）
- 能失败证明（变异法）：删 1 行 `[domain: ` → `80 → 79`

#### T0.6a / T0.6b — ✅ DONE（2026-10-26 16:58 / 16:59）commits `fa4d8e6` / `8135109`
- 80 行丢失的 `preferred_zh` 全部回填；依据文件 `names-basis-t0_6.tsv`（表头 + 80 行，含逐行来源）
- **关键事实（改变了本任务性质）**：这 80 个 concept 在 `aliases.tsv` 中**本来就有 `lang=zh kind=preferred` 别名**；损坏丢的是 `concepts.tsv` 的 `preferred_zh` **字段**，不是名字本身 ⇒ T0.6 是**字段回填**而非命名创作，无需仓外来源（计划 §T0.6 的 `--no-net` 分支即为此设）
- 复跑不变量：80/80 的 `preferred_zh` 非空且等于其 zh preferred 别名 → **PASS 80 / FAIL 0**
- 能失败证明：对 `t0_6a.ids` 中任一 id 清空 `preferred_zh` → 上句 FAIL 计数 0 → 1

#### T0.7a / T0.7b — ✅ DONE（2026-10-26 17:01 / 17:02）commits `a0cdab5` / `c2c4b7e`
- 48 行 `指“en”`（字面语言标签占位）zh 释义全部改写；依据文件 `defs-basis-t0_7.tsv`；来源标记 `corpus`（= 各 concept registry `notes` 的仓内依据）
- 复跑：`grep -c '指“en”' terms/registry/definitions.tsv` → `0`；audit `definitions.zh_en_corruption 0`
- RED 锚定（真实语料，非自造）：`git show HEAD~1:…` 计数 24（分两批各 24）／`git show f90e903:…` 计数 **48**
- **口径关联（实测）**：`t0_6{a,b}.ids` 与 `t0_7{a,b}.ids` 的交集 = **48** ⇒ 48 条损坏 zh 释义**全部**属于那 80 行畸形块，无一在块外（印证 R-2：中文名修复是 zh 释义修复的前置）

#### T0.8 — ✅ DONE（2026-10-26 17:03）commit `1e2cf30`
- `evidence.tsv` 规范化：213 行 4 列 + 214 行 5 列（`source` 列被粘进域名）→ 统一 5 列；另有 2 行 2 列
- 复跑：`awk` 列分布 → `{5: 3168}`；`grep -c '^internal:dict-improvements:' terms/registry/evidence.tsv` → `0`
- 66 个 domain 标签未丢弃：移入 `quote` 列（非空时追加为 `<quote> | domain: <label>`）
- 能失败证明（变异法）：副本中把一行 5 列截为 4 列 → `non5_cols 0 → 1`
- **改动量实测更正**：`git diff --numstat 1e2cf30^ 1e2cf30 -- terms/registry/evidence.tsv` → `429 429`，即**改动 429 行**
  （213 行 4 列 + 2 行 2 列 + 214 行 `source` 列粘连，并集恰 429）。计划 §T0.13 所述「evidence 规范化 642 行」为**误计**，以 **429** 为准
- commit message 曾因数字口径 amend 一次（`642 行` → 按实测改写）

#### T0.9 + T0.10 — ✅ DONE（2026-10-26 19:02）commit `08a2e98`（同一 commit，防 CI 红）
- `pipeline/validate_registry.py`（sha256 `f2e7f196…`）新增三门严格结构检查：`_ALLOWED_CATEGORIES`（16 类）、`_CONCEPT_COLUMN_COUNT = 8`、`_EVIDENCE_COLUMN_COUNT = 5`
- 次序设计：结构门置**语义检查之后**（保持 `tests/test_validate_case_leak.py` 绿，同时畸形行不再静默通过）
- `tests/test_registry_validator.py`（sha256 `a9a3d2e5…`）扩到 15 用例；`_MINIMAL_EVIDENCE` 改 5 列；新增 3 个真实语料锚定用例
- fixture 与历史逐字节一致：`pre_fix_concepts_shift.tsv` ← `f90e903` 行 3171-3173；`pre_fix_concepts_sixcol.tsv` ← 行 3316-3318（`diff` 无输出）
- **边界扩展（已记录）**：计划仅声明改 1 个测试文件，实际另机械补 tab 修改 8 个测试文件的合成 fixture（无逻辑/断言改动），并把 1 行陈旧 fixture 的 `component` 改为 `concept`（真实语料 `central-solenoid` 实为 `concept`；`component` 不在 16 类白名单，仅作为 `preferred_en` 出现）。理由：本任务验收要求全仓 `pytest` exit 0，且 RK2 禁止红 CI；替代方案（留 20 个陈旧 fixture 用例红）被否
- 能失败证明（受控实验，见 `red-green.md` §3）：同语料、只换 validator → 旧 `1e2cf30` 对三类畸形语料**全部 exit 0（静默通过）**，新 `08a2e98` **全部 exit 1**；未变异对照两者皆 exit 0

#### T0.11 — ✅ DONE（2026-10-26 19:50）commits `a4ac8d8`（门禁剖面修正）+ `5ed2127`（记录）
- 交付 `.github/plans/t4973-batches/red-green.md`：①命令原文 ②修复前 exit 1 输出 ③修复后 exit 0 输出 ④加严前后 exit 码对比表 ⑤fixture ↔ 历史行号对应
- 验收：`grep -c "exit" …/red-green.md` → **25**（≥6）；`scripts/registry_row_audit.py --expect-clean` → **exit 0**；`git show f90e903:terms/registry/concepts.tsv | sed -n '3316p' | awk -F'\t' '{print NF}'` → **6**
- **门禁剖面修正（已记录，属脚本改动）**：`--expect-clean` 原先把 W1 质量指标（`en_boilerplate`、`concepts_without_defs`）也纳入 gate ⇒ Phase 0 的完成定义在 Phase 0 永远无法 exit 0。改为 `--expect-clean` = **W0 结构集**（= 计划 Phase 0 列举的 5 项 + `bad_category`/`glued_source_rows`），新增更严格的 `--expect-clean-all` = 全集。`--audit` 仍报告全部指标，`is_clean`/`non_zero_metrics` 语义不变 ⇒ **未削弱任何检查**
- RED 保留实测：修复前三表 `--expect-clean` → **exit 1**，5 项非零（80/99/215/427/48）与 §T0.1 基线逐项一致

#### T0.12 — ✅ DONE（2026-10-26 19:51）commit `c781afc`
- 命令（串行，顺序不可换，因多个测试读 `artifacts/`）：
  1. `.venv/bin/python -m pipeline.export_registry --translation-dict --query-expansions --substitutions --tag-rules` → exit 0
  2. `.venv/bin/python -m pipeline.build_terms --config config.toml` → exit 0（`wrote artifacts/domain_terms.txt (3462 terms)`）
- 三项污点，运行前 → 运行后**同产物实测对照**：`translation_dict.json` 的 `'en'` 值 **166 → 0**；`query_expansions.json` 非 ASCII category **99 → 0**；`tag_rules.jsonl` 非 16 类 category **720 → 0**
- `wc -l artifacts/domain_terms.txt` → **3462**（W0 不增删 allowlist，故应恒等；实测恒等）
- 能失败证明（变异法）：经 `--terms-dir/--out-dir` 在**仓外**副本上把 1 行 `preferred_zh` 改成 `en` 重跑导出 → `'en'` 值 = **1**（≥1）；未变异对照 = **0**（仓内文件零触碰）
- 仅 `artifacts/translation_dict.json` 属 git tracked（其余为 gitignored）；提交时只说明指标变化

#### T0.13 — ✅ DONE（2026-10-26）本节 commit
- `CHANGELOG.md` 新增 `Unreleased` 条目；本节追加 W0 记录；commit message 使用 `feat(registry): …`（按 §T0.13 风险说明，避免非完成词）
- Phase 0 完成定义（一条命令）：`.venv/bin/python scripts/registry_row_audit.py --audit --expect-clean` → **exit 0**
- 全量门禁：`pytest -q` / `ruff format --check .` / `ruff check .` / `mypy pipeline/ --ignore-missing-imports` / `python -m pipeline.validate_registry` → **全部 exit 0**
- 能失败证明（实现回退法）：故意保留 1 行 6 列 concept → `--expect-clean` exit 1（本任务不得标记完成）

#### W0 收口数字（供 Phase 1–4 引用）
- registry：`3076` concepts（全 8 列）/ `10249` aliases / `3168` evidence rows（全 5 列）/ `6132` definitions
- 覆盖率（计划 §D 口径）：total 3076 / covered **1449** / uncovered **1627** / **47.11%**；`W2 738`（multiword 668 / single 70）／`W3a 854`／`proper_excluded 35`
  - 与 §T0.0 追加时相比 W2 由 584 → **738**（畸形行变为可计数），W3a 854 不变
- **本计划的 §D1 口径更正**（权威数字以本节为准）：覆盖率 `46.3%` → **`47.11%`**；`proper_excluded` `36` → **`35`**；T0.8 的 `wc -l == 3168` 表述应读作 **audit `data_rows == 3168`**（`evidence.tsv` 文件 `wc -l` 为 3217，含 47 空行 + 2 注释，修复前后均如此）；T0.13 所述「evidence 规范化 642 行」→ **429 行**（`git diff --numstat` 实测）
- **W0 修复量实测汇总**：概念行结构修复 **179 行**（99 行 category 左移 + 80 行 6 列）；`preferred_zh` 字段回填 **80 行**；zh 释义重写 **48 行**；`evidence.tsv` 规范化 **429 行**；三道污点归零（166 / 99 / 720 → 0 / 0 / 0）

#### W0 收尾裁决与追认（2026-10-26，用户在本会话 question 工具以结构化选项选定）

| # | 事项 | 裁决 | 影响 |
|---|------|------|------|
| D2-8 | W1 释义来源白名单 | **A. 允许仓内依据 `corpus`**（仅当释义显式引用外部权威时才要求 URL/`GB/T`/`ITER`/`IAEA`） | 解除 Phase 1 阻塞；W1 679 行可依仓内 `notes` / 既有 zh 释义改写，无需逐条上网取证 |
| 追认 1 | T0.9/T0.10 **修改边界扩展** | **A. 追认保留** | 保留 8 个测试文件的机械补 tab 改动 + 1 行陈旧 fixture 修正（`component` → `concept`）；commit `08a2e98` 与计划 Execution Log 中的偏差记录作为正式口径 |
| 追认 2 | `--expect-clean` **门禁剖面拆分** | **A. 追认保留** | `--expect-clean` = W0 结构集（= 本计划 Phase 0 完成定义）；`--expect-clean-all` = 全集（Phase 1 完成时使用）；commit `a4ac8d8`。计划原文「`--expect-clean` = 全部指标为 0」的字面表述以本条为准 |
| 授权 | **push** | **A. 不 push** | W0 的 20 个 commit 保持本地；远端不反映 W0 成果。后续如需 push 须再次显式授权（三要素齐备） |
| 裁决 3 | **zh 定义 ingestion 残留的处置** | **A. 授权一次性清扫 + 新增检测指标** | W1 收尾时执行一次**独立清扫提交**（覆盖**非 W1 集**的全部残留行），并为 `scripts/registry_row_audit.py` **新增**残留检测指标（新增 = 加严，不削弱既有门禁；纳入 `--expect-clean-all`）。W1 期间保持「批次内恢复性修复」策略（仅修本批 zh 行的 a)/b) 类残留；c) 类词头属编辑性，不在批次内改） |

---

### W1 definitions 质量重写 — T1.A* / T1.B* / T1.C*

> 每个批次 = 一个 `-EN` 子任务 + 一个 `-ZH` 子任务（D2-7=A：en/zh 双侧）；下方每条按**批次**记录（含两个子任务的证据）。
> 提交策略：数据改动与该批次的日志条目同 commit（避免为日志翻倍提交数）。门禁 RED→GREEN 复跑法见 `.github/plans/t4973-batches/red-green.md` 同类做法。

#### T1.A1-EN / T1.A1-ZH — ✅ DONE（2026-10-26 20:19）commits `e2e2809`（-EN）+ 本节（-ZH）

- 批次：`.github/plans/t4973-batches/w1_a_b01.ids`（**20** id）；属 **W1-A 组**（en 为套话 + zh 已有真实 GB/T 释义）
- **`-EN`**：20 条 `en` 行改写为真实英文技术释义（依据 = 该 concept 的仓内 GB/T zh 释义）
  - 命令：`.venv/bin/python scripts/registry_batch_verify.py --mode definitions --ids-file .github/plans/t4973-batches/w1_a_b01.ids --expect 20 --lang en` → **exit 0** `verdict=PASS`
  - 套话黑名单 **0/20**；en 最短长度 **70** 字符（≥40）；全部 ASCII
  - source：**19×** `GB/T-4960.9` + **1×** `corpus`（`x-point`——其 GB/T zh 行正文为纯交叉引用 `参见单/双零(2.2.122)。`，无定义性内容，依据改取该 concept 的 `concepts.tsv` notes，属 D2-8=A 允许的仓内依据）
  - 迁移实测（同一文件前后）：`internal:*` **4535 → 4515**；`GB/T-4960.9` **551 → 570**；`corpus` **48 → 49**；audit `en_boilerplate` **746 → 726**
  - **提交前裁决（父代理）**：`x-point` 草案含 divertor/separatrix 从句，经查 `notes`（`Null point of poloidal magnetic field`）与该 zh 行**均无此内容** ⇒ **删除**该从句（保留有据的核心 + 释义展开，110 字符）；`plasma-gun` 草案 70 字符**维持**（与 GB/T zh「用来产生高速等离子体团的设备。」逐字对应、零编造，不加无据内容凑长度）
- **`-ZH`**：zh 侧机械门禁**本已通过**（`--lang zh` 与 `--lang both` 均 exit 0，即 W1-A 的 zh 行本就是真实 GB/T 内容）⇒ 本子任务为**稀疏修复**而非重写
  - 修复 3 条 zh 行的**转换残留**（恢复性修复，非语义变更，`source` 不变）：
    | id | before → after |
    |----|---------------|
    | `lawson-criterion` | `…乘积大于 2 times 10^20 ~m^-3 ~s 。` → `…乘积大于 2×10^20 m^-3·s。` |
    | `magnetic-island` | `在非理想等粒子体中` → `在非理想等离子体中`（同句后半已写「等离子体」⇒ 自证讹字） |
    | `vertical-displacement-event` | `高拉长比的等离子 体更有` → `高拉长比的等离子体更有` |
- **能失败证明**（仓外副本 + `--repo-root`，**零触碰仓内文件**；未变异对照均 exit 0）
  - en 侧：`def_boilerplate_regex`（复原套话）／`def_len_en`（10 < 40）／`def_source_unknown`（`internal:dict-improvements`）→ 三者均 **exit 1**
  - zh 侧：`def_len_zh`（3 < 12）／`def_lang_placeholder`（含 `指“en”`）／`def_count_zh`（删除该 id 的 zh 行 → `expected exactly 1 zh row, found 0`）→ 三者均 **exit 1**
- 不变量：`data_rows` 恒 **6132**；列分布恒 `{4}`；改动面 `git diff --numstat` = `20/20`（-EN）+ `3/3`（-ZH）；改动 (id,lang) 对恰为批次 id，en 侧 0 条 zh 行被误改
- 全量门禁：`pipeline.validate_registry` / `pytest -q` / `ruff format --check .` / `ruff check .` / `mypy pipeline/` / `registry_row_audit --audit --expect-clean` → **全部 exit 0**

#### 已知观察 #1（**非阻断**，plan_ref = 本节）— zh 定义的「转换残留」类缺陷不在任何门禁覆盖内

- **现象**：`definitions.tsv` 的 zh 行存在 ingestion 残留，**W0 结构门禁与 W1 批门禁均不检测**：
  a) LaTeX 命令残留 `sim` / `times` / `cdot`：实测 4 行（`low-beta-plasma`、`low-temperature-plasma`、`glow-discharge-plasma`、`radio-frequency-wave`）
  b) 字符讹误 / 多余空格：如 `等粒子体`、`等离子 体`、`传感 器`、`³ H e`（`dd-reaction`）
  c) GB/T **词头前缀 + 空格**（约 15 行）：如 `孔栏 安装…`、`β 值 等离子体压强…`、`环流器 意为…`、`限制器` 对应 GB/T 词头 `孔栏` 未出现在 `aliases.tsv` —— 属**编辑性**变更，且牵涉命名/别名口径
- **实测规模**（2026-10-26，模式族扫描并已人工剔除假阳性如 `~100-200 GHz`、`TCL Modules`）：真缺陷族 **≤25 行**
  - 其中落在 **W1 集仅 7 行**（随 W1 批次自然修复，本批已修 3 行）
  - 其余 **~18 行**落在 W2（15）／W3（1）／**不在任何工作集（~15，多为已覆盖概念）**——这些行**不在任何阶段的 `modifications` 清单内**，不加处置将在计划结束后**残留**
- **本批处置**：仅在本批 20 行内做 a)/b) 类恢复性修复（3 行）；c) 类（`limiter` 词头）判为编辑性 → **不越界修改**
- **建议（待裁决，不阻断执行）**：① 登记「definitions zh 残留清扫」任务，或把 a)/b) 类并入 W2/W3 批次的同一 commit（需扩展相应任务的 `modifications` 边界）；② 为 `registry_row_audit.py` **新增**残留检测指标（新增 = 加严；不削弱任何既有门禁），使该类缺陷可量化、可回归

#### T1.A2-EN / T1.A2-ZH — ✅ DONE（2026-10-26 21:20）commits `89a2fb2`（-EN）+ 本节（-ZH）

- 批次：`.github/plans/t4973-batches/w1_a_b02.ids`（**20** id）；W1-A 组
- **`-EN`**：20 条 `en` 行由套话改写为真实释义（依据 = 各 concept 自身的 GB/T zh 释义）
  - 门禁：`registry_batch_verify.py --mode definitions --ids-file …/w1_a_b02.ids --expect 20 --lang en` → **exit 0** `verdict=PASS`
  - en 最短 **46** / 最长 551 字符；套话 0/20；全 ASCII；source：**20/20** `GB/T-4960.9`（0 `corpus`、0 `internal:*`）
  - 迁移：`internal:*` 4515 → **4495**；`GB/T-4960.9` 570 → **590**；audit `en_boilerplate` 726 → **706**
  - **提交前裁决**：`turbulent-transport`（GB/T zh 仅 13 字 ⇒ en 49 字符）**维持**，与 T1.A1 `plasma-gun` 同口径（忠实依据 > 凑长度）；GB/T 条款号 `(2.1.284)`/`(2.4.47)` **去除**（非技术事实，与 T1.A1 `tearing-mode` 先例一致）；`toroidal-alfven-eigenmode` 释义**维持**按指定依据措辞（与 `preferred_en` 对齐属命名/别名域）
- **`-ZH`**：本批 zh 侧**被门禁抓到真实 RED**（非人工构造）——`def_len_zh: electrostatic-confinement [zh]: 10 chars < required 12`，`--lang zh` **exit 1**
  - 修复 2 条 zh 行后 `--lang zh` **exit 0**、`--lang both` **exit 0**：
    | id | before → after | 依据 |
    |----|---------------|------|
    | `electrostatic-confinement` | `用电场约束等离子体。`（10） → `利用静电场对等离子体进行约束。`（15） | GB/T zh 行（`用电场约束等离子体`）+ 术语名「静电约束」；**未**引入 notes 中的 `fusor/polywell`（否则 source 须改 `corpus` 且与已提交的 en 侧不对称）。source 不变 `GB/T-4960.9` |
    | `halo-current` | `…流动的电流。 注：…` → `…流动的电流。注：…` | 标点后多余空格（恢复性） |
- **不变量 / 全量门禁**：`data_rows` 恒 **6132**；列分布恒 `{4}`；`git diff --numstat` = `20/20`（-EN）+ `2/2`（-ZH）；zh 行改动数 0（-EN 阶段整文件核验）；`validate_registry` / `pytest -q` / `ruff format --check .` / `ruff check .` / `mypy pipeline/` → 全部 **exit 0**

#### 清扫清单（滚动更新；W1 收尾执行，裁决 3 = A）

> 检测口径：对 `definitions.tsv` 逐行匹配下列模式（本表数字为 2026-10-26 21:20 实测，模式在 W1 收尾时须经 `--self-test` + 真实语料锚定后固化）。
> **注意**：类 1 的 `times/sim/cdot` 在 **en 行**存在合法英文用法（如 `… 10 times …`）⇒ 检测器**限定 zh 行**并需覆盖粘连形式（`20MHzsim`、`50mAcdot`），否则会误报。

| # | 类 | 判据（模式） | 实测规模 | 处置 |
|---|----|-------------|---------|------|
| 1 | LaTeX 命令残留 | `(times\|sim\|cdot)`（zh 行、含粘连） | **5 行** zh | ✔ 恢复性清扫 |
| 2 | 字符讹误 / 多余空格 | `CJK<sp>CJK` ／ `[。，、；：]\s+CJK` ／ `CJK[a-z]{3,}CJK` | **36 行** zh | ✔ 恢复性清扫 |
| 3 | 字段首尾空白 | 任一分量 `x != x.strip()` | **18 行**（**全为 en 行**，IAEA 源，形如 ` The ability of…`） | ✔ 恢复性清扫 |
| 4 | GB/T 词头前缀 | `^[CJK]{2,8} [CJK]` 或 `^[CJK]{2,8} [A-Za-z]` | **31 行** zh | ⚠ **编辑性**，须单独裁决（牵涉命名/别名口径） |
| 5 | GB/T 条款号 `(2.1.284)` | `\(\d+\.\d+(\.\d+)?\)` | **49 行** zh | ✘ **保留**（zh 侧为真实 GB/T 溯源信息） |
| 6 | en 行 < 40 字符 | — | **338 行**（IAEA `See X.` 词汇交叉引用存根，**W1 内 0**） | ✘ **排除**（合法词汇条目，非残留；**勿改**） |

- **恢复性并集（类 1 ∪ 2，zh）= 39 行**：W1 内 **5** ／ W2 **24** ／ W3 **3** ／ **不在任何工作集 7**（`advanced-takamak` 等见下）
- **不在任何工作集的 7 个 id**：`advanced-tokamak`、`collective-dose`、`cryostat`、`environment-module`、`mhd-stability-limit`、`plasma-frequency`、`tokamak`
- **清扫范围**（W1 收尾执行，裁决 3 = A）：类 1+2+3（= 39 zh + 18 en = **57 行**）减去 W1 集内的 5 行 ⇒ **≈52 行**；**类 4 单独裁决**；类 5/6 **不动**
- **测量口径纠错记录**：初测报「类 3 = 18 行」后又出现「0 行」，经三方方法（`splitlines`／`csv.reader`／`git show HEAD`）交叉复核确认 **18 行**；「0」系脚本默认参数 `rs=zh` 导致的**统计 bug**（该类命中全在 **en** 行），非数据变化。另：类 1 初测 3~4 行、现测 5 行，差异来自粘连形式（`MHzsim`/`mAcdot`）与 1 个新命中，检测器须固化后再定稿

#### T1.A3-EN / T1.A3-ZH — ✅ DONE（2026-10-26 21:15）commits `2a01af3`（-EN）+ 本节（-ZH）

- 批次：`.github/plans/t4973-batches/w1_a_b03.ids`（**20** id）；W1-A 组
- **`-EN`**：20 条 `en` 行由套话改写为真实释义（依据 = 各 concept 自身的 GB/T zh 释义）
  - 门禁：`registry_batch_verify.py --mode definitions --ids-file …/w1_a_b03.ids --expect 20 --lang en` → **exit 0** `verdict=PASS`
  - en 最短 **61** / 最长 513 字符；套话 0/20；全 ASCII；source：**20/20** `GB/T-4960.9`
  - 迁移：`internal:*` 4495 → **4475**；`GB/T-4960.9` 590 → **610**；audit `en_boilerplate` 706 → **686**
  - **未知情面**：本批 3 个 id（`dt-reaction`/`dd-reaction`/`d-he3-reaction`）的 zh 行含公式 mojibake；en 侧**未复制**畸形写法，直接写正确 ASCII 物理量（`D + T -> n + He-4 + 17.6 MeV` 等）；zh 侧修复见 `-ZH`
- **`-ZH`**：zh 门禁原本已 PASS（无机械 RED），但**人工审读发现类 7（公式/数字 mojibake）**——3 行修复（纯「去除转换器插入的空格」恢复性修复，不改语义、不改 source）：

  | id | before → after | 类 |
  |----|---------------|-----|
  | `dt-reaction` | `D + T → n + ⁴ H e + 1 7. 6 M e V` → `D + T → n + ⁴He + 17.6 MeV` | 7a+7c |
  | `dt-reaction` | `(D-Treaction)或氘-氚燃烧(D-Tburn)` → `(D-T reaction)或氘-氚燃烧(D-T burn)` | 7e（空格被删） |
  | `dd-reaction` | `。 反应式为` → `。反应式为`；`D + D → n + ³ H e` → `D + D → n + ³He` | 2c+7a |
  | `d-he3-reaction` | `D + ³ H e → p + ⁴ H e + 1 8. 4 M e V` → `D + ³He → p + ⁴He + 18.4 MeV` | 7a+7c+7b |

- **不变量 / 全量门禁**：`data_rows` 恒 **6132**；列分布恒 `{4}`；`git diff --numstat` = `20/20`（-EN）+ `3/3`（-ZH）；`--lang zh` / `--lang both` **exit 0**；`validate_registry` / `pytest -q` / `ruff format --check .` / `ruff check .` / `mypy pipeline/` → 全部 **exit 0**
- **zh 上标书写约定（本批确立）**：zh 释义中同位素写**上标式** `³He`/`⁴He`（与 `fusion-cross-section` 的 `D-³He`、`concepts.tsv` 中 `d-he3-reaction` 的 `preferred_zh = D-³He反应` 一致），**不**写 `He-3`/`He-4`（后者是 en 侧约定）

#### 清扫清单（滚动更新 — 类 7 新增）

| # | 类 | 判据（模式） | 实测规模 | 处置 |
|---|----|-------------|---------|------|
| 1 | LaTeX 命令残留 | `(times\|sim\|cdot)`（zh 行、含粘连） | **5 行** zh | ✔ 恢复性清扫 |
| 2 | 字符讹误 / 多余空格 | `CJK<sp>CJK` ／ `[。，、；：]\s+CJK` ／ `CJK[a-z]{3,}CJK` | **36 行** zh | ✔ 恢复性清扫 |
| 3 | 字段首尾空白 | 任一分量 `x != x.strip()` | **18 行**（全为 en 行，IAEA 源） | ✔ 恢复性清扫 |
| 4 | GB/T 词头前缀 | `^[CJK]{2,8} [CJK]` 或 `^[CJK]{2,8} [A-Za-z]` | **31 行** zh | ⚠ **编辑性**，须单独裁决 |
| 5 | GB/T 条款号 `(2.1.284)` | `\(\d+\.\d+(\.\d+)?\)` | **49 行** zh | ✘ **保留** |
| 6 | en 行 < 40 字符 | — | **338 行**（IAEA `See X.` 存根，W1 内 0） | ✘ **排除**（勿改） |
| 7 | **公式/数字 mojibake**（转换器在 token 内部插/删空格） | 精确模式三条（见下） | **7 行**：W1 3（本批已修）+ 集外 4 | ✔ 恢复性清扫 |

- **类 7 精确模式**（经人工逐条判定；naive 模式（`[A-Za-z]\s+[A-Za-z]` 或 `[CL]\s[CL]`）误报率极高，**不得直接用**）：
  1. `(?<![A-Za-z])[A-Za-z]\s+[a-z](?![A-Za-z])` — 字母+空格+单小写字母（`L i`、`H e`、`B m`）
  2. `[A-Za-z]\s+[\u2070-\u209f]` — 字母+空格+上/下标（`H ₂`、`B ₀`）
  3. `\d\s+\d\s*\.\s*\d` — 空格拆开的十进制（`1 7. 6`）
  4. `(?<![A-Za-z])[A-Z]-[A-Z][a-z]{3,}(?![A-Za-z])` — 空格被删（`D-Treaction`）
- **类 7 已知假阳性**（须在检测器中排除）：`Σ_T w_T·H_T`（合法数学记号，命中 `T w`）；英文散文（`half-life-t`、`risk`）；`1 V·s` / `4 K` / `5 b`（数字-单位间的合法空格，命中模式 1 的宽版）；`N-Particle`（`MCNP` 全称，合法）
- **类 7 全清单（7 行）**：`dd-reaction`、`d-he3-reaction`、`dt-reaction`（**W1，本批已修**）；`breeder`、`mirror-ratio`（集外）；`dissociative-recombination`、`magnetic-mirror-configuration`（W2）
- ⚠ **内容丢失变体**：`breeder` 的 `⁴ H e` 被转换器**整段删除**（残留 `L i + n → T + + 4. 8 M e V`，正反应为 `Li + n → T + ⁴He + 4.8 MeV`）——该类需**重建内容**而非仅去空格，W1 收尾清扫时须单独裁决
- **检测器落地要求（W1 收尾，裁决 3=A）**：`scripts/registry_row_audit.py` 新增该类指标时须带 `--self-test` + **真实语料锚定**（含上列假阳性负例），并覆盖粘连形式；**不得**仅凭上述粗模式直接写入门禁

#### T1.A4-EN / T1.A4-ZH — ✅ DONE（2026-10-26 21:20）commits `ec556e9`（-EN）+ 本节（-ZH）

- 批次：`.github/plans/t4973-batches/w1_a_b04.ids`（**7** id）；W1-A 组**收尾批**
- **`-EN`**：7 条 `en` 行由套话改写为真实释义（依据 = 各自 GB/T zh 释义；7/7 zh 行均含定义性内容 ⇒ 0 条走 `corpus`）
  - 门禁：`--ids-file …/w1_a_b04.ids --expect 7 --lang en` → **exit 0** `verdict=PASS`
  - en 最短 **72** / 最长 184；套话 0/7；全 ASCII；source **7/7** `GB/T-4960.9`
  - 迁移：`internal:*` 4475 → **4468**；`GB/T-4960.9` 610 → **617**；audit `en_boilerplate` 686 → **679**
  - **裁决 2 项（均接受）**：① `in-vessel-component` zh 行折行残迹 `诊断传感 器` 按 `diagnostic sensors` 读（语义无歧义，zh 侧本批修复）；② `radio-frequency-heating` 的 GB/T 条款号 `(2.1.246)` 不写入 en，交叉引用按允许口径保留为 `See also radio-frequency wave.`
- **`-ZH`**：zh 门禁原已 PASS；修复 1 行恢复性缺陷：

  | id | before → after | 类 |
  |----|---------------|-----|
  | `in-vessel-component` | `诊断传感 器等` → `诊断传感器等` | 2b（CJK 内插空格） |

  - `radio-frequency-heating` 的词头 `RF加热 ` 判为**类 4b（拉丁缩写 + 中文词头）编辑性**，**不动**
- **不变量 / 全量门禁**：`data_rows` 恒 **6132**；列分布恒 `{4}`；`git diff --numstat` = `7/7`（-EN）+ `1/1`（-ZH）；`--lang zh` / `--lang both` **exit 0**；`validate_registry` / `pytest -q` / `ruff format --check .` / `ruff check .` / `mypy pipeline/` → 全部 **exit 0**

#### W1-A 组收口 ✅（4/4 批次，67 id）

| 批次 | ids | -EN commit | -ZH commit |
|------|-----|-----------|-----------|
| T1.A1 | `w1_a_b01`（20） | `e2e2809` | `05b7223` |
| T1.A2 | `w1_a_b02`（20） | `89a2fb2` | `c87e1ba` |
| T1.A3 | `w1_a_b03`（20） | `2a01af3` | `d924a94` |
| T1.A4 | `w1_a_b04`（7）  | `ec556e9` | 本节 |

- **组级验收**：`registry_batch_verify --mode definitions --ids-file …/w1_a.ids --expect 67 --lang both` → **exit 0**（67 id 双侧全绿）
- **组级迁移（W1-A 累计）**：`internal:*` 4535 → **4468**（−67）；`GB/T-4960.9` 551 → **617**（+66）；`corpus` 48 → **49**（+1，`x-point`）；audit `en_boilerplate` 746 → **679**（−67）
- **组内裁决累计**：`x-point` 无据从句删除；`plasma-gun` / `turbulent-transport` 简短但忠实（维持）；GB/T 条款号统一不写入 en；`limiter` 词头（类 4）与 `RF加热` 词头（类 4b）编辑性不动；`toroidal-alfven-eigenmode` 措辞按指定依据
- **组内 zh 恢复性修复累计 9 行**（~~原文写 7~~，2026-10-27 账面纠正：逐项清单实为 9 行，见 §「会话恢复 — Bookkeeping 纠正」）：`lawson-criterion`、`magnetic-island`、`vertical-displacement-event`（A1）；`electrostatic-confinement`（门禁 RED，A2）、`halo-current`（A2）；`dt-reaction`、`dd-reaction`、`d-he3-reaction`（A3，类 7）；`in-vessel-component`（A4）
- **下一步**：进入 W1-B 组（34 批次 / 679 id）（~~694~~，2026-10-27 账面纠正：`w1_b.ids` 实测 679），并在第 5 个批次完成时执行 **D2-4 抽检**（该 cadence 表述见 §「会话恢复 — Bookkeeping 纠正」第 3 条定稿版）

#### 裁决 4 — `registry_batch_verify.py --self-test` 重锚（**off-plan**，用户裁决 A）— ✅ DONE（2026-10-26 21:30）

- **触发**：T1.B01-EN 期间由子代理上报、父代理独立复核：`--self-test` = **18/24 exit 1**；T0.2 落地时（§285-290 / §1155）记录为 **24/24 exit 0** ⇒ **回归**
- **根因（已定位并复核）**：6 条失败断言**全部**是「**锚点行被 W0 修好 ⇒ 规则不再触发**」，涉及 4 条规则：`concept_cols`（`concepts.tsv:3316`，W0 修成 8 列）、`names_zh_no_cjk`（`:3171`，zh 恢复 `能源安全`）、`def_boilerplate_mark` + `def_lang_placeholder`（`definitions.tsv:5838`，W0 T0.7a/b 修好 48 行 `指“en”`）
  - 同时刻语料实测：非 8 列 `concepts.tsv` 数据行 = **0**；含 `指“en”` 的 `definitions.tsv` 行 = **0** ⇒ 锚点目标已不存在
  - **规则本身未坏**：W1 每批均以「仓外副本 + `--repo-root`」变异法复证各规则会 exit 1（B01-EN：`def_boilerplate_regex` / `def_len_en` / `def_source_unknown` → 三者 exit 1，未变异对照 exit 0）
- **裁决**：用户选 **A. 立即修复（独立 commit，不并入 W1 收尾加固）**
- **做法（不削弱任何门禁）**：在**临时副本**中「就地重建」那 3 处历史缺陷（行数不变）⇒ **24 条断言与全部 `file:line` 锚点逐字保持不变**，规则**一条不改、不加、不减**。新增 `SELF_TEST_RESTORED_CASES = frozenset({0,1,3})` + `_build_restored_defect_corpus(real_root, dest)`；仅这 3 个用例改跑副本，其余 5 个仍跑真实语料；副本目录 `tempfile.mkdtemp` + `finally` 清理；**只写 `dest`，仓库文件零触碰**
  - 副本重建内容：`poloidal-field-power-supply` → `fields[:6]`；`energy-security` → `fields[COL_ZH] = fields[COL_EN]`；`adjoint-flux` zh 行 → `聚变/核工程术语，指“en”这一技术概念。`
  - 行切分用 `read_text().split("\n")` / `"\n".join(…)`（**不用** `splitlines()`，后者会在 `\x0b`/`\x0c`/`\u2028` 处切分而移动行号）
- **RED → GREEN**：修复前 `18/24 exit 1` → 修复后 **`24/24 exit 0`**
- **能失败证明（5 变体，脚本副本 + `--repo-root <真实仓库>`，仓内文件零触碰）**：

  | 变体 | 变异 | 实测 |
  |------|------|------|
  | `m1_boilerplate_regex` | `BOILERPLATE_EN_RE` 前置 `(?!)`（永不匹配） | `22/24`，**exit 1** |
  | `m2_concept_cols` | `concept_cols` 守卫放宽（6 列被放过，两处） | `22/24`，**exit 1** |
  | `m3_lang_placeholder` | `LANG_PLACEHOLDER_RE` → `(?!)` | `23/24`，**exit 1** |
  | `m4_control` | 不修改（对照） | `24/24`，**exit 0** |
  | `m5_no_restore` | `SELF_TEST_RESTORED_CASES = frozenset()`（禁用重建副本） | `18/24`，**exit 1**，6 条失败与修复前**逐条一致** |

  - `m5` 是**本次修复自身的承重证明**：变绿源于夹具重锚，**不是**规则被削弱的副作用；亦构成反例锚定（将来若禁用重建或让重建空转，`--self-test` 必须回到 18/24）
- **文件改动面**：`git diff --numstat` = `99/14`，仅 `scripts/registry_batch_verify.py`（972 → **1057** 行；sha256 `6fa9f254…` → `35d234b3…`）+ 新增证据文件 `.github/plans/t4973-batches/self-test-reanchor.md`
- **全量门禁**：`--self-test` / `pipeline.validate_registry` / `pytest -q` / `ruff format --check .` / `ruff check .` / `mypy pipeline/` / `registry_row_audit --audit --expect-clean` → **全部 exit 0**
- **不动**：`red-green.md`（T0.11 冻结交付，其记录的实测值不改）；§1155 中 T0.2 的 972 行 / sha256 保留为交付时点事实并加后记

#### T1.B01-EN / T1.B01-ZH — ✅ DONE（2026-10-26 21:35）commits `b578047`（-EN）+ 本节（-ZH）

- 批次：`.github/plans/t4973-batches/w1_b_b01.ids`（**20** id）；**W1-B 组首批**（34 批 / 679 id）
- **W1-B 与 W1-A 的分型差异**（执行前实测确认）：W1-B 的 **`en` 与 `zh` 双侧皆为占位/模板**（en = `Fusion/nuclear engineering term referring to 'X'…`；zh = `聚变/核工程术语，指“X”这一技术概念。`），双侧 source 均 `internal:dict-improvements` ⇒ **无 GB/T 真实释义可依据**，依 **裁决 D2-8=A** 以 concept 的 `notes`（仓内语料）+ 同 id 已提交的 en 行为依据 ⇒ source 一律 **`corpus`**
- **`-EN`**（commit `b578047`）：20 条 `en` 行改写
  - 门禁：`--ids-file …/w1_b_b01.ids --expect 20 --lang en` → **exit 0** `verdict=PASS`
  - en 最短 **112** / 最长 230；套话 0/20；全 ASCII；source **20/20** `corpus`
  - 迁移：`internal:*` 4468 → **4448**；`corpus` 49 → **69**；audit `en_boilerplate` 679 → **659**
  - **裁决 4 项（均接受）**：① `quench-detection` **不补**检测原理（属 notes 之外的机理细节）；② `sputtering`/`erosion`/`plasma-facing-component`/`magnet-feeder`/`superconducting-joint`/两条场线圈共 6–7 条 notes 偏薄的行，按教科书级**类别/功能**表述（未引入新实体、数值、项目名）；③ HTS/LTS 的 `30 K` 与材料族（`REBCO/YBCO/Bi-2212`、`NbTi/Nb3Sn`）**逐字见于 notes** ⇒ `corpus` 正确；④ 子代理上报的 `--self-test` 回归**不在本批修复**（属计划外文件 + 门禁脚本）⇒ 已单独走裁决流程（见上文「裁决 4」条，commit `471ab41`）
- **`-ZH`**（本节）：20 条 `zh` 行由模板改写为真实释义（与同 id 已提交 en **语义等价**，依据 = notes + en；source **20/20** `corpus`）
  - 门禁：`--lang zh` → **exit 0**（改写前为 `verdict=FAIL`，20 条 `def_boilerplate_mark` + `def_source_unknown`，属**设计内**的红）；`--lang both` → **exit 0**
  - zh 最短 **29** / 最长 58（均值 43.2）；模板 0/20；`指“en”` 0/20；source **20/20** `corpus`
  - 迁移：`internal:*` 4448 → **4428**；`corpus` 69 → **89**；audit `en_boilerplate` **659 → 659**（en 行零改动）
  - **本批自校一处**：两条 HTS/LTS 初稿写 `30K`（紧贴），复核仓内最近邻（`nb3sn` `T_c=18 K`、`nbti` `9.2 K`、`rebco` `92 K`）与 en 侧（`30 K`）均为**带空格**写法 ⇒ 规范为 `30 K`（纯格式，不改语义、不改 source）
  - 委派申报「无阻塞裁决项」；唯一的**非阻断**提请知悉：`toroidal-field-coil` 的 `preferred_zh` = 「纵场线圈」（大陆文献亦作「环向场线圈」）——属**命名/别名域**，归 W3，本批不动 `concepts.tsv`
- **能失败证明**（仓外副本 + `--repo-root`，**零触碰仓内文件**；未变异对照均 exit 0）
  - en 侧（B01-EN）：`def_boilerplate_regex`（复原套话）／`def_len_en`（截断到 10 字符）／`def_source_unknown`（写 `internal:dict-improvements`）→ 三者均 **exit 1**
  - zh 侧（B01-ZH）：`def_boilerplate_mark`（复原模板）／`def_len_zh`（截断到 `台基。`）／`def_source_unknown`（写 `internal:dict-improvements`）→ 三者均 **exit 1**
- **不变量 / 全量门禁**：`data_rows` 恒 **6132**；列分布恒 `{4}`；`git diff --numstat` = `20/20`（-EN）+ `20/20`（-ZH）；改动 (id,lang) 对恰为批次 id（-EN 全为 `en`、-ZH 全为 `zh`），en 行在 -ZH 阶段改动数 **0**；`validate_registry` / `pytest -q` / `ruff format --check .` / `ruff check .` / `mypy pipeline/` → 全部 **exit 0**
- **下一步**：`w1_b_b02` 起串行推进；**D2-4 抽检在第 5 个批次完成时执行**（W1-A 4 批 + B01 ⇒ 该批即 **B04 完成时**触发）〔2026-10-27 注记：**本行的 `B04 触发` 口径已废弃**（计数基准错误，漏计 W1-A 4 批）；定稿见 §「会话恢复 — Bookkeeping 纠正」第 3 条〕

#### T1.B02-EN / T1.B02-ZH — ✅ DONE（2026-10-27 11:25）commits `7024be1`（-EN）+ 本节（-ZH）

- 批次：`.github/plans/t4973-batches/w1_b_b02.ids`（**20** id）；**W1-B 组第 2 批**（34 批 / 679 id）
- **W1-B 分型**（同 B01 实测）：`en`/`zh` 双侧皆为占位模板（en = `Fusion/nuclear engineering term referring to 'X'…`；zh = `聚变/核工程术语，指“X”这一技术概念。`），双侧 source 均 `internal:dict-improvements` ⇒ **无 GB/T 真实释义可依据**，依 **D2-8=A** 以 concept 的 `notes`（`concepts.tsv` 第 7 列，仓内语料）为唯一依据 ⇒ source 一律 **`corpus`**
- **`-EN`**（commit `7024be1`）：20 条 `en` 行改写
  - 门禁：`--ids-file …/w1_b_b02.ids --expect 20 --lang en` → **exit 0** `verdict=PASS`（改写前 RED：**exit 1**，20 条 `def_boilerplate_regex` + 20 条 `def_source_unknown`，属设计内红）
  - en 最短 **124** / 最长 200；套话 0/20；source **20/20** `corpus`
  - 迁移：`internal:*` 4428 → **4408**；`corpus` 89 → **109**；audit `en_boilerplate` 659 → **639**
- **`-ZH`**（本节）：20 条 `zh` 行由模板改写为真实释义（与同 id 已提交 en **语义等价**，依据 = notes + en；source **20/20** `corpus`）
  - 门禁：`--lang zh` → **exit 0**（改写前 RED：**exit 1**，20 条 `def_boilerplate_mark` + 20 条 `def_source_unknown`）；`--lang both`（批收口，并入本节验收）→ **exit 0**
  - zh 最短 **26** / 最长 48（均值 39.5）；模板 0/20；`指“en”` 0/20；source **20/20** `corpus`
  - 迁移：`internal:*` 4408 → **4388**；`corpus` 109 → **129**；audit `en_boilerplate` **639 → 639**（en 行零改动）
  - `pytest -q` → **exit 0**（批收口）
- **本批自校 2 处**（均在 commit 前完成，未扩大改动面/不变量）：
  1. `modular-coil` en 初稿含 `superconducting` —— notes 仅记 `Non-planar coil producing stellarator rotational transform`，**未限定超导** ⇒ 删除该过写，改为 `A non-planar coil of a stellarator …`（不引入 notes 之外的物质属性）
  2. `stellarator-optimization` zh 初稿误写 `新城输运`（错字）⇒ 更正为 **`新古典输运`**（neoclassical transport 规范译名）
- **能失败证明**（仓外副本 + `--repo-root`，**零触碰仓内文件**；未变异对照 exit 0）
  - en 侧：`def_boilerplate_regex`（复原套话 1 行）／`def_len_en`（截断为 `short.`）／`def_source_unknown`（改写 `internal:dict-improvements`）→ 三者均 **exit 1**
  - zh 侧：`def_boilerplate_mark`（复原 `聚变/核工程术语…` 模板）／`def_len_zh`（截断为 `太短。`）→ 两者均 **exit 1**
  - 证据留存：`/tmp/opencode/t4973-b02/`（`red_{en,zh,both}_before.txt`、`green_{en,zh,both}.txt`、`mutlog_*.txt`、`mut_control.tsv`）
- **逐行依据留痕（物理期间无凭空扩写）**：20 条 en 释义逐条为 `notes` 的直接展开，未引入 notes 之外的实体/数值/项目名；`hohlraum` 的 `high-Z`、`fuel-capsule` 的 `DT ice / ablator shell`、`island-divertor` 的 `W7-X`、`rayleigh-taylor-instability` 的「加速界面 + ICF 内爆劣化」、`compact-toroid` 的「FRC + spheromak」均**逐字或等价见于 notes**；安防/物理疑点 **0**
- **不变量 / 全量门禁**：`data_rows` 恒 **6132**（`registry OK: 3076 concepts, 10249 aliases, 3168 evidence rows, 6132 definitions`）；列分布恒 `{4}`；`git diff --numstat` = `20/20`（-EN）+ `20/20`（-ZH），改动 (id,lang) 对恰为本批 id（-EN 全 `en`、-ZH 全 `zh`），en 行在 -ZH 阶段改动数 **0**；`validate_registry` / `pytest -q` → 全部 **exit 0**
- **下一步**：`w1_b_b03` 起串行推进；**D2-4 抽检按 §Phase 1 说明在 `w1_b` 第 5 批（B05）完成后触发**（W1-A 4 批 + B01/B02 已达 6 批，B01 日志所记 B04 为笔误口径，以 §Phase 1 正文 `B05` 为准）〔2026-10-27 注记：**本行的 `B05` 口径亦已废弃** —— 原 §Phase 1 正文的 `B05/B10/…` 列同样漏计 W1-A 4 批；定稿见 §「会话恢复 — Bookkeeping 纠正」第 3 条〕

#### T1.B03-EN / T1.B03-ZH — ✅ DONE（2026-10-27 11:47）commits `45313cc`（-EN）+ 本节（-ZH）

- 批次：`.github/plans/t4973-batches/w1_b_b03.ids`（**20** id）；**W1-B 组第 3 批**（34 批 / 679 id）
- **W1-B 分型**（同 B01/B02 实测）：`en`/`zh` 双侧皆为占位模板，双侧 source 均 `internal:dict-improvements` ⇒ 依 **D2-8=A** 以 `concepts.tsv` 第 7 列 `notes`（仓内语料）为唯一依据 ⇒ source 一律 **`corpus`**
- **`-EN`**（commit `45313cc`）：20 条 `en` 行改写
  - 门禁：`--ids-file …/w1_b_b03.ids --expect 20 --lang en` → **exit 0** `verdict=PASS`（改写前 RED：**exit 1**，20×`def_boilerplate_regex` + 20×`def_source_unknown`，属设计内红）
  - en 最短 **55** / 最长 135；套话 **0/20**；全 ASCII；source **20/20** `corpus`
  - 迁移：`internal:dict-improvements` 4388 → **4368**；`corpus` 129 → **149**；audit `en_boilerplate` 639 → **619**
- **`-ZH`**（本节）：20 条 `zh` 行由模板改写为真实释义（与同 id 已提交 en **语义等价**，依据 = notes + en；source **20/20** `corpus`）
  - 门禁：`--lang zh` → **exit 0**（改写前 RED：**exit 1**，20×`def_boilerplate_mark` + 20×`def_source_unknown`）；`--lang both`（批收口）→ **exit 0**
  - zh 最短 **16** / 最长 **47**（均值 26.4）；模板 0/20；`指“en”` 0/20；source **20/20** `corpus`
  - 迁移：`internal:*` 4368 → **4348**；`corpus` 149 → **169**；audit `en_boilerplate` **619 → 619**（en 行零改动）
  - `pytest -q` → **exit 0**（批收口）
  - **书写约定沿用**：zh 同位素用上标式（`¹¹B`、`α`），与 T1.A3 批确立约定一致；en 侧用 ASCII 形式
- **本批自校 1 处**（commit 前完成，未扩大改动面/不变量）：`magnetic-nozzle` en 初稿含 `propulsion system exhaust` 措辞冗长，按 notes「for DEC or propulsion exhaust」收束为 `for direct energy conversion or for the exhaust of a propulsion system`（不引入 notes 之外的实体/数值/项目名）
- **能失败证明**（仓外副本 + `--repo-root`，**零触碰仓内文件**；未变异对照 `ctrl` exit 0）
  - en 侧：`def_boilerplate_regex`（复原套话）／`def_len_en`（截断为 `short.`）／`def_source_unknown`（写 `internal:dict-improvements`）→ 三者均 **exit 1**
  - zh 侧：`def_boilerplate_mark`（复原 `聚变/核工程术语…` 模板）／`def_len_zh`（截断为 `太短。`）→ 两者均 **exit 1**
  - 证据留存：`/tmp/opencode/t4973-b03/`（`red_{en,zh}_before.txt`、`green_{en,zh,both}.txt`、`mutlog_{m1,m2,m3,m1z,m2z,ctrl}.txt`、`mutlog_summary.txt`）
- **逐行依据留痕**：20 条 en/zh 释义逐条为 `notes` 的直接展开（如 `cryogenic-target` 的 `18 K`、`spin-polarized-fuel` 的 `~50%`、`neutral-beam-driven-frc` 的 `TAE/ENN`、`high-beta` 的 `β` 均为 notes 逐字内容）；`high-beta` 的「β = 等离子体压强与磁压之比」为教科书本位释义（类别/功能级），未引入 notes 之外的项目名/数值；物理与安防疑点 **0**
- **不变量 / 全量门禁**：`data_rows` 恒 **6132**（`registry OK: 3076 concepts, 10249 aliases, 3168 evidence rows, 6132 definitions`）；列分布恒 `{4}`；`git diff --numstat` = `20/20`（-EN）+ `20/20`（-ZH），改动 (id,lang) 对恰为本批 id（-EN 全 `en`、-ZH 全 `zh`），`en` 行在 `-ZH` 阶段改动数 **0**；`validate_registry` / `pytest -q` → 全部 **exit 0**
- **下一步**：`w1_b_b04` 起串行推进；**D2-4 抽检 cadence** 以 §「会话恢复 — Bookkeeping 纠正」第 3 条为准（本批属 `B02–B06` 组）

#### 会话收口 — 优雅中断（**预算依据为实测，非"感知"**）— 2026-10-26 21:37

- **`[CTX: est≈140k, budget=262144, reason=硬信号（本会话 compaction 事件 6 次，且 harness 持续裁剪工具结果与推理）]`**
  - **实测来源**（`~/.local/share/opencode/opencode.db`，会话 `ses_e919b3f45ffetSh0Jd3OXSQoTl`）：`session_message` 中 `type='compaction'` 行 **6 条**（seq 1292 / 1882 / 2558 / 3534 / 3967 / 4421）；**最后一次 compaction 之后**的消息正文合计 **316,234 B**（53 条）⇒ 按混合中英文 UTF-8 ≈ 3 B/token 折算 ≈ **105k tokens**，加系统提示与工具 schema ⇒ **est ≈ 140k**
  - **阈值口径**（`instructions/context-budget.instructions.md`，window-relative）：`usable = limit.context − compaction.buffer`；`soft = 60% × usable ≈ 118k`、`hard = 85% × usable ≈ 167k` ⇒ 现处于 **soft 之上、hard 之下**，且 harness 已在裁剪 ⇒ 触发「Token 预算与优雅中断」
- **本轮（收口前）已全部落盘的成果**（均在 clean 边界，工作区无未提交改动）
  - **裁决 4**（off-plan，用户裁决 A）：`--self-test` 回归修复 → commit `471ab41`（`18/24 exit 1` → **`24/24 exit 0`**；规则一条未改；`m5` 变体证夹具承重）
  - **T1.B01-EN / T1.B01-ZH**（W1-B 首批，20 id）：commits `b578047` + `f58f0ff`；`--lang both` **exit 0**；`internal:*` 4468 → **4428**；`corpus` 49 → **89**
  - **W1-A 组**（4 批 / 67 id）已收口：`e2e2809`/`05b7223`、`89a2fb2`/`c87e1ba`、`2a01af3`/`d924a94`、`ec556e9`/`534ed89`
- **本轮收口态门禁**：`--self-test` / `w1_a --lang both` / `w1_a_b04 --lang both` / `w1_b_b01 --lang both` / `validate_registry` / `pytest -q` / `ruff format --check .` / `ruff check .` / `mypy pipeline/` / `registry_row_audit --audit --expect-clean` → **全部 exit 0**；`data_rows` 恒 **6132**
- **下一步（恢复后立即执行）**：`w1_b_b02` 起按同一循环串行推进至 `b34`（每批 `-EN` → 独立核验 → 仓外 RED → commit；`-ZH` → 门禁 + 批内恢复性修复 → 日志 + commit）；**D2-4 抽检在 B04 完成时触发**（W1-A 4 批 + B01 已占 5 批中的 1 批）〔2026-10-27 注记：**本行的 `B04 触发` 口径已废弃**；定稿见 §「会话恢复 — Bookkeeping 纠正」第 3 条〕
- **未做**：**未 push**（无授权；`origin/master` 仍停 `3cb3837`，本地领先 **36** 个 commit）〔2026-10-27 注记：`36` 为**该时点**实测值，**保留不篡**；当前实测（HEAD `e67af8c`）`origin/master..HEAD` = **45** 个 commit〕；W1 收尾清扫 / `registry_row_audit.py` 新指标（裁决 3=A）/ W1-C / W2 / W3 均未开始

#### 会话恢复 — Bookkeeping 纠正（2026-10-27，#T-4973，**单独 commit**）

> 本小节为**账面纠正**（不涉及 `terms/` 数据改动）；纪律：独立 commit，不与 W1 批次 commit 混装。所有纠正**只改口径数字 / 追加注记，不篡改历史时点事实**。

1. **W1-A 组内 zh 恢复性修复累计数纠正：7 → 9**。原条目（§「W1-A 组收口」）文字写「累计 7 行」，但**逐项清单实为 9 行**（`lawson-criterion`、`magnetic-island`、`vertical-displacement-event`、`electrostatic-confinement`、`halo-current`、`dt-reaction`、`dd-reaction`、`d-he3-reaction`、`in-vessel-component`）⇒ 以清单为准取 **9**。
2. **W1-B 规模纠正：694 → 679**。`.github/plans/t4973-batches/w1_b.ids` 实测 `wc -l` = **679**（34 批 = 20×33 + 19）。694 系笔误；批数与每批大小仍以 `.github/plans/t4973-batches/README.md` 为唯一权威。
3. **D2-4 抽检 cadence 定稿（含计数基准纠正）**：
   - **计数基准** = W1 的**全部 39 批**（`w1_a` 4 + `w1_b` 34 + `w1_c` 1），**不是**仅 `w1_b`。
   - **首组 = `A1–A4 + B01`（5 批，87 id / 174 定义行）已 PASS**：100% 机械门禁（`--mode definitions --lang both` exit 0）+ 独立复核（≥8 行语义）**PASS**。**证据来源 = 历史会话证据**（父代理转述；本会话未复跑该组抽检）。
   - **后续分组**：`B02–B06`、`B07–B11`、`B12–B16`、`B17–B21`、`B22–B26`、`B27–B31`、`B32–B34 + C1`。
   - **废弃声明**：§Phase 1 正文原列 `B05/B10/B15/B20/B25/B30/C1` **已废弃**（漏计 `w1_a` 4 批 ⇒ 整体偏移 4 批）；历史日志中 `B04 完成时触发`（B01、B02 条目）与 `B05 完成后触发`（B03 前条目）**均已废弃**。一律以本 cadence 为准。
4. **本地 ahead 数（历史 vs 当前，两者对应各自时点，非冲突）**：历史条目所记「本地领先 **36** 个 commit」= **历史时点事实，保留不篡**；**当前实测**（2026-10-27 11:33，HEAD `e67af8c`）`git rev-list --count origin/master..HEAD` = **45**。
5. **Deferred（已接受，**不修改这两条**）**：
   - `kink-mode`：GB/T 条款 `2.1.150` 的**术语名与 `concepts.tsv` `notes` 存在冲突**；
   - `impurity-screening`：GB/T `2.1.127` 的 **`notes` 与既有 zh 释义语义冲突**。
   两条**已接受为 deferred**：本计划内**不改这两条**（不纳入 W1 批次返工，不代表门禁失败）。
6. **W0 证据束 manifest 核实**：`/home/gw/opt/fusion-terms/artifacts/registry-evidence/20261026T231857Z-1984529/manifest.json` — SHA256 实测 `b6396fa58b389f27adefb38aa12b0986f2ec91f7ae80eede8247f6c64c833cfe`，与父代理给定值**逐字一致**（复核命令：`sha256sum <path>`，exit 0）。

## Read-only registry evidence handoff gate

Run the current Phase 0 gate with:

```bash
python3 scripts/registry_evidence_bundle.py --compare
```

The default profile is `w0`, matching the current plan's
`registry_row_audit --expect-clean` gate. It reports W1 definition-quality
metrics as deferred warnings without promoting them to a Phase 0 failure. Use
`--profile all` only when Phase 1 is complete; both phases always use the same
explicit profile.

The entry point freezes data and the minimal validator/audit import closure in
one regular-file snapshot, then runs the existing CLI gates in separate
baseline and batch evidence directories from that snapshot. Source hashes are
checked before and after copying. Complete stdout/stderr files are retained
with SHA-256 hashes; the 64 MiB per-stream limit is hard, so reaching it makes
the evidence incomplete and unsuccessful.

`--reuse` re-parses every saved phase/check evidence file and recomputes
return-code, incomplete, gate, warning, and non-zero metric status. It checks
the schema/profile, snapshot hashes, phase/check set, path safety, evidence
hashes, comparison result, and successful status. It never trusts a mutable
top-level `batch_status` field. The summary reports one external project entry
and four internal CLI checks; this is an outer-entry reduction only, not a
claim about validator/audit calls, model turns, or RPC calls.
