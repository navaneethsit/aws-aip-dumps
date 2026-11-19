"""
AIP-C01 Mock Exam — a Streamlit practice/mock-exam app for the
AWS Certified Generative AI Developer – Professional certification.

Run:  streamlit run app.py
"""
import html
import json
import math
import os
import re
import random
import time

import requests
import streamlit as st

from config import (AI, APP, DOMAIN_WEIGHTS, EXAM_MINUTES, EXAM_SIZE, MIN_PER_QUESTION,
                    OPENROUTER_MODELS, OPENROUTER_REFERER, OPENROUTER_TITLE, PASS_MARK, PERFORMANCE,
                    SET_MINUTES_PER_Q, SET_SIZE, STUDY_TIPS)
from exam import category_breakdown, is_correct, segment_score
from certyiq_key import CERTYIQ_KEY
from questions import CASE_STUDIES, CATEGORIES, QUESTIONS

QBY_ID = {q["id"]: q for q in QUESTIONS}
# Fixed sets: Set 1 = the first 25 questions by number, Set 2 = the next 25, and so on.
SETS = [sorted(q["id"] for q in QUESTIONS)[i:i + SET_SIZE]
        for i in range(0, len(QUESTIONS), SET_SIZE)]

# --------------------------------------------------------------------------- #
# Page setup + styling
# --------------------------------------------------------------------------- #
st.set_page_config(page_title=APP["title"], page_icon=APP["icon"], layout="wide")

DARK_CSS = """
<style>
:root{--bg:#0e1321;--panel:#182033;--panel2:#1e2740;--ink:#eef2f8;--muted:#aab4c8;--line:#34405c;--accent:#ff9f2e;}
.stApp,[data-testid="stAppViewContainer"],[data-testid="stHeader"]{background:var(--bg)!important;color:var(--ink)!important;}
[data-testid="stSidebar"]>div{background:#121a2c!important;}
.stApp p,.stApp li,.stApp label,.stApp span,.stApp h1,.stApp h2,.stApp h3,.stApp h4,.stApp strong,.stApp td,.stApp th{color:var(--ink)!important;}
.stApp [data-testid="stCaptionContainer"],.stApp small{color:var(--muted)!important;}
[data-testid="stMarkdownContainer"] p{font-size:1.04rem;line-height:1.62;}
[data-testid="stVerticalBlockBorderWrapper"]{background:var(--panel);border-color:var(--line)!important;border-radius:14px!important;padding:.4rem .6rem;}
[data-testid="stExpander"]{background:var(--panel);border:1px solid var(--line)!important;border-radius:12px;}
[data-testid="stExpander"] summary,[data-testid="stExpander"] p{color:var(--ink)!important;}
[data-testid="stMetric"]{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:.6rem .8rem;}
[data-testid="stMetricLabel"] p{color:var(--muted)!important;}
[data-testid="stMetricValue"]{color:var(--ink)!important;}
input,textarea,[data-baseweb="select"]>div,[data-baseweb="input"]>div{background:var(--panel2)!important;color:var(--ink)!important;border-color:var(--line)!important;}
[data-baseweb="select"] input::placeholder,[data-baseweb="select"] [aria-live],[data-baseweb="select"] div[class*="placeholder"]{color:var(--muted)!important;opacity:1!important;}
[data-baseweb="popover"] li,[data-baseweb="menu"] li{background:var(--panel2)!important;color:var(--ink)!important;}
.stButton>button{background:var(--panel2);color:var(--ink)!important;border:1px solid var(--line);border-radius:10px;font-weight:600;}
.stButton>button:hover{border-color:var(--accent);color:var(--accent)!important;}
.stButton>button[kind="primary"]{background:var(--accent);color:#1b1100!important;border-color:var(--accent);}
[data-testid="stProgress"]>div>div>div{background:var(--accent);}
[data-testid="stAlert"]{border-radius:12px;background:#1d2740!important;border:1px solid var(--line);border-left:4px solid var(--accent);}
[data-testid="stAlert"] *{color:var(--ink)!important;}
[data-testid="stAlert"] p{font-size:1rem;line-height:1.6;}
hr{border-color:var(--line)!important;}
[data-testid="stSidebar"] .stButton>button{padding:.35rem .1rem;min-width:0;}
[data-testid="stSidebar"] .stButton>button p{white-space:nowrap;font-size:.92rem;}
.pill{display:inline-block;padding:.22rem .7rem;border-radius:999px;font-size:.78rem;background:rgba(255,159,46,.18);color:#ffb865!important;font-weight:700;margin-right:.45rem;letter-spacing:.3px;}
.pill.type{background:rgba(120,150,220,.2);color:#b9cdfb!important;}
.pill.flag{background:rgba(255,80,80,.2);color:#ff9a9a!important;}
.main-header{background:linear-gradient(100deg,#0b1a33 0%,#1b2e52 55%,#7a3e00 100%)!important;border:1px solid var(--line);}
.main-header h1,.main-header p{color:#fff!important;}
@media (max-width:640px){.block-container{padding:1rem .75rem 3rem!important;}}
</style>
"""
st.html(DARK_CSS)




