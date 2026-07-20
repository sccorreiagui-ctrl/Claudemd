const API = "/api";

const state = {
  orcamentos: [],
  atual: null,
};

// ---------- utilitarios ----------

function fmtMoeda(valor) {
  if (valor === null || valor === undefined || Number.isNaN(valor)) return "";
  return valor.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

function fmtData(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  return d.toLocaleDateString("pt-BR");
}

function showToast(msg, isErro = false) {
  const toast = document.getElementById("toast");
  toast.textContent = msg;
  toast.style.background = isErro ? "#b3261e" : "#1f2328";
  toast.hidden = false;
  clearTimeout(showToast._t);
  showToast._t = setTimeout(() => { toast.hidden = true; }, 3500);
}

async function api(path, options = {}) {
  const resp = await fetch(`${API}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!resp.ok) {
    let detalhe = resp.statusText;
    try {
      const corpo = await resp.json();
      detalhe = corpo.detail || detalhe;
    } catch (e) { /* sem corpo json */ }
    throw new Error(detalhe);
  }
  if (resp.status === 204) return null;
  return resp.json();
}

// ---------- carregamento ----------

async function carregarLista() {
  state.orcamentos = await api("/orcamentos");
  renderSidebar();
}

async function selecionar(id) {
  state.atual = await api(`/orcamentos/${id}`);
  renderSidebar();
  renderConteudo();
}

async function recarregarAtual() {
  if (!state.atual) return;
  state.atual = await api(`/orcamentos/${state.atual.id}`);
  await carregarLista();
  renderConteudo();
}

// ---------- render: sidebar ----------

function renderSidebar() {
  const ul = document.getElementById("lista-orcamentos");
  ul.innerHTML = "";
  if (state.orcamentos.length === 0) {
    ul.innerHTML = '<li class="vazio">Nenhum orçamento ainda.</li>';
    return;
  }
  for (const orc of state.orcamentos) {
    const li = document.createElement("li");
    li.className = orc.id === state.atual?.id ? "ativo" : "";
    li.innerHTML = `
      <div class="titulo">${orc.numero_proposta || "(sem número)"} </div>
      <div class="subtitulo">${orc.cliente_nome || "—"}</div>
      <span class="badge ${orc.status}">${orc.status === "aprovado" ? "Aprovado" : "Rascunho"}</span>
    `;
    li.addEventListener("click", () => selecionar(orc.id));
    ul.appendChild(li);
  }
}

// ---------- render: conteudo principal ----------

function renderConteudo() {
  const orc = state.atual;
  const conteudo = document.getElementById("conteudo");
  if (!orc) {
    conteudo.innerHTML = '<p class="vazio">Selecione um orçamento na lista ao lado ou crie um novo.</p>';
    return;
  }

  const bloqueado = orc.status === "aprovado";
  const totais = calcularTotaisLocal(orc);

  conteudo.innerHTML = `
    ${bloqueado ? `<div class="aviso-aprovado">Orçamento aprovado em ${fmtData(orc.aprovado_em)} — não pode mais ser editado. Os preços foram gravados na memória do sistema.</div>` : ""}

    <div class="acoes-topo">
      <span class="status-pill ${orc.status}">${orc.status === "aprovado" ? "Aprovado" : "Rascunho"}</span>
      <button class="btn" id="btn-excel">Baixar Excel</button>
      ${!bloqueado ? `<button class="btn btn-primary" id="btn-aprovar">Aprovar orçamento</button>` : ""}
      ${!bloqueado ? `<button class="btn btn-danger" id="btn-excluir-orcamento">Excluir orçamento</button>` : ""}
    </div>

    <fieldset ${bloqueado ? "disabled" : ""}>
      <legend>Dados da proposta</legend>
      <div class="grid">
        <div class="campo">
          <label>Nº da proposta</label>
          <input type="text" data-campo="numero_proposta" value="${escapeAttr(orc.numero_proposta)}" placeholder="Ex: 260124 Rev 01" />
        </div>
        <div class="campo">
          <label>Criado por</label>
          <input type="text" data-campo="criado_por" value="${escapeAttr(orc.criado_por)}" />
        </div>
        <div class="campo">
          <label>Cliente</label>
          <input type="text" data-campo="cliente_nome" value="${escapeAttr(orc.cliente_nome)}" />
        </div>
        <div class="campo">
          <label>Att. (contato)</label>
          <input type="text" data-campo="cliente_att" value="${escapeAttr(orc.cliente_att)}" />
        </div>
        <div class="campo">
          <label>E-mail</label>
          <input type="email" data-campo="cliente_email" value="${escapeAttr(orc.cliente_email)}" />
        </div>
        <div class="campo">
          <label>Referência</label>
          <input type="text" data-campo="referencia" value="${escapeAttr(orc.referencia)}" />
        </div>
        <div class="campo span-2">
          <label>Endereço da obra</label>
          <input type="text" data-campo="endereco_obra" value="${escapeAttr(orc.endereco_obra)}" />
        </div>
        <div class="campo span-2">
          <label>Condições de pagamento</label>
          <input type="text" data-campo="condicoes_pagamento" value="${escapeAttr(orc.condicoes_pagamento)}" placeholder="Ex: 50% de sinal e o restante nas medições" />
        </div>
        <div class="campo">
          <label>% Material</label>
          <input type="number" step="0.01" data-campo="percentual_material" value="${orc.percentual_material}" />
        </div>
        <div class="campo">
          <label>% Serviço</label>
          <input type="number" step="0.01" data-campo="percentual_servico" value="${orc.percentual_servico}" />
        </div>
      </div>
    </fieldset>

    <fieldset ${bloqueado ? "disabled" : ""}>
      <legend>Categorias e itens</legend>
      <div id="categorias">${orc.categorias.map((c) => renderCategoria(c, bloqueado)).join("")}</div>
      ${!bloqueado ? '<button class="btn" id="btn-add-categoria">+ Adicionar categoria</button>' : ""}
    </fieldset>

    <div class="totais">
      <div class="linha"><span>Total material (${orc.percentual_material}%)</span><span>${fmtMoeda(totais.material)}</span></div>
      <div class="linha"><span>Total serviço (${orc.percentual_servico}%)</span><span>${fmtMoeda(totais.servico)}</span></div>
      <div class="linha total"><span>Total da proposta</span><span>${fmtMoeda(totais.geral)}</span></div>
    </div>
  `;

  ligarEventosHeader(bloqueado);
  ligarEventosCategorias(bloqueado);

  document.getElementById("btn-excel").addEventListener("click", () => {
    window.open(`${API}/orcamentos/${orc.id}/excel`, "_blank");
  });
  const btnAprovar = document.getElementById("btn-aprovar");
  if (btnAprovar) btnAprovar.addEventListener("click", aprovarOrcamento);
  const btnExcluirOrc = document.getElementById("btn-excluir-orcamento");
  if (btnExcluirOrc) btnExcluirOrc.addEventListener("click", excluirOrcamento);
}

function calcularTotaisLocal(orc) {
  let geral = 0;
  for (const cat of orc.categorias) {
    for (const item of cat.itens) {
      if (item.preco_total) geral += Number(item.preco_total);
    }
  }
  const material = geral * (Number(orc.percentual_material) || 0) / 100;
  const servico = geral * (Number(orc.percentual_servico) || 0) / 100;
  return { geral, material, servico };
}

function subtotalCategoria(categoria) {
  return categoria.itens.reduce((soma, item) => soma + (Number(item.preco_total) || 0), 0);
}

function renderCategoria(categoria, bloqueado) {
  return `
    <div class="categoria" data-cat="${categoria.id}">
      <div class="categoria-header">
        <input type="text" data-campo-cat="titulo" value="${escapeAttr(categoria.titulo)}" placeholder="Ex: SUBSOLO, COZINHA E LAVANDERIA" ${bloqueado ? "disabled" : ""} />
        ${!bloqueado ? `<button class="btn btn-sm" data-acao="mover-cat-up">↑</button>
        <button class="btn btn-sm" data-acao="mover-cat-down">↓</button>
        <button class="link-excluir" data-acao="excluir-categoria" title="Excluir categoria">✕</button>` : ""}
      </div>
      <table class="itens">
        <thead>
          <tr>
            <th>Descrição</th>
            <th class="col-qtd">Qtd.</th>
            <th class="col-un">Unid.</th>
            <th>Cobrança</th>
            <th class="col-preco">Preço unit.</th>
            <th class="col-total">Total</th>
            ${!bloqueado ? '<th class="col-acoes"></th>' : ""}
          </tr>
        </thead>
        <tbody>
          ${categoria.itens.map((item) => renderItem(categoria.id, item, bloqueado)).join("")}
        </tbody>
      </table>
      <div class="rodape-categoria">
        ${!bloqueado ? '<button class="btn btn-sm" data-acao="add-item">+ Item</button>' : "<span></span>"}
        <strong>Subtotal: ${fmtMoeda(subtotalCategoria(categoria))}</strong>
      </div>
    </div>
  `;
}

function renderItem(catId, item, bloqueado) {
  const isNormal = item.status_cobranca === "normal";
  return `
    <tr data-cat="${catId}" data-item="${item.id}">
      <td>
        <textarea data-field="descricao" ${bloqueado ? "disabled" : ""}>${escapeHtml(item.descricao)}</textarea>
        ${item.preco_sugerido_diferente ? '<span class="alerta-preco">⚠ Preço diferente do último usado para este item.</span>' : ""}
      </td>
      <td class="col-qtd"><input type="number" step="0.001" data-field="quantidade" value="${item.quantidade ?? ""}" ${bloqueado ? "disabled" : ""} /></td>
      <td class="col-un"><input type="text" data-field="unidade" value="${escapeAttr(item.unidade)}" ${bloqueado ? "disabled" : ""} /></td>
      <td>
        <select data-field="status_cobranca" ${bloqueado ? "disabled" : ""}>
          <option value="normal" ${isNormal ? "selected" : ""}>Normal</option>
          <option value="por_conta_contratante" ${item.status_cobranca === "por_conta_contratante" ? "selected" : ""}>Por conta da contratante</option>
          <option value="incluso" ${item.status_cobranca === "incluso" ? "selected" : ""}>Incluso</option>
        </select>
      </td>
      <td class="col-preco"><input type="number" step="0.01" data-field="preco_unitario" value="${isNormal && item.preco_unitario !== null ? item.preco_unitario : ""}" ${bloqueado || !isNormal ? "disabled" : ""} /></td>
      <td class="col-total">${isNormal ? fmtMoeda(Number(item.preco_total) || 0) : (item.status_cobranca === "incluso" ? "INCLUSO" : "por conta da contratante")}</td>
      ${!bloqueado ? `<td class="col-acoes"><button class="link-excluir" data-acao="excluir-item" title="Excluir item">✕</button></td>` : ""}
    </tr>
  `;
}

function escapeHtml(texto) {
  return (texto || "").replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
}
function escapeAttr(texto) {
  return escapeHtml(texto).replace(/"/g, "&quot;");
}

// ---------- eventos: cabecalho ----------

function ligarEventosHeader(bloqueado) {
  if (bloqueado) return;
  document.querySelectorAll("[data-campo]").forEach((el) => {
    el.addEventListener("blur", salvarCabecalho);
  });
}

async function salvarCabecalho() {
  const orc = state.atual;
  const payload = {
    numero_proposta: valorCampo("numero_proposta"),
    criado_por: valorCampo("criado_por"),
    cliente_nome: valorCampo("cliente_nome"),
    cliente_att: valorCampo("cliente_att"),
    cliente_email: valorCampo("cliente_email"),
    referencia: valorCampo("referencia"),
    endereco_obra: valorCampo("endereco_obra"),
    condicoes_pagamento: valorCampo("condicoes_pagamento"),
    percentual_material: parseFloat(valorCampo("percentual_material")) || 0,
    percentual_servico: parseFloat(valorCampo("percentual_servico")) || 0,
  };
  try {
    await api(`/orcamentos/${orc.id}`, { method: "PUT", body: JSON.stringify(payload) });
    await recarregarAtual();
  } catch (e) {
    showToast(`Erro ao salvar: ${e.message}`, true);
  }
}

function valorCampo(nome) {
  const el = document.querySelector(`[data-campo="${nome}"]`);
  return el ? el.value : "";
}

// ---------- eventos: categorias e itens ----------

function ligarEventosCategorias(bloqueado) {
  const btnAdd = document.getElementById("btn-add-categoria");
  if (btnAdd) btnAdd.addEventListener("click", adicionarCategoria);

  document.querySelectorAll(".categoria").forEach((catEl) => {
    const catId = Number(catEl.dataset.cat);

    if (!bloqueado) {
      const tituloInput = catEl.querySelector('[data-campo-cat="titulo"]');
      tituloInput.addEventListener("blur", () => salvarCategoria(catId, tituloInput.value));

      catEl.querySelector('[data-acao="excluir-categoria"]')?.addEventListener("click", () => excluirCategoria(catId));
      catEl.querySelector('[data-acao="mover-cat-up"]')?.addEventListener("click", () => moverCategoria(catId, -1));
      catEl.querySelector('[data-acao="mover-cat-down"]')?.addEventListener("click", () => moverCategoria(catId, 1));
      catEl.querySelector('[data-acao="add-item"]')?.addEventListener("click", () => adicionarItem(catId));
    }

    catEl.querySelectorAll("tr[data-item]").forEach((tr) => {
      const itemId = Number(tr.dataset.item);
      if (!bloqueado) {
        tr.querySelector('[data-acao="excluir-item"]')?.addEventListener("click", () => excluirItem(catId, itemId));
        tr.querySelector('[data-field="status_cobranca"]').addEventListener("change", () => salvarItem(catId, itemId, tr));
        tr.querySelectorAll('[data-field="quantidade"], [data-field="unidade"], [data-field="preco_unitario"]').forEach((el) => {
          el.addEventListener("blur", () => salvarItem(catId, itemId, tr));
        });
        tr.querySelector('[data-field="descricao"]').addEventListener("blur", () => tratarBlurDescricao(catId, itemId, tr));
      }
    });
  });
}

async function adicionarCategoria() {
  const orc = state.atual;
  try {
    await api(`/orcamentos/${orc.id}/categorias`, {
      method: "POST",
      body: JSON.stringify({ ordem: orc.categorias.length, titulo: "", itens: [] }),
    });
    await recarregarAtual();
  } catch (e) {
    showToast(`Erro ao adicionar categoria: ${e.message}`, true);
  }
}

async function salvarCategoria(catId, titulo) {
  const orc = state.atual;
  const categoria = orc.categorias.find((c) => c.id === catId);
  try {
    await api(`/orcamentos/${orc.id}/categorias/${catId}`, {
      method: "PUT",
      body: JSON.stringify({ ordem: categoria.ordem, titulo }),
    });
    await recarregarAtual();
  } catch (e) {
    showToast(`Erro ao salvar categoria: ${e.message}`, true);
  }
}

async function excluirCategoria(catId) {
  if (!confirm("Excluir esta categoria e todos os itens dentro dela?")) return;
  const orc = state.atual;
  try {
    await api(`/orcamentos/${orc.id}/categorias/${catId}`, { method: "DELETE" });
    await recarregarAtual();
  } catch (e) {
    showToast(`Erro ao excluir categoria: ${e.message}`, true);
  }
}

async function moverCategoria(catId, direcao) {
  const orc = state.atual;
  const ordenadas = [...orc.categorias].sort((a, b) => a.ordem - b.ordem);
  const indice = ordenadas.findIndex((c) => c.id === catId);
  const alvo = indice + direcao;
  if (alvo < 0 || alvo >= ordenadas.length) return;
  const a = ordenadas[indice];
  const b = ordenadas[alvo];
  try {
    await api(`/orcamentos/${orc.id}/categorias/${a.id}`, { method: "PUT", body: JSON.stringify({ ordem: b.ordem, titulo: a.titulo }) });
    await api(`/orcamentos/${orc.id}/categorias/${b.id}`, { method: "PUT", body: JSON.stringify({ ordem: a.ordem, titulo: b.titulo }) });
    await recarregarAtual();
  } catch (e) {
    showToast(`Erro ao reordenar: ${e.message}`, true);
  }
}

async function adicionarItem(catId) {
  const orc = state.atual;
  const categoria = orc.categorias.find((c) => c.id === catId);
  try {
    await api(`/orcamentos/${orc.id}/categorias/${catId}/itens`, {
      method: "POST",
      body: JSON.stringify({ ordem: categoria.itens.length, descricao: "", quantidade: 0, unidade: "m²", status_cobranca: "normal" }),
    });
    await recarregarAtual();
  } catch (e) {
    showToast(`Erro ao adicionar item: ${e.message}`, true);
  }
}

function coletarPayloadItem(tr) {
  const status = tr.querySelector('[data-field="status_cobranca"]').value;
  const precoRaw = tr.querySelector('[data-field="preco_unitario"]').value;
  return {
    ordem: 0,
    descricao: tr.querySelector('[data-field="descricao"]').value,
    quantidade: parseFloat(tr.querySelector('[data-field="quantidade"]').value) || 0,
    unidade: tr.querySelector('[data-field="unidade"]').value,
    status_cobranca: status,
    preco_unitario: status === "normal" && precoRaw !== "" ? parseFloat(precoRaw) : null,
  };
}

async function salvarItem(catId, itemId, tr) {
  const orc = state.atual;
  const categoria = orc.categorias.find((c) => c.id === catId);
  const itemAtual = categoria.itens.find((i) => i.id === itemId);
  const payload = coletarPayloadItem(tr);
  payload.ordem = itemAtual ? itemAtual.ordem : 0;
  try {
    await api(`/orcamentos/${orc.id}/categorias/${catId}/itens/${itemId}`, {
      method: "PUT",
      body: JSON.stringify(payload),
    });
    await recarregarAtual();
  } catch (e) {
    showToast(`Erro ao salvar item: ${e.message}`, true);
  }
}

async function tratarBlurDescricao(catId, itemId, tr) {
  const descricao = tr.querySelector('[data-field="descricao"]').value.trim();
  const statusSel = tr.querySelector('[data-field="status_cobranca"]');
  const precoInput = tr.querySelector('[data-field="preco_unitario"]');
  const unidadeInput = tr.querySelector('[data-field="unidade"]');

  if (descricao && statusSel.value === "normal" && !precoInput.value) {
    try {
      const sug = await api(`/itens-preco/sugestao?descricao=${encodeURIComponent(descricao)}`);
      if (sug.encontrado) {
        precoInput.value = Number(sug.ultimo_preco).toFixed(2);
        if (!unidadeInput.value) unidadeInput.value = sug.unidade;
        showToast(`Sugestão aplicada: ${fmtMoeda(sug.ultimo_preco)} (usado em ${fmtData(sug.atualizado_em)}). Ajuste se necessário.`);
      }
    } catch (e) { /* sugestao indisponivel, segue sem bloquear */ }
  }
  await salvarItem(catId, itemId, tr);
}

async function excluirItem(catId, itemId) {
  const orc = state.atual;
  try {
    await api(`/orcamentos/${orc.id}/categorias/${catId}/itens/${itemId}`, { method: "DELETE" });
    await recarregarAtual();
  } catch (e) {
    showToast(`Erro ao excluir item: ${e.message}`, true);
  }
}

// ---------- acoes globais ----------

async function criarNovoOrcamento() {
  try {
    const novo = await api("/orcamentos", {
      method: "POST",
      body: JSON.stringify({
        numero_proposta: "",
        cliente_nome: "",
        cliente_email: "",
        cliente_att: "",
        referencia: "Impermeabilização",
        endereco_obra: "",
        condicoes_pagamento: "",
        percentual_material: 60,
        percentual_servico: 40,
        criado_por: "",
      }),
    });
    await carregarLista();
    await selecionar(novo.id);
  } catch (e) {
    showToast(`Erro ao criar orçamento: ${e.message}`, true);
  }
}

async function aprovarOrcamento() {
  const orc = state.atual;
  if (!confirm("Aprovar este orçamento? Os preços unitários serão gravados como referência para os próximos orçamentos e a edição será bloqueada.")) return;
  try {
    await api(`/orcamentos/${orc.id}/aprovar`, { method: "POST" });
    await recarregarAtual();
    showToast("Orçamento aprovado. Preços atualizados na memória do sistema.");
  } catch (e) {
    showToast(`Erro ao aprovar: ${e.message}`, true);
  }
}

async function excluirOrcamento() {
  const orc = state.atual;
  if (!confirm("Excluir este orçamento (rascunho) permanentemente?")) return;
  try {
    await api(`/orcamentos/${orc.id}`, { method: "DELETE" });
    state.atual = null;
    await carregarLista();
    renderConteudo();
  } catch (e) {
    showToast(`Erro ao excluir: ${e.message}`, true);
  }
}

// ---------- inicializacao ----------

document.getElementById("btn-novo").addEventListener("click", criarNovoOrcamento);
carregarLista();
