# M3 查证报告：`physical-sputtering` / `物理溅射` 与 `sputtering` 的 zh 别名冲突

> **计划**：`.github/plans/5184-four-stage-closeout.md` §Phase S2（PM #5184 / FUSION-TERMS id240）
> **性质**：**只读查证**。本报告只陈述当前词表（registry）与当前 artifacts 的**既有内容与可观测行为**，不做数据修改，**不宣称成因/根因**，不评估上游来源是否正确。
> **判定口径**：`PASS` = 命题与仓内原文/实测无矛盾；`FAIL` = 与原文/实测矛盾；`UNDECIDABLE` = 依据不可得或语义无法判定（不计入 PASS）。
> **本报告不含任何数据写操作**：`terms/registry/*`、`artifacts/*` 全程只读（每 Task 末 `git diff --stat` 断言为空）。

## §1 冲突事实（原行证据）

冲突登记源：`.github/plans/t4973-batches/w3-name-conflicts.tsv:3`
（原文：`physical-sputtering	物理溅射	zh-alias	sputtering	pre-existing (concept 不在 w3.ids；W3a 未修改该行，仅登记)`）

实测：`grep -c '^physical-sputtering$' .github/plans/t4973-batches/w3.ids` = **0** ⇒ 该 concept 确实不在 W3 批次清单内。

以下为本次查证直接读取的原行（逐字，`file:行号`；完整转储见 `docs/reviews/t5184/m3-evidence-rows.tsv`）：

| 表 | 位置 | 原行（列以 `|` 分隔显示） |
|---|---|---|
| concepts | `terms/registry/concepts.tsv:82` | `sputtering` \| `concept` \| `溅射` \| `sputtering` \| (空) \| `active` \| Ejection of surface atoms by energetic particle impact \| `corpus` |
| concepts | `terms/registry/concepts.tsv:712` | `physical-sputtering` \| `concept` \| `物理溅射` \| `physical sputtering` \| (空) \| `active` \| Surface atom ejection by energetic ion bombardment \| `corpus` |
| concepts | `terms/registry/concepts.tsv:1659` | `chemical-sputtering` \| `concept` \| `化学溅射` \| `chemical sputtering` \| (空) \| `active` \| Chemical ejection of surface atoms via reactive hydrogen species \| `corpus` |
| aliases | `terms/registry/aliases.tsv:395` | `溅射` \| `sputtering` \| `zh` \| `preferred` \| preferred zh |
| aliases | `terms/registry/aliases.tsv:397` | `物理溅射` \| `sputtering` \| `zh` \| `alias` \| physical sputtering zh |
| aliases | `terms/registry/aliases.tsv:2501` | `physical sputtering` \| `physical-sputtering` \| `en` \| `preferred` \| (空) |
| aliases | `terms/registry/aliases.tsv:4566` | `物理溅射产额` \| `physical-sputtering` \| `zh` \| `alias` \| yield form |
| aliases | `terms/registry/aliases.tsv:7050` | `物理溅射率` \| `physical-sputtering` \| `zh` \| `forbidden` \| 率暗示时间量纲：正确为 物理溅射(产额) |
| definitions | `terms/registry/definitions.tsv:5503` | `sputtering` \| `en` \| The ejection of atoms from a surface as a result of the impact of energetic particles; a process by which the surface material of a plasma-facing surface is removed by particle bombardment. \| `corpus` |
| definitions | `terms/registry/definitions.tsv:5504` | `sputtering` \| `zh` \| 高能粒子撞击使表面原子被射出的过程，也是面向等离子体表面材料因粒子轰击而被去除的一种机制。 \| `corpus` |
| definitions | `terms/registry/definitions.tsv:5021` | `physical-sputtering` \| `en` \| Ejection of surface atoms by energetic ion bombardment. \| `corpus` |
| definitions | `terms/registry/definitions.tsv:5022` | `physical-sputtering` \| `zh` \| 物理溅射是高能离子轰击所导致的表面原子溅出。 \| `corpus` |
| definitions | `terms/registry/definitions.tsv:3763` | `chemical-sputtering` \| `en` \| The chemical ejection of surface atoms via reactive hydrogen species. \| `corpus` |
| definitions | `terms/registry/definitions.tsv:3764` | `chemical-sputtering` \| `zh` \| 化学溅射是反应性氢物种导致的表面原子化学抛出。 \| `corpus` |
| evidence | `terms/registry/evidence.tsv:73` | `sputtering` \| `https://en.wikipedia.org/wiki/Sputtering` \| (空) \| (空) \| (空) \| `2026-03-16` |
| evidence | `terms/registry/evidence.tsv:652` | `physical-sputtering` \| `internal:expansion:batch-24` \| Ion bombardment erosion \| `copilot` \| `2026-03-17` |
| evidence | `terms/registry/evidence.tsv:1512` | `chemical-sputtering` \| `internal:registry-gap-review:pwi-expansion` \| Chemical sputtering of surface atoms by reactive hydrogen species \| `copilot` \| `2026-04-13` |

