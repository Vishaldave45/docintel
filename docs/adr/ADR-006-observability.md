# ADR-006: Observability, Structured Logging, and Metrics

- **Status:** Accepted
- **Date:** 2026-09-01
- **Deciders:** DocIntel Platform Architecture Team

## Context & Problem Statement
Multimodal processing pipelines involve diverse failure points: corrupted PDF encodings, OCR layout segmentation misses, low classifier confidence, LLM rate limits, schema validation errors, and vector index drifts. Bolting on logging as an afterthought creates opaque production debugging.

## Decision Drivers
- **Traceability:** Every document ingestion generates a unique `trace_id` propagated across OCR, classification, extraction, and vector indexing.
- **Structured JSON Logging:** Standardized key-value structured logging via `structlog` for easy ingestion into OpenSearch / Datadog / CloudWatch.
- **Real-Time Telemetry:** Metrics covering OCR duration, classification latency, LLM token counts, repair loop frequencies, and retrieval cosine similarities.

## Implementation Standard
1. **Correlation IDs:** FastAPI middleware injects `X-Request-ID` and binds it to the `structlog` contextvars logger.
2. **Standard Log Event Schema:**
   ```json
   {
     "timestamp": "2026-09-01T22:00:00Z",
     "level": "info",
     "event": "document_extracted",
     "trace_id": "req-89a1c2",
     "document_id": "doc-4471",
     "document_type": "invoice",
     "ocr_blocks_count": 28,
     "classifier_confidence": 0.962,
     "extraction_latency_ms": 412,
     "repair_attempts": 0,
     "is_valid": true
   }
   ```
3. **Metrics Endpoint:** `/api/v1/system/metrics` exposes aggregated operational health, processing queue counts, and domain performance summaries.

## Consequences
- **Positive:** Complete visibility across complex multi-step pipelines, fast root-cause isolation.
- **Negative:** Minor performance overhead in logging serialization, handled via asynchronous logging sinks.
