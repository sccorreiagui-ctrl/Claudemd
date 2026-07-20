"""Geracao do PDF da proposta, espelhando o layout do excel_generator.py."""

from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from . import models, schemas
from .excel_generator import (
    AGENCIA,
    BANCO,
    CONTA,
    DISPOSICOES_GERAIS,
    EMPRESA_CNPJ,
    EMPRESA_COR_BARRA,
    EMPRESA_NOME,
    PIX,
    RESPONSAVEL_CARGO,
    RESPONSAVEL_CONTATO,
    RESPONSAVEL_NOME,
    STATUS_LABEL,
    _data_por_extenso,
    _fmt_moeda,
)
from .numero_por_extenso import valor_por_extenso

_AZUL = colors.HexColor(f"#{EMPRESA_COR_BARRA}")

_ESTILOS = getSampleStyleSheet()
_ESTILO_CORPO = ParagraphStyle("corpo", parent=_ESTILOS["Normal"], fontSize=9, leading=12)
_ESTILO_CORPO_NEGRITO = ParagraphStyle("corpo_negrito", parent=_ESTILO_CORPO, fontName="Helvetica-Bold")
_ESTILO_TITULO = ParagraphStyle("titulo", parent=_ESTILOS["Normal"], fontSize=13, leading=16, fontName="Helvetica-Bold")
_ESTILO_TABELA_CABECALHO = ParagraphStyle(
    "cabecalho_tabela", parent=_ESTILO_CORPO, fontName="Helvetica-Bold", textColor=colors.white, alignment=1
)
_ESTILO_CATEGORIA = ParagraphStyle("categoria", parent=_ESTILO_CORPO, fontName="Helvetica-Bold")
_ESTILO_SECAO = ParagraphStyle("secao", parent=_ESTILO_CORPO, fontName="Helvetica-Bold", spaceBefore=8, spaceAfter=2)


def _cabecalho_empresa() -> list:
    elementos = [
        Paragraph(f"<b>{EMPRESA_NOME} - CNPJ {EMPRESA_CNPJ}</b>", ParagraphStyle("emp", parent=_ESTILO_CORPO, textColor=_AZUL, fontSize=10)),
        Spacer(1, 3),
        HRFlowable(width="100%", thickness=2.5, color=_AZUL, spaceAfter=10),
    ]
    return elementos


def _pagina_itens(orcamento: models.Orcamento, totais: schemas.OrcamentoTotais) -> list:
    elementos = _cabecalho_empresa()

    numero = orcamento.numero_proposta or "—"
    tabela_topo = Table(
        [[Paragraph(f"<b>PROPOSTA Nº {numero}</b>", _ESTILO_TITULO),
          Paragraph(f"Rio de Janeiro, {_data_por_extenso(orcamento.data_proposta)}", ParagraphStyle("data", parent=_ESTILO_CORPO, alignment=2))]],
        colWidths=[10 * cm, 7.5 * cm],
    )
    tabela_topo.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    elementos += [tabela_topo, Spacer(1, 10)]

    elementos += [
        Paragraph("A", _ESTILO_CORPO_NEGRITO),
        Paragraph(f"<b>{orcamento.cliente_nome or ''}</b>", ParagraphStyle("cliente", parent=_ESTILO_CORPO, fontSize=11, fontName="Helvetica-Bold")),
        Paragraph(f"<b>Att:</b> {orcamento.cliente_att or ''}", _ESTILO_CORPO),
        Paragraph(f"<b>E-mail:</b> {orcamento.cliente_email or ''}", _ESTILO_CORPO),
        Spacer(1, 6),
        Paragraph(f"<b>REF:</b> {orcamento.referencia or ''}", _ESTILO_CORPO),
        Paragraph(f"<b>End:</b> {orcamento.endereco_obra or ''}", _ESTILO_CORPO),
        Spacer(1, 8),
        Paragraph(
            "<b>Prezados, apresentamos nossa proposta tecnico-comercial para execução dos serviços "
            "abaixo descritos:</b>",
            _ESTILO_CORPO,
        ),
        Spacer(1, 10),
    ]

    linhas = [[
        Paragraph("Item", _ESTILO_TABELA_CABECALHO),
        Paragraph("Descrição", _ESTILO_TABELA_CABECALHO),
        Paragraph("Qtd.", _ESTILO_TABELA_CABECALHO),
        Paragraph("Unid.", _ESTILO_TABELA_CABECALHO),
        Paragraph("Preço Unit.", _ESTILO_TABELA_CABECALHO),
        Paragraph("Preço Total", _ESTILO_TABELA_CABECALHO),
    ]]
    estilos_extra = [
        ("BACKGROUND", (0, 0), (-1, 0), _AZUL),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d0d0d0")),
    ]

    linha_atual = 1
    for indice_categoria, categoria in enumerate(orcamento.categorias, start=1):
        linhas.append([
            str(indice_categoria),
            Paragraph((categoria.titulo or "").upper(), _ESTILO_CATEGORIA),
            "", "", "", "",
        ])
        estilos_extra.append(("SPAN", (1, linha_atual), (5, linha_atual)))
        estilos_extra.append(("BACKGROUND", (0, linha_atual), (-1, linha_atual), colors.HexColor("#eaf1f8")))
        linha_atual += 1

        for item in categoria.itens:
            if item.status_cobranca == models.COBRANCA_NORMAL:
                preco_unit = _fmt_moeda(float(item.preco_unitario)) if item.preco_unitario is not None else ""
                preco_total = _fmt_moeda(float(item.preco_total)) if item.preco_total is not None else ""
                linhas.append([
                    "", Paragraph(item.descricao or "", _ESTILO_CORPO),
                    f"{float(item.quantidade):g}" if item.quantidade else "",
                    item.unidade or "", preco_unit, preco_total,
                ])
            else:
                rotulo = STATUS_LABEL.get(item.status_cobranca, "")
                linhas.append([
                    "", Paragraph(item.descricao or "", _ESTILO_CORPO),
                    f"{float(item.quantidade):g}" if item.quantidade else "",
                    item.unidade or "", "",
                    Paragraph(rotulo, ParagraphStyle("rotulo", parent=_ESTILO_CORPO, alignment=1)),
                ])
            linha_atual += 1

    linhas.append(["", Paragraph("<b>TOTAL DA PROPOSTA</b>", _ESTILO_CORPO_NEGRITO), "", "", "", Paragraph(f"<b>{_fmt_moeda(totais.total_geral)}</b>", ParagraphStyle("total", parent=_ESTILO_CORPO_NEGRITO, alignment=2))])
    estilos_extra.append(("SPAN", (0, linha_atual), (4, linha_atual)))
    estilos_extra.append(("LINEABOVE", (0, linha_atual), (-1, linha_atual), 1.2, _AZUL))

    tabela = Table(linhas, colWidths=[1.3 * cm, 8 * cm, 1.7 * cm, 1.5 * cm, 2.3 * cm, 2.7 * cm], repeatRows=1)
    tabela.setStyle(TableStyle(estilos_extra))
    elementos.append(tabela)
    return elementos


