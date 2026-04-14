from __future__ import annotations

import argparse
import re
import unicodedata
import warnings
from dataclasses import dataclass
from pathlib import Path

from pipeline.common import load_simple_list


CONCEPT_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

# Allowed provenance values for the concepts.tsv ``source`` column.
# Use a prefix-based allowlist so that ``GB/T-4960.x`` variants all pass.
_ALLOWED_SOURCE_PREFIXES = ("corpus", "GB/T-", "ITER-", "IAEA-", "")


@dataclass(frozen=True)
class Row:
    path: Path
    lineno: int
    fields: list[str]


def _iter_tsv_rows(path: Path) -> list[Row]:
    if not path.exists():
        return []

    try:
        lines = path.read_text("utf-8").splitlines()
    except UnicodeDecodeError as e:
        raise SystemExit(
            f"registry validation failed: {path} is not valid UTF-8 ({e}). "
            "Tip: re-save this TSV as UTF-8 without BOM."
        ) from e

    rows: list[Row] = []
    for lineno, line in enumerate(lines, start=1):
        s = line.strip("\n")
        if not s.strip() or s.lstrip().startswith("#"):
            continue
        fields = [c.strip() for c in s.split("\t")]
        rows.append(Row(path=path, lineno=lineno, fields=fields))
    return rows


def _control_or_invisible_desc(s: str) -> list[str]:
    bad: list[str] = []
    for ch in s:
        cat = unicodedata.category(ch)
        if cat.startswith("C"):
            name = unicodedata.name(ch, "<unknown>")
            bad.append(f"U+{ord(ch):04X} {name} ({cat})")
    return bad


def _fail(path: Path, lineno: int, msg: str) -> None:
    raise SystemExit(f"registry validation failed: {path}:{lineno}: {msg}")


