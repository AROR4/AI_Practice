from langchain_core.tools import tool
from langchain_community.tools.tavily_search import (
    TavilySearchResults
)

from config import TAVILY_API_KEY

search = TavilySearchResults(
    max_results=3,
    tavily_api_key=TAVILY_API_KEY
)


@tool
def web_search_tool(query: str) -> str:
    """
    Search the internet for latest information.
    """
    print("\n******** WEB SEARCH TOOL CALLED ********\n")
    
    results = search.invoke(query)

    return str(results)