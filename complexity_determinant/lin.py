from complexity_determinant import complexity

if __name__ == "__main__":
    determined_complexity = complexity.determine_from_files('lin', 'lin', 'lin')
    print(determined_complexity.complexity_info())
    print(determined_complexity.execution_time(10))
    print(determined_complexity.max_problem_size_for_time(10e-10))

data_structure = {
}

for i in range(90,100):
    data_structure[i] = list(range(1,i*50000))

def clean_function():
    return None

def tested_function(l):
    reversed(l)

class test:
    @staticmethod
    def tested_function(x):
        return x