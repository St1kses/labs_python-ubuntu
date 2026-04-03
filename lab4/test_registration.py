import unittest
from app import app
class RegistrationValidationTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
    def valid_payload(self):
        return {
            "email": "user@example.com",
            "phone": 9991234567,
            "name": "Ivan",
            "address": "Moscow",
            "index": 101000,
            "comment": "ok",
        }
    def test_email_valid(self):
        payload = self.valid_payload()
        response = self.client.post("/registration", data=payload)
        self.assertEqual(response.status_code, 200)
    def test_email_invalid(self):
        payload = self.valid_payload()
        payload["email"] = "not-an-email"
        response = self.client.post("/registration", data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.get_json())
    def test_phone_valid(self):
        payload = self.valid_payload()
        response = self.client.post("/registration", data=payload)
        self.assertEqual(response.status_code, 200)
    def test_phone_short_invalid(self):
        payload = self.valid_payload()
        payload["phone"] = 12345
        response = self.client.post("/registration", data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("phone", response.get_json())
    def test_phone_negative_invalid(self):
        payload = self.valid_payload()
        payload["phone"] = -9991234567
        response = self.client.post("/registration", data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("phone", response.get_json())
    def test_name_valid(self):
        payload = self.valid_payload()
        response = self.client.post("/registration", data=payload)
        self.assertEqual(response.status_code, 200)
    def test_name_required_invalid(self):
        payload = self.valid_payload()
        payload.pop("name")
        response = self.client.post("/registration", data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.get_json())
    def test_address_valid(self):
        payload = self.valid_payload()
        response = self.client.post("/registration", data=payload)
        self.assertEqual(response.status_code, 200)
    def test_address_required_invalid(self):
        payload = self.valid_payload()
        payload.pop("address")
        response = self.client.post("/registration", data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("address", response.get_json())
    def test_index_valid(self):
        payload = self.valid_payload()
        response = self.client.post("/registration", data=payload)
        self.assertEqual(response.status_code, 200)
    def test_index_required_invalid(self):
        payload = self.valid_payload()
        payload.pop("index")
        response = self.client.post("/registration", data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("index", response.get_json())
    def test_comment_optional_present(self):
        payload = self.valid_payload()
        payload["comment"] = "hello"
        response = self.client.post("/registration", data=payload)
        self.assertEqual(response.status_code, 200)
    def test_comment_optional_absent(self):
        payload = self.valid_payload()
        payload.pop("comment")
        response = self.client.post("/registration", data=payload)
        self.assertEqual(response.status_code, 200)
if __name__ == "__main__":
    unittest.main(verbosity=2)
