from tools.base_tool import (
    BaseTool,
    ToolCategory,
    ToolParameter,
    ToolResult
)


class CalendarTool(BaseTool):

    def __init__(self):
        super().__init__(
            name="calendar",
            description="Checks meeting availability and books calendar meetings.",
            category=ToolCategory.PLANNING,
            version="1.0.0"
        )

        self.parameters = [
            ToolParameter(
                name="action",
                type="string",
                description="Calendar action",
                enum=[
                    "check_availability",
                    "book_meeting"
                ]
            ),
            ToolParameter(
                name="title",
                type="string",
                description="Meeting title",
                required=False,
                default=""
            ),
            ToolParameter(
                name="date",
                type="string",
                description="Meeting date",
                required=False,
                default=""
            ),
            ToolParameter(
                name="time",
                type="string",
                description="Meeting time",
                required=False,
                default=""
            ),
            ToolParameter(
                name="duration_minutes",
                type="integer",
                description="Meeting duration in minutes",
                required=False,
                default=30
            ),
            ToolParameter(
                name="attendee",
                type="string",
                description="Meeting attendee",
                required=False,
                default=""
            )
        ]

    def execute(self, **kwargs) -> ToolResult:

        action = kwargs.get("action")
        title = kwargs.get("title", "")
        date = kwargs.get("date", "")
        time = kwargs.get("time", "")
        duration_minutes = kwargs.get("duration_minutes", 30)
        attendee = kwargs.get("attendee", "")

        if action == "check_availability":

            return ToolResult(
                success=True,
                data={
                    "action": "check_availability",
                    "date": date,
                    "time": time,
                    "available": True,
                    "message": (
                        f"The requested slot on {date} at {time} "
                        f"is available."
                    )
                },
                tool_name=self.name
            )

        if action == "book_meeting":

            if not title:
                return ToolResult(
                    success=False,
                    error="Meeting title is required.",
                    tool_name=self.name
                )

            if not date:
                return ToolResult(
                    success=False,
                    error="Meeting date is required.",
                    tool_name=self.name
                )

            if not time:
                return ToolResult(
                    success=False,
                    error="Meeting time is required.",
                    tool_name=self.name
                )

            return ToolResult(
                success=True,
                data={
                    "action": "book_meeting",
                    "meeting_title": title,
                    "date": date,
                    "time": time,
                    "duration_minutes": duration_minutes,
                    "attendee": attendee,
                    "message": (
                        f"Meeting '{title}' booked for {date} at {time} "
                        f"for {duration_minutes} minutes."
                    )
                },
                tool_name=self.name
            )

        return ToolResult(
            success=False,
            error=(
                "Unsupported calendar action. "
                "Use 'check_availability' or 'book_meeting'."
            ),
            tool_name=self.name
        )