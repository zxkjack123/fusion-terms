from __future__ import annotations

import argparse
import csv
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

LEDGER_FILENAME = "proper_names.txt"
EXCLUDE_MARKER = "# --- EXCLUDE_FROM_IME ---"
ALLOW_MARKER = "# --- ALLOW_IN_IME ---"
PROPER_CATEGORIES = frozenset({"company", "organization", "facility"})


class LedgerError(RuntimeError):
    """Malformed proper-name ledger or registry input."""


@dataclass(frozen=True)
class Ledger:
    path: Path
    exclude: dict[str, str]
    allow: dict[str, str]

    @property
    def exclude_terms(self) -> set[str]:
        return set(self.exclude)


def parse_ledger_text(
    text: str, *, source: str = "<ledger>"
) -> tuple[dict[str, str], dict[str, str]]:
    exclude: dict[str, str] = {}
    allow: dict[str, str] = {}
    section: dict[str, str] | None = None
    seen_markers: set[str] = set()

    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        if line == EXCLUDE_MARKER:
            section = exclude
            seen_markers.add(EXCLUDE_MARKER)
            continue
        if line == ALLOW_MARKER:
            section = allow
            seen_markers.add(ALLOW_MARKER)
            continue
        if line.startswith("#"):
            continue
        if section is None:
            raise LedgerError(
                f"{source}:{lineno}: entry appears before a section marker"
            )
        term, separator, reason = line.partition("\t")
        term = term.strip()
        reason = reason.strip()
        if not separator or not term or not reason:
            raise LedgerError(f"{source}:{lineno}: entries must be '<term>\\t<reason>'")
        if term in exclude or term in allow:
            raise LedgerError(f"{source}:{lineno}: duplicate ledger term: {term!r}")
        section[term] = reason

    missing = {EXCLUDE_MARKER, ALLOW_MARKER} - seen_markers
    if missing:
        raise LedgerError(f"{source}: missing section marker(s): {sorted(missing)!r}")
    return exclude, allow


def load_ledger(path: Path) -> Ledger:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise LedgerError(f"failed to read ledger {path}: {exc}") from exc
    exclude, allow = parse_ledger_text(text, source=str(path))
    return Ledger(path=path, exclude=exclude, allow=allow)


def load_proper_name_strings(concepts_path: Path) -> dict[str, list[str]]:
    if not concepts_path.exists():
        raise LedgerError(f"missing concepts file: {concepts_path}")
    result: dict[str, list[str]] = {}
    try:
        rows = csv.reader(
            concepts_path.read_text(encoding="utf-8").splitlines(), delimiter="\t"
        )
        for row in rows:
            if not row or row[0].lstrip().startswith("#") or len(row) < 4:
                continue
            concept_id, category, preferred_zh, preferred_en = row[:4]
            if category not in PROPER_CATEGORIES:
                continue
            for field_name, term in (
                ("preferred_zh", preferred_zh.strip()),
                ("preferred_en", preferred_en.strip()),
            ):
                if term:
                    result.setdefault(term, []).append(f"{concept_id}:{field_name}")
    except (OSError, UnicodeError) as exc:
        raise LedgerError(
            f"failed to read concepts file {concepts_path}: {exc}"
        ) from exc
    return result


