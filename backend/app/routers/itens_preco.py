from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/api/itens-preco", tags=["itens-preco"])


@router.get("", response_model=list[schemas.ItemPrecoRead])
def listar(db: Session = Depends(get_db)):
    return crud.listar_itens_preco(db)


@router.get("/sugestao", response_model=schemas.SugestaoPrecoResponse)
def sugestao(descricao: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    item = crud.buscar_sugestao_preco(db, descricao)
    if item is None:
        return schemas.SugestaoPrecoResponse(encontrado=False)
    return schemas.SugestaoPrecoResponse(
        encontrado=True,
        descricao=item.descricao,
        unidade=item.unidade,
        ultimo_preco=float(item.ultimo_preco),
        atualizado_em=item.atualizado_em,
    )
