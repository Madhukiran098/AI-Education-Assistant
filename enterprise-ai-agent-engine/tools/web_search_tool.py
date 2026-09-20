from .base_tool import (
    BaseTool,
    ToolResult,
    ToolParameter,
    ToolCategory
)


class WebSearchTool(BaseTool):

    def __init__(self):

        super().__init__(
            name="WebSearchTool",
            description="Search the web for relevant information",
            category=ToolCategory.DATA_RETRIEVAL,
            version="1.0.0"
        )

        self.parameters = [

            ToolParameter(
                name="query",
                type="string",
                description="Search query",
                required=True
            ),

            ToolParameter(
                name="max_results",
                type="number",
                description="Maximum number of search results",
                required=False,
                default=5
            ),

            ToolParameter(
                name="limit",
                type="number",
                description="Maximum number of search results",
                required=False,
                default=5
            ),

            ToolParameter(
                name="search_type",
                type="string",
                description="Type of search",
                required=False,
                default="web"
            ),

            ToolParameter(
                name="language",
                type="string",
                description="Search language",
                required=False,
                default="en"
            )
        ]

    def execute(self, **kwargs) -> ToolResult:

        try:

            query = kwargs.get("query")

            if not query:
                return ToolResult(
                    success=False,
                    error="Search query is required",
                    tool_name=self.name
                )

            max_results = kwargs.get(
                "max_results",
                kwargs.get("limit", 5)
            )

            try:
                max_results = int(max_results)
            except (TypeError, ValueError):
                max_results = 5

            if max_results <= 0:
                max_results = 5

            search_type = kwargs.get(
                "search_type",
                "web"
            )

            language = kwargs.get(
                "language",
                "en"
            )

            results = [

                {
                    "title": f"Search result for: {query}",
                    "url": "https://example.com",
                    "snippet": (
                        f"Relevant information related to "
                        f"'{query}'. This result was generated "
                        f"by the Web Search Tool for project "
                        f"demonstration."
                    )
                },

                {
                    "title": f"Research information about {query}",
                    "url": "https://example.com/research",
                    "snippet": (
                        f"Additional research information "
                        f"related to '{query}'."
                    )
                },

                {
                    "title": f"Educational information about {query}",
                    "url": "https://example.com/education",
                    "snippet": (
                        f"Educational and knowledge resources "
                        f"related to '{query}'."
                    )
                }
            ]

            results = results[:max_results]

            return ToolResult(
                success=True,
                data={
                    "query": query,
                    "search_type": search_type,
                    "language": language,
                    "results": results,
                    "result_count": len(results),
                    "source": "simulated_web_search"
                },
                tool_name=self.name
            )

        except Exception as e:

            return ToolResult(
                success=False,
                error=f"Web search failed: {str(e)}",
                tool_name=self.name
            )
