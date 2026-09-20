from .base_tool import BaseTool, ToolResult, ToolParameter, ToolCategory
import re


class DataValidationTool(BaseTool):

    def __init__(self):
        super().__init__(
            name="DataValidationTool",
            description="Validate data using common validation rules",
            category=ToolCategory.DATA_RETRIEVAL,
            version="1.1.0"
        )

        self.parameters = [
            ToolParameter(
                name="validation_type",
                type="string",
                description="Type of validation",
                required=True,
                enum=["email", "phone", "required", "numeric"]
            ),
            ToolParameter(
                name="data",
                type="string",
                description="Data to validate",
                required=True
            )
        ]

    def execute(self, **kwargs) -> ToolResult:
        try:
            validation_type = kwargs.get("validation_type")
            data = kwargs.get("data")

            if not validation_type:
                return ToolResult(
                    success=False,
                    error="Validation type is required",
                    tool_name=self.name
                )

            if data is None:
                return ToolResult(
                    success=False,
                    error="Data is required",
                    tool_name=self.name
                )

            text = str(data).strip()

            if validation_type == "email":
                valid = bool(
                    re.match(
                        r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
                        text
                    )
                )

                message = (
                    "The email address is valid."
                    if valid
                    else "The email address is not valid."
                )

            elif validation_type == "phone":
                valid = bool(
                    re.match(
                        r"^\+?[0-9]{10,15}$",
                        text
                    )
                )

                message = (
                    "The phone number is valid."
                    if valid
                    else "The phone number is not valid."
                )

            elif validation_type == "required":
                valid = bool(text)

                message = (
                    "The required field contains a value."
                    if valid
                    else "The required field is missing or empty."
                )

            elif validation_type == "numeric":
                try:
                    float(text)
                    valid = True
                except (ValueError, TypeError):
                    valid = False

                message = (
                    "The value is numeric."
                    if valid
                    else "The value must be numeric."
                )

            else:
                return ToolResult(
                    success=False,
                    error=f"Unsupported validation type: {validation_type}",
                    tool_name=self.name
                )

            return ToolResult(
                success=True,
                data={
                    "validation_type": validation_type,
                    "data": data,
                    "valid": valid,
                    "status": "Valid" if valid else "Invalid",
                    "message": message
                },
                tool_name=self.name
            )

        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Data validation failed: {str(e)}",
                tool_name=self.name
            )

