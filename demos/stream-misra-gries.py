from typing import Any, Sequence

from algorithms._config.interfaces import StreamingAlgorithm, numeric



class MisraAlgorithm(StreamingAlgorithm):
    def __init__(self) -> None: 
        self.results = {}
        self.k = 20
        

    def on_edge_calculate(self, edge: Sequence | dict) -> None:
        
        vertex_start = edge[0]
        vertex_end = edge[1]

        for vertex in [vertex_start, vertex_end]:
            if vertex in self.results:
                self.results[vertex] += 1
            elif len(self.results) < (self.k -1):
                self.results[vertex] = 1
            else:
                for vertex_in_results in list(self.results.keys()):
                    self.results[vertex_in_results] -= 1
                    if self.results[vertex_in_results] == 0:
                        self.results.pop(vertex_in_results, None)
                        
        

    def submit_results(self) -> list[tuple[Any, numeric]]: 
        return self.results.items()