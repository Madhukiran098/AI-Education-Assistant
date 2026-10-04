from datetime import datetime
import json
import math
from pathlib import Path
from typing import Any, Dict, Optional

LOG_DIR = Path("data")
LOG_FILE = LOG_DIR / "m3_monitoring.jsonl"


def log_event(
    college_id: str,
    agent_name: str,
    time_taken: float,
    status: str,
    student_id: Optional[str] = None,
    is_paid_user: Optional[bool] = None,
    revenue: float = 0.0,
    event: str = "agent_execution",
    student_request: str = "",
) -> Dict[str, Any]:

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    record = {
        "timestamp": datetime.now().isoformat(),
        "college_id": college_id,
        "student_id": student_id or "",
        "agent_name": agent_name,
        "time_taken": round(float(time_taken), 4),
        "status": status,
        "is_paid_user": is_paid_user,
        "revenue": round(float(revenue), 2),
        "event": event,
        "student_request": student_request,
    }

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(
            json.dumps(record) + "\n"
        )

    return record


def read_events() -> list[Dict[str, Any]]:
    if not LOG_FILE.exists():
        return []

    events = []

    with LOG_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            try:
                events.append(
                    json.loads(line)
                )
            except json.JSONDecodeError:
                continue

    return events


def monitoring_summary(events=None) -> Dict[str, Any]:
    """Return aggregate execution health without exposing request contents."""
    event_rows = read_events() if events is None else events
    valid_times = []
    succeeded = 0
    failed = 0

    for event in event_rows:
        try:
            elapsed = float(event.get("time_taken", 0.0))
        except (TypeError, ValueError):
            elapsed = 0.0
        if math.isfinite(elapsed) and elapsed >= 0:
            valid_times.append(elapsed)

        status = str(event.get("status", "")).lower()
        if status in {"success", "completed"}:
            succeeded += 1
        elif status in {"failed", "error"}:
            failed += 1

    sorted_times = sorted(valid_times)
    p95_index = max(0, math.ceil(0.95 * len(sorted_times)) - 1)

    return {
        "total_events": len(event_rows),
        "successful_events": succeeded,
        "failed_events": failed,
        "average_execution_seconds": (
            round(sum(valid_times) / len(valid_times), 4)
            if valid_times else 0.0
        ),
        "p95_execution_seconds": (
            round(sorted_times[p95_index], 4)
            if sorted_times else 0.0
        ),
    }
