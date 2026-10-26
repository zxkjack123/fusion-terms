# T4973 — `registry_batch_verify.py --self-test` 重锚（裁决 4，off-plan）

> **性质**：本文件记录一次 **off-plan 回归修复**的证据。它不是 T0.11 的交付——`red-green.md` 仍为 T0.11 的冻结交付（其记录的 `grep -c "exit"` = 25 等实测值**未**因本次修复而改动）。
>
> **触发**：2026-10-26 执行 T1.B01-EN 时，子代理上报异常、父代理独立复核：`--self-test` 为 **18/24 exit 1**。
> **事实基准**：T0.2 落地时（commit `3f4e022`，计划 §285-290 与 §1155 记录）为 **24/24 exit 0** ⇒ 属**回归**。
> **裁决**：用户裁决 **A. 立即修复（独立 commit，不并入 W1 收尾加固）**。

## 1. 回归定位 — 规则没坏，坏的是自检夹具

失败的 6 条断言全部是「**断言的锚点行已被 W0 修好 ⇒ 规则不再触发**」：

| # | 失败断言 | 锚点 | 锚点行现状 |
|---|---------|------|-----------|
| 1 | `[names] malformed: 6-column row (missing category/status/source) -> FAIL — got PASS with []` | `concepts.tsv:3316` | W0（`08a2e98`）修好 → 现为 **8 列** |
| 2 | 同上 → `rule concept_cols@terms/registry/concepts.tsv:3316 — fired=[]` | 同上 | 同上 |
| 3 | `[names] malformed: left-shifted row (zh slot holds the English name) -> FAIL — got PASS with []` | `concepts.tsv:3171` | W0 修好 → zh 现为 `能源安全`（含 CJK） |
| 4 | 同上 → `rule names_zh_no_cjk@terms/registry/concepts.tsv:3171 — fired=[]` | 同上 | 同上 |
| 5 | `[definitions] malformed: boilerplate + 指“en” + non-whitelisted source -> rule def_boilerplate_mark@terms/registry/definitions.tsv:5838` | `definitions.tsv:5838` | W0（T0.7a/T0.7b）修好 48 行 `指“en”` |
| 6 | 同上 → `rule def_lang_placeholder@terms/registry/definitions.tsv:5838` | 同上 | 同上 |

同一时刻的语料实测（证明「锚点目标已不存在」，而非「规则被放宽」）：

```console
$ .venv/bin/python - <<'EOF'
import csv
from pathlib import Path
c=[l for l in Path('terms/registry/concepts.tsv').read_text(encoding='utf-8').splitlines() if l and not l.startswith('#')]
print('concepts 非 8 列行数 =', sum(1 for l in c if len(l.split('\t'))!=8))
d=[l for l in Path('terms/registry/definitions.tsv').read_text(encoding='utf-8').splitlines() if l and not l.startswith('#')]
print('definitions 含 指“en” 行数 =', sum(1 for l in d if '指“en”' in l))
EOF
concepts 非 8 列行数 = 0
definitions 含 指“en” 行数 = 0
```

规则本身的有效性由 W1 **每批**的仓外变异法独立复证（`--repo-root` 指向副本，未变异对照 exit 0），例如 T1.B01-EN：
`def_boilerplate_regex`（复原套话）／`def_len_en`（截断到 10 字符）／`def_source_unknown`（写 `internal:dict-improvements`）→ 三者均 **exit 1**。

## 2. 修复方案 — 在临时副本中「就地重建」历史缺陷

**为什么不是改断言**：改了断言或删断言＝削弱自检覆盖（与「绝不为让测试通过而削弱门禁」冲突）。**为什么不是改阈值**：阈值与规则无关，6 条失败里 4 条是「规则未触发」而非「阈值不达」。

**采用的方案**：让那 3 个样本**继续是真实语料行**——把 3 处历史缺陷在**临时副本**中就地重建，**行数不变** ⇒ **24 条断言与全部 `file:line` 锚点逐字保持不变**，规则**一条不改、不加、不减**。

`scripts/registry_batch_verify.py` 的改动面（`git diff --numstat` = `99/14`，仅此一个文件）：

- 新增 `SELF_TEST_RESTORED_CASES: frozenset[int] = frozenset({0, 1, 3})`（指向 `SELF_TEST_CASES` 中的下标，附行内注释点名各 case）
- 新增 `_build_restored_defect_corpus(real_root, dest) -> Corpus`：把 `terms/registry/{concepts,definitions}.tsv` 与 `terms/allowlist_{en,zh}.txt` 复制到 `dest`，并在副本内重建：
  1. `poloidal-field-power-supply` → `fields[:6]`（丢 `category`/`status`/`source`，成 6 列）
  2. `energy-security` → `fields[COL_ZH] = fields[COL_EN]`（左移：zh 槽装英文名）
  3. `adjoint-flux` 的 zh 行 → `聚变/核工程术语，指“en”这一技术概念。`（低信息模板 + 语言标签泄漏）
