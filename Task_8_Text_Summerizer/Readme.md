

***

# Smart Text Summarizer Pro

## Overview

Smart Text Summarizer Pro is a professional AI-powered multi-method text summarization tool built with Python, Streamlit, and state-of-the-art NLP transformer models. This project supports multiple input sources: plain text, PDFs, URLs, and audio. It provides extractive, abstractive, TF-IDF, and hybrid summarization methods with multilingual translation of summaries.

***

## Features

- **Multi-Input Support:**  
  Summarize text from pasted input, **PDF upload**, web page URLs, and audio files (speech-to-text).

- **Multi-Method Summarization:**  
  - *Extractive:* TextRank-based ranking of key sentences  
  - *TF-IDF:* Keyword density sentence selection  
  - *Abstractive:* Transformer-based generative models for fluent summaries  
  - *Hybrid:* Combination of extractive and abstractive for better precision and readability

- **Structured Outputs:**  
  Clear, concise summaries in **well-formatted bullet points** or numbered lists for easy reading.

- **Multilingual Translation:**  
  Summaries can be translated to **Hindi, Tamil, or Telugu** using Google Gemini API integration.

- **User-Friendly UI:**  
  Built on Streamlit with dark-mode friendly theming and modern tab-based layout for input sources and methods.

- **Performance Optimization:**  
  Uses distilled transformer models to reduce resource consumption and avoid paging file errors on local machines.

- **Fallbacks and Robustness:**  
  Gracefully falls back to simpler extractive methods or partial summaries when API or model failures occur.

***

## Tech Stack Details

- **Python 3.10+**: Language for all backend, AI, and API integration logic.  
- **Streamlit**: Fast, interactive web UI framework for displaying and interacting with summaries.  
- **Transformers (Hugging Face)**: Open-source transformer models for abstractive summarization (using “sshleifer/distilbart-cnn-12-6”).  
- **Google Gemini API**: For powerful LLM summarization and multilingual translation generation.  
- **NLTK**: Natural language tokenizer for sentence splitting and preprocessing.  
- **NetworkX**: TextRank graph construction for extractive summarization.  
- **Scikit-learn**: TF-IDF vectorization for keyword based extractive summaries.  
- **PDFMiner / PyPDF2 / newspaper / Trafilatura**: For PDF and URL content extraction.  
- **SpeechRecognition / PyDub (optional)**: For audio transcription integration.

***

## Installation Instructions

1. Clone the repo:
   ```
   git clone <repo-url>
   cd smart-text-summarizer-pro
   ```

2. Create a Python virtual environment:
   ```
   python -m venv env
   source env/bin/activate  # or `env\Scripts\activate` on Windows
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Setup environment variables:
   - Create `.env` file with your Google Gemini API key:
     ```
     YOUR_GEMINI_API_KEY=your_api_key_here
     ```

5. Run the app:
   ```
   streamlit run app.py
   ```

***

## Usage

- Choose input source: Text, PDF, URL, or Audio.  
- Select summarization style (Brief, Moderate, Detailed).  
- Select translation language if desired.  
- Select summarization method (Extractive, Abstractive, Hybrid, TF-IDF).  
- Click Summarize and view the generated summary with metrics (compression ratio, reading time).

***

## Development Notes

- Abstractive summarization via a two-level fallback:  
  - Primary: Google Gemini LLM with bullet-point prompt  
  - Secondary: Local distilBART transformer  
- Extractive summarization uses PageRank scoring of sentence similarity graph.  
- TF-IDF method ranks sentences by keyword density with Scikit-learn's `TfidfVectorizer`.  
- Hybrid summarization combines extractive sentence selection with abstractive rewriting for clarity.  
- Translation also uses Gemini LLM API for accurate multilingual output.

***

## Limitations & Future Work

- URL scraping may fail on JS-heavy or paywalled sites. Future: integrate headless browsers.  
- Audio transcription currently basic, can improve with specialized ASR models.  
- Deploying on GPU/cloud recommended for large text inputs and faster abstractive summaries.  
- UI can be improved with better progress indicators and error handling messages.

***

## Contact

Developed by [Your Name] — reach out for bug reports or feature requests.

***

Let me know if you want me to generate the matching full updated `app.py` or any other files next! 
