from event import StartRunEvent, EndRunEvent, StartFoldEvent, EndFoldEvent, IterationEvent, ErrorEvent
import csv
import os


class Notifier:

    def __init__(self, start_run=False, end_run=False, start_fold=None, end_fold=False, iterations=None, errors=False):
        self.start_run = start_run
        self.end_run = end_run
        self.start_fold = start_fold
        self.end_fold = end_fold
        self.iterations = iterations
        self.errors = errors

    def should_notify(self, event):

        notify = False

        if isinstance(event, StartRunEvent) and self.start_run:
            notify = True
        elif isinstance(event, EndRunEvent) and self.end_run:
            notify = True
        elif isinstance(event, StartFoldEvent) and self.start_fold:
            notify = True
        elif isinstance(event, EndFoldEvent) and self.end_fold:
            notify = True
        elif isinstance(event, IterationEvent) and \
                (self.iterations or (isinstance(self.iterations, int) and event.iterations % self.iterations == 0)):
            notify = True
        elif isinstance(event, ErrorEvent) and self.errors:
            notify = True

        return notify

    def notify(self, event):

        if self.should_notify(event):
            self.__notify(event)

    def _notify(self, event):
        pass


class CSVNotifier:

    def __init__(self, run, basedir, run_file='learn-{project_name}-runs.csv',
                 folds_file='learn-{project_name}-{run_id}-folds.csv',
                 iterations_file='learn-{project_name}-{run_id}-iterations.csv', iterations=100,
                 delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL):
        Notifier.__init__(self, end_run=True, end_fold=True, errors=True, iterations=iterations)
        self.run = run
        self.basedir = basedir
        self.run_file = run_file
        self.folds_file = folds_file
        self.iterations_file = iterations_file

        self.delimiter = delimiter
        self.quotechar = quotechar
        self.quoting = quoting

    def _notify(self, event):

        if isinstance(event, EndRunEvent) and self.run_file:
            self.write_run(event)

    def write_run(self, event):
        run_file_path = self.__run_file_name(self.run.run_id)
        if os.path.exists(run_file_path):
            with open(self.__run_file_name(self.run.run_id), 'a') as csvfile:
                reader = csv.reader(csvfile, delimiter=self.delimiter, quotechar=self.quotechar)
                header = next(reader, None)

                rows = []

                if header:
                    rows.append(self.__get_column_values(header))
                else:
                    cols = self.__get_column_names()
                    rows.append(cols)
                    rows.append(self.__get_column_values(cols))

                writer = csv.writer(csvfile, delimiter=self.delimiter, quotechar=self.quotechar,
                                    quoting=self.quoting)
                for row in rows:
                    writer.writerow(row)
        else:
            with open(self.__run_file_name(self.run.run_id), 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter = self.delimiter, quotechar = self.quotechar, quoting=self.quoting)
                cols = self.__get_column_names()
                writer.writerow(cols)
                writer.writerow(self.__get_column_values(cols))

    def __get_column_names(self):
        cols = ['project_name', 'run_id', 'run_type', 'description', 'started', 'ended', 'duration-seconds']

        for p in self.run.params:
            cols.append(f'param-{p}')

        for meta in self.run.metadata:
            cols.append(f'meta-{meta}')

        for emeta in self.run.end_metadata:
            cols.append(f'end-meta-{emeta}')

        for metric in self.run.end_metrics:
            cols.append(f'metric-{metric}')

        return cols

    def __get_column_values(self, columns):
        values = [self.run.project.name, self.run.run_id, self.run.run_type, self.run.started, self.run.ended, self.run.duration]

        for col in columns:

            if col.startswith('param-'):
                values.append(self.run.params[col.replace('param-', '')])
            elif col.startswith('meta-'):
                values.append(self.run.metadata[col.replace('meta-', '')])
            elif col.startswith('end-meta-'):
                values.append(self.run.end_metadata[col.replace('end-meta-', '')])
            elif col.startswith('metric-'):
                values.append(self.run.end_metrics[col.replace('metric-', '')])
            elif col is 'project_name':
                values.append(self.run.project.name)
            elif col is 'run_id':
                values.append(self.run.run_id)
            elif col is 'run_type':
                values.append(self.run.run_type)
            elif col is 'description':
                values.append(self.run.description)
            elif col is 'started':
                values.append(self.run.started)
            elif col is 'ended':
                values.append(self.run.ended)
            elif col is 'duration':
                values.append(self.run.duration)

            return values

    def __run_file_name(self, run_id):
        path = os.path(self.basedir)
        return os.path.join(path, self.run_file.format(project_name = self.run.project.name, run_id = run_id))


class JSONNotifier:
    pass


class SlackNotifier:
    pass
