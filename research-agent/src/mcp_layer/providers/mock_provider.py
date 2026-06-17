from mcp_layer.providers.base_provider import BaseMCPProvider


class MockProvider(BaseMCPProvider):

    def search(self, query: str) -> str:

        query = query.lower()

        if "document" in query or "paper" in query:

            return """
Required Documents

Health Insurance:
- Aadhaar Card
- PAN Card
- Medical Records

Vehicle Insurance:
- RC Book
- Driving License

Life Insurance:
- Aadhaar Card
- Income Proof
"""
        
        return """
Insurance Products

Health Insurance
Vehicle Insurance
Life Insurance
"""