# --------------------------------------------------------------------------- #
# Optional AI explanations (OpenRouter) — cached per question
# --------------------------------------------------------------------------- #
def ai_key():
    """OpenRouter key from Streamlit secrets (openrouter_api_key or api_key) or the environment."""
    for name in ("openrouter_api_key", "api_key"):
        try:
            v = st.secrets.get(name)
        except Exception:
            v = None
        if v:
            return v
    return os.environ.get("OPENROUTER_API_KEY")


class AIError(Exception):
    """An AI problem we can explain to the user in plain words."""


def _answer_list(q: dict) -> list[str]:
    return [q["answer"]] if q["type"] == "single" else list(q["answer"])


def _letter(opt: str) -> str:
    return opt.strip()[:1].upper()


def _selected_options(q: dict, response) -> list[str]:
    if not response:
        return []
    return list(response) if isinstance(response, list) else [response]


def _parse_json(text: str) -> dict:
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise AIError("The AI reply was not in the expected format. Try again.")
    try:
        return json.loads(m.group(0))
    except ValueError as e:
        raise AIError("The AI reply could not be read. Try again.") from e


def ask_ai(q: dict, response, correct: bool) -> dict:
    """-> {'requirement': str, 'options': {letter: explanation}} for every option letter."""
    key = ai_key()
    if not key:
        raise AIError("No OpenRouter key is configured. Add `openrouter_api_key` to the app's Secrets.")
    marked = [_letter(x) for x in _answer_list(q)]
    selected = [_letter(x) for x in _selected_options(q, response)]
    prompt = (
        "QUESTION:\n" + q["question"] + "\n\n"
        "OPTIONS:\n" + "\n".join(q["options"]) + "\n\n"
        "MARKED CORRECT ANSWER: " + ", ".join(marked) + "\n"
        "LEARNER SELECTED: " + (", ".join(selected) if selected else "nothing") + "\n"
        "TRUSTED EXPLANATION: " + q.get("explanation", "") + "\n"
        "DOCUMENTATION: " + q.get("reference", "") + "\n"
    )
    headers = {"Authorization": "Bearer " + key, "Content-Type": "application/json",
               "HTTP-Referer": OPENROUTER_REFERER, "X-Title": OPENROUTER_TITLE}
    problems = []
    for model in OPENROUTER_MODELS:
        try:
            r = requests.post(
                AI["base_url"], headers=headers, timeout=60,
                json={"model": model,
                      "messages": [{"role": "system", "content": AI["system_prompt"]},
                                   {"role": "user", "content": prompt}],
                      "max_tokens": AI["max_tokens"], "temperature": AI["temperature"]},
            )
        except requests.RequestException as e:
            problems.append(model + ": network error (" + type(e).__name__ + ")")
            continue
        if r.status_code in (401, 403):
            raise AIError("OpenRouter rejected the key. Check `openrouter_api_key` in the app's Secrets.")
        if r.status_code == 402:
            raise AIError("OpenRouter says the account has no credit left. Add credits and try again.")
        if r.status_code != 200:
            problems.append(model + ": HTTP " + str(r.status_code))
            continue
        try:
            text = r.json()["choices"][0]["message"]["content"] or ""
        except (KeyError, IndexError, ValueError):
            problems.append(model + ": unexpected reply")
            continue
        if not text.strip():
            problems.append(model + ": empty reply")
            continue
        data = _parse_json(text)
        exp = {}
        for item in data.get("options") or []:
            L = str(item.get("letter", "")).strip().upper()[:1]
            if L:
                exp[L] = str(item.get("explanation", "")).strip()
        return {"requirement": str(data.get("requirement", "")).strip(), "options": exp}
    raise AIError("No model answered (" + "; ".join(problems) + "). Try again in a minute.")


