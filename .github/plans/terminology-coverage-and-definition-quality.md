---
plan_schema_version: "1.0"
linked_spec: null
scope_mode: "HOLD"
generated_at: "2026-10-26T05:10:00Z"
git_commit: "3cb3837"
mode: "refine"
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

> 🚧 **状态：待执行（refine 产出，未开工）** — 本文件由 Plan Architect `mode=refine` 基于 PM 任务 **#T-4973** 的既有批次细化而来。
> 所有基线数字为 **2026-10-26 在 HEAD `3cb3837`** 实测，逐条附复现命令；执行时**必须先重测**（见 §动态基线约定）。

# Plan: 术语注册表数据完整性修复 + definitions 质量重写 + allowlist 覆盖补齐（#T-4973）

## 背景与目标

- **问题/需求描述**：
  1. **数据完整性缺陷（最高优先）**：`terms/registry/concepts.tsv` 有 **179/3076** 行畸形（99 行缺 `category` 列导致列左移、80 行仅 6 列），静默穿过 `pipeline/validate_registry.py` 门禁，污染下游已发布产物。
  2. **definitions 质量缺陷**：746 行 en 通用套话 + 48 行 zh 模板残留（把语言标签 `en` 当术语名渲染）+ 10 个 concept 无任何 definitions。
  3. **registry → allowlist 覆盖率仅 46.3%**：1652/3076 行未进入 IME 词表（含 179 行畸形行必然缺失）。
- **根因分析（已取证，verdict=SURVIVED）**：
  - 唯一引入者 = commit **`f90e903`**（"registry: complete bilingual definition retrofit for all 3064 concepts"）。该 commit 对 `concepts.tsv` 是**纯追加**（`+472/-0`，其中 358 行数据行）。实测：父提交 `f2308c0` 畸形 **0**、`f90e903` 畸形 **179**、HEAD 畸形 **179**。
  - 机制 = 追加源列序与 8 字段表头不一致，且门禁只校验 `len(fields) >= 2`，无 schema/取值校验 → 静默通过。
  - 下游污染链（同一根因，全部机械可解释）：`pipeline/export_registry.py:_iter_concept_rows` 按**位置**取列（`parts[2]` → `preferred_zh`），6 字段行的 `parts[2]` 是字面量 `en` → `translation_dict.json` 出现 **166** 条值为 `'en'` 的 `en2zh` 条目；99 行左移行的 `parts[1]`（中文）被当 `category` → `query_expansions.json` 出现 **99** 个中文 `category`。
  - 48 条 zh 释义损坏**全部落在 80 行 6 字段块内**（48/48），机制 = 生成器把该行的 `preferred_zh` 槽位值（= `en`）渲染进模板 `聚变/核工程术语，指“X”这一技术概念。`。既有 2706 行与 f90e903 同步新增的 179 行规范队列**污染率 0**，故非生成器普遍缺陷，而是**该 80 行块的输入畸形**所致。
- **目标**：
  1. **W0**：179 行畸形全部归零；48 条损坏 zh 释义归零；`evidence.tsv` 列数/来源规范化；`validate_registry` 门禁加严到**可机械判定且能失败**（RED 证据来自真实畸形语料）；重跑导出链使已污染产物指标归零。
  2. **W1**：757 个 concept 的 definitions 重写（用户裁决：**全部重写**，不接受保留套话）。
  3. **W2**：584 行 registry→allowlist 机械补齐（排除 36 专名），重跑 `export_registry` → `build_terms` → `sync_to_fcitx`。
  4. **W3**：854 个 concept 的中文首选名起草（用户裁决：并入本批次），要求可核验产出 + 抽检比例 + 分批 ≤30 min。
- **非目标（不做什么）**：
  - **不**把专名（company 25 / organization 7 / facility 3，共 35~36 行）写入 IME 词表 —— 用户已裁决专名不入 IME 词表。
  - **不**改写 1517 行"低信息但未损坏"的 zh 模板释义（`聚指“X”` 除 48 条外的 762 行 + `对应英文“X”` 755 行）—— 用户裁决的 W1 范围为 757 concept；本批不动，仅登记为后续候选（见 §待裁决 D2-3）。
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

## 数据基线（全部为 2026-10-26 HEAD `3cb3837` 实测，附复现命令）

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
| D1 | 未覆盖 = 未覆盖规范行 + 179 畸形行 | **1473 + 179 = 1652 / 3076 → 覆盖率 46.3%** | 旧口径（仅 `preferred_*` 命中 allowlist）为 1493+179=1672 → 45.6%；任务书给的 1670/45.7% 属该口径，**已作废** |
| D2 | **W2**（可机械补齐）：未覆盖规范行 ∩ `preferred_zh` 非空 ∩ 非专名 | **584**（其中 `preferred_en` 含空格 **527**、单词形 **57**） | 任务书 595 系旧口径 |
| D3 | 专名排除 | **35**（company 25 / organization 7 / facility 3） | 任务书 36 |
| D4 | **W3a**（需起草中文首选名）：未覆盖规范行 ∩ `preferred_zh` 为空 | **854**（其中 107 行已有**真实 zh 释义**可推导；747 行仅 `对应英文“X”` 模板） | 任务书 860 系旧口径 |
| D5 | W3 组合口径修正 | **本计划 W3 = 854**（**不含** 99 左移行与 80 六列行，理由见 §基线修正 R-1/R-2） | 任务书 1039 = 860+99+80 |

### E. definitions.tsv 质量基线

