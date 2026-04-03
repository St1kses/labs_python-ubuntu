import unittest
from unittest.mock import patch
import datetime
from person import Person
from freezegun import freeze_time
class PersonTestCase(unittest.TestCase):
    def setUp(self):
        self.person = Person(name="Иван", year_of_birth=2000, address="Москва")
    @freeze_time("2026-01-01")
    def test_get_age(self):
        self.assertEqual(self.person.get_age(), 26)
    def test_get_name(self):
        self.assertEqual(self.person.get_name(), "Иван")
    def test_set_name(self):
        self.person.set_name("Петр")
        self.assertEqual(self.person.get_name(), "Петр")
    def test_set_address(self):
        self.person.set_address("Казань")
        self.assertEqual(self.person.get_address(), "Казань")
    def test_get_address(self):
        self.assertEqual(self.person.get_address(), "Москва")
    def test_is_homeless_false(self):
        self.assertFalse(self.person.is_homeless())
    def test_is_homeless_true_empty(self):
        p = Person(name="Аня", year_of_birth=1999, address="")
        self.assertTrue(p.is_homeless())
    def test_is_homeless_true_none(self):
        p = Person(name="Аня", year_of_birth=1999, address=None)
        self.assertTrue(p.is_homeless())
if __name__ == "__main__":
    unittest.main(verbosity=2)
