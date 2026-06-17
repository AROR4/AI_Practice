from langgraph.graph import (
    StateGraph,
    START,
    END
)

from state import AgentState

from agents.supervisor import classify_query

from tools.mcp_tool import mcp_tool
from tools.rag_tool import rag_tool
from tools.web_search_tool import web_search_tool

from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


# =====================================================
# LLM
# =====================================================

synthesizer_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


# =====================================================
# SUPERVISOR NODE
# =====================================================

def supervisor_node(state: AgentState):

    selected_tools = classify_query(
        state["query"]
    )

    print(
        f"\nSelected Tools: {selected_tools}\n"
    )

    return {
        "selected_tools": selected_tools
    }


# =====================================================
# MCP NODE
# =====================================================

def mcp_node(state: AgentState):

    if "MCP" not in state["selected_tools"]:
        return {}

    print(
        "\n========== MCP TOOL ==========\n"
    )

    result = mcp_tool.invoke(
        {
            "query": state["query"]
        }
    )

    return {
        "mcp_result": result
    }


# =====================================================
# RAG NODE
# =====================================================

def rag_node(state: AgentState):

    if "RAG" not in state["selected_tools"]:
        return {}

    print(
        "\n========== RAG TOOL ==========\n"
    )

    result = rag_tool.invoke(
        {
            "query": state["query"]
        }
    )

    return {
        "rag_result": result
    }


# =====================================================
# WEB NODE
# =====================================================

def web_node(state: AgentState):

    if "WEB" not in state["selected_tools"]:
        return {}

    print(
        "\n========== WEB TOOL ==========\n"
    )

    result = web_search_tool.invoke(
        {
            "query": state["query"]
        }
    )

    return {
        "web_result": result
    }


# =====================================================
# AGGREGATOR NODE
# =====================================================

def aggregator_node(state: AgentState):

    context_parts = []

    if state.get("mcp_result"):

        context_parts.append(
            f"""
MCP INFORMATION

{state['mcp_result']}
"""
        )

    if state.get("rag_result"):

        context_parts.append(
            f"""
RAG INFORMATION

{state['rag_result']}
"""
        )

    if state.get("web_result"):

        context_parts.append(
            f"""
WEB INFORMATION

{state['web_result']}
"""
        )

    aggregated_context = "\n\n".join(
        context_parts
    )

    return {
        "aggregated_context": aggregated_context
    }


# =====================================================
# SYNTHESIZER NODE
# =====================================================

def synthesizer_node(state: AgentState):

    prompt = f"""
You are Presidio's Enterprise Research Assistant.

User Question:
{state['query']}

Retrieved Context:

{state['aggregated_context']}

Instructions:

1. Answer using ONLY the provided context.
2. If multiple sources exist, combine them.
3. Remove duplicate information.
4. Produce a concise professional answer.
5. Use bullet points when appropriate.

Generate the final answer.
"""

    response = synthesizer_llm.invoke(
        prompt
    )

    return {
        "response": response.content
    }


# =====================================================
# GRAPH
# =====================================================

builder = StateGraph(
    AgentState
)

# Nodes

builder.add_node(
    "supervisor",
    supervisor_node
)

builder.add_node(
    "mcp",
    mcp_node
)

builder.add_node(
    "rag",
    rag_node
)

builder.add_node(
    "web",
    web_node
)

builder.add_node(
    "aggregator",
    aggregator_node
)

builder.add_node(
    "synthesizer",
    synthesizer_node
)

# Flow

builder.add_edge(
    START,
    "supervisor"
)

builder.add_edge(
    "supervisor",
    "mcp"
)

builder.add_edge(
    "mcp",
    "rag"
)

builder.add_edge(
    "rag",
    "web"
)

builder.add_edge(
    "web",
    "aggregator"
)

builder.add_edge(
    "aggregator",
    "synthesizer"
)

builder.add_edge(
    "synthesizer",
    END
)

# Compile

graph = builder.compile()