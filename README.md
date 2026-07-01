# 🛡️ GuardRail

> A security intelligence platform for AI-generated code - because apparently we now need software to babysit the software that writes our software. We live in interesting times.

GuardRail watches the code your AI assistant confidently hallucinated at 2am, runs it through a risk analysis pipeline, and politely tells you which parts are going to page you on a Saturday. Think of it as a smoke detector for your codebase, except it also explains _why_ there's smoke.

---

## 🤔 What is this thing, actually?

GuardRail ingests code submissions (the kind a CI pipeline or a GitHub webhook would throw at it), drops them onto a queue, and lets a worker chew through them asynchronously. The worker runs pattern checks **and** an LLM pass to sniff out risky coding practices, then stores the findings in a database you can query later.

In plain English: **code comes in → gets analyzed → risks come out → nobody cries in production.**

It's a learning project built to mirror a real-world Backend Engineer role (AI + developer tooling + security), so it deliberately uses the grown-up tools instead of duct tape and hope.

---

## 🧱 The Architecture (a.k.a. "where everything lives")

We're following **Clean Architecture**, which is a fancy way of saying _"dependencies point inward and nobody talks to the database directly like an animal."_

```
        ┌─────────────────────────────────────────┐
        │  API layer (FastAPI)                     │  ← the front door
        │   "Hi, I'd like to submit some code"     │
        └───────────────────┬─────────────────────┘
                            │
        ┌───────────────────▼─────────────────────┐
        │  Application layer (use cases)           │  ← the brain stem
        │   orchestrates the actual work           │
        └───────────────────┬─────────────────────┘
                            │
        ┌───────────────────▼─────────────────────┐
        │  Domain layer (entities + rules)         │  ← the soul
        │   knows nothing of databases or AWS      │
        │   blissfully unaware, deeply principled  │
        └───────────────────▲─────────────────────┘
                            │
        ┌───────────────────┴─────────────────────┐
        │  Infrastructure (DB, queue, AWS, LLM)    │  ← the plumbing
        │   does the dirty work nobody thanks it for│
        └──────────────────────────────────────────┘
```

**The Golden Rule:** the Domain layer is a hermit. It doesn't know FastAPI exists, has never heard of PostgreSQL, and thinks AWS is a sound you make when you stub your toe. Everything depends on the Domain; the Domain depends on no one. This is the Dependency Inversion Principle, and yes, it will feel weird until it suddenly feels obvious.

---

## 🗺️ The Flow (a day in the life of a code submission)

1. **Submission arrives** at the API. ("Please review my masterpiece.")
2. **Event gets queued.** The API doesn't analyze anything itself - it just takes a number and walks away, like a well-adjusted adult.
3. **A worker picks it up** off the queue, asynchronously, on its own time.
4. **Analysis runs:** pattern checks catch the usual suspects, the LLM catches the creative ones.
5. **Findings get saved** to PostgreSQL.
6. **You query the results** and feel a complicated mix of relief and dread.

This is **event-driven architecture** — the API and the worker are decoupled, so if analysis gets slow or busy, the front door stays snappy and nothing falls over. Resilience through commitment issues.

---

## 🧰 Tech Stack (the grown-up tools)

| Thing         | Tool                          | Why                                                     |
| ------------- | ----------------------------- | ------------------------------------------------------- |
| Language      | **Python 3.12+**              | It's what the AI/LLM world actually speaks              |
| API framework | **FastAPI**                   | Async, fast, generates its own docs so we don't have to |
| Database      | **PostgreSQL**                | The reliable friend who always shows up                 |
| Queue         | **Message queue (SQS-style)** | So the API and worker can ignore each other gracefully  |
| Cloud         | **AWS**                       | Where the magic (and the bill) happens                  |
| Brains        | **An LLM**                    | To catch the risks regex never could                    |

---

## 🚀 Getting Started

> ⚠️ This project is being built **one deliberate step at a time**. If you cloned this expecting a finished product, you're early. Pull up a chair.

```bash
# Clone it
git clone <your-repo-here> guardrail
cd guardrail

# Make a virtual environment (Python's way of not contaminating your whole machine)
python -m venv .venv

# Activate it
# macOS / Linux:
source .venv/bin/activate
# Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Install the goods
pip install -r requirements.txt

# Run the API
uvicorn app.api.main:app --reload

# Check it's alive
# Visit http://127.0.0.1:8000/health and bask in {"status": "ok"}
```

_Built with caffeine, Clean Architecture, and a healthy distrust of code that writes itself._ ☕
