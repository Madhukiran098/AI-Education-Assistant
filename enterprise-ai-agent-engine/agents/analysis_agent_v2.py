from agents.analysis_agent import AnalysisAgent


class AnalysisAgentV2(AnalysisAgent):

    def __init__(self, tool_registry=None):
        try:
            super().__init__(tool_registry)
        except TypeError:
            super().__init__()
        self.tool_registry = tool_registry
