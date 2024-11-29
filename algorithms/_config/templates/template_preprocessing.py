from typing import Any, Sequence

from algorithms._config.interfaces import PreprocessEdge


# Change this class name to something unique and descriptive
class NewPreprocessingFunction(PreprocessEdge):
    def __init__(self) -> None: ...

    def create_edge_from(self, line: Any) -> Sequence | dict: ...
