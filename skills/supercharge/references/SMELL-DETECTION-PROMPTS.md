# Smell Detection Prompts

> **MANDATORY**: Use these exact prompts during Phase 2 (SCAN) when launching Explore agents.

Each prompt is designed for a Task tool with `subagent_type=Explore`. Launch multiple agents in parallel for faster scanning.

---

## Parallel Scanning Strategy

For large codebases, launch 3-5 agents in parallel, each targeting different smell categories:

| Agent | Smell Categories | Prompt Reference |
|-------|-----------------|------------------|
| Agent 1 | Dead Code, Debug Code | Prompt 1 |
| Agent 2 | Verbose Functions, Deep Nesting | Prompt 2 |
| Agent 3 | Naming, Duplication | Prompt 3 |
| Agent 4 | Magic Literals, Long Parameters | Prompt 4 |
| Agent 5 | Style, Comments | Prompt 5 |

---

## Prompt 1: Dead Code & Debug Code Detection

```
Scan this codebase for DEAD CODE and DEBUG CODE artifacts.

DEAD CODE includes:
- Unused variables (declared but never read)
- Unused functions (defined but never called)
- Unused imports
- Unreachable code (after return, in always-false conditions)
- Commented-out code blocks

DEBUG CODE includes:
- console.log, console.debug, console.error (outside proper logging)
- print() statements (outside proper logging)
- fmt.Println, log.Println used for debugging
- TODO, FIXME, HACK, XXX comments
- debugger statements
- Hardcoded test data

For EACH issue found, report:
| File | Line | Issue Type | Code Snippet | Severity |
|------|------|------------|--------------|----------|

Severity: CRITICAL for dead code, CRITICAL for debug code in production paths.
```

---

## Prompt 2: Verbose Functions & Deep Nesting Detection

```
Scan this codebase for VERBOSE FUNCTIONS and DEEP NESTING.

VERBOSE FUNCTIONS (any of):
- Functions longer than 30 lines
- Functions with more than one level of abstraction
- Functions that require "and" to describe
- Functions with multiple independent operations

DEEP NESTING (any of):
- Indentation > 3 levels (12 spaces / 3 tabs)
- Multiple nested if/else blocks
- Nested try-catch blocks
- Loops inside loops inside conditionals

For EACH issue found, report:
| File | Line | Function Name | Issue | Lines/Depth | Suggested Fix |
|------|------|---------------|-------|-------------|---------------|

Suggested Fix: "Extract Function", "Guard Clauses", "Decompose Conditional"
Severity: HIGH for all.
```

---

## Prompt 3: Naming & Duplication Detection

```
Scan this codebase for POOR NAMING and COPY-PASTE DUPLICATION.

POOR NAMING includes:
- Generic names: data, result, temp, item, obj, val, value, x, info
- Manager/Handler/Processor/Helper/Utils without specificity
- Single letters (except i, j, k in loops)
- Abbreviations not universally known
- Names that mislead about what code does
- Inconsistent naming for same concept

DUPLICATION includes:
- Near-identical code blocks (>5 lines)
- Same logic with only variable names changed
- Repeated error handling patterns
- Repeated validation patterns
- Same API call pattern repeated

For EACH naming issue:
| File | Line | Current Name | Problem | Suggested Name |
|------|------|--------------|---------|----------------|

For EACH duplication:
| Location 1 | Location 2 | Lines Duplicated | Similarity % |
|------------|------------|------------------|--------------|

Severity: MEDIUM for naming, HIGH for duplication.
```

---

## Prompt 4: Magic Literals & Long Parameters Detection

```
Scan this codebase for MAGIC LITERALS and LONG PARAMETER LISTS.

MAGIC LITERALS include:
- Numbers without explanation (60, 24, 1000, 100, 404, 500)
- Repeated string literals
- Status codes as raw numbers
- Configuration values inline
- Timeout/retry values hardcoded

LONG PARAMETER LISTS include:
- Functions with 4+ parameters
- Multiple boolean parameters
- Parameters that always travel together
- Optional parameter sprawl

For EACH magic literal:
| File | Line | Literal | Context | Suggested Constant Name |
|------|------|---------|---------|------------------------|

For EACH long parameter list:
| File | Function Name | Param Count | Parameters | Suggested Fix |
|------|---------------|-------------|------------|---------------|

Suggested Fix: "Introduce Parameter Object", "Extract Class"
Severity: MEDIUM for magic literals, MEDIUM for long parameters.
```

