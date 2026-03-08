import streamlit as st
import google.generativeai as genai
import os

# API Key ko safe tarike se use karein
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

st.title("🧮 Smart Math Solver")
grade = st.selectbox("Class chunein:", [str(i) for i in range(1, 13)])
question = st.text_input("Sawal likhein:")
image_file = st.camera_input("Photo khinchein")

if st.button("Solve"):
    model = genai.GenerativeModel('gemini-1.5-flash')
    if image_file:
        import PIL.Image
        img = PIL.Image.open(image_file)
        response = model.generate_content(["Solve this math for class " + grade, img])
        st.write(response.text)
    elif question:
        response = model.generate_content("Solve this for class " + grade + ": " + question)
        st.write(response.text)
      
