"""Test Q2: YAML dict name is always quoted to prevent malformed YAML."""

from __future__ import annotations

from pipeline.generate_dict_yaml import _render_header


def test_name_with_colon_is_quoted() -> None:
    header = _render_header(name="test:dict", version="1.0")
    assert 'name: "test:dict"' in header


def test_simple_name_is_quoted() -> None:
    header = _render_header(name="rime_ice", version="1.0")
    assert 'name: "rime_ice"' in header


def test_name_with_special_chars_is_quoted() -> None:
    header = _render_header(name="my dict #1", version="2.0")
    assert 'name: "my dict #1"' in header
