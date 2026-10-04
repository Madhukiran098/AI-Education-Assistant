from .base_tool import BaseTool, ToolResult, ToolParameter, ToolCategory
from college_admin_dashboard import search_colleges, seed_sample_colleges


class DataRetrievalTool(BaseTool):

    def __init__(self, college_db_path=None):
        super().__init__(
            name="DataRetrievalTool",
            description="Retrieve information from configured data sources",
            category=ToolCategory.DATA_RETRIEVAL,
            version="1.0.0"
        )
        self.college_db_path = college_db_path

        self.parameters = [
            ToolParameter(
                name="source",
                type="string",
                description="Data source",
                required=True,
                enum=["database", "file", "api"]
            ),
            ToolParameter(
                name="query",
                type="string",
                description="Query used to retrieve data",
                required=True
            ),
            ToolParameter(
                name="limit",
                type="number",
                description="Maximum number of records",
                required=False,
                default=10
            )
        ]


    def execute(self, **kwargs) -> ToolResult:
        try:
            source = kwargs.get("source")
            query = kwargs.get("query")
            limit = int(kwargs.get("limit", 10))

            if not source:
                return ToolResult(
                    success=False,
                    error="Data source is required",
                    tool_name=self.name
                )

            if not query:
                return ToolResult(
                    success=False,
                    error="Query is required",
                    tool_name=self.name
                )

            if source == "database":
                return self._retrieve_from_database(query, limit)

            if source == "file":
                return ToolResult(
                    success=True,
                    data={
                        "source": source,
                        "query": query,
                        "records": [],
                        "message": "File retrieval simulation completed"
                    },
                    tool_name=self.name
                )

            if source == "api":
                return ToolResult(
                    success=True,
                    data={
                        "source": source,
                        "query": query,
                        "records": [],
                        "message": "API retrieval simulation completed"
                    },
                    tool_name=self.name
                )

            return ToolResult(
                success=False,
                error=f"Unsupported data source: {source}",
                tool_name=self.name
            )

        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Data retrieval failed: {str(e)}",
                tool_name=self.name
            )

    def _retrieve_from_database(
        self,
        query: str,
        limit: int
    ) -> ToolResult:

        if "colleges" in query.lower() or "college" in query.lower():
            seed_sample_colleges(self.college_db_path)
            records = search_colleges(query, self.college_db_path)[:limit]
            return ToolResult(
                success=True,
                data={
                    "source": "database",
                    "query": query,
                    "table": "colleges",
                    "records": records,
                    "count": len(records),
                },
                tool_name=self.name,
            )

        return ToolResult(
            success=False,
            error=f"Table matching query '{query}' was not found",
            tool_name=self.name
        )
