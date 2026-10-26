# Registry Evidence Bundle — 代码采纳 + 独立验收 + 提交

**Status**: ready-for-execution（2026-10-27，`date` 实测：Tue Oct 27 00:24 CST 2026）
**Execution Status**: implementation accepted; pending record + commit
**PM 来源**: 父代理关联 **T4973** ⇒ 提交信息必须含 `#T-4973`
**Scope Mode**: HOLD（不扩不缩）
**模式**: generate（本文件为唯一计划文件；本轮为 `mode=improve` 定向修订，见 §7）
**Repo**: `/home/gw/opt/fusion-terms`
**执行者**: dev-orchestrator（实施）｜独立验收：`doublecheck`（另起上下文）

**结构**：**1 个 Task**（≤30 min，含 checkpoint）＋ **2 个交付阶段**（阶段 B 独立验收 / 阶段 C 提交归档；阶段内是操作步骤，**不是**独立 Task）。

---

## 0. 允许文件白名单（唯一改动边界）

| # | 路径 | 动作 |
|---|------|------|
| 1 | `tests/test_registry_evidence_bundle.py` | **先写** 6 个测试 |
| 2 | `scripts/registry_evidence_bundle.py` | 4 处修复 + `ruff format` |
| 3 | `.gitignore` | 追加 3 行（bundle 不入 git，README 例外） |
| 4 | `artifacts/registry-evidence/README.md` | 新建 |
| 5 | `docs/notes/2026-10-27-dev-orchestrator-evidence-adoption.md` | 新建（目录不存在，需 `mkdir -p docs/notes`） |
| 6 | `.github/plans/registry-evidence-adoption.md` | 本文件 |
| 7 | `.github/plans/terminology-coverage-and-definition-quality.md` | **仅**工作区已有的末尾 29 行「Read-only registry evidence handoff gate」章节 |

**禁止**（越界即 STOP）：
- ⛔ 删除/覆盖 `artifacts/registry-evidence/` 下**任何**已有内容（bundle、`backups/*.bak`、锁文件）—— 历史证据**只增不删**
- ⛔ 提交 `terms/registry/definitions.tsv`（工作区已有独立修复，保持未暂存）
- ⛔ `git add -A` / `git add .` / `git commit -a` / `--amend` / `push` / `rebase`
- ⛔ 改 `PROFILES`、`DATA_FILES`、`CODE_FILES`、`CHECKS`、manifest `schema`、CLI 参数、`parse_result` 的 w0/all 判据
- ⛔ 触碰 `pipeline/`、`scripts/registry_row_audit.py`

---

## 1. 已完成前置（父代理实测，**无需重做**）

| 前置 | 实测值 |
|---|---|
| 无活动写入确认 | 已确认（锁可独占、无第三方进程） |
| 冻结归档 | `/tmp/opencode/registry-evidence-freeze-2026-10-27.tar.gz`，sha256 = `60b4fe081ccb60a532e3967f169c36e930991a20ee29636cbce7793fc7c9313a` |
| 源码回滚点 | `artifacts/registry-evidence/backups/20261026T163404Z-*`（`registry_evidence_bundle.py` / `test_registry_evidence_bundle.py`），**只读引用，不得覆盖** |
| 基线门禁 | `ruff check .` **红**（`B905`×2、`E702`、`F401`）、`ruff format --check .` 红（2 文件）；`pytest -q`（全量）**绿** |
| 真实 RED 证据 | `/tmp/opencode/missing-red.log` —— 「证据文件缺失」用例在**未修复**代码上的真实失败记录（test-first RED 回执） |

**执行时仍须按 §5 Pre-flight 重测**（本表数值不得当作执行时基线）。

---

## 2. 唯一 Task —— test-first 采纳（≤30 min，含 15 min checkpoint）

#### Task 1.1: 先写 6 个测试（RED）→ 再修 4 处（GREEN）→ 归位格式

- **依赖**：无（前置已完成）｜ **frontier**：是 ｜ **预估墙钟**：30 min（checkpoint 在 15 min：测试写完 + RED 已记录）
- **修改范围**：仅 `tests/test_registry_evidence_bundle.py` 与 `scripts/registry_evidence_bundle.py`

### Step 1（15 min）—— 测试先行，不碰脚本

在 `tests/test_registry_evidence_bundle.py` 追加 helper + **6 个测试**（每个测试名唯一，供 §6 V4 按成员校验）：

