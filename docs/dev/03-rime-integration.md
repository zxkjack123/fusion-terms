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