**冲突的三处并存事实（仅陈述，不推断成因）**：

1. `aliases.tsv:397` 把 `物理溅射` 挂到 **`sputtering`**（disposition = `alias`），而该行 `notes` 写的是 `physical sputtering zh`；
2. `concepts.tsv:712` 把 `物理溅射` 同时登记为 **`physical-sputtering`** 的 `preferred_zh`（第 3 列）；
3. `aliases.tsv:4566 / 4567` 只把**产额形式**（`物理溅射产额` / `physical sputtering yield`）挂到 `physical-sputtering`，该 concept 名下**没有**裸 `物理溅射` 的 alias 行。

⇒ 同一字符串 `物理溅射` 在词表内同时承担两种角色：`sputtering` 的 zh alias 与 `physical-sputtering` 的 zh preferred term。冲突全集扫描（T2.1）结果为 `TOTAL= 1`，即全库 zh 串冲突仅此一条。

## §2 下游投影实测（artifacts 只读）

实测命令（`set -euo pipefail`；断言全部通过才输出 `PROJECTION_OK`）：

```bash
python3 - <<'PY'
import json
d=json.load(open('artifacts/translation_dict.json',encoding='utf-8'))
q=json.load(open('artifacts/query_expansions.json',encoding='utf-8'))
print('A zh2en[物理溅射] =', d['zh2en'].get('物理溅射'))
print('B en2zh[physical sputtering] =', d['en2zh'].get('physical sputtering'))
print('C zh2en[化学溅射] =', d['zh2en'].get('化学溅射'))
print('D alias_index[物理溅射] =', q['alias_index'].get('物理溅射'))
print('E sputtering.all_terms 含物理溅射 =', '物理溅射' in q['concepts']['sputtering']['all_terms'])
assert d['zh2en'].get('物理溅射')=='sputtering'
assert d['en2zh'].get('physical sputtering')=='物理溅射'
assert d['zh2en'].get('化学溅射')=='chemical sputtering'
assert q['alias_index'].get('物理溅射')=='sputtering'
assert '物理溅射' in q['concepts']['sputtering']['all_terms']
print('PROJECTION_OK')
PY
```

**输出（2026-11-03 实测，逐字）**：

```text
A zh2en[物理溅射] = sputtering
B en2zh[physical sputtering] = 物理溅射
C zh2en[化学溅射] = chemical sputtering
D alias_index[物理溅射] = sputtering
E sputtering.all_terms 含物理溅射 = True
PROJECTION_OK
```

补充实测（同一 artifacts 快照，`generated_at = 2026-10-26`）：

```text
sputtering.all_terms          = ["sputtering", "溅射", "物理溅射"]
physical-sputtering.all_terms = ["physical sputtering", "physical sputtering yield", "物理溅射产额"]
chemical-sputtering.all_terms = ["chemical sputtering", "chemical-sputtering", "化学溅射"]
alias_index['physical sputtering'] = physical-sputtering
zh2en 中取值等于 sputtering 的条目  = ["溅射", "物理溅射"]
zh2en 中取值等于 physical-sputtering 的条目 = []          ← 空
en2zh['sputtering']            = 溅射
en2zh['physical sputtering']   = 物理溅射
en2zh_short['physical sputtering'] = None
```

**投影方向不对称（实测结论，不作价值判断）**：

| 方向 | 输入 | 输出 | 是否可达 `physical-sputtering` |
|---|---|---|---|
| en → zh | `physical sputtering` | `物理溅射` | 可达（`en2zh` 命中） |
| zh → en | `物理溅射` | `sputtering` | **不可达**（`zh2en` 与 `alias_index` 均指向 `sputtering`） |

即：`zh2en` 中不存在任何以 `physical-sputtering` 为值的条目，`物理溅射` 在 zh→en 方向被投影到其上位的 `sputtering`。该行为与 `sputtering.all_terms` 收录 `物理溅射`（`E = True`）一致，属词表当前状态的**确定性**投影结果，非随机或缓存异常（`PROJECTION_OK` 断言通过，重建快照后可用同一命令复现）。

