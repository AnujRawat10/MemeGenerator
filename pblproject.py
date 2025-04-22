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

# Function to send a prompt to a model
def fetch_model_response(user_prompt, model_name):
    headers = {
        "Content-Type": "application/json",
        "Apikey": API_KEYS[model_name]
    }
    data = {
        "payload": f"Optimize this prompt for clarity, grammar, and expected output quality:\n{user_prompt}",
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
    st.markdown("**Authors:** Anuj Rawat, Pulle Thirupathi")
    add_vertical_space(2)
    st.markdown("This tool enhances prompt structure based on your input grammar and intent using a hybrid AI approach.")

st.markdown("---")
user_input = st.text_area("💬 Enter your raw prompt here:")

if st.button("🚀 Optimize Prompt"):
    if user_input.strip():
        # Call both models
        gpt_response = fetch_model_response(user_input, "GPT 4o mini")
        deepseek_response = fetch_model_response(user_input, "Deepseek")

        # Hybrid strategy: You can choose to pick the best, average them, or merge.
        # For now, let's just show the GPT version if available, else Deepseek.
        final_optimized = gpt_response if len(gpt_response) > len(deepseek_response) else deepseek_response

        st.subheader("✅ Optimized Prompt")
        st.code(final_optimized.strip(), language='markdown')
    else:
        st.error("❗ Please enter a prompt to optimize.")
