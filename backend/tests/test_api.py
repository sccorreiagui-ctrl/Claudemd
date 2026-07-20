import os
import tempfile

import pytest


@pytest.fixture(scope="session")
def _tmp_data_dir():
    with tempfile.TemporaryDirectory() as tmp_dir:
        os.environ["ORCAMENTOS_DATA_DIR"] = tmp_dir
        yield tmp_dir


@pytest.fixture()
def client(_tmp_data_dir):
    from fastapi.testclient import TestClient

    from app import models
    from app.database import engine
    from app.main import app

    # Cada teste comeca com um banco limpo, mas reaproveita a mesma engine/arquivo.
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)

    yield TestClient(app)


def test_criar_orcamento_categoria_item_e_totais(client):
    resp = client.post("/api/orcamentos", json={
        "numero_proposta": "260200",
        "cliente_nome": "Cliente Teste",
        "percentual_material": 60,
        "percentual_servico": 40,
    })
    assert resp.status_code == 201
    orcamento = resp.json()

    resp = client.post(f"/api/orcamentos/{orcamento['id']}/categorias", json={
        "ordem": 0, "titulo": "BANHEIRO", "itens": [],
    })
    assert resp.status_code == 201
    categoria = resp.json()

    resp = client.post(
        f"/api/orcamentos/{orcamento['id']}/categorias/{categoria['id']}/itens",
        json={"ordem": 0, "descricao": "Impermeabilização X", "quantidade": 10, "unidade": "m²",
              "status_cobranca": "normal", "preco_unitario": 100},
    )
    assert resp.status_code == 201
    item = resp.json()
    assert item["preco_total"] == 1000.0

    resp = client.get(f"/api/orcamentos/{orcamento['id']}/totais")
    totais = resp.json()
    assert totais["total_geral"] == 1000.0
    assert totais["total_material"] == 600.0
    assert totais["total_servico"] == 400.0


def test_aprovacao_grava_preco_e_bloqueia_edicao(client):
    resp = client.post("/api/orcamentos", json={"numero_proposta": "260201"})
    orcamento_id = resp.json()["id"]

    categoria = client.post(f"/api/orcamentos/{orcamento_id}/categorias", json={
        "ordem": 0, "titulo": "SUBSOLO", "itens": [],
    }).json()

    client.post(
        f"/api/orcamentos/{orcamento_id}/categorias/{categoria['id']}/itens",
        json={"ordem": 0, "descricao": "Manta asfáltica tipo III", "quantidade": 5, "unidade": "m²",
              "status_cobranca": "normal", "preco_unitario": 197},
    )

    resp = client.post(f"/api/orcamentos/{orcamento_id}/aprovar")
    assert resp.status_code == 200
    assert resp.json()["status"] == "aprovado"

    sugestao = client.get("/api/itens-preco/sugestao", params={"descricao": "Manta asfáltica tipo III"}).json()
    assert sugestao["encontrado"] is True
    assert sugestao["ultimo_preco"] == 197.0

    resp = client.put(f"/api/orcamentos/{orcamento_id}", json={"numero_proposta": "outro"})
    assert resp.status_code == 409


def test_sugestao_diferente_gera_alerta(client):
    primeiro = client.post("/api/orcamentos", json={"numero_proposta": "A"}).json()
    cat1 = client.post(f"/api/orcamentos/{primeiro['id']}/categorias", json={"ordem": 0, "titulo": "X", "itens": []}).json()
    client.post(
        f"/api/orcamentos/{primeiro['id']}/categorias/{cat1['id']}/itens",
        json={"ordem": 0, "descricao": "Regularização de piso", "quantidade": 1, "unidade": "m²",
              "status_cobranca": "normal", "preco_unitario": 50},
    )
    client.post(f"/api/orcamentos/{primeiro['id']}/aprovar")

    segundo = client.post("/api/orcamentos", json={"numero_proposta": "B"}).json()
    cat2 = client.post(f"/api/orcamentos/{segundo['id']}/categorias", json={"ordem": 0, "titulo": "Y", "itens": []}).json()
    item = client.post(
        f"/api/orcamentos/{segundo['id']}/categorias/{cat2['id']}/itens",
        json={"ordem": 0, "descricao": "Regularização de piso", "quantidade": 1, "unidade": "m²",
              "status_cobranca": "normal", "preco_unitario": 80},
    ).json()

    assert item["preco_sugerido_diferente"] is True


def test_excel_gerado_para_orcamento_com_itens(client):
    orcamento = client.post("/api/orcamentos", json={"numero_proposta": "260202"}).json()
    categoria = client.post(f"/api/orcamentos/{orcamento['id']}/categorias", json={
        "ordem": 0, "titulo": "COBERTURA", "itens": [],
    }).json()
    client.post(
        f"/api/orcamentos/{orcamento['id']}/categorias/{categoria['id']}/itens",
        json={"ordem": 0, "descricao": "Manta", "quantidade": 2, "unidade": "m²",
              "status_cobranca": "normal", "preco_unitario": 10},
    )

    resp = client.get(f"/api/orcamentos/{orcamento['id']}/excel")
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("application/vnd.openxmlformats")
    assert len(resp.content) > 1000
