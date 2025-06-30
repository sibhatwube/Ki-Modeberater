# Fashion_GeniAI - Aapka Personal Stylist (Version 2)
# Yeh application ek image upload karne ya camera se photo lene par usme pehne gaye kapdo aur accessories ka analysis karti hai.
# Iske liye Google Gemini 1.5 Flash model ka istemal kiya gaya hai.

import streamlit as st
from PIL import Image
import google.generativeai as genai
import os

# --- Google API Key Configuration ---
# User dwara di gayi API key yahan set ki gayi hai.
# Suraksha ke liye, isey Streamlit Secrets me rakhna behtar hota hai, lekin request ke anusaar yahan direct dala gaya hai.
API_KEY = "AIzaSyCLR-6_0yS62F97deUqx31ozqeftKBOoBY"

try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"API Key configure karne me error aaya: {e}")
    st.error("Lütfen check karein ki API key sahi hai.")
    st.stop()


# --- Gemini Pro Vision Model Function ---
def get_gemini_vision_response(input_prompt, image):
    """
    Yeh function Gemini 1.5 Flash model ko call karta hai aur image se details nikalta hai.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        response = model.generate_content([input_prompt, image])
        return response.text
    except Exception as e:
        # Handle potential API errors, like invalid key or other issues
        st.error(f"Gemini API se response lene me error aaya: {e}")
        return None

# --- Streamlit App Layout ---

# Page ka title aur icon set karein
st.set_page_config(page_title="Fashion GeniAI", page_icon="👗", layout="wide")

# App ka main title
st.title("Fashion GeniAI - Aapka Personal Stylist 🤖✨")
st.write("Apni photo upload karein ya camera se photo lein aur dekhein AI aapke style ko kaise analyze karta hai!")

# Columns banayein: ek image ke liye, ek results ke liye
col1, col2 = st.columns(2)

image_source = None

with col1:
    st.header("1. Apni Photo Dein")
    
    # Tab banayein: ek upload ke liye, ek camera ke liye
    tab1, tab2 = st.tabs(["📁 Upload Karein", "📸 Camera Se Photo Lein"])

    with tab1:
        # File uploader widget
        uploaded_file = st.file_uploader("Ek image chunein...", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            image_source = uploaded_file

    with tab2:
        # Camera input widget
        camera_photo = st.camera_input("Apni photo lene ke liye yahan click karein")
        if camera_photo:
            image_source = camera_photo

    # Agar image source mil gaya hai to use display karein
    if image_source is not None:
        image = Image.open(image_source)
        st.image(image, caption='Aapki Chuni Hui Image', use_column_width=True)


with col2:
    st.header("2. AI Analysis Dekhein")
    if image_source is not None:
        # Analyze button
        if st.button('Analyze Karein', use_container_width=True, type="primary"):
            with st.spinner('AI aapke style ko samajh raha hai...'):
                # Image ko process karne ke liye taiyar karein
                image_for_api = Image.open(image_source)

                # Gemini model ke liye prompt
                input_prompt = """
                Aap Fashion_GeniAI project ke liye ek expert fashion advisor hain.
                Is image ko dhyan se dekhein aur neeche diye gaye format me details provide karein.
                Jawab hamesha saaf aur points me dein.
                Agar koi cheez saaf na dikhe, to likhein 'Not Clearly Visible'.

                - **Gender**: (Male/Female/Other)
                - **Skin Tone**: (Jaise: Fair, Wheatish, Light Brown, Dark)
                - **Upper Wear Type**: (Jaise: T-Shirt, Formal Shirt, Kurti, Top, Jacket)
                - **Upper Wear Color**: (Pehne gaye kapde ka rang)
                - **Lower Wear Type**: (Jaise: Jeans, Trousers, Skirt, Shorts)
                - **Lower Wear Color**: (Pehne gaye kapde ka rang)
                - **Footwear Type**: (Jaise: Sneakers, Sandals, Heels, Formal Shoes, Chappal)
                - **Footwear Color**: (Jooton ka rang)
                - **Accessories**: (Jaise: Watch, Glasses, Handbag, Jewellery - agar dikhe to)
                - **Overall Vibe**: (Jaise: Casual, Formal, Party, Street Style, Ethnic)
                """

                # Gemini API ko call karein
                response_text = get_gemini_vision_response(input_prompt, image_for_api)
                
                # Result ko display karein
                if response_text:
                    st.subheader("✨ Analysis Results ✨")
                    st.markdown(response_text)

    else:
        st.info("Analysis dekhne ke liye, pehle ek photo upload karein ya camera se lein.")

# --- Footer ---
st.markdown("---")
st.write("Built with ❤️ for the Fashion_GeniAI Project.")
