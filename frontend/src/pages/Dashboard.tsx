import { useState } from "react";
import { runAgent } from "../services/agentService";
import type { AgentResponse } from "../types/agent";

export default function Dashboard() {
  const [request, setRequest] = useState("");
  const [response, setResponse] = useState<AgentResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleRunAgent = async () => {
    if (!request.trim()) {
      setError("Please enter a request");
      return;
    }

    setLoading(true);
    setError("");
    setResponse(null);

    try {
      // Send "task" because the FastAPI API expects:
      // {
      //   "task": "..."
      // }
      const result = await runAgent({
        request: request,
      });

      setResponse(result);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-8">

      <div className="max-w-6xl mx-auto">

        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold">
            AI Decision Intelligence
          </h1>

          <p className="mt-2 text-slate-400">
            Coordinate specialized AI agents to analyze business problems.
          </p>
        </div>

        {/* Request Section */}
        <div className="mt-8">

          <label className="block mb-2 text-sm font-medium text-slate-300">
            Enter Your Request
          </label>

          <textarea
            value={request}
            onChange={(e) => setRequest(e.target.value)}
            placeholder="Example: How can AI improve business decision making?"
            className="w-full h-32 rounded-xl bg-slate-900 border border-slate-700 p-4 text-white placeholder-slate-500 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 resize-none"
          />

          <button
            onClick={handleRunAgent}
            disabled={loading}
            className="mt-4 rounded-xl bg-blue-600 px-6 py-3 font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
          >
            {loading
              ? "Agents Processing..."
              : "Run Analysis"}
          </button>

        </div>

        {/* Loading */}
        {loading && (
          <div className="mt-6 rounded-xl bg-slate-900 border border-slate-700 p-5">

            <p className="text-blue-400 font-medium">
              AI agents are processing your request...
            </p>

            <p className="mt-2 text-sm text-slate-400">
              Planner → Research → Analysis → Decision
            </p>

          </div>
        )}

        {/* Error */}
        {error && (
          <div className="mt-6 rounded-xl bg-red-900/30 border border-red-700 p-4">

            <p className="text-red-300">
              {error}
            </p>

          </div>
        )}

        {/* Response */}
        {response && !loading && (
          <div className="mt-10 space-y-6">

            {/* User Task */}
            <section>
              <h2 className="text-xl font-semibold">
                📝 User Task
              </h2>

              <div className="mt-2 rounded-xl bg-slate-900 border border-slate-700 p-5">

                <p className="text-slate-300 whitespace-pre-wrap">
                  {response.request}
                </p>

              </div>
            </section>

            {/* Planner Agent */}
            <section>
              <h2 className="text-xl font-semibold">
                🧠 Planner Agent
              </h2>

              <div className="mt-2 rounded-xl bg-slate-900 border border-slate-700 p-5">

                <div className="whitespace-pre-wrap text-slate-300">
                  {response.plan}
                </div>

              </div>
            </section>

            {/* Research Agent */}
            <section>
              <h2 className="text-xl font-semibold">
                🔎 Research Agent
              </h2>

              <div className="mt-2 rounded-xl bg-slate-900 border border-slate-700 p-5">

                <p className="mb-3 text-sm text-slate-500">
                  Topic: {response.research.topic}
                </p>

                <div className="whitespace-pre-wrap text-slate-300">
                  {response.research.information}
                </div>

              </div>
            </section>

            {/* Analysis Agent */}
            <section>
              <h2 className="text-xl font-semibold">
                📊 Analysis Agent
              </h2>

              <div className="mt-2 rounded-xl bg-slate-900 border border-slate-700 p-5">

                <p className="mb-3 text-sm text-slate-500">
                  Topic: {response.analysis.topic}
                </p>

                <div className="whitespace-pre-wrap text-slate-300">
                  {response.analysis.analysis}
                </div>

              </div>
            </section>

            {/* Decision Agent */}
            <section>
              <h2 className="text-xl font-semibold">
                🎯 Final Decision
              </h2>

              <div className="mt-2 rounded-xl bg-blue-950/40 border border-blue-700 p-5">

                <p className="mb-3 text-sm text-blue-300">
                  Topic: {response.decision.topic}
                </p>

                <div className="whitespace-pre-wrap text-slate-200">
                  {response.decision.decision}
                </div>

              </div>
            </section>

          </div>
        )}

      </div>
    </div>
  );
}