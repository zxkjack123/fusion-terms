# 四阶段证据索引 — PM #5184

**Status**: COMPLETED（2026-11-03 收口；`date` 实测 `Tue Nov  3 03:06:54 PM CST 2026`）

判定：PASS / FAIL / UNDECIDABLE。UNDECIDABLE 不计 PASS；M1 需 64/64 PASS，M4 需 10/10 PASS；M3 待裁决保持未勾。

> **收口口径（本文件 = 执行事实索引，非验收结论本身）**：执行区间 **`115da74..3d54c3e`（20 个 commit，全部 `#T-5184`）**；独立验收另有 `/tmp/opencode/t5184-final-acceptance.md`（acceptance-verifier，2026-11-03T14:59:54+08:00），V1–V9 全 PASS，探针 P1 `registry_batch_verify --self-test` = `27/27`、P2 `pytest -q` = 178 tests 全通过。
> **哈希口径（固定用已验收区间，不用 `HEAD~20`）**：下方所有复算命令一律锚定 **`115da74..3d54c3e`**。**不得**改用 `HEAD~20..HEAD`——本次收口会新增文档 commit 使 `HEAD` 前移，`HEAD~20` 会静默滑出已验收区间并把收口 commit 计入，导致「20 个 commit / 数据零改动 / 行数断言」全部失真。
> **本收口 commit 不在 20 个执行 commit 之内**：它只更新 `docs/reviews/t5184/README.md` 与计划文件（归档至 `completed/`），因此区间取 `115da74..3d54c3e` 而非 `..HEAD`。
> **计划归档位置**：`.github/plans/completed/5184-four-stage-closeout.md`（绝对路径 `/home/gw/opt/fusion-terms/.github/plans/completed/5184-four-stage-closeout.md`）。

| 阶段 | 产物路径（相对此目录） | 状态 |
|---|---|---|
| S1 | status-writeback.md | 已完成（T1.1–T1.3 全部提交） |
| S2 | m3-physical-sputtering.md（+ m3-evidence-rows.tsv） | 已完成（查证完成；**M3 裁决待用户，父计划保持未勾**） |
| S3 | m4-column-semantics.md（+ m4-sample.tsv） | 已完成（10/10 PASS，M4 已勾） |
| S4 | m1-summary.md（+ m1-sample-manifest.tsv、m1-group-G1..G8.md） | 已完成（55 PASS / 9 FAIL / 0 UNDECIDABLE，**M1 未勾**） |

| Task | 状态 | commit |
|---|---|---|
| T1.1 | PASS | 86e9b00 |
| T1.2 | PASS（IMPROVE-1 修订 AC 后独立复验；原 FAIL 保留见 §S1 执行记录） | 52dc8e8 |
| T1.3 | PASS（PM #5184 备注 + readback `status=doing`） | 791d189 |
| T2.1 | PASS（`TOTAL= 1` 冲突全集） | f2a520f |
| T2.2 | PASS（下游投影实测） | d87da10 |
| T2.3 | PASS（语义层级 / 来源可得性，H3=`UNDECIDABLE`） | 769c168 |
| T2.4 | PASS（A/B/C 三选项；**待用户裁决，未宣称授权**） | fa602ed |
| T3.1 | PASS（10 行确定性样本清单） | 4d8d003 |
| T3.2 | PASS（10 行列语义逐列留痕） | 477fc7f |
| T3.3 | PASS（M4 写回 `[x]`，10/10 PASS） | d16a11d |
| T4.1 | PASS（8×8 确定性样本 manifest + 8 条 set hash） | c2d3d3a |
| T4.2 | PASS（G1：5 PASS / 3 FAIL） | 6dde42b |
| T4.3 | PASS（G2：8/0） | 76cd84d |
| T4.4 | PASS（G3：8/0） | a174af4 |
| T4.5 | PASS（G4：6/2） | 488a1c3 |
| T4.6 | PASS（G5：6/2） | 1cf7bab |
| T4.7 | PASS（G6：6/2） | 0f335ec |
| T4.8 | PASS（G7：8/0） | 44c7d90 |
| T4.9 | PASS（G8：8/0） | 495f904 |
| T4.10 | PASS（汇总 55/9/0；**FAIL=9>0，M1 保持未勾**） | 3d54c3e |

