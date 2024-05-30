import streamlit as st
from streamlit_chat import message
import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
genai.configure(api_key="AIzaSyD5xP91E7lR4shBS1CqGGzQIUWNuBLsqx8")

st.set_page_config(page_title="VTR", page_icon=":earth_asia:", layout="wide", initial_sidebar_state="auto", menu_items=None)


col1, col2= st.columns(2)

with st.sidebar:

    st.header(":yellow[List of contents]")
    page_names = ["Home", "My Resume", "VTR ChatGPT", "Need Help?", "BMI Calculator"]
    page = st.radio("Navigation", page_names)

if page == "Home":
    st.header ("VTR Machine Learning", divider='rainbow')
    st.subheader("Machine Learning")
    st.write ("Machine Learning is a subset of artificial intelligence(AI) that focus on learning from data to develop an algorithm that can be used to make a prediction")
    st.write("A machine learning algorithm works by learning patterns and relationships from data to make predictions or decisions without being explicitly programmed for each task.")
    st.divider()

if page =="My Resume":
    st.write("L. Logidhasan")


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
        msg.chat_message("user").write(prompt)
        msg.chat_message("assistant").write(f"Echo: {prompt}")


if page =="BMI Calculator":
    st.title('Welcome to BMI Calculator')
    with col1:
        weight = st.number_input("Enter your weight (in kgs)")
        status = st.radio('Select your height format: ',
                      ('cms', 'meters', 'feet'))
        if(status == 'cms'):
            height = st.number_input('Centimeters')
            try:
                bmi = weight / ((height/100)**2)
            except:
                st.text("Enter some value of height")
     
        elif(status == 'meters'):
        
            height = st.number_input('Meters')
     
            try:
                bmi = weight / (height ** 2)
            except:
                st.text("Enter some value of height")
     
        else:
       
            height = st.number_input('Feet')
     
        
            try:
                bmi = weight / (((height/3.28))**2)
            except:
                st.text("Enter some value of height")
     
    
        if(st.button('Calculate BMI')):
            st.text("Your BMI Index is {}.".format(bmi))
        with col2:
            if(bmi < 16):
                st.error("You are Extremely Underweight")
            elif(bmi >= 16 and bmi < 18.5):
                st.warning("You are Underweight")
            elif(bmi >= 18.5 and bmi < 25):
                st.success("Healthy")
            elif(bmi >= 25 and bmi < 30):
                st.warning("Overweight")
            elif(bmi >= 30):
                st.error("Extremely Overweight")
    






