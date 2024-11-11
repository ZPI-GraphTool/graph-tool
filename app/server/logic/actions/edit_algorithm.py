import shelve
import shutil
from enum import StrEnum
from pathlib import Path

from .open_file_in_editor import open_file_in_editor

ALGORITHMS_DIRECTORY = Path(__file__).parents[3] / "algorithms"
TEMPLATES_DIRECTORY = ALGORITHMS_DIRECTORY / "templates"


class AlgorithmType(StrEnum):
    PREPROCESS = "preprocess"
    BATCH = "batch"
    STREAMING = "streaming"


class AlgorithmTypeSpecification:
    @classmethod
    def new_file(cls, type: AlgorithmType) -> str:
        match type:
            case AlgorithmType.PREPROCESS:
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
        match type:
            case AlgorithmType.PREPROCESS:
                template_file = "template_preprocess.py"
                directory = "preprocess"
            case AlgorithmType.BATCH:
                template_file = "template_batch.py"
                directory = "batch"
            case AlgorithmType.STREAMING:
                template_file = "template_streaming.py"
                directory = "streaming"
        template_path = TEMPLATES_DIRECTORY / template_file
        destination = ALGORITHMS_DIRECTORY / directory / cls.new_file(type)
        return template_path, destination


def edit_algorithm(option: str, type: AlgorithmType) -> None:
    if option == "new":
        template, destination = AlgorithmTypeSpecification.paths(type)
        new_file_path = shutil.copy(template, destination)
        open_file_in_editor(new_file_path)
    else:
        open_file_in_editor(Path(option))
