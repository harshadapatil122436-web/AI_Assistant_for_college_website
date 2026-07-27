"""
Document Ingestion Script
Run this to load your PDFs into Pinecone
"""

import os
import sys
import openai
import pinecone
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import Config
from app.utils.document_loader import DocumentLoader

def setup_pinecone():
    """Initialize Pinecone index"""
    pinecone.init(
        api_key=Config.PINECONE_API_KEY,
        environment=Config.PINECONE_ENVIRONMENT
    )
    
    # Check if index exists, create if not
    existing_indexes = pinecone.list_indexes()
    if Config.PINECONE_INDEX not in existing_indexes:
        pinecone.create_index(
            name=Config.PINECONE_INDEX,
            dimension=1536,  # Ada-002 embedding dimension
            metric='cosine'
        )
        print(f"✅ Created index: {Config.PINECONE_INDEX}")
    
    return pinecone.Index(Config.PINECONE_INDEX)

def ingest_documents():
    """Load PDFs, chunk, embed, and store in Pinecone"""
    
    # Setup
    openai.api_key = Config.OPENAI_API_KEY
    index = setup_pinecone()
    
    # Document directory
    docs_dir = Path(__file__).parent.parent / "data" / "documents"
    if not docs_dir.exists():
        print(f"❌ Documents directory not found: {docs_dir}")
        return
    
    # Process each PDF
    pdf_files = list(docs_dir.glob("*.pdf"))
    print(f"📄 Found {len(pdf_files)} PDF files")
    
    for pdf_file in pdf_files:
        print(f"\n📄 Processing: {pdf_file.name}")
        
        # Extract text
        text = DocumentLoader.load_pdf(str(pdf_file))
        if not text:
            print(f"  ❌ No text extracted from {pdf_file.name}")
            continue
        
        print(f"  📝 Extracted {len(text)} characters")
        
        # Chunk text
        chunks = DocumentLoader.chunk_document(
            text,
            chunk_size=Config.CHUNK_SIZE,
            overlap=Config.CHUNK_OVERLAP
        )
        print(f"  ✂️ Created {len(chunks)} chunks")
        
        # Generate embeddings and store
        batch_size = 50
        for i in range(0, len(chunks), batch_size):
            batch_chunks = chunks[i:i+batch_size]
            
            try:
                # Generate embeddings
                response = openai.Embedding.create(
                    input=batch_chunks,
                    model=Config.EMBEDDING_MODEL
                )
                
                # Prepare vectors for Pinecone
                vectors = []
                for j, chunk in enumerate(batch_chunks):
                    chunk_id = f"{pdf_file.stem}_{i+j}"
                    embedding = response['data'][j]['embedding']
                    
                    vectors.append((
                        chunk_id,
                        embedding,
                        {
                            "text": chunk,
                            "source": pdf_file.name,
                            "page": f"Chunk {i+j+1}"
                        }
                    ))
                
                # Upsert to Pinecone
                index.upsert(vectors=vectors)
                print(f"  ✅ Stored chunks {i+1}-{min(i+batch_size, len(chunks))}")
                
            except Exception as e:
                print(f"  ❌ Error processing batch: {e}")
    
    print("\n✅ Document ingestion complete!")

if __name__ == "__main__":
    ingest_documents()