# 🤖 AutoMate AI Assistant

A personal AI-powered automation assistant built with **n8n**, **Streamlit**, and **Groq (LLaMA)**. It connects to your everyday tools — Gmail, Google Calendar, Google Docs, and more — through a conversational chat interface.

---

## ✨ Features

| Capability | Description |
|---|---|
| 📧 **Gmail** | Read inbox, send emails to any recipient |
| 📅 **Google Calendar** | Create events, get event info, generate meeting links |
| 📝 **Google Docs** | Create, read, and append to documents |
| 💸 **Expense Tracker** | Log and read expenses via Google Sheets |
| 🔍 **Google Search** | Real-time web search (toggle on/off) |
| 🧮 **Calculator** | Math and unit conversions |
| 🧠 **Memory** | Remembers context within a session |

---

## 🏗️ Architecture

```
User (Streamlit UI)
        │
        │  HTTP POST (message)
        ▼
  n8n Webhook  ──►  AI Agent (Groq / LLaMA)
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
           Gmail    G-Calendar   G-Docs
                                      │
                              Expense Tracker (Sheets)
```

- **Frontend**: Streamlit chat UI
- **Orchestration**: n8n workflow automation
- **LLM**: Groq (LLaMA 3) via n8n AI Agent node
- **Integrations**: Google Workspace APIs via n8n

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- [n8n](https://n8n.io/) running locally or on a server
- Google Cloud project with OAuth credentials (for Gmail, Calendar, Docs, Sheets)
- Groq API key

### 1. Clone the repo

```bash
git clone https://github.com/Yuvraj-Saini-26/automate-ai-assistant.git
cd automate-ai-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env and add your n8n webhook URL
```

Then update `app.py` line 7 with your webhook URL:

```python
WEBHOOK_URL = "http://localhost:5678/webhook/YOUR-WEBHOOK-ID"
```

### 4. Set up n8n

- Import the workflow JSON (coming soon) into your n8n instance
- Connect your Google account and Groq API key in n8n credentials
- Activate the workflow

### 5. Run the app

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 📁 Project Structure

```
automate-ai-assistant/
├── app.py                  # Streamlit chat UI
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── .gitignore
└── src/
    ├── Assistant(AnkiBot).jpeg   # Assistant avatar
    └── User-logo.jpeg            # User avatar
```

---

## 🛠️ Tech Stack

- **[Streamlit](https://streamlit.io/)** — Python web UI framework
- **[n8n](https://n8n.io/)** — No-code/low-code workflow automation
- **[Groq](https://groq.com/)** — Ultra-fast LLM inference (LLaMA 3)
- **Google Workspace APIs** — Gmail, Calendar, Docs, Sheets

---

## 🔒 Security Notes

- Never commit your `.env` file or webhook URLs to GitHub
- Use n8n credentials manager for all API keys
- The webhook URL is rate-limited to your local machine by default

---

## 📌 Roadmap

- [ ] Export n8n workflow JSON for easy import
- [ ] Dockerize the full stack (n8n + Streamlit)
- [ ] Add voice input support
- [ ] Support multiple user sessions

---

## 👤 Author

Built by **Yuvraj Saini** — feel free to reach out or connect!

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://linkedin.com/in/saini-yuvraj)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?logo=github)](https://github.com/Yuvraj-Saini-26)
