import os
from dataclasses import dataclass

@dataclass
class Config:
    
    # Model Configuration
    OPENROUTER_MODEL: str = "openai/gpt-oss-20b:free"
    LLAMA3_MODEL: str = "llama-3.3-70b-versatile"
    
    # RAG Configuration
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 100
    TOP_K_RETRIEVAL: int = 6
    RERANK_TOP_K: int = 3
    
    # Embedding Model
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    RERANKER_MODEL: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    
    # ChromaDB
    CHROMA_PATH: str = "./chroma_db"
    COLLECTION_NAME: str = "qa_bot_chunks"

# Create config instance
config = Config()

# Load from environment variables or streamlit secrets
def load_secrets():
    """Load API keys from environment or streamlit secrets"""
    try:
        import streamlit as st
        config.OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY", os.getenv("OPENROUTER_API_KEY", ""))
        config.GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
    except:
        config.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
        config.GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Load secrets on import
load_secrets()
