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


### Changed


### Fixed

## v2026.03.16.1

### Added

- 术语纠错规则大幅扩充：新增 60+ deprecated/forbidden 别名，驱动 Vale substitution 规则（2 → 68 条）。
  - 英文常见拼写错误：tokomak, stellerator, bremstrahlung, disrution, Langmuire, trittium 等
  - 英文风格规范：H mode → H-mode, magneto-hydrodynamics → magnetohydrodynamics, scrapeoff → scrape-off 等
  - 中文非规范用词：等离子→等离子体, 电浆→等离子体, 超导磁铁→超导磁体, 中性束→中性粒子束注入, 边界局域模→边缘局域模 等
  - ITER 全称拼写错误检测（Research→Reactor, Internation→International）
- de-ai-fier 已同步更新：`fusion_terms_substitute.yml` 包含 68 条 swap 规则。

## v2026.03.16

### Added

- 术语库大规模扩充（32 → 455 concepts, 197 → 1408 aliases）：
  - 等离子体物理（磁约束基础、等离子体不稳定性、输运与湍流）
  - 等离子体—壁相互作用（溅射、再沉积、杂质输运、偏滤器物理）
  - 等离子体诊断（Thomson散射、ECE、干涉仪、Langmuir探针等）
  - 超导磁体（CICC、失超、HTS/LTS、磁体系统）
  - 仿星器 / 反场箍缩 / 场反位形 / 惯性约束聚变
  - p-B11 / 氢硼聚变（ENN 新奥装置、FRC 技术）
  - 聚变工程系统（真空/结构、氚系统、包层材料、冷却剂、中子学、主要装置 18 台）
  - 等离子体控制与运行（磁控/加热/粒子/位形控制）
  - 理论与模拟（MHD、漂移动理学、蒙特卡罗方法等）
  - 模拟工具与核数据（54 codes: ITER codes, CFD, MHD, PIC, 中子学, 活化, 停堆剂量率）
  - 数值方法（有限元/体/差分、自适应网格、并行计算等 15 条）
  - 聚变经济与路线图（FPP, COE, TRL, LCOE, Q, Qeng 等 20 条）
  - 聚变安全与废物（LOCA, LOFA, LLW/ILW/HLW, DBA 等 15 条）
  - 功率转化与电厂辅助系统（Rankine/Brayton/sCO2 循环, BOP, IHX 等 24 条）
- 术语库校验：455 concepts, 1408 aliases, 455 evidence rows，全部通过 validate_registry。
- 输入法导入：1018 entries 已导入 Rime (rime_ice)。

## v2026.03.02

### Changed

- 纯风格层清理：批量修复 `pipeline/` 与 `tests/` 中的行宽/格式噪音（仅重排与折行，不改变运行行为）。
- 文档更新：`README.md` 中 release 示例 tag 更新为 `v2026.03.02`。

### Fixed

- 解释器一致性：`pipeline.generate_dict_yaml`、`pipeline.rime_export`、`pipeline.rime_import_safe` 的子进程调用统一使用当前解释器（`sys.executable`），避免环境漂移。
- Rime 回滚健壮性：`pipeline.rime_import_safe` 在目标路径类型漂移（文件/目录互换）场景下可稳定恢复备份。
- `pipeline.review_pack` 返回类型收紧为 `TypedDict`，消除 `summary['counts'][...]` 的静态类型噪音。

## v2026.02.11.2

### Added

- 术语库扩充：补充氚燃料循环系统常用缩写及全称（TEP/TES/ISS/WDS/SDS/CPS），中英文 token-only。
- registry：为上述缩写补充 concept/alias 映射（缩写作为 alias，全称作为 preferred），便于下游做规范化建议。
- 术语库扩充：补充安全分析报告缩写及全称（PSAR/FSAR），中英文 token-only；并在 registry 中增加 acronyms→preferred 映射。
- 术语库扩充：补充辐射防护与屏蔽相关术语（ALARA、剂量约束/限值、屏蔽穿透、天空反照、串流、迷宫通道等），并在 registry 中增加规范化映射。
- 术语库扩充：补充辐射防护口径相关中文术语（职业照射、公众照射、有效剂量、当量剂量、导出空气浓度/DAC）并补齐 registry 映射。

## v2026.02.11.1

### Added

- 术语库扩充：补充 MCNP/FISPACT 及相关核数据/方差缩减/活化清单与停堆剂量率等中英文 token-only 术语。

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
