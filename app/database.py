import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Standard SQLAlchemy engine for running raw SQL analytics
engine = create_engine(DATABASE_URL)

def get_analytics_data():
    """
    Simulates a Data Engineering query.
    Extracts metadata from the JSONB column utilized by LangChain.
    """
    # LangChain stores metadata in a JSONB column named 'cmetadata' inside 'langchain_pg_embedding'
    query = text("""
        SELECT 
            cmetadata ->> 'category' as category, 
            COUNT(*) as chunk_count,
            AVG(CAST(cmetadata ->> 'word_count' AS INTEGER)) as avg_word_count
        FROM langchain_pg_embedding 
        GROUP BY cmetadata ->> 'category';
    """)
    
    with engine.connect() as conn:
        result = conn.execute(query)
        return [dict(row._mapping) for row in result]