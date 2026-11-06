# 5072 状态对账报告 — W3a 证据与释义补强

- **Plan under review**: `.github/plans/5072-w3a-evidence-definition-backfill.md`（1350 行，rev 2，mtime 2026-11-03）
- **PM task**: #5072（标题 `T-4973 W3a 证据与释义补强`）
- **Review date**: 2026-11-05（`date` 实测 `Thu Nov  5 03:25:47 PM CST 2026`）
- **Author**: doc-maintainer（S4 文档卫生巡检）
- **Nature**: 只读对账。**本报告不修改 5072 计划，不改变任何任务状态，不创建 PM 任务。**
- **Verification base**: `master` HEAD（`git log --oneline -1` = `5013321`），工作区未跟踪文件不纳入任何判断。

---

## 1. 矛盾陈述（原文引用）

### 1.1 头部声称「已执行 + 已独立验收」

`.github/plans/5072-w3a-evidence-definition-backfill.md`：

```
 L10  status: "done-execution (data unreleased)"
 L16  > **状态回写（2026-11-03，PM #5184）**：执行与独立验收已完成；**数据未进入任何发布 tag**
      > （`git tag --contains d84aabc`=0），不得宣称已发布。
```

- L16 的 tag 断言**实测为真**：`git tag --contains d84aabc | wc -l` = `0`，`git tag --contains 115da74 | wc -l` = `0`，
  `git merge-base --is-ancestor d84aabc HEAD` = 真（已合入 master，但未被任何 tag 覆盖）。
- 与 L10 **同一份 frontmatter / 同一段状态区**里，第 20 行仍写：

```
 L20  > **Status**: ACTIVE (2026-10-31, rev 2 — CT REFUTED 后按用户裁决修订)
```

⇒ 头部自身即存在 `status:` = `done-execution` 与正文 `Status: ACTIVE` 的**直接冲突**（同文件两处，未收敛）。

### 1.2 尾部验收块整块未勾

```
 L911  - [ ] P1: `curl -sS -o /dev/null -w '%{http_code}' -L -A 'Mozilla/5.0' https://www-pub.iaea.org/MTCD/Publications/PDF/PUB1830_web.pdf` → `200`
 L912  - [ ] P2: `curl -sS -o /dev/null -w '%{http_code}' -L -A 'Mozilla/5.0' https://www.iter.org/fusion-glossary` → `200`
 L916  - [ ] M1: 独立 verifier 对 75 条 zh 抽检做语义复核（DEFINITION：无新增事实/数字/缩写；CROSS_REF/CORRUPT：目标名恰当、污染未混入）。
 L917  - [ ] M2: 独立 verifier 对 86 条 evidence quote 与 raw 源做逐字对照。
 L918  - [ ] M3: 确认 `concepts.tsv` 的 `preferred_zh` / `category` 与 BASE 逐字节一致（只读 diff）。
 L919  - [ ] M4: 确认附录 C 的 29 条 `NO-TARGET` 英文目标行可被后续「概念补登」任务直接消费（不在本任务修）。
```

```
 L925  | I1a | `w3.ids` 854 条 zh 行全部非占位，占位计数 0 | 二元 |
 L926  | I1b | 431 条 `DEFINITION`：CJK + 无占位 + 数字/缩写多重集相等 + `source = translated:*` | 二元 |
 L927  | I1c | 316 条 `CROSS_REF` 族：zh 匹配 `^见 .+。$` 且无 `[]!;`；287 条目标 ∈ `concepts.preferred_zh`；29 条出现在附录 C 台账 | 二元 |
 L928  | I2 | 854 条 evidence 全部至少 1 条非空 quote | 二元 |
 L929  | I3 | 854 条 evidence 的 source 均为 URL，`--check-urls` exit 0，`probes=2` | 二元 |
 L930  | I4 | self-test 27/27 exit 0 | 二元 |
 L931  | I5 | `validate_registry` / `pytest` / `row_audit` / ruff 全 exit 0 | 二元 |
 L932  | I6 | 独立抽检 75 zh + 86 evidence，FAIL = 0 | 二元 |
 L933  | I7 | 修改范围仅 `definitions.tsv` / `evidence.tsv` / `registry_batch_verify.py` / `CHANGELOG.md` | 二元 |
 L934  | I8 | 每个批次有独立 commit，message 含 `#T-5072` | 二元 |
 L935  | I9 | 附录 C 的 16 条 CORRUPT 行均有污染描述，且 zh 未复现污染 | 二元 |
