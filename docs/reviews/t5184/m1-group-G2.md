# T4.3 组 G2 语义复核（PM #5184 / M1 抽样复核）

**报告头（date 核验）**：`date` → `Tue Nov  3 11:54:10 AM CST 2026`，即 **2026-11-03**。
本报告为只读复核产物：本会话仅新增本文件 `docs/reviews/t5184/m1-group-G2.md`，未修改 `terms/registry/*` 与任何其它文件，未执行任何写 git 的命令（无 add/commit/checkout/stash，无 push）。

## 输入与样本一致性

- 输入清单：`docs/reviews/t5184/m1-sample-manifest.tsv` 中 `group=G2`（batch_scope `w1_b_b02..w1_b_b06`）的 8 行，字段顺序 `group,batch_scope,concept_id,sha256_16`，逐行原样使用：

| group | batch_scope | concept_id | sha256_16 |
|---|---|---|---|
| G2 | w1_b_b02..w1_b_b06 | free-boundary-equilibrium | 02e2574796e0a8a8 |
| G2 | w1_b_b02..w1_b_b06 | proton-boron-fusion | 08afb62b3c7ec468 |
| G2 | w1_b_b02..w1_b_b06 | tbm | 0e39d2c2247be316 |
| G2 | w1_b_b02..w1_b_b06 | wccb | 0f32a60f2dfcff00 |
| G2 | w1_b_b02..w1_b_b06 | spin-polarized-fuel | 0fc83f77658dc81a |
| G2 | w1_b_b02..w1_b_b06 | zonal-flow | 129a82d6b30d54a3 |
| G2 | w1_b_b02..w1_b_b06 | flux-confinement | 14472fe29f3d03fb |
| G2 | w1_b_b02..w1_b_b06 | neutron-multiplier | 1915ea9503cc2f38 |

- `sha256_16` 溯源核验（附加）：8 行的 `sha256_16` 等于 `sha256(concept_id)` 前 16 位十六进制（对 8 个 cid 全部命中，例如 `sha256("flux-confinement")[:16] = 14472fe29f3d03fb`），据此确认清单行与 `concept_id` 一一绑定，本报告按同一 8 行使用。

## 数据通路与路由核验

- 8 条 G2 样本在 `concepts.tsv` 的 `source` 字段**全部为 `corpus`**（见各样本证据锚点行的行末列），故按任务路由表**逐条走 `corpus` 分支**：以 `terms/registry/concepts.tsv` 该行 notes 为原始语料（逐字原文 + 行号）。
- `GB/T-4960.9` 分支：8 条 source 均非 `GB/T-4960.9`，**未触发**；同时做交叉检索，`matched_concept_id` 无一命中这 8 个 cid。
- `IAEA/ITER` 分支：8 条 source 均非 IAEA/ITER，**未触发**；交叉检索 `artifacts/terminology_sources/iter_glossary_raw.tsv` 与 `artifacts/terminology_sources/iaea_safety_glossary_raw.tsv`，按 cid 与英文术语名（test blanket module / neutron multiplier / zonal flow / water-cooled ceramic / spin-polarized / proton-boron / free-boundary / flux confinement）检索均无命中。
- **路径偏差（如实记录）**：任务给定的 `.github/plans/t4973-batches/gbt4960_9_diff.tsv` **本仓不存在该文件**；实际 GB/T 差异表位于 `artifacts/terminology_sources/gbt4960_9_diff.tsv`（列头 `# term	status	matched_concept_id	term_id	zh	abbr	definition`），本报告的 GB/T 交叉检索以该实际文件为准。该偏差不改变样本判定（source 均为 corpus）。
- `http(s) URL` 分支：8 条 source 均非 URL，**未触发**。补充说明：`terms/registry/evidence.tsv:186` 记录了 proton-boron-fusion 的一条 Wikipedia URL 溯源指针，但该指针不是本任务的 `source` 路由键；本次**未做外部网络取回，也不据该 URL 主张任何内容**（不以未取回内容充当原文）。
- 术语/定义文件全程只读：`concepts.tsv`、`definitions.tsv`、`evidence.tsv`、GB/T 与 IAEA/ITER 语料文件均仅读取。
- 计数口径说明：本报告正文不使用"源缺失标记"字样，仅在下方 AC 实跑中以括号转义形式给出该模式的命中数，以免机械子串计数把本报告的叙述文字误计为样本条目。

## 样本复核

### D1 free-boundary-equilibrium

（manifest 行：`G2	w1_b_b02..w1_b_b06	free-boundary-equilibrium	02e2574796e0a8a8`）