def _esc_money(t: str) -> str:
    return t.replace("$", "\\$")


def _opt_text(q: dict, letter: str) -> str:
    for o in q["options"]:
        if _letter(o) == letter:
            t = o[3:].strip()
            return t if len(t) <= 110 else t[:107].rstrip() + "…"
    return ""


def render_ai(q: dict, res: dict, response, correct: bool) -> str:
    """Build the explanation in the order the learner asked for:
    1. exact selection + verdict, 2. the selected options explained,
    3. the correct answer explained (if the learner was wrong), 4. the remaining options."""
    marked = [_letter(x) for x in _answer_list(q)]
    selected = [_letter(x) for x in _selected_options(q, response)]
    exp = res.get("options", {})
    missing = "_(no explanation returned for this option)_"
    lines = []
    sel_txt = ", ".join(selected) if selected else "nothing"
    verdict = "✅ **Correct**" if correct else "❌ **Incorrect**"
    lines.append(f"**You selected:** {sel_txt} — {verdict}")
    if res.get("requirement"):
        lines.append(f"**Decisive requirement:** {res['requirement']}")

    def bullet(L: str, tag: str) -> str:
        t = _opt_text(q, L)
        return f"- **{L}.** {tag}{_esc_money(t)}  \n  {_esc_money(exp.get(L, missing))}"

    if selected:
        lines.append("\n**Your choice**")
        for L in selected:
            tag = "✅ correct — " if L in marked else "❌ incorrect — "
            lines.append(bullet(L, tag))
    if not correct:
        lines.append("\n**The correct answer**")
        for L in marked:
            tag = "✅ " + ("(you also picked this) — " if L in selected else "")
            lines.append(bullet(L, tag))
    rest = [o for o in (_letter(x) for x in q["options"]) if o not in selected and o not in marked]
    if rest:
        lines.append("\n**Why the other choices are wrong**")
        for L in rest:
            lines.append(bullet(L, "❌ "))
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Session state
# --------------------------------------------------------------------------- #
def init_state():
    ss = st.session_state
    ss.setdefault("mode", "home")
    ss.setdefault("deck", [])
    ss.setdefault("pos", 0)
    ss.setdefault("history", [])
    ss.setdefault("answered_ids", set())
    ss.setdefault("flags", set())
    ss.setdefault("exam_started_at", None)
    ss.setdefault("exam_minutes", EXAM_MINUTES)
    ss.setdefault("submitted", False)
    ss.setdefault("ai_cache", {})


init_state()


def start_session(mode: str, categories: list[str], fixed_ids: list[int] | None = None, label: str = ""):
    ss = st.session_state
    if fixed_ids is not None:                 # a numbered set: same questions, same order, every time
        ids = list(fixed_ids)
    else:
        pool = [q for q in QUESTIONS if not categories or q["category"] in categories]
        ids = [q["id"] for q in pool]
        random.shuffle(ids)                   # rotating draw — different every attempt
        if mode == "exam":
            ids = ids[: min(EXAM_SIZE, len(ids))]
    ss.label = label
    ss = st.session_state
    ss.mode, ss.deck, ss.pos = mode, ids, 0
    ss.history, ss.answered_ids, ss.flags = [], set(), set()
    ss.submitted = False
    ss.exam_started_at = time.time() if mode == "exam" else None
    # Timer scales with deck size at the official pace (2.4 min per question). Sets use the same pace.
    pace = SET_MINUTES_PER_Q if fixed_ids is not None else MIN_PER_QUESTION
    cap = EXAM_MINUTES if fixed_ids is None else 10_000
    ss.exam_minutes = min(cap, max(1, math.ceil(len(ids) * pace)))


def reset_home():
    for k in ("deck", "pos", "history", "answered_ids", "flags",
              "exam_started_at", "submitted", "label"):
        st.session_state.pop(k, None)
    st.session_state.mode = "home"
    init_state()


