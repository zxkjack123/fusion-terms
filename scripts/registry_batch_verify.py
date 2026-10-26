#!/usr/bin/env python3
r"""Batch acceptance gate for the fusion-terms W1/W2/W3 batches (plan task T0.2).

Single, mechanically decidable entry point that every batch task
(definitions rewrite / Chinese-name drafting / allowlist top-up) must pass.
All verdicts are derived from the files on disk; nothing is hard-coded.

Modes
-----
``definitions``
    For every id in ``--ids-file``: ``terms/registry/definitions.tsv`` must hold
    exactly one ``en`` row and (per ``--lang``) exactly one ``zh`` row.  Each row
    must (a) not match the placeholder boilerplate regex
    ``^Fusion/nuclear engineering term referring to '.*' in technical context\.$``,
    (b) not contain ``聚变/核工程术语``, (c) not contain a language-label
    placeholder (``指“en”``), (d) clear the length floor (en >= 40 chars,
    zh >= 12 chars), and (e) carry a whitelisted ``source``
    (``http(s)://...`` / ``GB/T-4960.9`` / ``ITER-glossary`` /
    ``IAEA-safety-glossary`` / ``corpus``); ``internal:TODO`` is rejected.
    With ``--check-urls`` every http(s) source is probed and must answer 200;
    ``--no-net`` prints ``SKIPPED-NET`` and skips the probes instead of
    silently passing.

``names``
    For every id: ``terms/registry/concepts.tsv`` must hold a ``preferred_zh``
    that is non-empty, contains CJK ideographs, carries no whitespace, and is
    not identical to ``preferred_en`` (unless the id is listed in
    ``--allow-latin-names``).

``allowlist``
    For every id: ``preferred_zh`` must be listed in ``terms/allowlist_zh.txt``
    and, when ``preferred_en`` is a multi-word phrase, the id's hyphenated token
    form (``concept_id``) must be listed in ``terms/allowlist_en.txt``.  The en
    allowlist itself must be whitespace-free, i.e. the plan's reference command
    ``grep -v '^#' terms/allowlist_en.txt | grep -c ' '`` must yield 0.

Exit codes: ``0`` = every assertion holds, ``1`` = violations (all printed with
``file:line``), ``2`` = usage or I/O error.

Read-only and deterministic apart from ``--check-urls``.  ``--self-test`` runs
built-in assertions anchored on *real* corpus rows (see ``SELF_TEST_CASES``);
the handful of samples whose anchor row was later repaired by the data cleanup
are re-created in a throw-away copy of the corpus (see
``SELF_TEST_RESTORED_CASES``) so their assertions keep matching real rows.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
import urllib.error
import urllib.request
from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass
from pathlib import Path

# --------------------------------------------------------------------------- #
# Schema / contract constants
# --------------------------------------------------------------------------- #

SCHEMA_CONCEPTS = (
    "concept_id",
    "category",
    "preferred_zh",
    "preferred_en",
    "preferred_abbr",
    "status",
    "notes",
    "source",
)
SCHEMA_DEFINITIONS = ("concept_id", "lang", "definition", "source")

COL_ID = SCHEMA_CONCEPTS.index("concept_id")
COL_ZH = SCHEMA_CONCEPTS.index("preferred_zh")
COL_EN = SCHEMA_CONCEPTS.index("preferred_en")
N_CONCEPT_COLS = len(SCHEMA_CONCEPTS)

DEF_COL_LANG = SCHEMA_DEFINITIONS.index("lang")
DEF_COL_TEXT = SCHEMA_DEFINITIONS.index("definition")
DEF_COL_SOURCE = SCHEMA_DEFINITIONS.index("source")
N_DEF_COLS = len(SCHEMA_DEFINITIONS)

#: The W1 placeholder that must disappear from every ``en`` definition.
BOILERPLATE_EN_RE = re.compile(
    r"^Fusion/nuclear engineering term referring to '.*' in technical context\.$"
)
#: The W1 placeholder marker that must disappear from every definition.
BOILERPLATE_ZH_MARK = "聚变/核工程术语"
#: Language-label leak (``指“en”``) left by the broken dict-improvements pass.
LANG_PLACEHOLDER_RE = re.compile(r"指[“”\"']?en[“”\"']?")

CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
WHITESPACE_RE = re.compile(r"\s")

DEF_SOURCE_WHITELIST = frozenset(
    {"GB/T-4960.9", "ITER-glossary", "IAEA-safety-glossary", "corpus"}
)
DEF_SOURCE_FORBIDDEN = "internal:TODO"
HTTP_SOURCE_RE = re.compile(r"^https?://")

MIN_EN_CHARS = 40
MIN_ZH_CHARS = 12
URL_TIMEOUT_S = 15.0

RULE_COLUMNS = "concept_cols"
RULE_ZH_EMPTY = "names_zh_empty"

MODES = ("definitions", "names", "allowlist")


# --------------------------------------------------------------------------- #
# Violations / report
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Violation:
    """One failed assertion, anchored at a ``file:line`` location."""

    rule: str
    location: str
    detail: str

    def render(self) -> str:
        return f"{self.location}: {self.rule}: {self.detail}"

    def as_dict(self) -> dict[str, str]:
        return {"rule": self.rule, "location": self.location, "detail": self.detail}


def _loc(path: Path, lineno: int | None = None) -> str:
    return f"{path}:{lineno}" if lineno is not None else str(path)


# --------------------------------------------------------------------------- #
# Read-only corpus access
# --------------------------------------------------------------------------- #


def _iter_rows(path: Path) -> Iterator[tuple[int, list[str]]]:
    """Yield ``(1-based lineno, fields)`` for data rows (comments/blanks skipped).

    Iterating the file handle splits on ``\\n`` only, so the reported line
    numbers agree with ``grep -n`` / ``sed -n``.
    """
    with path.open(encoding="utf-8") as handle:
        for lineno, raw in enumerate(handle, 1):
            line = raw.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            yield lineno, line.split("\t")


def _iter_terms(path: Path) -> Iterator[tuple[int, str]]:
    with path.open(encoding="utf-8") as handle:
        for lineno, raw in enumerate(handle, 1):
            line = raw.rstrip("\n")
            if not line.strip() or line.startswith("#"):
                continue
            yield lineno, line.strip()


def _raw_non_comment_lines(path: Path) -> list[str]:
    """Mirror ``grep -v '^#'`` (comments dropped, everything else kept verbatim)."""
    return [
        line
        for line in path.read_text(encoding="utf-8").splitlines()
        if not line.startswith("#")
    ]


class Corpus:
    """Lazy, read-only view of the registry files under a repository root."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.concepts_path = root / "terms" / "registry" / "concepts.tsv"
        self.definitions_path = root / "terms" / "registry" / "definitions.tsv"
        self.allowlist_zh_path = root / "terms" / "allowlist_zh.txt"
        self.allowlist_en_path = root / "terms" / "allowlist_en.txt"
        self._concepts: dict[str, tuple[int, list[str]]] | None = None
        self._definitions: dict[str, dict[str, list[tuple[int, str, str]]]] | None = (
            None
        )
        self._allowlist_zh: set[str] | None = None
        self._allowlist_en: set[str] | None = None

    def concepts(self) -> dict[str, tuple[int, list[str]]]:
        """``concept_id -> (lineno, fields)``; first occurrence wins."""
        if self._concepts is None:
            table: dict[str, tuple[int, list[str]]] = {}
            for lineno, fields in _iter_rows(self.concepts_path):
                table.setdefault(fields[COL_ID], (lineno, fields))
            self._concepts = table
        return self._concepts

    def definitions(self) -> dict[str, dict[str, list[tuple[int, str, str]]]]:
        """``concept_id -> {lang: [(lineno, text, source), ...]}``."""
        if self._definitions is None:
            table: dict[str, dict[str, list[tuple[int, str, str]]]] = {}
            for lineno, fields in _iter_rows(self.definitions_path):
                if len(fields) != N_DEF_COLS:
                    continue
                text = fields[DEF_COL_TEXT]
                source = fields[DEF_COL_SOURCE]
                per_lang = table.setdefault(fields[0], {})
                per_lang.setdefault(fields[DEF_COL_LANG], []).append(
                    (lineno, text, source)
                )
            self._definitions = table
        return self._definitions

    def allowlist_zh(self) -> set[str]:
        if self._allowlist_zh is None:
            self._allowlist_zh = {
                term for _, term in _iter_terms(self.allowlist_zh_path)
            }
        return self._allowlist_zh

    def allowlist_en(self) -> set[str]:
        if self._allowlist_en is None:
            self._allowlist_en = {
                term for _, term in _iter_terms(self.allowlist_en_path)
            }
        return self._allowlist_en

    def allowlist_en_space_lines(self) -> list[str]:
        return [
            line
            for line in _raw_non_comment_lines(self.allowlist_en_path)
            if " " in line
        ]

    def require(self, *paths: Path) -> list[str]:
        return [str(path) for path in paths if not path.is_file()]


