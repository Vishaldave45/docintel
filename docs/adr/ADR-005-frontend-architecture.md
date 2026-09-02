# ADR-005: Frontend Architecture & Physical Ledger Design Metaphor

- **Status:** Accepted
- **Date:** 2026-09-01
- **Deciders:** DocIntel Platform Architecture Team & Lead Designer

## Context & Problem Statement
DocIntel is used by operations, finance, and legal teams who handle paperwork, ledgers, stamps, and physical filing cabinets daily. Typical SaaS AI templates (monotonous rounded cards with gradient drop-shadows, cream-and-terracotta cliches, and all-caps tracked-out eyebrows) look generic, ungrounded, and fail to convey the physical gravitas of document workflows.

## Design Decisions

### 1. Concrete 5-Tone Archival Palette
- **Base / Paper (`#F7F5F0`):** Warm off-white evocative of uncoated archival rag stock.
- **Ink (`#211F1C`):** Deep charcoal warm black for crisp, high-contrast typography.
- **Ledger Blue (`#2B3A55`):** Deep desaturated indigo for navigation, active states, and archival ink stamps.
- **Stamp Red (`#B33A2E`):** Muted rubber-stamp red reserved exclusively for real flags ("needs review", failed validation, error markers).
- **Brass / Olive (`#8A7B4F`):** Muted olive-brass for structural index tab dividers, hairline rules, and document classification markers.

### 2. Typographic Hierarchy
- **Display / Headers:** `Zilla Slab` (slab serif with physical ledger character and tight tracking).
- **Body & Controls:** `IBM Plex Sans` (clean, humanist, official document feel).
- **Technical Values Only:** `IBM Plex Mono` (strictly for document IDs, SHA-256 hashes, raw OCR confidence numbers).

### 3. Layout: The Physical Filing / Index Card Metaphor
- Flat rectangular index cards with top-left category notches (`INV`, `CTR`, `REP`, `ID`, `REC`).
- Hairline ledger divider rules (`border-[#8A7B4F]/20`) separating metadata from OCR preview.
- RAG Q&A layout featuring a 2-column view where source citations appear as marginal annotations tied to exact line numbers and page coordinates.

### 4. State Management & API Layer
- **Client State:** Lightweight React state + typed stores for active document inspection and RAG queries.
- **Server State & Typed Contracts:** Fully typed OpenAPI contracts matching FastAPI v1 schemas with zero hand-written duplicate types.

## Consequences
- **Positive:** Instantly recognizable identity, high task efficiency for professional document handlers, clear visual distinction between valid extractions and flagged items.
- **Negative:** Requires custom utility styling rather than standard off-the-shelf component themes.
