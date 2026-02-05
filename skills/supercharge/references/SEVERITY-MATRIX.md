# Severity Matrix

> **MANDATORY**: Read this reference during Phase 3 (PRIORITIZE) to rank issues.

This matrix defines how to prioritize code quality issues for fixing during a supercharge session.

---

## Severity Levels

### CRITICAL - Fix Immediately

Issues that actively harm the codebase or could ship to production.

| Issue | Why Critical | Detection |
|-------|-------------|-----------|
| **Dead Code** | Confuses readers, maintenance burden | Unused vars, unreachable branches |
| **Debug Artifacts** | Could leak to production | console.log, print(), TODO in hot paths |
| **Hardcoded Credentials** | Security risk | Passwords, API keys in code |
| **Broken Imports** | Build failures | Missing dependencies, circular imports |

**Action**: Fix these before any other work. Block completion until resolved.

---

### HIGH - Fix This Session

Issues that significantly impact maintainability.

| Issue | Why High | Detection |
|-------|---------|-----------|
| **God Classes** | Unmaintainable, hard to test | >500 lines, >10 public methods |
| **Deep Nesting** | Cognitive load, bug-prone | >3 levels of indentation |
| **DRY Violations** | Change propagation risk | Duplicated code blocks |
| **Verbose Functions** | Hard to understand | >30 lines, multiple abstractions |
| **Long Parameter Lists** | Hard to call correctly | 5+ parameters |

**Action**: Address as many as time permits. Track remaining as tech debt.

---

### MEDIUM - Fix If Time Permits

Issues that reduce readability but don't block work.

| Issue | Why Medium | Detection |
|-------|-----------|-----------|
| **Poor Naming** | Slows comprehension | Generic names, misleading names |
| **Magic Literals** | Unclear meaning | Numbers without constants |
| **Feature Envy** | Wrong location for logic | Methods using other class's data |
| **Primitive Obsession** | Repeated validation | Same primitive used for concept |
| **Boolean Parameters** | Unclear call sites | `doThing(data, true, false)` |
| **Missing Types** | Reduced safety | `any`, untyped functions |

**Action**: Fix opportunistically when touching related code.

---

### LOW - Opportunistic

Issues that are minor or easily automated.

| Issue | Why Low | Detection |
|-------|--------|-----------|
| **Inconsistent Style** | Formatter can fix | Mixed conventions |
| **Excessive Comments** | Low impact | Obvious comments |
| **Minor Duplication** | Small scope | 2-3 line duplicates |
| **Overly Defensive** | Noise but functional | Unnecessary null checks |
| **Verbose Comments** | Low impact | Long block comments |

**Action**: Fix when convenient. Consider automated formatters.

---

## Prioritization Formula

Calculate priority score for each issue:

```
Priority = Severity × Impact × Frequency - Effort
```

| Factor | Score Range | Examples |
|--------|-------------|----------|
| **Severity** | 1-4 | LOW=1, MEDIUM=2, HIGH=3, CRITICAL=4 |
| **Impact** | 1-3 | 1=one file, 2=one module, 3=whole codebase |
| **Frequency** | 1-3 | 1=once, 2=few times, 3=everywhere |
| **Effort** | 1-5 | 1=trivial, 3=moderate, 5=major work |

**Example Calculations**:

| Issue | Severity | Impact | Frequency | Effort | Score | Priority |
|-------|----------|--------|-----------|--------|-------|----------|
| console.log in main.ts | 4 | 1 | 1 | 1 | 4×1×1-1=3 | HIGH |
| God class (800 lines) | 3 | 3 | 1 | 4 | 3×3×1-4=5 | HIGH |
| Magic number (one place) | 2 | 1 | 1 | 1 | 2×1×1-1=1 | LOW |
| Duplicated validation (5x) | 3 | 2 | 3 | 3 | 3×2×3-3=15 | CRITICAL |

---

## Quick Wins

Prioritize issues that are HIGH impact AND LOW effort:

| Quick Win | Severity | Effort | Action |
|-----------|----------|--------|--------|
| Remove dead imports | CRITICAL | 1 | Delete lines |
| Remove console.log | CRITICAL | 1 | Delete lines |
| Replace magic literal | MEDIUM | 1 | Extract constant |
| Apply guard clauses | HIGH | 2 | Restructure conditional |
| Rename unclear variable | MEDIUM | 1 | Find/replace |

**Quick win rule**: Fix issues with Effort ≤ 2 first, regardless of severity.

---

## Session Time Allocation

For a typical 1-hour supercharge session:

| Time | Focus | Expected Outcome |
|------|-------|-----------------|
| 0-10 min | CRITICAL issues | All debug/dead code removed |
| 10-30 min | HIGH issues | 2-3 major refactorings |
| 30-50 min | MEDIUM issues | 5-10 naming/literal fixes |
| 50-60 min | Cleanup + Report | All changes committed, report generated |

---

## Hotspot Analysis

Focus refactoring on files with:

1. **Highest issue count** - Most smells in one place
2. **Recent changes** - Actively worked code
3. **High complexity** - Cyclomatic complexity > 10
4. **Low coverage** - Untested code (riskier but needed)

Calculate hotspot score:

```
Hotspot = (Issue Count × 2) + (Recent Commits × 1) + (Complexity / 5)
```

Focus on top 3-5 hotspots per session.

---

## Issue Grouping

Group related issues for efficient fixing:

| Group | Issues | Single Refactoring |
|-------|--------|-------------------|
| One function | Long + Magic literals + Deep nesting | Extract + Decompose |
| One class | God class + Feature envy | Extract Class |
| One concept | Primitive obsession everywhere | Replace Primitive (once) |
| One pattern | Same duplication repeated | Extract Function (once) |

Grouped fixes are more efficient than fixing issues in isolation.

---

## Skip List

Do NOT fix these during supercharge:

| Skip | Reason |
|------|--------|
| Code in generated files | Will be overwritten |
| Code in vendor/node_modules | Not your code |
| Code pending deletion | Wasted effort |
| Test fixtures/mocks | Intentionally simplified |
| Legacy code with no tests | Too risky without coverage |

Mark skipped items in the report with reason.
