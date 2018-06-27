import uuid


class Project:

    def __init__(self, name, project_id=None):

        if id is None:
            self.project_id = uuid.uuid4()
        else:
            self.project_id = project_id

        self.name = name
