from langchain_groq import ChatGroq

from langgraph.prebuilt import create_react_agent

from tools.rag_tool import rag_tool
from tools.web_search_tool import web_search_tool
from tools.mcp_tool import mcp_tool


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

tools = [
    rag_tool,
    web_search_tool,
    mcp_tool
]

agent = create_react_agent(
    model=llm,
    tools=tools
)