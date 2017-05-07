import argparse
from complexity_determinant import complexity, logger

def run():
    """Command-line interface function"""
    # Parsing arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('data',
                        help='Must contain a dictionary called data_structure (size: problem)')
    parser.add_argument('test',
                        help='Must contain a function called tested_function, or a class with it')
    parser.add_argument('clean', help='Must contain a function called clean_function')
    parser.add_argument('-t', '--timeout', type=int, default=30,
                        help='Max execution time [s]')

    args = parser.parse_args()
    logger.Logger.minimum_log_level = logger.LoggingLevel.WARN
    determined_complexity = complexity.determine_from_files(args.data, args.test, args.clean, args.timeout)
    print(determined_complexity)

# Loaded directly
if __name__ == "__main__":
    run()
