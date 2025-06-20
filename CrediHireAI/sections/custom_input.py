import streamlit as st

def custom_input(vectorizer, model):
    st.subheader("🔍 Classify a Custom Job Description")

    with st.form("custom_form", clear_on_submit=True):
        custom_title = st.text_input("Job Title")
        custom_company = st.text_area("Company Profile (optional)")
        custom_description = st.text_area("Job Description")
        custom_requirements = st.text_area("Requirements")
        custom_benefits = st.text_area("Benefits (optional)")
        submitted = st.form_submit_button("Classify Job Posting")

    if submitted:
        combined_text = f"{custom_title} {custom_company} {custom_description} {custom_requirements} {custom_benefits}".lower().strip()
        transformed = vectorizer.transform([combined_text])
        probability = model.predict_proba(transformed)[0][1]
        prediction = "Fraud" if probability > 0.5 else "Genuine"
        st.markdown(f"### Result: **{prediction}**")
        st.progress(probability)
        st.markdown(f"**Fraud Probability:** `{probability:.2f}`")
