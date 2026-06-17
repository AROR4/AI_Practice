from langchain_core.tools import tool

from mcp_layer.client import (
    MCPClient
)

client = MCPClient()


@tool
def mcp_tool(
    query: str
) -> str:
    """
    Search enterprise knowledge sources.
    """

    print(
        "\n******** MCP TOOL CALLED ********\n"
    )

    return client.search(
        query
    )