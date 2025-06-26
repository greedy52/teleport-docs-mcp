from mcp.server.fastmcp import FastMCP
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

PERSIST_DIR = "chroma_index"
embeddings = OllamaEmbeddings(model="mxbai-embed-large")
docsearch = Chroma(
    persist_directory=PERSIST_DIR,
    embedding_function=embeddings
)
mcp = FastMCP("teleport-docs")


@mcp.tool()
def search_teleport_docs(prompt: str, k: int = 3) -> str:
    """
    Search the Teleport documentation and return the top-k most relevant chunks.

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
        f"{doc.metadata.get('source', 'unknown')}\n{doc.page_content}"
        for doc in results
    )

if __name__ == "__main__":
    mcp.run()
