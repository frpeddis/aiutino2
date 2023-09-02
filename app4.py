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
    label="Upload an image, take one with your camera, or load image from a URL",
    options=("Upload an image ⬆️", "Take a photo with my camera 📷", "Load image from a URL 🌐"),
)

if option == "Take a photo with my camera 📷":
    upload_img = st.camera_input(label="Take a picture")
    mode = "camera"

elif option == "Upload an image ⬆️":
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
        img_arr = np.asarray(pil_img)

        # Display original image
        #st.image(img_arr, use_column_width="auto", caption="Uploaded Image")

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
        #if st.button("↩️ Reset Rotation", use_container_width=True):
        #    st.success("Rotation reset to original!")
        
        # ---------- CROP ----------
        st.text("Crop image ✂️")
        cropped_img = st_cropper(rotated_img, should_resize_image=True)
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
        # ---------- FINAL OPERATIONS ----------
        
        
        #final_image.save("final_image.png")

        #with open("final_image.png", "rb") as file:
        #    st.download_button(
        #        "💾 Download final image",
        #        data=file,
        #        mime="image/png",
        #        use_container_width=True,
        #    )
