from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
STORAGE_DIR = ROOT_DIR / "storage"
LOG_DIR = ROOT_DIR / "logs"

for directory in [DATA_DIR, STORAGE_DIR, LOG_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

load_dotenv(ROOT_DIR / ".env")

REMOTE_LLM_MODES = {"gemma", "qwen", "remote", "openai_compatible", "openai-compatible"}


@dataclass(frozen=True)
class Settings:
    # Use LLM_MODE=mock para testar sem o token do professor.
    # Use LLM_MODE=gemma na entrega final para manter compatibilidade com o deploy.
    # Os nomes GEMMA_* são legados: hoje configuram um cliente LLM remoto OpenAI-compatible.
    llm_mode: str = os.getenv("LLM_MODE", "mock").strip().lower()
    gemma_base_url: str = os.getenv("GEMMA_BASE_URL", "")
    gemma_api_key: str = os.getenv("GEMMA_API_KEY", "")
    gemma_model: str = os.getenv("GEMMA_MODEL", "Qwen/Qwen2.5-14B-Instruct-AWQ")
    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    )
    data_dir: Path = DATA_DIR
    storage_dir: Path = STORAGE_DIR
    log_dir: Path = LOG_DIR

    @property
    def llm_mode_normalizado(self) -> str:
        return str(self.llm_mode or "").strip().lower()

    @property
    def usando_mock(self) -> bool:
        return self.llm_mode_normalizado == "mock"

    @property
    def usando_llm_remota(self) -> bool:
        return self.llm_mode_normalizado in REMOTE_LLM_MODES

    @property
    def llm_provider(self) -> str:
        return "mock" if self.usando_mock else "openai-compatible"

    @property
    def llm_provider_label(self) -> str:
        return str(self.gemma_model or "").strip() or "LLM remota OpenAI-compatible"

    def validate_llm(self) -> None:
        if self.usando_mock:
            return

        if not self.usando_llm_remota:
            raise RuntimeError(
                "LLM_MODE inválido: "
                + self.llm_mode_normalizado
                + ". Use mock, gemma, qwen, remote ou openai_compatible."
            )

        missing = []
        if not str(self.gemma_base_url or "").strip():
            missing.append("GEMMA_BASE_URL")
        api_key = str(self.gemma_api_key or "").strip()
        if not api_key or api_key in {"COLE_SEU_TOKEN_AQUI", "COLE_A_CHAVE_AQUI"}:
            missing.append("GEMMA_API_KEY")
        if missing:
            raise RuntimeError(
                "Variáveis de ambiente ausentes: "
                + ", ".join(missing)
                + ". Crie um arquivo .env baseado no .env.example. "
                + "Para testar sem token, defina LLM_MODE=mock no .env."
            )


settings = Settings()
