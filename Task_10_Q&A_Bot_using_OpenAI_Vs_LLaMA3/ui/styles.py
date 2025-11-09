def get_custom_css():
    return """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap');
    
    /* Animated Dark Background */
    .stApp {
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 25%, #0f0f0f 50%, #1a1a1a 75%, #0f0f0f 100%) !important;
        background-size: 400% 400% !important;
        animation: gradientShift 20s ease infinite !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    /* ===== KILL ALL BLUE AREAS ===== */
    .stChatFloatingInputContainer {
        background: transparent !important;
        background-color: transparent !important;
        background-image: none !important;
        border: none !important;
        box-shadow: none !important;
        padding: 1.5rem 0 3rem 0 !important;
    }
    
    div[data-testid="stChatInputContainer"] {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
    }
    
    div[data-testid="stBottom"] {
        background: transparent !important;
        background-color: transparent !important;
        background-image: none !important;
    }
    
    .main > div:last-child {
        background: transparent !important;
        background-color: transparent !important;
    }
    
    .stApp > div:last-child {
        background: transparent !important;
        background-color: transparent !important;
    }
    
    /* ===== CHAT MESSAGES (CARD STYLE) ===== */
    .stChatMessage {
        background: #1a1a1a !important;
        border-radius: 16px !important;
        border: 1px solid #2a2a2a !important;
        padding: 1.5rem !important;
        margin: 1rem auto !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
        max-width: 900px !important;
    }
    
    .stChatMessage:hover {
        background: #1f1f1f !important;
        border-color: #333333 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.5) !important;
    }
    
    .stChatMessage p {
        color: #e8e8e8 !important;
        font-size: 0.95rem !important;
        line-height: 1.7 !important;
    }
    
    /* ===== MODEL COLUMN CARDS ===== */
    .model-column {
        background: #1a1a1a;
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid #2a2a2a;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }
    
    .model-column:hover {
        background: #1f1f1f;
        border-color: #333333;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.5);
    }
    
    .model-header {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        padding-bottom: 0.8rem;
        border-bottom: 1px solid #2a2a2a;
    }
    
    .openai-header {
        color: #10a37f;
    }
    
    .llama-header {
        color: #7c3aed;
    }
    
    /* ===== ULTRA SLIM OVAL INPUT BOX ===== */
    .stChatInput {
        background: #1a1a1a !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 50px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
        padding: 0.75rem 1.5rem !important;
        max-width: 750px !important;
        margin: 0 auto !important;
        transition: all 0.2s ease !important;
        height: 48px !important;
    }
    
    .stChatInput:hover {
        border-color: #3a3a3a !important;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.5) !important;
    }
    
    .stChatInput:focus,
    .stChatInput:focus-within,
    .stChatInput:active {
        border: 1px solid #00d9ff !important;
        box-shadow: 0 0 0 2px rgba(0, 217, 255, 0.1), 0 6px 16px rgba(0, 0, 0, 0.5) !important;
        outline: none !important;
    }
    
    .stChatInput > div,
    .stChatInput > div > div {
        background: #1a1a1a !important;
        border: none !important;
        height: 100% !important;
    }
    
    .stChatInput textarea,
    .stChatInput input {
        background: #1a1a1a !important;
        color: #ffffff !important;
        border: none !important;
        font-size: 0.9rem !important;
        font-weight: 400 !important;
        height: 20px !important;
        padding: 0 !important;
    }
    
    .stChatInput textarea::placeholder,
    .stChatInput input::placeholder {
        color: #707070 !important;
    }
    
    .stChatInput textarea:hover,
    .stChatInput textarea:focus,
    .stChatInput input:hover,
    .stChatInput input:focus {
        background: #1a1a1a !important;
        border: none !important;
        outline: none !important;
    }
    
    /* Send button inside oval input */
    [data-testid="stChatInputSubmitButton"] button {
        background: transparent !important;
        color: #ffffff !important;
        border: none !important;
        padding: 0 !important;
        font-weight: 700 !important;
        transition: all 0.2s ease !important;
        font-size: 1.2rem !important;
    }
    
    [data-testid="stChatInputSubmitButton"] button:hover {
        color: #00d9ff !important;
        transform: scale(1.15) !important;
    }
    
    /* ===== VOTE THUMBS-UP BUTTONS (CIRCULAR) ===== */
    .model-column .stButton button {
        background: transparent !important;
        border: 2px solid #2a2a2a !important;
        border-radius: 50% !important;
        width: 45px !important;
        height: 45px !important;
        padding: 0 !important;
        font-size: 1.3rem !important;
        transition: all 0.3s ease !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        margin: 0 !important;
    }
    
    .model-column .stButton button:hover {
        background: rgba(0, 217, 255, 0.15) !important;
        border-color: #00d9ff !important;
        transform: scale(1.2) !important;
        box-shadow: 0 0 20px rgba(0, 217, 255, 0.4) !important;
    }
    
    .model-column .stButton button:active {
        transform: scale(0.9) !important;
        box-shadow: 0 0 10px rgba(0, 217, 255, 0.6) !important;
    }
    
    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background: #0f0f0f !important;
        border-right: 1px solid #2a2a2a !important;
    }
    
    section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }
    
    .stat-box {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }
    
    .stat-box:hover {
        background: #1f1f1f;
        border-color: #333333;
        transform: scale(1.02);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        color: #ffffff;
    }
    
    .stat-label {
        color: #888888;
        font-size: 0.75rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-top: 0.5rem;
        font-weight: 600;
    }
    
    /* ===== METRIC BADGES ===== */
    .metric-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.3rem;
        font-weight: 600;
    }
    
    .latency-badge {
        background: #1a3a52;
        color: #5dade2;
        border: 1px solid rgba(93, 173, 226, 0.3);
    }
    
    .sources-badge {
        background: #1a4d2e;
        color: #52c41a;
        border: 1px solid rgba(82, 196, 26, 0.3);
    }
    
    /* ===== BUTTONS (SIDEBAR) ===== */
    section[data-testid="stSidebar"] .stButton button {
        background: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 10px !important;
        padding: 0.7rem 1rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
        width: 100% !important;
        height: auto !important;
    }
    
    section[data-testid="stSidebar"] .stButton button:hover {
        background: #1f1f1f !important;
        border-color: #00d9ff !important;
        color: #00d9ff !important;
        transform: translateX(3px) !important;
        box-shadow: 0 4px 12px rgba(0, 217, 255, 0.2) !important;
    }
    
    /* ===== FILE UPLOADER ===== */
    .stFileUploader {
        background: #1a1a1a !important;
        border: 1px dashed #2a2a2a !important;
        border-radius: 12px !important;
        padding: 2rem !important;
    }
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 8px !important;
        height: 8px !important;
    }
    
    ::-webkit-scrollbar-track {
        background: transparent !important;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #2a2a2a !important;
        border-radius: 10px !important;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #3a3a3a !important;
    }
    
    /* ===== MAIN CONTAINER ===== */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 8rem !important;
        max-width: 1200px !important;
    }
    
    /* ===== NUCLEAR - REMOVE ALL BLUE ===== */
    * {
        background-image: none !important;
    }
    
    .stChatFloatingInputContainer,
    .stChatFloatingInputContainer > div,
    div[data-testid="stChatFloatingInputContainer"],
    div[data-testid="stBottom"] > div {
        background: transparent !important;
        background-color: transparent !important;
    }
    
    /* ===== SUCCESS MESSAGE STYLING ===== */
    .stSuccess {
        background: rgba(82, 196, 26, 0.1) !important;
        border: 1px solid rgba(82, 196, 26, 0.3) !important;
        border-radius: 10px !important;
        color: #52c41a !important;
        padding: 0.5rem 1rem !important;
        font-size: 0.85rem !important;
    }
</style>
"""
