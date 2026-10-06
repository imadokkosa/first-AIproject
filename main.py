import os
import streamlit as st

port = int(os.environ.get("PORT", 8501))

# ページ設定
st.set_page_config(page_title="My Streamlit App", layout="wide")

# 起動確認
st.write(f"Streamlit is running on port {port}")

# メインUI
st.title("My Streamlit App Launcher")

option = st.selectbox(
    "Choose an app to run:",
    ["First App", "Second App", "Third App"]
)

if option == "First App":
    st.header("First App")
    st.write("ここに 00_my_first_app.py の内容を書く")

elif option == "Second App":
    st.header("Second App")
    st.write("ここに 01_my_second_app.py の内容を書く")

elif option == "Third App":
    st.header("Third App")
    st.write("ここに 02_my_3_app.py の内容を書く")

