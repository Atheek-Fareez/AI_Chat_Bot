# ============================================================
# IT CAREER GUIDANCE CHATBOT — ChatGPT-Style UI
# Paper: "From Confusion to Clarity: IT Undergraduates,
#         Industry Expectations, and the Role of Quality
#         Internships (2024–2026)"
# ============================================================
# SETUP:
#   pip install streamlit google-genai qrcode[pil] Pillow
#   streamlit run app.py
# ============================================================

import streamlit as st
from google import genai
import re
import socket
import qrcode
import io
import base64
import time
import os
from datetime import datetime

# ── PAGE CONFIG ──────────────────────────────────────────────
st.set_page_config(
    page_title="IT Career Guidance with Atheek Fareez",
    page_icon="🎓",
    layout="wide",
)

# ── GEMINI CLIENT ────────────────────────────────────────────
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# ── HELPERS ──────────────────────────────────────────────────
def get_local_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return socket.gethostbyname(socket.gethostname())

def make_qr_base64(url: str) -> str:
    qr = qrcode.QRCode(box_size=4, border=2,
                       error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#7c3aed", back_color="#f5f3ff")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

@st.cache_data(show_spinner=False)
def load_knowledge_base(filepath: str) -> str | None:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None

def build_system_prompt(paper_text: str) -> str:
    return f"""
SYSTEM ROLE:
You are a friendly AI mentor trained ONLY on the research paper:
"From Confusion to Clarity: IT Undergraduates, Industry Expectations,
and the Role of Quality Internships (2024–2026)"

Your job is to help IT students understand:
- Career paths in IT (AI, Software Engineering, Data Science, Cloud, Cybersecurity, etc.)
- Industry expectations for freshers and interns
- Skills required for each IT career track
- Why internships matter and how to get quality ones
- Career roadmaps and practical guidance
- Common challenges IT students face and how to overcome them

KNOWLEDGE BASE (use ONLY this):
{paper_text}

STRICT RULES:
1. Answer ONLY from the research paper above.
2. Do NOT use external knowledge or guess.
3. Do NOT invent facts, statistics, or advice not found in the paper.

RESPONSE FORMAT:
- If question is RELATED to the research give a clear, helpful answer.
  Use simple English. Use bullet points. Be warm and practical.
  Keep it concise.
- If question is OUTSIDE the research scope reply EXACTLY:
  "I'm sorry, I don't have information about that yet.
  But I will definitely let you know once I learn about it"

TONE: Friendly mentor. Encouraging. Clear. Student-focused.
""".strip()

def ask_gemini(system_prompt: str, conversation_history: list) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=conversation_history,
        config={"system_instruction": system_prompt},
    )
    return response.text


# ── SESSION STATE ─────────────────────────────────────────────
if "chat_history"   not in st.session_state: st.session_state.chat_history   = []
if "gemini_history" not in st.session_state: st.session_state.gemini_history = []
if "input_key"      not in st.session_state: st.session_state.input_key      = 0
if "error_msg"      not in st.session_state: st.session_state.error_msg      = None
if "thinking"       not in st.session_state: st.session_state.thinking       = False
if "session_start"  not in st.session_state: st.session_state.session_start  = datetime.now()
if "session_mins"   not in st.session_state: st.session_state.session_mins   = 30
if "session_active" not in st.session_state: st.session_state.session_active = True


