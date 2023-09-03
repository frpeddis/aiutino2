import streamlit as st
from PIL import Image
import base64
import io

# This should be the very first Streamlit command
st.set_page_config(
    page_title="High-Res Image Capture",
    page_icon="📷",
    layout="wide",
)

# Then the rest of your code
st.title("High-Resolution Image Capture Example")



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
        streamlit.setComponentValue('imgDataUrl', imgDataUrl);
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

# Get Data URL from JavaScript and convert to PIL Image
img_data_url = st.experimental_get_component_value("imgDataUrl")

if img_data_url is not None:
    img_data = base64.b64decode(img_data_url.split(",")[1])
    img = Image.open(io.BytesIO(img_data))
    st.image(img, caption="Captured Image", use_column_width=True)
