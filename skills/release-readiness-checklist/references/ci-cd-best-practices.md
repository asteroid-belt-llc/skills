# CI/CD Pipeline Best Practices

Configuration best practices for GitHub Actions and GitLab CI pipelines.

## Table of Contents

- [Detecting Pipeline Type](#detecting-pipeline-type)
- [GitHub Actions Best Practices](#github-actions-best-practices)
- [GitLab CI Best Practices](#gitlab-ci-best-practices)
- [Common Anti-patterns](#common-anti-patterns)
- [Pre-release Pipeline Checklist](#pre-release-pipeline-checklist)

---

## Detecting Pipeline Type

Check which CI system the project uses:

```bash
# GitHub Actions
ls -la .github/workflows/

# GitLab CI
ls -la .gitlab-ci.yml
```

---

## GitHub Actions Best Practices

### Security

**Pin action versions to full SHA** (not tags):

```yaml
# Good - pinned to SHA
- uses: actions/checkout@8ade135a41bc03ea155e62e844d188df1ea18608  # v4.1.0

# Acceptable - pinned to major version
- uses: actions/checkout@v4

# Bad - unpinned or mutable tag
- uses: actions/checkout@main
```

**Use minimal permissions**:

```yaml
permissions:
  contents: read
  pull-requests: write  # Only if needed
```

**Use environment protection rules** for production deployments:

```yaml
jobs:
  deploy-prod:
    environment:
      name: production
      url: https://example.com
```

**Avoid storing secrets in code** - use GitHub Secrets:

```yaml
env:
  API_KEY: ${{ secrets.API_KEY }}
```

### Performance

**Cache dependencies**:

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

**Use matrix builds** for multi-version testing:

```yaml
strategy:
  matrix:
    node-version: [18, 20, 22]
    os: [ubuntu-latest, macos-latest]
```

**Run jobs in parallel** when independent:

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
  test:
    runs-on: ubuntu-latest
  # lint and test run in parallel
  deploy:
    needs: [lint, test]  # waits for both
```

### Reliability

**Set timeouts** to prevent hung jobs:

```yaml
jobs:
  build:
    timeout-minutes: 30
```

**Use `fail-fast: false`** when debugging matrix builds:

```yaml
strategy:
  fail-fast: false
  matrix:
    node-version: [18, 20]
```

**Add concurrency controls** to prevent duplicate runs:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

### Workflow Organization

**Use reusable workflows** for shared logic:

```yaml
# .github/workflows/reusable-test.yml
on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string

# .github/workflows/ci.yml
jobs:
  test:
    uses: ./.github/workflows/reusable-test.yml
    with:
      node-version: '20'
```

**Separate CI and CD workflows**:

```
.github/workflows/
├── ci.yml          # Runs on all PRs
├── release.yml     # Runs on tags/releases
└── deploy.yml      # Deployment workflow
```

---

## GitLab CI Best Practices

### Security

**Use protected variables** for secrets:

```yaml
deploy:
  script:
    - echo "$DEPLOY_TOKEN"  # Set in CI/CD Settings > Variables
  only:
    - main
```

**Restrict jobs to protected branches**:

```yaml
deploy-production:
  script:
    - ./deploy.sh
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual
```

**Use environment-specific variables**:

```yaml
deploy:
  environment:
    name: production
  variables:
    DATABASE_URL: $PROD_DATABASE_URL
```

### Performance

**Cache dependencies**:

```yaml
variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip/
    - node_modules/
  key:
    files:
      - package-lock.json
      - requirements.txt
```

**Use DAG (needs) for parallel execution**:

```yaml
stages:
  - build
  - test
  - deploy

build:
  stage: build

lint:
  stage: test
  needs: []  # Runs immediately, doesn't wait for build

unit-test:
  stage: test
  needs: [build]

deploy:
  stage: deploy
  needs: [lint, unit-test]
```

**Use rules instead of only/except**:

```yaml
# Good - rules
job:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == "main"

# Avoid - only/except (deprecated)
job:
  only:
    - main
```

### Reliability

**Set job timeouts**:

```yaml
build:
  timeout: 30 minutes
  script:
    - make build
```

**Use `interruptible` for cancellable jobs**:

```yaml
test:
  interruptible: true
  script:
    - make test
```

**Add retry for flaky external dependencies**:

```yaml
deploy:
  retry:
    max: 2
    when:
      - runner_system_failure
      - stuck_or_timeout_failure
```

### Pipeline Organization

**Use includes for shared config**:

```yaml
# .gitlab-ci.yml
include:
  - local: '.gitlab/ci/test.yml'
  - local: '.gitlab/ci/deploy.yml'
  - template: Security/SAST.gitlab-ci.yml
```

**Use extends for job templates**:

```yaml
.test-template:
  image: node:20
  before_script:
    - npm ci
  cache:
    paths:
      - node_modules/

unit-test:
  extends: .test-template
  script:
    - npm test

integration-test:
  extends: .test-template
  script:
    - npm run test:integration
```

**Use stages logically**:

```yaml
stages:
  - validate    # Lint, type check
  - build       # Compile, bundle
  - test        # Unit, integration tests
  - security    # SAST, dependency scanning
  - deploy      # Staging, production
```

---

## Common Anti-patterns

### Both Platforms

| Anti-pattern | Problem | Fix |
| ------------ | ------- | --- |
| Hardcoded secrets | Security risk | Use secrets/variables |
| No caching | Slow builds | Cache dependencies |
| Sequential independent jobs | Wasted time | Run in parallel |
| No timeouts | Hung jobs | Set reasonable limits |
| Running everything on every commit | Resource waste | Use path filters |

### Path Filtering Example

**GitHub Actions**:

```yaml
on:
  push:
    paths:
      - 'src/**'
      - 'package.json'
    paths-ignore:
      - '**.md'
      - 'docs/**'
```

**GitLab CI**:

```yaml
build:
  rules:
    - changes:
        - src/**/*
        - package.json
```

---

## Pre-release Pipeline Checklist

Before release, verify the pipeline:

- [ ] **Security**
  - [ ] Action versions pinned (GitHub) or images pinned (GitLab)
  - [ ] Secrets stored in CI/CD settings, not in code
  - [ ] Minimal permissions configured
  - [ ] Protected branch rules enabled for production

- [ ] **Performance**
  - [ ] Dependency caching configured
  - [ ] Independent jobs run in parallel
  - [ ] Path filters exclude irrelevant changes

- [ ] **Reliability**
  - [ ] Job timeouts set
  - [ ] Concurrency controls prevent duplicate runs
  - [ ] Retry configured for external dependencies

- [ ] **Release-specific**
  - [ ] Release workflow triggered by tags/releases
  - [ ] Staging deployment tested before production
  - [ ] Manual approval gate for production deployment
  - [ ] Rollback procedure documented
