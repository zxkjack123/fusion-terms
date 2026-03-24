# fusion-terms → de-ai-fier：接口契约（v1 / v1.1）

日期：2026-02-08
状态：草案（待 fusion-terms 与 de-ai-fier 双方确认）

> 本文件用于“定稿第一版接口契约”，明确 fusion-terms 对外发布的术语数据产品在 **文件清单、语义、格式、确定性、校验方式**上的约束。
>
> 设计原则：
> - **构建阶段**允许联网/跑 Python/拉取 tag 或下载 Release 资产；
> - **运行阶段**（de-ai-fier 门禁/质检执行时）只读本地文件，避免公网依赖；
> - `domain_terms.txt` 作为 **token-only** 基础词表；“短语级术语”走 Vale/registry 导出物。

## 0. 术语与约定

- **tag**：fusion-terms 仓库使用 CalVer tag（例如 `v2026.02.07`）。
- **commit**：tag 对应的 git commit SHA（40 hex）。
- **token-only**：术语条目不允许包含任何 whitespace 字符（空格、TAB 等）。
- **canonicalization**：alias → preferred 的归一化映射（不自动表示 deprecated/forbidden）。
- **registry(kind)**：结构化 registry 中对别名状态的分类（如 `preferred|alias|deprecated|forbidden`）。

示例（仅用于说明，不是硬编码）：
- `v2026.02.07` → `30a10e762471527752dfb8d6e23c4795a271a564`

## 1. 版本范围

- v1：门禁必需（MVP）
- v1.1：强烈建议（增加 substitution 强语义导出；synonyms 仍保持 canonicalization）
- 可选增强：registry export（query expansion / tag rules / Vale accept/reject）

## 2. 交付方式（二选一，推荐 Release 资产）

### 2.1 方式 A：固定 tag + 确定性构建（推荐默认）

- de-ai-fier 在构建/集成阶段：
  1) 拉取 fusion-terms 指定 tag；
  2) 运行确定性构建入口生成产物；
  3) 校验 manifest/sha256；
  4) 同步到 de-ai-fier 自身规则文件中。

### 2.2 方式 B：下载 Release 资产（强烈建议提供）

- fusion-terms 发布 `fusion-terms-artifacts-<tag>.tar.gz`，内含本契约规定的文件。
- de-ai-fier 在构建/集成阶段下载并校验即可，无需运行 fusion-terms 的构建链路。

## 3. v1（门禁必需）文件清单与契约

### 3.1 `domain_terms.txt`

用途：
- 基础 token 词表（白名单/术语保护/分词补充等）。

格式契约（必须）：
- 编码：UTF-8
- 结构：一行一个 term
- 处理：每行 `strip()` 后为有效 token
- **禁止 whitespace（token-only）**：term 内不得出现任何空白字符
- 去重：输出中无重复项
- 禁止控制/不可见字符（例如 BOM、零宽空格等）；违规应 fail-fast
- 排序稳定：
  - `zh-first / en-second` 分组
  - 组内字典序稳定

非目标（明确不承载）：
- 不承载短语级术语（含空格的 multi-word phrase）。若需要短语，请使用 v1.1/增强接口中的 `artifacts/vale/accept.txt`。

### 3.2 `fusion_terms_manifest.json`（或同等 manifest 文件）

用途：
- 制品校验（sha256）
- 镜像/缓存一致性校验
- 与 tag/commit 的可追溯绑定

字段契约（必须包含）：
- `version`：字符串，等于发布 tag（例如 `v2026.02.07`）
- `commit`：字符串，40 位 SHA
- `generated_at`：UTC ISO8601（例如 `2026-02-08T03:21:00Z`）
- `counts`：对象，至少包含：
  - `total`（int）
  - `zh`（int，可选但建议）
  - `en`（int，可选但建议）
  - `abbr`（int，可选）
- `sha256`：对象，键为文件名（相对 Release 根目录），值为 64 hex
  - v1 最少覆盖：`domain_terms.txt`
  - 若 Release 包含其他文件（allowlist/synonyms/substitution/vale），建议一并覆盖

示例（结构示意）：

```json
{
  "version": "v2026.02.07",
  "commit": "30a10e762471527752dfb8d6e23c4795a271a564",
  "generated_at": "2026-02-08T03:21:00Z",
  "counts": {"total": 1234, "zh": 800, "en": 420, "abbr": 14},
  "sha256": {
    "domain_terms.txt": "<64-hex>",
    "terms/allowlist_zh.txt": "<64-hex>"
  }
}
```

兼容性说明：
- 若已存在 `domain_terms_build_stats.json`（含 added/removed/schema_version 等），可继续保留；manifest 更偏“制品校验/镜像缓存”，build_stats 更偏“审计差分”。

