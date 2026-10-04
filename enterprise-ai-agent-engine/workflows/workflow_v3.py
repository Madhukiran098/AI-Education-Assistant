import asyncio
from datetime import datetime
from langgraph.graph import END, START, StateGraph

from state import CareerState
from monitoring import log_event
from memory_store import save_career_memory
from career_rag_memory import save_roadmap_to_memory, search_previous_roadmaps
from research_cache import cached_research

from agents.business_coordinator_agent import coordinate_business_request
from agents.business_access_agent import business_access_node
from agents.planner_agent import PlannerAgent
from agents.research_agent import ResearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.decision_agent import DecisionAgent
from payment_verification import verify_student_payment, PAYMENT_AMOUNT


planner_agent = PlannerAgent()
research_agent = ResearchAgent()
analysis_agent = AnalysisAgent()
decision_agent = DecisionAgent()


def add_agent_log(
    state: CareerState,
    agent_name: str,
    event: str,
    status: str = "success",
    time_taken: float = 0.0,
) -> None:
    state.setdefault("logs", []).append(
        {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "event": event,
            "status": status,
            "time_taken": round(time_taken, 4),
        }
    )

    state.setdefault("agent_timings", {})[agent_name] = round(
        time_taken,
        4,
    )

    log_event(
        college_id=state.get("college_id", ""),
        student_id=state.get("student_id", ""),
        agent_name=agent_name,
        time_taken=time_taken,
        status=status,
        is_paid_user=state.get("is_paid_user"),
        revenue=float(state.get("revenue", 0.0)),
        event=event,
        student_request=state.get("student_request", ""),
    )


def planner_node(state: CareerState) -> CareerState:
    start = datetime.now()

    try:
        request = state.get("student_request", "").strip()

        result = planner_agent.create_plan(request)

        state["planning_data"] = result
        state["short_term_memory"] = state.get("short_term_memory", {})
        state["short_term_memory"]["query"] = request
        state["short_term_memory"]["planner_output"] = result

        state["current_agent"] = "Planner"
        state["workflow_status"] = "planning_complete"

        elapsed = (datetime.now() - start).total_seconds()

        add_agent_log(
            state,
            "Planner",
            "Planning completed",
            "success",
            elapsed,
        )

        state.setdefault("messages", []).append(
            {
                "from": "Planner",
                "to": "Research",
                "college_id": state.get("college_id", ""),
                "data": state["planning_data"],
                "status": "success",
                "timestamp": datetime.now().isoformat(),
            }
        )

        return state

    except Exception as exc:
        state.setdefault("errors", []).append(
            {
                "agent": "Planner",
                "error": str(exc),
                "timestamp": datetime.now().isoformat(),
            }
        )

        state["workflow_status"] = "failed"

        elapsed = (datetime.now() - start).total_seconds()

        add_agent_log(
            state,
            "Planner",
            "Planning failed",
            "failed",
            elapsed,
        )

        return state


def research_node(state: CareerState) -> CareerState:
    start = datetime.now()

    try:
        request = state.get("student_request", "").strip()

        planner_result = state.get("planning_data", {})
        result = research_agent.research(planner_result)

        state["research_data"] = result
        state["short_term_memory"] = state.get("short_term_memory", {})
        state["short_term_memory"]["research_output"] = result
        state["current_agent"] = "Research"
        state["workflow_status"] = "research_complete"

        elapsed = (datetime.now() - start).total_seconds()

        add_agent_log(
            state,
            "Research",
            "Research completed",
            "success",
            elapsed,
        )

        state.setdefault("messages", []).append(
            {
                "from": "Research",
                "to": "Analysis",
                "college_id": state.get("college_id", ""),
                "data": result,
                "status": "success",
                "timestamp": datetime.now().isoformat(),
            }
        )

        return state

    except Exception as exc:
        state.setdefault("errors", []).append(
            {
                "agent": "Research",
                "error": str(exc),
                "timestamp": datetime.now().isoformat(),
            }
        )

        state["workflow_status"] = "failed"

        elapsed = (datetime.now() - start).total_seconds()

        add_agent_log(
            state,
            "Research",
            "Research failed",
            "failed",
            elapsed,
        )

        return state