def http_status(url: str, timeout: float = URL_TIMEOUT_S) -> int | None:
    """Return the HTTP status for ``url``, or ``None`` when unreachable."""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:  # noqa: S310
            return int(response.status)
    except urllib.error.HTTPError as exc:
        return int(exc.code)
    except (urllib.error.URLError, OSError, ValueError):
        return None


# --------------------------------------------------------------------------- #
# Mode: definitions
# --------------------------------------------------------------------------- #


def _definition_text_violations(
    cid: str, lang: str, text: str, location: str
) -> list[Violation]:
    found: list[Violation] = []
    if BOILERPLATE_EN_RE.match(text):
        found.append(
            Violation(
                "def_boilerplate_regex",
                location,
                f"{cid} [{lang}]: matches the W1 placeholder regex",
            )
        )
    if BOILERPLATE_ZH_MARK in text:
        found.append(
            Violation(
                "def_boilerplate_mark",
                location,
                f"{cid} [{lang}]: contains {BOILERPLATE_ZH_MARK!r}",
            )
        )
    if LANG_PLACEHOLDER_RE.search(text):
        found.append(
            Violation(
                "def_lang_placeholder",
                location,
                f"{cid} [{lang}]: contains a language-label placeholder (指“en”)",
            )
        )
    floor = MIN_EN_CHARS if lang == "en" else MIN_ZH_CHARS
    if len(text) < floor:
        found.append(
            Violation(
                f"def_len_{lang}",
                location,
                f"{cid} [{lang}]: {len(text)} chars < required {floor}",
            )
        )
    return found


