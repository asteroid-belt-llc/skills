# Fowler Refactorings Reference

> **MANDATORY**: Read this reference during Phase 4 (PLAN) to select appropriate refactorings.

This is a curated subset of [Martin Fowler's Refactoring Catalog](https://refactoring.com/catalog/) containing the 20 most applicable refactorings for cleaning AI-generated code.

---

## Table of Contents

1. [Function Refactorings](#function-refactorings)
2. [Variable Refactorings](#variable-refactorings)
3. [Conditional Refactorings](#conditional-refactorings)
4. [Organization Refactorings](#organization-refactorings)
5. [Data Refactorings](#data-refactorings)

---

## Function Refactorings

### Extract Function

**When to use**: Function is too long, or a code fragment needs explanation.

**Mechanics**:
1. Create new function with intention-revealing name
2. Copy extracted code to new function
3. Scan for local variables used only in extracted code (make them local to new function)
4. Scan for local variables modified by extracted code (may need to return them)
5. Replace extracted code with call to new function
6. Test

**Example**:
```javascript
// Before
function printOwing(invoice) {
  let outstanding = 0;
  console.log("***********************");
  console.log("**** Customer Owes ****");
  console.log("***********************");
  for (const o of invoice.orders) {
    outstanding += o.amount;
  }
  console.log(`name: ${invoice.customer}`);
  console.log(`amount: ${outstanding}`);
}

// After
function printOwing(invoice) {
  printBanner();
  const outstanding = calculateOutstanding(invoice);
  printDetails(invoice, outstanding);
}
```

---

### Inline Function

**When to use**: Function body is as clear as its name, or when you need to reorganize.

**Mechanics**:
1. Check function isn't polymorphic (overridden in subclasses)
2. Find all callers
3. Replace each call with function body
4. Remove function definition
5. Test

---

### Move Function

**When to use**: Function references elements of another context more than its own.

**Mechanics**:
1. Examine what the function references in current context
2. Decide whether to move as-is or extract part of it
3. Copy function to target context
4. Adjust function to fit new home
5. Update callers
6. Test

---

### Remove Dead Code

**When to use**: Code is never executed or referenced.

**Mechanics**:
1. If dead code can be referenced from outside (exported), check no callers exist
2. Remove the dead code
3. Test

---

### Replace Inline Code with Function Call

**When to use**: Inline code does same thing as existing function.

**Mechanics**:
1. Replace inline code with call to existing function
2. Test

---

## Variable Refactorings

### Extract Variable

**When to use**: Expression is complex and hard to understand.

**Mechanics**:
1. Ensure expression has no side effects
2. Declare immutable variable
3. Set it to the expression
4. Replace original expression with variable reference
5. Test

**Example**:
```python
# Before
return order.quantity * order.item_price - \
    max(0, order.quantity - 500) * order.item_price * 0.05 + \
    min(order.quantity * order.item_price * 0.1, 100)

# After
base_price = order.quantity * order.item_price
quantity_discount = max(0, order.quantity - 500) * order.item_price * 0.05
shipping = min(base_price * 0.1, 100)
return base_price - quantity_discount + shipping
```

---

### Inline Variable

**When to use**: Variable name says no more than the expression.

**Mechanics**:
1. Check expression has no side effects
2. Find first reference to variable
3. Replace with expression
4. Test
5. Repeat for each reference
6. Remove variable declaration
7. Test

---

### Rename Variable

**When to use**: Variable name doesn't clearly express what it contains.

**Mechanics**:
1. If variable used widely, consider encapsulating it first
2. Find all references and change them
3. Test

---

### Replace Magic Literal

**When to use**: Literal value with special meaning appears in code.

**Mechanics**:
1. Create a constant and set it to the magic literal
2. Find all occurrences of the magic literal
3. Replace each with constant reference
4. Test

---

### Encapsulate Variable

**When to use**: Data accessed directly from many places.

**Mechanics**:
1. Create encapsulating function(s) for getting/setting
2. Run find-replace to use new functions
3. Restrict visibility of variable
4. Test

---

### Replace Temp with Query

**When to use**: Temporary variable holds result of expression.

**Mechanics**:
1. Check temp is assigned only once
2. Extract the expression into a function
3. Replace temp with function call
4. Test

---

## Conditional Refactorings

### Decompose Conditional

**When to use**: Complex conditional (if-then-else) logic.

**Mechanics**:
1. Extract condition into function with intention-revealing name
2. Extract then-body into function
3. Extract else-body into function
4. Test

**Example**:
```typescript
// Before
if (date.before(SUMMER_START) || date.after(SUMMER_END)) {
  charge = quantity * winterRate + winterServiceCharge;
} else {
  charge = quantity * summerRate;
}

// After
if (isSummer(date)) {
  charge = summerCharge(quantity);
} else {
  charge = winterCharge(quantity);
}
```

---

### Replace Nested Conditional with Guard Clauses

**When to use**: Function has conditional behavior that doesn't make clear the normal path.

**Mechanics**:
1. Select outermost condition that needs guard clause
2. Restructure to guard clause (early return)
3. Test
4. Repeat for other conditions

**Example**:
```go
// Before
func getPayAmount() float64 {
    var result float64
    if isDead {
        result = deadAmount()
    } else {
        if isSeparated {
            result = separatedAmount()
        } else {
            if isRetired {
                result = retiredAmount()
            } else {
                result = normalPayAmount()
            }
        }
    }
    return result
}

// After
func getPayAmount() float64 {
    if isDead { return deadAmount() }
    if isSeparated { return separatedAmount() }
    if isRetired { return retiredAmount() }
    return normalPayAmount()
}
```

---

### Consolidate Conditional Expression

**When to use**: Sequence of conditional checks with same result.

**Mechanics**:
1. Check none of the conditionals have side effects
2. Combine into single conditional using logical operators
3. Consider extracting consolidated condition into function
4. Test

---

### Replace Conditional with Polymorphism

**When to use**: Complex conditional choosing different behavior based on type.

**Mechanics**:
1. Create subclass for each leg of conditional (or use strategy pattern)
2. Create factory function to return appropriate instance
3. Move conditional logic to subclass methods
4. Test

---

## Organization Refactorings

### Extract Class

**When to use**: Class does too much (God Class), or subset of data/methods go together.

**Mechanics**:
1. Decide what to split off
2. Create new class
3. Link old to new (usually via field)
4. Move fields using Move Field
5. Move methods using Move Function
6. Review interfaces, minimize what's public
7. Consider exposing new class directly
8. Test

---

### Move Field

**When to use**: Field is used more by another class, or when extracting a class.

**Mechanics**:
1. Ensure source field is encapsulated
2. Create field (and accessors) on target
3. Update source field accessors to use target
4. Test
5. Remove source field
6. Test

---

### Combine Functions into Class

**When to use**: Group of functions operate on same data.

**Mechanics**:
1. Create class with shared data as constructor arguments
2. Move each function into class
3. Extract logic on data into class methods
4. Test

---

### Slide Statements

**When to use**: Related code should be near each other.

**Mechanics**:
1. Identify target position for code
2. Check if there are interfering statements (side effects, dependencies)
3. Move code to target position
4. Test

---

## Data Refactorings

### Introduce Parameter Object

**When to use**: Group of parameters that go together.

**Mechanics**:
1. Create a new class/type for the parameter group
2. Add parameter of new type to function
3. Modify callers to pass new type
4. Replace individual parameters with fields from new type
5. Remove old parameters
6. Test

---

### Replace Primitive with Object

**When to use**: Primitive has behavior that should be encapsulated.

**Mechanics**:
1. Create class for the primitive
2. Add getter/setter for primitive value
3. Change callers to use new class
4. Add behavior methods to class
5. Test

---

### Remove Flag Argument

**When to use**: Boolean parameter switches function behavior.

**Mechanics**:
1. Create explicit function for each flag value
2. Replace callers that pass literal with appropriate function
3. For callers passing variable, keep original but refactor body
4. Test

**Example**:
```python
# Before
def set_dimension(name, value, is_height):
    if is_height:
        self.height = value
    else:
        self.width = value

# After
def set_height(value):
    self.height = value

def set_width(value):
    self.width = value
```

---

### Split Loop

**When to use**: Loop does two or more things.

**Mechanics**:
1. Copy loop
2. Identify and remove duplicate code in each loop
3. Test
4. Consider Extract Function on each loop

---

### Replace Loop with Pipeline

**When to use**: Loop processes a collection.

**Mechanics**:
1. Create variable for loop collection
2. Convert loop body to pipeline operations (filter, map, reduce)
3. Remove loop
4. Test

**Example**:
```javascript
// Before
const result = [];
for (const item of items) {
  if (item.active) {
    result.push(item.name.toUpperCase());
  }
}

// After
const result = items
  .filter(item => item.active)
  .map(item => item.name.toUpperCase());
```

---

## Quick Selection Guide

| Smell | Recommended Refactoring |
|-------|------------------------|
| Long Function | Extract Function |
| Dead Code | Remove Dead Code |
| Poor Names | Rename Variable/Function |
| Magic Literals | Replace Magic Literal |
| Duplication | Extract Function, Combine Functions into Class |
| Deep Nesting | Replace Nested Conditional with Guard Clauses |
| Long Parameter List | Introduce Parameter Object |
| God Class | Extract Class, Move Function |
| Feature Envy | Move Function |
| Primitive Obsession | Replace Primitive with Object |
| Boolean Parameter | Remove Flag Argument |
| Complex Conditional | Decompose Conditional |
