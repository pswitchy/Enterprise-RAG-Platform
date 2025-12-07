import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# LangChain / AI Imports
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

# Internal Imports
from app.database import get_analytics_data

load_dotenv()

app = FastAPI(title="Enterprise Knowledge & Analytics Platform")

# --- 1. Setup RAG Components (NiCE Skill) ---
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db_url = os.getenv("DATABASE_URL")

vector_store = PGVector(
    embeddings=embeddings,
    collection_name="enterprise_knowledge",
    connection=db_url,
)

# Initialize Groq (Llama 3)
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0.1 
)

# Prompt Engineering (Prevention of Hallucination)
prompt = ChatPromptTemplate.from_template("""
You are a Corporate AI Assistant. Answer the question based ONLY on the following context.
If the answer is not in the context, strictly state: "Data not available in knowledge base."

<context>
{context}
</context>

Question: {input}
""")

# Create Chain
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
document_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, document_chain)

# --- Models ---
class ChatRequest(BaseModel):
    query: str

# --- Endpoints ---

@app.get("/")
def home():
    return {"status": "System Online", "modules": ["RAG-AI", "Data-Analytics"]}

# Endpoint 1: The AI Chat (For NiCE)
@app.post("/chat")
async def chat_with_docs(request: ChatRequest):
    try:
        response = rag_chain.invoke({"input": request.query})
        return {
            "response": response["answer"],
            "retrieved_docs": [doc.metadata['source'] for doc in response['context']]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint 2: The Data Analytics (For Veeam)
@app.get("/analytics/dashboard")
async def get_dashboard_stats():
    """
    Returns aggregation metrics on the knowledge base.
    Proves SQL and structured data handling capabilities.
    """
    try:
        data = get_analytics_data()
        return {
            "dashboard_title": "Knowledge Base Metadata Analytics",
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)