原始语料: source 字段=`corpus` → 依据 `terms/registry/concepts.tsv:355` 该行 notes 逐字原文：`Equilibrium with self-consistent plasma-coil interaction`（该行全文：`free-boundary-equilibrium	concept	自由边界平衡	free-boundary equilibrium		active	Equilibrium with self-consistent plasma-coil interaction	corpus`）。GB/T-4960.9 分支未触发；IAEA/ITER 分支未触发；URL 分支未触发。

定义文本: en（definitions.tsv:4299）逐字：`Equilibrium solution in which the plasma-coil interaction is treated self-consistently.`
定义文本: zh（definitions.tsv:4300）逐字：`自洽处理等离子体与线圈相互作用的平衡解。`

适用性推理: ① en 以 `self-consistent` 与 `plasma-coil interaction` 完整承接语料限定语，未把边界当成给定，也未引入固定边界假设，准确刻画该概念；② zh `自洽处理…平衡解` 与 en 逐项对应（solution↔平衡解、treated self-consistently↔自洽处理），无增义/漏义/误译，仅语序调整；③ 同族 `plasma-equilibrium`（concepts.tsv:50）为上位、`grad-shafranov-equation`（:354）为方程层、`helena`（:403）自述为 fixed-boundary 求解器，故本条 free-boundary 语义位与之互补而非冲突，其 `self-consistent plasma-coil interaction` 限定语正好与 helena 的固定边界形成对照，无范围侵占。

判定: PASS
证据锚点: concepts.tsv:355

### D2 proton-boron-fusion

（manifest 行：`G2	w1_b_b02..w1_b_b06	proton-boron-fusion	08afb62b3c7ec468`）

原始语料: source 字段=`corpus` → 依据 `terms/registry/concepts.tsv:203` 该行 notes 逐字原文：`Aneutronic fusion reaction p + 11B → 3α`。GB/T-4960.9 分支未触发；IAEA/ITER 分支未触发；URL 分支未触发（`evidence.tsv:186` 的 Wikipedia URL 不作取回）。

定义文本: en（definitions.tsv:5148）逐字：`Aneutronic fusion reaction in which a proton reacts with boron-11 to produce three alpha particles.`
定义文本: zh（definitions.tsv:5149）逐字：`无中子聚变反应，质子与 ¹¹B 反应生成三个 α 粒子。`

适用性推理: ① en 把语料记法 `p + 11B → 3α` 完整展开为 proton、boron-11、three alpha particles，与反应式自洽（质量数 11+1=12=3×4，电荷数 5+1=6=3×2），且未省略 `Aneutronic` 这一关键限定语，准确刻画该概念；② zh `无中子聚变反应` 对译 `Aneutronic fusion reaction`，与同族既定中文命名 `无中子聚变`（concepts.tsv:204）一致，`质子与 ¹¹B 反应生成三个 α 粒子` 与 en 逐项对应，无增义/漏义/误译；③ 同族 `aneutronic-fusion`（:204，`no or negligible neutrons`）与 `dt-reaction`（:676，产 14.1 MeV 中子）各自范围清楚，p-B11 作为无中子类实例不与之冲突。

判定: PASS
证据锚点: concepts.tsv:203

### D3 tbm

（manifest 行：`G2	w1_b_b02..w1_b_b06	tbm	0e39d2c2247be316`）

原始语料: source 字段=`corpus` → 依据 `terms/registry/concepts.tsv:282` 该行 notes 逐字原文：`In-vessel test modules for ITER blanket qualification`。GB/T-4960.9 分支未触发（GB/T 差异表中 `ITER test blanket module` 行的 `matched_concept_id` 为空，未命中本 cid）；IAEA/ITER 分支未触发；URL 分支未触发。

定义文本: en（definitions.tsv:5613）逐字：`In-vessel test modules installed in ITER for the qualification of breeding blanket designs.`
定义文本: zh（definitions.tsv:5614）逐字：`安装于 ITER 真空室内、用于验证增殖包层设计的实验模块。`

适用性推理: ① en 保留语料限定语 `In-vessel` 与 `for ITER`，并把 `blanket qualification` 具体化为 `qualification of breeding blanket designs`，与 `breeding-blanket`（concepts.tsv:92）范围一致，属收窄细化而非曲解；② zh `安装于 ITER 真空室内、用于验证增殖包层设计的实验模块` 与 en 逐项对应，`in-vessel` 译 `真空室内` 准确，两条限定语一项不缺，未见增义、漏义或误译；③ 与 `wccb`（:278）、`hccb`（:277）、`hcll`（:279）、`hcpb`（:280）等包层方案条目角色不同（本条是装置内测试模块，彼等是包层方案），无冲突；另记跨源用字差异：GB/T 2.4.66 作 `ITER 试验包层模块`，本条 preferred_zh 作 `实验包层模块`（试验/实验 用字不同），该差异不影响 en↔zh 定义等价性，仅登记为跨源命名差异。

