from typing import TypedDict


class AgentState(TypedDict):
    query: str

    selected_tools: list[str]

    mcp_result: str
    rag_result: str
    web_result: str

    aggregated_context: str

    response: str