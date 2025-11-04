import streamlit as st
from datetime import datetime
import summarizer, evaluator, utils
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="Smart Text Summarizer Pro", page_icon="✨", layout="wide")

# --- Custom CSS ---
st.markdown("""
<style>
body, .stApp, .block-container {
    background: #202020 !important; color: #ededed !important;
}
section[data-testid="stSidebar"],
.st-emotion-cache-1r6slb0, .st-emotion-cache-6qob1r,
.st-emotion-cache-ocqkz7, .st-emotion-cache-1v0mbdj,
.st-emotion-cache-ul70rt, [data-testid="stSidebarNav"] ul,
.st-emotion-cache-12ttj6m {
    background: #181818 !important;
    color: #ededed !important;
}
[data-testid="stSidebarNav"] li:hover, .st-emotion-cache-ocqkz7:hover {
    background: #282828 !important;
    color: #fff !important;
    border-left: 3px solid #ff552b;
}
.st-emotion-cache-10trblm, .st-emotion-cache-1n76uvr, h1, h2, h3, h4 { color: #fff !important; }
.stTabs [data-baseweb="tab-list"], .stTabs [data-baseweb="tab-list"] button {
    background: #202020 !important;
    color: #ddd !important;
    box-shadow:none;
}
.stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
    background: #232323 !important;
    color: #fff !important;
    border-bottom:3px solid #ff552b;
}
.stTabs [data-baseweb="tab-panel"] {
    background: #202020 !important;
}
.stButton>button, .stSelectbox, .stDropdown, .stRadio label, .stMultiSelect {
    background: #232323 !important;
    color: #ededed !important;
    border-radius: 13px !important;
    border:none !important;
    font-weight:500;
}
.stTextArea textarea, .stTextInput input, .stFileUploader {
    background: #262626 !important;
    color: #ededed !important;
    border-radius: 11px !important;
    border: 1.5px solid #232323 !important;
}
</style>
""", unsafe_allow_html=True)
# ---

if 'history' not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.markdown("<span style='font-size:2rem; font-weight:800; color:#fff;'>🎯 Navigation</span>", unsafe_allow_html=True)
    page = st.radio("Select:", ["📝 Summarize", "📚 History", "ℹ️ About"], key="sidebar-nav")

st.markdown('<h1> Smart Text Summarizer </h1>', unsafe_allow_html=True)
st.write('<i>Professional AI-Powered Multi-Method Summarization</i>', unsafe_allow_html=True)

