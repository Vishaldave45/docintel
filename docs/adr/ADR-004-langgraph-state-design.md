# ADR-004: LangGraph State Graph Design for Type-Conditioned Extraction

- **Status:** Accepted
- **Date:** 2026-09-01
- **Deciders:** DocIntel Platform Architecture Team

## Context & Problem Statement
Direct one-shot prompting of LLMs for complex document field extraction (multi-page invoices, legal contracts with liability caps, government IDs) often generates invalid schema types, hallucinated keys, or silent omission of required fields. We need a deterministic, observable agentic state graph with schema validation and repair loops.

## State Graph Specification

### Graph State Schema (`ExtractionGraphState`)
```python
class ExtractionGraphState(TypedDict):
    document_id: str
    document_type: str  # invoice | contract | financial_report | identification | receipt
    raw_ocr_text: str
    layout_blocks: list[dict]
    target_schema_name: str
    extracted_data: dict[str, Any] | None
    validation_errors: list[str]
    repair_attempts: int
    max_repair_attempts: int
    is_valid: bool
    confidence_scores: dict[str, float]
    execution_trace: list[dict]
```

### Graph Topology
```
                  [Start]
                     │
                     ▼
          [select_schema_node]
                     │
                     ▼
         [route_by_type_conditional]
         ┌───────────┼───────────┐
         ▼           ▼           ▼
   [invoice_agent] [contract_agent] [id_agent]
         └───────────┬───────────┘
                     │
                     ▼
          [validate_schema_node]
                     │
         [is_valid_conditional]
             ┌───────┴───────┐
             │ (Valid)       │ (Invalid & attempts < max)
             ▼               ▼
          [End]       [repair_agent_node]
                             │
                             └────► (back to validate_schema_node)
```

## Failure & Retry Handling
- When schema validation fails (e.g. invalid date format, missing total amount, impossible date ranges), errors are structured into a typed error list.
- The `repair_agent_node` receives the previous attempt + exact Pydantic validation errors + original OCR layout text, instructing the model to repair only the invalid fields.
- If `repair_attempts >= max_repair_attempts` (default 2), the graph transitions to `End` with `is_valid = False` and status flagged as `"needs_review"`. Exceptions are never silently swallowed.

## Consequences
- **Positive:** High extraction accuracy, predictable output schemas, clear provenance of repairs, observable node latency.
- **Negative:** Multiple LLM calls for edge-case documents with damaged OCR. Bounded by `max_repair_attempts`.
