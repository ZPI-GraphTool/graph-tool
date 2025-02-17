from algorithms._config.interfaces import ResultList, StreamingAlgorithm


class DegreeCentralityAccurateVersion(StreamingAlgorithm):
    def __init__(self) -> None:
        self.degrees = {}
        self.results = {}

    def on_edge_calculate(self, edge: tuple) -> None:
        vertex_start = edge[0]
        vertex_end = edge[1]

        if vertex_start not in self.degrees:
            self.degrees[vertex_start] = 0

        if vertex_end not in self.degrees:
            self.degrees[vertex_end] = 0

        if vertex_start not in self.results:
            self.results[vertex_start] = 0

        if vertex_end not in self.results:
            self.results[vertex_end] = 0

        number_of_nodes = len(self.degrees.keys())
        self.degrees[vertex_start] = self.degrees[vertex_start] + 1
        self.degrees[vertex_end] = self.degrees[vertex_end] + 1

        for k, v in self.results.items():
            self.results[k] = self.degrees[k] / (number_of_nodes - 1)

    def submit_results(self) -> ResultList:
        return list(self.results.items())
