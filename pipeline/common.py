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

    lines_out: list[str] = []
    in_fence = False

    for raw_line in text.splitlines():
        line = raw_line

        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue

        if in_fence:
            continue

        # images first (avoid keeping alt text noise like 'Figure')
        line = MD_IMAGE_RE.sub(" ", line)

        # links: keep visible text
        line = MD_LINK_RE.sub(lambda m: m.group(1) or " ", line)

        # inline code
        line = INLINE_CODE_RE.sub(" ", line)

        # bare urls
        line = URL_RE.sub(" ", line)

        # collapse whitespace
        line = re.sub(r"\s+", " ", line).strip()
        if line:
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
    """

    if not path.exists():
        return {}

    mapping: dict[str, str] = {}
    for line in path.read_text("utf-8", errors="ignore").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        parts = s.split("\t")
        if len(parts) < 2:
            continue
        alias, preferred = parts[0].strip(), parts[1].strip()
        if alias and preferred:
            mapping[alias] = preferred
    return mapping
