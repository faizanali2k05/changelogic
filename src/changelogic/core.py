from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from collections.abc import Iterable


@dataclass(frozen=True)
class Fragment:
    category: str
    text: str
    source: str


DEFAULT_ORDER = ("breaking", "added", "changed", "deprecated", "fixed", "security", "removed")


def parse_text(text: str, *, source: str = "<memory>") -> Fragment:
    """Parse one fragment whose first non-empty line is ``category: text``."""

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        raise ValueError("fragment is empty")
    category, separator, summary = lines[0].partition(":")
    if not separator:
        category, summary = "changed", lines[0]
    category = category.strip().lower() or "changed"
    summary = summary.strip() or "(no summary)"
    return Fragment(category, summary, source)


def parse_directory(path: str | Path) -> list[Fragment]:
    """Parse Markdown fragments in deterministic filename order."""

    path = Path(path)
    if not path.is_dir():
        raise NotADirectoryError(path)
    fragments: list[Fragment] = []
    for file in sorted(path.glob("*.md")):
        if file.name.lower() in {"readme.md", "changelog.md"}:
            continue
        try:
            fragments.append(parse_text(file.read_text(encoding="utf-8"), source=file.name))
        except ValueError:
            continue
    return fragments


def render(fragments: Iterable[Fragment], title: str = "Release notes") -> str:
    """Render fragments into stable Markdown grouped by release category."""

    if not title.strip():
        raise ValueError("title must not be empty")
    groups: dict[str, list[Fragment]] = {}
    for fragment in fragments:
        groups.setdefault(fragment.category, []).append(fragment)
    lines = [f"# {title}", ""]
    order = {category: index for index, category in enumerate(DEFAULT_ORDER)}
    for category in sorted(groups, key=lambda value: (order.get(value, len(order)), value)):
        lines.extend([f"## {category.title()}", ""])
        lines.extend(f"- {fragment.text}<!-- {fragment.source} -->" for fragment in groups[category])
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
