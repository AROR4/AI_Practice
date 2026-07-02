import os
import sys
from mcp.server.fastmcp import FastMCP
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Initialize FastMCP server
mcp = FastMCP("Google Docs Server")

SCOPES = [
    'https://www.googleapis.com/auth/documents.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]

def get_credentials():
    path = os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE", "./service_account.json")
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Service account key file not found at '{path}'. "
            "Please place your 'service_account.json' file in the root folder or "
            "set the GOOGLE_SERVICE_ACCOUNT_FILE environment variable."
        )
    return service_account.Credentials.from_service_account_file(path, scopes=SCOPES)

def get_drive_service():
    creds = get_credentials()
    return build('drive', 'v3', credentials=creds)

def get_docs_service():
    creds = get_credentials()
    return build('docs', 'v1', credentials=creds)

def read_structural_elements(elements):
    """Recursively extracts text content from Google Doc elements."""
    text = ""
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                if 'textRun' in elem:
                    text += elem.get('textRun').get('content')
        elif 'table' in value:
            table = value.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += read_structural_elements(cell.get('content'))
        elif 'tableOfContents' in value:
            toc = value.get('tableOfContents')
            text += read_structural_elements(toc.get('content'))
    return text

@mcp.tool()
def list_google_docs(query: str = None, max_results: int = 10) -> str:
    """
    List Google Docs shared with this service account.
    Optional query can filter results by name/keyword.
    """
    try:
        service = get_drive_service()
        q = "mimeType = 'application/vnd.google-apps.document'"
        if query:
            safe_query = query.replace("'", "\\'")
            q += f" and name contains '{safe_query}'"
        
        results = service.files().list(
            q=q,
            pageSize=max_results,
            fields="files(id, name)"
        ).execute()
        
        files = results.get('files', [])
        if not files:
            return "No Google Docs found."
        
        out = []
        for f in files:
            out.append(f"- Name: {f['name']}\n  ID: {f['id']}")
        return "\n".join(out)
    except Exception as e:
        return f"Error listing Google Docs: {str(e)}"

@mcp.tool()
def read_google_doc(document_id: str) -> str:
    """
    Read the full plain-text content of a Google Doc using its document_id.
    """
    try:
        service = get_docs_service()
        doc = service.documents().get(documentId=document_id).execute()
        body = doc.get('body')
        if not body:
            return "Empty document."
        
        text = read_structural_elements(body.get('content', []))
        return text
    except Exception as e:
        return f"Error reading Google Doc: {str(e)}"

@mcp.tool()
def search_within_doc(document_id: str, term: str) -> str:
    """
    Search for a term within a Google Doc. Returns matching snippets with context.
    """
    try:
        text = read_google_doc(document_id)
        if text.startswith("Error reading Google Doc:"):
            return text
        
        term_lower = term.lower()
        lines = text.split('\n')
        matches = []
        for idx, line in enumerate(lines):
            if term_lower in line.lower():
                start = max(0, idx - 1)
                end = min(len(lines), idx + 2)
                snippet = "\n".join(lines[start:end])
                matches.append(f"Match at line {idx + 1}:\n{snippet}\n---")
        
        if not matches:
            return f"No matches found for '{term}' in document."
        
        return "\n".join(matches)
    except Exception as e:
        return f"Error searching within Google Doc: {str(e)}"

if __name__ == "__main__":
    # Check if SSE options are passed
    if "--transport" in sys.argv and "sse" in sys.argv:
        # Custom execution for SSE
        port = 8765
        if "--port" in sys.argv:
            try:
                port_idx = sys.argv.index("--port")
                port = int(sys.argv[port_idx + 1])
            except (ValueError, IndexError):
                pass
        mcp.settings.port = port
        mcp.run(transport="sse")
    else:
        # Default run (stdio)
        mcp.run()