1. `test_fingerprint_changes_on_data_and_checker_edits(tmp_path, monkeypatch)`
   fake root（`tmp_path/fakeroot`，含 `DATA_FILES + CODE_FILES` 副本 + `git init -q`）→ `monkeypatch.setattr(module, "ROOT", fake_root)` → `execution_fingerprint("w0")` 取 `fp1`；改 1 字节数据文件 ⇒ `fp2 != fp1`；改 1 行检查器文件 ⇒ `fp3 != fp2`；`make_snapshot()` 两次哈希不同 ⇒ 顺带**真正使用** `make_snapshot`（消除 `F401`）。断言工作区脚本 sha256 前后一致（零触碰证据）。
2. `test_reuse_refuses_changed_fingerprint(tmp_path)`：合法 bundle + `fingerprint="fp-good"` ⇒ `validate_manifest(bundle, "fp-good")` 不抛；`validate_manifest(bundle, "fp-bad")` ⇒ `SystemExit` 匹配 `execution fingerprint changed`。
3. `test_reuse_refuses_missing_evidence_file(tmp_path)`：删 `baseline/validate_registry.stdout` ⇒ `SystemExit` 匹配 `missing evidence path`。
4. `test_reuse_refuses_tampered_evidence_file(tmp_path)`：向 `batch/registry_row_audit.stdout` 追加字节 ⇒ `SystemExit` 匹配 `tampered evidence batch/registry_row_audit`。
5. `test_same_audit_scope_differs_between_w0_and_all()`：同一份 audit JSON（`w0_is_clean=True, is_clean=False, non_zero_metrics=..., deferred_w1_metrics=...`，`rc=0`）⇒ `parse_result(..., "w0")["status"]=="pass"`（且 warnings 含 `deferred:` 前缀项）、`parse_result(..., "all")["status"]=="fail"`。
6. `test_failed_comparison_cannot_reuse(tmp_path)`：各 check 全 pass 但 manifest `same_structured_result=False`（baseline/batch 摘要实际相同）⇒ `SystemExit` 匹配 `comparison summary mismatch`。

共享 helper `_build_passing_bundle(root, *, profile="w0", same=True, ...) -> Path`：造 `snapshot/`（复制 `DATA_FILES + CODE_FILES`）、`baseline/`、`batch/`、`manifest.json`（schema 3、`snapshot_hashes`、baseline/batch 全 pass 摘要、`same_structured_result`、`execution_fingerprint` 由调用方给定）。

**Step 1 收尾（RED 记录）**：
```bash
cp -p scripts/registry_evidence_bundle.py /tmp/opencode/pre-fix-registry_evidence_bundle.py   # 回滚点（仓外副本）
python3 -m pytest tests/test_registry_evidence_bundle.py -q -k "missing or tampered or fingerprint or scope or comparison" \
  > /tmp/opencode/evidence-adoption-red.log 2>&1; echo "rc=$?"
```
期望（**测试先行的判别力证明**）：
- 用例 3 **必须 RED**：未修复时代码抛未捕获 `FileNotFoundError`（与 `/tmp/opencode/missing-red.log` 同因）⇒ 证明该用例承重，**且不需要任何变异/破坏操作**
- 用例 1/2/4/5/6 在修复前即为 GREEN —— 它们是**既有守卫的回归锁**（characterization），**本节不声称它们 RED**（诚实口径）
- 若用例 3 竟然 GREEN ⇒ 停下核对是否已被修复；若确实已修则记录事实并说明 RED 回执来自 `/tmp/opencode/missing-red.log` 的既有时点

### Step 2（10 min）—— 最小修复（仅 4 处）

`scripts/registry_evidence_bundle.py`：
1. `zip(phase_results["baseline"], phase_results["batch"])` → 追加 `, strict=False`（两列同源 `CHECKS`、等长，保持现有语义）
2. `zip(baseline, batch)` → 追加 `, strict=False`
3. `baseline_dir.mkdir(); batch_dir.mkdir()` → 拆两行（消 `E702`）
4. `safe_bundle_path()` 内、既有 symlink 检查**之后**新增：
   ```python
   if not path.is_file():
       raise SystemExit(f"refusing reuse: missing evidence path: {relative}")
   ```
   （仅被 `validate_manifest` 的 stdout/stderr 两处调用 ⇒ 单点覆盖两侧，不新增参数）

