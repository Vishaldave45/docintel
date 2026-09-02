import React, { useState } from "react";
import { X, UploadCloud, FileText, Sparkles, AlertCircle } from "lucide-react";

interface IngestModalProps {
  isOpen: boolean;
  onClose: () => void;
  onIngestSuccess: () => void;
}

const PRESET_TEMPLATES = [
  {
    title: "Commercial Logistics Invoice",
    filename: "Apex_Freight_Invoice_8821.pdf",
    contentType: "application/pdf",
    content: `INVOICE
APEX FREIGHT & TRANSIT LLC
400 Port Terminal Rd, Seattle, WA
Invoice Number: INV-8821
Invoice Date: September 01, 2026
Payment Terms: Net 30
Due Date: October 01, 2026

BILL TO:
Kestrel Analytics Inc.
450 Ledger Plaza, New York, NY

LINE ITEMS:
1. Intermodal Refrigerated Container Haul | Qty: 2 | Unit: $2,800.00 | Total: $5,600.00
2. Cold-Chain Monitoring Telemetry Sensors | Qty: 10 | Unit: $120.00 | Total: $1,200.00
3. Port Drayage & Fuel Surcharge | Qty: 1 | Unit: $650.00 | Total: $650.00

Subtotal: $7,450.00
State & Local Tax (0%): $0.00
TOTAL AMOUNT DUE: $7,450.00

Remit payment via ACH to Wells Fargo Account #992140510, Routing #12100024.`,
  },
  {
    title: "Software IP & Non-Disclosure Agreement",
    filename: "Mutual_NDA_CloudSync.pdf",
    contentType: "application/pdf",
    content: `MUTUAL NON-DISCLOSURE AND PROPRIETARY INFORMATION AGREEMENT
This Agreement is entered into on September 01, 2026 by and between Kestrel Analytics Inc. ("Disclosing Party") and CloudSync Networks Inc. ("Receiving Party").

1. PURPOSE: Evaluation of high-throughput document ingestion APIs and vector indexing pipelines.
2. CONFIDENTIALITY PERIOD: Receiving Party agrees to protect Confidential Information for a period of two (2) years from disclosure.
3. GOVERNING LAW: This Agreement shall be governed by the laws of the State of New York.
4. TERMINATION: Either party may terminate discussions upon thirty (30) days written notice.
5. LIABILITY: Total liability for breach of non-willful confidentiality shall not exceed $500,000.00 USD.`,
  },
  {
    title: "Quarterly Board Revenue & EBITDA Statement",
    filename: "Q3_Revenue_EBITDA_Audit.pdf",
    contentType: "application/pdf",
    content: `KESTREL ANALYTICS CORP.
CONSOLIDATED OPERATIONAL UPDATE — Q3 2026
Fiscal Period: Three Months Ended September 30, 2026

FINANCIAL SUMMARY:
- Total Operating Revenue: $19,450,000.00
- Research & Development Expenses: $6,200,000.00
- Sales & Customer Success: $4,800,000.00
- General & Administrative: $2,450,000.00
Total Operating Expenses: $13,450,000.00

Operating Income: $6,000,000.00
Adjusted EBITDA: $6,450,000.00
NET INCOME: $4,750,000.00
Cash and Equivalents: $18,200,000.00

The company maintained a 99.4% net revenue retention rate across tier-one enterprise accounts.`,
  },
];

