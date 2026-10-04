from pathlib import Path
from typing import Any, Dict, List

try:
    from langchain_chroma import Chroma
except Exception:
    Chroma = None
from langchain_core.documents import Document

CHROMA_DIR = Path("data/chroma_career_memory")
COLLECTION_NAME = "career_roadmaps"


def get_vector_store():
    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=str(CHROMA_DIR),
    )


def save_roadmap_to_memory(state: Dict[str, Any]) -> str:
    student_id = state.get("student_id", "").strip()
    college_id = state.get("college_id", "").strip()
    request = state.get("student_request", "").strip()
    roadmap = state.get("final_roadmap", "").strip()

    if not student_id or not roadmap:
        return ""

    document = Document(
        page_content=(
            f"Student request: {request}\n"
            f"Career roadmap: {roadmap}"
        ),
        metadata={
            "student_id": student_id,
            "college_id": college_id,
            "is_paid_user": bool(
                state.get("is_paid_user", False)
            ),
            "revenue": float(
                state.get("revenue", 0.0)
            ),
        },
    )

    vector_store = get_vector_store()

    record_id = (
        f"{student_id}_{college_id}_"
        f"{abs(hash(request))}"
    )

    vector_store.add_documents(
        documents=[document],
        ids=[record_id],
    )

    return record_id


def search_previous_roadmaps(
    query: str,
    college_id: str = "",
    k: int = 3,
) -> List[Dict[str, Any]]:

    query = query.strip()

    if not query:
        return []

    vector_store = get_vector_store()

    if college_id:
        results = vector_store.similarity_search(
            query,
            k=k,
            filter={
                "college_id": college_id,
            },
        )
    else:
        results = vector_store.similarity_search(
            query,
            k=k,
        )

    return [
        {
            "content": document.page_content,
            "metadata": document.metadata,
        }
        for document in results
    ]
