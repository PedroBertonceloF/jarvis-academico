from __future__ import annotations

from datetime import datetime
import json
from typing import Any

from .config import settings

LOG_PATH = settings.log_dir / "tool_calls.jsonl"


def registrar_tool_call(ferramenta: str, entrada: dict[str, Any], saida: Any) -> None:
    registro = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "ferramenta": ferramenta,
        "entrada": entrada,
        "saida": saida,
    }
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")