| # | 断言 | 实测值 | 复现命令 |
|---|------|--------|----------|
| E1 | 数据行 / 列数 | **6132** 行，全部 4 列 | `awk -F'\t' '!/^#/ && NF>0 {print NF}' terms/registry/definitions.tsv \| sort \| uniq -c` |
| E2 | en 通用套话 | **746** 行（746 个 concept） | `grep -c "Fusion/nuclear engineering term referring to" terms/registry/definitions.tsv` |
| E3 | zh 模板残留 `指“en”` | **48** 行（⊂ E2 的 concept 集，全部落在 80 行 6 列块内） | `grep -cP '\tzh\t.*指“en”' terms/registry/definitions.tsv` |
| E4 | zh 模板族总量（低信息但未损坏，本批**不动**） | **1565** = 810 `指“X”` + 755 `对应英文“X”` | `grep -c "聚变/核工程术语" terms/registry/definitions.tsv` |
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
| R-3 | 覆盖率 45.7%（1670 行未覆盖） | 口径 `preferred_*` 命中 allowlist：1493+179 = 1672 → 45.6%；口径含 `concept_id`/alias：1473+179 = 1652 → 46.3% | **本计划以"是否进入 build 出的 `domain_terms.txt`"为唯一口径**（最贴近"IME 是否覆盖"），值 46.3%；W2/W3 规模按该口径重算（584/854），与任务书差 ≤2% |
| R-4 | `definitions.tsv` 747 行 en 套话 | 严格模板匹配（`^Fusion/nuclear engineering term referring to '.*' in technical context\.$`）为 **746** 行；宽松前缀 `grep -c "in technical context"` 亦为 746 | 取 **746**；旧"747"多计的 1 行不存在（无变体模板，`grep -v` 反查为 0 行） |
| R-5 | "已发布产物消费者可见" | `translation_dict.json` 入库（公开可见）；`query_expansions.json`/`tag_rules.jsonl` 被 gitignore；v2026.10.25 发布包**不含** registry 导出物（见 B6） | 污染**公开可见面**仅为 `translation_dict.json`；重跑导出链仍必要（本地/未来发布包） |
| R-6 | `code` 类 9 个概念待裁决（含 `opencascade`） | `opencascade` **已覆盖**（其 alias `OCC` 在 `allowlist_en.txt`），真正未覆盖的是 **8** 个：`vmec,desc,simsopt,cate,pactole,pactiter,tract,oscar`；且 `code` 类共 107 个 concept 中 **99 个已覆盖**；`MCNP` 在 `allowlist_en.txt` 与 `allowlist_zh.txt` **都**存在（`mcnp` 小写不存在） | 待裁决清单收敛为 8 个 id，且**先例强度**已量化（99/107 已入表）→ §待裁决 D2-1 |
| R-7 | W2 595 行 | 584 行；其中 527 行 `preferred_en` 含空格（须连字符 token 化），57 行为单词形，**其中 21 行为通用英文词**（`design/system/material/performance/...`），且 `system`、`mode` 已在 `denylist.txt` 中 | 新增 §待裁决 D2-2（通用词是否入 EN 词表） |

## 风险与对策表

| # | 风险 | 概率 | 影响 | 对策 | 触发信号 |
|---|------|------|------|------|---------|
| RK1 | W0 修 179 行时误改规范行 | 中 | 高（数据回归） | 只做**定点行替换**（行号 + concept_id 双锚），改后跑 `scripts/registry_row_audit` 断言 `规范行=2897+179=3076` 且 concept_id 集合与改动前 `diff` 为空 | audit 报 concept_id 集合变化 |
| RK2 | 门禁加严导致 CI 变红（本仓 CI 曾连续 4 次红灯，刚于 run #43 恢复） | 中 | 高 | 顺序纪律：**先修数据（T0.2–T0.5）再改门禁（T0.6–T0.7）**；每次 commit 前本地跑全量 G1–G5 | `ruff format --check`/CI 红 |
| RK3 | `ruff format --check .` 会格式化 **Markdown 内 python 代码块**（0.17.2 行为）→ 新计划/脚本被记为未格式化 | 高 | 中 | 新脚本按 `ruff format` 输出写；本计划文件提交前跑 `ruff format .github/plans/terminology-coverage-and-definition-quality.md`（先例 commit `8f51d52`） | `ruff format --check .` 报本文件 |
| RK4 | W1/W3 定义/名称的来源不可核验（"看起来对"） | 高 | 高 | 每批强制过 `scripts/registry_batch_verify.py`（模板正则黑名单 + 最小长度 + 来源白名单 + `--check-urls` 200 断言）；无网络环境改用仓内出处（`GB/T-4960.9`/`ITER-glossary`/`IAEA-safety-glossary`） | 批验收 exit ≠ 0 |
| RK5 | W2 向 `allowlist_en.txt` 注入空白项 → `build_terms` `SystemExit` | 中 | 高 | W2 仅写**连字符 token**（含空格者用 `concept_id`）；批验收含 `grep -v '^#' terms/allowlist_en.txt \| grep -c ' '` = 0 | `build_terms` 抛 whitespace |
| RK6 | W2/W3 批量追加引入重复行 | 中 | 中 | 追加前 `sort | uniq -d` 断言；批验收含唯一性检查 | 重复行非空 |
| RK7 | 修复后导出物数量大幅变化触发 snapshot 测试红 | 中 | 中 | 先跑 `pytest -q tests/test_export_registry*`；如为 hardcode 基线则按数据事实更新并记录 | pytest 相关用例失败 |
| RK8 | 47 处"隐式依赖"：179 行被 alias/evidence 引用 | 低 | 中 | 只改 `concepts.tsv` 列结构，不动 `concept_id`，故 alias/evidence 外键不变（`validate_registry` 会校验 `concepts without evidence`） | validate_registry 报缺失 evidence |
| RK9 | W3 起草 854 个中文名产生"机翻腔"或与既有别名冲突 | 中 | 中 | 与 `aliases.tsv` 既有 zh 别名做冲突检查（先例：`grep -P '^击穿\t'`）；抽检 ≥10% 且抽检不通过则整批返工 | 抽检 FAIL 行数 > 0 |
| RK10 | 长时间批处理会话上下文耗尽（38+ 批次） | 高 | 中 | 每批次独立 session（批清单落地为文件，会话无状态依赖）；每 5 批一次 `git status` + 全量门禁 | 批次验收命令报错 |

