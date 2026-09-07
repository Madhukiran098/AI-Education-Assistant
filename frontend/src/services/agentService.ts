import { API_ENDPOINTS } from "../config/api";
import type { AgentRequest, AgentResponse } from "../types/agent";

export async function runAgent(
  data: AgentRequest
): Promise<AgentResponse> {
  const response = await fetch(API_ENDPOINTS.runAgent, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorText = await response.text();

    throw new Error(
      `Backend error ${response.status}: ${errorText}`
    );
  }

  const result: AgentResponse = await response.json();

  return result;
}