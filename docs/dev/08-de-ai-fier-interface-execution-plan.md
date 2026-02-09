# fusion-terms → de-ai-fier：接口契约执行计划（v1 / v1.1）

日期：2026-02-08  
状态：执行计划（与接口契约配套；用于指导实现）

本计划用于把接口契约落成可交付的代码与 Release 资产。

- 接口契约基线：`docs/dev/07-de-ai-fier-interface-contract.md`
- 设计约束：
  - **构建阶段**允许联网/跑 Python/拉取 tag 或下载 Release 资产；
  - **运行阶段**（de-ai-fier 门禁/质检执行时）只读本地文件；
  - `domain_terms.txt` 为 **token-only** 基础词表；短语级术语走 `artifacts/vale/accept.txt`。

---

## 里程碑与交付物概览

### v1（门禁必需 / MVP）

- `domain_terms.txt`（已存在，由 `pipeline.build_terms` 生成）
- `fusion_terms_manifest.json`（新增：制品校验/镜像缓存）
-（建议）`fusion-terms-artifacts-<tag>.tar.gz`（新增：Release 资产包）

### v1.1（强烈建议）

- `terms/synonyms.tsv`（已存在：canonicalization；语义不变）
- substitution 专用导出（新增，强语义来自 registry(kind)）：
  - `artifacts/terminology_substitutions.tsv`
  - `artifacts/vale/terminology_substitute.yml`

### 可选增强（May）

- registry export（已有基础设施：`pipeline.export_registry`）：
  - `artifacts/vale/accept.txt`、`artifacts/vale/reject.txt`
  - `artifacts/query_expansions.json`
  - `artifacts/tag_rules.jsonl`

---

## 阶段 0：基线固化与发布边界（目标：1 天内）

### 任务 0.1：固化契约文档为实现基线

- **任务目标**：接口契约成为后续实现与 CI 的判定标准，避免口径漂移。
- **修改内容**：
  - 确保 `docs/dev/07-de-ai-fier-interface-contract.md` 在仓库中可审阅；
  -（可选）在 `README.md` 增加“对外接口契约文档”链接。
- **测试内容**：无。
- **验收要求**：
  - 文档中明确 `domain_terms.txt` token-only、短语走 `artifacts/vale/accept.txt`；
  - 对外沟通以该文档为唯一口径。

### 任务 0.2：确定下一次对外发布版本号与范围

- **任务目标**：为 v1/v1.1 的交付物设定明确的 tag 节点与范围。
- **修改内容**：
  - 在 `CHANGELOG.md` 的 Unreleased 区块预写将新增的交付物：manifest、release 包、substitution 导出；
  - 确定下一 tag（建议：`v2026.02.08`；如当日多次发布则 `v2026.02.08.1`）。
- **测试内容**：无。
- **验收要求**：发布范围在 changelog 中清晰可审阅。

---

## 阶段 1：v1 核心交付（manifest）（目标：1–2 天）

> 目标：补齐 `fusion_terms_manifest.json`，实现制品可校验、可缓存、可追溯。

### 任务 1.1：实现 manifest 生成器（新增脚本）

- **任务目标**：生成满足契约第 3.2 节的 `fusion_terms_manifest.json`。
- **修改内容**（建议实现）：
  - 新增：`pipeline/generate_manifest.py`
  - CLI 建议：
    - `--root <release_root>`：Release 根目录（staging 目录）；
    - `--version <tag>`：例如 `v2026.02.08`；
    - `--commit <sha>`：可显式传入（CI 推荐），否则尝试从 git 获取；
    - `--generated-at <UTC_ISO8601>`：可选（测试/重现用），默认当前 UTC；
    - `--files <path>...`：需要纳入 sha256 的文件相对路径列表（至少 `domain_terms.txt`）。
  - manifest 字段：
    - 必含：`version`、`commit`、`generated_at`、`counts`、`sha256`
    - 建议额外加：`schema_version: 1`
  - counts 计算策略（二选一，建议优先方案 A）：
    - A：读取 `domain_terms_build_stats.json` 的 counts（避免重复口径）；
    - B：直接统计 `domain_terms.txt`，并按“是否包含 CJK”粗分 zh/en。
- **测试内容**：
  - 单测：在临时目录中写入小型 `domain_terms.txt`（及可选 build_stats），运行脚本生成 manifest，断言：
    - JSON 可解析；
    - 字段齐全；
    - sha256 与外部计算一致；
    - `generated_at` 格式为 UTC ISO8601（推荐以 `Z` 结尾）。
