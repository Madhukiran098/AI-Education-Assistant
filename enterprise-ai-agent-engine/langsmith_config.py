import os

LANGSMITH_ENABLED = bool(
    os.getenv("LANGSMITH_TRACING")
    and os.getenv("LANGSMITH_API_KEY")
)

LANGSMITH_PROJECT = os.getenv(
    "LANGSMITH_PROJECT",
    "AI-Education-Career-M3",
)


def get_langsmith_status():
    return {
        "enabled": LANGSMITH_ENABLED,
        "project": LANGSMITH_PROJECT,
        "api_key_configured": bool(os.getenv("LANGSMITH_API_KEY")),
    }
