const state = {
  currentView: 'dashboard',
  lastToolCalls: [],
};

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];

function setStatus(text, busy = false) {
  const chip = $('#statusChip');
  if (!chip) return;
  chip.textContent = text;
  chip.style.color = busy ? 'var(--gold)' : 'var(--cyan)';
}

async function api(path, options = {}) {
  const response = await fetch(path, options);
  const contentType = response.headers.get('content-type') || '';
  const data = contentType.includes('application/json') ? await response.json() : await response.text();
  if (!response.ok) {
    const detail = typeof data === 'object' ? data.detail || JSON.stringify(data) : data;
    throw new Error(detail || `Erro HTTP ${response.status}`);
  }
  return data;
}

function escapeHtml(value) {
  return String(value ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function showView(view) {
  state.currentView = view;
  $$('.nav-item').forEach((item) => item.classList.toggle('active', item.dataset.view === view));
  $$('[data-panel]').forEach((panel) => {
    const panels = (panel.dataset.panel || '').split(/\s+/);
    panel.classList.toggle('visible', panels.includes(view));
  });
}

function addMessage(role, text) {
  const history = $('#chatHistory');
  const div = document.createElement('div');
  div.className = `message ${role}`;
  div.textContent = text;
  history.appendChild(div);
  history.scrollTop = history.scrollHeight;
}

function renderToolCalls(toolCalls = []) {
  const target = $('#toolCalls');
  state.lastToolCalls = toolCalls;
  if (!toolCalls.length) {
    target.className = 'empty-state';
    target.textContent = 'Nenhuma ferramenta foi chamada.';
    return;
  }

  target.className = '';
  target.innerHTML = toolCalls.map((item) => `
    <div class="tool-item">
      <strong>${escapeHtml(item.tool || 'ferramenta')}</strong>
      <p>Entrada: ${escapeHtml(JSON.stringify(item.args || {}))}</p>
    </div>
  `).join('');
}

function renderSources(toolCalls = []) {
  const docs = [];
  for (const call of toolCalls) {
    const saida = call.saida;
    if (saida?.documentos_recuperados) docs.push(...saida.documentos_recuperados);
    if (saida?.materiais_relevantes) docs.push(...saida.materiais_relevantes);
  }

  const target = $('#sourcesList');
  if (!docs.length) {
    target.className = 'empty-state';
    target.textContent = 'Nenhuma fonte recuperada nesta interação.';
    return;
  }

  const seen = new Set();
  const unique = docs.filter((doc) => {
    const key = `${doc.id}-${doc.fonte}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  }).slice(0, 8);

  target.className = '';
  target.innerHTML = unique.map((doc) => `
    <div class="source-item">
      <strong>${escapeHtml(doc.fonte || doc.id || 'fonte')}</strong>
      <p>Score: ${escapeHtml(doc.score ?? '—')}</p>
      <p>${escapeHtml((doc.texto || '').slice(0, 180))}${(doc.texto || '').length > 180 ? '...' : ''}</p>
    </div>
  `).join('');
}

async function sendMessage(message) {
  setStatus('processando', true);
  addMessage('user', message);
  try {
    const data = await api('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mensagem: message }),
    });
    addMessage('assistant', data.resposta || 'Sem resposta.');
    renderToolCalls(data.tool_calls || []);
    renderSources(data.tool_calls || []);
    await loadLogs();
  } catch (error) {
    addMessage('assistant', `Erro: ${error.message}`);
  } finally {
    setStatus('pronto');
  }
}

async function loadStatus() {
  const data = await api('/api/status');
  $('#modeLabel').textContent = `Modo ${data.modo_llm?.toUpperCase() || '—'}`;
  $('#baseLabel').textContent = `${data.base_rag.documentos} docs · ${data.base_rag.chunks} chunks`;
  $('#metricDocs').textContent = data.base_rag.documentos;
  $('#metricChunks').textContent = data.base_rag.chunks;
  $('#metricMode').textContent = data.modo_llm?.toUpperCase() || '—';
}

async function loadTasks() {
  const tasks = await api('/api/tasks');
  const target = $('#tasksList');
  if (!tasks.length) {
    target.innerHTML = '<div class="empty-state">Nenhuma tarefa pendente.</div>';
    return;
  }
  target.innerHTML = tasks.map((task) => `
    <div class="task-item">
      <strong>${escapeHtml(task.titulo)}</strong>
      <p>${escapeHtml(task.disciplina || 'Sem disciplina')} · ${escapeHtml(task.prioridade || 'média')} · prazo: ${escapeHtml(task.prazo || 'sem prazo')}</p>
      <button class="complete-button" data-complete="${escapeHtml(task.id)}">Marcar como concluída</button>
    </div>
  `).join('');

  $$('[data-complete]').forEach((button) => {
    button.addEventListener('click', async () => {
      await api(`/api/tasks/${encodeURIComponent(button.dataset.complete)}/complete`, { method: 'PATCH' });
      await loadTasks();
    });
  });
}

async function loadAgenda() {
  const agenda = await api('/api/agenda');
  const target = $('#agendaList');
  if (!agenda.length) {
    target.innerHTML = '<div class="empty-state">Nenhum evento cadastrado.</div>';
    return;
  }
  target.innerHTML = agenda.slice(0, 10).map((event) => `
    <div class="agenda-item">
      <strong>${escapeHtml(event.titulo)}</strong>
      <p>${escapeHtml(event.data)} · ${escapeHtml(event.hora_inicio || 'horário livre')} ${event.hora_fim ? `- ${escapeHtml(event.hora_fim)}` : ''}</p>
      <p>${escapeHtml(event.observacao || '')}</p>
    </div>
  `).join('');
}

async function loadLogs() {
  const data = await api('/api/logs?limit=12');
  const target = $('#logsList');
  const items = data.items || [];
  if (!items.length) {
    target.innerHTML = '<div class="empty-state">Nenhum log registrado ainda.</div>';
    return;
  }
  target.innerHTML = items.map((log) => `
    <div class="log-item">
      <strong>${escapeHtml(log.ferramenta || 'log')}</strong>
      <p>${escapeHtml(log.timestamp || '')}</p>
      <p>Entrada: ${escapeHtml(JSON.stringify(log.entrada || {})).slice(0, 240)}</p>
    </div>
  `).join('');
}

async function refreshAll() {
  await Promise.allSettled([loadStatus(), loadTasks(), loadAgenda(), loadLogs()]);
}

function setupEvents() {
  $$('.nav-item').forEach((item) => item.addEventListener('click', () => showView(item.dataset.view)));
  $('#refreshButton').addEventListener('click', refreshAll);
  $('#reloadTasks').addEventListener('click', loadTasks);
  $('#reloadAgenda').addEventListener('click', loadAgenda);
  $('#reloadLogs').addEventListener('click', loadLogs);

  $('#chatForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const input = $('#messageInput');
    const message = input.value.trim();
    if (!message) return;
    input.value = '';
    showView('chat');
    await sendMessage(message);
  });

  $('#uploadForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const files = $('#fileInput').files;
    if (!files.length) return;
    setStatus('reindexando', true);
    const formData = new FormData();
    [...files].forEach((file) => formData.append('files', file));
    try {
      const data = await api('/api/upload', { method: 'POST', body: formData });
      $('#uploadResult').textContent = `Salvos: ${data.salvos.join(', ') || 'nenhum'} · Rejeitados: ${data.rejeitados.length}`;
      await loadStatus();
    } catch (error) {
      $('#uploadResult').textContent = `Erro: ${error.message}`;
    } finally {
      setStatus('pronto');
    }
  });

  $('#taskForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const titulo = $('#taskTitle').value.trim();
    if (!titulo) return;
    await api('/api/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ titulo, prazo: $('#taskDeadline').value, disciplina: 'Inteligência Artificial', prioridade: 'média' }),
    });
    $('#taskTitle').value = '';
    $('#taskDeadline').value = '';
    await loadTasks();
  });

  $('#agendaForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const data = $('#agendaDate').value;
    const titulo = $('#agendaTitle').value.trim();
    if (!data || !titulo) return;
    await api('/api/agenda', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ data, titulo, hora_inicio: $('#agendaStart').value, tipo: 'estudo' }),
    });
    $('#agendaTitle').value = '';
    $('#agendaStart').value = '';
    await loadAgenda();
  });

  $$('[data-shortcut]').forEach((button) => {
    button.addEventListener('click', async () => {
      const type = button.dataset.shortcut;
      const message = {
        plan: 'Monte um plano de estudos para a prova de IA.',
        rag: 'O que é RAG?',
        heap: 'O que é heap?',
      }[type];
      if (message) {
        showView('chat');
        await sendMessage(message);
      }
    });
  });
}

document.addEventListener('DOMContentLoaded', async () => {
  setupEvents();
  showView('dashboard');
  await refreshAll();
  addMessage('assistant', 'Olá. Sou o JARVIS Acadêmico. Posso consultar seus materiais, organizar tarefas, montar planos de estudo e registrar as ferramentas usadas.');
});
