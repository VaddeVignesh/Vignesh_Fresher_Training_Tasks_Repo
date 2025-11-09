import statistics
import re
from typing import List, Dict
from datetime import datetime

class AnalyticsTracker:
    def __init__(self):
        self.total_queries = 0
        self.openai_wins = 0
        self.llama3_wins = 0
        self.openai_latencies = []
        self.llama3_latencies = []
        self.queries_log = []
        self.start_time = datetime.now()
        
        # Advanced metrics
        self.openai_answer_lengths = []
        self.llama3_answer_lengths = []
        self.openai_tokens_used = []
        self.llama3_tokens_used = []
        self.relevance_scores = []
    
    def add_query(self, query: str, openai_result: dict, llama3_result: dict):
        """Add query with comprehensive metrics"""
        self.total_queries += 1
        
        openai_answer = openai_result.get('answer', '')
        llama3_answer = llama3_result.get('answer', '')
        openai_latency = openai_result.get('latency', 0)
        llama3_latency = llama3_result.get('latency', 0)
        openai_tokens = openai_result.get('tokens', 0)
        llama3_tokens = llama3_result.get('tokens', 0)
        
        # Latency
        self.openai_latencies.append(float(openai_latency))
        self.llama3_latencies.append(float(llama3_latency))
        
        # Answer length
        self.openai_answer_lengths.append(len(openai_answer))
        self.llama3_answer_lengths.append(len(llama3_answer))
        
        # Token fallback if missing
        if openai_tokens <= 0:
            openai_tokens = len(openai_answer) // 4
        if llama3_tokens <= 0:
            llama3_tokens = len(llama3_answer) // 4
        
        self.openai_tokens_used.append(openai_tokens)
        self.llama3_tokens_used.append(llama3_tokens)
        
        # Relevance
        relevance = self._calculate_relevance(query, openai_answer, llama3_answer)
        self.relevance_scores.append(relevance)
        
        self.queries_log.append({
            'query': query,
            'openai_latency': openai_latency,
            'llama3_latency': llama3_latency,
            'openai_length': len(openai_answer),
            'llama3_length': len(llama3_answer),
            'openai_tokens': openai_tokens,
            'llama3_tokens': llama3_tokens,
            'timestamp': datetime.now(),
            'relevance': relevance
        })
    
    def record_vote(self, model: str):
        """Record user vote for better answer"""
        if model == "openai":
            self.openai_wins += 1
        elif model == "llama3":
            self.llama3_wins += 1

    def _calculate_relevance(self, query: str, ans1: str, ans2: str) -> float:
        """Calculate relevance score (0-100)"""
        query_words = set(query.lower().split())
        answer_words = set((ans1 + " " + ans2).lower().split())
        
        if not query_words:
            return 0.0
        
        overlap = len(query_words & answer_words)
        score = (overlap / len(query_words)) * 100
        
        return round(min(100, score), 1)

    # ===== HELPER METHOD =====
    
    def _safe_percent(self, value, total):
        """Safe percentage calculation with bounds"""
        if total <= 0:
            return 0.0
        percent = (value / total) * 100
        return round(min(max(percent, 0), 100), 1)

    # ===== ACCURACY & KNOWLEDGE =====

    def get_avg_relevance(self) -> float:
        """Average relevance score"""
        if not self.relevance_scores:
            return 0.0
        return round(statistics.mean(self.relevance_scores), 1)

    def get_accuracy(self, model: str) -> float:
        """Accuracy based on wins vs total queries"""
        if model == "openai":
            return self._safe_percent(self.openai_wins, self.total_queries)
        if model == "llama3":
            return self._safe_percent(self.llama3_wins, self.total_queries)
        return 0.0

    def get_precision(self, model: str) -> float:
        """Precision: Model wins / Total votes"""
        total_votes = self.openai_wins + self.llama3_wins
        if model == "openai":
            return self._safe_percent(self.openai_wins, total_votes)
        if model == "llama3":
            return self._safe_percent(self.llama3_wins, total_votes)
        return 0.0

    def get_recall(self, model: str) -> float:
        """Recall: Same as precision (no ground truth)"""
        return self.get_precision(model)

    def get_f1_score(self, model: str) -> float:
        """F1 Score: Harmonic mean of precision and recall"""
        p = self.get_precision(model)
        r = self.get_recall(model)
        if p + r == 0:
            return 0.0
        f1 = 2 * (p * r) / (p + r)
        return round(min(f1, 100), 1)

    def get_hallucination_rate(self, model: str) -> float:
        """Hallucination rate based on answer length variance"""
        if model == "openai":
            lengths = self.openai_answer_lengths
        else:
            lengths = self.llama3_answer_lengths

        if len(lengths) <= 1:
            return 0.0

        std_dev = statistics.stdev(lengths)
        avg = statistics.mean(lengths)

        if avg <= 0:
            return 0.0

        rate = (std_dev / avg) * 100
        return round(min(max(rate, 0), 100), 1)

    # ===== RESPONSE QUALITY =====

    def get_avg_answer_length(self, model: str) -> int:
        """Average answer length"""
        arr = self.openai_answer_lengths if model == "openai" else self.llama3_answer_lengths
        return round(statistics.mean(arr)) if arr else 0

    def get_completeness_score(self, model: str) -> float:
        """Completeness score (0-100)"""
        avg_length = self.get_avg_answer_length(model)
        score = (avg_length / 500) * 100
        return round(min(max(score, 0), 100), 1)

    def get_response_consistency(self, model: str) -> float:
        """Response consistency (0-100)"""
        arr = self.openai_latencies if model == "openai" else self.llama3_latencies
        if len(arr) <= 1:
            return 0.0
        
        std_dev = statistics.stdev(arr)
        avg = statistics.mean(arr)
        if avg <= 0:
            return 0.0
        
        cv = (std_dev / avg) * 100
        consistency = 100 - cv
        return round(min(max(consistency, 0), 100), 1)

    # ===== SPEED & PERFORMANCE =====

    def get_avg_latency(self, model: str) -> float:
        """Average latency"""
        arr = self.openai_latencies if model == "openai" else self.llama3_latencies
        return round(statistics.mean(arr), 2) if arr else 0.0

    def get_median_latency(self, model: str) -> float:
        """Median latency"""
        arr = self.openai_latencies if model == "openai" else self.llama3_latencies
        return round(statistics.median(arr), 2) if arr else 0.0

    def get_max_latency(self, model: str) -> float:
        """Max latency"""
        arr = self.openai_latencies if model == "openai" else self.llama3_latencies
        return round(max(arr), 2) if arr else 0.0

    def get_min_latency(self, model: str) -> float:
        """Min latency"""
        arr = self.openai_latencies if model == "openai" else self.llama3_latencies
        return round(min(arr), 2) if arr else 0.0

    def get_tokens_per_second(self, model: str) -> float:
        """Tokens per second"""
        tokens = self.openai_tokens_used if model == "openai" else self.llama3_tokens_used
        latencies = self.openai_latencies if model == "openai" else self.llama3_latencies

        if not tokens or not latencies:
            return 0.0

        total_tokens = sum(tokens)
        total_time = sum(latencies)

        if total_time <= 0:
            return 0.0
        
        return round(total_tokens / total_time, 1)

    def get_throughput(self) -> float:
        """Requests per second"""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        if elapsed <= 0:
            return 0.0
        return round(self.total_queries / elapsed, 2)

    # ===== COST & EFFICIENCY =====

    def get_total_tokens(self, model: str) -> int:
        """Total tokens used"""
        return sum(self.openai_tokens_used if model == "openai" else self.llama3_tokens_used)

    def get_avg_tokens_per_query(self, model: str) -> int:
        """Average tokens per query"""
        tokens = self.openai_tokens_used if model == "openai" else self.llama3_tokens_used
        return round(statistics.mean(tokens)) if tokens else 0

    def get_estimated_cost(self, model: str) -> float:
        """Estimated cost"""
        total_tokens = self.get_total_tokens(model)
        cost_per_1k = 0.0001 if model == "openai" else 0.0
        return round((total_tokens / 1000) * cost_per_1k, 4)

    # ===== HELPER METHODS =====

    def get_faster_model(self) -> str:
        """Get faster model with percentage"""
        if not self.openai_latencies or not self.llama3_latencies:
            return "N/A"
        
        avg_o = statistics.mean(self.openai_latencies)
        avg_l = statistics.mean(self.llama3_latencies)

        if avg_o <= 0 or avg_l <= 0:
            return "N/A"

        if avg_o < avg_l:
            pct = round(((avg_l - avg_o) / avg_l) * 100, 1)
            return f"🤖 OpenAI ({pct}% faster)"
        else:
            pct = round(((avg_o - avg_l) / avg_o) * 100, 1)
            return f"🦙 LLaMA3 ({pct}% faster)"

    def reset(self):
        """Reset analytics"""
        self.__init__()

