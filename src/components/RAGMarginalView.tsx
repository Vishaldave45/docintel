import React, { useState } from "react";
import { RAGResponse } from "../types";
import { Search, FileText, ArrowRight, CornerDownRight, Cpu, BookOpen, Clock } from "lucide-react";

interface RAGMarginalViewProps {
  onSelectDocumentById: (id: string) => void;
}

export const RAGMarginalView: React.FC<RAGMarginalViewProps> = ({ onSelectDocumentById }) => {
  const [query, setQuery] = useState("");
  const [filterType, setFilterType] = useState("all");
  const [isLoading, setIsLoading] = useState(false);
  const [history, setHistory] = useState<RAGResponse[]>([
    {
      query: "What is the liability cap specified in the vendor agreement?",
      answer:
        "According to the **Vendor Agreement (Master Services & Data Processing Agreement)**, Section 11 specifies that neither party's aggregate liability under this Agreement shall exceed **twelve (12) months of fees paid or payable** by Client immediately preceding the event giving rise to liability.",
      citations: [
        {
          document_id: "doc-9022",
          filename: "Vendor_Agreement_Kestrel.pdf",
          document_type: "contract",
          page_number: 4,
          block_id: "blk_005",
          snippet_text: "Liability Cap: 12 months fees paid. Governing Law: State of Delaware.",
          relevance_score: 0.962,
          line_number: 14,
        },
        {
          document_id: "doc-9022",
          filename: "Vendor_Agreement_Kestrel.pdf",
          document_type: "contract",
          page_number: 2,
          block_id: "blk_003",
          snippet_text: "The initial term shall be twenty-four (24) months. Termination without cause requires 60 days notice.",
          relevance_score: 0.810,
          line_number: 8,
        },
      ],
      retrieval_latency_ms: 38,
      model_name: "sentence-transformers/all-MiniLM-L6-v2 + FAISS",
      corpus_documents_searched: 4,
    },
  ]);

  const handleSearch = async (e?: React.FormEvent, customQuery?: string) => {
    if (e) e.preventDefault();
    const activeQ = customQuery || query;
    if (!activeQ.trim()) return;

    setIsLoading(true);
    try {
      const res = await fetch("/api/v1/rag/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query: activeQ,
          filter_document_type: filterType === "all" ? undefined : filterType,
          top_k: 4,
        }),
      });

      if (res.ok) {
        const data: RAGResponse = await res.json();
        setHistory((prev) => [data, ...prev]);
        if (!customQuery) setQuery("");
      }
    } catch (err) {
      console.error("RAG Query failed:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const SAMPLE_QUESTIONS = [
    "What is the total amount due on invoice #4471?",
    "What is the liability cap in the vendor agreement?",
    "What was Apex Logistics Q3 net income and EBITDA?",
    "What is the passport expiration date for Elizabeth Holloway?",
  ];

  return (
    <div className="space-y-6">
      {/* Top Query Ledger Section */}
      <div className="bg-[#FAF8F5] border border-[#8A7B4F]/30 p-5 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-[#8A7B4F]/20 pb-3">
          <div>
            <h2 className="font-display font-bold text-lg text-[#211F1C]">
              Corpus Semantic RAG & Ledger Query
            </h2>
            <p className="text-xs text-[#211F1C]/70 mt-0.5">
              Dense vector embeddings (Hugging Face) indexed in FAISS with exact marginal source citations.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs font-mono text-[#8A7B4F]">FILTER:</span>
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="px-2.5 py-1 text-xs border border-[#8A7B4F]/30 bg-[#F7F5F0] text-[#211F1C] font-mono focus:outline-none focus:border-[#2B3A55]"
            >
              <option value="all">All Document Types</option>
              <option value="invoice">Invoices Only</option>
              <option value="contract">Contracts Only</option>
              <option value="financial_report">Financial Reports Only</option>
              <option value="identification">Identification Only</option>
            </select>
          </div>
        </div>

        {/* Search Input Box */}
        <form onSubmit={handleSearch} className="flex gap-2">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-[#8A7B4F] absolute left-3 top-3" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Query across all filed documents (e.g. 'What are the termination notice terms?')..."
              className="w-full pl-9 pr-4 py-2.5 bg-[#F7F5F0] border border-[#8A7B4F]/40 text-sm text-[#211F1C] placeholder-[#211F1C]/40 focus:outline-none focus:border-[#2B3A55] font-sans"
            />
          </div>

          <button
            type="submit"
            disabled={isLoading || !query.trim()}
            className="px-5 py-2.5 bg-[#2B3A55] text-[#F7F5F0] hover:bg-[#211F1C] text-sm font-medium transition-colors flex items-center gap-2 border border-[#211F1C] disabled:opacity-50"
          >
            {isLoading ? (
              <span className="font-mono text-xs animate-pulse">Searching...</span>
            ) : (
              <>
                <span>Query Corpus</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        {/* Quick Question Chips */}
        <div className="flex items-center gap-2 flex-wrap pt-1">
          <span className="text-xs font-mono text-[#8A7B4F]">QUICK INQUIRIES:</span>
          {SAMPLE_QUESTIONS.map((q, idx) => (
            <button
              key={idx}
              onClick={() => {
                setQuery(q);
                handleSearch(undefined, q);
              }}
              className="px-2.5 py-1 text-xs border border-[#8A7B4F]/30 bg-[#F7F5F0] hover:bg-[#8A7B4F]/10 text-[#211F1C] text-left transition-colors"
            >
              {q}
            </button>
          ))}
        </div>
      </div>

      {/* Two-Column Marginal Annotated Conversation Stream */}
      <div className="space-y-6">
        {history.map((item, idx) => (
          <div
            key={idx}
            className="border border-[#8A7B4F]/30 bg-[#F7F5F0] overflow-hidden"
          >
            {/* Top Query Ledger Line */}
            <div className="px-5 py-3 border-b border-[#8A7B4F]/20 bg-[#F2EFE9] flex items-center justify-between">
              <div className="flex items-center gap-2 text-xs">
                <span className="font-mono font-bold text-[#2B3A55] uppercase">
                  INQUIRY #{history.length - idx}
                </span>
                <span className="text-[#8A7B4F]">·</span>
                <span className="font-medium text-[#211F1C]">{item.query}</span>
              </div>

              <div className="flex items-center gap-3 text-[11px] font-mono text-[#8A7B4F]">
                <span className="flex items-center gap-1">
                  <Clock className="w-3 h-3" /> {item.retrieval_latency_ms}ms
                </span>
                <span>·</span>
                <span>{item.corpus_documents_searched} docs searched</span>
              </div>
            </div>

            {/* Two-Column Split (Left: Synthesized ledger text; Right: Marginal source citations) */}
            <div className="grid grid-cols-1 lg:grid-cols-12 divide-y lg:divide-y-0 lg:divide-x divide-[#8A7B4F]/20">
              {/* Left Column (Synthesized Ledger Output) */}
              <div className="lg:col-span-7 p-5 space-y-3 bg-[#F7F5F0]">
                <div className="flex items-center gap-2 text-xs text-[#8A7B4F] font-mono">
                  <BookOpen className="w-3.5 h-3.5" />
                  <span>GROUNDED SYNTHESIS</span>
                </div>

                <div className="text-sm font-sans text-[#211F1C] leading-relaxed whitespace-pre-line border-l-2 border-[#2B3A55] pl-3 py-1">
                  {item.answer}
                </div>

                <div className="pt-2 text-[11px] font-mono text-[#8A7B4F] flex items-center gap-1.5">
                  <Cpu className="w-3 h-3" />
                  <span>Retrieved via {item.model_name}</span>
                </div>
              </div>

              {/* Right Column (Marginal Source Notes & Page Lineage) */}
              <div className="lg:col-span-5 p-5 space-y-3 bg-[#FAF8F5]">
                <div className="flex items-center justify-between text-xs text-[#8A7B4F] font-mono border-b border-[#8A7B4F]/20 pb-1.5">
                  <span>MARGINAL SOURCE CITATIONS</span>
                  <span>({item.citations.length})</span>
                </div>

                {item.citations.length === 0 ? (
                  <p className="text-xs text-[#211F1C]/60 italic">
                    No direct source snippets exceeded cosine threshold.
                  </p>
                ) : (
                  <div className="space-y-2.5">
                    {item.citations.map((cite, cIdx) => (
                      <div
                        key={cIdx}
                        onClick={() => onSelectDocumentById(cite.document_id)}
                        className="p-3 bg-[#F7F5F0] border border-[#8A7B4F]/30 hover:border-[#2B3A55] cursor-pointer transition-colors space-y-1.5 group"
                      >
                        <div className="flex items-center justify-between text-[11px]">
                          <span className="font-mono font-bold text-[#2B3A55] group-hover:underline flex items-center gap-1">
                            <FileText className="w-3 h-3" />
                            {cite.filename}
                          </span>
                          <span className="font-mono text-[#8A7B4F]">
                            PG {cite.page_number} · {(cite.relevance_score * 100).toFixed(0)}%
                          </span>
                        </div>

                        <p className="text-xs text-[#211F1C]/85 font-sans line-clamp-2 italic border-l border-[#8A7B4F]/30 pl-2">
                          "{cite.snippet_text}"
                        </p>

                        <div className="flex items-center justify-between text-[10px] font-mono text-[#8A7B4F]">
                          <span>BLOCK ID: #{cite.block_id}</span>
                          <span className="flex items-center gap-0.5 text-[#2B3A55]">
                            Inspect filed doc <CornerDownRight className="w-2.5 h-2.5" />
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
