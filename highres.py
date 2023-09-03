import streamlit as st
from PIL import Image
import base64
from io import BytesIO

st.title("High-Resolution Image Capture Example")

# JavaScript to handle high-res image capture
js_script = """
    <script>
        async function captureImage() {
            const video = document.createElement('video');
            video.style.display = 'none';
            const stream = await navigator.mediaDevices.getUserMedia({video: {facingMode: 'user', width: {ideal: 4096}, height: {ideal: 2160}}});
            video.srcObject = stream;
            await video.play();
            
            // Resize the output to fit the video element.
            google.colab.output.setIframeHeight(document.documentElement.scrollHeight, true);
            
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0);
            stream.getVideoTracks()[0].stop();
            return canvas.toDataURL('image/jpeg', quality=1.0);
        }
    </script>
"""

# Embed the JavaScript code
st.markdown(js_script, unsafe_allow_html=True)

# Button to capture image
if st.button("Capture from Camera"):
    js = "captureImage().then(dataUrl => document.getElementById('img_data').value = dataUrl);"
    st.markdown('<input type="hidden" id="img_data">', unsafe_allow_html=True)
    st.markdown(f"<button onclick='{js}'>Capture Image</button>", unsafe_allow_html=True)

# Hidden input to store base64 string
img_data_url = st.text_area("Image Data URL", "", key="base64input", max_chars=None, height=0)

if img_data_url:
    # Remove data URL prefix and convert base64 data to PIL Image
    img_data = base64.b64decode(img_data_url.split(",")[1])
    img = Image.open(BytesIO(img_data))
    st.image(img, caption="Captured High-Resolution Image", use_column_width=True)
