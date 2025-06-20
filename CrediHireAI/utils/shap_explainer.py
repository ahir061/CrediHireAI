import shap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

def explain_top_entries(model, vectorizer, df):
    try:
        top3_text = df['text'].iloc[:3].tolist()
        top3_vec = vectorizer.transform(top3_text)
        top3_dense = pd.DataFrame(top3_vec.toarray(), columns=vectorizer.get_feature_names_out())

        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(top3_dense)[1]

        for i in range(3):
            st.markdown(f"Listing #{i + 1}: {df.iloc[i]['title']}")
            shap_vals = shap_values[i]
            feature_names = top3_dense.columns
            instance_data = top3_dense.iloc[i]

            top_indices = np.argsort(np.abs(shap_vals))[-10:]
            explanation = shap.Explanation(
                values=shap_vals[top_indices],
                base_values=explainer.expected_value[1],
                data=instance_data.iloc[top_indices].values,
                feature_names=feature_names[top_indices]
            )

            fig = plt.figure(figsize=(8, 4))
            shap.plots.bar(explanation, show=False)
            st.pyplot(fig)
    except Exception as e:
        st.warning(f"SHAP visualization error: {e}")