### Step 3（5 min）—— 格式与 GREEN

```bash
.venv/bin/ruff --version                                   # 期望 0.17.2（与 requirements-dev.txt 钉版一致）
.venv/bin/ruff format scripts/registry_evidence_bundle.py tests/test_registry_evidence_bundle.py   # 只格式化这 2 个文件
python3 -m pytest tests/test_registry_evidence_bundle.py -q; echo "rc=$?"    # 期望 0
.venv/bin/ruff check .; echo "rc=$?"; .venv/bin/ruff format --check .; echo "rc=$?"   # 期望均 0
```

- **修改边界**：⛔ 不改白名单外文件；⛔ 不 `ruff format .`（会波及无关文件）；⛔ 不新增 CLI/字段/指标；⛔ 不用仓内 `backups/*.bak` 做任何实验素材
- **质量检查方式**：Step 1 的 RED 日志存在且用例 3 失败；Step 3 后同一命令全绿；`git diff --stat` 仅 2 文件
- **验收标准**（详见 §6 V1–V4，此处只列 Task 级出口条件）：
  - ✅ 6 个测试名**逐个按名执行**均 exit 0（成员校验，非计数）`[T-A]`
  - ✅ `ruff check .` 与 `ruff format --check .` 均 exit 0 且 `--check` 输出中 `would be reformatted` 计数为 0 `[T-A]`
  - ✅ RED 回执可溯源：`/tmp/opencode/evidence-adoption-red.log` 含用例 3 的失败痕迹 `[T-B]`
  - ✅ 全量 `pytest -q` exit 0（无回归）`[T-A]`
  - **能失败证明**：用例 3 的 RED 已在 Step 1 实测记录（test-first 的固定证据）；**不采用**任何变异/覆盖备份/破坏性操作来制造失败
- **潜在风险**：修脚本 ⇒ 其 sha256 变化 ⇒ **既有 bundle 的 `execution_fingerprint` 全部失效、不可 reuse**（设计内；旧 bundle 仅作历史留档，磁盘保留 + §1 冻结归档）；此点须写入 README 与 notes
- **checkpoint（15 min）**：若 15 min 时测试尚未写完 ⇒ 停止并回报进度，不得跳过 Step 1 直接改脚本（否则违反 test-first）

---

## 3. 阶段 B —— 独立验收（操作步骤，非独立 Task）

实施完成后**由另起上下文的 `doublecheck`** 复跑；`doublecheck` 不可用 ⇒ 自审并标注 `[⚠️ doublecheck delegation degraded]`。

**B1 生成修复后的新鲜 bundle 并取路径**（旧 bundle 因 fingerprint 失效，**必须**用新鲜 bundle 做 reuse 探针）：
```bash
python3 scripts/registry_evidence_bundle.py --compare               > /tmp/opencode/w0.json ; echo "w0 rc=$?"
python3 scripts/registry_evidence_bundle.py --compare --profile all > /tmp/opencode/all.json ; echo "all rc=$?"
FRESH_W0=$(python3 -c "import json;print(json.load(open('/tmp/opencode/w0.json'))['path'])")
FRESH_ALL=$(python3 -c "import json;print(json.load(open('/tmp/opencode/all.json'))['path'])")
```
> `all` 运行**期望 exit 1**（W1 未完成）但 stdout 仍为合法 JSON（含 `path`、`status=fail`）⇒ 从 json 文件取路径可靠。派单时必须写明「`all` 的 exit 1 是期望值」，避免复核者误报缺陷。

**B2 reuse 正/负路径**：
```bash
python3 scripts/registry_evidence_bundle.py --reuse "$FRESH_W0"                ; echo "rc=$?"   # 期望 0
python3 scripts/registry_evidence_bundle.py --reuse "$FRESH_ALL" --profile all ; echo "rc=$?"   # 期望 1，evidence incomplete or failed
```

**B3 仓外探针（只读副本；两个独立目录，期望互不混淆）**：
```bash
PT=/tmp/opencode/reuse-probe-tamper; PM=/tmp/opencode/reuse-probe-missing
mkdir -p "$PT" "$PM"; cp -a "$FRESH_W0"/. "$PT"/; cp -a "$FRESH_W0"/. "$PM"/
printf 'tamper' >> "$PT/batch/registry_row_audit.stdout"
python3 scripts/registry_evidence_bundle.py --reuse "$PT"; echo "rc=$?"   # 期望 1，tampered evidence batch/registry_row_audit
rm "$PM/baseline/validate_registry.stdout"                                # 仅动 /tmp 副本
python3 scripts/registry_evidence_bundle.py --reuse "$PM"; echo "rc=$?"   # 期望 1，missing evidence path: baseline/validate_registry.stdout
```
⛔ 探针**只允许**作用于 `/tmp/opencode/` 下的副本；⛔ 不得删改仓内任何 bundle。

