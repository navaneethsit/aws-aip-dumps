# AIP-C01 Mock Exam

An interactive **Streamlit** practice / mock-exam app for the
**AWS Certified Generative AI Developer – Professional (AIP-C01)** certification.
Same layout and behaviour as the `ai103-mock` app, adapted to AWS.

> ⚠️ **Study aid only.** Use it to learn the concepts, not to memorise live exam content.
> Always cross-check with the [official exam guide](https://docs.aws.amazon.com/aws-certification/latest/ai-professional-01/ai-professional-01.html)
> and the Official Pretest / Practice Question Set in AWS Skill Builder.

## Features

- **Two modes**
  - 📝 **Practice** — immediate feedback, the correct answer, an explanation of why each distractor fails, and an AWS documentation citation.
  - ⏱️ **Mock Exam** — up to **75 questions** drawn at random, timer scaled at the official pace (**180 min / 75 = 2.4 min per question**), **live countdown**, **flag-for-review**, question navigator, scored against the **75% (750/1000)** pass mark.
- **Official item types** — single choice and multiple response ("Choose three"), both **all-or-nothing** like the real exam.
- **Mapped to the 5 official domains** with their weights (31 / 26 / 20 / 12 / 11 %) and to the exam-guide **task number** (shown as a pill, e.g. `TASK 1.6`).
- **Community-vote + caution notes** — disputed answers show the vote split and a warning explaining the ambiguity.
- **Analytics** — per-domain breakdown with weak-area highlighting and a "show only incorrect" review.
- **Optional AI coach** — OpenRouter key gives a concise why-right / why-others-wrong / remember note, cached per question.

## Run

```powershell
cd D:\Workspace\certification\AWS\AI-Developer-Professional\aip-c01-mock
py -3 -m pip install -r requirements.txt
py -3 -m streamlit run app.py
```

Open http://localhost:8501.

## Structure

```
aip-c01-mock/
├── app.py             # Streamlit UI: home, practice, exam (timer+flags+navigator), results
├── questions.py       # Question bank (Exam A · Topic 1 · Q1-10) + CATEGORIES + schema docs
├── questions_extra.py # Q11-50 (EXTRA list) — add new batches as questions_extraN.py and import in questions.py
├── questions_extra2.py # Q51-75
├── questions_extra3.py # Q76-97, Q100, Q101
├── questions_extra4.py # Q105, Q115-119, Q122-136 (screenshot batch)
├── questions_extra5.py # Q137-149 (new questions from resources/1.text)
├── certyiq_key.py     # third-party answer key (Q1-97) used for the agree/disagree check
├── screenshots/       # source screenshots for Q51-100 (answers hidden in the source)
├── resources/         # CertyIQ AIP-C01 PDF/TXT (answers included)
├── exam.py            # Grading logic (all-or-nothing), UI-independent
├── config.py          # Pass mark, exam size/timer, domain weights, AI coach, tips
├── validate.py        # Integrity checker for the bank
├── requirements.txt
├── .streamlit/config.toml
└── README.md
```

## Adding questions

Append dicts to `EXTRA` in `questions_extra.py` (ids 11+):

```python
{
    "id": 11,
    "category": "1 · FM Integration, Data & Compliance",   # one of the 5 domains in questions.CATEGORIES
    "task": "1.5",                                         # optional exam-guide task
    "type": "single",                                      # single | multi
    "question": "…?",
    "options": ["A. …", "B. …", "C. …", "D. …"],          # multi needs >= 5 options, >= 2 answers
    "answer": "B. …",                                      # single: str · multi: list[str]
    "explanation": "Why B is right; why A/C/D are not.",
    "reference": "https://docs.aws.amazon.com/…",
    "votes": {"A": 18, "B": 59},                           # optional
    "note": "Disputed because …",                          # optional
}
```

Strip scraped markers such as "Most Voted" from options, then run:

```powershell
py -3 validate.py
```

## Optional: AI explanations

Create `.streamlit/secrets.toml`:

```toml
openrouter_api_key = "sk-or-…"
```

## Current coverage — 133 questions (Q1–97, Q100, practice Q101, Q105, Q115–119, Q122–136, Q137–149)

| Domain | Questions | Exam weight |
|---|---|---|
| 1 · FM Integration, Data & Compliance | 36 | 31% |
| 2 · Implementation & Integration | 33 | 26% |
| 3 · Safety, Security & Governance | 33 | 20% |
| 4 · Operational Efficiency & Optimization | 17 | 12% |
| 5 · Testing, Validation & Troubleshooting | 14 | 11% |

Q1–10 live in `questions.py`; Q11–50 in `questions_extra.py`; Q51–75 in `questions_extra2.py`; Q76–97 and Q100 in
`questions_extra3.py`. Q98 was missing from the source set, and the Q99 screenshot was an AWS Certified AI
Practitioner (AIF-C01) question, so it was left out. Domain 5 is the thinnest relative to its weight.

## Provenance and caveats

- Answers come from the pasted source set's marked answers and community consensus. The **explanations and citations were authored for this app** and the cited URLs were checked to resolve (HTTP 200), but explanations were not independently re-verified against each service's docs.
- **Answer-key check (`resources/` → `certyiq_key.py`).** The CertyIQ AIP-C01 PDF has 97 questions with answers, and every one of them was already in this bank (same numbering), so nothing new was added from it. Its key agrees with the bank on **93 of 97**; the app shows a 🔑 line on each answer. Where the key disagreed with my earlier derivation and I had no contrary evidence, I **adopted the key** (Q32, Q51, Q68, Q81, Q93). I **kept the bank's answer and added a note** on the four others: **Q21** and **Q30** (community vote disagrees with the key), **Q64** (Amazon Q index for ISVs pattern) and **Q82** (AWS docs: response streaming is REST-API-only). Q34 matches the key, but another source suggests B+C — also noted. Third-party keys can be wrong, so treat the disagreements as the items to double-check.
- **Q101** is a practice scenario (not a numbered official question). Q102 in your paste was a duplicate of Q34 and was not added again.
- **`resources/1.text` (second dump, 50 questions with answers + explanations):** 37 were already in the bank and skipped; the 13 new ones became **Q137–149** (`questions_extra5.py`). On the duplicates it agreed with the bank on 32 of 37 (one had no answer). The differences: file Q4 → bank Q82 (file says A; kept D per the AWS docs), file Q7 → bank Q8 (the file's letter contradicts its own explanation, no change), file Q17 → bank Q81 (three sources, three answers; noted) and file Q12 → bank Q34 (the file says B + C; the bank first followed it, then **went back to A + C** after CertyIQ's own page confirmed A + C and no AWS doc supports the B/VPC-endpoint option; noted on the question). This file's letters are not fully reliable and its explanations look machine-written, so each new answer was re-checked by reasoning; **Q138** is the one where I disagreed with its key (it says C; I chose B, noted).
- **Q105, Q115–119, Q122–136 (`questions_extra4.py`)** came from screenshots with the answers hidden and are *not* covered by the CertyIQ key (it stops at Q97), so they rest on my derivation alone; they were checked for duplicates against the rest of the bank (none). Least certain: **Q124** (low-moderate), then Q115, Q132, Q133, Q134 and Q135 (moderate) — each has a note naming the alternative. Q105 was numbered under a different site's Topic 3. Several of these questions read as machine-written, with plausible-sounding options that describe features that don't exist (e.g. Q123's 'sparse vector compression' in DynamoDB), so elimination of impossible options does most of the work.
- **Q31–97 and Q100 came from screenshots with the answers hidden**, so their answers were derived (exam guide + AWS docs) and then cross-checked against the key above. They have no vote data. Q37, Q41, Q47, Q54, Q64, Q82 and Q97 hinge on product details that were checked in AWS docs. The key agrees with most of the ones I had marked uncertain (Q36, Q50, Q67, Q77, Q78, Q79, Q86, Q90, Q91), which raises confidence in them. **Q100** is not in the key (it only covers Q1–97), so it rests on my derivation alone.
- Items flagged as disputed in the community vote carry a warning in the app: **Q1, Q3, Q13, Q15, Q16, Q24, Q28, Q29, Q30**. The weakest consensus is **Q24** (50%), **Q29** (57%) and **Q1** (59%).
- The Mock Exam draws up to 75 questions (the official count) at random from the 133, and the timer scales at 2.4 min/question (75 → 180 min).

## Question sets, timers and AI explanations (current)

- **Question sets:** the bank is cut into fixed sets of 25 questions by question number (Set 1 = Q1–Q25 …).
  Each set always uses the same questions in the same order, so you can repeat it and compare scores.
  Each set has its own timer at the official pace (2.4 min per question, so 60 min for 25 questions).
- **Full mock:** a random draw of up to 75 questions on the official 180-minute timer (unchanged).
- **Practice:** immediate feedback after each question (unchanged).
- **Results:** show the set name and the score per domain; wrong answers can be reviewed.
- **AI explanations (OpenRouter):** the *Get AI explanation* button tries each model in
  `OPENROUTER_MODELS` (config.py) in turn, so one busy model doesn't stop the explanation.
  Add the key as a Streamlit secret named `openrouter_api_key` (`api_key` also works), or as the
  `OPENROUTER_API_KEY` environment variable. A missing, rejected or out-of-credit key gets a clear message.

```toml
# .streamlit/secrets.toml (local) or the app's Secrets on Streamlit Cloud
openrouter_api_key = "sk-or-..."
```
