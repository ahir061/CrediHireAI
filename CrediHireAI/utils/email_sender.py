import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st

def send_fraud_report(df, user_email):
    fraud_df = df[df['Prediction'] == 1][['title', 'location', 'Fraud Probability']]
    html_table = fraud_df.to_html(index=False)

    msg = MIMEMultipart()
    msg['From'] = "scamjobdetection176@gmail.com"
    msg['To'] = user_email
    msg['Subject'] = "FraudScan Report - Suspicious Job Listings"

    body = f"""
    <h3>Dear User,</h3>
    <p>Here are the job listings flagged as <b>fraudulent</b>:</p>
    {html_table}
    <p>Stay safe,<br><b>FraudScan</b></p>
    """
    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("scamjobdetection176@gmail.com", "yvoglollyyojfaua")
    server.send_message(msg)
    server.quit()

    st.success(f"Report successfully sent to {user_email}!")