### Error & Rescue Map（关键失败路径映射）

| 代码路径/操作 | 可能的失败 | 错误类型 | 已处理？ | 处理方式 | 用户可见行为 |
|---|---|---|---|---|---|
| 修复 99 左移行 | 删列位置错（多删/少删） | 数据回归 | Y | 逐行断言「8 列 + `$2` ∈ 16 类 + `$3` 为中文」；回归计数 `2897+99` | audit 报错并回滚该行 |
| 修复 80 六列行 | category 取值越界 | 门禁红 | Y | 16 类白名单 + 兄弟 concept 对照（同 domain 已有规范行） | `validate_registry` 报错 |
| 修 48 zh 释义 | 中文名与 `preferred_zh` 不一致 | 语义漂移 | Y | 断言 zh 释义中出现的术语名 == 该 concept 的 `preferred_zh` | 批验收 exit 1 |
| evidence 列数规范化 | 插入空列破坏 `quote` 语义 | 语义漂移 | Y | 只做「列数 4→5 / 2→5」的**空 `quote` 补齐**，不改 `source`/`added_by`/`added_at` 值 | diff 仅新增空字段 |
| 门禁加严 | 现有 11 处测试 fixture 仍用 ≤4 列 evidence | 测试红 | Y | T0.7 同步更新 `_MINIMAL_EVIDENCE` 等 fixture（声明文件内改动） | pytest 红 → 按 T0.7 修复 |
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

> 上述 D2-1~D2-5 由父代理（或用户）裁决后回写本节；未裁决前按"推荐项"执行**但**在 commit message 与本节标注 `[默认取推荐项，待追认]`。
>
> **✅ 2026-10-26：D2-1 ~ D2-5 已全部裁决（用户选项 A），见文末《待裁决落地记录》。执行时按裁决口径，不再标注"待追认"。**

## 时序推演

| 阶段 | 关键决策/潜在阻塞 |
|------|------------------|
| 初期（T0.0–T0.5） | 先固化口径与审计脚本，再做数据修复。**先修数据后改门禁**（RK2）；T0.2/T0.3a 改列结构后立即跑全量门禁，确认无规范行回归 |
| 中期（T0.6–T0.9） | 门禁加严是"能失败"的证明点：先录 RED（真实 179 行语料 fixture 必须 FAIL），再录 GREEN（修复后 live registry PASS）。导出链重跑后三项污点指标须归零，否则回溯 parse 位置 |
| 后期（Phase 1–3） | W1/W3 是**人力密集型**（38 + 28 批），阻塞点 = 来源可达性（网络/URL 200）与批验收；W2 依赖 W0 的 `concepts.tsv` 修复结果（W2 清单口径须在 W0 后重算）。W3 依赖 W0（不得基于畸形行起草名字） |
| 收尾（Phase 4） | 发布包验证（`release_pack` + `verify_release_contract`）在最后；`sync_to_fcitx` 有本机副作用，放最后且先备份 |

## 执行计划

### Phase 0: W0 — 数据完整性修复 + 门禁加严（最高优先，Phase 1–3 的前置）

> **Phase 0 首步（强制）**：`git rev-parse HEAD` + `git status --porcelain` 实测；若 HEAD ≠ `3cb3837` 或工作区非空，先按 §动态基线约定重测 T0.1 审计基线并更新锚点（**行号锚点 3171/3316 仅在 HEAD `3cb3837` 成立**）。
> **Phase 0 完成定义（一条命令）**：`.venv/bin/python scripts/registry_row_audit.py --audit --expect-clean` → exit 0（`malformed=0, shifted=0, sixcol=0, evidence_cols_non5=0, zh_en_corruption=0`）。

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
  - `ruff format --check scripts/registry_coverage_report.py` 与 `ruff check scripts/registry_coverage_report.py` 通过。
- **验收标准**：
  - ✅ [脚本存在且可执行] `[T-A]` `.venv/bin/python scripts/registry_coverage_report.py` → exit 0，stdout 含 `coverage_pct: 46.3`（±0.1）且 `W2: 584`、`W3a: 854`（在 HEAD `3cb3837` 未修数据时）
  - ✅ [口径单调性] `[T-B]` `assert covered + uncovered == total == 3076`
  - ✅ [格式门禁] `[T-A]` `.venv/bin/ruff format --check scripts/registry_coverage_report.py` → exit 0
- **能失败证明（反例锚定法）**：临时把 `--terms-file` 指向 `/dev/null`（覆盖率应变为 0），命令非 0 结束或 `coverage_pct: 0.0`；若能仍报 46.3 则脚本写死数字 → 判 FAIL。
- **潜在风险**：`domain_terms.txt` 陈旧（未随 allowlist 重建）→ 本任务只读，若与 allowlist 不一致由 W2 T2.11 重建后重算。
- **预留歧义标注**：
  - [ ] 无歧义：所有字段可直接执行，无需额外推断

#### Task T0.1: 结构审计脚本（RED 证据与回归计数的唯一来源）

