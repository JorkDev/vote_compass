# app/services/advanced_model.py

import numpy as np
from typing import Tuple, List, Dict

def compute_latent_positions(
    user_answers: Dict[str, int],
    questions: List[Dict],
    parties: List[Dict]
) -> Tuple[Dict, List[Dict]]:
    """
    Compute 2D coordinates for the user and each party.
    - Responses on a 1–5 scale, centered by subtracting 3.
    - 'economic' questions map to x-axis.
    - 'civil_liberty' questions map to y-axis.

    Returns:
      user_coord: {"label":"You","x":float,"y":float}
      party_coords: [
        {"label": party_name, "x": float, "y": float},
        ...
      ]
    """
    # 1) User
    econ_vals = []
    social_vals = []
    for q in questions:
        qid = str(q["id"])
        if qid in user_answers:
            val = user_answers[qid] - 3
            if "economic" in q.get("dimension", []):
                econ_vals.append(val)
            if "civil_liberty" in q.get("dimension", []):
                social_vals.append(val)

    user_x = float(np.mean(econ_vals)) if econ_vals else 0.0
    user_y = float(np.mean(social_vals)) if social_vals else 0.0
    user_coord = {"label": "You", "x": round(user_x, 2), "y": round(user_y, 2)}

    # 2) Parties
    party_coords = []
    for party in parties:
        pe = []
        ps = []
        for q in questions:
            qid = str(q["id"])
            pos = party.get("positions", {}).get(qid, {}).get("value")
            if pos is not None:
                centered = pos - 3
                if "economic" in q.get("dimension", []):
                    pe.append(centered)
                if "civil_liberty" in q.get("dimension", []):
                    ps.append(centered)

        px = float(np.mean(pe)) if pe else 0.0
        py = float(np.mean(ps)) if ps else 0.0
        party_coords.append({
            "label": party["name"],
            "x": round(px, 2),
            "y": round(py, 2)
        })

    return user_coord, party_coords

