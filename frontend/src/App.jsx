import React, { useEffect, useMemo, useRef, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import {
  ArrowRight,
  BookOpen,
  BrainCircuit,
  CalendarDays,
  CheckCircle2,
  ChevronRight,
  Database,
  FileText,
  Gauge,
  GitBranch,
  GraduationCap,
  ListTodo,
  Loader2,
  Menu,
  MessageSquareText,
  Moon,
  Paperclip,
  RefreshCcw,
  Search,
  Send,
  ShieldCheck,
  Sparkles,
  TerminalSquare,
  UploadCloud,
  X,
  Zap,
} from 'lucide-react';

const API_BASE = import.meta.env.VITE_API_BASE || '';

const quickPrompts = [
  'O que é RAG?',
  'Explique regressão logística.',
  'Monte um plano de estudos para a prova de IA.',
  'Gere 3 exercícios sobre embeddings.',
  'O que é heap?',
];

const formatTime = () => new Intl.DateTimeFormat('pt-BR', {
  hour: '2-digit',
  minute: '2-digit',
}).format(new Date());

async function apiFetch(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: options.body instanceof FormData ? undefined : { 'Content-Type': 'application/json' },
    ...options,
  });

  if (!response.ok) {
    let detail = `Erro HTTP ${response.status}`;
    try {
      const data = await response.json();
      detail = data.detail || detail;
    } catch {
      // mantém erro padrão
    }
    throw new Error(detail);
  }
  return response.json();
}

function extractSources(toolCalls = []) {
  const map = new Map();
  for (const call of toolCalls) {
    const output = call?.saida || {};
    const docs = output.documentos_recuperados || output.materiais_relevantes || [];
    for (const doc of docs) {
      const key = doc.id || `${doc.fonte}-${doc.score}`;
      if (!map.has(key)) map.set(key, doc);
    }
  }
  return Array.from(map.values());
}

function humanToolName(tool) {
  const names = {
    buscar_material_rag: 'Busca RAG',
    consultar_agenda: 'Agenda',
    listar_tarefas: 'Tarefas',
    adicionar_tarefa: 'Nova tarefa',
    concluir_tarefa: 'Concluir tarefa',
    planejar_estudos: 'Plano de estudo',
    gerar_exercicios: 'Exercícios',
  };
  return names[tool] || tool || 'Ferramenta';
}

function inferMode(toolCalls = []) {
  if (!toolCalls.length) return { label: 'Resposta direta', tone: 'neutral' };
  const hasEmpty = toolCalls.some((call) => call?.saida?.resultado_vazio);
  const hasRag = toolCalls.some((call) => call?.tool === 'buscar_material_rag');
  if (hasEmpty) return { label: 'Fallback acadêmico', tone: 'warning' };
  if (hasRag) return { label: 'RAG fundamentado', tone: 'success' };
  return { label: 'Tool calling', tone: 'info' };
}

function BrandOrb() {
  return (
    <div className="brand-orb" aria-hidden="true">
      <span />
      <span />
      <span />
    </div>
  );
}

function Sidebar({ active, setActive, collapsed, setCollapsed }) {
  const items = [
    { id: 'chat', label: 'Chat', icon: MessageSquareText },
    { id: 'materiais', label: 'Materiais', icon: Database },
    { id: 'tarefas', label: 'Tarefas', icon: ListTodo },
    { id: 'agenda', label: 'Agenda', icon: CalendarDays },
    { id: 'logs', label: 'Logs', icon: TerminalSquare },
  ];

  return (
    <aside className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
      <div className="sidebar-top">
        <div className="brand">
          <BrandOrb />
          {!collapsed && (
            <div>
              <strong>JARVIS</strong>
              <span>Acadêmico</span>
            </div>
          )}
        </div>
        <button className="icon-button ghost" onClick={() => setCollapsed(!collapsed)} title="Alternar menu">
          <Menu size={18} />
        </button>
      </div>

      <nav className="nav-list">
        {items.map((item) => {
          const Icon = item.icon;
          return (
            <button
              key={item.id}
              className={`nav-item ${active === item.id ? 'active' : ''}`}
              onClick={() => setActive(item.id)}
            >
              <Icon size={18} />
              {!collapsed && <span>{item.label}</span>}
            </button>
          );
        })}
      </nav>

      {!collapsed && (
        <div className="sidebar-card">
          <div className="mini-label">Missão</div>
          <p>Organizar materiais, estudar com foco e registrar evidências técnicas do aprendizado.</p>
        </div>
      )}
    </aside>
  );
}