def research_and_billing_node(state: CareerState) -> CareerState:
    start = datetime.now()

    try:
        request = state.get("student_request", "").strip()
        student_id = state.get("student_id", "").strip()
        is_paid_user = bool(state.get("is_paid_user", False))
        payment_amount = float(state.get("payment_amount", 0.0))

        async def run_parallel_tasks():
            research_task = asyncio.to_thread(
                cached_research,
                request,
            )

            billing_task = asyncio.to_thread(
                verify_student_payment,
                student_id,
                is_paid_user,
                payment_amount,
            )

            return await asyncio.gather(
                research_task,
                billing_task,
            )

        research_result, payment_result = asyncio.run(
            run_parallel_tasks()
        )

        state["research_data"] = research_result

        previous_roadmaps = search_previous_roadmaps(
            query=request,
            college_id=state.get("college_id", ""),
            k=3,
        )

        state["memory_context"] = [
            {
                "type": "previous_career_roadmap",
                "source": "Chroma RAG",
                "content": item.get("content", ""),
                "metadata": item.get("metadata", {}),
            }
            for item in previous_roadmaps
            if item.get("content")
            and item.get("metadata")
        ]

        state["payment_verified"] = payment_result.get(
            "verified",
            False,
        )
        state["payment_status"] = payment_result.get(
            "status",
            "",
        )

        if payment_result.get("verified"):
            state["revenue"] = PAYMENT_AMOUNT
        else:
            state["revenue"] = 0.0

        state["current_agent"] = "Research + Billing"
        state["workflow_status"] = "research_billing_completed"

        elapsed = (datetime.now() - start).total_seconds()

        state.setdefault("messages", []).append(
            {
                "from": "Research",
                "to": "Analysis",
                "college_id": state.get("college_id", ""),
                "data": research_result,
                "status": "success",
                "timestamp": datetime.now().isoformat(),
            }
        )

        log_event(
            college_id=state.get("college_id", ""),
            student_id=student_id,
            agent_name="Research",
            time_taken=elapsed,
            status="success",
            is_paid_user=is_paid_user,
            revenue=float(state.get("revenue", 0.0)),
            event="Research completed with parallel billing check",
            student_request=request,
        )

        log_event(
            college_id=state.get("college_id", ""),
            student_id=student_id,
            agent_name="BillingCheck",
            time_taken=elapsed,
            status=(
                "success"
                if payment_result.get("verified")
                else "pending"
            ),
            is_paid_user=is_paid_user,
            revenue=float(state.get("revenue", 0.0)),
            event="Payment eligibility checked in parallel",
            student_request=request,
        )

        state.setdefault("agent_timings", {})["Research"] = round(
            elapsed,
            4,
        )
        state.setdefault("agent_timings", {})["BillingCheck"] = round(
            elapsed,
            4,
        )

        return state

    except Exception as exc:
        state.setdefault("errors", []).append(
            {
                "agent": "Research + Billing",
                "error": str(exc),
                "timestamp": datetime.now().isoformat(),
            }
        )

        state["workflow_status"] = "failed"

        elapsed = (datetime.now() - start).total_seconds()

        log_event(
            college_id=state.get("college_id", ""),
            student_id=state.get("student_id", ""),
            agent_name="Research + Billing",
            time_taken=elapsed,
            status="failed",
            is_paid_user=bool(
                state.get("is_paid_user", False)
            ),
            revenue=0.0,
            event="Parallel research and billing failed",
            student_request=state.get(
                "student_request",
                "",
            ),
        )

        return state



def analysis_node(state: CareerState) -> CareerState:
    start = datetime.now()

    try:
        research_result = state.get("research_data", {})
        student_profile = state.get("student_profile", {})

        result = analysis_agent.analyze(
            research_result,
            student_profile=student_profile,
        )

        state["analysis_data"] = result
        state["short_term_memory"] = state.get("short_term_memory", {})
        state["short_term_memory"]["analysis_output"] = result
        state["current_agent"] = "Analysis"
        state["workflow_status"] = "analysis_complete"

        elapsed = (datetime.now() - start).total_seconds()

        add_agent_log(
            state,
            "Analysis",
            "Analysis completed",
            "success",
            elapsed,
        )

        state.setdefault("messages", []).append(
            {
                "from": "Analysis",
                "to": "Decision",
                "college_id": state.get("college_id", ""),
                "data": result,
                "status": "success",
                "timestamp": datetime.now().isoformat(),
            }
        )

        return state

    except Exception as exc:
        state.setdefault("errors", []).append(
            {
                "agent": "Analysis",
                "error": str(exc),
                "timestamp": datetime.now().isoformat(),
            }
        )

        state["workflow_status"] = "failed"

        elapsed = (datetime.now() - start).total_seconds()

        add_agent_log(
            state,
            "Analysis",
            "Analysis failed",
            "failed",
            elapsed,
        )

        return state