- `run_self_test`：这 3 个下标改用副本（`sample = restored if index in SELF_TEST_RESTORED_CASES else corpus`），其余 5 个仍跑真实语料；副本目录由 `tempfile.mkdtemp` 建、`finally` 中 `shutil.rmtree`
- **只写 `dest`，绝不写 `real_root`**（仓库文件零触碰）
- 行切分用 `read_text().split("\n")` / `"\n".join(...)`，**不用** `splitlines()`——后者还会在 `\x0b` / `\x0c` / `\u2028` / `\u2029` 处切分，会移动行号、破坏锚点

## 3. RED → GREEN

| | 断言 | exit |
|---|---|---|
| **RED**（修复前 HEAD） | `self-test: 18/24 assertions passed` | **1** |
| **GREEN**（修复后 HEAD） | `self-test: 24/24 assertions passed` / `self-test: OK` | **0** |

```console
$ .venv/bin/python scripts/registry_batch_verify.py --self-test | tail -1
self-test: OK
$ echo $?
0
```

## 4. 能失败证明（5 个变体：脚本副本 + `--repo-root <真实仓库>`，零触碰仓内文件）

`m5` 是**本次修复自身的承重证明**：把 `SELF_TEST_RESTORED_CASES` 清空（禁用重建副本）后**恰好回到修复前那 6 条失败** ⇒ 变绿是「夹具重锚」带来的，**不是**规则被削弱的副作用。

| 变体 | 变异 | 实测 | 语义 |
|------|------|------|------|
| `m1_boilerplate_regex` | `BOILERPLATE_EN_RE` 前置 `(?!)`（永不匹配） | `22/24`，**exit 1**（2 条失败） | 规则回退 ⇒ 自检必红 |
| `m2_concept_cols` | `concept_cols` 两处守卫放宽为 `… and len(fields) > N_CONCEPT_COLS`（6 列被放过） | `22/24`，**exit 1**（2 条失败） | 同上 |
| `m3_lang_placeholder` | `LANG_PLACEHOLDER_RE` 改为 `(?!)`（永不匹配） | `23/24`，**exit 1**（1 条失败） | 同上 |
| `m4_control` | **不修改** | `24/24`，**exit 0** | 对照：副本机制本身不产生假红 |
| `m5_no_restore` | `SELF_TEST_RESTORED_CASES = frozenset()`（禁用重建副本） | `18/24`，**exit 1**（6 条失败，与修复前**逐条一致**） | **夹具承重** ⇒ 本次修复不可被「空操作」替代 |

`m5` 的 6 条失败摘要（与 §1 表格逐条对应）：

```text
FAIL  [names] malformed: 6-column row (missing category/status/source) -> FAIL — got PASS with []
FAIL  [names] malformed: 6-column row (missing category/status/source) -> rule concept_cols@terms/registry/concepts.tsv:3316 — fired=[]
FAIL  [names] malformed: left-shifted row (zh slot holds the English name) -> FAIL — got PASS with []
FAIL  [names] malformed: left-shifted row (zh slot holds the English name) -> rule names_zh_no_cjk@terms/registry/concepts.tsv:3171 — fired=[]
FAIL  [definitions] malformed: boilerplate + 指“en” + non-whitelisted source -> rule def_boilerplate_mark@terms/registry/definitions.tsv:5838 — fired=[…]
FAIL  [definitions] malformed: boilerplate + 指“en” + non-whitelisted source -> rule def_lang_placeholder@terms/registry/definitions.tsv:5838 — fired=[…]
```

> 反例锚定（本次修复的「若失效则应看到什么」）：若将来有人把 `SELF_TEST_RESTORED_CASES` 清空、或把 `_build_restored_defect_corpus` 改成不重建缺陷，则 `--self-test` **必须**回到 `18/24 exit 1`（即上表 `m5`）；若它仍显示 `24/24`，说明断言本身已被削弱，本文件判定 **FAIL** 并回溯。

## 5. 复跑清单（第三方逐条可复现）

```console
# 1) GREEN：HEAD 上自检通过
.venv/bin/python scripts/registry_batch_verify.py --self-test | tail -1   # self-test: OK
.venv/bin/python scripts/registry_batch_verify.py --self-test >/dev/null; echo $?   # 0

# 2) 锚点行现为「已修好」形态（证明 §1 的根因）
sed -n '3171p' terms/registry/concepts.tsv | cut -f3      # 能源安全（含 CJK）
sed -n '3316p' terms/registry/concepts.tsv | awk -F'\t' '{print NF}'   # 8
git show HEAD:terms/registry/definitions.tsv | sed -n '5838p' | grep -c '指“en”'   # 0

# 3) 能失败证明（脚本副本 + --repo-root，仓内文件零触碰）—— 见 §4 表，5 个变体
#    核心一条：清空 SELF_TEST_RESTORED_CASES 后必须回到 18/24 exit 1

# 4) 全量门禁
.venv/bin/python -m pytest -q && .venv/bin/python -m pipeline.validate_registry && \
  .venv/bin/ruff format --check . && .venv/bin/ruff check . && \
  .venv/bin/mypy pipeline/ --ignore-missing-imports                     # 全部 exit 0
.venv/bin/python scripts/registry_row_audit.py --audit --expect-clean    # exit 0
```
