from __future__ import annotations

import warnings

from pipeline.common import clean_markdown_lines
from pipeline.common import read_text_file


def test_clean_markdown_lines_drops_noise_and_truncates_references() -> None:
    md = """
# Title

This mentions tokamak and ITER in normal text.

Figure 1: tokamak schematic of ITER.
图 2：托卡马克装置示意图。

| Device | Heating |
| --- | --- |
| ITER | NBI |

A markdown link to [tokamak](https://example.com/tokamak)
should keep visible text.

Inline math like $q_{95}$ and $\\beta_N$ should keep inner content.

A URL should be removed: https://example.com/a/b/c

```python
# fenced code should be dropped entirely
print("NBI should not come from code fence")
```

$$
E = mc^2
$$

## References
[1] EAST tokamak paper. https://doi.org/10.0000/xyz
"""

    lines = clean_markdown_lines(md)
    joined = "\n".join(lines)

    # Captions removed
    assert "Figure 1" not in joined
    assert "图 2" not in joined

    # Table content kept (flattened), separator removed
    assert "ITER" in joined
    assert "NBI" in joined
    assert "---" not in joined

    # Link visible text preserved, URL removed
    assert "tokamak" in joined
    assert "https://" not in joined

    # Inline math keeps inner content (no $ delimiters)
    assert "q_{95}" in joined
    assert "\\beta_N" in joined
    assert "$q_{95}$" not in joined

    # Code fence and display math dropped
    assert "code fence" not in joined
    assert "E = mc^2" not in joined

    # Truncate at references
    assert "References" not in joined
    assert "EAST" not in joined


def test_read_text_file_truncate_multibyte_boundary_no_decode_warning(
    tmp_path,
) -> None:
    path = tmp_path / "truncated.md"
    raw = "alpha中beta".encode("utf-8")
    # Cut in the middle of a 3-byte UTF-8 char ('中').
    max_bytes = len("alpha".encode("utf-8")) + 2
    path.write_bytes(raw)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", RuntimeWarning)
        text = read_text_file(path, max_bytes=max_bytes)

    messages = [str(w.message) for w in caught]
    assert text == "alpha"
    assert any("file truncated" in msg for msg in messages)
    assert not any("UTF-8 decode error" in msg for msg in messages)


def test_read_text_file_invalid_utf8_still_warns(tmp_path) -> None:
    path = tmp_path / "invalid.md"
    path.write_bytes(b"abc\xffdef")

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", RuntimeWarning)
        text = read_text_file(path, max_bytes=100)

    messages = [str(w.message) for w in caught]
    assert "\ufffd" in text
    assert any("UTF-8 decode error" in msg for msg in messages)
