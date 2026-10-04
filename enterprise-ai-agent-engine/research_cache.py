from functools import lru_cache

from agents.research_agent import ResearchAgent


@lru_cache(maxsize=128)
def cached_research(user_request: str):
    request = user_request.strip()

    if not request:
        return {
            "topic": "",
            "information": "Research request is required.",
        }

    agent = ResearchAgent()
    return agent.research(request)


def clear_research_cache():
    cached_research.cache_clear()


def get_research_cache_info():
    return cached_research.cache_info()
