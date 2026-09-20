from .base_tool import BaseTool, ToolResult, ToolParameter, ToolCategory


class CalculationTool(BaseTool):

    def __init__(self):
        super().__init__(
            name="CalculationTool",
            description="Perform mathematical calculations",
            category=ToolCategory.ANALYSIS,
            version="1.1.0"
        )

        self.parameters = [
            ToolParameter(
                name="operation",
                type="string",
                description="Calculation operation",
                required=True,
                enum=[
                    "sum",
                    "average",
                    "min",
                    "max",
                    "percentage",
                    "roi",
                    "compound_interest",
                    "multiply",
                    "divide",
                    "add",
                    "subtract"
                ]
            ),
            ToolParameter(
                name="values",
                type="array",
                description="Values to calculate",
                required=False
            )
        ]

    def execute(self, **kwargs) -> ToolResult:
        try:
            operation = kwargs.get("operation")
            values = kwargs.get("values", [])

            if not operation:
                return ToolResult(
                    success=False,
                    error="Operation is required",
                    tool_name=self.name
                )

            if operation == "sum" or operation == "add":
                result = sum(values)

            elif operation == "multiply":
                if len(values) < 2:
                    return ToolResult(
                        success=False,
                        error="Multiplication requires at least two values",
                        tool_name=self.name
                    )
                result = 1
                for value in values:
                    result *= value

            elif operation == "divide":
                if len(values) < 2:
                    return ToolResult(
                        success=False,
                        error="Division requires two values",
                        tool_name=self.name
                    )
                if values[1] == 0:
                    return ToolResult(
                        success=False,
                        error="Cannot divide by zero",
                        tool_name=self.name
                    )
                result = values[0] / values[1]

            elif operation == "subtract":
                if len(values) < 2:
                    return ToolResult(
                        success=False,
                        error="Subtraction requires two values",
                        tool_name=self.name
                    )
                result = values[0] - values[1]

            elif operation == "average":
                if not values:
                    return ToolResult(
                        success=False,
                        error="Values are required",
                        tool_name=self.name
                    )
                result = sum(values) / len(values)

            elif operation == "min":
                if not values:
                    return ToolResult(
                        success=False,
                        error="Values are required",
                        tool_name=self.name
                    )
                result = min(values)

            elif operation == "max":
                if not values:
                    return ToolResult(
                        success=False,
                        error="Values are required",
                        tool_name=self.name
                    )
                result = max(values)

            elif operation == "percentage":
                if len(values) < 2:
                    return ToolResult(
                        success=False,
                        error="Percentage requires two values",
                        tool_name=self.name
                    )
                result = (values[0] / 100) * values[1]

            elif operation == "roi":
                if len(values) < 2:
                    return ToolResult(
                        success=False,
                        error="ROI requires investment and return values",
                        tool_name=self.name
                    )
                investment = values[0]
                return_value = values[1]
                result = ((return_value - investment) / investment) * 100

            elif operation == "compound_interest":
                if len(values) < 4:
                    return ToolResult(
                        success=False,
                        error="Compound interest requires principal, rate, time and frequency",
                        tool_name=self.name
                    )

                principal = values[0]
                rate = values[1]
                time = values[2]
                frequency = values[3]

                result = principal * (
                    1 + rate / (100 * frequency)
                ) ** (frequency * time)

            else:
                return ToolResult(
                    success=False,
                    error=f"Unsupported operation: {operation}",
                    tool_name=self.name
                )

            return ToolResult(
                success=True,
                data={
                    "operation": operation,
                    "values": values,
                    "result": result
                },
                tool_name=self.name
            )

        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Calculation failed: {str(e)}",
                tool_name=self.name
            )

