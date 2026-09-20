from .base_tool import BaseTool, ToolResult, ToolParameter, ToolCategory


class ReportGenerationTool(BaseTool):

    def __init__(self):
        super().__init__(
            name="ReportGenerationTool",
            description="Generate structured reports from provided data",
            category=ToolCategory.REPORTING,
            version="1.0.0"
        )

        self.parameters = [
            ToolParameter(
                name="report_type",
                type="string",
                description="Type of report",
                required=True,
                enum=["summary", "detailed", "executive"]
            ),
            ToolParameter(
                name="title",
                type="string",
                description="Report title",
                required=True
            ),
            ToolParameter(
                name="data",
                type="object",
                description="Data used to generate the report",
                required=True
            )
        ]

    def execute(self, **kwargs) -> ToolResult:
        try:
            report_type = kwargs.get("report_type")
            title = kwargs.get("title")
            data = kwargs.get("data")

            if not report_type:
                return ToolResult(
                    success=False,
                    error="Report type is required",
                    tool_name=self.name
                )

            if not title:
                return ToolResult(
                    success=False,
                    error="Report title is required",
                    tool_name=self.name
                )

            if data is None:
                return ToolResult(
                    success=False,
                    error="Report data is required",
                    tool_name=self.name
                )

            report = {
                "title": title,
                "report_type": report_type,
                "data": data,
                "status": "generated"
            }

            return ToolResult(
                success=True,
                data=report,
                tool_name=self.name
            )

        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Report generation failed: {str(e)}",
                tool_name=self.name
            )