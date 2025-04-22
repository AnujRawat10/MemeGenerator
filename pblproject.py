import streamlit as st
import requests
from streamlit_extras.add_vertical_space import add_vertical_space

# API Configuration
MODEL_ENDPOINTS = {
    "GPT 4o mini": "https://payload.vextapp.com/hook/TZ9Z7POAYP/catch/$(10)",
    "Deepseek": "https://payload.vextapp.com/hook/94I0QJYGUV/catch/10"
}

API_KEYS = {
    "GPT 4o mini": "Api-Key Ixgvb348.9g9qdwzROoygMc3r2KAE3rljhEec2vNH",
    "Deepseek": "Api-Key RHfDKtsq.w9tO8fgTqMOM9NGbISxrTivhpF4SxrcV"
}

# Function to send prompt to model
def fetch_model_response(user_prompt, model_name):
    headers = {
        "Content-Type": "application/json",
        "Apikey": API_KEYS[model_name]
    }
    data = {
        "payload": user_prompt,
        "env": "dev"
    }

    try:
        response = requests.post(MODEL_ENDPOINTS[model_name], headers=headers, json=data)
        response.raise_for_status()
        return response.json().get("text", "")
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Streamlit UI
st.set_page_config(page_title="Hybrid Prompt Optimizer", layout="centered", initial_sidebar_state="expanded")
st.title("🧠 Hybrid Prompt Optimizer")
st.markdown("Enter your raw prompt below and get a single **optimized** version using both GPT & DeepSeek intelligence.")

with st.sidebar:
    st.header("About")
    st.markdown("**Creators:** Anuj Rawat, Pulle Thirupathi")
    add_vertical_space(2)
    st.markdown("This tool enhances prompt structure based on your input grammar and intent using a hybrid AI approach.")

st.markdown("---")
user_input = st.text_area("💬 Enter your raw prompt here:")

# New: Domain selection
domain = st.text_input("🌐 Specify the domain (e.g., marketing, education, medical):", value="general")

if st.button("🚀 Optimize Prompt"):
    if user_input.strip():
        # Add domain context to the prompt
        prompt_to_send = (
            f"Optimize this prompt for clarity, grammar, and expected output quality "
            f"in the context of {domain}:\n{user_input}"
        )

        # Get model responses
        gpt_response = fetch_model_response(prompt_to_send, "GPT 4o mini")
        deepseek_response = fetch_model_response(prompt_to_send, "Deepseek")

        # Hybrid strategy
        final_optimized = gpt_response if len(gpt_response) > len(deepseek_response) else deepseek_response

        # Display optimized prompt
        st.subheader("✅ Optimized Prompt")
        st.code(final_optimized.strip(), language='markdown')
    else:
        st.error("❗ Please enter a prompt to optimize.")
