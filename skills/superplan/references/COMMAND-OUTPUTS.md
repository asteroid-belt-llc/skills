# Command Output Specifications

> **MANDATORY**: Every command in the plan MUST include expected output.

## Why Expected Outputs Matter

- **Zero ambiguity** - Executor knows exactly what success looks like
- **Debugging aid** - If output differs, executor can investigate
- **Documentation** - Plan serves as executable specification

---

## Quality Gate Commands

| Command | Expected Output | Indicates |
|---------|-----------------|-----------|
| `npm run lint` | `✓ No problems found` or exit code 0 | Linter passes |
| `npm run typecheck` | `Done in X.XXs` or exit code 0 | Types valid |
| `npm test -- path/to/test` | `PASS path/to/test` | Tests pass |
| `npm run build` | `✓ Built in X.XXs` or exit code 0 | Build succeeds |
| `ruff check .` | No output, exit code 0 | Python linter passes |
| `mypy src/` | `Success: no issues found` | Python types valid |
| `pytest tests/` | `X passed in Y.YYs` | Python tests pass |
| `go build ./...` | No output, exit code 0 | Go build passes |
| `go test ./...` | `ok` for each package | Go tests pass |

---

## TDD Step 2: Expected Failure Format

When writing failing tests, specify the expected failure:

```markdown
**Step 2: Run test to verify it fails**
- Command: `npm test -- tests/auth/login.test.ts`
- Expected Output:
  \`\`\`
  FAIL tests/auth/login.test.ts
  ● AuthService › login › should return token for valid credentials

    expect(received).toBeDefined()

    Received: undefined
  \`\`\`
- This confirms: Test is correctly detecting missing implementation
```

### Python Example

```markdown
**Step 2: Run test to verify it fails**
- Command: `pytest tests/test_auth.py::test_login -v`
- Expected Output:
  \`\`\`
  tests/test_auth.py::test_login FAILED

  E       AssertionError: assert None is not None
  E        +  where None = login('user', 'pass')
  \`\`\`
- This confirms: Function returns None before implementation
```

### Go Example

```markdown
**Step 2: Run test to verify it fails**
- Command: `go test ./auth -run TestLogin -v`
- Expected Output:
  \`\`\`
  === RUN   TestLogin
  --- FAIL: TestLogin (0.00s)
      auth_test.go:15: expected token, got empty string
  FAIL
  \`\`\`
```

---

## TDD Step 4: Expected Success Format

```markdown
**Step 4: Run test to verify it passes**
- Command: `npm test -- tests/auth/login.test.ts`
- Expected Output:
  \`\`\`
  PASS tests/auth/login.test.ts
  ✓ AuthService › login › should return token for valid credentials (15ms)

  Test Suites: 1 passed, 1 total
  Tests:       1 passed, 1 total
  \`\`\`
```

### Python Example

```markdown
**Step 4: Run test to verify it passes**
- Command: `pytest tests/test_auth.py::test_login -v`
- Expected Output:
  \`\`\`
  tests/test_auth.py::test_login PASSED [100%]

  ========== 1 passed in 0.05s ==========
  \`\`\`
```

---

## Definition of Done Verification

After each phase, run all quality gates and document output:

```markdown
### Quality Gate Results

| Check | Command | Result |
|-------|---------|--------|
| Lint | `npm run lint` | ✅ No problems found |
| Types | `npm run typecheck` | ✅ Done in 2.3s |
| Tests | `npm test` | ✅ 47 passed, 0 failed |
| Build | `npm run build` | ✅ Built in 4.1s |
```

---

## Error Output Format

When documenting expected errors (for validation, etc.):

```markdown
**Expected Error Response:**
- Status: 400 Bad Request
- Body:
  \`\`\`json
  {
    "error": "VALIDATION_ERROR",
    "message": "email is required",
    "details": [
      {"field": "email", "message": "Required"}
    ]
  }
  \`\`\`
```
