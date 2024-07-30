import streamlit as st
from streamlit_chat import message
import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
genai.configure(api_key="AIzaSyDRn3VdtoKDhxthgLtLaH8U10RZQ-KwTlI")

st.set_page_config(page_title="VTR", page_icon=":earth_asia:", layout="wide", initial_sidebar_state="auto", menu_items=None)


col1, col2= st.columns(2)

with st.sidebar:

    st.header(":yellow[List of contents]")
    page_names = ["Home", "My Resume", "VTR ChatGPT", "Need Help?", "Text to speech"]
    page = st.radio("Navigation", page_names)

if page == "Home":
    st.header ("VTR Machine Learning", divider='rainbow')
    st.subheader("Machine Learning")
    st.write ("Machine Learning is a subset of artificial intelligence(AI) that focus on learning from data to develop an algorithm that can be used to make a prediction")
    st.write("A machine learning algorithm works by learning patterns and relationships from data to make predictions or decisions without being explicitly programmed for each task.")
    st.divider()

if page =="My Resume":
    st.write("L. Logidhasan", "Mail ID: vetri.dreams2010@gmail.com", "Contact Number: 9342162117")


if page =="VTR ChatGPT":
    with col1:
        st.header(":yellow[Welcome to VTR ChatGPT]")
        Enter=st.text_input("Please enter")
        Start = st.button("Generate")
        messages = st.container(height=1200)
    if Start:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(Enter)
        X = response.text
        messages.write (X)

if page =="Need Help?":   
    st.header("Any Query")
    msg = st.container(height=600)
    if prompt := st.chat_input("Say something"):
        
        reply = "Hi, how are you"

        msg.chat_message("user").write(prompt)
        msg.chat_message("assistant").write(f"Echo: {reply}")


from gtts import gTTS
import os
from io import BytesIO


sound_file = BytesIO()

if page == "Text to speech":
    tlds = st.selectbox("choose the slang", ("us", "ca", "fr"))
    language = "en"
    mytext = st.text_area("Enter text to convert")
    enter = st.button ("Generate voice")
    if enter:
        
        myobj = gTTS(text=mytext, tld = tlds, lang=language, slow=False)

        myobj.write_to_fp(sound_file)

        st.audio(sound_file)




