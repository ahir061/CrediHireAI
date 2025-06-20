import joblib
import streamlit as st

@st.cache_resource
def load_resources():
    vectorizer = joblib.load("models/ahirr_vectorizer.pkl")
    model = joblib.load("models/ahirr_model.pkl")
    return vectorizer, model
