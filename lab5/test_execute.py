import inspect
import unittest
from app import app
class ExecuteEndpointTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
    def test_shell_true_not_used(self):
        src = inspect.getsource(app.view_functions["execute_code"])
        self.assertNotIn("shell=True", src)
    def test_valid_code_returns_output(self):
        response = self.client.post(
            "/execute",
            data={"code": "print(1+1)", "timeout": 5},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("2", response.data.decode("utf-8"))
def test_timeout(self):
    response = self.client.post(
        "/execute",
        data={"code": "__import__('time').sleep(10)", "timeout": 1},
    )
    self.assertEqual(response.status_code, 408)
    self.assertIn("не уложилось", response.data.decode("utf-8"))
    def test_invalid_form(self):
        response = self.client.post("/execute", data={})
        self.assertEqual(response.status_code, 400)
if __name__ == "__main__":
    unittest.main(verbosity=2)
