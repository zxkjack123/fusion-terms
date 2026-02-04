# 术语审核准则（Review Rules）

> 本文是 `terms/*` 人工审核与规范化的“宪法”。目标不是一次性完美，而是让每次审核都**可重复、可解释、可一致**。
>
> 与输入法策略绑定的关键约束：本项目最终产物 `artifacts/domain_terms.txt` **每行一个 token**，任何包含空白字符（空格/Tab）的词条都会被构建阶段拒绝。

## 1. 总体原则

1) **Repo 为唯一真相**：`terms/allowlist_*.txt`、`terms/denylist.txt`、`terms/synonyms.tsv` 是源数据；输入法 userdb 只是消费端缓存。

2) **宁缺毋滥**：宁可先不收，也不要把明显噪声收进 allowlist（后期清理成本更高）。

3) **一致性优先于“学术严谨”**：术语形式尽量与日常输入一致；必要时用 `synonyms.tsv` 归一化常见变体。

4) **单 token 合同（强约束）**：
   - ✅ 允许：连字符 `-`、斜杠 `/`、点号 `.`, 数字 `0-9`、希腊字母（如 `β`、`τ`）、下划线 `_`（若你决定保留）。
   - ❌ 禁止：任何空白字符（`neutral beam` 这种多词短语）。
   - 多词短语处理：拆分为组成词（如 `neutral`、`beam`、`injection`），或用缩写（如 `NBI`）。

## 2. 英文/混合词条规则（allowlist_en）

### 2.1 大小写

- **缩写**：全大写（`ITER`、`NBI`、`ICRH`）。
- **普通名词**：一般小写（`tokamak`、`stellarator`）。
- **专名**：按领域惯例（如果你更偏好全大写装置名，则保持一致即可）。

### 2.2 连字符、斜杠与标点

- 优先保留领域里高频且更“可读”的形式：
  - `H-mode` / `L-mode`（而不是 `Hmode`）
  - `D-T`（而不是 `DT`）
  - `W/Be`（而不是 `W-Be`）
- 若在语料中存在多种写法：
  - 在 allowlist 收 **preferred** 形式
  - 在 `synonyms.tsv` 把常见 alias 归一到 preferred（但 alias/preferred 两侧都必须是单 token）

### 2.3 复数与派生

- 默认收**最常用**的一个形态即可（例如 `disruption` vs `disruptions`）。
- 如果复数形式明显更常见或更符合输入习惯，可额外收录。

## 3. 中文词条规则（allowlist_zh）

- 优先收**稳定、常用**的中文术语：如 `托卡马克`、`等离子体`。
- 对同义词/异体：
  - 需要统一时，用 `synonyms.tsv`（注意：中文也必须是单 token，不能带空格）
- 避免收过短、泛化词（会干扰输入）：如单字或极泛的常用词。

## 4. 参数/符号类 token（强烈建议优先覆盖）

这类 token 往往是你最关心、且自动抽取最容易漏掉的。

- 建议 preferred：希腊字母形式（如 `β_N`、`τ_E`），并在 synonyms 中把 ASCII 变体归一过去（如 `beta_N → β_N`、`tau_E → τ_E`）。
- `q95` / `q_95`：二选一做 preferred，并在 synonyms 归一（当前建议 preferred 为 `q95`）。

## 5. denylist 的使用边界

`terms/denylist.txt` 是 **exact-match** 过滤（不是正则）。建议只放：

- 文档模板噪声：`Figure`、`Table`、`References`、`doi` 等
- Bib 噪声：`et`、`al`（若在候选中频繁出现）

不要把“可能是术语但你不喜欢”的词直接放 denylist；更推荐先不加 allowlist，或在 review pack 阶段再讨论。

## 6. synonyms.tsv 规范

- 格式：`alias\tpreferred\tlang(optional)`
- **第三列 `lang` 当前仅作为注释/保留字段**：构建流程目前只读取前两列（alias/preferred），不会按语言做不同处理。不要依赖 `lang` 生效。
- **alias 和 preferred 都必须是单 token（无空白）**。
- **同一个 alias 不能映射到多个 preferred**：若出现冲突（同 alias 不同 preferred），构建会失败（避免“后者覆盖前者”的隐蔽行为）。
- 只做“形式归一”，不做“扩写短语”：
  - ✅ `DT → D-T`
  - ✅ `Hmode → H-mode`
  - ❌ `neutral beam → NBI`（带空格，且属于短语层面的改写）

## 7. 审核时的最小检查清单（每次改 terms 都建议过一遍）

- [ ] 新增的每个英文词条都不含空格/Tab（否则构建会失败）
- [ ] `synonyms.tsv` 中 alias/preferred 都不含空格/Tab
- [ ] 重要类别都有覆盖：装置/缩写/材料/参数（q95、β_N、τ_E 等）
- [ ] 不确定的术语先不收，留到下一轮（避免污染）