def validate_registry(terms_dir: Path) -> None:
    registry_dir = terms_dir / "registry"
    concepts_path = registry_dir / "concepts.tsv"
    aliases_path = registry_dir / "aliases.tsv"
    evidence_path = registry_dir / "evidence.tsv"

    concepts_rows = _iter_tsv_rows(concepts_path)
    aliases_rows = _iter_tsv_rows(aliases_path)
    evidence_rows = _iter_tsv_rows(evidence_path)

    if not concepts_rows:
        raise SystemExit(
            f"registry validation failed: missing or empty {concepts_path}"
        )
    if not aliases_rows:
        raise SystemExit(
            f"registry validation failed: missing or empty {aliases_path}"
        )
    if not evidence_rows:
        raise SystemExit(
            f"registry validation failed: missing or empty {evidence_path}"
        )

    # ---- concepts.tsv ----
    concept_ids: set[str] = set()
    for r in concepts_rows:
        if len(r.fields) < 2:
            _fail(r.path, r.lineno, "expected at least 2 columns: concept_id, category")
        concept_id = r.fields[0]

        bad = _control_or_invisible_desc(concept_id)
        if bad:
            _fail(r.path, r.lineno, f"concept_id contains control/invisible chars: {', '.join(bad)}")

        if not CONCEPT_ID_RE.match(concept_id):
            _fail(
                r.path,
                r.lineno,
                f"invalid concept_id {concept_id!r} (expected lowercase letters/digits with hyphens)",
            )
        if concept_id in concept_ids:
            _fail(r.path, r.lineno, f"duplicate concept_id {concept_id!r}")
        concept_ids.add(concept_id)

        # Validate source column (8th field, index 7) if present.
        source = r.fields[7].strip() if len(r.fields) >= 8 else ""
        if source and not any(source.startswith(pfx) for pfx in _ALLOWED_SOURCE_PREFIXES if pfx):
            warnings.warn(
                f"validate_registry: unknown source {source!r} at "
                f"{r.path}:{r.lineno} (allowed prefixes: {_ALLOWED_SOURCE_PREFIXES})",
                RuntimeWarning,
                stacklevel=2,
            )

    # ---- aliases.tsv ----
    allowed_kinds = {"preferred", "alias", "deprecated", "forbidden"}
    allowed_langs = {"zh", "en", "abbr", "mixed", "unknown"}

    alias_to_concept: dict[str, str] = {}
    forbidden_or_deprecated: set[str] = set()
    concepts_with_preferred: set[str] = set()

    for r in aliases_rows:
        if len(r.fields) < 4:
            _fail(
                r.path,
                r.lineno,
                "expected at least 4 columns: alias, concept_id, lang, kind",
            )
        alias, concept_id, lang, kind = r.fields[0], r.fields[1], r.fields[2], r.fields[3]

        for label, value in [("alias", alias), ("concept_id", concept_id), ("lang", lang), ("kind", kind)]:
            bad = _control_or_invisible_desc(value)
            if bad:
                _fail(r.path, r.lineno, f"{label} contains control/invisible chars: {', '.join(bad)}")

        if not alias:
            _fail(r.path, r.lineno, "alias is empty")
        if concept_id not in concept_ids:
            _fail(r.path, r.lineno, f"unknown concept_id {concept_id!r}")
        if lang not in allowed_langs:
            _fail(r.path, r.lineno, f"invalid lang {lang!r} (allowed: {sorted(allowed_langs)})")
        if kind not in allowed_kinds:
            _fail(r.path, r.lineno, f"invalid kind {kind!r} (allowed: {sorted(allowed_kinds)})")

        if kind in {"forbidden", "deprecated"}:
            forbidden_or_deprecated.add(alias)
        if kind == "preferred":
            concepts_with_preferred.add(concept_id)

        # Alias must map to exactly one concept (avoid drift).
        if alias in alias_to_concept and alias_to_concept[alias] != concept_id:
            _fail(
                r.path,
                r.lineno,
                f"alias {alias!r} maps to multiple concept_ids: {alias_to_concept[alias]!r} and {concept_id!r}",
            )
        alias_to_concept.setdefault(alias, concept_id)

    missing_preferred = sorted(concept_ids - concepts_with_preferred)
    if missing_preferred:
        preview = ", ".join(repr(x) for x in missing_preferred[:10])
        more = "" if len(missing_preferred) <= 10 else f" ... (+{len(missing_preferred) - 10} more)"
        _fail(
            aliases_path,
            1,
            f"concepts without preferred alias: {preview}{more}",
        )

    # ---- evidence.tsv ----
    evidence_concept_ids: set[str] = set()
    for r in evidence_rows:
        if len(r.fields) < 2:
            _fail(r.path, r.lineno, "expected at least 2 columns: concept_id, source")
        concept_id, source = r.fields[0], r.fields[1]

        for label, value in [("concept_id", concept_id), ("source", source)]:
            bad = _control_or_invisible_desc(value)
            if bad:
                _fail(r.path, r.lineno, f"{label} contains control/invisible chars: {', '.join(bad)}")

        if concept_id not in concept_ids:
            _fail(r.path, r.lineno, f"unknown concept_id {concept_id!r}")
        if not source:
            _fail(r.path, r.lineno, "source is empty")
        if source.startswith("internal:TODO"):
            _fail(
                r.path,
                r.lineno,
                f"placeholder evidence source not allowed: {source!r}",
            )
        evidence_concept_ids.add(concept_id)

    missing_evidence = sorted(concept_ids - evidence_concept_ids)
    if missing_evidence:
        preview = ", ".join(repr(x) for x in missing_evidence[:10])
        more = "" if len(missing_evidence) <= 10 else f" ... (+{len(missing_evidence) - 10} more)"
        _fail(
            evidence_path,
            1,
            f"concepts without evidence rows: {preview}{more}",
        )

    # ---- definitions.tsv (optional) ----
    definitions_path = registry_dir / "definitions.tsv"
    definitions_rows = _iter_tsv_rows(definitions_path)
    allowed_def_langs = {"zh", "en"}
    definitions_count = 0
    for r in definitions_rows:
        if len(r.fields) < 3:
            _fail(r.path, r.lineno, "expected at least 3 columns: concept_id, lang, definition")
        cid, lang, defn = r.fields[0], r.fields[1], r.fields[2]
        if cid not in concept_ids:
            _fail(r.path, r.lineno, f"unknown concept_id {cid!r}")
        if lang not in allowed_def_langs:
            _fail(r.path, r.lineno, f"invalid lang {lang!r} (allowed: {sorted(allowed_def_langs)})")
        if not defn:
            _fail(r.path, r.lineno, "definition is empty")
        definitions_count += 1

    # ---- bridge check: forbidden/deprecated shouldn't leak into IME allowlists ----
    allow_zh = load_simple_list(terms_dir / "allowlist_zh.txt")
    allow_en = load_simple_list(terms_dir / "allowlist_en.txt")
    forbidden_lower = {t.lower() for t in forbidden_or_deprecated}
    allow_lower_to_orig: dict[str, str] = {}
    for t in allow_zh | allow_en:
        low = t.lower()
        if low not in allow_lower_to_orig:
            allow_lower_to_orig[low] = t
    leaked_lower = sorted(forbidden_lower & set(allow_lower_to_orig))
    leaked = [allow_lower_to_orig[lk] for lk in leaked_lower]
    if leaked:
        preview = "\n".join(f"- {t!r}" for t in leaked[:20])
        more = "" if len(leaked) <= 20 else f"\n... and {len(leaked) - 20} more"
        raise SystemExit(
            "registry validation failed: forbidden/deprecated aliases must not appear in IME allowlists\n"
            f"offending terms:\n{preview}{more}"
        )

    summary = (
        f"registry OK: "
        f"{len(concept_ids)} concepts, {len(alias_to_concept)} aliases, {len(evidence_rows)} evidence rows"
    )
    if definitions_count:
        summary += f", {definitions_count} definitions"
    print(summary)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate terminology registry tables under terms/registry/*.tsv"
    )
    parser.add_argument(
        "--terms-dir",
        default="terms",
        help="Directory containing allowlists and registry/",
    )
    args = parser.parse_args()

    validate_registry(Path(args.terms_dir))


if __name__ == "__main__":
    main()
