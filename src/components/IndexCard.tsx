import React from "react";
import { DocumentItem } from "../types";
import { FileText, ArrowUpRight, Cpu } from "lucide-react";

interface IndexCardProps {
  document: DocumentItem;
  isSelected?: boolean;
  onSelect: (doc: DocumentItem) => void;
}

const TYPE_NOTCHES: Record<string, { tag: string; label: string; bg: string }> = {
  invoice: { tag: "INV", label: "Invoice", bg: "bg-[#2B3A55] text-[#F7F5F0]" },
  contract: { tag: "CTR", label: "Contract", bg: "bg-[#2B3A55] text-[#F7F5F0]" },
  financial_report: { tag: "REP", label: "Financial Report", bg: "bg-[#8A7B4F] text-[#F7F5F0]" },
  identification: { tag: "ID", label: "Identification", bg: "bg-[#211F1C] text-[#F7F5F0]" },
  receipt: { tag: "REC", label: "Receipt", bg: "bg-[#8A7B4F] text-[#F7F5F0]" },
  general: { tag: "DOC", label: "Document", bg: "bg-[#2B3A55] text-[#F7F5F0]" },
};

export const IndexCard: React.FC<IndexCardProps> = ({
  document,
  isSelected,
  onSelect,
}) => {
  const notch = TYPE_NOTCHES[document.document_type] || TYPE_NOTCHES.general;
  const filedDate = new Date(document.created_at).toLocaleDateString("en-US", {
    month: "2-digit",
    day: "2-digit",
  });

  const isNeedsReview = document.extraction_status === "needs_review";

  return (
    <div
      onClick={() => onSelect(document)}
      className={`relative cursor-pointer transition-all border bg-[#F7F5F0] flex flex-col text-left ${
        isSelected
          ? "border-[#2B3A55] ring-2 ring-[#2B3A55]/20 shadow-sm"
          : "border-[#8A7B4F]/30 hover:border-[#2B3A55] hover:bg-[#F2EFE9]"
      }`}
    >
      {/* Top Bar with Tab Notch */}
      <div className="flex items-stretch border-b border-[#8A7B4F]/25">
        {/* Physical Index Tab Notch */}
        <div
          className={`px-3 py-1.5 font-mono font-bold text-xs flex items-center justify-center tracking-wider border-r border-[#8A7B4F]/25 ${notch.bg}`}
        >
          {notch.tag}
        </div>
        
        {/* Document Title Header */}
        <div className="flex-1 px-3 py-1.5 flex items-center justify-between min-w-0 bg-[#F7F5F0]">
          <h3 className="font-display font-semibold text-sm text-[#211F1C] truncate">
            {document.filename.replace(/_/g, " ").replace(/\.[^/.]+$/, "")}
          </h3>
          <ArrowUpRight className="w-3.5 h-3.5 text-[#8A7B4F] shrink-0 ml-1.5 opacity-60" />
        </div>
      </div>

      {/* Ledger Metadata Sub-row */}
      <div className="px-3.5 py-2 border-b border-[#8A7B4F]/20 flex items-center justify-between text-xs bg-[#F7F5F0]/60">
        <div className="flex items-center gap-2 text-[#211F1C]/75">
          <span>filed {filedDate}</span>
          <span className="text-[#8A7B4F]">·</span>
          <span>{document.page_count} pg{document.page_count > 1 ? "s" : ""}</span>
          <span className="text-[#8A7B4F]">·</span>
          <span className="font-mono text-[11px]">
            {(document.file_size_bytes / 1024).toFixed(0)} KB
          </span>
        </div>

        {/* Rubber Stamp Status Mark */}
        <div>
          {isNeedsReview ? (
            <span className="stamp-box stamp-review">
              Needs Review
            </span>
          ) : (
            <span className="stamp-box stamp-verified">
              {document.extraction_status === "repaired" ? "Repaired" : "Filed & Valid"}
            </span>
          )}
        </div>
      </div>

      {/* Document OCR Preview Excerpt */}
      <div className="p-3.5 flex-1 flex flex-col justify-between space-y-3 bg-[#FAF8F5]">
        {/* Segmented text block excerpt */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between text-[11px] text-[#8A7B4F] font-mono">
            <span>LAYOUT OCR ({document.layout_blocks.length} BLOCKS)</span>
            <span>CONF: {(document.classifier_confidence * 100).toFixed(1)}%</span>
          </div>

          <p className="text-xs text-[#211F1C]/85 line-clamp-3 leading-relaxed font-sans border-l-2 border-[#8A7B4F]/40 pl-2 bg-[#F7F5F0] py-1">
            {document.raw_ocr_text.slice(0, 180)}...
          </p>
        </div>

        {/* ML Feature Attribution Tags */}
        {document.top_features && document.top_features.length > 0 && (
          <div className="pt-2 border-t border-[#8A7B4F]/15 flex items-center gap-1.5 flex-wrap">
            <span className="text-[10px] font-mono text-[#8A7B4F] flex items-center gap-1">
              <Cpu className="w-3 h-3" /> TF-IDF:
            </span>
            {document.top_features.slice(0, 2).map((feat, idx) => (
              <span
                key={idx}
                className="px-1.5 py-0.5 text-[10px] font-mono bg-[#8A7B4F]/10 text-[#211F1C]/80 border border-[#8A7B4F]/20"
              >
                "{feat.feature_ngram}"
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Card Footer Key Fields Summary */}
      <div className="px-3.5 py-2 bg-[#F2EFE9] border-t border-[#8A7B4F]/20 text-xs flex items-center justify-between">
        <span className="text-[#211F1C]/70 truncate max-w-[180px]">
          {document.target_schema}
        </span>
        <span className="font-mono text-[11px] text-[#2B3A55] font-semibold">
          {Object.keys(document.extracted_fields || {}).length} fields extracted
        </span>
      </div>
    </div>
  );
};
