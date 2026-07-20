from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas


def _normaliza_descricao(descricao: str) -> str:
    return " ".join(descricao.strip().lower().split())


# ---------- Sugestao de preco ----------


def buscar_sugestao_preco(db: Session, descricao: str) -> models.ItemPreco | None:
    if not descricao or not descricao.strip():
        return None
    alvo = _normaliza_descricao(descricao)
    itens = db.execute(select(models.ItemPreco)).scalars().all()
    for item in itens:
        if _normaliza_descricao(item.descricao) == alvo:
            return item
    return None


def listar_itens_preco(db: Session) -> list[models.ItemPreco]:
    return list(db.execute(select(models.ItemPreco).order_by(models.ItemPreco.descricao)).scalars().all())


def _registrar_preco(db: Session, descricao: str, unidade: str, preco: float) -> None:
    """Grava/atualiza a memoria de ultimo preco. So deve ser chamado na aprovacao."""
    existente = buscar_sugestao_preco(db, descricao)
    if existente:
        existente.unidade = unidade
        existente.ultimo_preco = preco
        existente.atualizado_em = datetime.utcnow()
    else:
        db.add(
            models.ItemPreco(
                descricao=descricao.strip(),
                unidade=unidade,
                ultimo_preco=preco,
                atualizado_em=datetime.utcnow(),
            )
        )


# ---------- Calculo de item ----------


def _recalcular_item(item: models.OrcamentoItem, checar_sugestao: bool = True, db: Session | None = None) -> None:
    if item.status_cobranca == models.COBRANCA_NORMAL and item.preco_unitario is not None:
        item.preco_total = round(float(item.quantidade or 0) * float(item.preco_unitario), 2)
    else:
        item.preco_total = None
        item.preco_unitario = None

    item.preco_sugerido_diferente = False
    if checar_sugestao and db is not None and item.status_cobranca == models.COBRANCA_NORMAL and item.preco_unitario is not None:
        sugestao = buscar_sugestao_preco(db, item.descricao)
        if sugestao is not None and round(float(sugestao.ultimo_preco), 2) != round(float(item.preco_unitario), 2):
            item.preco_sugerido_diferente = True


# ---------- Orcamento ----------


def criar_orcamento(db: Session, dados: schemas.OrcamentoCreate) -> models.Orcamento:
    orcamento = models.Orcamento(**dados.model_dump())
    db.add(orcamento)
    db.commit()
    db.refresh(orcamento)
    return orcamento


def obter_orcamento(db: Session, orcamento_id: int) -> models.Orcamento | None:
    return db.get(models.Orcamento, orcamento_id)


def listar_orcamentos(db: Session) -> list[models.Orcamento]:
    return list(
        db.execute(select(models.Orcamento).order_by(models.Orcamento.criado_em.desc())).scalars().all()
    )


def atualizar_orcamento(db: Session, orcamento: models.Orcamento, dados: schemas.OrcamentoUpdate) -> models.Orcamento:
    if orcamento.status == models.STATUS_APROVADO:
        raise ValueError("Orçamento aprovado não pode ser editado.")
    for campo, valor in dados.model_dump().items():
        setattr(orcamento, campo, valor)
    db.commit()
    db.refresh(orcamento)
    return orcamento


def excluir_orcamento(db: Session, orcamento: models.Orcamento) -> None:
    db.delete(orcamento)
    db.commit()


# ---------- Categoria ----------


def criar_categoria(db: Session, orcamento: models.Orcamento, dados: schemas.OrcamentoCategoriaCreate) -> models.OrcamentoCategoria:
    categoria = models.OrcamentoCategoria(orcamento_id=orcamento.id, ordem=dados.ordem, titulo=dados.titulo)
    db.add(categoria)
    db.flush()
    for item_dados in dados.itens:
        item = models.OrcamentoItem(categoria_id=categoria.id, **item_dados.model_dump())
        _recalcular_item(item, db=db)
        db.add(item)
    db.commit()
    db.refresh(categoria)
    return categoria


def atualizar_categoria(db: Session, categoria: models.OrcamentoCategoria, dados: schemas.OrcamentoCategoriaUpdate) -> models.OrcamentoCategoria:
    categoria.ordem = dados.ordem
    categoria.titulo = dados.titulo
    db.commit()
    db.refresh(categoria)
    return categoria


def excluir_categoria(db: Session, categoria: models.OrcamentoCategoria) -> None:
    db.delete(categoria)
    db.commit()


# ---------- Item ----------


def criar_item(db: Session, categoria: models.OrcamentoCategoria, dados: schemas.OrcamentoItemCreate) -> models.OrcamentoItem:
    item = models.OrcamentoItem(categoria_id=categoria.id, **dados.model_dump())
    _recalcular_item(item, db=db)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def atualizar_item(db: Session, item: models.OrcamentoItem, dados: schemas.OrcamentoItemUpdate) -> models.OrcamentoItem:
    for campo, valor in dados.model_dump().items():
        setattr(item, campo, valor)
    _recalcular_item(item, db=db)
    db.commit()
    db.refresh(item)
    return item


def excluir_item(db: Session, item: models.OrcamentoItem) -> None:
    db.delete(item)
    db.commit()


# ---------- Totais ----------


def calcular_totais(orcamento: models.Orcamento) -> schemas.OrcamentoTotais:
    subtotais: dict[int, float] = {}
    total_geral = 0.0
    for categoria in orcamento.categorias:
        subtotal = sum(float(item.preco_total) for item in categoria.itens if item.preco_total is not None)
        subtotais[categoria.id] = round(subtotal, 2)
        total_geral += subtotal

    perc_material = float(orcamento.percentual_material or 0) / 100
    perc_servico = float(orcamento.percentual_servico or 0) / 100
    return schemas.OrcamentoTotais(
        total_geral=round(total_geral, 2),
        total_material=round(total_geral * perc_material, 2),
        total_servico=round(total_geral * perc_servico, 2),
        subtotais_categoria=subtotais,
    )


# ---------- Aprovacao ----------


def aprovar_orcamento(db: Session, orcamento: models.Orcamento) -> models.Orcamento:
    if orcamento.status == models.STATUS_APROVADO:
        raise ValueError("Orçamento já está aprovado.")
    if not orcamento.categorias:
        raise ValueError("Orçamento não possui itens para aprovar.")

    for categoria in orcamento.categorias:
        for item in categoria.itens:
            if item.status_cobranca == models.COBRANCA_NORMAL and item.preco_unitario is not None and item.descricao.strip():
                _registrar_preco(db, item.descricao, item.unidade, float(item.preco_unitario))
            item.preco_sugerido_diferente = False

    orcamento.status = models.STATUS_APROVADO
    orcamento.aprovado_em = datetime.utcnow()
    db.commit()
    db.refresh(orcamento)
    return orcamento
