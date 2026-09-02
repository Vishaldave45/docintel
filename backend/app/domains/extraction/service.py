"""Extraction Domain Service."""

from typing import Any

from app.domains.extraction.graph import ExtractionGraphRunner, ExtractionGraphState
from app.domains.extraction.llm import build_gemini_extraction_model, extract_with_gemini_schema
from app.domains.extraction.schemas import ExtractionResultDTO


class ExtractionService:
    """High-level extraction service coordinating LangGraph execution."""

    def __init__(self) -> None:
        self.runner = ExtractionGraphRunner()
        self.llm = build_gemini_extraction_model()

    async def extract_document_fields_with_llm(
        self,
        document_id: str,
        document_type: str,
        raw_ocr_text: str,
        layout_blocks: list[dict[str, Any]],
        schema: type[Any] | None = None,
    ) -> dict[str, Any] | None:
        """Try a Gemini structured-output extraction when the provider is configured."""
        if self.llm is None:
            return None

        target_schema = schema or self._resolve_schema_for_document_type(document_type)
        prompt = (
            f"Extract structured data for document_type='{document_type}'. "
            f"Return the fields in a validated JSON shape matching the schema.\n\n"
            f"OCR_TEXT:\n{raw_ocr_text}\n\n"
            f"LAYOUT_BLOCKS:\n{layout_blocks}"
        )
        return extract_with_gemini_schema(target_schema, prompt, model=self.llm)

    def _resolve_schema_for_document_type(self, document_type: str) -> type[Any]:
        """Map document type to the corresponding Pydantic schema."""
        doc_type = document_type.lower()
        if "invoice" in doc_type or "bill" in doc_type:
            from app.domains.extraction.schemas import InvoiceExtraction
            return InvoiceExtraction
        if "contract" in doc_type or "agreement" in doc_type or "nda" in doc_type:
            from app.domains.extraction.schemas import ContractExtraction
            return ContractExtraction
        if "report" in doc_type or "financial" in doc_type or "earnings" in doc_type:
            from app.domains.extraction.schemas import FinancialReportExtraction
            return FinancialReportExtraction
        if "id" in doc_type or "passport" in doc_type or "license" in doc_type:
            from app.domains.extraction.schemas import IDExtraction
            return IDExtraction
        if "receipt" in doc_type:
            from app.domains.extraction.schemas import ReceiptExtraction
            return ReceiptExtraction
        from app.domains.extraction.schemas import InvoiceExtraction
        return InvoiceExtraction

    async def extract_document_fields(
        self,
        document_id: str,
        document_type: str,
        raw_ocr_text: str,
        layout_blocks: list[dict[str, Any]],
        max_repair_attempts: int = 2,
    ) -> ExtractionResultDTO:
        """Run the type-conditioned LangGraph agent pipeline."""
        initial_state: ExtractionGraphState = {
            "document_id": document_id,
            "document_type": document_type,
            "raw_ocr_text": raw_ocr_text,
            "layout_blocks": layout_blocks,
            "target_schema_name": "",
            "extracted_data": None,
            "validation_errors": [],
            "repair_attempts": 0,
            "max_repair_attempts": max_repair_attempts,
            "is_valid": False,
            "confidence_scores": {},
            "execution_trace": [],
        }

        final_state = self.runner.run_graph(initial_state)

        flag_reason: str | None = None
        if len(raw_ocr_text.strip()) < 20:
            status = "flagged"
            flag_reason = "Extracted text is too short or degraded for reliable analysis."
        elif final_state["is_valid"]:
            status = "completed"
        elif final_state["repair_attempts"] >= max_repair_attempts:
            status = "needs_review"
        else:
            status = "failed"

        return ExtractionResultDTO(
            document_id=document_id,
            target_schema=final_state["target_schema_name"],
            status=status,
            is_valid=final_state["is_valid"],
            fields=final_state["extracted_data"] or {},
            flag_reason=flag_reason,
            validation_errors=final_state["validation_errors"],
            repair_attempts=final_state["repair_attempts"],
            confidence_scores=final_state["confidence_scores"],
            execution_trace=final_state["execution_trace"],
        )
