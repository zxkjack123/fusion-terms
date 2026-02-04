from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator


FENCE_RE = re.compile(r"^\s*```")
INLINE_CODE_RE = re.compile(r"`[^`]+`")
URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
MD_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")

# Common academic-doc noise patterns
REF_HEADING_RE = re.compile(
    r"^\s*(?:#{1,6}\s*)?(references|bibliography|参考文献)\s*[:：]?\s*$",
    re.IGNORECASE,
)
CAPTION_EN_RE = re.compile(
    r"^\s*(?:figure|fig\.?|table)\s*\d+(?:\.\d+)*\s*[:.：]",
    re.IGNORECASE,
)
CAPTION_ZH_RE = re.compile(r"^\s*[图表]\s*\d+(?:\.\d+)*\s*[:.：]")
TABLE_SEP_RE = re.compile(
    r"^\s*\|?\s*:?-{2,}:?\s*(?:\|\s*:?-{2,}:?\s*)+\|?\s*$"
)

MATH_FENCE_DOLLAR_RE = re.compile(r"^\s*\$\$\s*$")
MATH_FENCE_BRACKET_OPEN_RE = re.compile(r"^\s*\\\[\s*$")
MATH_FENCE_BRACKET_CLOSE_RE = re.compile(r"^\s*\\\]\s*$")
INLINE_MATH_RE = re.compile(r"\$[^$]+\$")
WORDLIKE_RE = re.compile(r"[A-Za-z0-9\u4e00-\u9fff]")


@dataclass(frozen=True)
class Example:
    text: str
    file: str


def sha1_text(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8", errors="ignore")).hexdigest()


def iter_markdown_files(root: Path) -> Iterator[Path]:
    for p in root.rglob("*.md"):
        if p.is_file():
            yield p


def clean_markdown_lines(text: str) -> list[str]:
    """Best-effort markdown cleanup for term extraction.

    - strips fenced code blocks
    - removes inline code
    - removes images and URLs
    - converts markdown links to visible link text

    This is deliberately conservative and fast.
    """

    def is_symbol_heavy(s: str) -> bool:
        compact = re.sub(r"\s+", "", s)
        if len(compact) < 40:
            return False
        wordlike = len(WORDLIKE_RE.findall(compact))
        return (wordlike / max(1, len(compact))) < 0.30

    lines_out: list[str] = []
    in_fence = False
    in_math = False

    for raw_line in text.splitlines():
        line = raw_line

        # Stop at references/bibliography sections (usually mostly citations).
        if REF_HEADING_RE.match(line):
            break

        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue

        if in_fence:
            continue

        # Drop display-math blocks.
        if (
            MATH_FENCE_DOLLAR_RE.match(line)
            or MATH_FENCE_BRACKET_OPEN_RE.match(line)
            or MATH_FENCE_BRACKET_CLOSE_RE.match(line)
        ):
            in_math = not in_math
            continue
        if in_math:
            continue

        # Drop figure/table captions (high noise; keep the body text instead).
        if CAPTION_EN_RE.match(line) or CAPTION_ZH_RE.match(line):
            continue

        # Drop table separator rows, but keep table content rows by flattening pipes.
        if TABLE_SEP_RE.match(line):
            continue
        if line.count("|") >= 2:
            line = line.replace("|", " ")

        # images first (avoid keeping alt text noise like 'Figure')
        line = MD_IMAGE_RE.sub(" ", line)

        # links: keep visible text
        line = MD_LINK_RE.sub(lambda m: m.group(1) or " ", line)

        # inline code
        line = INLINE_CODE_RE.sub(" ", line)

        # inline math: keep inner content, drop surrounding $...$
        line = INLINE_MATH_RE.sub(lambda m: m.group(0)[1:-1], line)

        # bare urls
        line = URL_RE.sub(" ", line)

        # collapse whitespace
        line = re.sub(r"\s+", " ", line).strip()
        if line and not is_symbol_heavy(line):
            lines_out.append(line)

    return lines_out


def read_text_file(path: Path, max_bytes: int = 10_000_000) -> str:
    # Guardrail for absurdly large files.
    with path.open("rb") as f:
        data = f.read(max_bytes + 1)
    if len(data) > max_bytes:
        data = data[:max_bytes]
    return data.decode("utf-8", errors="ignore")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def load_simple_list(path: Path) -> set[str]:
    if not path.exists():
        return set()
    out: set[str] = set()
    for line in path.read_text("utf-8", errors="ignore").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        out.add(s)
    return out


def load_synonyms_tsv(path: Path) -> dict[str, str]:
    """Load alias->preferred mapping from a TSV file.

        Format: alias\tpreferred\tlang(optional)
    Lines starting with # are ignored.

        Note:
        - The 3rd column (lang) is currently ignored by the build pipeline.
            It is treated as documentation / future extension only.
        - Conflicting mappings (same alias mapped to different preferred forms)
            are rejected to avoid non-deterministic 'last one wins' behavior.
    """

    if not path.exists():
        return {}

    mapping: dict[str, str] = {}
    for lineno, line in enumerate(
        path.read_text("utf-8", errors="ignore").splitlines(),
        start=1,
    ):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        parts = s.split("\t")
        if len(parts) < 2:
            continue
        alias, preferred = parts[0].strip(), parts[1].strip()
        if not (alias and preferred):
            continue

        if alias in mapping and mapping[alias] != preferred:
            raise SystemExit(
                "conflicting synonyms mapping in "
                f"{path}:{lineno}: {alias!r} maps to both "
                f"{mapping[alias]!r} and {preferred!r}"
            )

        mapping[alias] = preferred
    return mapping