function StatusBar({ status, onRefresh }) {
  const base = status?.base_rag || {};
  return (
    <header className="topbar">
      <div>
        <div className="eyebrow"><Sparkles size={14} /> Study workspace</div>
        <h1>Copiloto acadêmico com RAG e tool calling</h1>
      </div>
      <div className="topbar-actions">
        <span className={`status-pill ${status?.usando_mock ? 'mock' : 'gemma'}`}>
          <Gauge size={14} /> {status?.modo_llm || 'carregando'}
        </span>
        <span className="status-pill"><Database size={14} /> {base.chunks ?? 0} chunks</span>
        <button className="icon-button" onClick={onRefresh} title="Atualizar status">
          <RefreshCcw size={16} />
        </button>
      </div>
    </header>
  );
}

function MessageBubble({ message }) {
  const isUser = message.role === 'user';
  const mode = inferMode(message.tool_calls);
  return (
    <article className={`message ${isUser ? 'user' : 'assistant'}`}>
      <div className="message-avatar">
        {isUser ? <GraduationCap size={18} /> : <BrandOrb />}
      </div>
      <div className="message-body">
        <div className="message-meta">
          <strong>{isUser ? 'Você' : 'JARVIS'}</strong>
          <span>{message.time}</span>
          {!isUser && <span className={`mode-badge ${mode.tone}`}>{mode.label}</span>}
        </div>
        <div className="markdown-card">
          {isUser ? (
            <p>{message.content}</p>
          ) : (
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.content}</ReactMarkdown>
          )}
        </div>
        {!isUser && message.sources?.length > 0 && (
          <div className="source-row">
            {message.sources.slice(0, 3).map((source) => (
              <span key={source.id || source.fonte} className="source-chip">
                <FileText size={13} /> {source.fonte || source.id}
              </span>
            ))}
          </div>
        )}
      </div>
    </article>
  );
}

function ChatPanel({ messages, input, setInput, onSubmit, isLoading, onQuickPrompt }) {
  const bottomRef = useRef(null);
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
    <section className="chat-panel">
      <div className="session-card">
        <div>
          <span className="mini-label">Sessão atual</span>
          <h2>Prova de Inteligência Artificial</h2>
          <p>Converse com o JARVIS, importe materiais e acompanhe fontes, ferramentas e tarefas em tempo real.</p>
        </div>
        <div className="session-actions">
          <span><ShieldCheck size={15} /> Governança de fonte</span>
          <span><Zap size={15} /> Tutor mode</span>
        </div>
      </div>

      <div className="quick-row">
        {quickPrompts.map((prompt) => (
          <button key={prompt} className="quick-chip" onClick={() => onQuickPrompt(prompt)}>
            {prompt}
          </button>
        ))}
      </div>

      <div className="messages-area">
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
        {isLoading && (
          <article className="message assistant loading">
            <div className="message-avatar"><BrandOrb /></div>
            <div className="message-body">
              <div className="message-meta"><strong>JARVIS</strong><span>pensando...</span></div>
              <div className="typing"><span /><span /><span /></div>
            </div>
          </article>
        )}
        <div ref={bottomRef} />
      </div>

      <form className="composer" onSubmit={onSubmit}>
        <button type="button" className="composer-icon" title="Use o painel de Materiais para upload">
          <Paperclip size={18} />
        </button>
        <textarea
          value={input}
          onChange={(event) => setInput(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === 'Enter' && !event.shiftKey) {
              event.preventDefault();
              onSubmit(event);
            }
          }}
          placeholder="Pergunte ao JARVIS sobre seus estudos..."
          rows={1}
        />
        <button className="send-button" disabled={isLoading || !input.trim()}>
          {isLoading ? <Loader2 className="spin" size={18} /> : <Send size={18} />}
        </button>
      </form>
    </section>
  );
}

