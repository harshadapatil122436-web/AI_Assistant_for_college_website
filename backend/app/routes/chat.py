from fastapi import APIRouter, HTTPException
from app.model import ChatRequest, ChatResponse
from app.services.retrieval import retrieve_documents
from app.services.generation import generate_response
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["chat"])

@router.post("/ask", response_model=ChatResponse)
async def ask_question(request: ChatRequest):
    """Process user question and return AI response with sources"""
    try:
        logger.info(f"Query received: {request.query[:50]}...")
        
        # Retrieve relevant documents
        documents = retrieve_documents(request.query, top_k=request.top_k)
        logger.info(f"Retrieved {len(documents)} documents")
        
        # Generate response
        answer, sources = generate_response(request.query, documents)
        
        return ChatResponse(
            answer=answer,
            sources=sources if request.include_sources else None
        )
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return ChatResponse(
            answer="Sorry, I encountered an error processing your question.",
            error=str(e)
        )

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "RAG Assistant"}