# ══════════════════════════════════════════════════════════════
# CSS — clean, no overflow:hidden on html/body
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Oxanium:wght@600;700;800&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  /* ── background ── */
  .stApp {
    background-color: #f0f4ff;
    background-image:
      radial-gradient(circle, rgba(99,102,241,0.10) 1px, transparent 1px),
      radial-gradient(ellipse at 10% 40%, rgba(167,139,250,0.18) 0%, transparent 55%),
      radial-gradient(ellipse at 90% 15%, rgba(56,189,248,0.15) 0%, transparent 55%),
      radial-gradient(ellipse at 65% 85%, rgba(52,211,153,0.12) 0%, transparent 50%),
      linear-gradient(145deg, #eef2ff 0%, #f5f3ff 40%, #ecfdf5 70%, #eff6ff 100%);
    background-size: 28px 28px, auto, auto, auto, auto;
  }

  /* ── animated top bar ── */
  .stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #7c3aed, #06b6d4, #10b981, #f59e0b, #7c3aed);
    background-size: 300% 100%;
    animation: topbar 5s linear infinite;
    z-index: 9999;
  }
  @keyframes topbar {
    0%   { background-position: 0% 0%; }
    100% { background-position: 300% 0%; }
  }

  /* ── hide streamlit chrome ── */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding: 0 !important; max-width: 100% !important; }

  /* ── sidebar ── */
  [data-testid="stSidebar"] {
    background: rgba(255,255,255,0.92) !important;
    border-right: 1.5px solid rgba(124,58,237,0.12) !important;
    backdrop-filter: blur(12px);
  }
  [data-testid="stSidebar"] .block-container { padding: 1.5rem 1rem !important; }

  /* sidebar text */
  .sidebar-title {
    font-family: 'Oxanium', sans-serif; font-size: 1.1rem; font-weight: 800;
    background: linear-gradient(90deg,#7c3aed,#0891b2);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin-bottom: 0.2rem;
  }
  .sidebar-by  { font-size: 0.75rem; color:#0891b2; font-weight:600; margin-bottom:1.2rem; }
  .sidebar-desc{ font-size: 0.78rem; color:#475569; line-height:1.6; margin-bottom:1.2rem; }

  /* IT pills */
  .pill-wrap { display:flex; flex-direction:column; gap:6px; margin-bottom:1.2rem; }
  .s-pill { padding:5px 12px; border-radius:8px; font-size:0.73rem; font-weight:600; border:1.5px solid; }
  .s-pill.ai  { background:rgba(237,233,254,.9); border-color:rgba(124,58,237,.35); color:#6d28d9; }
  .s-pill.se  { background:rgba(219,234,254,.9); border-color:rgba(37,99,235,.35);  color:#1d4ed8; }
  .s-pill.ds  { background:rgba(209,250,229,.9); border-color:rgba(5,150,105,.35);  color:#047857; }
  .s-pill.cs  { background:rgba(254,243,199,.9); border-color:rgba(180,83,9,.35);   color:#b45309; }
  .s-pill.net { background:rgba(252,231,243,.9); border-color:rgba(190,24,93,.35);  color:#be185d; }
  .s-pill.im  { background:rgba(204,251,241,.9); border-color:rgba(15,118,110,.35); color:#0f766e; }
  .s-pill.ise { background:rgba(255,237,213,.9); border-color:rgba(194,65,12,.35);  color:#c2410c; }

  /* access card */
  .acc-card { background:rgba(237,233,254,.6); border:1.5px solid rgba(124,58,237,.2); border-radius:12px; padding:.8rem; margin-bottom:1rem; }
  .acc-title { font-size:.68rem; font-weight:700; color:#6d28d9; letter-spacing:.09em; text-transform:uppercase; margin-bottom:.5rem; }
  .acc-link  { display:block; padding:4px 10px; border-radius:7px; font-size:.76rem; font-weight:600; text-decoration:none !important; margin-bottom:4px; transition:all .18s; }
  .acc-link.local { background:rgba(237,233,254,.9); color:#6d28d9 !important; border:1px solid rgba(124,58,237,.25); }
  .acc-link.net   { background:rgba(224,242,254,.9); color:#0369a1 !important; border:1px solid rgba(8,145,178,.30); }
  .acc-link:hover { filter:brightness(.94); transform:translateX(2px); }

  /* timer */
  .timer-box { background:rgba(237,233,254,.85); border:1.5px solid rgba(124,58,237,.25); border-radius:12px; padding:.7rem .9rem; margin-bottom:.8rem; }
  .timer-label{ font-size:.67rem; font-weight:700; color:#6d28d9; letter-spacing:.09em; text-transform:uppercase; margin-bottom:4px; }
  .timer-val  { font-family:'Oxanium',sans-serif; font-size:1.4rem; font-weight:800; color:#7c3aed; line-height:1; }
  .timer-val.warn { color:#d97706; }
  .timer-val.expd { color:#dc2626; }
  .timer-sub  { font-size:.68rem; color:#94a3b8; margin-top:3px; }
  .expired-banner { background:rgba(254,226,226,.95); border:1.5px solid rgba(239,68,68,.4); border-radius:10px; padding:.7rem 1rem; color:#991b1b; font-size:.82rem; font-weight:600; text-align:center; margin-bottom:.8rem; }
  .sidebar-footer { font-size:.68rem; color:#94a3b8; text-align:center; margin-top:1.5rem; line-height:1.6; }
  .sidebar-footer strong { color:#7c3aed; }

  /* ══════════════════════════════════════════
     MAIN CHAT LAYOUT
     The key: use position:fixed for the input
     bar so it's ALWAYS at the bottom of the
     viewport regardless of content height.
     Give the chat area padding-bottom so the
     last message is never hidden behind it.
  ══════════════════════════════════════════ */

  /* chat header — fixed at top of content area */
  .chat-header {
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(240,244,255,0.96);
    backdrop-filter: blur(10px);
    border-bottom: 1.5px solid rgba(99,102,241,0.12);
    padding: 0.9rem 1rem 0.7rem;
    margin-bottom: 0.5rem;
  }
  .chat-header-title {
    font-family: 'Oxanium', sans-serif;
    font-size: 1.15rem; font-weight: 800;
    background: linear-gradient(90deg,#7c3aed,#0891b2,#059669);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  }
  .chat-header-sub { font-size:.74rem; color:#64748b; margin-top:2px; }

  /* ── THE KEY FIX: input bar truly fixed to viewport bottom ── */
  .pinned-input {
    position: fixed !important;
    bottom: 0 !important;
    /* offset left to account for the sidebar (~21rem wide) */
    left: 21rem !important;
    right: 0 !important;
    z-index: 9000 !important;
    background: rgba(240,244,255,0.98) !important;
    backdrop-filter: blur(16px) !important;
    border-top: 1.5px solid rgba(99,102,241,0.14) !important;
    padding: 0.65rem 2rem 0.9rem !important;
    box-shadow: 0 -4px 20px rgba(99,102,241,0.08) !important;
  }
  .pinned-input-inner {
    max-width: 780px;
    margin: 0 auto;
  }

  /* give the whole page enough bottom padding so the last
     message is never covered by the pinned input bar */
  .main-content-pad {
    padding-bottom: 130px;
    max-width: 780px;
    margin: 0 auto;
    padding-left: 1rem;
    padding-right: 1rem;
  }

  /* ── chat bubbles ── */
  .msg-row { display:flex; gap:10px; align-items:flex-start; animation:fadein .3s ease; margin-bottom:.6rem; }
  @keyframes fadein { from{opacity:0;transform:translateY(5px)} to{opacity:1;transform:translateY(0)} }
  .msg-row.user { flex-direction:row-reverse; }
  .msg-row.bot  { flex-direction:row; }

  .avatar { width:34px; height:34px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:1rem; flex-shrink:0; font-weight:700; }
  .avatar.user-av { background:linear-gradient(135deg,#7c3aed,#0891b2); color:#fff; }
  .avatar.bot-av  { background:linear-gradient(135deg,#ecfdf5,#d1fae5); color:#047857; border:1.5px solid rgba(5,150,105,.25); }
  .msg-name { font-size:.65rem; font-weight:600; color:#94a3b8; text-align:center; margin-top:3px; }

  .bubble { max-width:78%; padding:.75rem 1.1rem; border-radius:18px; font-size:.91rem; line-height:1.65; white-space:pre-wrap; }
  .bubble.user-bubble { background:linear-gradient(135deg,#7c3aed,#0891b2); color:#fff; border-radius:18px 4px 18px 18px; box-shadow:0 2px 12px rgba(124,58,237,.25); }
  .bubble.bot-bubble  { background:rgba(255,255,255,.92); color:#1e293b; border:1.5px solid rgba(99,102,241,.15); border-radius:4px 18px 18px 18px; box-shadow:0 2px 10px rgba(0,0,0,.06); }
  .bubble.bot-bubble p  { margin:0 0 .3rem 0; }
  .bubble.bot-bubble ul,
  .bubble.bot-bubble ol { margin:.1rem 0 .3rem 1.1rem; padding:0; }
  .bubble.bot-bubble li { margin-bottom:.1rem; }

  /* welcome card */
  .welcome-card { background:rgba(255,255,255,.82); border:1.5px solid rgba(124,58,237,.18); border-top:3px solid rgba(124,58,237,.5); border-radius:20px; padding:2rem; text-align:center; margin:1.5rem 0; box-shadow:0 4px 24px rgba(99,102,241,.10); }
  .welcome-icon  { font-size:2.5rem; display:block; margin-bottom:.4rem; }
  .welcome-title { font-family:'Oxanium',sans-serif; font-size:1.5rem; font-weight:800; background:linear-gradient(90deg,#7c3aed,#0891b2,#059669); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; margin-bottom:.2rem; }
  .welcome-by    { font-size:.85rem; color:#0891b2; font-weight:700; margin-bottom:.7rem; }
  .welcome-desc  { font-size:.83rem; color:#475569; line-height:1.65; margin-bottom:.9rem; }
  .suggestions   { display:flex; flex-wrap:wrap; gap:7px; justify-content:center; }
  .chip { background:rgba(237,233,254,.88); border:1.5px solid rgba(124,58,237,.25); border-radius:999px; padding:5px 14px; font-size:.74rem; font-weight:600; color:#6d28d9; }

  /* thinking dots */
  .thinking { display:flex; gap:5px; padding:.65rem 1rem; background:rgba(255,255,255,.88); border:1.5px solid rgba(99,102,241,.14); border-radius:4px 18px 18px 18px; width:fit-content; }
  .dot { width:7px; height:7px; border-radius:50%; background:#7c3aed; animation:bounce 1.2s infinite ease-in-out; }
  .dot:nth-child(2){ animation-delay:.2s; }
  .dot:nth-child(3){ animation-delay:.4s; }
  @keyframes bounce { 0%,80%,100%{transform:scale(.7);opacity:.5} 40%{transform:scale(1.1);opacity:1} }

  /* textarea */
  .stTextArea textarea {
    background-color: #ffffff !important;
    border: 1.5px solid rgba(99,102,241,.28) !important;
    border-radius: 14px !important;
    color: #1e293b !important;
    font-family: 'Inter', sans-serif !important;
    font-size: .93rem !important;
    font-weight: 400 !important;
    resize: none !important;
    caret-color: #7c3aed !important;
    box-shadow: 0 1px 6px rgba(0,0,0,.06) !important;
    padding: .7rem 1rem !important;
  }
  .stTextArea textarea::placeholder { color:rgba(100,116,139,.50) !important; }
  .stTextArea textarea:focus {
    border-color: rgba(124,58,237,.55) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,.10) !important;
    outline: none !important;
  }

  /* send button */
  .stButton > button {
    background: linear-gradient(135deg,#7c3aed,#0891b2) !important;
    color: #fff !important; border: none !important;
    border-radius: 14px !important; padding: .70rem 1.6rem !important;
    font-family: 'Inter', sans-serif !important; font-size: .90rem !important;
    font-weight: 700 !important; width: 100% !important;
    transition: all .22s !important; box-shadow: 0 3px 14px rgba(124,58,237,.28) !important;
  }
  .stButton > button:hover { background:linear-gradient(135deg,#6d28d9,#0369a1) !important; transform:translateY(-1px) !important; }
  .stButton > button:active { transform:translateY(0) !important; }

  /* error / warning */
  .msg-warn { background:rgba(255,251,235,.95); border:1.5px solid rgba(245,158,11,.4); border-radius:10px; padding:.65rem 1rem; color:#92400e; font-size:.84rem; font-weight:600; margin:.4rem 0; }
</style>
""", unsafe_allow_html=True)


# ── LOAD DATA ─────────────────────────────────────────────────
paper_text = load_knowledge_base("research_paper_cleaned.txt")
if paper_text is None:
    st.error("research_paper_cleaned.txt not found. Place it in the same folder as app.py.")
    st.stop()
system_prompt = build_system_prompt(paper_text)

local_ip    = get_local_ip()
network_url = f"http://{local_ip}:8501"
qr_src      = make_qr_base64(network_url)


# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sidebar-title">IT Career Guidance</div>
    <div class="sidebar-by">with Atheek Fareez</div>
    <div class="sidebar-desc">
      Your AI mentor powered by real research —
      <em>"From Confusion to Clarity"</em> (2024–2026).
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:.70rem;font-weight:700;color:#6d28d9;letter-spacing:.09em;text-transform:uppercase;margin-bottom:6px;">IT Fields Covered</div>
    <div class="pill-wrap">
      <span class="s-pill ai">🤖 AI / Machine Learning</span>
      <span class="s-pill se">💻 Software Engineering</span>
      <span class="s-pill ds">📊 Data Science</span>
      <span class="s-pill cs">🔐 Cyber Security</span>
      <span class="s-pill net">🌐 CS &amp; Networks</span>
      <span class="s-pill im">📱 Info Management</span>
      <span class="s-pill ise">⚙️ IS Engineering</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="acc-card">
      <div class="acc-title">Access Links</div>
      <a class="acc-link local" href="http://localhost:8501" target="_blank">💻 Localhost</a>
      <a class="acc-link net"   href="{network_url}"         target="_blank">📱 Network / Mobile</a>
      <div style="text-align:center;margin-top:8px;">
        <img src="{qr_src}" width="88" style="border-radius:8px;"/>
        <div style="font-size:.62rem;color:#94a3b8;margin-top:3px;font-weight:600;">SCAN TO OPEN</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Session timer ─────────────────────────────────────────
    elapsed   = datetime.now() - st.session_state.session_start
    limit_sec = st.session_state.session_mins * 60
    remain    = max(0, limit_sec - int(elapsed.total_seconds()))
    mins_left = remain // 60
    secs_left = remain % 60
    pct_used  = min(1.0, elapsed.total_seconds() / max(limit_sec, 1))
    bar_w     = max(0, int((1 - pct_used) * 100))

    if remain == 0:
        st.session_state.session_active = False
        timer_cls  = "expd"
        timer_text = "EXPIRED"
        bar_colour = "#dc2626"
    elif mins_left < 5:
        timer_cls  = "warn"
        timer_text = f"{mins_left:02d}:{secs_left:02d}"
        bar_colour = "#d97706"
    else:
        timer_cls  = ""
        timer_text = f"{mins_left:02d}:{secs_left:02d}"
        bar_colour = "#7c3aed"

    qa_count = len(st.session_state.chat_history) // 2
    st.markdown(f"""
    <div class="timer-box">
      <div class="timer-label">Session Memory Timer</div>
      <div class="timer-val {timer_cls}">{timer_text}</div>
      <div style="background:rgba(0,0,0,.08);border-radius:999px;height:5px;margin:6px 0;">
        <div style="background:{bar_colour};width:{bar_w}%;height:5px;border-radius:999px;"></div>
      </div>
      <div class="timer-sub">Memory {st.session_state.session_mins} min · {qa_count} Q&amp;A pairs</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:.68rem;font-weight:700;color:#6d28d9;letter-spacing:.08em;text-transform:uppercase;margin-bottom:4px;">Set Session Duration</div>', unsafe_allow_html=True)
    new_mins = st.select_slider("dur", options=[5,10,15,20,30,45,60,90,120],
                                value=st.session_state.session_mins, label_visibility="collapsed")
    if new_mins != st.session_state.session_mins:
        st.session_state.session_mins   = new_mins
        st.session_state.session_start  = datetime.now()
        st.session_state.session_active = True
        st.rerun()

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("New Session", use_container_width=True):
            st.session_state.chat_history   = []
            st.session_state.gemini_history = []
            st.session_state.session_start  = datetime.now()
            st.session_state.session_active = True
            st.session_state.error_msg      = None
            st.rerun()
    with col_b:
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.chat_history   = []
            st.session_state.gemini_history = []
            st.session_state.error_msg      = None
            st.rerun()

    st.markdown("""
    <div class="sidebar-footer">
      Gemini 2.5 Flash · Research 2024–2026<br>
      Made with ❤️ by <strong>Atheek Fareez</strong>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# MAIN AREA — header + scrollable content + PINNED input bar
# ══════════════════════════════════════════════════════════════

# ── Sticky chat header ────────────────────────────────────────
st.markdown("""
<div class="chat-header">
  <div class="chat-header-title">🎓 IT Career Guidance</div>
  <div class="chat-header-sub">Gemini 2.5 Flash · Research 2024–2026 · by Atheek Fareez</div>
</div>
""", unsafe_allow_html=True)

# ── Scrollable chat content ───────────────────────────────────
st.markdown('<div class="main-content-pad">', unsafe_allow_html=True)

# Expired banner
if not st.session_state.session_active:
    st.markdown("""
    <div class="expired-banner">
      Session Expired — Click <strong>New Session</strong> in the sidebar to start fresh.
    </div>
    """, unsafe_allow_html=True)

# Welcome card (only when no messages)
if not st.session_state.chat_history:
    st.markdown("""
    <div class="welcome-card">
      <span class="welcome-icon">🎓</span>
      <div class="welcome-title">IT Career Guidance</div>
      <div class="welcome-by">✦ with Atheek Fareez ✦</div>
      <div class="welcome-desc">
        Ask me anything about IT careers, internship tips,<br>
        required skills and roadmaps for AI, SE, DS, CS and more.
      </div>
      <div class="suggestions">
        <span class="chip">🤖 How to become an AI developer?</span>
        <span class="chip">📊 Data Science career path</span>
        <span class="chip">💼 Why internships matter?</span>
        <span class="chip">🔐 Cybersecurity skills needed</span>
        <span class="chip">💻 Software Engineering roadmap</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# Chat bubbles
for msg in st.session_state.chat_history:
    ts = msg.get("ts", "")
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="msg-row user">
          <div><div class="avatar user-av">U</div><div class="msg-name">You</div></div>
          <div>
            <div class="bubble user-bubble">{msg["text"]}</div>
            <div style="font-size:.62rem;color:#94a3b8;text-align:right;margin-top:3px;">{ts}</div>
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="msg-row bot">
          <div><div class="avatar bot-av">🤖</div><div class="msg-name">Bot</div></div>
          <div>
            <div class="bubble bot-bubble">{msg["text"]}</div>
            <div style="font-size:.62rem;color:#94a3b8;margin-top:3px;">{ts}</div>
          </div>
        </div>""", unsafe_allow_html=True)

# Thinking dots
if st.session_state.thinking:
    st.markdown("""
    <div class="msg-row bot">
      <div><div class="avatar bot-av">🤖</div><div class="msg-name">Bot</div></div>
      <div class="thinking"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>
    </div>""", unsafe_allow_html=True)

# Error message
if st.session_state.error_msg:
    st.markdown(f'<div class="msg-warn">⚠️ {st.session_state.error_msg}</div>',
                unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close main-content-pad


# ══════════════════════════════════════════════════════════════
# PINNED INPUT BAR — position:fixed, always at bottom
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="pinned-input"><div class="pinned-input-inner">', unsafe_allow_html=True)

col_in, col_btn = st.columns([6, 1])
with col_in:
    user_input = st.text_area(
        label="msg",
        label_visibility="collapsed",
        placeholder="Ask me about IT careers, skills, internships...",
        height=52,
        key=f"chat_input_{st.session_state.input_key}",
    )
with col_btn:
    send_clicked = st.button("Send ➤", use_container_width=True)

st.markdown('</div></div>', unsafe_allow_html=True)


# ── Handle send ───────────────────────────────────────────────
if send_clicked:
    if not user_input.strip():
        st.session_state.error_msg = "Please type a message before sending."
        st.rerun()
    elif not st.session_state.session_active:
        st.session_state.error_msg = "Session expired. Click New Session in the sidebar."
        st.rerun()
    else:
        elapsed   = datetime.now() - st.session_state.session_start
        limit_sec = st.session_state.session_mins * 60
        if elapsed.total_seconds() >= limit_sec:
            st.session_state.session_active = False
            st.session_state.error_msg = "Session expired. Click New Session in the sidebar."
            st.rerun()

        now_ts = datetime.now().strftime("%H:%M")
        st.session_state.chat_history.append({"role":"user","text":user_input.strip(),"ts":now_ts})
        st.session_state.gemini_history.append({"role":"user","parts":[{"text":user_input.strip()}]})
        st.session_state.error_msg  = None
        st.session_state.thinking   = True
        st.session_state.input_key += 1
        st.rerun()

# ── Process AI response ───────────────────────────────────────
if st.session_state.thinking:
    try:
        answer       = ask_gemini(system_prompt, st.session_state.gemini_history)
        answer_clean = re.sub(r'\n{3,}', '\n\n', answer.strip())
        now_ts       = datetime.now().strftime("%H:%M")
        st.session_state.chat_history.append({"role":"bot","text":answer_clean,"ts":now_ts})
        st.session_state.gemini_history.append({"role":"model","parts":[{"text":answer_clean}]})
        st.session_state.error_msg = None
    except Exception as e:
        error_text = str(e)
        if any(k in error_text.lower() for k in ["429","quota","rate","resource_exhausted"]):
            st.session_state.error_msg = "Too many requests. Please wait a few seconds and try again."
        else:
            st.session_state.error_msg = f"API Error: {error_text}"
        if st.session_state.gemini_history and st.session_state.gemini_history[-1]["role"] == "user":
            st.session_state.gemini_history.pop()
    finally:
        st.session_state.thinking = False
    st.rerun()