**B4 全量门禁**：`.venv/bin/ruff check .`、`.venv/bin/ruff format --check .`、`python3 -m pytest -q`、`python3 -m compileall -q pipeline tests`、`python3 -m pipeline.validate_registry --terms-dir terms` ⇒ 全部 exit 0。

**B5 回执**：逐条写入 `/tmp/opencode/acceptance-receipts.txt`（含每条的实测 `rc=`），交给 `doublecheck` 对照 §6 V 表逐条给 `[MATCH]/[MISMATCH]`，并要求其在 `/tmp` 副本上**独立复现至少 V5/V6/V7/V8**。任一 `[MISMATCH]` ⇒ 回到 Task 1.1 修复后**重跑 B1–B5 全部**（不新增 Task）。

---

## 4. 阶段 C —— 提交与归档（操作步骤，非独立 Task）

**C1 忽略规则**（`.gitignore` 末尾追加 3 行；负向规则必须位于正向规则之后）：
```
# Registry evidence bundles (machine-local evidence; regenerated on demand)
artifacts/registry-evidence/*
!artifacts/registry-evidence/README.md
```

**C2 证据目录 README**（`artifacts/registry-evidence/README.md`，≤45 行，用 `## ` 二级标题，6 节）：① 用途（Phase 0 只读证据包）② 运行（`--compare` 默认 w0；`--profile all` 仅 Phase 1 完成后；`--reuse`）③ 目录结构（`manifest.json` + `baseline/` + `batch/` + `snapshot/`，`backups/` 为改前 `.bak`）④ reuse 语义（逐份重解析、**从不信任**顶层 `batch_status`）⑤ **fingerprint 失效**（覆盖 6 数据 + 5 检查器文件 + git status + Python 版本 + profile ⇒ 任意数据/检查器改动使既有 bundle 不可 reuse，属设计内）⑥ 保留策略（机器本地、不入 git、**可保留不删**；如需释放空间由用户决定，README **不得**给出自动/批量清理命令）。
⛔ README 不得写「某次运行的 pass 数」等一次性结论；⛔ 不得声称 CLI 条目缩减等价于调用次数减少。

**C3 采纳记录**（`mkdir -p docs/notes` 后新建 `docs/notes/2026-10-27-dev-orchestrator-evidence-adoption.md`，≤60 行，6 节）：① 决策与范围 ② 冻结回执（§1 的归档路径 + sha256，**逐字复制父代理实测值**）③ 修复项（B905×2 / E702 / F401 / 缺失路径守卫）④ AC 回执路径（`/tmp/opencode/acceptance-receipts.txt`、`evidence-adoption-red.log`）⑤ 已知取舍（旧 bundle 不可 reuse；`all` 期望红；bundle 机器本地不入 git）⑥ 未做（未 push、未动 W1/W2/W3、未动 `definitions.tsv`）。
> 该路径由本计划指定（仓库常规开发文档在 `docs/dev/`，本文件不改动既有目录结构，仅在 `docs/notes/` 新增一份会议级记录）。

**C4 精确暂存 + 提交**（`#T-4973` 必须出现）：
```bash
git rev-parse origin/master | tee /tmp/opencode/origin-master-before.txt
git add tests/test_registry_evidence_bundle.py scripts/registry_evidence_bundle.py .gitignore \
        artifacts/registry-evidence/README.md docs/notes/2026-10-27-dev-orchestrator-evidence-adoption.md \
        .github/plans/registry-evidence-adoption.md \
        .github/plans/terminology-coverage-and-definition-quality.md
git diff --cached --name-only | sort > /tmp/opencode/staged.txt   # 必须与白名单 7 条逐字一致
git status --porcelain                                            # 期望只剩： M terms/registry/definitions.tsv
git commit -m "test(registry-evidence): adopt read-only registry evidence bundle (#T-4973)

- write refusal tests first (fingerprint drift, missing/tampered evidence, w0-vs-all scope, failed comparison)
- fix ruff gate (B905 x2, E702) and add explicit missing-evidence refusal
- ignore machine-local bundles, keep README under version control"
```

