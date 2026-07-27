import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_ORG_ID = os.getenv("OPENAI_ORG_ID")
    
    # Pinecone
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
    PINECONE_INDEX = os.getenv("PINECONE_INDEX")
    
    # Models
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4")
    
    # Chunking
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))
    TOP_K_RETRIEVAL = int(os.getenv("TOP_K_RETRIEVAL", 5))
    
    # API
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))