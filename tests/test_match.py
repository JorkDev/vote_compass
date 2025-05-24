# tests/test_match.py
def test_match_endpoint(client):
    # 1) seed a party
    party = {
        "party_id": "p1",
        "name": "P1",
        "faction": "center",
        "description": "",
        "inscription_date": None,
        "founder": None,
        "current_leader": None,
        "presidential_candidate": None,
        "positions": {"1": {"value": 3, "source": ""}}
    }
    client.post("/api/v1/parties/", json=party)

    # 2) seed a question
    question = {
        "id": "1",
        "text": "Q?",
        "options": ["1","2","3","4","5"],
        "dimension": "economic",
        "topic": "t",
        "additional_info": None
    }
    client.post("/api/v1/questions/", json=question)

    # 3) call /match
    payload = {"answers": {"1": 3}, "weights": {"1": 1}}
    res = client.post("/api/v1/match/", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "matches" in data
    assert isinstance(data["matches"], list)
    assert data["matches"][0]["party"] == "P1"
