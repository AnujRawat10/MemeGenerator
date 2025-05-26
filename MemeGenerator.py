import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import requests
import io
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

# Function to call model
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

# Meme generation (add caption to image)
def generate_meme(image, caption):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", size=40)  # You can change font and size

    # Wrap text
    lines = []
    words = caption.split()
    line = ""
    for word in words:
        if len(line + word) < 30:
            line += word + " "
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)

    y = 10
    for line in lines:
        w, h = draw.textsize(line, font=font)
        draw.text(((image.width - w) / 2, y), line, fill="white", stroke_width=2, stroke_fill="black", font=font)
        y += h + 5

    return image

# Streamlit UI
st.set_page_config(page_title="Meme Generator", layout="centered")
st.title("😂 Trendy Meme Generator")
st.markdown("Generate **creative**, **sarcastic**, and **trending** memes using AI power.")

with st.sidebar:
    st.header("About This App")
    st.markdown("**Creator:** Anuj Rawat")
    add_vertical_space(1)
    st.markdown("- Input a meme idea or upload an image.")
    st.markdown("- Choose a trend/topic (e.g., politics, exams, tech).")
    st.markdown("- Let AI generate a caption and create the meme.")

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    user_prompt = st.text_area("💬 Enter meme idea or description")

with col2:
    uploaded_image = st.file_uploader("📷 Or upload a meme image", type=["jpg", "jpeg", "png"])

trend = st.text_input("🔥 Mention the trend/topic (e.g., ChatGPT, elections, IPL, Gen Z)", value="general")

if st.button("🎯 Generate Meme"):
    if not user_prompt and not uploaded_image:
        st.error("❗ Please provide a prompt or upload an image.")
    else:
        full_prompt = f"Generate a sarcastic, trending meme caption related to '{trend}'. Idea: {user_prompt}"
        gpt_caption = fetch_model_response(full_prompt, "GPT 4o mini")
        deepseek_caption = fetch_model_response(full_prompt, "Deepseek")
        final_caption = gpt_caption if len(gpt_caption) > len(deepseek_caption) else deepseek_caption

        st.subheader("📝 Meme Caption")
        st.success(final_caption.strip())

        if uploaded_image:
            image = Image.open(uploaded_image).convert("RGB")
        else:
            image = Image.new("RGB", (600, 400), color="black")

        meme_img = generate_meme(image.copy(), final_caption.strip())
        st.image(meme_img, caption="Your Meme", use_column_width=True)
