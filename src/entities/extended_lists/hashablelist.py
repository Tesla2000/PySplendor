class hashablelist(list):
    def __hash__(self):
        return tuple(self).__hash__()
