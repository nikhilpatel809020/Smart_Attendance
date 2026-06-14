import streamlit as st

st.title("Camera Test")

picture = st.camera_input("Take a Picture")

if picture:
    st.success("Photo Captured")
    st.image(picture)