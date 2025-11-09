import streamlit as st
from ui.styles import get_custom_css

# Page config
st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Apply CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Title
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="
        font-size: 3.5rem;
        font-weight: 900;
        color: #ffffff;
        letter-spacing: -2px;
        margin: 0;
    ">📊 Analytics Dashboard</h1>
    <p style="
        font-size: 1rem;
        color: #888888;
        margin-top: 0.5rem;
    ">Real-time Performance & Quality Metrics</p>
</div>
""", unsafe_allow_html=True)

# Check if analytics exists
if 'analytics' not in st.session_state:
    st.error("⚠️ No analytics data available. Please run some queries first!")
    st.stop()

analytics = st.session_state.analytics

if analytics.total_queries == 0:
    st.info("📊 Ask some questions to generate analytics data!")
    st.stop()

# ===== OVERVIEW =====
st.markdown("## 📈 Overview")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Queries", analytics.total_queries)
with col2:
    st.metric("Documents", len(st.session_state.get('chunks', [])))
with col3:
    st.metric("Throughput", f"{analytics.get_throughput()} req/s")
with col4:
    st.metric("Avg Relevance", f"{analytics.get_avg_relevance()}%")

st.markdown("---")

# ===== RESPONSE QUALITY =====
st.markdown("## ✨ Response Quality")

quality_data = {
    "Metric": ["Avg Length", "Completeness", "Consistency", "Hallucination Rate"],
    "🤖 OpenAI": [
        f"{analytics.get_avg_answer_length('openai')} chars",
        f"{analytics.get_completeness_score('openai')}%",
        f"{analytics.get_response_consistency('openai')}%",
        f"{analytics.get_hallucination_rate('openai')}%"
    ],
    "🦙 LLaMA3": [
        f"{analytics.get_avg_answer_length('llama3')} chars",
        f"{analytics.get_completeness_score('llama3')}%",
        f"{analytics.get_response_consistency('llama3')}%",
        f"{analytics.get_hallucination_rate('llama3')}%"
    ]
}

st.table(quality_data)

st.markdown("---")

# ===== SPEED & PERFORMANCE =====
st.markdown("## ⚡ Speed & Performance")

speed_data = {
    "Metric": ["Avg Latency", "Median", "Min", "Max", "Tokens/sec", "Total Time"],
    "🤖 OpenAI": [
        f"{analytics.get_avg_latency('openai')}s",
        f"{analytics.get_median_latency('openai')}s",
        f"{analytics.get_min_latency('openai')}s",
        f"{analytics.get_max_latency('openai')}s",
        f"{analytics.get_tokens_per_second('openai'):.1f}",
        f"{sum(analytics.openai_latencies):.2f}s" if analytics.openai_latencies else "0.00s"
    ],
    "🦙 LLaMA3": [
        f"{analytics.get_avg_latency('llama3')}s",
        f"{analytics.get_median_latency('llama3')}s",
        f"{analytics.get_min_latency('llama3')}s",
        f"{analytics.get_max_latency('llama3')}s",
        f"{analytics.get_tokens_per_second('llama3'):.1f}",
        f"{sum(analytics.llama3_latencies):.2f}s" if analytics.llama3_latencies else "0.00s"
    ]
}

st.table(speed_data)

st.markdown("---")

# ===== COST & EFFICIENCY =====
st.markdown("## 💰 Cost & Efficiency")

cost_data = {
    "Metric": ["Total Tokens", "Avg Tokens/Query", "Estimated Cost"],
    "🤖 OpenAI": [
        f"{analytics.get_total_tokens('openai'):,}",
        f"{analytics.get_avg_tokens_per_query('openai')}",
        f"${analytics.get_estimated_cost('openai'):.4f}"
    ],
    "🦙 LLaMA3": [
        f"{analytics.get_total_tokens('llama3'):,}",
        f"{analytics.get_avg_tokens_per_query('llama3')}",
        "FREE"
    ]
}

st.table(cost_data)

st.markdown("---")

# ===== PERFORMANCE WINNER =====
st.markdown("## 🏆 Performance Winner")

faster_model = analytics.get_faster_model()
st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #1a3a2e 0%, #0f2d24 100%);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    border: 1px solid #2a4d42;
">
    <p style="font-size: 2rem; font-weight: 800; color: #52c41a; margin: 0;">{faster_model}</p>
    <p style="font-size: 0.9rem; color: #888888; margin: 1rem 0 0 0;">Based on Average Latency</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ===== USER PREFERENCE =====
st.markdown("## 👍 User Preference")

total_votes = analytics.openai_wins + analytics.llama3_wins

if total_votes > 0:
    openai_pct = round((analytics.openai_wins / total_votes) * 100, 1)
    llama3_pct = round((analytics.llama3_wins / total_votes) * 100, 1)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1a3a52 0%, #0f2d42 100%);
            border-radius: 12px;
            padding: 2rem;
            text-align: center;
            border: 1px solid #2a4d62;
        ">
            <p style="font-size: 2.5rem; font-weight: 800; color: #5dade2; margin: 0;">{openai_pct}%</p>
            <p style="font-size: 1rem; color: #ffffff; margin: 1rem 0 0 0;">🤖 OpenAI ({analytics.openai_wins} votes)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #3a1a52 0%, #2d0f42 100%);
            border-radius: 12px;
            padding: 2rem;
            text-align: center;
            border: 1px solid #4d2a62;
        ">
            <p style="font-size: 2.5rem; font-weight: 800; color: #9d5dde; margin: 0;">{llama3_pct}%</p>
            <p style="font-size: 1rem; color: #ffffff; margin: 1rem 0 0 0;">🦙 LLaMA3 ({analytics.llama3_wins} votes)</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("👆 Vote for your preferred model responses in the main chat to see preference stats!")

st.markdown("---")

# ===== COMPLETE COMPARISON TABLE =====
st.markdown("## 📋 Complete Side-by-Side Comparison")

comparison_data = {
    "Metric": [
        "Avg Answer Length",
        "Completeness",
        "Consistency",
        "Hallucination Rate",
        "Avg Latency",
        "Min Latency",
        "Max Latency",
        "Median Latency",
        "Tokens/sec",
        "Total Time",
        "Total Tokens",
        "Avg Tokens/Query",
        "User Votes",
        "Estimated Cost"
    ],
    "🤖 OpenAI": [
        f"{analytics.get_avg_answer_length('openai')} chars",
        f"{analytics.get_completeness_score('openai')}%",
        f"{analytics.get_response_consistency('openai')}%",
        f"{analytics.get_hallucination_rate('openai')}%",
        f"{analytics.get_avg_latency('openai')}s",
        f"{analytics.get_min_latency('openai')}s",
        f"{analytics.get_max_latency('openai')}s",
        f"{analytics.get_median_latency('openai')}s",
        f"{analytics.get_tokens_per_second('openai'):.1f}",
        f"{sum(analytics.openai_latencies):.2f}s" if analytics.openai_latencies else "0.00s",
        f"{analytics.get_total_tokens('openai'):,}",
        f"{analytics.get_avg_tokens_per_query('openai')}",
        f"{analytics.openai_wins}",
        f"${analytics.get_estimated_cost('openai'):.4f}"
    ],
    "🦙 LLaMA3": [
        f"{analytics.get_avg_answer_length('llama3')} chars",
        f"{analytics.get_completeness_score('llama3')}%",
        f"{analytics.get_response_consistency('llama3')}%",
        f"{analytics.get_hallucination_rate('llama3')}%",
        f"{analytics.get_avg_latency('llama3')}s",
        f"{analytics.get_min_latency('llama3')}s",
        f"{analytics.get_max_latency('llama3')}s",
        f"{analytics.get_median_latency('llama3')}s",
        f"{analytics.get_tokens_per_second('llama3'):.1f}",
        f"{sum(analytics.llama3_latencies):.2f}s" if analytics.llama3_latencies else "0.00s",
        f"{analytics.get_total_tokens('llama3'):,}",
        f"{analytics.get_avg_tokens_per_query('llama3')}",
        f"{analytics.llama3_wins}",
        "FREE"
    ]
}

st.table(comparison_data)

st.markdown("---")

# ===== METRICS EXPLANATION =====
with st.expander("📖 Metrics Explanation"):
    st.markdown("""
    ### Response Quality Metrics
    - **Avg Length**: Average character count of responses
    - **Completeness**: How comprehensive the answers are (0-100%)
    - **Consistency**: How stable response times are (0-100%, higher is better)
    - **Hallucination Rate**: Response variance measure (0-100%, lower is better)
    
    ### Speed & Performance Metrics
    - **Avg/Median/Min/Max Latency**: Response time statistics
    - **Tokens/sec**: Generation speed (higher is better)
    - **Total Time**: Cumulative time spent generating responses
    
    ### Cost & Efficiency Metrics
    - **Total Tokens**: Sum of all tokens used
    - **Avg Tokens/Query**: Average tokens per query
    - **Estimated Cost**: API cost (OpenAI ~$0.0001 per 1k tokens, LLaMA3 is FREE)
    
    ### User Preference
    - **Votes**: Number of times users selected this model as better
    - Shows which model users prefer based on answer quality
    """)

st.markdown("---")

# ===== FOOTER =====
st.markdown("""
<div style="text-align: center; padding: 2rem 0; color: #666666; font-size: 0.85rem;">
    <p>📊 Analytics Dashboard | Real-time Performance Tracking</p>
    <p>Simplified View - F1/Precision/Recall/Accuracy Removed</p>
</div>
""", unsafe_allow_html=True)
