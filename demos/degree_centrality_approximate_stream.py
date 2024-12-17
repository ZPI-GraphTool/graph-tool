from algorithms._config.interfaces import ResultList, StreamingAlgorithm


class DegreeCentralityApproximateVersion(StreamingAlgorithm):
    def __init__(self) -> None:
        self.degrees = {}

    def on_edge_calculate(self, edge: tuple) -> None:
        vertex_start = edge[0]
        vertex_end = edge[1]

        if vertex_start not in self.degrees:
            self.degrees[vertex_start] = 0

        if vertex_end not in self.degrees:
            self.degrees[vertex_end] = 0

        self.degrees[vertex_start] = self.degrees[vertex_start] + 1
        self.degrees[vertex_end] = self.degrees[vertex_end] + 1

    def submit_results(self) -> ResultList:
        return list(self.degrees.items())
