# 🎓 IT Career Guidance Chatbot
### *From Confusion to Clarity — AI-Powered Career Mentor for IT Undergraduates*

**"Helping IT students navigate their career path with confidence — powered by real research."**



## 🌟 About the Project

**IT Career Guidance Chatbot** is an AI-powered web application built for IT undergraduate students who feel lost about their career direction. The chatbot is trained exclusively on the research paper:

> *"From Confusion to Clarity: IT Undergraduates, Industry Expectations, and the Role of Quality Internships (2024–2026)"*

It acts as a **personal AI mentor** — answering questions about IT career paths, internship guidance, required skills, and industry expectations in simple, student-friendly language.

---

## 🎯 Problem It Solves

Most IT students graduate without a clear career direction. They face:

- ❓ Confusion about which IT field suits them (AI, SE, DS, Cybersecurity, etc.)
- 📉 Gap between academic knowledge and industry expectations
- 🔍 Lack of internship guidance and real-world career roadmaps
- 😟 No personalized mentor available 24/7

This chatbot bridges that gap — available **anytime, anywhere**, for **any IT student**.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🤖 **AI Mentor** | Powered by Google Gemini 2.5 Flash |
| 📄 **Research-Based** | Answers strictly from the 2024–2026 research paper |
| 🎓 **Student-Friendly** | Simple English, bullet points, practical advice |
| 📱 **Mobile Ready** | QR code + network URL to open on any device |
| 🔗 **Clickable Links** | Localhost & network URLs shown inside the app UI |
| 🛡️ **Rate Limit Protection** | Friendly 429 error message instead of raw crash |
| 🔄 **Auto-Clear Input** | Query box resets after each answer for smooth use |
| 🎨 **Modern Light UI** | Soft pastel tech theme — clean, attractive, professional |

---

## 🧭 IT Fields Covered

```
🤖 AI / Machine Learning        💻 Software Engineering
📊 Data Science                  🔐 Cyber Security
🌐 CS & Networks (CSNE)         📱 Information Management (IM)
⚙️  Information Systems Eng (ISE)
```

---

## 🛠️ Tech Stack

```
Frontend      →   Streamlit (Python)
AI Model      →   Google Gemini 2.5 Flash
Knowledge     →   Custom research paper (.txt)
QR Code       →   qrcode + Pillow
Deployment    →   Render.com
Language      →   Python 3.10+
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/it-career-guidance-chatbot.git
cd it-career-guidance-chatbot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your Gemini API key
Open `app.py` and paste your key:
```python
client = genai.Client(api_key="YOUR_GEMINI_API_KEY_HERE")
```

### 4. Run the app
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
📦 it-career-guidance-chatbot
 ┣ 📄 app.py                      ← Main Streamlit application
 ┣ 📄 requirements.txt            ← Python dependencies
 ┣ 📄 research_paper_cleaned.txt  ← Knowledge base (research paper)
 ┗ 📄 README.md                   ← You are here
```

---

## 🌐 Deployment on Render

| Setting | Value |
|---|---|
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run app.py --server.port $PORT --server.address 0.0.0.0` |
| **Environment** | Python 3 |

---

## 💡 How It Works

```
User asks a question
        ↓
App sends question + full research paper → Gemini 2.5 Flash
        ↓
Gemini answers ONLY from the research paper content
        ↓
Clean, student-friendly response shown in UI
        ↓
Input box auto-clears → ready for next question
```

---

## 📸 App Preview

```
┌─────────────────────────────────────────────────┐
│  🤖 AI/ML  💻 SE  📊 DS  🔐 CS  🌐 CSNE  📱 IM  │
├─────────────────────────────────────────────────┤
│                                                 │
│   🎓  IT Career Guidance                        │
│       ✦ with Atheek Fareez ✦                   │
│                                                 │
│   Powered by "From Confusion to Clarity"        │
│   Ask about careers, internships & skills       │
│                                                 │
├─────────────────────────────────────────────────┤
│  ⚡ YOUR QUESTION                               │
│  ┌─────────────────────────────────────────┐   │
│  │ What skills do I need for AI career?    │   │
│  └─────────────────────────────────────────┘   │
│  [ 🚀  ASK THE BOT ]                           │
├─────────────────────────────────────────────────┤
│  🤖 ANSWER                                      │
│  To pursue an AI career, the research           │
│  highlights these key skills:                   │
│  • Python & Machine Learning fundamentals       │
│  • Data analysis & statistics                   │
│  • Hands-on internship experience...            │
└─────────────────────────────────────────────────┘
```

---

## 🔒 Important Notes

- The chatbot answers **only** from the research paper — it will not guess or use outside knowledge
- For questions outside the research scope, it replies politely with a standard message
- API rate limits apply on free tier — wait a few seconds between rapid queries

---

## 👨‍💻 About the Developer

**Atheek Fareez**
IT Undergraduate | AI Enthusiast | Research-Driven Developer

> *"I built this chatbot to help fellow IT students find clarity in their career journey — the same clarity I wished I had when I started."*

- 🔗 [LinkedIn](https://www.linkedin.com/in/yourprofile)
- 💻 [GitHub](https://github.com/yourusername)

---

## 📜 Research Reference

Atheek Fareez, A. et al. (2024–2026). *"From Confusion to Clarity: IT Undergraduates, Industry Expectations, and the Role of Quality Internships."* — Unpublished Research Paper.

---

## 📄 License

This project is for **educational and research purposes**.
© 2024–2026 Atheek Fareez. All rights reserved.

---
