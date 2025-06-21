
def suggest_dynamic_pricing(current_rates, usage_levels):
    suggestions = {}
    for zone, rate in current_rates.items():
        usage = usage_levels.get(zone, 0)
        if usage > 90:
            suggestions[zone] = rate * 1.1
        elif usage < 50:
            suggestions[zone] = rate * 0.9
        else:
            suggestions[zone] = rate
    return suggestions
