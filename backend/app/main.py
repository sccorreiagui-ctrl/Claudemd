import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .database import Base, SessionLocal, engine
from .routers import catalogo, itens_preco, orcamentos
from .seed import seed_se_vazio

Base.metadata.create_all(bind=engine)

with SessionLocal() as _sessao_seed:
    seed_se_vazio(_sessao_seed)

app = FastAPI(title="Automação de Orçamentos — Rigel Engenharia")

app.include_router(orcamentos.router)
app.include_router(itens_preco.router)
app.include_router(catalogo.router)

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
if os.path.isdir(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
