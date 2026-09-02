import React, { useState, useEffect } from "react";
import { Header } from "./components/Header";
import { IndexCard } from "./components/IndexCard";
import { DocumentDetailDrawer } from "./components/DocumentDetailDrawer";
import { RAGMarginalView } from "./components/RAGMarginalView";
import { IngestModal } from "./components/IngestModal";
import { RepoExplorer } from "./components/RepoExplorer";
import { SystemHealthBanner } from "./components/SystemHealthBanner";
import { DocumentItem } from "./types";
import {
  FileText,
  Filter,
  Search,
  Plus,
  ArrowUpDown,
  BookOpen,
  FolderOpen,
  CheckCircle2,
  AlertTriangle,
} from "lucide-react";

export default function App() {
  const [activeTab, setActiveTab] = useState<"library" | "rag" | "architecture" | "telemetry">("library");
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [selectedType, setSelectedType] = useState<string>("all");
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [selectedDocument, setSelectedDocument] = useState<DocumentItem | null>(null);
  const [isIngestModalOpen, setIsIngestModalOpen] = useState<boolean>(false);
  const [isReExtracting, setIsReExtracting] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const fetchDocuments = async () => {
    setIsLoading(true);
    try {
      const res = await fetch("/api/v1/documents");
      if (res.ok) {
        const data = await res.json();
        setDocuments(data.documents || []);
        // update selected document if open
        if (selectedDocument) {
          const updated = data.documents?.find((d: DocumentItem) => d.id === selectedDocument.id);
          if (updated) setSelectedDocument(updated);
        }
      }
    } catch (err) {
      console.error("Failed to load documents:", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleReExtract = async (id: string) => {
    setIsReExtracting(true);
    try {
      const res = await fetch(`/api/v1/documents/${id}/re-extract`, { method: "POST" });
      if (res.ok) {
        const updated = await res.json();
        setSelectedDocument(updated);
        await fetchDocuments();
      }
    } catch (err) {
      console.error("Re-extraction failed:", err);
    } finally {
      setIsReExtracting(false);
    }
  };

  const handleSelectById = (id: string) => {
    const target = documents.find((d) => d.id === id);
    if (target) {
      setSelectedDocument(target);
    }
  };

  // Filter documents
  const filteredDocuments = documents.filter((doc) => {
    const matchesType = selectedType === "all" || doc.document_type === selectedType;
    const matchesQuery =
      !searchQuery ||
      doc.filename.toLowerCase().includes(searchQuery.toLowerCase()) ||
      doc.raw_ocr_text.toLowerCase().includes(searchQuery.toLowerCase()) ||
      doc.target_schema.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesType && matchesQuery;
  });

  const reviewCount = documents.filter((d) => d.extraction_status === "needs_review").length;

  return (
    <div className="min-h-screen bg-[#F7F5F0] text-[#211F1C] flex flex-col font-sans selection:bg-[#2B3A55]/15">
      {/* Top Main Navigation Header */}
      <Header
        activeTab={activeTab}
        onTabChange={setActiveTab}
        onOpenIngestModal={() => setIsIngestModalOpen(true)}
        totalDocuments={documents.length}
      />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* =================================================================== */}
        {/* VIEW 1: DOCUMENT LIBRARY (Physical Index Card Filing System)       */}
        {/* =================================================================== */}
        {activeTab === "library" && (
          <div className="space-y-6">
            {/* Ledger Filter & Search Sub-Header Bar */}
            <div className="bg-[#FAF8F5] border border-[#8A7B4F]/30 p-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
              {/* Category Filter Tabs */}
              <div className="flex items-center gap-1.5 flex-wrap">
                <span className="text-xs font-mono text-[#8A7B4F] mr-1 flex items-center gap-1">
                  <Filter className="w-3.5 h-3.5" /> TYPE:
                </span>
                {[
                  { id: "all", label: "All Records", tag: "ALL" },
                  { id: "invoice", label: "Invoices", tag: "INV" },
                  { id: "contract", label: "Contracts", tag: "CTR" },
                  { id: "financial_report", label: "Reports", tag: "REP" },
                  { id: "identification", label: "ID Cards", tag: "ID" },
                ].map((cat) => (
                  <button
                    key={cat.id}
                    onClick={() => setSelectedType(cat.id)}
                    className={`px-3 py-1.5 text-xs font-medium transition-colors border ${
                      selectedType === cat.id
                        ? "border-[#2B3A55] bg-[#2B3A55] text-[#F7F5F0]"
                        : "border-[#8A7B4F]/30 bg-[#F7F5F0] text-[#211F1C]/80 hover:bg-[#8A7B4F]/10"
                    }`}
                  >
                    <span className="font-mono text-[10px] opacity-75 mr-1">[{cat.tag}]</span>
                    <span>{cat.label}</span>
                  </button>
                ))}
              </div>

              {/* Search Box & Review Alert Counter */}
              <div className="flex items-center gap-3">
                {reviewCount > 0 && (
                  <div className="px-2.5 py-1 bg-[#B33A2E]/10 border border-[#B33A2E]/30 text-xs font-mono text-[#B33A2E] flex items-center gap-1.5">
                    <AlertTriangle className="w-3.5 h-3.5" />
                    <span>{reviewCount} Needs Review</span>
                  </div>
                )}

                <div className="relative w-full md:w-64">
                  <Search className="w-3.5 h-3.5 text-[#8A7B4F] absolute left-3 top-2.5" />
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search ledger records..."
                    className="w-full pl-8 pr-3 py-1.5 text-xs bg-[#F7F5F0] border border-[#8A7B4F]/40 text-[#211F1C] placeholder-[#211F1C]/40 focus:outline-none focus:border-[#2B3A55] font-sans"
                  />
                </div>
              </div>
            </div>

            {/* Document Index Cards Grid */}
            {isLoading ? (
              <div className="p-12 text-center text-xs font-mono text-[#8A7B4F] animate-pulse">
                Loading physical index cabinet records...
              </div>
            ) : filteredDocuments.length === 0 ? (
              <div className="p-12 text-center border border-dashed border-[#8A7B4F]/40 bg-[#FAF8F5] space-y-3">
                <FolderOpen className="w-8 h-8 text-[#8A7B4F] mx-auto opacity-70" />
                <h3 className="font-display font-semibold text-base text-[#211F1C]">
                  No filed documents match the current filter
                </h3>
                <p className="text-xs text-[#211F1C]/70 max-w-sm mx-auto">
                  Upload your first document or click below to ingest a benchmark archival sample into the corpus.
                </p>
                <button
                  onClick={() => setIsIngestModalOpen(true)}
                  className="px-4 py-2 bg-[#2B3A55] text-[#F7F5F0] text-xs font-medium hover:bg-[#211F1C] transition-colors"
                >
                  File New Document
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                {filteredDocuments.map((doc) => (
                  <IndexCard
                    key={doc.id}
                    document={doc}
                    isSelected={selectedDocument?.id === doc.id}
                    onSelect={(d) => setSelectedDocument(d)}
                  />
                ))}
              </div>
            )}
          </div>
        )}

        {/* =================================================================== */}
        {/* VIEW 2: CORPUS RAG & ANNOTATED MARGIN QUERY                        */}
        {/* =================================================================== */}
        {activeTab === "rag" && (
          <RAGMarginalView onSelectDocumentById={handleSelectById} />
        )}

        {/* =================================================================== */}
        {/* VIEW 3: ARCHITECTURE & ADR REPOSITORY EXPLORER                     */}
        {/* =================================================================== */}
        {activeTab === "architecture" && <RepoExplorer />}

        {/* =================================================================== */}
        {/* VIEW 4: MODEL REGISTRY & TELEMETRY                                 */}
        {/* =================================================================== */}
        {activeTab === "telemetry" && <SystemHealthBanner />}
      </main>

      {/* Slide-over Inspection Drawer for Active Document */}
      <DocumentDetailDrawer
        document={selectedDocument}
        onClose={() => setSelectedDocument(null)}
        onReExtract={handleReExtract}
        isReExtracting={isReExtracting}
      />

      {/* Ingestion & Upload Modal */}
      <IngestModal
        isOpen={isIngestModalOpen}
        onClose={() => setIsIngestModalOpen(false)}
        onIngestSuccess={() => {
          fetchDocuments();
          setActiveTab("library");
        }}
      />
    </div>
  );
}