```

**性质判定**：§10「独立验收清单」是一张**判定表（`| # | 条件 | 判定 |`），不是 checkbox 清单——表里没有
「已签收 / 已勾」这一列，所以「未打勾」本身不是伪证**。矛盾的真正来源是：**L16 宣称「独立验收已完成」，
但 §10 全表没有留下任何签收痕迹（无 PASS/FAIL 列、无签收人、无日期）**，而 §9 的 P1–P4 / M1–M4
又以 `- [ ]` 形式保持空白。**声称方（L16）与被声称对象（§10 / §9）之间缺少可核验的落痕**。

---

## 2. 逐项核验：可从仓库证据判定

以下均为**本次实测**（命令 + 结果），只读，未改任何数据。

| 判据 | 计划期望 | 实测结果 | 判定 |
|---|---|---:|---|
| V1 / I4 | self-test `27/27`, exit 0 | `registry_batch_verify.py --self-test` → `27/27 assertions passed`, exit 0 | ✅ DONE |
| V2 / I1a | `w3_zh=854 placeholder=0` | w3.ids 854 条；zh 行 854；含「对应英文」占位 = **0**；非空 zh = 854 | ✅ DONE |
| V3 / I2 / I3 | `ids=854 expect=854 verdict=PASS`，`probes=2` | `--mode evidence --ids-file w3.ids --expect 854 --check-urls` → `verdict=PASS`, `probes=2`, exit 0；data 层 854/854 有非空 quote，854/854 source 为 http(s) | ✅ DONE |
| V4 / I5a | `validate_registry` exit 0 | `registry OK: 3075 concepts, 10250 aliases, 3202 evidence rows, 6150 definitions`, exit 0 | ✅ DONE |
| V5 / I5b | `pytest` exit 0, 186 tests | **207 passed** in 8.59s, exit 0 | ✅ DONE（计数上漂 186→207；pass/fail 语义未变） |
| V6 / I5c | `row_audit --expect-clean-all` exit 0 | exit 0, `w0_is_clean: true` | ✅ DONE |
| V7 / I5d | ruff 双命令 exit 0 | `ruff check .` → `All checks passed!` exit 0；**`ruff format --check .` exit 1**（3 files would be reformatted） | ⚠️ **NOT DONE（已外因化，见 §3.1）** |
| V9 / I1b | 431 条 `translated:*` | 非 `See X.` 的 en 行 = 502，其 zh 无一条 `见 `-form；source 前缀分布 `translated:747` / `internal:81` / `GB/T-4960.9:26` | ✅ DONE（口径见 §3.3） |
| V10 / I1c | `{DEFINITION:431, CROSS_REF:300, CORRUPT:16}` | en `See X.` 行 = **352**，其中 zh 为 `见 X。` = **316**，余 36 条非 `见`-form | ✅ DONE（316 族精确；352 为超集，见 §3.2） |
| V11 / I1c | 316 条中 287 ∈ `preferred_zh`，29 条 ∈ 附录 C | targets 316 → **287 在 `preferred_zh`**、**29 不在**（样例：`waste container`/`volcano`/`eruption`/`waste`） | ✅ DONE（数字逐字吻合） |
| V12 | `grep -c '19/24'`=0 且 `grep -c '27/27'`≥1 | `0` / `1` | ✅ DONE |
| I8 | 每批独立 commit 含 `#T-5072` | `git log --grep='#T-5072' \| wc -l` = **44**（计划门槛 ≥38） | ✅ DONE |
| I7 / V8 | 仅 4 个声明文件（计划另计） | `git diff --stat b0bef07..115da74` → `definitions.tsv` / `evidence.tsv` / `registry_batch_verify.py` / `5072-*.md` / `CHANGELOG.md`（CHANGELOG 另计，符合 T3.4 声明） | ✅ DONE |

**结论：V1–V12 中 11 项可复现 PASS，1 项（V7 的 `ruff format --check`）当前为 FAIL。**

---

## 3. 关键发现（含不可判定项）

### 3.1 `ruff format --check` 当前失败，但不归因于 5072（pre-existing / 他任务引入）

```
$ .venv/bin/ruff format --check .
3 files would be reformatted, 193 files already formatted       (exit 1)
```

未格式化的 3 个文件全部**不是 5072 声明范围内的文件**：

