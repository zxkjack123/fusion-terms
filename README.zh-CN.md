# fusion-terms

[English](README.md)

版本化、可复现的 **聚变 / 核 / 等离子体工程**术语数据产品与生成工具链。

它既可以可靠导入 **Rime（雾凇拼音 / rime-ice）** 输入法词库，也为下游场景提供
结构化产物：**聚变自动翻译、双语资料检索、报告术语检查与替换、知识图谱构建、
OCR 提取内容质量检查与纠错**。

## 数据产品理念

本仓库把"术语"当作**数据产品**管理，全链路版本化、可复现、可审计：

1. **sources（外部语料）** → Markdown 语料（如 pdf2md 输出）
2. **candidates（候选词）** → 带频次与上下文的候选术语（发现用，不直接入库）
3. **review（人工审定）** → allowlist / denylist / synonyms，人是最终裁决者
4. **artifacts（生成产物）** → 词表、双语字典、替换规则、Registry 导出等

每个术语都可追溯到其来源与审定决定。

## 六大应用场景

### 1. 聚变自动翻译

- `artifacts/translation_dict.json` — 中英双向翻译字典，含 `zh2en` / `en2zh`
  两个方向，短键单独归入 `en2zh_short` 以避免歧义（见 `config.toml` 的
  `[export].min_en_key_len`）。
- `artifacts/terminology_substitutions.tsv` — 强语义替换对（
  `alias / preferred / status / lang / note`），其中 `status=forbidden`
  条目用于**纠错**：把常见误译强制替换回规范写法
  （例如 `ASDEX升级 → ASDEX Upgrade`）。

### 2. 双语资料检索

- `artifacts/query_expansions.json` — 查询扩展表，由 `concepts`（概念索引）与
  `alias_index`（别名索引）构成，支持**中文 ↔ 英文双向扩展**：用中文查询时自动
  带出英文别名，反之亦然。
- 检索到的内容可自动翻译成双语语料，从而同时命中中文与英文资料。

### 3. 输入法词库（Rime / 雾凇拼音）

- `artifacts/domain_terms.txt` — 最终词表，一行一词（中英混合，词内无空格），
  可直接进入 Rime 词库目录。
- 配合仓库内**安全导入**流程（自动备份、支持回滚）导入 Rime 用户词库；详见
  下文「Rime / 雾凇拼音集成」。

### 4. 报告术语检查与替换

- `artifacts/vale/terminology_substitute.yml` — 开箱即用的 Vale 术语检查规则
  （`extends: substitution` 的 swap 映射），可挂入报告/论文写作的 Vale 门禁，
  自动提示不规范术语并给出替换建议。
- 替换对的机器可读来源是 `terminology_substitutions.tsv`，两者由同一 Registry
  导出，保持同源一致。

### 5. 知识图谱构建

`terms/registry/` 下的四张表本身就是**图数据模型**：

| 表 | 图角色 | 字段（表头） |
|---|---|---|
| `concepts.tsv` | 概念节点 | `concept_id, category, preferred_zh, preferred_en, preferred_abbr, status, notes, source` |
| `aliases.tsv` | 别名→概念边 | `alias, concept_id, lang, kind, comment`（`kind`: preferred / alias / deprecated / forbidden） |
| `evidence.tsv` | 概念→证据边 | `concept_id, source, quote, added_by, added_at` |
| `definitions.tsv` | 定义属性 | `concept_id, lang, definition, source` |

- `artifacts/registry_exports.json` — 一站式导出：概念与别名计数、
  `query_expansions`、`tag_rules`、`terminology_substitutions`、
  Vale 接受/拒绝词表等，可直接喂给下游知识图谱或检索系统。
- `artifacts/tag_rules.jsonl` — 概念标签规则（含 `category`、`kind`、`match`），
  可直接用于实体标注/打标流水线。

### 6. OCR 提取质量检查与纠错

- `scripts/` 权威术语表提取：
  - `extract_gbt4960_md.py` — GB/T 4960.9-2013《核科学技术术语》Markdown 提取
  - `extract_iaea_glossary.py` — IAEA Safety Glossary 2018（PDF 版式解析）
  - `fetch_iter_glossary.py` — ITER Fusion Glossary 抓取
  - `ocr_gbt4960.py` — 扫描版 PDF 的 OCR（tesseract，chi_sim+eng）+ 术语对解析
