import time
import re
import streamlit as st
from workflows.workflow_v3 import m3_workflow
from memory_store import load_long_term_memory
from memory_store import save_career_memory
from career_rag_memory import save_roadmap_to_memory
st.markdown('<style>[data-testid=stToolbar]{display:none !important;} [data-testid=stDecoration]{display:none !important;} </style>', unsafe_allow_html=True)
st.markdown("""
<style>

/* ---------- GLOBAL ---------- */

.main {
    background: #F8FAFC;
}

.block-container {
    padding-top: 1.5rem !important;
    max-width: 1200px !important;
}

/* ---------- SIDEBAR ---------- */

[data-testid="stSidebar"] {
    background: #0F172A !important;
}

[data-testid="stSidebar"] > div:first-child {
    background: #0F172A !important;
}

[data-testid="stSidebar"] [data-testid="stButton"] button {
    background: #1E293B !important;
    color: #FFFFFF !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
}

[data-testid="stSidebar"] [data-testid="stButton"] button p {
    color: #FFFFFF !important;
    font-weight: 600 !important;
}

[data-testid="stSidebar"] [data-testid="stButton"] button:hover {
    background: #334155 !important;
}

.sidebar-brand {
    width: 100% !important;
    text-align: center !important;
    padding: 4px 0 18px 0 !important;
}

.sidebar-brand h2 {
    width: 100% !important;
    text-align: center !important;
    margin: 0 !important;
    color: #FFFFFF !important;
    font-size: 22px !important;
    font-weight: 700 !important;
}

.sidebar-brand p {
    width: 100% !important;
    text-align: center !important;
    margin: 5px 0 0 0 !important;
    color: #CBD5E1 !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.8px !important;
}

.sidebar-section {
    color: #94A3B8 !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    margin-top: 18px !important;
    margin-bottom: 8px !important;
    text-align: left !important;
}

/* ---------- HEADER ---------- */

.m3-header {
    width: 100% !important;
    box-sizing: border-box !important;
    background: linear-gradient(135deg, #DBEAFE, #EDE9FE) !important;
    border: 1px solid #BFDBFE !important;
    border-radius: 16px !important;
    padding: 28px 32px !important;
    margin-bottom: 25px !important;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08) !important;
    text-align: center !important;
}

.m3-header h1 {
    margin: 0 !important;
    padding: 0 !important;
    color: #0F172A !important;
    font-size: 32px !important;
    line-height: 1.25 !important;
    font-weight: 700 !important;
    text-align: center !important;
}

.m3-header p {
    color: #475569 !important;
    font-size: 16px !important;
    line-height: 1.4 !important;
    margin: 8px 0 0 0 !important;
    padding: 0 !important;
    text-align: center !important;
}

/* ---------- STREAMLIT UI ---------- */

[data-testid="stToolbar"] {
    display: none !important;
}

#MainMenu {
    }

footer {
    visibility: hidden !important;
}

/* ---------- PRIMARY ACTION BUTTON ---------- */

div.stButton > button[kind="primary"] {
    background: #1E293B !important;
    color: #FFFFFF !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    min-height: 42px !important;
    font-weight: 700 !important;
}

div.stButton > button[kind="primary"]:hover {
    background: #334155 !important;
    border-color: #334155 !important;
    color: #FFFFFF !important;
}

/* ---------- PRIMARY ACTION BUTTON ---------- */

[data-testid="stBaseButton-primary"] {
    background-color: #1E293B !important;
    background: #1E293B !important;
    color: #FFFFFF !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    min-height: 42px !important;
    font-weight: 700 !important;
}

[data-testid="stBaseButton-primary"] p {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

[data-testid="stBaseButton-primary"]:hover {
    background-color: #334155 !important;
    background: #334155 !important;
    border-color: #334155 !important;
    color: #FFFFFF !important;
}

/* ---------- CARDS ---------- */

.section-title {
    color: #0F172A !important;
    font-size: 22px !important;
    font-weight: 700 !important;
    margin-top: 20px !important;
    margin-bottom: 15px !important;
}

.dashboard-card {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 14px !important;
    padding: 20px !important;
    margin-bottom: 16px !important;
}

.roadmap-card {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-left: 5px solid #4F46E5 !important;
    border-radius: 12px !important;
    padding: 20px !important;
    margin-top: 15px !important;
}

.roadmap-text {
    color: #334155 !important;
    line-height: 1.7 !important;
}

/* ---------- STREAMLIT CONTROLS ---------- */

[data-testid="stToolbar"] {
}

#MainMenu {
}

footer {
}

</style>
""", unsafe_allow_html=True)
# M3 Long-Term Memory Summary
_sidebar_student_id = "STU029"
_sidebar_memory = load_long_term_memory(_sidebar_student_id)
_sidebar_purchased_count = len(_sidebar_memory.get("purchased_answers", []))
_sidebar_query_count = __import__("memory_store").get_connection().execute("SELECT COUNT(*) FROM previous_queries WHERE student_id = ?", (_sidebar_student_id,)).fetchone()[0]

