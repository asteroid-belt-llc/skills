# Safe Refactoring Rules

> **MANDATORY**: Read this reference during Phase 4 (PLAN) and Phase 5 (EXECUTE) to determine which refactorings can be auto-applied.

This document defines which refactorings are safe to apply automatically vs. which require human approval.

---

## Safety Classification

### SAFE (Auto-Apply)

These refactorings have minimal risk of breaking behavior and can be applied automatically:

| Refactoring | Why Safe | Prerequisites |
|-------------|----------|---------------|
| **Remove Dead Code** | Unused code has no effect | Verify truly unused (no reflection, no dynamic calls) |
| **Rename Variable** (local) | Only affects local scope | No shadowing, no reflection |
| **Rename Function** (private) | Limited call sites | Verify all callers updated |
| **Replace Magic Literal** | Semantically identical | Use exact same value |
| **Slide Statements** | Reordering, no logic change | Verify no dependencies between statements |
| **Remove Debug Code** | Should never be in production | Verify not intentional logging |
| **Inline Variable** (simple) | Eliminates indirection only | Variable used once, expression simple |
| **Format/Style Fixes** | Whitespace only | Use consistent formatter |

**Auto-apply criteria**:
- Change is localized to one file
- No behavioral change possible
- Easy to verify correctness visually
- Easy to revert if wrong

---

### REQUIRES APPROVAL

These refactorings are behavior-preserving but have higher risk or wider impact:

| Refactoring | Why Needs Approval | Risk |
|-------------|-------------------|------|
| **Extract Function** | Creates new abstraction boundary | Scope issues, parameter decisions |
| **Rename Function** (public) | Affects callers in other files/packages | Breaking external consumers |
| **Move Function** | Changes module boundaries | Import changes, dependency direction |
| **Extract Class** | Major structural change | Responsibility division decisions |
| **Introduce Parameter Object** | API signature change | Affects all callers |
| **Replace Primitive with Object** | Type change throughout codebase | Requires updating many files |
| **Extract Variable** (complex) | Naming decisions, scope decisions | Could introduce bugs |
| **Decompose Conditional** | Logic restructuring | Must verify all branches preserved |
| **Replace Loop with Pipeline** | Algorithm change | Edge cases in transformation |

**Approval criteria**:
- Present before/after diff
- Explain the change in plain language
- List all affected files
- Ask: "Apply this refactoring? (y/n)"

---

### NEVER AUTO-APPLY

These refactorings require explicit human decision-making:

| Refactoring | Why Never Auto | Requirement |
|-------------|---------------|-------------|
| **Delete Files** | Irreversible | Always ask |
| **Change Public API** | Breaking change | Always ask |
| **Modify Test Assertions** | Could hide bugs | Always ask |
| **Combine Functions into Class** | Design decision | Always ask |
| **Replace Conditional with Polymorphism** | Architecture change | Always ask |
| **Modify Error Handling** | Behavioral change | Always ask |
| **Change Configuration** | Environment impact | Always ask |
| **Modify Database Queries** | Data impact | Always ask |

---

## Safety Checklist Per Refactoring

Before applying ANY refactoring, verify:

### Pre-Flight Checks

- [ ] **Tests exist** for affected code
- [ ] **Tests pass** before refactoring
- [ ] **Understand** what the code does
- [ ] **Identified** all affected locations

### Post-Flight Checks

- [ ] **Tests pass** after refactoring
- [ ] **Behavior unchanged** (manual spot check)
- [ ] **No new warnings** from linter/type checker
- [ ] **Diff is minimal** (no accidental changes)

---

## Scope Limits

### Single-File Refactorings

Safe to apply in current session:
- All SAFE refactorings
- Extract Function (within same file)
- Rename (within same file)
- Decompose Conditional (within same function)

### Multi-File Refactorings

Require approval and should be done one file at a time:
- Move Function (to different file)
- Rename public function
- Extract Class (to new file)
- Replace Primitive with Object

### Cross-Module Refactorings

Require full plan and dedicated phase:
- API changes
- Shared type changes
- Configuration changes

---

## Language-Specific Safety Notes

### TypeScript/JavaScript

| Safe | Not Safe |
|------|----------|
| Rename local variable | Rename exported function |
| Remove unused import | Remove "unused" import (could be side effect) |
| Add type annotation | Change existing type |
| Extract private function | Extract to new module |

### Python

| Safe | Not Safe |
|------|----------|
| Rename local variable | Rename function (could be called dynamically) |
| Remove unused variable | Remove "unused" variable (could be used in locals()) |
| Add type hint | Change parameter types |

### Java/Kotlin

| Safe | Not Safe |
|------|----------|
| Rename local variable | Rename public method |
| Extract private method | Extract to new class |
| Remove unused import | Remove "unused" code (could be reflection) |

### Go

| Safe | Not Safe |
|------|----------|
| Rename unexported function | Rename exported function |
| Remove unused variable | Remove "unused" code (could be blank import) |
| Extract function (same package) | Move to different package |

---

## Decision Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    REFACTORING SAFETY DECISION                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  1. Is it in SAFE list?                                             │
│     YES → Check prerequisites → Apply automatically                 │
│     NO  ↓                                                            │
│                                                                      │
│  2. Is it in REQUIRES APPROVAL list?                                │
│     YES → Show diff → Ask user → Apply if approved                  │
│     NO  ↓                                                            │
│                                                                      │
│  3. Is it in NEVER AUTO-APPLY list?                                 │
│     YES → Create subtask for human review                           │
│     NO  → Default to REQUIRES APPROVAL                              │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Rollback Protocol

If any refactoring causes test failures:

1. **STOP** immediately
2. **Revert** the change (git checkout the file)
3. **Report** what went wrong
4. **Ask** user how to proceed

Never attempt to "fix forward" after a failed refactoring.
