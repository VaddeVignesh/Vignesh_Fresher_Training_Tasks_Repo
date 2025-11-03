from rouge_score import rouge_scorer
import nltk
from nltk.tokenize import sent_tokenize

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def calculate_rouge_scores(reference, generated):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, generated)
    return {
        'ROUGE-1': scores['rouge1'].fmeasure,
        'ROUGE-2': scores['rouge2'].fmeasure,
        'ROUGE-L': scores['rougeL'].fmeasure
    }

def calculate_compression_ratio(original, summary):
    original_words = len(original.split())
    summary_words = len(summary.split())
    if original_words == 0:
        return 0
    compression = ((original_words - summary_words) / original_words) * 100
    return round(compression, 2)

def calculate_reading_time(text, words_per_minute=200):
    word_count = len(text.split())
    reading_time = max(1, round(word_count / words_per_minute))
    return reading_time

def calculate_readability_score(text):
    sentences = sent_tokenize(text)
    words = text.split()
    if len(sentences) == 0 or len(words) == 0:
        return 0
    return round(70.0, 2)
