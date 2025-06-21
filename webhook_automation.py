import streamlit as st
import pandas as pd
from datetime import datetime

def run():
    st.title("🔗 Webhook Automation Simulator")

    st.subheader("🧪 Configure Webhook")
    endpoint = st.text_input("Webhook URL", value="https://api.example.com/webhook")
    trigger_event = st.selectbox("Trigger Type", ["New Signup", "Low Inventory", "VIP Upgrade", "Booking Confirmed"])

    sample_payloads = {
        "New Signup": {"event": "signup", "member_id": "M001", "tier": "Silver"},
        "Low Inventory": {"event": "alert", "zone": "Cafe", "item": "Bottled Water", "level": "low"},
        "VIP Upgrade": {"event": "upgrade", "member_id": "M002", "new_tier": "VIP"},
        "Booking Confirmed": {"event": "booking", "zone": "Court 1", "time": "2024-07-01 17:00"}
    }

    if st.button("Preview Payload"):
        payload = sample_payloads.get(trigger_event, {})
        st.json(payload)

    if "log" not in st.session_state:
        st.session_state["log"] = []

    if st.button("Send Webhook"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state["log"].append({
            "endpoint": endpoint,
            "event": trigger_event,
            "sent": timestamp
        })
        st.success(f"Webhook sent to {endpoint}")

    if st.session_state["log"]:
        st.subheader("📜 Webhook Dispatch Log")
        st.dataframe(pd.DataFrame(st.session_state["log"]))