判定: PASS
证据锚点: concepts.tsv:282

### D4 wccb

（manifest 行：`G2	w1_b_b02..w1_b_b06	wccb	0f32a60f2dfcff00`）

原始语料: source 字段=`corpus` → 依据 `terms/registry/concepts.tsv:278` 该行 notes 逐字原文：`Water-cooled ceramic breeder blanket (CN reference)`。GB/T-4960.9 分支未触发；IAEA/ITER 分支未触发（`water-cooled ceramic` 在两份 raw 语料中无命中）；URL 分支未触发。

定义文本: en（definitions.tsv:5813）逐字：`Water-cooled ceramic breeder blanket concept, used as the Chinese reference design.`
定义文本: zh（definitions.tsv:5814）逐字：`水冷陶瓷增殖剂包层方案，作为中国参考设计。`

适用性推理: ① en 逐项承接语料限定语 `Water-cooled` 与 `ceramic breeder`，并把 `(CN reference)` 展开为 `used as the Chinese reference design`，未改变指称对象，准确刻画该概念；② zh `水冷陶瓷增殖剂包层方案，作为中国参考设计` 与 en 等价，`ceramic breeder` 取材料义译作 `陶瓷增殖剂`、blanket concept 译作 `包层方案`，分工正确，无增义/漏义/误译；③ 需记录的范围歧义（非冲突判定）：`hccb`（concepts.tsv:277）语料同样标 `(CN reference)`，其 en 定义（definitions.tsv:4393）与本条同为 `…, used as the Chinese reference design.` 模板，二者均未限定归属计划（ITER TBM 与 CFETR 概念之别），在登记层面留下"何者才是中国参考设计"的范围歧义；但两者指称对象不同（WCCB≠HCCB），该歧义与语料 notes 同源而非定义层新增，不构成对同一对象的相反主张，故不判冲突，仅作为范围限定建议记录。

判定: PASS
证据锚点: concepts.tsv:278

### D5 spin-polarized-fuel

（manifest 行：`G2	w1_b_b02..w1_b_b06	spin-polarized-fuel	0fc83f77658dc81a`）

原始语料: source 字段=`corpus` → 依据 `terms/registry/concepts.tsv:236` 该行 notes 逐字原文：`Nuclear-spin-aligned fuel to enhance p-B11 cross-section (~50% gain)`。GB/T-4960.9 分支未触发；IAEA/ITER 分支未触发（`spin-polarized` 在两份 raw 语料中无命中）；URL 分支未触发。

定义文本: en（definitions.tsv:5501）逐字：`Fuel whose nuclear spins are aligned, enhancing the p-B11 fusion cross-section by about 50%.`
定义文本: zh（definitions.tsv:5502）逐字：`核自旋取向一致的燃料，可使 p-B11 聚变截面提高约 50%。`

适用性推理: ① en 完整承接三条语料限定语 `Nuclear-spin-aligned`、`p-B11 cross-section`、`(~50% gain)`，并把 gain 明确为增强方向（`enhancing … by about 50%`），未扩大适用范围，准确刻画该概念；② zh `核自旋取向一致的燃料` 对应 `nuclear spins are aligned`（状态义），`可使…提高约 50%` 对应 `enhancing … by about 50%`，其中 `可` 仅添加情态色彩而未改变定量主张或量值，属措辞层面差异，不构成增义、漏义或误译；③ 同族中与 p-B11 相关的仅 `aneutronic-fusion`（concepts.tsv:204）与 `proton-boron-fusion`（:203），仓内含 `polarized` 的自旋极化条目仅本条（:236），无同族条目与之争夺范围，无冲突。

判定: PASS
证据锚点: concepts.tsv:236

### D6 zonal-flow

（manifest 行：`G2	w1_b_b02..w1_b_b06	zonal-flow	129a82d6b30d54a3`）

原始语料: source 字段=`corpus` → 依据 `terms/registry/concepts.tsv:365` 该行 notes 逐字原文：`Toroidally and poloidally symmetric flow regulating turbulence`。GB/T-4960.9 分支未触发；IAEA/ITER 分支未触发（`zonal flow` 在两份 raw 语料中无命中）；URL 分支未触发。

定义文本: en（definitions.tsv:5835）逐字：`Flow that is symmetric in the toroidal and poloidal directions and that regulates plasma turbulence.`
定义文本: zh（definitions.tsv:5836）逐字：`在环向和极向均对称、用于调节等离子体湍流的流动。`