def _definition_source_violations(
    cid: str, source: str, location: str
) -> list[Violation]:
    if source == DEF_SOURCE_FORBIDDEN:
        return [
            Violation(
                "def_source_forbidden",
                location,
                f"{cid}: source {source!r} is explicitly forbidden",
            )
        ]
    if HTTP_SOURCE_RE.match(source) or source in DEF_SOURCE_WHITELIST:
        return []
    allowed = ", ".join(sorted(DEF_SOURCE_WHITELIST))
    return [
        Violation(
            "def_source_unknown",
            location,
            f"{cid}: source {source!r} is neither http(s)://… nor one of [{allowed}]",
        )
    ]


def check_definitions(
    corpus: Corpus,
    ids: Sequence[str],
    *,
    langs: Sequence[str] = ("en", "zh"),
    check_urls: bool = False,
    no_net: bool = False,
    url_probe: Callable[[str], int | None] | None = None,
    out: Callable[[str], None] = print,
) -> list[Violation]:
    index = corpus.definitions()
    probe = url_probe if url_probe is not None else http_status
    violations: list[Violation] = []
    status_cache: dict[str, int | None] = {}
    http_sources: set[str] = set()

    for cid in ids:
        per_lang = index.get(cid)
        if per_lang is None:
            violations.append(
                Violation(
                    "def_id_missing",
                    str(corpus.definitions_path),
                    f"no definitions row for id {cid!r}",
                )
            )
            continue
        for lang in langs:
            rows = per_lang.get(lang, [])
            if len(rows) != 1:
                violations.append(
                    Violation(
                        f"def_count_{lang}",
                        str(corpus.definitions_path),
                        f"{cid}: expected exactly 1 {lang} row, found {len(rows)}",
                    )
                )
                continue
            lineno, text, source = rows[0]
            location = _loc(corpus.definitions_path, lineno)
            violations.extend(_definition_text_violations(cid, lang, text, location))
            violations.extend(_definition_source_violations(cid, source, location))
            if check_urls and HTTP_SOURCE_RE.match(source):
                http_sources.add(source)
                if no_net:
                    continue
                if source not in status_cache:
                    status_cache[source] = probe(source)
                status = status_cache[source]
                if status != 200:
                    violations.append(
                        Violation(
                            "def_url_status",
                            location,
                            f"{cid}: source {source!r} answered {status!r} (require 200)",
                        )
                    )

    if check_urls and no_net:
        out(
            f"SKIPPED-NET: HTTP verification disabled by --no-net "
            f"({len(http_sources)} http source(s) in scope)"
        )
    return violations


