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
#openai.api_key = st.secrets["API_KEY"]
#st.set_page_config(page_title="Aiutino ")





# Set tesseract cmd path
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

st.set_page_config(
    page_title="Aiutino",
    page_icon="🖼️",
    layout="wide",
)

# ---------- HEADER ----------
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
    upload_img = st.file_uploader(
        "Upload an image", type=["bmp", "jpg", "jpeg", "png", "svg"]
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

with contextlib.suppress(NameError):
    if upload_img is not None:
        pil_img = upload_img.convert("RGB") if mode == "url" else Image.open(upload_img).convert("RGB")
        img_arr = np.array(pil_img)

        # Display original image
        st.image(img_arr, use_column_width="auto", caption="Uploaded Image")

        # Rotate
        degrees = st.slider(
            "Drag slider to rotate image clockwise 🔁",
            min_value=0,
            max_value=360,
            value=0,
            key="rotate_slider",
        )
        rotated_img = pil_img.rotate(360 - degrees)

        # Crop
        cropped_img = st_cropper(rotated_img, should_resize_image=True)

        # Final Image
        if st.checkbox("Use cropped Image?"):
            final_image = cropped_img
             
            # Perform OCR
            st.write("Recognized Text")
            text = pytesseract.image_to_string(final_image)
            st.write(text)

        
        else:
            final_image = rotated_img
            # Perform OCR
            st.write("Recognized Text")
            text = pytesseract.image_to_string(final_image)
            st.write(text)


        # Display final image
        st.image(final_image, use_column_width="auto", caption="Final Image")

        
       

        # Analyze text using ChatGPT and provide an opinion
        #if st.button("Analyze with ChatGPT"):
        #    prompt = f"This is a text to analyze: {text}. Look for any questions contained in the text. First think step by step, try to understand what the context of the topic is. then act as a super expert in that topic. then give me the answer you consider correct"
        #    response = openai.Completion.create(
        #        engine="text-davinci-002",
        #        prompt=prompt,
        #        max_tokens=200
        #    )

        #   st.write("GPT-3 Analysis")
        #   st.write(response.choices[0].text.strip())
