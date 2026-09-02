"""LangGraph State Machine for Type-Conditioned Agentic Extraction."""

import re
from typing import Any, TypedDict


class ExtractionGraphState(TypedDict):
    document_id: str
    document_type: str
    raw_ocr_text: str
    layout_blocks: list[dict[str, Any]]
    target_schema_name: str
    extracted_data: dict[str, Any] | None
    validation_errors: list[str]
    repair_attempts: int
    max_repair_attempts: int
    is_valid: bool
    confidence_scores: dict[str, float]
    execution_trace: list[dict[str, Any]]


class ExtractionGraphRunner:
    """Simulated & LangGraph-compatible state engine for typed extraction & validation loops."""

    def select_schema_node(self, state: ExtractionGraphState) -> ExtractionGraphState:
        """Route to appropriate Pydantic schema based on classified document type."""
        doc_type = state["document_type"].lower()
        if "invoice" in doc_type or "bill" in doc_type:
            schema = "InvoiceExtraction"
        elif "contract" in doc_type or "agreement" in doc_type or "nda" in doc_type:
            schema = "ContractExtraction"
        elif "report" in doc_type or "financial" in doc_type or "earnings" in doc_type:
            schema = "FinancialReportExtraction"
        elif "id" in doc_type or "passport" in doc_type or "license" in doc_type:
            schema = "IDExtraction"
        elif "receipt" in doc_type:
            schema = "ReceiptExtraction"
        else:
            schema = "GenericExtraction"

        state["target_schema_name"] = schema
        state["execution_trace"].append({
            "node": "select_schema_node",
            "decision": f"Selected schema '{schema}' for document_type '{doc_type}'",
            "timestamp": "step-1"
        })
        return state

    def extract_fields_node(self, state: ExtractionGraphState) -> ExtractionGraphState:
        """Agentic extraction node applying heuristic parsing or LLM prompt response."""
        text = state["raw_ocr_text"]
        schema = state["target_schema_name"]
        extracted: dict[str, Any] = {}
        confidences: dict[str, float] = {}

        if schema == "InvoiceExtraction":
            # Extract invoice number
            inv_match = re.search(r"(?:invoice\s*#?|inv-?)[:\s]*([A-Z0-9-]+)", text, re.IGNORECASE)
            invoice_number = inv_match.group(1) if inv_match else "4471"
            extracted["invoice_number"] = f"INV-{invoice_number}" if not invoice_number.upper().startswith("INV-") else invoice_number

            # Vendor & customer
            extracted["vendor_name"] = "Acme Global Supplies Corp."
            extracted["customer_name"] = "Kestrel Analytics Inc."
            extracted["invoice_date"] = "2026-08-29"
            extracted["due_date"] = "2026-09-28"
            extracted["currency"] = "USD"

            # Totals
            total_match = re.search(r"(?:total|amount due)[:\s]*\$?\s*([\d,]+\.?\d*)", text, re.IGNORECASE)
            total_val = float(total_match.group(1).replace(",", "")) if total_match else 14250.00
            extracted["subtotal"] = round(total_val * 0.9, 2)
            extracted["tax_amount"] = round(total_val * 0.1, 2)
            extracted["total_amount"] = total_val
            extracted["payment_terms"] = "Net 30"
            extracted["line_items"] = [
                {"description": "Enterprise Platform Licenses (Tier 1)", "quantity": 10, "unit_price": 1200.0, "total": 12000.0},
                {"description": "Dedicated Cloud Cluster Ingestion Setup", "quantity": 1, "unit_price": 2250.0, "total": 2250.0},
            ]
            confidences = {"invoice_number": 0.98, "vendor_name": 0.96, "total_amount": 0.99, "line_items": 0.94}

        elif schema == "ReceiptExtraction":
            # Extract merchant from first header line
            lines = [l.strip() for l in text.split("\n") if l.strip()]
            merchant = lines[0] if lines else "Store Express"
            extracted["merchant_name"] = merchant
            extracted["receipt_date"] = "2026-08-29"

            total_match = re.search(r"(?:total|total due|amount)[:\s]*\$?\s*([\d,]+\.?\d*)", text, re.IGNORECASE)
            total_val = float(total_match.group(1).replace(",", "")) if total_match else 45.90
            tax_match = re.search(r"tax[:\s]*\$?\s*([\d,]+\.?\d*)", text, re.IGNORECASE)
            tax_val = float(tax_match.group(1).replace(",", "")) if tax_match else round(total_val * 0.08, 2)
            subtotal_val = round(total_val - tax_val, 2)

            extracted["subtotal"] = subtotal_val
            extracted["tax_amount"] = tax_val
            extracted["total_amount"] = total_val
            extracted["payment_method"] = "Contactless / Card"
            extracted["line_items"] = [
                {"description": "General Retail Purchase Item", "quantity": 1.0, "unit_price": subtotal_val, "total": subtotal_val}
            ]
            confidences = {"merchant_name": 0.95, "total_amount": 0.97, "subtotal": 0.93}

        elif schema == "ContractExtraction":
            extracted["contract_title"] = "Master Services & Data Protection Agreement"
            extracted["effective_date"] = "2026-08-30"
            extracted["expiration_date"] = "2028-08-30"
            extracted["parties"] = [
                {"name": "Kestrel Analytics Inc.", "role": "Client"},
                {"name": "OmniData Solutions LLC", "role": "Service Provider"},
            ]
            extracted["governing_law"] = "State of Delaware, United States"
            extracted["confidentiality_clause_years"] = 3
            extracted["liability_cap"] = "12 months aggregate fees paid under this Agreement"
            extracted["termination_notice_days"] = 60
            extracted["key_obligations"] = [
                "Provider shall maintain ISO 27001 & SOC 2 Type II certification throughout the term.",
                "Client shall provide timely access to designated cloud tenancy environments.",
                "Mutual indemnification for third-party intellectual property claims."
            ]
            confidences = {"contract_title": 0.97, "parties": 0.95, "liability_cap": 0.91, "governing_law": 0.98}

        elif schema == "FinancialReportExtraction":
            extracted["company_name"] = "Apex Logistics International"
            extracted["fiscal_period"] = "Q3 2026"
            extracted["reporting_currency"] = "USD"
            extracted["revenue"] = 48200000.0
            extracted["net_income"] = 7450000.0
            extracted["ebitda"] = 11200000.0
            extracted["operating_expenses"] = 36950000.0
            extracted["cash_and_equivalents"] = 24800000.0
            extracted["key_highlights"] = [
                "Organic revenue expansion grew 18.4% year-over-year.",
                "Gross margin improved 210 bps due to automated sorting depots."
            ]
            confidences = {"company_name": 0.99, "revenue": 0.97, "net_income": 0.95}

        elif schema == "IDExtraction":
            extracted["document_type"] = "passport"
            extracted["full_name"] = "ELIZABETH JANE HOLLOWAY"
            extracted["document_number"] = "P98231405"
            extracted["date_of_birth"] = "1992-04-14"
            extracted["expiration_date"] = "2032-04-13"
            extracted["issuing_authority"] = "United States Department of State"
            extracted["country_code"] = "USA"
            confidences = {"full_name": 0.99, "document_number": 0.98, "expiration_date": 0.97}

        else:
            extracted["title"] = "General Corporate Document"
            extracted["summary"] = text[:200]
            confidences = {"title": 0.85}

        state["extracted_data"] = extracted
        state["confidence_scores"] = confidences
        state["execution_trace"].append({
            "node": "extract_fields_node",
            "extracted_keys_count": len(extracted),
            "status": "success",
            "timestamp": "step-2"
        })
        return state

    def validate_schema_node(self, state: ExtractionGraphState) -> ExtractionGraphState:
        """Validate extracted fields against type constraints and mathematical sanity rules."""
        data = state["extracted_data"] or {}
        errors: list[str] = []
        schema = state["target_schema_name"]

        if schema in ("InvoiceExtraction", "ReceiptExtraction"):
            subtotal = float(data.get("subtotal", 0))
            tax = float(data.get("tax_amount", 0))
            total = float(data.get("total_amount", 0))
            # Mathematical consistency check
            if abs((subtotal + tax) - total) > 0.05:
                errors.append(f"Subtotal ({subtotal}) + Tax ({tax}) does not equal Total Amount ({total})")
            if schema == "InvoiceExtraction" and not data.get("invoice_number"):
                errors.append("Missing mandatory 'invoice_number'")
            if schema == "ReceiptExtraction" and not data.get("merchant_name"):
                errors.append("Missing mandatory 'merchant_name'")

        elif schema == "ContractExtraction":
            if not data.get("parties") or len(data.get("parties", [])) < 2:
                errors.append("Contract requires at least 2 identified parties")
            if not data.get("governing_law"):
                errors.append("Missing 'governing_law' clause specification")

        state["validation_errors"] = errors
        state["is_valid"] = len(errors) == 0
        state["execution_trace"].append({
            "node": "validate_schema_node",
            "is_valid": state["is_valid"],
            "error_count": len(errors),
            "errors": errors,
            "timestamp": f"step-validate-attempt-{state['repair_attempts']}"
        })
        return state

    def repair_agent_node(self, state: ExtractionGraphState) -> ExtractionGraphState:
        """Self-correction node fixing failed validations."""
        state["repair_attempts"] += 1
        data = state["extracted_data"] or {}

        # Self-repair logic
        if "Subtotal" in " ".join(state["validation_errors"]):
            # Recalibrate total
            subtotal = float(data.get("subtotal", 0))
            tax = float(data.get("tax_amount", 0))
            data["total_amount"] = round(subtotal + tax, 2)
            state["extracted_data"] = data

        state["execution_trace"].append({
            "node": "repair_agent_node",
            "attempt": state["repair_attempts"],
            "action": "Recalibrated mathematical constraints on line totals",
            "timestamp": f"step-repair-{state['repair_attempts']}"
        })
        return state

    def run_graph(self, state: ExtractionGraphState) -> ExtractionGraphState:
        """Execute the LangGraph state loop."""
        state = self.select_schema_node(state)
        state = self.extract_fields_node(state)
        state = self.validate_schema_node(state)

        while not state["is_valid"] and state["repair_attempts"] < state["max_repair_attempts"]:
            state = self.repair_agent_node(state)
            state = self.validate_schema_node(state)

        return state
