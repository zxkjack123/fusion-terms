# #5290 — allowlist 覆盖补齐（`preferred_zh` → `terms/allowlist_zh.txt`）执行报告

Audience: repository developers / agents（内部技术产物 ⇒ `[de-ai-fier: N/A — 受众为开发者/agent]`）。

- 执行日期：`2026-11-06`（`date -Iseconds` 实测）
- 基线：`3155ecc`（`master` ahead 38，无 tag，tracked clean）
- 授权：用户 2026-11-06 本会话「做#5290」；任务 notes 要求的**前置影响评估**见 §2
- 任务：PM **`#5290`**（发现于 `#5259` 的 O-1；commit 尾标 `#T-5290`）

---

## 1. 背景与口径修正

任务登记时记录的缺口为「205 个概念 `preferred_zh` 未收录（含 CJK）；全量 208（含 3 条纯 ASCII）」。本次实测确认：

| 口径 | 数量 |
|---|---|
| `preferred_zh` 未出现在 `terms/allowlist_zh.txt` 的概念 | **205** |
| 其中 CJK 面 | 202 |
| 其中纯 ASCII 面（`W7-X` / `HSX` / `NIF`） | 3 |

`205` = 任务标题口径（CJK 相关）；`208` = 全量含 ASCII。**本报告统一用 205 作为「CJK 缺口」起点**。

## 2. 前置影响评估（先评估后改动）

| 维度 | 评估结果 |
|---|---|
| **`allowlist_zh.txt` 的消费者** | `pipeline/build_terms.py:204`（→ IME 词表 `artifacts/domain_terms.txt`，**该产物 untracked**）、`pipeline/proper_names.py`（专名台账）、`pipeline/review_pack.py`、`pipeline/release_pack.py:94`（随包发布）、`pipeline/validate_registry.py:310`（bridge check）、`scripts/registry_batch_verify.py`（`--mode allowlist`） |
| **文件结构** | 3929 行；131 行 `#` 段注释（惯例为「批次 + 段头」追加）；无重复行；**非排序**（按批次分段追加）⇒ 采用「追加新段」而非全表重排 |
| **bridge check 冲突** | 205 条缺口与任何 `forbidden`/`deprecated` 别名**零交叉** ⇒ 追加不会触发 `validate_registry` 的 allowlist 泄漏检查 |
| **类别排除项（政策而非缺口）** | ① **37 条**命中 `terms/proper_names.txt` 的 `EXCLUDE_FROM_IME`（机构/公司名，台账明确「属 registry 而不属 IME 词表」）；② **3 条**纯 ASCII 装置名（已在 `allowlist_en.txt`）；③ **5 条**含空格的短语面（`α 通道效应`、`α 功率`、`ITER 试验包层模块`、`L-H 转换阈值功率`、`逃逸 α 粒子探测器`）与 `build_terms` 的「词表不得含空白」契约冲突（与 T-4973 W2 已记录的同类例外一致） |
| **结论** | 合规收录 = 205 − 37 − 3 − 5 = **160 条**；其余 45 条按既有政策**不收录**并要求登记（非未完成工作） |

## 3. 改动

- 文件：`terms/allowlist_zh.txt` **唯一改动文件**
- 形式：末尾追加 1 行段头 + **160** 条词条（按 `concept_id` 稳定排序）
- `git diff --numstat` = **161 / 0** ⇒ **既有行零改动、零删除**；`sort | uniq -d` = **0**（无重复）
- 未改动：`terms/proper_names.txt`（台账）、`terms/allowlist_en.txt`、`terms/registry/*`、`pipeline/*.py`

## 4. 门禁（全绿；含一次被门禁拦下的修正）

| 门禁 | 结果 |
|---|---|
| `python3 -m pipeline.validate_registry` | exit 0 → `registry OK: 3075 concepts, 10250 aliases, 3202 evidence rows, 6150 definitions` |
| `python3 scripts/registry_row_audit.py --audit` | exit 0 → `is_clean: true` |
| `python3 scripts/registry_batch_verify.py --self-test` | exit 0 → `27/27` |
| `python3 -m pytest -o addopts="" -q` | exit 0 → **207 passed** |

**门禁拦截记录（重要）**：首次以 165 条落地后，`pytest` **2 failed** ——
`test_proper_names_ledger.py::test_repo_ledger_matches_repo_registry_and_wordlist` 与
`test_repo_terms_build.py::test_build_from_repo_terms_is_non_empty_and_token_only` 均报
`wordlist terms must not contain whitespace (after deny/synonyms normalization); split phrases into tokens instead`，并逐条列出前述 5 个短语面。
处置：**不改契约、不改测试**，从追加块中剔除这 5 条（165 → 160），复跑后全绿。此即「门禁正常工作」的证据，而非绕过。

## 5. 效果验证（`registry_batch_verify --mode allowlist`，前后同口径）

| 口径 | 前 | 后 |
|---|---|---|
| 受影响 id 数（pre-change 205 个）中报 `allow_zh_not_listed` | **205** | **45** |
| 6-id 抽样（含 `nuclide-inventory` / `核素存量`） | `verdict=FAIL`（`nuclide-inventory` 报错） | **`verdict=PASS`** |
| 残余 45 的分类 | — | `ledger_EXCLUDE` **37** / `ascii_proper` **3** / `whitespace_phrase` **5**，**未分类 0** |

## 6. 残余 45 条（按政策保留，需政策决定而非数据补齐）

| 类 | 数量 | 理由与去向 |
|---|---|---|
| `EXCLUDE_FROM_IME`（`terms/proper_names.txt`） | 37 | 机构/公司名（如 `国际放射防护委员会`、`TAE技术公司`）；台账语义为「进 registry、不进 IME 词表」。若要收录须先改台账政策 |
| 纯 ASCII 装置名 | 3 | `W7-X` / `HSX` / `NIF` 已在 `allowlist_en.txt`；`allowlist_zh` 为中文 IME 词表，收录拉丁名无实际收益 |
| 含空格短语面 | 5 | 与 `build_terms` 的 token-only 契约冲突；如确需支持须改 pipeline 的空白规则（T-4973 同类例外亦如此处理） |

## 7. 声明

- 未 push、未创建 tag；未改 `dist/`、`CHANGELOG.md`、`pipeline/*.py`、`terms/registry/*`、`terms/allowlist_en.txt`、`terms/proper_names.txt`。
- 并发三路径（`docs/publication/`、`evaluation/`、`.github/plans/publication-program-lre-scientificdata.md`）未读为判据、未改、未 stage。
- 钩子全程启用，未使用 `--no-verify`。
- 回滚：`git revert <本 commit>`（单文件、纯追加，完全可逆）。
