# ruff: noqa: D100, D103

import textwrap
from pathlib import Path

ROOT_DIRECTORY = Path(__file__).parent

results = ""

results += "Some metric: 0.123\n"


def get_content(results: str) -> str:
    return textwrap.dedent(f"""\
        ## Results
        {results}\
    """)


def save_results_logic() -> Path:
    save_file_path = ROOT_DIRECTORY / "results.md"
    content = get_content(results)
    with Path.open(save_file_path, "w") as file:
        file.write(content)
    return save_file_path
