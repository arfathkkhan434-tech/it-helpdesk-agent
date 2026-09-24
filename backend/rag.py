import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

load_dotenv()

CHROMA_DIR = "./chroma_db"
POLICY_FILE = "data/it_policies.txt"

def get_embeddings():
    # Local high-speed embedding model (no API call, no 404 errors)
    return FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")

def initialize_rag():
    if not os.path.exists(POLICY_FILE):
        raise FileNotFoundError(f"{POLICY_FILE} missing.")

    # Reset existing chroma db directory to avoid schema conflicts
    loader = TextLoader(POLICY_FILE)
    documents = loader.load()
    splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    docs = splitter.split_documents(documents)

    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=get_embeddings(),
        persist_directory=CHROMA_DIR
    )
    return vectorstore

def query_knowledge_base(query: str) -> str:
    vectorstore = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=get_embeddings()
    )
    results = vectorstore.similarity_search(query, k=2)
    return "\n".join([doc.page_content for doc in results])