function ContextPanel({ selectedMessage, logs, tasks, agenda, status }) {
  const toolCalls = selectedMessage?.tool_calls || [];
  const sources = selectedMessage?.sources || [];

  return (
    <aside className="context-panel">
      <section className="context-card glow-card">
        <div className="context-title"><BrainCircuit size={17} /> Estado do sistema</div>
        <div className="metric-grid">
          <div><strong>{status?.base_rag?.documentos ?? 0}</strong><span>docs</span></div>
          <div><strong>{status?.base_rag?.chunks ?? 0}</strong><span>chunks</span></div>
        </div>
      </section>

      <section className="context-card">
        <div className="context-title"><Search size={17} /> Fontes do turno</div>
        {sources.length ? sources.slice(0, 5).map((source) => (
          <div className="source-card" key={source.id || source.fonte}>
            <div><FileText size={15} /> <strong>{source.fonte || source.id}</strong></div>
            <p>{source.texto ? `${source.texto.slice(0, 170)}...` : 'Trecho recuperado pelo RAG.'}</p>
            {typeof source.score === 'number' && <span>score {source.score.toFixed(3)}</span>}
          </div>
        )) : <p className="muted">As fontes recuperadas aparecerão aqui após uma consulta RAG.</p>}
      </section>

      <section className="context-card">
        <div className="context-title"><TerminalSquare size={17} /> Ferramentas chamadas</div>
        {toolCalls.length ? toolCalls.map((call, index) => (
          <div className="tool-line" key={`${call.tool}-${index}`}>
            <span>{humanToolName(call.tool)}</span>
            <code>{Object.keys(call.args || {}).join(', ') || 'sem args'}</code>
          </div>
        )) : <p className="muted">Quando a LLM usar uma ferramenta, o rastro técnico aparece aqui.</p>}
      </section>

      <section className="context-card compact-list">
        <div className="context-title"><ListTodo size={17} /> Próximas tarefas</div>
        {tasks.slice(0, 3).map((task) => (
          <div className="mini-item" key={task.id}>
            <span>{task.titulo}</span>
            <small>{task.prazo || 'sem prazo'}</small>
          </div>
        ))}
        {!tasks.length && <p className="muted">Nenhuma tarefa pendente.</p>}
      </section>

      <section className="context-card compact-list">
        <div className="context-title"><CalendarDays size={17} /> Agenda</div>
        {agenda.slice(0, 2).map((event, index) => (
          <div className="mini-item" key={`${event.data}-${index}`}>
            <span>{event.titulo}</span>
            <small>{event.data} {event.hora_inicio || ''}</small>
          </div>
        ))}
        {!agenda.length && <p className="muted">Nenhum evento encontrado.</p>}
      </section>

      <section className="context-card compact-list">
        <div className="context-title"><GitBranch size={17} /> Últimos logs</div>
        {logs.slice(0, 3).map((log, index) => (
          <div className="mini-item" key={`${log.timestamp}-${index}`}>
            <span>{humanToolName(log.ferramenta)}</span>
            <small>{log.timestamp}</small>
          </div>
        ))}
        {!logs.length && <p className="muted">Sem logs ainda.</p>}
      </section>
    </aside>
  );
}

