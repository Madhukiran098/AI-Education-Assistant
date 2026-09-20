
import { useState } from "react";
import { runAgent } from "../services/agentService";
import type { AgentResponse } from "../types/agent";

function Dashboard() {
  const [request, setRequest] = useState("");
  const [result, setResult] = useState<AgentResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleRunAgent = async () => {
    if (!request.trim()) {
      setError("Please enter a request.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await runAgent({
        task: request,
      });

      setResult(response);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong while connecting to the backend."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="mx-auto max-w-7xl">

        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900">
            AI Education Assistant
          </h1>

          <p className="mt-2 text-gray-600">
            Your intelligent multi-agent assistant for personalized
            education, learning, and career guidance.
          </p>
        </div>

        <div className="rounded-xl bg-white p-6 shadow-md">
          <h2 className="mb-4 text-xl font-semibold text-gray-800">
            Ask Your Assistant
          </h2>

          <textarea
            value={request}
            onChange={(e) => setRequest(e.target.value)}
            placeholder="Example: How can AI help students choose the right career?"
            className="h-32 w-full rounded-lg border border-gray-300 p-4 outline-none focus:border-blue-500"
          />

          <button
            onClick={handleRunAgent}
            disabled={loading}
            className="mt-4 rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-gray-400"
          >
            {loading ? "Running Agents..." : "Run Analysis"}
          </button>

          {error && (
            <div className="mt-4 rounded-lg border border-red-300 bg-red-50 p-4 text-red-700">
              <strong>Error:</strong> {error}
            </div>
          )}
        </div>

        {result && (
          <div className="mt-6 space-y-6">

            <div className="rounded-xl bg-white p-6 shadow-md">
              <h2 className="mb-2 text-xl font-semibold text-gray-800">
                User Task
              </h2>

              <p className="text-gray-700">
                {result.request}
              </p>
            </div>

            <div className="rounded-xl bg-white p-6 shadow-md">
              <h2 className="text-2xl font-bold text-gray-900">
                Milestone 2 — Tool Integration
              </h2>

              <p className="mt-1 text-gray-600">
                Tools are selected and executed as part of the
                multi-agent workflow.
              </p>

              <div className="mt-5 grid gap-4 md:grid-cols-3">

                <div className="rounded-lg border bg-gray-50 p-5">
                  <p className="text-sm font-medium text-gray-500">
                    Selected Tool
                  </p>

                  <p className="mt-2 text-xl font-bold text-blue-600">
                    {result.selected_tool ||
                      result.tool_selection?.tool_name ||
                      "No tool selected"}
                  </p>

                  {result.tool_selection?.confidence !== undefined && (
                    <p className="mt-2 text-sm text-gray-600">
                      Confidence:{" "}
                      {Math.round(
                        result.tool_selection.confidence * 100
                      )}
                      %
                    </p>
                  )}
                </div>

                <div className="rounded-lg border bg-gray-50 p-5">
                  <p className="text-sm font-medium text-gray-500">
                    Tool Execution
                  </p>

                  <p className="mt-2 text-xl font-bold">
                    {result.tool_execution?.success
                      ? "Successful"
                      : "Not executed"}
                  </p>

                  {result.tool_execution?.execution_time !== undefined && (
                    <p className="mt-2 text-sm text-gray-600">
                      Execution time:{" "}
                      {result.tool_execution.execution_time.toFixed(3)}s
                    </p>
                  )}
                </div>

                <div className="rounded-lg border bg-gray-50 p-5">
                  <p className="text-sm font-medium text-gray-500">
                    Tools Used
                  </p>

                  <div className="mt-2">
                    {result.research?.tools_used &&
                    result.research.tools_used.length > 0 ? (
                      result.research.tools_used.map((tool, index) => (
                        <span
                          key={index}
                          className="mr-2 mb-2 inline-block rounded-full bg-blue-100 px-3 py-1 text-sm font-medium text-blue-700"
                        >
                          {tool}
                        </span>
                      ))
                    ) : (
                      <span className="text-gray-600">
                        No tools recorded
                      </span>
                    )}
                  </div>
                </div>

              </div>

              {result.tool_selection?.reason && (
                <div className="mt-4 rounded-lg bg-blue-50 p-4">
                  <p className="font-semibold text-blue-900">
                    Tool Selection Reason
                  </p>

                  <p className="mt-1 text-blue-800">
                    {result.tool_selection.reason}
                  </p>
                </div>
              )}

              {result.tool_statistics && (
                <div className="mt-6">
                  <h3 className="mb-4 text-lg font-semibold text-gray-800">
                    Tool Statistics
                  </h3>

                  <div className="grid gap-4 md:grid-cols-4">

                    <div className="rounded-lg border bg-gray-50 p-4">
                      <p className="text-sm text-gray-500">
                        Total Executions
                      </p>

                      <p className="mt-1 text-2xl font-bold">
                        {result.tool_statistics.total_executions}
                      </p>
                    </div>

                    <div className="rounded-lg border bg-gray-50 p-4">
                      <p className="text-sm text-gray-500">
                        Successful
                      </p>

                      <p className="mt-1 text-2xl font-bold">
                        {result.tool_statistics.successful_executions}
                      </p>
                    </div>

                    <div className="rounded-lg border bg-gray-50 p-4">
                      <p className="text-sm text-gray-500">
                        Failed
                      </p>

                      <p className="mt-1 text-2xl font-bold">
                        {result.tool_statistics.failed_executions}
                      </p>
                    </div>

                    <div className="rounded-lg border bg-gray-50 p-4">
                      <p className="text-sm text-gray-500">
                        Success Rate
                      </p>

                      <p className="mt-1 text-2xl font-bold">
                        {result.tool_statistics.success_rate}%
                      </p>
                    </div>

                  </div>
                </div>
              )}
            </div>

            {result.execution_trace &&
              result.execution_trace.length > 0 && (
                <div className="rounded-xl bg-white p-6 shadow-md">
                  <h2 className="mb-5 text-xl font-semibold text-gray-800">
                    Execution History
                  </h2>

                  <div className="space-y-3">
                    {result.execution_trace.map((trace, index) => (
                      <div
                        key={index}
                        className="flex items-center justify-between rounded-lg border bg-gray-50 p-4"
                      >
                        <div>
                          <p className="font-semibold text-gray-800">
                            {trace.step ||
                              trace.agent ||
                              "Step " + (index + 1)}
                          </p>

                          {trace.agent && (
                            <p className="text-sm text-gray-600">
                              Agent: {trace.agent}
                            </p>
                          )}

                          {trace.tool && (
                            <p className="text-sm text-gray-600">
                              Tool: {trace.tool}
                            </p>
                          )}
                        </div>

                        <div className="text-right">
                          {trace.status && (
                            <p className="text-sm font-medium text-gray-700">
                              {trace.status}
                            </p>
                          )}

                          {trace.execution_success !== undefined && (
                            <p
                              className={
                                trace.execution_success
                                  ? "text-sm font-semibold text-green-600"
                                  : "text-sm font-semibold text-red-600"
                              }
                            >
                              {trace.execution_success
                                ? "Success"
                                : "Failed"}
                            </p>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

            <div className="rounded-xl bg-white p-6 shadow-md">
              <h2 className="mb-5 text-xl font-semibold text-gray-800">
                Agent Workflow
              </h2>

              <div className="grid gap-4 md:grid-cols-4">

                <div className="rounded-lg border border-blue-200 bg-blue-50 p-5">
                  <h3 className="font-bold text-blue-900">
                    1. Planner Agent
                  </h3>

                  <p className="mt-2 text-sm text-blue-800">
                    Creates an execution plan for the user's request.
                  </p>
                </div>

                <div className="rounded-lg border border-purple-200 bg-purple-50 p-5">
                  <h3 className="font-bold text-purple-900">
                    2. Research Agent
                  </h3>

                  <p className="mt-2 text-sm text-purple-800">
                    Retrieves information and selects appropriate tools.
                  </p>
                </div>

                <div className="rounded-lg border border-orange-200 bg-orange-50 p-5">
                  <h3 className="font-bold text-orange-900">
                    3. Analysis Agent
                  </h3>

                  <p className="mt-2 text-sm text-orange-800">
                    Analyses collected information and tool results.
                  </p>
                </div>

                <div className="rounded-lg border border-green-200 bg-green-50 p-5">
                  <h3 className="font-bold text-green-900">
                    4. Decision Agent
                  </h3>

                  <p className="mt-2 text-sm text-green-800">
                    Produces the final recommendation or decision.
                  </p>
                </div>

              </div>
            </div>

            {result.plan && (
              <div className="rounded-xl bg-white p-6 shadow-md">
                <h2 className="mb-3 text-xl font-semibold text-gray-800">
                  Planner Agent
                </h2>

                <div className="whitespace-pre-wrap rounded-lg bg-gray-50 p-4 text-gray-700">
                  {result.plan}
                </div>
              </div>
            )}

            {result.research && (
              <div className="rounded-xl bg-white p-6 shadow-md">
                <h2 className="mb-3 text-xl font-semibold text-gray-800">
                  Research Agent
                </h2>

                <div className="rounded-lg bg-gray-50 p-4">
                  <p className="mb-2 font-semibold text-gray-800">
                    Topic
                  </p>

                  <p className="mb-4 text-gray-700">
                    {result.research.topic}
                  </p>

                  <p className="mb-2 font-semibold text-gray-800">
                    Information
                  </p>

                  <div className="whitespace-pre-wrap text-gray-700">
                    {result.research.information}
                  </div>
                </div>
              </div>
            )}

            {result.analysis && (
              <div className="rounded-xl bg-white p-6 shadow-md">
                <h2 className="mb-3 text-xl font-semibold text-gray-800">
                  Analysis Agent
                </h2>

                <div className="whitespace-pre-wrap rounded-lg bg-gray-50 p-4 text-gray-700">
                  {result.analysis.analysis}
                </div>
              </div>
            )}

            {result.decision && (
              <div className="rounded-xl bg-white p-6 shadow-md">
                <h2 className="mb-3 text-xl font-semibold text-gray-800">
                  Final Decision
                </h2>

                <div className="rounded-lg border border-green-200 bg-green-50 p-5">
                  <p className="whitespace-pre-wrap text-gray-800">
                    {result.decision.decision}
                  </p>
                </div>
              </div>
            )}

          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;

