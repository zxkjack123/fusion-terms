from __future__ import annotations

from pipeline.common import clean_markdown_lines


def test_clean_markdown_lines_drops_noise_and_truncates_references() -> None:
    md = """
# Title

This mentions tokamak and ITER in normal text.

Figure 1: tokamak schematic of ITER.
图 2：托卡马克装置示意图。

| Device | Heating |
| --- | --- |
| ITER | NBI |

A markdown link to [tokamak](https://example.com/tokamak) should keep visible text.

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
