from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


_GREEK_ROMANIZATION: dict[str, str] = {
    "α": "alpha",
    "β": "beta",
    "γ": "gamma",
    "δ": "delta",
    "ε": "epsilon",
    "κ": "kappa",
    "λ": "lambda",
    "μ": "mu",
    "ν": "nu",
    "π": "pi",
    "ρ": "rho",
    "σ": "sigma",
    "τ": "tau",
    "φ": "phi",
    "χ": "chi",
    "ω": "omega",
    "Ω": "Omega",
}


def _is_zh_term(t: str) -> bool:
    return any("\u4e00" <= ch <= "\u9fff" for ch in t)


def _has_non_ascii_non_zh(t: str) -> bool:
    """True if the term contains non-ASCII chars that are not CJK."""
    for ch in t:
        if ord(ch) < 128:
            continue
        if "\u4e00" <= ch <= "\u9fff":
            continue
        return True
    return False


def _typing_hints_for_term(t: str) -> list[str]:
    """Best-effort typing hints for symbol-heavy/non-ASCII (non-CJK) terms.

    Notes:
    - Hints are *suggestions*; actual triggerability depends on the user's schema.
    - We intentionally only generate hints for non-ASCII non-CJK terms to keep
      output focused.
    """

    if _is_zh_term(t):
        return []
    if not _has_non_ascii_non_zh(t):
        return []

    romanized = "".join(_GREEK_ROMANIZATION.get(ch, ch) for ch in t)
    ascii_only = "".join(ch for ch in romanized if ord(ch) < 128)

    hints: list[str] = []

    def _add(x: str) -> None:
        s = x.strip()
        if not s:
            return
        if s not in hints:
            hints.append(s)

    _add(ascii_only)
    _add(ascii_only.lower())
    _add(ascii_only.replace("_", ""))
    _add(ascii_only.lower().replace("_", ""))
    _add(ascii_only.replace("-", ""))
    _add(ascii_only.lower().replace("-", ""))
    _add(ascii_only.replace("/", ""))
    _add(ascii_only.lower().replace("/", ""))

    return hints


def _load_wordlist(path: Path) -> list[str]:
    if not path.exists():
        raise SystemExit(f"wordlist not found: {path}")
    terms: list[str] = []
    try:
        lines = path.read_text("utf-8").splitlines()
    except UnicodeDecodeError as e:
        raise SystemExit(
            f"IME acceptance pack failed: input is not valid UTF-8: {path} ({e}). "
            "Tip: regenerate artifacts with pipeline.build_terms."
        ) from e

    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        terms.append(s)
    # De-dup but preserve order.
    seen: set[str] = set()
    out: list[str] = []
    for t in terms:
        if t in seen:
            continue
        seen.add(t)
        out.append(t)
    return out


DEFAULT_MUST_HAVE = [
    # Devices / facilities
    "ITER",
    "EAST",
    "JET",
    "DIII-D",
    # Acronyms / regimes
    "NBI",
    "ICRH",
    "ECRH",
    "ELM",
    "H-mode",
    # Phrase components (token-level)
    "neutral",
    "beam",
    "injection",
    # Materials / mixed
    "Nb3Sn",
    "CuCrZr",
    "tungsten",
    "beryllium",
    "D-T",
    "W/Be",
    # Parameters / symbols
    "q95",
    "β_N",
    "τ_E",
    # Chinese
    "托卡马克",
    "等离子体",
]


