import os
import subprocess
import sys
from pathlib import Path

from app.server._config import PROJECT_DIRECTORY


def open_file(file_path: Path) -> None:
    try:
        subprocess.run(
            ["code", "-r", PROJECT_DIRECTORY, "-g", file_path], check=True, shell=True
        )
    except subprocess.CalledProcessError:
        if sys.platform == "win32":
            os.startfile(file_path)
        else:
            open_command = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([open_command, file_path])
