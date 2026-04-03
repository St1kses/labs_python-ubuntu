import sys
class Redirect:
    def __init__(self, *, stdout=None, stderr=None):
        self._new_stdout = stdout
        self._new_stderr = stderr
        self._old_stdout = None
        self._old_stderr = None
    def __enter__(self):
        self._old_stdout = sys.stdout
        self._old_stderr = sys.stderr
        if self._new_stdout is not None:
            sys.stdout = self._new_stdout
        if self._new_stderr is not None:
            sys.stderr = self._new_stderr
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._new_stdout is not None:
            sys.stdout = self._old_stdout
        if self._new_stderr is not None:
            sys.stderr = self._old_stderr
        return False