> 说明：本节仅记录 artifacts 的现有投影行为；`artifacts/` 本身在本次查证中未做任何写操作。

## §3 语义层级核验（H1–H2）

> 前置事实：`concepts.tsv` 的列定义（`terms/registry/concepts.tsv:1-3` 为注释头）为 `concept_id / category / preferred_zh / preferred_en / preferred_abbr / status / notes / source`，**没有 parent/上位指针列**；`aliases.tsv` 的 `kind` 枚举仅为 `preferred|alias|deprecated|forbidden`，**不表达层级**。故下文「上位/下位」是对**定义文本**的语义判断，不是词表内的结构关系断言。

### H1 `sputtering = 溅射` 是通用上位概念

证据: `terms/registry/definitions.tsv:5503`（en，`source=corpus`）："The ejection of atoms from a surface as a result of the impact of energetic particles; a process by which the surface material of a plasma-facing surface is removed by particle bombardment."；`terms/registry/definitions.tsv:5504`（zh，`source=corpus`）："高能粒子撞击使表面原子被射出的过程，也是面向等离子体表面材料因粒子轰击而被去除的一种机制。"；`terms/registry/concepts.tsv:82` 记 `preferred_zh=溅射`、`preferred_en=sputtering`、`notes=Ejection of surface atoms by energetic particle impact`；`terms/registry/aliases.tsv:395` 记 `溅射 → sputtering / zh / preferred`。

推理: en 定义的作用对象是 "energetic **particles**"（未限定粒子种类、未限定能量传递机制），且以 "a process by which the surface material of a plasma-facing surface is removed by particle bombardment" 给出**过程类**刻画，属对「表面原子被高能粒子击出」这一总过程的命名；zh 定义同样只写「高能粒子撞击」与「粒子轰击」，与 en 逐项对应，无增义（未追加离子/化学限定）、无漏义（保留了 plasma-facing surface 语境）。因此它是一个不限定具体机制的上位过程名；其能否实际涵盖物理/化学两类机制，需与 H2 的下位定义对照——`definitions.tsv:5021` 的 "energetic ion bombardment" 与 `definitions.tsv:3763` 的 "reactive hydrogen species" 都是 "energetic particles" 的具体取值，故上位判定与下位定义**不矛盾**。

判定: PASS

### H2 `physical-sputtering = 物理溅射` 与 `chemical-sputtering = 化学溅射` 是并列下位概念

证据: `terms/registry/definitions.tsv:5021`（physical-sputtering en）："Ejection of surface atoms by energetic ion bombardment."；`terms/registry/definitions.tsv:5022`（zh）："物理溅射是高能离子轰击所导致的表面原子溅出。"；`terms/registry/definitions.tsv:3763`（chemical-sputtering en）："The chemical ejection of surface atoms via reactive hydrogen species."；`terms/registry/definitions.tsv:3764`（zh）："化学溅射是反应性氢物种导致的表面原子化学抛出。"；对应概念行 `terms/registry/concepts.tsv:712`（`物理溅射` / `physical sputtering`）与 `terms/registry/concepts.tsv:1659`（`化学溅射` / `chemical sputtering`）。

推理: 两条定义共享同一结果项（"ejection of surface atoms" / "表面原子被…出"）与同一上位场域（面向等离子体表面的粒子诱导侵蚀），差别被**机制**唯一区分：一条限 "energetic ion bombardment"（物理动量传递），另一条限 "reactive hydrogen species"（反应性氢参与的化学过程）。二者互不包含：化学溅射定义不要求离子轰击，物理溅射定义不涉及反应性氢物种。zh 侧「物理溅射 / 化学溅射」与 en 的机制限定一一对应（"离子轰击"↔"ion bombardment"，"反应性氢物种"↔"reactive hydrogen species"），无增义或误译。故在 H1 上位成立的前提下，二者是并列下位；即使不承认 H1，二者仍因机制互斥而并列。**限制**：本判定只覆盖这三条定义文本是否存在包含/互斥矛盾，不覆盖词表是否还有其他机制（如弧光溅射、辐射增强溅射）未登记的情况。

判定: PASS

## §4 来源可得性与下游投影影响（H3–H4）

### H3 `物理溅射` 同时作为 `sputtering` 的 zh alias 是否成立

