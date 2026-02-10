from __future__ import annotations

from pathlib import Path


def test_repo_registry_has_at_least_one_deprecated_or_forbidden_alias() -> None:
    """Guardrail: release substitution outputs should not be empty.

    de-ai-fier consumes Vale substitution YAML exported from deprecated/forbidden aliases.
    This test ensures the repository registry includes at least one such entry.
    """

    repo_root = Path(__file__).resolve().parents[1]
    aliases_path = repo_root / "terms" / "registry" / "aliases.tsv"
    assert aliases_path.exists(), f"missing {aliases_path}"

    kinds: list[str] = []
    for raw in aliases_path.read_text("utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        parts = [c.strip() for c in raw.split("\t")]
        if len(parts) < 4:
            continue
        kinds.append(parts[3])

    assert any(k in {"deprecated", "forbidden"} for k in kinds), (
        "terms/registry/aliases.tsv must include at least one deprecated/forbidden alias "
        "so that artifacts/vale/terminology_substitute.yml and artifacts/terminology_substitutions.tsv "
        "are non-empty in release packs"
    )
