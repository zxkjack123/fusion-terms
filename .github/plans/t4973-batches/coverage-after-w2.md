# W2 覆盖率复算（T2.38）

> 生成时点：`date -Iseconds` 实测 **2026-10-28T22:14:32+08:00**（本地时区 Asia/Shanghai）。
> 基线：W2 起始 HEAD `6342c6a`；W2 收口 HEAD 见本节末「提交清单」。
> 唯一批清单权威：本目录 `README.md`（`w2.ids` = 738 → 37 批：20×36 + 18）。

## 1. 逐批交付（37/37）

| batch | zh+（含节注释） | en+（含节注释） | commit |
|---|---|---|---|
| 01 | 19 | 20 | `94817d8` |
| 02 | 21 | 21 | `a7d74ee` |
| 03 | 21 | 21 | `7f9d473` |
| 04 | 21 | 11 | `c005a90` |
| 05 | 21 | 13 | `c93e678` |
| 06 | 20 | 21 | `d8f8b03` |
| 07 | 21 | 21 | `95e6e10` |
| 08 | 21 | 21 | `3f4b0a4` |
| 09 | 21 | 21 | `4d770dc` |
| 10 | 21 | 21 | `d769d86` |
| 11 | 21 | 21 | `ee48b5b` |
| 12 | 21 | 21 | `faf8126` |
| 13 | 21 | 21 | `bd91097` |
| 14 | 21 | 21 | `a9f6812` |
| 15 | 21 | 21 | `c3cd6c5` |
| 16 | 21 | 21 | `02fabe4` |
| 17 | 20 | 20 | `5d3344b` |
| 18 | 21 | 21 | `9656bc9` |
| 19 | 21 | 21 | `4217090` |
| 20 | 20 | 21 | `1f9c26d` |
| 21 | 20 | 20 | `675124a` |
| 22 | 20 | 21 | `8bc09b6` |
| 23 | 19 | 21 | `6c9f44d` |
| 24 | 21 | 21 | `6898a7d` |
| 25 | 21 | 21 | `5578b53` |
| 26 | 21 | 21 | `56f275b` |
| 27 | 21 | 21 | `0f033ab` |
| 28 | 21 | 21 | `d714980` |
| 29 | 21 | 21 | `1c94e97` |
| 30 | 21 | 21 | `097c468` |
| 31 | 21 | 21 | `3138e07` |
| 32 | 21 | 21 | `d1ce589` |
| 33 | 21 | 21 | `131e65c` |
| 34 | 21 | 21 | `0745cda` |
| 35 | 21 | 21 | `a7fa8cd` |
| 36 | 21 | 21 | `2442fb9` |
| 37 | 19 | 19 | `65c9e74` |
| **合计** | **766** | **754** | — |

`git show --numstat` 的 `+` 行：每批每文件含 1 行节注释 `# --- T-4973 W2 batch NN ---`，
故**实际写入词条** = 766 − 37 = **729 zh**，754 − 37 = **717 en**。

前置提交：

| 内容 | commit |
|---|---|
| T2.0 denylist 冲突复算（新文件 `w2-denylist-conflicts.tsv`，未改任何 ids 文件） | `fca2ded` |
| 基线修复：删除 `allowlist_zh.txt` 重复首行空行（使 dup 门禁可读 0；**未删/改任何词条**） | `9c4c8b1` |

## 2. 计数对账（逐条解释偏差）

```
738 W2 ids
  −  2  zh 已在 allowlist_zh（晕电流 ← halo-current、线辐射 ← line-radiation）
  −  7  zh 含空格被跳过（见 §4.1，用户裁决「跳过并记录」）
= 729  zh 实写

668 multiword（写 concept_id 连字符 token，且无一条已在 en 表）
  + 49 single-word 领域专指（D2-2=A：36 领域专指 + 8 code + 5 台/装置名）
= 717  en 实写
```

构建产物对账：

```
artifacts/domain_terms.txt  3462 → 4893（+1431）
raw 写入 729 + 717 = 1446
  −  8  中文落入 denylist 被过滤（见 §4.2）
  −  7  zh 与 en 同一拉丁串（C-2U/DESC/EU-DEMO/K-DEMO/SIMSOPT/START/VMEC），集合并集去重
= 1431
```

`pipeline.build_terms` 互证：`wrote artifacts/domain_terms.txt (4893 terms)`，`zh 2927 / en 1966`。

## 3. 覆盖率（T2.38 验收命令实测）

```
.venv/bin/python scripts/registry_coverage_report.py --json /tmp/cov-final.json
  → exit 0
total 3076 | covered 1449 → 2181 | uncovered 1627 → 895
coverage_pct 47.11 → 70.90            （门槛 ≥ 70.0 ✅）
allowlist_only_coverage_pct 70.06
W2 738 → 6 | W3a 854 | proper_excluded 35
```