if page == "📝 Summarize":
    st.markdown('<div style="margin-top:15px;"></div>', unsafe_allow_html=True)
    tabs = st.tabs(["📄 Text", "📎 PDF", "🌐 URL"])  # AUDIO TAB REMOVED

    input_text = ""
    source_info = ""
    extracted_word_count = None

    with tabs[0]:
        input_text = st.text_area("Paste your text here:", height=240, label_visibility="collapsed")
        source_info = "Text Input"
        if input_text:
            extracted_word_count = len(input_text.split())
    with tabs[1]:
        pdf_file = st.file_uploader("Upload PDF", type="pdf", label_visibility="collapsed")
        if pdf_file:
            with st.spinner("Processing PDF..."):
                input_text = utils.extract_text_from_pdf(pdf_file)
                source_info = f"PDF: {pdf_file.name}"
                if not input_text.startswith("Error"):
                    extracted_word_count = len(input_text.split())
    with tabs[2]:
        url = st.text_input("Enter URL:", label_visibility="collapsed")
        if url:
            if utils.validate_url(url):
                with st.spinner("Scraping..."):
                    url_text = utils.scrape_url_content(url)
                    if url_text.startswith("Error"):
                        st.warning(url_text)
                        input_text = ""
                    else:
                        input_text = url_text
                        source_info = f"URL: {url}"
                        extracted_word_count = len(input_text.split())
            else:
                st.warning("Invalid URL. Please enter a valid http/https address.")

    # Controls row under tabs: Style left, Translate right
    colA, colB, colSpacer, colC = st.columns([1.4, 0.1, 6, 2])
    with colA:
        summary_style = st.selectbox("Style", ["Brief", "Moderate", "Detailed"], index=0)
    with colC:
        translate_lang = st.selectbox("Translate to", ["None", "Hindi", "Tamil", "Telugu"])

    if extracted_word_count:
        st.info(f"{extracted_word_count} words extracted 🟢")

    if input_text.strip() and not input_text.startswith("Error"):
        st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)
        summary_type = st.selectbox("Method:", ["Extractive", "Abstractive", "Hybrid", "TF-IDF"])
        if st.button("🚀 SUMMARIZE", use_container_width=True):
            with st.spinner("Generating..."):
                try:
                    size_map = {"Brief": 3, "Moderate": 5, "Detailed": 8}
                    num = size_map.get(summary_style, 5)
                    if summary_type == "Extractive":
                        summary_text, _ = summarizer.extractive_summary(input_text, num)
                    elif summary_type == "TF-IDF":
                        summary_text, _ = summarizer.tfidf_summary(input_text, num)
                    elif summary_type == "Abstractive":
                        summary_text = summarizer.advanced_abstractive_summary(input_text)
                    else:
                        summary_text = summarizer.hybrid_summary(input_text, num)

                    if translate_lang != "None":
                        summary_text = summarizer.translate_summary(summary_text, translate_lang)
                    
                    st.subheader("📋 Summary")
                    st.write(summary_text)
                    compression = evaluator.calculate_compression_ratio(input_text, summary_text)
                    reading_time = evaluator.calculate_reading_time(summary_text)
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Compression", f"{compression}%")
                    col2.metric("Original", len(input_text.split()))
                    col3.metric("Summary", len(summary_text.split()))
                    st.session_state.history.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "source": source_info,
                        "method": summary_type,
                        "summary": summary_text[:350]
                    })
                    st.success("✅ Saved to history!")
                except Exception as e:
                    st.error(f"Error: {e}")

elif page == "📚 History":
    st.subheader("History")
    for item in reversed(st.session_state.history):
        with st.expander(f"{item['timestamp']} | {item['source']}"):
            st.write(item['summary'])

elif page == "ℹ️ About":
    st.subheader("About Smart Text Summarizer Pro")
    st.markdown("""
<div style="padding:18px 22px 12px 8px; background:#181818; border-radius:9px;">
<b>Smart Text Summarizer Pro</b> is an advanced, AI-powered summarization suite for busy professionals, students, analysts, and teams.
<ul style="margin-top:18px;">
<li><b>✨ Multi-Source Input</b>: Summarize from raw text, PDF documents, and web URLs—just copy, upload, or paste!</li>
<li><b>🧠 Multiple Summarization Methods</b>: Choose from <b>Extractive (TextRank), Abstractive (LLM/GPT), TF-IDF, or Hybrid</b> for best results.</li>
<li><b>📝 Structured, Readable Output</b>: Results are always neat, with clear bullet points, clean formatting, and optional detail control.</li>
<li><b>🌏 Multilingual Support</b>: Instantly translate your summary into <b>Hindi, Tamil, or Telugu</b> (or keep in English)—perfect for local and regional projects.</li>
<li><b>⚡ Fast, Reliable, and Efficient</b>: Blazing performance using distilled transformer models and robust fallback logic—no crashes or long waits!</li>
<li><b>📊 Built-in Metrics</b>: Instant feedback on compression ratio, summary word count, and estimated reading time for every summary.</li>
<li><b>🕓 Secure Local Processing</b>: Your content stays on your machine; no third-party server uploads or sharing.</li>
<li><b>🖤 Beautiful, Distraction-Free UI</b>: Custom dark-mode interface with pro-level sidebar, minimalist controls, and focus on readability and speed.</li>
</ul>

</div>
</div>
""", unsafe_allow_html=True)


st.write("<div style='margin-top:35px;'></div>", unsafe_allow_html=True)
st.write("<div style='color:#878787;font-size:13px;text-align:center;opacity:.8;'>Made with ❤️ | Smart Summarization Pro</div>", unsafe_allow_html=True)
