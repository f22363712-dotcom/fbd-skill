#!/usr/bin/env python3
"""Install FBD skills into a Claude Code-compatible skills directory."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = REPO_ROOT / "skill_catalog.json"


def load_catalog() -> dict:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def build_install_plan(target: Path, selected: set[str] | None = None) -> list[tuple[str, Path, Path]]:
    plan = []
    for item in load_catalog()["included_skills"]:
        name = item["name"]
        if selected and name not in selected:
            continue
        plan.append((name, REPO_ROOT / item["source"], target / name))
    return plan


def install_plan(plan: list[tuple[str, Path, Path]], update: bool = False) -> None:
    for _, source, destination in plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(
            source,
            destination,
            dirs_exist_ok=update,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--target",
        type=Path,
        default=Path.home() / ".claude" / "skills",
        help="Claude Code skills directory",
    )
    parser.add_argument(
        "--skills",
        help="Comma-separated included skill names; default installs all",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Copy changed files into existing skill directories without deleting other files",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    catalog_names = {item["name"] for item in load_catalog()["included_skills"]}
    selected = None
    if args.skills:
        selected = {name.strip() for name in args.skills.split(",") if name.strip()}
        unknown = sorted(selected - catalog_names)
        if unknown:
            print(json.dumps({"ok": False, "error": "unknown skills", "skills": unknown}))
            return 2

    target = args.target.expanduser().resolve()
    plan = build_install_plan(target, selected)
    conflicts = [str(destination) for _, _, destination in plan if destination.exists()]
    if conflicts and not args.update:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": "destination exists; rerun with --update to copy changed files",
                    "conflicts": conflicts,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1

    if not args.dry_run:
        install_plan(plan, update=args.update)

    print(
        json.dumps(
            {
                "ok": True,
                "dry_run": args.dry_run,
                "target": str(target),
                "installed": [name for name, _, _ in plan],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
