import pytest

from src.config import Settings


def test_settings_aceita_modos_remotos_legados_e_novos():
    for modo in ["gemma", "qwen", "remote", "openai_compatible", "openai-compatible", "QWEN"]:
        settings = Settings(
            llm_mode=modo,
            gemma_base_url="https://example.com/v1/model",
            gemma_api_key="token",
            gemma_model="Qwen/Qwen2.5-14B-Instruct-AWQ",
        )

        settings.validate_llm()
        assert settings.llm_provider == "openai-compatible"


def test_settings_rejeita_modo_llm_desconhecido():
    settings = Settings(
        llm_mode="desconhecido",
        gemma_base_url="https://example.com/v1/model",
        gemma_api_key="token",
        gemma_model="Qwen/Qwen2.5-14B-Instruct-AWQ",
    )

    with pytest.raises(RuntimeError, match="LLM_MODE inválido"):
        settings.validate_llm()
