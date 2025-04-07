def calculate_agreement(user_answers: dict, weights: dict, party_positions: dict) -> float:
    total_distance = 0
    max_distance = 0

    for q_id_str, user_val in user_answers.items():
        q_id = str(q_id_str)
        weight = weights.get(q_id, 1)
        party_val = party_positions.get(q_id, {}).get('value')
        if party_val is None:
            continue
        distance = abs(user_val - party_val) * weight
        max_possible = (abs(user_val - 3) + 2) * weight
        total_distance += distance
        max_distance += max_possible
    if max_distance == 0:
        return 0
    return round((1 - total_distance / max_distance) * 100, 2)

def match_user_to_parties(user_answers: dict, weights: dict, parties: list) -> list:
    results = []
    for party in parties:
        score = calculate_agreement(user_answers, weights, party['positions'])
        results.append({
            'party': party['name'],
            'score': score
        })
    return sorted(results, key=lambda x: x['score'], reverse=True)
