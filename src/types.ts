export interface LayoutBlock {
  id: string;
  block_type: "header" | "paragraph" | "table" | "key_value" | "signature" | "stamp" | "barcode";
  text: string;
  confidence: number;
  bbox: { x: number; y: number; width: number; height: number };
  page_number: number;
  reading_order: number;
}

export interface FeatureContribution {
  feature_ngram: string;
  weight: number;
}

export interface ExecutionTraceItem {
  node: string;
  decision?: string;
  status?: string;
  timestamp: string;
  errors?: string[];
  error_count?: number;
}

export interface DocumentItem {
  id: string;
  filename: string;
  content_type: string;
  file_size_bytes: number;
  page_count: number;
  document_type: "invoice" | "contract" | "financial_report" | "identification" | "receipt" | "general";
  classifier_confidence: number;
  classification_model_version: string;
  top_features: FeatureContribution[];
  raw_ocr_text: string;
  layout_blocks: LayoutBlock[];
  extraction_status: "completed" | "needs_review" | "verified" | "repaired";
  target_schema: string;
  extracted_fields: Record<string, any>;
  validation_errors: string[];
  repair_attempts: number;
  confidence_scores: Record<string, number>;
  execution_trace: ExecutionTraceItem[];
  is_indexed_in_faiss: boolean;
  created_at: string;
}

export interface SourceCitation {
  document_id: string;
  filename: string;
  document_type: string;
  page_number: number;
  block_id: string;
  snippet_text: string;
  relevance_score: number;
  line_number?: number;
}

export interface RAGResponse {
  query: string;
  answer: string;
  citations: SourceCitation[];
  retrieval_latency_ms: number;
  model_name: string;
  corpus_documents_searched: number;
}

export interface SystemModelStatus {
  name: string;
  type: string;
  version?: string;
  status: string;
  dimension?: number;
  classes?: string[];
  sha256?: string;
}

export interface SystemHealth {
  status: string;
  version: string;
  environment: string;
  registered_models: SystemModelStatus[];
  telemetry: {
    total_documents_filed: number;
    total_layout_blocks_indexed: number;
    mean_ocr_latency_ms: number;
    mean_extraction_latency_ms: number;
    validation_pass_rate: string;
  };
}
