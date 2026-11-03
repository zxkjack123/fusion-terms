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
