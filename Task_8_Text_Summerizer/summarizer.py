import os
import nltk
from nltk.tokenize import sent_tokenize
import numpy as np
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from dotenv import load_dotenv
import google.generativeai as genai
from transformers import pipeline

load_dotenv()
GEMINI_API_KEY = os.getenv("AIzaSyC8MuY3okHBz1YUTbl7HgkqqDb_mAxdyGA")
genai.configure(api_key=GEMINI_API_KEY)

# Use smaller model to avoid memory issues
abstractive_summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=-1)

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

def sentence_similarity(sent1, sent2):
    words1 = set(w.lower() for w in nltk.word_tokenize(sent1) if w.isalnum())
    words2 = set(w.lower() for w in nltk.word_tokenize(sent2) if w.isalnum())
    if not words1 or not words2:
        return 0
    return len(words1 & words2) / len(words1 | words2)

def build_similarity_matrix(sentences):
    n = len(sentences)
    sim_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                sim_matrix[i][j] = sentence_similarity(sentences[i], sentences[j])
    return sim_matrix

def extractive_summary(text, num_sentences=3):
    sentences = sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return text, list(range(len(sentences)))
    sim_matrix = build_similarity_matrix(sentences)
    graph = nx.from_numpy_array(sim_matrix)
    scores = nx.pagerank(graph)
    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    top_sentences = [s for _, s in ranked_sentences[:num_sentences]]
    summary = ' '.join(top_sentences)
    return summary, top_sentences

def tfidf_summary(text, num_sentences=3):
    sentences = sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return text, list(range(len(sentences)))
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(sentences)
    scores = tfidf_matrix.sum(axis=1).A1
    top_idx = np.argsort(scores)[-num_sentences:][::-1]
    top_idx_sorted = np.sort(top_idx)
    summary = ' '.join([sentences[i] for i in top_idx_sorted])
    return summary, top_idx_sorted.tolist()

def advanced_abstractive_summary(text, max_length=150, min_length=40):
    prompt = f"""Summarize the following text into clear, concise bullet points (max 7 points):

{text}

Summary:
"""
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        if response.text:
            return response.text.strip()
        result = abstractive_summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return result[0]["summary_text"]
    except Exception as e:
        print("Summarization error:", e)
        return ' '.join(sent_tokenize(text)[:3])

def hybrid_summary(text, num_sentences=5):
    extract, _ = extractive_summary(text, num_sentences)
    return advanced_abstractive_summary(extract)

def translate_summary(text, target_language="Hindi"):
    prompt = f"Translate the following text into {target_language}:\n\n{text}"
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text.strip() if response.text else text
    except Exception as e:
        print("Translation error:", e)
        return text
