import React, { useState, useEffect } from "react";
import { Folder, FileText, ChevronRight, ChevronDown, Check, Code, Shield } from "lucide-react";

interface TreeNode {
  name: string;
  path: string;
  type: "file" | "directory";
  size?: number;
  children?: TreeNode[];
}

export const RepoExplorer: React.FC = () => {
  const [tree, setTree] = useState<TreeNode[]>([]);
  const [selectedPath, setSelectedPath] = useState<string>("docs/adr/ADR-001-service-boundaries.md");
  const [fileContent, setFileContent] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [expandedDirs, setExpandedDirs] = useState<Record<string, boolean>>({
    docs: true,
    "docs/adr": true,
    backend: true,
    "backend/app": true,
    "backend/app/domains": true,
    ml: true,
    ".github": true,
  });

  // Fetch repository tree
  useEffect(() => {
    fetch("/api/v1/repo/tree")
      .then((res) => res.json())
      .then((data) => {
        if (data.root) setTree(data.root);
      })
      .catch((err) => console.error("Failed to load repo tree:", err));
  }, []);

  // Fetch file content when selectedPath changes
  useEffect(() => {
    if (!selectedPath) return;
    setIsLoading(true);
    fetch(`/api/v1/repo/file?path=${encodeURIComponent(selectedPath)}`)
      .then((res) => res.json())
      .then((data) => {
        setFileContent(data.content || "// Unable to load file content");
      })
      .catch((err) => {
        setFileContent("// Error loading file");
      })
      .finally(() => setIsLoading(false));
  }, [selectedPath]);

  const toggleDir = (path: string) => {
    setExpandedDirs((prev) => ({ ...prev, [path]: !prev[path] }));
  };

  const ADR_SHORTCUTS = [
    { id: "ADR-001", file: "docs/adr/ADR-001-service-boundaries.md", label: "Service Boundaries" },
    { id: "ADR-002", file: "docs/adr/ADR-002-async-backend.md", label: "Async FastAPI & DB" },
    { id: "ADR-003", file: "docs/adr/ADR-003-model-artifact-versioning.md", label: "Model Artifacts" },
    { id: "ADR-004", file: "docs/adr/ADR-004-langgraph-state-design.md", label: "LangGraph State" },
    { id: "ADR-005", file: "docs/adr/ADR-005-frontend-architecture.md", label: "Frontend & Ledger UI" },
    { id: "ADR-006", file: "docs/adr/ADR-006-observability.md", label: "Observability & Tracing" },
  ];

  const renderTree = (nodes: TreeNode[], depth = 0) => {
    return nodes.map((node) => {
      const isDir = node.type === "directory";
      const isExpanded = expandedDirs[node.path];
      const isSelected = selectedPath === node.path;

      return (
        <div key={node.path} className="select-none">
          <div
            onClick={() => {
              if (isDir) toggleDir(node.path);
              else setSelectedPath(node.path);
            }}
            style={{ paddingLeft: `${depth * 14 + 10}px` }}
            className={`py-1 pr-2 flex items-center gap-1.5 text-xs font-mono cursor-pointer transition-colors ${
              isSelected
                ? "bg-[#2B3A55] text-[#F7F5F0] font-semibold"
                : "text-[#211F1C]/85 hover:bg-[#8A7B4F]/15"
            }`}
          >
            {isDir ? (
              <>
                {isExpanded ? (
                  <ChevronDown className="w-3.5 h-3.5 text-[#8A7B4F] shrink-0" />
                ) : (
                  <ChevronRight className="w-3.5 h-3.5 text-[#8A7B4F] shrink-0" />
                )}
                <Folder className="w-3.5 h-3.5 text-[#8A7B4F] shrink-0" />
              </>
            ) : (
              <>
                <span className="w-3.5" />
                <FileText className="w-3.5 h-3.5 text-[#8A7B4F] shrink-0" />
              </>
            )}
            <span className="truncate">{node.name}</span>
          </div>

          {isDir && isExpanded && node.children && (
            <div>{renderTree(node.children, depth + 1)}</div>
          )}
        </div>
      );
    });
  };

  return (
    <div className="space-y-6">
      {/* Top ADR Quick Index Bar */}
      <div className="bg-[#FAF8F5] border border-[#8A7B4F]/30 p-4 space-y-3">
        <div className="flex items-center justify-between border-b border-[#8A7B4F]/20 pb-2">
          <div>
            <h2 className="font-display font-bold text-lg text-[#211F1C]">
              Architecture Decision Records (ADR Catalog)
            </h2>
            <p className="text-xs text-[#211F1C]/70">
              Formal engineering specs governing domain boundaries, async ORM layering, model registries, LangGraph state design, and observability.
            </p>
          </div>
          <span className="px-2 py-0.5 text-xs font-mono bg-[#2B3A55] text-[#F7F5F0]">
            6/6 ACCEPTED
          </span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2">
          {ADR_SHORTCUTS.map((adr) => (
            <button
              key={adr.id}
              onClick={() => setSelectedPath(adr.file)}
              className={`p-2 border text-left transition-colors text-xs ${
                selectedPath === adr.file
                  ? "border-[#2B3A55] bg-[#2B3A55] text-[#F7F5F0]"
                  : "border-[#8A7B4F]/30 bg-[#F7F5F0] hover:bg-[#8A7B4F]/10 text-[#211F1C]"
              }`}
            >
              <div className="font-mono font-bold text-[10px] opacity-80">{adr.id}</div>
              <div className="font-display font-semibold truncate mt-0.5">{adr.label}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Codebase File Explorer (Split Pane) */}
      <div className="border border-[#8A7B4F]/30 bg-[#F7F5F0] grid grid-cols-1 lg:grid-cols-12 min-h-[580px] divide-y lg:divide-y-0 lg:divide-x divide-[#8A7B4F]/30">
        {/* Left Pane: Tree View */}
        <div className="lg:col-span-4 p-3 bg-[#FAF8F5] overflow-y-auto max-h-[640px] space-y-2">
          <div className="px-2 py-1 text-xs font-mono text-[#8A7B4F] border-b border-[#8A7B4F]/20 flex items-center justify-between">
            <span>REPOSITORY EXPLORER</span>
            <span>docintel/</span>
          </div>
          <div>{tree.length > 0 ? renderTree(tree) : <p className="text-xs font-mono text-[#8A7B4F] p-2">Loading repository files...</p>}</div>
        </div>

        {/* Right Pane: Code / Markdown Viewer */}
        <div className="lg:col-span-8 flex flex-col bg-[#F7F5F0]">
          <div className="px-4 py-2.5 bg-[#F2EFE9] border-b border-[#8A7B4F]/30 flex items-center justify-between">
            <div className="flex items-center gap-2 font-mono text-xs text-[#211F1C]">
              <Code className="w-4 h-4 text-[#8A7B4F]" />
              <span className="font-semibold">{selectedPath}</span>
            </div>
            <span className="text-[11px] font-mono text-[#8A7B4F]">
              {fileContent.split("\n").length} lines
            </span>
          </div>

          <div className="p-4 flex-1 overflow-y-auto max-h-[590px]">
            {isLoading ? (
              <div className="p-6 text-xs font-mono text-[#8A7B4F] animate-pulse">
                Loading file contents...
              </div>
            ) : (
              <pre className="text-xs font-mono text-[#211F1C] leading-relaxed whitespace-pre-wrap selection:bg-[#2B3A55]/20">
                {fileContent}
              </pre>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