# --------------------------------------------------------------------------- #
# Mode: names
# --------------------------------------------------------------------------- #


def check_names(
    corpus: Corpus,
    ids: Sequence[str],
    *,
    allow_latin_names: frozenset[str] = frozenset(),
) -> list[Violation]:
    index = corpus.concepts()
    violations: list[Violation] = []
    for cid in ids:
        entry = index.get(cid)
        if entry is None:
            violations.append(
                Violation(
                    "concept_id_missing",
                    str(corpus.concepts_path),
                    f"no concepts row for id {cid!r}",
                )
            )
            continue
        lineno, fields = entry
        location = _loc(corpus.concepts_path, lineno)
        if len(fields) != N_CONCEPT_COLS:
            violations.append(
                Violation(
                    RULE_COLUMNS,
                    location,
                    f"{cid}: expected {N_CONCEPT_COLS} columns, found {len(fields)}",
                )
            )
        zh = fields[COL_ZH] if len(fields) > COL_ZH else ""
        en = fields[COL_EN] if len(fields) > COL_EN else ""
        if not zh:
            violations.append(
                Violation(RULE_ZH_EMPTY, location, f"{cid}: preferred_zh is empty")
            )
            continue
        if WHITESPACE_RE.search(zh):
            violations.append(
                Violation(
                    "names_zh_whitespace",
                    location,
                    f"{cid}: preferred_zh {zh!r} contains whitespace",
                )
            )
        if not CJK_RE.search(zh):
            violations.append(
                Violation(
                    "names_zh_no_cjk",
                    location,
                    f"{cid}: preferred_zh {zh!r} contains no CJK ideograph",
                )
            )
        if zh == en and cid not in allow_latin_names:
            violations.append(
                Violation(
                    "names_zh_equals_en",
                    location,
                    f"{cid}: preferred_zh == preferred_en {zh!r} "
                    f"(not listed in --allow-latin-names)",
                )
            )
    return violations


# --------------------------------------------------------------------------- #
# Mode: allowlist
# --------------------------------------------------------------------------- #


def check_allowlist_en_lint(corpus: Corpus) -> list[Violation]:
    """Global lint: the plan's ``grep -v '^#' … | grep -c ' '`` must yield 0."""
    spaced = corpus.allowlist_en_space_lines()
    if not spaced:
        return []
    return [
        Violation(
            "allowlist_en_whitespace",
            str(corpus.allowlist_en_path),
            f"{len(spaced)} non-comment line(s) contain a space "
            f"(grep -c ' ' must be 0); first offender: {spaced[0]!r}",
        )
    ]


def check_allowlist(corpus: Corpus, ids: Sequence[str]) -> list[Violation]:
    violations: list[Violation] = check_allowlist_en_lint(corpus)

    zh_listed = corpus.allowlist_zh()
    en_listed = corpus.allowlist_en()
    index = corpus.concepts()
    for cid in ids:
        entry = index.get(cid)
        if entry is None:
            violations.append(
                Violation(
                    "concept_id_missing",
                    str(corpus.concepts_path),
                    f"no concepts row for id {cid!r}",
                )
            )
            continue
        lineno, fields = entry
        location = _loc(corpus.concepts_path, lineno)
        if len(fields) != N_CONCEPT_COLS:
            violations.append(
                Violation(
                    RULE_COLUMNS,
                    location,
                    f"{cid}: expected {N_CONCEPT_COLS} columns, found {len(fields)}",
                )
            )
        zh = fields[COL_ZH] if len(fields) > COL_ZH else ""
        en = fields[COL_EN] if len(fields) > COL_EN else ""
        if zh not in zh_listed:
            violations.append(
                Violation(
                    "allow_zh_not_listed",
                    location,
                    f"{cid}: preferred_zh {zh!r} not listed in {corpus.allowlist_zh_path}",
                )
            )
        if " " in en and cid not in en_listed:
            violations.append(
                Violation(
                    "allow_en_not_listed",
                    location,
                    f"{cid}: preferred_en {en!r} is a phrase; hyphenated token form "
                    f"{cid!r} not listed in {corpus.allowlist_en_path}",
                )
            )
    return violations


# --------------------------------------------------------------------------- #
# ids file handling
# --------------------------------------------------------------------------- #


