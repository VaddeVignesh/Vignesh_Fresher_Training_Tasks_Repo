import streamlit as st
import summarizer
import evaluator
import utils
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="Smart Text Summarizer Pro", page_icon="✨", layout="wide")

st.markdown("""
<style>
body, .stApp {background: #151515; color: #ededed; font-family: 'Inter', sans-serif;}
header, .st-emotion-cache-18ni7ap {background: #151515 !important; box-shadow: none !important;}
section[data-testid="stSidebar"] {background: #141414 !important; color: #e0e0e0;}
.block-container {padding-top: 24px; padding-left: 32px; padding-right: 32px;}
.card-block {background: #212121; border-radius:16px; padding:22px 26px 26px 26px; margin-bottom:18px; box-shadow: 0 2px 9px #10101055;}
.top-controls {display: flex; gap:2rem; margin-bottom:0.1rem;}
.stTabs [data-baseweb="tab-list"] {background: #17171a!important; border-radius: 18px; padding-left: 8px!important; box-shadow: 0 1px 8px #11111333!important; margin-bottom: 0.2rem!important;}
.stTabs [data-baseweb="tab-list"] button {background: #18181b!important; color: #bcbaca!important; border-radius: 14px 14px 0 0!important; font-weight: 600!important; border: none!important; margin-right: 3px!important; padding: .6rem 2.2rem !important; transition: 0.18s;}
.stTabs [data-baseweb="tab-list"] button[aria-selected="true"]{background: linear-gradient(90deg,#212124,#1e1e22 99%)!important; color: #fff!important; font-weight: 700!important; box-shadow: 0 3px 8px #19191d38; border-bottom: 2.5px solid #ff552b !important;}
.stTabs [data-baseweb="tab-list"] button:active {outline:none;}
.stTabs [data-baseweb="tab-panel"] {background: #19191b !important; border-radius: 0 0 15px 15px; padding-top: 0.7rem; border-top: none; margin-bottom:3px;}
.stTextArea textarea, .stTextInput input, .stSelectbox, .stFileUploader {background-color: #18181b !important; color: #ededed !important; border-radius: 11px !important; border: 2px solid #222222 !important; font-size: 16px !important;}
.stTextArea textarea:focus, .stTextInput input:focus, .stSelectbox:focus, .stFileUploader:focus {border-color: #444 !important;}
.stButton>button {background: #232323; border-radius: 9px !important; color: #ffe6d6 !important; font-size: 16px !important; border: 1.2px solid #202020 !important; box-shadow: 0 1px 3px #08080866; transition: 0.15s;}
.stButton>button:hover {background: #272828; color: #fff !important; border-color: #ff552b !important;}
.stMetric {background: #19191a !important; border-radius: 10px !important; color: #eddcbe !important; font-weight: 600;}
.stExpander {background: #202020 !important; border-radius: 10px !important;}
[data-baseweb="tab-panel"] > div {margin-top: -7px !important;}
.stRadio [role="radiogroup"] {flex-direction: row;}
.stRadio label {background: #222226; border-radius: 18px; padding: .56rem 1.38rem; margin-right: 7px; font-weight: 500; font-size: 15.3px; border:1px solid transparent; transition:0.16s;}
.stRadio label[data-selected="true"]{background: linear-gradient(90deg,#2e2530 70%,#24282e 100%); color:#fff; border: 1.8px solid #ff552b;}
.stRadio label:hover {background: #24252e;}
.stTabs, .stTabs [data-baseweb="tab-panel"] > div {margin-bottom: 0!important;}
</style>
""", unsafe_allow_html=True)

if 'history' not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.title("🎯 Navigation")
    page = st.radio("Select:", ["📝 Summarize", "📚 History", "⚙️ Settings"])

st.markdown('<h1> Smart Text Summarizer </h1>', unsafe_allow_html=True)
st.write('<i>Professional AI-Powered Multi-Method Summarization</i>', unsafe_allow_html=True)

