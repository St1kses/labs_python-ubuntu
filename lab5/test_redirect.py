import io
import sys
import unittest
import traceback
from redirect_streams import Redirect
class RedirectTestCase(unittest.TestCase):
    def test_redirect_stdout_only(self):
        buf = io.StringIO()
        old = sys.stdout
        with Redirect(stdout=buf):
            print("x")
        self.assertIs(sys.stdout, old)
        self.assertIn("x", buf.getvalue())
    def test_redirect_stderr_traceback(self):
        out_buf = io.StringIO()
        err_buf = io.StringIO()
        with Redirect(stdout=out_buf, stderr=err_buf):
            try:
                raise Exception("Hello stderr.txt")
            except Exception:
                sys.stderr.write(traceback.format_exc())
        self.assertIn("Hello stderr.txt", err_buf.getvalue())
if __name__ == "__main__":
    unittest.main(verbosity=2)
