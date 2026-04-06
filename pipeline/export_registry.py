from __future__ import annotations

import argparse
import json
import warnings
from datetime import date
from pathlib import Path


try:
    import tomllib  # py>=3.11
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

from pipeline.common import ensure_dir
from pipeline.validate_registry import validate_registry


_KIND_SEVERITY: dict[str, int] = {
    # Higher wins when the same alias appears multiple times.
    "forbidden": 3,
    "deprecated": 2,
    "preferred": 1,
    "alias": 0,
}


def _json_quote(s: str) -> str:
    # Emit a JSON string literal; valid in YAML double-quoted scalars.
    # This makes escaping deterministic and easy to test.
    return json.dumps(s, ensure_ascii=False)


def _collect_substitutions(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Compute strong-semantic substitutions (deprecated/forbidden -> preferred).

    Returns a deterministic list of rows with keys:
      alias, preferred, status, lang, note

    Selection rule matches docs/dev/08 execution plan:
      - choose preferred within the same concept:
          1) same-lang preferred if exists
          2) else any preferred
          3) tie-breaker: (lang, alias) lexicographic
      - coalesce by alias; forbidden wins over deprecated
      - reject alias==preferred
    """

    preferred_by_concept: dict[str, list[dict[str, str]]] = {}
    for r in rows:
        if r.get("kind") == "preferred":
            preferred_by_concept.setdefault(r.get("concept_id", ""), []).append(r)

    def choose_preferred(*, concept_id: str, lang: str) -> dict[str, str]:
        prefs = preferred_by_concept.get(concept_id, [])
        if not prefs:
            raise SystemExit(
                "export_registry failed: substitutions export requires at least one preferred alias "
                f"for concept_id={concept_id!r}"
            )
        same_lang = [p for p in prefs if p.get("lang", "") == lang]
        candidates = same_lang or prefs
        candidates_sorted = sorted(
            candidates,
            key=lambda p: ((p.get("lang", "") or ""), (p.get("alias", "") or "")),
        )
        return candidates_sorted[0]

    # Coalesce by alias: forbidden wins over deprecated.
    by_alias: dict[str, dict[str, str]] = {}
    for r in rows:
        kind = r.get("kind", "")
        if kind not in {"forbidden", "deprecated"}:
            continue
        alias = r.get("alias", "")
        if not alias:
            continue

        existing = by_alias.get(alias)
        if existing is None:
            by_alias[alias] = r
            continue

        sev_new = _KIND_SEVERITY.get(kind, 0)
        sev_old = _KIND_SEVERITY.get(existing.get("kind", "deprecated"), 0)
        if sev_new > sev_old:
            by_alias[alias] = r
        elif sev_new == sev_old:
            # Tie-breaker for determinism: pick lexicographically smallest lang.
            if (r.get("lang", "") or "") < (existing.get("lang", "") or ""):
                by_alias[alias] = r

    out: list[dict[str, str]] = []
    for alias in sorted(by_alias.keys()):
        r = by_alias[alias]
        concept_id = r.get("concept_id", "")
        lang = r.get("lang", "")
        status = r.get("kind", "")
        note = (r.get("comment", "") or "").replace("\t", " ").replace("\n", " ").strip()

        pref_row = choose_preferred(concept_id=concept_id, lang=lang)
        preferred = pref_row.get("alias", "")
        if not preferred:
            raise SystemExit(
                "export_registry failed: preferred term is empty while exporting substitutions; "
                f"concept_id={concept_id!r} alias={alias!r}"
            )
        if alias == preferred:
            raise SystemExit(
                "export_registry failed: substitutions must not contain alias==preferred; "
                f"concept_id={concept_id!r} alias={alias!r}"
            )

        out.append(
            {
                "alias": alias,
                "preferred": preferred,
                "status": status,
                "lang": lang,
                "note": note,
            }
        )

    return out


def _load_config(config_path: Path) -> dict:
    if not config_path.exists():
        return {}
    with config_path.open("rb") as f:
        return tomllib.load(f)


def _iter_alias_rows(aliases_path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    try:
        lines = aliases_path.read_text("utf-8").splitlines()
    except UnicodeDecodeError as e:
        raise SystemExit(
            f"export_registry failed: aliases TSV is not valid UTF-8: {aliases_path} ({e})"
        ) from e

    for lineno, line in enumerate(lines, start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = [c.strip() for c in line.split("\t")]
        # alias, concept_id, lang, kind, comment(optional)
        if len(parts) < 4:
            warnings.warn(
                (
                    "export_registry: skipping short alias row at "
                    f"{aliases_path}:{lineno}: {line!r}"
                ),
                RuntimeWarning,
                stacklevel=2,
            )
            continue
        rows.append(
            {
                "alias": parts[0],
                "concept_id": parts[1],
                "lang": parts[2],
                "kind": parts[3],
                "comment": parts[4] if len(parts) >= 5 else "",
            }
        )
    return rows


def _iter_concept_rows(concepts_path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    try:
        lines = concepts_path.read_text("utf-8").splitlines()
    except UnicodeDecodeError as e:
        raise SystemExit(
            f"export_registry failed: concepts TSV is not valid UTF-8: {concepts_path} ({e})"
        ) from e

    for lineno, line in enumerate(lines, start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = [c.strip() for c in line.split("\t")]
        # concept_id, category, preferred_zh, preferred_en, preferred_abbr, status, notes
        if len(parts) < 2:
            warnings.warn(
                (
                    "export_registry: skipping short concept row at "
                    f"{concepts_path}:{lineno}: {line!r}"
                ),
                RuntimeWarning,
                stacklevel=2,
            )
            continue
        rows.append(
            {
                "concept_id": parts[0],
                "category": parts[1],
                "preferred_zh": parts[2] if len(parts) >= 3 else "",
                "preferred_en": parts[3] if len(parts) >= 4 else "",
                "preferred_abbr": parts[4] if len(parts) >= 5 else "",
                "status": parts[5] if len(parts) >= 6 else "",
                "notes": parts[6] if len(parts) >= 7 else "",
            }
        )
    return rows


def export_vale_terms(*, terms_dir: Path, out_dir: Path) -> dict[str, str]:
    """Export Vale accept/reject lists from registry aliases.

    Accept contains preferred + alias.
    Reject contains forbidden + deprecated.

    If a term appears in both, reject wins.
    """

    registry_dir = terms_dir / "registry"
    aliases_path = registry_dir / "aliases.tsv"

    rows = _iter_alias_rows(aliases_path)

    accept: set[str] = set()
    reject: set[str] = set()

    for r in rows:
        alias = r["alias"]
        kind = r["kind"]
        if kind in {"preferred", "alias"}:
            accept.add(alias)
        elif kind in {"forbidden", "deprecated"}:
            reject.add(alias)

    # reject wins
    accept -= reject

    vale_dir = out_dir / "vale"
    ensure_dir(vale_dir)

    accept_path = vale_dir / "accept.txt"
    reject_path = vale_dir / "reject.txt"

    accept_path.write_text("\n".join(sorted(accept)) + "\n", encoding="utf-8")
    reject_path.write_text("\n".join(sorted(reject)) + "\n", encoding="utf-8")

    return {
        "vale_accept": str(accept_path),
        "vale_reject": str(reject_path),
        "accept_count": len(accept),
        "reject_count": len(reject),
    }


def export_query_expansions(*, terms_dir: Path, out_dir: Path) -> dict[str, object]:
    """Export query expansions for search/KB retrieval.

    Output: artifacts/query_expansions.json

    Notes:
    - We keep both "include" (preferred/alias) and "deprecated" terms.
      Consumers can decide whether to include deprecated in recall-oriented queries.
    - "forbidden" terms are exported separately (typically excluded from writing),
      but can still be useful for recall or drift scanning.
    """

    registry_dir = terms_dir / "registry"
    concepts_path = registry_dir / "concepts.tsv"
    aliases_path = registry_dir / "aliases.tsv"

    concepts_rows = _iter_concept_rows(concepts_path)
    concepts: dict[str, dict[str, str]] = {r["concept_id"]: r for r in concepts_rows}

    rows = _iter_alias_rows(aliases_path)

    concept_terms: dict[str, dict[str, set[str]]] = {}
    alias_index: dict[str, str] = {}

    for r in rows:
        alias = r["alias"]
        concept_id = r["concept_id"]
        kind = r["kind"]

        alias_index[alias] = concept_id

        buckets = concept_terms.setdefault(
            concept_id,
            {
                "include": set(),
                "deprecated": set(),
                "forbidden": set(),
            },
        )

        if kind in {"preferred", "alias"}:
            buckets["include"].add(alias)
        elif kind == "deprecated":
            buckets["deprecated"].add(alias)
        elif kind == "forbidden":
            buckets["forbidden"].add(alias)

    # Deterministic export: stable ordering.
    concepts_out: dict[str, object] = {}
    for concept_id in sorted(concepts.keys()):
        c = concepts[concept_id]
        buckets = concept_terms.get(
            concept_id,
            {"include": set(), "deprecated": set(), "forbidden": set()},
        )
        include = sorted(buckets["include"])
        deprecated = sorted(buckets["deprecated"])
        forbidden = sorted(buckets["forbidden"])

        concepts_out[concept_id] = {
            "category": c.get("category", ""),
            "status": c.get("status", ""),
            "preferred": {
                "zh": c.get("preferred_zh", ""),
                "en": c.get("preferred_en", ""),
                "abbr": c.get("preferred_abbr", ""),
            },
            "include": include,
            "deprecated": deprecated,
            "forbidden": forbidden,
            "all_terms": sorted(set(include) | set(deprecated)),
        }

    payload = {
        "schema_version": 1,
        "concepts": concepts_out,
        "alias_index": {k: alias_index[k] for k in sorted(alias_index.keys())},
    }

    out_path = out_dir / "query_expansions.json"
    out_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    return {
        "query_expansions": str(out_path),
        "concept_count": len(concepts_out),
        "alias_count": len(alias_index),
    }


def export_tag_rules(*, terms_dir: Path, out_dir: Path) -> dict[str, object]:
    """Export tag rules for auto-tagging / indexing.

    Output: artifacts/tag_rules.jsonl

    Each line is a JSON object describing a literal match rule:
      {alias, concept_id, category, lang, kind, match}

    Notes:
    - We export all alias kinds (preferred/alias/deprecated/forbidden).
      Consumers can decide whether to ignore forbidden/deprecated at runtime.
    - If the same alias appears multiple times (same concept_id), we coalesce
      to a single rule using kind severity: forbidden > deprecated > preferred > alias.
    """

    registry_dir = terms_dir / "registry"
    concepts_path = registry_dir / "concepts.tsv"
    aliases_path = registry_dir / "aliases.tsv"

    concepts_rows = _iter_concept_rows(concepts_path)
    concepts: dict[str, dict[str, str]] = {r["concept_id"]: r for r in concepts_rows}

    rows = _iter_alias_rows(aliases_path)

    # Coalesce by alias to keep output stable and easy to consume.
    by_alias: dict[str, dict[str, str]] = {}
    for r in rows:
        alias = r["alias"]
        concept_id = r["concept_id"]
        kind = r["kind"]

        existing = by_alias.get(alias)
        if existing is None:
            by_alias[alias] = r
            continue

        # Same alias mapping to multiple concepts is already rejected by validator.
        # Still, prefer deterministic behavior if invoked without validation.
        if existing.get("concept_id") != concept_id:
            # Keep the existing entry; downstream should rely on validator.
            continue

        sev_new = _KIND_SEVERITY.get(kind, 0)
        sev_old = _KIND_SEVERITY.get(existing.get("kind", "alias"), 0)
        if sev_new > sev_old:
            by_alias[alias] = r
        elif sev_new == sev_old:
            # Tie-breaker for determinism: pick lexicographically smallest lang.
            if (r.get("lang", "") or "") < (existing.get("lang", "") or ""):
                by_alias[alias] = r

    out_path = out_dir / "tag_rules.jsonl"
    lines: list[str] = []
    for alias in sorted(by_alias.keys()):
        r = by_alias[alias]
        concept_id = r["concept_id"]
        c = concepts.get(concept_id, {})
        rule = {
            "alias": alias,
            "concept_id": concept_id,
            "category": c.get("category", ""),
            "lang": r.get("lang", ""),
            "kind": r.get("kind", ""),
            "match": "literal",
        }
        lines.append(json.dumps(rule, ensure_ascii=False, sort_keys=True))

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return {
        "tag_rules": str(out_path),
        "tag_rule_count": len(lines),
    }


def export_substitutions_tsv(*, terms_dir: Path, out_dir: Path) -> dict[str, object]:
    """Export strong-semantic substitutions from registry aliases.

    Output: artifacts/terminology_substitutions.tsv

    Rules:
    - Only deprecated/forbidden aliases are exported.
    - preferred term is selected from kind=preferred within the same concept:
        1) prefer same-lang preferred
        2) else fallback to any preferred
        3) tie-breaker: (lang, alias) lexicographic, pick first
    - Each alias is exported at most once; forbidden wins over deprecated.
    - alias==preferred is rejected (indicates broken registry data).
    """

    registry_dir = terms_dir / "registry"
    aliases_path = registry_dir / "aliases.tsv"
    rows = _iter_alias_rows(aliases_path)
    out_path = out_dir / "terminology_substitutions.tsv"

    lines: list[str] = []
    # Header as comment for TSV consumers.
    lines.append("# alias\tpreferred\tstatus\tlang\tnote")

    subs = _collect_substitutions(rows)
    for r in subs:
        lines.append(
            f"{r['alias']}\t{r['preferred']}\t{r['status']}\t{r['lang']}\t{r['note']}"
        )

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return {
        "terminology_substitutions": str(out_path),
        "substitution_count": len(subs),
    }


def export_vale_substitute_yaml(*, terms_dir: Path, out_dir: Path) -> dict[str, object]:
    """Export Vale substitution YAML for deprecated/forbidden aliases.

    Output: artifacts/vale/terminology_substitute.yml
    """

    registry_dir = terms_dir / "registry"
    aliases_path = registry_dir / "aliases.tsv"
    rows = _iter_alias_rows(aliases_path)

    subs = _collect_substitutions(rows)
    swap = {r["alias"]: r["preferred"] for r in subs}

    vale_dir = out_dir / "vale"
    ensure_dir(vale_dir)
    out_path = vale_dir / "terminology_substitute.yml"

    lines: list[str] = []
    lines.append("# Auto-generated by pipeline.export_registry --vale-substitute")
    lines.append("# schema_version: 1")
    lines.append("extends: substitution")
    lines.append("message: " + _json_quote("Use '%s' instead of '%s'."))
    lines.append("level: warning")
    lines.append("ignorecase: false")
    lines.append("swap:")

    for alias in sorted(swap.keys()):
        preferred = swap[alias]
        lines.append(f"  {_json_quote(alias)}: {_json_quote(preferred)}")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return {
        "vale_terminology_substitute": str(out_path),
        "vale_terminology_substitute_count": len(swap),
    }


def export_translation_dict(
    *, terms_dir: Path, out_dir: Path, min_en_key_len: int = 3
) -> dict[str, object]:
    """Export translation dictionary JSON for zh↔en lookup.

    Output: artifacts/translation_dict.json
    """

    registry_dir = terms_dir / "registry"
    concepts_path = registry_dir / "concepts.tsv"
    aliases_path = registry_dir / "aliases.tsv"

    concepts_rows = _iter_concept_rows(concepts_path)
    alias_rows = _iter_alias_rows(aliases_path)

    preferred_en_by_concept: dict[str, str] = {}
    preferred_zh_by_concept: dict[str, str] = {}
    for row in concepts_rows:
        concept_id = row.get("concept_id", "")
        preferred_en_by_concept[concept_id] = row.get("preferred_en", "")
        preferred_zh_by_concept[concept_id] = row.get("preferred_zh", "")

    zh2en: dict[str, str] = {}
    en2zh: dict[str, str] = {}
    en2zh_concept: dict[str, str] = {}
    en2zh_abbr_keys: set[str] = set()

    for row in alias_rows:
        alias = row.get("alias", "")
        concept_id = row.get("concept_id", "")
        kind = row.get("kind", "")
        lang = row.get("lang", "")

        if kind not in {"preferred", "alias"}:
            continue

        preferred_en = preferred_en_by_concept.get(concept_id, "")
        preferred_zh = preferred_zh_by_concept.get(concept_id, "")

        if lang == "abbr" and preferred_zh:
            en2zh_abbr_keys.add(alias)

        if lang in {"zh", "abbr", "mixed"} and preferred_en and alias not in zh2en:
            zh2en[alias] = preferred_en
        if lang in {"en", "abbr", "mixed"} and preferred_zh and alias not in en2zh:
            en2zh[alias] = preferred_zh
            en2zh_concept[alias] = concept_id

    en2zh_short: dict[str, dict[str, str]] = {}
    for key in list(en2zh.keys()):
        if key.isascii() and (
            len(key) < min_en_key_len or key in en2zh_abbr_keys
        ):
            en2zh_short[key] = {
                "zh": en2zh.pop(key),
                "concept_id": en2zh_concept[key],
            }

    payload = {
        "schema_version": 2,
        "zh2en": zh2en,
        "en2zh": en2zh,
        "en2zh_short": en2zh_short,
        "metadata": {
            "generated_at": date.today().isoformat(),
            "pairs_zh2en": len(zh2en),
            "pairs_en2zh": len(en2zh),
            "pairs_en2zh_short": len(en2zh_short),
        },
    }

    out_path = out_dir / "translation_dict.json"
    out_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    return {
        "translation_dict": str(out_path),
        "pairs_zh2en": len(zh2en),
        "pairs_en2zh": len(en2zh),
        "pairs_en2zh_short": len(en2zh_short),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export multi-consumer artifacts from terms/registry (currently: Vale accept/reject)."
    )
    parser.add_argument(
        "--config",
        default="config.toml",
        help="Path to config.toml",
    )
    parser.add_argument(
        "--terms-dir",
        default="terms",
        help="Directory containing registry/",
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help="Output dir (overrides config)",
    )
    parser.add_argument(
        "--no-vale",
        action="store_true",
        help="Do not export Vale accept/reject lists",
    )
    parser.add_argument(
        "--query-expansions",
        action="store_true",
        help="Export query expansions JSON (artifacts/query_expansions.json)",
    )
    parser.add_argument(
        "--tag-rules",
        action="store_true",
        help="Export tag rules JSONL (artifacts/tag_rules.jsonl)",
    )
    parser.add_argument(
        "--substitutions",
        action="store_true",
        help="Export strong-semantic substitutions TSV (artifacts/terminology_substitutions.tsv)",
    )
    parser.add_argument(
        "--vale-substitute",
        action="store_true",
        help="Export Vale substitution YAML (artifacts/vale/terminology_substitute.yml)",
    )
    parser.add_argument(
        "--translation-dict",
        action="store_true",
        help="Export translation dictionary JSON (artifacts/translation_dict.json)",
    )

    args = parser.parse_args()

    cfg = _load_config(Path(args.config))
    out_dir = Path(
        args.out_dir or cfg.get("artifacts", {}).get("out_dir", "artifacts")
    ).expanduser()
    terms_dir = Path(args.terms_dir)

    # Default behavior: export Vale unless explicitly disabled.
    do_vale = not args.no_vale
    do_query = bool(args.query_expansions)
    do_tag = bool(args.tag_rules)
    do_subs = bool(args.substitutions)
    do_vale_sub = bool(args.vale_substitute)
    do_translation = bool(args.translation_dict)

    # Gate: registry must be consistent.
    validate_registry(terms_dir)

    ensure_dir(out_dir)

    manifest: dict[str, object] = {}
    if do_vale:
        manifest.update(export_vale_terms(terms_dir=terms_dir, out_dir=out_dir))
    if do_query:
        manifest.update(export_query_expansions(terms_dir=terms_dir, out_dir=out_dir))
    if do_tag:
        manifest.update(export_tag_rules(terms_dir=terms_dir, out_dir=out_dir))
    if do_subs:
        manifest.update(export_substitutions_tsv(terms_dir=terms_dir, out_dir=out_dir))
    if do_vale_sub:
        manifest.update(export_vale_substitute_yaml(terms_dir=terms_dir, out_dir=out_dir))
    if do_translation:
        min_en_key_len = cfg.get("export", {}).get("min_en_key_len", 3)
        manifest.update(
            export_translation_dict(
                terms_dir=terms_dir,
                out_dir=out_dir,
                min_en_key_len=min_en_key_len,
            )
        )

    # Emit a small manifest to make downstream tooling simpler.
    manifest_path = out_dir / "registry_exports.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"exported registry artifacts to {out_dir}")
    print(f"wrote {manifest_path}")


if __name__ == "__main__":
    main()
