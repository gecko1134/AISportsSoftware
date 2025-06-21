
def generate_zone_risk_scores(zone_usage):
    risks = {}
    for zone, hours in zone_usage.items():
        if hours < 20:
            risks[zone] = "⚠️ Inactive"
        elif hours < 50:
            risks[zone] = "🟡 Low Activity"
        else:
            risks[zone] = "🟢 Healthy"
    return risks
