from server.logic.interfaces import StreamingAlgorithm


# Change this class name to something unique and descriptive
class NewStreamingAlgorithmo(StreamingAlgorithm):
    def __init__(self) -> None: ...

    def on_edge_calculate(self, edge): ...

    def submit_results(self): ...