证据: `terms/registry/aliases.tsv:397`：`物理溅射 → sputtering / zh / alias / comment=physical sputtering zh`（即该行自身注释声称它是 `physical sputtering` 的中文形式，却挂在 `sputtering` 名下）；`terms/registry/aliases.tsv:395` 已把 `溅射` 定为 `sputtering` 的 `zh / preferred`；`terms/registry/concepts.tsv:712` 又把 `物理溅射` 定为 `physical-sputtering` 的 `preferred_zh`。上游依据：`artifacts/terminology_sources/` 六个文件对 `物理溅射` 与 `physical sputtering` 的命中数**全部为 0**（实测见 `/tmp/opencode/t5184-t23-sources.txt`：`gbt4960_9_diff/terms`、`iaea_safety_glossary_diff/raw`、`iter_glossary_diff/raw` 均 `zh=0 en=0`）；`terms/registry/evidence.tsv:73` 对 `sputtering` 只给 `https://en.wikipedia.org/wiki/Sputtering`（`2026-03-16`，英文条目，未提供中文术语来源），`evidence.tsv:652` 与 `evidence.tsv:1512` 均为 `internal:` / `copilot` 内部注记，非外部权威。

推理: 词表内部对该字符串存在两种互不相容的归属（`sputtering` 的 zh alias vs `physical-sputtering` 的 zh preferred），这一点由 §1 的原行直接证实，无需外部来源。但 H3 要判定的是「把 `物理溅射` 当作 `sputtering` 的通用中文同义词使用」这一**外部用语事实**是否成立：若中文文献普遍用「物理溅射」泛指溅射过程，则该 alias 成立；若中文文献只用它指称物理机制的溅射，则该 alias 使上位概念侵占了并列下位概念的专名。仓内 6 个上游术语表快照均无该串，无法据此判断。**依据: 不可得** —— 上游快照缺该词条属覆盖范围问题（GB/T-4960.9 / IAEA safety glossary / ITER glossary 均非溅射专题词表），**上游无该串不等于上游否定该用法**，故既不能判 PASS（承认该 alias）也不能判 FAIL（否定该 alias）。

判定: UNDECIDABLE

### H4 下游 `zh2en` / `alias_index` 投影是否造成信息丢失

证据: §2 实测 A `zh2en[物理溅射] = sputtering`、D `alias_index[物理溅射] = sputtering`、E `sputtering.all_terms 含物理溅射 = True`、B `en2zh[physical sputtering] = 物理溅射`；补充实测：`zh2en` 中取值等于 `physical-sputtering` 的条目数 = **0**（空），`physical-sputtering.all_terms = ["physical sputtering","physical sputtering yield","物理溅射产额"]`（不含裸 `物理溅射`），而 `sputtering.all_terms = ["sputtering","溅射","物理溅射"]`。

推理: 投影在两个方向上不对称。en→zh 方向，`physical sputtering` 可正常到达 `物理溅射`；zh→en 方向，`物理溅射` 只能到达 `sputtering`，全表中没有任何以 `physical-sputtering` 为值的 zh→en 条目，故 `physical-sputtering` 在 zh→en 方向**不可达**。这是一次多对一（有损）粗化：`physical-sputtering` 的中文首选名在下游不再指向自身。该行为可复现（`PROJECTION_OK` 断言 + 同一 artifacts 快照重跑一致），属事实层结论。**边界**：本节不判定该粗化是否「应修」——其规范性取决于 H3 的裁决（若 `物理溅射` 确为通用同义词，粗化是符合词表的合理合并；若仅为下位专名，则应视为下游丢失）。

判定: PASS

> §4 汇总：H1 `PASS` / H2 `PASS` / H3 `UNDECIDABLE` / H4 `PASS`。**H3 的 UNDECIDABLE 不计入 PASS**，M3 因此不得勾选（待用户裁决）。全报告**不宣称成因**：§1 只登记三类并存事实，未判定该 alias 行由何流程、何时、因何写入。

## §5 三选项建议（只出建议，不动数据）

> **共同前提**：本阶段**没有**数据写权限（父代理委派口径：S2 默认只输出证据与裁决建议）。下列三项均为**提案**，任一项的实际执行都需用户先行裁决；本报告不声称任何一项已获实施许可。
> **共同约束**：三项都只触及 `terms/registry/` 的 zh 命名，不改 `definitions`/`evidence`/`concepts.notes`；改后需重建 `artifacts/translation_dict.json` 与 `artifacts/query_expansions.json`，故「机械影响」均含一次 artifacts 重建。

