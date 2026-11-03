# 状态事实矩阵

## 原样基线（B1/B2/B9/B11/B12/B13）

```text
## 2026-11-03T08:35:14+08:00
115da749251f6a8c94e8a1d4ea0ce3c412c614bf
?? .github/plans/5184-four-stage-closeout.md
## tags-contain-5072
0
0
## tag-5110
fa34be1
  origin/HEAD -> origin/master
  origin/master
## contract
contract OK: domain_terms.txt terms=6375 version=v2026.10.30 commit=fa34be1f6d6d generated_at=2026-10-30T01:49:57Z
contract_exit=0
## 5072-status
10:status: "active"
## M-open
979:- [ ] M1: W1 抽检（每 5 批 ≥8 行）语义正确性复核 —— **未勾选**：批次记录中无独立语义抽检留痕（`registry_batch_verify` 机械门禁全绿 ≠ 语义正确）；移交 PM 5072。
981:- [ ] M3: `w3-name-conflicts.tsv` 中的冲突项人工裁决 —— **未勾选**：`physical-sputtering` / `物理溅射` 与 `sputtering` 的 zh 别名冲突为 **pre-existing**（该 id 不在 `w3.ids`，W3a 未改该行），待人工裁决（PM 5072 承载）。
982:- [ ] M4: 目视抽检 T0.4（99 行）/T0.5（80 行）修复后 10 行的列语义（中文/英文是否各归其位）—— **未记录**：`registry_row_audit --audit --expect-clean-all` 结构门禁 exit 0（`malformed=0 / shifted=0 / sixcol=0`），但无 10 行目视留痕 ⇒ 不勾选。
```

## 结论与边界

- 5072：历史 PM/独立验收记录为执行完成；本次实测数据未进入任何发布 tag，不等于已发布。
- 5110：v2026.10.30 已发布且本地发布契约通过，无需重发。远端分支信息为本地已有引用，未联网刷新。
- M1/M3/M4 均未勾，后续依据语义证据分别判断。
- B2 与原计划漂移：当前仅执行计划未跟踪，未发现历史 iaea_fusion.html；不据此修改任何数据。
- 数据目录 terms/、artifacts/、pipeline/、scripts/ 全程只读。
