# prompt: connect my bot to front end using stream lit

# !pip install -q streamlit

import google.generativeai as genai
import os
import streamlit as st

# 🔑 Set up your Gemini API key
# Consider using Streamlit secrets for better security: https://docs.streamlit.io/develop/concepts/secrets
# If you are running this directly from Colab, the key will be exposed if you share the notebook.
# For production, use environment variables or Streamlit secrets.
GOOGLE_API_KEY = 'AIzaSyAZCBwvR2bKgrzbbSKpYSAXXH9TwEhjoS4'  # Replace with your own key if needed
genai.configure(api_key=GOOGLE_API_KEY)

# 🎭 Initialize the Gemini model
# Initialize the model outside of the main loop
model = genai.GenerativeModel(model_name='gemini-2.0-flash')

# 🗣️ Define the role and start the roleplay
role_prompt = """
You are a passive-aggressive boss. You blame your employee (me) for a team failure,
even if it's not fully my fault. Keep your tone subtle but hurtful.
Don't be too obvious. I will reply as an employee trying to stay calm.
Start the conversation now.
"""

# --- Streamlit App ---
st.title("🤖 AI Roleplay Therapist Chatbot")
st.write("Simulate emotional situations for resilience training.")

# Initialize chat history in Streamlit's session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    # Start the initial conversation with the role prompt
    chat = model.start_chat(history=st.session_state.chat_history)
    initial_response = chat.send_message(role_prompt)
    st.session_state.chat_history.append({"role": "model", "parts": [initial_response.text]})
    st.session_state.initial_prompt_sent = True
else:
    # Re-initialize the chat with the history
    chat = model.start_chat(history=st.session_state.chat_history)


# Display chat messages from history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["parts"][0]) # Assuming only one part for simplicity

# Get user input
user_input = st.chat_input("Enter your response:")

if user_input:
    # Add user message to chat history and display
    st.session_state.chat_history.append({"role": "user", "parts": [user_input]})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send user message to the model and get response
    response = chat.send_message(user_input)

    # Add model response to chat history and display
    st.session_state.chat_history.append({"role": "model", "parts": [response.text]})
    with st.chat_message("model"):
        st.markdown(response.text)

# To run this Streamlit app in Colab:
# 1. Save this code as a Python file (e.g., app.py).
# 2. In a new code cell in Colab, run: !streamlit run app.py & npx localtunnel --port 8501
# 3. Click the localtunnel URL provided in the output to open the app in your browser.