**C5 归档**（仅在 B 阶段全绿后执行；**归档是唯一允许的 follow-up commit**）：
```bash
git mv .github/plans/registry-evidence-adoption.md .github/plans/completed/registry-evidence-adoption.md
git commit -m "docs(plans): archive registry-evidence-adoption after acceptance (#T-4973)"
```
未全绿 ⇒ 标记 `[ARCHIVE: BLOCKED]`，**不执行** C5。

---

## 5. Pre-flight（每次开始操作前重测，替换一切硬编码基线）

```bash
cd /home/gw/opt/fusion-terms
date                                                  # 日期类输出唯一来源
git rev-parse HEAD; git rev-parse origin/master       # 动态基线
git status --porcelain                                # 期望： M ×2（主计划 + definitions.tsv）+ ?? artifacts/registry-evidence/ scripts/…
sha256sum scripts/registry_evidence_bundle.py tests/test_registry_evidence_bundle.py
.venv/bin/ruff --version                              # 期望 0.17.2
```
漂移处置：白名单外出现新的 ` M`/`??` ⇒ STOP 并向父代理确认；`definitions.tsv` 变为已暂存 ⇒ `git restore --staged terms/registry/definitions.tsv`；两文件 sha256 与 §1 回滚点不一致 ⇒ 说明有他人改动，先回报再动手。

---

## 6. Post-Execution Verification（机械 AC）

| ID | 内容 | 命令 | Expected |
|----|------|------|----------|
| V1 | lint 归零 | `.venv/bin/ruff check .` | exit 0 |
| V2 | 格式归零 | `.venv/bin/ruff format --check .` | exit 0 且输出无 `would be reformatted` |
| V3 | 全量测试 | `python3 -m pytest -q` | exit 0 |
| V4 | 6 个测试**按成员**齐备且逐个通过 | `python3 -m pytest tests/test_registry_evidence_bundle.py --collect-only -q` 的输出中逐名 `grep -qx`；再对每个名字跑 `python3 -m pytest tests/test_registry_evidence_bundle.py -q -k "<name>"` | 6 个名字全部命中且每次 exit 0（**不校验总数**） |
| V5 | w0 真跑 | `python3 scripts/registry_evidence_bundle.py --compare` | exit 0，`status=pass` |
| V6 | all 真跑 | `python3 scripts/registry_evidence_bundle.py --compare --profile all` | exit **1**，`status=fail`（W1 未完成，**期望值**） |
| V7 | reuse 正路径 | `--reuse "$FRESH_W0"` | exit 0 |
| V8 | reuse 负路径 | `--reuse "$FRESH_ALL" --profile all` | exit 1，`evidence incomplete or failed` |
| V9 | 编译 | `python3 -m compileall -q pipeline tests` | exit 0 |
| V10 | 数据门禁 | `python3 -m pipeline.validate_registry --terms-dir terms` | exit 0 |
| V11 | bundle 未入库 | `git ls-files artifacts/registry-evidence` | 输出恰为 `artifacts/registry-evidence/README.md` 一行 |
| V12 | 提交范围**按成员**等于白名单 | `git show --name-only --pretty=format: HEAD \| grep . \| sort` 与 §0 七路径 `sort` 后 `diff` | diff 空 |
| V13 | 未夹带 definitions | `git show --name-only --pretty=format: HEAD \| grep -c definitions.tsv` | `0`，且 `git status --porcelain terms/registry/definitions.tsv` 非空 |
| V14 | 未 push | `test "$(git rev-parse origin/master)" = "$(cat /tmp/opencode/origin-master-before.txt)"` | exit 0 |
| V15 | PM 关联 | `git log -1 --pretty=%B \| grep -q '#T-4973'` | exit 0（C5 归档提交须同样含） |
| V16 | 历史证据未被删改 | `ls -1d artifacts/registry-evidence/2*/` 的集合 ⊇ §1 冻结清单集合；`tar -tzf /tmp/opencode/registry-evidence-freeze-2026-10-27.tar.gz \| wc -l` ≥ 归档时实测值 | exit 0 |

### Deferred (needs restart / deployment)
- 无（本计划不涉及服务/部署）。

