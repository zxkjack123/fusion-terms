from __future__ import annotations

import argparse
import os
import re
import tempfile
import unicodedata
import warnings
from dataclasses import dataclass
from pathlib import Path

from pipeline.common import ensure_dir, load_simple_list, load_synonyms_tsv


WHITESPACE_RE = re.compile(r"\s")


@dataclass(frozen=True)
class Decision:
    action: str
    value: str
    preferred: str
    lang: str
    comment: str


AUTO_MARKER = "# --- AUTO-INBOX (managed by pipeline.apply_decisions)"


def _control_or_invisible_desc(s: str) -> list[str]:
    bad: list[str] = []
    for ch in s:
        cat = unicodedata.category(ch)
        if cat.startswith("C"):
            name = unicodedata.name(ch, "<unknown>")
            bad.append(f"U+{ord(ch):04X} {name} ({cat})")
    return bad


def _validate_token(s: str, *, label: str, path: Path, lineno: int) -> None:
    if not s:
        raise SystemExit(f"decisions apply failed: {path}:{lineno}: {label} is empty")
    if WHITESPACE_RE.search(s):
        raise SystemExit(
            f"decisions apply failed: {path}:{lineno}: {label} must be token-only (no whitespace): {s!r}"
        )
    bad = _control_or_invisible_desc(s)
    if bad:
        raise SystemExit(
            f"decisions apply failed: {path}:{lineno}: {label} contains control/invisible chars: {', '.join(bad)}"
        )


def _parse_decisions(path: Path) -> list[Decision]:
    if not path.exists():
        raise SystemExit(f"decisions apply failed: missing decisions file: {path}")

    out: list[Decision] = []
    try:
        lines = path.read_text("utf-8").splitlines()
    except UnicodeDecodeError as e:
        raise SystemExit(
            f"decisions apply failed: {path} is not valid UTF-8 ({e}). "
            "Tip: re-save this file as UTF-8 without BOM."
        ) from e

    for lineno, line in enumerate(lines, start=1):
        s = line.strip("\n")
        if not s.strip() or s.lstrip().startswith("#"):
            continue
        parts = [c.strip() for c in s.split("\t")]
        if len(parts) < 2:
            raise SystemExit(
                f"decisions apply failed: {path}:{lineno}: expected at least 2 columns: action, value"
            )

        action = parts[0]
        value = parts[1]
        preferred = parts[2] if len(parts) >= 3 else ""
        lang = parts[3] if len(parts) >= 4 else ""
        comment = parts[4] if len(parts) >= 5 else ""

        action_norm = action.strip().lower()
        if action_norm not in {"allow_en", "allow_zh", "deny", "synonym"}:
            raise SystemExit(
                f"decisions apply failed: {path}:{lineno}: unknown action {action!r} (allowed: allow_en, allow_zh, deny, synonym)"
            )

        if action_norm in {"allow_en", "allow_zh", "deny"}:
            _validate_token(value, label="term", path=path, lineno=lineno)
        else:
            _validate_token(value, label="alias", path=path, lineno=lineno)
            _validate_token(preferred, label="preferred", path=path, lineno=lineno)
            if lang:
                _validate_token(lang, label="lang", path=path, lineno=lineno)

        out.append(
            Decision(
                action=action_norm,
                value=value,
                preferred=preferred,
                lang=lang,
                comment=comment,
            )
        )

    return out


def _read_file_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    try:
        return path.read_text("utf-8").splitlines()
    except UnicodeDecodeError as e:
        raise SystemExit(
            f"decisions apply failed: failed to read UTF-8 file: {path} ({e}). "
            "Tip: re-save this file as UTF-8 without BOM."
        ) from e


def _atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=str(path.parent),
    )
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        os.replace(tmp_path, path)
    finally:
        try:
            tmp_path.unlink()
        except FileNotFoundError:
            pass


def _warn_if_manual_content_after_marker(
    *, lines: list[str], idx: int, path: Path
) -> None:
    tail = lines[idx + 1 :]
    has_manual_content = any(
        ln.strip() and not ln.strip().startswith("#") for ln in tail
    )
    if has_manual_content:
        warnings.warn(
            f"content after AUTO_MARKER will be overwritten: {path}",
            UserWarning,
            stacklevel=2,
        )


