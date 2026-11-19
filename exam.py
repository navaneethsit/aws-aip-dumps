"""Grading and helper logic for the AIP-C01 mock exam (UI-independent, testable).

AWS scoring convention: single-choice and multiple-response items are both
all-or-nothing (no partial credit), 1 point each.
"""
from __future__ import annotations


def is_correct(q: dict, response) -> bool:
    """True only if the response fully matches the correct answer.

    response shapes:
      single -> str
      multi  -> list/set[str]
    """
    if response is None:
        return False
    if q["type"] == "single":
        return response == q["answer"]
    if q["type"] == "multi":
        return set(response) == set(q["answer"])
    return False


def segment_score(q: dict, response) -> tuple[int, int]:
    """Points earned / available. Always 0-or-1 of 1 (all-or-nothing)."""
    return (1 if is_correct(q, response) else 0), 1


def category_breakdown(history: list[dict]) -> dict[str, dict]:
    """Aggregate correct/total per category from a run history."""
    out: dict[str, dict] = {}
    for h in history:
        cat = h["category"]
        out.setdefault(cat, {"correct": 0, "total": 0})
        out[cat]["total"] += 1
        if h["is_correct"]:
            out[cat]["correct"] += 1
    return out
