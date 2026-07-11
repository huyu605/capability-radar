#!/usr/bin/env python3
"""Minimal dependency-free validation for a SKILL.md package."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def validate(skill_path: Path) -> tuple[bool, str]:
    skill_md = skill_path / "SKILL.md"
    if not skill_md.is_file():
        return False, "SKILL.md not found"
    content = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---(?:\n|$)", content, re.DOTALL)
    if not match:
        return False, "invalid YAML frontmatter boundaries"
    frontmatter = match.group(1)
    fields: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if not line.strip() or line.startswith((" ", "\t", "#")):
            return False, "frontmatter must contain only top-level name and description fields"
        key, separator, value = line.partition(":")
        if not separator:
            return False, f"invalid frontmatter line: {line}"
        fields[key.strip()] = value.strip().strip('"\'')
    if set(fields) != {"name", "description"}:
        return False, "frontmatter must contain exactly name and description"
    name = fields["name"]
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        return False, "name must be hyphen-case and at most 64 characters"
    description = fields["description"]
    if not description or len(description) > 1024 or "<" in description or ">" in description:
        return False, "description is empty, too long, or contains angle brackets"
    if "TODO" in content:
        return False, "SKILL.md contains unresolved TODO text"
    return True, "Skill is valid!"


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: quick_validate.py <skill_directory>", file=sys.stderr)
        return 2
    valid, message = validate(Path(sys.argv[1]))
    print(message)
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