适用性推理: ① en 把 `Toroidally and poloidally symmetric` 展开为 `symmetric in the toroidal and poloidal directions`，保留环向与极向双重对称这一关键限定语（对应 m=n=0 结构），并保留 `regulates plasma turbulence`，准确刻画该概念；② zh `在环向和极向均对称` 对应无误，`用于调节等离子体湍流` 对应 `regulates plasma turbulence`，其中 `用于` 带轻微目的性色彩而 en 为描述性的 regulates，属措辞层面增义，未改变概念外延（仍限定为对湍流起调节作用的对称流动）；③ 同族 `geodesic-acoustic-mode`（concepts.tsv:366）自述为 `Oscillatory zonal-flow branch`，其振荡分支（m=1）与本条"极向对称"限定并存而不相互否定，`predator-prey-oscillation`（:867，turbulence 与 zonal flows 的非线性振荡）与 `drift-wave`（:562）亦无冲突。

判定: PASS
证据锚点: concepts.tsv:365

### D7 flux-confinement

（manifest 行：`G2	w1_b_b02..w1_b_b06	flux-confinement	14472fe29f3d03fb`）

原始语料: source 字段=`corpus` → 依据 `terms/registry/concepts.tsv:166` 该行 notes 逐字原文：`Confinement of poloidal flux within FRC separatrix`。GB/T-4960.9 分支未触发；IAEA/ITER 分支未触发（`flux confinement` 在两份 raw 语料中无命中）；URL 分支未触发。

定义文本: en（definitions.tsv:4279）逐字：`The confinement of toroidal plasma by the closed poloidal magnetic flux inside the separatrix of a field-reversed configuration.`
定义文本: zh（definitions.tsv:4280）逐字：`场反位形中，等离子体由分界面内闭合的极向磁通所约束。`

适用性推理: ① en 承接 `poloidal flux` 与 `within FRC separatrix` 两条限定语，把 FRC 展开为 `field-reversed configuration` 并补出 `closed`，与 `flux-surface`（concepts.tsv:350，`constant poloidal flux`）及 `field-reversed-configuration`（:162）自洽，准确刻画该概念；② zh `场反位形中，等离子体由分界面内闭合的极向磁通所约束` 与 en 等价，`分界面` 采用仓内 `separatrix`（:66）既定中文命名，`闭合的极向磁通` 对应 `closed poloidal magnetic flux`；唯 zh 未译出 en 中的 `toroidal`（等离子体前少一限定语），属单一限定语漏译，未改变概念外延（FRC 等离子体本身即环形位形）；③ 与 `magnetic-confinement`（:49，磁约束）命名与语义区分明确，`frc-merging`（:228）讲高磁通 FRC 形成，均不与本条范围冲突。

判定: PASS
证据锚点: concepts.tsv:166

### D8 neutron-multiplier

（manifest 行：`G2	w1_b_b02..w1_b_b06	neutron-multiplier	1915ea9503cc2f38`）

原始语料: source 字段=`corpus` → 依据 `terms/registry/concepts.tsv:260` 该行 notes 逐字原文：`Material (Be, Pb) producing extra neutrons for tritium breeding`。GB/T-4960.9 分支未触发；IAEA/ITER 分支未触发（`neutron multiplier` 仅见于 ITER raw 语料的 `Breeding Technologies` 段落描述，非本 cid 词条命中）；URL 分支未触发。

定义文本: en（definitions.tsv:4859）逐字：`Material such as beryllium or lead that produces extra neutrons for tritium breeding.`
定义文本: zh（definitions.tsv:4860）逐字：`铍、铅等通过核反应为氚增殖提供额外中子的材料。`

适用性推理: ① en 把 `(Be, Pb)` 展开为 `such as beryllium or lead`（保留"举例而非穷举"的限定），并保留 `extra neutrons` 与 `for tritium breeding` 两个限定语，准确刻画该概念；② zh `铍、铅等通过核反应为氚增殖提供额外中子的材料` 与 en 等价，`铍、铅等` 对应开放列举，`通过核反应` 属机制性补充（(n,2n) 等），为正确细化而非范围扩张，未见漏义或误译；③ 同族 `beryllium-neutron-multiplier`（concepts.tsv:1424）、`beryllium-multiplier`（:786）、`beryllium-pebble-bed`（:1423）、`lithium-lead`（:257，含 Pb 倍增剂）、`functional-material`（:793）构成自洽的上下位关系（本条为通用材料概念，彼等为铍基/铅基具体化），无冲突。

