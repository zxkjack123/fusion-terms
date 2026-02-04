from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import tomllib  # py>=3.11
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

from pipeline.common import ensure_dir
from pipeline.validate_registry import validate_registry


def _load_config(config_path: Path) -> dict:
    if not config_path.exists():
        return {}
    with config_path.open("rb") as f:
        return tomllib.load(f)


def _iter_alias_rows(aliases_path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in aliases_path.read_text("utf-8", errors="ignore").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = [c.strip() for c in line.split("\t")]
        # alias, concept_id, lang, kind, comment(optional)
        if len(parts) < 4:
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
    for line in concepts_path.read_text("utf-8", errors="ignore").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = [c.strip() for c in line.split("\t")]
        # concept_id, category, preferred_zh, preferred_en, preferred_abbr, status, notes
        if len(parts) < 2:
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

    args = parser.parse_args()

    cfg = _load_config(Path(args.config))
    out_dir = Path(
        args.out_dir or cfg.get("artifacts", {}).get("out_dir", "artifacts")
    ).expanduser()
    terms_dir = Path(args.terms_dir)

    # Default behavior: export Vale unless explicitly disabled.
    do_vale = not args.no_vale
    do_query = bool(args.query_expansions)

    # Gate: registry must be consistent.
    validate_registry(terms_dir)

    ensure_dir(out_dir)

    manifest: dict[str, object] = {}
    if do_vale:
        manifest.update(export_vale_terms(terms_dir=terms_dir, out_dir=out_dir))
    if do_query:
        manifest.update(export_query_expansions(terms_dir=terms_dir, out_dir=out_dir))

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
