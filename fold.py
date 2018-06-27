import time
from event import StartFoldEvent, EndFoldEvent
from errors import IllegalIterationState


class Fold:

    started = None
    metrics = None
    ended = None
    duration = None
    metadata = None
    iterations = []

    def __init__(self, run, fold_number, total_folds):
        self.run = run
        self.fold_number = fold_number
        self.total_folds = total_folds

    def start(self):
        self.started = time.time()
        self.run.notify(StartFoldEvent(self.run, self))

    def end(self, metrics={}, metadata={}):
        self.metrics = metrics
        self.metadata = metadata
        self.ended = time.time()
        self.duration = self.ended - self.started

        self.run.notify(EndFoldEvent(self.run, self, metrics, metadata))

    def add_iteration(self, iteration):
        if iteration.number in self.iterations:
            raise IllegalIterationState(f'{iteration.number} already exists for this run')
        self.iterations[iteration.number] = iteration
