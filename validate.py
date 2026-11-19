"""Sanity-check the question bank. Run:  python validate.py"""
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from exam import is_correct
from questions import CATEGORIES, QUESTIONS


def main() -> int:
    errors = []
    seen_ids = set()

    for q in QUESTIONS:
        qid = q.get("id", "?")
        if qid in seen_ids:
            errors.append(f"Q{qid}: duplicate id")
        seen_ids.add(qid)

        if q.get("category") not in CATEGORIES:
            errors.append(f"Q{qid}: unknown category {q.get('category')!r}")

        for field in ("question", "explanation", "reference", "type"):
            if not q.get(field):
                errors.append(f"Q{qid}: missing {field}")

        opts = q.get("options", [])
        if len(set(opts)) != len(opts):
            errors.append(f"Q{qid}: duplicate options")
        if any("most voted" in o.lower() for o in opts):
            errors.append(f"Q{qid}: scraped 'Most Voted' marker left in an option")

        t = q.get("type")
        if t == "single":
            if len(opts) < 4:
                errors.append(f"Q{qid}: single needs >= 4 options")
            if q["answer"] not in opts:
                errors.append(f"Q{qid}: answer not in options")
            if not is_correct(q, q["answer"]):
                errors.append(f"Q{qid}: single self-grade failed")
        elif t == "multi":
            if len(opts) < 5:
                errors.append(f"Q{qid}: multi needs >= 5 options")
            if len(q["answer"]) < 2:
                errors.append(f"Q{qid}: multi needs >= 2 correct answers")
            for a in q["answer"]:
                if a not in opts:
                    errors.append(f"Q{qid}: multi answer {a!r} not in options")
            if not is_correct(q, list(q["answer"])):
                errors.append(f"Q{qid}: multi self-grade failed")
        else:
            errors.append(f"Q{qid}: unknown type {t!r}")

    print(f"Checked {len(QUESTIONS)} questions across {len(CATEGORIES)} domains.")
    by_cat = {}
    for q in QUESTIONS:
        by_cat[q["category"]] = by_cat.get(q["category"], 0) + 1
    for c in CATEGORIES:
        print(f"  {c:<46} {by_cat.get(c, 0)}")

    if errors:
        print("\nFAILED:")
        for e in errors:
            print("  -", e)
        return 1
    print("\nAll checks passed ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())