| 文件 | 引入 commit |
|---|---|
| `.github/plans/5184-m3-m1-repair.md` | 未跟踪（`??`，另一会话在写） |
| `docs/reviews/t5184/repair-m3-execution.md` | `1d2dfc1`（#T-5257） |
| `tests/test_registry_physical_sputtering_projection.py` | `5013321`（#T-5257） |

⇒ I5 在 5072 执行时（2026-11-03）为真，**此后被 #T-5257 与并发未跟踪文件打破**。
**这是回归，但责任不在 5072**；且修复它们触碰 `tests/`/他任务输出，超出本次 S4 授权范围（见 §6）。
不建议就此重开 5072——应作为 5184/5257 侧的独立格式门禁项处理。

### 3.2 352 vs 316 的口径差已由计划自证，不是缺口

en 侧 `See X.` 形态共 352 条，而 W3a 族只收 316 条（300 + 16 CORRUPT）。差额 36 条是**非 w3 范围的
`See X.` 行**（样例 `abnormal-operation`：en `See plant states (considered in design): …`，zh 为真实翻译
而非 `见`-form）。计划 §6 / L161「已知限制」明确把「非 w3 的 303 条 en 短定义 / 1040 条空 quote」
列为**不在验收口径内**。⇒ **36 条属计划外超集，非未完成项**。

### 3.3 `source=translated:747` 与 I1b「431 条 translated」不构成矛盾

747 = 431（DEFINITION 翻译）+ 316（CROSS_REF 方案甲补齐），**全部**以 `translated:` 前缀落盘；
剩余 81 `internal:` + 26 `GB/T-4960.9:` 为既有非占位行（本任务前已存在）。I1b 约束的是
**431 条必须在 `translated:*` 之列**，747 ⊇ 431，满足。⇒ 通过。

### 3.4 无法从仓库证据判定的部分（UNVERIFIABLE）

| 项 | 无法判定的原因 |
|---|---|
| **I6 / M1 / M2（独立抽检 75 zh + 86 evidence）** | 独立 verifier 的抽检结论只存在于计划 L818–819 的判定规则与会话产物，**仓内无签署文件**（不同于 #5184 的 `docs/reviews/t5184/` 有落盘证据）。L16 的「独立验收已完成」**缺少可引用的验收产物**。 |
| **M3（`concepts.tsv` 与 BASE 逐字节一致）** | 需对 `b0bef07` 做只读 diff；`terms/` 自 2026-11-03 后已被 #T-5257/#T-5184 repair 改动（`concepts.tsv` mtime 2026-11-05 12:41），**当前工作区无法还原到 5072 收尾时刻**判定。 |
| **M4（29 条 `NO-TARGET` 可被后续任务消费）** | 依赖尚未创建的「概念补登」任务；计划自带 `不在本任务修`。**前瞻性确认，非交付项**。 |
| **P1 / P2 探针（IAEA / ITER URL 200）** | 本报告未执行外网探针（与 V3 的 `--check-urls` 重复度 100%，V3 已 PASS 且 `probes=2` 恰为这两个 URL，间接覆盖）。 |
| **§13 Execution Log 的 T3.4 自述** | L1001 记录 `#T-5072` commit 数 = 43，本次实测 **44**（含 115da74 自身）。属计数口径差（自述在 commit 落盘前写就），**不影响结论**。 |

### 3.5 独立发现：5072 是父计划归档的**唯一残留阻断**，且其自身也带来一个新阻断

父计划 `.github/plans/terminology-coverage-and-definition-quality.md` L2202 原文（**注意：主语是父计划自身，不是 5072**）：

> 「**未做（用户裁决，`question` 选「同步 IME + 文档收尾，不归档」）**：主计划**不**移入
> `.github/plans/completed/`。理由：PM **5072**（W3a 证据/释义补强）仍为 `todo`（2026-11-03 实测：
> 5072 执行完成、独立验收 PASS，但数据未发布；归档仍暂缓。），归档会误示缺口已关闭。
> **归档动作待 5072 收口后执行。**」

