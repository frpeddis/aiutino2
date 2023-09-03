import streamlit as st
from PIL import Image
import base64
from io import BytesIO

# Ensure this is at the top of your file
st.set_page_config(
    page_title="High-Resolution Image Capture",
    page_icon="📷",
    layout="wide",
)

st.title("High-Resolution Image Capture Example")

st.markdown(
    """
    <script>
    async function captureHighQualityImage() {
        const video = document.createElement('video');
        video.style.display = 'none';
        const stream = await navigator.mediaDevices.getUserMedia({video: {facingMode: 'user', width: {ideal: 4096}, height: {ideal: 2160}}});
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
        const inputElement = document.createElement('textarea');
        inputElement.value = imgDataUrl;
        inputElement.setAttribute('id', 'base64input');
        document.body.appendChild(inputElement);
    }
    </script>
    """,
    unsafe_allow_html=True,
)

# Capture Button
capture_button = st.button("Capture High-Res Image")

if capture_button:
    st.write(
        "<script type='text/javascript'>captureHighQualityImage()</script>",
        unsafe_allow_html=True,
    )

# Hidden input to store base64 string
img_data_url = st.text_area("Image Data URL", "", key="base64input", max_chars=None, height=0)

if img_data_url:
    # Remove data URL prefix and convert base64 data to PIL Image
    img_data = base64.b64decode(img_data_url.split(",")[1])
    img = Image.open(BytesIO(img_data))
    st.image(img, caption="Captured High-Resolution Image", use_column_width=True)