def _rewrite_auto_inbox_list(path: Path, new_terms: set[str]) -> None:
    """Ensure an AUTO-INBOX block exists and is rewritten deterministically."""

    lines = _read_file_lines(path)

    if not lines:
        # Fresh file.
        content = [AUTO_MARKER]
        content.extend(sorted(new_terms))
        _atomic_write_text(path, "\n".join(content) + "\n")
        return

    if AUTO_MARKER in lines:
        idx = lines.index(AUTO_MARKER)
        _warn_if_manual_content_after_marker(lines=lines, idx=idx, path=path)
        head = lines[: idx + 1]
        # Drop any previous auto-inbox payload (until EOF).
        body = sorted(new_terms)
        _atomic_write_text(path, "\n".join(head + body) + "\n")
        return

    # Append a new auto block at the end.
    out = list(lines)
    if out and out[-1].strip() != "":
        # Ensure there is a blank line before the marker for readability.
        out.append("")
    out.append(AUTO_MARKER)
    out.extend(sorted(new_terms))
    _atomic_write_text(path, "\n".join(out) + "\n")


def _rewrite_auto_inbox_synonyms(
    path: Path, new_pairs: dict[str, tuple[str, str]]
) -> None:
    """Rewrite synonyms AUTO-INBOX block with alias->preferred(+lang) rows."""

    lines = _read_file_lines(path)
    rows = []
    for alias in sorted(new_pairs.keys()):
        preferred, lang = new_pairs[alias]
        if lang:
            rows.append(f"{alias}\t{preferred}\t{lang}")
        else:
            rows.append(f"{alias}\t{preferred}")

    if not lines:
        content = [AUTO_MARKER]
        content.extend(rows)
        _atomic_write_text(path, "\n".join(content) + "\n")
        return

    if AUTO_MARKER in lines:
        idx = lines.index(AUTO_MARKER)
        _warn_if_manual_content_after_marker(lines=lines, idx=idx, path=path)
        head = lines[: idx + 1]
        _atomic_write_text(path, "\n".join(head + rows) + "\n")
        return

    out = list(lines)
    if out and out[-1].strip() != "":
        out.append("")
    out.append(AUTO_MARKER)
    out.extend(rows)
    _atomic_write_text(path, "\n".join(out) + "\n")


