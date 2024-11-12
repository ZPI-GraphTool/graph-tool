import shelve
import shutil
from enum import StrEnum
from pathlib import Path

from .open_file_in_editor import open_file_in_editor

ALGORITHMS_DIRECTORY = Path(__file__).parents[3] / "algorithms"
TEMPLATES_DIRECTORY = ALGORITHMS_DIRECTORY / "templates"


class AlgorithmType(StrEnum):
    PREPROCESSING = "preprocessing"
    BATCH = "batch"
    STREAMING = "streaming"


class AlgorithmTypeSpecification:
    @classmethod
    def new_file(cls, type: AlgorithmType) -> str:
        match type:
            case AlgorithmType.PREPROCESSING:
                prefix = "function"
            case AlgorithmType.BATCH | AlgorithmType.STREAMING:
                prefix = "algorithm"
        # this caches how many files of each type have been created
        # so that we know what number to name the new file of a given type
        with shelve.open(ALGORITHMS_DIRECTORY / "counter") as counter:
            key = f"{type}_counter"
            if key not in counter:
                counter[key] = 0
            file_name = f"{prefix}_{counter[key]}.py"
            counter[key] += 1
        return file_name

    @classmethod
    def paths(cls, type: AlgorithmType) -> tuple[Path, Path]:
        template_path = TEMPLATES_DIRECTORY / f"template_{type}.py"
        destination = ALGORITHMS_DIRECTORY / type / cls.new_file(type)
        return template_path, destination


def edit_algorithm(option: str, type: AlgorithmType) -> None:
    if option == "New":
        template, destination = AlgorithmTypeSpecification.paths(type)
        new_file_path = shutil.copy(template, destination)
        open_file_in_editor(new_file_path)
    else:
        open_file_in_editor(Path(option))
