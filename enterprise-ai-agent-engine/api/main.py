from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from workflows.workflow_v2 import ToolIntegratedWorkflow
from workflows.workflow_v3 import m3_workflow
from tools.tool_factory import get_tool_registry
from monitoring import monitoring_summary


app = FastAPI(
    title="AI Education & Career Guidance Assistant",
    version="2.0.0"
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Models
# ---------------------------------------------------------

class AgentRequest(BaseModel):
    task: str


class ToolExecutionRequest(BaseModel):
    tool_name: str
    parameters: Dict[str, Any] = Field(default_factory=dict)


class CareerWorkflowRequest(BaseModel):
    student_request: str = Field(min_length=3, max_length=2000)
    student_id: str = Field(default="STU029", min_length=1, max_length=80)
    college_id: str = Field(default="COL002", min_length=1, max_length=80)
    m1_score: Optional[float] = Field(default=85.0, ge=0, le=100)


# ---------------------------------------------------------
# Application objects
# ---------------------------------------------------------

workflow = ToolIntegratedWorkflow()
tool_registry = get_tool_registry()


# ---------------------------------------------------------
# Root
# ---------------------------------------------------------

@app.get("/")
def root():

    return {
        "message": "AI Education & Career Guidance Assistant API is running",
        "version": "2.0.0",
        "features": [
            "multi-agent-orchestration",
            "tool-integration",
            "intelligent-tool-selection",
            "tool-execution",
            "decision-support"
        ]
    }


# ---------------------------------------------------------
# Health
# ---------------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "version": "2.0.0"
    }


@app.get("/monitoring/summary")
def monitoring():
    return monitoring_summary()


@app.post("/career/run")
def run_career_workflow(data: CareerWorkflowRequest):
    request = data.student_request.strip()
    if len(request) < 3:
        raise HTTPException(
            status_code=422,
            detail="Please provide a career request with at least 3 characters.",
        )

    try:
        result = m3_workflow.invoke(
            {
                "student_id": data.student_id.strip(),
                "college_id": data.college_id.strip(),
                "is_paid_user": False,
                "payment_amount": 0.0,
                "m1_score": data.m1_score,
                "revenue": 0.0,
                "student_request": request,
            }
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="The career workflow could not be completed.",
        ) from exc

    return {
        "success": result.get("workflow_status") != "failed",
        "workflow_status": result.get("workflow_status", "unknown"),
        "student_request": request,
        "decision": result.get("decision_data", {}).get("decision", ""),
        "preview_answer": result.get("preview_answer", ""),
        "purchase_required": result.get("purchase_required", False),
        "purchase_amount": result.get("purchase_amount", 0.0),
        "agent_timings": result.get("agent_timings", {}),
        "messages": result.get("messages", []),
        "errors": result.get("errors", []),
    }


# ---------------------------------------------------------
# Run Agent
# ---------------------------------------------------------

@app.post("/run")
def run_agent(data: AgentRequest):

    # -----------------------------------------------------
    # Input Validation
    # -----------------------------------------------------

    if not data.task or not data.task.strip():

        return {
            "success": False,
            "request": data.task,
            "answer": "Please enter a request."
        }

    if len(data.task.strip()) < 3:

        return {
            "success": False,
            "request": data.task,
            "answer": "Please enter a more detailed request."
        }

    try:

        # -------------------------------------------------
        # Execute complete AI workflow
        # -------------------------------------------------

        result = workflow.run(
            data.task.strip()
        )

        # -------------------------------------------------
        # Use Human-Readable Response Generator
        # -------------------------------------------------

        answer = result.get(
            "answer",
            "Unable to generate an answer."
        )

        decision = result.get(
            "decision",
            {}
        )

        # -------------------------------------------------
        # Return clean user-facing response
        # -------------------------------------------------

        return {
            "success": result.get(
                "success",
                True
            ),

            "request": data.task,

            "answer": answer,

            "selected_tool":
                result.get(
                    "selected_tool"
                ),

            "tool_selection":
                result.get(
                    "tool_selection"
                ),

            "research":
                result.get(
                    "research"
                ),

            "analysis":
                result.get(
                    "analysis"
                ),

            "decision":
                decision,

            "study_plan":
                result.get(
                    "study_plan"
                ),

            "tool_execution":
                result.get(
                    "tool_execution"
                )
        }

    except Exception as e:

        print(
            f"Workflow error: {e}"
        )

        return {
            "success": False,
            "request": data.task,
            "answer": (
                "Something went wrong while "
                "processing your request. "
                "Please try again."
            ),
            "error": str(e)
        }


