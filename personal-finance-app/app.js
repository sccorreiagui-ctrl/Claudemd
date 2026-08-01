(() => {
  'use strict';

  const STORAGE_KEY = 'bussola-financas-v1';
  const currency = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' });
  const CHART_COLORS = ['#14b881', '#3b82f6', '#f59e0b', '#a855f7', '#ec4899', '#06b6d4', '#f97316', '#84cc16', '#6366f1', '#ef4444'];

  const monthNames = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];

  // ---------- State ----------
  function uid() {
    return Math.random().toString(36).slice(2, 10) + Date.now().toString(36);
  }

  function todayKey() {
    const d = new Date();
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
  }

  function loadRoot() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) return JSON.parse(raw);
    } catch (e) { /* corrupted, fall through */ }
    return { currentMonth: todayKey(), months: {} };
  }

  let root = loadRoot();
  if (!root.months) root.months = {};
  if (!root.currentMonth) root.currentMonth = todayKey();

  function save() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(root));
  }

  function monthKeys() {
    return Object.keys(root.months).sort();
  }

  function findPreviousMonthWithData(key) {
    const keys = monthKeys().filter(k => k < key);
    return keys.length ? keys[keys.length - 1] : null;
  }

  function ensureMonth(key) {
    if (root.months[key]) return root.months[key];
    const prevKey = findPreviousMonthWithData(key);
    const month = { incomes: [], categories: [] };
    if (prevKey) {
      month.categories = root.months[prevKey].categories.map(c => ({
        id: uid(), name: c.name, planned: c.planned, expenses: []
      }));
    }
    root.months[key] = month;
    save();
    return month;
  }

  function currentMonth() {
    return ensureMonth(root.currentMonth);
  }

  // ---------- Number parsing ----------
  function parseMoney(str) {
    if (typeof str !== 'string') return NaN;
    const cleaned = str.trim().replace(/[R$\s]/g, '').replace(/\./g, '').replace(',', '.');
    return parseFloat(cleaned);
  }

  // ---------- DOM refs ----------
  const $ = sel => document.querySelector(sel);
  const monthLabel = $('#monthLabel');
  const content = $('#content');
  const alertStack = $('#alertStack');
  const incomeList = $('#incomeList');
  const categoryGrid = $('#categoryGrid');
  const barChart = $('#barChart');
  const pieSvg = $('#pieSvg');
  const pieLegend = $('#pieLegend');
  const ringProgress = $('#ringProgress');
  const ringPct = $('#ringPct');
  const toastEl = $('#toast');

  // ---------- Toast ----------
  let toastTimer;
  function toast(msg) {
    toastEl.textContent = msg;
    toastEl.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toastEl.classList.remove('show'), 2400);
  }

  // ---------- Count-up animation ----------
  function animateCount(el, target) {
    const start = 0;
    const duration = 900;
    const startTime = performance.now();
    function step(now) {
      const t = Math.min(1, (now - startTime) / duration);
      const eased = 1 - Math.pow(1 - t, 3);
      const value = start + (target - start) * eased;
      el.textContent = currency.format(value);
      if (t < 1) requestAnimationFrame(step);
      else el.textContent = currency.format(target);
    }
    requestAnimationFrame(step);
  }

  // ---------- Calculations ----------
  function categorySpent(cat) {
    return cat.expenses.reduce((s, e) => s + e.value, 0);
  }

  function monthTotals(month) {
    const income = month.incomes.reduce((s, i) => s + i.value, 0);
    const planned = month.categories.reduce((s, c) => s + c.planned, 0);
    const spent = month.categories.reduce((s, c) => s + categorySpent(c), 0);
    const free = income - planned;
    return { income, planned, spent, free };
  }

  // ---------- Rendering ----------
  let currentDetailCategoryId = null;

  function formatMonthLabel(key) {
    const [y, m] = key.split('-').map(Number);
    return `${monthNames[m - 1]} ${y}`;
  }

  function showSkeleton() {
    categoryGrid.innerHTML = Array.from({ length: 3 }).map(() => '<div class="skeleton skeleton-card"></div>').join('');
    incomeList.innerHTML = '<div class="skeleton skeleton-stat" style="height:44px"></div>';
  }

  function render(withTransition) {
    monthLabel.textContent = formatMonthLabel(root.currentMonth);

    if (withTransition) {
      content.classList.remove('switching');
      showSkeleton();
      void content.offsetWidth;
      content.classList.add('switching');
      setTimeout(() => renderFull(), 260);
    } else {
      renderFull();
    }
  }

  function renderFull() {
    const month = currentMonth();
    const totals = monthTotals(month);

    renderAlerts(month, totals);
    renderStats(totals);
    renderRing(totals);
    renderIncomes(month);
    renderCategories(month);
    renderBarChart(month);
    renderPieChart(month);
  }

  function renderAlerts(month, totals) {
    alertStack.innerHTML = '';
    if (totals.planned > totals.income && totals.income > 0) {
      addAlert(`A soma das alocações (${currency.format(totals.planned)}) ultrapassa a renda do mês (${currency.format(totals.income)}).`);
    } else if (totals.planned > 0 && totals.income === 0) {
      addAlert('Você já planejou gastos, mas ainda não informou nenhuma renda para este mês.');
    }
    $('#freeCard').classList.toggle('negative', totals.free < 0);
  }

  function addAlert(text) {
    const div = document.createElement('div');
    div.className = 'alert-banner';
    div.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24"><path d="M12 9v4M12 17h.01M10.3 3.9L1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg><span>${text}</span>`;
    alertStack.appendChild(div);
  }

  function renderStats(totals) {
    animateCount(document.querySelector('[data-count="income"]'), totals.income);
    animateCount(document.querySelector('[data-count="planned"]'), totals.planned);
    animateCount(document.querySelector('[data-count="spent"]'), totals.spent);
    animateCount(document.querySelector('[data-count="free"]'), totals.free);
  }

  function renderRing(totals) {
    const circumference = 2 * Math.PI * 60;
    const pct = totals.planned > 0 ? Math.min(1.5, totals.spent / totals.planned) : 0;
    const displayPct = Math.round(pct * 100);
    const clampedOffset = circumference * (1 - Math.min(1, pct));
    requestAnimationFrame(() => {
      ringProgress.style.strokeDasharray = `${circumference}`;
      ringProgress.style.strokeDashoffset = `${clampedOffset}`;
      ringProgress.classList.toggle('over', pct > 1);
    });
    ringPct.textContent = `${displayPct}%`;
  }

  function renderIncomes(month) {
    if (!month.incomes.length) {
      incomeList.innerHTML = '<div class="row-empty">Nenhuma fonte de renda cadastrada ainda.</div>';
      return;
    }
    incomeList.innerHTML = '';
    month.incomes.forEach(inc => {
      const row = document.createElement('div');
      row.className = 'income-row';
      row.innerHTML = `
        <span class="income-name">${escapeHtml(inc.name)}</span>
        <span class="income-right">
          <span class="income-value">${currency.format(inc.value)}</span>
          <button class="expense-del" data-action="del-income" data-id="${inc.id}" aria-label="Remover">
            <svg width="15" height="15" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/></svg>
          </button>
        </span>`;
      incomeList.appendChild(row);
    });
  }

  function renderCategories(month) {
    if (!month.categories.length) {
      categoryGrid.innerHTML = '<div class="row-empty">Nenhuma categoria criada. Clique em "+ Nova categoria" para começar.</div>';
      return;
    }
    categoryGrid.innerHTML = '';
    month.categories.forEach(cat => {
      const spent = categorySpent(cat);
      const remaining = cat.planned - spent;
      const over = cat.planned > 0 ? spent > cat.planned : spent > 0;
      const pct = cat.planned > 0 ? Math.min(1, spent / cat.planned) : (spent > 0 ? 1 : 0);

      const card = document.createElement('div');
      card.className = 'category-card card' + (over ? ' over-budget' : '');
      card.dataset.id = cat.id;
      card.innerHTML = `
        <div class="cat-top">
          <span class="cat-name">${escapeHtml(cat.name)}</span>
          ${over ? '<span class="badge-over">Estourado</span>' : ''}
        </div>
        <div class="cat-figures">
          <span class="cat-spent${over ? ' over' : ''}">${currency.format(spent)}</span>
          <span class="cat-planned">de ${currency.format(cat.planned)}</span>
        </div>
        <div class="progress-track"><div class="progress-fill${over ? ' over' : ''}" data-pct="${pct * 100}"></div></div>
        <div class="cat-footer">
          <span>Saldo</span>
          <span class="cat-remaining${remaining < 0 ? ' negative' : ''}">${currency.format(remaining)}</span>
        </div>
      `;
      card.addEventListener('click', () => openDetail(cat.id));
      categoryGrid.appendChild(card);
    });

    requestAnimationFrame(() => {
      categoryGrid.querySelectorAll('.progress-fill').forEach(el => {
        const pct = el.dataset.pct;
        requestAnimationFrame(() => { el.style.width = `${pct}%`; });
      });
    });
  }

  function renderBarChart(month) {
    if (!month.categories.length) {
      barChart.innerHTML = '<div class="bar-empty">Sem categorias ainda</div>';
      return;
    }
    barChart.innerHTML = '';
    const maxVal = Math.max(1, ...month.categories.map(c => Math.max(categorySpent(c), c.planned)));
    month.categories.forEach((cat, i) => {
      const spent = categorySpent(cat);
      const over = cat.planned > 0 && spent > cat.planned;
      const heightPct = Math.min(100, (spent / maxVal) * 100);
      const col = document.createElement('div');
      col.className = 'bar-col';
      col.innerHTML = `
        <span class="bar-value">${spent > 0 ? currency.format(spent).replace('R$', '').trim() : ''}</span>
        <div class="bar-rect${over ? ' over' : ''}" data-h="${heightPct}" style="transition-delay:${i * 80}ms"></div>
        <span class="bar-label">${escapeHtml(cat.name)}</span>
      `;
      barChart.appendChild(col);
    });
    requestAnimationFrame(() => {
      barChart.querySelectorAll('.bar-rect').forEach(el => {
        const h = el.dataset.h;
        requestAnimationFrame(() => { el.style.height = `${h}%`; });
      });
    });
  }

  function renderPieChart(month) {
    const data = month.categories.map(c => ({ name: c.name, value: categorySpent(c) })).filter(d => d.value > 0);
    pieLegend.innerHTML = '';
    if (!data.length) {
      pieSvg.innerHTML = '<circle cx="60" cy="60" r="50" fill="none" stroke="var(--border-soft)" stroke-width="14"></circle>';
      pieLegend.innerHTML = '<span class="row-empty">Sem gastos lançados</span>';
      return;
    }
    const total = data.reduce((s, d) => s + d.value, 0);
    const r = 50, circumference = 2 * Math.PI * r;
    let offsetAcc = 0;
    pieSvg.innerHTML = '';
    const bg = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    bg.setAttribute('cx', 60); bg.setAttribute('cy', 60); bg.setAttribute('r', r);
    bg.setAttribute('fill', 'none'); bg.setAttribute('stroke', 'var(--border-soft)'); bg.setAttribute('stroke-width', 14);
    pieSvg.appendChild(bg);

    data.forEach((d, i) => {
      const frac = d.value / total;
      const dashLen = frac * circumference;
      const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      circle.setAttribute('cx', 60); circle.setAttribute('cy', 60); circle.setAttribute('r', r);
      circle.setAttribute('fill', 'none');
      circle.setAttribute('stroke', CHART_COLORS[i % CHART_COLORS.length]);
      circle.setAttribute('stroke-width', 14);
      circle.setAttribute('stroke-dasharray', `0 ${circumference}`);
      circle.setAttribute('stroke-dashoffset', -offsetAcc);
      circle.setAttribute('transform', 'rotate(-90 60 60)');
      circle.classList.add('pie-seg');
      pieSvg.appendChild(circle);
      requestAnimationFrame(() => {
        setTimeout(() => {
          circle.setAttribute('stroke-dasharray', `${dashLen} ${circumference - dashLen}`);
        }, i * 70);
      });
      offsetAcc += dashLen;

      const legendItem = document.createElement('div');
      legendItem.className = 'legend-item';
      legendItem.innerHTML = `<span class="legend-dot" style="background:${CHART_COLORS[i % CHART_COLORS.length]}"></span>${escapeHtml(d.name)} · ${Math.round(frac * 100)}%`;
      pieLegend.appendChild(legendItem);
    });
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  // ---------- Modal helpers ----------
  function openModal(id) { document.getElementById(id).classList.add('open'); }
  function closeModal(id) { document.getElementById(id).classList.remove('open'); }

  document.querySelectorAll('[data-close]').forEach(btn => {
    btn.addEventListener('click', () => closeModal(btn.dataset.close));
  });
  document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', e => { if (e.target === overlay) overlay.classList.remove('open'); });
  });

  // ---------- Confirm dialog ----------
  function confirmAction(message, onConfirm) {
    $('#confirmMessage').textContent = message;
    $('#confirmOverlay').classList.add('open');
    const okBtn = $('#confirmOk');
    const cancelBtn = $('#confirmCancel');
    function cleanup() {
      $('#confirmOverlay').classList.remove('open');
      okBtn.removeEventListener('click', onOk);
      cancelBtn.removeEventListener('click', onCancel);
    }
    function onOk() { cleanup(); onConfirm(); }
    function onCancel() { cleanup(); }
    okBtn.addEventListener('click', onOk);
    cancelBtn.addEventListener('click', onCancel);
  }

  // ---------- Month navigation ----------
  $('#prevMonth').addEventListener('click', () => {
    const [y, m] = root.currentMonth.split('-').map(Number);
    const d = new Date(y, m - 2, 1);
    root.currentMonth = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
    save();
    render(true);
  });
  $('#nextMonth').addEventListener('click', () => {
    const [y, m] = root.currentMonth.split('-').map(Number);
    const d = new Date(y, m, 1);
    root.currentMonth = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
    save();
    render(true);
  });

  // ---------- Theme ----------
  const THEME_KEY = 'bussola-theme';
  function applyTheme(theme) {
    if (theme) document.documentElement.setAttribute('data-theme', theme);
    else document.documentElement.removeAttribute('data-theme');
  }
  const savedTheme = localStorage.getItem(THEME_KEY);
  if (savedTheme) applyTheme(savedTheme);
  $('#themeToggle').addEventListener('click', () => {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const current = document.documentElement.getAttribute('data-theme') || (prefersDark ? 'dark' : 'light');
    const next = current === 'dark' ? 'light' : 'dark';
    applyTheme(next);
    localStorage.setItem(THEME_KEY, next);
  });

  // ---------- Income form ----------
  $('#addIncomeBtn').addEventListener('click', () => {
    $('#incomeForm').reset();
    openModal('incomeModal');
  });
  $('#incomeForm').addEventListener('submit', e => {
    e.preventDefault();
    const name = $('#incomeName').value.trim();
    const value = parseMoney($('#incomeValue').value);
    if (!name || isNaN(value) || value < 0) { toast('Preencha nome e valor válidos.'); return; }
    currentMonth().incomes.push({ id: uid(), name, value });
    save();
    closeModal('incomeModal');
    renderFull();
    toast('Fonte de renda adicionada.');
  });

  incomeList.addEventListener('click', e => {
    const btn = e.target.closest('[data-action="del-income"]');
    if (!btn) return;
    const id = btn.dataset.id;
    confirmAction('Remover esta fonte de renda?', () => {
      const month = currentMonth();
      month.incomes = month.incomes.filter(i => i.id !== id);
      save();
      renderFull();
      toast('Fonte de renda removida.');
    });
  });

  // ---------- Category form ----------
  let editingCategoryId = null;

  $('#addCategoryBtn').addEventListener('click', () => {
    editingCategoryId = null;
    $('#categoryModalTitle').textContent = 'Nova categoria';
    $('#categoryForm').reset();
    openModal('categoryModal');
  });

  $('#categoryForm').addEventListener('submit', e => {
    e.preventDefault();
    const name = $('#categoryName').value.trim();
    const planned = parseMoney($('#categoryPlanned').value);
    if (!name || isNaN(planned) || planned < 0) { toast('Preencha nome e valor planejado válidos.'); return; }
    const month = currentMonth();
    if (editingCategoryId) {
      const cat = month.categories.find(c => c.id === editingCategoryId);
      cat.name = name;
      cat.planned = planned;
    } else {
      month.categories.push({ id: uid(), name, planned, expenses: [] });
    }
    save();
    closeModal('categoryModal');
    renderFull();
    if (currentDetailCategoryId) renderDetail();
    toast('Categoria salva.');
  });

  // ---------- Category detail / expenses ----------
  function openDetail(categoryId) {
    currentDetailCategoryId = categoryId;
    renderDetail();
    openModal('detailModal');
  }

  function renderDetail() {
    const month = currentMonth();
    const cat = month.categories.find(c => c.id === currentDetailCategoryId);
    if (!cat) { closeModal('detailModal'); return; }
    const spent = categorySpent(cat);
    const over = cat.planned > 0 ? spent > cat.planned : spent > 0;
    const pct = cat.planned > 0 ? Math.min(1, spent / cat.planned) : (spent > 0 ? 1 : 0);

    $('#detailCategoryName').textContent = cat.name;
    $('#detailCategorySub').textContent = `${currency.format(spent)} gastos de ${currency.format(cat.planned)} planejados`;
    const fill = $('#detailProgressFill');
    fill.classList.toggle('over', over);
    fill.style.width = '0%';
    requestAnimationFrame(() => { fill.style.width = `${pct * 100}%`; });

    const list = $('#expenseList');
    if (!cat.expenses.length) {
      list.innerHTML = '<div class="row-empty">Nenhum gasto lançado nesta categoria.</div>';
    } else {
      const sorted = [...cat.expenses].sort((a, b) => b.date.localeCompare(a.date));
      list.innerHTML = sorted.map(exp => `
        <div class="expense-row">
          <div class="expense-info">
            <span class="expense-desc">${escapeHtml(exp.desc)}</span>
            <span class="expense-date">${formatDate(exp.date)}</span>
          </div>
          <div class="expense-right">
            <span class="expense-value">${currency.format(exp.value)}</span>
            <button class="expense-del" data-action="del-expense" data-id="${exp.id}" aria-label="Excluir">
              <svg width="15" height="15" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/></svg>
            </button>
          </div>
        </div>`).join('');
    }
  }

  function formatDate(iso) {
    const [y, m, d] = iso.split('-');
    return `${d}/${m}/${y}`;
  }

  $('#editCategoryBtn').addEventListener('click', () => {
    const month = currentMonth();
    const cat = month.categories.find(c => c.id === currentDetailCategoryId);
    if (!cat) return;
    editingCategoryId = cat.id;
    $('#categoryModalTitle').textContent = 'Editar categoria';
    $('#categoryName').value = cat.name;
    $('#categoryPlanned').value = cat.planned.toFixed(2).replace('.', ',');
    openModal('categoryModal');
  });

  $('#deleteCategoryBtn').addEventListener('click', () => {
    confirmAction('Excluir esta categoria e todos os seus lançamentos?', () => {
      const month = currentMonth();
      month.categories = month.categories.filter(c => c.id !== currentDetailCategoryId);
      save();
      closeModal('detailModal');
      renderFull();
      toast('Categoria excluída.');
    });
  });

  $('#addExpenseBtn').addEventListener('click', () => {
    $('#expenseForm').reset();
    $('#expenseDate').value = new Date().toISOString().slice(0, 10);
    openModal('expenseModal');
  });

  $('#expenseForm').addEventListener('submit', e => {
    e.preventDefault();
    const date = $('#expenseDate').value;
    const desc = $('#expenseDesc').value.trim();
    const value = parseMoney($('#expenseValue').value);
    if (!date || !desc || isNaN(value) || value <= 0) { toast('Preencha todos os campos com valores válidos.'); return; }
    const month = currentMonth();
    const cat = month.categories.find(c => c.id === currentDetailCategoryId);
    cat.expenses.push({ id: uid(), date, desc, value });
    save();
    closeModal('expenseModal');
    renderDetail();
    renderFull();
    toast('Gasto lançado.');
  });

  $('#expenseList').addEventListener('click', e => {
    const btn = e.target.closest('[data-action="del-expense"]');
    if (!btn) return;
    const id = btn.dataset.id;
    confirmAction('Excluir este lançamento?', () => {
      const month = currentMonth();
      const cat = month.categories.find(c => c.id === currentDetailCategoryId);
      cat.expenses = cat.expenses.filter(exp => exp.id !== id);
      save();
      renderDetail();
      renderFull();
      toast('Lançamento excluído.');
    });
  });

  // ---------- Init ----------
  render(false);
})();
