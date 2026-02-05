from __future__ import annotations

from pathlib import Path

from pipeline.common import iter_markdown_files


def test_iter_markdown_files_includes_uppercase_md(tmp_path: Path) -> None:
    (tmp_path / "a.md").write_text("# a\n", encoding="utf-8")
    (tmp_path / "b.MD").write_text("# b\n", encoding="utf-8")
    (tmp_path / "c.markdown").write_text("# c\n", encoding="utf-8")
    (tmp_path / "not_md.txt").write_text("no\n", encoding="utf-8")

    files1 = list(iter_markdown_files(tmp_path))
    files2 = list(iter_markdown_files(tmp_path))

    assert files1 == files2  # deterministic ordering

    names = {p.name for p in files1}
    assert "a.md" in names
    assert "b.MD" in names
    assert "c.markdown" not in names
    assert "not_md.txt" not in names
