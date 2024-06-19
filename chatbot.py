import streamlit as st
import openai
import os 
# Set your OpenAI API key
openai.api_key = os.getenv["api_key"]


initial_prompt = {
    "role": "system",
    "content": (
        "You are a humane chatbot that analyzes user text and identifies the emotion behind it. "
        "You give counselor-like feedback and also engage the user by asking relevant questions about his mood. "
        "You are ONLY to answer in relation to mental counselling; nothing else."
    )
}

# Function to generate a response from the fine-tuned GPT model
def query_chatgpt(message, conversation_history):
    try:
        response = openai.ChatCompletion.create(
            model="ft:gpt-3.5-turbo-0125:personal::9bBTZFV7",  # Replace with your fine-tuned model
            messages=[initial_prompt] + conversation_history + [{"role": "user", "content": message}],
            max_tokens=150
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return str(e)

# Streamlit UI
st.title("Welcome to TheraBot")

# Initialize the conversation history
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Input message from the user
user_message = st.text_input("You: ", "")

if user_message:
    # Query the ChatGPT API
    response_message = query_chatgpt(user_message, st.session_state.conversation_history)

    # Update the conversation history
    st.session_state.conversation_history.append({"role": "user", "content": user_message})
    st.session_state.conversation_history.append({"role": "assistant", "content": response_message})

    # Clear the input box
    # st.text_input("You: ", "", key="empty_input")

# Display the conversation history
for message in st.session_state.conversation_history:
    if message['role'] == 'user':
        st.write(f"You: {message['content']}")
    else:
        st.write(f"TheraBot: {message['content']}")