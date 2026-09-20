from .base_tool import BaseTool, ToolResult, ToolParameter, ToolCategory


class DataRetrievalTool(BaseTool):

    def __init__(self):
        super().__init__(
            name="DataRetrievalTool",
            description="Retrieve information from configured data sources",
            category=ToolCategory.DATA_RETRIEVAL,
            version="1.0.0"
        )

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

        self.mock_database = {
            "employees": [
                {"id": 1, "name": "Rahul", "department": "Finance"},
                {"id": 2, "name": "Priya", "department": "HR"},
                {"id": 3, "name": "Arjun", "department": "IT"},
                {"id": 4, "name": "Sneha", "department": "Marketing"},
                {"id": 5, "name": "Kiran", "department": "Operations"}
            ]
        }

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

        query_lower = query.lower()

        for table_name, records in self.mock_database.items():

            if table_name in query_lower:

                limited_records = records[:limit]

                return ToolResult(
                    success=True,
                    data={
                        "source": "database",
                        "query": query,
                        "table": table_name,
                        "records": limited_records,
                        "count": len(limited_records)
                    },
                    tool_name=self.name
                )

        return ToolResult(
            success=False,
            error=f"Table matching query '{query}' was not found",
            tool_name=self.name
        )
