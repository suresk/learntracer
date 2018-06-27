class IllegalFoldState(Exception):

    def __init__(self, reason):
        Exception.__init__(self, f'Illegal Fold State: {reason}')

class IllegalIterationState(Exception):

    def __init__(self, reason):
        Exception.__init__(self, f'Illegal Iteration State: {reason}')