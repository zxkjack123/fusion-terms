from __future__ import annotations

from pathlib import Path

import pytest

from pipeline.common import read_text_file


def test_read_text_file_warns_and_replaces_invalid_utf8(tmp_path: Path) -> None:
    p = tmp_path / "bad.md"
    # Invalid UTF-8 bytes (0xFF) embedded.
    p.write_bytes(b"ok\n\xff\nend\n")

    with pytest.warns(RuntimeWarning):
        text = read_text_file(p)

    # Invalid bytes should not be silently dropped; they should become U+FFFD.
    assert "\ufffd" in text
    assert "ok" in text
    assert "end" in text
