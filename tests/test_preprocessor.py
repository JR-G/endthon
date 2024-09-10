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
    print(f"Hello, {name}!")"""
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
    print("Hello, World!")"""
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
                break"""
        self.assertEqual(self.preprocessor.preprocess(endthon_code).strip(), expected_python_code.strip())

    def test_multiline_statements(self):
        endthon_code = """
def long_function(arg1,
                  arg2,
                  arg3)
    print("This is a long function")
end

if (condition1 and
    condition2 and
    condition3)
    print("Complex condition")
end
"""
        expected_python_code = """
def long_function(arg1, arg2, arg3):
    print("This is a long function")

if (condition1 and condition2 and condition3):
    print("Complex condition")"""
        self.assertEqual(self.preprocessor.preprocess(endthon_code).strip(), expected_python_code.strip())

    def test_preserve_comments_and_empty_lines(self):
        endthon_code = """
# This is a comment
def function()
    # This is an indented comment
    print("Hello")

    # Another comment
end
# Final comment
"""
        expected_python_code = """
# This is a comment
def function():
    # This is an indented comment
    print("Hello")

    # Another comment
# Final comment"""
        self.assertEqual(self.preprocessor.preprocess(endthon_code).strip(), expected_python_code.strip())

    def test_try_except_finally(self):
        endthon_code = """
try
    risky_operation()
except ValueError
    handle_value_error()
except KeyError
    handle_key_error()
else
    no_error_occurred()
finally
    cleanup()
end
"""
        expected_python_code = """
try:
    risky_operation()
except ValueError:
    handle_value_error()
except KeyError:
    handle_key_error()
else:
    no_error_occurred()
finally:
    cleanup()"""
        self.assertEqual(self.preprocessor.preprocess(endthon_code).strip(), expected_python_code.strip())

if __name__ == '__main__':
    unittest.main()
