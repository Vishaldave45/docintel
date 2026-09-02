"""Extraction Domain Service."""

from typing import Any
from app.domains.extraction.schemas import ExtractionResultDTO
from app.domains.extraction.graph import ExtractionGraphRunner, ExtractionGraphState


class ExtractionService:
    """High-level extraction service coordinating LangGraph execution."""

    def __init__(self) -> None:
        self.runner = ExtractionGraphRunner()

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

        status = "completed" if final_state["is_valid"] else ("needs_review" if final_state["repair_attempts"] >= max_repair_attempts else "failed")

        return ExtractionResultDTO(
            document_id=document_id,
            target_schema=final_state["target_schema_name"],
            status=status,
            is_valid=final_state["is_valid"],
            fields=final_state["extracted_data"] or {},
            validation_errors=final_state["validation_errors"],
            repair_attempts=final_state["repair_attempts"],
            confidence_scores=final_state["confidence_scores"],
            execution_trace=final_state["execution_trace"],
        )