# ---------------------------------------------------------
# List All Tools
# ---------------------------------------------------------

@app.get("/tools")
def list_tools():

    tools = []

    for name, tool_class in tool_registry.get_all_tools().items():

        tool = tool_class()

        tools.append({

            "name":
                tool.name,

            "description":
                tool.description,

            "category":
                tool.category.value,

            "version":
                tool.version,

            "enabled":
                tool.enabled,

            "parameters": [

                {
                    "name":
                        parameter.name,

                    "type":
                        parameter.type,

                    "description":
                        parameter.description,

                    "required":
                        parameter.required,

                    "default":
                        parameter.default,

                    "enum":
                        parameter.enum
                }

                for parameter in tool.parameters
            ]
        })

    return {

        "total_tools":
            len(tools),

        "tools":
            tools
    }


# ---------------------------------------------------------
# Get Specific Tool
# ---------------------------------------------------------

@app.get("/tools/{tool_name}")
def get_tool(tool_name: str):

    try:

        tool = tool_registry.get_tool(
            tool_name
        )

        return {

            "name":
                tool.name,

            "description":
                tool.description,

            "category":
                tool.category.value,

            "version":
                tool.version,

            "enabled":
                tool.enabled,

            "parameters": [

                {
                    "name":
                        parameter.name,

                    "type":
                        parameter.type,

                    "description":
                        parameter.description,

                    "required":
                        parameter.required,

                    "default":
                        parameter.default,

                    "enum":
                        parameter.enum
                }

                for parameter in tool.parameters
            ]
        }

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


# ---------------------------------------------------------
# Execute Tool
# ---------------------------------------------------------

@app.post("/tools/execute")
def execute_tool(
    data: ToolExecutionRequest
):

    try:

        tool = tool_registry.get_tool(
            data.tool_name
        )

        result = tool.execute(
            **data.parameters
        )

        return {

            "success":
                result.success,

            "tool_name":
                result.tool_name,

            "data":
                result.data,

            "error":
                result.error,

            "execution_time":
                result.execution_time
        }

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception as e:

        return {

            "success":
                False,

            "tool_name":
                data.tool_name,

            "data":
                None,

            "error":
                str(e)
        }


# ---------------------------------------------------------
# History
# ---------------------------------------------------------

@app.get("/history")
def history():

    if hasattr(
        workflow,
        "history"
    ):

        return {
            "history":
                workflow.history
        }

    return {
        "history": []
    }


# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------

@app.get("/statistics")
def statistics():

    if hasattr(
        workflow,
        "statistics"
    ):

        return workflow.statistics

    return {
        "message":
            "Statistics are available after workflow execution."
    }


# ---------------------------------------------------------
# Calculation Tool
# ---------------------------------------------------------

@app.post("/tools/calculate")
def calculate(
    parameters: Dict[str, Any]
):

    try:

        tool = tool_registry.get_tool(
            "calculation"
        )

        result = tool.execute(
            **parameters
        )

        return {

            "success":
                result.success,

            "data":
                result.data,

            "error":
                result.error
        }

    except Exception as e:

        return {

            "success":
                False,

            "error":
                str(e)
        }


# ---------------------------------------------------------
# Data Validation Tool
# ---------------------------------------------------------

