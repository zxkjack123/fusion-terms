from __future__ import annotations

from pathlib import Path

import pytest

from pipeline.sync_to_fcitx import main


def test_sync_copies_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    src = tmp_path / "domain_terms.txt"
    src.write_text("ITER\n托卡马克\n", encoding="utf-8")

    dst = tmp_path / "fcitx" / "rime" / "wordlists" / "domain_terms.txt"

    monkeypatch.setattr(
        "sys.argv",
        [
            "sync_to_fcitx",
            "--input",
            str(src),
            "--dest",
            str(dst),
        ],
    )

    main()

    assert dst.exists()
    assert dst.read_text("utf-8") == "ITER\n托卡马克\n"


def test_sync_fails_on_missing_input(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    src = tmp_path / "missing.txt"
    dst = tmp_path / "fcitx" / "rime" / "wordlists" / "domain_terms.txt"

    monkeypatch.setattr(
        "sys.argv",
        [
            "sync_to_fcitx",
            "--input",
            str(src),
            "--dest",
            str(dst),
        ],
    )

    with pytest.raises(SystemExit, match="input not found"):
        main()


def test_sync_creates_parent_dirs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    src = tmp_path / "domain_terms.txt"
    src.write_text("ECRH\n", encoding="utf-8")

    dst = tmp_path / "a" / "b" / "c" / "domain_terms.txt"

    monkeypatch.setattr(
        "sys.argv",
        [
            "sync_to_fcitx",
            "--input",
            str(src),
            "--dest",
            str(dst),
        ],
    )

    assert not dst.parent.exists()
    main()

    assert dst.parent.exists()
    assert dst.read_text("utf-8") == "ECRH\n"