**Phase 2 完成定义**（计划 line 753）实测：

```
.venv/bin/python scripts/registry_coverage_report.py --json /tmp/cov.json && \
python3 -c "import json;d=json.load(open('/tmp/cov.json'));assert d['coverage_pct'] >= 70.0"
  → exit 0
```

### 3.1 W2 残余 6 个（全部为计划预期内不可机械补齐项）

| concept_id | preferred_zh | 原因 |
|---|---|---|
| `system` | 系统 | zh 在 denylist（写入无效）＋ single-word 通用词（D2-2=A 不写 EN） |
| `calculation` | 计算 | 同上 |
| `material` | 材料 | 同上 |
| `simulation` | 模拟 | 同上 |
| `mode` | 模式 | 同上 |
| `device` | 装置 | 同上 |

其余 4 个 denylist zh 冲突 id（`halo-current` 晕电流、`line-radiation` 线辐射、`magnetic-moment` 磁矩、
`mode-number` 模数）已由 **EN 侧**连字符 token 覆盖（`halo-current`/`line-radiation`/`magnetic-moment`/`mode-number`），
故 `W2_zh_in_denylist` 由 10 降为 6。**这不是漏写**（README「执行批次时必须注意」第 1 条）。

## 4. 偏差与例外（逐条登记）

### 4.1 7 个 `preferred_zh` 含空格 → 跳过并记录（用户裁决）

| concept_id | preferred_zh | batch | EN 侧 |
|---|---|---|---|
| `alpha-channel-effect` | `α 通道效应` | b06 | ✅ `alpha-channel-effect` |
| `l-h-threshold-power` | `L-H 转换阈值功率` | b17 | ✅ `l-h-threshold-power` |
| `lost-alpha-detectors` | `逃逸 α 粒子探测器` | b20 | ✅ `lost-alpha-detectors` |
| `alpha-power` | `α 功率` | b21 | ✅ `alpha-power` |
| `iter-test-blanket-module` | `ITER 试验包层模块` | b22 | ✅ `iter-test-blanket-module` |
| `helion-trenta` | `Helion Trenta` | b23 | ✅ `helion-trenta` |
| `gamma-10` | `GAMMA 10` | b23 | ✅ `gamma-10` |

- **冲突实测**：原样写入 `allowlist_zh.txt` 时 `pipeline.build_terms` **exit 1**
  （`wordlist terms must not contain whitespace … - 'α 通道效应'`，变异法证据见 §5）；
  而不写入则 `registry_batch_verify --mode allowlist` 报 `allow_zh_not_listed`。
  ⇒ 计划的两条门禁对这 7 项**不可同时满足**（计划缺口，非执行缺陷）。
- **裁决**：用户在当前会话经 `question` 选择 **「跳过并记录（推荐）」** ⇒ 不改 registry、不改 pipeline、
  不放宽门禁；7 项标记为 known-issue，留待后续（命名/规范化）修复后补写。
- **这批 id 的受影响批次验收方式**：以「排除这 7 个 id 的子集 ids 文件」执行 `--mode allowlist`
  （`--expect` 同步减 1/2），**exit 0**；被排除 id 在本次记录中逐条列明，**未伪造 PASS**。
- 这 7 个 concept 仍经 EN 侧入 IME 词表并计入覆盖率（`covered`），故不影响 §3 的覆盖率结果。

### 4.2 10 个 zh 在 denylist（README 第 1 条，写入即无效）

本次实际新增写入 8 个（`系统`/`计算`/`材料`/`模拟`/`模式`/`装置`/`磁矩`/`模数`）；
`晕电流`/`线辐射` 本已在 allowlist_zh，未重复写入。8 条被 `build_terms` 过滤 ⇒ 构建无副作用。

### 4.3 D2-2=A：21 个通用英文单词形 concept 不写 EN 侧

`design`/`system`/`material`/`performance`/`simulation`/`calculation`/`maintenance`/`evaluation`/
`method`/`mode`/`device`/`mitigation`/`decay`/`cooling`/`damage`/`protection`/`sealing`/`steel`/
`wall`/`lining`/`fuels` —— 仅写 zh 侧（其中 8 个 zh 又被 denylist 过滤）。
这就是 b04/b05/b17/b21 的 en+ 明显低于 20 的原因（11/13/19/19）。

### 4.4 D2-1=A：8 个 code id 以代号形式入 EN 表

`VMEC`/`DESC`/`SIMSOPT`/`CATE`/`PACTOLE`/`PACTITER`/`TRACT`/`OSCAR`（大写代号，与既有 `MCNP`/`ITER` 先例一致）。

