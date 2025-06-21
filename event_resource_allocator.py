import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("🎯 Event Resource Allocator")

    event_file = st.file_uploader("Upload events.csv", type=["csv"])
    resource_file = st.file_uploader("Upload resources.csv", type=["csv"])

    if event_file and resource_file:
        events = pd.read_csv(event_file)
        resources = pd.read_csv(resource_file)
    else:
        np.random.seed(42)
        events = pd.DataFrame({
            "event_id": range(1, 11),
            "event_type": np.random.choice(["Tournament", "Clinic", "Showcase"], 10),
            "expected_attendance": np.random.randint(50, 300, 10),
            "required_staff": np.random.randint(2, 6, 10),
            "required_equipment": np.random.choice(["Net", "Cones", "Balls"], 10)
        })
        resources = pd.DataFrame({
            "resource_id": range(101, 121),
            "type": np.random.choice(["Staff", "Net", "Balls", "Cones"], 20),
            "status": np.random.choice(["Available", "Unavailable"], 20, p=[0.8, 0.2])
        })

    st.subheader("📋 Events")
    st.dataframe(events)

    st.subheader("🛠️ Available Resources")
    st.dataframe(resources)

    assigned = []
    for _, event in events.iterrows():
        assigned_staff = resources[
            (resources["type"] == "Staff") & (resources["status"] == "Available")
        ].head(event["required_staff"])
        assigned_equip = resources[
            (resources["type"] == event["required_equipment"]) & (resources["status"] == "Available")
        ].head(1)

        staff_ids = assigned_staff["resource_id"].tolist()
        equip_ids = assigned_equip["resource_id"].tolist()

        assigned.append({
            "event_id": event["event_id"],
            "staff_assigned": staff_ids,
            "equipment_assigned": equip_ids
        })

        resources = resources[~resources["resource_id"].isin(staff_ids + equip_ids)]

    assigned_df = pd.DataFrame(assigned)
    st.subheader("📦 Resource Assignments")
    st.dataframe(assigned_df)