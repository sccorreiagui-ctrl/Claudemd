from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

StatusCobranca = Literal["normal", "por_conta_contratante", "incluso"]
StatusOrcamento = Literal["rascunho", "aprovado"]


# ---------- Itens de preco (memoria) ----------


class ItemPrecoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    descricao: str
    unidade: str
    ultimo_preco: float
    atualizado_em: datetime


class SugestaoPrecoResponse(BaseModel):
    encontrado: bool
    descricao: str | None = None
    unidade: str | None = None
    ultimo_preco: float | None = None
    atualizado_em: datetime | None = None


# ---------- Item do orcamento ----------


class OrcamentoItemBase(BaseModel):
    ordem: int = 0
    descricao: str = ""
    quantidade: float = 0
    unidade: str = ""
    status_cobranca: StatusCobranca = "normal"
    preco_unitario: float | None = None
    percentual_material: float | None = None


class OrcamentoItemCreate(OrcamentoItemBase):
    pass


class OrcamentoItemUpdate(OrcamentoItemBase):
    pass


class OrcamentoItemRead(OrcamentoItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    categoria_id: int
    preco_total: float | None = None
    preco_sugerido_diferente: bool = False


# ---------- Categoria do orcamento ----------


class OrcamentoCategoriaBase(BaseModel):
    ordem: int = 0
    titulo: str = ""


class OrcamentoCategoriaCreate(OrcamentoCategoriaBase):
    itens: list[OrcamentoItemCreate] = Field(default_factory=list)


class OrcamentoCategoriaUpdate(OrcamentoCategoriaBase):
    pass


class OrcamentoCategoriaRead(OrcamentoCategoriaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    orcamento_id: int
    itens: list[OrcamentoItemRead] = Field(default_factory=list)


# ---------- Orcamento ----------


class OrcamentoBase(BaseModel):
    numero_proposta: str = ""
    cliente_nome: str = ""
    cliente_email: str = ""
    cliente_att: str = ""
    referencia: str = "Impermeabilização"
    endereco_obra: str = ""
    condicoes_pagamento: str = ""
    percentual_material: float = 60
    percentual_servico: float = 40
    criado_por: str = ""


class OrcamentoCreate(OrcamentoBase):
    pass


class OrcamentoUpdate(OrcamentoBase):
    pass


class OrcamentoListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    numero_proposta: str
    cliente_nome: str
    referencia: str
    status: StatusOrcamento
    criado_em: datetime
    aprovado_em: datetime | None = None
    numero_revisao: int = 1
    orcamento_origem_id: int | None = None


class OrcamentoRead(OrcamentoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: StatusOrcamento
    data_proposta: datetime
    criado_em: datetime
    aprovado_em: datetime | None = None
    numero_revisao: int = 1
    orcamento_origem_id: int | None = None
    categorias: list[OrcamentoCategoriaRead] = Field(default_factory=list)


class OrcamentoTotais(BaseModel):
    total_geral: float
    total_material: float
    total_servico: float
    subtotais_categoria: dict[int, float]


# ---------- Catalogo de servicos ----------


class ServicoCatalogoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    descricao: str
    unidade_padrao: str


# ---------- Templates de categoria ----------


class CategoriaTemplateItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ordem: int
    descricao: str
    unidade: str


class CategoriaTemplateRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    ordem: int
    itens: list[CategoriaTemplateItemRead] = Field(default_factory=list)
