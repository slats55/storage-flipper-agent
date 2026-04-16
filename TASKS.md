# Task Tracker - Storage Flipper Agent

## Current Sprint: Phase 2 Week 1

### Hermes Tasks (in progress — still needed for production)
- [ ] Research eBay API documentation
- [ ] Test eBay sold listings data extraction
- [ ] Research Facebook Marketplace pricing sources
- [ ] Test vision_analyze (or agreed vision API) with sample photos
- [ ] Document API requirements: auth, rate limits, JSON shapes, confidence fields

### Cursor Tasks (blocked on Hermes specs)
- [ ] Integrate **vision_analyze** (or documented vision endpoint) in `item_identifier.py` / `hermes_cli.py`
- [ ] Parse structured vision JSON + confidence scores
- [ ] Replace mock comparable prices in `price_researcher.py` per Hermes/eBay spec
- [ ] Optional: measure test coverage in CI (e.g. pytest-cov) toward 80%+

### Cursor Tasks (completed — Phase 2 Week 1 plumbing)
- [x] Logging (`agent.log`, `flipper.*` loggers)
- [x] Error handling: retries, graceful Hermes failures, batch does not abort on one item
- [x] `hermes_cli.py` single entry for Hermes subprocess calls
- [x] Inventory CSV: canonical columns, UTF-8, safe `mark_sold`
- [x] Default inventory path: `<repo>/data/inventory`
- [x] Unit tests (`tests/`, pytest, mocked Hermes)
- [x] tqdm on batch processing
- [x] `requirements.txt` valid for pip (Python version documented in comment, not as a package)
- [x] `.gitignore` for `.env`, venvs, caches, `logs/`

### Blocked / waiting
- eBay API credentials (developer account) — Hermes / client
- **vision_analyze** (or equivalent) contract from Hermes — payload, response JSON, errors
- Sample photos from client (for Hermes vision testing)

### Completed (earlier)
- [x] MVP architecture
- [x] Demo script
- [x] Project structure
- [x] Initial modules
- [x] Gameplan / handoff documents

---

## Next actions

**Hermes (now)**  
1. Run end-to-end smoke: `hermes` on PATH, batch folder of real images, check `logs/agent.log` + `data/inventory/`.  
2. Publish a short spec: **vision** JSON + **eBay/sold listings** data shape (or API doc links).  
3. Continue GAMEPLAN Week 1 research tasks above.

**Cursor (after spec)**  
1. Implement vision + pricing per Hermes doc.  
2. Add tests for new parsers/API wrappers.

**Myles**  
1. Confirm `git remote` + push when ready.  
2. Client questions (GAMEPLAN “Questions to Answer”) as needed.

**Last updated**: 2026-04-09 (Cursor)
