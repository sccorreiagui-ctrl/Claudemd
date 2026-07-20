from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..database import get_db
from ..excel_generator import gerar_excel

router = APIRouter(prefix="/api/orcamentos", tags=["orcamentos"])


def _obter_ou_404(db: Session, orcamento_id: int) -> models.Orcamento:
    orcamento = crud.obter_orcamento(db, orcamento_id)
    if orcamento is None:
        raise HTTPException(status_code=404, detail="Orçamento não encontrado.")
    return orcamento


def _obter_categoria_ou_404(orcamento: models.Orcamento, categoria_id: int) -> models.OrcamentoCategoria:
    for categoria in orcamento.categorias:
        if categoria.id == categoria_id:
            return categoria
    raise HTTPException(status_code=404, detail="Categoria não encontrada.")


def _obter_item_ou_404(categoria: models.OrcamentoCategoria, item_id: int) -> models.OrcamentoItem:
    for item in categoria.itens:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item não encontrado.")


@router.get("", response_model=list[schemas.OrcamentoListItem])
def listar(db: Session = Depends(get_db)):
    return crud.listar_orcamentos(db)


@router.post("", response_model=schemas.OrcamentoRead, status_code=201)
def criar(dados: schemas.OrcamentoCreate, db: Session = Depends(get_db)):
    return crud.criar_orcamento(db, dados)


@router.get("/{orcamento_id}", response_model=schemas.OrcamentoRead)
def obter(orcamento_id: int, db: Session = Depends(get_db)):
    return _obter_ou_404(db, orcamento_id)


@router.put("/{orcamento_id}", response_model=schemas.OrcamentoRead)
def atualizar(orcamento_id: int, dados: schemas.OrcamentoUpdate, db: Session = Depends(get_db)):
    orcamento = _obter_ou_404(db, orcamento_id)
    try:
        return crud.atualizar_orcamento(db, orcamento, dados)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.delete("/{orcamento_id}", status_code=204)
def excluir(orcamento_id: int, db: Session = Depends(get_db)):
    orcamento = _obter_ou_404(db, orcamento_id)
    crud.excluir_orcamento(db, orcamento)


@router.get("/{orcamento_id}/totais", response_model=schemas.OrcamentoTotais)
def totais(orcamento_id: int, db: Session = Depends(get_db)):
    orcamento = _obter_ou_404(db, orcamento_id)
    return crud.calcular_totais(orcamento)


@router.post("/{orcamento_id}/aprovar", response_model=schemas.OrcamentoRead)
def aprovar(orcamento_id: int, db: Session = Depends(get_db)):
    orcamento = _obter_ou_404(db, orcamento_id)
    try:
        return crud.aprovar_orcamento(db, orcamento)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("/{orcamento_id}/excel")
def baixar_excel(orcamento_id: int, db: Session = Depends(get_db)):
    orcamento = _obter_ou_404(db, orcamento_id)
    if not orcamento.categorias:
        raise HTTPException(status_code=409, detail="Orçamento não possui categorias/itens.")
    totais_calculados = crud.calcular_totais(orcamento)
    buffer = gerar_excel(orcamento, totais_calculados)
    identificador = orcamento.numero_proposta or str(orcamento.id)
    nome_arquivo = f"Proposta_{identificador.replace(' ', '_')}.xlsx"
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{nome_arquivo}"'},
    )


# ---------- Categorias ----------


@router.post("/{orcamento_id}/categorias", response_model=schemas.OrcamentoCategoriaRead, status_code=201)
def criar_categoria(orcamento_id: int, dados: schemas.OrcamentoCategoriaCreate, db: Session = Depends(get_db)):
    orcamento = _obter_ou_404(db, orcamento_id)
    if orcamento.status == models.STATUS_APROVADO:
        raise HTTPException(status_code=409, detail="Orçamento aprovado não pode ser editado.")
    return crud.criar_categoria(db, orcamento, dados)


@router.put("/{orcamento_id}/categorias/{categoria_id}", response_model=schemas.OrcamentoCategoriaRead)
def atualizar_categoria(
    orcamento_id: int, categoria_id: int, dados: schemas.OrcamentoCategoriaUpdate, db: Session = Depends(get_db)
):
    orcamento = _obter_ou_404(db, orcamento_id)
    if orcamento.status == models.STATUS_APROVADO:
        raise HTTPException(status_code=409, detail="Orçamento aprovado não pode ser editado.")
    categoria = _obter_categoria_ou_404(orcamento, categoria_id)
    return crud.atualizar_categoria(db, categoria, dados)


@router.delete("/{orcamento_id}/categorias/{categoria_id}", status_code=204)
def excluir_categoria(orcamento_id: int, categoria_id: int, db: Session = Depends(get_db)):
    orcamento = _obter_ou_404(db, orcamento_id)
    if orcamento.status == models.STATUS_APROVADO:
        raise HTTPException(status_code=409, detail="Orçamento aprovado não pode ser editado.")
    categoria = _obter_categoria_ou_404(orcamento, categoria_id)
    crud.excluir_categoria(db, categoria)


# ---------- Itens ----------


@router.post("/{orcamento_id}/categorias/{categoria_id}/itens", response_model=schemas.OrcamentoItemRead, status_code=201)
def criar_item(
    orcamento_id: int, categoria_id: int, dados: schemas.OrcamentoItemCreate, db: Session = Depends(get_db)
):
    orcamento = _obter_ou_404(db, orcamento_id)
    if orcamento.status == models.STATUS_APROVADO:
        raise HTTPException(status_code=409, detail="Orçamento aprovado não pode ser editado.")
    categoria = _obter_categoria_ou_404(orcamento, categoria_id)
    return crud.criar_item(db, categoria, dados)


@router.put("/{orcamento_id}/categorias/{categoria_id}/itens/{item_id}", response_model=schemas.OrcamentoItemRead)
def atualizar_item(
    orcamento_id: int,
    categoria_id: int,
    item_id: int,
    dados: schemas.OrcamentoItemUpdate,
    db: Session = Depends(get_db),
):
    orcamento = _obter_ou_404(db, orcamento_id)
    if orcamento.status == models.STATUS_APROVADO:
        raise HTTPException(status_code=409, detail="Orçamento aprovado não pode ser editado.")
    categoria = _obter_categoria_ou_404(orcamento, categoria_id)
    item = _obter_item_ou_404(categoria, item_id)
    return crud.atualizar_item(db, item, dados)


@router.delete("/{orcamento_id}/categorias/{categoria_id}/itens/{item_id}", status_code=204)
def excluir_item(orcamento_id: int, categoria_id: int, item_id: int, db: Session = Depends(get_db)):
    orcamento = _obter_ou_404(db, orcamento_id)
    if orcamento.status == models.STATUS_APROVADO:
        raise HTTPException(status_code=409, detail="Orçamento aprovado não pode ser editado.")
    categoria = _obter_categoria_ou_404(orcamento, categoria_id)
    item = _obter_item_ou_404(categoria, item_id)
    crud.excluir_item(db, item)
