# ResearchRAG Evaluation

## Overview

ResearchRAG uses a multi-stage retrieval and generation architecture.

The evaluation framework measures both retrieval quality and
answer-generation quality.

## Retrieval Strategies

The following retrieval strategies are evaluated:

1. Semantic retrieval
2. BM25 lexical retrieval
3. Hybrid retrieval using Reciprocal Rank Fusion
4. Hybrid retrieval with cross-encoder reranking

## Retrieval Metrics

### Recall@K

Measures whether relevant chunks appear within the first K
retrieved results.

### Mean Reciprocal Rank

Measures how early the first relevant result appears.

### nDCG@K

Measures ranking quality while giving greater importance to
higher-ranked relevant documents.

## Generation Metrics

ResearchRAG currently includes:

- Answer/reference keyword overlap
- Answer relevance
- Lexical faithfulness baseline

The lexical faithfulness metric should not be interpreted as
proof of factual correctness.

An additional LLM-as-a-judge evaluator is provided using the
configured Ollama model.

## Latency

The evaluation framework supports:

- Average latency
- P95 latency
- Minimum latency
- Maximum latency

Python's `time.perf_counter()` is used for timing.

## Evaluation Dataset

The evaluation dataset contains:

- User question
- Relevant chunk IDs
- Reference answer

The example dataset must be replaced or expanded with questions
and ground-truth chunk IDs from the actual indexed research corpus.

## Running Evaluation

From the project root:

```powershell
python scripts/evaluate.py