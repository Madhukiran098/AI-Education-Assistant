import streamlit as st

st.set_page_config(
    page_title="AI Education & Career Guidance Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "page" not in st.session_state:
    st.session_state.page = "dashboard"


def go_to_login():
    st.session_state.page = "login"


def go_to_dashboard():
    st.session_state.page = "dashboard"


st.markdown(
    """
    <style>

    .stApp {
        background: #f8fafc;
    }

    .main .block-container {
        max-width: 1400px;
        padding-top: 35px;
        padding-bottom: 50px;
    }

    section[data-testid="stSidebar"] {
        background: #0f2480;
        border-right: 1px solid #1e3a8a;
    }

    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    .sidebar-brand {
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .sidebar-subtitle {
        font-size: 12px;
        color: #cbd5e1 !important;
        line-height: 1.5;
        margin-bottom: 25px;
    }

    .sidebar-section {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        color: #cbd5e1 !important;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    .system-status {
        background: #dcfce7;
        color: #166534 !important;
        border-radius: 8px;
        padding: 10px 12px;
        font-size: 13px;
        font-weight: 700;
        text-align: center;
        margin-top: 10px;
    }

    .main-title {
        text-align: center;
        color: #0f172a;
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 18px;
        line-height: 1.2;
    }

    .subtitle-box {
        background: #f1f5f9;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 12px;
        text-align: center;
        color: #475569;
        font-size: 15px;
        margin: 0 auto 35px auto;
        max-width: 1000px;
    }

    .section-title {
        color: #0f172a;
        font-size: 22px;
        font-weight: 750;
        margin-top: 30px;
        margin-bottom: 18px;
    }

    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
        padding: 24px;
        text-align: center;
        min-height: 145px;
        transition: all 0.2s ease;
        margin-bottom: 8px;
    }

    .metric-card:hover {
        transform: translateY(-4px);
        border-color: #3b82f6;
        box-shadow: 0 5px 14px rgba(15, 23, 42, 0.10);
    }

    .metric-label {
        font-size: 11px;
        text-transform: uppercase;
        color: #64748b;
        letter-spacing: 1.2px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 34px;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.1;
        margin-bottom: 15px;
    }

    .request-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 24px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
    }

    .stButton > button {
        border-radius: 8px;
        font-weight: 650;
        min-height: 42px;
        border: 1px solid #cbd5e1;
        background: #ffffff;
        color: #0f172a;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        border-color: #3b82f6;
        color: #1d4ed8;
        background: #f8fafc;
    }

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 12px;
        margin-top: 45px;
        padding-top: 20px;
        border-top: 1px solid #e2e8f0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


if st.session_state.page == "login":

    st.markdown(
        """
        <div class="main-title">
            Student Login
        </div>

        <div class="subtitle-box">
            Access the AI Education & Career Guidance Assistant
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        username = st.text_input(
            "Username",
            placeholder="Enter your username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            if (
                username == "student@aiassistant.com"
                and password == "AI@12345"
            ):
                st.success("Login successful.")
                st.session_state.page = "dashboard"
                st.rerun()

            else:
                st.error("Username or password is incorrect.")

        if st.button(
            "Back to Dashboard",
            use_container_width=True
        ):
            go_to_dashboard()
            st.rerun()

    st.stop()


with st.sidebar:

    st.markdown(
        '<div class="sidebar-brand">AI Assistant</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">'
        'Education & Career Intelligence Platform'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        '<div class="sidebar-section">Navigation</div>',
        unsafe_allow_html=True
    )

    if st.button("Dashboard", use_container_width=True):
        st.session_state.page = "dashboard"
        st.rerun()

    if st.button("AI Assistant", use_container_width=True):
        go_to_login()
        st.rerun()

    if st.button("Tool Integration", use_container_width=True):
        go_to_login()
        st.rerun()

    if st.button("System Overview", use_container_width=True):
        go_to_login()
        st.rerun()

    st.divider()

    st.markdown(
        '<div class="sidebar-section">System Status</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="system-status">System Active - Online</div>',
        unsafe_allow_html=True
    )


st.markdown(
    """
    <div class="main-title">
        AI Education & Career Guidance Assistant
    </div>

    <div class="subtitle-box">
        AI-powered platform for education, career guidance and intelligent assistance
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    '<div class="section-title">Platform Overview</div>',
    unsafe_allow_html=True
)


def metric_card(label, value):

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


col1, col2, col3, col4 = st.columns(4)

with col1:

    metric_card("AI Agents", "4")

    if st.button(
        "View Details",
        key="agents_details",
        use_container_width=True
    ):
        go_to_login()
        st.rerun()


with col2:

    metric_card("Tools", "9")

    if st.button(
        "View Details",
        key="tools_details",
        use_container_width=True
    ):
        go_to_login()
        st.rerun()


with col3:

    metric_card("Platform", "Active")

    if st.button(
        "View Details",
        key="platform_details",
        use_container_width=True
    ):
        go_to_login()
        st.rerun()


with col4:

    metric_card("Status", "AI Enabled")

    if st.button(
        "View Details",
        key="status_details",
        use_container_width=True
    ):
        go_to_login()
        st.rerun()


st.markdown(
    '<div class="section-title">AI Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="request-card">',
    unsafe_allow_html=True
)

request = st.text_area(
    "Enter your request",
    placeholder="Enter an education or career-related request",
    height=120
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

if st.button(
    "Run AI Analysis",
    use_container_width=True
):
    go_to_login()
    st.rerun()


st.markdown(
    '<div class="section-title">Available Tools</div>',
    unsafe_allow_html=True
)


tools = [
    "Web Search",
    "Data Analysis",
    "Report Generation",
    "Study Planner",
    "Data Validation",
    "Communication",
    "Data Retrieval",
    "Email",
    "Calendar"
]


tool_columns = st.columns(4)


for index, tool_name in enumerate(tools):

    with tool_columns[index % 4]:

        if st.button(
            tool_name,
            key=f"tool_{index}",
            use_container_width=True
        ):
            go_to_login()
            st.rerun()


st.markdown(
    """
    <div class="footer">
        AI Education & Career Guidance Assistant
    </div>
    """,
    unsafe_allow_html=True
)