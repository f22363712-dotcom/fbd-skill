#!/usr/bin/env python3
"""Report deterministic English style risks without rewriting the draft."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


MODE_LIMITS = {"reply": 280, "post": 1500, "thread": 9000, "article": 100000, "general": 100000}
STOCK_OPENERS = (
    "one nuance",
    "one caveat",
    "worth noting",
    "it is worth noting",
    "it's worth noting",
    "the key takeaway",
    "let's unpack",
    "in today's fast-paced",
    "in conclusion",
)
MODEL_CLICHES = (
    "delve into",
    "game-changing",
    "game changer",
    "unlock the potential",
    "ever-evolving landscape",
    "paradigm shift",
    "this highlights the importance",
    "it is important to note",
    "a testament to",
)
SPECIALIST_TERMS = (
    r"\bimplied move\b",
    r"\bshort[- ]vol\b",
    r"\bentry iv\b",
    r"\biv\b",
    r"\bstrikes?\b",
    r"\bconvexity\b",
    r"\bbasis points?\b",
    r"\bebitda\b",
    r"\bfree cash flow\b",
    r"\bfcf\b",
    r"\bnpl\b",
    r"\bmultiple compression\b",
    r"\brisk[- ]on\b",
    r"\brisk[- ]off\b",
)


def add_issue(issues: list[dict[str, str]], severity: str, code: str, message: str) -> None:
    issues.append({"severity": severity, "code": code, "message": message})


def first_words(text: str, count: int = 4) -> str:
    words = re.findall(r"[A-Za-z0-9%+-]+", text.lower())
    return " ".join(words[:count])


def sentence_words(text: str) -> list[int]:
    sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", text.strip()) if part.strip()]
    return [len(re.findall(r"\b[\w'+-]+\b", sentence)) for sentence in sentences]


def inspect(text: str, mode: str, max_chars: int, history: str = "") -> dict[str, object]:
    issues: list[dict[str, str]] = []
    stripped = text.strip()
    lower = stripped.lower()

    if not stripped:
        add_issue(issues, "fail", "empty", "Draft is empty.")
    if len(stripped) > max_chars:
        add_issue(issues, "fail", "length", f"{mode} has {len(stripped)} characters; limit is {max_chars}.")
    if mode == "reply" and stripped and len(stripped) < 60:
        add_issue(issues, "warn", "thin_reply", "Reply is under 60 characters; confirm it adds a useful increment.")

    for opener in STOCK_OPENERS:
        if lower.startswith(opener):
            add_issue(issues, "fail", "stock_opener", f"Template-like opener: '{opener}'.")
            break

    found_cliches = [phrase for phrase in MODEL_CLICHES if phrase in lower]
    if found_cliches:
        add_issue(issues, "fail", "model_cliche", "Model/corporate cliché: " + ", ".join(found_cliches) + ".")

    if mode == "reply":
        jargon = [pattern for pattern in SPECIALIST_TERMS if re.search(pattern, lower)]
        if len(jargon) > 2:
            add_issue(issues, "fail", "jargon_stack", f"Reply contains {len(jargon)} specialist terms; explain, replace, or remove some.")
        if stripped.count(";") > 1:
            add_issue(issues, "fail", "memo_punctuation", "Multiple semicolons make the reply read like a memo.")
        elif stripped.count(";") == 1:
            add_issue(issues, "warn", "semicolon", "Check whether the semicolon can become a natural sentence break.")
        if "?" not in stripped:
            add_issue(issues, "warn", "closed_reply", "No question is present; confirm the reply still leaves a natural conversational opening.")

    lengths = sentence_words(stripped)
    if any(length > 42 for length in lengths):
        add_issue(issues, "fail", "long_sentence", "At least one sentence exceeds 42 words.")
    if len(lengths) >= 3 and max(lengths) - min(lengths) <= 3:
        add_issue(issues, "warn", "flat_rhythm", "Sentence lengths are unusually uniform; read aloud for model-like rhythm.")
    if stripped.count("!") > 1:
        add_issue(issues, "fail", "hype_punctuation", "More than one exclamation mark weakens restrained professional tone.")

    correction_markers = sum(
        lower.count(marker)
        for marker in ("doesn't prove", "does not prove", "the headline misses", "precision matters", "that said")
    )
    if correction_markers >= 2:
        add_issue(issues, "fail", "correction_stack", "Multiple correction markers make the copy sound adversarial or review-like.")
    elif correction_markers == 1:
        add_issue(issues, "warn", "correction_posture", "Check whether the correction directly answers the author rather than grading them.")

    if history.strip() and stripped:
        opener = first_words(stripped)
        recent_openers = {first_words(line) for line in history.splitlines() if line.strip()}
        if opener and opener in recent_openers:
            add_issue(issues, "fail", "repeated_opener", f"Opening phrase repeats recent copy: '{opener}'.")

    failures = [issue for issue in issues if issue["severity"] == "fail"]
    warnings = [issue for issue in issues if issue["severity"] == "warn"]
    return {
        "ok": not failures,
        "mode": mode,
        "characters": len(stripped),
        "max_characters": max_chars,
        "failures": failures,
        "warnings": warnings,
        "note": "Deterministic checks only. Complete the nine semantic TDD gates before publication.",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path, help="UTF-8 text or Markdown draft")
    parser.add_argument("--mode", choices=MODE_LIMITS, default="general")
    parser.add_argument("--max-chars", type=int, help="Override the mode character limit")
    parser.add_argument("--history", type=Path, help="Optional UTF-8 file with one recent item per line")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        text = args.draft.read_text(encoding="utf-8-sig")
        history = args.history.read_text(encoding="utf-8-sig") if args.history else ""
    except OSError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    result = inspect(text, args.mode, args.max_chars or MODE_LIMITS[args.mode], history)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{'PASS' if result['ok'] else 'FAIL'} | mode={result['mode']} | chars={result['characters']}/{result['max_characters']}")
        for issue in result["failures"] + result["warnings"]:
            print(f"{issue['severity'].upper()} {issue['code']}: {issue['message']}")
        print(result["note"])
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
