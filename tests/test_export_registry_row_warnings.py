from __future__ import annotations

import warnings
from pathlib import Path

from pipeline.export_registry import _iter_alias_rows
from pipeline.export_registry import _iter_concept_rows


def test_iter_alias_rows_warns_on_short_row(tmp_path: Path) -> None:
    p = tmp_path / "aliases.tsv"
    p.write_text(
        "# alias\tconcept_id\tlang\tkind\nok\titer\ten\talias\ntoo_short\titer\n",
        encoding="utf-8",
    )

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        rows = _iter_alias_rows(p)

    assert len(rows) == 1
    assert rows[0]["alias"] == "ok"
    assert any("skipping short alias row" in str(w.message) for w in caught)


def test_iter_concept_rows_warns_on_short_row(tmp_path: Path) -> None:
    p = tmp_path / "concepts.tsv"
    p.write_text(
        "# concept_id\tcategory\niter\tdevice\nonly_id\n",
        encoding="utf-8",
    )

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        rows = _iter_concept_rows(p)

    assert len(rows) == 1
    assert rows[0]["concept_id"] == "iter"
    assert any("skipping short concept row" in str(w.message) for w in caught)
