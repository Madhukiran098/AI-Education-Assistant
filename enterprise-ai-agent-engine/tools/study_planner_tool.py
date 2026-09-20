from .base_tool import BaseTool, ToolResult, ToolParameter, ToolCategory


class StudyPlannerTool(BaseTool):

    def __init__(self):
        super().__init__(
            name="StudyPlannerTool",
            description="Create structured study plans for students",
            category=ToolCategory.PLANNING,
            version="1.1.0"
        )

        self.parameters = [
            ToolParameter(
                name="subject",
                type="string",
                description="Subject to study",
                required=True
            ),
            ToolParameter(
                name="days",
                type="number",
                description="Number of study days",
                required=True
            ),
            ToolParameter(
                name="level",
                type="string",
                description="Student learning level",
                required=False,
                default="beginner"
            )
        ]

    def execute(self, **kwargs) -> ToolResult:
        try:
            subject = kwargs.get("subject")
            days = int(kwargs.get("days", 0))
            level = kwargs.get("level", "beginner")

            if not subject:
                return ToolResult(
                    success=False,
                    error="Subject is required",
                    tool_name=self.name
                )

            if days <= 0:
                return ToolResult(
                    success=False,
                    error="Days must be greater than zero",
                    tool_name=self.name
                )

            study_stages = [
                {
                    "topic": "Introduction and Fundamentals",
                    "activities": [
                        "Understand the basic concepts",
                        "Learn important terminology",
                        "Practice simple examples"
                    ]
                },
                {
                    "topic": "Core Concepts",
                    "activities": [
                        "Study the main concepts",
                        "Work through guided examples",
                        "Create short practice notes"
                    ]
                },
                {
                    "topic": "Practical Application",
                    "activities": [
                        "Solve practical problems",
                        "Apply concepts to examples",
                        "Complete hands-on exercises"
                    ]
                },
                {
                    "topic": "Practice and Problem Solving",
                    "activities": [
                        "Attempt practice questions",
                        "Identify and correct mistakes",
                        "Complete a short assessment"
                    ]
                },
                {
                    "topic": "Revision and Mini Project",
                    "activities": [
                        "Revise the important concepts",
                        "Build a small practical project",
                        "Review areas that need improvement"
                    ]
                },
                {
                    "topic": "Advanced Concepts",
                    "activities": [
                        "Explore advanced concepts",
                        "Study real-world applications",
                        "Practice challenging examples"
                    ]
                },
                {
                    "topic": "Final Review and Assessment",
                    "activities": [
                        "Review the complete syllabus",
                        "Take a final practice test",
                        "Prepare a personal revision checklist"
                    ]
                }
            ]

            plan = []

            for day in range(1, days + 1):
                stage = study_stages[(day - 1) % len(study_stages)]

                plan.append({
                    "day": day,
                    "topic": f"{subject} - {stage['topic']}",
                    "activities": stage["activities"],
                    "level": level
                })

            return ToolResult(
                success=True,
                data={
                    "subject": subject,
                    "days": days,
                    "level": level,
                    "daily_hours": 2,
                    "study_plan": plan
                },
                tool_name=self.name
            )

        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Study plan generation failed: {str(e)}",
                tool_name=self.name
            )
