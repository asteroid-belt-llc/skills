# Verification Examples by Content Type

Detailed examples of verification questions for different types of technical content.

---

## Conceptual Content (Theory, Mental Models)

**Verification method:** Explain-back

**Goal:** Confirm learner can articulate the concept in their own words, not just recognize it.

### Examples

**Topic:** Why RAG systems use retrieval + generation

> "In your own words, why can't we just use a larger context window instead of retrieval?"

**Good answer signals:**
- Mentions cost/latency of large contexts
- Notes retrieval can access unlimited knowledge
- Understands context windows have limits

**Topic:** CAP theorem trade-offs

> "Explain to me like I'm a colleague: why can't a distributed database have all three of consistency, availability, and partition tolerance?"

**Good answer signals:**
- Can give concrete scenario (network split)
- Explains the forced choice
- Doesn't just recite the theorem

**Topic:** Eventual consistency

> "A junior developer asks why their read returned stale data. How would you explain what happened?"

---

## Procedural Content (How-to, Workflows)

**Verification method:** Applied exercise

**Goal:** Confirm learner can apply the steps to a new situation.

### Examples

**Topic:** Setting up a Python project with uv

> "You're starting a new CLI tool project. Walk me through the first 5 commands you'd run."

**Good answer signals:**
- `uv init --package`
- Creates src/ layout
- Adds dependencies
- Runs `uv sync`
- Knows to check with `uv run pytest`

**Topic:** Git rebase workflow

> "Your feature branch is 10 commits behind main and has 3 commits of your own. Describe how you'd update it."

**Topic:** Debugging a failing test

> "A test passes locally but fails in CI. What's your systematic approach to diagnose this?"

---

## Factual Content (Definitions, Specs, Numbers)

**Verification method:** Quick quiz (multiple choice or fill-in)

**Goal:** Confirm accurate recall of specific facts.

### Examples

**Topic:** Embedding model dimensions

> "What's the embedding dimension of all-MiniLM-L6-v2?
> (a) 128  (b) 384  (c) 768  (d) 1536"

**Topic:** SQLite FTS5 tokenizers

> "Which tokenizer would you use if you want 'running' to match 'run'?
> (a) unicode61  (b) porter  (c) trigram  (d) ascii"

**Topic:** HTTP status codes

> "A client sends malformed JSON. What status code should your API return?
> (a) 400  (b) 404  (c) 500  (d) 422"

**Topic:** Fill-in-the-blank

> "LanceDB stores vectors in a columnar format called ______ for efficient similarity search."

---

## Architectural Content (Systems, Trade-offs)

**Verification method:** Design question

**Goal:** Confirm learner can reason about trade-offs and make justified decisions.

### Examples

**Topic:** Choosing storage strategy

> "Your knowledge base grows from 1,000 to 1,000,000 documents. What changes would you make to the current SQLite + LanceDB architecture?"

**Good answer signals:**
- Considers sharding or distributed storage
- Thinks about indexing time
- Mentions potential move to dedicated vector DB
- Weighs operational complexity

**Topic:** Caching decisions

> "Users complain search is slow. Where would you add caching, and what are the trade-offs of each option?"

**Topic:** API design

> "Should the search endpoint return full document content or just IDs? Argue both sides, then pick one."

**Topic:** Failure modes

> "The embedding service is down. How should the system behave? What are your options?"

---

## Code-Heavy Content

**Verification method:** Code task

**Goal:** Confirm learner can write working code using the pattern.

### Examples

**Topic:** Pydantic model validation

> "Write a Pydantic model for a BlogPost with: title (required, 5-100 chars), content (required), tags (optional list), published_at (optional datetime)."

**Topic:** SQLite context manager

> "Write a context manager that handles SQLite connections with proper cleanup on exceptions."

**Topic:** Async patterns

> "Convert this synchronous function to async, handling the case where the API call might timeout."

**Topic:** Testing patterns

> "Write a pytest fixture that creates a temporary SQLite database with the schema we discussed."

---

## Combination Scenarios

Some content needs multiple verification types.

### Example: Teaching a complete feature

**Content:** Implementing FTS5 search in the codebase

**Verification sequence:**

1. **Factual:** "What's the SQL to create an FTS5 virtual table with porter stemming?"

2. **Conceptual:** "Why do we use `content='triggers'` instead of storing text directly in the FTS table?"

3. **Code task:** "Write the Python function that searches triggers and returns (unit_id, score) tuples."

4. **Architectural:** "A user searches for 'authentication' but wants results about 'auth', 'login', and 'signin' too. How would you improve the search?"

---

## Signs Verification Is Working

**Learner understands:**
- Answers correctly on first try
- Can explain reasoning, not just give answer
- Asks clarifying questions that show engagement
- Makes connections to previous chunks

**Learner needs more help:**
- Wrong answer
- Right answer but can't explain why
- Hesitant, qualified answers ("I think maybe...")
- Asking to see the content again

**Learner is confused (pivot to foundations):**
- Repeatedly wrong despite rephrasing
- Answers unrelated to question
- "I have no idea"
- Frustration signals

---

## Verification Anti-Patterns

**Avoid these:**

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| "Does that make sense?" | Invites false "yes" | "Explain back to me..." |
| "Any questions?" | Puts burden on confused learner | Verify actively |
| "Got it?" | Binary, no depth check | Quiz or explain-back |
| Asking exact same words from content | Tests recognition, not understanding | Rephrase or apply |
| Long multi-part questions | Cognitive overload | One question at a time |
| Gotcha questions | Damages trust | Fair assessment of what was taught |