---

## Prompt 5: Style & Comments Detection

```
Scan this codebase for INCONSISTENT STYLE and EXCESSIVE COMMENTS.

INCONSISTENT STYLE includes:
- Mixed camelCase and snake_case in same file
- Mixed quote styles (' vs ")
- Inconsistent indentation (tabs vs spaces, 2 vs 4)
- Mixed async patterns (callbacks, promises, async/await)
- Inconsistent brace style
- Mixed import styles

EXCESSIVE COMMENTS includes:
- Comments explaining what code does (not why)
- Comments duplicating the code exactly
- Outdated comments not matching code
- Block comments before every line
- Trivial JSDoc/docstrings on private functions

For EACH style issue:
| File | Issue | Example 1 | Example 2 |
|------|-------|-----------|-----------|

For EACH comment issue:
| File | Line | Comment | Problem | Recommendation |
|------|------|---------|---------|----------------|

Severity: LOW for style (formatter can fix), LOW for comments.
```

---

## Prompt 6: God Classes & Feature Envy Detection

```
Scan this codebase for GOD CLASSES and FEATURE ENVY.

GOD CLASSES (any of):
- Classes > 500 lines
- Classes with 10+ public methods
- Classes with unrelated methods
- "Manager", "Handler", "Processor", "Service", "Utils" in name
- Classes touching multiple domains

FEATURE ENVY (any of):
- Methods calling multiple getters on same external object
- Long method chains on another object (a.b.c.d())
- Calculations using only another object's fields
- Methods that should logically belong to another class

For EACH god class:
| File | Class Name | Lines | Public Methods | Responsibilities Found |
|------|------------|-------|----------------|----------------------|

For EACH feature envy:
| File | Method | Target Class | Calls to Target | Recommendation |
|------|--------|--------------|-----------------|----------------|

Severity: HIGH for god classes, MEDIUM for feature envy.
```

---

## Prompt 7: Boolean Parameters & Primitive Obsession Detection

```
Scan this codebase for BOOLEAN PARAMETERS and PRIMITIVE OBSESSION.

BOOLEAN PARAMETERS include:
- Functions accepting boolean flags
- doSomething(data, true) patterns (what does true mean?)
- Multiple boolean parameters
- if/else in function based on boolean parameter

PRIMITIVE OBSESSION includes:
- Email as string instead of Email type
- Money as float/int instead of Money type
- Phone numbers, zip codes as strings
- Status as string instead of enum/union
- Validation repeated for same concept

For EACH boolean parameter:
| File | Function | Parameter | Behavior Change | Suggested Fix |
|------|----------|-----------|-----------------|---------------|

For EACH primitive obsession:
| File | Concept | Current Type | Suggested Type | Occurrences |
|------|---------|--------------|----------------|-------------|

Suggested Fix: "Remove Flag Argument", "Replace Primitive with Object"
Severity: MEDIUM for all.
```

---

## Prompt 8: Overly Defensive Code Detection

```
Scan this codebase for OVERLY DEFENSIVE CODE.

Look for:
- Null checks on values that can never be null (TypeScript non-null types, required params)
- Try-catch wrapping simple operations that can't throw
- Defensive copies of immutable data
- Validation of trusted internal inputs
- Redundant type checks (after TypeScript/type annotations)
- Empty catch blocks that swallow errors
- Excessive optional chaining (?.) on required values

For EACH issue:
| File | Line | Defensive Code | Why Unnecessary | Recommendation |
|------|------|----------------|-----------------|----------------|

Severity: LOW for most, MEDIUM if hiding bugs.
```

---

## Summary Report Prompt

After all detection agents complete, use this prompt to consolidate:

```
Compile a SUMMARY REPORT from the smell detection results.

Group findings by severity:
1. CRITICAL: Must fix immediately (dead code, debug artifacts)
2. HIGH: Fix this session (verbose functions, god classes, duplication, deep nesting)
3. MEDIUM: Fix if time permits (naming, magic literals, parameters, primitives)
4. LOW: Opportunistic (style, comments, defensive code)

Provide counts:
| Severity | Count | Top 3 File Hotspots |
|----------|-------|---------------------|

Identify quick wins (high impact, low effort):
- Remove Dead Code in [files]
- Remove Debug Code in [files]
- Apply Guard Clauses in [functions]

Recommend scanning priority for next phase:
1. [File/directory with most issues]
2. [File/directory with second most]
3. [File/directory with third most]
```