- **目标**：把 §A/§E/§F 全部结构断言固化为一条命令，供修复前后对照。
- **依赖**：无
- **frontier**：是
- **执行者**：Simulation Builder
- **预估墙钟**：25 min
- **修改内容**：
  - 新增文件 `/home/gw/opt/fusion-terms/scripts/registry_row_audit.py`：对 `concepts.tsv` 输出 `data_rows / cols_dist / malformed_cols / bad_category / shifted_rows(行号区间) / sixcol_rows(行号区间) / concept_ids_sha256`；对 `evidence.tsv` 输出 `cols_dist / non5_cols / glued_source_rows`；对 `definitions.tsv` 输出 `en_boilerplate / zh_en_corruption / concepts_without_defs`；参数 `--audit`（打印 JSON）、`--expect-clean`（全部指标为 0 时 exit 0，否则 exit 1）、`--json PATH`。
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
    - `w1_a.ids`（67 行，仓内可推导）、`w1_b.ids`（679 行，须外部出处）、`w1_c.ids`（10 行，缺失 definitions）
    - `w1_a_b01.ids`…`w1_a_b03.ids`（23/22/22）、`w1_b_b01.ids`…`w1_b_b34.ids`（每批 20）
    - `w2.ids`（584）、`w2_b01.ids`…`w2_b10.ids`（每批 58~59）
    - `w3.ids`（854）、`w3_b01.ids`…`w3_b28.ids`（107 行按 36/36/35 分 3 批 + 747 行按每批 27 分 27 批 + 1 批余量→ 共 31 批，见 Phase 3 表）
    - `README.md`（清单口径、生成命令、批次总数）
  - 生成命令：`.venv/bin/python scripts/registry_coverage_report.py --emit-lists .github/plans/t4973-batches --batch-size 20`
- **修改边界**：只新增 `.github/plans/t4973-batches/` 下文件；不得改动任何 `terms/`、`pipeline/`、`artifacts/` 文件。
- **质量检查方式**：清单总行数与 §D 实测对齐；每批文件行数 == 批大小。
- **验收标准**：
  - ✅ [集合规模] `[T-A]` `wc -l .github/plans/t4973-batches/{w1_a,w1_b,w1_c,w2,w3}.ids` → 分别为 `67 679 10 584 854`（exit 0）
  - ✅ [无重复无交集] `[T-A]` `sort .github/plans/t4973-batches/w2.ids .github/plans/t4973-batches/w3.ids | uniq -d | wc -l` → `0`
  - ✅ [批次无遗漏] `[T-A]` `cat .github/plans/t4973-batches/w1_b_b*.ids | wc -l` → `679`
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

- **目标**：把 48 条把语言标签当术语名的 zh 释义重写为真实释义（**W0 范围**，属根因修复；W1 只负责 en 行）。
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
  - ✅ [行数不变] `[T-A]` `wc -l terms/registry/evidence.tsv` → `3168`
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
  - 文件 `CHANGELOG.md`：新增 W0 条目（数据修复 179 行、48 条 zh 释义、evidence 规范化 642 行、门禁加严、三项污点归零）。
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

**范围清算（与任务书口径的对账）**

| 组 | 内容 | 行数 | 依据 |
|----|------|------|------|
| W1-A | 746 行 en 套话中，**已有真实 zh 释义**（源 `GB/T-4960.9`）的 67 个 concept → en 释义由仓内 zh 释义改写 | 67 行 | `§E6` 实测 |
| W1-B | 746 行 en 套话中，**仅有 zh 模板**的 679 个 concept → 须外部出处 | 679 行 | `§E6` 实测 |
| W1-C | 10 个**完全无 definitions** 的 concept → 新增 en+zh | 20 行 | `§E5` 实测 |
| 小计 | 757 concept / **766 行** | 766 行 | W1-A+B+C |
| （移出）| 48 条损坏 zh 释义 | — | **已在 Phase 0 T0.7a/T0.7b 完成**（根因修复，避免与 en 重写重复研究） |
| （非目标）| 1517 行低信息 zh 模板 | — | 见 §待裁决 D2-3 |

> 任务书"795 行（747 en + 48 zh）"→ 本计划为 **766 行（746 en + 20 新增）+ 48 zh 在 W0**，总行数一致（814 行），仅**相位归属**不同；差值 1 行 = §R-4（746 vs 747）。

**批次任务统一规格（下表每行即一个独立 Task）**

- **目标**：为该批 concept 的 `definitions.tsv` 行写出**真实、带可核验出处**的释义。
- **依赖**：T0.9（门禁加严）、T0.10；同 wave 内批次相互独立。
- **frontier**：同 wave 内为"是"（不同批次的 concept 集合不相交；但 `definitions.tsv` 为**同一文件**→ 实际执行须串行或分批 commit，禁止并发写同一文件）。
- **执行者**：Academic Writer（技术释义）；Simulation Builder 负责落表与批验收。
- **修改内容**：文件 `terms/registry/definitions.tsv`（**定点替换**该批 concept 的 `en` 行；W1-C 额外新增 `zh` 行）；必要时文件 `terms/registry/evidence.tsv` 追加出处 URL。
- **修改边界**：
  - 不得修改非本批 concept 的任何行；不得改 `zh` 行（W1-C 除外）；不得改 `preferred_zh`/`preferred_en`。
  - **禁止** `internal:dict-improvements`、`internal:TODO` 作为新释义出处（前者正是套话批次的标记）。
  - 不得改动 `terms/registry/concepts.tsv`。
- **质量检查方式**：批验收脚本 + 抽检（D2-4）。
- **验收标准（每批同构，替换 `<mode>/<ids>/<N>`）**：
  - ✅ [批验收] `[T-A]` `.venv/bin/python scripts/registry_batch_verify.py --mode definitions --ids-file .github/plans/t4973-batches/<ids> --expect <N> --check-urls` → **exit 0**
  - ✅ [模板黑名单] `[T-B]` `assert 本批 en 行无一匹配 ^Fusion/nuclear engineering term referring to '.*' in technical context\.$`
  - ✅ [全局门禁] `[T-A]` `.venv/bin/python -m pipeline.validate_registry` → **exit 0**
  - ✅ [测试] `[T-A]` `.venv/bin/python -m pytest -q` → **exit 0**
- **能失败证明（反例锚定）**：任取一批，把 1 行新释义改回套话 → 批验收必须 exit 1。
- **潜在风险**：`--check-urls` 依赖网络；无网环境改用仓内出处（`GB/T-4960.9`/`ITER-glossary`/`IAEA-safety-glossary`）并在批记录中标注 `[NO-NET]`。

