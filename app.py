import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import os
import base64

# --- 1. CONFIGURATION (Aapki Nayi API Key) ---
API_KEY = "AIzaSyAvptSpKH_NuBseXBmNhS3Igkyx7eeV0lQ"

genai.configure(api_key=API_KEY, transport='rest')
model = genai.GenerativeModel('gemini-1.5-flash')


# Sabse stable model select kiya hai
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Maths Guru Pro", page_icon="🎓", layout="centered")

# --- 2. SPEAKER FUNCTION (Solution Sunne ke liye) ---
def play_audio(text):
    try:
        # Symbols hatane ke liye taaki awaz saaf aaye
        clean_text = text.replace('*', '').replace('#', '') 
        tts = gTTS(text=clean_text, lang='hi')
        tts.save("ans.mp3")
        with open("ans.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay></audio>', unsafe_allow_html=True)
        os.remove("ans.mp3")
    except Exception as e:
        st.warning("Audio play nahi ho saka, par hal niche likha hai.")

# --- 3. LOGIN SYSTEM ---
if 'login' not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("📱 Maths Guru Login")
    st.subheader("Class 1 se 12 tak ke sawalo ka hal")
    mob = st.text_input("Mobile Number enter karein", placeholder="9876543210")
    if st.button("Login Karein"):
        if len(mob) >= 10:
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Kripya sahi mobile number dalein.")
else:
    # --- 4. MAIN APP INTERFACE ---
    st.sidebar.title("My Profile")
    st.sidebar.write("👤 User: Sandeep")
    if st.sidebar.button("Logout"):
        st.session_state.login = False
        st.rerun()

    st.title("🎓 Maths Guru Pro")
    st.write("Sawal puchein aur saral bhasha mein hal payein.")

    mode = st.selectbox("Sawal kaise puchna chahenge?", ["Type Karein", "Photo Khichein"])

    user_query = ""
    user_img = None

    if mode == "Type Karein":
        user_query = st.text_area("Apna sawal yahan likhein:", placeholder="Example: 5 + 10 = ? ya 2x + 5 = 15")
    
    elif mode == "Photo Khichein":
        file = st.file_uploader("Sawal ki photo upload karein", type=['jpg', 'png', 'jpeg'])
        if file:
            user_img = Image.open(file)
            st.image(user_img, caption="Aapka Sawal", use_container_width=True)

    # --- 5. HAL NIKALEIN LOGIC ---
    if st.button("Hal Batayein"):
        with st.spinner("AI hal nikal raha hai..."):
            try:
                if user_img:
                    # Photo ke liye prompt
                    res = model.generate_content(["Is math question ko step-by-step saral bhasha mein solve karein.", user_img])
                else:
                    # Text ke liye prompt
                    res = model.generate_content(f"Solve this math problem simply for a student in Hindi: {user_query}")
                
                st.session_state.result = res.text
            except Exception as e:
                st.error("Connection Error! Kripya 1 minute baad dobara try karein.")
                st.info(f"Detail: {str(e)}")

    # Result Display aur Speaker
    if 'result' in st.session_state:
        st.success("✅ Aapka Hal:")
        st.markdown(st.session_state.result)
        
        st.divider()
        st.subheader("🔊 Solution Suniye")
        if st.button("🔈 Play Audio"):
            play_audio(st.session_state.result)

st.divider()
st.caption("Made with ❤️ by Sandeep")
