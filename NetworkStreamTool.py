import subprocess
import sys
import time
from pathlib import Path

EXECUTABLE_DIRECTORY = Path(sys.executable).resolve().parent
PYTHON_PATH = EXECUTABLE_DIRECTORY / ".venv" / "Scripts" / "python.exe"

if __name__ == "__main__":
    # creation_flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else None
    # subprocess.Popen([str(PYTHON_PATH), "app/app.py"], creationflags=creation_flags)
    subprocess.Popen([str(PYTHON_PATH), "app/app.py"])
    time.sleep(2)
    # webbrowser.open("http://localhost:8000")
