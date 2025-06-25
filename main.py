import os
import sys

from mcp.server.fastmcp import FastMCP
from tqdm import tqdm
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_ollama.llms import OllamaLLM
from langchain_ollama import OllamaEmbeddings


### embeddings
print("🛠️ Preparing to embed and store documents...", file=sys.stderr)

embedding_model = OllamaEmbeddings(
    model="mxbai-embed-large",base_url="http://127.0.0.1:11434"
)
model = OllamaLLM(model="qwen3",base_url="http://127.0.0.1:11434")

all_docs = []
for root, _, files in os.walk("./docs/pages/enroll-resources/auto-discovery"):
    for file in files:
        if file.endswith(".mdx"):
            path = os.path.join(root, file)
            loader = TextLoader(path)
            all_docs.extend(loader.load())

print(f"✅ Loaded {len(all_docs)} documents from .mdx files.", file=sys.stderr)

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(all_docs)

print(f"🧩 Split into {len(texts)} chunks.", file=sys.stderr)

docsearch = Chroma(embedding_function=embedding_model)
for doc in tqdm(texts, desc="📦 Adding to Chroma"):
    docsearch.add_documents([doc])

qa=RetrievalQA.from_chain_type(llm=model,retriever=docsearch.as_retriever())

print("🔁 All documents embedded and stored in Chroma.", file=sys.stderr)
print("🛰️ Starting MCP server.", file=sys.stderr)

### MCP
mcp = FastMCP("teleport-docs")

@mcp.tool()
def search_teleport_docs(prompt: str) -> str:
    """
    Search Teleport documentation based on a user prompt.

    What this tool does:
        - Takes a natural language query (prompt)
        - Runs it through a RAG pipeline over embeddings generated from Teleport official documentations.
        - Returns a textual answer based on relevant docs

    Arguments:
        prompt (str): A natural language question or request, 
                      such as "How does access control work in Teleport?"

    Returns:
        str: A generated answer based on the most relevant parts of the documentation.
    """
    return qa.run(prompt)

if __name__ == "__main__":
    mcp.run()
