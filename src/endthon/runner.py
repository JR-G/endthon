from endthon.preprocessor import EndthonPreprocessor
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: endthon <filename.epy>")
        return

    input_file = sys.argv[1]
    
    preprocessor = EndthonPreprocessor()
    
    try:
        with open(input_file, 'r') as f:
            endthon_code = f.read()
        
        python_code = preprocessor.preprocess(endthon_code)
        
        exec(python_code)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()