# --------------------------------------------------------------------------- #
# Response helpers
# --------------------------------------------------------------------------- #
def read_response(q: dict, key_prefix: str):
    ss = st.session_state
    if q["type"] == "single":
        return ss.get(f"{key_prefix}_r")
    if q["type"] == "multi":
        return [o for o in q["options"] if ss.get(f"{key_prefix}_c_{o}")]
    return None


def has_answer(q: dict, key_prefix: str) -> bool:
    r = read_response(q, key_prefix)
    if isinstance(r, list):
        return bool(r)
    return r is not None


def pills(q: dict, flagged: bool = False) -> str:
    task = f'<span class="pill">TASK {q["task"]}</span>' if q.get("task") else ""
    flag = '<span class="pill flag">🚩 FLAGGED</span>' if flagged else ""
    return (f'<span class="pill">{q["category"]}</span>{task}'
            f'<span class="pill type">{"CHOOSE " + str(len(q["answer"])) if q["type"] == "multi" else "SINGLE"}</span>'
            f'{flag}')


def render_question_body(q: dict, key_prefix: str):
    if q.get("case"):
        with st.expander("📄 Case study scenario", expanded=False):
            st.markdown(CASE_STUDIES[q["case"]])
    st.markdown(q["question"].replace("\n", "\n\n"))

    if q["type"] == "single":
        return st.radio("Select one:", q["options"], index=None, key=f"{key_prefix}_r")
    if q["type"] == "multi":
        st.caption(f"Select all that apply ({len(q['answer'])} correct) — all-or-nothing.")
        return [o for o in q["options"] if st.checkbox(o, key=f"{key_prefix}_c_{o}")]
    return None


def render_correct(q: dict):
    if q["type"] == "single":
        st.markdown(f"**Correct answer:** {q['answer']}")
    else:
        st.markdown("**Correct answers:**")
        for a in q["answer"]:
            st.markdown(f"- {a}")



CALLOUT = {
    "success": ("#133a27", "#d4f8e4", "#3ddc97"),
    "error": ("#3d1d26", "#ffd9e0", "#ff6b7f"),
    "info": ("#1c2b4b", "#dce9ff", "#7aa7ff"),
    "warn": ("#3d3317", "#ffecaa", "#ffc857"),
}


def _md_html(text: str) -> str:
    """Tiny markdown -> HTML for explanations: **bold**, `code`, '- ' bullets, paragraphs."""
    out, ul = [], False
    for raw in html.escape(text).split("\n"):
        line = raw.strip()
        if not line:
            if ul:
                out.append("</ul>"); ul = False
            continue
        line = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)
        line = re.sub(r"`([^`]+)`", r"<code>\1</code>", line)
        if line.startswith("- "):
            if not ul:
                out.append("<ul>"); ul = True
            out.append("<li>" + line[2:] + "</li>")
        else:
            if ul:
                out.append("</ul>"); ul = False
            out.append("<p>" + line + "</p>")
    if ul:
        out.append("</ul>")
    return "".join(out)


def callout(kind: str, body: str, raw: bool = False) -> None:
    """A coloured message box with its colours set inline, so it reads well in any Streamlit version."""
    bg, fg, edge = CALLOUT[kind]
    inner = body if raw else _md_html(body)
    st.html(
        f'<div style="background:{bg};color:{fg};border-left:4px solid {edge};border-radius:12px;'
        f'padding:12px 16px;margin:6px 0 10px;font-size:1rem;line-height:1.6;">'
        f'<style>.co p{{margin:0 0 6px}} .co ul{{margin:0 0 6px 1.2em;padding:0}}</style>'
        f'<div class="co">{inner}</div></div>'
    )


def render_extras(q: dict):
    """Explanation, community-vote caution, and citation."""
    callout("info", q["explanation"])
    if q.get("votes"):
        split = " · ".join(f"{k} {v}%" for k, v in q["votes"].items())
        st.caption(f"🗳️ Community vote: {split}")
    key = CERTYIQ_KEY.get(q["id"])
    if key:
        mine = q["answer"][0] if q["type"] == "single" else "".join(sorted(a[0] for a in q["answer"]))
        if key == mine:
            st.caption("🔑 Agrees with the CertyIQ answer key.")
        else:
            st.caption(f"🔑 CertyIQ answer key says **{key}** — see the note below.")
    if q.get("reference"):
        st.caption(f"📚 Citation: {q['reference']}")


