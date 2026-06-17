from langchain_groq import ChatGroq
from tools.file_tool import read_file
from tools.search_tool import web_search
from logger_config import logger

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


def handle_it_query(query: str):

    logger.info(
        f"IT Agent processing query: {query}"
    )

    docs = read_file("data/it_docs.txt")

    search_results = web_search.invoke(query)

    prompt = f"""
You are an IT Support Agent.

Use the internal documentation first.

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