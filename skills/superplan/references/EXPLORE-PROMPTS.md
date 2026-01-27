# Codebase Exploration Prompts

> **MANDATORY**: Use these exact prompts when exploring the codebase in Phase 5.

## Launch 3 Parallel Explore Agents

### Agent 1: Pattern Discovery

```
"Find 2-3 existing implementations similar to [FEATURE].

Search for:
- Files with similar names (e.g., if building 'payments', search for 'billing', 'orders', 'transactions')
- Routes with similar endpoints
- Components with similar functionality
- Services following similar patterns

Return in this format:
| File | Pattern Used | Testing Approach | Reusable? |
|------|--------------|------------------|-----------|
| path/to/file.ts | Pattern name | Unit/Integration/E2E | Yes/No + reason |
"
```

### Agent 2: Integration Points

```
"Identify all files that will need modification for [FEATURE].

Search for:
- Route registrations (where routes are mounted)
- Type definitions (shared types, interfaces)
- Shared utilities (validation, formatting, logging)
- Configuration files (env, constants)
- Test setup files (fixtures, mocks, helpers)
- Index/barrel files that re-export

Return in this format:
| File | Lines | Change Needed |
|------|-------|---------------|
| exact/path/file.ts | 45-50 | What specifically needs to change |
"
```

### Agent 3: Technical Debt Scan

```
"Analyze code quality in files related to [FEATURE].

Check for:
- TODO comments
- FIXME notes
- @deprecated markers
- Missing tests (files in src/ without corresponding test file)
- Complex functions (>50 lines or >10 cyclomatic complexity)
- Commented-out code blocks
- Outdated dependencies mentioned in comments

Return in this format:
| File | Issue Type | Severity | Recommended Action |
|------|------------|----------|-------------------|
| path/file.ts:45 | TODO comment | Medium | Address in Phase 0 |
"
```

---

## Output Format

After all agents complete, compile results:

```markdown
## Codebase Analysis Results

### Similar Implementations Found
| File | Pattern | Testing Approach | Reusable? |
|------|---------|------------------|-----------|
| `src/features/auth/login.ts` | Service + Handler | Unit + Integration | Yes - copy structure |
| `src/features/users/create.ts` | Service + Handler | Unit only | Partial - add integration |

### Integration Points
| File | Lines | Change Needed |
|------|-------|---------------|
| `src/routes/index.ts` | 45-50 | Add route import and registration |
| `src/types/index.ts` | 12 | Export new types |
| `tests/setup.ts` | 78-82 | Add test fixtures |

### Technical Debt in Affected Areas
| File | Issue | Severity | Action |
|------|-------|----------|--------|
| `src/utils/validate.ts` | No tests | Medium | Add to Phase 0 |
| `src/services/base.ts` | TODO: refactor | Low | Note for future |

### Patterns to Follow
1. **Service + Handler pattern** - seen in `src/features/auth/`, applies because it separates business logic from HTTP handling
2. **Zod validation** - seen in `src/middleware/validate.ts`, applies for request validation
3. **Factory fixtures** - seen in `tests/factories/`, applies for test data generation
```

---

## Feature-Specific Search Queries

### For API Endpoints
```
Search for: existing route handlers, middleware chains, response formatting, error handling patterns
```

### For UI Components
```
Search for: similar components, shared UI primitives, state management patterns, styling conventions
```

### For Database Features
```
Search for: existing models/schemas, migration patterns, query builders, transaction handling
```

### For Background Jobs
```
Search for: existing job definitions, queue setup, retry logic, monitoring patterns
```

---

## When Exploration Reveals Issues

If Agent 3 finds significant debt:

1. Document all findings in the plan
2. Flag for Phase 6 (Refactor Assessment)
3. Consider adding Phase 0 tasks for critical issues

Severity guide:
- **Critical**: Blocks feature implementation → Must fix first
- **High**: Will cause problems during implementation → Strongly recommend fixing
- **Medium**: Technical debt that will grow → Note and discuss with user
- **Low**: Nice to fix but not blocking → Document for future
