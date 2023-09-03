import contextlib
from io import BytesIO
import numpy as np
import requests
import streamlit as st
from PIL import Image
from streamlit_cropper import st_cropper
import openai
import pytesseract
import base64
import io

# Initialize GPT API (Replace with your actual API key)
openai.api_key = st.secrets["API_KEY"]

# Set tesseract cmd path
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
VERSION = "0.7.0"

# Inject JavaScript for high-quality image capture
st.markdown(
    """
    <script>
        async function captureHighQualityImage() {
            const video = document.createElement('video');
            video.style.display = 'none';
            const stream = await navigator.mediaDevices.getUserMedia({video: {facingMode: 'user', width: 1920, height: 1080}});
            
            document.body.appendChild(video);
            video.srcObject = stream;
            await video.play();

            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0);
            stream.getTracks().forEach(track => track.stop());

            const imgDataUrl = canvas.toDataURL('image/jpeg', 1.0);
            document.body.removeChild(video);
            
            return imgDataUrl;
        }
    </script>
    """,
    unsafe_allow_html=True,
)

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
    options=("Upload an image ⬆️", "Take a photo with my camera 📷", "Load image from a URL 🌐", "Take a high-quality photo with my camera 📷"),
)

if option == "Take a photo with my camera 📷":
    upload_img = st.camera_input(label="Take a picture")
    mode = "camera"

elif option == "Take a high-quality photo with my camera 📷":
    img_data_url = st.text_input("High Quality Image Data URL", value="", type="default")
    if st.button("Capture High Quality Image"):
        st.write(
            "<script>async function setFileInputFromCamera(){ let imgDataUrl = await captureHighQualityImage(); document.querySelector('input[data-testid=\"imgDataUrl\"]').value = imgDataUrl; }</script>",
            unsafe_allow_html=True,
        )
        st.write(
            "<button onclick=\"setFileInputFromCamera()\">Capture High Quality Image</button>",
            unsafe_allow_html=True,
        )
    if img_data_url:
        base64_data = img_data_url.split(",")[1]
        img_bytes = base64.b64decode(base64_data)
        upload_img = Image.open(io.BytesIO(img_bytes))
        mode = "camera_high_quality"

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
            if mode in ["url", "camera_high_quality"]
            else Image.open(upload_img).convert("RGB")
        )
        img_arr = np.asarray(pil_img)

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

        st.text("Crop image ✂️")
        cropped_img = st_cropper(rotated_img, should_resize_image=True)
        
        if st.checkbox(
            label="Use cropped Image?",
            help="Select to use the cropped image in further operations",
            key="crop",
        ):
            final_image = cropped_img
        else:
            final_image = rotated_img

        st.write("Recognized Text")
        text = pytesseract.image_to_string(final_image)
        st.write(text)

if st.button("Analyze with ChatGPT"):
    prompt = f"This is a text to analyze: {text}. Look for any questions contained in the text. First think step by step, try to understand what the context of the topic is. then act as a super expert in that topic. then give me the answer you consider correct"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=200
    )

    st.write("GPT-3 Analysis")
    st.write(response.choices[0].text.strip())
