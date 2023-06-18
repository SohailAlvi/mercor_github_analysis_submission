import streamlit as st

st.title('Get the Most Complex Repository from among your Github profile with the Help of GPT')
github_url = st.text_input("Enter like github.com/SohailAlvi")

if github_url:
    st.write({'github_url': github_url})
