import streamlit as st
from config.page_config import set_page
from utils.model_loader import load_resources
from utils.text_processing import combine_columns
from utils.shap_explainer import explain_top_entries
from utils.email_sender import send_fraud_report
from sections.sidebar import sidebar
from sections.dashboard import show_dashboard
from sections.custom_input import custom_input
# from sections.api_server import start_api_server  # Optional

set_page()
vectorizer, model = load_resources()
uploaded_file = sidebar()

if uploaded_file:
    import pandas as pd
    df = pd.read_csv(uploaded_file)
    st.dataframe(df.head(), use_container_width=True)
    df = combine_columns(df)

    X = vectorizer.transform(df['text'])
    probs = model.predict_proba(X)[:, 1]
    preds = (probs > 0.5).astype(int)

    df['Fraud Probability'] = probs
    df['Prediction'] = preds
    df['Prediction Label'] = df['Prediction'].map({0: 'Genuine', 1: 'Fraud'})

    st.subheader("Summary Metrics")
    show_dashboard(df)

    st.subheader("Top 10 Suspicious Job Listings")
    st.dataframe(df.sort_values("Fraud Probability", ascending=False).head(10)[["title", "location", "Fraud Probability"]], use_container_width=True)

    st.subheader("Why These Were Flagged, SHAP Plots")
    explain_top_entries(model, vectorizer, df)

    st.subheader("Get Notified")
    with st.form("email_form"):
        user_email = st.text_input("Enter your email to receive the fraud listing report:")
        submit_email = st.form_submit_button("Send Email")
    if submit_email:
        if user_email and "@" in user_email:
            send_fraud_report(df, user_email)
        else:
            st.warning("Please enter a valid email address.")

    with st.expander("Full Prediction Results", expanded=True):
        st.dataframe(df[["title", "location", "Fraud Probability", "Prediction Label"]], use_container_width=True)

    st.download_button(
        label="Download Results as CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='fraud_predictions.csv',
        mime='text/csv'
    )
else:
    st.info("You can upload a CSV from the sidebar to analyze multiple listings.")

custom_input(vectorizer, model)
# if False:
#     start_api_server(vectorizer, model)
