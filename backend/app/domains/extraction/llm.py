"""LLM model factory for extraction workflows."""

from __future__ import annotations

from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel

from app.core.config import settings


def build_gemini_extraction_model() -> BaseChatModel | None:
    """Build the Gemini chat model used for schema-driven extraction.

    The project intentionally keeps Pydantic structured-output schemas unchanged and
    delegates provider choice to the underlying LangChain model wrapper.
    """
    if not settings.gemini_api_key:
        return None

    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
    except ImportError as exc:  # pragma: no cover - dependency installation guard
        raise RuntimeError(
            "langchain-google-genai is required for Gemini extraction. "
            "Install it with: pip install langchain-google-genai"
        ) from exc

    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=settings.gemini_api_key,
        temperature=0.2,
    )


def extract_with_gemini_schema(
    schema: type[Any],
    prompt: str,
    *,
    model: BaseChatModel | None = None,
) -> Any | None:
    """Use Gemini structured output with a Pydantic schema when an API key is configured."""
    if model is None:
        model = build_gemini_extraction_model()
    if model is None:
        return None

    try:
        structured_model = model.with_structured_output(schema)
        return structured_model.invoke(prompt)
    except Exception:
        return None
