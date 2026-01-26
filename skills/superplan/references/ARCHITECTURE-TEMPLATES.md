# Architecture Templates

> **MANDATORY**: Use these templates when designing solutions in Phase 7.

## Architecture Decision Checklist

For EVERY architecture component, answer these questions:

### 1. High-Level Architecture (REQUIRED)

- [ ] What new components/services are being added?
- [ ] How do they connect to existing components?
- [ ] What is the data flow for the primary use case?
- [ ] What is the data flow for error cases?

---

## System Context Diagram Template

```
┌─────────────────────────────────────────────────────────────┐
│                    SYSTEM CONTEXT                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  [Existing]          [NEW]              [Existing]           │
│  ┌────────┐       ┌────────┐          ┌────────┐            │
│  │ User   │──────▶│ Feature│─────────▶│Database│            │
│  │ Client │       │ Service│          │        │            │
│  └────────┘       └────────┘          └────────┘            │
│                       │                                      │
│                       ▼                                      │
│                  ┌────────┐                                  │
│                  │ [NEW]  │                                  │
│                  │ Cache  │                                  │
│                  └────────┘                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## API Endpoint Template

For EACH endpoint, specify ALL of these:

```markdown
### POST /api/v1/[resource]

**Auth:** Bearer token required | None | API key

**Request:**
\`\`\`json
{
  "field1": "string (required, max 255 chars)",
  "field2": "number (optional, default: 0)",
  "field3": {
    "nested": "object structure"
  }
}
\`\`\`

**Response 201 Created:**
\`\`\`json
{
  "id": "uuid",
  "field1": "string",
  "createdAt": "2025-01-21T00:00:00Z"
}
\`\`\`

**Response 400 Bad Request:**
\`\`\`json
{
  "error": "VALIDATION_ERROR",
  "message": "field1 is required",
  "details": [{"field": "field1", "message": "Required"}]
}
\`\`\`

**Response 401 Unauthorized:**
\`\`\`json
{
  "error": "UNAUTHORIZED",
  "message": "Invalid or expired token"
}
\`\`\`

**Response 403 Forbidden:**
\`\`\`json
{
  "error": "FORBIDDEN",
  "message": "Insufficient permissions"
}
\`\`\`

**Response 404 Not Found:**
\`\`\`json
{
  "error": "NOT_FOUND",
  "message": "[Resource] not found"
}
\`\`\`

**Response 500 Internal Server Error:**
\`\`\`json
{
  "error": "INTERNAL_ERROR",
  "message": "An unexpected error occurred"
}
\`\`\`
```

---

## Data Model Template

Specify ALL of these for schema changes:

```sql
-- Migration UP
-- Description: [What this migration does]
-- Date: [YYYY-MM-DD]

CREATE TABLE feature_table (
  -- Primary key
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Foreign keys
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

  -- Required fields
  field1 VARCHAR(255) NOT NULL,
  status VARCHAR(50) NOT NULL DEFAULT 'pending',

  -- Optional fields
  field2 INTEGER,
  metadata JSONB,

  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for common queries
CREATE INDEX idx_feature_user ON feature_table(user_id);
CREATE INDEX idx_feature_status ON feature_table(status);
CREATE INDEX idx_feature_created ON feature_table(created_at DESC);

-- Trigger for updated_at
CREATE TRIGGER update_feature_updated_at
  BEFORE UPDATE ON feature_table
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Migration DOWN
DROP TRIGGER IF EXISTS update_feature_updated_at ON feature_table;
DROP TABLE IF EXISTS feature_table;
```

### Schema Checklist

- [ ] All columns have types and constraints
- [ ] Foreign keys have ON DELETE behavior
- [ ] Required indexes for query patterns
- [ ] Timestamps for auditing
- [ ] Migration DOWN script works

---

## Component Tree Template

For UI features, document the component hierarchy:

```
FeaturePage
├── FeatureHeader
│   ├── props: { title: string, onBack: () => void }
│   └── state: none (stateless)
│
├── FeatureForm
│   ├── props: { onSubmit: (data) => Promise, initialData?: Data }
│   ├── state: { formData, errors, isSubmitting }
│   └── children:
│       ├── FormField (×N)
│       │   └── props: { name, type, validation, error }
│       └── SubmitButton
│           └── props: { loading, disabled, label }
│
└── FeatureList
    ├── props: { items: Item[], onSelect: (id) => void }
    ├── state: { selectedId }
    └── children:
        └── FeatureItem (×N)
            └── props: { item, selected, onClick }
```

### Component Checklist

- [ ] Props interface defined for each component
- [ ] State location decided (local vs global)
- [ ] Event flow documented (who calls what)
- [ ] Loading/error states planned

---

## Data Flow Diagram Template

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA FLOW: [Operation Name]               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. User Action (click, submit, navigate)                    │
│     │                                                        │
│     ▼                                                        │
│  ┌──────────────────┐                                       │
│  │ Validate Input   │ ──── Invalid ───▶ Show Error          │
│  └────────┬─────────┘                                       │
│           │ Valid                                            │
│           ▼                                                  │
│  ┌──────────────────┐                                       │
│  │ Call API         │                                       │
│  └────────┬─────────┘                                       │
│           │                                                  │
│      ┌────┴────┐                                            │
│      │         │                                             │
│   Success    Failure                                         │
│      │         │                                             │
│      ▼         ▼                                             │
│  ┌───────┐ ┌───────────┐                                    │
│  │Update │ │Show Error │                                    │
│  │ State │ │ + Retry?  │                                    │
│  └───┬───┘ └───────────┘                                    │
│      │                                                       │
│      ▼                                                       │
│  ┌──────────────────┐                                       │
│  │ Update UI        │                                       │
│  └──────────────────┘                                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```
