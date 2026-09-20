import streamlit as st
import requests
import html

st.set_page_config(
    page_title="AI Education & Career Guidance Assistant",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

BACKEND_URL = "http://127.0.0.1:8002"

USERNAME = "student@aiassistant.com"
PASSWORD = "AI@12345"

if "page" not in st.session_state:
    st.session_state.page = "m1"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "selected_tool" not in st.session_state:
    st.session_state.selected_tool = None

if "answer" not in st.session_state:
    st.session_state.answer = None


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    [data-testid="stToolbar"] { display: none !important; }

    .stApp {
        background: #F8FAFC;
    }

    .block-container {
        padding-top: 1.4rem;
        padding-left: 2.2rem;
        padding-right: 2.2rem;
        padding-bottom: 2rem;
    }

    /* DARK BLUE SIDEBAR */
    section[data-testid="stSidebar"] {
        background: #0F172A !important;
    }

    section[data-testid="stSidebar"] > div {
        background: #0F172A !important;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    section[data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        color: #E2E8F0 !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        text-align: left !important;
        margin-bottom: 7px;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #1E3A5F !important;
        border-color: #60A5FA !important;
    }

    /* TITLE */
    .title-box {
        background: linear-gradient(135deg, #DBEAFE, #EDE9FE);
        border: 1px solid #BFDBFE;
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 25px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08);
        text-align: center;
    }

    .title-main {
        color: #1E3A8A;
        font-size: 32px;
        font-weight: 900;
        letter-spacing: 0.2px;
        margin: 0;
    }

    .title-sub {
        color: #475569;
        font-size: 16px;
        margin-top: 8px;
        font-weight: 500;
    }

    .main-heading {
        color: #1E3A8A;
        font-size: 27px;
        font-weight: 800;
        margin-top: 8px;
        margin-bottom: 5px;
    }

    .main-description {
        color: #64748B;
        font-size: 15px;
        margin-bottom: 22px;
    }

    /* OVERVIEW CARDS */
    .overview-card {
        background: white;
        border: 1px solid #DBE3EE;
        border-radius: 13px;
        padding: 18px;
        text-align: center;
        min-height: 95px;
        box-shadow: 0 2px 7px rgba(15, 23, 42, 0.05);
    }

    .overview-number {
        color: #1D4ED8;
        font-size: 24px;
        font-weight: 850;
    }

    .overview-label {
        color: #64748B;
        font-size: 13px;
        margin-top: 5px;
    }

    /* AGENT / TOOL CARDS */
    .card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 21px;
        min-height: 145px;
        margin-bottom: 10px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06);
    }

    .card-title {
        color: #1E3A8A;
        font-size: 18px;
        font-weight: 750;
        margin-bottom: 8px;
    }

    .card-text {
        color: #64748B;
        font-size: 14px;
        line-height: 1.55;
    }

    .active-badge {
        display: inline-block;
        margin-top: 12px;
        padding: 4px 10px;
        border-radius: 20px;
        background: #DCFCE7;
        color: #166534;
        font-size: 11px;
        font-weight: 700;
    }

    /* TOOL SELECTION */
    .selected-tool {
        background: #EFF6FF;
        border-left: 5px solid #2563EB;
        border-radius: 9px;
        padding: 14px 18px;
        margin: 18px 0;
        color: #1E3A8A;
        font-weight: 750;
    }

    /* ANSWER */
    .answer-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 24px;
        margin-top: 22px;
        box-shadow: 0 3px 10px rgba(15, 23, 42, 0.07);
    }

    .answer-title {
        color: #1E3A8A;
        font-size: 20px;
        font-weight: 800;
        margin-bottom: 12px;
    }

    .answer-text {
        color: #334155;
        font-size: 15px;
        line-height: 1.75;
        white-space: pre-wrap;
    }

    /* LOGIN */
    .login-box {
        background: white;
        border: 1px solid #DBE3EE;
        border-radius: 16px;
        padding: 32px;
        max-width: 540px;
        margin: 35px auto;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.08);
    }

    /* BUTTONS */
    .stButton > button {
        background: #1E293B !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        min-height: 42px;
        font-weight: 700;
    }

    .stButton > button:hover {
        background: #334155 !important;
        color: white !important;
    }

    textarea {
        border-radius: 10px !important;
    }

    input {
        border-radius: 8px !important;
    }

    .footer {
        text-align: center;
        color: #94A3B8;
        font-size: 12px;
        margin-top: 45px;
        padding-top: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# COMMON HEADER
# ============================================================

def show_header():
    st.markdown(
        """
        <div class="title-box">
            <div class="title-main">
                AI Education & Career Guidance Assistant
            </div>
            <div class="title-sub">
                Intelligent Multi-Agent Platform for Education and Career Support
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            text-align:center;
            font-size:22px;
            font-weight:850;
            margin-top:8px;
            margin-bottom:3px;
        ">
            AI Education
        </div>

        <div style="
            text-align:center;
            color:#60A5FA !important;
            font-size:11px;
            font-weight:700;
            letter-spacing:1px;
            margin-bottom:25px;
        ">
            CAREER GUIDANCE v2.0
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Dashboard", use_container_width=True):
        st.session_state.page = "m1"
        st.rerun()

    if st.button("AI Agents (4)", use_container_width=True):
        if st.session_state.logged_in:
            st.session_state.page = "m2"
        else:
            st.session_state.page = "login"
        st.rerun()

    if st.button("Tools Hub (9)", use_container_width=True):
        if st.session_state.logged_in:
            st.session_state.page = "m2"
        else:
            st.session_state.page = "login"
        st.rerun()

    if st.button("Analytics", use_container_width=True):
        if st.session_state.logged_in:
            st.session_state.page = "m2"
        else:
            st.session_state.page = "login"
        st.rerun()

    st.markdown(
        """
        <div style="
            background:#1E293B;
            border-radius:10px;
            padding:15px;
            margin-top:35px;
        ">
            <div style="font-size:11px;color:#94A3B8 !important;font-weight:700;">
                SYSTEM STATUS
            </div>
            <div style="color:#22C55E !important;font-weight:700;margin-top:8px;">
                System Operational
            </div>
            <div style="font-size:13px;margin-top:7px;">
                4 Agents Active
            </div>
            <div style="font-size:13px;margin-top:4px;">
                9 Tools Integrated
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# BACKEND
# ============================================================

def run_backend(request_text):

    try:
        response = requests.post(
            f"{BACKEND_URL}/run",
            json={"task": request_text},
            timeout=120
        )

        data = response.json()

        if response.status_code != 200:
            return "The request could not be processed."

        answer = data.get("answer")

        if answer:
            return str(answer).strip()

        return "The assistant processed the request, but no readable answer was returned."

    except requests.exceptions.ConnectionError:
        return (
            "The AI backend is not running. "
            "Please start the FastAPI backend and try again."
        )

    except requests.exceptions.Timeout:
        return "The request took too long to complete. Please try again."

    except Exception as e:
        return f"The request could not be completed: {str(e)}"


# ============================================================
# OVERVIEW
# ============================================================

def show_overview(tool_count=9):

    st.markdown("### Platform Overview")

    c1, c2, c3, c4 = st.columns(4)

    cards = [
        ("4", "AI Agents"),
        (str(tool_count), "Integrated Tools"),
        ("Active", "AI Engine"),
        ("Active", "System")
    ]

    for col, (number, label) in zip([c1, c2, c3, c4], cards):
        with col:
            st.markdown(
                f"""
                <div class="overview-card">
                    <div class="overview-number">{number}</div>
                    <div class="overview-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# AGENTS
# ============================================================

def show_agents():

    st.markdown("### AI Agents")

    agents = [
        (
            "Planner Agent",
            "Plans tasks and creates structured execution steps."
        ),
        (
            "Research Agent",
            "Retrieves relevant education and career information."
        ),
        (
            "Analysis Agent",
            "Analyzes information and identifies useful insights."
        ),
        (
            "Decision Agent",
            "Provides structured decision support and recommendations."
        )
    ]

    c1, c2 = st.columns(2)

    for index, (name, description) in enumerate(agents):

        col = c1 if index % 2 == 0 else c2

        with col:
            st.markdown(
                f"""
                <div class="card">
                    <div class="card-title">{name}</div>
                    <div class="card-text">{description}</div>
                    <span class="active-badge">ACTIVE</span>
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# M1
# ============================================================

if st.session_state.page == "m1":

    show_header()

    st.markdown(
        '<div class="main-heading">AI Education & Career Assistant</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-description">Choose a tool and ask the AI assistant what you need. The selected tool will help process your request and provide a clear, human-readable response.</div>',
        unsafe_allow_html=True
    )
    show_overview(9)
    st.markdown("")
    show_agents()

    st.markdown("### Enter Your Request")

    m1_request = st.text_area(
        "Enter Your Request",
        placeholder="How can AI help students choose the right career?",
        height=110,
        key="m1_request",
        label_visibility="collapsed"
    )

    c1, c2, c3 = st.columns([1, 1, 2])

    with c1:
        if st.button("Run AI Analysis", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

    st.markdown(
        '<div class="footer">AI Education & Career Guidance Assistant | Enterprise AI Platform | v2.0</div>',
        unsafe_allow_html=True
    )


# ============================================================
# LOGIN
# ============================================================

elif st.session_state.page == "login":

    show_header()

    st.markdown(
        '<div class="main-heading" style="text-align:center;">Welcome Back</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-description" style="text-align:center;">Sign in to access the AI Education & Career Assistant.</div>',
        unsafe_allow_html=True
    )

    email = st.text_input(
        "Email",
        value="student@aiassistant.com",
        placeholder="Enter your email"
    )

    password = st.text_input(
        "Password",
        value=PASSWORD,
        type="password",
        placeholder="Enter your password"
    )

    if st.button("Sign In", use_container_width=True):

        if email == USERNAME and password == PASSWORD:

            st.session_state.logged_in = True
            st.session_state.page = "m2"
            st.session_state.answer = None
            st.rerun()

        else:
            st.error("Invalid email or password.")

    if st.button("Back to Dashboard"):
        st.session_state.page = "m1"
        st.rerun()


# ============================================================
# M2
# ============================================================

elif st.session_state.page == "m2":

    if not st.session_state.logged_in:
        st.session_state.page = "login"
        st.rerun()

    show_header()

    st.markdown(
        '<div class="main-heading">AI Education & Career Assistant</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-description">Choose a tool and ask the AI assistant what you need. The selected tool will help process your request and provide a clear, human-readable response.</div>',
        unsafe_allow_html=True
    )
    show_overview(9)
    st.markdown("")

    tools = [
        ("Calculation", "Perform mathematical calculations.", "calculation"),
        ("Communication", "Create clear communication messages.", "communication"),
        ("Data Retrieval", "Retrieve information from configured data sources.", "data_retrieval"),
        ("Data Validation", "Validate information using common validation rules.", "data_validation"),
        ("Report Generation", "Generate structured reports from provided information.", "report_generation"),
        ("Study Planner", "Create structured study plans for students.", "study_planner"),
        ("Web Search", "Search for relevant information.", "web_search"),
        ("Email", "Create and simulate email tasks.", "email"),
        ("Calendar", "Check availability and manage meetings.", "calendar")
    ]

    st.markdown(f"### Tools Hub — {len(tools)} Tools")

    for start in range(0, len(tools), 3):

        row = tools[start:start + 3]
        cols = st.columns(3)

        for col, (name, description, tool_id) in zip(cols, row):

            with col:

                st.markdown(
                    f"""
                    <div class="card">
                        <div class="card-title">{name}</div>
                        <div class="card-text">{description}</div>
                        <span class="active-badge">ACTIVE</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    "Use Tool",
                    key=f"use_{tool_id}",
                    use_container_width=True
                ):
                    st.session_state.selected_tool = tool_id
                    st.session_state.answer = None
                    st.rerun()

    if st.session_state.selected_tool:

        selected = next(
            (
                item for item in tools
                if item[2] == st.session_state.selected_tool
            ),
            None
        )

        if selected:

            selected_name = selected[0]

            st.markdown(
                f"""
                <div class="selected-tool">
                    Selected Tool: {selected_name}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("### How can I help you?")

            request_text = st.text_area(
                "Enter Your Request",
                placeholder=f"Enter your request for {selected_name}...",
                height=120,
                key=f"request_{st.session_state.selected_tool}"
            )

            if st.button(
                "Run AI Analysis",
                key=f"run_{st.session_state.selected_tool}",
                use_container_width=False
            ):

                if not request_text.strip():

                    st.warning("Please enter your request.")

                else:

                    with st.spinner("Processing your request..."):

                        st.session_state.answer = run_backend(
                            request_text.strip()
                        )

            if st.session_state.answer:

                safe_answer = html.escape(
                    str(st.session_state.answer)
                ).replace("\n", "<br>")

                st.markdown(
                    f"""
                    <div class="answer-box">
                        <div class="answer-text">
                            {safe_answer}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            if st.button(
                "Clear Selected Tool",
                key="clear_tool"
            ):
                st.session_state.selected_tool = None
                st.session_state.answer = None
                st.rerun()

    st.markdown(
        '<div class="footer">AI Education & Career Guidance Assistant | Enterprise AI Platform | v2.0</div>',
        unsafe_allow_html=True
    )





