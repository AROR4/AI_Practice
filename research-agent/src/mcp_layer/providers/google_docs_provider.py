import asyncio
import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp_layer.providers.base_provider import BaseMCPProvider


class GoogleDocsProvider(BaseMCPProvider):

    async def _async_search(self, query: str) -> str:
        # Resolve path to server.py in the workspace root
        server_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "../../../server.py"
            )
        )
        server_params = StdioServerParameters(
            command=sys.executable,
            args=[server_path],
            env=os.environ.copy()
        )

        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()

                # 1. List all Google Docs
                list_result = await session.call_tool(
                    "list_google_docs",
                    arguments={"query": ""}
                )
                docs_text = (
                    list_result.content[0].text
                    if list_result.content else ""
                )

                if "No Google Docs found" in docs_text or "Error" in docs_text:
                    return docs_text

                # 2. Parse doc names and IDs
                lines = docs_text.split('\n')
                doc_ids = []
                current_name = ""
                for line in lines:
                    if line.strip().startswith("- Name:"):
                        current_name = line.split("- Name:")[1].strip()
                    elif line.strip().startswith("ID:"):
                        doc_id = line.split("ID:")[1].strip()
                        doc_ids.append((current_name, doc_id))

                if not doc_ids:
                    return (
                        f"Found docs, but failed to parse IDs from:\n{docs_text}"
                    )

                
                # 3. Read each document instead of keyword searching
                results = []

                for name, doc_id in doc_ids:
                    doc_result = await session.call_tool(
                        "read_google_doc",
                        arguments={
                            "document_id": doc_id
                        }
                    )

                    content = (
                        doc_result.content[0].text
                        if doc_result.content else ""
                    )

                    if content and not content.startswith("Error"):
                        results.append(
                            f"""
                Document: {name}
                Document ID: {doc_id}

                {content}
                """
                        )

                if not results:
                    return "Unable to read any Google Docs."

                return "\n\n".join(results)

    def search(self, query: str) -> str:
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if loop.is_running():
            from concurrent.futures import ThreadPoolExecutor
            with ThreadPoolExecutor() as executor:
                return executor.submit(
                    lambda: asyncio.run(self._async_search(query))
                ).result()
        else:
            return loop.run_until_complete(
                self._async_search(query)
            )