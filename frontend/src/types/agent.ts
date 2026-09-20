export interface AgentRequest {
  task: string;
}

export interface ResearchResult {
  topic: string;
  information: string;
  tools_used?: string[];
  tool_results?: Record<string, unknown>[];
}

export interface AnalysisResult {
  topic: string;
  analysis: string;
  tools_used?: string[];
}

export interface DecisionResult {
  topic: string;
  decision: string;
}

export interface ToolSelection {
  success: boolean;
  tool_name?: string;
  confidence?: number;
  parameters?: Record<string, unknown>;
  reason?: string;
}

export interface ToolExecution {
  success: boolean;
  tool_name?: string;
  data?: unknown;
  error?: string | null;
  execution_time?: number;
}

export interface ToolStatistics {
  total_executions: number;
  successful_executions: number;
  failed_executions: number;
  success_rate: number;
}

export interface ExecutionTrace {
  step?: string;
  agent?: string;
  tool?: string;
  selected_tool?: string;
  confidence?: number;
  parameters?: Record<string, unknown>;
  execution_success?: boolean;
  status?: string;
}

export interface AgentResponse {
  request: string;
  plan: string;

  research: ResearchResult;

  selected_tool?: string;
  tool_selection?: ToolSelection;
  tool_execution?: ToolExecution;

  analysis: AnalysisResult;

  report?: unknown;

  decision: DecisionResult;

  execution_trace?: ExecutionTrace[];

  tool_statistics?: ToolStatistics;
}