判定: PASS
证据锚点: concepts.tsv:260

## 台账（FAIL / UNDECIDABLE）

| D<n> | <cid> | <FAIL|UNDECIDABLE> | 原因 |
|---|---|---|---|

数据行数 = 0 = FAIL(0) + UNDECIDABLE(0)。

## 结论

- G2 组 8 条样本全部 **PASS**：8 条定义的 en 均如实承接 `corpus` 语料限定语，zh 与 en 无实质增义/漏义/误译，未发现同族概念冲突。
- 未判 FAIL 的观察（建议记录，不改变本次三值判定）：D4 与 `hccb`（concepts.tsv:277 / definitions.tsv:4393）共用 `used as the Chinese reference design` 模板而均未限定归属计划，形成登记层面范围歧义；D3 的 `实验/试验` 用字与 GB/T 2.4.66 不一致；D6 的 `用于调节` 与 en 描述性 `regulates` 存在轻微语气差；D7 的 zh 漏译单一限定语 `toroidal`。
- 本次样本的原始语料均可用（8/8 有 `concepts.tsv` 行内 notes 逐字原文），源缺失条数 = 0，与 UNDECIDABLE 条数 = 0 一致；无样本因源缺失而被判三值中的不可判定值。

## AC 自检（实跑）

```text
grep -c '^### ' docs/reviews/t5184/m1-group-G2.md
grep -cP '^判定: (PASS|FAIL|UNDECIDABLE)$' docs/reviews/t5184/m1-group-G2.md
grep -c '^原始语料: ' docs/reviews/t5184/m1-group-G2.md
grep -c '^定义文本: ' docs/reviews/t5184/m1-group-G2.md
grep -c '^适用性推理: ' docs/reviews/t5184/m1-group-G2.md
grep -c '^证据锚点: ' docs/reviews/t5184/m1-group-G2.md
grep -c 'concepts\.tsv:' docs/reviews/t5184/m1-group-G2.md
grep -o 'definitions\.tsv:' docs/reviews/t5184/m1-group-G2.md | wc -l
grep -cP '^原始语料:.*不可[得]' docs/reviews/t5184/m1-group-G2.md
grep -cP '^判定: UNDECIDABLE$' docs/reviews/t5184/m1-group-G2.md
grep -c '^| D[0-9]' docs/reviews/t5184/m1-group-G2.md
git status --porcelain
```

实跑输出（同会话回填）：

```text
$ date
Tue Nov  3 11:54:10 AM CST 2026

$ grep -c '^### ' docs/reviews/t5184/m1-group-G2.md
8

$ grep -cP '^判定: (PASS|FAIL|UNDECIDABLE)$' docs/reviews/t5184/m1-group-G2.md
8

$ grep -c '^原始语料: ' ... ; grep -c '^定义文本: ' ... ; grep -c '^适用性推理: ' ... ; grep -c '^证据锚点: ' ...
8
16
8
8

$ grep -c 'concepts\.tsv:' ... ; grep -o 'definitions\.tsv:' ... | wc -l
25
18

$ grep -cP '^原始语料:.*不可[得]' ... ; grep -cP '^判定: UNDECIDABLE$' ... ; grep -c '^| D[0-9]' ...
0
0
0

$ grep -cP '^判定: PASS$' / '^判定: FAIL$' / '^判定: UNDECIDABLE$'
8 / 0 / 0

$ git status --porcelain
?? .github/plans/5184-four-stage-closeout.md
?? docs/reviews/t5184/m1-group-G1.md
?? docs/reviews/t5184/m1-group-G2.md
```

AC 结论：8 个样本标题、8 条三值单行、四字段（原始语料/定义文本/适用性推理/证据锚点）各 ≥8、`concepts.tsv` 引用 ≥8、`definitions.tsv` 引用 ≥16、源缺失条数(0)==UNDECIDABLE 条数(0)、台账数据行数(0)==FAIL+UNDECIDABLE(0)，全部满足。

`git status` 声明：本会话仅新建 `docs/reviews/t5184/m1-group-G2.md`（本报告）。`git status --porcelain` 另见两条非本会话产物：`.github/plans/5184-four-stage-closeout.md`（mtime 2026-11-03 09:00:44，早于本会话 11:54 开始，本会话首次 `ls` 即已见）与 `docs/reviews/t5184/m1-group-G1.md`（mtime 2026-11-03 12:02:43，与本报告写入时刻 12:02:41 相邻，系并行兄弟会话的 G1 产物）。二者均非本会话创建、本会话未读取写入、未修改。本会话未执行任何写 git 命令（无 add/commit/checkout/stash），未改动其它文件，未 push。
