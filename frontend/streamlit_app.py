import streamlit as st
import requests

st.title("AI Meeting Agent")
uploaded_file = st.file_uploader("Upload Zoom/Teams recording (MP4, M4A)", type=["mp4", "m4a"])

if uploaded_file:
    with st.spinner("Processing..."):
        response = requests.post(
            "http://localhost:8000/upload/",
            files={"file": uploaded_file}
        )
        data = response.json()
        st.subheader("📝 Summary")
        st.markdown(data["summary"])
        st.subheader("🎤 Full Transcript")
        st.text_area("", value=data["transcript"], height=400)
