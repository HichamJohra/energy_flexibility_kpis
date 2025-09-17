from copy import deepcopy

class Definition:
    def __init__(self):
        pass

    def info(self) -> str:
        return str(self)

    def copy(self):
        return deepcopy(self)