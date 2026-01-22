# Example Teaching Session

This shows how a teaching session unfolds using the skill's flow.

---

## Scenario

**Document:** Phase 2 Core Infrastructure Plan (SQLite + LanceDB storage, indexing pipeline)

**Learner:** Software developer, knows Python, no experience with vector databases or RAG systems

---

## Session Transcript

### INTAKE Phase

**Teacher:** I've reviewed the Phase 2 Core Infrastructure Plan. It covers:

1. SQLite storage for metadata and full-text search (FTS5)
2. LanceDB for vector embeddings
3. An indexing pipeline to parse YAML files and populate both databases
4. Basic retrieval combining trigger matching and semantic search

Before we dive in — are there other documents I should include? For example, any related architecture docs or the YAML schema?

**Learner:** No, this should be enough.

**Teacher:** Great. I'll break this into teachable chunks. Here's our learning path:

1. Why dual storage (SQLite + vectors)?
2. SQLite fundamentals and FTS5
3. Vector embeddings and LanceDB
4. The indexing pipeline
5. Retrieval strategies (trigger vs semantic vs hybrid)

Let's start with chunk 1.

---

### Chunk 1: Why Dual Storage

**Teacher:** Before we discuss why this system uses both SQLite and a vector database, let me check your foundation.

What do you know about how traditional database search (like SQL `LIKE` or full-text search) differs from vector/semantic search?

**Learner:** SQL search looks for exact matches or patterns. I'm not sure about vector search.

**Teacher:** Good start on SQL. You've got a gap on vector search — want me to explain the basics first?

**Learner:** Yes please.

**Teacher:** *[BACKFILL: Vector Search Basics]*

Traditional search matches keywords. "How do I optimize React performance?" only finds documents containing those exact words.

Vector search works differently:
1. Text gets converted to numbers (a "vector" — like coordinates in space)
2. Similar meanings end up near each other in this space
3. Search finds documents "close" to your query, even with different words

So "How do I make my React app faster?" would match documents about "React performance optimization" — same meaning, different words.

Does that distinction click?

**Learner:** Yes — keyword matching vs meaning matching.

**Teacher:** Exactly. Now, why would you want BOTH?

*[TEACH CHUNK]*

This system uses dual storage because each excels at different things:

| Storage | Strength | Use Case |
|---------|----------|----------|
| SQLite + FTS5 | Exact phrase matching, filtering by metadata | "Show me all units about 'prompt injection'" |
| LanceDB vectors | Semantic similarity | "How do I prevent LLM attacks?" (matches prompt injection content) |

The hybrid approach gives you:
- Speed of keyword matching when queries are precise
- Flexibility of semantic matching when queries are conceptual
- Ability to filter by type, topic, confidence before searching

*[VERIFY: Architectural/Design Question]*

**Teacher:** Quick check: If a user asks "What is FTS5?" — would you expect better results from keyword search or semantic search? Why?

**Learner:** Keyword search, because "FTS5" is a specific term they're looking for exactly.

**Teacher:** Correct. And if they ask "How do I find relevant documents quickly?" — which search?

**Learner:** Semantic, because "relevant documents" could match content about retrieval, search, indexing...

**Teacher:** You've got it. Ready for chunk 2, or want to sit with this?

---

### Chunk 2: SQLite and FTS5

**Teacher:** Before we dig into the SQLite schema and FTS5, what's your experience with SQLite?

**Learner:** I've used it for small projects. Basic CRUD, some JOINs.

**Teacher:** Good foundation. Have you used full-text search in any database?

**Learner:** No.

**Teacher:** No problem — I'll cover FTS5 from scratch.

*[TEACH CHUNK]*

FTS5 (Full-Text Search 5) is SQLite's full-text search engine. Key concepts:

**Virtual table:** FTS5 creates a special table optimized for text search:
```sql
CREATE VIRTUAL TABLE triggers_fts USING fts5(
    trigger_phrase,
    tokenize='porter unicode61'
);
```

**Tokenizer:** Breaks text into searchable pieces. Porter stemmer means "running" matches "run".

**BM25 ranking:** Results ranked by relevance, not just "contains match."

**External content:** FTS5 can reference another table, so you don't duplicate data:
```sql
CREATE VIRTUAL TABLE triggers_fts USING fts5(
    trigger_phrase,
    content='triggers',  -- References the triggers table
    content_rowid='id'
);
```

The plan uses triggers (SQL triggers, not the phrase kind) to keep FTS5 synced when data changes.

*[VERIFY: Factual Quiz]*

**Teacher:** Quick quiz:

1. What does the porter tokenizer do?
   - (a) Encrypts text for security
   - (b) Stems words so "running" matches "run"
   - (c) Translates text to vectors

**Learner:** (b)

**Teacher:** Correct.

2. Why use `content='triggers'` in the FTS5 definition?
   - (a) To encrypt the trigger phrases
   - (b) To avoid duplicating data between tables
   - (c) To make searches slower but more accurate

**Learner:** (b)

**Teacher:** Two for two. Let's move on.

---

### Natural Break Point

**Teacher:** Good stopping point — we've covered the "why" and SQLite/FTS5 foundations.

You now understand:
✓ Why dual storage (keywords + semantics)
✓ How FTS5 provides full-text search in SQLite
✓ Porter stemming and BM25 ranking

Still ahead:
- Vector embeddings and LanceDB
- The indexing pipeline
- Retrieval strategies

Continue, or save progress for later?

**Learner:** Let's continue.

---

### Chunk 3: Vector Embeddings and LanceDB

**Teacher:** We covered vector search conceptually. Now let's get concrete.

Do you know what "embedding dimension" means? For example, "384-dimensional embeddings"?

**Learner:** Not really. I know vectors have dimensions but not what it means for embeddings.

**Teacher:** *[BACKFILL]*

An embedding is just a list of numbers representing text. The "dimension" is how many numbers.

- all-MiniLM-L6-v2: 384 numbers per text
- OpenAI text-embedding-3-small: 1536 numbers per text

More dimensions can capture more nuance, but:
- Use more memory
- Slower to search
- Diminishing returns

384 dimensions is a sweet spot for most use cases — fast, small, good quality.

Does that make sense?

**Learner:** Yes — it's like coordinates, and more dimensions means more precise location but more storage.

**Teacher:** Great analogy. Now for LanceDB...

*[Session continues...]*

---

## Key Patterns Demonstrated

1. **Just-in-time probing** — Asked about vector search only when chunk 1 needed it
2. **Backfill with permission** — "Want me to explain the basics first?"
3. **Varied verification** — Design question for architecture, quiz for factual content
4. **Natural break** — Offered pause after conceptual foundation was solid
5. **Adaptive tone** — Built on learner's analogy ("like coordinates")
