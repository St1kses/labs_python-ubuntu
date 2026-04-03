import unittest
from block_errors import BlockErrors
class BlockErrorsTestCase(unittest.TestCase):
    def test_ignored_zero_division(self):
        with BlockErrors({ZeroDivisionError}):
            _ = 1 / 0
        self.assertTrue(True)
    def test_propagates_type_error(self):
        with self.assertRaises(TypeError):
            with BlockErrors({ZeroDivisionError}):
                _ = 1 / "0"
    def test_nested_outer_type_catches_inner_type_error(self):
        with BlockErrors({TypeError}):
            with BlockErrors({ZeroDivisionError}):
                _ = 1 / "0"
    def test_child_exception_ignored_by_exception(self):
        with BlockErrors({Exception}):
            _ = 1 / "0"
        self.assertTrue(True)
if __name__ == "__main__":
    unittest.main(verbosity=2)
