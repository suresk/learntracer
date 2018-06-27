import uuid
import time
from event import StartRunEvent, EndRunEvent, ErrorRunEvent
from errors import IllegalIterationState, IllegalFoldState


class Run:

    started = None
    ended = None
    duration = None
    error = None
    end_metrics = None
    end_metadata = None

    folds = {}
    iterations = {}

    def __init__(self, project, notifiers=[], run_type=None, params={}, metadata={}, description=None):
        self.project = project
        self.notifiers = notifiers
        self.run_type = run_type
        self.params = params
        self.metadata = metadata
        self.description = description

        self.run_id = uuid.uuid4()

    def start(self):
        self.started = time.time()
        self.notify(StartRunEvent(self))

    def finish(self, metrics={}, metadata={}):
        self.ended = time.time()
        self.duration = self.ended - self.started
        self.end_metrics = metrics
        self.end_metadata = metadata
        self.notify(EndRunEvent(self, metrics, metadata))

    def error(self, error):
        self.finish()
        self.error = error
        self.notify(ErrorRunEvent)

    def notify(self, event):

        if self.notifiers:
            for notifier in self.notifiers:
                notifier.notify(event)

    def add_fold(self, fold):

        if not fold.fold_number:
            raise IllegalFoldState('Fold number is required')

        if self.folds[fold.fold_number]:
            raise IllegalFoldState(f'Fold ({fold_number}) already exists on this run')

        self.folds[fold.fold_number] = fold

    def add_iteration(self, iteration):

        if self.folds and not iteration.fold:
            raise IllegalIterationState(f'This run declares folds, but the iteration does not include one')

        if self.folds and iteration.fold.fold_number not in self.folds:
            raise IllegalIterationState(f'This fold ({iteration.fold.fold_number}) is not in the list of folds for this run.')

        if not self.folds and iteration.fold:
            raise IllegalIterationState(f'This iteration declares a fold ({iteration.fold.fold_number}) but this run has none.')

        if iteration.fold:
            self.folds[iteration.fold.fold_number].add_iteration(iteration)
        else:
            if iteration.number in self.iterations:
                raise IllegalIterationState(f'{iteration.number} already exists for this run')
            self.iterations[iteration.number] = iteration
