import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import os
import base64

# --- 1. APNI KEY YAHAN PASTE KAREIN ---
API_KEY = "AIzaSyCYoopuipaOM-_uJ9J9l8xfKQxTdXYggfI"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Maths Guru Pro", page_icon="🎓")

# --- 2. SPEAKER FUNCTION ---
def play_audio(text):
    clean_text = text.replace('*', '') # Symbols hatane ke liye
    tts = gTTS(text=clean_text, lang='hi')
    tts.save("ans.mp3")
    with open("ans.mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay></audio>', unsafe_allow_html=True)
    os.remove("ans.mp3")

# --- 3. UI DESIGN ---
if 'login' not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("📱 Login Karein")
    mob = st.text_input("Mobile Number")
    if st.button("Login"):
        st.session_state.login = True
        st.rerun()
else:
    st.title("🎓 Maths Guru: Class 1-12")
    st.write("Sawal puchein aur saral bhasha mein hal payein.")

    mode = st.selectbox("Kaise sawal puchna hai?", ["Photo Khichein", "Type Karein", "Bol Kar (Voice)"])

    user_query = ""
    user_img = None

    if mode == "Photo Khichein":
        file = st.file_uploader("Sawal ki photo dalein", type=['jpg', 'png', 'jpeg'])
        if file:
            user_img = Image.open(file)
            st.image(user_img, width=300)

    elif mode == "Type Karein":
        user_query = st.text_area("Sawal yahan likhein...")

    elif mode == "Bol Kar (Voice)":
        user_query = st.text_input("Boliye (Yahan text dikhega)")
        st.info("Tip: Keyboard ka mic button daba kar boleing.")

    if st.button("Hal Nikalein"):
        with st.spinner("AI solution taiyar kar raha hai..."):
            if user_img:
                res = model.generate_content(["Is math question ko step-by-step saral bhasha mein solve karein.", user_img])
            else:
                res = model.generate_content(f"Solve this math problem simply for a student: {user_query}")
            
            st.session_state.result = res.text

    if 'result' in st.session_state:
        st.success("✅ Aapka Hal:")
        st.write(st.session_state.result)
        if st.button("🔈 Solution Suniye"):
            play_audio(st.session_state.result)

    if st.sidebar.button("Logout"):
        st.session_state.login = False
        st.rerun()
        