def _pagina_condicoes(orcamento: models.Orcamento, totais: schemas.OrcamentoTotais) -> list:
    elementos = _cabecalho_empresa()
    elementos.append(Paragraph(f"<b>PROPOSTA Nº {orcamento.numero_proposta or '—'}</b>", _ESTILO_TITULO))
    elementos.append(Spacer(1, 10))

    valor_extenso = valor_por_extenso(totais.total_geral)
    elementos += [
        Paragraph("<b>1. PREÇO GLOBAL:</b>", _ESTILO_SECAO),
        Paragraph(f"{_fmt_moeda(totais.total_geral)} ({valor_extenso})", _ESTILO_CORPO),
        Paragraph("<b>2. CONDIÇÕES DE PAGAMENTO:</b>", _ESTILO_SECAO),
        Paragraph(orcamento.condicoes_pagamento or "", _ESTILO_CORPO),
        Paragraph("<b>3. PRAZO DE EXECUÇÃO</b>", _ESTILO_SECAO),
        Paragraph("Conforme cronograma da obra", _ESTILO_CORPO),
        Paragraph(
            f"<b>4. PORCENTAGENS:</b> {float(orcamento.percentual_material):g}% material / "
            f"{float(orcamento.percentual_servico):g}% serviço",
            _ESTILO_SECAO,
        ),
        Paragraph("<b>5. DISPOSIÇÕES GERAIS</b>", _ESTILO_SECAO),
    ]
    for indice, texto in enumerate(DISPOSICOES_GERAIS, start=1):
        elementos.append(Paragraph(f"5.{indice}. {texto}", _ESTILO_CORPO))

    elementos += [
        Spacer(1, 10),
        Paragraph("<b>DADOS PARA FATURAMENTO:</b>", _ESTILO_SECAO),
        Paragraph(f"Banco: {BANCO} &nbsp;&nbsp; Ag.: {AGENCIA} &nbsp;&nbsp; Cc.: {CONTA} &nbsp;&nbsp; Pix {PIX}", _ESTILO_CORPO),
        Spacer(1, 16),
        Paragraph("Atenciosamente,", _ESTILO_CORPO),
        Spacer(1, 14),
        Paragraph(f"<b>{RESPONSAVEL_NOME}</b>", _ESTILO_CORPO),
        Paragraph(RESPONSAVEL_CARGO, _ESTILO_CORPO),
        Paragraph(RESPONSAVEL_CONTATO, _ESTILO_CORPO),
    ]
    return elementos


def gerar_pdf(orcamento: models.Orcamento, totais: schemas.OrcamentoTotais) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=1.8 * cm, rightMargin=1.8 * cm, topMargin=1.6 * cm, bottomMargin=1.6 * cm,
        title=f"Proposta {orcamento.numero_proposta}",
    )
    elementos = _pagina_itens(orcamento, totais)
    elementos.append(PageBreak())
    elementos += _pagina_condicoes(orcamento, totais)
    doc.build(elementos)
    buffer.seek(0)
    return buffer
