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
