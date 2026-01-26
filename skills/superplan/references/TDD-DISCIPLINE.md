# TDD Discipline Guide

> **MANDATORY**: This guide defines the non-negotiable rules of Test-Driven Development.

## The Iron Law

**NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.**

No exceptions. No rationalizations. No shortcuts.

---

## The Red-Green-Refactor Cycle

```
┌─────────────────────────────────────────────────────────────────────┐
│                    RED-GREEN-REFACTOR CYCLE                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. RED            2. VERIFY RED      3. GREEN                      │
│  ┌───────┐         ┌───────┐          ┌───────┐                    │
│  │ Write │  ───▶   │ Watch │   ───▶   │ Write │                    │
│  │ Test  │         │ Fail  │          │ Code  │                    │
│  └───────┘         └───────┘          └───────┘                    │
│                        │                  │                         │
│                   MANDATORY           MINIMAL                       │
│                                                                     │
│  4. VERIFY GREEN   5. REFACTOR                                      │
│  ┌───────┐         ┌───────┐                                       │
│  │ Watch │  ───▶   │ Clean │  ───▶  REPEAT                         │
│  │ Pass  │         │  Up   │                                       │
│  └───────┘         └───────┘                                       │
│      │                 │                                            │
│  MANDATORY         TESTS STAY GREEN                                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Step 1: RED - Write Failing Test

Create one minimal test demonstrating desired behavior:

- Clear, descriptive name
- Single focused behavior
- Real code (minimal mocking)

### Step 2: VERIFY RED - Watch It Fail (MANDATORY)

**This step is NOT optional.** Run tests and confirm:

- Test **fails** (not errors due to syntax)
- Failure message is **expected**
- Fails because **feature is missing**, not typos or imports

**If the test passes immediately:** You are testing existing behavior. Fix your test or you are not doing TDD.

### Step 3: GREEN - Write Minimal Code

Write the **simplest** implementation passing the test:

- Just enough to satisfy assertions
- No over-engineering
- No features beyond current test
- Do NOT refactor yet

### Step 4: VERIFY GREEN - Watch It Pass (MANDATORY)

**This step is NOT optional.** Run tests and confirm:

- Test **passes**
- Other tests **remain passing**
- No errors or warnings in output

### Step 5: REFACTOR - Clean Up

After achieving green, improve code:

- Remove duplication
- Improve naming
- Extract helpers

**Tests must stay green throughout refactoring.** Do NOT add new behavior.

---

## Characteristics of Good Tests

| Quality | Standard | Anti-Pattern |
|---------|----------|--------------|
| **Minimal** | One behavior per test | "test validates email and domain and whitespace" |
| **Clear** | Name describes actual behavior | "test1", "testFunction" |
| **Intent** | Demonstrates desired API usage | Obscures requirements |
| **Focused** | Tests behavior, not implementation | Asserts on internal state |

---

## Why Order Matters

### The Testing-After Trap

Tests written after code pass immediately. This proves nothing.

- You cannot verify the test actually catches bugs
- You cannot discover edge cases you overlooked
- You cannot confirm the test validates real behavior

### Testing-First Advantage

Testing first forces you to:

1. See the test fail - proves it validates something real
2. Observe the test catching the bug *before* implementation
3. Design the API from the caller's perspective
4. Think about edge cases before writing code

---

## Common Rationalizations - ALL REJECTED

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Tests take 30 seconds. Write them. |
| "I'll test after" | Tests-after pass immediately. No proof of value. |
| "Tests after achieve same goals" | Tests-after answer "what does this do?" Tests-first answer "what SHOULD this do?" |
| "Already manually tested" | Ad-hoc testing is not systematic. Cannot re-run automatically. |
| "Deleting X hours is wasteful" | Sunk cost fallacy. Unverified code is technical debt. |
| "Keep as reference" | You will adapt it. That is testing-after. Delete means delete. |
| "Need to explore first" | Exploration is fine. Throw it away. Start TDD fresh. |
| "Hard to test = design unclear" | Listen to the test. Difficult testing signals hard-to-use APIs. |
| "This is just a prototype" | Prototypes become production. TDD from the start. |
| "The code is obviously correct" | Obvious code breaks. Evidence, not confidence. |

---

## Red Flags - STOP and Start Over

Abandon current work and restart with TDD when you encounter:

- Code written before test
- Testing after implementation
- Tests passing immediately (without implementation)
- Unable to explain why test failed
- Tests added "later" to existing code
- Rationalizing "just this once"
- Claims of "manually tested everything"
- Arguing tests-after achieve identical goals
- Suggesting it is about "spirit not ritual"
- Keeping code "as reference" or adapting existing work
- Citing time spent on existing code (sunk cost)
- Framing TDD as dogmatic rather than pragmatic
- Any variation of "this is different because..."

**All of these mean: Delete code. Start with TDD.**

---

## Bug Fix Workflow

Bug fixes follow TDD too:

### 1. RED: Write Failing Test

Write a test that reproduces the bug:

```typescript
it('should reject empty email addresses', () => {
  const result = validateEmail('');
  expect(result.valid).toBe(false);
  expect(result.error).toBe('Email required');
});
```

### 2. VERIFY RED: Confirm It Fails

Run the test. Confirm it fails with the bug present:

```
FAIL: Expected valid to be false, received true
```

This proves the test catches the bug.

### 3. GREEN: Fix the Bug

Write minimal code to make the test pass:

```typescript
function validateEmail(email: string) {
  if (!email) return { valid: false, error: 'Email required' };
  // ... rest of validation
}
```

### 4. VERIFY GREEN: Confirm Fix

Run all tests. Bug fix test passes. No regressions.

### 5. REFACTOR

Clean up if needed. Tests stay green.

---

## When Stuck

| Problem | Solution |
|---------|----------|
| Do not know how to test | Write the wished-for API first. Draft assertions. Ask for help. |
| Test too complicated | Design is too complex. Simplify the interface. |
| Must mock everything | Code is too coupled. Use dependency injection. |
| Massive test setup | Extract helpers. If still complex, reconsider design. |
| Test seems redundant | It is not. Tests document behavior. Write it anyway. |

---

## Verification Checklist

Before marking any work complete:

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason (feature missing, not typos)
- [ ] Wrote minimal code for each test
- [ ] All tests pass
- [ ] Output clean (no errors, warnings)
- [ ] Tests use real code (mocks only when unavoidable)
- [ ] Edge cases and errors covered

**Cannot check all boxes? You skipped TDD. Start over.**

---

## Summary

1. **Test first** - Always
2. **Verify failure** - Mandatory
3. **Minimal code** - No more than needed
4. **Verify pass** - Mandatory
5. **Refactor** - Tests stay green
6. **No exceptions** - None

**Production code exists = test exists and failed first. Otherwise = not TDD.**
