import unittest
from decrypt import decrypt
class DecryptTestCase(unittest.TestCase):
    def test_group_one_dot(self):
        cases = [
            ("абра-кадабра.", "абра-кадабра"),
            (".", ""),
            ("1..2.3", "23"),
            ("абр......a.", "a"),
        ]
        for encrypted, expected in cases:
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decrypt(encrypted), expected)
    def test_group_two_dots(self):
        cases = [
            ("абраа..-кадабра", "абра-кадабра"),
            ("абраа..-.кадабра", "абра-кадабра"),
            ("абра--..кадабра", "абра-кадабра"),
        ]
        for encrypted, expected in cases:
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decrypt(encrypted), expected)
    def test_group_many_dots(self):
        cases = [
            ("абрау...-кадабра", "абра-кадабра"),
            ("абра........", ""),
            ("1.......................", ""),
        ]
        for encrypted, expected in cases:
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decrypt(encrypted), expected)
if __name__ == "__main__":
    unittest.main(verbosity=2)