### 4.5 D2-6 拉丁名 id（9 个）→ W2 已按现值写入，W3b 后须清理重跑

| concept_id | 写入内容 | batch | 状态 |
|---|---|---|---|
| `vmec` / `desc` / `simsopt` | `VMEC` / `DESC` / `SIMSOPT` | b37 | zh+en 同一串（去重 1 条） |
| `c-2u` | `C-2U` | b23 | 同上 |
| `eu-demo` | `EU-DEMO` | b28 | 同上 |
| `k-demo` | `K-DEMO` | b28 | 同上 |
| `start-device` | `START` | b25 | 同上 |
| `helion-trenta` | `Helion Trenta`（zh 含空格） | b23 | **zh 跳过**，仅 EN |
| `gamma-10` | `GAMMA 10`（zh 含空格） | b23 | **zh 跳过**，仅 EN |

计划 line 737 已预置处置：「若已先写，则须在 W3b 后重跑 T2.38 复算并清理」。
⇒ **W3b 完成后必须复跑 T2.38**（本文件届时需重生成）。当前覆盖率已含这 9 个 id，不影响本阶段门槛。

## 5. 门禁证据（可复跑）

| 检查 | 命令 | 实测 |
|---|---|---|
| 批验收（每批） | `.venv/bin/python scripts/registry_batch_verify.py --mode allowlist --ids-file <ids> --expect <N>` | 37/37 **exit 0**（6 批按 §4.1 使用排除子集，`--expect` 相应减 1/2） |
| 无空白 EN 项 | `grep -v '^#' terms/allowlist_en.txt \| grep -c ' '` | **0** |
| 无重复 zh | `sort terms/allowlist_zh.txt \| uniq -d \| wc -l` | **0**（起始基线为 1，来源是重复空行，已在 `9c4c8b1` 修复） |
| IME 构建不炸 | `.venv/bin/python -m pipeline.build_terms --config config.toml` | 每批 **exit 0**；收口 `wrote artifacts/domain_terms.txt (4893 terms)` |
| 能失败证明（变异法） | 临时追加 `corrosion product` 到 `allowlist_en.txt` 后构建 | **exit 1**（`must not contain whitespace … 'corrosion product'`）；还原后 **exit 0** |
| 发布契约不破 | `.venv/bin/python -m pytest -q` | **exit 0**（175 passed） |
| 注册表自检 | `.venv/bin/python -m pipeline.validate_registry` | `registry OK: 3076 concepts, 10249 aliases, 3203 evidence rows, 6152 definitions` |

## 6. 结论

- W2 机械补齐：**731/738 ids 双语、7/738 仅 EN（zh 因空格冲突跳过，用户已裁决并登记）**。
- `coverage_pct = 70.90 ≥ 70.0` ✅；`artifacts/domain_terms.txt 4893` 行，与 `3462 + 1431` 逐项对账一致。
- 遗留（非本阶段 blocker，均为计划预置）：
  1. 7 个含空格 `preferred_zh`（§4.1）需后续命名/规范化后补写；
  2. 6 个 W2 残余 id（§3.1）受 denylist + D2-2=A 约束，机械手段无法覆盖；
  3. D2-6 的 9 个拉丁名 id 需在 **W3b 后重跑 T2.38** 清理（§4.5）。

## 7. 独立验收（acceptance-verifier，环节 7）

- 委派会话：`ses_e7d21cb8fffe3NTnfCjnTOUQpZ`；验收对象 = HEAD `25e6bae`；**只读复跑，未改仓**。
- 判定：**`PASS`** / confidence HIGH / **blocking 0** / warnings 3 / known-issue 1。
- 独立复跑要点（全部与执行者声明逐项一致）：
  - `registry_coverage_report.py` exit 0：`coverage_pct 70.9`、`covered 2181`、`uncovered 895`、`W2 6`、`terms_file_entries 4893`；Phase 2 完成定义断言 exit 0。
  - 37 批 `--mode allowlist`：31 批全量 exit 0；6 批全量 exit 1 且 **violations 恰为 predicted 的 7 个 `allow_zh_not_listed`，无其它违规**；排除子集后 6 批均 exit 0。
  - `build_terms` exit 0 / `4893` 行；变异法 exit 1 → `cp` 还原（sha256 `13720677…8f5d` 前后一致，`git diff -- terms/` 为空）→ exit 0。
  - EN 空白 0；zh 重复 0；`pytest -q` 175 passed；`validate_registry` 3076 / 6152。
  - 提交范围：`6342c6a..HEAD` 40 commits 仅 6 个文件；`terms/registry/`、`scripts/`、`pipeline/`、`tests/`、`*.ids` 改动数 **0**；`git diff 6342c6a HEAD -- terms/registry/` 为空（registry 逐字节未变）。
  - 计数：729 zh / 717 en 块内词条；`git numstat` 766/754 −37 节注释 = 729/717；`3462+1431=4893` 三源互证。
