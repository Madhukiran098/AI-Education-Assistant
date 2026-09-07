export interface AgentRequest {
  request: string;
}

export interface AgentResponse {
  request: string;
  plan: string;
  research: {
    topic: string;
    information: string;
  };
  analysis: {
    topic: string;
    analysis: string;
  };
  decision: {
    topic: string;
    decision: string;
  };
}