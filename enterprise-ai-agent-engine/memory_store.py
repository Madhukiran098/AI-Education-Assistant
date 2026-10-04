import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

DB_DIR = Path("data")
DB_FILE = DB_DIR / "m3_memory.db"


def get_connection():
    DB_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_memory_db():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS career_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                college_id TEXT NOT NULL,
                is_paid_user INTEGER NOT NULL DEFAULT 0,
                revenue REAL NOT NULL DEFAULT 0.0,
                student_request TEXT,
                final_roadmap TEXT,
                created_at TEXT NOT NULL
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS previous_queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                query TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS purchased_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                college_id TEXT,
                query TEXT NOT NULL,
                answer TEXT NOT NULL,
                amount REAL NOT NULL DEFAULT 0.0,
                purchased_at TEXT NOT NULL
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS student_profiles (
                student_id TEXT PRIMARY KEY,
                career_preferences TEXT,
                purchased_count INTEGER NOT NULL DEFAULT 0,
                total_spent REAL NOT NULL DEFAULT 0.0,
                updated_at TEXT NOT NULL
            )
            """
        )

        connection.commit()


def save_career_memory(state: Dict[str, Any]) -> int:
    initialize_memory_db()

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO career_memory (
                student_id,
                college_id,
                is_paid_user,
                revenue,
                student_request,
                final_roadmap,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                state.get("student_id", ""),
                state.get("college_id", ""),
                int(bool(state.get("is_paid_user", False))),
                float(state.get("revenue", 0.0)),
                state.get("student_request", ""),
                state.get("final_roadmap", ""),
                datetime.now().isoformat(),
            ),
        )

        connection.commit()

        return int(cursor.lastrowid)


def get_student_memory(student_id: str) -> List[Dict[str, Any]]:
    initialize_memory_db()

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                id,
                student_id,
                college_id,
                is_paid_user,
                revenue,
                student_request,
                final_roadmap,
                created_at
            FROM career_memory
            WHERE student_id = ?
            ORDER BY id DESC
            """,
            (student_id,),
        ).fetchall()

    return [dict(row) for row in rows]


def get_college_memory(college_id: str) -> List[Dict[str, Any]]:
    initialize_memory_db()

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                id,
                student_id,
                college_id,
                is_paid_user,
                revenue,
                student_request,
                final_roadmap,
                created_at
            FROM career_memory
            WHERE college_id = ?
            ORDER BY id DESC
            """,
            (college_id,),
        ).fetchall()

    return [dict(row) for row in rows]


def save_previous_query(
    student_id: str,
    query: str,
) -> int:
    initialize_memory_db()

    student_id = str(student_id or "").strip()
    query = str(query or "").strip()

    if not student_id or not query:
        return 0

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO previous_queries (
                student_id,
                query,
                created_at
            )
            VALUES (?, ?, ?)
            """,
            (
                student_id,
                query,
                datetime.now().isoformat(),
            ),
        )

        connection.commit()

        return int(cursor.lastrowid)


def get_previous_queries(
    student_id: str,
    limit: int = 20,
) -> List[Dict[str, Any]]:
    initialize_memory_db()

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                id,
                student_id,
                query,
                created_at
            FROM previous_queries
            WHERE student_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (
                str(student_id or "").strip(),
                int(limit),
            ),
        ).fetchall()

    return [dict(row) for row in rows]


def save_purchased_answer(
    student_id: str,
    college_id: str,
    query: str,
    answer: str,
    amount: float,
) -> int:
    initialize_memory_db()

    student_id = str(student_id or "").strip()
    query = str(query or "").strip()
    answer = str(answer or "").strip()
    amount = float(amount or 0.0)

    if not student_id or not query or not answer:
        return 0

    existing = find_purchased_answer(student_id, query)
    if existing:
        return int(existing.get('id', 0) or 0)

    purchased_at = datetime.now().isoformat()

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO purchased_answers (
                student_id,
                college_id,
                query,
                answer,
                amount,
                purchased_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                student_id,
                str(college_id or "").strip(),
                query,
                answer,
                amount,
                purchased_at,
            ),
        )

        connection.execute(
            """
            INSERT INTO student_profiles (
                student_id,
                career_preferences,
                purchased_count,
                total_spent,
                updated_at
            )
            VALUES (?, ?, 1, ?, ?)
            ON CONFLICT(student_id)
            DO UPDATE SET
                purchased_count = student_profiles.purchased_count + 1,
                total_spent = student_profiles.total_spent + excluded.total_spent,
                updated_at = excluded.updated_at
            """,
            (
                student_id,
                query,
                amount,
                purchased_at,
            ),
        )

        connection.commit()

        return int(cursor.lastrowid)


def get_purchased_answers(
    student_id: str,
) -> List[Dict[str, Any]]:
    initialize_memory_db()

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                id,
                student_id,
                college_id,
                query,
                answer,
                amount,
                purchased_at
            FROM purchased_answers
            WHERE student_id = ?
            ORDER BY id DESC
            """,
            (str(student_id or "").strip(),),
        ).fetchall()

    return [dict(row) for row in rows]


def find_purchased_answer(
    student_id: str,
    query: str,
) -> Dict[str, Any] | None:
    initialize_memory_db()

    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT
                id,
                student_id,
                college_id,
                query,
                answer,
                amount,
                purchased_at
            FROM purchased_answers
            WHERE student_id = ?
              AND query = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (
                str(student_id or "").strip(),
                str(query or "").strip(),
            ),
        ).fetchone()

    return dict(row) if row else None


def get_student_profile(
    student_id: str,
) -> Dict[str, Any]:
    initialize_memory_db()

    student_id = str(student_id or "").strip()

    if not student_id:
        return {
            "student_id": "",
            "career_preferences": "",
            "purchased_count": 0,
            "total_spent": 0.0,
        }

    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT
                student_id,
                career_preferences,
                purchased_count,
                total_spent,
                updated_at
            FROM student_profiles
            WHERE student_id = ?
            """,
            (student_id,),
        ).fetchone()

    if not row:
        return {
            "student_id": student_id,
            "career_preferences": "",
            "purchased_count": 0,
            "total_spent": 0.0,
        }

    return dict(row)


def load_long_term_memory(
    student_id: str,
) -> Dict[str, Any]:
    return {
        "previous_queries": get_previous_queries(student_id),
        "purchased_answers": get_purchased_answers(student_id),
        "student_profile": get_student_profile(student_id),
    }


initialize_memory_db()

