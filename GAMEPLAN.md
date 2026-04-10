# Storage Flipper Agent - Development Gameplan
## Hermes + Cursor (Claude) Collaboration Strategy

**Project Goal**: Build production-ready storage unit flipping automation agent
**Timeline**: Phase 2 (Integration) → Phase 3 (Automation) → Phase 4 (Polish)

---

## Division of Labor

### CURSOR (Claude) - Code Development & Refinement
**Best for**: Deep coding, refactoring, debugging, IDE integration

**Primary Responsibilities**:
1. **Core Code Development**
   - Write and refine Python modules
   - Implement complex algorithms
   - Debug code with error tracebacks
   - Refactor for performance/readability
   - Add type hints and docstrings
   - Write unit tests

2. **Feature Implementation**
   - Build vision integration (Hermes API calls)
   - Implement web scraping logic
   - Create API wrappers (eBay, Facebook, etc.)
   - Build data processing pipelines
   - Develop UI/CLI improvements

3. **Code Quality**
   - Fix bugs and errors
   - Optimize performance
   - Add error handling
   - Code reviews and improvements
   - Git commits and version control

**Workflow in Cursor**:
- Open ~/storage-flipper-agent/ project
- Edit modules in real-time with full context
- Run tests immediately
- Debug with full stack traces
- Commit changes with git

---

### HERMES (You) - Research, Integration & Orchestration
**Best for**: Research, API testing, automation, external integrations

**Primary Responsibilities**:
1. **Research & Discovery**
   - Research platform APIs (eBay, Facebook Marketplace)
   - Find pricing data sources
   - Test web scraping approaches
   - Investigate competitor tools
   - Research best practices

2. **API Testing & Integration**
   - Test eBay API endpoints
   - Experiment with authentication flows
   - Verify API rate limits
   - Test real data examples
   - Document API quirks

3. **External Service Setup**
   - Configure Google Sheets API
   - Set up webhook endpoints
   - Create cron jobs for automation
   - Test Telegram notifications
   - Configure environment variables

4. **End-to-End Testing**
   - Run full workflow tests
   - Process real photos
   - Verify output quality
   - Monitor performance
   - Report issues to Cursor/Claude

5. **Documentation & Planning**
   - Project planning and prioritization
   - Update README and docs
   - Track progress and blockers
   - Create task lists
   - Send daily updates via Telegram

6. **Deployment & Automation**
   - Set up production environment
   - Configure background services
   - Schedule automated tasks
   - Monitor system health

---

## Phase 2: Integration - Task Breakdown

### Week 1: Vision Integration & Price Research

**Cursor Tasks**:
- [ ] Refactor `item_identifier.py` to use Hermes vision_analyze API
- [ ] Add image preprocessing (resize, enhance)
- [ ] Implement retry logic for vision API
- [ ] Create structured output parsing
- [ ] Write tests for item identification
- [ ] Add error handling for bad photos

**Hermes Tasks**:
- [ ] Research eBay price scraping methods (API vs scraping)
- [ ] Test eBay Sold Listings data extraction
- [ ] Find Facebook Marketplace pricing sources
- [ ] Document API requirements and limitations
- [ ] Test vision_analyze with real storage unit photos
- [ ] Create sample dataset of 20 test photos

**Handoff Point**: Cursor implements, Hermes tests with real data

---

### Week 2: Platform APIs & Listing Automation

**Cursor Tasks**:
- [ ] Build eBay API wrapper (`ebay_api.py`)
- [ ] Implement listing creation logic
- [ ] Add photo upload functionality
- [ ] Create platform authentication handlers
- [ ] Build listing template system
- [ ] Add category mapping logic
- [ ] Write tests for API wrappers

**Hermes Tasks**:
- [ ] Get eBay Developer credentials
- [ ] Test eBay API sandbox environment
- [ ] Research Facebook Marketplace automation (likely manual)
- [ ] Find Mercari/OfferUp API alternatives
- [ ] Test authentication flows
- [ ] Document platform-specific requirements
- [ ] Create test listings on sandbox

**Handoff Point**: Hermes provides API credentials and docs, Cursor builds integration

---

### Week 3: Inventory System & Analytics

**Cursor Tasks**:
- [ ] Build Google Sheets integration (`sheets_manager.py`)
- [ ] Add inventory sync logic
- [ ] Create analytics dashboard generator
- [ ] Implement profit/loss calculations
- [ ] Add reporting features
- [ ] Build data visualization helpers
- [ ] Write tests for inventory operations

