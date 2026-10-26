#!/usr/bin/env python3
"""Canonical registry -> allowlist coverage report (plan `#T-4973` task T0.0).

Purpose
-------
Freeze ONE coverage definition so the three historical figures
(45.6 % / 45.7 % / 46.3 %) can no longer be mixed and every downstream work set
(W1 / W2 / W3) can be recomputed from data instead of from plan prose.

Primary metric (plan `terminology-coverage-and-definition-quality.md` §D,
"本计划唯一定义，禁止再用旧口径"):

    a concept is COVERED  <=>  its ``concept_id``, ``preferred_en``,
    ``preferred_zh``, or ANY of its aliases appears in the built IME word list
    ``artifacts/domain_terms.txt``.

Two further figures are printed for cross-audit only and are **not** the plan
metric:

* ``allowlist_only_coverage_pct`` -- legacy '口径' (``preferred_*`` present in
  ``terms/allowlist_{zh,en}.txt``; task-book value 45.7 %),
* ``coverage_pct_incl_allowlist`` -- union of the plan metric and the legacy one
  (12 allowlist entries are not present in the built word list, so the union is
  a few rows larger).

Work sets (plan §D2/§D4) are computed over **well-formed** concept rows only
(8 columns and a category inside the canonical 16-value domain, §A4).  The
malformed rows (§A2: 99 column-shifted + 80 six-column) are reported separately:
their field slots are misplaced, therefore any per-field verdict on them is
provisional and must not enter W2/W3.

Nothing is hard-coded except the *classification rules* (category domain,
proper-name categories, boilerplate regex).  Every number comes from the files
actually read; input digests are printed for provenance.

Read-only, deterministic, offline.

Usage
-----
    .venv/bin/python scripts/registry_coverage_report.py
    .venv/bin/python scripts/registry_coverage_report.py --json /tmp/cov.json
    .venv/bin/python scripts/registry_coverage_report.py \
        --emit-lists .github/plans/t4973-batches --batch-size 20
    # failure proof (W1_A_BASELINE / empty-corpus probe): coverage must drop to 0
    .venv/bin/python scripts/registry_coverage_report.py --terms-file /dev/null

Exit codes: 0 = report produced, 2 = an input file is missing/unreadable.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

# --- classification rules (no statistics) ----------------------------------

CANON_CATEGORIES = frozenset(
    {
        "concept",
        "nuclear-fusion",
        "metric",
        "method",
        "code",
        "device",
        "system",
        "material",
        "diagnostic",
        "company",
        "organization",
        "doc",
        "limit",
        "effect",
        "facility",
        "principle",
    }
)

PROPER_CATEGORIES = frozenset({"company", "organization", "facility"})

EN_BOILERPLATE_RE = re.compile(
    r"^Fusion/nuclear engineering term referring to '.*' in technical context\.$"
)

#: zh definitions that render the language tag ``en`` as if it were a term name
ZH_CORRUPT_MARKER = "指“en”"

#: spec source backing "in-repo derivable" W1 definitions (plan §E6)
W1_A_SOURCE = "GB/T-4960.9"

DEFAULT_CONCEPTS = "terms/registry/concepts.tsv"
DEFAULT_ALIASES = "terms/registry/aliases.tsv"
DEFAULT_DEFINITIONS = "terms/registry/definitions.tsv"
DEFAULT_ALLOWLIST_ZH = "terms/allowlist_zh.txt"
DEFAULT_ALLOWLIST_EN = "terms/allowlist_en.txt"
DEFAULT_DENYLIST = "terms/denylist.txt"
DEFAULT_TERMS_FILE = "artifacts/domain_terms.txt"

SCHEMA = "registry-coverage-report/1"


class InputError(RuntimeError):
    """A required input file is missing or unreadable."""


# --- io helpers ------------------------------------------------------------


def read_tsv(path: Path) -> list[tuple[int, tuple[str, ...]]]:
    """Return ``(1-based line number, tab-split fields)`` for data rows only."""
    rows: list[tuple[int, tuple[str, ...]]] = []
    try:
        with path.open(encoding="utf-8") as handle:
            for line_no, raw in enumerate(handle, 1):
                line = raw.rstrip("\n")
                if not line.strip() or line.startswith("#"):
                    continue
                rows.append((line_no, tuple(line.split("\t"))))
    except OSError as exc:  # missing file, permission, directory, ...
        raise InputError(f"cannot read TSV {path}: {exc}") from exc
    return rows


def read_tokens(path: Path) -> list[str]:
    """Return non-comment, non-blank lines of a term list, order preserved."""
    try:
        with path.open(encoding="utf-8") as handle:
            raw_lines = handle.readlines()
    except OSError as exc:
        raise InputError(f"cannot read term list {path}: {exc}") from exc
    tokens: list[str] = []
    for raw in raw_lines:
        token = raw.rstrip("\n").strip()
        if not token or token.startswith("#"):
            continue
        tokens.append(token)
    return tokens


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


# --- data model ------------------------------------------------------------


@dataclass(frozen=True)
class ConceptRow:
    """One `concepts.tsv` data row, addressed by field position."""

    line_no: int
    fields: tuple[str, ...]

    @property
    def concept_id(self) -> str:
        return self.fields[0] if self.fields else ""

    @property
    def category(self) -> str:
        return self.fields[1] if len(self.fields) > 1 else ""

    @property
    def preferred_zh(self) -> str:
        return self.fields[2] if len(self.fields) > 2 else ""

    @property
    def preferred_en(self) -> str:
        return self.fields[3] if len(self.fields) > 3 else ""

    @property
    def kind(self) -> str:
        """``wellformed`` / ``shifted`` / ``sixcol`` / ``malformed_len``."""
        if len(self.fields) == 6:
            return "sixcol"
        if len(self.fields) == 8:
            return "wellformed" if self.category in CANON_CATEGORIES else "shifted"
        return "malformed_len"

    @property
    def has_zh(self) -> bool:
        return bool(self.preferred_zh.strip())


def hyphenated(text: str) -> str:
    """Phrase -> hyphen token, i.e. the only IME-legal form (plan §RK5)."""
    return re.sub(r"\s+", "-", text.strip())


def domain_term_hits(
    row: ConceptRow, aliases: dict[str, tuple[str, ...]], terms: set[str]
) -> tuple[str, ...]:
    """Which of the plan §D four entry points are found in the word list."""
    hits: list[str] = []
    if row.concept_id and row.concept_id in terms:
        hits.append("concept_id")
    if row.preferred_en and row.preferred_en in terms:
        hits.append("preferred_en")
    if row.preferred_zh and row.preferred_zh in terms:
        hits.append("preferred_zh")
    for alias in aliases.get(row.concept_id, ()):
        if alias in terms:
            hits.append(f"alias:{alias}")
            break
    return tuple(hits)


def allowlist_hits(
    row: ConceptRow, allow_zh: set[str], allow_en: set[str]
) -> tuple[str, ...]:
    """Legacy '口径': ``preferred_zh`` / ``preferred_en`` present in allowlists."""
    hits: list[str] = []
    if row.preferred_zh and row.preferred_zh in allow_zh:
        hits.append("preferred_zh")
    if row.preferred_en:
        if row.preferred_en in allow_en:
            hits.append("preferred_en")
        elif hyphenated(row.preferred_en) in allow_en:
            hits.append("preferred_en_hyphenated")
    return tuple(hits)


# --- work sets -------------------------------------------------------------


def build_alias_index(
    alias_rows: list[tuple[int, tuple[str, ...]]],
) -> dict[str, tuple[str, ...]]:
    grouped: dict[str, list[str]] = {}
    for _line_no, fields in alias_rows:
        if len(fields) < 2:
            continue
        alias, concept_id = fields[0], fields[1]
        if not alias or not concept_id:
            continue
        bucket = grouped.setdefault(concept_id, [])
        if alias not in bucket:
            bucket.append(alias)
    return {cid: tuple(values) for cid, values in grouped.items()}


@dataclass
class DefinitionIndex:
    """Per-concept view of ``definitions.tsv`` used for the W1 splits."""

    en_boilerplate: tuple[str, ...]
    zh_corrupt: tuple[str, ...]
    with_definitions: frozenset[str]
    zh_source_gbt: frozenset[str]
    available: bool


def build_definition_index(
    path: Path, concept_order: tuple[str, ...]
) -> DefinitionIndex:
    if not path.exists():
        return DefinitionIndex((), (), frozenset(), frozenset(), available=False)
    rows = read_tsv(path)
    boiler: list[str] = []
    boiler_seen: set[str] = set()
    corrupt: list[str] = []
    corrupt_seen: set[str] = set()
    with_defs: set[str] = set()
    gbt: set[str] = set()
    for _line_no, fields in rows:
        if len(fields) < 4:
            continue
        concept_id, lang, text, source = fields[0], fields[1], fields[2], fields[3]
        with_defs.add(concept_id)
        if (
            lang == "zh"
            and ZH_CORRUPT_MARKER in text
            and concept_id not in corrupt_seen
        ):
            corrupt_seen.add(concept_id)
            corrupt.append(concept_id)
        if lang == "en" and EN_BOILERPLATE_RE.match(text):
            if concept_id not in boiler_seen:
                boiler_seen.add(concept_id)
                boiler.append(concept_id)
        if lang == "zh" and source == W1_A_SOURCE:
            gbt.add(concept_id)
    order = {cid: idx for idx, cid in enumerate(concept_order)}
    ordered = lambda ids: tuple(  # noqa: E731 - small local key
        sorted(ids, key=lambda cid: order.get(cid, len(order)))
    )
    return DefinitionIndex(
        en_boilerplate=ordered(boiler),
        zh_corrupt=ordered(corrupt),
        with_definitions=frozenset(with_defs),
        zh_source_gbt=frozenset(gbt),
        available=True,
    )


def chunk(items: tuple[str, ...], size: int) -> list[tuple[str, ...]]:
    if size < 1:
        raise ValueError("batch size must be >= 1")
    return [items[i : i + size] for i in range(0, len(items), size)]


# --- report ----------------------------------------------------------------


def build_report(
    args: argparse.Namespace,
) -> tuple[dict[str, object], dict[str, object], dict[str, tuple[str, ...]]]:
    root = Path(args.repo_root)
    paths = {
        "concepts": root / args.concepts,
        "aliases": root / args.aliases,
        "definitions": root / args.definitions,
        "allowlist_zh": root / args.allowlist_zh,
        "allowlist_en": root / args.allowlist_en,
        "denylist": root / args.denylist,
        "terms_file": Path(args.terms_file)
        if str(args.terms_file).startswith("/")
        else root / args.terms_file,
    }

    terms = set(read_tokens(paths["terms_file"]))
    allow_zh = set(read_tokens(paths["allowlist_zh"]))
    allow_en = set(read_tokens(paths["allowlist_en"]))
    denylist = set(read_tokens(paths["denylist"]))
    concept_rows = [ConceptRow(ln, f) for ln, f in read_tsv(paths["concepts"])]
    aliases = build_alias_index(read_tsv(paths["aliases"]))

    concepts = {
        "total": len(concept_rows),
        "covered": 0,
        "uncovered": 0,
        "covered_incl_allowlist": 0,
        "covered_allowlist_only": 0,
        "wellformed": 0,
        "shifted": 0,
        "sixcol": 0,
        "malformed_len": 0,
        "uncovered_wellformed": 0,
        "uncovered_malformed": 0,
        "covered_malformed": 0,
    }
    proper_by_category: dict[str, int] = {}
    proper_all = 0
    uncovered_wellformed: list[ConceptRow] = []
    uncovered_malformed: list[ConceptRow] = []
    uncovered_ids: list[str] = []
    covered_ids: list[str] = []
    hit_counts: dict[str, int] = dict.fromkeys(
        ("concept_id", "preferred_en", "preferred_zh", "alias"), 0
    )
    hit_examples: dict[str, list[str]] = {
        name: [] for name in ("concept_id", "preferred_en", "preferred_zh", "alias")
    }

    for row in concept_rows:
        kind = row.kind
        concepts[kind] = int(concepts[kind]) + 1  # type: ignore[operator]
        in_dt = domain_term_hits(row, aliases, terms)
        in_allow = allowlist_hits(row, allow_zh, allow_en)
        if in_dt:
            concepts["covered"] = int(concepts["covered"]) + 1
            covered_ids.append(row.concept_id)
            for reason in in_dt:
                bucket = reason.split(":", 1)[0]
                hit_counts[bucket] += 1
                if len(hit_examples[bucket]) < 5:
                    hit_examples[bucket].append(row.concept_id)
        else:
            concepts["uncovered"] = int(concepts["uncovered"]) + 1
            uncovered_ids.append(row.concept_id)
            if kind == "wellformed":
                uncovered_wellformed.append(row)
                if row.category in PROPER_CATEGORIES:
                    proper_all += 1
            else:
                uncovered_malformed.append(row)
        if in_dt or in_allow:
            concepts["covered_incl_allowlist"] = (
                int(concepts["covered_incl_allowlist"]) + 1
            )
        if in_allow:
            concepts["covered_allowlist_only"] = (
                int(concepts["covered_allowlist_only"]) + 1
            )

    concepts["uncovered_wellformed"] = len(uncovered_wellformed)
    concepts["uncovered_malformed"] = len(uncovered_malformed)
    concepts["covered_malformed"] = (
        int(concepts["shifted"])
        + int(concepts["sixcol"])
        + int(concepts["malformed_len"])
        - len(uncovered_malformed)
    )

    # --- W2 / W3a over well-formed uncovered rows only (plan §D2/§D4) -------
    w2: list[ConceptRow] = []
    w3a: list[ConceptRow] = []
    proper_wellformed = 0
    for row in uncovered_wellformed:
        if row.category in PROPER_CATEGORIES:
            proper_wellformed += 1
            proper_by_category[row.category] = (
                proper_by_category.get(row.category, 0) + 1
            )
            continue
        if row.has_zh:
            w2.append(row)
        else:
            w3a.append(row)
    w2_multiword = [r for r in w2 if re.search(r"\s", r.preferred_en)]
    w2_single = [r for r in w2 if not re.search(r"\s", r.preferred_en)]

    w2_ids = tuple(r.concept_id for r in w2)
    w3_ids = tuple(r.concept_id for r in w3a)
    # denylist collision pre-check for W2 (plan §RK5 / §T2.0 / §D2-2):
    # writing a term that is already denied is a silent no-op.
    w2_deny_en = tuple(
        r.concept_id
        for r in w2
        if r.preferred_en in denylist or hyphenated(r.preferred_en) in denylist
    )
    w2_deny_id = tuple(r.concept_id for r in w2 if r.concept_id in denylist)
    w2_deny_zh = tuple(r.concept_id for r in w2 if r.preferred_zh in denylist)

    # --- legacy/union口径 side metrics (cross-audit) -----------------------
    covered_incl = int(concepts["covered_incl_allowlist"])
    covered_allow = int(concepts["covered_allowlist_only"])
    # W2/W3a under the union口径, for difference auditing only
    union_uncovered_wf: list[ConceptRow] = []
    for row in concept_rows:
        if row.kind != "wellformed":
            continue
        if domain_term_hits(row, aliases, terms) or allowlist_hits(
            row, allow_zh, allow_en
        ):
            continue
        union_uncovered_wf.append(row)
    union_w2 = [
        r
        for r in union_uncovered_wf
        if r.category not in PROPER_CATEGORIES and r.has_zh
    ]
    union_w3a = [
        r
        for r in union_uncovered_wf
        if r.category not in PROPER_CATEGORIES and not r.has_zh
    ]

    # --- W1 splits (definitions) ------------------------------------------
    concept_order = tuple(r.concept_id for r in concept_rows)
    defs = build_definition_index(paths["definitions"], concept_order)
    w1_a: tuple[str, ...] = ()
    w1_b: tuple[str, ...] = ()
    w1_c: tuple[str, ...] = ()
    if defs.available:
        boiler = set(defs.en_boilerplate)
        w1_a = tuple(
            cid for cid in concept_order if cid in boiler and cid in defs.zh_source_gbt
        )
        a_set = set(w1_a)
        w1_b = tuple(cid for cid in concept_order if cid in boiler and cid not in a_set)
        w1_c = tuple(cid for cid in concept_order if cid not in defs.with_definitions)

    total = int(concepts["total"])
    covered = int(concepts["covered"])
    uncovered = int(concepts["uncovered"])

    def pct(numerator: int) -> float:
        return round(100.0 * numerator / total, 2) if total else 0.0

    metrics: dict[str, object] = {
        "total": total,
        "covered": covered,
        "uncovered": uncovered,
        "coverage_pct": pct(covered),
        "W2": len(w2),
        "W2_multiword": len(w2_multiword),
        "W2_single": len(w2_single),
        "W3a": len(w3a),
        "proper_excluded": proper_all,
        "allowlist_only_coverage_pct": pct(covered_allow),
        # --- consistency / decomposition ---
        "covered_plus_uncovered_check": "PASS"
        if covered + uncovered == total
        else "FAIL",
        "wellformed_rows": int(concepts["wellformed"]),
        "shifted_rows": int(concepts["shifted"]),
        "sixcol_rows": int(concepts["sixcol"]),
        "malformed_len_rows": int(concepts["malformed_len"]),
        "uncovered_wellformed": len(uncovered_wellformed),
        "uncovered_malformed": len(uncovered_malformed),
        "covered_malformed": int(concepts["covered_malformed"]),
        "proper_excluded_wellformed": proper_wellformed,
        "W2_denylist_en_conflicts": len(w2_deny_en),
        "W2_denylist_en_conflict_ids": ",".join(w2_deny_en),
        "W2_id_in_denylist": len(w2_deny_id),
        "W2_zh_in_denylist": len(w2_deny_zh),
        "W2_zh_in_denylist_ids": ",".join(w2_deny_zh),
        # --- cross-audit口径 ---
        "coverage_pct_incl_allowlist": pct(covered_incl),
        "W2_incl_allowlist": len(union_w2),
        "W3a_incl_allowlist": len(union_w3a),
        # --- W1 work sets ---
        "W1_a": len(w1_a),
        "W1_b": len(w1_b),
        "W1_c": len(w1_c),
        "en_boilerplate_concepts": len(defs.en_boilerplate),
        "zh_corrupt_concepts": len(defs.zh_corrupt),
        # --- provenance ---
        "terms_file": str(paths["terms_file"]),
        "terms_file_entries": len(terms),
        "concepts_file": str(paths["concepts"]),
        "definitions_available": defs.available,
    }

    inputs: dict[str, object] = {}
    for name, path in paths.items():
        entry: dict[str, object] = {"path": str(path)}
        if path.exists():
            entry["sha256"] = sha256_file(path)
            entry["bytes"] = path.stat().st_size
        else:
            entry["sha256"] = None
        inputs[name] = entry

    work_sets: dict[str, object] = {
        "W2": list(w2_ids),
        "W3a": list(w3_ids),
        "W1_a": list(w1_a),
        "W1_b": list(w1_b),
        "W1_c": list(w1_c),
        "uncovered": uncovered_ids,
        "covered": covered_ids,
        "uncovered_malformed": [
            {"concept_id": r.concept_id, "kind": r.kind, "line_no": r.line_no}
            for r in uncovered_malformed
        ],
    }

    hit_reasons: dict[str, dict[str, object]] = {
        name: {"count": hit_counts[name], "examples": hit_examples[name]}
        for name in hit_counts
    }

    report: dict[str, object] = {
        "schema": SCHEMA,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        **metrics,
        "coverage_hit_reasons": hit_reasons,
        "proper_excluded_by_category": proper_by_category,
        "inputs": inputs,
        "work_sets": work_sets,
    }
    groups: dict[str, tuple[str, ...]] = {
        "w1_a": w1_a,
        "w1_b": w1_b,
        "w1_c": w1_c,
        "w2": w2_ids,
        "w3": w3_ids,
    }
    return metrics, report, groups


STDOUT_ORDER = (
    "total",
    "covered",
    "uncovered",
    "coverage_pct",
    "W2",
    "W2_multiword",
    "W2_single",
    "W3a",
    "proper_excluded",
    "allowlist_only_coverage_pct",
    "coverage_pct_incl_allowlist",
    "covered_plus_uncovered_check",
    "wellformed_rows",
    "shifted_rows",
    "sixcol_rows",
    "uncovered_wellformed",
    "uncovered_malformed",
    "covered_malformed",
    "proper_excluded_wellformed",
    "W2_denylist_en_conflicts",
    "W2_denylist_en_conflict_ids",
    "W2_id_in_denylist",
    "W2_zh_in_denylist",
    "W2_zh_in_denylist_ids",
    "W2_incl_allowlist",
    "W3a_incl_allowlist",
    "W1_a",
    "W1_b",
    "W1_c",
    "en_boilerplate_concepts",
    "zh_corrupt_concepts",
    "terms_file",
    "terms_file_entries",
    "concepts_file",
    "definitions_available",
)


def emit_lists(
    directory: Path, batch_size: int, groups: dict[str, tuple[str, ...]]
) -> list[Path]:
    directory.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for name, ids in groups.items():
        main = directory / f"{name}.ids"
        main.write_text("".join(f"{cid}\n" for cid in ids), encoding="utf-8")
        written.append(main)
        batches = chunk(ids, batch_size)
        width = max(2, len(str(len(batches))))
        for idx, batch in enumerate(batches, 1):
            path = directory / f"{name}_b{idx:0{width}d}.ids"
            path.write_text("".join(f"{cid}\n" for cid in batch), encoding="utf-8")
            written.append(path)
    return written


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Canonical registry -> allowlist coverage report (T0.0).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--repo-root", default=".", help="repository root")
    parser.add_argument("--concepts", default=DEFAULT_CONCEPTS)
    parser.add_argument("--aliases", default=DEFAULT_ALIASES)
    parser.add_argument("--definitions", default=DEFAULT_DEFINITIONS)
    parser.add_argument("--allowlist-zh", default=DEFAULT_ALLOWLIST_ZH)
    parser.add_argument("--allowlist-en", default=DEFAULT_ALLOWLIST_EN)
    parser.add_argument("--denylist", default=DEFAULT_DENYLIST)
    parser.add_argument(
        "--terms-file",
        default=DEFAULT_TERMS_FILE,
        help=(
            "coverage denominator word list; override with /dev/null (or the "
            "W1_A_BASELINE snapshot) to prove the rules are corpus-bound"
        ),
    )
    parser.add_argument("--json", metavar="PATH", help="write machine-readable JSON")
    parser.add_argument(
        "--emit-lists",
        metavar="DIR",
        help="write work-set id lists and per-batch chunks into DIR",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=20,
        help="ids per generated batch file (used with --emit-lists)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        metrics, report, groups = build_report(args)
    except InputError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    for key in STDOUT_ORDER:
        print(f"{key}: {metrics[key]}")

    if not report["definitions_available"]:
        print(
            f"WARNING: definitions file not found ({args.definitions}); "
            "W1_a/W1_b/W1_c set to 0 and w1_*.ids not emitted",
            file=sys.stderr,
        )

    if args.json:
        json_path = Path(args.json)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"json_written: {json_path}")

    if args.emit_lists:
        written = emit_lists(Path(args.emit_lists), args.batch_size, groups)
        print(f"emit_lists_dir: {args.emit_lists}")
        print(f"emit_lists_batch_size: {args.batch_size}")
        print(f"emit_lists_files: {len(written)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
