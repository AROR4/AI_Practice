from dotenv import load_dotenv

load_dotenv("../.env")

from graph import graph

print("=" * 60)
print("PRESIDIO RESEARCH AGENT")
print("=" * 60)

while True:

    query = input(
        "\nAsk Question (q to quit): "
    )

    if query.lower() == "q":
        break

    result = graph.invoke(
        {
            "query": query,
            "selected_tools": [],
            "mcp_result": "",
            "rag_result": "",
            "web_result": "",
            "aggregated_context": "",
            "response": ""
        }
    )

    print("\nANSWER\n")

    print(
        result["response"]
    )