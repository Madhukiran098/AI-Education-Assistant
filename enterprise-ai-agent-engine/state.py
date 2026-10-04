from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict


class CareerState(TypedDict, total=False):
    """
    Shared state for the M3 enterprise career guidance workflow.

    The state is passed between the Coordinator, Planner, Research,
    Analysis and Decision agents.
    """

    # Student and business identity
    student_id: str
    college_id: str

    # Business / payment status
    is_paid_user: bool
    payment_amount: float
    payment_verified: bool
    payment_status: str
    college_verified: bool
    revenue: float

    # Student analysis
    m1_score: Optional[float]
    student_request: str
    m2_answer: str

    # Agent outputs
    planning_data: Dict[str, Any]
    research_data: Dict[str, Any]
    analysis_data: Dict[str, Any]
    decision_data: Dict[str, Any]
    final_roadmap: str

    # Agent communication
    messages: List[Dict[str, Any]]

    # Monitoring
    logs: List[Dict[str, Any]]
    agent_timings: Dict[str, float]

    # Error and retry management
    errors: List[Dict[str, Any]]
    retry_count: int

    # Memory references
    memory_context: List[Dict[str, Any]]
    rag_record_id: str

    # M3 Short-Term Memory
    short_term_memory: Dict[str, Any]

    # M3 Monetization and Answer Access
    preview_answer: str
    full_answer: str
    purchase_required: bool
    purchase_amount: float

    # M3 Long-Term Memory
    previous_queries: List[str]
    purchased_answers: List[Dict[str, Any]]
    student_profile: Dict[str, Any]

    # Workflow status
    current_agent: str
    workflow_status: str
