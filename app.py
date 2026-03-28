import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import os
import base64

# --- 1. CONFIGURATION ---
API_KEY = "AIzaSyCYoopuipaOM-_uJ9J918xfKQxTdXYggfI" # Aapki key
genai.configure(api_key=API_KEY)

# MODEL NAME UPDATED TO LATEST
model = genai.GenerativeModel('gemini-1.5-flash-latest')

st.set_page_config(page_title="Maths Guru Pro", page_icon="🎓")

# --- 2. SPEAKER FUNCTION ---
def play_audio(text):
    try:
        clean_text = text.replace('*', '') 
        tts = gTTS(text=clean_text, lang='hi')
        tts.save("ans.mp3")
        with open("ans.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay></audio>', unsafe_allow_html=True)
        os.remove("ans.mp3")
    except:
        st.warning("Audio play nahi ho saka, par hal niche likha hai.")

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
    mode = st.selectbox("Kaise sawal puchna hai?", ["Type Karein", "Photo Khichein"])

    user_query = ""
    user_img = None

    if mode == "Photo Khichein":
        file = st.file_uploader("Sawal ki photo dalein", type=['jpg', 'png', 'jpeg'])
        if file:
            user_img = Image.open(file)
            st.image(user_img, width=300)

    elif mode == "Type Karein":
        user_query = st.text_area("Sawal yahan likhein (Jaise: 2*5=)")

    if st.button("Hal Nikalein"):
        with st.spinner("AI hal nikal raha hai..."):
            try:
                if user_img:
                    res = model.generate_content(["Is math question ko saral hindi bhasha mein step-by-step solve karein.", user_img])
                else:
                    res = model.generate_content(f"Solve this math problem simply for a student: {user_query}")
                
                st.session_state.result = res.text
            except Exception as e:
                st.error(f"Error: AI model connect nahi ho pa raha. Kripya API Key check karein. {e}")

    if 'result' in st.session_state:
        st.success("✅ Aapka Hal:")
        st.write(st.session_state.result)
        if st.button("🔈 Solution Suniye"):
            play_audio(st.session_state.result)

    if st.sidebar.button("Logout"):
        st.session_state.login = False
        st.rerun()
        
