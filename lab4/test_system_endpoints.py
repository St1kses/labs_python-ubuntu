import unittest
from app import app
class SystemEndpointsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
    def test_uptime_returns_text(self):
        response = self.client.get("/uptime")
        text = response.data.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Current uptime is", text)
    def test_ps_with_valid_args(self):
        response = self.client.get("/ps?arg=a&arg=u&arg=x")
        text = response.data.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("<pre>", text)
    def test_ps_with_invalid_arg(self):
        response = self.client.get("/ps?arg=;rm -rf /")
        self.assertEqual(response.status_code, 400)
if __name__ == "__main__":
    unittest.main(verbosity=2)
