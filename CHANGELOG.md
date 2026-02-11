# Changelog

本项目的变更记录与版本策略。

## 版本策略（CalVer）

- 采用 **CalVer**（日历版本）：`vYYYY.MM.DD`。
- 若同一天需要多次发布：`vYYYY.MM.DD.N`（从 1 开始递增）。
- “发布（release）”的最小动作：
  1) 更新本文件的 *Unreleased* 区块（把条目移动到新版本号下）。
  2) 确保质量门禁全绿：`python -m compileall` + `pytest`。
  3) 打 Git tag：`vYYYY.MM.DD`（或 `vYYYY.MM.DD.N`）。

> 说明：导出产物中的 `schema_version`（例如 `*_build_stats.json`、registry 导出 manifest 等）用于 **数据格式/兼容性**；它与项目的 CalVer tag 不同维度，按需要独立演进。

## Unreleased

### Added

- 术语库扩充：补充 MCNP/FISPACT 及相关核数据/方差缩减/活化清单与停堆剂量率等中英文 token-only 术语。





### Changed


### Fixed

## v2026.02.11

### Added

- v1.1 substitution 导出增强：在 registry 中补齐最小 deprecated 映射种子，使 `artifacts/terminology_substitutions.tsv` 与 `artifacts/vale/terminology_substitute.yml` 的 swap 非空；同时在 `fusion_terms_manifest.json` 的 counts 中增加 substitution 计数字段，便于下游验收。

## v2026.02.10

### Added

- 术语库扩充：补充仿星器相关术语（装置/磁几何/新古典）中英文词条。

## v2026.02.09.1

### Added

- 术语库扩充：补充 p-11B（氢硼 / HB11）聚变相关中英文术语种子。

## v2026.02.09

### Added

- 对外交付（de-ai-fier 接口 v1/v1.1）核心产物：
  - manifest 生成器：`pipeline/generate_manifest.py`（生成 `fusion_terms_manifest.json`，包含 sha256 + counts）。
  - 契约校验器：`pipeline/verify_release_contract.py`（校验 `domain_terms.txt` + manifest sha256 + counts 自洽）。
  - release 打包器：`pipeline/release_pack.py`（生成 `fusion-terms-artifacts-<tag>.tar.gz`，可用于离线门禁接入）。
- registry 强语义 substitution 导出（v1.1）：
  - `pipeline.export_registry --substitutions`：导出 `artifacts/terminology_substitutions.tsv`。
  - `pipeline.export_registry --vale-substitute`：导出 `artifacts/vale/terminology_substitute.yml`。
- 文档：`README.md` 增加 de-ai-fier 接入示例（方式 A 固定 tag 构建 / 方式 B 下载 Release 资产包）。

### Changed

- release 包构建可选纳入 registry 导出产物（query expansions/tag rules/substitutions/Vale YAML），并由 manifest 的 sha256 覆盖校验。

## v2026.02.07

### Added

- 术语库扩充：补齐聚变装置工程体系的关键中文术语，覆盖仪控/联锁/DAQ、辐射监测细分、氚形态与取样、真空子部件、热工水力测量、辐照效应与制造连接工艺等。
  - 默认配置下，`pipeline.build_terms` 生成的 `artifacts/domain_terms.txt` 词条规模提升到 **1066**。

### Changed

- Rime 导入/导出脚本增强：为调用 `rime_import_wordlist.py` 增加参数透传，支持指定 `dict_name`、覆盖 `rime_user_dir`、可选包含非 CJK 词条，以及在 userdb 锁定时禁用自动重启 fcitx。
- 停用词与噪声治理：补充一批在语料中稳定出现的噪声 token（如章节编号、OCR/LaTeX 伪词等），降低候选抽取污染。


## v2026.02.05

### Added

- 构建统计报表：`pipeline.build_terms` 默认写出 `*_build_stats.json`（新增/删除/总数、zh/en 拆分、synonyms 归一化计数）。
- Rime 集成加固：安全导入包装器（dry-run/备份/失败回滚）与 baked dict 生成器（`fusion_terms.dict.yaml`）。
- 审核工具化：review pack（候选增量 diff）与 decisions apply（将审阅决定确定性写入 allow/deny/synonyms）。
- registry 升级：validator + 多消费者导出（Vale accept/reject、query expansions、tag rules）与 IME 兼容回归保障。
- 抽词增强：支持按 glob 排除派生/噪声 Markdown 文件（`config.toml [sources].exclude_globs` + `--exclude-glob`）。

### Changed

- 构建门禁更严格：拒绝 whitespace 词条、不可见/控制字符、以及冲突 synonyms 映射。
- 抽词流水线：增量 cache + delta report；提供 filtered candidates 输出与 stopwords 种子支持。
- 编码策略收紧：对 `terms/`、registry、decisions 等人工维护输入采用 UTF-8 strict（坏编码直接报错）；对外部语料 Markdown 读取在遇到坏字节时用 U+FFFD 替换并发出告警，避免静默丢字节。
- 工作流更可移植：Rime importer 默认路径使用 `~/.local/bin/rime_import_wordlist.py`（不写死用户名/家目录）。

### Fixed

- 抽词文件遍历兼容：`iter_markdown_files()` 不再漏掉 `.MD`（大写扩展名）的 Markdown 文件。
