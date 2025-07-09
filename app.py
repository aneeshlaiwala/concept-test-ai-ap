import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import uuid

st.title("AI-Powered Concept Test")

# Load Concept Image (PNG version)
image = Image.open("concept.png")
st.image(image, caption="Concept Image", use_column_width=True)

# Collect Feedback
like = st.text_area("💚 What do you like about this concept?")
dislike = st.text_area("💔 What do you dislike about this concept?")
rating = st.slider("⭐ Rate this concept (1-10)", 1, 10, 5)

# Ask for Changes
st.subheader("Suggest Changes")
modify = st.checkbox("I want to modify the concept image")

change_color = None
new_text = None
text_position = None

if modify:
    change_color = st.color_picker("Pick a new background color")
    new_text = st.text_input("New text to display")
    text_position = st.radio("Text Position", ["Top", "Center", "Bottom"])

    # Apply Changes to Image (Prototype)
    modified_image = image.copy()
    draw = ImageDraw.Draw(modified_image)

    if change_color:
        bg = Image.new("RGB", image.size, change_color)
        bg.paste(modified_image, (0, 0), modified_image.convert('RGBA'))
        modified_image = bg

    if new_text:
        font = ImageFont.load_default()
        w, h = modified_image.size
        if text_position == "Top":
            position = (10, 10)
        elif text_position == "Center":
            position = (w // 2 - 50, h // 2)
        else:
            position = (10, h - 30)
        draw.text(position, new_text, fill="white", font=font)

    st.image(modified_image, caption="Modified Image", use_column_width=True)

    # Collect Feedback on Modified Image
    like2 = st.text_area("💚 What do you like about the modified concept?")
    dislike2 = st.text_area("💔 What do you dislike about the modified concept?")
    rating2 = st.slider("⭐ Rate the modified concept (1-10)", 1, 10, 5)

else:
    like2 = dislike2 = rating2 = None

# Save Responses
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
        "like2": like2,
        "dislike2": dislike2,
        "rating2": rating2
    }
    try:
        df = pd.read_csv("responses.csv")
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame([record])
    df.to_csv("responses.csv", index=False)
    st.success("Response Saved Successfully ✅")
