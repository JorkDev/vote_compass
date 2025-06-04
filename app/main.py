# app/main.py
from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uuid import UUID
import requests
import traceback

from app.core.config import settings
from app.api.v1 import users, questions, parties, answers, results, match
from app.db.session import get_db

templates = Jinja2Templates(directory="app/templates")

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    @app.get("/", response_class=HTMLResponse)
    def read_root(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    @app.post("/truncate", response_class=PlainTextResponse)
    def truncate_all(db=Depends(get_db)):
        db.execute("TRUNCATE answers, results, parties, questions, users RESTART IDENTITY CASCADE;")
        db.commit()
        return "✅ Database truncated."

    @app.get("/quiz")
    def get_quiz(request: Request, email: str = ""):
        # questions = requests.get("http://api:8000/api/v1/questions/").json()
        questions = requests.get("http://localhost:8000/api/v1/questions/").json()

        return templates.TemplateResponse(
            "quiz.html", {"request": request, "questions": questions, "email": email}
        )

    @app.post("/quiz")
    async def post_quiz(request: Request):
        form = await request.form()

        # 1) Parse form data
        try:
            email = form.get("email") or None
            answers = {}
            weights = {}
            for key, val in form.multi_items():
                if key.startswith("answer_"):
                    qid = key.split("_", 1)[1]
                    answers[qid] = int(val)
                if key.startswith("weight_"):
                    qid = key.split("_", 1)[1]
                    weights[qid] = int(val)
        except Exception as exc:
            tb = traceback.format_exc()
            raise HTTPException(
                status_code=400,
                detail=f"Error parsing form data:\n{tb}"
            )

        # 2) Create or fetch user (if email provided)
        user_id = None
        if email:
            try:
                r = requests.post("http://localhost:8000/api/v1/users/", json={"email": email})
                r.raise_for_status()
                user_id = r.json().get("id")
            except Exception as exc:
                tb = traceback.format_exc()
                raise HTTPException(
                    status_code=502,
                    detail=f"Error creating/fetching user:\n{tb}"
                )

        # 3) Call the results endpoint
        payload = {"answers": answers, "weights": weights}
        if user_id is not None:
            payload["user_id"] = user_id

        try:
            res = requests.post("http://localhost:8000/api/v1/results/", json=payload)
            res.raise_for_status()
            data = res.json()
            token = data.get("token")
            if not token:
                raise ValueError("No token returned from results endpoint.")
        except Exception as exc:
            tb = traceback.format_exc()
            raise HTTPException(
                status_code=502,
                detail=f"Error computing results:\n{tb}"
            )

        # 4) Redirect to the results page
        return RedirectResponse(url=f"/results/{token}", status_code=303)

    @app.get("/results/{token}")
    def show_results(request: Request, token: UUID):
        return templates.TemplateResponse(
            "results.html",
            {"request": request, "token": token}
        )

    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(o) for o in settings.cors_origins],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(users.router,     prefix="/api/v1/users",     tags=["users"])
    app.include_router(questions.router, prefix="/api/v1/questions", tags=["questions"])
    app.include_router(parties.router,   prefix="/api/v1/parties",   tags=["parties"])
    app.include_router(answers.router,   prefix="/api/v1/answers",   tags=["answers"])
    app.include_router(results.router,   prefix="/api/v1/results",   tags=["results"])
    app.include_router(match.router,     prefix="/api/v1/match",     tags=["match"])

    return app

app = create_app()
