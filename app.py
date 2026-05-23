from __future__ import annotations

"""Compatibility entrypoint for the current FastAPI application.

The final project uses React + FastAPI, so this module only exposes
the FastAPI `app` object and allows `python app.py` to start the
backend locally.
"""

import os

import uvicorn

from web_api.main import app


def main() -> None:
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("web_api.main:app", host="0.0.0.0", port=port, reload=False)


if __name__ == "__main__":
    main()
