from typing import Any, Sequence

from algorithms._config.interfaces import PreprocessEdge


class ConnectionPreprocess(PreprocessEdge):
    def __init__(self) -> None: ...

    def create_edge_from(self, line: Any) -> Sequence | dict:
        return (line["start_stop"], line["end_stop"])

    # this does not make sense
    def set_number_of_headers_to_ignore(self, lines_to_ignore: int = 1):
        ...
        # return super().set_number_of_headers_to_ignore(lines_to_ignore)
