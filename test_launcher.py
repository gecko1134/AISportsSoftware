import streamlit as st
import subprocess

def run():
    st.title("🚀 AI Module Test Launcher")

    tests = {
        "AI Scheduler Test": "test_ai_scheduler_tool.py",
        "Contract Generator": "auto_contract_generator.py",
        "Pricing Optimizer": "dynamic_pricing_tool.py"
    }

    selected = st.multiselect("Select Modules to Test", options=list(tests.keys()), default=list(tests.keys()))
    if st.button("Run Selected Tests"):
        for key in selected:
            script = tests[key]
            st.write(f"🔍 Running: {key}")
            try:
                with open(script) as f:
                    exec(f.read())
                st.success(f"✅ {key} completed successfully.")
            except Exception as e:
                st.error(f"❌ {key} failed: {e}")