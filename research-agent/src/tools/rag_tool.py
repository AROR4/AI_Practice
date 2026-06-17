from langchain_core.tools import tool

from services.vector_service import VectorService

vector_service = VectorService()


@tool
def rag_tool(query: str) -> str:
    """
    Search company policies and internal knowledge base.
    """
    print("\n******** RAG TOOL CALLED ********\n")

    documents = vector_service.search_documents(
        query=query,
        k=3
    )

    return "\n\n".join(
        [doc.page_content for doc in documents]
    )