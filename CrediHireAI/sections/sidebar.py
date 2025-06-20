import streamlit as st

def sidebar():
    with st.sidebar:
        st.title("Upload Job Listings")
        uploaded_file = st.file_uploader("Choose CSV File", type=["csv"])
        st.markdown("---")
        st.caption("Built with love using ML and Streamlit")
    return uploaded_file
