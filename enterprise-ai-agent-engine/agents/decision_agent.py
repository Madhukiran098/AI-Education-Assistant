import re


class DecisionAgent:
    """M3 Decision Agent - Monetization and Final Answer Agent."""

    def __init__(self):
        self.name = "Decision Agent"
        self.role = "Monetization & Final Answer Agent"
        self.payment_amount = 150.0

    def is_career_request(self, topic):
        topic = (topic or "").lower()

        career_terms = [
            "career",
            "job",
            "employment",
            "profession",
            "developer",
            "software engineer",
            "software career",
            "government job",
            "upsc",
            "civil services",
            "public service",
            "finance career",
            "banking career",
            "investment career",
            "career roadmap",
            "career guidance",
            "career path",
            "internship",
            "placement",
        ]

        return any(term in topic for term in career_terms)

    def _create_preview(self, full_answer):
        if not full_answer:
            return "No final answer is available."

        preview_length = max(
            1,
            int(len(full_answer) * 0.20)
        )

        preview = full_answer[:preview_length].strip()

        if len(full_answer) > preview_length:
            preview += "\n\n[Preview ends here. Full personalized answer is locked.]"

        return preview

    def make_decision(
        self,
        analysis_result,
        m1_score=None,
        career_query=None,
    ):
        analysis_result = analysis_result or {}

        topic = (
            career_query
            or analysis_result.get("topic")
            or ""
        ).strip()

        analysis = str(
            analysis_result.get("analysis", "")
        ).strip()

        score = float(m1_score or 0)

        if score >= 80:
            interest_level = "High Interest"
        elif score >= 60:
            interest_level = "Good Interest"
        else:
            interest_level = "Developing Interest"

        if not self.is_career_request(topic):
            full_answer = (
                "Decision guidance for the provided request.\n\n"
                f"{analysis}"
            )

            return {
                "agent": self.name,
                "role": self.role,
                "topic": topic,
                "decision": full_answer,
                "full_answer": full_answer,
                "preview_answer": self._create_preview(full_answer),
                "purchase_required": False,
                "purchase_amount": 0.0,
                "m1_score": score,
                "m1_interest": interest_level,
                "career_name": "",
                "analysis_input": analysis_result,
            }

        lower_topic = topic.lower()
        name_match = re.search(
            r"\bmy name is\s+([A-Za-z][A-Za-z'-]*)",
            topic,
            re.IGNORECASE,
        )
        student_name = name_match.group(1) if name_match else ""

        recommendation_detail = ""
        personalized_greeting = (
            f"Personalized guidance for {student_name}\n\n"
            if student_name else ""
        )

        if "mpc" in lower_topic:
            is_cse_request = any(term in lower_topic for term in [
                "cse", "computer science", "software engineering"
            ])
            if is_cse_request:
                career_name = "Computer Science and Engineering (CSE)"
                skills = (
                    "Programming in Python or Java, data structures and "
                    "algorithms, SQL and DBMS, operating systems, computer "
                    "networks, Git, problem solving, and technical communication."
                )
                roles = (
                    "Software Engineer, Application Developer, QA Engineer, "
                    "and entry-level Data or Cloud Engineering roles."
                )
            else:
                career_name = "MPC STEM Pathways"
                skills = (
                    "Mathematics, physics fundamentals, logical reasoning, "
                    "problem solving, communication, and programming basics."
                )
                roles = (
                    "Software Engineer, Electronics Engineer, Data Analyst, "
                    "and other STEM roles depending on the selected course."
                )

            research_result = analysis_result.get("research_input", {})
            catalog = research_result.get("tool_results", {}).get(
                "College Catalog",
                [],
            )
            if catalog:
                # Keep all valid admin-catalog colleges in the roadmap.
                # Do not exclude colleges solely because of their fee range.
                college_lines = [
                    (
                        f'- {college["name"]}: {college["course"]}; '
                        f'fees {college["fees"]:,.0f}'
                        if college.get("fees") is not None else
                        f'- {college["name"]}: {college["course"]}; '
                        "fees not listed"
                    )
                    + (
                        f'; placement {college["placement"]:.0f}%; '
                        f'{college["location"]}'
                        if college.get("placement") is not None else
                        f'; placement not listed; {college["location"]}'
                    )
                    for college in catalog
                ]
                college_recommendations = "\n".join(college_lines)
            else:
                college_recommendations = (
                    "No matching college records are currently listed in "
                    "the College Admin catalog."
                )

            if is_cse_request:
                top_career_paths = (
                    "Top 3 CSE Career Paths\n"
                    "1. Software Engineering: build applications, services, "
                    "and production systems.\n"
                    "2. Data Engineering and Analytics: build data pipelines "
                    "and use databases and analytics tools.\n"
                    "3. Cloud and Cybersecurity: learn cloud infrastructure, "
                    "network security, and secure system design.\n\n"
                )
            else:
                top_career_paths = (
                    "Top 3 Career Recommendations (MPC)\n"
                    "1. Computer Science and Engineering: suited to students "
                    "interested in programming, software, and technology.\n"
                    "2. Electronics and Electrical Engineering: suited to "
                    "students interested in circuits, devices, and applied physics.\n"
                    "3. Data Science, Mathematics, or Statistics: suited to "
                    "students interested in quantitative analysis and computing.\n\n"
                )

            recommendation_detail = (
                top_career_paths +
                "CSE Skills to Learn\n"
                "Build programming fundamentals, data structures and "
                "algorithms, SQL/DBMS, operating systems, computer networks, "
                "Git, and practical project experience.\n\n"
                "Recommended Colleges from the Admin Catalog\n"
                f"{college_recommendations}\n\n"
                "Relevant Entrance Examinations\n"
                "JEE Main and JEE Advanced (where eligible), the relevant "
                "state engineering entrance exam such as EAPCET, BITSAT for "
                "BITS programs, and CUET for participating universities. "
                "For Architecture, check NATA or the applicable JEE route. "
                "Confirm current eligibility and exam requirements with "
                "each institution.\n\n"
                "Four-Year Career Roadmap\n"
                "Year 1: Strengthen mathematics and science foundations; "
                "explore introductory programming and core subjects.\n"
                "Year 2: Choose a specialization, build practical skills, "
                "and complete small course-related projects.\n"
                "Year 3: Complete an internship or substantial project, "
                "develop a portfolio, and prepare for placement or higher study.\n"
                "Year 4: Finish a capstone project, apply for relevant roles "
                "or postgraduate programs, and prepare for interviews or "
                "entrance examinations.\n\n"
            )

        elif any(term in lower_topic for term in [
            "software",
            "developer",
            "programming",
            "python",
            "technology",
        ]):
            career_name = "Software Career"
            skills = (
                "Programming, problem solving, data structures, "
                "databases, software development, and practical projects."
            )
            roles = (
                "Software Developer, Python Developer, Web Developer, "
                "Data Analyst, and related technology roles."
            )

        elif any(term in lower_topic for term in [
            "government",
            "upsc",
            "civil services",
            "public service",
        ]):
            career_name = "Government Career"
            skills = (
                "Subject knowledge, current affairs, analytical reasoning, "
                "communication, and competitive examination preparation."
            )
            roles = (
                "Civil Services, State Government Services, "
                "Administrative Services, and related public-sector roles."
            )

        elif any(term in lower_topic for term in [
            "finance",
            "mba",
            "banking",
            "investment",
            "business",
        ]):
            career_name = "Finance and Business Career"
            skills = (
                "Financial analysis, accounting, communication, "
                "business management, Excel, and analytical decision-making."
            )
            roles = (
                "Financial Analyst, Banking Professional, Business Analyst, "
                "Investment-related roles, and management positions."
            )

        else:
            career_name = "Career Guidance Path"
            skills = (
                "Communication, domain knowledge, digital skills, "
                "problem solving, and practical experience."
            )
            roles = (
                "Relevant entry-level professional roles based on the "
                "student's qualification and specialization."
            )

        full_answer = (
            personalized_greeting +
            f"Personalized Career Roadmap for {student_name}\n\n"
            f"Recommended Career Area: {career_name}\n\n"
            "1. Foundation\n"
            f"Build the following skills: {skills}\n\n"
            "2. Practical Development\n"
            "Complete relevant projects, certifications, internships, "
            "and practical assignments that demonstrate the required skills.\n\n"
            "3. Advanced Preparation\n"
            "Develop stronger domain knowledge, communication skills, "
            "problem-solving ability, and interview readiness.\n\n"
            "4. Career Opportunities\n"
            f"Potential role areas include: {roles}\n\n"
            "5. Personalized Next Step\n"
            "Follow the selected pathway consistently and review progress "
            "against eligibility, skills, experience, and career goals.\n\n"
            f"{recommendation_detail}"
        )

        return {
            "agent": self.name,
            "role": self.role,
            "topic": topic,
            "decision": full_answer,
            "full_answer": full_answer,
            "preview_answer": self._create_preview(full_answer),
            "purchase_required": True,
            "purchase_amount": self.payment_amount,
            "m1_score": score,
            "m1_interest": interest_level,
            "career_name": career_name,
            "analysis_input": analysis_result,
        }













