import sqlite3
from pathlib import Path


DEFAULT_DB_PATH = Path(__file__).resolve().parent / "data" / "college_admin.db"


def _connect(db_path=None):
    path = Path(db_path) if db_path else DEFAULT_DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_college_db(db_path=None):
    with _connect(db_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS colleges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                course TEXT NOT NULL,
                fees REAL CHECK (fees IS NULL OR fees >= 0),
                placement REAL CHECK (
                    placement IS NULL OR (placement >= 0 AND placement <= 100)
                ),
                location TEXT NOT NULL DEFAULT ''
            )
            """
        )
        columns = {
            row[1]: row
            for row in connection.execute("PRAGMA table_info(colleges)")
        }
        if columns.get("fees", (None, None, None, None, 0))[3] or columns.get(
            "placement", (None, None, None, None, 0)
        )[3]:
            connection.execute(
                """
                CREATE TABLE colleges_updated (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    course TEXT NOT NULL,
                    fees REAL CHECK (fees IS NULL OR fees >= 0),
                    placement REAL CHECK (
                        placement IS NULL OR (placement >= 0 AND placement <= 100)
                    ),
                    location TEXT NOT NULL DEFAULT ''
                )
                """
            )
            connection.execute(
                """
                INSERT INTO colleges_updated (id, name, course, fees, placement, location)
                SELECT id, name, course, fees, placement, location FROM colleges
                """
            )
            connection.execute("DROP TABLE colleges")
            connection.execute("ALTER TABLE colleges_updated RENAME TO colleges")


def seed_sample_colleges(db_path=None):
    samples = [
        ("JNTU Hyderabad", "CSE", 100000, 80, "Hyderabad"),
        ("CBIT Hyderabad", "AI and DS", 150000, 85, "Hyderabad"),
        ("OU Hyderabad", "ECE", 80000, 75, "Hyderabad"),
        ("MGIT Hyderabad", "CSE", 120000, 82, "Hyderabad"),
    ]
    initialize_college_db(db_path)
    with _connect(db_path) as connection:
        for college in samples:
            connection.execute(
                """
                INSERT INTO colleges (name, course, fees, placement, location)
                SELECT ?, ?, ?, ?, ?
                WHERE NOT EXISTS (
                    SELECT 1 FROM colleges WHERE name = ? AND course = ?
                )
                """,
                (*college, college[0], college[1]),
            )


def create_college(name, course, fees, placement, location="", db_path=None):
    name = str(name or "").strip()
    course = str(course or "").strip()
    fees = None if fees is None else float(fees)
    placement = None if placement is None else float(placement)
    location = str(location or "").strip()

    if not name or not course:
        raise ValueError("College name and course are required.")
    if fees is not None and fees < 0:
        raise ValueError("Fees cannot be negative.")
    if placement is not None and not 0 <= placement <= 100:
        raise ValueError("Placement must be between 0 and 100 percent.")

    initialize_college_db(db_path)
    with _connect(db_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO colleges (name, course, fees, placement, location)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, course, fees, placement, location),
        )
        return int(cursor.lastrowid)


def list_colleges(db_path=None):
    initialize_college_db(db_path)
    with _connect(db_path) as connection:
        rows = connection.execute(
            "SELECT id, name, course, fees, placement, location "
            "FROM colleges ORDER BY name, course"
        ).fetchall()
    return [dict(row) for row in rows]


def update_college(
    college_id,
    name,
    course,
    fees,
    placement,
    location="",
    db_path=None,
):
    name = str(name or "").strip()
    course = str(course or "").strip()
    fees = None if fees is None else float(fees)
    placement = None if placement is None else float(placement)
    location = str(location or "").strip()

    if not name or not course:
        raise ValueError("College name and course are required.")
    if fees is not None and fees < 0:
        raise ValueError("Fees cannot be negative.")
    if placement is not None and not 0 <= placement <= 100:
        raise ValueError("Placement must be between 0 and 100 percent.")

    initialize_college_db(db_path)
    with _connect(db_path) as connection:
        cursor = connection.execute(
            """
            UPDATE colleges
            SET name = ?, course = ?, fees = ?, placement = ?, location = ?
            WHERE id = ?
            """,
            (name, course, fees, placement, location, int(college_id)),
        )
        return cursor.rowcount > 0


def delete_college(college_id, db_path=None):
    initialize_college_db(db_path)
    with _connect(db_path) as connection:
        cursor = connection.execute(
            "DELETE FROM colleges WHERE id = ?",
            (int(college_id),),
        )
        return cursor.rowcount > 0


def search_colleges(query, db_path=None):
    query_lower = str(query or "").lower()
    initialize_college_db(db_path)
    if "mpc" in query_lower and not any(
        course in query_lower for course in ("cse", "ece", "ai", "data science")
    ):
        return list_colleges(db_path)

    if "cse" in query_lower:
        with _connect(db_path) as connection:
            rows = connection.execute(
                """
                SELECT id, name, course, fees, placement, location
                FROM colleges
                WHERE (
                    LOWER(course) LIKE '%cse%'
                    OR LOWER(course) LIKE '%ai and ds%'
                )
                AND fees >= 100000
                AND fees <= 150000
                AND (placement IS NULL OR placement <= 85)
                ORDER BY fees, name
                LIMIT 10
                """
            ).fetchall()
        return [dict(row) for row in rows]
    stop_words = {
        "a", "an", "and", "after", "best", "career", "for", "in", "low", "near",
        "of", "the", "with", "college", "colleges", "university",
        "universities", "fee", "fees", "cost", "affordable", "percent",
        "marks", "mark", "score",
    }
    terms = [
        term.strip(".,?!:;()[]{}\"'")
        for term in str(query or "").lower().split()
    ]
    terms = [term for term in terms if len(term) > 1 and term not in stop_words]

    sql = "SELECT id, name, course, fees, placement, location FROM colleges"
    parameters = []
    if terms:
        clauses = []
        for term in terms:
            pattern = f"%{term}%"
            clauses.append("(LOWER(name) LIKE ? OR LOWER(course) LIKE ? OR LOWER(location) LIKE ?)")
            parameters.extend((pattern, pattern, pattern))
        sql += " WHERE " + " OR ".join(clauses)
    sql += " ORDER BY fees, name LIMIT 10"

    with _connect(db_path) as connection:
        rows = connection.execute(sql, parameters).fetchall()
    return [dict(row) for row in rows]


def render_college_admin_dashboard(db_path=None):
    import streamlit as st

    seed_sample_colleges(db_path)
    st.markdown("### College Catalog")
    st.caption("Manage colleges that the Career Guidance Research Agent can retrieve.")

    with st.form("create_college_form", clear_on_submit=True):
        st.markdown("**Add College**")
        name = st.text_input("College Name", key="catalog_new_name")
        course = st.text_input("Course", key="catalog_new_course")
        fees = st.number_input(
            "Annual Fees (leave blank if unknown)",
            min_value=0.0,
            value=None,
            step=1000.0,
            key="catalog_new_fees",
        )
        placement = st.number_input(
            "Placement Percentage (leave blank if unknown)",
            min_value=0.0,
            max_value=100.0,
            value=None,
            step=1.0,
            key="catalog_new_placement",
        )
        location = st.text_input("Location", key="catalog_new_location")
        submitted = st.form_submit_button("Add College")

    if submitted:
        try:
            create_college(name, course, fees, placement, location, db_path)
            st.success("College added to the catalog.")
            st.rerun()
        except (TypeError, ValueError, sqlite3.Error) as exc:
            st.error(str(exc))

    colleges = list_colleges(db_path)
    if not colleges:
        st.info("No colleges have been added yet.")
        return

    st.dataframe(colleges, use_container_width=True, hide_index=True)
    by_id = {college["id"]: college for college in colleges}
    selected_id = st.selectbox(
        "Select a college to edit or delete",
        options=list(by_id),
        format_func=lambda college_id: (
            f'{by_id[college_id]["name"]} - {by_id[college_id]["course"]}'
        ),
    )
    selected = by_id[selected_id]

    with st.form("edit_college_form"):
        st.markdown("**Edit College**")
        edit_name = st.text_input("College Name", value=selected["name"], key="catalog_edit_name")
        edit_course = st.text_input("Course", value=selected["course"], key="catalog_edit_course")
        edit_fees = st.number_input(
            "Annual Fees",
            min_value=0.0,
            value=float(selected["fees"]),
            step=1000.0,
            key="catalog_edit_fees",
        )
        edit_placement = st.number_input(
            "Placement Percentage",
            min_value=0.0,
            max_value=100.0,
            value=float(selected["placement"]),
            step=1.0,
            key="catalog_edit_placement",
        )
        edit_location = st.text_input(
            "Location",
            value=selected["location"],
            key="catalog_edit_location",
        )
        update_submitted = st.form_submit_button("Save Changes")

    if update_submitted:
        try:
            update_college(
                selected_id,
                edit_name,
                edit_course,
                edit_fees,
                edit_placement,
                edit_location,
                db_path,
            )
            st.success("College details updated.")
            st.rerun()
        except (TypeError, ValueError, sqlite3.Error) as exc:
            st.error(str(exc))

    if st.button("Delete Selected College", type="secondary"):
        delete_college(selected_id, db_path)
        st.success("College deleted from the catalog.")
        st.rerun()



