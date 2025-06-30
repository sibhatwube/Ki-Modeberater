
import streamlit as st
from PIL import Image
import google.generativeai as genai
import warnings
import time

# --- Google API Key Configuration ---
# For deployment, ALWAYS use Streamlit Secrets to secure your API key:
# st.secrets["GOOGLE_API_KEY"]
# For local testing, you can temporarily use your key directly, but remove before sharing/deploying.
API_KEY = "AIzaSyCLR-6_0yS62F97deUqx31ozqeftKBOoBY" # <<< IMPORTANT: REPLACE WITH YOUR ACTUAL GOOGLE GEMINI API KEY

if API_KEY == "YOUR_GEMINI_API_KEY" or not API_KEY:
    st.error("❌ Google Gemini API Key Missing!")
    st.error("Please enter your actual Google Gemini API key in the 'API_KEY' variable or use Streamlit Secrets.")
    st.stop()

try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"❌ Error configuring Gemini API: {e}")
    st.error("Please check that your API key is correct and has the necessary permissions.")
    st.stop()

# --- Gemini Model Functions ---
def get_gemini_vision_response(input_prompt, image):
    """Generates a response from Gemini 1.5 Flash Vision model for image analysis."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        with st.spinner("Saundarya is meticulously analyzing your image... ✨"):
            response = model.generate_content([input_prompt, image])
            if hasattr(response, 'text'):
                return response.text
            elif response.parts and hasattr(response.parts[0], 'text'):
                return response.parts[0].text
            else:
                st.warning("Gemini API response did not contain directly accessible text. Retrying for clarity...")
                return "AI response not clear. Please try again."
    except Exception as e:
        st.error(f"❌ Error getting response from Gemini API: {e}")
        st.error("Please try again later or check your network connection.")
        return None

def get_gemini_text_response(input_prompt):
    """Generates a response from Gemini 1.5 Flash model for text-based queries."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        with st.spinner("Saundarya is curating the perfect insights for you... 🤔"):
            response = model.generate_content(input_prompt)
            if hasattr(response, 'text'):
                time.sleep(0.7) # Slightly longer delay for richer content
                return response.text
            elif response.parts and hasattr(response.parts[0], 'text'):
                time.sleep(0.7)
                return response.parts[0].text
            else:
                st.warning("Gemini API response did not contain directly accessible text. Retrying for clarity...")
                return "AI response not clear. Please try again."
    except Exception as e:
        st.error(f"❌ Error getting response from Gemini API: {e}")
        st.error("Please try again later or check your network connection.")
        return None

