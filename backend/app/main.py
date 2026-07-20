import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .database import Base, engine
from .routers import itens_preco, orcamentos

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Automação de Orçamentos — Rigel Engenharia")

app.include_router(orcamentos.router)
app.include_router(itens_preco.router)

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
if os.path.isdir(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
