# app/services/matcher.py

from typing import List, Dict


def calculate_agreement(
    user_answers: Dict[str, int],
    weights: Dict[str, int],
    party_positions: Dict[str, Dict[str, int]]
) -> float:
    """
    Calculate a match score between the user's answers and a party's positions.
    Returns a percentage 0–100 where 100 means perfect agreement.
    """
    total_distance = 0.0
    max_distance = 0.0

    for q_id, user_val in user_answers.items():
        # default weight = 1 if not provided
        weight = weights.get(q_id, 1)
        # party_positions[q_id] should be a dict like {'value': int, 'source': str}
        party_pos = party_positions.get(q_id, {}).get('value')
        if party_pos is None:
            # skip questions the party has no position on
            continue

        # distance from user to party on this question
        distance = abs(user_val - party_pos) * weight
        # maximum possible distance given the user's answer (scale 1–5 centered on 3)
        max_possible = (abs(user_val - 3) + 2) * weight

        total_distance += distance
        max_distance += max_possible

    if max_distance == 0:
        return 0.0

    # score = (1 - (distance / max)) * 100
    score = (1 - total_distance / max_distance) * 100
    return round(score, 2)


def match_user_to_parties(
    user_answers: Dict[str, int],
    weights: Dict[str, int],
    parties: List[Dict]
) -> List[Dict]:
    """
    Given:
      - user_answers: {"1": 4, "2": 2, ...}
      - weights:      {"1": 2, "2": 1, ...}
      - parties:      [{"name": "Party A", "positions": {...}}, ...]
    Returns:
      [
        {"party": "Party A", "score": 87.5},
        {"party": "Party B", "score": 65.0},
        ...
      ]
    sorted by descending score.
    """
    results = []
    for party in parties:
        score = calculate_agreement(user_answers, weights, party["positions"])
        results.append({"party": party["name"], "score": score})

    return sorted(results, key=lambda x: x["score"], reverse=True)
