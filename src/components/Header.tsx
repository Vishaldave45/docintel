import React from "react";
import { FileText, Search, Database, Plus, ShieldCheck, HardDrive } from "lucide-react";

interface HeaderProps {
  activeTab: "library" | "rag" | "architecture" | "telemetry";
  onTabChange: (tab: "library" | "rag" | "architecture" | "telemetry") => void;
  onOpenIngestModal: () => void;
  totalDocuments: number;
}

export const Header: React.FC<HeaderProps> = ({
  activeTab,
  onTabChange,
  onOpenIngestModal,
  totalDocuments,
}) => {
  return (
    <header className="border-b border-[#8A7B4F]/30 bg-[#F7F5F0] sticky top-0 z-30">
      {/* Top Ledger Utility Rule */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand & Archival Heading */}
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 bg-[#2B3A55] text-[#F7F5F0] flex items-center justify-center font-display font-bold text-lg rounded-none border border-[#211F1C]">
              D
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-display font-bold text-xl text-[#211F1C] tracking-tight">
                  DocIntel
                </span>
                <span className="inline-block px-1.5 py-0.5 text-[10px] font-mono text-[#8A7B4F] border border-[#8A7B4F]/40 bg-[#8A7B4F]/5">
                  v1.2.0-PROD
                </span>
              </div>
              <p className="text-xs text-[#211F1C]/70">
                Multimodal Document Filing & Knowledge Engine
              </p>
            </div>
          </div>

          {/* Navigation Tabs (Structural filing tabs) */}
          <nav className="flex items-center gap-1">
            <button
              onClick={() => onTabChange("library")}
              className={`px-3.5 py-2 text-sm font-medium transition-colors border-b-2 flex items-center gap-1.5 ${
                activeTab === "library"
                  ? "border-[#2B3A55] text-[#2B3A55] bg-[#2B3A55]/5"
                  : "border-transparent text-[#211F1C]/70 hover:text-[#211F1C] hover:bg-[#8A7B4F]/10"
              }`}
            >
              <FileText className="w-4 h-4 text-[#8A7B4F]" />
              <span>Document Library</span>
              <span className="font-mono text-xs text-[#8A7B4F] ml-1">
                ({totalDocuments})
              </span>
            </button>

            <button
              onClick={() => onTabChange("rag")}
              className={`px-3.5 py-2 text-sm font-medium transition-colors border-b-2 flex items-center gap-1.5 ${
                activeTab === "rag"
                  ? "border-[#2B3A55] text-[#2B3A55] bg-[#2B3A55]/5"
                  : "border-transparent text-[#211F1C]/70 hover:text-[#211F1C] hover:bg-[#8A7B4F]/10"
              }`}
            >
              <Search className="w-4 h-4 text-[#8A7B4F]" />
              <span>Corpus RAG & Citations</span>
            </button>

            <button
              onClick={() => onTabChange("architecture")}
              className={`px-3.5 py-2 text-sm font-medium transition-colors border-b-2 flex items-center gap-1.5 ${
                activeTab === "architecture"
                  ? "border-[#2B3A55] text-[#2B3A55] bg-[#2B3A55]/5"
                  : "border-transparent text-[#211F1C]/70 hover:text-[#211F1C] hover:bg-[#8A7B4F]/10"
              }`}
            >
              <Database className="w-4 h-4 text-[#8A7B4F]" />
              <span>Architecture & ADRs</span>
            </button>

            <button
              onClick={() => onTabChange("telemetry")}
              className={`px-3.5 py-2 text-sm font-medium transition-colors border-b-2 flex items-center gap-1.5 ${
                activeTab === "telemetry"
                  ? "border-[#2B3A55] text-[#2B3A55] bg-[#2B3A55]/5"
                  : "border-transparent text-[#211F1C]/70 hover:text-[#211F1C] hover:bg-[#8A7B4F]/10"
              }`}
            >
              <ShieldCheck className="w-4 h-4 text-[#8A7B4F]" />
              <span>ML Registry & Health</span>
            </button>
          </nav>

          {/* Action: Ingest Document Button */}
          <div className="flex items-center gap-3">
            <button
              onClick={onOpenIngestModal}
              className="px-4 py-2 bg-[#2B3A55] text-[#F7F5F0] hover:bg-[#211F1C] text-sm font-medium transition-colors flex items-center gap-2 border border-[#211F1C]"
            >
              <Plus className="w-4 h-4" />
              <span>File New Document</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};
