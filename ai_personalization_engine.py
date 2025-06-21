
def get_tool_recommendations(user_role):
    base_tools = ["Dashboard", "Schedule Optimizer"]
    role_specific = {
        "admin": ["Revenue Maximizer", "Contract Generator"],
        "sponsor": ["ROI Tracker", "Zone Map Viewer"],
        "board": ["Board Packet Generator", "Churn AI"],
        "foundation": ["Grant Tools", "Member Loyalty AI"]
    }
    return base_tools + role_specific.get(user_role, [])
