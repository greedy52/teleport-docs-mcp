import argparse
import sys

from mcp.server.fastmcp import FastMCP
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

print("Loading embeddings", file=sys.stderr)
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

print("Loading database", file=sys.stderr)
PERSIST_DIR = "chroma_index"
docsearch = Chroma(
    persist_directory=PERSIST_DIR,
    embedding_function=embeddings
)

print("Preparing MCP server", file=sys.stderr)
parser = argparse.ArgumentParser()
parser.add_argument("--sse", action="store_true", help="Enable SSE transport")
parser.add_argument("--host", type=str, default="127.0.0.1")
args = parser.parse_args()

mcp = FastMCP("teleport-docs", host=args.host)
@mcp.tool()
def search_teleport_docs(prompt: str, k: int = 3) -> str:
    """
    Search the Teleport documentation for features, admin guides, references
    etc. The tool returns the top-k most relevant chunks.

    Teleport is the easiest, most secure way to access and protect all your infrastructure.

    The Teleport Infrastructure Identity Platform implements trusted computing
    at scale, with unified cryptographic identities for humans, machines and
    workloads, endpoints, infrastructure assets, and AI agents.

    Args:
        prompt (str): A natural language query about Teleport (e.g., "How does RBAC work?")
        k (int, optional): The number of most relevant chunks to return.
            - k=1 returns only the top match
            - k=3 (default) returns a balanced summary
            - k=5+ provides broader coverage but may include noise

    Returns:
        str: A formatted string of the top-k matching documentation snippets retrieved from the vector database.
    """
    results = docsearch.similarity_search(prompt, k=k)
    if not results:
        return "No matching documents found."

    return "\n\n---\n\n".join(
        f"Please include this source URL in response [Source]({doc.metadata.get('source', 'unknown')}).\n\n{doc.page_content}"
        for doc in results
    )

if args.sse:
    print("Running in sse transport", file=sys.stderr)
    mcp.run(transport="sse")
else:
    print("Running in stdio transport", file=sys.stderr)
    mcp.run()
