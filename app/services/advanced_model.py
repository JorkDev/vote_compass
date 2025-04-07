import numpy as np

def compute_latent_positions(user_answers: dict, questions: list, parties: list):
    """
    Compute latent positions for the user and parties using a simplified model.
    - Responses are on a 1–5 scale.
    - Center responses by subtracting 3.
    - 'economic' questions contribute to the x-axis.
    - 'civil_liberty' questions contribute to the y-axis.
    In production, replace this with factor analysis and a Bayesian ordered probit model.
    """
    # Compute user's latent coordinates
    econ = []
    social = []
    for q in questions:
        qid = q["id"]
        if qid in user_answers:
            ans = user_answers[qid]
            if "economic" in q.get("dimension", []):
                econ.append(ans - 3)
            if "civil_liberty" in q.get("dimension", []):
                social.append(ans - 3)
    x = np.mean(econ) if econ else 0
    y = np.mean(social) if social else 0
    user_coord = {"label": "You", "x": round(x, 2), "y": round(y, 2)}
    
    # Compute party latent coordinates
    party_coords = []
    for party in parties:
        econ_vals = []
        social_vals = []
        for q in questions:
            qid = q["id"]
            pos = party["positions"].get(qid, {}).get("value")
            if pos is not None:
                if "economic" in q.get("dimension", []):
                    econ_vals.append(pos - 3)
                if "civil_liberty" in q.get("dimension", []):
                    social_vals.append(pos - 3)
        px = np.mean(econ_vals) if econ_vals else 0
        py = np.mean(social_vals) if social_vals else 0
        party_coords.append({
            "label": party["name"],
            "x": round(px, 2),
            "y": round(py, 2)
        })
    
    return user_coord, party_coords