def render_feedback(q: dict, response):
    correct = is_correct(q, response)
    earned, total = segment_score(q, response)
    callout("success" if correct else "error",
            ("✅ Correct!" if correct else "❌ Not quite.") + f"  ({earned}/{total} point)", raw=True)
    render_correct(q)
    render_extras(q)

    if ai_key():
        ss = st.session_state
        chosen = "|".join(sorted(_selected_options(q, response))) or "none"
        ckey = str(q["id"]) + "::" + chosen
        if ckey in ss.ai_cache:
            with st.container(border=True):
                st.markdown("🤖 **AI explanation**")
                st.markdown(render_ai(q, ss.ai_cache[ckey], response, correct))
                st.caption("📚 " + q.get("reference", ""))
        elif st.button("🤖 AI explanation", key="ai_" + str(q["id"]) + "_" + chosen):
            with st.spinner("Explaining your answer…"):
                try:
                    ss.ai_cache[ckey] = ask_ai(q, response, correct)
                except AIError as e:
                    callout("warn", html.escape(str(e)), raw=True)  # not cached: the user can retry
                    return
                except Exception as e:
                    callout("warn", "AI explanation unavailable: " + html.escape(type(e).__name__) + ". Try again.", raw=True)
                    return
            st.rerun()


def record(q: dict, response):
    e, t = segment_score(q, response)
    st.session_state.history.append({
        "id": q["id"], "category": q["category"], "question": q["question"][:90],
        "is_correct": is_correct(q, response), "earned": e, "total": t,
    })
    st.session_state.answered_ids.add(q["id"])


# --------------------------------------------------------------------------- #
# Header
# --------------------------------------------------------------------------- #
st.html(
    f"""<div class="main-header"><h1>{APP['icon']} {APP['title']}</h1>
    <p>{APP['subtitle']} · v{APP['version']} · {len(QUESTIONS)} questions across
    {len(CATEGORIES)} domains</p></div>""")


# --------------------------------------------------------------------------- #
# HOME
# --------------------------------------------------------------------------- #
def view_home():
    n_exam = min(EXAM_SIZE, len(QUESTIONS))
    n_min = min(EXAM_MINUTES, max(1, math.ceil(n_exam * MIN_PER_QUESTION)))
    c1, c2 = st.columns(2)
    with c1, st.container(border=True):
        st.markdown("### 📝 Practice")
        st.write("Immediate feedback, the correct answer, an explanation of why each "
                 "distractor fails, and an AWS documentation citation after each question. "
                 "Optional AI coach.")
    with c2, st.container(border=True):
        st.markdown("### ⏱️ Mock Exam")
        st.write(f"**{n_exam} questions · {n_min} minutes** (official exam: 75 questions · "
                 f"180 min; timer scales at 2.4 min/question), scored at the end against the "
                 f"{PASS_MARK}% pass mark (750/1000). Multiple-response items are "
                 "all-or-nothing. Flag questions and jump around with the navigator.")

    st.write("")
    cats = st.multiselect("Filter by domain (optional — leave empty for all):", CATEGORIES)
    b1, b2 = st.columns(2)
    if b1.button("▶️ Start Practice", use_container_width=True, type="primary"):
        start_session("practice", cats)
        st.rerun()
    if b2.button("⏱️ Start Mock Exam", use_container_width=True):
        start_session("exam", cats)
        st.rerun()

    st.divider()
    st.markdown("#### 📚 Question sets")
    st.caption(f"The bank is split into fixed sets of {SET_SIZE} questions (by question number). "
               "Every set is the same questions in the same order each time, so you can repeat a set and "
               "compare scores. Each set has its own timer at the official pace.")
    labels = []
    for i, ids in enumerate(SETS, 1):
        mins = max(1, math.ceil(len(ids) * SET_MINUTES_PER_Q))
        labels.append(f"Set {i} · Q{ids[0]}–Q{ids[-1]} · {len(ids)} questions · {mins} min")
    pick = st.selectbox("Choose a set", range(len(SETS)), format_func=lambda i: labels[i], key="set_pick")
    if st.button(f"⏱️ Start {labels[pick].split(' · ')[0]}", use_container_width=True, key="start_set"):
        start_session("exam", [], fixed_ids=SETS[pick], label=labels[pick].split(" · ")[0])
        st.rerun()

    st.divider()
    left, right = st.columns([1, 1])
    with left:
        st.markdown("#### 💡 Study tips")
        for t in STUDY_TIPS:
            st.markdown(f"- {t}")
    with right:
        st.markdown("#### 📚 Coverage by domain (official weight)")
        counts = {c: 0 for c in CATEGORIES}
        for q in QUESTIONS:
            counts[q["category"]] += 1
        for c, w in zip(CATEGORIES, DOMAIN_WEIGHTS.values()):
            st.markdown(f"- **{c}** — {counts[c]} questions · {w}% of exam")


