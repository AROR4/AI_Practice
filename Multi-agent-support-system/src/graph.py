from langgraph.graph import StateGraph, START, END

from state import AgentState

from agents.supervisor import classify_query
from agents.it_agent import handle_it_query
from agents.finance_agent import handle_finance_query

from logger_config import logger



def supervisor_node(state: AgentState):

    logger.info("Supervisor node started")

    route = classify_query(
        state["query"]
    )

    return {
        "route": route
    }




def it_node(state: AgentState):

    logger.info(
        "Executing IT Agent node"
    )

    response = handle_it_query(
        state["query"]
    )

    return {
        "response": response
    }



def finance_node(state: AgentState):

    logger.info(
        "Executing Finance Agent node"
    )

    response = handle_finance_query(
        state["query"]
    )

    return {
        "response": response
    }



def route_decision(state: AgentState):

    return state["route"]




builder = StateGraph(AgentState)

builder.add_node(
    "supervisor",
    supervisor_node
)

builder.add_node(
    "it_agent",
    it_node
)

builder.add_node(
    "finance_agent",
    finance_node
)

builder.add_edge(
    START,
    "supervisor"
)

# Conditional Routing
builder.add_conditional_edges(
    "supervisor",
    route_decision,
    {
        "it": "it_agent",
        "finance": "finance_agent"
    }
)

builder.add_edge(
    "it_agent",
    END
)

builder.add_edge(
    "finance_agent",
    END
)

graph = builder.compile()