@app.post("/tools/validate")
def validate(
    parameters: Dict[str, Any]
):

    try:

        tool = tool_registry.get_tool(
            "data_validation"
        )

        result = tool.execute(
            **parameters
        )

        return {

            "success":
                result.success,

            "data":
                result.data,

            "error":
                result.error
        }

    except Exception as e:

        return {

            "success":
                False,

            "error":
                str(e)
        }


# ---------------------------------------------------------
# Report Generation Tool
# ---------------------------------------------------------

@app.post("/tools/report")
def generate_report(
    parameters: Dict[str, Any]
):

    try:

        tool = tool_registry.get_tool(
            "report_generation"
        )

        result = tool.execute(
            **parameters
        )

        return {

            "success":
                result.success,

            "data":
                result.data,

            "error":
                result.error
        }

    except Exception as e:

        return {

            "success":
                False,

            "error":
                str(e)
        }# ---------------------------------------------------------
# Human-Readable Selected Tool Execution
# ---------------------------------------------------------

@app.post("/tools/run-selected")
def run_selected_tool(data: Dict[str, Any]):

    tool_name = str(data.get("tool_name", "")).strip().lower()
    request_text = str(data.get("request", "")).strip()

    if not tool_name:
        return {
            "success": False,
            "answer": "Please select a tool."
        }

    if not request_text:
        return {
            "success": False,
            "answer": "Please enter a request."
        }

    try:

        # ---------------------------------------------------------
        # CALCULATION
        # ---------------------------------------------------------
        if tool_name in ["calculation", "calculationtool"]:

            import re

            expression = request_text.strip()
            expression = re.sub(
                r"^(?:calculate|compute|what is)\s+",
                "",
                expression,
                flags=re.IGNORECASE,
            ).rstrip(" ?.!").replace("Ã—", "*").replace("Ã·", "/")

            if (
                re.fullmatch(r"[\d\s.+*/()%\-^]+", expression)
                and re.search(r"[+*/%^()-]", expression)
            ):
                result = tool_registry.get_tool("calculation").execute(
                    operation="expression",
                    expression=expression,
                )

                if result.success:
                    value = result.data.get("result")
                    if isinstance(value, float) and value.is_integer():
                        value = int(value)
                    return {
                        "success": True,
                        "tool_name": "calculation",
                        "answer": f"The calculation result is {value}.",
                        "data": result.data,
                    }

                return {
                    "success": False,
                    "tool_name": "calculation",
                    "answer": result.error or "The calculation could not be completed.",
                }

            numbers = re.findall(r"-?\d+(?:\.\d+)?", request_text)
            values = [float(x) for x in numbers]

            if all(x.is_integer() for x in values):
                values = [int(x) for x in values]

            text_lower = request_text.lower()

            if "per day" in text_lower and "for" in text_lower and "day" in text_lower:
                operation = "multiply"
            elif any(x in text_lower for x in ["multiply", "times", "*"]):
                operation = "multiply"
            elif any(x in text_lower for x in ["divide", "divided by", "/"]):
                operation = "divide"
            elif any(x in text_lower for x in ["percentage", "percent"]):
                operation = "percentage"
            elif "average" in text_lower:
                operation = "average"
            elif any(x in text_lower for x in ["subtract", "minus"]):
                operation = "subtract"
            elif any(x in text_lower for x in ["add", "sum", "+"]):
                operation = "add"
            else:
                operation = "sum"

            result = tool_registry.get_tool("calculation").execute(
                operation=operation,
                values=values
            )

            if result.success:
                value = result.data.get("result")

                if operation == "multiply":
                    answer = f"The calculated total is {value}."
                elif operation == "percentage":
                    answer = f"The calculated percentage is {value:.2f}%."
                elif operation == "average":
                    answer = f"The average is {value:.2f}."
                else:
                    answer = f"The calculation result is {value}."

                if "study" in text_lower and operation == "multiply":
                    answer = f"You will study {value} hours in total."

                return {
                    "success": True,
                    "tool_name": "calculation",
                    "answer": answer,
                    "data": result.data
                }

            return {
                "success": False,
                "tool_name": "calculation",
                "answer": result.error or "The calculation could not be completed."
            }

        # ---------------------------------------------------------
        # COMMUNICATION
        # ---------------------------------------------------------
        if tool_name in ["communication", "communicationtool"]:

            import re

            text = request_text.strip()
            text_lower = text.lower()

            # Generate a useful message from common student communication requests.
            if "leave" in text_lower and "teacher" in text_lower:
                message = (
                    "Dear Teacher,\n\n"
                    "I would like to request leave for one day due to personal reasons. "
                    "Kindly grant me leave for the day.\n\n"
                    "Thank you.\n\n"
                    "Yours sincerely,\n"
                    "Student"
                )
            elif "leave" in text_lower:
                message = (
                    "Dear Sir/Madam,\n\n"
                    "I would like to request leave for one day due to personal reasons. "
                    "Kindly grant me leave for the day.\n\n"
                    "Thank you.\n\n"
                    "Yours sincerely,\n"
                    "Student"
                )
            elif any(word in text_lower for word in ["email", "mail"]):
                message = (
                    "Dear Sir/Madam,\n\n"
                    f"{text}\n\n"
                    "Thank you.\n\n"
                    "Regards,\n"
                    "Student"
                )
            else:
                message = (
                    "Dear Sir/Madam,\n\n"
                    f"{text}\n\n"
                    "Thank you.\n\n"
                    "Regards,\n"
                    "Student"
                )

            result = tool_registry.get_tool("communication").execute(
                message_type="email",
                recipient="Teacher",
                subject="Student Communication",
                message=message,
                priority="normal"
            )

            if result.success:
                return {
                    "success": True,
                    "tool_name": "communication",
                    "answer": f"Your message has been prepared:\n\n{message}",
                    "data": result.data
                }

            return {
                "success": False,
                "tool_name": "communication",
                "answer": result.error or "The message could not be created."
            }
        # ---------------------------------------------------------
        # DATA RETRIEVAL
        # ---------------------------------------------------------
        if tool_name in ["data retrieval", "data_retrieval", "dataretrievaltool"]:

            import re

            text = request_text.strip()
            text_lower = text.lower()

            if any(word in text_lower for word in ["college", "colleges", "university", "universities"]):
                result = tool_registry.get_tool("data_retrieval").execute(
                    source="database",
                    query=text,
                    limit=10
                )

                if result.success:
                    data_result = result.data

                    if isinstance(data_result, dict):
                        records = data_result.get("records", [])

                        if records:
                            answer_lines = []
                            for record in records:
                                if isinstance(record, dict):
                                    name = record.get("name", "College")
                                    location = record.get("location", "")
                                    fees = record.get("fees", "")
                                    placement = record.get("placement", "")

                                    line = f"{name}"
                                    if location:
                                        line += f" — {location}"
                                    if fees != "":
                                        line += f" | Fees: ₹{fees}"
                                    if placement != "":
                                        line += f" | Placement: {placement}%"

                                    answer_lines.append(line)

                            answer = "\n".join(answer_lines)
                        else:
                            answer = "No matching college records were found."

                    else:
                        answer = str(data_result)

                    return {
                        "success": True,
                        "tool_name": "data_retrieval",
                        "answer": f"Here is the information retrieved:\n\n{answer}",
                        "data": data_result
                    }

                return {
                    "success": False,
                    "tool_name": "data_retrieval",
                    "answer": result.error or "The requested information could not be retrieved."
                }

            topic_match = re.search(
                r"(?:about|on|for)\s+(.+?)[.!?]?$",
                text,
                re.IGNORECASE
            )

            topic = topic_match.group(1).strip() if topic_match else text

            return {
                "success": True,
                "tool_name": "data_retrieval",
                "answer": (
                    "Information retrieval completed successfully.\n\n"
                    f"Topic: {topic}\n"
                    "Source: Configured knowledge source\n"
                    "Status: Retrieved"
                ),
                "data": {
                    "source": "configured_knowledge_source",
                    "topic": topic,
                    "status": "Retrieved"
                }
            }
        # ---------------------------------------------------------
        # DATA VALIDATION
        # ---------------------------------------------------------
        if tool_name in ["data validation", "data_validation", "datavalidationtool"]:

            import re

            text = request_text.strip()
            text_lower = text.lower()

            if "email" in text_lower:
                validation_type = "email"
                match = re.search(
                    r"([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})",
                    text
                )
                data_value = match.group(1) if match else text

            elif any(x in text_lower for x in ["phone", "mobile", "telephone"]):
                validation_type = "phone"
                match = re.search(
                    r"(\+?[0-9][0-9\s-]{8,14})",
                    text
                )
                data_value = match.group(1).replace(" ", "").replace("-", "") if match else text

            elif any(x in text_lower for x in ["age", "number", "numeric"]):
                validation_type = "numeric"
                match = re.search(
                    r"-?\d+(?:\.\d+)?",
                    text
                )
                data_value = match.group(0) if match else text

            else:
                validation_type = "required"
                data_value = text

            result = tool_registry.get_tool("data_validation").execute(
                validation_type=validation_type,
                data=data_value
            )

            if result.success:
                data_result = result.data

                return {
                    "success": True,
                    "tool_name": "data_validation",
                    "answer": (
                        f"Validation completed successfully.\n\n"
                        f"Data: {data_value}\n"
                        f"Type: {validation_type.title()}\n"
                        f"Status: {data_result.get('status', 'Unknown')}\n"
                        f"Message: {data_result.get('message', '')}"
                    ),
                    "data": data_result
                }

            return {
                "success": False,
                "tool_name": "data_validation",
                "answer": result.error or "The data could not be validated."
            }
        # ---------------------------------------------------------
        # REPORT GENERATION
        # ---------------------------------------------------------
        if tool_name in ["report generation", "report_generation", "reportgenerationtool"]:

            result = tool_registry.get_tool("report_generation").execute(
                report_type="summary",
                title="Career Guidance Report",
                data={"request": request_text}
            )

            if result.success:
                data_result = result.data

                if isinstance(data_result, dict):
                    report_data = data_result.get("data", {})
                    topic = (
                        report_data.get("request", request_text)
                        if isinstance(report_data, dict)
                        else request_text
                    )

                    answer = (
                        "Report Generated Successfully\n\n"
                        f"Title: {data_result.get('title', 'Career Guidance Report')}\n"
                        f"Type: {str(data_result.get('report_type', 'summary')).title()}\n"
                        f"Topic: {topic}\n"
                        f"Status: {str(data_result.get('status', 'generated')).title()}"
                    )
                else:
                    answer = (
                        "Report Generated Successfully\n\n"
                        f"{data_result}"
                    )

                return {
                    "success": True,
                    "tool_name": "report_generation",
                    "answer": answer,
                    "data": data_result
                }

            return {
                "success": False,
                "tool_name": "report_generation",
                "answer": result.error or "The report could not be generated."
            }
        # ---------------------------------------------------------
        # STUDY PLANNER
        # ---------------------------------------------------------
        if tool_name in ["study planner", "study_planner", "studyplannertool"]:

            import re

            text = request_text.strip()

            days_match = re.search(
                r"(\d+)\s*[- ]?\s*day",
                text,
                re.IGNORECASE
            )
            days = int(days_match.group(1)) if days_match else 5

            subject = text

            reverse_match = re.search(
                r"^(?:create|make|prepare|generate)\s+(?:a|an)\s+"
                r"\d+\s*[- ]?\s*day\s+(.+?)\s+"
                r"(?:study plan|study schedule|learning plan)\s*\.?$",
                text,
                re.IGNORECASE
            )

            forward_match = re.search(
                r"(?:study plan|study schedule|learning plan)\s+"
                r"(?:for|on)\s+(.+?)\s*\.?$",
                text,
                re.IGNORECASE
            )

            if reverse_match:
                subject = reverse_match.group(1).strip()
            elif forward_match:
                subject = forward_match.group(1).strip()
            else:
                subject = re.sub(
                    r"^(?:create|make|prepare|generate)\s+(?:a|an)\s+",
                    "",
                    subject,
                    flags=re.IGNORECASE
                )
                subject = re.sub(
                    r"^\d+\s*[- ]?\s*day\s+",
                    "",
                    subject,
                    flags=re.IGNORECASE
                )
                subject = re.sub(
                    r"\s+(?:study plan|study schedule|learning plan)\s*\.?$",
                    "",
                    subject,
                    flags=re.IGNORECASE
                )

            subject = subject.rstrip(".?! ").strip()

            if not subject:
                subject = "your subject"

            result = tool_registry.get_tool("study_planner").execute(
                subject=subject,
                days=days
            )
            if result.success:
                data_result = result.data

                if isinstance(data_result, dict):
                    lines = []

                    for key, value in data_result.items():
                        title = key.replace("_", " ").title()
                        lines.append(f"{title}: {value}")

                    answer = "Here is your study plan:\n\n" + "\n".join(lines)
                else:
                    answer = f"Here is your study plan:\n\n{data_result}"

                return {
                    "success": True,
                    "tool_name": "study_planner",
                    "answer": answer,
                    "data": data_result
                }

            return {
                "success": False,
                "tool_name": "study_planner",
                "answer": result.error or "The study plan could not be created."
            }

        # ---------------------------------------------------------
        # WEB SEARCH
        # ---------------------------------------------------------
        if tool_name in ["web search", "web_search", "websearchtool"]:

            result = tool_registry.get_tool("web_search").execute(
                query=request_text
            )

            if result.success:
                results = result.data.get("results", [])

                if results:
                    lines = ["Here are the relevant search results:\n"]

                    for item in results:
                        title = item.get("title", "Search Result")
                        snippet = item.get("snippet", "")
                        lines.append(f"{title}\n{snippet}\n")

                    answer = "\n".join(lines)
                else:
                    answer = "The search completed, but no relevant results were found."

                return {
                    "success": True,
                    "tool_name": "web_search",
                    "answer": answer,
                    "data": result.data
                }

            return {
                "success": False,
                "tool_name": "web_search",
                "answer": result.error or "The web search could not be completed."
            }

        # ---------------------------------------------------------
        # EMAIL
        # ---------------------------------------------------------
        if tool_name in ["email", "emailtool"]:

            result = tool_registry.get_tool("email").execute(
                to="recipient@example.com",
                subject="AI Education Assistant",
                body=request_text
            )

            if result.success:
                return {
                    "success": True,
                    "tool_name": "email",
                    "answer": (
                        "Your email has been prepared successfully.\n\n"
                        f"Subject: AI Education Assistant\n\n"
                        f"Message:\n{request_text}"
                    ),
                    "data": result.data
                }

            return {
                "success": False,
                "tool_name": "email",
                "answer": result.error or "The email could not be created."
            }

        # ---------------------------------------------------------
        # CALENDAR
        # ---------------------------------------------------------
        if tool_name in ["calendar", "calendartool"]:

            result = tool_registry.get_tool("calendar").execute(
                action="book_meeting",
                title="Career Guidance Meeting",
                date="To be confirmed",
                time="To be confirmed",
                duration_minutes=30,
                attendee="Student"
            )

            if result.success:
                return {
                    "success": True,
                    "tool_name": "calendar",
                    "answer": (
                        "Your career guidance meeting request has been prepared.\n\n"
                        "Meeting: Career Guidance Meeting\n"
                        "Duration: 30 minutes\n"
                        "Date: To be confirmed\n"
                        "Time: To be confirmed"
                    ),
                    "data": result.data
                }

            return {
                "success": False,
                "tool_name": "calendar",
                "answer": result.error or "The meeting could not be scheduled."
            }

        return {
            "success": False,
            "tool_name": tool_name,
            "answer": f"The selected tool '{tool_name}' is not supported."
        }

    except Exception as e:

        return {
            "success": False,
            "tool_name": tool_name,
            "answer": f"The request could not be completed: {str(e)}"
        }