# --------------------------------------------------------------------------- #
# PRACTICE
# --------------------------------------------------------------------------- #
def view_practice():
    ss = st.session_state
    if ss.pos >= len(ss.deck):
        ss.mode = "results"
        st.rerun()

    q = QBY_ID[ss.deck[ss.pos]]
    st.html(pills(q))
    st.caption(f"Question {ss.pos + 1} of {len(ss.deck)}")

    with st.container(border=True):
        render_question_body(q, key_prefix=f"p{q['id']}")

    if not ss.submitted:
        if st.button("Submit", type="primary"):
            ss.submitted = True
            record(q, read_response(q, key_prefix=f"p{q['id']}"))
            st.rerun()
    else:
        render_feedback(q, read_response(q, key_prefix=f"p{q['id']}"))
        n1, n2, _ = st.columns([1, 1, 4])
        if n1.button("➡️ Next", type="primary"):
            ss.pos += 1
            ss.submitted = False
            st.rerun()
        if n2.button("🏁 Finish"):
            ss.mode = "results"
            st.rerun()
    _sidebar_practice()


# --------------------------------------------------------------------------- #
# EXAM
# --------------------------------------------------------------------------- #
def view_exam():
    ss = st.session_state

    @st.fragment(run_every=1)
    def clock():
        remaining = ss.exam_minutes * 60 - (time.time() - ss.exam_started_at)
        if remaining <= 0:
            st.session_state._force_submit = True
            st.rerun(scope="app")
        mm, s = divmod(int(remaining), 60)
        color = "#c62828" if remaining < 300 else "inherit"
        st.html(
            f"<div style='text-align:right;font-size:1.4rem;font-weight:700;"
            f"font-variant-numeric:tabular-nums;color:{color}'>⏱ {mm:02d}:{s:02d}</div>"
        )

    if ss.get("_force_submit"):
        ss.pop("_force_submit", None)
        _grade_exam()
        return

    q = QBY_ID[ss.deck[ss.pos]]
    top = st.columns([3, 1])
    with top[0]:
        answered_n = sum(1 for qid in ss.deck if has_answer(QBY_ID[qid], f"e{qid}"))
        st.progress(answered_n / len(ss.deck))
        st.caption(f"Question {ss.pos + 1} of {len(ss.deck)} · answered {answered_n} · "
                   f"flagged {len(ss.flags)}")
    with top[1]:
        clock()

    st.html(pills(q, flagged=q["id"] in ss.flags))

    with st.container(border=True):
        render_question_body(q, key_prefix=f"e{q['id']}")

    flagged = q["id"] in ss.flags
    nav = st.columns([1, 1, 1.2, 1.4, 3])
    if nav[0].button("⬅️ Prev", disabled=ss.pos == 0):
        ss.pos -= 1
        st.rerun()
    if nav[1].button("Next ➡️", disabled=ss.pos >= len(ss.deck) - 1):
        ss.pos += 1
        st.rerun()
    if nav[2].button("🚩 Unflag" if flagged else "🚩 Flag"):
        ss.flags.discard(q["id"]) if flagged else ss.flags.add(q["id"])
        st.rerun()
    if nav[3].button("✅ Submit exam", type="primary"):
        _grade_exam()
        return

    _exam_navigator()


