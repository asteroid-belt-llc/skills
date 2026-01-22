# Semantic Versioning Guide

## Format: MAJOR.MINOR.PATCH

Version numbers communicate the nature of changes to users and automated tools.

## When to Increment

### MAJOR (breaking changes)
Increment when changes require users to modify their code or configuration:

```
1.2.3 → 2.0.0

Examples:
- Removed deprecated API endpoint
- Changed required parameters
- Renamed public function from `getData()` to `fetchData()`
- Changed return type from array to object
- Dropped support for Node.js 14
```

### MINOR (new features)
Increment when adding functionality that doesn't break existing usage:

```
1.2.3 → 1.3.0

Examples:
- Added new optional parameter to existing function
- New API endpoint
- New configuration option with sensible default
- Deprecated old method (still works, warns about removal)
```

### PATCH (bug fixes)
Increment for backward-compatible bug fixes:

```
1.2.3 → 1.2.4

Examples:
- Fixed null pointer exception
- Corrected calculation error
- Fixed typo in error message
- Security patch that doesn't change behavior
```

## Pre-release Versions

Use suffixes for pre-release versions:

```
1.0.0-alpha.1    # Early testing, unstable
1.0.0-beta.1     # Feature complete, testing
1.0.0-rc.1       # Release candidate, final testing
```

## Initial Development (0.x.x)

Before 1.0.0, anything may change at any time:
- 0.1.0 → 0.2.0 may contain breaking changes
- Use for early development before public API is stable

## Decision Tree

```
Is the change backward-compatible?
├── No → Does it remove/change existing functionality?
│        ├── Yes → MAJOR
│        └── No → Likely still MAJOR (consult team)
└── Yes → Does it add new functionality?
         ├── Yes → MINOR
         └── No → PATCH
```

## Version in Different Ecosystems

| Ecosystem | File | Field |
|-----------|------|-------|
| Node.js | package.json | `version` |
| Python | pyproject.toml / setup.py | `version` |
| Rust | Cargo.toml | `version` |
| Go | go.mod + git tags | tag format |
| Ruby | gemspec / version.rb | `version` |
| Java | pom.xml / build.gradle | `version` |

## Git Tags

Standard format: `v1.2.3`

```bash
# Create annotated tag
git tag -a v1.2.3 -m "Release version 1.2.3"

# Push tag
git push origin v1.2.3

# List tags
git tag -l "v*"
```
