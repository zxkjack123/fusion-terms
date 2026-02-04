from __future__ import annotations

import argparse
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

from pipeline.common import load_simple_list


CONCEPT_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass(frozen=True)
class Row:
    path: Path
    lineno: int
    fields: list[str]


def _iter_tsv_rows(path: Path) -> list[Row]:
    if not path.exists():
        return []

    rows: list[Row] = []
    for lineno, line in enumerate(path.read_text("utf-8", errors="ignore").splitlines(), start=1):
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

    # ---- aliases.tsv ----
    allowed_kinds = {"preferred", "alias", "deprecated", "forbidden"}
    allowed_langs = {"zh", "en", "abbr", "mixed", "unknown"}

    alias_to_concept: dict[str, str] = {}
    forbidden_or_deprecated: set[str] = set()

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

        # Alias must map to exactly one concept (avoid drift).
        if alias in alias_to_concept and alias_to_concept[alias] != concept_id:
            _fail(
                r.path,
                r.lineno,
                f"alias {alias!r} maps to multiple concept_ids: {alias_to_concept[alias]!r} and {concept_id!r}",
            )
        alias_to_concept.setdefault(alias, concept_id)

    # ---- evidence.tsv ----
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

    # ---- bridge check: forbidden/deprecated shouldn't leak into IME allowlists ----
    allow_zh = load_simple_list(terms_dir / "allowlist_zh.txt")
    allow_en = load_simple_list(terms_dir / "allowlist_en.txt")
    leaked = sorted((forbidden_or_deprecated & (allow_zh | allow_en)))
    if leaked:
        preview = "\n".join(f"- {t!r}" for t in leaked[:20])
        more = "" if len(leaked) <= 20 else f"\n... and {len(leaked) - 20} more"
        raise SystemExit(
            "registry validation failed: forbidden/deprecated aliases must not appear in IME allowlists\n"
            f"offending terms:\n{preview}{more}"
        )

    print(
        "registry OK: "
        f"{len(concept_ids)} concepts, {len(alias_to_concept)} aliases, {len(evidence_rows)} evidence rows"
    )


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
