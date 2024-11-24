from typing import Any, Sequence

from algorithms._config.interfaces import PreprocessEdge


# Change this class name to something unique and descriptive
class NewPreprocessingFunction(PreprocessEdge):
    def __init__(self) -> None: ...

    def create_edge_from(self, line: Any) -> Sequence | dict: ...

    def set_number_of_headers_to_ignore(self, lines_to_ignore: int) -> None: ...
