# Release draft: v2026.02.09 (local, not pushed yet)

日期：2026-02-09  
状态：已发布（tag 已 push；GitHub Release 已创建并上传资产）

本文件用于把一次发布需要的关键信息“钉死”，避免之后临时口径漂移。

## Release identity

- Tag: `v2026.02.09`（annotated tag）
- Target commit: `e2d543d2c2354416213581924cfc1a77182a70ec`
- Commit subject: `docs: add copy/paste GitHub release body for v2026.02.09`

GitHub Release:

- https://github.com/zxkjack123/fusion-terms/releases/tag/v2026.02.09

## Release asset (local build)

- File: `dist/fusion-terms-artifacts-v2026.02.09.tar.gz`
- Size: 18,899 bytes（GitHub Release 记录；本机约 ~19 KiB）
- SHA256:

  `b07f0f60bbd7e59cee7b8022fccfdd4f76cffb98407e1cc8df2fe3cab6897450`

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

发布后校验：

- 已通过 GitHub API 确认 Release 资产存在（asset 名称/size 与预期一致）。
- 由于当前执行环境对 GitHub release asset 下载链接存在网络超时（`curl: (28) Connection timed out`），未能完成“从 GitHub 下载资产 → 解包 → verify”的在线回归。

## GitHub Release body (copy/paste)

### Assets

- `fusion-terms-artifacts-v2026.02.09.tar.gz`
  - SHA256: `b07f0f60bbd7e59cee7b8022fccfdd4f76cffb98407e1cc8df2fe3cab6897450`

### Highlights

- de-ai-fier 接口交付（v1/v1.1）：
  - `domain_terms.txt`（token-only 基础术语表）
  - `fusion_terms_manifest.json`（sha256 + counts + version/commit metadata）
  - substitution 强语义导出（来自 registry(kind)）：
    - `artifacts/terminology_substitutions.tsv`
    - `artifacts/vale/terminology_substitute.yml`
- Release 包可选纳入 registry 导出产物，并由 manifest sha256 覆盖校验。

完整变更记录：见 `CHANGELOG.md` 的 `## v2026.02.09`。

## Manual publish steps (completed)

本节保留为发布记录。

1) Push tag:

- `git push origin v2026.02.09`

2) Create GitHub Release and upload asset:

- Release tag: `v2026.02.09`
- Asset file to upload: `dist/fusion-terms-artifacts-v2026.02.09.tar.gz`
- Suggested release text：优先复制本文件的 “GitHub Release body (copy/paste)”；或使用 `CHANGELOG.md` 中 `## v2026.02.09` 章节

（可选）若使用 GitHub CLI：

- `gh release create v2026.02.09 dist/fusion-terms-artifacts-v2026.02.09.tar.gz --title v2026.02.09 --notes-file <(extract notes from CHANGELOG)`

3) Post-publish sanity (download & verify):

- 下载发布资产到干净目录，解包后运行：
  - `python -m pipeline.verify_release_contract --root .`

## Notes / pitfalls

- `generated_at` 会随每次构建变化，因此 tar.gz 字节级不一定复现；发布时应以“上传的那个 tar.gz 的 sha256”为准。
- 若重新执行 `release_pack` 并打算替换发布资产，务必更新本文件中的 SHA256 与 size（或重新生成一份 release draft）。