def _load_terms(path: Path) -> set[str]:
    if not path.exists():
        raise LedgerError(f"missing wordlist file: {path}")
    try:
        return {
            line.strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
    except (OSError, UnicodeError) as exc:
        raise LedgerError(f"failed to read wordlist {path}: {exc}") from exc


def _preview(prefix: str, values: set[str], *, limit: int = 20) -> list[str]:
    ordered = sorted(values)
    lines = [f"{prefix}: {value!r}" for value in ordered[:limit]]
    if len(ordered) > limit:
        lines.append(f"{prefix}: ... and {len(ordered) - limit} more")
    return lines


def check_ledger(
    *,
    terms_dir: Path,
    ledger_path: Path | None = None,
    concepts_path: Path | None = None,
    wordlist_path: Path = Path("artifacts/domain_terms.txt"),
) -> tuple[list[str], dict[str, int]]:
    ledger = load_ledger(ledger_path or (terms_dir / LEDGER_FILENAME))
    concepts = load_proper_name_strings(
        concepts_path or (terms_dir / "registry" / "concepts.tsv")
    )
    wordlist = _load_terms(wordlist_path)
    allowlists: set[str] = set()
    for name in ("allowlist_zh.txt", "allowlist_en.txt"):
        path = terms_dir / name
        if path.exists():
            allowlists.update(
                line.strip()
                for line in path.read_text(encoding="utf-8").splitlines()
                if line.strip() and not line.lstrip().startswith("#")
            )

    registry_terms = set(concepts)
    ledger_terms = set(ledger.exclude) | set(ledger.allow)
    violations: list[str] = []
    violations.extend(_preview("LEDGER_MISSING_ENTRY", registry_terms - ledger_terms))
    violations.extend(_preview("LEDGER_UNKNOWN_ENTRY", ledger_terms - registry_terms))
    violations.extend(
        _preview("LEDGER_SECTION_OVERLAP", set(ledger.exclude) & set(ledger.allow))
    )
    violations.extend(_preview("WORDLIST_LEAK", wordlist & set(ledger.exclude)))
    violations.extend(
        _preview("ALLOW_NOT_IN_ALLOWLIST", set(ledger.allow) - allowlists)
    )
    violations.extend(_preview("ALLOW_NOT_IN_WORDLIST", set(ledger.allow) - wordlist))
    stats = {
        "registry_terms": len(registry_terms),
        "exclude_terms": len(ledger.exclude),
        "allow_terms": len(ledger.allow),
        "wordlist_terms": len(wordlist),
    }
    return violations, stats


def _write_fixture(root: Path) -> tuple[Path, Path, Path, Path]:
    terms_dir = root / "terms"
    registry = terms_dir / "registry"
    registry.mkdir(parents=True)
    (registry / "concepts.tsv").write_text(
        "# concept_id\tcategory\tpreferred_zh\tpreferred_en\n"
        "acme\tcompany\t艾克米公司\tAcme\n"
        "iaea\torganization\t国际原子能机构\tIAEA\n",
        encoding="utf-8",
    )
    (terms_dir / "allowlist_zh.txt").write_text("国际原子能机构\n", encoding="utf-8")
    (terms_dir / "allowlist_en.txt").write_text("\n", encoding="utf-8")
    ledger = terms_dir / LEDGER_FILENAME
    ledger.write_text(
        "# fixture\n"
        f"{EXCLUDE_MARKER}\n"
        "艾克米公司\tregistry:acme:preferred_zh\n"
        "Acme\tregistry:acme:preferred_en\n"
        "IAEA\tregistry:iaea:preferred_en\n"
        f"{ALLOW_MARKER}\n"
        "国际原子能机构\tretained Chinese organization name\n",
        encoding="utf-8",
    )
    wordlist = root / "domain_terms.txt"
    wordlist.write_text("国际原子能机构\n", encoding="utf-8")
    return terms_dir, ledger, registry / "concepts.tsv", wordlist


def self_test() -> int:
    with tempfile.TemporaryDirectory(prefix="proper-names-self-test-") as raw:
        root = Path(raw)
        terms_dir, ledger, concepts, wordlist = _write_fixture(root)
        violations, _ = check_ledger(
            terms_dir=terms_dir,
            ledger_path=ledger,
            concepts_path=concepts,
            wordlist_path=wordlist,
        )
        if violations:
            print(
                "self-test valid fixture failed:",
                *violations,
                sep="\n",
                file=sys.stderr,
            )
            return 1

        wordlist.write_text("国际原子能机构\n艾克米公司\n", encoding="utf-8")
        violations, _ = check_ledger(
            terms_dir=terms_dir,
            ledger_path=ledger,
            concepts_path=concepts,
            wordlist_path=wordlist,
        )
        if not any(item.startswith("WORDLIST_LEAK") for item in violations):
            print("self-test negative fixture did not fail", file=sys.stderr)
            return 1
        print("proper-name ledger self-test: valid=0, negative=1")
        return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check the proper-name IME ledger.")
    parser.add_argument("--terms-dir", default="terms")
    parser.add_argument("--ledger", default=None)
    parser.add_argument("--concepts", default=None)
    parser.add_argument("--wordlist", default="artifacts/domain_terms.txt")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()

    terms_dir = Path(args.terms_dir).expanduser()
    try:
        violations, stats = check_ledger(
            terms_dir=terms_dir,
            ledger_path=Path(args.ledger).expanduser() if args.ledger else None,
            concepts_path=Path(args.concepts).expanduser() if args.concepts else None,
            wordlist_path=Path(args.wordlist).expanduser(),
        )
    except LedgerError as exc:
        print(f"proper-name ledger input error: {exc}", file=sys.stderr)
        return 2
    if violations:
        print("proper-name ledger check: FAIL", file=sys.stderr)
        print("\n".join(violations), file=sys.stderr)
        return 1
    print(
        "proper-name ledger check: OK "
        f"(registry={stats['registry_terms']}, exclude={stats['exclude_terms']}, "
        f"allow={stats['allow_terms']}, wordlist={stats['wordlist_terms']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
