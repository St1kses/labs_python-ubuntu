class BlockErrors:
    def __init__(self, err_types):
        self.err_types = set(err_types)
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return False
        for allowed in self.err_types:
            if issubclass(exc_type, allowed):
                return True
        return False
