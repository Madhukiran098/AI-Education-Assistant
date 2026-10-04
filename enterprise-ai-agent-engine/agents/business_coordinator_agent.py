from datetime import datetime
from typing import Any, Dict

from state import CareerState
from college_subscription import verify_college_subscription
from monitoring import log_event


class BusinessCoordinatorAgent:
    name = "BusinessCoordinator"

    def _log(self, state, event, status="success", details=""):
        logs = state.setdefault("logs", [])
        logs.append({
            "timestamp": datetime.now().isoformat(),
            "agent": self.name,
            "event": event,
            "status": status,
            "details": details,
        })

    def _message(self, state, to_agent, data, status="success"):
        messages = state.setdefault("messages", [])
        messages.append({
            "from": self.name,
            "to": to_agent,
            "college_id": state.get("college_id", ""),
            "data": data,
            "status": status,
            "timestamp": datetime.now().isoformat(),
        })

    def coordinate(self, state: CareerState):
        start = datetime.now()

        state.setdefault("logs", [])
        state.setdefault("messages", [])
        state.setdefault("errors", [])
        state.setdefault("retry_count", 0)
        state.setdefault("agent_timings", {})
        state.setdefault("memory_context", [])

        student_request = state.get("student_request", "").strip()
        college_id = state.get("college_id", "").strip()

        if not student_request:
            error_message = "Student request is required."

            state["errors"].append({
                "agent": self.name,
                "error": error_message,
                "timestamp": datetime.now().isoformat(),
            })

            state["workflow_status"] = "failed"
            self._log(state, "Request validation", "failed", error_message)

            elapsed = (datetime.now() - start).total_seconds()

            log_event(
                college_id=college_id,
                student_id=state.get("student_id", ""),
                agent_name=self.name,
                time_taken=elapsed,
                status="failed",
                is_paid_user=state.get("is_paid_user"),
                revenue=float(state.get("revenue", 0.0)),
                event="Request validation",
                student_request=student_request,
            )

            return state

        if not college_id:
            error_message = "College ID is required."

            state["errors"].append({
                "agent": self.name,
                "error": error_message,
                "timestamp": datetime.now().isoformat(),
            })

            state["workflow_status"] = "failed"
            self._log(state, "Business validation", "failed", error_message)

            elapsed = (datetime.now() - start).total_seconds()

            log_event(
                college_id=college_id,
                student_id=state.get("student_id", ""),
                agent_name=self.name,
                time_taken=elapsed,
                status="failed",
                is_paid_user=state.get("is_paid_user"),
                revenue=float(state.get("revenue", 0.0)),
                event="Business validation",
                student_request=student_request,
            )

            return state

        subscription = verify_college_subscription(college_id)

        if not subscription["verified"]:
            error_message = subscription["message"]

            state["errors"].append({
                "agent": self.name,
                "error": error_message,
                "timestamp": datetime.now().isoformat(),
            })

            state["college_verified"] = False
            state["workflow_status"] = "failed"

            self._log(
                state,
                "College subscription verification",
                "failed",
                error_message,
            )

            elapsed = (datetime.now() - start).total_seconds()

            log_event(
                college_id=college_id,
                student_id=state.get("student_id", ""),
                agent_name=self.name,
                time_taken=elapsed,
                status="failed",
                is_paid_user=state.get("is_paid_user"),
                revenue=float(state.get("revenue", 0.0)),
                event="College subscription verification",
                student_request=student_request,
            )

            return state

        state["college_verified"] = True
        state["current_agent"] = self.name
        state["workflow_status"] = "coordinating"

        details = (
            f'College {college_id} has an active '
            f'?{subscription["annual_fee"]:.0f} annual subscription.'
        )

        self._log(
            state,
            "College subscription verified",
            "success",
            details,
        )

        self._message(
            state,
            "Planner",
            {
                "student_request": student_request,
                "action": "create_plan",
                "college_verified": True,
            },
        )

        elapsed = (datetime.now() - start).total_seconds()

        state.setdefault("agent_timings", {})[self.name] = round(
            elapsed,
            4,
        )

        log_event(
            college_id=college_id,
            student_id=state.get("student_id", ""),
            agent_name=self.name,
            time_taken=elapsed,
            status="success",
            is_paid_user=state.get("is_paid_user"),
            revenue=float(state.get("revenue", 0.0)),
            event="College subscription verified",
            student_request=student_request,
        )

        state["workflow_status"] = "ready_for_planning"

        return state


def coordinate_business_request(state):
    coordinator = BusinessCoordinatorAgent()
    return coordinator.coordinate(state)
