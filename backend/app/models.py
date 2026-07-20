from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base

STATUS_RASCUNHO = "rascunho"
STATUS_APROVADO = "aprovado"

COBRANCA_NORMAL = "normal"
COBRANCA_POR_CONTA_CONTRATANTE = "por_conta_contratante"
COBRANCA_INCLUSO = "incluso"


class ItemPreco(Base):
    """Memoria de ultimo preco aprovado por item (Opcao A)."""

    __tablename__ = "itens_preco"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(Text, nullable=False, unique=True, index=True)
    unidade: Mapped[str] = mapped_column(String(20), nullable=False)
    ultimo_preco: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    atualizado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Orcamento(Base):
    __tablename__ = "orcamentos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    numero_proposta: Mapped[str] = mapped_column(String(50), nullable=False)
    data_proposta: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    cliente_nome: Mapped[str] = mapped_column(String(200), default="")
    cliente_email: Mapped[str] = mapped_column(String(200), default="")
    cliente_att: Mapped[str] = mapped_column(String(200), default="")
    referencia: Mapped[str] = mapped_column(String(200), default="")
    endereco_obra: Mapped[str] = mapped_column(Text, default="")
    condicoes_pagamento: Mapped[str] = mapped_column(Text, default="")
    percentual_material: Mapped[float] = mapped_column(Numeric(5, 2), default=60)
    percentual_servico: Mapped[float] = mapped_column(Numeric(5, 2), default=40)
    status: Mapped[str] = mapped_column(String(20), default=STATUS_RASCUNHO)
    criado_por: Mapped[str] = mapped_column(String(100), default="")
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    aprovado_em: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    numero_revisao: Mapped[int] = mapped_column(Integer, default=1)
    orcamento_origem_id: Mapped[int | None] = mapped_column(
        ForeignKey("orcamentos.id", ondelete="SET NULL"), nullable=True
    )

    categorias: Mapped[list["OrcamentoCategoria"]] = relationship(
        back_populates="orcamento",
        cascade="all, delete-orphan",
        order_by="OrcamentoCategoria.ordem",
    )


class OrcamentoCategoria(Base):
    __tablename__ = "orcamento_categorias"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    orcamento_id: Mapped[int] = mapped_column(ForeignKey("orcamentos.id", ondelete="CASCADE"))
    ordem: Mapped[int] = mapped_column(Integer, default=0)
    titulo: Mapped[str] = mapped_column(String(300), default="")

    orcamento: Mapped["Orcamento"] = relationship(back_populates="categorias")
    itens: Mapped[list["OrcamentoItem"]] = relationship(
        back_populates="categoria",
        cascade="all, delete-orphan",
        order_by="OrcamentoItem.ordem",
    )


class OrcamentoItem(Base):
    __tablename__ = "orcamento_itens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    categoria_id: Mapped[int] = mapped_column(ForeignKey("orcamento_categorias.id", ondelete="CASCADE"))
    ordem: Mapped[int] = mapped_column(Integer, default=0)
    descricao: Mapped[str] = mapped_column(Text, default="")
    quantidade: Mapped[float] = mapped_column(Numeric(12, 3), default=0)
    unidade: Mapped[str] = mapped_column(String(20), default="")
    status_cobranca: Mapped[str] = mapped_column(String(30), default=COBRANCA_NORMAL)
    preco_unitario: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    preco_total: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    preco_sugerido_diferente: Mapped[bool] = mapped_column(Boolean, default=False)
    percentual_material: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)

    categoria: Mapped["OrcamentoCategoria"] = relationship(back_populates="itens")


class ServicoCatalogo(Base):
    """Catalogo de descricoes de servico reutilizaveis (autocomplete ao criar itens)."""

    __tablename__ = "servico_catalogo"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(Text, nullable=False, unique=True, index=True)
    unidade_padrao: Mapped[str] = mapped_column(String(20), default="")
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class CategoriaTemplate(Base):
    """Modelo de categoria com itens tipicos, para acelerar a montagem do orcamento."""

    __tablename__ = "categoria_templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    ordem: Mapped[int] = mapped_column(Integer, default=0)

    itens: Mapped[list["CategoriaTemplateItem"]] = relationship(
        back_populates="template",
        cascade="all, delete-orphan",
        order_by="CategoriaTemplateItem.ordem",
    )


class CategoriaTemplateItem(Base):
    __tablename__ = "categoria_template_itens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    template_id: Mapped[int] = mapped_column(ForeignKey("categoria_templates.id", ondelete="CASCADE"))
    ordem: Mapped[int] = mapped_column(Integer, default=0)
    descricao: Mapped[str] = mapped_column(Text, default="")
    unidade: Mapped[str] = mapped_column(String(20), default="")

    template: Mapped["CategoriaTemplate"] = relationship(back_populates="itens")
