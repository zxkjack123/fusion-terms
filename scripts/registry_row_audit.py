#!/usr/bin/env python3
r"""Structural audit of the fusion-terms registry TSVs (read-only, deterministic, offline).

Purpose
-------
Single source of truth for the *structural* defects catalogued in
``.github/plans/terminology-coverage-and-definition-quality.md`` (§A/§E/§F).
It is simultaneously the RED-evidence producer and the regression counter used
*before* and *after* the W0 registry repair (T0.1 / T0.13).

Metric contract (each number is derived from the corpus, never hard-coded)
-------------------------------------------------------------------------
data row
    A physical line that (a) does not start with ``#`` and (b) is not empty.
    This mirrors the plan's reference rule ``awk -F'\\t' '!/^#/ && NF>0'``.
    1-based physical line numbers are reported as *hints only*; the
    ``concept_id`` lists are the authoritative identifiers, because line
    numbers shift whenever HEAD changes.

concepts (``terms/registry/concepts.tsv``, 8-column schema)
    ``data_rows``          number of data rows (comments + blanks excluded).
    ``cols_dist``          histogram of field counts (JSON keys are strings).
    ``malformed_cols``     data rows whose field count != 8.
    ``bad_category``       8-column data rows whose ``category`` (field 2) is
                           not a member of the 16-value whitelist.
    ``shifted_rows``       ``concept_id`` list of the ``bad_category`` rows
                           (column left-shift signature), plus line hints.
    ``sixcol_rows``        ``concept_id`` list of the 6-column rows (shifted
                           block that lost ``category``/``status``/``source``).
    ``concept_ids_sha256`` sha256 over the sorted **unique** concept_id list,
                           newline-joined with a trailing newline.  This is the
                           anchor proving the repair only changed column
                           structure and neither added nor removed a concept.
                           The sort is by **Unicode code point**, i.e. it is
                           locale independent and reproduces exactly with
                           ``LC_ALL=C sort``.  Reproduce::

                               awk -F'\t' '!/^#/&&NF>0{print $1}' \
                                   terms/registry/concepts.tsv \
                                   | LC_ALL=C sort -u | sha256sum

                           Beware: a bare ``sort -u`` under ``en_US.UTF-8``
                           collation yields a *different* digest because that
                           collation ignores punctuation such as hyphens.
    ``concept_ids_sha256_locale_collate``
                           identical digest computed under the active
                           ``en_US.UTF-8`` collation, reported only so that a
                           bare ``sort -u`` reproduction can be cross-checked.
                           ``null`` when that locale is unavailable.
    ``concept_ids_all_sha256``
                           same hash but over **all** data-row concept_ids
                           (duplicates preserved) -- an extra guard against
                           accidental row duplication introduced by a repair.

evidence (``terms/registry/evidence.tsv``, 5-column schema)
    ``cols_dist``          histogram of field counts.
    ``non5_cols``          data rows whose field count != 5.
    ``glued_source_rows``  rows whose declared ``source`` column (field 2)
                           carries a glued domain suffix, i.e. matches
                           ``^internal:dict-improvements:<domain-id>$``.
    ``glued_any_cell_rows`` cross-check over every cell of the row.

definitions (``terms/registry/definitions.tsv``, 4-column schema)
    ``cols_dist``          histogram of field counts.
    ``en_boilerplate``     ``en`` rows matching the boilerplate template
                           ``Fusion/nuclear engineering term referring to
                           '<X>' in technical context.``
    ``zh_en_corruption``   ``zh`` rows containing the broken fragment ``指“en”``.
    ``concepts_without_defs``
                           active concepts with no definitions row (headline;
                           task wording).  A concept counts as active when its
                           canonical 8-column row has ``status == active``, or
                           when it only ever appears in a non-8-column row
                           (status slot unreliable -> kept, conservatively).
    ``concepts_without_defs_any_status``
                           cross-check over *all* concept_ids (the plan §E5
                           reproduction rule); equals the headline value on the
                           pre-repair corpus.

Gate profiles
-------------
``--expect-clean``
    Gates the **W0 (Phase 0) structural set** only, which is exactly the metric
    list of the plan's "Phase 0 完成定义" (``malformed=0, shifted=0, sixcol=0,
    evidence_cols_non5=0, zh_en_corruption=0`` + the ``bad_category`` /
    ``glued_source_rows`` structural gates).  The two definition-*quality*
    metrics (``en_boilerplate``, ``concepts_without_defs``) are Phase 1 (W1)
    deliverables and therefore cannot block Phase 0 completion; they are
    reported in ``deferred_w1_metrics``.

``--expect-clean-all``
    Gates *every* metric (W0 structural + W1 quality).  This is the stricter
    gate to run at Phase 1 completion; it is a superset of ``--expect-clean``,
    so no metric is ever un-gated by the profile split.

Exit codes
----------
``0``  audit succeeded (and, with a gate flag, every gated metric is 0).
``1``  the requested gate flag found at least one non-zero gated metric.
``2``  input error (missing/unreadable file).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import locale
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONCEPTS = REPO_ROOT / "terms" / "registry" / "concepts.tsv"
DEFAULT_EVIDENCE = REPO_ROOT / "terms" / "registry" / "evidence.tsv"
DEFAULT_DEFINITIONS = REPO_ROOT / "terms" / "registry" / "definitions.tsv"

CONCEPTS_COLS = 8
EVIDENCE_COLS = 5
DEFINITIONS_COLS = 4

CATEGORY_WHITELIST = frozenset(
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

# Boilerplate en definition: fusion/nuclear engineering term referring to '<X>'
# in technical context.  (Plan §E2 / R-4.)
EN_BOILERPLATE_RE = re.compile(
    r"^Fusion/nuclear engineering term referring to '.*' in technical context\.$"
)
# Broken zh template that leaked the literal language tag into the text (§E3).
ZH_EN_CORRUPTION_MARKER = "指“en”"
# `source` column polluted with a glued domain id (§F2).
GLUED_SOURCE_RE = re.compile(r"^internal:dict-improvements:.+$")

# Phase 0 (W0) gate: pure structural integrity of the three registry tables.
# This is exactly the metric list of the plan's "Phase 0 完成定义"
# (`malformed=0, shifted=0, sixcol=0, evidence_cols_non5=0, zh_en_corruption=0`)
# plus the two further structural gates (`bad_category`, `glued_source_rows`).
W0_CLEAN_METRICS = (
    "concepts.malformed_cols",
    "concepts.bad_category",
    "evidence.non5_cols",
    "evidence.glued_source_rows",
    "definitions.zh_en_corruption",
)

# Definition-*quality* metrics that are Phase 1 (W1) deliverables: rewriting the
# 746-row `en` boilerplate and authoring definitions for the 10 concepts that
# have none.  Always reported by `--audit`, but gated only by
# `--expect-clean-all`, because Phase 0 must be able to complete while these are
# still non-zero (they are the W1 work set).
W1_DEFERRED_METRICS = (
    "definitions.en_boilerplate",
    "definitions.concepts_without_defs",
)

# Every gated metric (W0 structural + W1 deferred) — the `--expect-clean-all` set.
CLEAN_METRICS = W0_CLEAN_METRICS + W1_DEFERRED_METRICS


def iter_data_rows(path: Path):
    """Yield ``(lineno, fields)`` for each data row of ``path``.

    A data row is a physical line that does not start with ``#`` and is not
    empty; this mirrors ``awk -F'\\t' '!/^#/ && NF>0'``.  ``lineno`` is 1-based.
    """
    text = path.read_text(encoding="utf-8")
    for lineno, line in enumerate(text.splitlines(), start=1):
        if line.startswith("#") or line == "":
            continue
        yield lineno, line.split("\t")


def _sha256_lines(items: list[str]) -> str:
    digest = hashlib.sha256()
    payload = "\n".join(items)
    if payload:
        payload += "\n"
    digest.update(payload.encode("utf-8"))
    return digest.hexdigest()


def _sorted_with_locale(items: list[str], locale_name: str) -> list[str] | None:
    """Sort ``items`` under an explicit collation, restoring the locale after.

    Returns ``None`` when the requested locale is not installed, so callers can
    degrade gracefully instead of failing the whole audit.
    """
    saved = locale.setlocale(locale.LC_COLLATE)
    try:
        locale.setlocale(locale.LC_COLLATE, locale_name)
    except locale.Error:
        return None
    try:
        return sorted(items, key=locale.strxfrm)
    finally:
        locale.setlocale(locale.LC_COLLATE, saved)


def _contiguous_ranges(numbers: list[int]) -> list[list[int]]:
    ranges: list[list[int]] = []
    for n in numbers:
        if ranges and n == ranges[-1][1] + 1:
            ranges[-1][1] = n
        else:
            ranges.append([n, n])
    return ranges


def audit_concepts(path: Path) -> dict:
    data_rows = 0
    cols_dist: dict[str, int] = {}
    shifted: list[tuple[int, str]] = []
    sixcol: list[tuple[int, str]] = []
    all_ids: list[str] = []
    statuses: dict[str, set[str]] = {}
    ids_with_canonical_row: set[str] = set()

    for lineno, fields in iter_data_rows(path):
        data_rows += 1
        ncols = len(fields)
        cols_dist[str(ncols)] = cols_dist.get(str(ncols), 0) + 1
        concept_id = fields[0]
        if concept_id:
            all_ids.append(concept_id)

        if ncols == CONCEPTS_COLS:
            ids_with_canonical_row.add(concept_id)
            statuses.setdefault(concept_id, set()).add(fields[5])
            if fields[1] not in CATEGORY_WHITELIST:
                shifted.append((lineno, concept_id))
        elif ncols == 6:
            sixcol.append((lineno, concept_id))

    malformed_cols = data_rows - cols_dist.get(str(CONCEPTS_COLS), 0)
    unique_ids = sorted(set(all_ids))
    locale_sorted = _sorted_with_locale(unique_ids, "en_US.UTF-8")

    # Conservative "active" definition: canonical row says active, or the
    # concept only ever shows up in a non-canonical row (status unknowable).
    active_ids = set()
    for concept_id in set(all_ids):
        if "active" in statuses.get(concept_id, set()):
            active_ids.add(concept_id)
        elif concept_id not in ids_with_canonical_row:
            active_ids.add(concept_id)

    shifted_linenos = [lineno for lineno, _ in shifted]
    sixcol_linenos = [lineno for lineno, _ in sixcol]

    return {
        "path": str(path),
        "data_rows": data_rows,
        "cols_dist": dict(sorted(cols_dist.items(), key=lambda kv: int(kv[0]))),
        "malformed_cols": malformed_cols,
        "bad_category": len(shifted),
        "shifted_rows": {
            "count": len(shifted),
            "concept_ids": sorted({concept_id for _, concept_id in shifted}),
            "line_numbers_min": min(shifted_linenos) if shifted_linenos else None,
            "line_numbers_max": max(shifted_linenos) if shifted_linenos else None,
            "line_ranges": _contiguous_ranges(shifted_linenos),
            "note": "line numbers are hints only; concept_ids are authoritative",
        },
        "sixcol_rows": {
            "count": len(sixcol),
            "concept_ids": sorted({concept_id for _, concept_id in sixcol}),
            "line_numbers_min": min(sixcol_linenos) if sixcol_linenos else None,
            "line_numbers_max": max(sixcol_linenos) if sixcol_linenos else None,
            "line_ranges": _contiguous_ranges(sixcol_linenos),
            "note": "line numbers are hints only; concept_ids are authoritative",
        },
        "concept_ids_unique": len(unique_ids),
        "concept_ids_sha256": _sha256_lines(unique_ids),
        "concept_ids_sha256_locale_collate": (
            _sha256_lines(locale_sorted) if locale_sorted is not None else None
        ),
        "concept_ids_all_sha256": _sha256_lines(sorted(all_ids)),
        "concept_ids_sha256_spec": (
            "sha256 over '\\n'.join(sorted(set(concept_ids))) + '\\n'; "
            "sort is by Unicode code point (locale independent, == LC_ALL=C sort)"
        ),
        # internal helper consumed by the definitions audit (not a metric)
        "_active_ids": sorted(active_ids),
        "_universe_ids": unique_ids,
    }


def audit_evidence(path: Path) -> dict:
    data_rows = 0
    cols_dist: dict[str, int] = {}
    non5_cols = 0
    glued_source_rows = 0
    glued_any_cell_rows = 0

    for _lineno, fields in iter_data_rows(path):
        data_rows += 1
        ncols = len(fields)
        cols_dist[str(ncols)] = cols_dist.get(str(ncols), 0) + 1
        if ncols != EVIDENCE_COLS:
            non5_cols += 1
        if len(fields) > 1 and GLUED_SOURCE_RE.match(fields[1]):
            glued_source_rows += 1
        if any(GLUED_SOURCE_RE.match(cell) for cell in fields):
            glued_any_cell_rows += 1

    return {
        "path": str(path),
        "data_rows": data_rows,
        "cols_dist": dict(sorted(cols_dist.items(), key=lambda kv: int(kv[0]))),
        "non5_cols": non5_cols,
        "glued_source_rows": glued_source_rows,
        "glued_any_cell_rows": glued_any_cell_rows,
    }


def audit_definitions(path: Path, active_ids: set[str], universe_ids: set[str]) -> dict:
    data_rows = 0
    cols_dist: dict[str, int] = {}
    en_boilerplate = 0
    zh_en_corruption = 0
    defined_ids: set[str] = set()

    for _lineno, fields in iter_data_rows(path):
        data_rows += 1
        ncols = len(fields)
        cols_dist[str(ncols)] = cols_dist.get(str(ncols), 0) + 1
        if ncols < 3:
            continue
        concept_id, lang, definition = fields[0], fields[1], fields[2]
        defined_ids.add(concept_id)
        if lang == "en" and EN_BOILERPLATE_RE.match(definition):
            en_boilerplate += 1
        if lang == "zh" and ZH_EN_CORRUPTION_MARKER in definition:
            zh_en_corruption += 1

    missing_active = sorted(active_ids - defined_ids)
    missing_any = sorted(universe_ids - defined_ids)

    return {
        "path": str(path),
        "data_rows": data_rows,
        "cols_dist": dict(sorted(cols_dist.items(), key=lambda kv: int(kv[0]))),
        "en_boilerplate": en_boilerplate,
        "zh_en_corruption": zh_en_corruption,
        "concepts_without_defs": len(missing_active),
        "concepts_without_defs_ids": missing_active,
        "concepts_without_defs_any_status": len(missing_any),
        "concepts_without_defs_any_status_ids": missing_any,
    }


def _flatten(metrics: dict) -> dict[str, int]:
    return {
        "concepts.malformed_cols": metrics["concepts"]["malformed_cols"],
        "concepts.bad_category": metrics["concepts"]["bad_category"],
        "evidence.non5_cols": metrics["evidence"]["non5_cols"],
        "evidence.glued_source_rows": metrics["evidence"]["glued_source_rows"],
        "definitions.en_boilerplate": metrics["definitions"]["en_boilerplate"],
        "definitions.zh_en_corruption": metrics["definitions"]["zh_en_corruption"],
        "definitions.concepts_without_defs": metrics["definitions"][
            "concepts_without_defs"
        ],
    }


def run_audit(concepts_path: Path, evidence_path: Path, definitions_path: Path) -> dict:
    concepts = audit_concepts(concepts_path)
    active_ids = set(concepts.pop("_active_ids"))
    universe_ids = set(concepts.pop("_universe_ids"))
    evidence = audit_evidence(evidence_path)
    definitions = audit_definitions(definitions_path, active_ids, universe_ids)

    metrics: dict[str, Any] = {
        "concepts": concepts,
        "evidence": evidence,
        "definitions": definitions,
    }
    flat = _flatten(metrics)
    metrics["clean_metrics"] = flat
    metrics["non_zero_metrics"] = {
        key: value for key, value in flat.items() if value != 0
    }
    metrics["is_clean"] = not metrics["non_zero_metrics"]
    # Gate profiles: W0 (structural, gates `--expect-clean`) and W1-deferred
    # (definition quality, gates `--expect-clean-all` together with W0).
    metrics["w0_clean_metrics"] = {key: flat.get(key, 0) for key in W0_CLEAN_METRICS}
    metrics["w0_non_zero_metrics"] = {
        key: value for key, value in metrics["w0_clean_metrics"].items() if value != 0
    }
    metrics["w0_is_clean"] = not metrics["w0_non_zero_metrics"]
    metrics["deferred_w1_metrics"] = {
        key: flat.get(key, 0) for key in W1_DEFERRED_METRICS
    }
    return metrics


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Structural audit of terms/registry/{concepts,evidence,definitions}.tsv "
            "(read-only, deterministic, offline)."
        )
    )
    parser.add_argument(
        "--audit",
        action="store_true",
        help="print the audit result as JSON on stdout (default action)",
    )
    parser.add_argument(
        "--expect-clean",
        action="store_true",
        help=(
            "exit 0 only when every W0 (structural) gate metric is 0; otherwise "
            "exit 1 and echo the non-zero metrics on stderr. Definition-quality "
            "metrics (en_boilerplate, concepts_without_defs) are Phase 1 work and "
            "are reported as deferred_w1_metrics instead of gated here."
        ),
    )
    parser.add_argument(
        "--expect-clean-all",
        action="store_true",
        help=(
            "stricter gate: exit 0 only when every metric is 0, i.e. the W0 "
            "structural set plus the W1 definition-quality metrics"
        ),
    )
    parser.add_argument(
        "--json",
        type=Path,
        default=None,
        metavar="PATH",
        help="also write the audit result as JSON to PATH",
    )
    parser.add_argument(
        "--concepts",
        type=Path,
        default=DEFAULT_CONCEPTS,
        metavar="PATH",
        help="override concepts.tsv path",
    )
    parser.add_argument(
        "--evidence",
        type=Path,
        default=DEFAULT_EVIDENCE,
        metavar="PATH",
        help="override evidence.tsv path",
    )
    parser.add_argument(
        "--definitions",
        type=Path,
        default=DEFAULT_DEFINITIONS,
        metavar="PATH",
        help="override definitions.tsv path",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    for path in (args.concepts, args.evidence, args.definitions):
        if not path.is_file():
            print(f"registry_row_audit: input not found: {path}", file=sys.stderr)
            return 2

    try:
        metrics = run_audit(args.concepts, args.evidence, args.definitions)
    except OSError as exc:  # pragma: no cover - defensive I/O guard
        print(f"registry_row_audit: I/O error: {exc}", file=sys.stderr)
        return 2

    payload = json.dumps(metrics, ensure_ascii=False, indent=2, sort_keys=True)
    print(payload)

    if args.json is not None:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(payload + "\n", encoding="utf-8")

    if args.expect_clean and not metrics["w0_is_clean"]:
        non_zero = metrics["w0_non_zero_metrics"]
        print(
            f"registry_row_audit: --expect-clean FAILED — "
            f"{len(non_zero)} non-zero W0 structural metric(s):",
            file=sys.stderr,
        )
        for key in W0_CLEAN_METRICS:
            if key in non_zero:
                print(f"  {key} = {non_zero[key]}", file=sys.stderr)
        deferred = {k: v for k, v in metrics["deferred_w1_metrics"].items() if v != 0}
        if deferred:
            print(
                "  (deferred to W1, not gated here: "
                + ", ".join(f"{k} = {v}" for k, v in deferred.items())
                + ")",
                file=sys.stderr,
            )
        return 1

    if args.expect_clean_all and not metrics["is_clean"]:
        non_zero = metrics["non_zero_metrics"]
        print(
            f"registry_row_audit: --expect-clean-all FAILED — "
            f"{len(non_zero)} non-zero metric(s):",
            file=sys.stderr,
        )
        for key in CLEAN_METRICS:
            if key in non_zero:
                print(f"  {key} = {non_zero[key]}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
