from complexity_determinant import complexity

if __name__ == "__main__":
    determined_complexity = complexity.determine_from_files(
        'sqr',
        'sqr',
        'sqr')
    print(determined_complexity.complexity_info())
    print(determined_complexity.execution_time(1000))
    print(determined_complexity.max_problem_size_for_time(1000))


data_structure = {
}

for i in range(40, 60):
    data_structure[i] = list(range(1, i*100))


def clean_function():
    return None


def tested_function(l):
    for i in l:
        for j in l:
            i*j


class test:
    @staticmethod
    def tested_function(x):
        return x