function MaterialsView({ status, onRefresh }) {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);
  const inputRef = useRef(null);

  async function upload() {
    if (!files.length) return;
    setUploading(true);
    setResult(null);
    try {
      const formData = new FormData();
      Array.from(files).forEach((file) => formData.append('files', file));
      const data = await apiFetch('/api/upload', { method: 'POST', body: formData });
      setResult(data);
      inputRef.current.value = '';
      setFiles([]);
      onRefresh();
    } catch (error) {
      setResult({ error: error.message });
    } finally {
      setUploading(false);
    }
  }

  const arquivos = status?.base_rag?.arquivos || [];
  return (
    <section className="workspace-view">
      <div className="view-header">
        <div>
          <span className="mini-label">Base de conhecimento</span>
          <h2>Materiais conectados ao JARVIS</h2>
          <p>Importe PDFs, Markdown, textos ou código. O RAG reindexa a base e passa a responder com esses materiais.</p>
        </div>
        <button className="primary-button" onClick={onRefresh}><RefreshCcw size={16} /> Atualizar</button>
      </div>

      <div className="upload-zone">
        <UploadCloud size={30} />
        <h3>Importar documentos</h3>
        <p>Formatos suportados: PDF, MD, TXT e PY.</p>
        <input ref={inputRef} type="file" multiple accept=".pdf,.md,.txt,.py" onChange={(event) => setFiles(event.target.files)} />
        <button className="primary-button" disabled={!files.length || uploading} onClick={upload}>
          {uploading ? <Loader2 className="spin" size={16} /> : <UploadCloud size={16} />}
          Salvar e reindexar
        </button>
        {result && (
          <div className={`result-box ${result.error ? 'error' : 'ok'}`}>
            {result.error ? result.error : `Arquivos salvos: ${result.salvos?.join(', ') || 'nenhum'}`}
          </div>
        )}
      </div>

      <div className="file-grid">
        {arquivos.map((arquivo) => (
          <div className="file-card" key={arquivo}>
            <FileText size={18} />
            <span>{arquivo}</span>
          </div>
        ))}
      </div>
    </section>
  );
}

function TasksView({ tasks, refresh }) {
  const [form, setForm] = useState({ titulo: '', prazo: '', disciplina: 'Inteligência Artificial', prioridade: 'alta' });

  async function addTask(event) {
    event.preventDefault();
    if (!form.titulo.trim()) return;
    await apiFetch('/api/tasks', { method: 'POST', body: JSON.stringify(form) });
    setForm({ ...form, titulo: '', prazo: '' });
    refresh();
  }

  async function completeTask(id) {
    await apiFetch(`/api/tasks/${id}/complete`, { method: 'PATCH' });
    refresh();
  }

  return (
    <section className="workspace-view">
      <div className="view-header">
        <div>
          <span className="mini-label">Execução</span>
          <h2>Tarefas de estudo</h2>
          <p>Organize pendências e deixe o JARVIS usar esses dados no planejamento.</p>
        </div>
      </div>
      <form className="task-form" onSubmit={addTask}>
        <input placeholder="Nova tarefa" value={form.titulo} onChange={(e) => setForm({ ...form, titulo: e.target.value })} />
        <input type="date" value={form.prazo} onChange={(e) => setForm({ ...form, prazo: e.target.value })} />
        <button className="primary-button"><ArrowRight size={16} /> Adicionar</button>
      </form>
      <div className="list-stack">
        {tasks.map((task) => (
          <div className="list-card" key={task.id}>
            <div>
              <strong>{task.titulo}</strong>
              <span>{task.disciplina} • {task.prazo || 'sem prazo'} • {task.prioridade}</span>
            </div>
            {!task.concluida && <button className="icon-button" onClick={() => completeTask(task.id)}><CheckCircle2 size={18} /></button>}
          </div>
        ))}
      </div>
    </section>
  );
}

function AgendaView({ agenda }) {
  return (
    <section className="workspace-view">
      <div className="view-header">
        <div>
          <span className="mini-label">Rotina</span>
          <h2>Agenda acadêmica</h2>
          <p>Eventos consultados pela ferramenta de agenda durante as respostas.</p>
        </div>
      </div>
      <div className="timeline">
        {agenda.map((event, index) => (
          <div className="timeline-item" key={`${event.data}-${index}`}>
            <div className="timeline-dot" />
            <div>
              <strong>{event.titulo}</strong>
              <span>{event.data} • {event.hora_inicio || '--:--'} {event.hora_fim ? `até ${event.hora_fim}` : ''}</span>
              {event.observacao && <p>{event.observacao}</p>}
            </div>
          </div>
        ))}
        {!agenda.length && <p className="muted">Nenhum evento na agenda.</p>}
      </div>
    </section>
  );
}