| Task | 组 | ids 文件 | 数量 | 预估墙钟 | 修改文件 |
|------|----|---------|------|---------|---------|
| T1.1 | W1-A 仓内可推导 | `w1_a_b01.ids` | 23 | 25 min | `terms/registry/definitions.tsv` |
| T1.2 | W1-A | `w1_a_b02.ids` | 22 | 25 min | `terms/registry/definitions.tsv` |
| T1.3 | W1-A | `w1_a_b03.ids` | 22 | 25 min | `terms/registry/definitions.tsv` |
| T1.4 | W1-B 外部出处 | `w1_b_b01.ids` | 20 | 30 min | `terms/registry/definitions.tsv`（+`evidence.tsv`） |
| T1.5 | W1-B | `w1_b_b02.ids` | 20 | 30 min | 同上 |
| T1.6 | W1-B | `w1_b_b03.ids` | 20 | 30 min | 同上 |
| T1.7 | W1-B | `w1_b_b04.ids` | 20 | 30 min | 同上 |
| T1.8 | W1-B | `w1_b_b05.ids` | 20 | 30 min | 同上 |
| T1.9 | W1-B | `w1_b_b06.ids` | 20 | 30 min | 同上 |
| T1.10 | W1-B | `w1_b_b07.ids` | 20 | 30 min | 同上 |
| T1.11 | W1-B | `w1_b_b08.ids` | 20 | 30 min | 同上 |
| T1.12 | W1-B | `w1_b_b09.ids` | 20 | 30 min | 同上 |
| T1.13 | W1-B | `w1_b_b10.ids` | 20 | 30 min | 同上 |
| T1.14 | W1-B | `w1_b_b11.ids` | 20 | 30 min | 同上 |
| T1.15 | W1-B | `w1_b_b12.ids` | 20 | 30 min | 同上 |
| T1.16 | W1-B | `w1_b_b13.ids` | 20 | 30 min | 同上 |
| T1.17 | W1-B | `w1_b_b14.ids` | 20 | 30 min | 同上 |
| T1.18 | W1-B | `w1_b_b15.ids` | 20 | 30 min | 同上 |
| T1.19 | W1-B | `w1_b_b16.ids` | 20 | 30 min | 同上 |
| T1.20 | W1-B | `w1_b_b17.ids` | 20 | 30 min | 同上 |
| T1.21 | W1-B | `w1_b_b18.ids` | 20 | 30 min | 同上 |
| T1.22 | W1-B | `w1_b_b19.ids` | 20 | 30 min | 同上 |
| T1.23 | W1-B | `w1_b_b20.ids` | 20 | 30 min | 同上 |
| T1.24 | W1-B | `w1_b_b21.ids` | 20 | 30 min | 同上 |
| T1.25 | W1-B | `w1_b_b22.ids` | 20 | 30 min | 同上 |
| T1.26 | W1-B | `w1_b_b23.ids` | 20 | 30 min | 同上 |
| T1.27 | W1-B | `w1_b_b24.ids` | 20 | 30 min | 同上 |
| T1.28 | W1-B | `w1_b_b25.ids` | 20 | 30 min | 同上 |
| T1.29 | W1-B | `w1_b_b26.ids` | 20 | 30 min | 同上 |
| T1.30 | W1-B | `w1_b_b27.ids` | 20 | 30 min | 同上 |
| T1.31 | W1-B | `w1_b_b28.ids` | 20 | 30 min | 同上 |
| T1.32 | W1-B | `w1_b_b29.ids` | 20 | 30 min | 同上 |
| T1.33 | W1-B | `w1_b_b30.ids` | 20 | 30 min | 同上 |
| T1.34 | W1-B | `w1_b_b31.ids` | 20 | 30 min | 同上 |
| T1.35 | W1-B | `w1_b_b32.ids` | 20 | 30 min | 同上 |
| T1.36 | W1-B | `w1_b_b33.ids` | 20 | 30 min | 同上 |
| T1.37 | W1-B（尾批） | `w1_b_b34.ids` | 19 | 30 min | 同上 |
| T1.38 | W1-C 无 definitions | `w1_c.ids` | 10（+20 行） | 30 min | `terms/registry/definitions.tsv`（新增 en+zh 各 10 行）+ `evidence.tsv` |

**Phase 1 完成定义（一条命令）**：

- ✅ `[T-A]` `.venv/bin/python scripts/registry_row_audit.py --audit` → `en_boilerplate=0 && concepts_without_defs=0`（exit 0）
- ✅ `[T-A]` `.venv/bin/python -m pipeline.validate_registry` → exit 0，且输出 `… 6132 + 20 = 6152 definitions`
- ✅ `[T-A]` `.venv/bin/python -m pytest -q` → exit 0

**逐 Task 验收命令展开规则（消除下游猜测；以上表每一行为一个 Task）**：把统一规格中的 `<ids>` 换为该行的 `ids 文件` 名、`<N>` 换为该行的 `数量`。**worked example（T1.4）**：

```bash
.venv/bin/python scripts/registry_batch_verify.py --mode definitions \
  --ids-file .github/plans/t4973-batches/w1_b_b01.ids --expect 20 --check-urls
# 期望 exit 0；若在无网环境：追加 --no-net 并把本批出处改为仓内出处（GB/T-4960.9 / ITER-glossary / IAEA-safety-glossary）
```

**批次提交纪律**：每批单独 commit，message 形如 `feat(registry): rewrite definitions batch W1-B-01 (#T-4973)`；`git diff --stat` 只含 `terms/registry/definitions.tsv`（必要时 +`evidence.tsv`）。

