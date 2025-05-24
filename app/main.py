# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1 import users, questions, parties, answers, results, match

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        docs_url="/docs",
        redoc_url="/redoc",
    )

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
