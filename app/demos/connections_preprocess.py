from typing import Any, Sequence

from server.logic.interfaces import PreprocessEdge


class ConnectionPreprocess(PreprocessEdge):
    def __init__(self) -> None: ...

    def create_edge_from(self, line: Any) -> Sequence | dict:
        print("Called create edge")
        return ("", "")

    # this does not make sense
    def set_number_of_headers_to_ignore(self, lines_to_ignore: int = 1):
        ...
        # return super().set_number_of_headers_to_ignore(lines_to_ignore)