- **验收要求**：
  - 在本机、CI 中均可生成一致的 manifest；
  - sha256 校验 100% 通过；
  - 字段缺失或文件不存在时 fail-fast 并给出明确错误。

### 任务 1.2：新增“契约校验器”（可选但强烈建议）

- **任务目标**：发布前一键验证 v1 契约（减少人为漏检）。
- **修改内容**（建议实现）：
  - 新增：`pipeline/verify_release_contract.py`
  - 校验内容：
    - `domain_terms.txt`：无空行、无重复、token-only（无 whitespace）、无控制/不可见字符；
    - `fusion_terms_manifest.json`：字段齐全；sha256 覆盖文件存在且校验通过。
- **测试内容**：
  - 单测：构造含空格/含零宽字符的词条，verify 必须失败；
  - 单测：manifest sha256 故意写错，verify 必须失败。
- **验收要求**：
  - 发布前执行一次 verify 即可得到明确 PASS/FAIL（含原因）。

---

## 阶段 2：交付方式 B（Release 资产包）（目标：1–2 天）

> 目标：生成 `fusion-terms-artifacts-<tag>.tar.gz`，让 de-ai-fier 无需运行本仓库构建也可接入；同时适配离线镜像缓存。

### 任务 2.1：实现 release 打包器（staging → tar.gz）

- **任务目标**：自动生成契约第 6 节建议目录结构的 release 包，并确保 manifest sha256 覆盖关键文件。
- **修改内容**（建议实现）：
  - 新增：`pipeline/release_pack.py`
  - 运行顺序建议（保证一致性）：
    1) 运行 `pipeline.build_terms` → 生成 `artifacts/domain_terms.txt` 与 `artifacts/domain_terms_build_stats.json`
    2) 创建 staging（如 `dist/stage/<tag>/`）并复制文件到 **release 根目录相对路径**：
       - `domain_terms.txt`
       - `domain_terms_build_stats.json`（可选但推荐）
       - `terms/allowlist_zh.txt`、`terms/allowlist_en.txt`、`terms/synonyms.tsv`（若要放入包内）
    3)（可选增强）运行 `pipeline.export_registry` 并复制：
       - `artifacts/vale/accept.txt`、`artifacts/vale/reject.txt` 等
    4) 调用 `pipeline.generate_manifest` 对 staging 内文件计算 sha256，生成 `fusion_terms_manifest.json`
    5) 打包为 `fusion-terms-artifacts-<tag>.tar.gz`
  - 注意：manifest 的 `sha256` key 应使用 **相对 release 根目录** 的路径（例如 `terms/allowlist_zh.txt`）。
- **测试内容**：
  - 集成测试：在临时目录运行 release_pack，得到 tar.gz；解包后运行 verify_contract，必须通过。
- **验收要求**：
  - 包在没有 git、没有本仓库源码的环境解压后仍可完成校验与消费；
  - 内容路径与契约一致。

### 任务 2.2：补充文档与使用示例

- **任务目标**：让对方团队照文档就能集成。
- **修改内容**：
  - 在 `README.md` 补充：
    - “方式 A：固定 tag + 构建”示例
    - “方式 B：下载 release 包 + 校验”示例
    - 指向契约与本执行计划文档链接
- **测试内容**：无。
- **验收要求**：de-ai-fier 维护者可按 README 独立完成接入。

---

## 阶段 3：v1.1（substitution 强语义导出）（目标：2–4 天）

> 目标：保持 `terms/synonyms.tsv` 的单一语义（canonicalization），把 deprecated/forbidden 强语义从 registry(kind) 导出为 substitution 专用产物。

### 任务 3.1：定稿“preferred 选择规则”（先定规则再写代码）

- **任务目标**：确保 substitution 产物语义稳定、可解释。
- **修改内容**（建议规则）：
  - 对每条 `terms/registry/aliases.tsv` 中 `kind in {deprecated, forbidden}` 的 alias：
    - 在同 `concept_id` 下选择 `kind=preferred` 且 `lang` 优先匹配的 preferred；
    - 若无同 lang preferred，则 fallback 为同 concept 的任意 preferred（稳定排序取第一个）；
    - 若 concept 无 preferred，视为 registry 数据不完整 → fail-fast。
- **测试内容**：最小 registry fixture 覆盖：同 lang / 不同 lang fallback / 缺 preferred 报错。
- **验收要求**：同一输入多次导出字节级一致；错误信息可定位到 concept/alias。