function LogsView({ logs }) {
  return (
    <section className="workspace-view">
      <div className="view-header">
        <div>
          <span className="mini-label">Evidência técnica</span>
          <h2>Logs de tool calling</h2>
          <p>Registro das ferramentas chamadas, entradas e saídas. Útil para demonstrar o requisito do trabalho.</p>
        </div>
      </div>
      <div className="log-stack">
        {logs.map((log, index) => (
          <details className="log-card" key={`${log.timestamp}-${index}`}>
            <summary>
              <span>{humanToolName(log.ferramenta)}</span>
              <small>{log.timestamp}</small>
            </summary>
            <pre>{JSON.stringify(log, null, 2)}</pre>
          </details>
        ))}
      </div>
    </section>
  );
}

function ChatWorkspace({ active, ...props }) {
  if (active === 'materiais') return <MaterialsView status={props.status} onRefresh={props.refreshAll} />;
  if (active === 'tarefas') return <TasksView tasks={props.tasks} refresh={props.refreshAll} />;
  if (active === 'agenda') return <AgendaView agenda={props.agenda} />;
  if (active === 'logs') return <LogsView logs={props.logs} />;
  return <ChatPanel {...props} />;
}

export default function App() {
  const [active, setActive] = useState('chat');
  const [collapsed, setCollapsed] = useState(false);
  const [status, setStatus] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [agenda, setAgenda] = useState([]);
  const [logs, setLogs] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      role: 'assistant',
      time: formatTime(),
      content: 'Olá! Eu sou o **JARVIS Acadêmico**. Posso consultar seus materiais, montar planos de estudo, gerar exercícios e registrar as ferramentas usadas em cada resposta.',
      tool_calls: [],
      sources: [],
    },
  ]);

  const selectedMessage = useMemo(() => {
    return [...messages].reverse().find((msg) => msg.role === 'assistant') || null;
  }, [messages]);

  async function refreshAll() {
    try {
      const [statusData, taskData, agendaData, logData] = await Promise.all([
        apiFetch('/api/status'),
        apiFetch('/api/tasks'),
        apiFetch('/api/agenda'),
        apiFetch('/api/logs?limit=20'),
      ]);
      setStatus(statusData);
      setTasks(taskData || []);
      setAgenda(agendaData || []);
      setLogs(logData.items || []);
    } catch (error) {
      console.error(error);
    }
  }

  useEffect(() => {
    refreshAll();
  }, []);

  async function submitMessage(event) {
    event?.preventDefault();
    const text = input.trim();
    if (!text || isLoading) return;

    setInput('');
    setActive('chat');
    const userMessage = { id: crypto.randomUUID(), role: 'user', content: text, time: formatTime() };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const data = await apiFetch('/api/chat', {
        method: 'POST',
        body: JSON.stringify({ mensagem: text }),
      });
      const sources = extractSources(data.tool_calls || []);
      const assistantMessage = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: data.resposta || 'Sem resposta retornada.',
        time: formatTime(),
        tool_calls: data.tool_calls || [],
        sources,
      };
      setMessages((prev) => [...prev, assistantMessage]);
      refreshAll();
    } catch (error) {
      setMessages((prev) => [...prev, {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: `### Erro controlado\n${error.message}`,
        time: formatTime(),
        tool_calls: [],
        sources: [],
      }]);
    } finally {
      setIsLoading(false);
    }
  }

  function onQuickPrompt(prompt) {
    setInput(prompt);
    setActive('chat');
  }

  return (
    <div className="app-shell">
      <Sidebar active={active} setActive={setActive} collapsed={collapsed} setCollapsed={setCollapsed} />
      <main className="main-area">
        <StatusBar status={status} onRefresh={refreshAll} />
        <div className="workspace-grid">
          <ChatWorkspace
            active={active}
            messages={messages}
            input={input}
            setInput={setInput}
            onSubmit={submitMessage}
            isLoading={isLoading}
            onQuickPrompt={onQuickPrompt}
            status={status}
            tasks={tasks}
            agenda={agenda}
            logs={logs}
            refreshAll={refreshAll}
          />
          <ContextPanel selectedMessage={selectedMessage} logs={logs} tasks={tasks} agenda={agenda} status={status} />
        </div>
      </main>
    </div>
  );
}