def decision_node(state: CareerState) -> CareerState:
    start = datetime.now()

    try:
        analysis_result = state.get("analysis_data", {})

        result = decision_agent.make_decision(
            analysis_result,
            m1_score=state.get("m1_score"),
            career_query=state.get(
                "student_request",
                analysis_result.get("topic", ""),
            ),
        )

        state["decision_data"] = result
        state["final_roadmap"] = result.get(
            "decision",
            "",
        )
        state["preview_answer"] = result.get(
            "preview_answer",
            "",
        )
        state["full_answer"] = result.get(
            "full_answer",
            result.get("decision", ""),
        )
        state["purchase_required"] = bool(
            result.get("purchase_required", False)
        )
        state["purchase_amount"] = float(
            result.get("purchase_amount", PAYMENT_AMOUNT)
        )
        state["short_term_memory"] = state.get("short_term_memory", {})
        state["short_term_memory"]["decision_output"] = result

        state["current_agent"] = "Decision"

        # M3: paid users receive the full roadmap immediately
        if state.get("is_paid_user", False) and state.get("payment_completed", False):
            state["purchase_required"] = False
            state["workflow_status"] = "decision_unlocked"
        else:
            state["workflow_status"] = "decision"

        elapsed = (datetime.now() - start).total_seconds()

        add_agent_log(
            state,
            "Decision",
            "Decision completed",
            "success",
            elapsed,
        )

        return state

    except Exception as exc:
        state.setdefault("errors", []).append(
            {
                "agent": "Decision",
                "error": str(exc),
                "timestamp": datetime.now().isoformat(),
            }
        )

        state["workflow_status"] = "failed"

        elapsed = (datetime.now() - start).total_seconds()

        add_agent_log(
            state,
            "Decision",
            "Decision failed",
            "failed",
            elapsed,
        )

        return state


def memory_save_node(state: CareerState) -> CareerState:
    try:
        if state.get('skip_memory_save', False):
            state['memory_save_pending'] = True
            state['workflow_status'] = state.get('workflow_status', 'completed')
            return state

        save_career_memory(state)

        rag_record_id = save_roadmap_to_memory(state)

        state["memory_context"] = state.get(
            "memory_context",
            [],
        )

        # Keep memory_context limited to previously retrieved
        # career roadmaps. The newly saved roadmap is represented
        # separately by the Chroma record ID.
        state["rag_record_id"] = rag_record_id

        state["workflow_status"] = state.get(
            "workflow_status",
            "completed",
        )

        return state
    except Exception as exc:
        state.setdefault("errors", []).append(
            {
                "agent": "MemoryStore",
                "error": str(exc),
                "timestamp": datetime.now().isoformat(),
            }
        )
        return state


def coordinator_router(state: CareerState):
    if state.get("workflow_status") == "failed":
        return "end"

    return "planner"


def agent_router(state: CareerState):
    if state.get("workflow_status") == "failed":
        return "end"

    current_agent = state.get("current_agent", "")

    if current_agent == "Planner":
        return "continue"

    if current_agent == "Research":
        return "continue"

    if current_agent == "Analysis":
        return "continue"

    if current_agent == "Decision":
        return "continue"

    return "end"

def build_m3_workflow():
    graph = StateGraph(CareerState)

    graph.add_node(
        "business_coordinator",
        coordinate_business_request,
    )

    graph.add_node(
        "planner",
        planner_node,
    )

    graph.add_node(
        "research",
        research_node,
    )

    graph.add_node(
        "analysis",
        analysis_node,
    )

    graph.add_node(
        "decision",
        decision_node,
    )

    graph.add_node(
        "business_access",
        business_access_node,
    )

    graph.add_node(
        "memory_save",
        memory_save_node,
    )

    graph.add_edge(
        START,
        "business_coordinator",
    )

    graph.add_conditional_edges(
        "business_coordinator",
        coordinator_router,
        {
            "planner": "planner",
            "end": END,
        },
    )

    graph.add_conditional_edges(
        "planner",
        agent_router,
        {
            "continue": "research",
            "end": END,
        },
    )

    graph.add_conditional_edges(
        "research",
        agent_router,
        {
            "continue": "analysis",
            "end": END,
        },
    )

    graph.add_node(
        "research_billing",
        research_and_billing_node,
    )

    graph.add_conditional_edges(
        "research_billing",
        agent_router,
        {
            "continue": "analysis",
            "end": END,
        },
    )

    graph.add_conditional_edges(
        "analysis",
        agent_router,
        {
            "continue": "decision",
            "end": END,
        },
    )

    graph.add_conditional_edges(
        "decision",
        agent_router,
        {
            "continue": "business_access",
            "end": END,
        },
    )

    graph.add_edge(
        "business_access",
        "memory_save",
    )

    graph.add_edge(
        "memory_save",
        END,
    )

    return graph.compile()


m3_workflow = build_m3_workflow()



