"""Scikit-Learn Document Classification Pipeline Training Script.

Trains a TF-IDF Vectorizer + Calibrated Logistic Regression model on labeled document samples.
Exports versioned model artifact (joblib) and metadata JSON with cross-validation metrics.
"""

import json
import os
import hashlib
from datetime import datetime, timezone
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import classification_report
import joblib

DATASET = [
    # Invoices
    {"text": "INVOICE #4471 Acme Corp Bill To: Kestrel Due Date: 2026-09-28 Total Amount Due: $14,250.00 Net 30", "label": "invoice"},
    {"text": "Tax Invoice Vendor: Global Logistics Remit Payment to: Bank of America Subtotal: $1,200 Tax: $120 Total: $1,320", "label": "invoice"},
    {"text": "Commercial Invoice PO-9921 Quantity 5 Units Unit Price $300 Balance Due $1,500 Terms: Net 15", "label": "invoice"},
    {"text": "BILLING STATEMENT Account #8812 Previous Balance $0.00 New Charges: $450.00 Due Upon Receipt", "label": "invoice"},

    # Contracts
    {"text": "MASTER SERVICES AGREEMENT by and between Client and Vendor. Term: 2 years. Confidentiality and Indemnification.", "label": "contract"},
    {"text": "NON-DISCLOSURE AGREEMENT (NDA). Disclosing Party and Receiving Party agree to hold confidential information in strict trust.", "label": "contract"},
    {"text": "Employment Agreement. Compensation: $160,000 per annum. Termination notice period: 30 days. Governing law: Delaware.", "label": "contract"},
    {"text": "Software License Agreement. Grant of License, Limitation of Liability, Warranty Disclaimer, and Governing Law.", "label": "contract"},

    # Financial Reports
    {"text": "Quarterly Financial Report Q3 2026. Consolidated Balance Sheet. Net Income: $7.45M. Operating Revenue: $48.2M. EBITDA: $11.2M.", "label": "financial_report"},
    {"text": "Annual Report 2025. Assets: $140M, Liabilities: $65M. Cash Flow from Operations grew by 14% year-over-year.", "label": "financial_report"},
    {"text": "Shareholder Letter & Earnings Release. Diluted Earnings Per Share (EPS) $1.42 vs $1.10 guidance.", "label": "financial_report"},
    {"text": "Audit Committee Statement. Consolidated Income Statement, Statements of Cash Flows and Stockholders Equity.", "label": "financial_report"},

    # Identification
    {"text": "PASSPORT United States of America. Name: Holloway Elizabeth Jane. DOB: 14 APR 1992. Sex: F. Exp: 13 APR 2032.", "label": "identification"},
    {"text": "DRIVER LICENSE State of California. DL Number: D8819201. Class C. Expires: 05/12/2029. Height: 5-08 Eyes: BRN.", "label": "identification"},
    {"text": "NATIONAL IDENTITY CARD. Republic of France. Surname: Dubois. Given Names: Jean-Pierre. Nationality: FRA.", "label": "identification"},

    # Receipts
    {"text": "Store Receipt #9102. Cashier: Dave. 1x Office Supplies $42.50. Subtotal $42.50. Tax $3.40. VISA *4491 Approved.", "label": "receipt"},
    {"text": "Supermarket Receipt. Total Items Sold: 14. Total Due: $88.19. Change Due: $0.00. Thank you for shopping with us.", "label": "receipt"},
    {"text": "Fuel Station Express. Pump #4 Regular Unleaded $55.00. Tax Included. Payment Method: Contactless Chip.", "label": "receipt"},
]


def train_and_export(output_dir: str = "ml/artifacts/classification/v1.2.0") -> None:
    """Train pipeline and export serialized artifact."""
    os.makedirs(output_dir, exist_ok=True)

    texts = [item["text"] for item in DATASET]
    labels = [item["label"] for item in DATASET]
    classes = sorted(list(set(labels)))

    print(f"Training on {len(texts)} samples across {len(classes)} classes: {classes}")

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)),
        ("clf", LogisticRegression(C=1.0, max_iter=200, class_weight="balanced")),
    ])

    # 3-Fold Stratified Cross Validation
    cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    scores = cross_val_score(pipeline, texts, labels, cv=cv, scoring="accuracy")
    print(f"Stratified CV Accuracy: {scores.mean():.4f} (+/- {scores.std():.4f})")

    # Fit full pipeline
    pipeline.fit(texts, labels)
    preds = pipeline.predict(texts)
    report = classification_report(labels, preds, output_dict=True)

    # Save model artifact
    artifact_path = os.path.join(output_dir, "pipeline.joblib")
    joblib.dump(pipeline, artifact_path)

    # Calculate SHA256
    with open(artifact_path, "rb") as f:
        sha256 = hashlib.sha256(f.read()).hexdigest()

    metadata = {
        "model_name": "docintel_classifier_tfidf_logreg",
        "version": "v1.2.0",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "classes": classes,
        "cv_accuracy_mean": float(scores.mean()),
        "cv_accuracy_std": float(scores.std()),
        "sha256": sha256,
        "sample_count": len(texts),
        "classification_report": report,
    }

    with open(os.path.join(output_dir, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"Model exported successfully to {output_dir}/pipeline.joblib (SHA256: {sha256[:16]}...)")


if __name__ == "__main__":
    train_and_export()