- `scripts/diff_terminology_source.py` — 权威术语表 vs Registry **差异审校**：
  找出新增、缺失与不一致条目，供人工修订。
- `terms/denylist.txt` — 人工审定的**禁用/纠错词条**（噪声、OCR 误识、废弃术语），
  在构建词表时被排除。

## Registry 规模

当前规模（直接统计自 `terms/registry/` 数据行，不含注释/空行；截至
[v2026.08.12](https://github.com/zxkjack123/fusion-terms/tree/v2026.08.12)）：

| 表 | 数据行数 |
|---|---|
| `concepts.tsv` | 3064 |
| `aliases.tsv` | 10232 |
| `evidence.tsv` | 3156 |
| `definitions.tsv` | 6128 |

历史快照
[v2026.04.14.1](https://github.com/zxkjack123/fusion-terms/tree/v2026.04.14.1)
（见 `CHANGELOG.md`）：concepts **2697** / aliases **8373** / evidence rows
**2729** / definitions **1549**。

设计文档：`docs/dev/06-terminology-registry-upgrade.md`；版本历史：`CHANGELOG.md`
（CalVer 版本策略 `vYYYY.MM.DD`）。

## 目录结构

```
fusion-terms/
├── pipeline/     # 生成工具链（提取、构建、导出、发布、校验）
├── terms/        # 人工审定的输入：allowlist/denylist/synonyms + registry
│   └── registry/ # 术语登记册四表（concepts/aliases/evidence/definitions）
├── artifacts/    # 生成产物（词表、字典、替换规则、Registry 导出）
├── sources/      # 外部语料指针（不复制整个语料库）
├── scripts/      # IAEA / ITER / GB/T 4960 术语表提取 + OCR 质量检查
├── docs/dev/     # 架构与设计文档
├── tests/        # 测试与 fixtures 语料
└── config.toml   # 全局配置
```

## 安装

```bash
git clone https://github.com/zxkjack123/fusion-terms.git
cd fusion-terms
pip install -r requirements.txt
```

Python 3.11+ 直接可用（`requirements.txt` 仅含低版本兼容包 `tomli`）。

## 快速开始

### 1) 从 Markdown 语料提取候选术语

提取器读取 `config.toml` 中 `[sources].root` 指向的语料目录（默认为仓库内
fixtures，可修改或通过 CLI 覆盖），输出：

- `artifacts/candidates_zh.tsv` — 中文候选（Han 字符跨度 2–8，含频次与上下文）
- `artifacts/candidates_en.tsv` — 英文/混合候选

编码规范：

- `terms/` 与 `terms/registry/` 下的文件必须为**严格 UTF-8**，流水线快速失败。
- 外部语料可能含坏字节，提取器会告警并以 `U+FFFD` 替换，便于定位上游问题。

> 注意：`candidates_*.tsv` 只是**发现产物**，不会自动进入最终词表。

### 2) 人工审定候选

- 接受的术语 → `terms/allowlist_zh.txt` / `terms/allowlist_en.txt`
- 拒绝的噪声术语 → `terms/denylist.txt`
- （可选）别名归一 → `terms/synonyms.tsv`

只有 `terms/` 下人工审定的清单参与最终构建——**人是最终裁决者**。

### 3) 构建最终词表

- 输出 `artifacts/domain_terms.txt`

可选：同步到本地 Fcitx/Rime 词表路径（默认
`~/.config/fcitx/rime/wordlists/domain_terms.txt`，见 `config.toml`）。

### 4) （可选）生成 Rime 导入文件并导入

- 生成 `artifacts/.rime_import_rime_ice.txt`；
- 导入用户词库优先使用**安全流程**（自动备份、支持回滚），见下节。

## Rime / 雾凇拼音集成

安全导入/导出支持常用的透传选项：

- 选择目标词典名（默认 `rime_ice`）
- 覆盖 Rime 用户目录（如 `~/.config/fcitx/rime`）
- 可选包含非 CJK 词条
- 用户词库被锁定时可选禁用 fcitx 自动重启

> 导入负载文件（`artifacts/.rime_import_*.txt`）、备份清单
> （`artifacts/rime_backups/`）与 `*.userdb/` 目录是**本机状态**，不应提交。
> 本仓库是**唯一事实源**，不要以 `*.userdb` 为规范词库。

## 下游消费与发布契约

本仓库同时以**版本化、可验证的术语数据产品**形式被下游工具链消费
（例如术语检查/去 AI 化工具 de-ai-fier 的发布契约）。

- 契约（文件含义）：`docs/dev/07-de-ai-fier-interface-contract.md`
- 执行计划（如何产出）：`docs/dev/08-de-ai-fier-interface-execution-plan.md`

设计原则：集成/构建阶段可以运行 Python、拉取 tag 或 release 资产；
**运行期质量门禁必须离线**，只读本地文件。

### 推荐消费的产物

基础（v1）：

- `domain_terms.txt` — 纯词条词表（一行一词，词内无空白）
- `fusion_terms_manifest.json` — sha256 + 计数 + 版本/提交元数据

强烈推荐（v1.1）：

- `artifacts/terminology_substitutions.tsv` — 由 Registry `kind` 导出的强语义替换对
- `artifacts/vale/terminology_substitute.yml` — Vale 即用的替换规则层

### 方式 A：固定 tag 本地构建（确定性）

在集成/构建流水线中固定 tag，构建自包含的发布根目录（或 tarball），
生成并校验 manifest。

```bash
TAG=v2026.08.12

git clone https://github.com/zxkjack123/fusion-terms.git
cd fusion-terms
git checkout "$TAG"

python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

# 构建发布根目录 + tar.gz（含 v1.1 替换规则导出）
python3 -m pipeline.release_pack \
	--tag "$TAG" \
	--include-registry-exports \
	--substitutions \
	--vale-substitute

# （可选）对 release_pack 打印的 staged 目录再次校验
python3 -m pipeline.verify_release_contract --root "dist/stage/$TAG"
```

此后下游项目把所需文件复制进自己的仓库/运行镜像，运行期校验保持离线。

### 方式 B：下载 release 资产并验证

不想运行构建流水线时，直接下载本仓库发布的 release tarball 并本地验证。

```bash
TAG=v2026.03.29
ASSET="fusion-terms-artifacts-${TAG}.tar.gz"
URL="https://github.com/zxkjack123/fusion-terms/releases/download/${TAG}/${ASSET}"

mkdir -p third_party/fusion-terms/${TAG}
cd third_party/fusion-terms/${TAG}

curl -L -o "$ASSET" "$URL"
tar -xzf "$ASSET"

# 校验契约（需要 verifier 代码；可 vendor 或从固定 tag 运行）
python3 -m pipeline.verify_release_contract --root .
```

注：release tarball 目前发布至 `v2026.03.29`；更高版本（截至 `v2026.08.12`）
仅有 git tag。需要最新数据请优先使用方式 A。

## 开发与贡献

欢迎贡献术语与代码。开发环境、Registry 贡献顺序、提交约定与 PR 检查清单见
[CONTRIBUTING.md](CONTRIBUTING.md)。

核心流程一览：

- 提取候选（`pipeline.extract_candidates`）
- 审定 allow/deny/synonyms（`terms/`）
- 构建词表（`pipeline.build_terms`）
- 可选生成/导入 Rime 产物（`pipeline.rime_import_safe`）
- 发布打包与校验（`pipeline.release_pack` + `pipeline.verify_release_contract`）

Registry 变更必须先运行 `python3 -m pipeline.validate_registry` 通过校验。

## License

本项目基于 [MIT License](LICENSE) 开源（Copyright (c) 2026 Xiaokang Zhang）。
你可以自由使用、修改、分发本项目，包括用于商业用途，前提是保留
原始版权声明与许可文本。

## 附注

- 提取策略**先高精度、后扩召回**，扩展设计见 `docs/dev/`。
- 若你的 pdf2md 流水线生成派生 Markdown（`*.qa_report.md` / `*.autofix.md` 等），
  可通过 `config.toml`（`[sources].exclude_globs`）或 CLI
  `--exclude-glob` 排除。
