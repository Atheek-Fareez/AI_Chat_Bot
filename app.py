# ============================================================
# IT CAREER GUIDANCE CHATBOT - Streamlit App
# Paper: "From Confusion to Clarity: IT Undergraduates,
#         Industry Expectations, and the Role of Quality
#         Internships (2024–2026)"
# ============================================================
# SETUP:
#   pip install streamlit google-genai
#   streamlit run app.py
# ============================================================

import streamlit as st
from google import genai
import re
import socket
import qrcode
import io
import base64

# ── PAGE CONFIG ──────────────────────────────────────────────
st.set_page_config(
    page_title="IT Career Guidance with Atheek Fareez",
    page_icon="🎓",
    layout="centered",
)

# ── GEMINI CLIENT ────────────────────────────────────────────
# Paste your Gemini API key below ↓
client = genai.Client(api_key="AIzaSyCt-Es5RnPB7dFhq2OUrJzoLJTVNnAEFsw")


# ── FULL PAGE CSS + BUILT-IN IT BACKGROUND ───────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Oxanium:wght@300;400;600;700;800&family=Share+Tech+Mono&display=swap');

  html, body, [class*="css"] {
    font-family: 'Oxanium', sans-serif;
  }

  /* ── light tech background ── */
  .stApp {
    min-height: 100vh;
    background-color: #f0f4ff;
    background-image:
      /* soft dot grid */
      radial-gradient(circle, rgba(99,102,241,0.12) 1px, transparent 1px),
      /* soft colour blobs */
      radial-gradient(ellipse at 15% 40%, rgba(167,139,250,0.22) 0%, transparent 55%),
      radial-gradient(ellipse at 85% 15%, rgba(56,189,248,0.20) 0%, transparent 55%),
      radial-gradient(ellipse at 70% 85%, rgba(52,211,153,0.15) 0%, transparent 50%),
      radial-gradient(ellipse at 30% 90%, rgba(251,113,133,0.12) 0%, transparent 45%),
      /* base light gradient */
      linear-gradient(145deg, #eef2ff 0%, #f5f3ff 35%, #ecfdf5 70%, #eff6ff 100%);
    background-size: 28px 28px, auto, auto, auto, auto, auto;
    position: relative;
  }

  /* ── top animated bar ── */
  .stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, #7c3aed, #06b6d4, #10b981, #f59e0b, #7c3aed);
    background-size: 300% 100%;
    animation: topbar 5s linear infinite;
    z-index: 9999;
  }
  @keyframes topbar {
    0%   { background-position: 0% 0%; }
    100% { background-position: 300% 0%; }
  }

  /* ── floating IT field pills strip ── */
  .it-fields {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin-bottom: 1.4rem;
  }
  .it-pill {
    background: rgba(255,255,255,0.75);
    border: 1.5px solid rgba(99,102,241,0.20);
    border-radius: 999px;
    padding: 5px 15px;
    font-size: 0.72rem;
    font-family: 'Share Tech Mono', monospace;
    font-weight: 700;
    letter-spacing: 0.06em;
    color: #64748b;
    transition: all 0.2s;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  }
  .it-pill.ai   { border-color: rgba(124,58,237,0.40); color: #6d28d9; background: rgba(237,233,254,0.90); }
  .it-pill.se   { border-color: rgba(37,99,235,0.35);  color: #1d4ed8; background: rgba(219,234,254,0.90); }
  .it-pill.ds   { border-color: rgba(5,150,105,0.35);  color: #047857; background: rgba(209,250,229,0.90); }
  .it-pill.cs   { border-color: rgba(180,83,9,0.35);   color: #b45309; background: rgba(254,243,199,0.90); }
  .it-pill.net  { border-color: rgba(190,24,93,0.35);  color: #be185d; background: rgba(252,231,243,0.90); }
  .it-pill.im   { border-color: rgba(15,118,110,0.35); color: #0f766e; background: rgba(204,251,241,0.90); }
  .it-pill.ise  { border-color: rgba(194,65,12,0.35);  color: #c2410c; background: rgba(255,237,213,0.90); }

  /* ── main card ── */
  .main-card {
    background: rgba(255,255,255,0.82);
    border: 1.5px solid rgba(124,58,237,0.18);
    border-top: 2px solid rgba(124,58,237,0.50);
    border-radius: 22px;
    padding: 2.2rem 2.5rem 2rem;
    backdrop-filter: blur(16px);
    box-shadow:
      0 4px 24px rgba(99,102,241,0.10),
      0 1px 0 rgba(255,255,255,0.9) inset;
    margin-bottom: 1.4rem;
    position: relative;
    overflow: hidden;
  }
  /* rainbow top-corner accent */
  .main-card::after {
    content: "";
    position: absolute;
    top: -1px; right: -1px;
    width: 70px; height: 70px;
    background: linear-gradient(225deg, rgba(124,58,237,0.25) 0%, transparent 65%);
    border-radius: 0 22px 0 0;
  }

  /* ── hero section ── */
  .hero-icon {
    font-size: 2.8rem;
    margin-bottom: 0.5rem;
    display: block;
    filter: drop-shadow(0 4px 10px rgba(124,58,237,0.35));
  }
  .hero-title {
    font-size: 2.1rem;
    font-weight: 800;
    background: linear-gradient(90deg, #7c3aed 0%, #0891b2 55%, #059669 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.15rem;
    line-height: 1.15;
    letter-spacing: -0.01em;
  }
  .hero-by {
    font-size: 0.95rem;
    font-weight: 700;
    color: #0891b2;
    margin-bottom: 0.7rem;
    letter-spacing: 0.04em;
  }
  .hero-sub {
    font-size: 0.87rem;
    color: #475569;
    font-weight: 500;
    line-height: 1.65;
    margin-bottom: 0;
  }

  /* ── section label ── */
  .field-label {
    color: #6d28d9;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.45rem;
  }

  /* ── divider ── */
  .divider {
    border: none;
    border-top: 1.5px solid rgba(99,102,241,0.15);
    margin: 1.4rem 0;
  }

  /* ── textarea ── */
  .stTextArea textarea {
    background-color: #ffffff !important;
    border: 1.5px solid rgba(99,102,241,0.30) !important;
    border-radius: 12px !important;
    color: #1e293b !important;
    font-family: 'Oxanium', sans-serif !important;
    font-size: 0.93rem !important;
    font-weight: 500 !important;
    resize: none !important;
    caret-color: #7c3aed !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
  }
  .stTextArea textarea::placeholder {
    color: rgba(100,116,139,0.55) !important;
  }
  .stTextArea textarea:focus {
    border-color: rgba(124,58,237,0.60) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.12) !important;
    outline: none !important;
  }

  /* ── ask button ── */
  .stButton > button {
    background: linear-gradient(135deg, #7c3aed 0%, #0891b2 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.70rem 2rem !important;
    font-family: 'Oxanium', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    width: 100% !important;
    transition: all 0.25s !important;
    box-shadow: 0 4px 18px rgba(124,58,237,0.30) !important;
  }
  .stButton > button:hover {
    background: linear-gradient(135deg, #6d28d9 0%, #0369a1 100%) !important;
    box-shadow: 0 6px 26px rgba(124,58,237,0.45) !important;
    transform: translateY(-2px) !important;
  }
  .stButton > button:active {
    transform: translateY(0) !important;
  }

  /* ── response box ── */
  .response-box {
    background: rgba(255,255,255,0.90);
    border: 1.5px solid rgba(99,102,241,0.20);
    border-left: 4px solid #7c3aed;
    border-radius: 14px;
    padding: 1.3rem 1.6rem;
    color: #1e293b;
    font-size: 0.93rem;
    font-weight: 500;
    line-height: 1.65;
    white-space: pre-wrap;
    box-shadow: 0 2px 16px rgba(99,102,241,0.08);
  }
  .response-box p  { margin: 0 0 0.35rem 0; }
  .response-box ul,
  .response-box ol { margin: 0.15rem 0 0.35rem 1.2rem; padding: 0; }
  .response-box li { margin-bottom: 0.12rem; }
  .response-box br { display: block; content: ""; margin: 0; line-height: 0.4; }

  /* ── question echo ── */
  .q-echo {
    font-size: 0.80rem;
    color: #0891b2;
    font-style: italic;
    font-weight: 400;
    text-transform: none;
    letter-spacing: 0;
  }

  /* ── warning / error ── */
  .msg-warn {
    background: rgba(255,251,235,0.95);
    border: 1.5px solid rgba(245,158,11,0.45);
    border-radius: 12px;
    padding: 0.85rem 1.2rem;
    color: #92400e;
    font-size: 0.88rem;
    font-weight: 600;
    box-shadow: 0 1px 6px rgba(245,158,11,0.12);
  }
  .msg-error {
    background: rgba(255,241,242,0.95);
    border: 1.5px solid rgba(239,68,68,0.35);
    border-radius: 12px;
    padding: 0.85rem 1.2rem;
    color: #9b1c1c;
    font-size: 0.88rem;
    font-weight: 600;
    box-shadow: 0 1px 6px rgba(239,68,68,0.10);
  }

  /* ── footer ── */
  .footer {
    text-align: center;
    color: #94a3b8;
    font-size: 0.74rem;
    font-weight: 500;
    margin-top: 2.5rem;
    letter-spacing: 0.03em;
  }
  .footer strong { color: #7c3aed; }

  /* ── spinning loader dots ── */
  @keyframes pulse { 0%,100%{opacity:.3} 50%{opacity:1} }

  /* ── access links card ── */
  .access-card {
    background: rgba(255,255,255,0.80);
    border: 1.5px solid rgba(99,102,241,0.20);
    border-radius: 16px;
    padding: 0.9rem 1.4rem;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 1.2rem;
    flex-wrap: wrap;
    box-shadow: 0 2px 12px rgba(99,102,241,0.08);
  }
  .access-title {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    color: #6d28d9;
    margin-bottom: 0.5rem;
  }
  .access-link {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: rgba(237,233,254,0.90);
    border: 1.5px solid rgba(124,58,237,0.30);
    border-radius: 8px;
    padding: 5px 14px;
    color: #6d28d9 !important;
    font-size: 0.82rem;
    font-weight: 700;
    text-decoration: none !important;
    margin-right: 8px;
    margin-bottom: 4px;
    transition: all 0.2s;
  }
  .access-link:hover {
    background: rgba(221,214,254,0.95);
    border-color: rgba(124,58,237,0.55);
    box-shadow: 0 3px 12px rgba(124,58,237,0.18);
    transform: translateY(-1px);
  }
  .access-link.net-link {
    background: rgba(224,242,254,0.90);
    border-color: rgba(8,145,178,0.35);
    color: #0369a1 !important;
  }
  .access-link.net-link:hover {
    background: rgba(186,230,255,0.95);
    border-color: rgba(8,145,178,0.60);
    box-shadow: 0 3px 12px rgba(8,145,178,0.18);
  }
  .qr-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
  }
  .qr-label {
    font-size: 0.65rem;
    color: #94a3b8;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }

  /* hide streamlit chrome */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 2rem !important; }
</style>
""", unsafe_allow_html=True)


# ── LOAD KNOWLEDGE BASE ──────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_knowledge_base(filepath: str) -> str | None:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None


# ── BUILD SYSTEM PROMPT ──────────────────────────────────────
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

═══════════════════════════════════════════════
KNOWLEDGE BASE (use ONLY this):
{paper_text}
═══════════════════════════════════════════════

STRICT RULES:
1. Answer ONLY from the research paper above.
2. Do NOT use external knowledge or guess.
3. Do NOT invent facts, statistics, or advice not found in the paper.

RESPONSE FORMAT:
- If question is RELATED to the research → give a clear, helpful answer.
  • Use simple English a first-year student can understand.
  • Use bullet points when listing steps or skills.
  • Be warm, supportive, and practical.
  • Keep it concise — avoid lengthy essays.

- If question is OUTSIDE the research scope → reply EXACTLY:
  "I'm sorry, I don't have information about that yet.
  But I will definitely let you know once I learn about it 😊"

TONE: Friendly mentor. Encouraging. Clear. Student-focused.
""".strip()


# ── ASK GEMINI ───────────────────────────────────────────────
def ask_gemini(system_prompt: str, user_question: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_question,
        config={"system_instruction": system_prompt},
    )
    return response.text


# ── SESSION STATE ─────────────────────────────────────────────
if "answer"        not in st.session_state: st.session_state.answer        = None
if "input_key"     not in st.session_state: st.session_state.input_key     = 0
if "last_question" not in st.session_state: st.session_state.last_question = ""
if "error_msg"     not in st.session_state: st.session_state.error_msg     = None


# ══════════════════════════════════════════════════════════════
# UI
# ══════════════════════════════════════════════════════════════

# ── NETWORK ACCESS LINKS + QR CODE ──────────────────────────
def get_local_ip() -> str:
    """Get the machine local network IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return socket.gethostbyname(socket.gethostname())

def make_qr_base64(url: str) -> str:
    """Generate a QR code PNG and return it as a base64 data URI."""
    qr = qrcode.QRCode(box_size=4, border=2,
                       error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#6d28d9", back_color="#f5f3ff")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

local_ip    = get_local_ip()
network_url = f"http://{local_ip}:8501"
qr_src      = make_qr_base64(network_url)

st.markdown(f"""
<div class="access-card">
  <div style="flex:1; min-width:180px;">
    <div class="access-title">🔗 Access Links</div>
    <a class="access-link" href="http://localhost:8501" target="_blank">💻 Localhost</a>
    <a class="access-link net-link" href="{network_url}" target="_blank">📱 Network / Mobile</a>
    <div style="font-size:0.70rem; color:rgba(148,163,184,0.55); margin-top:6px;">
      Make sure phone &amp; laptop are on the same WiFi
    </div>
  </div>
  <div class="qr-wrap">
    <img src="{qr_src}" width="80" style="border-radius:6px;"/>
    <span class="qr-label">Scan to open</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── IT field pills (decorative, shows the domains covered) ───
st.markdown("""
<div class="it-fields">
  <span class="it-pill ai">🤖 AI / ML</span>
  <span class="it-pill se">💻 Software Eng</span>
  <span class="it-pill ds">📊 Data Science</span>
  <span class="it-pill cs">🔐 Cyber Security</span>
  <span class="it-pill net">🌐 CS &amp; Networks</span>
  <span class="it-pill im">📱 Intractive Media</span>
  <span class="it-pill ise">⚙️ IS Engineering</span>
</div>
""", unsafe_allow_html=True)

# ── Hero card ─────────────────────────────────────────────────
st.markdown("""
<div class="main-card">
  <span class="hero-icon">🎓</span>
  <div class="hero-title">IT Career Guidance</div>
  <p class="hero-sub">
    Your AI mentor powered by the research paper
    <strong style="color:#c4b5fd;">"From Confusion to Clarity"</strong> (2024–2026).<br>
    Ask anything about IT careers, internships trends, skills &amp; roadmaps — AI, SE, DS, CS, CSNE, IM &amp; ISE.
  </p>
</div>
""", unsafe_allow_html=True)

# ── Load knowledge base ───────────────────────────────────────
paper_text = load_knowledge_base("research_paper_cleaned.txt")

if paper_text is None:
    st.markdown("""
    <div class="msg-error">
      ⚠️ <strong>research_paper_cleaned.txt not found.</strong><br>
      Place it in the same folder as <code>app.py</code> and re-run.
    </div>
    """, unsafe_allow_html=True)
    st.stop()

system_prompt = build_system_prompt(paper_text)

# ── Input area ────────────────────────────────────────────────
st.markdown('<div class="field-label">⚡ Your Question</div>', unsafe_allow_html=True)
user_question = st.text_area(
    label="question",
    label_visibility="collapsed",
    placeholder="e.g.  What skills do I need to become an AI developer?",
    height=115,
    key=f"input_{st.session_state.input_key}",
)

ask_clicked = st.button("🚀  Ask the Bot")

# ── Handle submit ─────────────────────────────────────────────
if ask_clicked:
    if not user_question.strip():
        st.markdown("""
        <div class="msg-warn">✏️ Please type a question before clicking Ask.</div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("Thinking..."):
            try:
                answer = ask_gemini(system_prompt, user_question.strip())
                answer_clean = re.sub(r'\n{3,}', '\n\n', answer.strip())

                st.session_state.answer        = answer_clean
                st.session_state.last_question = user_question.strip()
                st.session_state.error_msg     = None
                st.session_state.input_key    += 1   # clears textarea

            except Exception as e:
                error_text = str(e)
                if any(k in error_text.lower() for k in ["429", "quota", "rate", "resource_exhausted"]):
                    st.session_state.error_msg = "⏳ Too many requests were sent in a short time. Please wait a few seconds and try again."
                else:
                    st.session_state.error_msg = error_text
                st.session_state.answer = None

        st.rerun()

# ── Show error ────────────────────────────────────────────────
if st.session_state.error_msg:
    if "Too many requests" in st.session_state.error_msg or "⏳" in st.session_state.error_msg:
        st.error(st.session_state.error_msg)
    else:
        st.markdown(f'''
        <div class="msg-error">
          ❌ <strong>API Error:</strong> {st.session_state.error_msg}<br><br>
          Check that your API key is correct and that you have internet access.
        </div>
        ''', unsafe_allow_html=True)

# ── Show answer ───────────────────────────────────────────────
if st.session_state.answer:
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    short_q   = st.session_state.last_question[:90]
    ellipsis  = "…" if len(st.session_state.last_question) > 90 else ""
    st.markdown(
        f'<div class="field-label">🤖 Answer '
        f'<span class="q-echo">— {short_q}{ellipsis}</span></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="response-box">{st.session_state.answer}</div>',
        unsafe_allow_html=True
    )

# ── Footer ────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  IT Career Guidance · Gemini 2.5 Flash · "From Confusion to Clarity" (2024–2026)<br>
  Made by <strong>Atheek Fareez</strong>
</div>
""", unsafe_allow_html=True)