export const IngestModal: React.FC<IngestModalProps> = ({
  isOpen,
  onClose,
  onIngestSuccess,
}) => {
  const [filename, setFilename] = useState("Uploaded_Invoice_0901.pdf");
  const [contentType, setContentType] = useState("application/pdf");
  const [textContent, setTextContent] = useState(PRESET_TEMPLATES[0].content);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleApplyPreset = (idx: number) => {
    const p = PRESET_TEMPLATES[idx];
    setFilename(p.filename);
    setContentType(p.contentType);
    setTextContent(p.content);
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setFilename(file.name);
    setContentType(file.type || "application/octet-stream");

    const reader = new FileReader();
    reader.onload = (event) => {
      const text = event.target?.result as string;
      setTextContent(text || `Document ingested from ${file.name}`);
    };
    reader.readAsText(file);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!textContent.trim()) {
      setError("Document text cannot be empty.");
      return;
    }

    setIsProcessing(true);
    setError(null);

    try {
      const res = await fetch("/api/v1/documents/upload", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          filename,
          content_type: contentType,
          text_content: textContent,
        }),
      });

      if (!res.ok) {
        throw new Error("Failed to process document through ingestion pipeline.");
      }

      onIngestSuccess();
      onClose();
    } catch (err: any) {
      setError(err.message || "An error occurred during ingestion.");
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-[#211F1C]/50 backdrop-blur-xs flex items-center justify-center p-4 z-50">
      <div className="bg-[#F7F5F0] border border-[#8A7B4F]/40 shadow-2xl max-w-2xl w-full max-h-[90vh] flex flex-col">
        {/* Header */}
        <div className="px-6 py-4 border-b border-[#8A7B4F]/30 bg-[#F2EFE9] flex items-center justify-between">
          <div>
            <h3 className="font-display font-bold text-lg text-[#211F1C]">
              File New Document into DocIntel
            </h3>
            <p className="text-xs text-[#211F1C]/70">
              Triggers Layout Segmentation, Classical ML Classifier, LangGraph Extraction, and FAISS Vector Indexing.
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 hover:bg-[#8A7B4F]/20 text-[#211F1C] border border-[#8A7B4F]/20"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4 overflow-y-auto flex-1">
          {error && (
            <div className="p-3 bg-[#B33A2E]/10 border border-[#B33A2E]/40 text-xs text-[#B33A2E] flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {/* Quick Benchmark Presets */}
          <div>
            <label className="block text-xs font-mono text-[#8A7B4F] mb-1.5">
              LOAD BENCHMARK ARCHIVAL TEMPLATE:
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
              {PRESET_TEMPLATES.map((p, idx) => (
                <button
                  type="button"
                  key={idx}
                  onClick={() => handleApplyPreset(idx)}
                  className="p-2.5 text-left border border-[#8A7B4F]/30 bg-[#FAF8F5] hover:bg-[#8A7B4F]/10 transition-colors text-xs space-y-1"
                >
                  <div className="font-display font-semibold text-[#2B3A55] truncate">
                    {p.title}
                  </div>
                  <div className="font-mono text-[10px] text-[#8A7B4F] truncate">
                    {p.filename}
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* File Name & Upload Input */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-mono text-[#8A7B4F] mb-1">
                DOCUMENT FILENAME:
              </label>
              <input
                type="text"
                value={filename}
                onChange={(e) => setFilename(e.target.value)}
                required
                className="w-full px-3 py-2 bg-[#FAF8F5] border border-[#8A7B4F]/40 text-xs text-[#211F1C] font-mono focus:outline-none focus:border-[#2B3A55]"
              />
            </div>

            <div>
              <label className="block text-xs font-mono text-[#8A7B4F] mb-1">
                OR ATTACH PHYSICAL SCAN / TEXT:
              </label>
              <label className="w-full px-3 py-2 bg-[#FAF8F5] border border-dashed border-[#8A7B4F]/50 text-xs text-[#211F1C] cursor-pointer hover:bg-[#8A7B4F]/10 flex items-center justify-center gap-1.5">
                <UploadCloud className="w-4 h-4 text-[#8A7B4F]" />
                <span className="truncate">Select Local File</span>
                <input
                  type="file"
                  onChange={handleFileUpload}
                  className="hidden"
                  accept=".pdf,.txt,.png,.jpg,.jpeg"
                />
              </label>
            </div>
          </div>

          {/* Raw Text Content */}
          <div>
            <label className="block text-xs font-mono text-[#8A7B4F] mb-1">
              DOCUMENT RAW TEXT / OCR STREAM:
            </label>
            <textarea
              rows={8}
              value={textContent}
              onChange={(e) => setTextContent(e.target.value)}
              placeholder="Paste raw OCR text or document stream here..."
              className="w-full p-3 bg-[#FAF8F5] border border-[#8A7B4F]/40 text-xs text-[#211F1C] font-mono leading-relaxed focus:outline-none focus:border-[#2B3A55]"
            />
          </div>

          {/* Pipeline execution indicator */}
          <div className="p-3 bg-[#F2EFE9] border border-[#8A7B4F]/20 text-[11px] text-[#211F1C]/75 font-mono space-y-1">
            <div className="font-bold text-[#2B3A55]">PIPELINE EXECUTION SPECIFICATION:</div>
            <div>1. Ingestion: OCR Layout Analyzer (Heuristic BBox Segmentation)</div>
            <div>2. Classification: Scikit-Learn TF-IDF + LogisticRegression</div>
            <div>3. Extraction: LangGraph Type-Conditioned Agent + Pydantic Validation</div>
            <div>4. Indexing: Sentence-Transformers (384-dim) into FAISS Corpus</div>
          </div>
        </form>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-[#8A7B4F]/30 bg-[#F2EFE9] flex items-center justify-end gap-3">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 border border-[#8A7B4F]/30 text-xs font-medium text-[#211F1C] hover:bg-[#8A7B4F]/10 transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            disabled={isProcessing}
            className="px-5 py-2 bg-[#2B3A55] text-[#F7F5F0] hover:bg-[#211F1C] text-xs font-medium transition-colors flex items-center gap-2 border border-[#211F1C] disabled:opacity-50"
          >
            {isProcessing ? (
              <span className="font-mono animate-pulse">Running Ingestion Pipeline...</span>
            ) : (
              <>
                <Sparkles className="w-3.5 h-3.5" />
                <span>Ingest & File Document</span>
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};
