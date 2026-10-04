from datetime import datetime

from payment_verification import verify_student_payment, PAYMENT_AMOUNT
from state import CareerState
from monitoring import log_event
from memory_store import (
    find_purchased_answer,
    save_purchased_answer,
    save_previous_query,
)


class BusinessAccessAgent:
    name = "BusinessAccess"

    def _log(self, state, event, status="success", details=""):
        logs = state.setdefault("logs", [])
        logs.append({
            "timestamp": datetime.now().isoformat(),
            "agent": self.name,
            "event": event,
            "status": status,
            "details": details,
        })

    def process_access(self, state: CareerState):
        start = datetime.now()

        student_id = state.get("student_id", "").strip()
        college_id = state.get("college_id", "").strip()
        is_paid_user = bool(state.get("is_paid_user", False))
        payment_amount = float(state.get("payment_amount", 0.0))

        decision_data = state.get("decision_data", {})

        user_request = state.get(
            "student_request",
            "Career guidance",
        ).strip()

        tool_result = decision_data.get(
            "decision",
            state.get("final_roadmap", ""),
        )

        topic = decision_data.get(
            "topic",
            user_request,
        )

        # Check long-term memory before requesting another payment.
        save_previous_query(
            student_id=student_id,
            query=user_request,
        )

        previous_purchase = find_purchased_answer(
            student_id=student_id,
            query=user_request,
        )

        # Reuse an existing purchase for the same student and same request.
        # A different student can still purchase the same career roadmap.
        if previous_purchase:
            state["payment_verified"] = True
            state["payment_status"] = "already_purchased"
            state["revenue"] = 0.0
            state["workflow_status"] = "paid_full_access"
            state["purchase_required"] = False
            state["purchase_amount"] = float(
                previous_purchase.get("amount", PAYMENT_AMOUNT)
                or PAYMENT_AMOUNT
            )
            state["full_answer"] = previous_purchase.get("answer", "")
            state["final_roadmap"] = state["full_answer"]
            state["preview_answer"] = state["full_answer"]
            state["skip_memory_save"] = True

            self._log(
                state,
                "Existing purchase reused",
                "success",
                "Existing purchased roadmap reused for this student and request.",
            )

            return state

        payment_result = verify_student_payment(
            student_id=student_id,
            payment_status=is_paid_user,
            amount=payment_amount,
        )

        state["payment_verified"] = payment_result["verified"]
        state["payment_status"] = payment_result["status"]

        elapsed = (datetime.now() - start).total_seconds()

        if payment_result["verified"]:
            state["revenue"] = PAYMENT_AMOUNT

            decision = decision_data.get("decision", "").strip()

            career_name = decision_data.get("career_name", "").strip()

            if career_name and decision:
                state["final_roadmap"] = (
                    f"User Request:\n{user_request}\n\n"
                    f"Decision Agent Output:\n{tool_result}\n\n"
                    f"Personalized Career Roadmap:\n{decision}"
                )
            else:
                state["final_roadmap"] = (
                    f"User Request:\n{user_request}\n\n"
                    f"Decision Agent Output:\n{tool_result}"
                )

            state["workflow_status"] = "paid_full_access"
            state["purchase_required"] = False
            state["purchase_amount"] = PAYMENT_AMOUNT
            state["full_answer"] = state["final_roadmap"]
            state["preview_answer"] = decision_data.get(
                "preview_answer",
                state["final_roadmap"],
            )

            save_purchased_answer(
                student_id=student_id,
                college_id=college_id,
                query=user_request,
                answer=state["full_answer"],
                amount=PAYMENT_AMOUNT,
            )

            self._log(
                state,
                "Student payment verified",
                "success",
                f"Rs. {PAYMENT_AMOUNT:.0f} payment verified. Full roadmap unlocked.",
            )

            log_event(
                college_id=college_id,
                student_id=student_id,
                agent_name=self.name,
                time_taken=elapsed,
                status="success",
                is_paid_user=True,
                revenue=PAYMENT_AMOUNT,
                event="Student payment verified",
                student_request=user_request,
            )

            state.setdefault("agent_timings", {})[self.name] = round(
                elapsed,
                4,
            )

            return state

        state["revenue"] = 0.0

        state["full_answer"] = decision_data.get(
            "full_answer",
            decision_data.get("decision", tool_result),
        )
        state["preview_answer"] = decision_data.get(
            "preview_answer",
            state["full_answer"],
        )
        state["purchase_required"] = True
        state["purchase_amount"] = PAYMENT_AMOUNT
        state["final_roadmap"] = state["preview_answer"]

        state["workflow_status"] = "free_payment_required"

        self._log(
            state,
            "Student payment required",
            "pending",
            payment_result["message"],
        )

        log_event(
            college_id=college_id,
            student_id=student_id,
            agent_name=self.name,
            time_taken=elapsed,
            status="pending",
            is_paid_user=False,
            revenue=0.0,
            event="Student payment required",
            student_request=user_request,
        )

        state.setdefault("agent_timings", {})[self.name] = round(
            elapsed,
            4,
        )

        return state


def business_access_node(state):
    agent = BusinessAccessAgent()
    return agent.process_access(state)


# Backward-compatible alias
process_business_access = business_access_node



