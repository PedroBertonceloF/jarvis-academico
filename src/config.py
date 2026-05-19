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


@dataclass(frozen=True)
class Settings:
    # Use LLM_MODE=mock para testar sem o token do professor.
    # Use LLM_MODE=gemma na entrega final, com GEMMA_API_KEY preenchido.
    llm_mode: str = os.getenv("LLM_MODE", "mock").strip().lower()
    gemma_base_url: str = os.getenv("GEMMA_BASE_URL", "")
    gemma_api_key: str = os.getenv("GEMMA_API_KEY", "")
    gemma_model: str = os.getenv("GEMMA_MODEL", "google/gemma-3-12b-it")
    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    )
    data_dir: Path = DATA_DIR
    storage_dir: Path = STORAGE_DIR
    log_dir: Path = LOG_DIR

    @property
    def usando_mock(self) -> bool:
        return self.llm_mode == "mock"

    def validate_llm(self) -> None:
        if self.usando_mock:
            return

        missing = []
        if not self.gemma_base_url:
            missing.append("GEMMA_BASE_URL")
        if not self.gemma_api_key or self.gemma_api_key == "COLE_SEU_TOKEN_AQUI":
            missing.append("GEMMA_API_KEY")
        if missing:
            raise RuntimeError(
                "Variáveis de ambiente ausentes: "
                + ", ".join(missing)
                + ". Crie um arquivo .env baseado no .env.example. "
                + "Para testar sem token, defina LLM_MODE=mock no .env."
            )


settings = Settings()
