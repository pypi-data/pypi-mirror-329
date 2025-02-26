import unittest
from starco_utility import StarcoUtility

class TestStarcoUtility(unittest.TestCase):
    def setUp(self):
        self.utility = StarcoUtility()

    def test_basic_functionality(self):
        result = self.utility.process_data("test_input")
        self.assertIsNotNone(result)
        
    def test_data_validation(self):
        valid_data = {"key": "value"}
        self.assertTrue(self.utility.validate_data(valid_data))
        
        invalid_data = None
        self.assertFalse(self.utility.validate_data(invalid_data))
        
    def test_error_handling(self):
        with self.assertRaises(ValueError):
            self.utility.process_data(None)
            
    def test_data_transformation(self):
        input_data = [1, 2, 3]
        expected_output = [2, 4, 6]
        result = self.utility.transform_data(input_data)
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()
