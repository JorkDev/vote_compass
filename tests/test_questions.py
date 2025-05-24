# tests/test_questions.py
import uuid

BASE = "/api/v1/questions/"

sample = {
    "id": "q1",
    "text": "Sample?",
    "options": ["No", "Yes"],
    "dimension": "economic",
    "topic": "sample",
    "additional_info": None
}

def test_crud_questions(client):
    # Create
    res = client.post(BASE, json=sample)
    assert res.status_code == 201
    assert res.json()["id"] == sample["id"]

    # List
    res = client.get(BASE)
    assert res.status_code == 200
    assert any(q["id"] == sample["id"] for q in res.json())

    # Read
    res = client.get(BASE + sample["id"])
    assert res.status_code == 200

    # Update
    updated = sample.copy()
    updated["text"] = "Updated?"
    res = client.put(BASE + sample["id"], json=updated)
    assert res.status_code == 200
    assert res.json()["text"] == "Updated?"

    # Delete
    res = client.delete(BASE + sample["id"])
    assert res.status_code == 204
    # Now 404
    res = client.get(BASE + sample["id"])
    assert res.status_code == 404
