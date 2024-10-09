import streamlit as st
from main import run_main

options = ["wquil","prime"]

st.set_page_config(layout="wide")

st.title("OnChain Data Scrapper")
token = st.selectbox("Choose Token : ", options)
    
scrape_option = st.radio("Choose no of day(s):", ["1 day", "7 days"])

if st.button(f"Start for {token} , type {scrape_option}"):
    st.write("Starting Scrape...")
    
    if scrape_option == "1 day":
        days = 1 
    else:
        days = 7

    addresses, image_path, result = run_main(token,days)
    
    st.session_state.dom_content = result
    
    with st.expander(f"View top addresses for token {token}"):
        st.text_area("Addresses", addresses, height=300)
    
    st.success("Scraping completed!")
        
#if we saved the content
if "dom_content" in st.session_state:
    #show charts
    st.title("Charts")
    st.image(image_path, caption= "Charts", use_column_width=True) 
    
