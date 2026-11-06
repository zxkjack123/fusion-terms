# 5072 独立验收补齐 —— I6（75 zh + 86 evidence）与 I9（16 CORRUPT）

Audience: repository developers / agents（内部技术产物 ⇒ `[de-ai-fier: N/A — 受众为开发者/agent]`）。

- 日期：`2026-11-06`（`date` 实测）
- 基线：`8304c42`（branch `master`，无 tag）
- 执行者：`acceptance-verifier`（**只读**，未改任何仓文件；产物由父代理落盘）
- 计划：`.github/plans/5072-w3a-evidence-definition-backfill.md` §10 行 **I6 / I9**（原标 `UNVERIFIED`）
- 授权：用户 2026-11-06「做第 1 项（补齐 5072 的 I6/I9）」

## 1. 先决：行型分类基准复现

按 plan §D6 口径（`EN_SEE` / `BODY`）对 854 w3 ids 分类：全量 502/336/16；**对 747 条 `translated:` in-scope 行 = 431 / 300 / 16** ⇒ plan §D5「必须整体成立」基线**精确复现**。其余 107 条为 pre-existing zh（`GB/T-4960.9` 26 + `internal:dict-improvements` 81），按 §1 `BOUNDARY OUT` 不属本任务修改范围。

## 2. 抽样（确定性、可复现）

- 排序键：`(sha256(concept_id)[:16], concept_id)` 升序（第二键消歧；实测无碰撞）
- I6-zh 样本 = 前 **75**；I6-evidence 样本 = 前 **86**
- 家族分布：zh 样本 DEFINITION 43 / CROSS_REF 28 / CORRUPT 4（三族均非空）；evidence 样本 48 / 34 / 4
- **样本集指纹**（`sha256("\n".join(sorted(ids)))`）：
  - I6-zh：`d2a83a3935e57f890bc4390b4a9b6e2f1ef389ed73019900eb8fa058a2c1265a`
  - I6-evidence：`1dd3bad2328452a5121fb9f43b74df405adf3175e950fbb2ab4f30b13af4f1bf`
- I6-zh 样本 id（75，按抽样顺序）：
  `gut-transfer-factor, level, medical-exposure, abnormal-operation, upper-ports, institutional-control, evacuation, safety-class, radiological-medical-practitioner, tritium-recycling, aleatory-uncertainty, rock-igneous, plant-equipment, iaea-publication, low-specific-activity-material, certificate, relative-biological-effectiveness, emergency-procedures, procedure, end-state, naturally-occurring-radioactive-material, immediate-dismantling, bioshield, on-site, physical-half-life, natural-uranium, functional-diversity, projected-dose, operator, nbtf, maintenance-bypass, senior-management, shutdown, qualified-equipment, criticality-safety-index, logic, cooldown, service-conditions, core-components, pretreatment, electron-beam, routine-monitoring, failure-mode, processing, deferred-dismantling, performance-indicator, essential-services, dose-and-dose-rate-effectiveness-factor, transportation, special-population-group, capable-fault, safety-assessment, nuclear-fuel-cycle-facility, health-professional, absorption-type-lung, becquerel, reference-air-kerma-rate, publication-iaea, gray, operating-personnel, non-fixed-contamination, personal-dose-equivalent-hp, control, unsealed-source, common-mode-failure, dose-concepts, notification, crust-earth-s, urgent-protective-action, dose-equivalent-quantities, therapeutic-exposure, radioactivity, monitoring, diffusion, sievert`
- **口径声明**：I6-zh 按 **747 in-scope** 判定；样本中 5 条 pre-existing 行（`abnormal-operation`、`aleatory-uncertainty`、`absorption-type-lung`、`becquerel`、`bioshield`）不计入 PASS 分母，已显式列出而非静默剔除。

## 3. 结果

| 检查 | 样本 | PASS | FAIL | 判定 |
|---|---:|---:|---:|---|
| I6-zh（语义） | 75（in-scope 70） | **70** | **0** | **PASS** |
| I6-evidence（逐字） | 86 | **86** | **0** | **PASS** |
| I9（16 CORRUPT，全量非抽样） | 16 | **16** | **0** | **PASS** |

### 3.1 I6-zh 机械判据（逐族）

