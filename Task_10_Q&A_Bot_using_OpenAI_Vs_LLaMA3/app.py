import streamlit as st
import os
import tempfile
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer, CrossEncoder

# Import from local modules
from utils.config import config
from utils.document_processor import simple_split, extract_document_info
from utils.retriever import HybridRetriever
from models.model_handler import ModelHandler
from analytics.tracker import AnalyticsTracker
from ui.styles import get_custom_css
from langchain_core.documents import Document

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="OpenAI vs LLaMA3 Q&A Bot",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# ==================== SESSION STATE ====================
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'analytics' not in st.session_state:
    st.session_state.analytics = AnalyticsTracker()
if 'chunks' not in st.session_state:
    st.session_state.chunks = []
if 'retriever' not in st.session_state:
    st.session_state.retriever = None
if 'retriever_ready' not in st.session_state:
    st.session_state.retriever_ready = False
if 'last_query' not in st.session_state:
    st.session_state.last_query = None

# ==================== LOAD MODELS ====================
@st.cache_resource
def load_models():
    embedder = SentenceTransformer(config.EMBEDDING_MODEL)
    reranker = CrossEncoder(config.RERANKER_MODEL)
    model_handler = ModelHandler()
    return embedder, reranker, model_handler

# ==================== ANSWER GENERATION ====================
def generate_answers(query: str, retriever, model_handler) -> dict:
    """Generate answers from both models"""
    
    # Retrieve context
    relevant_docs = retriever.retrieve(query, top_k=config.TOP_K_RETRIEVAL)
    
    if not relevant_docs:
        return {
            "openrouter": {"answer": "No relevant information found.", "latency": 0, "sources": 0, "tokens": 0},
            "llama3": {"answer": "No relevant information found.", "latency": 0, "sources": 0, "tokens": 0}
        }
    
    context_text = "\n\n---\n\n".join([doc.page_content for doc in relevant_docs])
    
    system_prompt = """You are an elite AI assistant specializing in document analysis. 
Provide precise, professional, and well-structured responses based solely on the given context."""
    
    user_prompt = f"""Context:
{context_text}

Question: {query}

Provide a clear, accurate answer based only on the context above."""
    
    # Query both models
    results = model_handler.query_both(system_prompt, user_prompt)
    
    # Add sources
    results['openrouter']['sources'] = len(relevant_docs)
    results['llama3']['sources'] = len(relevant_docs)
    
    return results