**Hermes Tasks**:
- [ ] Set up Google Cloud project
- [ ] Configure Sheets API credentials
- [ ] Create inventory spreadsheet template
- [ ] Test sheet read/write operations
- [ ] Monitor data sync performance
- [ ] Set up automated backups
- [ ] Create sample reports

**Handoff Point**: Cursor implements, Hermes deploys and monitors

---

## Communication Protocol

### Cursor → Hermes Handoffs
When Claude (Cursor) completes code:
1. Commit changes to git
2. Message Hermes on Telegram: "Ready for testing: [feature]"
3. Provide specific test cases to run
4. List any dependencies needed

### Hermes → Cursor Handoffs
When Hermes completes research/testing:
1. Create detailed spec document
2. Provide code snippets/examples
3. Document API endpoints and auth
4. List bugs found with reproduction steps
5. Message: "Ready for implementation: [feature]"

### Daily Sync (via Telegram)
- Morning: Hermes sends overnight progress + today's plan
- Evening: Status update and blockers
- Ad-hoc: Questions, bugs, urgent issues

---

## Workflow Example: "Add eBay Price Research"

### Step 1: Research (Hermes)
```
1. Research eBay API documentation
2. Test endpoints in terminal
3. Extract sample pricing data
4. Document data structure
5. Create spec: RESEARCH_ebay_pricing.md
6. Message Cursor: "eBay research complete, ready for implementation"
```

### Step 2: Implementation (Cursor)
```
1. Open project in Cursor IDE
2. Read Hermes spec document
3. Implement price_researcher.py with eBay API
4. Add error handling and tests
5. Commit changes
6. Message Hermes: "eBay pricing implemented, ready for testing"
```

### Step 3: Testing (Hermes)
```
1. Pull latest code
2. Run with real data: python flipper_agent.py process-item test.jpg
3. Verify eBay prices are accurate
4. Test edge cases (no results, API errors)
5. Report bugs or success
6. If bugs: Document reproduction steps for Cursor
```

### Step 4: Refinement (Cursor)
```
1. Fix reported bugs
2. Optimize performance
3. Add requested features
4. Commit and notify Hermes
```

---

## Tools & Setup

### Cursor Workspace
```bash
# Open project in Cursor
cd ~/storage-flipper-agent
cursor .

# Cursor should have access to:
- Full project files
- Git integration
- Python interpreter
- Terminal for testing
```

### Hermes Environment
```bash
# Hermes has:
- Telegram bot for updates
- Full system access
- Web research tools
- API testing capabilities
- Background process management
- Cron scheduling
```

---

## Current Phase 2 Priority Tasks

### IMMEDIATE (This Week):

**Hermes**:
1. Research eBay API - find best method for sold listings data
2. Test vision_analyze with 5 sample photos
3. Document API requirements for eBay, Google Sheets
4. Create test photo dataset

**Cursor**:
1. Refactor item_identifier.py to use real vision API
2. Improve error handling across all modules
3. Add logging system
4. Create unit tests for existing modules

### THIS MONTH:

**Hermes**:
- Set up eBay developer account
- Configure Google Sheets API
- Test all integrations end-to-end
- Set up monitoring and alerts

**Cursor**:
- Implement all API wrappers
- Build complete testing suite
- Optimize performance
- Add comprehensive error handling

---

## Success Metrics

### Phase 2 Complete When:
- [ ] Real photos processed with 90%+ identification accuracy
- [ ] Live eBay pricing data integrated
- [ ] At least 2 platforms have automated posting
- [ ] Inventory syncs to Google Sheets
- [ ] Full batch processing works (50+ items)
- [ ] Processing time: 10-15 hours per unit (vs 40-80 baseline)

---

## Notes for Client Demo

After Phase 2, we'll demo:
1. Upload 20 photos from a real storage unit
2. Agent processes all items in 30 minutes
3. Generates listings for eBay + Facebook
4. Shows pricing analysis and profit projections
5. Displays inventory in Google Sheets

**Demo Goal**: Prove 60%+ time savings and convince client to use in production

---

## Questions to Answer

Before starting Phase 2:
1. Does client have eBay seller account? (need for API)
2. What's the acquisition cost per unit? (for profit calculations)
3. Where are photos stored? (local, cloud, mobile?)
4. Preferred inventory system? (Sheets vs local CSV)
5. Manual approval before posting, or fully automated?

---

**Last Updated**: 2026-04-09
**Status**: MVP Complete, Phase 2 Planning
**Next Action**: Hermes starts eBay API research
