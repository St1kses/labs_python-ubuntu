import unittest
from app import app, finance_storage
class FinanceEndpointsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
    def setUp(self):
        finance_storage.clear()
        finance_storage.update({
            2024: {1: 100, 2: 200},
            2025: {3: 300},
        })
    def test_add_existing_month(self):
        response = self.client.get("/add/20240115/50")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(finance_storage[2024][1], 150)
    def test_add_new_month(self):
        response = self.client.get("/add/20240401/700")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(finance_storage[2024][4], 700)
    def test_add_new_year(self):
        response = self.client.get("/add/20270101/900")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(finance_storage[2027][1], 900)
    def test_calculate_year_success(self):
        response = self.client.get("/calculate/2024")
        text = response.data.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("300", text)
    def test_calculate_year_no_year_data(self):
        response = self.client.get("/calculate/2030")
        text = response.data.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("0", text)
    def test_calculate_year_empty_storage(self):
        finance_storage.clear()
        response = self.client.get("/calculate/2030")
        text = response.data.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("0", text)
    def test_calculate_month_success(self):
        response = self.client.get("/calculate/2025/3")
        text = response.data.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("300", text)
    def test_calculate_month_absent_data(self):
        response = self.client.get("/calculate/2025/12")
        text = response.data.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("0", text)
    def test_calculate_month_empty_storage(self):
        finance_storage.clear()
        response = self.client.get("/calculate/2030/1")
        text = response.data.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("0", text)
    def test_add_invalid_date(self):
        response = self.client.get("/add/not_a_date/100")
        self.assertNotEqual(response.status_code, 200)
if __name__ == "__main__":
    unittest.main(verbosity=2)

