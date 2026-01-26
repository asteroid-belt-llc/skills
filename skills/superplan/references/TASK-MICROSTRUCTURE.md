# Task Micro-Structure (TDD Cycle)

> **MANDATORY**: Every task within a phase MUST follow this 5-step structure.

## Step Format Template

For each task in your plan, use this exact format:

```markdown
**Task: [Task Name]**

**Files:**
- Create: `exact/path/to/new-file.ts`
- Modify: `exact/path/to/existing.ts:45-67`
- Test: `tests/exact/path/to/test-file.test.ts`

**Step 1: Write the failing test**
\`\`\`[language]
// Full test code here - no pseudocode
\`\`\`

**Step 2: Run test to verify it fails**
- Command: `[exact test command]`
- Expected: FAIL - `[expected error message]`

**Step 3: Write minimal implementation**
\`\`\`[language]
// Full implementation code here - no pseudocode
\`\`\`

**Step 4: Run test to verify it passes**
- Command: `[exact test command]`
- Expected: PASS - `[expected success output]`

**Step 5: Stage for commit**
\`\`\`bash
git add [specific files]
\`\`\`
```

---

## Complete Example

```markdown
**Task: Add validateToken function**

**Files:**
- Create: `src/services/auth.ts`
- Modify: `src/services/index.ts:12-15`
- Test: `tests/services/auth.test.ts`

**Step 1: Write the failing test**
\`\`\`typescript
import { validateToken } from '../src/services/auth';

describe('validateToken', () => {
  it('should return user for valid token', async () => {
    const token = 'valid-jwt-token';
    const result = await validateToken(token);

    expect(result).toBeDefined();
    expect(result.id).toBe('user-123');
  });

  it('should return null for invalid token', async () => {
    const result = await validateToken('invalid');
    expect(result).toBeNull();
  });
});
\`\`\`

**Step 2: Run test to verify it fails**
- Command: `npm test -- tests/services/auth.test.ts`
- Expected Output:
  \`\`\`
  FAIL tests/services/auth.test.ts
  ● validateToken › should return user for valid token

    Cannot find module '../src/services/auth'
  \`\`\`

**Step 3: Write minimal implementation**
\`\`\`typescript
// src/services/auth.ts
import jwt from 'jsonwebtoken';
import { db } from '../db';
import { User } from '../types/user';

export async function validateToken(token: string): Promise<User | null> {
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!) as { userId: string };
    return db.users.findById(decoded.userId);
  } catch {
    return null;
  }
}
\`\`\`

**Step 4: Run test to verify it passes**
- Command: `npm test -- tests/services/auth.test.ts`
- Expected Output:
  \`\`\`
  PASS tests/services/auth.test.ts
  ✓ validateToken › should return user for valid token (15ms)
  ✓ validateToken › should return null for invalid token (3ms)

  Test Suites: 1 passed, 1 total
  Tests:       2 passed, 2 total
  \`\`\`

**Step 5: Stage for commit**
\`\`\`bash
git add src/services/auth.ts tests/services/auth.test.ts
\`\`\`
```

---

## Why This Structure?

| Benefit | Explanation |
|---------|-------------|
| **Executable steps** | No ambiguity about what to do next |
| **Verifiable progress** | Each step has clear success/failure criteria |
| **TDD enforced** | Tests written before implementation |
| **Atomic commits** | Each task is one logical unit of work |
| **Zero context** | A fresh agent can execute without asking questions |

---

## Common Mistakes to Avoid

### ❌ Pseudocode instead of real code
```typescript
// BAD: Don't do this
function validate(token) {
  // validate the token here
  // return user if valid
}
```

### ❌ Missing expected output
```markdown
**Step 2: Run test**
- Command: `npm test`
- Expected: Should fail  ← TOO VAGUE
```

### ❌ Vague file paths
```markdown
**Files:**
- Modify: `auth.ts`  ← WHERE IS THIS FILE?
```

### ✅ Correct approach
```typescript
// GOOD: Full, runnable code
export async function validateToken(token: string): Promise<User | null> {
  const decoded = jwt.verify(token, process.env.JWT_SECRET!);
  if (!decoded) return null;
  return db.users.findById(decoded.userId);
}
```
