import openai
from typing import List, Dict, Tuple
from app.config import Config

def generate_response(query: str, documents: List[Dict]) -> Tuple[str, List[Dict]]:
    """Generate response using LLM with context"""
    
    if not documents:
        return "I couldn't find relevant information in the documents. Please contact the college directly.", []
    
    # Build context
    context_parts = []
    sources = []
    
    for i, doc in enumerate(documents, 1):
        context_parts.append(f"[Source {i}] {doc['text']}")
        sources.append({
            "source": doc['source'],
            "page": doc['page'],
            "relevance": round(doc['score'] * 100, 2)
        })
    
    context = "\n\n".join(context_parts)
    
    # Build prompt
    system_prompt = """You are a helpful college admission assistant for Vidya Polytechnic.
    Answer questions based ONLY on the provided context.
    If the answer cannot be found in the context, say so politely.
    Always cite your sources using [Source X] notation.
    Be concise, accurate, and helpful."""
    
    user_prompt = f"""Context:
{context}

Question: {query}

Answer based on the context above. Use [Source X] to cite sources."""
    try:
        response = client.chat.completions.create(
            model=Config.LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        answer = response.choices[0].message.content
        return answer, sources
    except Exception as e:
        print(f"Generation error: {e}")
        return "I'm having trouble generating a response. Please try again later.", []
    
