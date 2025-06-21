import streamlit as st
import pandas as pd
import os
from PIL import Image

def run():
    st.title("🎞️ Sponsor Media Preview Tool")

    uploaded = st.file_uploader("Upload sponsor_assets.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "sponsor_name": ["FitFuel", "TeamWorks", "HydroTech"],
            "logo_path": ["logo1.png", "logo2.png", "logo3.png"],
            "placement": ["Court Banner", "Website Footer", "Email Header"]
        })

    st.subheader("📋 Sponsor Assets & Placement")
    st.dataframe(df)

    st.markdown("### 📺 Preview Mock Placements")

    for _, row in df.iterrows():
        st.markdown(f"**{row['sponsor_name']}** — {row['placement']}")
        try:
            if os.path.exists(row["logo_path"]):
                st.image(Image.open(row["logo_path"]), width=250)
            else:
                st.warning(f"Mock preview placeholder for {row['logo_path']}")
        except:
            st.warning("Preview unavailable for this row.")