import streamlit as st
from PIL import Image
import google.generativeai as genai
import warnings

# --- Google API Key Configuration ---
API_KEY = "AIzaSyCLR-6_0yS62F97deUqx31ozqeftKBOoBY"  # Manage API key securely

try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"Error configuring API key: {e}")
    st.error("Please check that your API key is correct.")
    st.stop()

# --- Gemini Pro Vision Model Function ---
def get_gemini_vision_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        response = model.generate_content([input_prompt, image])
        return response.text
    except Exception as e:
        st.error(f"Error getting response from Gemini API: {e}")
        return None

# --- Streamlit App Layout ---

st.set_page_config(
    page_title="Fashion GeniAI",
    page_icon="👗",
    layout="wide"
)

# Suppress warnings (optional, but not using deprecated options)
warnings.filterwarnings('ignore')

# App main title
st.title("Fashion GeniAI - Your Personal Stylist 🤖✨")
st.write("Upload your photo or take a photo with your camera and see how AI analyzes your style!")

# Columns: one for image, one for results
col1, col2 = st.columns(2)

image_source = None

with col1:
    st.header("1. Provide Your Photo")
    
    # Camera activation checkbox
    use_camera = st.checkbox("📸 Use Camera", value=False)

    if use_camera:
        # Camera input widget
        camera_photo = st.camera_input("Click here to take your photo")
        if camera_photo:
            image_source = camera_photo
    else:
        # File uploader widget
        uploaded_file = st.file_uploader("📁 Choose an image...", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            image_source = uploaded_file

    # If image source is available, display it
    if image_source is not None:
        image = Image.open(image_source)
        st.image(image, caption='Your Selected Image', use_container_width=True)

with col2:
    st.header("2. View AI Analysis")
    if image_source is not None:
        # Analyze button
        if st.button('Analyze', use_container_width=True, type="primary"):
            with st.spinner('AI is analyzing your style...'):
                image_for_api = Image.open(image_source)
                input_prompt = """
                You are an expert fashion advisor for the Fashion GeniAI project.
                Carefully analyze the image and provide details in the following format.
                Always answer clearly and in points.
                If something is not clearly visible, write 'Not Clearly Visible'.

                - **Gender**: (Male/Female/Other)
                - **Skin Tone**: (e.g., Fair, Wheatish, Light Brown, Dark)
                - **Upper Wear Type**: (e.g., T-Shirt, Formal Shirt, Kurti, Top, Jacket)
                - **Upper Wear Color**: (Color of the upper clothing)
                - **Lower Wear Type**: (e.g., Jeans, Trousers, Skirt, Shorts)
                - **Lower Wear Color**: (Color of the lower clothing)
                - **Footwear Type**: (e.g., Sneakers, Sandals, Heels, Formal Shoes, Slippers)
                - **Footwear Color**: (Color of the shoes)
                - **Accessories**: (e.g., Watch, Glasses, Handbag, Jewellery - if visible)
                - **Overall Vibe**: (e.g., Casual, Formal, Party, Street Style, Ethnic)
                """
                response_text = get_gemini_vision_response(input_prompt, image_for_api)
                if response_text:
                    st.subheader("✨ Analysis Results ✨")
                    st.markdown(response_text)
    else:
        st.info("To view analysis, please upload a photo or use your camera.")

# --- Footer ---
st.markdown("---")
st.write("Built with ❤️ for the Fashion GeniAI Project")
