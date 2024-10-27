import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="My Streamlit App"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("About this App")

st.write("This is a Streamlit App that acts as a mini-compendium of Singapore's Infectious Disease Act.")

with st.expander("How to use this App"):
    st.write("1. Enter your prompt in the text area.")
    st.write("2. Click the 'Submit' button.")
    st.write("3. The app will generate a text completion based on your query.")

with st.expander("Disclaimer"):
    st.write("1. This API is not intended for real-world use and only meant as an educational assignment.")
    st.write("2. LLM may generate inaccurate or incorrect information. Exercise discretion.")
    st.write("3. Always cross-check the accuracy and factualness of the information.")