### 任务 3.2：导出 `artifacts/terminology_substitutions.tsv`

- **任务目标**：提供机器友好 substitution TSV（alias, preferred, status, lang, note）。
- **修改内容**：
  - 扩展 `pipeline/export_registry.py`：增加 `--substitutions` 选项，写出：
    - `artifacts/terminology_substitutions.tsv`
  - TSV 行建议以注释 header 起始（`# alias\tpreferred\tstatus\tlang\tnote`）。
- **测试内容**：
  - 单测：只导出 deprecated/forbidden；不出现 alias==preferred；排序稳定。
- **验收要求**：de-ai-fier importer 可直接消费该 TSV。

### 任务 3.3：导出 `artifacts/vale/terminology_substitute.yml`

- **任务目标**：提供 Vale 可直接用的 substitution 规则文件（便利层）。
- **修改内容**：
  - 在 `pipeline/export_registry.py` 或新模块生成 YAML：
    - 至少包含 `swap:` 映射 alias→preferred；
    - `deprecated`/`forbidden` 是否分文件或分组由实现决定（保持简单优先）。
  - 注意：Vale substitution YAML 的具体格式需与 de-ai-fier 现有规则约定对齐（先对齐一个最小样例）。
- **测试内容**：
  - 单测：YAML 可被解析（可引入 dev 依赖或做最小语法校验）。
- **验收要求**：de-ai-fier 在 CI 中启用该规则不报格式错误。

---

## 阶段 4：发布与验收（目标：0.5–1 天）

### 任务 4.1：发布前门禁

- **任务目标**：将契约第 8 节的自测项固化为发布前必跑。
- **修改内容**：
  - 在 `CHANGELOG.md` 完成 release 章节；
  -（如有）CI 增加 job：生成 release 包 → verify → 产物上传。
- **测试内容**：
  - `python -m compileall`
  - `pytest`
  - `pipeline.verify_release_contract`（若实现）
- **验收要求**：所有门禁通过后才允许打 tag / 发布 Release。

### 任务 4.2：发布 tag 与 Release 资产

- **任务目标**：形成可下载、可校验、可离线缓存的交付物。
- **修改内容**：
  - 打 tag（例如 `v2026.02.08`）；
  - 发布 GitHub Release，附带 `fusion-terms-artifacts-<tag>.tar.gz`。
- **测试内容**：下载 release 包到干净环境解压校验。
- **验收要求**：de-ai-fier 侧按“方式 B”仅靠包即可完成同步并离线运行门禁。

---

## 进度跟踪 Checklist（建议复制到 issue/PR）

### Milestone A：v1（manifest + release 包）

- [ ] 契约文档 ACK（双方）
- [x] `pipeline/generate_manifest.py` 实现
- [x] manifest 字段齐全（version/commit/generated_at/counts/sha256）
- [x] manifest sha256 至少覆盖 `domain_terms.txt`
- [x] `pipeline/verify_release_contract.py` 实现（可选但强烈建议）
- [x] `pipeline/release_pack.py` 生成 `fusion-terms-artifacts-<tag>.tar.gz`
- [x] 解包后 verify（或手动校验 sha256）100% 通过
- [x] pytest 覆盖 manifest + pack（最小集成测试）
- [x] `README.md` 补充对外接入示例（方式 A / 方式 B）
- [x] 更新 `CHANGELOG.md` 并（本地）打 tag（不 push）
- [x] 准备 Release draft（产物清单 + sha256 + 手工发布步骤）：`docs/dev/09-release-v2026.02.09.md`
- [ ] push tag + 发布 GitHub Release 资产（需人工确认后执行）

### Milestone B：v1.1（substitution 强语义导出）

- [ ] preferred 选择规则定稿（lang 优先 + fallback）
- [x] `artifacts/terminology_substitutions.tsv` 导出
- [x] `artifacts/vale/terminology_substitute.yml` 导出
- [x] pytest 覆盖：仅 deprecated/forbidden、无自映射、排序稳定（TSV/YAML）
- [x] release 包可纳入上述文件并由 manifest 覆盖 sha256（release_pack 开启 registry exports 时）

### Milestone C：增强接口（可选）

- [ ] `artifacts/vale/accept.txt` / `reject.txt`（短语支持）
- [ ] `artifacts/query_expansions.json` / `tag_rules.jsonl`（schema_version 明确）

