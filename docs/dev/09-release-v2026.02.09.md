# Release draft: v2026.02.09 (local, not pushed yet)

日期：2026-02-09  
状态：本地准备完成（已产出 tar.gz + 已验收；尚未 push tag / 尚未创建 GitHub Release）

本文件用于把一次发布需要的关键信息“钉死”，避免之后临时口径漂移。

## Release identity

- Tag: `v2026.02.09`（annotated tag, local）
- Target commit: `c09df47052a9c8a45a9e5d6230535b8262bd8663`
- Commit subject: `chore: prep v2026.02.09 release (notes + tag checklist)`

## Release asset (local build)

- File: `dist/fusion-terms-artifacts-v2026.02.09.tar.gz`
- Size: ~19 KiB（本机生成）
- SHA256:

  `67e392c914308d877b3479200333327d9d29614250e53bffdaaa779a3f45d176`

### Asset contents (paths relative to release root)

- `domain_terms.txt`
- `fusion_terms_manifest.json`
- `domain_terms_build_stats.json`
- `terms/allowlist_zh.txt`
- `terms/allowlist_en.txt`
- `terms/denylist.txt`
- `terms/synonyms.tsv`
- `artifacts/registry_exports.json`
- `artifacts/terminology_substitutions.tsv`
- `artifacts/vale/terminology_substitute.yml`
- `artifacts/vale/accept.txt`
- `artifacts/vale/reject.txt`

## Acceptance checks performed

- 全量门禁：`python -m compileall -q pipeline` + `pytest -q`（全绿）
- Release 资产验收：
  - `pipeline.release_pack` 生成 staging + tar.gz
  - 解包 tar.gz 后，执行 `pipeline.verify_release_contract --root <extracted_root>` 通过（离线只读本地文件）

## Manual publish steps (intentionally NOT executed here)

> 注意：按项目约束，本阶段允许联网；但当前工作约定是“可 commit、不可 push”。因此以下步骤仅作为发布脚本/清单。

1) Push tag:

- `git push origin v2026.02.09`

2) Create GitHub Release and upload asset:

- Release tag: `v2026.02.09`
- Asset file to upload: `dist/fusion-terms-artifacts-v2026.02.09.tar.gz`
- Suggested release text来源：`CHANGELOG.md` 中 `## v2026.02.09` 章节

（可选）若使用 GitHub CLI：

- `gh release create v2026.02.09 dist/fusion-terms-artifacts-v2026.02.09.tar.gz --title v2026.02.09 --notes-file <(extract notes from CHANGELOG)`

3) Post-publish sanity (download & verify):

- 下载发布资产到干净目录，解包后运行：
  - `python -m pipeline.verify_release_contract --root .`

## Notes / pitfalls

- `generated_at` 会随每次构建变化，因此 tar.gz 字节级不一定复现；发布时应以“上传的那个 tar.gz 的 sha256”为准。
- 若重新执行 `release_pack` 并打算替换发布资产，务必更新本文件中的 SHA256 与 size（或重新生成一份 release draft）。
