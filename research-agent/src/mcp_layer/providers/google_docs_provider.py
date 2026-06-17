from mcp_layer.providers.base_provider import (
    BaseMCPProvider
)


class GoogleDocsProvider(
    BaseMCPProvider
):

    def search(
        self,
        query: str
    ) -> str:

        raise NotImplementedError(
            "Google Docs MCP integration not implemented yet."
        )