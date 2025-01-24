import unittest
import os
import tempfile
from endthon.runner import main
import sys
from io import StringIO
from unittest.mock import patch

class TestRunner(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)
        
    def create_test_file(self, content):
        file_path = os.path.join(self.test_dir, 'test.epy')
        with open(file_path, 'w') as f:
            f.write(content)
        return file_path

    @patch('sys.stdout', new_callable=StringIO)
    def test_basic_program(self, mock_stdout):
        test_code = '''
def greet()
    print("Hello, World!")
end

greet()
'''
        file_path = self.create_test_file(test_code)
        with patch('sys.argv', ['endthon', file_path]):
            main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Hello, World!")

    @patch('sys.stdout', new_callable=StringIO)
    def test_if_else_program(self, mock_stdout):
        test_code = '''
x = 5
if x > 3
    print("Greater")
else
    print("Lesser")
end
'''
        file_path = self.create_test_file(test_code)
        with patch('sys.argv', ['endthon', file_path]):
            main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Greater")

    @patch('sys.stdout', new_callable=StringIO)
    def test_no_file_provided(self, mock_stdout):
        with patch('sys.argv', ['endthon']):
            main()
        self.assertIn("Usage: endthon <filename.epy>", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_file_not_found(self, mock_stdout):
        with patch('sys.argv', ['endthon', 'nonexistent.epy']):
            main()
        self.assertIn("Error: File 'nonexistent.epy' not found", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_syntax_error(self, mock_stdout):
        test_code = '''
def invalid_function()
    print("Missing end statement"
'''
        file_path = self.create_test_file(test_code)
        with patch('sys.argv', ['endthon', file_path]):
            main()
        self.assertIn("Error:", mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
