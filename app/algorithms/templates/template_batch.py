from server.logic.interfaces.batch_algorithm import BatchAlgorithm


# Change this class name to something unique and descriptive
class NewBatchAlgorithm(BatchAlgorithm):
    def __init__(self) -> None: ...

    def calculate_property(self, data): ...

    def submit_results(self): ...
