import argparse
from complexity_determinant import ComplexityDeterminant
import importlib

def run():
    # Parsing arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('data',
                        help='Must contain a dictionary called data_structure (size: problem)')
    parser.add_argument('test',
                        help='Must contain a function called tested_function, or a class with it')
    parser.add_argument('clean', help='Must contain a function called clean_function')
    parser.add_argument('-t', '--timeout', type=int, default=30,
                        help='Max execution time [s]')
    parser.add_argument('-st', '--single_timeout', type=int, default=10,
                        help='Max execution time for one problem [s]')

    args = parser.parse_args()

    ComplexityDeterminant.TOTAL_TIMEOUT = args.timeout
    ComplexityDeterminant.SINGLE_TIMEOUT = args.single_timeout
    complexity_determinant = ComplexityDeterminant.from_files(args.data, args.test, args.clean)
    if complexity_determinant is None:
        return
    else:
        complexity = complexity_determinant.complexity
        print(complexity)

# Loaded directly
if __name__ == "__main__":
    run()
