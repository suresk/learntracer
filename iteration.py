from event import IterationEvent


class Iteration:

    params = None
    metrics = None

    def __init__(self, run, number, fold=None):
        self.run = run
        self.number = number
        self.fold = fold

    def record(self, params={}, metrics={}):
        self.params = params
        self.metrics = metrics
        self.run.notify(IterationEvent(self.run, self.fold, self.metrics, self.params))
