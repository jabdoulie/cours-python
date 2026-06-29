import unittest
from unittest.mock import patch
from cli_tool import greet_interactive  # Function that uses input()

class TestCLIInteractive(unittest.TestCase):
    @patch("builtins.input", return_value="Alice")  # Simulate user input
    def test_greet_input(self, mock_input):
        self.assertEqual(greet_interactive(), "Hello, Alice!")
        
if __name__ == "__main__":
    unittest.main()