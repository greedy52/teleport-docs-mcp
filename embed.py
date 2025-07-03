import os
import sys
from urllib.parse import quote

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Settings
MDX_DIR = "docs/pages_fixed"
PERSIST_DIR = "chroma_index"
BASE_URL = "https://goteleport.com/docs/"

# Step 1: Load .mdx files
print("📂 Loading MDX files...")
docs = []
for root, _, files in os.walk(MDX_DIR):
    for file in files:
        if file.endswith(".mdx"):
            path = os.path.join(root, file)
            loader = TextLoader(path)
            # Load the file
            loaded_docs = loader.load()

            # Relative to MDX_DIR
            rel_path = os.path.relpath(path, MDX_DIR)  # e.g. "enroll-resources/application-access/application-access.mdx"
            parts = rel_path.replace(".mdx", "").split(os.sep)  # e.g. ['enroll-resources', 'application-access', 'application-access']

            # Collapse final segment if it repeats
            if len(parts) >= 2 and parts[-1] == parts[-2]:
                parts = parts[:-1]  # remove the redundant one

            doc_url = BASE_URL + quote("/".join(parts)) + "/"

            for doc in loaded_docs:
                doc.metadata["source"] = doc_url

            docs.extend(loaded_docs)


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
