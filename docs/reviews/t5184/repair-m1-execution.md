# T-5259 — M1（D1–D9）逐项验证-修复 · 执行与收口报告

Audience: repository developers / agents（内部技术产物 ⇒ `[de-ai-fier: N/A — 受众为开发者/agent]`）。

- 报告日期：`2026-11-05`（`date -Iseconds` 实测，见 §7 证据）
- 计划依据：`.github/plans/5184-m3-m1-repair.md` §6（M1 D1–D9 逐项验证-修复）+ §10.2 V13
- PM 任务：**`#T-5259`**（本链全部 commit 尾标；无 `#T-5184`）
- 链起点：`ea5411d`（S1 关闭 M3）；链终点：`fa6048b`；`master ... origin/master [ahead 36]`；**无 tag、未 push**
- 审查性质声明：`docs/reviews/t5184/m1-summary.md` 的三值口径（**55 PASS / 9 FAIL / 0 UNDECIDABLE**，抽检 64/756 = 8.5%）**未被本报告改写**；本报告记录 D1–D9 的**逐项处置**，不重判抽检结论。

---

## 1. 处置总表

| D | concept | 判定 | 处置 | commit | 改动面 |
|---|---|---|---|---|---|
| D1 | `turbulent-transport` | 证据充分 | 改 `notes` 对齐 GB/T 定义（撤除侵入 `anomalous-transport` 语义域的未声明限定） | `2e267b3` | `concepts.tsv` 1/1 |
| D4 | `debye-shielding` | 证据充分 | 补强 corpus 定义：机制 + 特征尺度 λ_D（**source 维持 `corpus`，不冒称 GB/T**） | `8e64972` | `definitions.tsv` 2/2 |
| D9 | `rupture-disc` | 证据充分（仓内依据引语） | zh 删越界词「主动」、en 补 `at set pressure differential`；**同缺陷面**同步清理 `concepts.tsv` notes 的同一越界词 | `65bdcea` | `concepts.tsv` 1/1 + `definitions.tsv` 2/2 |
| D6 | `nuclide-inventory` | 证据充分 | 首选 zh `核素产额`→`核素存量`；`核素产额` 降为 **`deprecated`**（**非** `forbidden`，避免改写作门）；重建投影 | `3be960b` | `concepts.tsv`/`definitions.tsv`/`aliases.tsv` + `translation_dict.json` + `terminology_substitutions.tsv` |
| D2 | `lawson-criterion` | 证据充分（R3 唯一授权路径 ①） | 仅改 `notes` 对齐 GB/T 双门限口径并写入与 `fusion-triple-product` 的边界；**`definitions.tsv` 双行 sha256 前后一致** | `9668c2f` | `concepts.tsv` 1/1 |
| D8 | `plasma-termination` | 证据充分 | 合并 → `plasma-shutdown`（保留 gleiche face 为 alias、清孤儿、保号注释免断 self-test 锚点）；补救：恢复 zh preferred 面 `等离子体熄灭`、修正 3 条 zh 规则指向、刷新 tracked 投影 | `b8d4fda` + `fa6048b` | `concepts.tsv`/`definitions.tsv`/`aliases.tsv`/`evidence.tsv` + 2 tracked artifacts |
| D3 | `poloidal-field-coil` | **UNDECIDABLE** | 只登记不改（建议见 `repair-m1-b1-suggestion.md`） | `644b9a7` | 仅新增报告 |
| D5 | `pfirsch-schlueter-regime` | **UNDECIDABLE** | 只登记不改（建议见 `repair-m1-b2-suggestion.md`） | `2e13370` | 仅新增报告 |
| D7 | `nuclear-fusion` | **UNDECIDABLE（见 §5 O-5 定性修正）** | 只登记不改（建议见 `repair-m1-b3-suggestion.md`） | `8460437` | 仅新增报告 |

**计数**：已修 **6**（D1/D2/D4/D6/D8/D9）｜`UNDECIDABLE` **3**（D3/D5/D7）｜假通过 **0**。

---

## 2. 每项的门禁与关键断言（全部实跑，exit 记录）

