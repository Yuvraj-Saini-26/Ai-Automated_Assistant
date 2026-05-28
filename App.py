import streamlit as st
import requests
import json

# Paste your n8n production webhook URL below.
# To get it: open your workflow in n8n → click the Webhook node → copy the Production URL
WEBHOOK_URL = "paste your webhook url here"

# Basic page config — change the title/icon if you want
st.set_page_config(page_title="AutoMate AI Assistant", page_icon="🤖")

# Header: logo on the left, title on the right
col1, col2 = st.columns([1, 6])
with col1:
    st.image("src/Assistant(AnkiBot).jpeg", width=120)
with col2:
    st.title("AutoMate-Ai-Assistant")

# This keeps the chat history alive across reruns.
# Without this, messages would vanish every time Streamlit re-renders.
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello 👋 I am AnkiBott. How can I help you today?"
        }
    ]

# This function sends the user's message to n8n and returns the AI's reply.
# n8n can return the response in a bunch of different shapes depending on
# how your workflow is built — so we check all the common ones.
def send_to_n8n(user_message: str) -> str:
    payload = {"message": user_message}
    headers = {"Content-Type": "application/json"}

    # Terminal log — useful when running locally to see what's going out
    print("\n" + "="*50)
    print("📤 Sending to n8n...")
    print(f"   URL     : {WEBHOOK_URL}")
    print(f"   Message : {user_message}")
    print("="*50)

    try:
        response = requests.post(
            WEBHOOK_URL,
            json=payload,
            headers=headers,
            timeout=60  # give the AI up to 60s to respond
        )

        # Terminal log — shows what came back from n8n
        print(f"📥 Response: {response.status_code}")
        print(f"   Body: {response.text}\n")

        if response.status_code != 200:
            return f"❌ HTTP Error {response.status_code}: {response.text}"

        try:
            data = response.json()
        except Exception as e:
            print(f"⚠️  Couldn't parse JSON: {e}")
            return response.text.strip()

        # n8n AI Agent can return the reply inside different keys depending
        # on how you've set up the workflow — we try all common ones here
        if isinstance(data, list) and len(data) > 0:
            item = data[0]
            for key in ["output", "text", "message", "response", "content"]:
                if key in item:
                    return str(item[key])
            return json.dumps(item)

        elif isinstance(data, dict):
            for key in ["output", "text", "message", "response", "content"]:
                if key in data:
                    return str(data[key])
            return json.dumps(data)

        return str(data)

    except requests.exceptions.ConnectionError:
        msg = "❌ Couldn't connect — is n8n running? Is the workflow active?"
        print(f"🔴 {msg}")
        return msg

    except requests.exceptions.Timeout:
        msg = "❌ Timed out after 60s — n8n might still be processing, try again"
        print(f"🔴 {msg}")
        return msg

    except Exception as e:
        msg = f"❌ Unexpected error: {type(e).__name__}: {e}"
        print(f"🔴 {msg}")
        return msg


# Sidebar — just the essentials, no debug clutter
with st.sidebar:
    st.header("⚙️ Controls")
    st.markdown("**What I can do**")
    st.markdown("- 📅 Google Calendar scheduling")
    st.markdown("- 📧 Gmail send & read")
    st.markdown("- 📝 Google Docs notes")
    st.markdown("- 💸 Expense tracking")
    st.markdown("- 🔍 Google Search")
    st.markdown("---")
    if st.button("🗑️ Clear chat history"):
        st.session_state.messages = []
        st.rerun()

# Render all previous messages in order
for msg in st.session_state.messages:
    avatar = (
        "src/Assistant(AnkiBot).jpeg"
        if msg["role"] == "assistant"
        else "src/User-logo.jpeg"
    )
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

# Main chat input — pressing Enter sends the message
user_input = st.chat_input("Type your message...")

if user_input:
    # Show the user's message right away
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="src/User-logo.jpeg"):
        st.write(user_input)

    # Hit the webhook and show the reply once it comes back
    with st.chat_message("assistant", avatar="src/Assistant(AnkiBot).jpeg"):
        with st.spinner("Thinking..."):
            reply = send_to_n8n(user_input)
        st.write(reply)

    # Save the reply so it stays visible on next rerun
    st.session_state.messages.append({"role": "assistant", "content": reply})
