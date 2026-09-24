import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000/api"

st.set_page_config(page_title="AI IT Helpdesk Agent", layout="wide")
st.title("🤖 Autonomous AI Agent for IT Helpdesk")

with st.sidebar:
    st.header("👤 Employee Profile")
    user_email = st.text_input("Corporate Email", value="shaikhmohammedaleem@gmail.com")
    
    st.divider()
    st.header("📋 Live Audit Logs")
    if st.button("Refresh Logs"):
        try:
            res = requests.get(f"{BACKEND_URL}/tickets")
            if res.status_code == 200:
                tickets = res.json()
                if not tickets:
                    st.info("No tickets found.")
                for t in tickets:
                    # UPDATED: Matches the backend database columns exactly (id, status, request_text)
                    st.markdown(f"**#{t.get('id', 'N/A')}** | `{t.get('status', 'N/A')}`\n- **Req:** {t.get('request_text', 'N/A')}")
                    st.divider()
        except Exception as e:
            st.error(f"Cannot fetch logs: {e}")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your autonomous IT support agent. What can I help you with today?"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_query = st.chat_input("Type an IT request (e.g., 'Reset my password' or 'Install Docker')...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing request and executing resolution..."):
            try:
                res = requests.post(
                    f"{BACKEND_URL}/resolve-ticket",
                    json={"user_email": user_email, "request_text": user_query}
                )
                if res.status_code == 200:
                    answer = res.json().get("response")
                else:
                    answer = "Error: Backend returned a failure status."
            except Exception as ex:
                answer = f"Connection error: Make sure FastAPI backend is running! ({ex})"
            
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})