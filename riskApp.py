# -*- coding: utf-8 -*-
"""
Streamlit Risk & Benefit Assessment Tool
"""

import streamlit as st

# -------------------- Assessment Function --------------------
def assess_risk(q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12_selected, q12_options):
    risk = 0
    benefit = 0

    # --- Risk scoring --- Changing weightings of questions here ---
    if q1 == "Yes":
        risk += 0
    elif q1 == "Not Sure":
        risk += 90
    else:
        risk += 1000
    risk += 1000 if q2 == "Yes" else 0
    risk += 0 if q3 == "Yes" else 100
    risk += 1000 if q4 == "Yes" else 0 #1000 for no purchase under any circumstance
    risk += 0 if q5 == "Yes" else 100
    risk += 0 if q6 == "Yes" else 1000
    risk += 0 if q7 == "Yes" else 1000
    risk += 0 if q8 == "Yes" else 100
    risk += 0 if q11 == "Yes" else 1000

    # Q12: add 10 points for each NOT selected
    for option in q12_options:
        if option not in q12_selected:
            risk += 10

    # --- Benefit scoring ---
    benefit += q9  # higher cost saving = higher benefit
    risk += (100-q9) // 2  # higher cost saving = lower risk
    benefit += 0 if q10 == "Yes" else 50

    # --- Map Risk to category ---  Change thresholds for risk categories here ---
    if risk <= 50:
        risk_category = "Low"
    elif risk <= 101:
        risk_category = "Medium"
    elif risk <= 900:
        risk_category = "High"
    else:
        risk_category = "Very High. Do Not Proceed"

    # --- Map Benefit to category --- Change thresholds for benefit categories here ---
    if benefit <= 20:
        benefit_category = "Low"
    elif benefit <= 90:
        benefit_category = "Medium"
    else:
        benefit_category = "High"

    return risk_category, benefit_category

# -------------------- Map Category to Color -------------------- Change colours here --------------------
# Map Risk to colors
def map_risk_to_color(category):
    if category == "High":
        return "#FF4B4B"  # red
    elif category == "Very High. Do Not Proceed":
        return "#8B0000"  # dark red
    elif category == "Medium":
        return "#FFA500"  # orange
    else:
        return "#4CAF50"  # green

# Map Benefit to colors
def map_benefit_to_color(category):
    if category == "High":
        return "#4CAF50"  # green
    elif category == "Medium":
        return "#FFA500"  # orange
    else:
        return "#FF4B4B"  # red


# -------------------- Streamlit App --------------------
st.title("Risk & Benefit Assessment Tool")
st.write("Answer the questions below:")

# --- Questions ---
q1 = st.radio("1. Is the listing real?", ["Yes", "No", "Not Sure"])
q2 = st.radio("2. Has the device been stolen?", ["Yes", "No", "Not Sure"])
q3 = st.radio("3. Is the device coming from another NHS trust?", ["Yes", "No", "Not Sure"])
q4 = st.radio("4. Does this device have a field safety notice?", ["Yes", "No", "Not Sure"])
q5 = st.radio("5. Are you able to confirm why the device is being sold?", ["Yes", "No"])
q6 = st.radio("6. Does the listing indicate the device is functional and not modified?", ["Yes", "No"])
q7 = st.radio("7. Does the original manufacturer still support the device?", ["Yes", "No"])
q8 = st.radio("8. Does the device integrate with existing systems?", ["Yes", "No"])
q9 = st.slider(
    "9. Cost saving compared to buying new (0% = same price, 50% = half, 100% = free)",
    min_value=0, max_value=100
)
q10 = st.radio("10. Is the device available from a registered supplier or the original manufacturer?", ["Yes", "No"])
q11 = st.radio(
    "11. Once purchased, will necessary testing ensure the device is functioning and safe?", ["Yes", "No"]
)

q12_options = [
    "a clear statement that the device is being resold/donated",
    "a certificate of decontamination",
    "the user manuals and training requirements",
    "full details of maintenance and servicing requirements",
    "service history and manual",
    "usage history",
    "quality assurance test details",
    "safety updates, including MHRA and manufacturer’s documents that have been released since the medical device was first supplied."
]
q12_selected = st.multiselect(
    "12. Which of the following documentation have you obtained? (Select all that apply)",
    q12_options
)

# --- Button to assess ---
if st.button("Assess Risk & Benefit"):
    risk, benefit = assess_risk(q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12_selected, q12_options)
    
    # Map colors dynamically
    risk_color = map_risk_to_color(risk)
    benefit_color = map_benefit_to_color(benefit)

    # Display headers
    st.markdown(
        f'<div style="background-color:{risk_color}; color:white; padding:15px; border-radius:8px; font-size:24px; text-align:center;">Predicted Risk: {risk}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div style="background-color:{benefit_color}; color:white; padding:15px; border-radius:8px; font-size:24px; text-align:center;">Predicted Benefit: {benefit}</div>',
        unsafe_allow_html=True
    )