⇒ **父计划**（`terminology-coverage-and-definition-quality.md`）的归档被**绑死在 5072 收口**上：
5072 一日不收口，父计划一日不能归档。而 5072 自身又挂着 12 条专名 known-issue（§4，父计划 L1012
「登记 PM 5072 / 待用户裁决」）⇒ **形成依赖环：父计划等 5072，5072 等专名裁决，专名裁决等用户。**
这是本次对账中最值得上报的结构性问题——它不是任何单个计划的执行缺陷，而是**归档链条上的死锁**。
收敛顺序应为：用户裁决专名 → 5072 补签收并收敛状态 → 归档 5072 → 归档父计划（见 §5 R6→R3/R2→R1）。

---

## 4. 遗留项：12 条专名裁决仍待 USER 裁决（**独立事项，本报告不代行**）

> 本节按任务要求单独标注。**未做任何操作**：未创建任务、未改 `terms/proper_names.txt`、未改 IME 词表。

**来源**：父计划 `terminology-coverage-and-definition-quality.md` L1012（M1 验收项备注）——
`artifacts/domain_terms.txt` 内存在 **12 条专名串**（pre-existing，可追溯至 `161decf`，本任务 allowlist
落地前的人工审定行），全部已在 `terms/proper_names.txt` 台账内逐条登记：

| 段位 | 条目 | 现状 |
|---|---|---|
| `ALLOW_IN_IME` | `新奥` / `欧洲聚变能组织` / `聚变能源机构` / `核工业西南物理研究院` / 等离子体物理研究所 / 联邦聚变系统 / 通用原子能 / 国际原子能机构 | 8 条中文机构名保留并逐条写明理由（`#T-5110 用户裁决`） |
| `EXCLUDE_FROM_IME` | `ENN` / `EUROfusion` / `ICRP` + 其余 7 条多词/未入 allowlist 串 | 3 条拉丁串**已机械排除** |

**实测佐证**：`.rime_import_rime_ice.txt` 中 `ENN` / `EUROfusion` / `ICRP` 命中数 = **0**（拉丁串排除生效）；
上述 8 条中文机构名在 `artifacts/domain_terms.txt` 中均为 **1 次**（仍保留在词表）；`tests/test_proper_names_ledger.py` 11 项全绿。

**仍待 USER 裁决的实质问题**（父计划 L1012 原话）：

> 「**是否删除人工 allowlist 行属数据策略问题**，登记 PM 5072 / 待用户裁决，本任务未擅自删除。」

⇒ 待裁决的是 **8 条中文机构名是否应继续留在 IME 词表**（产品口径），**不是**「是否入台账」。
该裁决是 5072 归档的**前置阻断条件**（§3.5）。

**建议（不执行）**：为这 8 条（台账总计 12 条专名）单开一个新 PM 任务，指向用户提问
（保留全部 / 按频次分级保留 / 全量移除），结论回写 `terms/proper_names.txt` 与父计划 L1012，
再解锁 5072 归档。**不要在 5072 名下就地处理**——它是产品数据策略裁决，不是 W3a 证据补强。

---

## 5. 建议的对账动作（**建议，非执行**）

| # | 动作 | 对象 | 理由 |
|---|---|---|---|
| R1 | **暂不归档 5072 计划**，待 R6 完成后连同 R3/R2 一起执行；5072 归档后再归档父计划 | `.github/plans/5072-*.md`（父计划另案） | 5072 仍承载 12 条专名 known-issue（§4），且 §10 无签收痕迹；先归档会制造「文档说完成、证据没签收」的缺陷，并连带误示父计划缺口已关闭（§3.5）。 |
| R2 | **重开 / 修正状态行**：把 L10 `status` 与 L20 `Status` 收敛为单一表述 | 5072 计划（**由有权限的 agent 执行，非本报告**） | 同一文件两处状态互相矛盾（`done-execution` vs `ACTIVE`），是本次矛盾的结构性根因。建议改为 `status: "done-execution (data unreleased; acceptance signature MISSING; blocked on proper-name ruling §4)"` 并删去/改写 L20 的 `ACTIVE`。 |
| R3 | **补签收 or 补标注** §10：新增一列 `签收证据（命令 exit / 产物路径）`，逐行填本次实测结果 | 5072 计划 | §10 现为无痕判定表。本报告 §2 已给出可直接回填的 13 行实测值。I6/M1/M2 若确实无产物落盘，应显式标注 `UNVERIFIED — no artifact`，**不得**默认 PASS。 |
| R4 | **`ruff format` 回归另案** | #T-5257 / #T-5184 侧 | 3 个未格式化文件均非 5072 交付物（§3.1）。在 5072 名下重开会使归因错误；应由 5184 收口或 5257 跟进。 |
| R5 | **剩余工作归属**：5072 名下**无**未完成的技术交付 | — | W3a 数据侧（V1–V6、V9–V12）已 100% 可复现。遗留 = (a) 签收痕迹（R3，文档）、(b) 专名裁决（§4，**新任务**）、(c) 格式回归（R4，他任务）。 |
| R6 | **新任务**：8 条中文机构名 IME 去留裁决 | 新 PM 任务（**未创建**） | 见 §4。这是 5072 收口与父计划归档链上的**起点阻断**（§3.5）。 |