def _exam_navigator():
    ss = st.session_state
    with st.sidebar:
        st.subheader("Navigator")
        st.caption("● answered · 🚩 flagged · ▸ current")
        cols = st.columns(5)
        for idx, qid in enumerate(ss.deck):
            answered = has_answer(QBY_ID[qid], f"e{qid}")
            mark = "▸" if idx == ss.pos else ("🚩" if qid in ss.flags else
                                              ("●" if answered else "○"))
            if cols[idx % 5].button(f"{mark}{idx + 1}", key=f"jump{idx}"):
                ss.pos = idx
                st.rerun()
        st.divider()
        if st.button("✅ Submit exam now", use_container_width=True, type="primary"):
            _grade_exam()
            st.rerun()
        if st.button("🚪 Quit to home", use_container_width=True):
            reset_home()
            st.rerun()


def _grade_exam():
    ss = st.session_state
    ss.history = []
    for qid in ss.deck:
        q = QBY_ID[qid]
        record(q, read_response(q, key_prefix=f"e{qid}"))
    ss.mode = "results"
    st.rerun()


# --------------------------------------------------------------------------- #
# RESULTS
# --------------------------------------------------------------------------- #
def view_results():
    ss = st.session_state
    hist = ss.history
    if not hist:
        callout("info", "No answered questions yet.")
        if st.button("🏠 Home"):
            reset_home(); st.rerun()
        return

    earned = sum(h["earned"] for h in hist)
    total = sum(h["total"] for h in hist)
    pct = round(100 * earned / total) if total else 0
    scaled = 100 + round(9 * pct)          # rough 100–1000 equivalent for orientation
    passed = pct >= PASS_MARK

    st.subheader("📊 Results" + (f" — {ss.get('label')}" if ss.get("label") else ""))
    m = st.columns(4)
    m[0].metric("Score", f"{pct}%", help=f"≈ {scaled}/1000 (illustrative; AWS scores are scaled)")
    m[1].metric("Points", f"{earned}/{total}")
    m[2].metric("Questions", len(hist))
    m[3].metric("Result", "PASS ✅" if passed else "FAIL ❌")
    st.progress(pct / 100)
    callout("success" if passed else "error",
            f"{'🎉 Above' if passed else 'Below'} the {PASS_MARK}% pass mark (750/1000)."
            + ("" if passed else " Focus on the weakest domains below."))

    st.markdown("#### Performance by domain")
    cb = category_breakdown(hist)
    for cat, d in sorted(cb.items(), key=lambda x: x[1]["correct"] / x[1]["total"]):
        rate = round(100 * d["correct"] / d["total"])
        bar = "🟩" if rate >= PERFORMANCE["good"] else "🟨" if rate >= PERFORMANCE["fair"] else "🟥"
        st.markdown(f"{bar} **{cat}** — {d['correct']}/{d['total']} ({rate}%)")

    st.markdown("#### Review answers")
    only_wrong = st.toggle("Show only incorrect", value=False)
    for i, h in enumerate(hist, 1):
        if only_wrong and h["is_correct"]:
            continue
        q = QBY_ID[h["id"]]
        icon = "✅" if h["is_correct"] else "❌"
        with st.expander(f"{icon} Q{i}. [{q['category']}] {h['question']}…"):
            render_correct(q)
            render_extras(q)

    r1, r2 = st.columns(2)
    if r1.button("🔁 New session", type="primary"):
        reset_home(); st.rerun()
    if r2.button("🏠 Home"):
        reset_home(); st.rerun()


# --------------------------------------------------------------------------- #
# Practice sidebar
# --------------------------------------------------------------------------- #
def _sidebar_practice():
    ss = st.session_state
    with st.sidebar:
        st.subheader("Progress")
        answered = len(ss.history)
        correct = sum(1 for h in ss.history if h["is_correct"])
        st.metric("Answered", f"{answered}/{len(ss.deck)}")
        if answered:
            st.metric("Accuracy", f"{round(100 * correct / answered)}%")
        st.divider()
        if st.button("🏁 Finish now", use_container_width=True):
            ss.mode = "results"; st.rerun()
        if st.button("🚪 Quit to home", use_container_width=True):
            reset_home(); st.rerun()


# --------------------------------------------------------------------------- #
# Router
# --------------------------------------------------------------------------- #
mode = st.session_state.mode
if mode == "home":
    view_home()
elif mode == "practice":
    view_practice()
elif mode == "exam":
    view_exam()
elif mode == "results":
    view_results()
else:
    reset_home()
    st.rerun()
