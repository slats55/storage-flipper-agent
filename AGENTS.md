# Storage Flipper Agent — agent instructions

This file is the project anchor for AI assistants (same role as a `CLAUDE.md` in Claude Code).

## Docs to read first

- **`docs/BEST_PRACTICES.md`** — general agentic / collaboration reference (start here for “how we work”)
- `CURSOR_HANDOFF.md` — roles (Cursor vs Hermes), priorities
- `GAMEPLAN.md` — phases, handoffs
- `TASKS.md` — current checklist
- `research/` — implementation specs when present

## Tech

- Python 3.8+; imports use **`from modules.…`** with project root on `sys.path` (see `flipper_agent.py`, `demo.py`, `tests/conftest.py`).
- Run **`python -m pytest tests/ -q`** before considering work complete.

## Workflow

Follow **Research → Plan → Execute → Review → Ship** (see `docs/BEST_PRACTICES.md` and `.cursor/rules/agentic-workflow.mdc`), aligned with [claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice).

## Collaboration

- **Cursor (this agent):** code, tests, refactors  
- **Hermes:** live APIs, credentials, research, end-to-end validation  
- Coordination via owner (e.g. Telegram) per `GAMEPLAN.md`
