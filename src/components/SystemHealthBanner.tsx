import React, { useEffect, useState } from "react";
import { SystemHealth } from "../types";
import { ShieldCheck, Cpu, HardDrive, Zap, CheckCircle2, RefreshCw } from "lucide-react";

export const SystemHealthBanner: React.FC = () => {
  const [health, setHealth] = useState<SystemHealth | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const fetchHealth = () => {
    setIsLoading(true);
    fetch("/api/v1/system/health")
      .then((res) => res.json())
      .then((data) => setHealth(data))
      .catch((err) => console.error("Health check error:", err))
      .finally(() => setIsLoading(false));
  };

  useEffect(() => {
    fetchHealth();
  }, []);

  if (!health) {
    return (
      <div className="p-8 text-center text-xs font-mono text-[#8A7B4F]">
        Loading System Model Registry...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Top Status Header */}
      <div className="bg-[#FAF8F5] border border-[#8A7B4F]/30 p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="font-display font-bold text-lg text-[#211F1C]">
              Model Registry & Platform Observability
            </h2>
            <span className="px-2 py-0.5 text-[11px] font-mono bg-[#2B3A55] text-[#F7F5F0]">
              STATUS: OPERATIONAL
            </span>
          </div>
          <p className="text-xs text-[#211F1C]/70 mt-0.5">
            Real-time status of Scikit-Learn pipelines, sentence-transformer FAISS indices, and LangGraph runtime metrics.
          </p>
        </div>

        <button
          onClick={fetchHealth}
          className="px-3.5 py-1.5 border border-[#8A7B4F]/40 bg-[#F7F5F0] hover:bg-[#8A7B4F]/10 text-xs font-mono text-[#211F1C] flex items-center gap-1.5 transition-colors self-start sm:self-auto"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? "animate-spin text-[#2B3A55]" : ""}`} />
          <span>Refresh Telemetry</span>
        </button>
      </div>

      {/* Telemetry Metrics Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-4 border border-[#8A7B4F]/30 bg-[#F7F5F0] space-y-1">
          <div className="text-xs font-mono text-[#8A7B4F]">TOTAL DOCUMENTS FILED</div>
          <div className="font-display font-bold text-2xl text-[#2B3A55]">
            {health.telemetry.total_documents_filed}
          </div>
          <div className="text-[11px] text-[#211F1C]/70">Verified & indexed</div>
        </div>

        <div className="p-4 border border-[#8A7B4F]/30 bg-[#F7F5F0] space-y-1">
          <div className="text-xs font-mono text-[#8A7B4F]">INDEXED FAISS VECTORS</div>
          <div className="font-display font-bold text-2xl text-[#2B3A55]">
            {health.telemetry.total_layout_blocks_indexed}
          </div>
          <div className="text-[11px] text-[#211F1C]/70">384-dimensional dense vectors</div>
        </div>

        <div className="p-4 border border-[#8A7B4F]/30 bg-[#F7F5F0] space-y-1">
          <div className="text-xs font-mono text-[#8A7B4F]">OCR SEGMENTATION SPEED</div>
          <div className="font-display font-bold text-2xl text-[#2B3A55]">
            ~{health.telemetry.mean_ocr_latency_ms}ms
          </div>
          <div className="text-[11px] text-[#211F1C]/70">Heuristic BBox analyzer</div>
        </div>

        <div className="p-4 border border-[#8A7B4F]/30 bg-[#F7F5F0] space-y-1">
          <div className="text-xs font-mono text-[#8A7B4F]">SCHEMA VALIDATION PASS RATE</div>
          <div className="font-display font-bold text-2xl text-[#2B3A55]">
            {health.telemetry.validation_pass_rate}
          </div>
          <div className="text-[11px] text-[#211F1C]/70">LangGraph self-repair loop enabled</div>
        </div>
      </div>

      {/* Model Artifact Registry Cards */}
      <div className="border border-[#8A7B4F]/30 bg-[#FAF8F5] p-5 space-y-4">
        <div className="border-b border-[#8A7B4F]/20 pb-2 flex items-center justify-between">
          <h3 className="font-display font-bold text-base text-[#211F1C]">
            Active Registered ML Artifacts (Hot-Loaded)
          </h3>
          <span className="text-xs font-mono text-[#8A7B4F]">ADR-003 Lineage Compliant</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {health.registered_models.map((model, idx) => (
            <div key={idx} className="p-4 bg-[#F7F5F0] border border-[#8A7B4F]/30 space-y-3">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-[#2B3A55]">
                  {model.name}
                </span>
                <span className="stamp-box stamp-verified text-[10px]">
                  {model.status}
                </span>
              </div>

              <div className="text-xs text-[#211F1C]/80 font-sans">
                {model.type}
              </div>

              <div className="pt-2 border-t border-[#8A7B4F]/20 text-[11px] font-mono text-[#8A7B4F] space-y-1">
                {model.version && <div>VERSION: {model.version}</div>}
                {model.classes && <div>CLASSES: {model.classes.length} labeled types</div>}
                {model.dimension && <div>DIMENSION: {model.dimension}</div>}
                {model.sha256 && <div className="truncate">SHA256: {model.sha256}</div>}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
