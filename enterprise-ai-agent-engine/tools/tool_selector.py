from typing import Dict, Any
import re


class ToolSelector:

    def __init__(self, tool_registry=None):
        self.tool_registry = tool_registry

    def select_tool(self, user_request: str) -> Dict[str, Any]:

        request = user_request.lower().strip()

        # ---------------------------------------------------------
        # DATA VALIDATION
        # ---------------------------------------------------------
        if any(phrase in request for phrase in [
            "validate",
            "validation",
            "check data",
            "validate data",
            "required field",
            "missing field",
            "empty field",
            "check whether",
            "is missing",
            "is empty"
        ]):

            if "email" in request:
                validation_type = "email"
                match = re.search(
                    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                    user_request
                )
                data = match.group(0) if match else user_request

            elif any(word in request for word in [
                "phone",
                "mobile",
                "telephone"
            ]):
                validation_type = "phone"
                match = re.search(r"\+?[0-9][0-9\s-]{8,14}", user_request)
                data = match.group(0).strip() if match else user_request

            elif any(word in request for word in [
                "numeric",
                "number",
                "age",
                "amount",
                "value"
            ]):
                validation_type = "numeric"
                numbers = re.findall(r"-?\d+(?:\.\d+)?", user_request)
                data = numbers[-1] if numbers else user_request

            else:
                validation_type = "required"
                data = user_request

            return {
                "success": True,
                "tool_name": "data_validation",
                "confidence": 0.95,
                "parameters": {
                    "validation_type": validation_type,
                    "data": data
                },
                "reason": "Data validation request detected"
            }

        # ---------------------------------------------------------
        # CALCULATION
        # ---------------------------------------------------------
        calculation_phrases = [
            "calculate",
            "calculation",
            "how many total",
            "total hours",
            "total amount",
            "multiply",
            "times",
            "divide",
            "percentage",
            "percent",
            "%",
            "average",
            "roi",
            "add",
            "subtract",
            "sum",
            "minimum",
            "maximum"
        ]

        if any(phrase in request for phrase in calculation_phrases):

            numbers = re.findall(
                r"-?\d+(?:\.\d+)?",
                user_request
            )

            values = [float(number) for number in numbers]

            if all(value.is_integer() for value in values):
                values = [int(value) for value in values]

            if (
                "per day" in request
                and "for" in request
                and "days" in request
            ):
                operation = "multiply"
            elif (
                "times" in request
                or "multiply" in request
                or "*" in request
                or "multiplied by" in request
            ):
                operation = "multiply"
            elif (
                "divide" in request
                or "divided by" in request
                or "/" in request
            ):
                operation = "divide"
            elif (
                "percentage" in request
                or "percent" in request
                or "%" in request
            ):
                operation = "percentage"
            elif "average" in request:
                operation = "average"
            elif "minimum" in request or "min" in request:
                operation = "min"
            elif "maximum" in request or "max" in request:
                operation = "max"
            elif (
                "subtract" in request
                or "minus" in request
                or "-" in request
            ):
                operation = "subtract"
            elif (
                "add" in request
                or "sum" in request
                or "+" in request
            ):
                operation = "add"
            else:
                operation = "sum"

            return {
                "success": True,
                "tool_name": "calculation",
                "confidence": 0.95,
                "parameters": {
                    "operation": operation,
                    "values": values
                },
                "reason": "Calculation request detected"
            }

        # ---------------------------------------------------------
        # EMAIL
        # ---------------------------------------------------------
        if any(phrase in request for phrase in [
            "send email",
            "email",
            "compose email",
            "write an email",
            "draft an email",
            "prepare an email"
        ]):

            recipient_match = re.search(
                r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                user_request
            )

            recipient = (
                recipient_match.group(0)
                if recipient_match
                else "mentor@example.com"
            )

            if "mentor" in request:
                subject = "Request for Project Review Meeting"
                body = (
                    "Dear Mentor,\n\n"
                    "I would like to request a meeting to review my "
                    "AI Education and Career Guidance Assistant project. "
                    "I would appreciate your feedback and suggestions "
                    "for further improvement.\n\n"
                    "Thank you."
                )
            else:
                subject = "AI Education and Career Guidance Assistant"
                body = user_request

            return {
                "success": True,
                "tool_name": "email",
                "confidence": 0.95,
                "parameters": {
                    "to": recipient,
                    "subject": subject,
                    "body": body
                },
                "reason": "Email request detected"
            }

        # ---------------------------------------------------------
        # CALENDAR
        # ---------------------------------------------------------
        if any(phrase in request for phrase in [
            "calendar",
            "schedule meeting",
            "book meeting",
            "schedule a meeting",
            "meeting",
            "appointment",
            "check availability"
        ]):

            if "check availability" in request or "available" in request:
                action = "check_availability"
            else:
                action = "book_meeting"

            time_match = re.search(
                r"\b(?:at\s*)?(\d{1,2}(?::\d{2})?\s*(?:AM|PM|am|pm))\b",
                user_request
            )

            duration_match = re.search(
                r"(\d+)\s*(?:minute|minutes|min)",
                user_request,
                re.IGNORECASE
            )

            time_value = time_match.group(1) if time_match else ""

            duration = (
                int(duration_match.group(1))
                if duration_match
                else 30
            )

            if "project" in request:
                title = "Project Review Meeting"
            else:
                title = "AI Education and Career Guidance Meeting"

            return {
                "success": True,
                "tool_name": "calendar",
                "confidence": 0.95,
                "parameters": {
                    "action": action,
                    "title": title,
                    "date": "Tomorrow" if "tomorrow" in request else "",
                    "time": time_value,
                    "duration_minutes": duration,
                    "attendee": "Mentor" if "mentor" in request else ""
                },
                "reason": "Calendar request detected"
            }

        # ---------------------------------------------------------
        # STUDY PLANNER
        # ---------------------------------------------------------
        if any(phrase in request for phrase in [
            "study plan",
            "study schedule",
            "learning plan",
            "prepare for exam",
            "exam preparation"
        ]):

            subject = user_request.strip()

            subject_match = re.search(
                r"(?:study plan|study schedule|learning plan)\s+(?:for|on)\s+(.+)",
                subject,
                re.IGNORECASE
            )

            if subject_match:
                subject = subject_match.group(1).strip()

            subject = re.sub(
                r"^(?:create|make|prepare|generate)\s+(?:a|an)\s+",
                "",
                subject,
                flags=re.IGNORECASE
            )

            subject = re.sub(
                r"^\d+\s*-\s*day\s+",
                "",
                subject,
                flags=re.IGNORECASE
            )

            subject = re.sub(
                r"^\d+\s+day\s+",
                "",
                subject,
                flags=re.IGNORECASE
            )

            subject = subject.rstrip(".?").strip()

            days_match = re.search(
                r"(\d+)\s*[- ]?\s*day",
                request
            )

            days = int(days_match.group(1)) if days_match else 5

            return {
                "success": True,
                "tool_name": "study_planner",
                "confidence": 0.95,
                "parameters": {
                    "subject": subject,
                    "days": days
                },
                "reason": "Study planning request detected"
            }

        # ---------------------------------------------------------
        # REPORT GENERATION
        # ---------------------------------------------------------
        if any(phrase in request for phrase in [
            "report",
            "generate report",
            "create report",
            "write a report"
        ]):

            title = "AI Education Report"

            if "career" in request:
                title = "AI Education and Career Report"
            elif "education" in request:
                title = "AI in Education Report"

            return {
                "success": True,
                "tool_name": "report_generation",
                "confidence": 0.95,
                "parameters": {
                    "report_type": "summary",
                    "title": title,
                    "data": {
                        "topic": user_request,
                        "request": user_request
                    }
                },
                "reason": "Report generation request detected"
            }

        # ---------------------------------------------------------
        # WEB SEARCH
        # ---------------------------------------------------------
        if any(phrase in request for phrase in [
            "search",
            "latest",
            "current",
            "find information",
            "research",
            "web search",
            "skills required",
            "current skills"
        ]):

            return {
                "success": True,
                "tool_name": "web_search",
                "confidence": 0.95,
                "parameters": {
                    "query": user_request,
                    "max_results": 5
                },
                "reason": "Web search request detected"
            }

        # ---------------------------------------------------------
        # DATA RETRIEVAL
        # ---------------------------------------------------------
        if any(phrase in request for phrase in [
            "retrieve",
            "database",
            "get data",
            "fetch data"
        ]):

            source = "database"

            if "file" in request:
                source = "file"
            elif "api" in request:
                source = "api"

            return {
                "success": True,
                "tool_name": "data_retrieval",
                "confidence": 0.90,
                "parameters": {
                    "source": source,
                    "query": user_request,
                    "limit": 10
                },
                "reason": "Data retrieval request detected"
            }

        # ---------------------------------------------------------
        # COMMUNICATION
        # ---------------------------------------------------------
        if any(phrase in request for phrase in [
            "communicate",
            "message",
            "notify",
            "send message",
            "write a polite message"
        ]):

            recipient = "Mentor"

            message = user_request

            if "mentor" in request and "feedback" in request:
                message = (
                    "Dear Mentor,\n\n"
                    "I would appreciate your feedback on my "
                    "AI Education and Career Guidance Assistant project. "
                    "Please let me know your suggestions for improvement.\n\n"
                    "Thank you."
                )

            return {
                "success": True,
                "tool_name": "communication",
                "confidence": 0.95,
                "parameters": {
                    "message_type": "notification",
                    "recipient": recipient,
                    "subject": "Project Feedback Request",
                    "message": message,
                    "priority": "normal"
                },
                "reason": "Communication request detected"
            }

        # ---------------------------------------------------------
        # DEFAULT
        # ---------------------------------------------------------
        return {
            "success": True,
            "tool_name": "web_search",
            "confidence": 0.50,
            "parameters": {
                "query": user_request
            },
            "reason": "General request routed to research/web search"
        }