def build_acceptance_pack(
    *,
    wordlist_path: Path,
    out_json: Path,
    out_terms_txt: Path,
    out_hints_tsv: Path,
    out_report_md: Path,
    report_date: str,
    must_have: list[str],
    pick_n: int,
) -> dict[str, object]:
    terms_ordered = _load_wordlist(wordlist_path)
    terms_set = set(terms_ordered)

    zh = [t for t in terms_ordered if _is_zh_term(t)]
    en = [t for t in terms_ordered if t not in set(zh)]

    checks: list[dict[str, object]] = []
    missing: list[str] = []
    for t in must_have:
        ok = t in terms_set
        checks.append({"term": t, "in_wordlist": ok})
        if not ok:
            missing.append(t)

    # Deterministic suggested typing list:
    # - must-have first (in the given order)
    # - then fill with additional terms from the wordlist (lexicographic)
    # Note: we never truncate must-have terms; if pick_n is smaller than
    # len(must_have), we raise it to keep the acceptance list intact.
    target_n = max(int(pick_n), len(must_have))
    suggested: list[str] = []
    seen: set[str] = set()
    for t in must_have:
        if t not in seen:
            seen.add(t)
            suggested.append(t)

    extras = sorted([t for t in terms_set if t not in seen])
    for t in extras:
        if len(suggested) >= target_n:
            break
        suggested.append(t)

    typing_hints: dict[str, list[str]] = {}
    for t in suggested:
        hints = _typing_hints_for_term(t)
        if hints:
            typing_hints[t] = hints

    pack = {
        "schema_version": 1,
        "wordlist": str(wordlist_path),
        "outputs": {
            "json": str(out_json),
            "typing_terms": str(out_terms_txt),
            "typing_hints_tsv": str(out_hints_tsv),
            "report_md": str(out_report_md),
        },
        "counts": {
            "total": len(terms_set),
            "zh": len(set(zh)),
            "en": len(set(en)),
            "must_have": len(must_have),
            "missing_must_have": len(missing),
            "suggested_typing_terms": len(suggested),
            "typing_hints_terms": len(typing_hints),
        },
        "must_have": must_have,
        "checks": checks,
        "missing_must_have": missing,
        "suggested_typing_terms": suggested,
        "typing_hints": typing_hints,
    }

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(
        json.dumps(pack, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    out_terms_txt.parent.mkdir(parents=True, exist_ok=True)
    out_terms_txt.write_text("\n".join(suggested) + "\n", encoding="utf-8")

    out_hints_tsv.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = ["term\thints"]
    for t in suggested:
        term_hints = typing_hints.get(t)
        if not term_hints:
            continue
        lines.append(f"{t}\t{'|'.join(term_hints)}")
    out_hints_tsv.write_text("\n".join(lines) + "\n", encoding="utf-8")

    out_report_md.parent.mkdir(parents=True, exist_ok=True)
    report_lines: list[str] = []
    report_lines.append("# IME manual acceptance report")
    report_lines.append("")
    report_lines.append(f"- generated_date: {report_date}")
    report_lines.append(f"- wordlist: {wordlist_path}")
    report_lines.append(f"- pack_json: {out_json}")
    report_lines.append(f"- typing_terms: {out_terms_txt}")
    report_lines.append(f"- typing_hints_tsv: {out_hints_tsv}")
    report_lines.append("")
    report_lines.append("## Pre-checks (wordlist presence)")
    report_lines.append("")
    report_lines.append(f"- must_have: {len(must_have)}")
    report_lines.append(f"- missing_must_have: {len(missing)}")
    if missing:
        report_lines.append("")
        report_lines.append("Missing terms (must fix before IME testing):")
        for t in missing:
            report_lines.append(f"- {t}")

    report_lines.append("")
    report_lines.append("## Manual IME trigger checklist (fill in)")
    report_lines.append("")
    report_lines.append("> Tips: test each term in a real input field after import/deploy; if a term is hard to type, consider adding an alias mapping in your schema/dict.")
    report_lines.append("")

    must_have_set = set(must_have)
    for t in suggested:
        mark = "must-have" if t in must_have_set else "extra"
        term_hints = typing_hints.get(t)
        if term_hints:
            report_lines.append(
                f"- [ ] {t} ({mark}; hints: {' | '.join(term_hints)})"
            )
        else:
            report_lines.append(f"- [ ] {t} ({mark})")

    out_report_md.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    return pack


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate an IME manual acceptance pack (JSON + typing list) from a built wordlist."
        )
    )
    parser.add_argument(
        "--wordlist",
        default="artifacts/domain_terms.txt",
        help="Built wordlist path (default: artifacts/domain_terms.txt)",
    )
    parser.add_argument(
        "--out-dir",
        default="artifacts",
        help="Output directory for acceptance pack artifacts (default: artifacts)",
    )
    parser.add_argument(
        "--out-json",
        default=None,
        help="Optional JSON output path (default: <out-dir>/ime_acceptance_pack.json)",
    )
    parser.add_argument(
        "--out-terms",
        default=None,
        help=(
            "Optional typing-terms output path (default: <out-dir>/ime_acceptance_terms.txt)"
        ),
    )
    parser.add_argument(
        "--out-hints-tsv",
        default=None,
        help=(
            "Optional typing-hints TSV output path (default: <out-dir>/ime_acceptance_terms_hints.tsv)"
        ),
    )
    parser.add_argument(
        "--out-report",
        default=None,
        help=(
            "Optional Markdown report output path (default: <out-dir>/ime_acceptance_report.md)"
        ),
    )
    parser.add_argument(
        "--report-date",
        default=None,
        help=(
            "Optional report date string for ime_acceptance_report.md (default: today, YYYY-MM-DD). "
            "Useful for deterministic tests."
        ),
    )
    parser.add_argument(
        "--must-have",
        action="append",
        default=[],
        help="Must-have term to check (repeatable). If omitted, uses a default list.",
    )
    parser.add_argument(
        "--pick-n",
        type=int,
        default=30,
        help=(
            "Target number of terms in suggested_typing_terms (default: 30). "
            "Will be raised to at least len(must_have) to avoid truncating must-have terms."
        ),
    )

    args = parser.parse_args()

    wordlist_path = Path(args.wordlist).expanduser()
    out_dir = Path(args.out_dir).expanduser()
    out_json = (
        Path(args.out_json).expanduser()
        if args.out_json
        else (out_dir / "ime_acceptance_pack.json")
    )
    out_terms = (
        Path(args.out_terms).expanduser()
        if args.out_terms
        else (out_dir / "ime_acceptance_terms.txt")
    )
    out_hints_tsv = (
        Path(args.out_hints_tsv).expanduser()
        if args.out_hints_tsv
        else (out_dir / "ime_acceptance_terms_hints.tsv")
    )
    out_report_md = (
        Path(args.out_report).expanduser()
        if args.out_report
        else (out_dir / "ime_acceptance_report.md")
    )

    report_date = str(args.report_date) if args.report_date else date.today().isoformat()

    must_have = [str(x) for x in (args.must_have or [])]
    if not must_have:
        must_have = list(DEFAULT_MUST_HAVE)

    pack = build_acceptance_pack(
        wordlist_path=wordlist_path,
        out_json=out_json,
        out_terms_txt=out_terms,
        out_hints_tsv=out_hints_tsv,
        out_report_md=out_report_md,
        report_date=report_date,
        must_have=must_have,
        pick_n=int(args.pick_n),
    )

    counts_obj = pack.get("counts") if isinstance(pack, dict) else None
    missing_must_have = "unknown"
    typing_terms = "unknown"
    if isinstance(counts_obj, dict):
        missing_must_have = str(counts_obj.get("missing_must_have", "unknown"))
        typing_terms = str(counts_obj.get("suggested_typing_terms", "unknown"))

    print(
        "ime acceptance pack written: "
        f"missing_must_have={missing_must_have} "
        f"typing_terms={typing_terms}"
    )


if __name__ == "__main__":
    main()
