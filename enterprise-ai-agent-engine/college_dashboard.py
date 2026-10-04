import streamlit as st

from college_admin_dashboard import render_college_admin_dashboard
from dashboard_data import calculate_dashboard_metrics
from monitoring import read_events


st.set_page_config(
    page_title="College Admin Dashboard",
    page_icon=None,
    layout="wide",
)


def render_college_dashboard(college_id: str = "COL002"):

    st.markdown(
        """
        <style>
/* College Admin color scheme */


        .stApp {
            background: #F8FAFC;
        }

        [data-testid="stSidebar"] {
            background: #0F172A;
        }

        [data-testid="stSidebar"] * {
            color: #E2E8F0;
        }

        .dashboard-title {
            font-size: 34px;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 4px;
        }

        .dashboard-subtitle {
            font-size: 16px;
            color: #64748B;
            margin-bottom: 28px;
        }

        .section-title {
            font-size: 21px;
            font-weight: 650;
            color: #0F172A;
            margin-top: 25px;
            margin-bottom: 14px;
        }

        .metric-card {
            background: white;
            border: 1px solid #E2E8F0;
            border-radius: 14px;
            padding: 20px;
            min-height: 125px;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
        }

        .metric-label {
            color: #64748B;
            font-size: 14px;
            margin-bottom: 8px;
        }

        .metric-value {
            color: #0F172A;
            font-size: 29px;
            font-weight: 700;
        }

        .metric-note {
            color: #94A3B8;
            font-size: 12px;
            margin-top: 5px;
        }



        /* Career Trends - blue visual theme */
        [data-testid="stVegaLiteChart"] {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 14px !important;
            padding: 12px !important;
        }

        [data-testid="stSidebar"] [data-testid="stButton"] button { background: #1E293B !important; color: #FFFFFF !important; border: 1px solid #334155 !important; border-radius: 8px !important; }

        [data-testid="stSidebar"] [data-testid="stButton"] button p { color: #FFFFFF !important; }

        .info-card {
            background: white;
            border: 1px solid #E2E8F0;
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 15px;
        }
        </style>
<style>
/* College Admin color scheme */


[data-testid="stAppDeployButton"] {
    display: none !important;
}
</style>
        """,
        unsafe_allow_html=True,
    )

    metrics = calculate_dashboard_metrics(college_id)
    events = read_events()

    college_events = [
        event
        for event in events
        if event.get("college_id") == college_id
    ]

    if "admin_page" not in st.session_state:
        st.session_state.admin_page = "dashboard"
    # Sidebar
    with st.sidebar:
        st.markdown("## AI Education")
        st.markdown("### COLLEGE ADMIN")
        st.divider()

        st.markdown("**Dashboard**")
        if st.button("Student Analytics", use_container_width=True):
            st.session_state.admin_page = "analytics"
            st.rerun()

        if st.button("Business Performance", use_container_width=True):
            st.session_state.admin_page = "business"
            st.rerun()

        if st.button("Communication Logs", use_container_width=True):
            st.session_state.admin_page = "logs"
            st.rerun()

        if st.button("College Catalog", use_container_width=True):
            st.session_state.admin_page = "catalog"
            st.rerun()

        st.divider()

        st.markdown(
            f"""
            <div style="
                background:#1E293B;
                border:1px solid #334155;
                border-radius:10px;
                padding:12px 14px;
                margin:8px 0 16px 0;
            ">
                <div style="
                    color:#94A3B8;
                    font-size:12px;
                    margin-bottom:4px;
                ">College ID</div>
                <div style="
                    color:#FFFFFF;
                    font-size:20px;
                    font-weight:700;
                ">{college_id}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        st.markdown("**System Status**")
        st.success("System Operational")

    # Header
    st.markdown(
        '<div class="dashboard-title">College Admin Dashboard</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'Business monitoring, student analytics and platform performance'
        '</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.admin_page == "catalog":
        render_college_admin_dashboard()
        st.stop()

    if st.session_state.admin_page == "analytics":
        st.markdown(
            '<div class="section-title">Student Analytics</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Total Students</div>
                <div class="metric-value">{metrics["total_students"]}</div>
                <div class="metric-note">Unique students</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if college_events:
            student_records = {}
            for event in college_events:
                student_id = event.get("student_id", "")
                if student_id:
                    student_records[student_id] = {
                        "Student ID": student_id,
                        "Paid User": (
                            "Yes"
                            if event.get("is_paid_user") is True
                            else "No"
                        ),
                        "Career Request": event.get(
                            "student_request",
                            "",
                        ),
                        "Revenue": float(
                            event.get("revenue", 0.0)
                        ),
                    }

            if student_records:
                st.dataframe(
                    list(student_records.values()),
                    use_container_width=True,
                    hide_index=True,
                )
        st.stop()

    if st.session_state.admin_page == "business":
        st.markdown(
            '<div class="section-title">Business Performance</div>',
            unsafe_allow_html=True,
        )

        cols = st.columns(3)

        performance_cards = [
            (
                "Revenue Generated",
                f'₹{metrics["revenue_generated"]:.0f}',
                "Student payments",
            ),
            (
                "Average Response Time",
                f'{metrics["average_response_time"]:.4f}s',
                "Successful agent events",
            ),
            (
                "Failure Rate",
                f'{metrics["failure_rate"]:.1f}%',
                "Failed monitoring events",
            ),
        ]

        for col, (label, value, note) in zip(cols, performance_cards):
            with col:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">{label}</div>
                        <div class="metric-value">{value}</div>
                        <div class="metric-note">{note}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown(
            f'**Paid Students:** {metrics["paid_students"]}'
        )
        st.markdown(
            f'**Free Students:** {metrics["free_students"]}'
        )
        st.markdown(
            f'**Conversion Rate:** {metrics["paid_conversion_rate"]:.1f}%'
        )
        st.stop()

    if st.session_state.admin_page == "logs":
        st.markdown(
            '<div class="section-title">Communication Logs</div>',
            unsafe_allow_html=True,
        )

        if college_events:
            log_rows = []

            for event in reversed(college_events):
                log_rows.append(
                    {
                        "Agent": event.get(
                            "agent_name",
                            "Unknown",
                        ),
                        "Student ID": event.get(
                            "student_id",
                            "",
                        ),
                        "Status": event.get(
                            "status",
                            "unknown",
                        ),
                        "Response Time": (
                            f'{float(event.get("time_taken", 0)):.4f}s'
                        ),
                        "Event": event.get(
                            "event",
                            "",
                        ),
                    }
                )

            st.dataframe(
                log_rows,
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No communication logs available.")

        st.caption(
            f"Monitoring events recorded for college {college_id}: "
            f'{metrics["total_events"]}'
        )
        st.stop()
    # Business overview
    st.markdown(
        '<div class="section-title">Business Overview</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(4)

    cards = [
        (
            "Total Students",
            str(metrics["total_students"]),
            "Unique students",
        ),
        (
            "Free Students",
            str(metrics["free_students"]),
            "Current free users",
        ),
        (
            "Paid Students",
            str(metrics["paid_students"]),
            "Paid users",
        ),
        (
            "Conversion Rate",
            f'{metrics["paid_conversion_rate"]:.1f}%',
            "Free to paid conversion",
        ),
    ]

    for col, (label, value, note) in zip(cols, cards):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-note">{note}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Performance
    st.markdown(
        '<div class="section-title">Revenue & Performance</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(3)

    performance_cards = [
        (
            "Revenue Generated",
            f'₹{metrics["revenue_generated"]:.0f}',
            "Student payments",
        ),
        (
            "Average Response Time",
            f'{metrics["average_response_time"]:.4f}s',
            "Successful agent events",
        ),
        (
            "Failure Rate",
            f'{metrics["failure_rate"]:.1f}%',
            "Failed monitoring events",
        ),
    ]

    for col, (label, value, note) in zip(cols, performance_cards):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-note">{note}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown(
        '<div class="section-title">Student Purchase & Execution Flow</div>',
        unsafe_allow_html=True,
    )

    flow_steps = [
        ("1", "Student Request", "Student submits a career guidance request."),
        ("2", "AI Processing", "Business Coordinator → Planner → Research → Analysis → Decision."),
        ("3", "Free Preview", "Student receives basic career direction and guidance."),
        ("4", "Purchase", "Student can unlock the complete roadmap for ₹150."),
        ("5", "Payment Verification", "Business Access verifies the ₹150 payment."),
        ("6", "Full Roadmap", "Personalized career roadmap is unlocked."),
        ("7", "Memory & Monitoring", "Roadmap, revenue and execution logs are stored."),
    ]

    for number, title, description in flow_steps:
        st.markdown(
            f"""
            <div class="info-card">
                <div style="font-size:13px;color:#64748B;font-weight:600;">
                    STEP {number}
                </div>
                <div style="font-size:19px;color:#0F172A;font-weight:700;margin-top:4px;">
                    {title}
                </div>
                <div style="font-size:14px;color:#64748B;margin-top:5px;">
                    {description}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="business-model-card">
            <div style="font-size:15px;color:#0F172A;font-weight:700;">
                Business Model
            </div>
            <div style="font-size:14px;color:#64748B;margin-top:6px;">
                Free users receive a basic career preview. Students who purchase
                the ₹150 personalized roadmap receive full career guidance.
                College subscription: ₹5,000/year.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Career trends
    st.markdown(
        '<div class="section-title">Career Trends</div>',
        unsafe_allow_html=True,
    )

    trends = metrics.get("career_trends", {})

    if trends:
        chart_data = {
            "Career": list(trends.keys()),
            "Students": list(trends.values()),
        }

        st.bar_chart(
            chart_data,
            x="Career",
            y="Students",
        )
    else:
        st.info(
            "Career trend data will appear as student career requests are recorded."
        )

if __name__ == "__main__":
    render_college_dashboard()
























st.markdown('''<style>[data-testid="stToolbar"] {display:none !important;}</style>''', unsafe_allow_html=True)
