
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import uuid

st.title("AI-Powered Concept Test")

# Load Concept Image
image = Image.open("concept.png")
st.image(image, caption="Concept Image", use_container_width=True)

# Collect Initial Feedback
like = st.text_area("💚 What do you like about this concept?")
dislike = st.text_area("💔 What do you dislike about this concept?")
rating = st.slider("⭐ Rate this concept (1-10)", 1, 10, 5)

# Ask for Changes
st.subheader("Suggest Changes")
modify = st.checkbox("I want to modify the concept image")

change_color = None
new_text = None
text_position = None
use_openai = False
openai_api_key = ""
openai_prompt = ""

if modify:
    change_color = st.color_picker("Pick a new background color")
    new_text = st.text_input("New text to display")
    text_position = st.radio("Text Position", ["Top", "Center", "Bottom"])
    
    use_openai = st.checkbox("I want to use my OpenAI API key for advanced changes")
    if use_openai:
        openai_api_key = st.text_input("Enter your OpenAI API Key (optional)", type="password")
        openai_prompt = st.text_area("Describe your advanced changes using AI")

# Submit Button
if st.button("Submit Response"):
    record = {
        "id": str(uuid.uuid4()),
        "like": like,
        "dislike": dislike,
        "rating": rating,
        "modify": modify,
        "change_color": change_color,
        "new_text": new_text,
        "text_position": text_position,
        "use_openai": use_openai,
        "openai_api_key": "Provided" if openai_api_key else "Not Provided",
        "openai_prompt": openai_prompt
    }
    
    # Save Responses
    try:
        df = pd.read_csv("responses.csv")
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame([record])
    df.to_csv("responses.csv", index=False)
    st.success("Response Saved Successfully ✅")

    # Show modified image (only after submission)
    modified_image = image.copy()
    if modify:
        if change_color:
            bg = Image.new("RGB", image.size, change_color)
            bg.paste(modified_image, (0, 0), modified_image.convert('RGBA'))
            modified_image = bg

        if new_text:
            draw = ImageDraw.Draw(modified_image)
            font = ImageFont.load_default()
            w, h = modified_image.size
            if text_position == "Top":
                position = (10, 10)
            elif text_position == "Center":
                position = (w // 2 - 50, h // 2)
            else:
                position = (10, h - 30)
            draw.text(position, new_text, fill="white", font=font)

    st.subheader("Modified Image (after applying your changes)")
    st.image(modified_image, caption="Modified Concept Image", use_container_width=True)

    if use_openai:
        st.warning("Note: OpenAI API changes are not yet implemented. Placeholder for future AI-powered edits.")

else:
    st.info("Fill the form and click Submit to apply changes.")
