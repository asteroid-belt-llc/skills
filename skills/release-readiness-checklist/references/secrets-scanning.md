# Secrets Scanning Guide

Detect and remediate accidentally exposed secrets in version control.

## Table of Contents

- [Why This Matters](#why-this-matters)
- [Scanning Tools](#scanning-tools)
- [Quick Scans](#quick-scans)
- [Full History Scan](#full-history-scan)
- [Remediation](#remediation)
- [Prevention](#prevention)

---

## Why This Matters

Secrets committed to git remain in history even after deletion. Attackers scan public repositories for:

- API keys and tokens
- Database credentials
- Private keys (SSH, TLS, signing)
- Cloud provider credentials (AWS, GCP, Azure)
- OAuth client secrets
- Webhook URLs with embedded tokens

A single exposed secret can compromise entire systems.

---

## Scanning Tools

### Recommended Tools

| Tool | Best For | Install |
| ---- | -------- | ------- |
| gitleaks | Fast, comprehensive | `brew install gitleaks` |
| trufflehog | Deep history scan, entropy detection | `brew install trufflehog` |
| git-secrets | AWS-focused, pre-commit hooks | `brew install git-secrets` |

### GitHub Native

- **Secret scanning**: Automatically enabled for public repos
- **Push protection**: Blocks commits containing known secret patterns
- Check: Repository Settings → Security → Secret scanning

---

## Quick Scans

### Using gitleaks (recommended)

Scan current state:

```bash
gitleaks detect --source . --no-git
```

Scan with verbose output:

```bash
gitleaks detect --source . -v
```

### Using trufflehog

Scan filesystem:

```bash
trufflehog filesystem .
```

### Manual grep patterns

Quick check for common patterns:

```bash
# API keys (generic patterns)
grep -rn "api[_-]key\|apikey" --include="*.{js,ts,py,json,yaml,yml,env}" .

# AWS credentials
grep -rn "AKIA[0-9A-Z]{16}" .

# Private keys
grep -rn "BEGIN RSA PRIVATE KEY\|BEGIN OPENSSH PRIVATE KEY" .

# Connection strings
grep -rn "mongodb://\|postgres://\|mysql://" .
```

---

## Full History Scan

Scanning only current files misses secrets that were committed and later deleted.

### Using gitleaks

Scan entire git history:

```bash
gitleaks detect --source . --log-opts="--all"
```

Scan specific branch:

```bash
gitleaks detect --source . --log-opts="main"
```

### Using trufflehog

Scan git history:

```bash
trufflehog git file://. --since-commit HEAD~100
```

Full repository scan:

```bash
trufflehog git file://. --only-verified
```

### Output to file for review

```bash
gitleaks detect --source . --log-opts="--all" --report-format json --report-path secrets-report.json
```

---

## Remediation

### If secrets are found

1. **Rotate immediately** - Assume the secret is compromised
   - Generate new API keys/tokens
   - Change passwords
   - Revoke and reissue certificates

2. **Remove from history** (if not yet pushed publicly)

   Using git-filter-repo (recommended):

   ```bash
   # Install: pip install git-filter-repo
   git filter-repo --invert-paths --path path/to/secret-file
   ```

   Using BFG Repo-Cleaner:

   ```bash
   # Install: brew install bfg
   bfg --delete-files secret-file.txt
   bfg --replace-text passwords.txt
   git reflog expire --expire=now --all && git gc --prune=now --aggressive
   ```

3. **Force push** (coordinate with team)

   ```bash
   git push --force-with-lease
   ```

4. **Notify affected parties** if secret was exposed publicly

### If already in public history

- Rotation is the only safe option
- Git history rewriting won't help - assume it's been cloned/cached

---

## Prevention

### Pre-commit hooks

Using gitleaks:

```bash
# Install hook
gitleaks protect --staged
```

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
```

Using git-secrets:

```bash
git secrets --install
git secrets --register-aws
```

### .gitignore essentials

```gitignore
# Environment files
.env
.env.*
*.env

# Credentials
credentials.json
secrets.yaml
**/secrets/**

# Keys
*.pem
*.key
id_rsa*
*.p12

# Cloud configs
.aws/credentials
.gcp/credentials.json
```

### Environment variable patterns

Store secrets in environment, not code:

```bash
# Good: Reference environment variable
DATABASE_URL="${DATABASE_URL}"

# Bad: Hardcoded value
DATABASE_URL="postgres://user:password@host/db"
```

### CI/CD integration

Add to GitHub Actions:

```yaml
- name: Scan for secrets
  uses: gitleaks/gitleaks-action@v2
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## Checklist Summary

Before release, verify:

- [ ] Ran `gitleaks detect --source . --log-opts="--all"` with no findings
- [ ] Checked for secrets in git history, not just current files
- [ ] Verified `.gitignore` excludes sensitive file patterns
- [ ] Pre-commit hooks installed and working
- [ ] Any previously exposed secrets have been rotated
