
def match_sponsors_to_zones(sponsor_data, zone_data):
    matches = []
    for sponsor in sponsor_data:
        for zone in zone_data:
            if sponsor['target'] in zone['tags']:
                matches.append({'sponsor': sponsor['name'], 'zone': zone['id']})
    return matches
