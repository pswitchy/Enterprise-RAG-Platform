import os
import random
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector

load_dotenv()

# Configuration
DATA_FOLDER = "data"
DB_CONNECTION = os.getenv("DATABASE_URL")

def determine_category(text_content):
    """Simulate intelligent classification for Metadata tags"""
    text_lower = text_content.lower()
    if "salary" in text_lower or "leave" in text_lower or "benefits" in text_lower:
        return "HR_Policy"
    elif "api" in text_lower or "python" in text_lower or "deploy" in text_lower:
        return "Technical_Docs"
    else:
        return "General_Info"

def run_pipeline():
    print("--- Starting ETL Pipeline ---")
    
    # 1. Load Documents
    pdf_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith('.pdf')]
    if not pdf_files:
        print("No PDFs found in /data folder.")
        return

    all_docs = []
    for pdf in pdf_files:
        path = os.path.join(DATA_FOLDER, pdf)
        print(f"Processing: {pdf}...")
        loader = PyPDFLoader(path)
        docs = loader.load()
        all_docs.extend(docs)

    # 2. Split Text (Chunking)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(all_docs)
    print(f"Generated {len(splits)} chunks.")

    # 3. Metadata Enrichment (Critical for Veeam/Data Engineering)
    # We inject structured data into the unstructured chunks
    for split in splits:
        category = determine_category(split.page_content)
        word_count = len(split.page_content.split())
        
        # Add to metadata dict
        split.metadata["category"] = category
        split.metadata["word_count"] = word_count
        split.metadata["source"] = split.metadata.get("source", "unknown")

    # 4. Embed & Store (Critical for NiCE/AI)
    print("Generating Embeddings & Storing in pgvector...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # This automatically creates the tables in Postgres if they don't exist
    PGVector.from_documents(
        embedding=embeddings,
        documents=splits,
        collection_name="enterprise_knowledge",
        connection=DB_CONNECTION,
    )
    
    print("--- ETL Pipeline Complete: Data Indexed successfully ---")

if __name__ == "__main__":
    run_pipeline()