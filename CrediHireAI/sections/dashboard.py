import streamlit as st
import plotly.express as px
import pandas as pd

def show_dashboard(df):
    total_jobs = len(df)
    total_frauds = df['Prediction'].sum()
    fraud_rate = (total_frauds / total_jobs) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Jobs Analyzed", f"{total_jobs:,}")
    col2.metric("Fraudulent Listings", f"{total_frauds:,}")
    col3.metric("Fraud Rate (%)", f"{fraud_rate:.2f} %")

    st.divider()
    st.subheader("Visual Insights")
    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.histogram(df, x='Fraud Probability', nbins=20,
                            color='Prediction Label',
                            color_discrete_map={'Fraud': 'red', 'Genuine': 'green'},
                            title="Fraud Probability Distribution")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.pie(df, names='Prediction Label',
                      color='Prediction Label',
                      color_discrete_map={'Fraud': 'red', 'Genuine': 'green'},
                      title="Genuine vs Fraud Breakdown")
        st.plotly_chart(fig2, use_container_width=True)
