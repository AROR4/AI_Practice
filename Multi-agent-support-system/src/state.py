from typing import TypedDict


class AgentState(TypedDict):
    query: str
    route: str
    response: str