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
            processed_line = self.process_line(line)
            if processed_line is not None:
                processed_lines.append(processed_line)

        return '\n'.join(processed_lines)

    def process_line(self, line):
        stripped_line = line.strip()

        if not stripped_line or stripped_line.startswith('#'):
            return line

        if self.in_multiline:
            return self.handle_multiline(stripped_line)

        if stripped_line == 'end':
            self.handle_end()
            return None

        return self.handle_regular_line(stripped_line)

    def handle_multiline(self, line):
        self.multiline_buffer.append(line)
        if ')' in line:
            self.in_multiline = False
            return self.process_multiline()
        return None

    def handle_end(self):
        if self.block_stack:
            self.indentation_level = self.block_stack.pop()

    def handle_regular_line(self, line):
        if line.startswith(('def ', 'if ', 'for ', 'while ', 'class ')):
            return self.handle_block_start(line)
        elif line == 'try':
            return self.handle_block_start(line)
        elif line.startswith(('elif ', 'else', 'except ', 'finally')):
            return self.handle_conditional_block(line)
        else:
            return self.add_indentation(line)

    def handle_block_start(self, line):
        if '(' in line and ')' not in line:
            self.in_multiline = True
            self.multiline_buffer = [line]
            return None
        processed_line = self.add_indentation(f"{line}:")
        self.increase_indent()
        return processed_line

    def handle_conditional_block(self, line):
        if self.block_stack:
            self.indentation_level = self.block_stack[-1]
        processed_line = self.add_indentation(f"{line}:")
        self.increase_indent()
        return processed_line

    def process_multiline(self):
        joined_line = ' '.join(self.multiline_buffer).replace('\n', '')
        processed_line = self.add_indentation(f"{joined_line}:")
        self.increase_indent()
        self.multiline_buffer = []
        return processed_line

    def increase_indent(self):
        self.block_stack.append(self.indentation_level)
        self.indentation_level += 1

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
