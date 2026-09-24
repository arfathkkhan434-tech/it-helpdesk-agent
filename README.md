```markdown
# ⚡ Autonomous AI IT Helpdesk Agent

A full-stack, AI-powered IT Helpdesk support system that uses Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) to autonomously resolve employee IT requests, enforce company policies, and trigger automated physical actions.

## 🌟 Key Features
* **Autonomous Reasoning:** Powered by LangChain and Google Gemini (`gemini-3.6-flash`), the agent dynamically decides when to consult IT policy and when to execute system tools.
* **Retrieval-Augmented Generation (RAG):** Uses ChromaDB to embed and search internal enterprise IT policies efficiently.
* **Automated Actions:** Integrates with SMTP to physically email temporary passwords and secure reset links directly to users.
* **Live Audit Database:** Persists every interaction, request, and resolution status to a local SQLite database (`it_helpdesk.db`).
* **Decoupled Architecture:** 
  * **Backend:** A high-performance FastAPI server managing database transactions and LLM orchestration.
  * **Frontend:** A responsive Streamlit dashboard featuring live analytics, chat UI, custom avatars, and real-time database syncing.

---

## 🛠️ Tech Stack
* **AI & Orchestration:** Google Gemini (3.6 Flash), LangChain
* **Backend Framework:** FastAPI, Uvicorn
* **Frontend UI:** Streamlit, HTML/CSS/JS (for standalone reset portal)
* **Databases:** SQLite (Relational Audit Logs), ChromaDB (Vector Embeddings)

---

## 📂 Project Structure

```text
it-helpdesk-agent/
│
├── backend/
│   ├── app.py           # FastAPI server, API routing, and SQLite database logic
│   ├── agent.py         # LangChain orchestration, Gemini configuration, and Tool definitions
│   └── rag.py           # ChromaDB vector store setup and document embedding pipeline
│
├── frontend/
│   └── streamlit_app.py # Streamlit UI, chat interface, and analytics dashboard
│
├── .env                 # (Git-ignored) Private API keys and SMTP credentials
├── requirements.txt     # Python dependencies list
└── README.md            # Project documentation

```

---

## 🚀 Local Setup & Run Instructions

**1. Clone the Repository**

```bash
git clone [https://github.com/arfathkkhan434-tech/it-helpdesk-agent.git](https://github.com/arfathkkhan434-tech/it-helpdesk-agent.git)
cd it-helpdesk-agent

```

**2. Configure Environment Variables**
Create a new file named `.env` in the root directory and add your private credentials.

```env
GOOGLE_API_KEY="your_google_api_key_here"
EMAIL_ADDRESS="your_sender_email@gmail.com"
EMAIL_APP_PASSWORD="your_google_app_password_here"

```

**3. Install Dependencies**

```bash
pip install -r requirements.txt

```

**4. Start the Backend Server (FastAPI)**
Open a terminal and start Uvicorn to host the API and databases:

```bash
python -m uvicorn backend.app:app --reload --port 8000

```

**5. Start the Frontend Dashboard (Streamlit)**
Open a **second, separate terminal** and launch the UI:

```bash
streamlit run frontend/streamlit_app.py

```
