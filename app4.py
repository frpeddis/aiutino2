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

st.title("🖼️ Welcome to Aiutino!")

# Image loading options
option = st.radio(
    "Upload an image, take one with your camera, or load image from a URL",
    ("Upload an image ⬆️", "Take a photo with my camera 📷", "Load image from a URL 🌐"),
)

upload_img = None
if option == "Take a photo with my camera 📷":
    upload_img = st.camera_input("Take a picture")
    mode = "camera"
elif option == "Upload an image ⬆️":
    upload_img = st.file_uploader("Upload an image", type=["bmp", "jpg", "jpeg", "png", "svg"])
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

with contextlib.suppress(NameError):
    if upload_img is not None:
        pil_img = upload_img.convert("RGB") if mode == "url" else Image.open(upload_img).convert("RGB")
        img_arr = np.array(pil_img)
        st.image(img_arr, use_column_width="auto", caption="Uploaded Image")

        degrees = st.slider("Drag slider to rotate image clockwise 🔁", min_value=0, max_value=360, value=0)
        rotated_img = pil_img.rotate(360 - degrees)

        cropped_img = st_cropper(rotated_img, should_resize_image=True)

        if st.checkbox("Use cropped Image?"):
            final_image = cropped_img
            st.write("Recognized Text")
            text = pytesseract.image_to_string(final_image)
            st.write(text)
            prompt = f"This is a text to analyze: {text}. First think step by step, then understand what is the topic of the text. You are an expert on that topic. Now give me your opinion about that topic."
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=200,
                temperature=0.2
            )
            
            st.write("GPT-3 Analysis")
            st.write(response.choices[0].text.strip())

        else:
            final_image = rotated_img
            st.write("Recognized Text")
            text = pytesseract.image_to_string(final_image)
            st.write(text)
            prompt = f"This is a text to analyze: {text}. First think step by step, then understand what is the topic of the text. You are an expert on that topic. Now give me your opinion about that topic."
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=200,
                temperature=0.2
            )
            
            st.write("GPT-3 Analysis")
            st.write(response.choices[0].text.strip())


        #st.image(final_image, use_column_width="auto", caption="Final Image")

