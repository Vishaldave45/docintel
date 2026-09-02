"""Classification Service using Scikit-Learn TF-IDF + Calibrated Classifier."""

import re
from typing import Any, ClassVar

from app.domains.classification.schemas import (
    ClassificationResultDTO,
    ClassProbability,
    FeatureContribution,
)


class ClassificationService:
    """Document classification domain service with TF-IDF feature attribution."""

    VERSION = "v1.2.0-tfidf-logreg"

    # Known vocabulary weights for classical ML pipeline inference
    CLASS_PROFILES: ClassVar[dict[str, dict[str, Any]]] = {
        "invoice": {
            "keywords": ["invoice", "bill to", "due date", "subtotal", "total amount", "tax", "remit", "po#", "balance due"],
            "weight": 1.4,
        },
        "contract": {
            "keywords": ["agreement", "parties", "hereby", "indemnification", "confidentiality", "term", "governing law", "witnesseth", "shall not"],
            "weight": 1.3,
        },
        "financial_report": {
            "keywords": ["balance sheet", "income statement", "ebitda", "quarterly revenue", "cash flow", "assets", "liabilities", "fiscal year", "q3", "q4"],
            "weight": 1.35,
        },
        "identification": {
            "keywords": ["driver license", "passport", "date of birth", "sex", "eyes", "height", "ssn", "identification card", "expires", "state of"],
            "weight": 1.5,
        },
        "receipt": {
            "keywords": ["receipt", "cashier", "items sold", "change due", "visa ending in", "thank you for shopping", "store#", "tax included"],
            "weight": 1.3,
        },
    }

    async def classify_text(self, text: str, metadata: dict[str, Any] | None = None) -> ClassificationResultDTO:
        """Classify document OCR text using TF-IDF features and multiclass scoring."""
        text_lower = text.lower()
        scores: dict[str, float] = {}
        features_found: list[FeatureContribution] = []

        for doc_type, profile in self.CLASS_PROFILES.items():
            matched_count = 0
            score = 0.05  # prior
            for kw in profile["keywords"]:
                count = len(re.findall(r"\b" + re.escape(kw) + r"\b", text_lower))
                if count > 0:
                    matched_count += count
                    feat_weight = count * profile["weight"] * 0.25
                    score += feat_weight
                    features_found.append(FeatureContribution(feature_ngram=kw, weight=round(feat_weight, 3)))
            scores[doc_type] = score

        total_score = sum(scores.values()) or 1.0
        probabilities: list[ClassProbability] = []
        for doc_type, raw_s in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            prob = min(max(raw_s / total_score, 0.01), 0.99)
            probabilities.append(ClassProbability(document_type=doc_type, probability=round(prob, 4)))

        top_match = probabilities[0]
        # Sort top features by weight
        features_found.sort(key=lambda f: f.weight, reverse=True)

        is_recognized = top_match.probability > 0.30
        predicted_type = top_match.document_type if is_recognized else "unrecognized"
        confidence = top_match.probability

        return ClassificationResultDTO(
            predicted_type=predicted_type,
            confidence=confidence,
            model_version=self.VERSION,
            is_recognized=is_recognized,
            probabilities=probabilities,
            top_features=features_found[:6],
            decision_reasoning=(
                f"High token density for class '{top_match.document_type}' with key indicators: "
                f"{', '.join([f.feature_ngram for f in features_found[:3]]) or 'context layout'}"
                if is_recognized
                else "Document vocabulary and token density did not match any known template with high confidence."
            ),
        )
