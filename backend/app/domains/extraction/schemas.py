"""Type-Specific Extraction Pydantic Schemas and Validation Contracts."""

from typing import Any, Literal

from pydantic import BaseModel, Field


class InvoiceLineItem(BaseModel):
    description: str
    quantity: float
    unit_price: float
    total: float


class InvoiceExtraction(BaseModel):
    invoice_number: str = Field(..., description="Unique invoice identifier or code")
    vendor_name: str = Field(..., description="Entity issuing the invoice")
    customer_name: str = Field(..., description="Billed entity name")
    invoice_date: str = Field(..., description="Date of issuance YYYY-MM-DD")
    due_date: str = Field(..., description="Payment due date YYYY-MM-DD")
    currency: str = Field(default="USD")
    subtotal: float
    tax_amount: float = Field(default=0.0)
    total_amount: float
    payment_terms: str = Field(default="Net 30")
    line_items: list[InvoiceLineItem] = Field(default_factory=list)


class ContractParty(BaseModel):
    name: str
    role: str  # e.g. "Disclosing Party", "Client", "Vendor"


class ContractExtraction(BaseModel):
    contract_title: str
    effective_date: str
    expiration_date: str | None = None
    parties: list[ContractParty]
    governing_law: str
    confidentiality_clause_years: int = Field(default=2)
    liability_cap: str
    termination_notice_days: int = Field(default=30)
    key_obligations: list[str] = Field(default_factory=list)


class FinancialReportExtraction(BaseModel):
    company_name: str
    fiscal_period: str  # e.g. "Q3 2025" or "FY2025"
    reporting_currency: str = "USD"
    revenue: float
    net_income: float
    ebitda: float | None = None
    operating_expenses: float
    cash_and_equivalents: float
    key_highlights: list[str] = Field(default_factory=list)


class IDExtraction(BaseModel):
    document_type: Literal["passport", "driver_license", "national_id"]
    full_name: str
    document_number: str
    date_of_birth: str
    expiration_date: str
    issuing_authority: str
    country_code: str


class ExtractionResultDTO(BaseModel):
    document_id: str
    target_schema: str
    status: Literal["completed", "needs_review", "flagged", "failed"]
    is_valid: bool
    fields: dict[str, Any]
    flag_reason: str | None = None
    validation_errors: list[str] = Field(default_factory=list)
    repair_attempts: int = 0
    confidence_scores: dict[str, float] = Field(default_factory=dict)
    execution_trace: list[dict[str, Any]] = Field(default_factory=list)
