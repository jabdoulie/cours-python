import unittest
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

class TestMath(unittest.TestCase):
    def test_divide(self):
        with self.assertRaises(ValueError):
            divide(10, 0)  # ✅ Expected Error

if __name__ == "__main__":
    unittest.main()