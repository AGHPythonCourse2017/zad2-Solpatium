import random
from complexity_determinant import complexity

if __name__ == "__main__":
    determined_complexity = complexity.determine_from_files('log', 'log', 'log')
    print(determined_complexity.complexity_info())
    print(determined_complexity.execution_time(1000))
    print(determined_complexity.max_problem_size_for_time(1000))

data_structure = {
}

for i in range(1,10):
    data_structure[i] = [random.randint(0,100000) for x in range(i*100000)]

def clean_function():
    return None

def tested_function(l):
    sorted(l)

class test:
    @staticmethod
    def tested_function(x):
        return x