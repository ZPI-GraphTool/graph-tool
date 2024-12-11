from typing import Any, Sequence

from algorithms._config.interfaces import PreprocessEdge


class ConnectionPreprocessing(PreprocessEdge):
    def __init__(self) -> None: ...

    def create_edge_from(self, line: Any) -> Sequence | dict:
        # The edge is a dictionary. Its keys are the headers of the supplied .csv file.
        return (line["start_stop"], line["end_stop"])