# ==================== MAIN APP ====================
def main():
    # ===== BIG BOLD CENTERED TITLE =====
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0 2rem 0;">
        <h1 style="
            font-size: 4.5rem;
            font-weight: 900;
            color: #ffffff;
            letter-spacing: -3px;
            margin: 0;
            line-height: 1.2;
        ">OpenAI vs LLaMA3</h1>
        <p style="
            font-size: 1.2rem;
            color: #888888;
            margin-top: 0.8rem;
            font-weight: 300;
            letter-spacing: 0.5px;
        ">Q&A Bot</p>
        <p style="
            font-size: 0.95rem;
            color: #666666;
            margin-top: 1rem;
            font-weight: 300;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
            line-height: 1.5;
        ">Advanced comparison of leading AI models with hybrid retrieval & real-time analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load models
    embedder, reranker, model_handler = load_models()
    
    # ==================== SIDEBAR ====================
    with st.sidebar:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1a1a1a 0%, #1f1f1f 100%);
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid #2a2a2a;
            margin-bottom: 2rem;
        ">
            <div style="text-align: center;">
                <p style="font-size: 1.3rem; font-weight: 800; color: #ffffff; margin: 0;">⚙️ Controls</p>
                <p style="font-size: 0.8rem; color: #888888; margin: 0.5rem 0 0 0;">Upload & Manage Documents</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick Stats
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📈 Queries", st.session_state.analytics.total_queries)
        with col2:
            st.metric("📄 Chunks", len(st.session_state.chunks))
        
        st.markdown("---")
        
        st.markdown("### 📤 Upload Document")
        uploaded = st.file_uploader("Choose PDF", type=['pdf'])
        
        if uploaded and st.button("🚀 Process Document"):
            with st.spinner("Processing PDF..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as f:
                        f.write(uploaded.read())
                        pdf_path = f.name
                    
                    reader = PdfReader(pdf_path)
                    docs = []
                    for i, page in enumerate(reader.pages[:50]):
                        text = page.extract_text()
                        if text and len(text.strip()) > 50:
                            docs.append(Document(
                                page_content=text,
                                metadata={"page": i+1}
                            ))
                    
                    if not docs:
                        st.error("No text found in PDF")
                        st.stop()
                    
                    chunks = simple_split(docs, chunk_size=config.CHUNK_SIZE)
                    st.session_state.chunks = chunks[:150]
                    
                    st.session_state.retriever = HybridRetriever(
                        st.session_state.chunks,
                        embedder,
                        reranker
                    )
                    st.session_state.retriever_ready = True
                    
                    os.unlink(pdf_path)
                    st.success(f"✅ Processed {len(chunks)} chunks!")
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        st.markdown("---")
        
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.session_state.last_query = None
            st.rerun()
        
        if st.button("♻️ Reset Analytics"):
            st.session_state.analytics.reset()
            st.rerun()
        
        st.markdown("---")
        
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1a3a52 0%, #0f2d42 100%);
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
            border: 1px solid #2a4d62;
        ">
            <p style="font-size: 0.9rem; font-weight: 700; color: #5dade2; margin: 0;">
                📊 View Detailed Analytics →
            </p>
            <p style="font-size: 0.75rem; color: #888888; margin: 0.5rem 0 0 0;">
                Check sidebar navigation
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # ==================== CHAT HISTORY WITH INLINE VOTE BUTTONS ====================
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message("user", avatar="👤").markdown(msg["content"])
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="model-column">', unsafe_allow_html=True)
                st.markdown('<div class="model-header openai-header">🤖 OpenAI (via OpenRouter)</div>', unsafe_allow_html=True)
                st.markdown(msg["openrouter"]["answer"])
                
                # Metrics and Vote Button
                metric_col, vote_col = st.columns([4, 1])
                with metric_col:
                    st.markdown(f'<span class="metric-badge latency-badge">⚡ {msg["openrouter"]["latency"]}s</span> <span class="metric-badge sources-badge">📄 {msg["openrouter"]["sources"]} sources</span>', unsafe_allow_html=True)
                with vote_col:
                    if st.session_state.messages[-1] == msg:
                        if st.button("👍", key=f"vote_openai_{len(st.session_state.messages)}", help="Vote for OpenAI"):
                            st.session_state.analytics.record_vote("openai")
                            st.success("✅ OpenAI!")
                            st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="model-column">', unsafe_allow_html=True)
                st.markdown('<div class="model-header llama-header">🦙 LLaMA3</div>', unsafe_allow_html=True)
                st.markdown(msg["llama3"]["answer"])
                
                # Metrics and Vote Button
                metric_col, vote_col = st.columns([4, 1])
                with metric_col:
                    st.markdown(f'<span class="metric-badge latency-badge">⚡ {msg["llama3"]["latency"]}s</span> <span class="metric-badge sources-badge">📄 {msg["llama3"]["sources"]} sources</span>', unsafe_allow_html=True)
                with vote_col:
                    if st.session_state.messages[-1] == msg:
                        if st.button("👍", key=f"vote_llama3_{len(st.session_state.messages)}", help="Vote for LLaMA3"):
                            st.session_state.analytics.record_vote("llama3")
                            st.success("✅ LLaMA3!")
                            st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    # ==================== CHAT INPUT ====================
    if prompt := st.chat_input("Ask a question about your document..."):
        if not st.session_state.retriever_ready:
            st.error("⚠️ Please upload and process a PDF first!")
            st.stop()
        
        if st.session_state.last_query != prompt:
            st.session_state.last_query = prompt
            
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.spinner("🔍 Querying both models..."):
                results = generate_answers(prompt, st.session_state.retriever, model_handler)
            
            st.session_state.analytics.add_query(prompt, results['openrouter'], results['llama3'])
            
            st.session_state.messages.append({
                "role": "assistant",
                "openrouter": results['openrouter'],
                "llama3": results['llama3']
            })
            
            print("=" * 50)
            print("📊 ANALYTICS DEBUG")
            print(f"Total Queries: {st.session_state.analytics.total_queries}")
            print(f"OpenAI Wins: {st.session_state.analytics.openai_wins}")
            print(f"LLaMA3 Wins: {st.session_state.analytics.llama3_wins}")
            print("=" * 50)
            
            st.rerun()


if __name__ == "__main__":
    main()