- 数据改动项（D1/D4/D9/D6/D2/D8）逐项：`validate_registry` **exit 0**、`registry_row_audit --audit` **exit 0 / `is_clean`: true**、`registry_batch_verify --self-test` **27/27**、`pytest -o addopts="" -q` **failed=0**。
- D2 额外断言：`definitions.tsv` 的 `lawson-criterion` en/zh 行 sha256 前后一致（`2e1acda3d27103ff` / `8ad4d691a36aa601`）。
- D8 额外断言：`^plasma-termination\t` 在 4 个注册表 TSV 中 **0/0/0/0**（孤儿门）；`alias_index['等离子体终止'] == plasma-shutdown`；`plasma-ramp-down` 字节未动；`plasma-ramp-down` 均值哈希与 `b8d4fda~1` 一致。
- D6 额外断言：`nuclide-inventory` 恰有 **1** 条 zh `preferred`；`核素产额` = `deprecated` 且**未**进入 `allowlist_zh.txt`（0 命中）。

## 3. HEAD 门禁（收口时复跑）

| 门禁 | 结果 |
|---|---|
| `python3 -m pipeline.validate_registry` | exit 0 → **3075 concepts / 10250 aliases / 3202 evidence / 6150 definitions** |
| `python3 scripts/registry_row_audit.py --audit` | exit 0 → `is_clean: true` |
| `python3 scripts/registry_batch_verify.py --self-test` | exit 0 → `27/27` |
| `python3 -m pytest -o addopts="" -q` | exit 0 → **207 passed**（0 failed；含本会话+并发会话新增测试） |

**基线漂移说明**：概念 3076→3075、evidence 3203→3202、definitions 6152→6150 全部来自 D8 的合并（1 个概念 + 其 2 条定义 + 1 条 evidence 退役）；aliases 10250→10250（D6 +1、D8 −1、D8 补救 +1）。**无未解释漂移**。

**内容幂等**：以临时 `--out-dir` 重导出后，`terminology_substitutions.tsv` 字节级 MATCH、`translation_dict.json` 忽略 `metadata.generated_at` 后深度相等、`query_expansions.json` 字节 MATCH、`registry_exports.json` 计数全等（差异仅为 out-dir 路径串）。⇒ 派生一致，无悬挂。

## 4. 独立验收（`acceptance-verifier`，只读，2026-11-05）

- **总判：PARTIAL**（`blocking: []`，`cautions` 6 条）。逐项行级断言 D1/D2/D4/D6/D8/D9 双向 byte 对照**全部 ✅**；D3/D5 的 `UNDECIDABLE` 依据**独立复现**（阻碍串在 allowlist 中确实存在、`gbt4960_9_diff.tsv:211` 的 `matched_concept_id` 确实为空、ITER `:98` 同样为空）。
- 其证伪尝试：D3/D5 **未找到**「在既定边界内可修」的反例；D8 修复**真实有效**（`b8d4fda` 时 3 条 zh 规则仍指向中文旧名，`fa6048b` 后指向 `等离子体熄灭`）。
- 其口径纠正（已接受并反映于本报告）：`ahead` 实测 **36**（非 37）；`pytest` 实测 **207**（非计划基线 186）；本报告 §1 的 commit 清单跨越 `ea5411d..HEAD`，其中 D1/D4/D9/D6 不在 `9668c2f~1..HEAD` 范围内（属我先前表述的基线混淆，**已更正**）。

## 5. 已知问题（Known Issues；**非阻塞**，须另行授权）

| # | 内容 | 定性 |
|---|---|---|
| **O-1** | `registry_batch_verify --mode allowlist` 对 `nuclide-inventory` 报 `allow_zh_not_listed`（`preferred_zh` 未列入 `terms/allowlist_zh.txt`） | **既有类级缺口，非本次引入**：真实 pre-M1 基线（`ea5411d`）即已有 **205** 个概念处于同一状态（D6 改名前 `核素产额` 同样 0 命中），改名后仍为 **205**（净 0）。修法需写 `terms/allowlist_*`（**硬禁止**）⇒ 只登记建议，另立授权任务 |
| **O-2** | `terms/allowlist_en.txt:1120` 保留已退役 `plasma-termination` | 既有 IME 词表残留；`repair-m1-b4-merge.md` §6/§8 已声明；注册表层无孤儿 |
| **O-3** | 含退役 id 的 ids-file 经 `registry_batch_verify` 会得 `concept_id_missing` | 既有测试夹具级联，非本次引入 |
| **O-4** | `terminology_substitutions.tsv` 中 **67** 条 zh 规则给出英文替换 | 与 pre-M1 **同值（67→67，净 0）**；D8 修复的是其命中的**该实例**，未及**该类**（类级审计需另立任务） |
| **O-5** | D7 定性修正：`gbt4960_9_diff.tsv:110` **确实**提供了 `fusion` 的权威指向，按计划自身规则属「证据充分」；实际阻断因素是**结果风险**（把领域名 `核聚变` 挂到自述 `Generic academic glue word` 的概念）+ `allowlist_zh.txt:1128` 钉住 `核聚变` | 建议改述为「证据充分但结果风险被拒」；**不改变数据**。B3 报告中的 `UNDECIDABLE` 字样以此节为准 |