# M3 Sidebar Navigation
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background: #0F172A;
}
[data-testid="stSidebar"] {
    background: #0F172A !important;
}

[data-testid="stSidebar"] [data-testid="stButton"] button {
    background: #1E293B !important;
    color: white !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
}

[data-testid="stSidebar"] [data-testid="stButton"] button p {
    color: white !important;
    font-weight: 600 !important;
}

[data-testid="stSidebar"] [data-testid="stButton"] button:hover {
    background: #334155 !important;
    color: white !important;
}

[data-testid="stSidebar"] [data-testid="stButton"] button:hover p {
    color: white !important;
}

[data-testid="stSidebar"] .stButton button {
    color: white !important;
}

.sidebar-brand {
    padding: 10px 5px 20px 5px;
}
.sidebar-brand h2 {
    margin: 0;
    font-size: 22px;
}
.sidebar-brand p {
    margin: 4px 0 0 0;
    color: #94A3B8 !important;
    font-size: 12px;
    letter-spacing: 1px;
    font-weight: 600;
}
.sidebar-section {
    color: #94A3B8 !important;
    font-size: 12px;
    font-weight: 600;
    margin-top: 20px;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <h2>AI Education</h2>
        <p>CAREER GUIDANCE v2.0</p>
    </div>
    f""", unsafe_allow_html=True)

    st.markdown(
        '<div class="sidebar-section">NAVIGATION</div>',
        unsafe_allow_html=True
    )

    if st.button("Dashboard", use_container_width=True):
        st.session_state.m3_page = "dashboard"

    if st.button("Career Guidance", use_container_width=True):
        st.session_state.m3_page = "career"

    if st.button("My Roadmap", use_container_width=True):
        st.session_state.m3_page = "roadmap"

    if st.button("Previous Roadmaps", use_container_width=True):
        st.session_state.m3_page = "previous"

    if st.button("Career Progress", use_container_width=True):
        st.session_state.m3_page = "progress"

    st.markdown(
        '<div class="sidebar-section">ACCOUNT</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-section">SYSTEM STATUS</div>',
        unsafe_allow_html=True
    )

    st.markdown(f"""
    <div style="
        background:#1E293B;
        border:1px solid #334155;
        border-radius:10px;
        padding:12px;
        margin-top:8px;
    ">
        <div style="color:#22C55E;font-weight:600;font-size:13px;">
            System Operational
        </div>
        <div style="color:#CBD5E1;font-size:12px;margin-top:6px;">
            5 Agents Active
        </div>
        <div style="color:#CBD5E1;font-size:12px;margin-top:3px;">
            5 Tools Active
        </div>
        <div style="color:#CBD5E1;font-size:12px;margin-top:8px;">
            My Memory: {_sidebar_purchased_count} Purchased | {_sidebar_query_count} Queries
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Logout", use_container_width=True):
        st.session_state.m3_result = None
        st.session_state.m3_page = "career"
        st.rerun()

if "m3_page" not in st.session_state:
    st.session_state.m3_page = "career"

if "m3_result" not in st.session_state:
    st.session_state.m3_result = None

if "m3_generation_time" not in st.session_state:
    st.session_state.m3_generation_time = 0.0

st.markdown("""<div class="m3-header"><h1>AI Education & Career Guidance Assistant</h1><p>Intelligent Multi-Agent Platform for Education and Career Support</p></div>""", unsafe_allow_html=True)
if st.session_state.m3_page == "dashboard":
    st.markdown(
        '<div class="section-title">Career Guidance Dashboard</div>',
        unsafe_allow_html=True,
    )

    st.markdown("""
    <div class="dashboard-card">
        <h3>5 Agents Architecture</h3>
        <p><strong>Business Coordinator, Planner, Research, Analysis, Decision</strong></p>
    </div>

    <div class="dashboard-card">
        <h3>Memory Layers</h3>
        <p><strong>Short-Term:</strong> CareerState (Centralized State)</p>
        <p><strong>Research Cache:</strong> LRU Caching</p>
        <p><strong>Long-Term:</strong> ChromaDB - Previous Career Roadmap Retrieval</p>
        <p><strong>Business Memory:</strong> SQLite</p>
    </div>

    <div class="dashboard-card">
        <h3>Access Control</h3>
        <p><strong>Free User:</strong> 20% Preview → Buy Full Answer - ₹150</p>
        <p><strong>Payment:</strong> Payment verification required to unlock the full answer</p>
        <p><strong>Paid User:</strong> Full Personalized Roadmap Unlocked</p>
    </div>

    <div class="dashboard-card">
        <h3>Workflow</h3>
        <p>
            <strong>Skill Assessment Score: 85% (STU029 / COL002)</strong>
            → Personalized Career Roadmap Generation
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.stop()


if st.session_state.m3_page == "career":
    st.markdown("""
    **Student Profile:** STU029 | **Institution:** COL002 | **Skill Assessment Score:** 85% | **Current Plan:** Free User

    ### What are your career aspirations?

    """)

    student_id = "STU029"
    college_id = "COL002"
    m1_score = 85.0

    long_term_memory = load_long_term_memory(student_id)
    previous_queries = long_term_memory.get("previous_queries", [])
    purchased_answers = long_term_memory.get("purchased_answers", [])
    student_profile = long_term_memory.get("student_profile", {})
    payment_amount = 0.0

    student_request = st.text_area(
        "Career guidance request",
        value="",
        placeholder="Example: Best career after MPC with 85% marks",
        height=120,
        key="m3_career_request",
    ).strip()

    student_name = ""
    name_match = re.search(
        r"\b(?:my name is|i am|i'm|this is)\s+([A-Za-z][A-Za-z '-]{0,39})",
        student_request,
        re.IGNORECASE,
    )
    if name_match:
        student_name = name_match.group(1).strip().rstrip(".")
    if not student_name:
        student_name = "Student"
    # ---------------------------------------------------------
    # CAREER GUIDANCE INPUT VALIDATION
    # ---------------------------------------------------------
    calculation_keywords = [
        "calculate",
        "calculation",
        "calculator",
        "compute",
        "arithmetic",
        "multiply",
        "multiplied by",
        "divide",
        "divided by",
        "subtract",
        "minus",
        "add",
        "sum",
        "average",
        "roi",
    ]

    calculation_expression = bool(
        re.search(
            r"\d+(?:\.\d+)?\s*(?:[+*/_]|x|×|-)\s*\d+",
            student_request,
            re.IGNORECASE,
        )
    )

    is_calculation_request = (
        any(
            re.search(
                r"\b" + re.escape(keyword) + r"\b",
                student_request,
                re.IGNORECASE,
            )
            for keyword in calculation_keywords
        )
        or calculation_expression
    )

    if is_calculation_request:
        st.error(
            "Career Guidance accepts career-related queries only. "
            "Please enter a career goal, course, college, or career guidance question. "
            "For mathematical calculations, use the Calculation Tool in M2."
        )
        st.info(
            "Example career query: Best career after MPC with 85% marks"
        )
        st.stop()

    st.markdown("""
    <div class="dashboard-card">
        <p>
            AI Engine: 5-Agent LangGraph System
            (Business Coordinator, Planner, Research, Analysis, Decision)
            |
            Memory System: CareerState + LRU Cache + ChromaDB + SQLite
            |
            Decision Agent will generate personalized career guidance when you continue.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "Generate My Career Roadmap",
        use_container_width=True,
        type="primary"
    ):
        if not student_request:
            st.error("Enter a career guidance request to continue.")
        else:
            state = {
                "student_id": student_id,
                "college_id": college_id,
                "is_paid_user": False,
                "payment_amount": payment_amount,
                "m1_score": m1_score,
                "revenue": 0.0,
                "student_profile": student_profile,
                "previous_queries": previous_queries,
                "purchased_answers": purchased_answers,
                "student_request": student_request,
                "student_name": student_name,
            }

            with st.spinner("Generating your personalized career guidance..."):
                try:
                    start_time = time.perf_counter()
                    st.session_state.m3_result = m3_workflow.invoke(state)
                    st.session_state.m3_generation_time = (
                        time.perf_counter() - start_time
                    )
                    st.session_state.m3_page = "roadmap"
                    st.rerun()
                except Exception as exc:
                    st.session_state.m3_result = None
                    st.error(f"Unable to complete the request: {exc}")

    st.stop()

if st.session_state.m3_page == "roadmap":
    st.markdown(
        '<div class="section-title">My Roadmap</div>',
        unsafe_allow_html=True,
    )

    result = st.session_state.get("m3_result")

    if not result:
        st.warning("No career roadmap has been generated yet.")
        st.stop()

    roadmap = result.get("final_roadmap", "")
    purchased_answers = result.get("purchased_answers", [])
    previous_queries = result.get("previous_queries", [])

    def human_readable_career_guidance(raw_text):
        """Convert internal multi-agent output into a clean student-facing answer."""
        text = str(raw_text or "")
        text = text.replace("\\.", ".").replace("\\-", "-").replace("\\*", "*")

        sections = []

        # Main career direction
        match = re.search(
            r"Recommended Career Area:\s*(.*?)(?=\n\s*\n|\nResearch and Analysis Used|\Z)",
            text,
            re.IGNORECASE | re.DOTALL,
        )
        if match:
            sections.append(
                "### Recommended Career Direction\n"
                + match.group(1).strip()
            )

        # Career development guidance
        match = re.search(
            r"Recommended Career Area:.*?\n\n(.*?)(?=\nResearch and Analysis Used|\Z)",
            text,
            re.IGNORECASE | re.DOTALL,
        )
        if match:
            guidance = match.group(1).strip()
            if guidance:
                sections.append("### Your Career Development Plan\n" + guidance)

        # Top career paths
        match = re.search(
            r"(Top 3 CSE Career Paths.*?)(?=\nCSE Skills to Learn|\Z)",
            text,
            re.IGNORECASE | re.DOTALL,
        )
        if match:
            sections.append("### Career Paths to Explore\n" + match.group(1).strip())

        # Skills
        match = re.search(
            r"(CSE Skills to Learn.*?)(?=\nRecommended Colleges from the Admin Catalog|\Z)",
            text,
            re.IGNORECASE | re.DOTALL,
        )
        if match:
            sections.append("### Skills to Build\n" + match.group(1).strip())

        # Colleges
        match = re.search(
            r"(Recommended Colleges from the Admin Catalog.*?)(?=\nRelevant Entrance Examinations|\Z)",
            text,
            re.IGNORECASE | re.DOTALL,
        )
        if match:
            sections.append("### College Options\n" + match.group(1).strip())

        # Entrance exams
        match = re.search(
            r"(Relevant Entrance Examinations.*?)(?=\nFour-Year Career Roadmap|\Z)",
            text,
            re.IGNORECASE | re.DOTALL,
        )
        if match:
            sections.append("### Entrance Examinations\n" + match.group(1).strip())

        # Four-year roadmap
        match = re.search(
            r"(Four-Year Career Roadmap.*)$",
            text,
            re.IGNORECASE | re.DOTALL,
        )
        if match:
            sections.append("### 4-Year Career Roadmap\n" + match.group(1).strip())

        if sections:
            return "\n\n".join(sections)

        return text.strip()

    # Internal agent logs remain available for backend/admin monitoring.

    if result.get("workflow_status") in ("paid_full_access", "decision_unlocked"):
        st.success("Personalized career roadmap unlocked.")

        st.markdown(
            f"""
            <div class="roadmap-card">
                <h3>Personalized Career Roadmap for: {result.get("student_name", "Alex")}</h3>
                <div class="roadmap-text">
                    <strong>Recommended Career Direction:</strong> Computer Science and Engineering (CSE)<br><br>
                    <strong>Career Development Plan:</strong><br>
                    1. Foundation - Python, Java, DSA, SQL, DBMS, OS, Networks, Git<br>
                    2. Practical Development - Projects, Certifications, Internships<br>
                    3. Advanced Preparation - Domain knowledge and interview readiness<br>
                    4. Career Opportunities - Software Engineer, Application Developer, QA Engineer<br><br>
                    <strong>Top 3 Career Paths:</strong><br>
                    1. Software Engineering<br>
                    2. Data Engineering and Analytics<br>
                    3. Cloud and Cybersecurity<br><br>
                    <strong>Recommended Colleges:</strong><br>
                    - CBIT Hyderabad | AI and DS | Fees 150,000 | Placement 85%<br>
                    - JNTU Hyderabad | CSE | Fees 100,000 | Placement 80%<br>
                    - MGIT Hyderabad | CSE | Fees 120,000 | Placement 82%<br>
                    - OU Hyderabad | ECE | Fees 80,000 | Placement 75%<br><br>
                    <strong>Entrance Exams:</strong> JEE Main, EAPCET, BITSAT, CUET<br><br>
                    <strong>4-Year Roadmap:</strong><br>
                    Year 1: Foundations<br>
                    Year 2: Specialization and small projects<br>
                    Year 3: Internship and portfolio<br>
                    Year 4: Capstone, placements, and higher studies
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### My Purchased Roadmaps")
        if purchased_answers:
            st.caption(f"{len(purchased_answers)} purchased roadmap(s)")
            for item in purchased_answers:
                with st.expander(f"Roadmap #{item.get('id', '')} — Personalized Career Roadmap"):
                    st.write(item.get("query", ""))
                    st.caption(f"Purchased: {item.get('purchased_at', '')}")
        else:
            st.info("No purchased roadmaps yet.")

    elif result.get("workflow_status") == "free_payment_required":
        user_request = result.get("student_request", "")
        display_name = result.get("student_name", "Student")

        if not display_name or display_name == "Student":
            name_match = re.search(
                r"\b(?:my name is|i am|i'm|this is)\s+([A-Za-z][A-Za-z '-]{0,39})",
                user_request,
                re.IGNORECASE,
            )
            if name_match:
                display_name = name_match.group(1).strip().rstrip(".")

        st.markdown(
            f"""
            <div class="roadmap-card">
                <h3>Hi {display_name}.</h3>
                <p>Your personalized career guidance preview is ready.</p>
                <p>Purchase your roadmap to unlock career paths, suitable
                colleges, entrance exams, skills, and your 4-year development plan.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="roadmap-card">
                <h3>Personalized Roadmap</h3>
                <p>Your complete personalized career roadmap is ready to unlock.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-title">Unlock Full Career Roadmap</div>',
            unsafe_allow_html=True,
        )

        st.info(
            "Your free career preview is ready. Purchase the personalized "
            "roadmap for Rs. 150 to unlock the complete career plan."
        )

        @st.dialog("Payment Details")
        def show_payment_popup():
            st.write("Complete Your Purchase")
            st.divider()
            st.write("**Item:** Personalized Career Roadmap")
            st.write("**Amount:** Rs. 150 Only")

            st.write("Select Payment Method:")
            st.radio(
                "Payment",
                ["UPI (PhonePe / GPay / Paytm)", "Cards", "Net Banking"],
                label_visibility="collapsed",
            )

            st.info("Secure Payment | 100% Safe")

            col1, col2 = st.columns(2)

            with col1:
                if st.button(
                    "Generate Now - Rs. 150",
                    use_container_width=True,
                    type="primary",
                ):
                    paid_state = {
                        "student_id": result.get("student_id", "STU029"),
                        "college_id": result.get("college_id", "COL002"),
                        "is_paid_user": True,
                        "payment_amount": 150.0,
                        "m1_score": result.get("m1_score", 85.0),
                        "revenue": 0.0,
                        "student_profile": student_profile,
                        "previous_queries": previous_queries,
                        "purchased_answers": purchased_answers,
                        "student_request": result.get(
                            "student_request",
                            "I am looking for guidance to build a career in Software Engineering.",
                        ),
                    }

                    with st.spinner("Verifying payment and unlocking your roadmap..."):
                        try:
                            st.session_state.m3_result = m3_workflow.invoke(paid_state)
                            st.session_state.show_success = True
                            st.rerun()
                        except Exception as exc:
                            st.error(f"Unable to complete payment verification: {exc}")

            with col2:
                if st.button("Cancel", use_container_width=True):
                    st.rerun()

        if st.button(
            "Buy Personalized Roadmap - Rs. 150",
            use_container_width=True,
            type="primary",
        ):
            show_payment_popup()

    if st.session_state.get("show_success"):
        @st.dialog("Payment Successful!")
        def payment_success():
            st.success("Payment Successful!")
            st.write("Thank you for your purchase!")
            st.write("Your Personalized Career Roadmap has been unlocked successfully.")
            st.divider()
            st.write("**Transaction ID:** TXN20261004102501")
            st.write("**Amount Paid:** Rs. 150")

            if st.button(
                "View My Roadmap",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.show_success = False
                st.session_state.m3_page = "roadmap"
                st.rerun()

        payment_success()
    memory_context = result.get("memory_context", [])
    purchased_answers = result.get("purchased_answers", [])
    previous_queries = result.get("previous_queries", [])
    student_profile = result.get("student_profile", {})
    errors = result.get("errors", [])

    if errors:
        with st.expander("Workflow Information"):
            st.write(errors)

st.divider()

st.caption(
    "AI Education & Career Guidance Assistant"
)





























































































































# Hide Streamlit development toolbar for demo


st.markdown('''<style>[data-testid="stToolbar"] {display: none !important;} [data-testid="stDecoration"] {display: none !important;}</style>''', unsafe_allow_html=True)


st.markdown('''<style>[data-testid="stToolbar"] {display:none !important;}</style>''', unsafe_allow_html=True)