> Task 的「PASS」= 该 Task 的交付与 AC 完成；**不等于**对应父计划 M 项已勾。父计划 M 项实际状态见下。

## 父计划 M 项实际状态（父计划文件本体，本收口未改）

| M 项 | 父计划行 | 状态 | 原因 |
|---|---|---|---|
| M1 | `terminology-coverage-and-definition-quality.md:979` | `- [ ]` 未勾 | 64/64 抽检中 **PASS 55 / FAIL 9 / UNDECIDABLE 0**，未达 64/64 PASS；缺陷台账 D1–D9（9 行）= FAIL 数 |
| M3 | `:981` | `- [ ]` 未勾 | S2 查证完成，但「人工裁决」未发生 → `待用户裁决 (D2)`，无授权声明 |
| M4 | `:982` | `- [x]` 已勾 | 10/10 PASS（`^判定: PASS$` = 10，FAIL=0，UNDECIDABLE=0），仅在 d16a11d（T3.3）授权阶段勾选 |

## Phase Record S1
phase_goal: 事实矩阵、状态对齐与 PM 回写。
phase_exit: T1.1–T1.3 AC 通过并分别提交。
accepted_baseline: HEAD 115da74；无 checkpoint；仅执行计划未跟踪。

## S1 执行记录

T1.1：86e9b00；T1.2：52dc8e8；T1.3：791d189。
T1.2 **初次 AC#5 FAIL**（旧白名单空转且按字面不可满足，命令块未设 `set -e`，AC 失败仍生成 52dc8e8）——该 finding **保留，不抹历史、不改写 52dc8e8**；IMPROVE-1 修订 AC 后由 acceptance-verifier 独立复验，AC 7/7。后续所有 Task 以 `set -euo pipefail` + 提交前 `git diff --cached` 范围断言执行。
T1.3：pm-coordinator 已追加 #5184 备注并回读 status=doing；保留原备注前缀。
Receipt: /home/gw/opt/copilot-agents/.receipts/T5184-status-writeback.r1.json

## S2 / S3 / S4 执行记录

- **S2（T2.1–T2.4，f2a520f..fa602ed）**：冲突全集 `TOTAL= 1`（`aliases.tsv:397` `物理溅射 → sputtering`）；H1/H2 PASS、H3 **UNDECIDABLE**（上游 `artifacts/terminology_sources/` 6 文件对 `物理溅射` / `physical sputtering` 0 命中）；A/B/C 三选项 + `可逆性:` 齐备；报告内「已授权 / 用户已批准」命中 = 0。
- **S3（T3.1–T3.3，4d8d003..d16a11d）**：10 行样本由 `sed -n '2p;21p;41p;61p;81p'`（shift99）+ `'2p;17p;33p;49p;65p'`（sixcol80）确定性抽取，独立复算 10/10 与 `m4-sample.tsv` 一致；列语义 10/10 PASS。
- **S4（T4.1–T4.10，c2d3d3a..3d54c3e）**：8 组 × 8 行 = 64 / 756 ids（8.5%）；组内 id 数 87/100×6/69，39 批连续切分实测吻合；三值合计 **55 / 9 / 0**。

## 哈希口径与复算例（V9 固化）

**契约（唯一正确口径）**：`sha256( '\n'.join(sorted(ids)) )` —— id **升序排序**，以**换行连接**，**不含末尾换行**，UTF-8 编码。