**另有 1 处需登记的观察**：D9 与 D8 的改动使 `concepts.tsv`/`definitions.tsv` 出现 `# retired (#)…` 与行注释标记——经 `validate_registry`（逐行列数/重复键校验）与全量 `pytest` 验证**不破坏消费方**；导出器亦正确跳过注释行。

## 6. M1 完成判定（**未达；复选框保持未勾**）

依据计划 §8.5 / §10.2 V13：勾选需要 **重跑抽检 64/64 PASS + 独立验收签署 + 用户确认**，三者缺一不可。

- 本次 D1–D9 的处置**不等于** M1 完成：6 项已达**行级**验收，3 项 `UNDECIDABLE` **维持 FAIL** ⇒ **64/64 不可达**。
- 因此 **M1 复选框不得勾选**；本报告不重写 `m1-summary.md` 的 55/9/0 口径。
- 未做：对 64 行样本按 M1 语义 rubric 的**重判**（该重判属新抽检，需独立复核者按原 rubric 执行，且受 `#T-5259` 边界约束）。

## 7. 声明

- **未 push、未创建 tag**；`git tag --points-at HEAD` = 0。
- 未改 `dist/`、`CHANGELOG.md`、`pipeline/*.py`、`terms/allowlist_*`、`artifacts/terminology_sources/*`（只读快照）。
- 并发三路径（`docs/publication/`、`evaluation/`、`.github/plans/publication-program-lre-scientificdata.md`）**未读为判据、未改、未 stage**。
- 3 条 M3 forbidden 行（`aliases.tsv:3812/3813/7050`）**未改写**（本轮未触碰；`aliases.tsv:4242` 亦未改写，仅登记建议）。
- 钩子全程启用：一次 `trim trailing whitespace` 中止后按规范化版本重提（**未使用 `--no-verify`**）。
- 无 `traces/checkpoint.json`（本仓无 traces/ 机制）。

**→ handoff: USER**（M1 勾选需用户确认，且当前不可达；O-1 的 `allowlist_zh` 写入需单独授权；发布面 push/tag 未授权）。

## 6.1 口径修订与本轮收口（2026-11-06，用户裁决 R11）

> 本节为**追加**，不覆盖 §6 的原始判定文字（保留历史）。

- **修订依据**：用户 2026-11-06 经 `question` 选定「修订口径收口 M1（推荐）」；裁决记录见 `.github/plans/5184-m3-m1-repair.md` §0.4 **R11**，判据改写见同文件 §8.5 rev 4 段与 §10 V13 修订注。
- **修订原因**：D3/D5/D7 的三类阻断均落在授权边界之外（`terms/allowlist_*` 硬禁止写入 ⇒ id 无法退役；正字法无仓内权威；D7 为「证据充分但结果语义倒退 + `核聚变` 被 allowlist 钉住」），故 `64/64 PASS` **结构性不可达**，而「维持未勾」会使唯一开放任务永久挂起。
- **修订后判据（三条齐备即收口）**：① 9/9 逐项处置完整（6 修复 + 3 `UNDECIDABLE` 书面归档，各带 commit）；② 独立验收 `PARTIAL` 且 `blocking = []`；③ 用户确认。
- **本轮满足情况**：① 见 §1 总表（`2e267b3` / `8e64972` / `65bdcea` / `3be960b` / `9668c2f` / `b8d4fda`+`fa6048b`；`644b9a7` / `2e13370` / `8460437`）；② 见 §4；③ 用户 2026-11-06 确认。
- **仍然成立的红线**：**不改写** `m1-summary.md` 的 55 PASS / 9 FAIL / 0 UNDECIDABLE；**不声称** 64/64；3 项残余作为已知缺陷保留（§5 O-1…O-5）。重抽检不作为本轮前置。
- **落地**：父计划 M1 行由 `- [ ]` 改为 `- [x]`（附日期与依据注记）；PM `#5259` 置 `done`/100%（由 pm-coordinator 执行，见其回执）。