**Phase 1 说明（抽检，落实 D2-4 推荐项）**：每 5 批（T1.5、T1.10、T1.15、T1.20、T1.25、T1.30、T1.35、T1.38 后）执行一次抽检：`scripts/registry_batch_verify.py --mode definitions --ids-file <最近 5 批 union> --sample 8 --semantic-digest`，产出 8 行摘要交独立 agent 复核语义正确性；复核 FAIL > 0 → 该 5 批返工（不得只改被抽中的行）。

### Phase 2: W2 — allowlist 机械补齐（584 行，排除 35 专名）

> 依据 §D2：`preferred_zh` 非空且非专名的未覆盖规范行 584 条；其中 **527 条 `preferred_en` 含空格**（→ 入 `allowlist_en.txt` 时必须用**连字符 token**，禁止空白，见 RK5），**57 条单词形**（其中 21 条为通用英文词，见 §待裁决 D2-2；其中 `system`/`mode` 已在 `denylist.txt`，写入无效）。

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
- **潜在风险**：批量 59 行/批 偏紧 → 允许拆为 30+29 并更新 README 批号。

| Task | ids 文件 | 数量 | 预估墙钟 | 修改文件 |
|------|---------|------|---------|---------|
| T2.0（预检+重算） | — | — | 20 min | `.github/plans/t4973-batches/w2*.ids`（重算）、`w2-denylist-conflicts.tsv` |
| T2.1 | `w2_b01.ids`（含 8 个 code id，待 D2-1） | 59 | 30 min | `terms/allowlist_zh.txt`、`terms/allowlist_en.txt` |
| T2.2 | `w2_b02.ids`（含 21 个通用词中的一部分，待 D2-2） | 59 | 30 min | 同上 |
| T2.3 | `w2_b03.ids` | 58 | 30 min | 同上 |
| T2.4 | `w2_b04.ids` | 58 | 30 min | 同上 |
| T2.5 | `w2_b05.ids` | 58 | 30 min | 同上 |
| T2.6 | `w2_b06.ids` | 58 | 30 min | 同上 |
| T2.7 | `w2_b07.ids` | 58 | 30 min | 同上 |
| T2.8 | `w2_b08.ids` | 58 | 30 min | 同上 |
| T2.9 | `w2_b09.ids` | 58 | 30 min | 同上 |
| T2.10 | `w2_b10.ids`（尾批） | 59 | 30 min | 同上 |
| T2.11 | 全量复算 | — | 25 min | `artifacts/domain_terms.txt`（重建）、`.github/plans/t4973-batches/coverage-after-w2.md` |

**T2.0 验收**：✅ `[T-A]` `.venv/bin/python scripts/registry_coverage_report.py --json /tmp/cov-w2.json` → exit 0 且 `W2=584`（W0 修复后应更新为 **584 − 已由修复覆盖的行数**，以实测为准；差值必须能逐行解释）；✅ `[T-B]` 断言 `w2.ids` 与 `denylist.txt` 交集 == `{"system","mode"}`。

**T2.11 验收**：

- ✅ [覆盖率提升] `[T-A]` `.venv/bin/python scripts/registry_coverage_report.py` → `coverage_pct ≥ 46.3 + 18.9（= 584/3076）`，即 **≥ 65.2%**（若 D2-1/D2-2 采用保守项则按实际 N 折算并在记录中写明）
- ✅ [IME 词表增长] `[T-A]` `.venv/bin/python -m pipeline.build_terms --config config.toml && wc -l artifacts/domain_terms.txt` → 行数 ≈ `3462 + 584`（允许 zh/EN 冲突去重造成的少量偏差，偏差须逐条解释）
- ✅ [发布契约不破] `[T-A]` `.venv/bin/python -m pytest -q` → exit 0

**Phase 2 完成定义**：`.venv/bin/python scripts/registry_coverage_report.py --json /tmp/cov.json && python3 -c "import json;d=json.load(open('/tmp/cov.json'));assert d['coverage_pct'] >= 65.0"` → exit 0。

**逐 Task 验收命令展开规则**：把统一规格中的 `<ids>` 换为该行 `ids 文件` 名、`<N>` 换为该行 `数量`。**worked example（T2.3）**：

```bash
.venv/bin/python scripts/registry_batch_verify.py --mode allowlist \
  --ids-file .github/plans/t4973-batches/w2_b03.ids --expect 58
grep -v '^#' terms/allowlist_en.txt | grep -c ' '        # 期望 0
sort terms/allowlist_zh.txt | uniq -d | wc -l            # 期望 0
.venv/bin/python -m pipeline.build_terms --config config.toml   # 期望 exit 0
```

**批次提交纪律**：每批单独 commit，message 形如 `feat(registry): allowlist fill W2-batch-03 (#T-4973)`；`git diff --stat` 只含 `terms/allowlist_zh.txt` + `terms/allowlist_en.txt`。

### Phase 3: W3 — 中文首选名起草（854 个 concept）

> 依据 §D4/D5：**本计划 W3 = 854**（未覆盖规范行 ∩ `preferred_zh` 空 ∩ 非专名）。其中 **107** 行可从仓内 `GB/T-4960.9` zh 释义推导；**747** 行无仓内出处（仅 `对应英文“X”` 模板）。
> 任务书口径 1039（含 99 左移行 + 80 六列行）已按 §R-1/R-2 修正：99 行中文名**本就存在**（无需起草）；80 行中文名在 Phase 0 T0.6a/b 完成。

**批次任务统一规格**