### Probe (best-effort, run if available)
- [ ] P1 `--reuse /tmp/opencode/reuse-probe-tamper` → exit 1 含 `tampered evidence`
- [ ] P2 `--reuse /tmp/opencode/reuse-probe-missing` → exit 1 含 `missing evidence path`
- [ ] P3 `--reuse <T1.1 之前的旧 bundle>` → exit 1 `execution fingerprint changed`（反证 fingerprint 门在真跑路径承重，并固化「旧 bundle 仅历史留档」）
- [ ] P4 `sha256sum /tmp/opencode/registry-evidence-freeze-2026-10-27.tar.gz` → 与 §1 值一致

### Manual（真正需要人工判断）
- [ ] M1 阅读 `artifacts/registry-evidence/README.md`：确认「fingerprint 失效 / 不入 git / 不自动清理」三条无歧义，且未与主计划末尾章节的门禁承诺冲突
- [ ] M2 阅读 notes：确认「已知取舍 / 未做」完整覆盖本次决策边界，且无「已获 push 授权」类表述
- [ ] M3 人工比对提交范围语义（机器只做 diff，人判路径是否确属本次采纳）

---

## 7. 风险与回滚（安全优先）

| # | 风险 | 缓解 | 回滚（**不破坏既有产物**） |
|---|------|------|--------------------------|
| R-1 | `git add -A` 夹带 `definitions.tsv` | C4 只按白名单逐路径 `git add`；V13 | `git restore --staged terms/registry/definitions.tsv`；重做 C4 |
| R-2 | 大体积 bundle（~21 MB）入库 | C1 先加忽略规则；V11 | `git rm -r --cached artifacts/registry-evidence`（不动磁盘文件）；重做 C1 |
| R-3 | `ruff format` 波及无关文件 | 只格式化指定 2 文件；V2 复核 | `git restore -- <白名单外文件>`（**逐文件**，**禁止** `git checkout -- .`） |
| R-4 | ruff 版本漂移 | Pre-flight 校验 0.17.2；只调 `.venv/bin/ruff` | 换钉版解释器重跑 Step 3 |
| R-5 | 脚本修复 ⇒ 旧 bundle 不可 reuse | 设计内；README ⑤ + notes ⑤ + P3 固化 | 无需回滚（旧 bundle 保留于磁盘与冻结归档） |
| R-6 | 测试先行被跳过 | Step 1 checkpoint 强制；RED 回执留档 | 回到 Step 1 重做 |
| R-7 | 并发会话写 bundle | Pre-flight + §1 锁自查；发现写入者 STOP | 重跑冻结流程（由父代理） |
| R-8 | `all` 期望红被误判缺陷 | §3 B1 派单明示期望值；notes ⑤ | — |
| R-9 | 回滚需求 | 回滚点：`/tmp/opencode/pre-fix-registry_evidence_bundle.py`（Step 1 副本）与 §1 的 `20261026T163404Z` 备份 | `cp -p /tmp/opencode/pre-fix-registry_evidence_bundle.py scripts/registry_evidence_bundle.py`（**只读引用备份，绝不覆盖 `.bak`**） |

**硬禁令**：⛔ 任何 `rm -rf`（含清理示例）⛔ `git checkout -- .` / `git reset --hard` ⛔ 覆盖或删除 `backups/*.bak` 与既有 bundle ⛔ 用历史产物做变异/破坏性实验（失败判别力一律取自 Step 1 的真实 RED 日志）。

---

## 8. 本轮 improve 修订记录（诚实口径）

本文件由 `mode=improve` 定向修订，**仅**针对父代理列出的缺陷逐条修正；**未**对全文条款做全量复核，也**不声称**所有条款均已审过。

