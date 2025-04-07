from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict
from app.services.matcher import match_user_to_parties
from app.utils.helpers import load_json

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

# Load data once at startup
parties = load_json("app/data/parties.json")
questions = load_json("app/data/questions.json")


class MatchRequest(BaseModel):
    answers: Dict[str, int]
    weights: Dict[str, int]


@app.post("/match")
def match(request: MatchRequest):
    results = match_user_to_parties(request.answers, request.weights, parties)
    return {"matches": results}


@app.get("/questions")
def get_questions():
    return JSONResponse(content=questions)


class Answers(BaseModel):
    answers: Dict[str, int]


@app.post("/positions")
def get_positions(answers_payload: Answers):
    user_answers = answers_payload.answers
    from app.services.advanced_model import compute_latent_positions

    user_coord, party_coords = compute_latent_positions(
        user_answers, questions, parties
    )
    data = [user_coord] + party_coords
    return JSONResponse(content=data)


# Landing flow endpoints
@app.get("/", response_class=HTMLResponse)
def landing(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/begin", response_class=HTMLResponse)
def begin(request: Request):
    return templates.TemplateResponse("begin.html", {"request": request})


@app.get("/quiz", response_class=HTMLResponse)
def quiz(request: Request):
    return templates.TemplateResponse("quiz.html", {"request": request})


@app.get("/results", response_class=HTMLResponse)
def results(request: Request):
    return templates.TemplateResponse("results.html", {"request": request})
