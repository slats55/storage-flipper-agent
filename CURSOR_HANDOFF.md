# CURSOR HANDOFF DOCUMENT
Storage Unit Flipper Agent - Complete Development Brief

**Your Role**: Code Developer (Python)
**Partner**: Hermes Agent (Research & Testing)
**Owner**: Myles
**Status**: Phase 2 Week 1 — **plumbing done** (logging, retries, tests, batch UX). **Blocked on Hermes** for `vision_analyze` contract and real eBay/sold-listing data path.

## QUICK START

1. You write code, Cursor handles development
2. Hermes researches APIs and tests integrations  
3. Communication flows through Myles (via Telegram)

## PROJECT SUMMARY

Build AI automation for storage unit flipping business:
- **Problem**: 40-80 hours per unit processing items manually
- **Solution**: AI identifies items, prices them, generates listings
- **Goal**: Reduce to 10-15 hours (75% time savings)
- **Client**: Processes 200-500 items per unit, sells on eBay/Facebook/Mercari/OfferUp

## IMMEDIATE TASKS

**Task 1: Add Logging** (Priority 1) — **DONE**
- `modules/agent_logging.py` + `configure_logging()`; loggers under `flipper.*`
- File: `logs/agent.log`; console: INFO+. Format: timestamp, level, logger, message

**Task 2: Error Handling** (Priority 1) — **DONE**
- `modules/retry_utils.py`: exponential backoff + jitter (used for Hermes subprocess timeouts)
- Price research always returns a pricing dict (category fallback if Hermes fails)
- Batch: per-item try/except; vision/Hermes missing → filename-based fallback (no hard crash)

**Task 3: Vision Integration** — **BLOCKED (Hermes)**
- Integrate Hermes **vision_analyze** API (or documented equivalent)
- Parse JSON responses; handle confidence scores
- **Integration point**: `modules/hermes_cli.py` and `item_identifier.py`

**Task 4: Unit Tests** (Priority 2) — **DONE (MVP scope)**
- `tests/` + pytest; Hermes mocked via `run_hermes_chat` / module patches
- **Note**: 80%+ coverage not enforced in CI yet — run `python -m pytest tests/ -q` locally

**Task 5: Progress Bars** (Priority 3) — **DONE**
- `tqdm` on `process_batch`; batch summary + failure count in logs/stdout

## CODE STRUCTURE

```
modules/
  agent_logging.py      - Central logging setup
  retry_utils.py        - Backoff helper
  hermes_cli.py         - Hermes CLI entry (swap/extend for vision_analyze)
  item_identifier.py    - Vision via Hermes chat + fallback (NEEDS real vision API)
  price_researcher.py   - Hermes chat + mock comps (NEEDS real sold data / API)
  listing_generator.py  - Multi-platform listings (WORKING)
  inventory_manager.py  - CSV + JSON per SKU; canonical columns (WORKING)
```

## STANDARDS

- Python 3.8+, PEP 8 style
- Type hints, Google-style docstrings
- 100 char line length
- pytest for testing

## COLLABORATION

**You Do**: Write/debug/test code in IDE
**Hermes Does**: Research APIs, test real data, setup services
**Communication**: Via Myles (Telegram)

## FILES TO READ

1. README.md - Project overview
2. GAMEPLAN.md - Full collaboration strategy  
3. TASKS.md - Live task tracker (updated with Cursor/Hermes status)
4. demo.py - See working example
5. modules/*.py - Review existing code

## START HERE

```bash
cd ~/storage-flipper-agent   # or your clone path
pip install -r requirements.txt
python -m pytest tests/ -q
python demo.py
```

**Done this sprint**: logging, error handling, retries, tqdm, pytest suite. **Next for Cursor** after Hermes specs: wire `vision_analyze`, replace mock eBay prices with real data/API.

Full details in GAMEPLAN.md and existing code comments.

**Last updated**: 2026-04-09 (Cursor)