def read_ids(path: Path) -> list[tuple[int, str]]:
    """Return ``(lineno, id)`` for every non-comment, non-blank line."""
    entries: list[tuple[int, str]] = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        entries.append((lineno, line))
    return entries


def _ids_file_violations(
    path: Path, entries: Sequence[tuple[int, str]], expect: int | None
) -> list[Violation]:
    violations: list[Violation] = []
    seen: dict[str, int] = {}
    for lineno, cid in entries:
        if cid in seen:
            violations.append(
                Violation(
                    "ids_duplicate",
                    _loc(path, lineno),
                    f"{cid}: duplicated (first seen at line {seen[cid]})",
                )
            )
        else:
            seen[cid] = lineno
    if expect is not None and len(entries) != expect:
        violations.append(
            Violation(
                "ids_count",
                str(path),
                f"expected {expect} id(s), found {len(entries)}",
            )
        )
    return violations


def _parse_allow_latin_names(value: str | None) -> frozenset[str]:
    if not value:
        return frozenset()
    candidate = Path(value)
    if candidate.is_file():
        return frozenset(term for _, term in _iter_terms(candidate))
    return frozenset(item.strip() for item in value.split(",") if item.strip())


# --------------------------------------------------------------------------- #
# Self-test
# --------------------------------------------------------------------------- #

#: Malformed samples are *real* corpus rows; locations must reproduce on HEAD.
SELF_TEST_CASES: tuple[tuple[str, str, tuple[str, ...], bool, tuple[str, ...]], ...] = (
    (
        "malformed: 6-column row (missing category/status/source)",
        "names",
        ("poloidal-field-power-supply",),
        False,
        (f"{RULE_COLUMNS}@terms/registry/concepts.tsv:3316",),
    ),
    (
        "malformed: left-shifted row (zh slot holds the English name)",
        "names",
        ("energy-security",),
        False,
        ("names_zh_no_cjk@terms/registry/concepts.tsv:3171",),
    ),
    (
        "malformed: empty preferred_zh",
        "names",
        ("neutral-beam-injection",),
        False,
        (f"{RULE_ZH_EMPTY}@terms/registry/concepts.tsv:8",),
    ),
    (
        "malformed: boilerplate + 指“en” + non-whitelisted source",
        "definitions",
        ("adjoint-flux",),
        False,
        (
            "def_boilerplate_regex@terms/registry/definitions.tsv:5837",
            "def_boilerplate_mark@terms/registry/definitions.tsv:5838",
            "def_lang_placeholder@terms/registry/definitions.tsv:5838",
            "def_source_unknown@terms/registry/definitions.tsv:5837",
        ),
    ),
    (
        "malformed: preferred_zh absent from allowlist_zh.txt",
        "allowlist",
        ("poloidal-field-power-supply",),
        False,
        ("allow_zh_not_listed@terms/registry/concepts.tsv:3316",),
    ),
    ("compliant: names", "names", ("tokamak",), True, ()),
    (
        "compliant: allowlist (zh listed; phrase backed by allowlist_en)",
        "allowlist",
        ("tokamak-exhaust-processing-system",),
        True,
        (),
    ),
    ("compliant: definitions", "definitions", ("aspect-ratio",), True, ()),
)

#: Indices into ``SELF_TEST_CASES`` whose malformed sample was a *real* corpus row
#: that a later data repair removed.  T0.7a/T0.7b deleted the ``指“en”`` rows and
#: T0.9/T0.10 fixed the 6-column block plus the left-shifted row, so those three
#: anchor rows no longer exist on HEAD and their assertions went red **without any
#: rule changing**.  Re-creating the defects in a throw-away copy of the real
#: corpus keeps every assertion and its ``file:line`` anchor literally identical,
#: and makes the fixture immune to the next round of data repairs.
SELF_TEST_RESTORED_CASES: frozenset[int] = frozenset(
    {
        0,  # malformed: 6-column row (poloidal-field-power-supply)
        1,  # malformed: left-shifted row (energy-security)
        3,  # malformed: boilerplate + 指“en” + non-whitelisted source (adjoint-flux)
    }
)


