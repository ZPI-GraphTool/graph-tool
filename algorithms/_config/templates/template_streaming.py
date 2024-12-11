from typing import Any, Sequence

from algorithms._config.interfaces import StreamingAlgorithm, numeric


# Change this class name to something unique and descriptive
class NewStreamingAlgorithm(StreamingAlgorithm):
    def __init__(self) -> None: 
        ...

    def on_edge_calculate(self, edge: Sequence | dict) -> None: 
        ...

    def submit_results(self) -> list[tuple[Any, numeric]]: 
        ...