- 反例（会 8/8 不匹配）：`cat ids | sha256sum`（保留末尾换行）、按 manifest 文件出现顺序连接、`id\t<sha256>` 拼接。
- 实测（本收口复算，8/8 MATCH）：
  - G1 = `317638db70047ff5343d125ffbf27bce7991ea3e8b02f3d4f84b5f84053d36a9` → 与 manifest `# group_sample_sha256 G1` 一致；
  - 同组加末尾换行 = `03f3c7a9…bad10c` → **不匹配**，证明「无末尾换行」是契约的一部分。

复算例（可直接粘贴，只用已跟踪文件与本区间）：

```bash
cd /home/gw/opt/fusion-terms
# 逐组复算并与 manifest 内嵌值比对（期望 8 行全部 MATCH）
python3 - <<'PY'
import hashlib
from collections import defaultdict
M='docs/reviews/t5184/m1-sample-manifest.tsv'
g=defaultdict(list); exp={}
for l in open(M):
    if l.startswith('# group_sample_sha256'):
        _,_,grp,h=l.split(); exp[grp]=h
    elif not l.startswith('group\t'):
        g[l.split('\t')[0]].append(l.rstrip('\n').split('\t')[2])
for grp in sorted(g):
    got=hashlib.sha256('\n'.join(sorted(g[grp])).encode()).hexdigest()   # 排序 + \n 连接 + 无末尾换行
    print(grp, 'MATCH' if got==exp[grp] else 'MISMATCH')
PY
```

## 区间与范围复算（固定用 115da74..3d54c3e，不用 HEAD~20）

```bash
cd /home/gw/opt/fusion-terms
git rev-list --count 115da74..3d54c3e                                    # 期望 20
git log --oneline 115da74..3d54c3e --grep='#T-5184' | wc -l              # 期望 20
git diff --stat 115da74 3d54c3e -- terms/ artifacts/ pipeline/ scripts/  # 期望空（数据零改动）
git diff --check 115da74 3d54c3e                                         # 期望空，exit 0
git show --stat --name-only 115da74..3d54c3e | grep -vE '^(docs/reviews/t5184/|\.github/plans/(5072-w3a-evidence-definition-backfill|terminology-coverage-and-definition-quality)\.md)' | grep -vE '^(commit |$|[0-9]+ files? changed)'   # 期望空：区间内只碰报告与两个父/兄弟计划的指定行
```

> 说明：`HEAD~20` 写法在本次收口后**不再等价于**已验收区间——新增文档 commit 会把窗口整体前移一格。所有复验请使用上文的固定 SHA 区间。

## 已知限制（表述边界，不得超范围引用）

1. **64/64 corpus ≠ 外部源验证**：64 个样本 id 的 `concepts.tsv` 第 8 列 `source` **全部为 `corpus`**（64/64）。这只说明「notes 原文在仓内语料可得」，因此 `UNDECIDABLE=0` 在结构上成立；**不构成**对 GB/T、IAEA、ITER、URL 四类外部依据路径的覆盖（零覆盖）。不得把 64/64 引述为「外部权威源已验证」。
2. **抽检 ≠ 全量**：64 / 756 = 8.5%，不得外推为 W1 全量语义正确性；机械门禁（格式/占位/长度）不覆盖语义。
3. **9 条 FAIL 是审查发现，不是修复授权**：D1–D9 需另行裁决/补证，本轮未改任何 `terms/` 数据。
4. **M3 未裁决**：本仓库无 `物理溅射` 的中文权威条目，`UNDECIDABLE` 不等于「不存在冲突/无问题」。
5. **组报告字段标签不统一（O5）**：G4/G5/G6 使用 `- 原始语料:` 行内形式，计划字面 AC 的 `^原始语料:` 行首格式在这 3 组不成立（内容字段实质齐备）；非阻塞项，已在计划归档件中登记为已知偏差。
6. **5072 数据未发布**：`git tag --contains d84aabc` = 0；`v2026.10.30` = `fa34be1` 早于 5072 全部提交，本计划未触发重发。
