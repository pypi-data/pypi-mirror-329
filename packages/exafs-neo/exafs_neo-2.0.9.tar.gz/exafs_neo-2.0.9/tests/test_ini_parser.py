import unittest

from exafs_neo.ini_parser import optional_var


class TestValidator(unittest.TestCase):
    def test_optional_var(self):

        input_dict = {}
        selection_options = optional_var(input_dict, 'file', 0, int)
        self.assertEqual(input_dict['file'], 0)

    def test_optional_type(self):
        input_dict = {}
        selection_options = optional_var(input_dict, 'file', 0, int)
        self.assertIsInstance(input_dict['file'], int)




if __name__ == '__main__':
    unittest.main()
