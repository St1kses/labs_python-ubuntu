import unittest
from datetime import datetime
from freezegun import freeze_time
from app import app
class HelloWorldEndpointTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
    @staticmethod
    def expected_weekday_genitive(date_str: str) -> str:
        weekday_map = {
            0: "понедельника",
            1: "вторника",
            2: "среды",
            3: "четверга",
            4: "пятницы",
            5: "субботы",
            6: "воскресенья",
        }
        return weekday_map[datetime.strptime(date_str, "%Y-%m-%d").weekday()]
    @freeze_time("2026-04-06")
    def test_can_get_correct_username_and_weekday(self):
        response = self.client.get("/hello-world/Саша")
        text = response.data.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Привет, Саша.", text)
        self.assertIn(f"Хорошей {self.expected_weekday_genitive('2026-04-06')}!", text)
    @freeze_time("2026-04-08")
    def test_username_that_looks_like_wish(self):
        response = self.client.get("/hello-world/Хорошей среды")
        text = response.data.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Привет, Хорошей среды.", text)
        self.assertIn("Хорошей среды!", text)
        self.assertNotIn("Хорошей пятницы!", text)
    @freeze_time("2026-04-12")
    def test_weekday_is_not_stuck(self):
        response = self.client.get("/hello-world/Ира")
        text = response.data.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Хорошей воскресенья!", text)
if __name__ == "__main__":
    unittest.main(verbosity=2)
