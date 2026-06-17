from dotenv import load_dotenv

load_dotenv("../.env")

from graph import graph


def print_banner():
    print("\n" + "=" * 60)
    print("MULTI AGENT SUPPORT SYSTEM")
    print("=" * 60)
    print("Available Domains:")
    print("1. IT Support")
    print("2. Finance Support")
    print("=" * 60)


def main():

    print_banner()

    while True:

        query = input(
            "\nAsk a question (q to quit): "
        ).strip()

        if query.lower() == "q":
            print("\nExiting system...")
            break

        print("\nProcessing query...\n")

        try:

            result = graph.invoke(
                {
                    "query": query,
                    "route": "",
                    "response": ""
                }
            )

            print("\nResponse:")
            print("-" * 60)
            print(result["response"])
            print("-" * 60)

        except Exception as e:

            print(f"\nError: {e}")


if __name__ == "__main__":
    main()