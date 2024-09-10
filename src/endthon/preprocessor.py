class EndthonPreprocessor:
    def __init__(self):
        self.indentation_level = 0
        self.block_stack = []
        self.multiline_buffer = []
        self.in_multiline = False

    def preprocess(self, endthon_code):
        lines = endthon_code.split('\n')
        processed_lines = []
        self.indentation_level = 0
        self.block_stack = []

        for line in lines:
            stripped_line = line.strip()

            if not stripped_line or stripped_line.startswith('#'):
                processed_lines.append(line)
                continue

            if self.in_multiline:
                self.multiline_buffer.append(stripped_line)
                if ')' in stripped_line:
                    self.in_multiline = False
                    processed_lines.append(self.process_multiline())
                continue

            if stripped_line == 'end':
                if self.block_stack:
                    self.indentation_level = self.block_stack.pop()
                continue

            if stripped_line.startswith(('def ', 'if ', 'for ', 'while ', 'class ')):
                if '(' in stripped_line and ')' not in stripped_line:
                    self.in_multiline = True
                    self.multiline_buffer = [stripped_line]
                    continue
                parts = stripped_line.split(' ', 1)
                condition = parts[1]
                processed_lines.append(self.add_indentation(f"{parts[0]} {condition}:"))
                self.block_stack.append(self.indentation_level)
                self.indentation_level += 1
            elif stripped_line == 'try':
                processed_lines.append(self.add_indentation('try:'))
                self.block_stack.append(self.indentation_level)
                self.indentation_level += 1
            elif stripped_line.startswith(('elif ', 'else', 'except ', 'finally')):
                if self.block_stack:
                    self.indentation_level = self.block_stack[-1]
                processed_lines.append(self.add_indentation(f"{stripped_line}:"))
                self.indentation_level += 1
            else:
                processed_lines.append(self.add_indentation(stripped_line))

        return '\n'.join(processed_lines)

    def process_multiline(self):
        joined_line = ' '.join(self.multiline_buffer).replace('\n', '')
        parts = joined_line.split(' ', 1)
        processed_line = self.add_indentation(f"{parts[0]} {parts[1]}:")
        self.block_stack.append(self.indentation_level)
        self.indentation_level += 1
        return processed_line

    def add_indentation(self, line):
        return ' ' * (4 * self.indentation_level) + line

def preprocess_file(input_file, output_file):
    with open(input_file, 'r') as f:
        endthon_code = f.read()

    preprocessor = EndthonPreprocessor()
    python_code = preprocessor.preprocess(endthon_code)

    with open(output_file, 'w') as f:
        f.write(python_code)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print('Usage: python preprocessor.py input_file.epy output_file.py')
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    preprocess_file(input_file, output_file)
    print(f'Preprocessed {input_file} and saved results to {output_file}')
