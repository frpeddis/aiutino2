import contextlib
from io import BytesIO
import numpy as np
import requests
import streamlit as st
from PIL import Image
from streamlit_cropper import st_cropper
import openai
import pytesseract

# Initialize GPT API (Replace with your actual API key)
openai.api_key = st.secrets["API_KEY"]

# Set tesseract cmd path
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
VERSION = "0.7.0"

st.set_page_config(
    page_title="Aiutino",
    page_icon="🖼️",
    layout="wide",
)

# ---------- HEADER ----------
st.title("🖼️ Welcome to Aiutino!")

# Image loading options
option = st.radio(
    label="Upload an image or load image from a URL",
    options=("Upload an image ⬆️", "Load image from a URL 🌐"),
)

if option == "Upload an image ⬆️":
    upload_img = st.file_uploader(
        label="Upload an image", type=["bmp", "jpg", "jpeg", "png", "svg"]
    )
    mode = "upload"

elif option == "Load image from a URL 🌐":
    url = st.text_input("Image URL", key="url")
    mode = "url"

    if url != "":
        try:
            response = requests.get(url)
            upload_img = Image.open(BytesIO(response.content))
        except:
            st.error("The URL does not seem to be valid.")

# Process image and apply operations
with contextlib.suppress(NameError):
    if upload_img is not None:
        pil_img = (
            upload_img.convert("RGB")
            if mode == "url"
            else Image.open(upload_img).convert("RGB")
        )

        # ---------- ROTATE ----------
        degrees = st.slider(
            "Drag slider to rotate image clockwise 🔁",
            min_value=0,
            max_value=360,
            value=0,
            key="rotate_slider",
        )
        rotated_img = pil_img.rotate(360 - degrees)
        st.image(
            rotated_img,
            use_column_width="auto",
            caption=f"Rotated by {degrees} degrees clockwise",
        )
        
        # ---------- CROP ----------
        st.text("Crop image ✂️")
        aspect_ratio_tuple = (rotated_img.size[0], rotated_img.size[1])
        cropped_img = st_cropper(rotated_img, should_resize_image=True, aspect_ratio=aspect_ratio_tuple)
        st.text(
            f"Cropped width = {cropped_img.size[0]}px and height = {cropped_img.size[1]}px"
        )

        if st.checkbox(
            label="Use cropped Image?",
            help="Select to use the cropped image in further operations",
            key="crop",
        ):
            final_image = cropped_img
        else:
            final_image = rotated_img

        # Perform OCR
        st.write("Recognized Text")
        text = pytesseract.image_to_string(final_image)
        st.write(text)

# Analyze text using ChatGPT and provide an opinion
if st.button("Analyze with ChatGPT"):
    prompt = f"This is a text to analyze: {text}. First think step by step, try to understand what the context of the topic is. then act as a super expert in that topic with 30 years of experience. Then Look for any questions contained in the text and give me the answer you consider correct"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=200
    )

    st.write("GPT-3 Analysis")
    st.write(response.choices[0].text.strip())
