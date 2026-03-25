from __future__ import annotations

from pipeline.extract_candidates import _extractor_signature


def test_signature_changes_with_min_zh_len() -> None:
    sig_a = _extractor_signature(
        min_zh_len=2,
        max_zh_len=8,
        en_phrases="off",
    )
    sig_b = _extractor_signature(
        min_zh_len=3,
        max_zh_len=8,
        en_phrases="off",
    )
    assert sig_a != sig_b


def test_signature_changes_with_en_phrases() -> None:
    sig_a = _extractor_signature(
        min_zh_len=2,
        max_zh_len=8,
        en_phrases="off",
    )
    sig_b = _extractor_signature(
        min_zh_len=2,
        max_zh_len=8,
        en_phrases="rake",
    )
    assert sig_a != sig_b


def test_signature_deterministic() -> None:
    sig_a = _extractor_signature(
        min_zh_len=2,
        max_zh_len=8,
        en_phrases="rake",
    )
    sig_b = _extractor_signature(
        min_zh_len=2,
        max_zh_len=8,
        en_phrases="rake",
    )
    assert sig_a == sig_b
