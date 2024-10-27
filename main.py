# Set up and run this Streamlit App
import streamlit as st
import pandas as pd
import io
from helper_functions import llm
from helper_functions.utility import check_password  
from logics.user_query_handler import process_user_message

# Check if the password is correct.  
if not check_password():  
    st.stop() 

# <--- This is the helper function that we have created 
# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="My Streamlit App"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("Streamlit App")

form = st.form(key="form")
form.subheader("Query")

user_prompt = form.text_area("Enter your prompt here", height=200)

if form.form_submit_button("Submit"):
    
    st.toast(f"User Query Submitted - {user_prompt}")

    st.divider()

    response, disease_details = process_user_message(user_prompt)
    st.write(response)

    st.divider()

    print(disease_details)