### 选项 A 删除 `物理溅射 → sputtering` 这条 zh alias（`aliases.tsv:397`）

- **做法**：删除 `terms/registry/aliases.tsv:397`（`物理溅射 / sputtering / zh / alias / comment=physical sputtering zh`）。按 §2 实测，`zh2en` 与 `alias_index` 的 zh 侧映射由 alias 行生成、`concepts.preferred_zh` 未被消费（证据：`zh2en` 中以 `physical-sputtering` 为值的条目数 = 0，而 `concepts.tsv:712` 早已登记 `preferred_zh=物理溅射`）⇒ **单删会把「错指向」变成「无指向」**，因此完整形态为 **A′ = 删除 397 行 + 新增一条 `物理溅射 / physical-sputtering / zh / preferred`**。
- **优点**：消除 §1 的三处并存事实；与 H1/H2 的层级判定（上位=`溅射`，下位=`物理溅射`/`化学溅射`）一致；修复后 `物理溅射` 在 zh→en 方向可达 `physical-sputtering`，补回 H4 实测的丢失。
- **缺点**：A′ 是两处数据改动（删 1 行 + 加 1 行），且新行的 `kind=preferred` 会与 `concepts.tsv:712` 的 `preferred_zh` 形成第二处「首选名」声明，需保证两处一致；若 H3 最终裁决为「`物理溅射` 确是溅射的通用中文同义词」，则 A′ 反而删掉了一个成立的上位别名。
- **机械影响**：`aliases.tsv` ±1 行（A′ 净 0 行）；受影响产物 `artifacts/translation_dict.json`（`zh2en['物理溅射']`：`sputtering` → `physical-sputtering`）、`artifacts/query_expansions.json`（`alias_index` 与两个 concept 的 `all_terms`）、`artifacts/vale/accept.txt`/`reject.txt` 及 `terminology_substitutions.tsv`（由 aliases 派生）。**预期回归**：`pipeline.validate_registry`、`scripts/registry_row_audit.py --audit`、`scripts/registry_batch_verify.py --self-test` 需重跑。
- **风险**：中。若只删不补（漏做 A′ 的后半步），`物理溅射` 会从「指向错误概念」退化为「无 zh→en 映射」，对下游查询是净损失；`vale` 词表重建若有缓存未刷新，会出现 accept/reject 与 dict 不一致。**未验证项**：artifacts 生成器对 `kind=preferred`/`alias` 的处理差异本次未读源码确认，属 `[⚠️ 待验证]`。
- 可逆性: **高**。纯行级增删，反向操作即恢复；且可先备份 `aliases.tsv` 的 397 行原文（本报告 §1 已逐字留存原始行），`git revert` 单 commit 即可完全回退。
- **成本**：低（约 15 min：改 2 行 + 重建 artifacts + 跑 3 个门禁）。

### 选项 B 改 `physical-sputtering` 的 `preferred_zh`（`concepts.tsv:712` 第 3 列）

- **做法**：把 `concepts.tsv:712` 的 `preferred_zh` 由 `物理溅射` 改为另一中文名（例如「离子溅射」或「物理溅射（离子轰击）」），从而让 `物理溅射` 只保留 `sputtering` alias 的身份。
- **优点**：不改 `aliases.tsv`，冲突在「首选名」层一次性消解；`zh2en` 的 zh→en 粗化（H4）保持原样但仍自洽。
- **缺点**：`preferred_zh` 是 concept 的**规范中文名**，被 IME 导出、`concepts.tsv` 文档与外部引用共用；改名会波及所有引用该概念中文名的位置，且新名的选取需要领域命名权威——本阶段**无**该权威依据（H3 已 UNDECIDABLE，改名的语义前提同样不可得）。此外 `aliases.tsv:7050` 的 forbidden 行注释已把「物理溅射(产额)」当作正确形式，说明词表内部对「物理溅射」的用法另有约定，B 会与该行注释产生新的不一致。
- **机械影响**：`concepts.tsv` 1 行 1 列；派生影响面比 A 大（`registry_exports.json`、IME 导出、`query_expansions` 的 concept 名、可能的 `dist/` 产物）；`scripts/registry_row_audit.py` 的列断言与 `pipeline.validate_registry` 的名称一致性检查需重跑。
- **风险**：**高**。属规范名变更，影响面超出本冲突；新名无来源支撑（`artifacts/terminology_sources/` 6 文件对相关串 0 命中），等于用未证实的命名替换已登记命名。
- 可逆性: 中。单行可 revert，但若已重建 artifacts 并外发（如 `dist/` 打包或 IME 词表），需同步回收下游副本。
- **成本**：中（约 30 min：选名需领域判断 + 重建 + 3 门禁 + 下游核对）。

