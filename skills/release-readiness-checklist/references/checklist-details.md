# Checklist Item Details

Detailed explanations for each release readiness checklist item.

## Table of Contents

- [Code Quality](#code-quality)
- [Testing](#testing)
- [Documentation](#documentation)
- [Security](#security)
- [Versioning](#versioning)
- [CI/CD](#cicd)
- [Release Artifacts](#release-artifacts)
- [Operational Readiness](#operational-readiness)

---

## Code Quality

### All code changes reviewed and approved

Every change in the release should have been reviewed by at least one other team member. Check:
- All PRs merged to the release branch have approvals
- No pending review requests on included changes

### No TODO/FIXME comments blocking release

Search codebase for blocking comments:
```bash
grep -rn "TODO\|FIXME\|HACK\|XXX" --include="*.{js,ts,py,go,java,rb}" .
```
Evaluate if any are blockers. Not all TODOs require immediate action.

### No debug code or console statements

Remove temporary debugging code:
```bash
# JavaScript/TypeScript
grep -rn "console.log\|console.debug\|debugger" --include="*.{js,ts,tsx}"

# Python
grep -rn "print(\|pdb\|breakpoint()" --include="*.py"
```

### Linting passes

Run linter with no errors:

```bash
# Prefer project task runner if available
make lint             # Makefile
just lint             # Justfile

# Or language-specific commands
npm run lint          # Node.js
ruff check .          # Python
cargo clippy          # Rust
golangci-lint run     # Go
```

### Type checking passes

For typed languages, verify no type errors:

```bash
# Prefer project task runner if available
make check            # Makefile (often includes type checking)
just check            # Justfile

# Or language-specific commands
npx tsc --noEmit      # TypeScript
mypy .                # Python
```

---

## Testing

### All tests pass

Run full test suite. All tests must pass:

```bash
# Prefer project task runner if available
make test             # Makefile
just test             # Justfile

# Or language-specific commands
npm test              # Node.js
pytest                # Python
cargo test            # Rust
go test ./...         # Go
```

### Test coverage meets threshold

Check coverage meets project minimum (common thresholds: 70-80%):

```bash
# Prefer project task runner if available
make coverage         # Makefile
just coverage         # Justfile

# Or language-specific commands
npm run test:coverage # Node.js
pytest --cov          # Python
```

### Critical paths have integration tests

Verify key user journeys are covered:
- Authentication flow
- Primary business operations
- External API integrations
- Database transactions

### Manual testing for new features

Document manual testing performed:
- Feature works as specified
- Edge cases handled
- Error states display correctly

### Regression testing for bug fixes

For each bug fix:
- Confirm bug is fixed
- Verify fix doesn't break related functionality
- Add automated test to prevent regression

---

## Documentation

### CHANGELOG updated

Follow Keep a Changelog format:
```markdown
## [1.2.0] - 2024-01-15

### Added
- New feature X

### Changed
- Updated behavior Y

### Fixed
- Bug in Z
```

### README updated

Update if any of these changed:
- Installation steps
- Configuration options
- API usage examples
- System requirements

### API documentation reflects changes

Update API docs for:
- New endpoints
- Changed parameters
- Deprecated features
- New response formats

### Migration guide for breaking changes

For MAJOR versions, document:
- What changed
- Why it changed
- Step-by-step migration instructions
- Code examples (before/after)

---

## Security

### No secrets in codebase

Scan for exposed secrets:

```bash
# Use tools like git-secrets, trufflehog, or gitleaks
gitleaks detect --source .
```

Check for:

- API keys
- Passwords
- Private keys
- Connection strings

### Git history scanned for exposed secrets

Secrets committed and later deleted remain in git history. Scan the full history:

```bash
# Full history scan with gitleaks
gitleaks detect --source . --log-opts="--all"

# Or with trufflehog
trufflehog git file://.
```

If secrets found:

1. **Rotate immediately** - assume compromised
2. **Remove from history** if not yet public (use git-filter-repo or BFG)
3. **Add pre-commit hooks** to prevent future leaks

See [secrets-scanning.md](secrets-scanning.md) for detailed remediation steps.

### Dependencies scanned

Run vulnerability scan:

```bash
# Prefer project task runner if available
make audit            # Makefile
just audit            # Justfile

# Or language-specific commands
npm audit             # Node.js
pip-audit             # Python
cargo audit           # Rust
```

Address critical and high severity issues before release.

### Security-sensitive changes reviewed

Extra scrutiny for changes to:
- Authentication/authorization
- Input validation
- Cryptographic operations
- Data handling (PII, financial)

### Auth changes tested

For authentication/authorization changes:
- Test all user roles
- Verify permission boundaries
- Check session handling
- Test logout/token revocation

---

## Versioning

### Version bumped correctly

See references/semver.md for guidance. Verify:
- Version follows semantic versioning
- Bump matches change significance
- Pre-release suffix if applicable

### Version consistent across files

Check all version files match:
```bash
# Find version references
grep -rn "version" package.json pyproject.toml Cargo.toml
```

### Git tag prepared

Create tag but don't push yet:
```bash
git tag -a v1.2.3 -m "Release 1.2.3"
# Verify with: git tag -l
```

### Previous version accessible

Confirm users can still access previous version:
- Git tag exists
- Package registry has previous version
- Documentation for previous version available

---

## CI/CD

### All CI checks pass

Verify in CI dashboard:

- Build succeeds
- Tests pass
- Linting passes
- Security scans pass

### Pipeline configuration follows best practices

Review pipeline configuration against best practices:

```bash
# Detect pipeline type
ls -la .github/workflows/  # GitHub Actions
ls -la .gitlab-ci.yml      # GitLab CI
```

Key checks:

- **Security**: Action/image versions pinned, secrets not hardcoded, minimal permissions
- **Performance**: Caching enabled, parallel jobs where possible, path filters configured
- **Reliability**: Timeouts set, concurrency controls in place

See [ci-cd-best-practices.md](ci-cd-best-practices.md) for detailed guidance.

### Build artifacts generated

Confirm build produces expected outputs:
- Compiled binaries
- Docker images
- Package files (npm, wheel, gem)

### Deployment tested in staging

Before production:
- Deploy to staging environment
- Run smoke tests
- Verify critical functionality
- Check logs for errors

### Rollback procedure tested

Document and test rollback:
- How to revert deployment
- Database rollback if needed
- Time estimate for rollback
- Who can authorize rollback

---

## Release Artifacts

### Release notes drafted

Include:
- Summary of changes
- Breaking changes highlighted
- Upgrade instructions
- Known issues
- Acknowledgments

### Changelog entry finalized

Entry matches actual release content. Verify:
- All significant changes listed
- Dates are correct
- Links work

### Distribution packages built

Build final packages:

```bash
# Prefer project task runner if available
make build            # Makefile
just build            # Justfile

# Or language-specific commands
npm pack              # Node.js
python -m build       # Python
cargo build --release # Rust
```

### Checksums generated

For binary distributions:
```bash
sha256sum release-binary > SHA256SUMS
gpg --sign SHA256SUMS  # Optional: GPG signature
```

---

## Operational Readiness

### Monitoring configured

Verify monitoring covers:
- Application health endpoints
- Error rates
- Performance metrics
- Business metrics

### Rollback plan documented

Document includes:
- Decision criteria for rollback
- Step-by-step rollback procedure
- Communication plan during rollback
- Post-rollback verification

### On-call team notified

Inform relevant teams:
- Deployment time window
- Expected changes
- Potential risks
- Escalation contacts

### Communication plan ready

Prepare announcements:
- Internal team notification
- Customer communication (if applicable)
- Social media / blog post (if applicable)
- Support team briefing