| # | 原缺陷 | 本版处理 |
|---|--------|---------|
| 1 | 用旧备份 `.p1.bak` 作反例（违反保留要求） | 删除该做法；失败判别力改引自 Step 1 真实 RED 回执（`/tmp/opencode/evidence-adoption-red.log` 与既有 `missing-red.log`） |
| 2 | README 含 `rm -rf` 批量清理示例（违反不删除） | 删除；README ⑥ 只述「机器本地、不入 git、保留不删」，清理决策交用户 |
| 3 | 回滚用 `git checkout -- .`（丢工作） | 改为逐文件 `git restore -- <file>`；脚本回滚用 `/tmp` 副本 `cp -p`；硬禁令列明 |
| 4 | 先修后测（违反 test-first） | 重排为 Step 1 测试先行 + RED 记录、Step 2 修复、Step 3 GREEN；checkpoint 强约束 |
| 5 | 测试数记错（实为 6 个，却按 5 计并写死 12 通过数） | 更正为 6 个；V4 改为**按测试名成员校验**（逐个 `-k <name>`），取消所有通过数硬编码 |
| 6 | 11 个 Task 与「单一 commit」冲突 | 压缩为 **1 个 ≤30 min Task** + 阶段 B（独立验收）/ 阶段 C（提交归档）操作步骤；阶段不设 Task 编号 |
| 7 | 声称 `docs/notes/` 为「用户指定路径」（不实） | 改为「本计划指定」，并说明仓库常规开发文档在 `docs/dev/` |
| 8 | 未关联 PM 来源 | 全篇按 **T4973** 标注，提交信息必含 `#T-4973`（V15） |

**已知残留（未处置，交父代理判断）**：app 未对「测试 1/2/4/5/6 属回归锁而非 RED」做进一步拆分（本次要求压缩为单 Task）；`--profile all` 期望红的措辞依赖复核者读派单 prompt。

---

## 9. Handoff

- Task 1.1 完成 → **阶段 B**（`doublecheck` 独立验收，操作步骤）→ **阶段 C**（提交 `#T-4973` + 归档）
- 结束后回报：V1–V16 回执行 + `/tmp/opencode/acceptance-receipts.txt` 路径 + `git show --stat` 摘要
- → handoff: **USER**（**不 push**，远端同步待用户决定）

## 10. Execution Log（实际执行口径）

- **实际 RED 回执**：`/tmp/opencode/missing-red.log`（新增 missing-evidence 用例在修复前抛 `FileNotFoundError`）。计划 Step 1 中的 `/tmp/opencode/evidence-adoption-red.log` 未生成；验收者确认以 missing-red.log 为有效替代。首次尝试写入测试时出现 heredoc `\n` 被 shell 展开的语法错误，修正后重测，该收集失败不计作 RED 证据。
- **独立验收证据目录**：`/tmp/opencode/evidence-adoption-acceptance/`（`RECEIPTS.txt` + V/P/M 日志；编号为验收者自有口径，与 §6 V 表非逐一同名）。验收判定 **PASS**，无 blocking 项。
- **V8 实测拒绝理由**：`--reuse <all bundle> --profile all` 返回 `execution fingerprint changed`，而非 `evidence incomplete or failed`（all bundle 生成时指纹已含 profile=all）。两者均为安全拒绝；下游若按文本匹配需知悉。
- **README 补充**：新增「Fingerprint scope」（指纹排除 `artifacts/registry-evidence/` 自身的 git status 行）与「Retention」明确 `backups/` 同样被忽略；措辞低于实际强度，不宣称鉴权作者身份。
- **§1 基线为修复前口径**：执行后 `ruff check .` / `ruff format --check .` 已转绿（全量 175 passed，目标文件 13 passed）。
- **最终哈希**：`scripts/registry_evidence_bundle.py` = `a2380a4620724a8fabbbae7f6a0b610c80dd96d0574f9ab49683050a639f6c6e`；`tests/test_registry_evidence_bundle.py` = `35673d15b689ab1b3334918c9ea5bf55cf542e9b99553173a2c48f402e90c06b`。
- **未做**：未 push；未提交 `terms/registry/definitions.tsv`（保留其独立修复）；未删改任何历史 bundle 或 `backups/*.bak`。

### 10.1 提交后保留性复核（更正）

- 提交后初次用 `ls -1d artifacts/registry-evidence/2*/` 核对，只列出 8 个目录，曾误判有 3 个历史 bundle 缺失。
- 复核方式：`ls -1 artifacts/registry-evidence`、Python `Path.glob('2*')` 与定点 `stat` 三种路径一致显示 **13 个 bundle 目录 + backups + README**；冻结清单中的 11 个全部在位，另 2 个为验收阶段新生成。
- 用冻结 tarball 做只补缺、不覆盖的回填演练：`RESTORED_FILES=0`（无文件需要恢复），且 `git status` 仍只显示 `terms/registry/definitions.tsv` 一项，未产生任何写入。
- 结论：**历史证据完整保留，未发生删除**；此前 8 条的输出是列举方式造成的观测误差，不是数据丢失。带尾斜杠的 glob 列举不可作为保留性判据，改用 `ls -1 <dir>` 计数。
