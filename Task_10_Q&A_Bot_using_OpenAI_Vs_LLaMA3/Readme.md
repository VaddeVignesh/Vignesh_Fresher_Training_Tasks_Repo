
# OpenAI vs LLaMA3 Q&A Bot - Model Comparison System

**OpenAI vs LLaMA3 Q&A Bot** is an intelligent document-based chatbot built with Streamlit and a Retrieval-Augmented Generation (RAG) pipeline. It allows you to upload PDFs and compare responses from two powerful LLMs — **OpenAI models (via OpenRouter)** and **Meta LLaMA3** — side-by-side in real-time.

---

## Task Preview

![Task Screenshot](https://image2url.com/images/1762663087655-c33a2cca-1c5d-404f-98f6-899d5c4f46b2.png)

---

## Features

- **Dual-Model Comparison**: Get answers from both OpenAI and LLaMA3 simultaneously for the same question
- **Hybrid RAG Retrieval**: Combines BM25 keyword search + Semantic embeddings + Cross-encoder reranking for maximum accuracy
- **Upload Any PDF**: Research papers, reports, manuals — any document up to 50 pages
- **Interactive Voting**: Rate which model gave better answers with thumbs-up buttons
- **Real-Time Analytics**: Track 14+ metrics including speed, quality, cost, and user preferences
- **Modern Dark UI**: Clean, professional interface with animated gradients and chat-style messages
- **Performance Dashboard**: Separate analytics page showing detailed comparison metrics
- **Smart Chunking**: Intelligent text splitting maintains context for better retrieval
- **Answer Transparency**: Every response shows latency and number of sources used

---

## Example Use Cases

- **Research Analysis**: Compare how different LLMs interpret academic papers
- **Technical Documentation**: See which model better understands complex technical content
- **Business Reports**: Evaluate model accuracy for financial data extraction
- **Legal Documents**: Test which LLM provides more precise clause interpretations
- **Model Evaluation**: Benchmark LLM performance for specific domains

---

## How It Works

Here's the complete flow of the dual-model RAG pipeline:

### 1. PDF Upload & Processing
- Upload your document via Streamlit sidebar
- Text is extracted using `pypdf`
- Content is split into 500-character chunks with 50-char overlap
- Each chunk is tagged with page metadata

### 2. Hybrid Retrieval System
The custom retriever uses **three techniques** simultaneously:
- **BM25**: Keyword-based sparse retrieval for exact matches
- **Semantic Search**: Dense embeddings using `SentenceTransformer` (all-MiniLM-L6-v2)
- **Reranking**: `CrossEncoder` (ms-marco-MiniLM-L-6-v2) for final precision

### 3. Dual-Model Querying
- Query is sent to **both models in parallel**:
  - **OpenAI models** via OpenRouter API
  - **LLaMA3-8B-8192** via Groq (free, ultra-fast)
- Top 5 context chunks are provided to each model
- System prompts ensure precise, context-grounded answers

### 4. Response Comparison
- Both answers displayed **side-by-side** in clean cards
- Latency shown for each model (e.g., OpenAI: 3-5s, LLaMA3: 0.3-0.5s)
- Number of source chunks displayed
- Thumbs-up voting buttons to rate preferred answer

### 5. Analytics Tracking
Every query records:
- Response time (avg, min, max, median)
- Answer length and completeness
- Token usage and estimated costs
- User vote preferences
- Response consistency and hallucination rates

### 6. Dashboard Visualization
Navigate to **Analytics** page to see:
- Performance comparison tables
- Speed winner (% faster)
- Quality metrics breakdown
- User preference statistics
- Complete metric history

---

## Tech Stack Overview

| Layer | Tool / Library |
|-------|----------------|
| **Frontend** | Streamlit |
| **Styling** | Custom CSS (Dark theme + animated gradient) |
| **Vector Store** | In-memory (BM25 + Embeddings) |
| **Embeddings** | SentenceTransformer (all-MiniLM-L6-v2) |
| **Reranking** | CrossEncoder (ms-marco-MiniLM-L-6-v2) |
| **LLM 1** | OpenAI models (via OpenRouter) |
| **LLM 2** | LLaMA3-8B-8192 (via Groq) |
| **PDF Processing** | PyPDF |
| **Analytics** | Custom tracker with 14+ metrics |
| **Language** | Python 3.10+ |

---

## Installation & Setup

### Prerequisites
- Python 3.10 or higher
- OpenRouter API key (for OpenAI models)
- Groq API key (for LLaMA3 - free!)

### Step 1: Clone Repository
```
git clone https://github.com/yourusername/qa_bot_openai_vs_llama3.git
cd qa_bot_openai_vs_llama3
```

### Step 2: Install Dependencies
```
pip install -r requirements.txt
```

### Step 3: Configure API Keys
Edit `utils/config.py` and add your keys:
```
OPENROUTER_API_KEY = "your_openrouter_key_here"
GROQ_API_KEY = "your_groq_key_here"
```

Get your keys:
- **OpenRouter**: https://openrouter.ai/
- **Groq**: https://console.groq.com/ (FREE!)

### Step 4: Run Application
```
streamlit run app.py
```

Open browser to `http://localhost:8501`

---

## Usage Guide

### Step 1: Upload Document
1. Click **"Choose PDF"** in left sidebar
2. Select your PDF (max 50 pages recommended)
3. Click **"🚀 Process Document"**
4. Wait for confirmation message

### Step 2: Ask Questions
1. Type your question in chat input box at bottom
2. Press Enter
3. Watch both models generate answers simultaneously

### Step 3: Compare Responses
- Read both answers side-by-side
- Check latency (OpenAI usually 3-5s, LLaMA3 usually 0.3-0.5s)
- See how many source chunks each used
- Click 👍 on the better answer to vote

### Step 4: View Analytics
1. Click **"📊 Analytics"** in sidebar navigation
2. See complete performance breakdown
3. Check which model is faster/better
4. View user preference statistics

---

## Project Structure

```
qa_bot_openai_vs_llama3/
│
├── app.py                          # Main chat interface
│
├── pages/
│   └── 1_📊_Analytics.py          # Analytics dashboard
│
├── analytics/
│   └── tracker.py                  # Performance tracking
│
├── models/
│   └── model_handler.py            # OpenAI & LLaMA3 handlers
│
├── utils/
│   ├── config.py                   # API keys & settings
│   ├── retriever.py                # Hybrid retrieval (BM25+Semantic+Rerank)
│   └── document_processor.py       # PDF processing & chunking
│
├── ui/
│   └── styles.py                   # Custom CSS
│
└── requirements.txt                # Dependencies
```

---

## Key Metrics Tracked

### Response Quality
- **Avg Length**: Character count of answers
- **Completeness**: How thorough the response is (0-100%)
- **Consistency**: Response time stability (0-100%)
- **Hallucination Rate**: Variance in answer quality (lower = better)

### Speed & Performance
- **Latency Stats**: Average, median, min, max response times
- **Tokens/sec**: Generation speed
- **Throughput**: Queries processed per second

### Cost Analysis
- **Total Tokens**: Cumulative token usage
- **Avg Tokens/Query**: Efficiency per question
- **Estimated Cost**: OpenAI charges based on model, LLaMA3 is **FREE**

### User Preference
- **Vote Count**: Times each model was rated better
- **Win Percentage**: Model preference distribution

---

## Sample Results

**Test Document:** Machine Learning Research Paper (25 pages)  
**Questions:** 8 queries  

| Metric | OpenAI (OpenRouter) | LLaMA3-8B | Winner |
|--------|----------------|-----------|---------|
| Avg Latency | 3.5s | 0.4s | 🦙 LLaMA3 (88% faster) |
| Avg Length | 420 chars | 350 chars | 🤖 OpenAI |
| Completeness | 84% | 70% | 🤖 OpenAI |
| User Votes | 5 | 3 | 🤖 OpenAI (62.5%) |
| Total Cost | $0.0003 | FREE | 🦙 LLaMA3 |

**Verdict:** LLaMA3 wins on **speed and cost**, OpenAI wins on **answer quality and detail**.

---

## Conclusion

**OpenAI vs LLaMA3 Q&A Bot** transforms static PDFs into interactive knowledge sources while providing real-time comparison of two leading LLMs. 

It demonstrates how combining **hybrid RAG retrieval** with **dual-model inference** enables:
- Better evaluation of LLM capabilities
- Data-driven model selection for specific use cases
- Understanding speed vs. quality tradeoffs
- Transparent performance analytics

This isn't just a chatbot — it's a **complete LLM evaluation platform** built for comparing how different models understand and respond to your documents.

---

## Future Enhancements

- [ ] Multi-document querying across PDFs
- [ ] Export chat conversations as PDF/Markdown
- [ ] Add more LLMs (Claude, Gemini, Mistral)
- [ ] Voice input/output support
- [ ] Cloud deployment (Hugging Face Spaces)
- [ ] Advanced metrics (BLEU, ROUGE scores)
- [ ] Batch processing for multiple queries

---

