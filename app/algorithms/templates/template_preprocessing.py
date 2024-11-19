from server.logic.interfaces import PreprocessEdge


# Change this class name to something unique and descriptive
class NewPreprocessingFunction(PreprocessEdge):
    def __init__(self) -> None: ...

    def create_edge_from(self, line): ...

    def set_number_of_headers_to_ignore(self, lines_to_ignore): ...
