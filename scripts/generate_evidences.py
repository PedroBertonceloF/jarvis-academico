from __future__ import annotations

from pathlib import Path
import subprocess
import sys

EVID = Path("evidencias")
EVID.mkdir(exist_ok=True)

checks = [
    ("01_compilacao.txt", [sys.executable, "-m", "compileall", "-q", "src", "app.py", "main.py"]),
    ("02_dataset.txt", [sys.executable, "scripts/check_dataset.py"]),
]

for filename, cmd in checks:
    result = subprocess.run(cmd, text=True, capture_output=True)
    (EVID / filename).write_text(
        f"COMANDO: {' '.join(cmd)}

STDOUT:
{result.stdout}

STDERR:
{result.stderr}

RETURN_CODE: {result.returncode}
",
        encoding="utf-8",
    )

print(f"Evidências geradas em: {EVID.resolve()}")
