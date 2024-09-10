import unittest
from src.endthon.preprocessor import EndthonPreprocessor

class TestEndthonPreprocessor(unittest.TestCase):
    def setUp(self):
        self.preprocessor = EndthonPreprocessor()

    def test_simple_function(self):
        endthon_code = """
def greet(name)
    print(f"Hello, {name}!")
end
"""
        expected_python_code = """
def greet(name):
    print(f"Hello, {name}!")
"""
        self.assertEqual(self.preprocessor.preprocess(endthon_code).strip(), expected_python_code.strip())

    def test_if_else_statement(self):
        endthon_code = """
if name
    print(f"Hello, {name}!")
else
    print("Hello, World!")
end
"""
        expected_python_code = """
if name:
    print(f"Hello, {name}!")
else:
    print("Hello, World!")
"""
        self.assertEqual(self.preprocessor.preprocess(endthon_code).strip(), expected_python_code.strip())

    def test_nested_statements(self):
        endthon_code = """
def outer()
    if condition
        for item in items
            print(item)
        end
    else
        while True
            print("Looping")
            if done
                break
            end
        end
    end
end
"""
        expected_python_code = """
def outer():
    if condition:
        for item in items:
            print(item)
    else:
        while True:
            print("Looping")
            if done:
                break
"""
        self.assertEqual(self.preprocessor.preprocess(endthon_code).strip(), expected_python_code.strip())

if __name__ == '__main__':
    unittest.main()
