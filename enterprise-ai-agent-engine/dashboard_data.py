from collections import Counter
from typing import Any, Dict, List

from monitoring import read_events


def get_college_events(college_id: str) -> List[Dict[str, Any]]:
    events = read_events()

    return [
        event
        for event in events
        if event.get("college_id") == college_id
    ]


def _unique_students(events: List[Dict[str, Any]]) -> set:
    return {
        str(event.get("student_id"))
        for event in events
        if event.get("student_id")
    }


def _paid_students(events: List[Dict[str, Any]]) -> set:
    return {
        str(event.get("student_id"))
        for event in events
        if event.get("student_id")
        and event.get("is_paid_user") is True
    }


def _revenue_by_student(events: List[Dict[str, Any]]) -> Dict[str, float]:
    revenue_by_student: Dict[str, float] = {}

    for event in events:
        student_id = str(event.get("student_id", "")).strip()

        if not student_id:
            continue

        revenue_by_student[student_id] = max(
            revenue_by_student.get(student_id, 0.0),
            float(event.get("revenue", 0.0)),
        )

    return revenue_by_student


def calculate_dashboard_metrics(
    college_id: str,
) -> Dict[str, Any]:

    all_events = read_events()

    college_events = [
        event
        for event in all_events
        if event.get("college_id") == college_id
    ]

    # Global student count across all colleges.
    all_student_ids = _unique_students(all_events)

    # Selected college student metrics.
    student_ids = _unique_students(college_events)
    paid_students = _paid_students(college_events)
    free_students = student_ids - paid_students

    total_students = len(student_ids)
    paid_count = len(paid_students)
    free_count = len(free_students)

    conversion_rate = (
        (paid_count / total_students) * 100
        if total_students
        else 0.0
    )

    # Revenue is calculated from every successful student payment event.
    revenue = sum(
        float(event.get("revenue", 0.0))
        for event in college_events
        if event.get("event") == "Student payment verified"
        and event.get("status") == "success"
    )

    # Response time is calculated from actual successful monitoring events.
    response_times = []

    for event in college_events:
        if event.get("status") != "success":
            continue

        try:
            elapsed = float(event.get("time_taken", 0.0))
        except (TypeError, ValueError):
            continue

        if elapsed > 0:
            response_times.append(elapsed)

    average_response_time = (
        sum(response_times) / len(response_times)
        if response_times
        else 0.0
    )

    # Failure rate is based on all recorded monitoring events.
    failed_events = [
        event
        for event in college_events
        if event.get("status") == "failed"
    ]

    failure_rate = (
        (len(failed_events) / len(college_events)) * 100
        if college_events
        else 0.0
    )

    career_keywords = {
        "Software": [
            "software",
            "python",
            "developer",
            "programming",
            "it career",
        ],
        "Government": [
            "government",
            "civil",
            "upsc",
            "public service",
            "govt",
        ],
        "Education": [
            "education",
            "teacher",
            "teaching",
            "school",
        ],
        "Business": [
            "business",
            "management",
            "finance",
            "mba",
            "entrepreneur",
        ],
    }

    career_counts = Counter()
    processed_students = set()

    for event in college_events:
        student_id = str(event.get("student_id", "")).strip()

        if not student_id or student_id in processed_students:
            continue

        request_text = str(
            event.get("student_request", "")
        ).lower()

        if not request_text:
            continue

        for career, keywords in career_keywords.items():
            if any(
                keyword in request_text
                for keyword in keywords
            ):
                career_counts[career] += 1
                processed_students.add(student_id)
                break

    return {
        "college_id": college_id,

        # Selected-college metrics.
        "total_students": total_students,
        "paid_students": paid_count,
        "free_students": free_count,

        # Global metric.
        "total_students_all_colleges": len(all_student_ids),

        "paid_conversion_rate": round(
            conversion_rate,
            2,
        ),

        "revenue_generated": round(
            revenue,
            2,
        ),

        "average_response_time": round(
            average_response_time,
            4,
        ),

        "failure_rate": round(
            failure_rate,
            2,
        ),

        "career_trends": dict(career_counts),

        "total_events": len(college_events),
    }

