from __future__ import annotations

from src.agent import JarvisAgent
from src.storage import inicializar_dados_demo


def main() -> None:
    inicializar_dados_demo()
    agent = JarvisAgent()
    print("JARVIS Acadêmico iniciado. Digite 'sair' para encerrar.")
    while True:
        pergunta = input("\nVocê: ").strip()
        if pergunta.lower() in {"sair", "exit", "quit"}:
            break
        try:
            resultado = agent.responder(pergunta)
            print("\nJARVIS:", resultado["resposta"])
            if resultado["tool_calls"]:
                print("\nFerramentas chamadas:")
                for chamada in resultado["tool_calls"]:
                    print("-", chamada["tool"])
        except Exception as exc:
            print(f"Erro: {exc}")


if __name__ == "__main__":
    main()
