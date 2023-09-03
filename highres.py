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

# Embed the HTML page
st.markdown(
    f'<iframe src="camera.html" width="700" height="600"></iframe>',
    unsafe_allow_html=True,
)

# Hidden input to store base64 string
img_data_url = st.text_area("Image Data URL", "", key="base64input", max_chars=None, height=0)

if img_data_url:
    # Remove data URL prefix and convert base64 data to PIL Image
    img_data = base64.b64decode(img_data_url.split(",")[1])
    img = Image.open(BytesIO(img_data))
    st.image(img, caption="Captured High-Resolution Image", use_column_width=True)