---

## 实施建议（优先级）

1) 先做 v1：manifest + release_pack（de-ai-fier 立刻能稳定接入）
2) 再做 v1.1：substitution 强语义导出（避免把 synonyms 变成多语义文件）
3) 最后做 May：query expansion / tag rules（增强但不绑死门禁）

---

## 实现注意事项 / 常见坑（强烈建议在实现前阅读）

本节用于把“容易踩坑但不写就会踩”的工程细节显式化，避免出现 release 资产错配、下游校验困难、或 de-ai-fier 集成失败。

### 1) 产物生成位置：尽量“直接生成到 staging”，避免先写 repo 的 `artifacts/` 再复制

- **风险**：如果先写 repo 的 `artifacts/` 再复制到 staging，未来在 CI 并行/多次执行时，可能出现“复制到 staging 的文件不是同一轮生成”的错配（尤其当你把 registry export/substitution 也加入 pack 时）。
- **推荐做法**：在 `release_pack.py` 中显式传 `--out-dir <staging_root>`：
  - `pipeline.build_terms` 已支持 `--out-dir`，可直接把 `domain_terms.txt` 与 `domain_terms_build_stats.json` 写到 staging 根目录。
  - `pipeline.export_registry` 也支持 `--out-dir`，可直接写到 `<staging_root>/artifacts/...`。
- **验收要点**：staging 目录成为“Release 根目录的唯一真值”，manifest 的 sha256 只对 staging 内文件计算。

### 2) `commit` 字段不要强依赖 git：必须支持“无 git 环境”

- **风险**：方式 B（下载 Release 资产）/某些 CI 环境可能没有 `.git/` 或未安装 git，若 manifest 生成脚本硬依赖 `git rev-parse` 会直接失败。
- **推荐做法**：
  - `generate_manifest.py`：优先读取 `--commit` 参数；缺省时再尝试从 git 获取；两者都不可用时给出清晰错误。
  - `verify_release_contract.py`：**不要求 git**，仅做本地文件/sha256 校验。

### 3) `generated_at` 会导致 manifest 不同：这是预期，不应被当作“确定性失败”

- **说明**：同一 tag 多次生成 release 包时，`generated_at` 会变化，因此 manifest 文件字节不一致是正常的。
- **推荐做法**：
  - 在测试中允许通过 `--generated-at` 固定时间戳，便于快照/断言；
  - “确定性”的硬标准应落在：`domain_terms.txt` 内容、以及 sha256 校验能通过。

### 4) tar.gz 的“字节可复现性”不是硬要求，但会影响缓存命中（可选增强）

- **风险**：tar 默认会带文件 mtime/uid/gid，导致同内容也可能打出不同字节的 tar 包；这会降低内部镜像/缓存的命中率。
- **可选增强**：
  - 打包时固定 mtime/uid/gid（例如置 0 或置为 tag 的时间），并按稳定顺序写入文件。
- **验收要点**：即便不追求 tar 字节级可复现，也必须保证“解包后文件内容 + manifest 校验”可复现。

### 5) substitution 的 preferred 选择规则要“可测且可解释”：建议明确排序键

- **风险**：同一 concept 下可能存在多个 preferred（不同 lang/不同写法），若不明确选择规则，会出现导出不稳定或下游争议。
- **推荐规则（可落地且稳定）**：
  1) 同 `concept_id` 下先找与 alias `lang` 匹配的 `kind=preferred`；
  2) 若没有，fallback 为任意 `kind=preferred`；
  3) 多个候选时按稳定键排序并取第一个（建议键：`lang`、`alias` 字典序）。
- **验收要点**：同一 registry 输入，多次导出 substitution TSV/YAML 字节一致。

### 6) Vale substitution YAML 格式必须先对齐“最小可用样例”，并纳入验收

- **风险**：YAML 结构与 Vale 期望不一致时，最常见的失败是“规则不生效/CI 才发现格式错误”。
- **推荐做法**：
  - 在实现前由 de-ai-fier 提供一个最小样例（包含 `swap:` 的有效结构）；
  - 在验收中加入：在 de-ai-fier 仓库里实际跑一次 Vale（或他们 CI）验证格式与效果。

### 7) 把“无 git / 无网络 / 无源码”的验收当成一等公民

- 建议至少做一次“干净环境验收”：只拿 `fusion-terms-artifacts-<tag>.tar.gz` 解包，然后运行 verify（或 de-ai-fier importer）完成全流程。
