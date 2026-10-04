import unittest
from app import add_numbers, validate_input

class TestAdditionApp(unittest.TestCase):

    def test_add_numbers_integers(self):
        self.assertEqual(add_numbers(3, 5), 8.0)

    def test_add_numbers_floats(self):
        self.assertEqual(add_numbers(3.5, 2.1), 5.6)

    def test_add_numbers_mixed(self):
        self.assertEqual(add_numbers(4, 6.5), 10.5)

    def test_validate_input_non_numeric(self):
        with self.assertRaises(ValueError):
            validate_input('abc')

    def test_validate_input_empty(self):
        with self.assertRaises(ValueError):
            validate_input('')

    def test_validate_input_special_characters(self):
        with self.assertRaises(ValueError):
            validate_input('$100')

    def test_add_numbers_negative(self):
        self.assertEqual(add_numbers(-7, -3), -10.0)

    def test_add_numbers_zero(self):
        self.assertEqual(add_numbers(0, 5), 5.0)

if __name__ == '__main__':
    unittest.main()