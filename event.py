import time


class Event:
    event_time = time.time()

    def __init__(self, run):
        self.run = run


class RunEvent(Event):
    pass


class ErrorEvent(Event):
    pass


class FoldEvent(Event):
    pass


class IterationEvent(Event):
    pass


class StartRunEvent(RunEvent):

    def __init__(self, run):
        Event.__init__(self, run)


class EndRunEvent(RunEvent):

    def __init__(self, run, metrics={}, metadata={}):
        Event.__init__(self, run)
        self.metrics = metrics
        self.metadata = metadata


class ErrorRunEvent(RunEvent, ErrorEvent):

    def __init__(self, run, error):
        Event.__init__(self, run)
        self.error = error


class StartFoldEvent(FoldEvent):

    def __init__(self, run, fold):
        Event.__init__(self, run)
        self.fold = fold


class EndFoldEvent(FoldEvent):

    def __init__(self, run, fold, metrics={}, metadata={}):
        Event.__init__(self, run)
        self.fold = fold
        self.metrics = metrics
        self.metadata = metadata


class IterationEvent(IterationEvent):

    def __init__(self, run, fold=None, metrics={}, params={}):
        Event.__init__(self, run)
        self.fold = fold
        self.metrics = metrics
        self.params = params
