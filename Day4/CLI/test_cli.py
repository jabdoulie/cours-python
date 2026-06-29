import unittest
from cli_tool import greet  # Import the function to test

class TestCLI(unittest.TestCase):
    def test_greet(self):
        self.assertEqual(greet("Alice"), "Hello, Alice!")

if __name__ == "__main__":
    unittest.main()