| 判据 | 适用 | 结果 |
|---|---|---|
| DEFINITION：含 CJK / 非空 / zh≠en / 无占位串 | 41 | PASS 41 |
| DEFINITION：数字多重集 == en（`\d+(?:\.\d+)?`） | 41 | PASS 41 |
| DEFINITION：en 缩写无缺失 / 无新增 | 41 | PASS 41（3 处新增缩写经裁定合法，见 §3.3） |
| CROSS_REF：`^见 .+。$`、无 `[]!;`、目标 == `preferred_zh`（含附录 C 覆写） | 25 | PASS 25 |
| CORRUPT：`^见 .+。$`、无 `[]!;`、无污染残余 | 4 | PASS 4 |

### 3.2 I6-evidence

- 86/86 quote 在对应 raw 源中**逐字命中**（归一化：去私用区字形 → 换空格 → 压 `\s+`；**未**使用近似匹配）；无空 quote、无无法定位、无中途截断（长度 10–5247 字符）。
- **源-文件严格对齐**（非空转证明）：IAEA URL 80 行全部命中 `iaea_safety_glossary_raw.tsv`、ITER URL 6 行全部命中 `iter_glossary_raw.tsv`，无交叉命中。
- **负对照**：将首条 quote 尾部 5 字符改为 `XYZ` 后全部 raw 源均无法定位 ⇒ 判定具备可失败性。

### 3.3 三处边界裁定（均 PASS，附依据）

| # | 现象 | 裁定与依据 |
|---|---|---|
| a | `nbtf` zh 新增缩写 `NBTF`（en 无此串） | **PASS** —— 该概念 `preferred_en = "NBTF"`，规则 2/3 授权；同族 `epfl`→`EPFL`、`mast-upgrade`→`MAST` 同理。全库 431 条 translated DEFINITION 中仅此 3 条有新增缩写，3/3 均可由 `preferred_en` 解释 |
| b | `dose-concepts` 命中「术语，」占位检测器 | **PASS（虚警）** —— 上下文为「应酌情使用更为具体和精确的术语，例如待积剂量或集体剂量」，忠实对应 en；该行 en 为 8 条目聚合，zh 完整覆盖 8 个头 |
| c | `physical-half-life` / `therapeutic-exposure` 目标不在直配集 | **PASS** —— 二者均为附录 C.2 已登记行（#34 `见 放射性半衰期。`、#50 `见 医疗照射。`），属 D5 步骤③ 复合拆解；zh 与台账逐字一致 |

### 3.4 I9（16 条 CORRUPT，全量）

16/16 四项全过：① 均在附录 C.1；② 均有污染形态描述；③ zh **逐字等于**台账「应写 zh」；④ zh 无 `[ ] ! ;` 且无残余。附加对抗检验：取每条 en `BODY` 残余中所有 ≥4 字符英文 token 在 zh 中检索 ⇒ **0 泄漏**。附录 C.1 解析 16 行、C.2 解析 52 行（合计 68，与「29 NO-TARGET + 39 复合」台账规模一致）。

## 4. 顺带关闭 I3（原「未重跑」）

```
timeout 300 python3 scripts/registry_batch_verify.py --mode evidence \
  --ids-file .github/plans/t4973-batches/w3.ids --expect 854 --check-urls
→ probes=2 ； verdict=PASS ； ids=854 ； exit=0
```

⇒ I3 由「⚠️ 未重跑」转为 **✅ 实测通过**。

## 5. 观察项（不阻塞，建议另立）

- 附录 B applier 的缩写门禁是**单向**的（`set(ACR(en)) - set(ACR(zh))`：只查缺失、不查新增）⇒ 无法阻止真正编造的缩写。本次 3 条新增缩写恰好合法，未造成缺陷。建议后续补一条反向断言：「新增缩写必须 ∈ `concepts.preferred_en`」。

## 6. 声明

- 独立执行者为只读；本报告由父代理（dev-orchestrator）落盘，内容与 verifier 回传一致。
- 未 push、未创建 tag；未改 `terms/`、`artifacts/`、`pipeline/`、`dist/`、`CHANGELOG.md`。
- 抽样与判定可复现：给定 §2 的排序键与指纹，可重建同一 75/86 样本集。
