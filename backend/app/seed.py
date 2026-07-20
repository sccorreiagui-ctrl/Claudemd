"""Dados iniciais de catalogo de servicos e templates de categoria.

Extraidos das propostas reais da Rigel (Delfim Moreira, Esquina do Leblon, Cisterna)
para o sistema ja nascer util, sem exigir que o catalogo seja povoado do zero.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models

CATALOGO_SERVICOS: list[tuple[str, str]] = [
    (
        "Regularização: Argamassa de cimento portland e areia, traço volumétrico 1:3, com "
        "acabamento áspero, desempenado fino, isento de quaisquer aditivos, consistência firme, "
        "não sendo permitido o tipo \"farofa\", com caimento de 0,5% para os ralos",
        "m²",
    ),
    (
        "Impermeabilização: com argamassa polimérica tipo Viaplus 100 ou similar, consumo 3kg/m², "
        "seguido de argamassa termoplástica, Viaplus 700 ou similar, consumo de 4kg/m²",
        "m²",
    ),
    (
        "Impermeabilização: com Manta asfáltica Tipo III, Classe A, espessura 3mm, totalmente "
        "aderida no maçarico. Manta Asfáltica Tipo Torodin ou equivalente.",
        "m²",
    ),
    (
        "Proteção mecânica piso e rodapés: Aplicação de uma camada de chapisco de cimento e areia "
        "traço 1:3, seguido da colocação de uma tela plástica (tela de polietileno, gramatura "
        "205 gr/m², com malha 14 x 14 mm (~½\"), Nortene ou equivalente.",
        "m²",
    ),
    ("Preparo e limpeza da superfície: Lixamento e limpeza de substrato com lava jato de alta pressão", "m²"),
    ("Impermeabilização: Membrana Epóxi, espessura de filme seco 1000 micrômetros.", "m²"),
    (
        "Membrana de polímero acrílico com cimento e fibras, estruturado com tela resinada, "
        "espessura ou revestida, esp. mín. 2,0 mm",
        "m²",
    ),
    ("Contrapiso com caimento de 0,5%", "m²"),
    ("Proteção mecânica: assentamento do piso sobre a camada impermeável com AC III", "m²"),
    (
        "Impermeabilização: Manta asfáltica Tipo III, espessura 4mm, aderida com asfalto quente. "
        "Manta asfáltica Tipo Torodin ou equivalente.",
        "m²",
    ),
    ("Camada separadora com virada de 40cm: filme de polietileno 24 micra.", "m²"),
    ("Proteção mecânica armada. Espessura máx. 3,0cm", "m²"),
    ("Pintura antirraiz = esp. Desprezível", "m²"),
    ("Membrana de poliuretano com acabamento alifático", "m²"),
    ("Proteção mecânica: Top coat alifático com acabamento anti-derrapante", "m²"),
    ("Dupla manta asfáltica 4mm - Tipo III - Classe A, aderida com asfalto quente", "m²"),
    ("Instalação de andaimes, equipamentos de ventilação mecânica e segurança.", "vb."),
    ("Remoção de impermeabilização existente com retirada do entulho.", "vb."),
    ("Lixamento completo da superfície", "m²"),
    (
        "Correção completa do substrato de concreto, removendo-se todas as rebarbas, "
        "corrigindo-se todas as imperfeições de concretagem, tratando-se de eventuais ninho e "
        "emendas de concretagem com as técnicas mais adequadas para cada caso. Sempre que houver "
        "a necessidade de se emendar o concreto velho com um novo, graute ou argamassa de cimento "
        "e areia, empregar na interface de colagem um adesivo estrutural de base epoxídica.",
        "m²",
    ),
    ("Recuperação de ferragens expostas", "vb."),
    (
        "Impermeabilização com argamassa polimérica com duas demão de VIAPLUS 1000 e duas "
        "demãos de VIAPLUS 7000",
        "m²",
    ),
    ("Limpeza e desmobilização da obra", "vb."),
]

TEMPLATES_CATEGORIA: list[tuple[str, list[tuple[str, str]]]] = [
    (
        "Banheiro (membrana acrílica)",
        [
            (CATALOGO_SERVICOS[0][0], "m²"),
            (CATALOGO_SERVICOS[6][0], "m²"),
            (CATALOGO_SERVICOS[7][0], "m²"),
            (CATALOGO_SERVICOS[8][0], "m²"),
        ],
    ),
    (
        "Subsolo / Cisterna (Membrana Epóxi)",
        [
            (CATALOGO_SERVICOS[4][0], "m²"),
            (CATALOGO_SERVICOS[5][0], "m²"),
        ],
    ),
    (
        "Área externa / terraço (manta dupla)",
        [
            (CATALOGO_SERVICOS[0][0], "m²"),
            (CATALOGO_SERVICOS[15][0], "m²"),
            (CATALOGO_SERVICOS[10][0], "m²"),
            (CATALOGO_SERVICOS[11][0], "m²"),
        ],
    ),
    (
        "Cobertura / terraço (poliuretano)",
        [
            (CATALOGO_SERVICOS[0][0], "m²"),
            (CATALOGO_SERVICOS[13][0], "m²"),
            (CATALOGO_SERVICOS[7][0], "m²"),
            (CATALOGO_SERVICOS[14][0], "m²"),
        ],
    ),
    (
        "Reservatório enterrado (VIAPLUS)",
        [
            (CATALOGO_SERVICOS[16][0], "vb."),
            (CATALOGO_SERVICOS[17][0], "vb."),
            (CATALOGO_SERVICOS[18][0], "m²"),
            (CATALOGO_SERVICOS[19][0], "m²"),
            (CATALOGO_SERVICOS[20][0], "vb."),
            (CATALOGO_SERVICOS[21][0], "m²"),
            (CATALOGO_SERVICOS[22][0], "vb."),
        ],
    ),
]


def seed_se_vazio(db: Session) -> None:
    if db.execute(select(models.ServicoCatalogo.id).limit(1)).first() is None:
        for descricao, unidade in CATALOGO_SERVICOS:
            db.add(models.ServicoCatalogo(descricao=descricao, unidade_padrao=unidade))
        db.commit()

    if db.execute(select(models.CategoriaTemplate.id).limit(1)).first() is None:
        for ordem, (nome, itens) in enumerate(TEMPLATES_CATEGORIA):
            template = models.CategoriaTemplate(nome=nome, ordem=ordem)
            db.add(template)
            db.flush()
            for item_ordem, (descricao, unidade) in enumerate(itens):
                db.add(
                    models.CategoriaTemplateItem(
                        template_id=template.id, ordem=item_ordem, descricao=descricao, unidade=unidade
                    )
                )
        db.commit()