def _build_restored_defect_corpus(real_root: Path, dest: Path) -> Corpus:
    """Copy the real corpus to ``dest`` and re-create three historical defects.

    The re-created defects are exactly the ones the self-test's malformed samples
    were originally anchored on:

    * ``poloidal-field-power-supply`` — the concepts row lost its
      ``category``/``status``/``source`` tail (6 columns instead of 8);
    * ``energy-security`` — the row was left-shifted, so the zh slot holds the
      English name instead of ``能源安全``;
    * ``adjoint-flux`` — the zh definition was the low-information template that
      leaked the language label (``聚变/核工程术语，指“en”这一技术概念。``).

    Only the copies under ``dest`` are mutated; ``real_root`` is never written.
    Row counts are preserved, so every ``file:line`` anchor in
    ``SELF_TEST_CASES`` still resolves to the same line.
    """
    source_registry = real_root / "terms" / "registry"
    registry = dest / "terms" / "registry"
    registry.mkdir(parents=True, exist_ok=True)

    # ``split("\n")`` / ``"\n".join`` rather than ``splitlines``: the latter also
    # splits on \x0b / \x0c / \u2028 / \u2029, which would shift line numbers.
    concepts = (
        (source_registry / "concepts.tsv").read_text(encoding="utf-8").split("\n")
    )
    for index, line in enumerate(concepts):
        fields = line.split("\t")
        if len(fields) <= COL_EN:
            continue
        if fields[0] == "poloidal-field-power-supply":
            concepts[index] = "\t".join(fields[:6])  # defect: 6 columns
        elif fields[0] == "energy-security":
            fields[COL_ZH] = fields[COL_EN]  # defect: zh slot holds the English name
            concepts[index] = "\t".join(fields)
    (registry / "concepts.tsv").write_text("\n".join(concepts), encoding="utf-8")

    definitions = (
        (source_registry / "definitions.tsv").read_text(encoding="utf-8").split("\n")
    )
    for index, line in enumerate(definitions):
        fields = line.split("\t")
        if len(fields) <= DEF_COL_TEXT or fields[0] != "adjoint-flux":
            continue
        if fields[DEF_COL_LANG] == "zh":
            # defect: low-information template that leaked the language label
            fields[DEF_COL_TEXT] = f"{BOILERPLATE_ZH_MARK}，指“en”这一技术概念。"
            definitions[index] = "\t".join(fields)
    (registry / "definitions.tsv").write_text("\n".join(definitions), encoding="utf-8")

    for name in ("allowlist_zh.txt", "allowlist_en.txt"):
        shutil.copyfile(real_root / "terms" / name, dest / "terms" / name)
    return Corpus(dest)


def _expected_tokens(corpus: Corpus, mode: str, ids: Sequence[str]) -> list[Violation]:
    if mode == "names":
        return check_names(corpus, ids)
    if mode == "definitions":
        return check_definitions(corpus, ids, langs=("en", "zh"))
    return check_allowlist(corpus, ids)


def _build_synthetic_corpus(
    root: Path, *, allowlist_en_extra: Sequence[str] = ()
) -> Corpus:
    """Minimal temp corpus used only for branches with no real failing sample.

    The repository currently declares zero http(s) sources in
    ``definitions.tsv`` and a whitespace-clean ``allowlist_en.txt``, so those
    branches cannot be exercised on real data without inventing provenance or
    corrupting the corpus.  This synthetic corpus is a *unit* fixture for those
    branches only; every malformed and compliant sample used by the self-test's
    mode checks is a real corpus row.
    """
    registry = root / "terms" / "registry"
    registry.mkdir(parents=True, exist_ok=True)
    rows = [
        "# concept_id\tlang\tdefinition\tsource",
        "unit-alpha\ten\t" + "E" * MIN_EN_CHARS + "\thttps://example.org/en",
        "unit-alpha\tzh\t" + "测" * MIN_ZH_CHARS + "\thttps://example.org/zh",
    ]
    (registry / "definitions.tsv").write_text("\n".join(rows) + "\n", encoding="utf-8")
    allowlist_en = root / "terms" / "allowlist_en.txt"
    allowlist_en.write_text(
        "\n".join(["# synthetic allowlist", "ok-token", *allowlist_en_extra]) + "\n",
        encoding="utf-8",
    )
    (root / "terms" / "allowlist_zh.txt").write_text(
        "# synthetic allowlist\n", encoding="utf-8"
    )
    return Corpus(root)


