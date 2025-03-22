import streamlit as st
import requests

API_URL = "http://localhost:8000/chat"

st.title("🛡️ Infinum Legal Advisor Chatbot")

question = st.text_input("Ask a legal question:")

if st.button("Get Advice"):
    if question:
        response = requests.post(API_URL, json={"question": question})
        if response.status_code == 200:
            st.write("**OpenAI Response:**")
            st.write(response.json()["answer"])
        else:
            st.error("Error fetching response from the backend.")
