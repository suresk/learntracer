from iteration import Iteration


class LightGBMRecorder:

    def __init__(self, run, fold):
        self.run = run
        self.fold = fold

    def callback(self, env):
        iteration = Iteration(self.run, env.iteration, self.fold)

        metrics = []

        for m in env.metrics:
            metric = {}
            metric.name = m[0]
            metric.type = m[1]
            metric.value = m[2]
            metrics.append(metric)

        iteration.record(env.params, metrics)

        self.run.add_iteration(iteration)
