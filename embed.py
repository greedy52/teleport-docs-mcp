import os

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Settings
MDX_DIR = "docs/pages_fixed"
PERSIST_DIR = "chroma_index"

# Step 1: Load .mdx files
print("📂 Loading MDX files...")
docs = []
for root, _, files in os.walk(MDX_DIR):
    for file in files:
        if file.endswith(".mdx"):
            path = os.path.join(root, file)
            loader = TextLoader(path)
            docs.extend(loader.load())

print(f"✅ Loaded {len(docs)} raw documents")

# Step 2: Chunk them
print("✂️  Splitting into chunks...")
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = splitter.split_documents(docs)
print(f"🧩 Created {len(chunks)} chunks")

# Embedding setup
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

# Now store them
print("💾 Embedding and storing in persistent Chroma DB. It takes forever and burns your laptop, so be patient.")
docsearch = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="chroma_index"
)
print("✅ Done.")
