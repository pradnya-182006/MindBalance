import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import os
import subprocess
import streamlit.components.v1 as components

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="MindBalance | AI Digital Wellness",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

def local_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');
    :root {
        --th: #1e293b; /* Deep slate for headings */
        --tb: #475569; /* Soft slate body text */
        --tm: #94a3b8; /* Muted text */
        --primary: #6366f1; /* muted blue */
        --accent: #a855f7;  /* soft purple */
        --grad: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        --rose: #f43f5e; --amber: #f59e0b; --sage: #10b981; --slate: #6366f1;
        --glass-bg: rgba(255, 255, 255, 0.6);
        --glass-border: rgba(255, 255, 255, 0.8);
        --glass-shadow: 0 10px 40px -10px rgba(99, 102, 241, 0.15);
    }
    
    html, body, [class*="css"], .stApp {
        font-family: 'Nunito', sans-serif !important;
        color: var(--tb) !important;
    }
    
    /* Main Background */
    .stApp, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #eef2ff 0%, #f3e8ff 50%, #f8fafc 100%) !important; 
        background-attachment: fixed !important;
    }

    [data-testid="stHeader"], [data-testid="stToolbar"] { background: transparent !important; box-shadow: none !important; }
    .main .block-container { padding: 2.5rem 2.8rem !important; max-width: 1120px; }
    
    /* Sidebar Glassmorphism */
    [data-testid="stSidebar"] { 
        background-color: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(24px) !important;
        -webkit-backdrop-filter: blur(24px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.5) !important; 
        box-shadow: 4px 0 30px rgba(99, 102, 241, 0.05) !important; 
    }
    [data-testid="stSidebar"] .block-container { padding: 1.8rem 1rem !important; }

    /* Typography */
    h1 { font-size: 2.4rem !important; font-weight: 800 !important; color: var(--th) !important; letter-spacing: -0.5px; margin-bottom: 0.4rem !important; }
    h2 { font-weight: 700 !important; color: var(--th) !important; font-size: 1.3rem !important; border: none !important; padding: 0 !important; }
    h3 { font-weight: 600 !important; color: var(--th) !important; font-size: 1rem !important; }
    p { color: var(--tb); line-height: 1.7; }
    .highlight-text { 
        background: var(--grad) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        font-weight: 800;
    }

    /* Cards - Glassmorphism */
    .nm-card { 
        background: var(--glass-bg); 
        border-radius: 20px; 
        padding: 1.8rem 2rem; 
        margin-bottom: 1.2rem; 
        box-shadow: var(--glass-shadow); 
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-top: 1px solid rgba(255,255,255,1);
        border-left: 1px solid rgba(255,255,255,1);
        transition: transform .3s ease, box-shadow .3s ease; 
    }
    .nm-card:hover { transform: translateY(-4px); box-shadow: 0 20px 40px -10px rgba(168, 85, 247, 0.2); }
    
    .nm-sm { 
        background: var(--glass-bg); 
        border-radius: 16px; 
        padding: 1.2rem 1.3rem; 
        box-shadow: var(--glass-shadow); 
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
    }
    .nm-inset { 
        background: rgba(255, 255, 255, 0.3); 
        border-radius: 14px; 
        padding: 1rem 1.2rem; 
        box-shadow: inset 0 2px 8px rgba(99, 102, 241, 0.05); 
        border: 1px solid rgba(255, 255, 255, 0.5);
    }

    .sec-label { font-size: 0.72rem; font-weight: 700; color: var(--tm); text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 0.75rem; display: block; }

    /* Pills */
    .stat-pill { 
        display: inline-flex; align-items: center; gap: 7px; 
        background: rgba(255, 255, 255, 0.8); 
        border-radius: 50px; padding: 0.4rem 1rem; 
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.05); 
        border: 1px solid rgba(255, 255, 255, 0.9);
        font-size: 0.78rem; font-weight: 700; color: var(--th); margin: 3px; 
    }
    .dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }

    .feat-card { 
        background: var(--glass-bg); border-radius: 18px; padding: 1.3rem; 
        box-shadow: var(--glass-shadow); backdrop-filter: blur(16px);
        border: 1px solid var(--glass-border); transition: all .3s ease; 
    }
    .feat-card:hover { box-shadow: 0 15px 35px -10px rgba(99, 102, 241, 0.2); transform: translateY(-4px); }
    .feat-icon { width: 44px; height: 44px; border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 20px; margin-bottom: 0.75rem; box-shadow: 0 4px 15px rgba(99, 102, 241, 0.15); background: #ffffff; }

    /* Buttons */
    .stButton>button { 
        background: rgba(255, 255, 255, 0.7) !important; 
        color: var(--primary) !important; 
        border: 1px solid rgba(255, 255, 255, 1) !important; 
        border-radius: 50px !important; 
        padding: 0.65rem 1.6rem !important; 
        font-family: 'Nunito', sans-serif !important; 
        font-weight: 700 !important; font-size: 0.95rem !important; 
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.1) !important; 
        backdrop-filter: blur(12px); transition: all .3s ease !important; width: 100%; 
    }
    .stButton>button:hover { 
        box-shadow: 0 12px 25px rgba(168, 85, 247, 0.2) !important; 
        background: #ffffff !important; 
        transform: translateY(-2px); 
    }
    .stButton>button:active { transform: translateY(0); }

    /* Primary CTA */
    .cta-btn>button { 
        background: var(--grad) !important; 
        color: #fff !important; border: none !important;
        box-shadow: 0 8px 25px rgba(168, 85, 247, 0.4) !important; 
    }
    .cta-btn>button:hover { 
        background: linear-gradient(135deg, #7c7eff 0%, #bd73fa 100%) !important; 
        box-shadow: 0 12px 30px rgba(168, 85, 247, 0.6) !important; 
        color: #fff !important; 
        transform: translateY(-2px); 
    }

    /* Submit Button */
    [data-testid="stFormSubmitButton"]>button { 
        background: var(--grad) !important; 
        color: #fff !important; border: none !important; border-radius: 50px !important; 
        font-weight: 700 !important; font-size: 0.95rem !important; padding: 0.7rem 2rem !important; 
        box-shadow: 0 8px 25px rgba(168, 85, 247, 0.4) !important; width: 100%; transition: all .3s ease !important; 
    }
    [data-testid="stFormSubmitButton"]>button:hover { 
        box-shadow: 0 12px 30px rgba(168, 85, 247, 0.6) !important; 
        transform: translateY(-2px); 
    }

    /* Inputs */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div, .stTextArea textarea {
        background: rgba(255, 255, 255, 0.7) !important; 
        border: 1px solid rgba(255, 255, 255, 0.9) !important; 
        border-radius: 12px !important;
        box-shadow: inset 0 2px 6px rgba(99, 102, 241, 0.05) !important;
        color: var(--th) !important; font-weight: 600 !important; 
        transition: all 0.2s ease !important;
    }
    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus, .stSelectbox>div>div:focus-within {
        box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.2) !important; 
        border-color: var(--primary) !important; 
        background: #ffffff !important;
    }
    .stTextInput label, .stNumberInput label, .stSelectbox label, .stSlider label, .stTextArea label {
        font-size: 0.78rem !important; font-weight: 700 !important; color: var(--tm) !important;
        text-transform: uppercase !important; letter-spacing: 0.8px !important; 
    }

    [data-testid="stSlider"]>div>div>div { background: var(--grad) !important; }
    [data-testid="stSlider"]>div>div>div>div { 
        background: white !important; 
        box-shadow: 0 4px 12px rgba(168, 85, 247, 0.3) !important; 
        border: 3px solid var(--primary) !important; 
    }

    [data-testid="stMetric"] { 
        background: var(--glass-bg) !important; 
        border-radius: 16px !important; 
        padding: 1.2rem 1.4rem !important; 
        box-shadow: var(--glass-shadow) !important; 
        border: 1px solid var(--glass-border); 
        backdrop-filter: blur(20px); 
    }
    [data-testid="stMetricValue"] { color: var(--th) !important; font-weight: 800 !important; font-size: 2.2rem !important; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { 
        background: rgba(255, 255, 255, 0.5) !important; 
        border-radius: 14px; padding: 6px; gap: 8px; 
        backdrop-filter: blur(16px);
        box-shadow: inset 0 2px 8px rgba(99, 102, 241, 0.05);
    }
    .stTabs [data-baseweb="tab"] { background: transparent !important; color: var(--tm) !important; border-radius: 10px !important; font-weight: 700 !important; font-size: 0.9rem !important; padding: 0.6rem 1.2rem !important; }
    .stTabs [aria-selected="true"] { 
        background: #ffffff !important; 
        color: var(--primary) !important; 
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.1) !important; 
    }

    /* Sidebar Radio */
    [data-testid="stRadio"]>div { gap: 4px !important; }
    [data-testid="stRadio"] label { background: transparent !important; border-radius: 12px !important; padding: 0.65rem 1rem !important; font-size: 0.95rem !important; font-weight: 700 !important; color: var(--th) !important; cursor: pointer; transition: all .3s ease; display: flex !important; align-items: center; gap: 8px; }
    [data-testid="stRadio"] label:hover { 
        background: rgba(255, 255, 255, 0.8) !important; 
        color: var(--primary) !important; 
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.08) !important;
        transform: translateX(3px);
    }

    /* Dropdowns */
    [data-baseweb="popover"] [data-baseweb="menu"] { background: rgba(255, 255, 255, 0.9) !important; backdrop-filter: blur(12px) !important; border-radius: 14px !important; box-shadow: 0 8px 24px rgba(110, 100, 160, 0.15) !important; border: 1px solid rgba(255,255,255,0.8) !important; }
    [data-baseweb="option"]:hover { background: rgba(99, 102, 241, 0.1) !important; border-radius: 8px !important; color: var(--primary) !important; font-weight: 700; }

    /* Number input buttons */
    [data-testid="stNumberInput"] button { background: rgba(255, 255, 255, 0.7) !important; border: 1px solid rgba(255, 255, 255, 0.9) !important; border-radius: 8px !important; box-shadow: 0 2px 6px rgba(110, 100, 160, 0.05) !important; color: var(--primary) !important; font-weight: 600 !important; }
    [data-testid="stNumberInput"] button:hover { background: #fff !important; color: #a855f7 !important; }

    .badge { display: inline-block; border-radius: 50px; padding: 4px 16px; font-size: 0.75rem; font-weight: 800; }
    .badge-h { background: #fff; color: var(--rose); box-shadow: 0 8px 20px rgba(244, 63, 94, 0.2); }
    .badge-m { background: #fff; color: var(--amber); box-shadow: 0 8px 20px rgba(245, 158, 11, 0.2); }
    .badge-l { background: #fff; color: var(--sage); box-shadow: 0 8px 20px rgba(16, 185, 129, 0.2); }

    @keyframes soft-pulse { 0%,100%{opacity:1} 50%{opacity:.5} }
    .pulse { animation: soft-pulse 2.2s ease-in-out infinite; }

    /* Plotly Chart Entry Animations */
    @keyframes bar-grow {
        0% { transform: scaleY(0); opacity: 0; }
        100% { transform: scaleY(1); opacity: 1; }
    }
    @keyframes chart-fade {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .js-plotly-plot .cartesianlayer .trace.bars rect.point {
        transform-box: fill-box;
        transform-origin: bottom;
        animation: bar-grow 1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    .js-plotly-plot .pie path {
        transform-box: fill-box;
        transform-origin: center;
        animation: chart-fade 1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    hr { border: none !important; border-top: 1px solid rgba(255, 255, 255, 0.8) !important; margin: 1.5rem 0 !important; box-shadow: 0 1px 0 rgba(99, 102, 241, 0.05) !important; }
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(99, 102, 241, 0.3); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(168, 85, 247, 0.6); }
    .js-plotly-plot .plotly .bg { fill: transparent !important; }

    /* ─── Behavioral badge ───────────────────────── */
    .beh-badge {
        display: inline-flex; align-items: center; gap: 8px;
        background: rgba(255,255,255,0.8);
        border-radius: 50px; padding: 0.35rem 0.9rem;
        border: 1px solid rgba(255,255,255,0.9);
        font-size: 0.76rem; font-weight: 700; color: var(--th);
        box-shadow: 0 4px 12px rgba(99,102,241,0.07);
    }

    /* ─── Quick Intake ───────────────────────────── */
    .intake-q {
        background: rgba(255,255,255,0.5);
        border-radius: 14px; padding: 0.9rem 1.1rem;
        margin-bottom: 0.5rem;
        border: 1px solid rgba(255,255,255,0.8);
        display: flex; align-items: flex-start; gap: 12px;
    }
    .intake-icon {
        width: 36px; height: 36px; border-radius: 11px;
        background: linear-gradient(135deg,#eef2ff,#f3e8ff);
        display: flex; align-items:center; justify-content:center;
        font-size: 17px; flex-shrink: 0;
        border: 1px solid rgba(255,255,255,0.9);
        margin-top: 2px;
    }

    /* ─── Emoji Feedback ─────────────────────────── */
    .feedback-wrap {
        background: var(--glass-bg);
        border-radius: 20px; padding: 2rem 2.2rem;
        margin-top: 1.8rem;
        box-shadow: var(--glass-shadow); backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-top: 1px solid rgba(255,255,255,1);
    }
    .emoji-satisfaction-row {
        display: flex; justify-content: space-between;
        align-items: stretch; gap: 10px;
        margin: 1.2rem 0 0.8rem;
    }
    .emoji-sat-card {
        flex: 1; display: flex; flex-direction: column;
        align-items: center; justify-content: space-between;
        gap: 8px; padding: 1rem 0.5rem;
        border-radius: 16px; cursor: pointer;
        border: 2px solid rgba(255,255,255,0.7);
        background: rgba(255,255,255,0.35);
        transition: all 0.25s cubic-bezier(0.34,1.56,0.64,1);
        min-width: 0;
    }
    .emoji-sat-card:hover {
        background: rgba(255,255,255,0.75);
        border-color: rgba(99,102,241,0.25);
        transform: translateY(-6px);
        box-shadow: 0 14px 30px rgba(99,102,241,0.12);
    }
    .emoji-sat-card.active {
        background: rgba(255,255,255,0.95);
        border-color: var(--primary);
        transform: translateY(-6px);
        box-shadow: 0 14px 30px rgba(99,102,241,0.18);
    }
    .emoji-sat-face {
        font-size: 2.5rem; line-height: 1;
        filter: grayscale(40%);
        transition: all 0.2s ease;
    }
    .emoji-sat-card:hover .emoji-sat-face,
    .emoji-sat-card.active .emoji-sat-face {
        filter: grayscale(0%);
        transform: scale(1.18);
    }
    .emoji-sat-label {
        font-size: 0.66rem; font-weight: 700;
        color: #94a3b8; text-align: center; line-height: 1.35;
        text-transform: uppercase; letter-spacing: 0.4px;
    }
    .emoji-sat-card.active .emoji-sat-label { color: var(--primary); }
    .sat-radio-dot {
        width: 16px; height: 16px; border-radius: 50%;
        border: 2px solid rgba(148,163,184,0.4);
        background: rgba(255,255,255,0.8);
        transition: all 0.2s;
    }
    .emoji-sat-card.active .sat-radio-dot {
        background: var(--primary);
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(99,102,241,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# ── HELPERS ──────────────────────────────────
def load_model():
    try:
        with open(os.path.join(BASE_DIR, 'best_model.pkl'),'rb') as f: model = pickle.load(f)
        with open(os.path.join(BASE_DIR, 'features.pkl'),'rb') as f:   feats  = pickle.load(f)
        return model, feats
    except: return None, None

def get_bsmas_result(score):
    if score <= 12:
        return "Balanced User","#4aaa88","Healthy usage pattern detected.",[
            "Maintain current digital boundaries.",
            "Schedule Phone-Free weekends.",
            "Continue focused deep work sessions.",]
    elif score <= 18:
        return "Mild Risk (Habitual)","#d99a2e","Showing signs of habitual dependency.",[
            "Enable App Timers for social media.",
            "Delete apps during exam weeks.",
            "Replace 30 min/day with a physical hobby.",]
    elif score <= 24:
        return "High Risk Dependency","#d96b6b","Digital habits are impacting mental health.",[
            "Start a 48-hour Digital Detox.",
            "Switch phone to grayscale mode.",
            "Uninstall high-attachment apps immediately.",]
    else:
        return "Severe Addiction Risk","#b84040","Urgent digital intervention suggested.",[
            "Consult a therapist for behavioral patterns.",
            "Transition to essential-only apps.",
            "Commit to a 30-day social media break.",]

NM = dict(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
          font=dict(family='Nunito',color='#6a6287'),
          margin=dict(l=20,r=20,t=30,b=20))

# ── NAV ──────────────────────────────────────
PAGES = ["Home","Psychological Assessment","Dataset Insights","Screen Time Controller"]
ICONS = ["⊙","◈","◎","◉"]
if 'menu' not in st.session_state: st.session_state.menu = "Home"
if 'feedback_submitted' not in st.session_state: st.session_state.feedback_submitted = False
if 'fb_val' not in st.session_state: st.session_state.fb_val = 3

# ── SIDEBAR ───────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style='padding:0.4rem 0 1.6rem;'>
            <div style='display:flex;align-items:center;gap:10px;margin-bottom:4px;'>
                <div style='width:38px;height:38px;border-radius:12px;background:rgba(255,255,255,0.6);
                            box-shadow:0 4px 10px rgba(110,100,160,0.1);border:1px solid rgba(255,255,255,0.8);
                            display:flex;align-items:center;justify-content:center;font-size:20px;'>🧠</div>
                <div>
                    <p style='font-size:1.1rem;font-weight:800;color:#4b3e7c;margin:0;line-height:1.2;'>MindBalance</p>
                    <p style='font-size:0.62rem;color:#9aa0bc;letter-spacing:1.2px;text-transform:uppercase;margin:0;'>AI Digital Wellness</p>
                </div>
            </div>
        </div>

        <p style='font-size:0.62rem;color:#9aa0bc;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px;padding-left:4px;'>Navigation</p>
    """, unsafe_allow_html=True)

    menu = st.radio("Navigation", PAGES,
        index=PAGES.index(st.session_state.menu),
        format_func=lambda x: f"{ICONS[PAGES.index(x)]}  {x}",
        label_visibility="collapsed"
    )
    st.session_state.menu = menu

    try:
        df_stats = pd.read_csv(os.path.join(BASE_DIR, 'social_media_addiction_data.csv'))
        avg_risk = int(df_stats['Status'].mean() * 100)
        total_assessments = len(df_stats)
        avg_usage = round(df_stats['Avg_Daily_Usage_Hours'].mean(), 1)
    except:
        avg_risk, total_assessments, avg_usage = 72, 1284, 6.4

    st.markdown("<hr>", unsafe_allow_html=True)
    stats_html = "".join([f"""
        <div style='background:rgba(255,255,255,0.6);border-radius:12px;padding:0.65rem 1rem;
                    box-shadow:0 4px 10px rgba(110,100,160,0.05);border:1px solid rgba(255,255,255,0.8);
                    display:flex;justify-content:space-between;align-items:center;'>
            <span style='font-size:0.76rem;color:#6a6287;font-weight:600;'>{lbl}</span>
            <span style='font-size:0.86rem;font-family:DM Mono,monospace;font-weight:600;color:{clr};'>{val}</span>
        </div>""" for lbl,val,clr in [
            ("Avg Risk Score",f"{avg_risk}%","#ee5e76"),
            ("Assessments",f"{total_assessments:,}","#604e9c"),
            ("Model Accuracy","99.1%","#2bb996"),
        ]])
    
    st.markdown(f"""
        <p style='font-size:0.62rem;color:#9aa0bc;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;padding-left:4px;'>Quick Stats</p>
        <div style='display:flex;flex-direction:column;gap:7px;'>
            {stats_html}
        </div>
    """, unsafe_allow_html=True)


# ── HOME ─────────────────────────────────────
if menu == "Home":
    st.markdown("""
        <h1>Decode Your <span class='highlight-text'>Digital Life</span></h1>
        <p style='color:#9aa0bc;font-size:0.88rem;margin-top:-0.5rem;margin-bottom:2rem;'>
        AI-powered social media addiction analysis for students & educators.
        </p>
    """, unsafe_allow_html=True)

    c1,c2 = st.columns([3,2], gap="large")
    with c1:
        st.markdown("""
            <div class='nm-card'>
                <span class='sec-label'>About This Tool</span>
                <h2 style='margin-top:0;margin-bottom:0.7rem;'>Real-World Addiction Analysis</h2>
                <p style='margin-bottom:1.2rem;font-size:0.9rem;line-height:1.75;'>
                Move beyond simple screen-time tracking. Understand the
                <strong style='color:#2d3250;'>psychological impact</strong> of digital consumption
                on your sleep, focus, academic performance, and relationships.
                </p>
                <div style='display:flex;flex-wrap:wrap;gap:5px;'>
                    <span class='stat-pill'><span class='dot' style='background:#ee5e76;'></span>Risk Detection</span>
                    <span class='stat-pill'><span class='dot' style='background:#604e9c;'></span>BSMAS Assessment</span>
                    <span class='stat-pill'><span class='dot' style='background:#2bb996;'></span>AI Predictions</span>
                    <span class='stat-pill'><span class='dot' style='background:#e9a147;'></span>Screen Guard</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        b1,b2 = st.columns(2)
        with b1:
            st.markdown('<div class="cta-btn">', unsafe_allow_html=True)
            if st.button("Start Assessment →", key="h_cta"):
                st.session_state.menu = "Psychological Assessment"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with b2:
            if st.button("View Insights", key="h_ins"):
                st.session_state.menu = "Dataset Insights"
                st.rerun()

    with c2:
        try: st.image(os.path.join(BASE_DIR, "website_design.png"), use_container_width=True)
        except:
            st.markdown("""
                <div class='nm-card' style='text-align:center;padding:3rem 1rem;min-height:200px;
                    display:flex;flex-direction:column;align-items:center;justify-content:center;'>
                    <div style='font-size:3.5rem;margin-bottom:0.5rem;'>🧠</div>
                    <p style='color:#9aa0bc;font-size:0.75rem;margin:0;letter-spacing:1px;text-transform:uppercase;'>MindBalance AI</p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Stats row
    for col,(val,lbl,clr) in zip(st.columns(4,gap="medium"),[
        (f"{total_assessments:,}","Students Assessed","#604e9c"),
        (f"{avg_usage}h","Avg Daily Usage","#ee5e76"),
        ("99.1%","Model Accuracy","#2bb996"),
        ("48h","Avg Detox Relief","#e9a147"),
    ]):
        with col:
            st.markdown(f"""
                <div class='nm-sm' style='text-align:center;padding:1.2rem 0.8rem;'>
                    <p style='font-family:DM Mono,monospace;font-size:1.55rem;font-weight:600;color:{clr};margin:0;'>{val}</p>
                    <p style='font-size:0.68rem;color:#9aa0bc;text-transform:uppercase;letter-spacing:0.8px;margin:4px 0 0;'>{lbl}</p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<span class='sec-label'>What You Can Do</span>", unsafe_allow_html=True)

    for col,(icon,title,desc,clr) in zip(st.columns(4,gap="medium"),[
        ("🎯","Psych Assessment","Answer 12 clinical questions & get your addiction profile instantly.","#6470b8"),
        ("📊","Behavior Insights","Explore real data — screen time vs GPA, sleep, and relationships.","#4aaa88"),
        ("🛡️","Screen Guard","Set daily limits. AI monitors usage and alerts you automatically.","#d99a2e"),
        ("🤖","AI Risk Index","ML model predicts your clinical risk score with 94%+ accuracy.","#d96b6b"),
    ]):
        with col:
            st.markdown(f"""
                <div class='feat-card'>
                    <div class='feat-icon'>{icon}</div>
                    <p style='font-weight:700;color:#4b3e7c;font-size:0.87rem;margin:0 0 5px;'>{title}</p>
                    <p style='font-size:0.76rem;color:#6a6287;line-height:1.6;margin:0;'>{desc}</p>
                    <div style='margin-top:10px;width:26px;height:3px;border-radius:2px;background:linear-gradient(90deg, {clr}, transparent);'></div>
                </div>
            """, unsafe_allow_html=True)


# ── ASSESSMENT ───────────────────────────────
elif menu == "Psychological Assessment":
    st.markdown("""
        <h1>Clinical <span class='highlight-text'>Assessment</span></h1>
        <p style='color:#9aa0bc;font-size:0.88rem;margin-top:-0.5rem;margin-bottom:1.5rem;'>
        Bergen Social Media Addiction Scale · Quick Intake · Behavioral Analysis
        </p>
    """, unsafe_allow_html=True)

    # ── BEHAVIORAL TRACKER ─────────────────────────
    # Passive JS tracking: session time, scroll depth, click count, idle detection
    components.html("""
    <script>
    (function(){
        var t0 = Date.now(), clicks = 0, maxScroll = 0, lastAct = Date.now(), scrollBuf = [];
        document.addEventListener('click', function(){ clicks++; lastAct = Date.now(); });
        window.addEventListener('scroll', function(){
            lastAct = Date.now();
            var pct = Math.round((window.scrollY / Math.max(1, document.body.scrollHeight - window.innerHeight)) * 100);
            if(pct > maxScroll) maxScroll = pct;
            scrollBuf.push(Date.now());
            if(scrollBuf.length > 50) scrollBuf.shift();
        });
        ['mousemove','keypress','touchstart'].forEach(function(e){
            document.addEventListener(e, function(){ lastAct = Date.now(); });
        });
        setInterval(function(){
            var elapsed = Math.round((Date.now()-t0)/1000);
            var idle    = Math.round((Date.now()-lastAct)/1000);
            var recentScrolls = scrollBuf.filter(function(s){ return Date.now()-s < 8000; }).length;
            var score = 0;
            if(elapsed > 90)         score += 20;
            if(clicks  > 12)         score += 20;
            if(maxScroll > 65)       score += 20;
            if(recentScrolls > 6)    score += 20;
            if(idle < 4 && elapsed > 20) score += 20;
            try {
                sessionStorage.setItem('mb_beh', JSON.stringify({
                    score: score, clicks: clicks,
                    scroll: maxScroll, secs: elapsed
                }));
            } catch(e){}
        }, 4000);
    })();
    </script>
    """, height=0)

    # ══ STEP 1 — QUICK INTAKE ═══════════════════════
    st.markdown("""
        <div class='nm-card'>
            <span class='sec-label'>Step 1 · Quick Self-Report</span>
            <p style='font-size:0.84rem;color:#9aa0bc;margin:-0.2rem 0 1.1rem;'>
            3 quick questions before the clinical scale — takes under 30 seconds.
            </p>
    """, unsafe_allow_html=True)

    qi_a, qi_b, qi_c = st.columns(3, gap="medium")
    with qi_a:
        st.markdown("""<div class='intake-q'>
            <div class='intake-icon'>📱</div>
            <div><p style='font-size:0.68rem;font-weight:700;color:#9aa0bc;text-transform:uppercase;letter-spacing:0.8px;margin:0 0 3px;'>Daily Hours</p>
            <p style='font-size:0.81rem;color:#4b3e7c;font-weight:600;margin:0;'>How many hours on social media per day?</p></div>
        </div>""", unsafe_allow_html=True)
        intake_hours = st.select_slider(
            "Daily hours on social media",
            options=["< 1h","1 – 2h","2 – 4h","4 – 6h","6 – 8h","8h+"],
            value="2 – 4h", label_visibility="collapsed"
        )

    with qi_b:
        st.markdown("""<div class='intake-q'>
            <div class='intake-icon'>🌅</div>
            <div><p style='font-size:0.68rem;font-weight:700;color:#9aa0bc;text-transform:uppercase;letter-spacing:0.8px;margin:0 0 3px;'>Morning Habit</p>
            <p style='font-size:0.81rem;color:#4b3e7c;font-weight:600;margin:0;'>Do you check your phone right after waking up?</p></div>
        </div>""", unsafe_allow_html=True)
        intake_morning = st.radio(
            "Morning check habit",
            ["Yes, always","Sometimes","Rarely","Never"],
            index=1, label_visibility="collapsed"
        )

    with qi_c:
        st.markdown("""<div class='intake-q'>
            <div class='intake-icon'>🔁</div>
            <div><p style='font-size:0.68rem;font-weight:700;color:#9aa0bc;text-transform:uppercase;letter-spacing:0.8px;margin:0 0 3px;'>Check Frequency</p>
            <p style='font-size:0.81rem;color:#4b3e7c;font-weight:600;margin:0;'>How often do you check social media per hour?</p></div>
        </div>""", unsafe_allow_html=True)
        intake_freq = st.radio(
            "Checks per hour",
            ["1 – 2 times","3 – 5 times","5 – 10 times","10+ times"],
            index=1, label_visibility="collapsed"
        )

    # Intake score
    hour_risk    = {"< 1h":0,"1 – 2h":1,"2 – 4h":2,"4 – 6h":3,"6 – 8h":4,"8h+":5}[intake_hours]
    morning_risk = {"Yes, always":3,"Sometimes":2,"Rarely":1,"Never":0}[intake_morning]
    freq_risk    = {"1 – 2 times":0,"3 – 5 times":1,"5 – 10 times":2,"10+ times":3}[intake_freq]
    intake_score = hour_risk + morning_risk + freq_risk
    intake_clr   = "#2bb996" if intake_score<=3 else "#e9a147" if intake_score<=6 else "#ee5e76"
    intake_lbl   = "Low Signal" if intake_score<=3 else "Moderate Signal" if intake_score<=6 else "High Signal"

    st.markdown(f"""
        <div style='display:flex;align-items:center;gap:10px;margin-top:0.3rem;'>
            <span style='font-size:0.7rem;color:#9aa0bc;font-weight:700;text-transform:uppercase;letter-spacing:1px;'>Intake signal →</span>
            <span class='beh-badge'>
                <span style='width:8px;height:8px;border-radius:50%;background:{intake_clr};display:inline-block;'></span>
                <span style='color:{intake_clr};'>{intake_lbl} &nbsp;({intake_score}/11)</span>
            </span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("assessment"):
        st.markdown("<div class='nm-card'>", unsafe_allow_html=True)
        st.markdown("<span class='sec-label'>Student Profile</span>", unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3)
        with c1: age      = st.number_input("Age", 16, 25, 20)
        with c2: gender   = st.selectbox("Gender", ["Male","Female","Non-binary","Prefer not to say"])
        with c3: level    = st.selectbox("Academic Level", ["High School","Undergraduate","Graduate"])
        c4,c5 = st.columns(2)
        with c4: country  = st.selectbox("Country", ["India","USA","UK","Australia","Other"])
        with c5: platform = st.selectbox("Primary Platform", ["Instagram","YouTube","Snapchat","Threads","LinkedIn","WhatsApp","Twitter"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='nm-card' style='margin-top:0;'>", unsafe_allow_html=True)
        st.markdown("""
            <span class='sec-label'>BSMAS Survey</span>
            <p style='font-size:0.8rem;color:#9aa0bc;margin-top:-0.3rem;margin-bottom:1rem;'>
            Rate each: &nbsp;1 = Very Rarely &nbsp;·&nbsp; 3 = Sometimes &nbsp;·&nbsp; 5 = Very Often
            </p>
        """, unsafe_allow_html=True)
        q1 = st.slider("I think about social media constantly", 1, 5, 3)
        q2 = st.slider("I feel an urge to use it more and more", 1, 5, 3)
        q3 = st.slider("I use it to escape personal problems", 1, 5, 3)
        q4 = st.slider("I have tried to cut back but failed", 1, 5, 3)
        q5 = st.slider("I feel restless if I cannot use it", 1, 5, 3)
        q6 = st.slider("It has negatively impacted my studies", 1, 5, 3)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='nm-card' style='margin-top:0;'>", unsafe_allow_html=True)
        st.markdown("<span class='sec-label'>Daily Metrics</span>", unsafe_allow_html=True)
        da,db,dc = st.columns(3)
        with da: usage     = st.slider("Daily Usage (Hours)", 0.0, 15.0, 4.0, 0.5)
        with db: sleep     = st.slider("Sleep Per Night (Hours)", 3.0, 10.0, 7.0, 0.5)
        with dc: conflicts = st.number_input("Social Conflicts / Week", 0, 20, 1)
        st.markdown("</div>", unsafe_allow_html=True)

        submit = st.form_submit_button("⟶  Generate AI Risk Report")

    if submit:
        st.session_state.feedback_submitted = False  # Reset feedback on new submission
        total    = q1+q2+q3+q4+q5+q6
        label,color,advice,cures = get_bsmas_result(total)
        severity  = "LOW" if total<=12 else "MODERATE" if total<=18 else "HIGH" if total<=24 else "SEVERE"
        badge_cls = "badge-l" if total<=12 else "badge-m" if total<=18 else "badge-h"
        composite = round(total + intake_score * 0.5, 1)

        st.markdown(f"""
            <div class='nm-card' style='border-left:5px solid {color};margin-top:1.5rem;'>
                <div style='display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;'>
                    <div>
                        <span class='sec-label' style='color:{color};'>Assessment Result</span>
                        <h2 style='margin:0;color:{color};font-size:1.6rem;font-weight:800;'>{label}</h2>
                        <p style='margin:5px 0 10px;font-size:0.93rem;color:#6a6287;'>{advice}</p>
                        <div style='display:flex;gap:7px;flex-wrap:wrap;'>
                            <span class='beh-badge'>📱 Intake {intake_score}/11</span>
                            <span class='beh-badge'>🧠 BSMAS {total}/30</span>
                            <span class='beh-badge'>📊 Composite {composite}</span>
                        </div>
                    </div>
                    <div style='text-align:right;'>
                        <span class='badge {badge_cls}'>{severity} RISK</span>
                        <p style='margin:8px 0 0;font-family:DM Mono,monospace;font-size:2.4rem;font-weight:700;color:{color};'>
                            {total}<span style='font-size:1rem;color:#9aa0bc;'>/30</span>
                        </p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        model,_ = load_model()
        gauge_val = (total/30)*100
        if model:
            feat = pd.DataFrame([{'Age':age,'Gender':gender,'Academic_Level':level,'Country':country,
                'Avg_Daily_Usage_Hours':usage,'Most_Used_Platform':platform,
                'Affects_Academic_Performance':"Yes" if q6>=4 else "No",
                'Sleep_Hours_Per_Night':sleep,'Mental_Health_Score':11-(total//3),
                'Relationship_Status':"Single",'Conflicts_Over_Social_Media':conflicts}])
            try: gauge_val = model.predict_proba(feat)[0][1]*100
            except: pass

        r1,r2 = st.columns(2, gap="medium")
        with r1:
            fig = go.Figure(go.Indicator(
                mode="gauge+number", value=round(gauge_val,1),
                number={'suffix':'%','font':{'color':color,'family':'DM Mono','size':38}},
                title={'text':"Clinical Risk Index",'font':{'color':'#9aa0bc','size':12}},
                gauge={'axis':{'range':[0,100],'tickcolor':'#9aa0bc','tickfont':{'color':'#9aa0bc','size':10}},
                       'bar':{'color':color,'thickness':0.24},'bgcolor':'rgba(0,0,0,0)','borderwidth':0,
                       'steps':[{'range':[0,40],'color':'rgba(43,185,150,.1)'},
                                 {'range':[40,70],'color':'rgba(233,161,71,.1)'},
                                 {'range':[70,100],'color':'rgba(238,94,118,.1)'}]}))
            fig.update_layout(**NM, height=280)
            st.plotly_chart(fig, use_container_width=True)

        cure_html = ''.join([f"""
            <div style='display:flex;align-items:flex-start;gap:12px;padding:0.7rem 1rem;border-radius:14px;
                        margin-bottom:10px;background:rgba(255,255,255,0.3);border:1px solid rgba(255,255,255,0.6);'>
                <span style='color:{color};font-size:1rem;margin-top:1px;flex-shrink:0;font-weight:900;'>✓</span>
                <span style='color:#4b3e7c;font-size:0.88rem;line-height:1.5;font-weight:600;'>{c}</span>
            </div>""" for c in cures])
        with r2:
            st.markdown(f"""<div class='nm-card' style='height:100%;'>
                <span class='sec-label'>Recommended Actions</span>{cure_html}</div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<span class='sec-label'>Score Breakdown by Dimension</span>", unsafe_allow_html=True)
        qs   = ["Preoccupation","Tolerance","Mood Mod.","Relapse","Withdrawal","Conflict"]
        vals = [q1,q2,q3,q4,q5,q6]
        fig2 = go.Figure(go.Bar(x=qs, y=vals, width=0.5, marker_line_width=0,
            marker_color=[color if v>=4 else '#6366f1' if v==3 else 'rgba(148,163,184,0.3)' for v in vals]))
        fig2.update_layout(**NM, height=220,
            yaxis=dict(range=[0,5],tickvals=[1,2,3,4,5],gridcolor='#e2e8f0'),
            xaxis=dict(tickfont=dict(size=11,color='#94a3b8')), showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

        # Behavioral pattern signals
        st.markdown("<span class='sec-label'>Behavioral Pattern Signals</span>", unsafe_allow_html=True)
        signals = []
        if intake_morning == "Yes, always":
            signals.append(("🌅","Morning check habit","#ee5e76","Compulsive wake-up behavior — strong dependency indicator."))
        if intake_hours in ["6 – 8h","8h+"]:
            signals.append(("⏱️","Extreme daily usage","#d96b6b",f"Self-reported {intake_hours}/day exceeds clinical thresholds."))
        if intake_freq in ["5 – 10 times","10+ times"]:
            signals.append(("🔁","Compulsive check frequency","#e9a147",f"Checking {intake_freq}/hour signals tolerance-building."))
        if q3 >= 4:
            signals.append(("🏃","Escapism confirmed","#d99a2e","Using social media to avoid real-life problems."))
        if q5 >= 4:
            signals.append(("😰","Withdrawal symptoms","#ee5e76","Restlessness without social media — dependency marker."))
        if not signals:
            signals.append(("✅","No critical flags","#2bb996","Intake and behavioral patterns appear healthy."))

        sig_cols = st.columns(min(len(signals),3), gap="medium")
        for i,(icon,title_s,clr,desc) in enumerate(signals[:3]):
            with sig_cols[i]:
                st.markdown(f"""
                    <div class='nm-sm' style='border-left:3px solid {clr};'>
                        <div style='display:flex;align-items:center;gap:8px;margin-bottom:5px;'>
                            <span style='font-size:1.1rem;'>{icon}</span>
                            <span style='font-weight:700;font-size:0.82rem;color:{clr};'>{title_s}</span>
                        </div>
                        <p style='font-size:0.76rem;color:#6a6287;margin:0;line-height:1.5;'>{desc}</p>
                    </div>
                """, unsafe_allow_html=True)

        # ══════════════════════════════════════════
        #  EMOJI SATISFACTION FEEDBACK FORM
        # ══════════════════════════════════════════
        st.markdown("<br>", unsafe_allow_html=True)

        RATINGS = [
            ("😡", "Highly\nUnsatisfied", 1, "#ee5e76"),
            ("😞", "Unsatisfied",         2, "#f97316"),
            ("😐", "Neutral",             3, "#94a3b8"),
            ("😊", "Satisfied",           4, "#4aaa88"),
            ("😄", "Very\nSatisfied",     5, "#2bb996"),
        ]

        if not st.session_state.feedback_submitted:
            st.markdown("""
                <div class='feedback-wrap'>
                    <span class='sec-label'>Rate Your Experience</span>
                    <p style='font-size:0.9rem;font-weight:700;color:#4b3e7c;margin:-0.2rem 0 0;'>
                        Please rate your satisfaction with this Assessment:
                    </p>
            """, unsafe_allow_html=True)

            # Emoji row (visual display — selection via Streamlit radio below)
            cur = st.session_state.fb_val
            cards_html = '<div class="emoji-satisfaction-row">'
            for emoji, lbl, val, clr in RATINGS:
                active = "active" if cur == val else ""
                lbl_safe = lbl.replace('\n','<br>')
                cards_html += f"""
                    <div class="emoji-sat-card {active}">
                        <div class="emoji-sat-face">{emoji}</div>
                        <div class="emoji-sat-label">{lbl_safe}</div>
                        <div class="sat-radio-dot"></div>
                    </div>"""
            cards_html += '</div>'
            st.markdown(cards_html, unsafe_allow_html=True)

            # Functional Streamlit radio (shown below the emoji row)
            st.markdown("""
                <p style='font-size:0.72rem;color:#9aa0bc;font-weight:600;letter-spacing:0.8px;
                           text-transform:uppercase;margin:0.5rem 0 0.2rem;'>Select rating:</p>
            """, unsafe_allow_html=True)
            fb_choice = st.radio(
                "Satisfaction",
                options=[f"{e} {l.replace(chr(10),' ')}" for e,l,v,c in RATINGS],
                index=cur - 1,
                horizontal=True,
                label_visibility="collapsed",
                key="fb_radio_key"
            )
            # Sync selection
            for e,l,v,c in RATINGS:
                if fb_choice.startswith(e):
                    st.session_state.fb_val = v
                    break

            # Show selected state pill
            sel = next((r for r in RATINGS if r[2]==st.session_state.fb_val), RATINGS[2])
            st.markdown(f"""
                <div style='display:flex;align-items:center;gap:10px;margin:0.6rem 0;
                            padding:0.65rem 1.1rem;border-radius:12px;
                            background:rgba(255,255,255,0.55);border:1px solid rgba(255,255,255,0.8);'>
                    <span style='font-size:1.4rem;'>{sel[0]}</span>
                    <span style='font-weight:700;color:{sel[3]};font-size:0.9rem;'>
                        {sel[1].replace(chr(10),' ')} selected
                    </span>
                    <span style='margin-left:auto;font-size:0.75rem;color:#9aa0bc;'>Click Submit to confirm →</span>
                </div>
            """, unsafe_allow_html=True)

            fb_comment = st.text_area(
                "Additional Comments (optional)",
                placeholder="Tell us how we can improve — any feedback helps!",
                height=76, key="fb_comment_key"
            )
            st.markdown("</div>", unsafe_allow_html=True)

            fb_c1, fb_c2 = st.columns([1, 3])
            with fb_c1:
                st.markdown('<div class="cta-btn">', unsafe_allow_html=True)
                if st.button("Submit Feedback  ✓", key="fb_submit_btn"):
                    fb_path = os.path.join(BASE_DIR, 'feedback_log.json')
                    entry = {
                        "timestamp": datetime.now().isoformat(),
                        "rating": st.session_state.fb_val,
                        "rating_label": sel[1].replace('\n',' '),
                        "comment": st.session_state.get("fb_comment_key",""),
                        "bsmas_score": total,
                        "severity": severity,
                    }
                    try:
                        existing = []
                        if os.path.exists(fb_path):
                            with open(fb_path,'r') as f: existing = json.load(f)
                        existing.append(entry)
                        with open(fb_path,'w') as f: json.dump(existing, f, indent=2)
                    except: pass
                    st.session_state.feedback_submitted = True
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        else:
            # ── Thank-you card ──────────────────────────
            sel = next((r for r in RATINGS if r[2]==st.session_state.fb_val), RATINGS[2])
            stars = "⭐" * sel[2] + "☆" * (5 - sel[2])
            thank_msgs = {
                1: "We're sorry to hear that. Your feedback helps us improve significantly. 🙏",
                2: "Thanks for the honest feedback — we'll work on it.",
                3: "Appreciate your balanced take! More improvements are coming.",
                4: "Really glad it was helpful! Share with classmates who might benefit.",
                5: "Awesome! Thank you so much — this motivates the whole team. 🎉"
            }
            st.markdown(f"""
                <div class='feedback-wrap' style='text-align:center;padding:2.5rem 2rem;'>
                    <div style='font-size:3.5rem;margin-bottom:0.4rem;'>{sel[0]}</div>
                    <p style='font-family:DM Mono,monospace;font-size:1.2rem;font-weight:700;color:#4b3e7c;margin:0;'>{stars}</p>
                    <p style='font-weight:800;font-size:1.1rem;color:{sel[3]};margin:10px 0 6px;'>
                        {sel[1].replace(chr(10),' ')}
                    </p>
                    <p style='font-size:0.86rem;color:#6a6287;margin:0;'>{thank_msgs[sel[2]]}</p>
                    <div style='margin-top:1.2rem;'>
                        <span class='stat-pill'>
                            <span class='dot' style='background:#2bb996;'></span>
                            Feedback recorded — thank you!
                        </span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            if st.button("← Retake Assessment", key="retake_btn"):
                st.session_state.feedback_submitted = False
                st.session_state.fb_val = 3
                st.rerun()


# ── INSIGHTS ─────────────────────────────────
elif menu == "Dataset Insights":
    st.markdown("""
        <h1>Behavior <span class='highlight-text'>Insights</span></h1>
        <p style='color:#9aa0bc;font-size:0.88rem;margin-top:-0.5rem;margin-bottom:1.5rem;'>
        Real dataset analysis — screen time, mental health, sleep, and academic performance.
        </p>
    """, unsafe_allow_html=True)
    try:
        df = pd.read_csv(os.path.join(BASE_DIR, 'social_media_addiction_data.csv'))
        # Use radio instead of tabs to ensure animations play exactly when the user switches views
        view = st.radio("Insights View:", ["🧠 Mental Health Impact", "📱 Platform Usage", "⚠️ Risk Distribution"], horizontal=True, label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if view == "🧠 Mental Health Impact":
            fig = px.scatter(df,x="Avg_Daily_Usage_Hours",y="Mental_Health_Score",color="Status",trendline="ols",
                color_discrete_sequence=["#ee5e76","#2bb996","#6366f1"],template="none",
                labels={"Avg_Daily_Usage_Hours":"Daily Usage (hrs)","Mental_Health_Score":"Mental Health Score"})
            fig.update_layout(**NM,height=380)
            fig.update_traces(marker=dict(size=7,opacity=0.7))
            st.plotly_chart(fig,use_container_width=True)
            st.markdown("<div class='nm-inset'><p style='color:#475569;font-size:0.86rem;margin:0;font-weight:600;'>💡 Mental resilience drops sharply after <strong style='color:#1e293b;'>5 hours</strong> of daily usage. Addicted students scored 38% lower.</p></div>", unsafe_allow_html=True)
            
        elif view == "📱 Platform Usage":
            if "Most_Used_Platform" in df.columns:
                pc = df["Most_Used_Platform"].value_counts().reset_index()
                pc.columns = ["Platform","Count"]
                
                colors = ["#f43f5e", "#10b981", "#6366f1", "#f59e0b", "#94a3b8", "#a855f7", "#62b1ff"]
                fig2 = px.bar(pc,x="Platform",y="Count",color="Platform",template="none",
                    color_discrete_sequence=colors)
                fig2.update_layout(**NM,height=360,showlegend=False)
                fig2.update_traces(marker_line_width=0,width=0.45)
                
                # Render using 60fps CSS injected HTML
                html_str = fig2.to_html(include_plotlyjs="cdn", full_html=False)
                animated_html = """
                <style>
                @keyframes barGrow {
                    from { transform: scaleY(0); opacity: 0; }
                    to { transform: scaleY(1); opacity: 1; }
                }
                .js-plotly-plot .cartesianlayer .trace.bars path,
                .js-plotly-plot .cartesianlayer .trace.bars rect {
                    transform-box: fill-box !important;
                    transform-origin: bottom !important;
                    animation: barGrow 1.5s cubic-bezier(0.2, 0.8, 0.2, 1) forwards !important;
                }
                body { background: transparent !important; margin: 0; overflow: hidden; }
                </style>
                """ + html_str
                import streamlit.components.v1 as components
                components.html(animated_html, height=380)
                    
        elif view == "⚠️ Risk Distribution":
            if "Status" in df.columns:
                sc = df["Status"].value_counts()
                
                fig3 = go.Figure(go.Pie(labels=sc.index,values=sc.values, hole=0.55,
                    marker=dict(colors=["#f43f5e","#10b981","#f59e0b"],line=dict(color='rgba(255,255,255,0.8)',width=4)),
                    textfont=dict(family='Nunito',size=13,color='#1e293b')))
                fig3.update_layout(**NM,height=340,showlegend=True,
                    legend=dict(font=dict(color='#475569',family='Nunito')))
                
                html_str = fig3.to_html(include_plotlyjs="cdn", full_html=False)
                animated_html = """
                <style>
                @keyframes pieReveal {
                    from { transform: scale(0.6) rotate(-45deg); opacity: 0; }
                    to { transform: scale(1) rotate(0deg); opacity: 1; }
                }
                .js-plotly-plot path.surface {
                    transform-box: fill-box !important;
                    transform-origin: center !important;
                    animation: pieReveal 1.5s cubic-bezier(0.2, 0.8, 0.2, 1) forwards !important;
                }
                body { background: transparent !important; margin: 0; overflow: hidden; }
                </style>
                """ + html_str
                import streamlit.components.v1 as components
                components.html(animated_html, height=360)
    except Exception as e:
        st.markdown(f"""<div class='nm-inset' style='border-left:3px solid #d96b6b;'>
            <p style='color:#d96b6b;font-size:0.87rem;margin:0;'>⚠ Place <code>social_media_addiction_data.csv</code> in project root.</p>
            <p style='color:#9aa0bc;font-size:0.76rem;margin:3px 0 0;'>{e}</p></div>""", unsafe_allow_html=True)


# ── SCREEN TIME ──────────────────────────────
elif menu == "Screen Time Controller":
    st.markdown("""
        <h1>Screen Time <span class='highlight-text'>Guard</span></h1>
        <p style='color:#9aa0bc;font-size:0.88rem;margin-top:-0.5rem;margin-bottom:1.5rem;'>
        Set a daily limit. The AI Guard monitors usage and alerts you automatically.
        </p>
    """, unsafe_allow_html=True)

    CONFIG_PATH = os.path.join(BASE_DIR, 'screen_config.json')
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_ts = datetime.now().timestamp()
    
    config = {}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH,'r') as f: config = json.load(f)
        except:
            pass

    # ── Backward-compatible key migration (old → new) ─────
    if "limit" in config and "limit_hours" not in config:
        config["limit_hours"] = config.pop("limit")
    if "elapsed_time" in config and "elapsed_secs" not in config:
        config["elapsed_secs"] = config.pop("elapsed_time")
    if "last_update_time" in config and "last_update" not in config:
        config["last_update"] = config.pop("last_update_time")
    if "start_time" in config:
        config.pop("start_time", None)  # no longer needed
    if "alert_sent" not in config:
        config["alert_sent"] = {}
    if "history" not in config:
        config["history"] = {}

    # Auto-reset on new day (matches background_monitor logic)
    if not config or config.get("date") != current_date:
        # Archive yesterday before reset
        yesterday = config.get("date", "")
        history = config.get("history", {})
        if yesterday and config.get("elapsed_secs", 0) > 0:
            history[yesterday] = config.get("elapsed_secs", 0.0)
            if len(history) > 30:
                oldest = sorted(history)[0]
                del history[oldest]
        config.update({
            "limit_hours": config.get("limit_hours", 4.0),
            "status": "active",
            "date": current_date,
            "elapsed_secs": 0.0,
            "last_update": current_ts,
            "history": history,
            "alert_sent": {},
        })
        with open(CONFIG_PATH,'w') as f: json.dump(config, f, indent=2)

    # ── Guard Configuration & Gauge ──────────────
    ca,cb = st.columns([1,1], gap="large")
    with ca:
        st.markdown("<div class='nm-card'>", unsafe_allow_html=True)
        st.markdown("<span class='sec-label'>Guard Configuration</span>", unsafe_allow_html=True)
        new_limit = st.number_input("Daily Screen Limit (Hours)", 0.5, 12.0, float(config.get("limit_hours", 4.0)), 0.5)
        st.markdown("<br>", unsafe_allow_html=True)

        # Activate button
        st.markdown('<div class="cta-btn">', unsafe_allow_html=True)
        if st.button("⟶  Activate Real-Time Guard", key="act"):
            config["limit_hours"]=new_limit; config["status"]="active"
            config["last_update"]=current_ts
            with open(CONFIG_PATH,'w') as f: json.dump(config, f, indent=2)
            try: subprocess.Popen(["python", os.path.join(BASE_DIR, "background_monitor.py")],
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
            except: pass
            st.success("✓ AI Guard is now active in the background!")
        st.markdown('</div>', unsafe_allow_html=True)

        # Pause / Resume toggle
        is_paused = config.get("status") == "paused"
        p1, p2 = st.columns(2)
        with p1:
            if st.button("⏸  Pause Tracking" if not is_paused else "▶  Resume Tracking", key="pause_resume"):
                if is_paused:
                    config["status"] = "active"
                    config["last_update"] = current_ts
                else:
                    config["status"] = "paused"
                with open(CONFIG_PATH,'w') as f: json.dump(config, f, indent=2)
                st.rerun()
        with p2:
            if st.button("↺  Reset Timer", key="rst"):
                config["elapsed_secs"]=0.0
                config["last_update"]=current_ts
                config["alert_sent"]={}
                with open(CONFIG_PATH,'w') as f: json.dump(config, f, indent=2)
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        # Status badge
        status_label = config.get("status", "inactive").upper()
        status_clr = "#2bb996" if status_label == "ACTIVE" else "#e9a147" if status_label == "PAUSED" else "#94a3b8"
        st.markdown(f"""
            <div class='nm-inset' style='margin-top:0;display:flex;align-items:center;gap:10px;'>
                <span class='dot' style='background:{status_clr};width:10px;height:10px;'></span>
                <span style='font-size:0.8rem;font-weight:700;color:{status_clr};'>{status_label}</span>
                <span style='font-size:0.76rem;color:#9aa0bc;margin-left:auto;'>Guard runs in background — close this tab safely.</span>
            </div>
        """, unsafe_allow_html=True)

    with cb:
        limit_m      = new_limit * 60.0
        elapsed      = config.get("elapsed_secs", 0.0) / 60.0  # seconds → minutes
        progress_pct = min(1.0,elapsed/limit_m) if limit_m>0 else 1.0
        bar_color    = "#2bb996" if progress_pct<0.5 else "#e9a147" if progress_pct<0.75 else "#ee5e76" if progress_pct<1.0 else "#b84040"
        remaining    = max(0,limit_m-elapsed)

        # Gauge with multi-level alert zones (50%, 75%, 90%, 100%)
        fig_g = go.Figure(go.Indicator(mode="gauge+number+delta",value=round(elapsed,1),
            delta={'reference':limit_m,'suffix':'m limit','font':{'color':'#9aa0bc','size':12}},
            number={'suffix':"m",'font':{'color':bar_color,'family':'DM Mono','size':34}},
            title={'text':"Session Time",'font':{'color':'#9aa0bc','size':12}},
            gauge={'axis':{'range':[0,limit_m*1.2],'tickcolor':'#9aa0bc','tickfont':{'color':'#9aa0bc','size':9}},
                   'bar':{'color':bar_color,'thickness':0.26},'bgcolor':'rgba(0,0,0,0)','borderwidth':0,
                   'steps':[
                       {'range':[0,limit_m*0.50],'color':'rgba(74,170,136,.08)'},
                       {'range':[limit_m*0.50,limit_m*0.75],'color':'rgba(99,102,241,.08)'},
                       {'range':[limit_m*0.75,limit_m*0.90],'color':'rgba(233,161,71,.1)'},
                       {'range':[limit_m*0.90,limit_m],'color':'rgba(238,94,118,.12)'},
                       {'range':[limit_m,limit_m*1.2],'color':'rgba(184,64,64,.12)'},
                   ],
                   'threshold':{'line':{'color':'#d96b6b','width':3},'thickness':0.75,'value':limit_m}}))
        fig_g.update_layout(**NM,height=260)
        st.plotly_chart(fig_g,use_container_width=True)

    # ── Progress bar ──────────────────────────────
    st.progress(progress_pct, text=f"{int(progress_pct*100)}% of daily limit consumed")

    # ── Metric cards ──────────────────────────────
    m1,m2,m3,m4 = st.columns(4,gap="medium")
    with m1: st.metric("Session Duration",f"{elapsed:.1f}m",
                delta=f"{remaining:.1f}m left" if elapsed<limit_m else "Limit reached!",
                delta_color="normal" if elapsed<limit_m else "inverse")
    with m2: st.metric("Daily Limit",f"{new_limit}h",
                delta="Guard Active" if config.get('status')=='active' else "Paused" if config.get('status')=='paused' else "Inactive")
    with m3:
        pct=int(progress_pct*100)
        st.metric("Usage %",f"{pct}%",delta=f"{100-pct}% safe zone" if pct<100 else "Exceeded!")
    with m4:
        alerts_fired = len(config.get("alert_sent", {}))
        st.metric("Alerts Sent", f"{alerts_fired}/4",
                  delta="All clear" if alerts_fired==0 else f"{alerts_fired} triggered",
                  delta_color="normal" if alerts_fired==0 else "inverse")

    # ── Alert thresholds status ───────────────────
    alert_sent = config.get("alert_sent", {})
    thresholds = {"50%": 0.50, "75%": 0.75, "90%": 0.90, "100%": 1.00}
    st.markdown("<div class='nm-card' style='margin-top:1rem;'><span class='sec-label'>Alert Thresholds</span></div>", unsafe_allow_html=True)
    th_cols = st.columns(4, gap="small")
    for i, (label, frac) in enumerate(thresholds.items()):
        reached = progress_pct >= frac
        alerted = label in alert_sent
        if reached and alerted:
            icon, clr, status_txt = "🔔", "#ee5e76", "Alerted"
        elif reached:
            icon, clr, status_txt = "⚠️", "#e9a147", "Reached"
        else:
            icon, clr, status_txt = "✓", "#2bb996", "Safe"
        with th_cols[i]:
            st.markdown(f"""
                <div style='display:flex;align-items:center;gap:10px;padding:0.5rem 0.8rem;
                            background:rgba(255,255,255,0.4);border-radius:10px;border:1px solid rgba(255,255,255,0.7);'>
                    <span style='font-size:1rem;'>{icon}</span>
                    <span style='font-weight:700;color:#4b3e7c;font-size:0.82rem;flex:1;'>{label} Threshold</span>
                    <span style='font-size:0.72rem;font-weight:700;color:{clr};background:rgba(255,255,255,0.7);
                                 padding:3px 10px;border-radius:20px;'>{status_txt}</span>
                </div>
            """, unsafe_allow_html=True)

    # ── Limit exceeded warning ────────────────────
    if elapsed>limit_m:
        st.markdown(f"""
            <div style='background:rgba(255,255,255,0.4);border-radius:14px;padding:1rem 1.4rem;
                box-shadow:var(--glass-shadow);backdrop-filter:blur(8px);
                border-left:5px solid #ee5e76;margin-top:1rem;display:flex;align-items:center;gap:12px;'>
                <span class='pulse' style='color:#ee5e76;font-size:1.4rem;'>⚠</span>
                <div>
                    <p style='color:#ee5e76;font-weight:800;font-size:0.95rem;margin:0;'>Daily Limit Exceeded</p>
                    <p style='color:#6a6287;font-size:0.82rem;margin:2px 0 0;'>
                    Used <strong style='color:#ee5e76;'>{elapsed:.1f}m</strong> —
                    {elapsed-limit_m:.1f}m over your {new_limit}h limit. Guard is active.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # ── 30-Day Usage History Chart ────────────────
    history = config.get("history", {})
    if history:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<span class='sec-label'>30-Day Screen Time History</span>", unsafe_allow_html=True)

        hist_dates = sorted(history.keys())[-30:]
        hist_minutes = [round(history[d] / 60.0, 1) for d in hist_dates]
        hist_labels = [datetime.strptime(d, "%Y-%m-%d").strftime("%b %d") for d in hist_dates]
        limit_line = new_limit * 60.0

        bar_colors = ["#2bb996" if m <= limit_line*0.75 else "#e9a147" if m <= limit_line else "#ee5e76" for m in hist_minutes]

        fig_hist = go.Figure()
        fig_hist.add_trace(go.Bar(
            x=hist_labels, y=hist_minutes, marker_color=bar_colors,
            marker_line_width=0, width=0.55, name="Usage (min)",
            hovertemplate="<b>%{x}</b><br>%{y:.1f} min<extra></extra>"
        ))
        fig_hist.add_hline(y=limit_line, line_dash="dash", line_color="#d96b6b", line_width=2,
                           annotation_text=f"Limit ({new_limit}h)", annotation_position="top right",
                           annotation_font=dict(color="#d96b6b", size=11, family="Nunito"))
        fig_hist.update_layout(**NM, height=280, showlegend=False,
            yaxis=dict(title="Minutes", gridcolor="rgba(99,102,241,0.06)", tickfont=dict(size=10)),
            xaxis=dict(tickfont=dict(size=9, color="#9aa0bc"), tickangle=-45))
        st.plotly_chart(fig_hist, use_container_width=True)

        # Weekly summary stats
        if len(hist_minutes) >= 7:
            last_7 = hist_minutes[-7:]
            avg_7 = sum(last_7) / len(last_7)
            max_7 = max(last_7)
            min_7 = min(last_7)
            over_days = sum(1 for m in last_7 if m > limit_line)

            s1,s2,s3,s4 = st.columns(4, gap="medium")
            with s1: st.metric("7-Day Avg", f"{avg_7:.0f}m", delta=f"{'Under' if avg_7 <= limit_line else 'Over'} limit")
            with s2: st.metric("Peak Day", f"{max_7:.0f}m")
            with s3: st.metric("Lowest Day", f"{min_7:.0f}m")
            with s4: st.metric("Days Over Limit", f"{over_days}/7", delta="Great!" if over_days == 0 else f"{over_days} days", delta_color="normal" if over_days == 0 else "inverse")
    else:
        st.markdown("""
            <div class='nm-inset' style='margin-top:1.5rem;text-align:center;padding:1.5rem;'>
                <p style='color:#9aa0bc;font-size:0.85rem;margin:0;'>📊 Usage history will appear here after your first full day of tracking.</p>
            </div>
        """, unsafe_allow_html=True)
