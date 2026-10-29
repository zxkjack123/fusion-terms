# W3a allowlist 落地独立验收（T3.43A）

- 验收对象：PM T-4973，用户授权的计划外增量；base `161decf`，HEAD `1ed5e94`
- 范围：43 批 `w3_b01…w3_b43`，`allowlist_zh.txt` / `allowlist_en.txt`
- 独立验收代理：`acceptance-verifier`，只读会话 `ses_e784b1b00ffev9xjQVXYF1I6D3`
- 时间：2026-10-29（本会话 `date -Iseconds` 实测 2026-10-29T20:58:01+08:00）
- **Verdict: PARTIAL**；blocking **0**；warnings **4**

## 复核结果

| 检查 | 结果 |
|---|---|
| 43 批 allowlist gate | **43/43 exit 0**；b06/b10/b12 排除 denylist id 后按 19 条验收 |
| 全量可入集合 | **851/851 exit 0**（854 − area/control/diffusion） |
| 反例锚定 | b12 含 `diffusion` 的全量 gate **exit 1**；排除后 **exit 0** |
| denylist 例外 | `区域`/`控制`/`扩散` 确在 denylist，且不在 allowlist_zh；跳过不是绕过 |
| 变更范围 | `allowlist_zh` **855/0**、`allowlist_en` **707/0**；43 个功能 commit 每个只改两张 allowlist 表 |
| 行 discipline | zh 新增 43 节注释 + 812 条词；en 新增 43 节注释 + 664 条 id；新增空行/重复/空白 **0** |
| 全局门禁 | row audit **0**；validate_registry **0**；build_terms **0**，6378 行；pytest **0**，175 tests |
| W3a names 回归 | names gate 854/854 **0**；D2-6 residual **0** |
| coverage | **98.57%**，covered **3032**，uncovered **44**，W3a **0**，W2 **9**，proper_excluded **35**；3032+44=3076 |
| proper names | W3a 新增 0 个 company/organization/facility；35 个 proper_excluded 未泄漏 |

## 质量抽样与非阻塞警告

- 独立抽样 **20 条、20 个不同批次**，命名/词条映射 FAIL **0**；无重复语义映射。
- 新增 812 条中文词中，**3 条单字 + 118 条双字 = 121 条（14.90%）**为 1–2 字词；验收者认为它们均可由对应英文概念支撑，但这是 IME 词库产品口径的剩余裁决，不应由机械门禁替代。
- 23 条属于辐射防护语境中的常见词头（如「吸收」「处理」「管理」「风险」），未判缺陷，但建议由词库维护者后续做使用频率/误召回评估。
- T3.43A 的 `--check-urls` 命名回归只证明 exit 0，不证明 URL（names mode 空转问题已在 W3a acceptance 与 PM 5072 登记）。
- 「逐批 build_terms 行数」不是可从 git 单独重放的历史 provenance，但最终 build 已独立重跑 exit 0 / 6378。

## 判定与后续

allowlist 数据边界、批门禁、反例、覆盖率和回归均通过；没有需要回滚或返工的 blocking defect。综合仍为 **PARTIAL**，因为 121/812 条短词的 IME 产品取舍属于 Type-B 人工口径，不能冒充 PASS。

已知例外：3 个 denylist 阻塞、35 个 proper_excluded、9 个 W2 残余、self-test 19/24 漂移、names-mode `--check-urls` 空转。证据/释义补强由 PM **5072** 承接。
