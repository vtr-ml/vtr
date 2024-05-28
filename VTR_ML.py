import streamlit as st
from streamlit_chat import message
import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown


st.header ("VTR Machine Learning", divider='rainbow')

col1, col2= st.columns(2)

with st.sidebar:

    st.header(":yellow[List of contents]")
    main = st.button("Main Menu")
    gpt = st.button("Chat GPT")

    bt = st.button("My Resume")
if bt:
    with col1:
        st.write ("L LOGIDHASAN", 
                  "vetri.dreams2010@gmail.com ")
                  
                  
                  


if main:
    st.header("Machine Learning")
    st.write ("Machine Learning is a subset of artificial intelligence(AI) that focus on learning from data to develop an algorithm that can be used to make a prediction")
    st.write("A machine learning algorithm works by learning patterns and relationships from data to make predictions or decisions without being explicitly programmed for each task.")
    st.divider()




if gpt:
    with col1:
        





