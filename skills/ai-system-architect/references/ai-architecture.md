# AI Architecture

Read this whenever AI is genuinely in scope — either the whole system is AI-centric (AI System mode) or an AI component sits inside a larger system. The goal here is the same as everywhere else in this skill: justify each AI-specific piece of architecture against a real requirement rather than adding it because the system happens to touch an LLM.

## General AI system shape

```
User → Application → AI Orchestrator → Model → Tools → Knowledge/RAG → External Systems
```

Components to consider including, only as far as the project needs them: LLM, model gateway, prompt layer, agent/orchestrator, tool layer, MCP, RAG pipeline, embeddings, vector store, reranker, guardrails, evaluation system, human-approval step, observability.

## Model selection

Don't default to the largest or newest model. Evaluate against: reasoning requirements, latency budget, cost per request/token, context length needed, structured-output support, tool-use requirements, data privacy constraints, availability/reliability of the provider, and accuracy bar for the use case.

Because model and vendor offerings change quickly, mark any specific model recommendation as time-sensitive in the document rather than presenting it as a permanent architectural fact — the *criteria* for model selection are durable; the specific model that best satisfies them today is not.

## RAG architecture

When retrieval-augmented generation is actually justified by a need to ground responses in a knowledge base the model wasn't trained on:

```
Data source → Ingestion → Parsing → Chunking → Embedding → Vector store
→ Retrieval → Reranking → Context construction → LLM → Response
```

Analyze: source freshness requirements, metadata needed for filtering, access control (can retrieval leak data a given user shouldn't see), retrieval quality strategy, citation requirements, indexing strategy, and how the index stays updated as the source changes.

## Agent architecture

When the system needs autonomous multi-step reasoning and tool use (justify this against a real need for that autonomy, not just "the system uses an LLM"):

```
Agent goal → Planner/Reasoner → Tools → Memory/State → Knowledge → Execution
→ Validation → Human approval where necessary
```

Specify: tool permissions (what the agent is and isn't allowed to do), state and memory model, guardrails, termination conditions (how the agent knows to stop), retry behavior, and where a human approval gate belongs in the loop. Avoid multi-agent architectures unless the problem genuinely decomposes into cooperating specialized roles — a single well-tooled agent handles most cases that don't have a structural reason for more.

## AI evaluation

For any AI system in scope, define how quality will be measured: correctness, hallucination rate, tool-use accuracy, retrieval quality (for RAG), latency, cost, safety, and a plan for regression testing as prompts/models/data change over time. An AI architecture without an evaluation plan has no way to know if a later change made things worse.
