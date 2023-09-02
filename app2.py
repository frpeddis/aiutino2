from io import BytesIO
import numpy as np
import requests
import streamlit as st
from PIL import Image
from streamlit_cropper import st_cropper

st.set_page_config(
    page_title="Aiutino",
    page_icon="🖼️",
    layout="wide",
)

st.title("🖼️ Welcome to Aiutino!")

# Upload options
option = st.radio(
    label="Upload an image, take one with your camera, or load image from a URL",
    options=(
        "Upload an image ⬆️",
        "Take a photo with my camera 📷",
        "Load image from a URL 🌐",
    )
)

if option == "Take a photo with my camera 📷":
    upload_img = st.camera_input(
        label="Take a picture",
    )
    mode = "camera"

elif option == "Upload an image ⬆️":
    upload_img = st.file_uploader(
        label="Upload an image",
        type=["bmp", "jpg", "jpeg", "png", "svg"],
    )
    mode = "upload"

elif option == "Load image from a URL 🌐":
    url = st.text_input("Image URL")
    mode = "url"

    if url != "":
        try:
            response = requests.get(url)
            upload_img = Image.open(BytesIO(response.content))
        except:
            st.error("The URL does not seem to be valid.")

if 'upload_img' in locals():
    if upload_img is not None:
        pil_img = (
            upload_img.convert("RGB")
            if mode == "url"
            else Image.open(upload_img).convert("RGB")
        )
        img_arr = np.asarray(pil_img)

        st.image(img_arr, use_column_width="auto", caption="Uploaded Image")
        st.text(
            f"Original width = {pil_img.size[0]}px and height = {pil_img.size[1]}px"
        )

        # Crop Feature
        st.text("Crop image ✂️")
        cropped_img = st_cropper(Image.fromarray(img_arr), should_resize_image=True)
        st.text(
            f"Cropped width = {cropped_img.size[0]}px and height = {cropped_img.size[1]}px"
        )

        # Use Cropped Image or Original
        if st.checkbox(
            label="Use cropped Image?",
            help="Select to use the cropped image in further operations",
            key="crop",
        ):
            image = cropped_img
        else:
            image = Image.fromarray(img_arr)

        # Rotate Feature
        degrees = st.slider(
            "Drag slider to rotate image clockwise 🔁",
            min_value=0,
            max_value=360,
            value=0,
            key="rotate_slider",
        )
        rotated_img = image.rotate(360 - degrees)
        st.image(
            rotated_img,
            use_column_width="auto",
            caption=f"Rotated by {degrees} degrees clockwise",
        )

        if st.button("↩️ Reset Rotation"):
            st.success("Rotation reset to original!")
