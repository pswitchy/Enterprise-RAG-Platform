# Enterprise Knowledge Graph & RAG Analytics Platform

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-High%20Performance-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-blue)
![AI](https://img.shields.io/badge/GenAI-Llama%203.3-orange)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)

A production-grade **Hybrid Intelligence Platform** that combines **Generative AI (RAG)** with **Structured Data Analytics**. 

This system ingests unstructured enterprise documentation (PDFs), processes them through an **ETL pipeline** to extract both semantic embeddings and structured metadata, and serves insights via a high-performance **FastAPI** backend.

---

## 🚀 Key Technical Highlights
This project was engineered to bridge the gap between **GenAI Ops** and **Data Engineering**.

### For AI Engineering (GenAI / LLM Ops)
*   **RAG Architecture:** Implements Retrieval-Augmented Generation to ground LLM responses in private data, eliminating hallucinations.
*   **Vector Database:** Utilizes **PostgreSQL with `pgvector`** for high-dimensional semantic search.
*   **Prompt Engineering:** Uses Context-Aware prompting with Llama 3.3 (via Groq) for precise enterprise Q&A.
*   **Embeddings:** Runs local inference using `all-MiniLM-L6-v2` (HuggingFace) for cost-efficient vectorization.

### For Data Engineering (ETL & Analytics)
*   **Automated ETL Pipeline:** A Python-based ingestion script that cleans, chunks, and enriches raw PDFs with metadata.
*   **Hybrid Storage Schema:** Stores vectors alongside structured columns (Category, Word Count, Source), enabling complex SQL queries on unstructured data.
*   **Analytics Endpoint:** tailored SQL aggregations to visualize knowledge base distribution (simulating OLAP workflows).

---

## 🛠 Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Backend API** | FastAPI (Python) | High-concurrency Async REST API |
| **LLM Inference** | Groq API (Llama 3.3) | Ultra-low latency text generation |
| **Orchestration** | LangChain | Chain management and retrieval logic |
| **Database** | PostgreSQL + pgvector | Hybrid Vector & Relational Storage |
| **Embeddings** | HuggingFace | Local embedding generation |
| **Infrastructure** | Docker / Docker Compose | Containerization and Dependency Management |

---

## 🏗 Architecture Flow

```mermaid
graph TD
    A[Raw PDF Documents] -->|ETL Script| B(Text Chunking & Cleaning)
    B -->|Feature Extraction| C{Data Processing}
    C -->|Semantic Embeddings| D[Postgres pgvector]
    C -->|Metadata Extraction| E[Postgres SQL Columns]
    
    User -->|Query| F[FastAPI Backend]
    F -->|Vector Search| D
    F -->|SQL Aggregation| E
    F -->|Context + Prompt| G[Llama 3.3 LLM]
    G -->|Answer| User
```

---

## ⚡️ Setup & Installation

### Prerequisites
*   Python 3.10+
*   Docker & Docker Compose (Recommended) OR Local PostgreSQL 14+ with `pgvector` installed.
*   Groq API Key (Free tier available).

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/enterprise-rag-platform.git
cd enterprise-rag-platform
```

### 2. Environment Configuration
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=gsk_your_actual_key_here
POSTGRES_USER=admin
POSTGRES_PASSWORD=password123
POSTGRES_DB=rag_db
DATABASE_URL=postgresql+psycopg2://admin:password123@localhost:5432/rag_db
```

### 3. Start Infrastructure (Docker)
If using Docker (easiest method):
```bash
docker-compose up -d
```
*This starts a PostgreSQL container with the Vector extension pre-loaded.*

### 4. Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🏃‍♂️ Running the Pipeline

### Step 1: Ingest Data (ETL)
Place your PDF documents (e.g., HR Policies, Technical Manuals) in the `data/` folder. Then run the ingestion pipeline:

```bash
python3 -m app.ingest
```
*Output:*
> ✅ Processed 1240 chunks.
> ✅ Metadata extracted (Category: HR_Policy).
> ✅ Embeddings stored in pgvector.

### Step 2: Start the API Server
```bash
python3 -m app.main
```
The server will start at `http://0.0.0.0:8000`.

---

## 🔌 API Usage Examples

### 1. GenAI Chat (RAG)
**Endpoint:** `POST /chat`
**Description:** Asks the LLM a question based *only* on the uploaded documents.

<img width="728" height="674" alt="Screenshot 2025-12-08 at 2 57 25 AM" src="https://github.com/user-attachments/assets/c67c7c2d-cdd6-4803-ae70-774dfbecea59" />


### 2. Knowledge Analytics (Data Eng)
**Endpoint:** `GET /analytics/dashboard`
**Description:** Returns SQL aggregations on document metadata.

<img width="693" height="710" alt="Screenshot 2025-12-08 at 3 02 40 AM" src="https://github.com/user-attachments/assets/b2a66b26-c2a8-49ed-ad62-628906ce07f8" />

---

## 🔮 Future Improvements
*   **Infrastructure:** Deploy to Azure App Service with CI/CD via GitHub Actions.
*   **Data Engineering:** Migrate ETL pipeline to Apache Airflow for scheduled ingestion.
*   **UI:** Build a Streamlit or React frontend for interactive visualization.