def run_self_test(corpus: Corpus) -> int:
    failures: list[str] = []
    checks = 0

    def expect(condition: bool, label: str, extra: str = "") -> None:
        nonlocal checks
        checks += 1
        if condition:
            print(f"  PASS  {label}")
        else:
            print(f"  FAIL  {label}{(' — ' + extra) if extra else ''}")
            failures.append(label)

    print("self-test: rule-level assertions on real corpus text")
    definitions = corpus.definitions()
    adjoint_en = definitions["adjoint-flux"]["en"][0][1]
    aspect_en = definitions["aspect-ratio"]["en"][0][1]
    expect(
        BOILERPLATE_EN_RE.match(adjoint_en) is not None,
        "boilerplate regex fires on the real adjoint-flux en text",
        f"regex did not match {adjoint_en[:60]!r}",
    )
    expect(
        BOILERPLATE_EN_RE.match(aspect_en) is None,
        "boilerplate regex does not fire on a real ITER definition",
    )
    expect(
        corpus.allowlist_en_space_lines() == [],
        "allowlist_en.txt has no whitespace on non-comment lines",
    )
    expect(
        CJK_RE.search("托卡马克") is not None
        and CJK_RE.search("energy security") is None,
        "CJK detector separates 托卡马克 from 'energy security'",
    )

    print("self-test: mode verdicts on real corpus rows")
    restored_root = Path(tempfile.mkdtemp(prefix="t0_2_selftest_restored_"))
    try:
        # Three samples sit on rows that later data repairs removed (see
        # SELF_TEST_RESTORED_CASES); they run against a copy of the real corpus in
        # which those defects are re-created.  The rules — and every assertion,
        # including its file:line anchor — are unchanged.
        restored = _build_restored_defect_corpus(corpus.root, restored_root)
        for index, (label, mode, ids, expect_ok, expected) in enumerate(
            SELF_TEST_CASES
        ):
            sample = restored if index in SELF_TEST_RESTORED_CASES else corpus
            violations = _expected_tokens(sample, mode, ids)
            ok = not violations
            expect(
                ok == expect_ok,
                f"[{mode}] {label} -> {'PASS' if expect_ok else 'FAIL'}",
                f"got {'PASS' if ok else 'FAIL'} with {[v.render() for v in violations]}",
            )
            fired = {f"{v.rule}@{_suffix(v.location, 'terms/')}" for v in violations}
            for token in expected:
                expect(
                    token in fired,
                    f"[{mode}] {label} -> rule {token}",
                    f"fired={sorted(fired)}",
                )
    finally:
        shutil.rmtree(restored_root, ignore_errors=True)

    print("self-test: --check-urls branch (synthetic fixture, no network)")
    tmp_root = Path(tempfile.mkdtemp(prefix="t0_2_selftest_"))
    try:
        synthetic = _build_synthetic_corpus(tmp_root)
        ok_200 = check_definitions(
            synthetic,
            ["unit-alpha"],
            langs=("en", "zh"),
            check_urls=True,
            url_probe=lambda _url: 200,
        )
        expect(ok_200 == [], "http source answering 200 passes", repr(ok_200))
        bad_404 = check_definitions(
            synthetic,
            ["unit-alpha"],
            langs=("en", "zh"),
            check_urls=True,
            url_probe=lambda _url: 404,
        )
        expect(
            {v.rule for v in bad_404} == {"def_url_status"},
            "http source answering 404 fails with def_url_status",
            repr([v.as_dict() for v in bad_404]),
        )
        captured: list[str] = []
        skipped = check_definitions(
            synthetic,
            ["unit-alpha"],
            langs=("en", "zh"),
            check_urls=True,
            no_net=True,
            out=captured.append,
        )
        expect(
            skipped == [] and any("SKIPPED-NET" in line for line in captured),
            "--no-net skips probes and prints SKIPPED-NET",
            repr(captured),
        )
        spaced = _build_synthetic_corpus(
            tmp_root / "allowlist_case", allowlist_en_extra=["bad token"]
        )
        spaced_rules = {v.rule for v in check_allowlist_en_lint(spaced)}
        expect(
            spaced_rules == {"allowlist_en_whitespace"},
            "allowlist_en whitespace lint fires on a synthetic spaced line",
            repr(sorted(spaced_rules)),
        )
    finally:
        shutil.rmtree(tmp_root, ignore_errors=True)

    print(f"self-test: {checks - len(failures)}/{checks} assertions passed")
    if failures:
        print("self-test: FAILED", file=sys.stderr)
        return 1
    print("self-test: OK")
    return 0


