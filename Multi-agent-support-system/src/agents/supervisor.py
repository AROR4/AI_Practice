from langchain_groq import ChatGroq
from logger_config import logger

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

def classify_query(query: str) -> str:

    prompt = f"""
You are a routing agent.

Classify the user query into ONLY one category.

IT
FINANCE

Query:
{query}

Return only:
IT
or
FINANCE
"""

    response = llm.invoke(prompt)

    result = response.content.strip().upper()

    route = "finance" if "FINANCE" in result else "it"

    logger.info(
        f"Routing query to {route.upper()} agent"
    )

    return route