# fusion-terms: Rime (雾凇拼音 / rime-ice) integration

## Recommended approach (Option A): import into `rime_ice.userdb`

This repo produces:

- `artifacts/domain_terms.txt` — one term per line
- `artifacts/.rime_import_rime_ice.txt` — import payload (term + pinyin for zh; term + itself for en)

You already have a working importer script:

- `/home/gw/.local/bin/rime_import_wordlist.py`

The flow becomes:

1) Build: sources → allowlist → `domain_terms.txt`
2) Generate import file: `domain_terms.txt` → `.rime_import_rime_ice.txt`
3) Import into Rime: importer updates `rime_ice.userdb` and restarts Fcitx (optional)

### Safe import (backup + rollback)

为了让 Option A 的导入“可回滚、可定位”，仓库提供了一个安全包装器：

- `python -m pipeline.rime_import_safe`

它会：

1) 先生成 import payload（等价于 dry-run）
2) 若你显式指定 `--import`：在导入前做备份（写入 `manifest.json`）
3) 导入失败时自动回滚（不会静默失败）

示例（建议先 dry-run）：

- 只生成 payload（不导入）：
	- `python -m pipeline.rime_import_safe --dry-run`

- 带备份的导入（需要你告诉它要备份哪些关键路径）：
	- `python -m pipeline.rime_import_safe --import --backup-path ~/.local/share/fcitx/rime --backup-path ~/.config/fcitx/rime`

导入完成后会打印 rollback 命令（基于备份 manifest），你也可以手工执行：

- `python -m pipeline.rime_import_safe --rollback <manifest.json>`

> 说明：真实 Rime 环境的关键路径因发行版/Fcitx 版本而异。
> 安全包装器默认不猜测“你要备份什么”，避免误操作；建议你首次使用时把相关目录作为 `--backup-path` 明确指定。

## Keeping your system wordlist in sync

If you use:

- `~/.config/fcitx/rime/wordlists/domain_terms.txt`

You can copy/sync `artifacts/domain_terms.txt` to that location (the repo stays the source of truth).

## When to upgrade to a baked dictionary

Upgrade to Option B (`fusion_terms.dict.yaml`) when:

- your allowlist stabilizes
- you care about consistent ranking independent of userdb
- you want to share the same dictionary with teammates

This repo’s pipeline is designed so that adding a `.dict.yaml` generator later is a small incremental change.

### Generate `fusion_terms.dict.yaml`

仓库已提供生成器：

- `python -m pipeline.generate_dict_yaml`

它会复用现有的 `rime_import_wordlist.py` 来生成 3 列 TSV payload（`text/code/weight`），并包装成 Rime 可直接引用的 `.dict.yaml`。

示例：

- `python -m pipeline.generate_dict_yaml --input artifacts/domain_terms.txt --out-dir artifacts`

输出默认是：

- `artifacts/fusion_terms.dict.yaml`

### Minimal integration notes (conceptual)

把生成的 `fusion_terms.dict.yaml` 放到你的 Rime 配置目录（例如 `~/.config/fcitx/rime/`）后，按你使用的方案接入：

- 方案 1：在 schema 里通过 `import_tables` 引入（常见做法）
- 方案 2：使用 `table_translator` 指向 `fusion_terms`（取决于你当前的 schema 结构）

由于不同发行版 / rime-ice 版本的 schema 结构可能不同，这里不强行给出“唯一正确”的 patch。
建议做法是：先把文件放入目录 → 执行 deploy → 再用固定验收用例集（ITER/EAST/NBI/H-mode/q95/β_N/τ_E/托卡马克 等）做一次手工验证。
