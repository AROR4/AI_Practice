from mcp_layer.providers.google_docs_provider import (
    GoogleDocsProvider
)


class MCPClient:

    def __init__(self):

        self.provider = GoogleDocsProvider()


    def search(
        self,
        query: str
    ) -> str:

        return self.provider.search(
            query
        )