- **目标**：为每个 concept 填 `preferred_zh`（中文首选名），并附可核验依据。
- **依赖**：Phase 0 完成（不得基于畸形行起草）；T0.2/T0.3。
- **执行者**：Academic Writer（命名）；Simulation Builder 落表。
- **修改内容**：文件 `terms/registry/concepts.tsv`（**定点填 `preferred_zh`**）；必要时 `terms/registry/evidence.tsv`（追加依据 URL）。
- **修改边界**：只填 `preferred_zh`；不得改 `preferred_en`/`category`/`notes`；不得与 `aliases.tsv` 既有 zh 别名冲突（冲突须列入 `w3-name-conflicts.tsv` 并交裁决，**不得静默择一**）。
- **质量检查方式**：批验收 `--mode names`；每批结束后与 `aliases.tsv` 做冲突扫描。
- **验收标准（每批同构）**：
  - ✅ [批验收] `[T-A]` `.venv/bin/python scripts/registry_batch_verify.py --mode names --ids-file .github/plans/t4973-batches/<ids> --expect <N>` → **exit 0**
  - ✅ [依据可核验] `[T-A]` 同上加 `--check-urls`（`--no-net` 时须为仓内出处）→ **exit 0**
  - ✅ [无冲突未登记] `[T-A]` `wc -l .github/plans/t4973-batches/w3-name-conflicts.tsv` 与批记录中的冲突数一致（不允许"零冲突但输出非空"）
  - ✅ [门禁不退化] `[T-A]` `.venv/bin/python -m pipeline.validate_registry` → **exit 0**
- **能失败证明（反例锚定）**：把某行 `preferred_zh` 改为英文串（如 `en`/`OpenCASCADE`）→ `--mode names` 必须 exit 1。
- **潜在风险**：854 个命名的质量风险最高（RK9）→ 强制抽检。

| Task | 组 | ids 文件 | 数量 | 预估墙钟 | 修改文件 |
|------|----|---------|------|---------|---------|
| T3.1 | 仓内可推导（GB/T） | `w3_a_b01.ids` | 36 | 30 min | `terms/registry/concepts.tsv` |
| T3.2 | 仓内可推导 | `w3_a_b02.ids` | 36 | 30 min | 同上 |
| T3.3 | 仓内可推导（尾批） | `w3_a_b03.ids` | 35 | 30 min | 同上 |
| T3.4 | 外部依据 | `w3_b_b01.ids` | 27 | 30 min | `terms/registry/concepts.tsv`（+`evidence.tsv`） |
| T3.5 … T3.30 | 外部依据 | `w3_b_b02.ids` … `w3_b_b27.ids` | 各 27 | 各 30 min | 同上 |
| T3.31 | 外部依据（尾批） | `w3_b_b28.ids` | 18 | 25 min | 同上 |

> **批次展开规则（消除下游猜测）**：上表"T3.5 … T3.30"为 26 个同构任务，逐批 ids 文件按 `w3_b_b02.ids`→`w3_b_b27.ids` 顺序一一对应；每批数量 27（`27×27 + 18 = 747` ✓）。批次号与数量以 `.github/plans/t4973-batches/README.md`（T0.3 产出）为**唯一权威**。

**Phase 3 完成定义（一条命令）**：`.venv/bin/python scripts/registry_row_audit.py --audit --expect-clean` → `w3a_empty_zh=0`（exit 0）。

**Phase 3 抽检（≥10%，落实 D2-5）**：每 5 批抽检 ≥10%（≥14 行）由独立 agent 复核命名准确性（对照该 concept 的 `preferred_en` + 依据 URL 摘要）；抽检 FAIL → 该 5 批返工；`w3-name-conflicts.tsv` 中的冲突项**全部**须人工裁决后才能收尾。

**逐 Task 验收命令展开规则**：把统一规格中的 `<ids>` 换为该行 `ids 文件` 名、`<N>` 换为该行 `数量`。**worked example（T3.4）**：

