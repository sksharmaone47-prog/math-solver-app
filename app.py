import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import os
import base64

# --- 1. SETTINGS & AI SETUP ---
genai.configure(api_key="YOUR_GEMINI_API_KEY") # Apni Key yahan dalein
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Maths Guru Pro", layout="centered", page_icon="📝")

# --- 2. SPEAKER FUNCTION ---
def play_audio(text):
    tts = gTTS(text=text, lang='hi')
    tts.save("ans.mp3")
    with open("ans.mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay></audio>', unsafe_allow_html=True)
    os.remove("ans.mp3")

# --- 3. LOGIN PAGE ---
if 'login' not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("📱 Maths Guru Login")
    num = st.text_input("Mobile Number")
    if st.button("Get OTP"):
        otp = st.text_input("Enter OTP (Try: 1234)")
        if st.button("Verify"):
            if otp == "1234":
                st.session_state.login = True
                st.rerun()
else:
    # --- 4. MAIN APP INTERFACE ---
    st.title("🎓 Saral Maths Solver")
    mode = st.radio("Sawal kaise puchein?", ["Likh kar (Type)", "Photo Khichein (Camera)", "Bol kar (Voice)"])

    user_input = ""
    user_image = None

    if mode == "Likh kar (Type)":
        user_input = st.text_area("Yahan apna sawal likhein...")
    
    elif mode == "Photo Khichein (Camera)":
        img_file = st.file_uploader("Sawal ki photo upload karein", type=['jpg', 'png', 'jpeg'])
        if img_file:
            user_image = Image.open(img_file)
            st.image(user_image, width=250)

    elif mode == "Bol kar (Voice)":
        st.info("Browser Mic allow karein aur niche button dabayein.")
        # Note: Browser mic ke liye alag se component lagta hai, simple version ke liye typing use karein
        user_input = st.text_input("Boliye (Mic input yahan dikhega)...")

    # --- 5. GENERATE SOLUTION ---
    if st.button("Hal Batayein"):
        with st.spinner("AI hal nikal raha hai..."):
            if user_image:
                res = model.generate_content(["Is math question ko saral hindi-english mix mein solve karein.", user_image])
            else:
                res = model.generate_content(f"Solve this math problem simply for a student: {user_input}")
            
            st.session_state.ans = res.text

    if 'ans' in st.session_state:
        st.success("Aapka Hal:")
        st.write(st.session_state.ans)
        if st.button("🔈 Solution Suniye"):
            play_audio(st.session_state.ans)