if page == "📝 Summarize":
    st.markdown('<div class="card-block">', unsafe_allow_html=True)
    col1, col2 = st.columns([2,3])
    with col1:
        summary_style = st.selectbox("Style", ["Brief", "Moderate", "Detailed"], index=0)
    with col2:
        translate_lang = st.radio("Translate to", ["None", "Hindi", "Tamil", "Telugu"], horizontal=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card-block">', unsafe_allow_html=True)
    tabs = st.tabs(["📄 Text", "📎 PDF", "🌐 URL", "🎵 Audio"])
    input_text = ""
    source_info = ""
    with tabs[0]:
        input_text = st.text_area("Paste your text here:", height=240, label_visibility="collapsed")
        source_info = "Text Input"
    with tabs[1]:
        pdf_file = st.file_uploader("Upload PDF", type="pdf", label_visibility="collapsed")
        if pdf_file:
            with st.spinner("Processing PDF..."):
                input_text = utils.extract_text_from_pdf(pdf_file)
                source_info = f"PDF: {pdf_file.name}"
                if not input_text.startswith("Error"):
                    st.success(f"✅ {len(input_text.split())} words extracted")
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
                        st.success(f"✅ {len(input_text.split())} words extracted")
            else:
                st.warning("Invalid URL. Please enter a valid http/https address.")
    with tabs[3]:
        audio_file = st.file_uploader("Upload Audio (MP3, WAV)", type=["mp3", "wav"], label_visibility="collapsed")
        if audio_file:
            with st.spinner("🎙️ Transcribing..."):
                input_text = utils.extract_audio_transcript(audio_file)
                source_info = f"Audio: {audio_file.name}"
                if not input_text.startswith("Error") and not input_text.startswith("Could"):
                    st.success(f"✅ {len(input_text.split())} words transcribed")
                else:
                    st.warning(input_text)
                    input_text = ""
    st.markdown('</div>', unsafe_allow_html=True)

    if input_text.strip() and not input_text.startswith("Error"):
        st.markdown('<div class="card-block">', unsafe_allow_html=True)
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
                        summary_text = summarizer.abstractive_summary(input_text, summary_style.lower())
                    else:
                        summary_text = summarizer.hybrid_summary(input_text, num)
                    if translate_lang != "None":
                        summary_text = summarizer.translate_summary(summary_text, translate_lang)
                    st.markdown('<div class="card-block">', unsafe_allow_html=True)
                    st.subheader("📋 Summary")
                    st.write(summary_text)
                    st.markdown('</div>', unsafe_allow_html=True)
                    compression = evaluator.calculate_compression_ratio(input_text, summary_text)
                    reading_time = evaluator.calculate_reading_time(summary_text)
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Compression", f"{compression}%")
                    col2.metric("Original", len(input_text.split()))
                    col3.metric("Summary", len(summary_text.split()))
                    col4.metric("Read Time", f"{reading_time}m")
                    st.session_state.history.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "source": source_info,
                        "method": summary_type,
                        "summary": summary_text[:300]
                    })
                    st.success("✅ Saved to history!")
                except Exception as e:
                    st.error(f"Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "📚 History":
    st.markdown('<div class="card-block">', unsafe_allow_html=True)
    st.subheader("History")
    for item in reversed(st.session_state.history):
        with st.expander(f"{item['timestamp']} | {item['source']}"):
            st.write(item['summary'])
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "⚙️ Settings":
    st.markdown('<div class="card-block">', unsafe_allow_html=True)
    st.subheader("Features")
    st.write("✅ Text, PDF, URL, Audio input")
    st.write("✅ Extractive (TextRank), TF-IDF, Abstractive, Hybrid methods")
    st.write("✅ Analytics & metrics")
    st.write("✅ Translation: Hindi, Tamil, Telugu")
    st.write("✅ History tracking")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("<div style='margin-top:50px;'></div>", unsafe_allow_html=True)
st.write("<div style='color:#878787;font-size:13px;text-align:center;opacity:.8;'>Made with ❤️ | Smart Summarization Pro</div>", unsafe_allow_html=True)