# --- Streamlit App Configuration ---
st.set_page_config(
    page_title="Saundarya - Your Personal AI Stylist",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Suppress warnings
warnings.filterwarnings('ignore')

# --- Custom CSS for enhanced UI and unique look ---
st.markdown("""
    <style>
    /* Overall App Styling */
    .stApp {
        background: linear-gradient(to right, #1a1a2e, #16213e); /* Deep, dark blue gradient */
        color: #e0e0e0; /* Light gray for main text */
        font-family: 'Open Sans', sans-serif; /* Modern, readable font */
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #e94560; /* Vibrant Rose Red for headings */
        font-family: 'Playfair Display', serif; /* Elegant and distinctive font */
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #5a189a; /* Deep purple accent line */
    }
    h1 {
        font-size: 3rem;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    h2 {
        font-size: 2.4rem;
        color: #c951ed; /* Lighter purple for sub-headings */
    }
    h3 {
        font-size: 1.8rem;
        color: #f0f0f0; /* Near white for section headings */
    }

    /* Sidebar Styling */
    .stSidebar {
        background-color: #0f3460; /* Darker blue for sidebar */
        padding: 20px;
        border-right: 2px solid #5a189a; /* Deep purple border */
        box-shadow: 2px 0 10px rgba(0,0,0,0.5); /* Stronger shadow */
    }
    .stSidebar .stRadio > label {
        font-size: 1.15rem;
        font-weight: 600;
        color: #c951ed; /* Lighter purple for sidebar text */
        padding: 10px 0;
        transition: color 0.3s ease;
    }
    .stSidebar .stRadio > label:hover {
        color: #e94560; /* Rose Red on hover */
    }
    .stSidebar .stRadio div[role="radiogroup"] label[data-baseweb="radio"] {
        padding: 8px 0; /* Adjust padding for radio buttons */
    }

    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 0.75rem;
        padding: 0.9rem 1.4rem;
        font-size: 1.2rem;
        font-weight: bold;
        background-color: #5a189a; /* Deep purple for primary button */
        color: white;
        border: none;
        transition: background-color 0.3s ease, transform 0.2s ease;
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
    .stButton>button:hover {
        background-color: #c951ed; /* Lighter purple on hover */
        transform: translateY(-3px); /* More pronounced lift effect */
        color: #1a1a2e; /* Dark text on hover for contrast */
    }

    /* Info/Warning/Error boxes */
    .stAlert {
        border-radius: 0.75rem;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 5px solid;
        color: #e0e0e0 !important; /* Ensure alert text is light */
    }
    .stAlert.info { border-color: #1abc9c; background-color: rgba(26, 188, 156, 0.2); } /* Teal */
    .stAlert.warning { border-color: #f39c12; background-color: rgba(243, 156, 18, 0.2); } /* Orange */
    .stAlert.error { border-color: #e74c3c; background-color: rgba(231, 76, 60, 0.2); } /* Red */

    /* Text Inputs, Selectboxes, Sliders */
    .stTextInput>div>div>input, .stSelectbox>div>div, .stSlider>div>div>div {
        border-radius: 0.6rem;
        border: 1px solid #5a189a; /* Purple border */
        padding: 0.6rem;
        background-color: #2e2e42; /* Slightly lighter dark background for inputs */
        color: #e0e0e0; /* Light text in inputs */
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
    }
    .stSelectbox>div>div {
        background-color: #2e2e42;
    }
    .stSelectbox>div>div>span { /* Text inside selectbox */
        color: #e0e0e0;
    }
    .stSlider .st-bd .st-eg { /* Slider track color */
        background-color: #5a189a;
    }
    .stSlider .st-bd .st-dx { /* Slider thumb color */
        background-color: #e94560;
    }

    /* Main Content Area Padding */
    .block-container {
        padding-top: 2rem;
        padding-right: 3rem;
        padding-left: 3rem;
        padding-bottom: 2rem;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #2e2e42; /* Darker header for expander */
        color: #e94560; /* Rose Red text */
        font-weight: bold;
        border-radius: 0.75rem;
        padding: 0.8rem 1.2rem;
        margin-bottom: 0.75rem;
        border: 1px solid #5a189a;
        transition: background-color 0.3s ease;
    }
    .streamlit-expanderHeader:hover {
        background-color: #3e3e52; /* Slightly lighter on hover */
        cursor: pointer;
    }
    .streamlit-expanderContent {
        background-color: #16213e; /* Matches main app background */
        padding: 1.2rem;
        border-left: 4px solid #c951ed; /* Lighter purple accent */
        border-bottom-left-radius: 0.75rem;
        border-bottom-right-radius: 0.75rem;
        color: #e0e0e0; /* Light text for content */
    }

    /* Image captions */
    .stImage > figcaption {
        color: #e0e0e0;
        font-style: italic;
        text-align: center;
        margin-top: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)


# --- Navigation Setup (Sidebar) ---
st.sidebar.title("🌸 Saundarya Menu")
st.sidebar.markdown("Explore our exquisite fashion insights:")
page_selection = st.sidebar.radio(
    "Choose Your Path",
    ["Analyze My Style", "Fashion Trends", "Style Inspiration", "Virtual Try-On (Future)", "About Saundarya"]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip**: Start your personalized fashion journey by selecting 'Analyze My Style' to receive instant insights!")
st.sidebar.markdown("Crafted with ❤️ by Saundarya Project Team.")

# --- Page Content Based on Selection ---

# --- Analyze My Style Page ---
if page_selection == "Analyze My Style":
    st.title("👗 Saundarya: Your Personal Style Analyzer")
    st.markdown("""
    Upload your photo or capture one with your camera, and let **Saundarya**, your AI stylist, delve into your look.
    Receive **meticulously crafted personalized recommendations** to elevate your style!
    """)
    st.markdown("---")

    col1, col2 = st.columns([1, 1])
    image_source = None

    with col1:
        st.header("📸 1. Provide Your Photo")
        st.markdown("Kindly provide an image of yourself or the outfit you wish to analyze. A clear, well-lit photo will yield the best results.")

        use_camera = st.checkbox("Use Device Camera", value=False, help="Check this to use your device's camera for a live capture.")

        if use_camera:
            camera_photo = st.camera_input("Click here to snap your photo")
            if camera_photo:
                image_source = camera_photo
                st.success("Photo captured! Ready for analysis. ✅")
        else:
            uploaded_file = st.file_uploader("Choose an image file...", type=["jpg", "jpeg", "png"], help="Supported formats: JPG, JPEG, PNG.")
            if uploaded_file:
                image_source = uploaded_file
                st.success("Image successfully uploaded! ✅")

        if image_source is not None:
            try:
                image = Image.open(image_source)
                st.image(image, caption='Your Selected Image', use_container_width=True)
                st.markdown("---")
            except Exception as e:
                st.error(f"❌ Error loading image: {e}. Please try a different, valid image file.")
                image_source = None

    with col2:
        st.header("🌟 2. Refine Your Analysis & Get Recommendations")
        if image_source is not None:
            st.subheader("Specify the Occasion:")
            occasion = st.selectbox(
                "Tailor recommendations for:",
                ("Everyday Casual", "Formal Event", "Party/Night Out", "Business Professional",
                 "Traditional/Ethnic", "Sporty/Active Wear", "Vacation/Travel", "Date Night", "Job Interview", "Cultural Festival"),
                help="Selecting an occasion helps Saundarya provide more relevant and precise fashion advice."
            )

            st.subheader("AI Confidence Level:")
            confidence_level = st.slider(
                "How much creative freedom should Saundarya have? (Lower = more practical, Higher = more adventurous)",
                min_value=0.5, max_value=1.0, value=0.8, step=0.05,
                help="Adjust this to influence the AI's creativity versus directness in its recommendations."
            )
            st.info(f"Saundarya's creative recommendation focus: **{int(confidence_level * 100)}%**")

            if st.button('🚀 Get Saundarya\'s Style Analysis & Recommendations', use_container_width=True, type="primary"):
                with st.spinner('Saundarya is meticulously analyzing your style and generating bespoke recommendations... This might take a moment. Please be patient.'):
                    image_for_api = Image.open(image_source)
                    
                    input_prompt = f"""
                    You are an extremely discerning, creative, and highly skilled personal fashion stylist named 'Saundarya' for the Fashion GeniAI project. Your ultimate goal is to provide a comprehensive, actionable, and profoundly inspiring fashion report based on the user's uploaded image.

                    Perform a meticulous visual analysis of every detail in the image. Subsequently, offer insightful, personalized, and transformative fashion recommendations that are perfectly tailored to the '{occasion}' occasion. Emphasize uniqueness, elegance, and practicality in your advice.

                    ---
                    ## 📝 Saundarya's Personalized Fashion Report

                    Based on your photo, here's an insightful analysis and our expertly tailored advice:

                    ### **1. Initial Style Assessment:**
                    - **Detected Gender**: (Male/Female/Non-Binary/Not Clearly Visible from outfit)
                    - **Estimated Skin Tone**: (e.g., Fair, Medium, Olive, Dark - state 'Not Clearly Visible' if ambiguous)
                    - **Body Silhouette (General)**: (e.g., Lean, Average, Athletic, Curvy - based on visible clothing fit. Avoid intrusive details. If unclear, state 'Not Clearly Visible')
                    - **Hair Style & Color**: (e.g., Short Wavy Blonde Bob, Long Straight Black Hair, Styled Pompadour - state 'Not Clearly Visible' if ambiguous)
                    - **Overall Current Aesthetic/Vibe**: (e.g., Effortlessly Casual, Sophisticated Urban, Bohemian Chic, Polished Business, Sporty & Dynamic. Be highly descriptive and insightful!)

                    ### **2. Detailed Outfit Breakdown:**
                    - **Upper Wear**:
                        - **Type**: (e.g., Collared button-down shirt, Cropped knit sweater, Structured blazer)
                        - **Color/Pattern**: (Specific shade, e.g., Emerald Green, Dusty Rose; and pattern, e.g., Subtle pinstripe, Bold floral, Solid)
                        - **Fit & Style**: (e.g., Relaxed fit, Slim-fit, Oversized, Tailored, Drapey)
                    - **Lower Wear**:
                        - **Type**: (e.g., High-waisted wide-leg trousers, Distressed skinny jeans, A-line midi skirt)
                        - **Color/Pattern**: (Specific shade and pattern)
                        - **Fit & Style**: (e.g., Tailored, Flowy, Figure-hugging)
                    - **Footwear**:
                        - **Type**: (e.g., Classic white sneakers, Stiletto heels, Leather loafers, Combat boots)
                        - **Color/Material**: (Detailed color and primary material, e.g., Tan suede, Patent black leather)
                    - **Accessories (Elaborate on each visible item)**: (e.g., Delicate layered gold necklaces, Oversized cat-eye sunglasses, Structured top-handle bag, Minimalist watch, Statement earrings. If none, state 'No prominent accessories visible')

                    ### **3. Saundarya's Transformative Recommendations for '{occasion}':**
                    Considering your unique current look and the selected '{occasion}', here are Saundarya's expert suggestions to truly elevate your ensemble:

                    -   **🎯 Core Style Enhancement**: Based on Saundarya's **{confidence_level}** confidence focus, propose the single most impactful adjustment or addition. This could be introducing a strategic layering piece, a particular type of footwear, or a bold statement accessory that ties the whole look together for the occasion.
                    -   **🎨 Harmonizing Colors & Textures**: Suggest a sophisticated color palette (e.g., monochromatic neutrals with a pop of jewel tone, earthy tones, pastels) or introduce a luxurious texture (e.g., silk, velvet, cashmere, linen) that would seamlessly integrate with your current style and enhance the '{occasion}' vibe.
                    -   **👟 Elevated Footwear & Accessory Pairing**: Advise on the perfect footwear and 1-2 specific, impactful accessories (e.g., a chic belt, a designer clutch, a pair of elegantly designed eyeglasses) that will complete the recommended '{occasion}' outfit with flair.
                    -   **🌟 The "Saundarya Spark" - Our Signature Touch**: Offer a unique, often-overlooked styling trick or a subtle detail that can dramatically transform the look (e.g., mastering the French tuck, rolling up sleeves just so, adding a pocket square, a unique way to layer necklaces). This is where your individual style truly shines.
                    -   **❌ Constructive Reconsideration**: Gently highlight any element in your current outfit that might subtly detract from the ideal '{occasion}' look, and explain why. Frame this as an opportunity for refinement.

                    ### **4. Connecting with Current Fashion Narratives:**
                    -   **Trend Alignment**: Does your current outfit resonate with any significant fashion trends of 2024-2025 (e.g., Quiet Luxury, Dopamine Dressing, Sustainable Minimalism, Coastal Grandmother, Grunge Revival, Oversized Silhouettes)? Briefly explain the connection.
                    -   **Introducing New Horizons**: Suggest one emerging or highly relevant trend that you could effortlessly integrate into your existing wardrobe, helping you stay fresh, modern, and fashion-forward. Provide actionable steps for incorporation.

                    ---
                    **Remember**: Fashion is a powerful form of self-expression. Use Saundarya's insights as a sophisticated guide to boldly explore and confidently refine your personal style.
                    """
                    response_text = get_gemini_vision_response(input_prompt, image_for_api)
                    
                    if response_text:
                        st.subheader("✨ Saundarya's AI-Powered Style Report ✨")
                        st.markdown(response_text)
                        
                        st.markdown("---")
                        st.info("💡 **Tip**: Experiment with different photos, occasions, and confidence levels to uncover diverse and exciting fashion insights!")
                    else:
                        st.warning("No analysis generated. Please ensure your image is clear and try again.")
        else:
            st.info("To unlock Saundarya's analysis and recommendations, please upload a photo or capture one using your camera in the left panel first.")

# --- Fashion Trends Page ---
elif page_selection == "Fashion Trends":
    st.title("📈 Saundarya: Discovering the Pulse of Fashion Trends")
    st.markdown("""
    Stay effortlessly ahead of the curve! Here, **Saundarya** curates the most impactful and exciting fashion trends for **2024-2025**.
    Dive deep into what's shaping the world of style.
    """)
    st.markdown("---")

    trend_options = [
        "Quiet Luxury", "Dopamine Dressing", "Sustainable Fashion",
        "Utility Wear", "Y2K Revival", "Maximalism", "Athleisure Evolution",
        "Retro Sportswear", "Tailored Essentials", "Texture Play", "Gender-Fluid Fashion"
    ]
    
    selected_trend = st.selectbox("Select a prominent trend to explore in detail:", trend_options)

    if st.button(f"Unveil '{selected_trend}' Insights", type="primary"):
        with st.spinner(f"Saundarya is meticulously researching '{selected_trend}' trends for you..."):
            trend_prompt = f"""
            You are an expert fashion journalist and trend forecaster for Fashion GeniAI, named 'Saundarya'.
            Provide a comprehensive and engaging overview of the fashion trend: '{selected_trend}'.
            Structure your response with clear headings and bullet points for excellent readability.

            ## Trend Spotlight: '{selected_trend}'

            ### **What Defines This Trend?**
            - A concise, captivating definition of the trend.
            - What is its core philosophy or aesthetic?

            ### **Key Characteristics & Elements:**
            - **Colors**: Dominant color palettes or surprising color combinations.
            - **Silhouettes**: Characteristic shapes and forms (e.g., oversized, fitted, flowing).
            - **Fabrics & Materials**: Popular textures and textiles (e.g., satin, denim, organic cotton, tech fabrics).
            - **Key Garments**: Specific clothing items that embody this trend (e.g., oversized blazers, cargo pants, slip dresses).
            - **Details**: Unique embellishments or finishing touches.

            ### **How to Elegantly Incorporate This Trend:**
            - Provide 3-5 practical, actionable tips on how an average person can seamlessly integrate this trend into their existing wardrobe, from subtle touches to bold statements.
            - Offer ideas for various comfort levels and personal styles.

            ### **Who Is This Trend For?**
            - Describe the type of individual or lifestyle this trend naturally appeals to.
            - Are there specific occasions or demographics that would particularly embrace it?

            ### **Future Outlook & Longevity:**
            - Is this a fleeting micro-trend, a seasonal staple, or a long-term shift in fashion?
            - What factors might influence its evolution or decline?

            Please ensure all details are precise, informative, and presented with a sophisticated fashion tone.
            """
            trend_info = get_gemini_text_response(trend_prompt)
            if trend_info:
                st.subheader(f"Understanding: {selected_trend}")
                st.markdown(trend_info)
            else:
                st.warning("Could not retrieve detailed information about this trend. Please try again.")
    
    st.markdown("---")
    st.info("Explore different trends to stay updated on the ever-evolving world of fashion!")

# --- Style Inspiration Page ---
elif page_selection == "Style Inspiration":
    st.title("💡 Saundarya: Your Wellspring of Style Inspiration")
    st.markdown("""
    Unleash your creativity and discover new dimensions of personal style!
    **Saundarya** provides curated inspiration from diverse themes, iconic celebrity looks, and seasonal aesthetics.
    """)
    st.markdown("---")

    inspiration_type = st.radio(
        "What kind of inspiration are you seeking today?",
        ("Style Theme", "Celebrity Look", "Seasonal Style"),
        horizontal=True
    )

    if inspiration_type == "Style Theme":
        theme = st.selectbox(
            "Select an intriguing Style Theme:",
            ["Minimalist Chic", "Boho-Glam", "Vintage Revival", "Edgy Street Style", "Classic Elegance", "Futuristic Avant-Garde", "Dark Academia"],
            help="Choose a theme to receive tailored stylistic guidance."
        )
        if st.button(f"Inspire Me with '{theme}' Style"):
            with st.spinner(f"Saundarya is generating captivating inspiration for '{theme}' style..."):
                inspiration_prompt = f"""
                You are an inspirational style consultant for Fashion GeniAI, named 'Saundarya'.
                Provide comprehensive and artistic inspiration based on the style theme: '{theme}'.
                Structure your response with clear headings and bullet points for enhanced readability.

                ## Style Essence: '{theme}'

                ### **Core Concept & Vibe:**
                - What is the fundamental essence and overall feeling this style conveys?
                - Describe its unique aura.

                ### **Key Wardrobe Essentials:**
                - List and briefly describe 3-5 crucial clothing pieces that are foundational to this theme.
                - Focus on versatility and impact.

                ### **Signature Accessories:**
                - Which accessories are indispensable for perfecting this look?
                - How do they contribute to the overall aesthetic?

                ### **Recommended Color Palette & Textures:**
                - Suggest a primary color palette and any accent colors that define this style.
                - Highlight key fabrics and textures that evoke the theme's feel.

                ### **Saundarya's Styling Mastery Tip:**
                - Offer a unique, expert tip or a nuanced approach to truly master this style and make it your own.
                """
                inspiration_info = get_gemini_text_response(inspiration_prompt)
                if inspiration_info:
                    st.subheader(f"Style Theme: {theme}")
                    st.markdown(inspiration_info)
                else:
                    st.warning("Could not generate inspiration for this theme. Please try again.")

    elif inspiration_type == "Celebrity Look":
        celeb_name = st.text_input("Enter a Celebrity's Full Name (e.g., Zendaya, Timothée Chalamet, Rihanna):")
        if st.button(f"Analyze {celeb_name}'s Iconic Style"):
            if celeb_name:
                with st.spinner(f"Saundarya is meticulously analyzing {celeb_name}'s style legacy..."):
                    celeb_prompt = f"""
                    You are a highly knowledgeable celebrity stylist and fashion critic for Fashion GeniAI, named 'Saundarya'.
                    Provide an in-depth analysis of the general fashion style of celebrity '{celeb_name}' and explore some of their most iconic or signature looks.
                    Structure your response with clear headings and bullet points for readability.

                    ## Celebrity Style File: {celeb_name}

                    ### **Their Signature Aesthetic:**
                    - Describe their overall fashion philosophy and the general vibe they project through their clothing.
                    - Is it consistent, or do they famously reinvent their style?

                    ### **Key Signature Pieces & Trends:**
                    - List 3-5 specific clothing items, silhouettes, or accessories that they are known for or frequently wear.
                    - Mention any fashion trends they've pioneered or famously embraced.

                    ### **Color & Fabric Preferences:**
                    - Do they have a noticeable preferred color palette? Are they known for bold colors, neutrals, or specific patterns?
                    - What fabrics or textures do they seem to favor?

                    ### **Saundarya's Insight: How to Get Inspired:**
                    - Offer 3 practical, actionable, and budget-friendly ways for a regular person to draw inspiration from '{celeb_name}'s style and incorporate elements into their own wardrobe.
                    - Focus on transferable concepts rather than exact replicas.

                    ### **Memorable Fashion Moments (Optional, if applicable):**
                    - Briefly mention 1-2 particularly iconic outfits or red-carpet moments that define their fashion journey.
                    """
                    celeb_info = get_gemini_text_response(celeb_prompt)
                    if celeb_info:
                        st.subheader(f"Decoding {celeb_name}'s Style")
                        st.markdown(celeb_info)
                    else:
                        st.warning(f"Could not retrieve detailed style information for {celeb_name}. Please verify the name or try another.")
            else:
                st.warning("Please enter a celebrity's full name to get style insights.")
    
    elif inspiration_type == "Seasonal Style":
        season = st.selectbox(
            "Select a Season for Fresh Tips:",
            ["Spring", "Summer", "Autumn", "Winter"],
            help="Get Saundarya's curated fashion tips perfectly suited for each season."
        )
        if st.button(f"Unlock '{season}' Style Tips"):
            with st.spinner(f"Saundarya is crafting sophisticated style tips for '{season}'..."):
                seasonal_prompt = f"""
                You are a highly insightful seasonal fashion expert for Fashion GeniAI, named 'Saundarya'.
                Provide comprehensive and practical style tips specifically tailored for the season: '{season}'.
                Structure your response with clear headings and bullet points for excellent readability.

                ## Seasonal Style Guide: {season}

                ### **Essential Wardrobe Staples:**
                - What 3-5 key clothing items are absolutely crucial for comfort and style in this season?
                - Consider both versatility and seasonal appropriateness.

                ### **Recommended Color Palettes & Textures:**
                - Which color schemes (e.g., brights, muted tones, jewel tones) and fabrics (e.g., linen, wool, silk, cotton) are ideal for this season?
                - Explain why these choices work well.

                ### **Mastering Layering (If Applicable):**
                - Provide specific, actionable advice on effective layering strategies for the season's fluctuating temperatures.
                - Suggest combinations of garments.

                ### **Perfecting with Accessories:**
                - What season-specific accessories (e.g., scarves, sunglasses, hats, jewelry) can elevate outfits and add a stylish touch?

                ### **Saundarya's Seasonal Style Tip:**
                - Offer a unique, practical tip or a subtle trick that will help the user truly excel in their style for this specific season.

                ### **What to Thoughtfully Avoid:**
                - Briefly mention any clothing items, fabrics, or styling choices that are generally less suitable or comfortable for this season, and why.
                """
                seasonal_info = get_gemini_text_response(seasonal_prompt)
                if seasonal_info:
                    st.subheader(f"Saundarya's Guide to {season} Style")
                    st.markdown(seasonal_info)
                else:
                    st.warning("Could not generate seasonal tips. Please try again.")

    st.markdown("---")
    st.info("Let Saundarya ignite your imagination and transform your style journey!")

# --- Virtual Try-On (Future) Page ---
elif page_selection == "Virtual Try-On (Future)":
    st.title("👗 Virtual Try-On - Revolutionizing Your Wardrobe (Coming Soon!) 🚀")
    st.markdown("""
    Envision a world where you can effortlessly try on any outfit without a single change of clothes!
    **Saundarya's Virtual Try-On** feature is poised to redefine your fashion exploration and shopping experience.
    
    ### **The Vision: How it will work (Concept):**
    1.  **Seamless Photo Upload:** Simply upload a clear, full-body photograph of yourself.
    2.  **Expansive Virtual Wardrobe:** Browse through an extensive, curated collection of virtual clothing items – from haute couture to everyday essentials.
    3.  **Real-time Visualization:** Our cutting-edge AI will ingeniously overlay the selected outfit onto your photo. It will intelligently adapt to your unique body shape, posture, and lighting, providing an exceptionally realistic preview.
    
    ### **Why This Will Be a Game-Changer:**
    -   **Unprecedented Time-Saving:** Bid farewell to traditional changing rooms and endless queues!
    -   **Empowered Decision-Making:** Gain absolute clarity on how clothes truly drape, fit, and complement your figure before making any purchase.
    -   **Boundless Style Experimentation:** Fearlessly explore bold new looks, experiment with daring combinations, and discover your next signature style without any commitment.
    
    This groundbreaking feature is currently under active research and development, leveraging the very latest in AI and computer vision. We are dedicated to bringing this transformative experience to you soon.
    """)
    
    st.image("https://via.placeholder.com/800x400?text=Saundarya+Virtual+Try-On+Future+Vision", caption="A Glimpse into the Future: Virtual Try-On Concept by Saundarya")
    st.markdown("---")
    st.info("We are tirelessly working to bring this innovative and thrilling feature to your fingertips! Stay tuned for more.")

# --- About Saundarya Page ---
elif page_selection == "About Saundarya":
    st.title("ℹ️ About Saundarya: Your Connoisseur of Personal Style")
    st.markdown("""
    Welcome to **Saundarya**, your quintessential personal AI stylist, meticulously powered by the revolutionary **Google Gemini technology**!
    
    Our profound mission is to democratize the art of fashion advice, making sophisticated, personalized styling exquisitely accessible to everyone, everywhere. Whether your quest is for inspired daily outfit concepts, meticulous preparation for a grand special occasion, or simply an insatiable curiosity about the avant-garde trends shaping tomorrow's fashion landscape, **Saundarya** stands as your dedicated guide.
    
    ### **Our Exquisite Offerings:**
    -   **Instant, Insightful Style Analysis**: Upload any photograph and receive a comprehensive, nuanced breakdown of your current ensemble, revealing its inherent potential.
    -   **Bespoe, Personalized Recommendations**: Unlock highly tailored suggestions, meticulously crafted based on your visual input and the specific occasion you designate.
    -   **Cutting-Edge Trend Insights**: Remain impeccably informed and ahead of the curve with our expertly curated analyses of the season's most influential fashion trends.
    -   **Pioneering Future Innovations**: We are relentlessly engaged in research and development, striving to introduce groundbreaking features like our upcoming Virtual Try-On, all designed to profoundly elevate your personal fashion journey.
    
    ### **The Genesis of Our Technology:**
    Saundarya harnesses the unparalleled capabilities of **Google Gemini's multi-modal AI**, specifically leveraging `gemini-1.5-flash`. This advanced model possesses an extraordinary aptitude for comprehending, interpreting, and generating insights from intricate visual information, enabling us to deliver fashion advice that is both highly accurate and profoundly relevant.
    
    ### **Our Grand Vision:**
    We passionately believe that fashion transcends mere clothing; it is a vibrant, empowering, and intrinsically joyful form of self-expression. **Saundarya** aspires to be your trusted confidante and indispensable partner in the exhilarating journey of discovering, refining, and celebrating your truly unique personal style.
    
    Thank you for becoming an integral part of the discerning **Saundarya** community! Your style revolution begins here.
    """)
    st.markdown("---")
    st.write("Saundarya is meticulously crafted with ❤️ passion, artistic vision, and relentless innovation. © 2025 Fashion GeniAI.")