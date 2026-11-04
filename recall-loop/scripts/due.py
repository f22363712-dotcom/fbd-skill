#!/usr/bin/env python3
"""Compute which cards are due from a `复习台账.md` ledger.

Usage:
  python due.py                # due today + overdue
  python due.py --days 3       # within the next 3 days
  python due.py --all          # whole table
  python due.py --subject 国际商务文化
  python due.py --file path/to/复习台账.md

Ledger lookup order: --file, $RECALL_LEDGER, first 复习台账.md under the
current directory.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

LEDGER_NAME = "复习台账.md"
COLS = ["ID", "科目", "卡片", "等级", "间隔", "下次", "上次结果", "连续正确"]
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}


def find_ledger(explicit: str | None) -> Path:
    if explicit:
        path = Path(explicit).expanduser()
        if path.is_file():
            return path
        sys.exit(f"ERROR: ledger not found: {path}")

    env = os.environ.get("RECALL_LEDGER")
    if env:
        path = Path(env).expanduser()
        if path.is_file():
            return path
        sys.exit(f"ERROR: RECALL_LEDGER points to a missing file: {path}")

    for root, dirs, files in os.walk(Path.cwd()):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        if LEDGER_NAME in files:
            return Path(root) / LEDGER_NAME

    sys.exit(f"ERROR: no {LEDGER_NAME} found; pass --file or set RECALL_LEDGER")


def parse_rows(path: Path) -> list[dict[str, str | dt.date]]:
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 8 or not re.fullmatch(r"C-\d+", cells[0]):
            continue
        rec = dict(zip(COLS, cells[:8]))
        try:
            rec["_due"] = dt.date.fromisoformat(str(rec["下次"]))
        except ValueError:
            print(f"[warn] bad date, skipped: {s}", file=sys.stderr)
            continue
        rows.append(rec)
    return rows


def fmt(rec: dict, today: dt.date) -> str:
    delta = (rec["_due"] - today).days
    tag = (
        f"逾期 {-delta} 天"
        if delta < 0
        else ("今天" if delta == 0 else f"{delta} 天后")
    )
    return (
        f"  {rec['ID']:>6}  {rec['等级']:<3} {rec['间隔']:>3}d  "
        f"{rec['下次']}  ({tag})  {rec['上次结果']}  连对{rec['连续正确']}  {rec['卡片']}"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file")
    ap.add_argument("--days", type=int, default=0, help="0 = due only, N = next N days")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--subject")
    args = ap.parse_args()

    today = dt.date.today()
    path = find_ledger(args.file)
    rows = parse_rows(path)
    if args.subject:
        rows = [r for r in rows if r["科目"] == args.subject]
    if not rows:
        print(f"No matching cards in {path}")
        return 0

    if not args.all:
        cutoff = today + dt.timedelta(days=args.days)
        rows = [r for r in rows if r["_due"] <= cutoff]

    print(f"# {today.isoformat()}  {len(rows)} card(s)  [{path}]")
    if not rows:
        print("(nothing due today)")
        return 0

    groups: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        groups[str(r["科目"])].append(r)

    for subject, items in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        items.sort(key=lambda r: (r["_due"], r["等级"]))
        print(f"\n## {subject} · {len(items)}")
        for r in items:
            print(fmt(r, today))

    overdue = sum(1 for r in rows if r["_due"] < today)
    print(f"\nTotal due {len(rows)}, overdue {overdue}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