```bash
.venv/bin/python scripts/registry_batch_verify.py --mode names \
  --ids-file .github/plans/t4973-batches/w3_b_b01.ids --expect 27 --check-urls
# 期望 exit 0；另需确认本批新增冲突已全部登记：wc -l .github/plans/t4973-batches/w3-name-conflicts.tsv
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
  - ✅ `[T-A]` `.venv/bin/python scripts/registry_row_audit.py --audit --expect-clean` → exit 0
  - ✅ `[T-A]` `.venv/bin/python -m pytest -q` → exit 0
  - ✅ `[T-A]` `.venv/bin/mypy pipeline/ --ignore-missing-imports` → exit 0
  - ✅ `[T-A]` `.venv/bin/ruff format --check .` → exit 0（含本计划文件；否则先 `ruff format` 本文件）
  - ✅ `[T-A]` `.venv/bin/ruff check .` → exit 0
  - ✅ `[T-A]` `.venv/bin/python3 -m pipeline.validate_registry` → exit 0（输出 `6152 definitions`）
  - ✅ `[T-A]` `.venv/bin/python scripts/registry_coverage_report.py` → `coverage_pct ≥ 78.0`（584/3076 + 854/3076 = 46.3 + 18.9 + 27.8 ≈ 93.0% 理论上限；实际以 D2-1/D2-2/D2-5 裁决与去重为准，**下限取 78%** 作为"W2+W3 至少完成一半"的保守闸门）
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
| W1 | T1.x 批内串行 | T1.1 | W0-11 | `definitions.tsv` 单文件 → **串行**；跨 wave 无并行（同文件） |
| W2 | T2.x 串行 | T2.1 | W0-11、T2.0 | allowlist 两文件 → 串行；T2.11 依赖全部批 |
| W3 | T3.x 串行 | T3.1 | W0-11 | `concepts.tsv` 单文件 → 串行 |
| W4 | T4.2、T4.3 | T4.1 | 全部 | T4.2/T4.3 在 T4.1 后**可真并行**（不同目标） |

> **并行上限**：本次计划全程受"单文件写入"约束，实质并发度 ≈1（除 W0-1 的三脚本、W0-7 的两个不同文件、W4 的两项）。**不得为追求并发而拆分同一文件的批量写入**。

## 动态基线约定（禁止硬编码）

- 本计划所有 `HEAD`/行号/计数均为 **2026-10-26 @ `3cb3837`** 的**生成时快照**；执行时**必须重测**：`git rev-parse HEAD`、`git status --porcelain`、`.venv/bin/python scripts/registry_row_audit.py --audit`。
- 行号锚点（99 行 = 3171–3315、80 行 = 3316–3395）**仅在 `3cb3837` 成立**；实现时以 `concept_id` 为锚，行号仅作提示。
- 前端数字（584/854/746/48/427/215 等）在 Phase 0 修复后会**变化**：每相位开始时用 `scripts/registry_coverage_report.py` 与 `registry_row_audit.py --audit` 重算，差值必须能逐行解释后再动手。

## Post-Execution Verification

### Automated Verification（Dev Orchestrator / TE 自动执行）

| ID | Description | Command | Expected |
|----|-------------|---------|----------|
| V1 | 结构完整性（W0 核心闸门） | `.venv/bin/python scripts/registry_row_audit.py --audit --expect-clean` | exit 0；`malformed_cols=0, bad_category=0, sixcol_rows=0, non5_cols=0, en_boilerplate=0, zh_en_corruption=0, concepts_without_defs=0` |
| V2 | registry 门禁 | `.venv/bin/python -m pipeline.validate_registry` | exit 0；`registry OK: 3076 concepts, …, 6152 definitions` |
| V3 | 单元测试（CI 同口径） | `.venv/bin/python -m pytest -q` | exit 0（≥159 + 新增用例） |
| V4 | 覆盖率终值 | `.venv/bin/python scripts/registry_coverage_report.py` | exit 0；`coverage_pct ≥ 78.0` |
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
| W2 | `.venv/bin/python scripts/registry_coverage_report.py --json /tmp/c.json && python3 -c "import json;d=json.load(open('/tmp/c.json'));assert d['coverage_pct'] >= 65.0"` | exit 0 |
| W3 | `.venv/bin/python scripts/registry_row_audit.py --audit --expect-clean` | exit 0（`w3a_empty_zh=0`） |
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
- [ ] `evidence.tsv` 列数全部为 5、行数仍 **3168**
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
| 数据基线 | 8 组（A–H）共 40 条断言，每条附复现命令；2026-10-26 @ `3cb3837` 实测 |
| 与任务书差异 | 7 条（R-1 ~ R-7），每条给复现与处置 |
| 风险与对策 | 10 条风险 + Error & Rescue Map 10 条路径，0 CRITICAL GAP |
| 待裁决 | 5 项（D2-1 ~ D2-5），各含现状数据/选项/阻塞下游 |
| 执行计划 | 4 Phase + 1 收尾相位；**101 个 Task**（W0: 16（含 T0.6a/b、T0.7a/b 拆分）、W1: 38、W2: 12、W3: 31、W4: 4）—— 每个 Task 均有 ≤30 min 预估 + 修改文件清单 + 可执行验收命令/期望 exit code |
| 验收清单 | 5 条 Phase 级"一条命令"判定 + 14 项回归检查 |
| 已知局限 | ① W1(766 行)/W3(854 名) 为人力密集型（合计 ≈ 1620 行内容产出）；101 个 Task × 均值 ≈28 min → wall-clock 估计 **≈ 45 h**；② 覆盖率终值取决于 D2 裁决；③ 抽检语义判定（M1/M2）无法完全机械化 |

## 待裁决落地记录（由父代理/用户回写）

| # | 裁决 | 日期 | 载体 |
|---|------|------|------|
| D2-1 | **A. 入表** —— `vmec`/`desc`/`simsopt`/`cate`/`pactole`/`pactiter`/`tract`/`oscar` 8 个 code 以代号形式写入 allowlist（先例 99/107） | 2026-10-26 | 用户在本会话显式裁决（question 工具，选项 A） |
| D2-2 | **A. 只入领域专指项** —— W2 的 EN 侧只写 36 个领域专指概念 + 8 个 code；21 个通用英文词（`design`/`system`/`method`/`wall`/`steel`…）**不写入** `allowlist_en.txt` | 2026-10-26 | 同上 |
| D2-3 | **A. 后续批次** —— 剩余 1517 行「低信息但未损坏」zh 模板释义（762 行 `指“X”` + 755 行 `对应英文“X”`）**不在本批范围**，登记为独立后续批次 | 2026-10-26 | 同上 |
| D2-4 | **A. 每批 100% 机械门禁 + 每 5 批抽检 10%（≥8 行）由独立 agent 复核语义**；抽检 FAIL → 该 5 批返工 | 2026-10-26 | 同上 |
| D2-5 | **A. 允许仓外权威来源** —— W3 命名依据可用 `preferred_en` + Wikipedia/IAEA/ITER 等权威 URL（须实测 HTTP 200）；仓内 `GB/T-4960.9` 释义为优先来源 | 2026-10-26 | 同上 |

> **裁决状态：D2-1 ~ D2-5 全部已裁决（2026-10-26，用户在本会话以结构化选项选定 A）**。以下前置的用户口径同样构成本计划的执行前提：
> ① W1 口径 = **重写全部**（含 746 条 en 通用套话，非删除）；② **专名不入 IME 词表**（company 25 / organization 8 / facility 3 共 36 个排除）；③ **W3 并入本批次**（不独立排期）；④ 先落本计划文件、再由 Dev Orchestrator 逐任务闭环执行。

## Execution Log

> 由 Dev Orchestrator / Task Executor 在执行过程中追加；每条含 `[YYYY-MM-DD HH:MM] Task X.Y — [STATUS]` + 命令原文 + 实测输出（≥3 行）。
> 结构化失败项请用 ```json fenced block 落 `error_id/error_type/summary/root_cause_guess/confidence/retry_suggestion/blocked_downstream/task_id/attempted_fixes`，供 `mode=improve` 解析。

（尚无记录）
