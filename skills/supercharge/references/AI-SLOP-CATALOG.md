# AI Slop Catalog

> **MANDATORY**: Read this reference during Phase 2 (SCAN) to identify code quality issues.

This catalog documents the 15 most common AI-generated code problems ("slop") that supercharge targets.

---

## Table of Contents

1. [Verbose Functions](#1-verbose-functions)
2. [Dead Code](#2-dead-code)
3. [Poor Naming](#3-poor-naming)
4. [Excessive Comments](#4-excessive-comments)
5. [Magic Numbers/Strings](#5-magic-numbersstrings)
6. [Copy-Paste Duplication](#6-copy-paste-duplication)
7. [Deep Nesting](#7-deep-nesting)
8. [Long Parameter Lists](#8-long-parameter-lists)
9. [God Classes](#9-god-classes)
10. [Feature Envy](#10-feature-envy)
11. [Primitive Obsession](#11-primitive-obsession)
12. [Boolean Parameters](#12-boolean-parameters)
13. [Inconsistent Style](#13-inconsistent-style)
14. [Overly Defensive Code](#14-overly-defensive-code)
15. [Hardcoded Debug Code](#15-hardcoded-debug-code)

---

## 1. Verbose Functions

**What it is**: Functions that do too much, contain multiple responsibilities, or are unnecessarily long.

**Why AI does this**: LLMs optimize for "complete" solutions, generating everything in one place rather than composing smaller pieces.

**Detection signals**:
- Functions > 30 lines
- Multiple levels of abstraction in one function
- Function name requires "and" to describe what it does
- Multiple return statements handling different concerns

**Refactoring**: Extract Function, Extract Variable

**Example**:
```javascript
// BAD: AI slop - does validation, transformation, AND persistence
function processUserData(userData) {
  // 50 lines of mixed concerns
}

// GOOD: Single responsibility
function validateUserData(userData) { /* 10 lines */ }
function transformUserData(validated) { /* 10 lines */ }
function persistUserData(transformed) { /* 10 lines */ }
```

---

## 2. Dead Code

**What it is**: Unused variables, unreachable branches, commented-out code, unused imports, unused functions.

**Why AI does this**: LLMs generate "just in case" code, leave debugging artifacts, and don't track what's actually used.

**Detection signals**:
- Variables declared but never read
- Functions defined but never called
- `if (false)` or always-true conditions
- Commented-out code blocks
- Imports without usage

**Refactoring**: Remove Dead Code

**Example**:
```python
# BAD: AI slop
def calculate_total(items):
    debug_mode = False  # Never used
    # old_calculation = sum(items)  # Commented out
    if False:  # Unreachable
        print("debug")
    return sum(items)

# GOOD: Clean
def calculate_total(items):
    return sum(items)
```

---

## 3. Poor Naming

**What it is**: Generic, meaningless, or misleading variable and function names.

**Why AI does this**: LLMs default to common patterns from training data without domain context.

**Detection signals**:
- Names like: `data`, `result`, `temp`, `item`, `obj`, `val`, `x`, `i` (outside loops)
- Names like: `handler`, `manager`, `processor`, `helper`, `utils`, `misc`
- Single-letter variables (except loop counters)
- Abbreviations that aren't universally known
- Names that don't match what the code does

**Refactoring**: Rename Variable, Rename Function

**Example**:
```typescript
// BAD: AI slop
function processData(data: any): any {
  const result = data.map(item => item.value);
  return result;
}

// GOOD: Meaningful names
function extractPricesFromProducts(products: Product[]): number[] {
  const prices = products.map(product => product.price);
  return prices;
}
```

---

## 4. Excessive Comments

**What it is**: Comments that explain obvious code, or comments used instead of clear code.

**Why AI does this**: LLMs are trained on documentation-heavy code and generate comments to appear helpful.

**Detection signals**:
- Comments explaining what code does (not why)
- Comments that duplicate the code exactly
- Outdated comments that don't match code
- Block comments before every line
- JSDoc/docstrings for trivial private functions

**Refactoring**: Rename to make code self-documenting, Remove redundant comments

**Example**:
```java
// BAD: AI slop
// Loop through the users
for (User user : users) {
    // Get the user's name
    String name = user.getName();
    // Print the name
    System.out.println(name);
}

// GOOD: Self-documenting
for (User user : users) {
    System.out.println(user.getName());
}
```

---

## 5. Magic Numbers/Strings

**What it is**: Hardcoded literal values without named constants explaining their meaning.

**Why AI does this**: LLMs generate working code without considering maintainability.

**Detection signals**:
- Numbers like `60`, `24`, `1000`, `100` without context
- Repeated string literals
- Status codes as raw numbers
- Configuration values inline

**Refactoring**: Replace Magic Literal, Extract Variable

**Example**:
```go
// BAD: AI slop
if age >= 18 && status == "active" && retryCount < 3 {
    time.Sleep(1000 * time.Millisecond)
}

// GOOD: Named constants
const (
    MinimumAge      = 18
    ActiveStatus    = "active"
    MaxRetries      = 3
    RetryDelayMs    = 1000
)
if age >= MinimumAge && status == ActiveStatus && retryCount < MaxRetries {
    time.Sleep(RetryDelayMs * time.Millisecond)
}
```

---

## 6. Copy-Paste Duplication

**What it is**: Near-identical code blocks repeated in multiple places (DRY violations).

**Why AI does this**: LLMs generate each piece of code independently without awareness of existing similar code.

**Detection signals**:
- Identical or near-identical code blocks
- Same logic with only variable names changed
- Same error handling repeated
- Same validation repeated

**Refactoring**: Extract Function, Combine Functions into Class

**Example**:
```python
# BAD: AI slop - same pattern repeated
def get_user_by_id(user_id):
    try:
        response = requests.get(f"/users/{user_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to get user: {e}")
        raise

def get_order_by_id(order_id):
    try:
        response = requests.get(f"/orders/{order_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to get order: {e}")
        raise

# GOOD: Extracted common logic
def fetch_resource(resource_type, resource_id):
    try:
        response = requests.get(f"/{resource_type}/{resource_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to get {resource_type}: {e}")
        raise
```

---

## 7. Deep Nesting

**What it is**: Code with 3+ levels of nested conditionals or loops.

**Why AI does this**: LLMs generate code sequentially, adding conditions without restructuring.

**Detection signals**:
- Indentation > 3 tabs/12 spaces
- Multiple nested if/else blocks
- Nested try-catch blocks
- Loops inside loops inside conditionals

**Refactoring**: Replace Nested Conditional with Guard Clauses, Extract Function, Decompose Conditional

**Example**:
```javascript
// BAD: AI slop - 4 levels deep
function processOrder(order) {
  if (order) {
    if (order.items) {
      if (order.items.length > 0) {
        if (order.status === 'pending') {
          // actual logic buried here
        }
      }
    }
  }
}

// GOOD: Guard clauses
function processOrder(order) {
  if (!order) return;
  if (!order.items || order.items.length === 0) return;
  if (order.status !== 'pending') return;

  // actual logic at top level
}
```

---

## 8. Long Parameter Lists

**What it is**: Functions with 4+ parameters.

**Why AI does this**: LLMs add parameters incrementally without considering object composition.

**Detection signals**:
- Functions with 4+ parameters
- Boolean parameters (especially multiple)
- Parameters that always go together
- Optional parameters sprawl

**Refactoring**: Introduce Parameter Object, Combine Functions into Class

**Example**:
```typescript
// BAD: AI slop
function createUser(
  name: string,
  email: string,
  age: number,
  address: string,
  city: string,
  country: string,
  phone: string,
  isAdmin: boolean
) { /* ... */ }

// GOOD: Parameter object
interface CreateUserRequest {
  name: string;
  email: string;
  age: number;
  address: Address;
  phone: string;
  isAdmin: boolean;
}
function createUser(request: CreateUserRequest) { /* ... */ }
```

---

## 9. God Classes

**What it is**: Classes with too many responsibilities, usually 500+ lines.

**Why AI does this**: LLMs centralize related functionality without considering separation of concerns.

**Detection signals**:
- Classes > 500 lines
- Classes with 10+ public methods
- Classes with unrelated methods
- "Manager", "Handler", "Processor", "Utils" in class name
- Class touches multiple domains

**Refactoring**: Extract Class, Move Function, Move Field

---

## 10. Feature Envy

**What it is**: Methods that use another class's data more than their own.

**Why AI does this**: LLMs don't understand object boundaries, placing logic wherever it's first needed.

**Detection signals**:
- Multiple getter calls on the same object
- Long method chains on another object
- Calculations using only another object's fields

**Refactoring**: Move Function

**Example**:
```java
// BAD: AI slop - Order logic in Invoice class
class Invoice {
    double calculateShipping(Order order) {
        return order.getWeight() * order.getDistance() * order.getRate();
    }
}

// GOOD: Logic belongs with data
class Order {
    double calculateShipping() {
        return weight * distance * rate;
    }
}
```

---

## 11. Primitive Obsession

**What it is**: Using primitives (string, int) instead of small domain objects.

**Why AI does this**: LLMs generate the simplest working code without domain modeling.

**Detection signals**:
- Email as `string` instead of `Email` type
- Money as `float` instead of `Money` type
- Phone numbers, zip codes as strings
- Status as string instead of enum
- Validation logic repeated for same concept

**Refactoring**: Replace Primitive with Object

---

## 12. Boolean Parameters

**What it is**: Functions that accept boolean flags to change behavior.

**Why AI does this**: LLMs extend existing functions with flags rather than creating new functions.

**Detection signals**:
- `doSomething(data, true)` - what does `true` mean?
- Multiple boolean parameters
- if/else in function based on boolean parameter

**Refactoring**: Remove Flag Argument, Extract Function

**Example**:
```python
# BAD: AI slop
def render_user(user, show_email=True, show_phone=False, is_admin=False):
    # Different logic based on flags

# GOOD: Separate functions or configuration object
def render_user_public(user): ...
def render_user_admin(user): ...
```

---

## 13. Inconsistent Style

**What it is**: Mixed naming conventions, formatting, or patterns within the same codebase.

**Why AI does this**: LLMs generate code based on varied training data without consistent style.

**Detection signals**:
- Mixed `camelCase` and `snake_case`
- Mixed quote styles (`'` vs `"`)
- Inconsistent indentation
- Some functions with types, some without
- Mixed async patterns (callbacks, promises, async/await)

**Refactoring**: Apply consistent style (usually via formatter)

---

## 14. Overly Defensive Code

**What it is**: Unnecessary null checks, try-catches everywhere, defensive copies.

**Why AI does this**: LLMs add defensive code "just in case" without understanding actual risks.

**Detection signals**:
- Null checks on values that can never be null
- Try-catch wrapping every operation
- Defensive copies of immutable data
- Validation of trusted internal inputs

**Refactoring**: Remove unnecessary guards (after verifying they're truly unnecessary)

---

## 15. Hardcoded Debug Code

**What it is**: Console.log, print statements, TODO comments, temporary debugging artifacts.

**Why AI does this**: LLMs include debugging code from training data or generate it for "helpfulness".

**Detection signals**:
- `console.log`, `print()`, `fmt.Println` outside logging infrastructure
- `// TODO`, `// FIXME`, `// HACK` comments
- Hardcoded test data
- `debugger` statements
- Disabled code via comments

**Refactoring**: Remove Dead Code, Replace with proper logging

---

## Quick Reference Table

| # | Smell | Primary Refactoring | Severity |
|---|-------|---------------------|----------|
| 1 | Verbose Functions | Extract Function | HIGH |
| 2 | Dead Code | Remove Dead Code | CRITICAL |
| 3 | Poor Naming | Rename | MEDIUM |
| 4 | Excessive Comments | Rename / Remove | LOW |
| 5 | Magic Numbers | Replace Magic Literal | MEDIUM |
| 6 | Duplication | Extract Function | HIGH |
| 7 | Deep Nesting | Guard Clauses | HIGH |
| 8 | Long Parameters | Parameter Object | MEDIUM |
| 9 | God Classes | Extract Class | HIGH |
| 10 | Feature Envy | Move Function | MEDIUM |
| 11 | Primitive Obsession | Replace Primitive | MEDIUM |
| 12 | Boolean Parameters | Remove Flag Argument | MEDIUM |
| 13 | Inconsistent Style | Formatter | LOW |
| 14 | Overly Defensive | Remove Guards | LOW |
| 15 | Debug Code | Remove Dead Code | CRITICAL |