def apply_decisions(
    *, terms_dir: Path, decisions_path: Path, apply: bool
) -> dict[str, object]:
    decisions = _parse_decisions(decisions_path)

    allow_en_path = terms_dir / "allowlist_en.txt"
    allow_zh_path = terms_dir / "allowlist_zh.txt"
    deny_path = terms_dir / "denylist.txt"
    synonyms_path = terms_dir / "synonyms.tsv"

    allow_en_existing = load_simple_list(allow_en_path)
    allow_zh_existing = load_simple_list(allow_zh_path)
    deny_existing = load_simple_list(deny_path)
    synonyms_existing = load_synonyms_tsv(synonyms_path)

    add_allow_en: set[str] = set()
    add_allow_zh: set[str] = set()
    add_deny: set[str] = set()

    add_syn: dict[str, tuple[str, str]] = {}

    for d in decisions:
        if d.action == "allow_en":
            if d.value not in allow_en_existing:
                add_allow_en.add(d.value)
        elif d.action == "allow_zh":
            if d.value not in allow_zh_existing:
                add_allow_zh.add(d.value)
        elif d.action == "deny":
            if d.value not in deny_existing:
                add_deny.add(d.value)
        elif d.action == "synonym":
            alias = d.value
            preferred = d.preferred
            lang = d.lang

            if alias in synonyms_existing and synonyms_existing[alias] != preferred:
                raise SystemExit(
                    "decisions apply failed: conflicting synonyms mapping: "
                    f"{alias!r} maps to both {synonyms_existing[alias]!r} and {preferred!r}"
                )
            if alias in add_syn and add_syn[alias][0] != preferred:
                raise SystemExit(
                    "decisions apply failed: conflicting synonyms mapping inside decisions: "
                    f"{alias!r} maps to both {add_syn[alias][0]!r} and {preferred!r}"
                )
            # Even if it already exists, allow re-stating the same mapping.
            add_syn.setdefault(alias, (preferred, lang))

    summary = {
        "decisions": str(decisions_path),
        "terms_dir": str(terms_dir),
        "add_allow_en": sorted(add_allow_en),
        "add_allow_zh": sorted(add_allow_zh),
        "add_deny": sorted(add_deny),
        "add_synonyms": {
            k: {"preferred": v[0], "lang": v[1]} for k, v in sorted(add_syn.items())
        },
        "applied": bool(apply),
    }

    if not apply:
        return summary

    # We only manage the AUTO-INBOX terms; manual sections remain untouched.
    # Merge with any existing AUTO-INBOX terms (if present) by parsing the managed region.
    def _existing_auto_terms(path: Path) -> set[str]:
        lines = _read_file_lines(path)
        if AUTO_MARKER not in lines:
            return set()
        idx = lines.index(AUTO_MARKER)
        terms: set[str] = set()
        for ln in lines[idx + 1 :]:
            s = ln.strip()
            if not s or s.startswith("#"):
                continue
            terms.add(s)
        return terms

    # Allowlists/denylist
    allow_en_auto = _existing_auto_terms(allow_en_path) | set(add_allow_en)
    allow_zh_auto = _existing_auto_terms(allow_zh_path) | set(add_allow_zh)
    deny_auto = _existing_auto_terms(deny_path) | set(add_deny)

    _rewrite_auto_inbox_list(allow_en_path, allow_en_auto)
    _rewrite_auto_inbox_list(allow_zh_path, allow_zh_auto)
    _rewrite_auto_inbox_list(deny_path, deny_auto)

    # Synonyms: only manage auto block; keep existing file content above it.
    def _existing_auto_syn(path: Path) -> dict[str, tuple[str, str]]:
        lines = _read_file_lines(path)
        if AUTO_MARKER not in lines:
            return {}
        idx = lines.index(AUTO_MARKER)
        out: dict[str, tuple[str, str]] = {}
        for ln in lines[idx + 1 :]:
            s = ln.strip()
            if not s or s.startswith("#"):
                continue
            parts = [c.strip() for c in s.split("\t")]
            if len(parts) < 2:
                continue
            alias, preferred = parts[0], parts[1]
            lang = parts[2] if len(parts) >= 3 else ""
            out[alias] = (preferred, lang)
        return out

    syn_auto = _existing_auto_syn(synonyms_path)
    # Only add new (or same) mappings; conflicts already rejected.
    for alias, (preferred, lang) in add_syn.items():
        existing = syn_auto.get(alias)
        if existing is None:
            syn_auto[alias] = (preferred, lang)
        else:
            # Keep existing lang if decisions didn't specify it.
            if existing[0] == preferred and not existing[1] and lang:
                syn_auto[alias] = (preferred, lang)

    _rewrite_auto_inbox_synonyms(synonyms_path, syn_auto)

    return summary


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Apply review decisions TSV into repo truth files under terms/. "
            "This is an optional helper to reduce manual allow/deny/synonyms editing."
        )
    )
    parser.add_argument(
        "--terms-dir",
        default="terms",
        help="Directory containing allow/deny/synonyms",
    )
    parser.add_argument(
        "--decisions",
        default="artifacts/review_pack/decisions.tsv",
        help="Decisions TSV (default: artifacts/review_pack/decisions.tsv)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually write changes into terms/*. Without this, runs in dry-run mode.",
    )

    args = parser.parse_args()
    terms_dir = Path(args.terms_dir)
    decisions_path = Path(args.decisions)

    if not terms_dir.exists():
        raise SystemExit(
            f"decisions apply failed: terms dir does not exist: {terms_dir}"
        )

    # Ensure artifacts dir exists if user wants to keep decisions there.
    ensure_dir(Path(__file__).resolve().parent.parent / "artifacts")

    summary = apply_decisions(
        terms_dir=terms_dir, decisions_path=decisions_path, apply=bool(args.apply)
    )

    # Minimal human-friendly output.
    add_allow_en = summary.get("add_allow_en")
    add_allow_zh = summary.get("add_allow_zh")
    add_deny = summary.get("add_deny")
    add_synonyms = summary.get("add_synonyms")

    print("decisions parsed:", summary["decisions"])
    print("dry-run" if not summary["applied"] else "applied")
    print("add_allow_en:", len(add_allow_en) if isinstance(add_allow_en, list) else 0)
    print("add_allow_zh:", len(add_allow_zh) if isinstance(add_allow_zh, list) else 0)
    print("add_deny:", len(add_deny) if isinstance(add_deny, list) else 0)
    print(
        "add_synonyms:",
        len(add_synonyms) if isinstance(add_synonyms, dict) else 0,
    )


if __name__ == "__main__":
    main()
