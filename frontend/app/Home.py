import streamlit as st
from pages.Voice_Activity_Detection import voice_activity_detection
from pages.Upload_File import upload_file


def home():
    st.title("Home")

    st.sidebar.title("Services")

    page_names_to_funcs = {
        "Upload File": upload_file,
        "VAD": voice_activity_detection,
    }

    pages = st.sidebar.selectbox("Choose a service", page_names_to_funcs.keys())
    page_names_to_funcs[pages]()


if __name__ == "__main__":
    home()
