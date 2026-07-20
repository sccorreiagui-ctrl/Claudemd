from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/api/catalogo", tags=["catalogo"])


@router.get("/servicos", response_model=list[schemas.ServicoCatalogoRead])
def buscar_servicos(q: str = Query(..., min_length=2), db: Session = Depends(get_db)):
    return crud.buscar_catalogo(db, q)


@router.get("/templates", response_model=list[schemas.CategoriaTemplateRead])
def listar_templates(db: Session = Depends(get_db)):
    return crud.listar_templates(db)
