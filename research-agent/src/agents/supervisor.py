from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


def classify_query(query: str):

    prompt = f"""
You are a routing agent.

Available tools:

MCP
- insurance products
- company information
- compliance documents

RAG
- HR policies
- leave policy
- AI policy
- employee handbook

WEB
- latest news
- regulations
- market trends

A query may require MULTIPLE tools.

Examples:

What insurance products are offered?
["MCP"]

What is the leave policy?
["RAG"]

Latest AI regulations?
["WEB"]

What is Presidio's AI policy and how does it compare to AI regulations in India?
["RAG","WEB"]

What insurance products do we offer and what are current market trends?
["MCP","WEB"]

Return ONLY a Python list.
No explanation.

Query:
{query}
"""

    result = llm.invoke(prompt)

    return eval(result.content.strip())