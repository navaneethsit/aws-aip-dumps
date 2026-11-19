"""Configuration for the AIP-C01 practice / mock exam app."""

APP = {
    "title": "AIP-C01 Mock Exam",
    "subtitle": "AWS Certified Generative AI Developer – Professional",
    "icon": "🤖",
    "version": "1.0",
}

# Official: scaled score 100-1000, pass = 750 (~75%).
PASS_MARK = 75  # percent

# Official format: 75 questions (65 scored + 10 unscored) in 180 minutes.
# The mock draws up to EXAM_SIZE questions from the bank (capped at bank size)
# and scales the timer at MIN_PER_QUESTION (180 / 75 = 2.4 min) up to EXAM_MINUTES.
EXAM_SIZE = 75
EXAM_MINUTES = 180
MIN_PER_QUESTION = 2.4

# Official domain weights (share of scored content) — shown on the home page.
DOMAIN_WEIGHTS = {
    "1 · FM Integration, Data & Compliance": 31,
    "2 · Implementation & Integration": 26,
    "3 · Safety, Security & Governance": 20,
    "4 · Operational Efficiency & Optimization": 12,
    "5 · Testing, Validation & Troubleshooting": 11,
}

# --- Optional AI explanations (OpenRouter). Left disabled by default. --------
# To enable: add `openrouter_api_key = "sk-..."` to .streamlit/secrets.toml
AI = {
    "base_url": "https://openrouter.ai/api/v1/chat/completions",
    "max_tokens": 600,
    "temperature": 0.1,
    "system_prompt": (
        "You are an AWS Generative AI solutions architect coaching someone for the AIP-C01 exam. "
        "You are given the question, the options, the MARKED correct answer and a trusted explanation. "
        "Rules:\n"
        "- The marked correct answer is authoritative. Do not second-guess it or pick a different answer.\n"
        "- Explain the learner's own choice specifically: which requirement it fails or satisfies.\n"
        "- Stay grounded in the trusted explanation and in standard AWS behaviour; do not invent features or limits.\n"
        "- Plain language, short sentences, no filler. Do not restate the whole question.\n"
        "Reply in exactly this markdown structure:\n"
        "**Your answer:** correct or incorrect, in one line.\n"
        "**Why the correct answer is right:** one or two sentences tied to the requirement.\n"
        "**About your choice:** if correct, say which requirement it meets; if incorrect, say which requirement it breaks.\n"
        "**Remember:** one line takeaway.\n"
        "Keep the whole reply under 170 words."
    ),
}

PERFORMANCE = {"excellent": 90, "good": 80, "fair": 75}

# Question sets: the bank, sorted by question number, cut into fixed sets so every set is repeatable.
# Timer per set uses the same official pace (2.4 min per question).
SET_SIZE = 25
SET_MINUTES_PER_Q = MIN_PER_QUESTION

# OpenRouter: the first model is tried first; if it fails or is rate-limited the next one is used.
OPENROUTER_MODELS = [
    "mistralai/mistral-small-3.2-24b-instruct",
    "meta-llama/llama-3.3-70b-instruct",
    "openai/gpt-4o-mini",
]
OPENROUTER_REFERER = "https://share.streamlit.io"
OPENROUTER_TITLE = "AIP-C01 Mock Exam"

STUDY_TIPS = [
    "🎯 Find the decisive requirement first: LEAST operational overhead, lowest latency, proactive, no redeploy, auditable.",
    "🧩 Prefer managed/native options (Bedrock Knowledge Bases, Guardrails, Prompt Management, Prompt Flows, AppConfig) over custom code.",
    "🚫 Eliminate distractors that use a real service for the wrong job, describe a feature that doesn't exist, or react when the stem needs prevention.",
    "🔎 RAG is the heaviest topic: chunking, vector store choice, hybrid search, reranking, metadata filtering.",
    "🛡️ Guardrails: denied topics vs content filters vs word filters vs contextual grounding vs PII.",
    "🔐 Private connectivity = interface VPC endpoints (PrivateLink); fine-grained data access = Lake Formation.",
    "⚡ Streaming = InvokeModelWithResponseStream + WebSocket/SSE. Config without redeploy = AppConfig.",
    "✅ Multiple-response items are all-or-nothing — pick exactly the stated number.",
]
