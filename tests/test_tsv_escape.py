"""Test Q3: TSV export sanitizes tab/newline characters in fields."""

from __future__ import annotations

from pipeline.export_registry import _sanitize_tsv_field


def test_tab_replaced_with_space() -> None:
    assert _sanitize_tsv_field("hello\tworld") == "hello world"


def test_newline_replaced_with_space() -> None:
    assert _sanitize_tsv_field("line1\nline2") == "line1 line2"


def test_carriage_return_replaced() -> None:
    assert _sanitize_tsv_field("a\rb") == "a b"


def test_mixed_control_chars() -> None:
    assert _sanitize_tsv_field("a\tb\nc\rd") == "a b c d"


def test_clean_string_unchanged() -> None:
    assert _sanitize_tsv_field("normal text") == "normal text"


def test_empty_string() -> None:
    assert _sanitize_tsv_field("") == ""
