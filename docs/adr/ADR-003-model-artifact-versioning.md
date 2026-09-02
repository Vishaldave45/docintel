# ADR-003: Model Artifact Versioning and Hot-Reload Registry

- **Status:** Accepted
- **Date:** 2026-09-01
- **Deciders:** DocIntel Platform Architecture Team

## Context & Problem Statement
DocIntel relies on two primary stateful ML artifacts:
1. **Document Classifier**: A Scikit-Learn pipeline (TF-IDF vectorizer + CalibratedClassifierCV/LogisticRegression).
2. **Vector Index**: A FAISS dense embedding index with Hugging Face sentence-transformer mappings.

Storing unversioned `.pkl` or `.faiss` binaries directly in the repository root causes reproducibility failures, prevents zero-downtime hot reloading, and breaks model rollback capabilities.

## Architecture: Model Artifact Registry Pattern
```
[Artifact Registry Storage: local / S3 / GCS]
  └── artifacts/
      ├── classification/
      │   ├── v1.2.0/
      │   │   ├── pipeline.joblib
      │   │   ├── metadata.json (metrics, classes, feature_names, date)
      │   │   └── checksum.sha256
      │   └── current -> v1.2.0 (symlink / registry pointer)
      └── retrieval/
          ├── faiss_index_v2.bin
          └── corpus_manifest.json
```

## Hot-Reloading Mechanism
- An in-memory **`ModelRegistry`** singleton manages thread-safe pointers (using `asyncio.Lock` / `threading.RLock`) to the active classifier and FAISS index.
- Healthcheck and model status endpoints (`/api/v1/system/models`) expose the loaded artifact version, SHA-256 hash, and training timestamp.
- On background retraining or artifact promotion, the registry downloads, verifies SHA-256 checksums, loads the candidate into a shadow instance, runs a synthetic sanity probe, and atomically swaps the pointer.

## Retraining Path
- Documented CLI training script in `ml/classification/train.py` ingests labeled corpus, performs stratified 5-fold cross-validation, generates classification reports (precision, recall, F1 per class), and exports a versioned bundle containing `pipeline.joblib` and `metadata.json`.

## Consequences
- **Positive:** Zero-downtime model upgrades, deterministic lineage, instant rollbacks, protection against corrupted pickled files via SHA-256 verification.
- **Negative:** Requires strict metadata schema discipline.
