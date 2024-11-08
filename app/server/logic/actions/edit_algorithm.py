import shutil
from enum import IntEnum
from pathlib import Path

from .open_file_in_editor import open_file_in_editor

ALGORITHMS_DIRECTORY = Path(__file__).parents[3] / "algorithms"
TEMPLATES_DIRECTORY = ALGORITHMS_DIRECTORY / "templates"


class AlgorithmType(IntEnum):
    PREPROCESS = -1
    BATCH = 0
    STREAMING = 1


class AlgorithmTypeSpec:
    counter = {
        AlgorithmType.PREPROCESS: 0,
        AlgorithmType.BATCH: 0,
        AlgorithmType.STREAMING: 0,
    }

    @classmethod
    def template(cls, type: AlgorithmType) -> Path:
        match type:
            case AlgorithmType.PREPROCESS:
                template_file = "template_preprocess.py"
            case AlgorithmType.BATCH:
                template_file = "template_batch.py"
            case AlgorithmType.STREAMING:
                template_file = "template_streaming.py"
        return TEMPLATES_DIRECTORY / template_file

    @classmethod
    def new_file_name(cls, type: AlgorithmType) -> str:
        match type:
            case AlgorithmType.PREPROCESS:
                prefix = "function"
            case AlgorithmType.BATCH | AlgorithmType.STREAMING:
                prefix = "algorithm"
        file_name = f"{prefix}_{cls.counter[type]}.py"
        cls.counter[type] += 1
        return file_name

    @classmethod
    def destination(cls, type: AlgorithmType) -> Path:
        match type:
            case AlgorithmType.PREPROCESS:
                directory = "preprocess"
            case AlgorithmType.BATCH:
                directory = "batch"
            case AlgorithmType.STREAMING:
                directory = "streaming"
        return ALGORITHMS_DIRECTORY / directory / cls.new_file_name(type)


def duplicate_file(file_path: Path, destination: Path) -> Path:
    return shutil.copy(file_path, destination)


def edit_algorithm(type: AlgorithmType) -> None:
    template = AlgorithmTypeSpec.template(type)
    destination = AlgorithmTypeSpec.destination(type)

    new_file_path = duplicate_file(template, destination)
    open_file_in_editor(new_file_path)
