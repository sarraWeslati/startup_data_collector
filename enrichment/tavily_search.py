import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)
def search_entity_sources(entity):

    name = (
        entity.get("startup_name")
        or entity.get("investor_name")
        or ""
    )

    if not name:
        return []

    entity_type = entity.get(
        "entity_type",
        ""
    )

    if entity_type == "startup":

        query = (
            f'"{name}" startup company '
            f'linkedin github funding founders'
        )

    else:

        query = (
            f'"{name}" investor venture capital '
            f'portfolio investments linkedin'
        )

    result = client.search(
        query=query,
        max_results=5
    )

    return result.get(
        "results",
        []
    )