> **收敛顺序**：R6（用户裁决）→ R3（补签收痕迹）+ R2（状态行收敛）→ R1（归档 5072）→ 归档父计划。R4 与本链无关，可并行。

---

## 6. 本次刻意未做的事

| 未做 | 原因 |
|---|---|
| 未移动 5072 计划到 `completed/` | 5072 仍承载专名 known-issue（§4），且 §10 无签收痕迹；先归档会误示父计划缺口已关闭（§3.5 / R1）。 |
| 未修改 5072 计划任何一行 | 任务硬性要求「不修改 5072 计划、不改变任务状态」；改动应走 R2/R3 且有权限的 agent。 |
| 未勾选 / 未取消勾选 P1–P4、M1–M4 | 同上；且 P/M 项属「执行者签收」职责，非文档管理员。 |
| 未把 I6/M1/M2 判为 PASS | 仓内无可引用验收产物 ⇒ 只能记 `UNVERIFIABLE`（§3.4），不得脑补。 |
| 未修复 3 个 `ruff format` 失败文件 | 触碰 `tests/`、他任务产物与并发未跟踪文件，超 S4 授权（§3.1 / R4）。 |
| 未创建 PM 任务（专名 / 格式回归） | 任务边界明令禁止创建 PM 任务。 |
| 未执行 P1/P2 外网探针 | V3 已 `--check-urls` PASS 且 `probes=2`，探针目标完全重合，重复执行无增量。 |
| 未触碰 `terms/`、`artifacts/`、`pipeline/`、`dist/`、`CHANGELOG.md`、`docs/publication/`、`evaluation/` | 任务边界硬约束。 |

---

## 7. 结论

**PARTIAL / 需用户裁决后收敛。** 5072 的技术交付（W3a 854 条 zh 释义 + 854 条 evidence quote +
self-test 27/27）**可从仓库证据完全复现，属实完成**；但「独立验收已完成」这一句**缺少仓内可核验的
签收产物**，且计划文件自身状态行（L10 vs L20）自相矛盾、§10 判定表无签收痕迹。同时 5072 仍承载
12 条专名 known-issue，使**父计划归档 ← 5072 收口 ← 专名裁决 ← 用户** 构成依赖环（§3.5）。
⇒ **暂不归档（保持原地），建议：用户先裁决 8 条中文机构名 → 5072 补签收并收敛状态行 → 再归档 5072 → 最后归档父计划。**

→ handoff: USER

---

## 4.1 用户裁决（2026-11-06）：8 个中文机构名**保留排除**

- **裁决**：用户 2026-11-06 经 `question` 选定「**保留排除（维持现状，推荐）**」。
- **落地**：`terms/proper_names.txt` 中 8 个中文机构名（如 `国际原子能机构`、`新奥` 等）**继续** `EXCLUDE_FROM_IME`；**不新增、不删除**台账行；`terms/allowlist_zh.txt` 不为它们补录。
- **依据**：台账语义（`pipeline/proper_names.py` 文件头）明确「机构/公司名属 registry 身份，不属 IME 词表」；中文输入法实际极少键入全称。
- **对本报告结论的影响**：§4 记录的「12 个专名待裁决」中，**中文机构名这 8 项至此定案**（另 3 项为纯 ASCII 装置名，已在 `allowlist_en.txt`，本就不属 zh IME 词表；余 1 项为计数口径差）。⇒ **本报告 R1（5072 归档）的前置阻断已解除**。
- **仍未执行（需另行授权，本次不做）**：R2（统一 `L10`/`L20` 状态行）、R3（§10 表格补「命令 + exit + 产物路径」或标 `UNVERIFIED`）、R5/R6（归档 5072 与父计划链）。上述三项均为**写操作**，未包含在本次「保留排除」裁决内。
