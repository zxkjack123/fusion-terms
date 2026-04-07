from __future__ import annotations

import shutil
from pathlib import Path

import pytest

import pipeline.sync_to_fcitx as sync_to_fcitx


main = sync_to_fcitx.main


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


def test_sync_uses_atomic_temp_replace(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    src = tmp_path / "domain_terms.txt"
    src.write_text("NBI\n", encoding="utf-8")

    dst = tmp_path / "fcitx" / "rime" / "wordlists" / "domain_terms.txt"

    copy_targets: list[Path] = []
    replace_calls: list[tuple[Path, Path]] = []
    real_copyfile = shutil.copyfile
    real_replace = sync_to_fcitx.os.replace

    def _copyfile_with_trace(
        src_path: str | Path,
        dst_path: str | Path,
    ) -> str | Path:
        copy_targets.append(Path(dst_path))
        return real_copyfile(src_path, dst_path)

    def _replace_with_trace(
        src_path: str | Path,
        dst_path: str | Path,
    ) -> None:
        replace_calls.append((Path(src_path), Path(dst_path)))
        real_replace(src_path, dst_path)

    monkeypatch.setattr(sync_to_fcitx.shutil, "copyfile", _copyfile_with_trace)
    monkeypatch.setattr(sync_to_fcitx.os, "replace", _replace_with_trace)
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
    assert dst.read_text("utf-8") == "NBI\n"
    assert copy_targets == [dst.with_name(f".{dst.name}.tmp")]
    assert replace_calls == [(dst.with_name(f".{dst.name}.tmp"), dst)]
    assert not dst.with_name(f".{dst.name}.tmp").exists()
