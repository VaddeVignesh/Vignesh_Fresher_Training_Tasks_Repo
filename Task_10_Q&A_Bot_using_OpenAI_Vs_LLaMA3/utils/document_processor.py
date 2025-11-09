import re
from typing import List
from langchain_core.documents import Document

def simple_split(documents: List[Document], chunk_size: int = 800) -> List[Document]:
    """Split documents into chunks"""
    chunks = []
    for doc in documents:
        text = doc.page_content
        sentences = re.split(r'[.!?]\s+', text)
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < chunk_size:
                current_chunk += sentence + ". "
            else:
                if current_chunk.strip():
                    chunks.append(Document(
                        page_content=current_chunk.strip(),
                        metadata=doc.metadata
                    ))
                current_chunk = sentence + ". "
        
        if current_chunk.strip():
            chunks.append(Document(
                page_content=current_chunk.strip(),
                metadata=doc.metadata
            ))
    
    return chunks

def extract_document_info(documents: List[Document]) -> dict:
    """Extract title and chapters from documents"""
    info = {"title": "Untitled", "chapters": []}
    
    if not documents:
        return info
    
    first_page_text = documents[0].page_content
    lines = first_page_text.strip().split('\n')
    
    for line in lines[:10]:
        line = line.strip()
        if 5 < len(line) < 120:
            if not any(skip in line.lower() for skip in ['page', 'author:', 'by:', 'date:', 'copyright']):
                info["title"] = line
                break
    
    return info
