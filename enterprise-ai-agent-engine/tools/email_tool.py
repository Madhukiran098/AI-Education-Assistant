from typing import Any, Dict

from tools.base_tool import (
    BaseTool,
    ToolCategory,
    ToolParameter,
    ToolResult
)


class EmailTool(BaseTool):

    def __init__(self):
        super().__init__(
            name="email",
            description="Creates and simulates sending emails.",
            category=ToolCategory.COMMUNICATION,
            version="1.0.0"
        )

        self.parameters = [
            ToolParameter(
                name="to",
                type="string",
                description="Recipient email address"
            ),
            ToolParameter(
                name="subject",
                type="string",
                description="Email subject"
            ),
            ToolParameter(
                name="body",
                type="string",
                description="Email body"
            )
        ]

    def execute(self, **kwargs) -> ToolResult:

        to = kwargs.get("to")
        subject = kwargs.get("subject")
        body = kwargs.get("body")

        if not to:
            return ToolResult(
                success=False,
                error="Recipient email is required.",
                tool_name=self.name
            )

        if not subject:
            return ToolResult(
                success=False,
                error="Email subject is required.",
                tool_name=self.name
            )

        if not body:
            return ToolResult(
                success=False,
                error="Email body is required.",
                tool_name=self.name
            )

        return ToolResult(
            success=True,
            data={
                "action": "send_email",
                "recipient": to,
                "subject": subject,
                "body": body,
                "message": f"Email prepared successfully for {to}."
            },
            tool_name=self.name
        )