- **warnings（不阻塞，已登记）**：
  1. 7 个含空格 zh 的处置**授权来源**：验收代理无法从委派提示看到用户原话 → 本条由父代理补证：**用户 2026-10-28 在本会话经 `question` 工具对选项「跳过并记录（推荐）」作出选择**（选项集：跳过并记录 / 修正 registry / 放宽 build_terms / 原样写入并接受构建失败）。技术冲突本身已由验收代理独立复现。
  2. 文档口径差：§4.2 与计划 line 705 对 denylist 10 项的「写入/已存在」描述层级不同（cosmetic，无需动作）。
  3. `9c4c8b1` 删除 1 行 —— 经验收确认为**空行**（非词条），属基线修复；计划「不得删除既有行」按绝对措辞在此留痕。

## 8. W3b 完成后的清理复跑（2026-10-28，W3b 收口时补记）

W3b（D2-6=A，169 个拉丁名 concept 补中文首选名）完成后，按计划 line 737「若已先写，则须在 W3b 后重跑 T2.38 复算并清理」执行清理：

| 动作 | 内容 |
|---|---|
| 替换（7 行） | `allowlist_zh.txt` 中 W2 写入的拉丁串按新中文首选名原位替换：`VMEC`→`VMEC三维平衡程序`、`DESC`→`DESC仿星器平衡优化程序`、`SIMSOPT`→`SIMSOPT仿星器优化框架`、`C-2U`→`C-2U装置`、`EU-DEMO`→`欧洲聚变示范堆`、`K-DEMO`→`韩国聚变示范堆`、`START`→`START球形托卡马克` |
| 补写（2 行） | 先前因 zh 含空格被跳过的 `helion-trenta` / `gamma-10`，其新的中文首选名无空白 ⇒ 补入：`赫利昂Trenta装置`、`GAMMA10串列磁镜装置`（附节注释 `# --- T-4973 W3b cleanup ---`） |
| 复跑结果 | `build_terms` exit 0，`artifacts/domain_terms.txt 4893 → 4902`（+9）；`coverage_pct 70.90`（不变：这 9 个 concept 已由 EN 侧覆盖）；`W2 6 / W3a 854 / proper_excluded 35` 不变 |
| 门禁 | `sort terms/allowlist_zh.txt \| uniq -d \| wc -l` = 0；EN 空白项 = 0 |

> 说明：本文 §4.5 所列「W3b 后须复跑 T2.38」已由本节关闭；W2 残余 6 项（§3.1）与 7 个空格项（§4.1）的**已知问题状态**不变。

## 9. W3a allowlist 落地（计划外·用户授权，2026-10-29）

W3a 的 854 个中文首选名写完后**未进 allowlist**（W3 原文只写 `concepts.tsv`）⇒ coverage 报告 `W3a: 0`、覆盖率停在 72.17%。用户 2026-10-29 经 `question` 裁决「全量落地，逐批提交」，按 `w3_b01…w3_b43` 逐批写入并提交（`d9f80ed`…`ff408e2`，43 个 commit）。

| 项 | 值 |
|---|---|
| `allowlist_zh.txt` 非注释行 | 2986 → **3798**（**+812** 个名 + 43 条节注释） |
| `allowlist_en.txt` 非注释行 | 2021 → **2685**（**+664** 个 id + 43 条节注释；短语 EN 需 id 背书） |
| 逐批门禁 | `--mode allowlist` **43/43 exit 0**；`zh uniq -d` = 0；`en 空格` = 0；`build_terms` exit 0 |
| 全量门禁 | `--mode allowlist` 851/851 **exit 0**；`--mode names` 854/854 **exit 0** |
| `artifacts/domain_terms.txt` | 4902 → **6378** |
| `coverage_pct` | 72.17 → **98.57**（covered 2220 → **3032**，uncovered 856 → **44**） |
| 覆盖桶 | `W3a` **0**；`W2` **9**；`proper_excluded` **35** |

**已知例外（不变）**：`area`/`control`/`diffusion` 的 zh 名在 `terms/denylist.txt` 中，写入为静默 no-op ⇒ 未写入；这 3 批以排除该 id 的子集验收（`--expect 19`）并 exit 0。该 3 项与既有 6 项共同构成 `W2` 桶的 9 个残余。**35 个专名**（company/organization/facility）按 H2 永不入词表。

> 证据/释义缺口（747 行占位 zh 释义、854 条空 `quote`）不在本阶段范围，由 **PM 5072** 承接；W3a 命名与 allowlist 落地不受其阻塞。
