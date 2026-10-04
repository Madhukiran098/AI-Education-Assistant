from langsmith import traceable


@traceable(name="M3-Career-Workflow")
def trace_m3_workflow(student_id: str, college_id: str, student_request: str):
    return {
        "student_id": student_id,
        "college_id": college_id,
        "student_request": student_request,
    }
