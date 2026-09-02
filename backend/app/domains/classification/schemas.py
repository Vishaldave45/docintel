"""Classification Domain DTOs and Schemas."""

from pydantic import BaseModel, Field


class ClassProbability(BaseModel):
    document_type: str
    probability: float = Field(..., ge=0.0, le=1.0)


class FeatureContribution(BaseModel):
    feature_ngram: str
    weight: float


class ClassificationResultDTO(BaseModel):
    predicted_type: str
    confidence: float
    model_version: str
    probabilities: list[ClassProbability]
    top_features: list[FeatureContribution]
    decision_reasoning: str
