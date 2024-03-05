class hashabledict(dict):
    def __hash__(self):
        return tuple(self.items()).__hash__()