def _suffix(location: str, marker: str) -> str:
    """Return the tail of ``location`` starting at ``marker`` (else the whole string)."""
    index = location.rfind(marker)
    return location[index:] if index >= 0 else location


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="registry_batch_verify",
        description=(
            "Batch acceptance gate for the fusion-terms W1/W2/W3 batches "
            "(plan task T0.2). Read-only; exit 0 = pass, 1 = violations, 2 = usage."
        ),
    )
    parser.add_argument("--mode", choices=MODES, help="acceptance mode to run")
    parser.add_argument(
        "--ids-file",
        type=Path,
        help="newline-separated concept ids (one per line, '#' comments allowed)",
    )
    parser.add_argument(
        "--expect",
        type=int,
        default=None,
        help="expected number of ids in --ids-file (asserted exactly)",
    )
    parser.add_argument(
        "--lang",
        choices=("en", "zh", "both"),
        default="both",
        help="definitions mode: which language rows to validate (default: both)",
    )
    parser.add_argument(
        "--check-urls",
        action="store_true",
        help="definitions mode: probe http(s) sources and require HTTP 200",
    )
    parser.add_argument(
        "--no-net",
        action="store_true",
        help="with --check-urls: skip probes and print SKIPPED-NET",
    )
    parser.add_argument(
        "--allow-latin-names",
        default=None,
        help=(
            "names mode: comma-separated ids (or a file of ids) whose "
            "preferred_zh may equal preferred_en"
        ),
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="repository root holding terms/ (default: parent of scripts/)",
    )
    parser.add_argument(
        "--json",
        type=Path,
        default=None,
        help="write the machine-readable verdict to this path",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run the built-in assertions on real corpus rows and exit",
    )
    return parser


def _emit_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    root = (args.repo_root or Path(__file__).resolve().parent.parent).resolve()
    corpus = Corpus(root)

    if args.self_test:
        missing = corpus.require(
            corpus.concepts_path,
            corpus.definitions_path,
            corpus.allowlist_zh_path,
            corpus.allowlist_en_path,
        )
        if missing:
            print(
                "registry_batch_verify: input not found: " + ", ".join(missing),
                file=sys.stderr,
            )
            return 2
        return run_self_test(corpus)

    if args.mode is None or args.ids_file is None:
        print(
            "registry_batch_verify: --mode and --ids-file are required "
            "(or use --self-test)",
            file=sys.stderr,
        )
        return 2
    if not args.ids_file.is_file():
        print(
            f"registry_batch_verify: ids file not found: {args.ids_file}",
            file=sys.stderr,
        )
        return 2

    needed = [corpus.concepts_path]
    if args.mode == "definitions":
        needed = [corpus.definitions_path]
    elif args.mode == "allowlist":
        needed = [
            corpus.concepts_path,
            corpus.allowlist_zh_path,
            corpus.allowlist_en_path,
        ]
    missing = corpus.require(*needed)
    if missing:
        print(
            "registry_batch_verify: input not found: " + ", ".join(missing),
            file=sys.stderr,
        )
        return 2

    try:
        entries = read_ids(args.ids_file)
    except OSError as exc:  # pragma: no cover - defensive I/O guard
        print(f"registry_batch_verify: I/O error: {exc}", file=sys.stderr)
        return 2

    ids = [cid for _, cid in entries]
    violations = _ids_file_violations(args.ids_file, entries, args.expect)

    if args.mode == "names":
        violations.extend(
            check_names(
                corpus,
                ids,
                allow_latin_names=_parse_allow_latin_names(args.allow_latin_names),
            )
        )
    elif args.mode == "definitions":
        langs = ("en", "zh") if args.lang == "both" else (args.lang,)
        violations.extend(
            check_definitions(
                corpus,
                ids,
                langs=langs,
                check_urls=args.check_urls,
                no_net=args.no_net,
            )
        )
    else:
        violations.extend(check_allowlist(corpus, ids))

    verdict = "PASS" if not violations else "FAIL"
    header = (
        f"registry_batch_verify: mode={args.mode} ids_file={args.ids_file} "
        f"ids={len(ids)} expect={args.expect} verdict={verdict}"
    )
    print(header)
    for violation in violations:
        print(f"  {violation.render()}")

    payload = {
        "mode": args.mode,
        "ids_file": str(args.ids_file),
        "ids_expected": args.expect,
        "ids_seen": len(ids),
        "verdict": verdict,
        "violation_count": len(violations),
        "violations": [violation.as_dict() for violation in violations],
    }
    if args.json is not None:
        _emit_json(args.json, payload)

    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