### 3.3 确定性构建入口

- fusion-terms 提供稳定 CLI：
  - `python -m pipeline.build_terms --config config.toml`
- 确定性要求：同一 tag + 同一输入配置 → 同一输出（文件内容字节级一致，含排序）。

## 4. v1.1（强烈建议）文件清单与契约

### 4.1 `terms/synonyms.tsv`（canonicalization）

语义（必须明确）：
- alias → preferred 的归一化映射（canonicalization）。
- **不自动表达 deprecated/forbidden 强约束**。

格式契约（建议）：
- UTF-8
- TSV（制表符分隔）
- 忽略空行与以 `#` 开头的注释行
- 至少两列：
  1) `alias`
  2) `preferred`
- 可选第三列 `lang`（例如 `zh|en|any`），即使 build pipeline 当前忽略也允许保留

校验建议（should）：
- alias 与 preferred 均非空
- 不出现 alias==preferred
- 不出现循环映射（A→B→A）

### 4.2 substitution 专用导出（强语义来自 registry）

目的：让 de-ai-fier 能把 deprecated/forbidden 写法转成 Vale substitution / reject，而不污染 `terms/synonyms.tsv` 的单一语义。

建议同时提供两个层次（强烈建议，二者可同时提供）：

1) 机器友好（canonical）：`artifacts/terminology_substitutions.tsv`
- TSV 列建议为：
  1) `alias`
  2) `preferred`
  3) `status`：`deprecated|forbidden`（必须来自 registry(kind)）
  4) `lang`：`zh|en|any`（可选）
  5) `note`：可选

2) Vale 直接可用（便利层）：`artifacts/vale/terminology_substitute.yml`
- Vale substitution 规则文件，至少包含 `swap:`，并能表达 `alias → preferred`
- de-ai-fier 默认消费策略建议：
  - `deprecated`：level=suggestion 或 warning（可配置）
  - `forbidden`：建议同时进入 reject 或升级为更强提示（由 de-ai-fier 决定）

## 5. 可选增强接口（May）

如 fusion-terms 已具备 registry export 基础设施，可额外提供：

- `artifacts/vale/accept.txt`：Vale 术语 accept（可包含短语/空格）
- `artifacts/vale/reject.txt`：Vale 术语 reject
- `artifacts/query_expansions.json`：建议包含 `schema_version`，并按 include/deprecated/forbidden 分桶
- `artifacts/tag_rules.jsonl`：建议包含 schema 版本字段

> 说明：这些增强接口不进入 de-ai-fier 门禁必需链路，但可显著提升“术语一致性提示 / 检索扩展 / 打标规则”的可维护性。

## 6. Release 资产目录结构建议

建议 `fusion-terms-artifacts-<tag>.tar.gz` 解压后包含（示例；路径均相对 Release 根目录）：

- `domain_terms.txt`
- `fusion_terms_manifest.json`
- `domain_terms_build_stats.json`（可选）
- `terms/allowlist_zh.txt`（如有）
- `terms/allowlist_en.txt`（如有）
- `terms/synonyms.tsv`（v1.1，如有）
- `artifacts/terminology_substitutions.tsv`（v1.1，如有）
- `artifacts/vale/terminology_substitute.yml`（v1.1，如有）
- `artifacts/vale/accept.txt`（可选增强）
- `artifacts/vale/reject.txt`（可选增强）
- `artifacts/query_expansions.json`（可选增强）
- `artifacts/tag_rules.jsonl`（可选增强）

## 7. 兼容性与演进规则

- 所有结构化文件（JSON/TSV/JSONL/YAML）建议携带 `schema_version` 或在 manifest 中记录版本信息。
- 新增字段应保持向后兼容（旧消费者忽略未知字段）。
- 如需 breaking change，应通过：
  - 新文件名/新路径，或
  - 提升 schema_version 并在 release notes 明确说明。

## 8. 自测/CI 验收清单（建议 fusion-terms 发布前必跑）

- `domain_terms.txt`：
  - 无重复、无空行、无 BOM、无控制字符、行内无前后空白
  - 每行不含 whitespace（token-only）
  - 排序稳定（同输入多次构建一致）
- `fusion_terms_manifest.json`：
  - `version/commit/generated_at/counts` 字段齐全
  - `sha256` 与实际文件一致
- （v1.1）`terms/synonyms.tsv`：
  - alias/preferred 非空；无自映射；无循环
- （v1.1）substitution 导出：
  - status 仅来自 registry(kind) 的 deprecated/forbidden

---

确认方式（建议）：
- fusion-terms 与 de-ai-fier 双方在 issue/PR 下对本文件签字式确认（ACK），并以该版本作为后续联调与 CI 约束基线。
