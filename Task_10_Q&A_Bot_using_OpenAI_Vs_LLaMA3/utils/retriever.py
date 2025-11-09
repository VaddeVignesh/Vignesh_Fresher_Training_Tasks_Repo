from typing import List
from langchain_core.documents import Document
from rank_bm25 import BM25Okapi
import numpy as np

class HybridRetriever:
    """Combines semantic and keyword-based retrieval (no ChromaDB needed)"""
    
    def __init__(self, documents: List[Document], embedder, reranker):
        self.documents = documents
        self.embedder = embedder
        self.reranker = reranker
        
        # BM25 for keyword search
        tokenized_docs = [doc.page_content.lower().split() for doc in documents]
        self.bm25 = BM25Okapi(tokenized_docs)
        
        # Embed documents for semantic search
        print("Encoding documents for semantic search...")
        self.doc_embeddings = embedder.encode(
            [doc.page_content for doc in documents],
            show_progress_bar=False
        )
        print(f"Embedded {len(documents)} documents")
    
    def retrieve(self, query: str, top_k: int = 6) -> List[Document]:
        """Hybrid retrieval with reranking"""
        
        # Semantic search
        query_embedding = self.embedder.encode([query])[0]
        semantic_scores = self.doc_embeddings @ query_embedding
        semantic_top_indices = semantic_scores.argsort()[-top_k:][::-1]
        
        # Keyword search (BM25)
        tokenized_query = query.lower().split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        bm25_top_indices = bm25_scores.argsort()[-top_k:][::-1]
        
        # Combine results
        combined_indices = list(set(semantic_top_indices) | set(bm25_top_indices))
        candidates = [self.documents[i] for i in combined_indices]
        
        if not candidates:
            return []
        
        # Rerank with CrossEncoder
        pairs = [[query, doc.page_content] for doc in candidates]
        rerank_scores = self.reranker.predict(pairs)
        ranked_indices = rerank_scores.argsort()[::-1][:top_k]
        
        return [candidates[i] for i in ranked_indices if i < len(candidates)]
