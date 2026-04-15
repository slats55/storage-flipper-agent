# General best practices — AI-assisted development

This is a **human-readable reference** for how we work on this repo. It aligns with [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) (Claude Code patterns) and maps them to **Cursor + this codebase**.

Machine-scoped reminders live in `.cursor/rules/` and `AGENTS.md`.

---

## Core workflow: Research → Plan → Execute → Review → Ship

| Phase | What to do |
|--------|------------|
| **Research** | Read specs, existing code, and tests before editing. Search the repo; don’t guess APIs. |
| **Plan** | For non-trivial work, outline steps and scope. Prefer one coherent change over mixed refactors. |
| **Execute** | Smallest diff that satisfies the request. Match local style, types, and patterns. |
| **Review** | Run tests and linters; fix failures. Re-read diffs for accidental edits. |
| **Ship** | Clear commit message; hand off integration/credentials to the right owner (here: often **Hermes** per `GAMEPLAN.md`). |

---

## Specs and ambiguity

- **Reduce ambiguity before coding** — short written spec or bullet acceptance criteria beats a vague ticket.
- **Phase-wise work** — split large efforts; gate each phase with tests or a demo.
- **Prototype vs spec** — for exploration, fast spikes are fine; once direction is set, document it (e.g. under `research/`).

---

## Testing and verification

- **Run tests before declaring done:** `python -m pytest tests/ -q` from the project root (after `pip install -r requirements.txt`).
- **Mock external systems** in unit tests (e.g. Hermes CLI) so CI and local runs don’t need live keys.
- Prefer **new or updated tests** when behavior changes.

---

## Git and collaboration

- Prefer **small, logical commits** (one feature or fix per commit when practical) so review and `git revert` stay easy.
- Avoid committing **secrets** (`.env` is gitignored).
- For cross-agent handoffs (Cursor ↔ Hermes), note **what to test** and **dependencies** in the PR or chat.

---

## Prompting (working with AI)

- **Be specific** — files, acceptance criteria, and out-of-scope items.
- **Challenge outputs** — ask for edge cases, tests, or “what could break?” when risk is high.
- **Don’t micromanage every line** — give goal + constraints; let the agent propose and you correct.
- Reuse **repeatable workflows** as Cursor rules or short scripts instead of retyping long prompts.

---

## Claude Code vs Cursor (mental model)

| Idea | Here |
|------|------|
| `CLAUDE.md` | `AGENTS.md`, `docs/BEST_PRACTICES.md`, handoff docs |
| Slash commands / skills | Cursor rules (`.cursor/rules/`) and user skills |
| Subagents / parallel work | Split tasks; Hermes for research/runtime validation |
| MCP / tools | Use when available; document required env in `.env.example` |

---

## This repository

- **Imports:** `from modules.…` with project root on `sys.path` — see `flipper_agent.py` and `tests/conftest.py`.
- **Logging / retries:** Preserve existing patterns in `modules/` unless changing behavior is the task.
- **Docs index:** `CURSOR_HANDOFF.md`, `GAMEPLAN.md`, `TASKS.md`, `research/`.

---

## Further reading

- Upstream concepts and links: [claude-code-best-practice README](https://github.com/shanraisshan/claude-code-best-practice/blob/main/README.md)
- Official Claude Code docs: [code.claude.com/docs](https://code.claude.com/docs)
