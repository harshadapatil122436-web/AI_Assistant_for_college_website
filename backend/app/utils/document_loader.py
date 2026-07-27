import os
import PyPDF2
from typing import List, Dict
from pathlib import Path

class DocumentLoader:
    @staticmethod
    def load_pdf(file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error loading PDF {file_path}: {e}")
        return text
    
    @staticmethod
    def load_document(file_path: str) -> str:
        """Load document based on file extension"""
        ext = Path(file_path).suffix.lower()
        if ext == '.pdf':
            return DocumentLoader.load_pdf(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    
    @staticmethod
    def chunk_document(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Split document into overlapping chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk:
                chunks.append(chunk)
        
        return chunks