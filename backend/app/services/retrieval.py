import openai
import pinecone
from typing import List, Dict
from app.config import Config

# Initialize Pinecone
pinecone.init(
    api_key=Config.PINECONE_API_KEY,
    environment=Config.PINECONE_ENVIRONMENT
)
index = pinecone.Index(Config.PINECONE_INDEX)

def retrieve_documents(query: str, top_k: int = 5) -> List[Dict]:
    """Retrieve relevant documents based on query"""
    try:
        # Generate query embedding
        response = openai.Embedding.create(
            input=[query],
            model=Config.EMBEDDING_MODEL
        )
        query_embedding = response['data'][0]['embedding']
        
        # Query Pinecone
        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        
        documents = []
        for match in results['matches']:
            documents.append({
                "text": match['metadata'].get('text', ''),
                "source": match['metadata'].get('source', 'Unknown'),
                "page": match['metadata'].get('page', 'N/A'),
                "score": match['score']
            })
        
        return documents
    except Exception as e:
        print(f"Retrieval error: {e}")
        return []