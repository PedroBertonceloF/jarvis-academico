from __future__ import annotations

import json

import streamlit as st

from src.agent import JarvisAgent
from src.rag import RagEngine
from src.storage import AgendaStore, EventoAgenda, Tarefa, TarefaStore, inicializar_dados_demo

st.set_page_config(page_title="JARVIS Acadêmico", page_icon="🎓", layout="wide")

inicializar_dados_demo()


@st.cache_resource(show_spinner="Indexando materiais da pasta /data...")
def get_rag() -> RagEngine:
    return RagEngine(carregar_agora=True)


@st.cache_resource(show_spinner="Inicializando agente...")
def get_agent() -> JarvisAgent:
    return JarvisAgent()


st.title("🎓 JARVIS Acadêmico")
st.caption("Assistente inteligente com RAG, agenda, tarefas e tool calling via Gemma 12B.")

with st.sidebar:
    st.header("Base de conhecimento")
    rag = get_rag()
    st.write(f"Documentos: **{len(rag.docs)}**")
    st.write(f"Chunks: **{len(rag.chunks)}**")
    if st.button("Reindexar materiais"):
        get_rag.clear()
        get_agent.clear()
        st.rerun()

    st.divider()
    st.header("Agenda rápida")
    with st.form("novo_evento"):
        data = st.date_input("Data")
        titulo = st.text_input("Título do evento")
        hora_inicio = st.text_input("Início", value="19:00")
        hora_fim = st.text_input("Fim", value="21:00")
        tipo = st.selectbox("Tipo", ["aula", "prova", "trabalho", "estudo", "outro"])
        enviado = st.form_submit_button("Adicionar evento")
        if enviado and titulo.strip():
            AgendaStore().adicionar(EventoAgenda(
                data=data.isoformat(),
                titulo=titulo.strip(),
                hora_inicio=hora_inicio,
                hora_fim=hora_fim,
                tipo=tipo,
            ))
            st.success("Evento adicionado.")

    st.divider()
    st.header("Tarefa rápida")
    with st.form("nova_tarefa"):
        tarefa_titulo = st.text_input("Tarefa")
        prazo = st.date_input("Prazo")
        disciplina = st.text_input("Disciplina", value="Inteligência Artificial")
        prioridade = st.selectbox("Prioridade", ["baixa", "média", "alta"], index=2)
        enviar_tarefa = st.form_submit_button("Adicionar tarefa")
        if enviar_tarefa and tarefa_titulo.strip():
            TarefaStore().adicionar(Tarefa(
                titulo=tarefa_titulo.strip(),
                prazo=prazo.isoformat(),
                disciplina=disciplina,
                prioridade=prioridade,
            ))
            st.success("Tarefa adicionada.")

abas = st.tabs(["Chat", "Agenda", "Tarefas", "Active Recall", "Logs"])

with abas[0]:
    st.subheader("Converse com o JARVIS")
    st.info("Exemplos: 'Explique regressão logística', 'O que tenho hoje?', 'Adicione tarefa estudar BM25 para sexta', 'Monte um plano para a prova de IA'.")

    if "historico" not in st.session_state:
        st.session_state.historico = []

    for item in st.session_state.historico:
        with st.chat_message(item["role"]):
            st.markdown(item["content"])

    pergunta = st.chat_input("Digite sua mensagem...")
    if pergunta:
        st.session_state.historico.append({"role": "user", "content": pergunta})
        with st.chat_message("user"):
            st.markdown(pergunta)
        with st.chat_message("assistant"):
            with st.spinner("Pensando e chamando ferramentas quando necessário..."):
                try:
                    resposta = get_agent().responder(pergunta)
                    st.markdown(resposta["resposta"])
                    if resposta["tool_calls"]:
                        with st.expander("Ferramentas chamadas"):
                            st.json(resposta["tool_calls"])
                    st.session_state.historico.append({"role": "assistant", "content": resposta["resposta"]})
                except Exception as e:
                    st.error(f"Erro: {e}")

with abas[1]:
    st.subheader("Agenda acadêmica")
    eventos = AgendaStore().listar()
    st.dataframe(eventos, use_container_width=True)

with abas[2]:
    st.subheader("Lista de tarefas")
    tarefas = TarefaStore().listar(incluir_concluidas=True)
    st.dataframe(tarefas, use_container_width=True)
    concluir = st.text_input("ID ou trecho do título para concluir")
    if st.button("Marcar como concluída") and concluir.strip():
        try:
            item = TarefaStore().concluir(concluir)
            st.success(f"Concluída: {item['titulo']}")
            st.rerun()
        except Exception as e:
            st.error(str(e))

with abas[3]:
    st.subheader("Prática interativa — Active Recall")
    st.write("O sistema faz uma pergunta, você responde e depois recebe feedback.")
    tema = st.text_input("Tema", value="RAG e embeddings")

    if st.button("Gerar pergunta"):
        with st.spinner("Buscando material e gerando pergunta..."):
            base = rag.responder(f"Crie uma pergunta de revisão sobre {tema}", k=3)
            prompt = (
                "Com base nesta explicação, crie uma pergunta objetiva de active recall e uma resposta esperada. "
                "Formato: Pergunta: ... Resposta esperada: ...\n\n"
                + base["resposta"]
            )
            from src.llm_client import GemmaClient
            st.session_state.pergunta_active = GemmaClient().chat([
                {"role": "system", "content": "Você cria perguntas de revisão acadêmica."},
                {"role": "user", "content": prompt},
            ])

    if "pergunta_active" in st.session_state:
        st.markdown(st.session_state.pergunta_active)
        resposta_aluno = st.text_area("Sua resposta")
        if st.button("Avaliar minha resposta") and resposta_aluno.strip():
            from src.llm_client import GemmaClient
            feedback_prompt = f"""
Avalie a resposta do estudante com postura de professor.
Dê: classificação (correta/parcial/incorreta), pontos fortes, correção objetiva e recomendação de revisão.

Pergunta e resposta esperada:
{st.session_state.pergunta_active}

Resposta do estudante:
{resposta_aluno}
""".strip()
            feedback = GemmaClient().chat([
                {"role": "system", "content": "Você avalia respostas de estudantes com feedback objetivo."},
                {"role": "user", "content": feedback_prompt},
            ])
            st.markdown(feedback)

with abas[4]:
    st.subheader("Logs de tool calling")
    from src.config import settings
    log_path = settings.log_dir / "tool_calls.jsonl"
    if log_path.exists():
        linhas = log_path.read_text(encoding="utf-8").splitlines()[-50:]
        for linha in linhas[::-1]:
            try:
                st.json(json.loads(linha))
            except Exception:
                st.code(linha)
    else:
        st.info("Nenhum log ainda. Use o chat para acionar ferramentas.")
