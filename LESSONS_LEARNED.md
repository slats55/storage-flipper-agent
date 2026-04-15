# Lessons Learned - Storage Flipper Agent Development

**Date**: April 9, 2026
**Session**: Initial MVP and collaboration setup

## Key Insights

### 1. Hermes+Cursor Collaboration Works

**What worked**:
- Clear division of labor (Hermes=research, Cursor=coding)
- Comprehensive handoff documents (CURSOR_HANDOFF.md, GAMEPLAN.md)
- Git as coordination mechanism
- Telegram for async updates

**Critical success factors**:
- Don't have both tools do the same work
- Document everything (specs, patterns, decisions)
- Test immediately after implementation
- Daily sync to prevent drift

### 2. Production AI Systems Need Defensive Patterns

**Must-haves**:
- JSON schema validation (AI outputs are unpredictable)
- Tiered fallbacks (primary → fallback → heuristic → manual)
- Aggressive caching (60-80% cost savings)
- Rate limiting (prevent API exhaustion)
- Metrics tracking (know when things break)
- Manual review queue (some edge cases need humans)

**Cost management**:
- 500 items × $0.10/API call = $50 without caching
- With 70% cache hit rate = $15 actual cost
- Always track and alert on cost spikes

### 3. Architecture Patterns Matter

**Implement from day one**:
- Repository pattern (data access abstraction)
- Service layer (business logic isolation)
- Strategy pattern (swappable algorithms like pricing)
- Factory pattern (complex object creation)

**Why**: Makes testing easy, swapping implementations trivial, scaling straightforward.

### 4. File System Quirks

**Issue encountered**: Working directory corruption ("No such file or directory: 'hermes'")

**Solution**: Always use absolute paths or explicit workdir parameter:
```python
# Good
terminal(command="...", workdir="/tmp")
Path.home() / "project"

# Bad
"hermes"  # Relative path breaks if cwd is wrong
```

### 5. Memory Management is Critical

**Hermes memory limit**: 2200 characters
**Strategy**: Compress aggressively, prioritize actionable knowledge

```
# Verbose (100 chars):
"The Repository Pattern provides data access abstraction which makes testing easier"

# Compressed (30 chars):
"Repository(data abstraction)"
```

### 6. Progressive Disclosure for Learning

**Pattern that worked**:
1. Generate comprehensive content locally (execute_code)
2. Save full details to file
3. Output concise summary to user
4. Save compressed version to memory

**Don't**: Try to output 50KB of content in one go (token limits)

### 7. Always Verify Environment First

**Checklist before starting**:
- Python version and location
- pip availability and permissions
- Git, curl, essential tools
- Can install packages?
- File system write access?

**5 minutes of verification saves hours of debugging**

### 8. API Integration Workflow

**Best practice discovered**:
1. Hermes researches API (30-60 min)
   - Read docs
   - Test with curl
   - Document responses, edge cases, rate limits
2. Hermes creates spec document with working examples
3. Cursor implements based on spec (1-2 hours)
4. Hermes tests with real credentials (15-30 min)
5. Iterate on bugs

**Key**: Real testing with actual API credentials, not mocks.

### 9. Testing AI Systems is Different

**Property-based testing** instead of exact matches:
```python
# Don't:
assert result['title'] == "Vintage Camera"  # Too brittle

# Do:
assert 'title' in result
assert len(result['title']) > 3
assert result['confidence'] >= 0 and result['confidence'] <= 1
assert result['category'] in VALID_CATEGORIES
```

**Test pyramid for AI**: 80% unit / 15% integration / 5% E2E

### 10. Documentation is Code

**Created during session**:
- README.md (project overview)
- GAMEPLAN.md (collaboration strategy - 8.6KB)
- CURSOR_HANDOFF.md (detailed brief for Cursor)
- TASKS.md (sprint tracker)
- QUICKSTART.md (usage guide)

**Why**: Enables asynchronous work, reduces context switching, serves as specification.

## What Would We Do Differently?

**Next time**:
1. Set up virtual environment immediately (avoid global package conflicts)
2. Initialize git repo from start (track all changes)
3. Create test fixtures earlier (speed up testing)
4. Set up CI/CD from day one (automated testing)
5. Define success metrics upfront (track progress objectively)

## Patterns to Reuse

✅ Hermes+Cursor collaboration model
✅ Comprehensive handoff documents
✅ Tiered fallback strategy for AI
✅ Caching layer for cost savings
✅ Validation schemas for AI outputs
✅ Repository/Service/Strategy patterns
✅ Structured JSON logging
✅ Progressive disclosure for learning

## Anti-Patterns to Avoid

❌ Both tools doing the same research
❌ Implementing features without testing with real data
❌ Trusting AI outputs without validation
❌ No caching (cost explosion)
❌ Working in isolation for days
❌ Skipping comprehensive handoff docs
❌ Not tracking metrics/costs

## Success Metrics

**Project velocity**: MVP completed in one session (4 hours)
**Code quality**: Modular architecture, testable design
**Documentation**: 5 comprehensive docs created
**Collaboration setup**: Full workflow defined and documented
**Learning captured**: 2 major study sessions with patterns saved

## Next Phase Goals

- Integrate real vision API (blocked on testing)
- Implement eBay API (blocked on Hermes research)
- Add comprehensive error handling
- Create test suite
- Set up monitoring and metrics
- Deploy to production

---

**Key Takeaway**: Success comes from clear division of labor, comprehensive documentation, defensive AI patterns, and continuous testing with real data.
