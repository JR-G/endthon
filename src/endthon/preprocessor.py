class EndthonPreprocessor:
    def __init__(self):
        self.indentation_level = 0
        self.indentation_stack = []

    def preprocess(self, endthon_code):
        lines = endthon_code.split('\n')
        processed_lines = []

        for line in lines:
            stripped_line = line.strip()

            if not stripped_line:
                processed_lines.append('')
                continue

            if stripped_line.startswith(('def ', 'if ', 'for ', 'while ', 'class ')):
                processed_lines.append(' ' * (4 * self.indentation_level) + stripped_line + ':')
                self.indentation_level += 1
                self.indentation_stack.append(stripped_line.split()[0])
            elif stripped_line.startswith('else'):
                self.indentation_level -= 1
                processed_lines.append(' ' * (4 * self.indentation_level) + stripped_line + ':')
                self.indentation_level += 1
            elif stripped_line == 'end':
                self.indentation_level -= 1
                if self.indentation_stack:
                    self.indentation_stack.pop()
            else:
                processed_lines.append(' ' * (4 * self.indentation_level) + stripped_line)

        return '\n'.join(processed_lines)


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
