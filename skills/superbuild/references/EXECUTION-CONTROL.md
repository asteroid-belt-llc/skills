# Execution Control Reference

> Detailed patterns for functional testing, stop behavior, and build-all mode.

## Functional Testing Instructions

After commit message, explain how to functionally test the phase:

```
FUNCTIONAL TESTING - Phase [X]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

To manually verify this phase works:

1. [Step 1 - e.g., Start the development server]
   $ npm run dev

2. [Step 2 - e.g., Navigate to the feature]
   Open http://localhost:3000/[feature]

3. [Step 3 - e.g., Test the happy path]
   - Fill in [field1] with "test value"
   - Click [button]
   - Verify [expected result]

4. [Step 4 - e.g., Test error handling]
   - Submit empty form
   - Verify error message appears

Expected Results:
- [Result 1]
- [Result 2]
```

### Integration Test Script Offer

**ONLY if applicable. ALWAYS ask. NEVER auto-create.**

```
Would you like me to write an integration test script for this phase?

This would:
- Automate the manual verification steps above
- Be saved to scripts/test-phase-[X].sh (or .py)
- Be runnable for regression testing

Options:
1. Yes, write the integration test script
2. No, manual testing is sufficient

[WAIT FOR USER RESPONSE]
```

**If user says yes:** Write script to `scripts/` directory.
**If user says no:** Continue to stop execution.

---

## Stop Execution Output

**FULL STOP after each phase (unless --build-all override).**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE [X] EXECUTION COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Summary:
- Definition of Done: ✅ All checks passed
- Plan Document: ✅ Updated (tasks and status checked off)
- Conventional Commit: ✅ Generated (user to commit)
- Functional Testing: ✅ Instructions provided

Progress:
| Phase | Status |
|-------|--------|
| 0 | ✅ Complete |
| 1 | ✅ Complete |
| 2A | ⬜ Next |
| 2B | ⬜ Pending |
| 2C | ⬜ Pending |
| 3 | ⬜ Pending |

💡 Context Management Suggestion
Consider compacting the conversation before the next phase
to preserve context for the remaining work.

[EXECUTION PAUSED]

To continue: "Continue to Phase 2A"
To compact first: Use /compact then return with "Resume superbuild"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Context Compaction Behavior

**CRITICAL: If this session resumes after context compaction:**

1. Complete ONLY the phase that was in-progress
2. Output the commit message and functional test instructions
3. STOP - Do not auto-continue to next phase
4. Wait for explicit user instruction: "Continue to Phase X"

The todo list showing pending phases is NOT authorization to continue.
Only explicit user instruction authorizes next phase execution.

```
POST-COMPACTION RESUME
━━━━━━━━━━━━━━━━━━━━━━

Detected: Session resumed after compaction
Phase in progress: [X]

Completing Phase [X]...
[finish work]

PHASE [X] COMPLETE
[commit message + functional test instructions]

[EXECUTION PAUSED]

Remaining phases: [list]
To continue: "Continue to Phase [Y]"

⚠️  I will NOT auto-continue. Awaiting your instruction.
```

---

## Build-All Override

**ONLY if user explicitly specifies.**

```
⚠️  BUILD-ALL MODE DETECTED
━━━━━━━━━━━━━━━━━━━━━━━━━━

You've requested to build the entire plan without stopping.

This is NOT RECOMMENDED because:
- Context may be exhausted mid-build
- Errors compound across phases
- You lose ability to commit incrementally

Are you sure you want to continue?
1. Yes, build all phases (override safety)
2. No, execute phase by phase (recommended)
```

---

## Parallel Phase Commits

When parallel phases complete, output ALL commit messages:

```
PARALLEL PHASES COMPLETE (2A, 2B, 2C)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PHASE 2A - Commit Message:
━━━━━━━━━━━━━━━━━━━━━━━━━━
feat(api): implement user authentication endpoints
...

PHASE 2B - Commit Message:
━━━━━━━━━━━━━━━━━━━━━━━━━━
feat(ui): create login form component
...

PHASE 2C - Commit Message:
━━━━━━━━━━━━━━━━━━━━━━━━━━
test(auth): add authentication test coverage
...

⚠️  Create separate commits for each phase, or squash as appropriate.
    User handles all git operations.
```
