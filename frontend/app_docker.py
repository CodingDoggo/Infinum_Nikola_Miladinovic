import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Legal Advisor Chatbot", layout="wide")
API_URL = "http://backend:8000"


# Initialize session state variables if they don't exist
if 'current_conversation_id' not in st.session_state:
    st.session_state.current_conversation_id = None
if 'conversations' not in st.session_state:
    st.session_state.conversations = []
if 'messages' not in st.session_state:
    st.session_state.messages = []

def load_conversations():
    try:
        response = requests.get(f"{API_URL}/conversations")
        if response.ok:
            conversations = response.json()
            # conversations.sort(key=lambda conv: conv["updated_at"], reverse=True)
            st.session_state.conversations = conversations
        else:
            st.error("Error loading conversations.")
    except Exception as e:
        st.error(f"Error loading conversations: {e}")
    

# Function to load messages for a selected conversation
def load_messages(conversation_id):
    try:
        response = requests.get(f"{API_URL}/conversations/{conversation_id}/messages")
        if response.ok:
            st.session_state.messages = response.json()
        else:
            st.error("Error loading messages.")
    except Exception as e:
        st.error(f"Error loading messages: {e}")

if not st.session_state.conversations:
    load_conversations()

# Ensure messages for the current conversation are loaded
if st.session_state.current_conversation_id:
    load_messages(st.session_state.current_conversation_id)

# Function to create a new conversation with a custom title
def create_new_conversation(title):
    try:
        response = requests.post(f"{API_URL}/conversations", json={"title": title})
        if response.ok:
            new_conv = response.json()
            st.session_state.current_conversation_id = new_conv["id"]
            st.session_state.conversations.append(new_conv)
            st.session_state.messages = []
        else:
            st.error("Error creating conversation.")
    except Exception as e:
        st.error(f"Error creating conversation: {e}")

# Function to send a message to the chat endpoint
def send_message(question):
    try:
        payload = {
            "question": question,
            "conversation_id": st.session_state.current_conversation_id
        }
        response = requests.post(f"{API_URL}/chat", json=payload)
        if response.ok:
            data = response.json()
            st.session_state.current_conversation_id = data["conversation_id"]
            load_messages(st.session_state.current_conversation_id)
            load_conversations()
        else:
            st.error("Error sending message.")
    except Exception as e:
        st.error(f"Error sending message: {e}")

# Configure the main page layout
st.title("🛡️ Infinum Legal Advisor Chatbot")

# Sidebar: Conversation management
with st.sidebar:
    st.header("Conversations")
    
    # Section to create a new conversation with a custom title
    st.subheader("New Conversation")
    # new_title = st.text_input("Conversation Title", value="New Conversation", key="new_title")
    if st.button("Create Conversation"):
        create_new_conversation("New Conversation")
        load_conversations()
    
    st.markdown("---")
    # if st.button("Refresh Conversations"):
        # load_conversations()

    st.markdown("### Existing Conversations")
    if st.session_state.conversations:
        for conv in st.session_state.conversations:
            # Format the creation date
            dt = datetime.fromisoformat(conv["updated_at"].replace("Z", "+00:00"))
            date_str = dt.strftime("%b %d, %Y")  # Example: "Mar 22, 2025"

            # Shorten title if it's too long
            short_title = conv["title"][:30] + "..." if len(conv["title"]) > 30 else conv["title"]

            if st.button(f"{short_title} | {date_str}", key=f"conv_{conv['id']}"):
                st.session_state.current_conversation_id = conv["id"]
                load_messages(conv["id"])
    else:
        load_conversations()
        st.info("No conversations available. Create a new one!")

# Main chat area
if st.session_state.current_conversation_id is None:
    st.info("Select an existing conversation or create a new one to start chatting.")
else:
    st.subheader("Chat History")
    
    # Display conversation messages using Streamlit's chat_message components if available.
    # Otherwise, fallback to st.write.
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            try:
                st.chat_message("user").write(msg["content"])
            except Exception:
                st.write(f"🧑 You: {msg['content']}")
        elif msg["role"] == "assistant":
            try:
                st.chat_message("assistant").write(msg["content"])
            except Exception:
                st.write(f"🤖 Legal Advisor: {msg['content']}")
                
    st.markdown(
        "<script>window.scrollTo(0, document.body.scrollHeight);</script>",
        unsafe_allow_html=True,
    )            

    # Form to send a new message
    with st.form(key="message_form", clear_on_submit=True):
        question = st.text_area("Ask a legal question:", height=100)
        submit_button = st.form_submit_button("Send")
        if submit_button and question.strip():
            send_message(question.strip())
            st.rerun()