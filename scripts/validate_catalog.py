#!/usr/bin/env python3
"""Validate the FBD skill catalog, metadata, routes, and local Markdown links."""

from __future__ import annotations

import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = REPO_ROOT / "skill_catalog.json"
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def parse_frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    errors: list[str] = []
    if not lines or lines[0].strip() != "---":
        return {}, [f"{path}: missing YAML frontmatter"]
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        return {}, [f"{path}: unclosed YAML frontmatter"]

    values: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        if ":" not in line:
            errors.append(f"{path}: invalid frontmatter line: {line}")
            continue
        key, raw = line.split(":", 1)
        raw = raw.strip()
        if not raw:
            errors.append(f"{path}: empty frontmatter field: {key}")
            continue
        quoted = len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in {'"', "'"}
        if not quoted and ": " in raw:
            errors.append(f"{path}: quote frontmatter value containing ': ': {key}")
        values[key.strip()] = raw[1:-1] if quoted else raw
    return values, errors


def validate_markdown_links(path: Path) -> list[str]:
    errors = []
    text = path.read_text(encoding="utf-8-sig")
    for match in LINK_PATTERN.finditer(text):
        target = match.group(1).strip().split("#", 1)[0]
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.exists():
            errors.append(f"{path}: broken local link: {target}")
    return errors


def validate_catalog() -> list[str]:
    errors: list[str] = []
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    included = catalog.get("included_skills", [])
    names = [item.get("name") for item in included]
    if len(names) != len(set(names)):
        errors.append("skill_catalog.json: duplicate included skill name")

    compass_text = (REPO_ROOT / "project-compass" / "SKILL.md").read_text(encoding="utf-8-sig")
    for item in included:
        name = item.get("name")
        source = REPO_ROOT / str(item.get("source", ""))
        skill_file = source / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"missing SKILL.md for {name}: {skill_file}")
            continue
        metadata, metadata_errors = parse_frontmatter(skill_file)
        errors.extend(metadata_errors)
        if metadata.get("name") != name:
            errors.append(f"{skill_file}: name does not match catalog entry {name}")
        if not metadata.get("description"):
            errors.append(f"{skill_file}: description is required")
        if name != "project-compass" and f"`{name}`" not in compass_text:
            errors.append(f"project-compass does not reference included skill: {name}")

    routed_targets = set()
    for line in compass_text.splitlines():
        if "→" in line:
            routed_targets.update(re.findall(r"`([a-z0-9-]+)`", line))
    declared_targets = (set(names) - {"project-compass"}) | set(catalog.get("external_route_targets", []))
    if routed_targets != declared_targets:
        missing = sorted(routed_targets - declared_targets)
        stale = sorted(declared_targets - routed_targets)
        if missing:
            errors.append(f"skill_catalog.json missing routed targets: {missing}")
        if stale:
            errors.append(f"skill_catalog.json declares unrouted targets: {stale}")

    route_cases = json.loads(
        (REPO_ROOT / "project-compass" / "references" / "route-cases.json").read_text(encoding="utf-8")
    )
    for case in route_cases:
        if f"`{case['expected_route']}`" not in compass_text:
            errors.append(f"route case target missing from project-compass: {case['expected_route']}")

    for path in (REPO_ROOT / "README.md", REPO_ROOT / "docs" / "README_CN.md"):
        errors.extend(validate_markdown_links(path))

    stale_phrases = {
        REPO_ROOT / "README.md": ("7-dimension", "7 dimensions"),
        REPO_ROOT / "docs" / "README_CN.md": ("七维",),
        REPO_ROOT / "ARCHITECTURE.md": ("七维评分", "七维技能"),
    }
    for path, phrases in stale_phrases.items():
        text = path.read_text(encoding="utf-8-sig")
        for phrase in phrases:
            if phrase in text:
                errors.append(f"{path}: stale skill-review dimension count: {phrase}")
    return errors


def main() -> int:
    errors = validate_catalog()
    print(json.dumps({"ok": not errors, "errors": errors}, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
