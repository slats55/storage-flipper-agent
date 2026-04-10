# CURSOR HANDOFF DOCUMENT
Storage Unit Flipper Agent - Complete Development Brief

**Your Role**: Code Developer (Python)
**Partner**: Hermes Agent (Research & Testing)
**Owner**: Myles
**Status**: MVP Complete, Phase 2 Starting

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

**Task 1: Add Logging** (Priority 1)
- Add logging module to all .py files
- Log to logs/agent.log
- Include timestamps, levels, context

**Task 2: Error Handling** (Priority 1)  
- Add retry logic with exponential backoff
- Handle API failures gracefully
- Don't crash batch on single item error

**Task 3: Vision Integration** (BLOCKED - wait for Hermes)
- Integrate Hermes vision_analyze API
- Parse JSON responses
- Handle confidence scores

**Task 4: Unit Tests** (Priority 2)
- Create tests/ directory with pytest
- Mock external APIs
- Aim for 80%+ coverage

**Task 5: Progress Bars** (Priority 3)
- Add tqdm for batch processing
- Show ETA and success/fail counts

## CODE STRUCTURE

```
modules/
  item_identifier.py    - Vision AI (NEEDS WORK)
  price_researcher.py   - eBay pricing (NEEDS WORK) 
  listing_generator.py  - Multi-platform listings (WORKING)
  inventory_manager.py  - CSV tracking (WORKING)
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
3. demo.py - See working example
4. modules/*.py - Review existing code

## START HERE

```bash
cd ~/storage-flipper-agent
pip install -r requirements.txt
python3 demo.py  # See it work
```

Then tackle Task 1 (logging) and Task 2 (error handling).

Full details in GAMEPLAN.md and existing code comments.