### 选项 C 维持现状，登记为已知歧义

- **做法**：`aliases.tsv` / `concepts.tsv` 均不改；在 `w3-name-conflicts.tsv` 已有登记（`:3`，`pre-existing`）之外，把 §1 的三处并存事实与 §2 的投影不对称结论写入本报告，并把 H3 标为待裁决项。
- **优点**：与 H3 = `UNDECIDABLE` 的证据状态严格一致——**不在依据不可得时做不可逆的命名决策**；零数据风险、零下游回归；保留全部原始证据供后续裁决。
- **缺点**：H4 实测的 zh→en 不可达（`物理溅射` 只能到 `sputtering`，`physical-sputtering` 在该方向不可达）继续存在；查询「物理溅射」的用法若本意是下位概念，会持续得到上位概念的结果。
- **机械影响**：无。`terms/`、`artifacts/` 零 diff。
- **风险**：低（技术风险）；但**遗留风险**是歧义长期驻留，后续若有人按 `物理溅射` 批量生成双语对照，会把 `physical-sputtering` 的用例系统性译成 `sputtering`。
- 可逆性: **完全可逆**（无改动可回退）。
- **成本**：零（本报告即产物）。

## §6 推荐与裁决请求

**推荐（条件式，非执行指令）**：

1. **若用户裁决 H3 = 不成立**（即 `物理溅射` 在中文技术语境中专指物理机制的溅射，不作 `sputtering` 的通用同义词）⇒ **推荐选项 A 的完整形态 A′**。依据：H1/H2 已判 `PASS`，层级为「`溅射`（上位）⊃ `物理溅射` / `化学溅射`（并列下位）」；`aliases.tsv:397` 的 `comment` 字段自身写着 `physical sputtering zh`，与其挂载目标 `sputtering` 不一致（§1 事实 1）；A′ 同时修复 H4 实测的 zh→en 不可达，而 B 需要无来源支撑的新命名、C 保留 H4 的丢失。
2. **若用户裁决 H3 = 成立**（`物理溅射` 确为通用同义词）⇒ **推荐选项 C**（维持），并需另行决定 `concepts.tsv:712` 的 `preferred_zh` 是否随之调整——该问题超出本冲突范围，本报告不代为决定。
3. **若用户暂不裁决 H3**（当前证据状态）⇒ **推荐选项 C 作为默认**，保持 `w3-name-conflicts.tsv:3` 的 `pre-existing` 登记不变，M3 保持未勾。**不得**以「上游没有该串」为由推进 A/B——§4 已说明上游无该串仅反映术语表覆盖范围，不构成否定证据。

**裁决请求（待用户裁决 (D2)）**：

| 编号 | 待决事项 | 需要的用户输入 | 本报告能提供 / 不能提供 |
|---|---|---|---|
| D2-1 | H3 是否成立：`物理溅射` 可否作为 `sputtering` 的通用中文同义词 | 领域裁决，或提供可引用的中文权威（教材/标准/文献）条目 | **能**：§1 原行、§2 投影实测、§4 上游 0 命中清单。**不能**：仓内无该串的上游权威，无法自证 |
| D2-2 | 若 H3 不成立，选 A′ 还是 B | 是否接受「删除 397 行 + 新增 preferred alias」的两步改动（A′），或接受规范名变更（B） | **能**：三项的做法/优缺点/机械影响/风险/可逆性/成本对比。**不能**：新中文名的领域命名依据 |
| D2-3 | 若选 A′，是否同批重建 `artifacts/` 并重跑 3 个门禁 | 是否授权一次数据写窗口 | **能**：受影响产物清单（§5 A 的机械影响）。**不能**：本阶段无写权限，需另行派单 |

> **状态声明**：S2 的查证工作到此完成（冲突全集扫描 + 原行证据 + 下游投影实测 + 语义层级与来源可得性 + 三选项建议），但 **M3 的语义是「人工裁决」，裁决未发生**，故父计划 M3 行**保持未勾**，仅追加 `S2 查证完成` 的状态注记。
> **不宣称事项**：本报告不判定该 alias 行的写入原因/流程/时间（不宣称根因）；不判定上游术语表对「物理溅射」的态度（无该串）；不评估 `chemical-sputtering` 之外的并列机制是否有缺登记。
