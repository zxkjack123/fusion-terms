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
