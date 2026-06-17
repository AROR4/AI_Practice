from langchain_groq import ChatGroq
from tools.file_tool import read_file
from tools.search_tool import web_search
from logger_config import logger



llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


def handle_finance_query(query: str):

    logger.info(
        f"Finance Agent processing query: {query}"
    )

    docs = read_file("data/finance_docs.txt")

    search_results = web_search.invoke(query)

    prompt = f"""
You are a Finance Support Agent.

Use internal documentation first.

Internal Documentation:
{docs}

Web Results:
{search_results}

Question:
{query}

Provide a professional answer.
"""

    response = llm.invoke(prompt)

    return response.content