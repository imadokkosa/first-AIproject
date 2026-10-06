import streamlit as st
import subprocess

st.title("My Streamlit App Launcher")

option = st.selectbox(
    "Choose an app to run:",
    ["00_my_first_app.py", "01_my_second_app.py", "02_my_3_app.py"]
)

if st.button("Run selected app"):
    subprocess.run(["streamlit", "run", option])