# Evidence bundle adoption — registry gates

本目录为采纳记录路径；仓库常规开发文档仍在 `docs/dev/`。

## Decision
保留 `registry_evidence_bundle` 原型并采纳为机器本地证据工具，而非删除或原样入库。
边界：不删除任何历史 bundle 或 `backups/*.bak`；不提交 `terms/registry/definitions.tsv`（其独立修复保留）；不 push。

## Frozen inputs
- 冻结归档：`/tmp/opencode/registry-evidence-freeze-2026-10-27.tar.gz`
  sha256 `60b4fe081ccb60a532e3967f169c36e930991a20ee29636cbce7793fc7c9313a`（11 bundle / 258 条目）
- 源码回滚点：`artifacts/registry-evidence/backups/20261026T163404Z-*.bak`（与改前 sha256 一致）
- 改前基线：`ruff check` 红（B905×2、E702、F401）、`ruff format --check` 红（2 文件）、全量 pytest 绿

## Fixes
- 新增 missing-evidence 显式拒绝（原为未捕获 `FileNotFoundError`）；RED 回执 `/tmp/opencode/missing-red.log`
- 修复 `zip()` 缺 `strict=`（B905×2）与分号合并语句（E702）
- 测试侧消除未使用导入（F401），并补齐 6 个行为测试：指纹漂移拒绝、指纹变更拒绝、篡改拒绝、缺失拒绝、w0/all 范围差异、比对失败拒绝
- 仅对目标两文件执行 `ruff format`

## Verification
- 独立验收目录：`/tmp/opencode/evidence-adoption-acceptance/`（判定 PASS，无 blocking）
- 关键实测：`ruff check .` / `ruff format --check .` / 全量 pytest / compileall / validate_registry 均 exit 0
- `--compare`（w0）exit 0 `status=pass`；新鲜 w0 bundle `--reuse` exit 0
- `--compare --profile all` exit 1 `status=fail`（T-4973 W1 未完成，期望红）；`--reuse` all bundle exit 1
- 仓外副本探针：篡改 / 缺失 / snapshot 哈希 / 顶层状态翻转均被拒绝
- 变异证明（仅 /tmp 副本）：删除 4 项守卫分别使对应测试变红，恢复后哈希与仓内一致

## Known trade-offs
- 修复脚本改变其 sha256 ⇒ 既有 bundle 的执行指纹失效，仅作历史留档，不可 reuse（设计内）
- `--reuse <all>` 实际拒绝理由为 `execution fingerprint changed`，非 `evidence incomplete or failed`
- 证据哈希只能发现意外改动，不能证明作者身份；bundle 为机器本地产物，不入 git（仅 README 入库）

## Not done
- 未 push；未提交 `terms/registry/definitions.tsv`
- 未触碰 W1/W2/W3 术语数据；未新增 audit 指标；未删改历史产物
