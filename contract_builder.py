import streamlit as st
import datetime

def run():
    st.title("📄 Contract Builder")

    st.write("Fill out the fields below to generate a custom sponsor contract.")

    with st.form("contract_form"):
        sponsor_name = st.text_input("Sponsor Name")
        amount = st.number_input("Sponsorship Amount ($)", min_value=0)
        tier = st.selectbox("Sponsorship Tier", ["Bronze", "Silver", "Gold", "Platinum"])
        start_date = st.date_input("Start Date", datetime.date.today())
        end_date = st.date_input("End Date", datetime.date.today() + datetime.timedelta(days=365))
        benefits = st.text_area("Key Benefits Provided", "Banner placement, website listing, event shoutouts")
        submit = st.form_submit_button("Generate Contract")

    if submit:
        st.subheader("📜 Generated Contract Preview")
        contract_text = f"""SPONSORSHIP AGREEMENT

This agreement is made between [FACILITY NAME] and {sponsor_name}, effective from {start_date} to {end_date}.

Sponsor has agreed to support the facility at the {tier} level with a contribution of ${amount:,.2f}.

In return, the facility will provide the following benefits:
{benefits}

Signed,
_____________________     _____________________
Facility Representative   Sponsor Representative
Date: {datetime.date.today()}
"""
        st.code(contract_text, language="text")