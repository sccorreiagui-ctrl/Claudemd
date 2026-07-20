import re
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas

_PADRAO_REV = re.compile(r"\s+rev\s*\d+\s*$", re.IGNORECASE)


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


# ---------- Catalogo de servicos (autocomplete) ----------


def registrar_no_catalogo(db: Session, descricao: str, unidade: str) -> None:
    descricao = (descricao or "").strip()
    if not descricao:
        return
    alvo = _normaliza_descricao(descricao)
    existentes = db.execute(select(models.ServicoCatalogo)).scalars().all()
    for item in existentes:
        if _normaliza_descricao(item.descricao) == alvo:
            if unidade and not item.unidade_padrao:
                item.unidade_padrao = unidade
            return
    db.add(models.ServicoCatalogo(descricao=descricao, unidade_padrao=unidade or ""))


def buscar_catalogo(db: Session, consulta: str, limite: int = 20) -> list[models.ServicoCatalogo]:
    alvo = _normaliza_descricao(consulta)
    if not alvo:
        return []
    resultado = []
    for item in db.execute(select(models.ServicoCatalogo)).scalars().all():
        if alvo in _normaliza_descricao(item.descricao):
            resultado.append(item)
    resultado.sort(key=lambda i: len(i.descricao))
    return resultado[:limite]


# ---------- Templates de categoria ----------


def listar_templates(db: Session) -> list[models.CategoriaTemplate]:
    return list(
        db.execute(select(models.CategoriaTemplate).order_by(models.CategoriaTemplate.ordem)).scalars().all()
    )


def obter_template(db: Session, template_id: int) -> models.CategoriaTemplate | None:
    return db.get(models.CategoriaTemplate, template_id)


def aplicar_template(
    db: Session, orcamento: models.Orcamento, template: models.CategoriaTemplate
) -> models.OrcamentoCategoria:
    categoria = models.OrcamentoCategoria(orcamento_id=orcamento.id, ordem=len(orcamento.categorias), titulo=template.nome)
    db.add(categoria)
    db.flush()
    for ordem, template_item in enumerate(template.itens):
        item = models.OrcamentoItem(
            categoria_id=categoria.id,
            ordem=ordem,
            descricao=template_item.descricao,
            quantidade=0,
            unidade=template_item.unidade,
            status_cobranca=models.COBRANCA_NORMAL,
        )
        _recalcular_item(item, db=db)
        db.add(item)
    db.commit()
    db.refresh(categoria)
    return categoria


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
        registrar_no_catalogo(db, item.descricao, item.unidade)
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
    registrar_no_catalogo(db, item.descricao, item.unidade)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def atualizar_item(db: Session, item: models.OrcamentoItem, dados: schemas.OrcamentoItemUpdate) -> models.OrcamentoItem:
    for campo, valor in dados.model_dump().items():
        setattr(item, campo, valor)
    _recalcular_item(item, db=db)
    registrar_no_catalogo(db, item.descricao, item.unidade)
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
    total_material = 0.0
    perc_material_padrao = float(orcamento.percentual_material or 0)

    for categoria in orcamento.categorias:
        subtotal = 0.0
        for item in categoria.itens:
            if item.preco_total is None:
                continue
            valor_item = float(item.preco_total)
            subtotal += valor_item
            perc_item = float(item.percentual_material) if item.percentual_material is not None else perc_material_padrao
            total_material += valor_item * perc_item / 100
        subtotais[categoria.id] = round(subtotal, 2)
        total_geral += subtotal

    return schemas.OrcamentoTotais(
        total_geral=round(total_geral, 2),
        total_material=round(total_material, 2),
        total_servico=round(total_geral - total_material, 2),
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


# ---------- Duplicacao e revisao ----------


def _clonar_categorias(db: Session, origem: models.Orcamento, destino: models.Orcamento) -> None:
    for categoria in origem.categorias:
        nova_categoria = models.OrcamentoCategoria(orcamento_id=destino.id, ordem=categoria.ordem, titulo=categoria.titulo)
        db.add(nova_categoria)
        db.flush()
        for item in categoria.itens:
            novo_item = models.OrcamentoItem(
                categoria_id=nova_categoria.id,
                ordem=item.ordem,
                descricao=item.descricao,
                quantidade=item.quantidade,
                unidade=item.unidade,
                status_cobranca=item.status_cobranca,
                preco_unitario=item.preco_unitario,
                percentual_material=item.percentual_material,
            )
            _recalcular_item(novo_item, db=db)
            db.add(novo_item)


def duplicar_orcamento(db: Session, orcamento: models.Orcamento) -> models.Orcamento:
    numero = orcamento.numero_proposta.strip()
    novo = models.Orcamento(
        numero_proposta=f"{numero} (cópia)" if numero else "",
        cliente_nome=orcamento.cliente_nome,
        cliente_email=orcamento.cliente_email,
        cliente_att=orcamento.cliente_att,
        referencia=orcamento.referencia,
        endereco_obra=orcamento.endereco_obra,
        condicoes_pagamento=orcamento.condicoes_pagamento,
        percentual_material=orcamento.percentual_material,
        percentual_servico=orcamento.percentual_servico,
        criado_por=orcamento.criado_por,
        status=models.STATUS_RASCUNHO,
        numero_revisao=1,
        orcamento_origem_id=None,
    )
    db.add(novo)
    db.flush()
    _clonar_categorias(db, orcamento, novo)
    db.commit()
    db.refresh(novo)
    return novo


def nova_revisao(db: Session, orcamento: models.Orcamento) -> models.Orcamento:
    proxima_revisao = orcamento.numero_revisao + 1
    base = _PADRAO_REV.sub("", orcamento.numero_proposta.strip())
    novo = models.Orcamento(
        numero_proposta=f"{base} Rev {proxima_revisao:02d}".strip(),
        cliente_nome=orcamento.cliente_nome,
        cliente_email=orcamento.cliente_email,
        cliente_att=orcamento.cliente_att,
        referencia=orcamento.referencia,
        endereco_obra=orcamento.endereco_obra,
        condicoes_pagamento=orcamento.condicoes_pagamento,
        percentual_material=orcamento.percentual_material,
        percentual_servico=orcamento.percentual_servico,
        criado_por=orcamento.criado_por,
        status=models.STATUS_RASCUNHO,
        numero_revisao=proxima_revisao,
        orcamento_origem_id=orcamento.id,
    )
    db.add(novo)
    db.flush()
    _clonar_categorias(db, orcamento, novo)
    db.commit()
    db.refresh(novo)
    return novo
