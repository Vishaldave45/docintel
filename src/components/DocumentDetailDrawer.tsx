import React, { useState } from "react";
import { DocumentItem } from "../types";
import {
  X,
  Layers,
  Cpu,
  GitFork,
  CheckCircle2,
  AlertTriangle,
  RotateCw,
  Code2,
  FileCheck,
  Hash,
} from "lucide-react";

interface DocumentDetailDrawerProps {
  document: DocumentItem | null;
  onClose: () => void;
  onReExtract: (id: string) => void;
  isReExtracting: boolean;
}

export const DocumentDetailDrawer: React.FC<DocumentDetailDrawerProps> = ({
  document,
  onClose,
  onReExtract,
  isReExtracting,
}) => {
  const [activeTab, setActiveTab] = useState<"fields" | "layout" | "classifier" | "trace" | "json">("fields");

  if (!document) return null;

  const isNeedsReview = document.extraction_status === "needs_review";

  return (
    <div className="fixed inset-y-0 right-0 w-full max-w-3xl bg-[#F7F5F0] border-l border-[#8A7B4F]/40 shadow-2xl z-50 flex flex-col">
      {/* Top Header Ledger Bar */}
      <div className="px-6 py-4 border-b border-[#8A7B4F]/30 bg-[#F2EFE9] flex items-center justify-between">
        <div className="flex items-center gap-3 min-w-0">
          <div className="px-2.5 py-1 bg-[#2B3A55] text-[#F7F5F0] font-mono text-xs font-bold border border-[#211F1C]">
            {document.document_type.toUpperCase().slice(0, 3)}
          </div>
          <div className="min-w-0">
            <h2 className="font-display font-bold text-lg text-[#211F1C] truncate">
              {document.filename}
            </h2>
            <div className="flex items-center gap-2 text-xs text-[#211F1C]/70">
              <span className="font-mono">ID: {document.id}</span>
              <span>·</span>
              <span>Schema: {document.target_schema}</span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2 shrink-0">
          <button
            onClick={() => onReExtract(document.id)}
            disabled={isReExtracting}
            className="px-3 py-1.5 border border-[#8A7B4F]/40 bg-[#F7F5F0] hover:bg-[#8A7B4F]/10 text-xs font-medium text-[#211F1C] flex items-center gap-1.5 transition-colors disabled:opacity-50"
          >
            <RotateCw className={`w-3.5 h-3.5 ${isReExtracting ? "animate-spin text-[#2B3A55]" : ""}`} />
            <span>Re-run Agent Graph</span>
          </button>

          <button
            onClick={onClose}
            className="p-1.5 hover:bg-[#8A7B4F]/20 text-[#211F1C] transition-colors border border-[#8A7B4F]/20"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Sub-header Tabs */}
      <div className="px-6 border-b border-[#8A7B4F]/25 bg-[#F7F5F0] flex items-center gap-1 overflow-x-auto">
        <button
          onClick={() => setActiveTab("fields")}
          className={`px-3 py-2.5 text-xs font-medium border-b-2 flex items-center gap-1.5 transition-colors whitespace-nowrap ${
            activeTab === "fields"
              ? "border-[#2B3A55] text-[#2B3A55] font-semibold"
              : "border-transparent text-[#211F1C]/70 hover:text-[#211F1C]"
          }`}
        >
          <FileCheck className="w-3.5 h-3.5" />
          <span>Extracted Fields</span>
        </button>

        <button
          onClick={() => setActiveTab("layout")}
          className={`px-3 py-2.5 text-xs font-medium border-b-2 flex items-center gap-1.5 transition-colors whitespace-nowrap ${
            activeTab === "layout"
              ? "border-[#2B3A55] text-[#2B3A55] font-semibold"
              : "border-transparent text-[#211F1C]/70 hover:text-[#211F1C]"
          }`}
        >
          <Layers className="w-3.5 h-3.5" />
          <span>Layout & OCR BBoxes ({document.layout_blocks.length})</span>
        </button>

        <button
          onClick={() => setActiveTab("classifier")}
          className={`px-3 py-2.5 text-xs font-medium border-b-2 flex items-center gap-1.5 transition-colors whitespace-nowrap ${
            activeTab === "classifier"
              ? "border-[#2B3A55] text-[#2B3A55] font-semibold"
              : "border-transparent text-[#211F1C]/70 hover:text-[#211F1C]"
          }`}
        >
          <Cpu className="w-3.5 h-3.5" />
          <span>ML Classification</span>
        </button>

        <button
          onClick={() => setActiveTab("trace")}
          className={`px-3 py-2.5 text-xs font-medium border-b-2 flex items-center gap-1.5 transition-colors whitespace-nowrap ${
            activeTab === "trace"
              ? "border-[#2B3A55] text-[#2B3A55] font-semibold"
              : "border-transparent text-[#211F1C]/70 hover:text-[#211F1C]"
          }`}
        >
          <GitFork className="w-3.5 h-3.5" />
          <span>LangGraph State Trace ({document.execution_trace?.length || 0})</span>
        </button>

        <button
          onClick={() => setActiveTab("json")}
          className={`px-3 py-2.5 text-xs font-medium border-b-2 flex items-center gap-1.5 transition-colors whitespace-nowrap ${
            activeTab === "json"
              ? "border-[#2B3A55] text-[#2B3A55] font-semibold"
              : "border-transparent text-[#211F1C]/70 hover:text-[#211F1C]"
          }`}
        >
          <Code2 className="w-3.5 h-3.5" />
          <span>Raw DTO</span>
        </button>
      </div>

      {/* Main Drawer Scrollable Content */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {/* Status Stamp Alert */}
        {isNeedsReview ? (
          <div className="p-3.5 bg-[#B33A2E]/10 border border-[#B33A2E]/40 flex items-start gap-3">
            <AlertTriangle className="w-5 h-5 text-[#B33A2E] shrink-0 mt-0.5" />
            <div>
              <h4 className="font-display font-semibold text-sm text-[#B33A2E]">
                Extraction Flagged for Manual Review
              </h4>
              <p className="text-xs text-[#211F1C]/80 mt-0.5">
                {document.validation_errors.join("; ") || "Schema confidence fell below threshold."}
              </p>
            </div>
          </div>
        ) : (
          <div className="p-3.5 bg-[#2B3A55]/10 border border-[#2B3A55]/30 flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <CheckCircle2 className="w-5 h-5 text-[#2B3A55]" />
              <div>
                <h4 className="font-display font-semibold text-sm text-[#2B3A55]">
                  Schema Validated & Filed
                </h4>
                <p className="text-xs text-[#211F1C]/70">
                  Passed mathematical consistency checks. Indexed into FAISS corpus.
                </p>
              </div>
            </div>
            <span className="stamp-box stamp-verified">
              {document.repair_attempts > 0 ? `Repaired (${document.repair_attempts})` : "Verified"}
            </span>
          </div>
        )}

        {/* TAB 1: Structured Fields */}
        {activeTab === "fields" && (
          <div className="space-y-4">
            <div className="flex items-center justify-between border-b border-[#8A7B4F]/25 pb-2">
              <h3 className="font-display font-semibold text-base text-[#211F1C]">
                Extracted Pydantic Fields ({document.target_schema})
              </h3>
              <span className="font-mono text-xs text-[#8A7B4F]">
                {Object.keys(document.extracted_fields || {}).length} keys mapped
              </span>
            </div>

            <div className="divide-y divide-[#8A7B4F]/15 border border-[#8A7B4F]/30 bg-[#FAF8F5]">
              {Object.entries(document.extracted_fields || {}).map(([key, value]) => {
                const conf = document.confidence_scores?.[key] || 0.95;
                const isComplex = typeof value === "object" && value !== null;

                return (
                  <div key={key} className="p-3.5 flex flex-col sm:flex-row sm:items-start justify-between gap-2">
                    <div className="sm:w-1/3">
                      <span className="font-mono text-xs font-semibold text-[#2B3A55]">
                        {key}
                      </span>
                      <div className="text-[10px] text-[#8A7B4F] font-mono mt-0.5">
                        CONF: {(conf * 100).toFixed(0)}%
                      </div>
                    </div>

                    <div className="sm:w-2/3">
                      {isComplex ? (
                        <pre className="text-xs font-mono bg-[#F7F5F0] p-2 border border-[#8A7B4F]/20 overflow-x-auto text-[#211F1C]">
                          {JSON.stringify(value, null, 2)}
                        </pre>
                      ) : (
                        <span className="text-xs font-sans text-[#211F1C] font-medium break-words">
                          {String(value)}
                        </span>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* TAB 2: Layout & OCR Bounding Boxes */}
        {activeTab === "layout" && (
          <div className="space-y-4">
            <div className="flex items-center justify-between border-b border-[#8A7B4F]/25 pb-2">
              <h3 className="font-display font-semibold text-base text-[#211F1C]">
                Segmented OCR Blocks & Bounding Geometry
              </h3>
              <span className="text-xs font-mono text-[#8A7B4F]">
                Reading Order Segmenter v1.0
              </span>
            </div>

            {/* Visual Canvas Representation */}
            <div className="border border-[#8A7B4F]/30 bg-[#FAF8F5] p-4 space-y-3">
              <div className="text-xs font-mono text-[#8A7B4F] mb-2 flex items-center justify-between">
                <span>CANVAS EMULATION (PAGE 1)</span>
                <span>520px x 400px VIRTUAL RASTER</span>
              </div>

              {document.layout_blocks.map((block) => (
                <div
                  key={block.id}
                  className={`p-2.5 border transition-all ${
                    block.block_type === "header"
                      ? "border-[#2B3A55] bg-[#2B3A55]/5"
                      : block.block_type === "table"
                      ? "border-[#8A7B4F] bg-[#8A7B4F]/10"
                      : "border-[#8A7B4F]/30 bg-[#F7F5F0]"
                  }`}
                >
                  <div className="flex items-center justify-between text-[11px] font-mono text-[#8A7B4F] mb-1">
                    <span className="font-bold text-[#2B3A55]">
                      #{block.id} [{block.block_type.toUpperCase()}]
                    </span>
                    <span>
                      BBOX: ({block.bbox.x}, {block.bbox.y}, {block.bbox.width}x{block.bbox.height}) · {(block.confidence * 100).toFixed(0)}%
                    </span>
                  </div>
                  <p className="text-xs font-sans text-[#211F1C] whitespace-pre-line">
                    {block.text}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 3: ML Classification */}
        {activeTab === "classifier" && (
          <div className="space-y-5">
            <div className="border-b border-[#8A7B4F]/25 pb-2">
              <h3 className="font-display font-semibold text-base text-[#211F1C]">
                Classical ML Classification Pipeline
              </h3>
              <p className="text-xs text-[#211F1C]/70">
                Scikit-Learn TF-IDF vectorizer + multiclass logistic regression with n-gram feature attribution.
              </p>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 border border-[#8A7B4F]/30 bg-[#FAF8F5]">
                <div className="text-xs text-[#8A7B4F] font-mono">PREDICTED CLASS</div>
                <div className="font-display font-bold text-xl text-[#2B3A55] mt-1 capitalize">
                  {document.document_type.replace(/_/g, " ")}
                </div>
                <div className="text-xs text-[#211F1C]/70 mt-1">
                  Confidence: {(document.classifier_confidence * 100).toFixed(1)}%
                </div>
              </div>

              <div className="p-4 border border-[#8A7B4F]/30 bg-[#FAF8F5]">
                <div className="text-xs text-[#8A7B4F] font-mono">MODEL LINEAGE</div>
                <div className="font-mono text-sm font-semibold text-[#211F1C] mt-1">
                  {document.classification_model_version}
                </div>
                <div className="text-xs text-[#211F1C]/70 mt-1">
                  SHA256: 8f2a91e4b3c0...
                </div>
              </div>
            </div>

            {/* Feature attribution table */}
            <div className="border border-[#8A7B4F]/30 bg-[#FAF8F5] p-4">
              <h4 className="font-display font-semibold text-sm text-[#211F1C] mb-3">
                Top TF-IDF Token Attributions
              </h4>
              <div className="space-y-2">
                {document.top_features?.map((feat, idx) => (
                  <div key={idx} className="flex items-center justify-between text-xs">
                    <span className="font-mono text-[#2B3A55]">
                      "{feat.feature_ngram}"
                    </span>
                    <div className="flex items-center gap-2">
                      <div className="w-24 bg-[#8A7B4F]/20 h-2">
                        <div
                          className="bg-[#2B3A55] h-2"
                          style={{ width: `${Math.min(100, feat.weight * 180)}%` }}
                        />
                      </div>
                      <span className="font-mono text-[#8A7B4F] w-10 text-right">
                        +{feat.weight}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* TAB 4: LangGraph State Trace */}
        {activeTab === "trace" && (
          <div className="space-y-4">
            <div className="border-b border-[#8A7B4F]/25 pb-2">
              <h3 className="font-display font-semibold text-base text-[#211F1C]">
                LangGraph State Execution Flow
              </h3>
              <p className="text-xs text-[#211F1C]/70">
                Deterministic agent graph node transitions, validation passes, and self-repair actions.
              </p>
            </div>

            <div className="space-y-3 relative before:absolute before:left-3 before:top-2 before:bottom-2 before:w-0.5 before:bg-[#8A7B4F]/30 pl-8">
              {document.execution_trace?.map((trace, idx) => (
                <div key={idx} className="relative bg-[#FAF8F5] border border-[#8A7B4F]/30 p-3.5">
                  <div className="absolute -left-[27px] top-4 w-3.5 h-3.5 bg-[#2B3A55] border-2 border-[#F7F5F0]" />
                  <div className="flex items-center justify-between text-xs mb-1">
                    <span className="font-mono font-bold text-[#2B3A55]">
                      {trace.node}
                    </span>
                    <span className="font-mono text-[#8A7B4F] text-[11px]">
                      {trace.timestamp}
                    </span>
                  </div>
                  <p className="text-xs text-[#211F1C]/85">
                    {trace.decision || trace.status || "Completed node execution"}
                  </p>
                  {trace.errors && trace.errors.length > 0 && (
                    <div className="mt-2 text-xs text-[#B33A2E] font-mono bg-[#B33A2E]/10 p-2 border border-[#B33A2E]/30">
                      Validation errors: {trace.errors.join(", ")}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 5: Raw JSON */}
        {activeTab === "json" && (
          <div className="space-y-2">
            <div className="text-xs font-mono text-[#8A7B4F]">DOCUMENT DTO CONTRACT</div>
            <pre className="p-4 bg-[#211F1C] text-[#F7F5F0] font-mono text-xs overflow-x-auto border border-[#211F1C]">
              {JSON.stringify(document, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
};
