import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def run():
    st.title("🏆 League Revenue Splitter")

    st.write("Simulate profit distribution between league and facility.")

    teams = st.slider("Number of Teams", 4, 40, 12)
    reg_fee = st.slider("League Registration Fee per Team ($)", 100, 1000, 500)
    facility_cost = st.slider("Facility Cost per Hour ($)", 50, 250, 100)
    games_per_team = st.slider("Games per Team", 3, 15, 8)
    game_duration = st.selectbox("Game Length (mins)", [60, 90])

    total_game_hours = teams * games_per_team * (game_duration / 60) / 2  # each game = 2 teams
    total_rev = teams * reg_fee
    total_cost = total_game_hours * facility_cost
    profit = total_rev - total_cost

    st.metric("Total Revenue", f"${total_rev:,.2f}")
    st.metric("Facility Cost", f"${total_cost:,.2f}")
    st.metric("Net Profit", f"${profit:,.2f}")

    fig, ax = plt.subplots()
    ax.pie([total_cost, profit], labels=["Facility Cost", "Profit"], autopct="%1.1f%%", colors=["#66b3ff", "#99ff99"])
    ax.set_title("Revenue Allocation")
    st.pyplot(fig)