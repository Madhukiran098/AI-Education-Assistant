from .base_tool import BaseTool, ToolResult, ToolParameter, ToolCategory


class CommunicationTool(BaseTool):

    def __init__(self):
        super().__init__(
            name="CommunicationTool",
            description="Send notifications and communication messages",
            category=ToolCategory.COMMUNICATION,
            version="1.0.0"
        )

        self.parameters = [
            ToolParameter(
                name="message_type",
                type="string",
                description="Type of communication",
                required=True,
                enum=["email", "notification", "sms"]
            ),
            ToolParameter(
                name="recipient",
                type="string",
                description="Recipient address",
                required=True
            ),
            ToolParameter(
                name="subject",
                type="string",
                description="Message subject",
                required=False
            ),
            ToolParameter(
                name="message",
                type="string",
                description="Message content",
                required=True
            ),
            ToolParameter(
                name="priority",
                type="string",
                description="Message priority",
                required=False,
                default="normal",
                enum=["low", "normal", "high"]
            )
        ]

    def execute(self, **kwargs) -> ToolResult:
        try:
            message_type = kwargs.get("message_type")
            recipient = kwargs.get("recipient")
            subject = kwargs.get("subject", "")
            message = kwargs.get("message")
            priority = kwargs.get("priority", "normal")

            if not message_type:
                return ToolResult(
                    success=False,
                    error="Message type is required",
                    tool_name=self.name
                )

            if not recipient:
                return ToolResult(
                    success=False,
                    error="Recipient is required",
                    tool_name=self.name
                )

            if not message:
                return ToolResult(
                    success=False,
                    error="Message is required",
                    tool_name=self.name
                )

            return ToolResult(
                success=True,
                data={
                    "message_type": message_type,
                    "recipient": recipient,
                    "subject": subject,
                    "message": message,
                    "priority": priority,
                    "status": "sent"
                },
                tool_name=self.name
            )

        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Communication failed: {str(e)}",
                tool_name=self.name
            )