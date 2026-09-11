"""
Custom Dark Cyberpunk / Urban Tech Styling for Bengaluru Road Hazard Detector App
"""

import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
    /* Dark Futuristic Theme Overrides */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #1a1f2c 0%, #0d1117 70%, #05070a 100%);
        color: #e6edf3;
    }
    
    /* Header Gradient Banner */
    .app-header {
        background: linear-gradient(135deg, rgba(13, 17, 23, 0.9) 0%, rgba(22, 27, 34, 0.95) 100%);
        border: 1px solid rgba(0, 242, 254, 0.2);
        box-shadow: 0 8px 32px 0 rgba(0, 242, 254, 0.1);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .app-header-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 50%, #00e676 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .app-header-subtitle {
        color: #8b949e;
        font-size: 0.95rem;
        margin-top: 4px;
        font-weight: 400;
    }

    /* Metric Cards */
    .metric-card {
        background: rgba(22, 27, 34, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px 20px;
        backdrop-filter: blur(8px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(0, 242, 254, 0.4);
    }
    
    .metric-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #8b949e;
        font-weight: 600;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #f0f6fc;
        margin-top: 4px;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .metric-subtext {
        font-size: 0.75rem;
        color: #00f2fe;
        margin-top: 2px;
    }
    
    /* Precautionary Warning Banner (Pulse Animation) */
    @keyframes alertPulse {
        0% {
            box-shadow: 0 0 0 0 rgba(255, 0, 85, 0.7);
            border-color: #ff0055;
        }
        70% {
            box-shadow: 0 0 0 15px rgba(255, 0, 85, 0);
            border-color: #ff5588;
        }
        100% {
            box-shadow: 0 0 0 0 rgba(255, 0, 85, 0);
            border-color: #ff0055;
        }
    }

    .precaution-alert-box {
        background: linear-gradient(135deg, rgba(255, 0, 85, 0.15) 0%, rgba(100, 0, 30, 0.3) 100%);
        border: 2px solid #ff0055;
        border-radius: 14px;
        padding: 20px 24px;
        margin: 16px 0;
        animation: alertPulse 1.8s infinite;
        display: flex;
        align-items: center;
        gap: 16px;
    }

    .precaution-icon {
        font-size: 2.2rem;
    }

    .precaution-title {
        font-weight: 800;
        font-size: 1.2rem;
        color: #ff4d7d;
        letter-spacing: 0.5px;
    }

    .precaution-desc {
        color: #f0f6fc;
        font-size: 0.95rem;
        margin-top: 4px;
    }

    /* Status Badges */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .badge-severe {
        background: rgba(255, 0, 85, 0.2);
        color: #ff4d7d;
        border: 1px solid rgba(255, 0, 85, 0.5);
    }
    
    .badge-moderate {
        background: rgba(255, 153, 0, 0.2);
        color: #ffb84d;
        border: 1px solid rgba(255, 153, 0, 0.5);
    }
    
    .badge-minor {
        background: rgba(0, 230, 118, 0.2);
        color: #5cf29d;
        border: 1px solid rgba(0, 230, 118, 0.5);
    }

    .badge-info {
        background: rgba(0, 242, 254, 0.2);
        color: #00f2fe;
        border: 1px solid rgba(0, 242, 254, 0.5);
    }

    /* Custom Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%) !important;
        color: #05070a !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 14px rgba(0, 242, 254, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 242, 254, 0.5) !important;
    }

    /* Tabs Customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(13, 17, 23, 0.8);
        padding: 8px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .stTabs [data-baseweb="tab"] {
        height: 48px;
        white-space: pre-wrap;
        border-radius: 8px;
        color: #8b949e;
        font-weight: 600;
        font-size: 0.9rem;
        padding: 0 16px;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 242, 254, 0.15) 0%, rgba(79, 172, 254, 0.15) 100%) !important;
        color: #00f2fe !important;
        border: 1px solid rgba(0, 242, 254, 0.4) !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: #0d1117;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    </style>
    """, unsafe_allow_html=True)
